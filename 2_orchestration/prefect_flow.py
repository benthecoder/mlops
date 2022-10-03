import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.metrics import mean_squared_error
import xgboost as xgb

from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from hyperopt.pyll import scope

import pickle
import mlflow

from prefect import flow, task
from prefect.deployments import Deployment
from prefect.orion.schemas.schedules import IntervalSchedule
from datetime import timedelta


@task
def read_preprocess(file_name) -> pd.DataFrame:

    df = pd.read_parquet(file_name)

    # parse dates
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)

    # get trip duration
    df["duration"] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
    df.duration = df.duration.apply(lambda x: x.total_seconds() / 60)

    df = df.loc[(df.duration >= 1) & (df.duration <= 60)]

    cat = ["PULocationID", "DOLocationID"]
    df[cat] = df[cat].astype(str)

    df["PU_DO"] = df["PULocationID"] + "_" + df["DOLocationID"]

    return df


@task
def add_features(df_train, df_val):
    print(len(df_train))
    print(len(df_val))

    # cat = ['PULocationID', 'DOLocationID']
    cat = ["PU_DO"]
    num = ["trip_distance"]

    dv = DictVectorizer()

    train_dict = df_train[cat + num].to_dict(orient="records")
    X_train = dv.fit_transform(train_dict)

    val_dict = df_val[cat + num].to_dict(orient="records")
    X_val = dv.transform(val_dict)

    target = "duration"
    y_train = df_train[target].values
    y_val = df_val[target].values

    return X_train, X_val, y_train, y_val, dv


@task
def train_model_search(train, valid, y_val):
    def objective(params):

        with mlflow.start_run():
            mlflow.set_tag("model", "xgboost")
            mlflow.log_params(params)
            booster = xgb.train(
                params=params,
                dtrain=train,
                num_boost_round=100,  # iterations of booster
                evals=[(valid, "validation")],
                early_stopping_rounds=50,  # if >50 iterations without improvement
            )
            y_pred = booster.predict(valid)
            rmse = mean_squared_error(y_val, y_pred, squared=False)
            mlflow.log_metric("rmse", rmse)

        return {"loss": rmse, "status": STATUS_OK}

    # ranges for hyperopt to explore
    search_space = {
        "max_depth": scope.int(hp.quniform("max_depth", 4, 100, 1)),
        "learning_rate": hp.loguniform("learning_rate", -3, 0),
        "reg_alpha": hp.loguniform("reg_alpha", -5, -1),
        "reg_lambda": hp.loguniform("reg_lambda", -6, -1),
        "min_child_weight": hp.loguniform("min_child_weight", -1, 3),
        "objective": "reg:squarederror",
        "seed": 42,
    }

    best_result = fmin(
        fn=objective,
        space=search_space,
        algo=tpe.suggest,
        max_evals=1,
        trials=Trials(),
    )

    return


@task
def train_best_model(train, valid, y_val, dv):

    with mlflow.start_run():

        best_params = {
            "learning_rate": 0.09585355369315604,
            "max_depth": 30,
            "min_child_weight": 1.060597050922164,
            "objective": "reg:linear",
            "reg_alpha": 0.018060244040060163,
            "reg_lambda": 0.011658731377413597,
            "seed": 42,
        }

        mlflow.log_params(best_params)

        booster = xgb.train(
            params=best_params,
            dtrain=train,
            num_boost_round=100,
            evals=[(valid, "validation")],
            early_stopping_rounds=50,
        )

        y_pred = booster.predict(valid)
        rmse = mean_squared_error(y_val, y_pred, squared=False)
        mlflow.log_metric("rmse", rmse)
        with open("models/preprocessor.b", "wb") as f_out:
            pickle.dump(dv, f_out)
        mlflow.log_artifact("models/preprocessor.b", artifact_path="preprocessor")

        mlflow.xgboost.log_model(booster, artifact_path="models_mlflow")


@flow
def main(
    train_path: str = "./data/green_tripdata_2021-01.parquet",
    val_path: str = "./data/green_tripdata_2021-02.parquet",
):

    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("nyc-taxi-experiment")

    X_train = read_preprocess(train_path)
    X_val = read_preprocess(val_path)
    X_train, X_val, y_train, y_val, dv = add_features(X_train, X_val)
    train = xgb.DMatrix(X_train, label=y_train)
    valid = xgb.DMatrix(X_val, label=y_val)
    train_model_search(train, valid, y_val)
    train_best_model(train, valid, y_val, dv)


if __name__ == "__main__":

    deployment = Deployment.build_from_flow(
        flow=main,
        name="model_training",
        schedule=IntervalSchedule(interval=timedelta(minutes=5)),
        work_queue_name="ml",
    )

    deployment.apply()
