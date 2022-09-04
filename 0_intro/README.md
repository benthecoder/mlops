# Notes for week 1

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



## office hours insights

- why dict vectorizer?