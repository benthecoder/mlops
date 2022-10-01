# mlflow notes

- [mlflow notes](#mlflow-notes)
  - [run mlflow](#run-mlflow)
  - [Code](#code)
    - [Setup](#setup)
    - [Experiment](#experiment)
    - [Logging](#logging)
    - [load model](#load-model)
    - [Download artifacts](#download-artifacts)
    - [model registry](#model-registry)
  - [what model log saves](#what-model-log-saves)

## run mlflow

1. create env `conda create -n mlflow_env python=3.9`
2. `pip install -r requirements.txt`
3. run mlflow and configure backend `mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root artifacts`

[setup mlflow on aws rds](https://github.com/DataTalksClub/mlops-zoomcamp/blob/main/02-experiment-tracking/mlflow_on_aws.md)

## Code

### Setup

The MlflowClient object allows us to interact with...

- an MLflow Tracking Server that creates and manages experiments and runs.
- an MLflow Registry Server that creates and manages registered models and model versions.

```py
from mlflow.tracking import MlflowClient

MLFLOW_TRACKING_URI = "sqlite:///mlflow.db"
client = MlflowClient(MLFLOW_TRACKING_URI)
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

```

### Experiment

```py
client.list_experiments()
client.create_experiment("my_experiment")
mlflow.set_experiment("my_experiment")
```

### Logging

```py
mlflow.set_tag("model", "model_name")
mlflow.log_param("param_name", param)
mlflow.log_metric("metric_name", metric)

# log model options
# 1
mlflow.log_artifact(local_path = "path/to/model", artifact_path="models")

# 2
mlflow.<framework>.log_model(model, artifat_path="models")

mlflow.xgboost.autolog()
mlflow.sklearn.autolog()

# log preprocessor
dv = DictVectorizer()
with open("models/preprocessor.b", "wb") as f_out:
    pickle.dump(dv, f_out)

mlflow.log_artifact("models/preprocessor.b", artifact_path = "preprocessor")

```

### load model

```py
logged_model = 'runs:/run_id/models_mlflow'

# Load model as a PyFuncModel.
loaded_model = mlflow.pyfunc.load_model(logged_model)

# load as xgboost object
xgboost_model = mlflow.xgboost.load_model(logged_model)
```

### Download artifacts

```py
client.download_artifacts(run_id=run_id, path='preprocessor', dst_path='.')
```

### model registry

```py
model_name = "model_name"

# register model
run_id = "ecf6dbc7209042318cc19a4d6a8ac2e9"
model_uri = f"runs:/{run_id}/model"
mlflow.register_model(model_uri, model_name)

# list versions
latest_versions = client.get_latest_versions(name=model_name)
for version in latest_versions:
    print(f"version: {version.version}, stage: {version.current_stage}")

# change stage
model_version = 4
new_stage = "Staging"
client.transition_model_version_stage(
    name = model_name,
    version = model_version,
    stage = new_stage,
    archive_existing_versions=False
)

# add description
from datetime import datetime
date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
client.update_model_version(
    name = model_name,
    version = model_version,
    description = f"This is a model version {model_version} was transitioned to {new_stage} on {date}",
)

# list runs and sort by metric
runs = client.search_runs(
    experiment_ids=experiment.experiment_id,
    run_view_type=ViewType.ACTIVE_ONLY,
    max_results=log_top,
    order_by=["metrics.rmse ASC"],
)


# production v3 & staging v4 -> archieve v3 & production v4
client.transition_model_version_stage(
    name = model_name,
    version = 4,
    stage = "Production",
    archive_existing_versions=True
)
```

## what model log saves

1\. MLModel file

example

```yaml
artifact_path: models_mlflow
flavors:
  python_function:
    data: model.xgb
    env: conda.yaml
    loader_module: mlflow.xgboost
    python_version: 3.9.13
  xgboost:
    code: null
    data: model.xgb
    model_class: xgboost.core.Booster
    xgb_version: 1.6.2
mlflow_version: 1.28.0
model_uuid: c4ee6367d4c74d238c7c16f74437e8dd
run_id: 272a28f2395e4d75ae627a85fdd8cb90
utc_time_created: '2022-09-04 23:21:36.309514'
```

2\. conda.yaml file

```yaml
channels:
  - conda-forge
dependencies:
  - python=3.9.13
  - pip<=22.1.2
  - pip:
      - mlflow
      - pandas==1.4.4
      - psutil==5.9.2
      - scikit-learn==1.1.2
      - xgboost==1.6.2
name: mlflow-env
```

3\. model itself

4\. requirements file

5\. Python_env yaml

```yaml
python: 3.9.13
build_dependencies:
  - pip==22.1.2
  - setuptools==63.4.1
  - wheel==0.37.1
dependencies:
  - -r requirements.txt
```
