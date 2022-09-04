# mlflow notes

## run mlflow

1. create env `conda create -n mlflow_env python=3.9`
2. `pip install -r requirements.txt`
3. run mlflow and configure backend `mlflow ui --backend-store-uri sqlite:///mlflow.db`

## functions

```py
import mlflow

mlflow.set_tracking_uri('sqlite:///mlflow.db')
mlflow.set_experiment("experiment_name") 

mlflow.set_tag("model", "xgboost")
mlflow.log_param("param_name", param)
mlflow.log_metric("metric_name", metric)

# log model options 
# 1
mlflow.log_artifact(local_path = "path/to/model", artifact_path="models")

# 2 
mlflow.<framework>.log_model(model, artifat_path="models")

mlflow.xgboost.autolog()


logged_model = 'runs:/run_id/models_mlflow'

# Load model as a PyFuncModel.
loaded_model = mlflow.pyfunc.load_model(logged_model)

# load as xgboost object
xgboost_model = mlflow.xgboost.load_model(logged_model)
```


model log saves

1. MLModel file

``` yaml
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

2. conda.yaml file

``` yaml
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

3. model itself

4. requirements file