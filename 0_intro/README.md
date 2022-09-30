# Notes for week 0

MLOps is putting ML into production using best practices

Notebooks are bad. Why?

- easy to overwrite changes and history is lost
  - experimentes are not tracked
    - log all the metrics used to train model -> experiment tracking
  - models trained are not tracked
    - save all models trained -> model registry
- if changing parameters, re-execute the entire notebook

Goal is reproducability and tracking what we do.

ML Pipeline

load data -> preprocess -> train -> model

put pipeline into a script

`python pipeline.py --train_data "" --val_data ""`

Allows retraining to be reproducible

Deployment

- server model to users

Monitor

- watch for drop in performance (data drift) -> new data to pipeline -> model v2 -> serve

This process can be fully automated.

## MLOps Maturity model

<https://docs.microsoft.com/en-us/azure/architecture/example-scenario/mlops/mlops-maturity-model>

- l0 : no mlops
- l1 : devops without mlops
- l2 : automated training
- l3 : automated model deployment
- l4 : full mlops automation

## office hours insights

why dict vectorizer? vs pd.get_dummies

- in get_dummies, when you have diff set of features in your train and valid, it will create empty columns in your validation even though it doesn't exist
- in dict vectorizer, it will just ignore absent features and won't store them (sparsity advantage), it also stores featrure names along with values
