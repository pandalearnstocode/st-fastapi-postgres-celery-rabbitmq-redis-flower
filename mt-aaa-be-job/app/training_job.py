import time

from celery import Celery
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import redis
from .settings import *
import pickle
import requests

app = Celery("tasks", broker=BROKER_CONN_URI, backend=BACKEND_CONN_URI)
redis_store = redis.Redis.from_url(REDIS_STORE_CONN_URI)
APPLICATION_SERVICE_URL = "http://mt-aaa-be-api:5000/model/"

def train_model(
    data_path="https://raw.githubusercontent.com/elleobrien/wine/master/wine_quality.csv",
    y_var="quality",
    split_ratio=0.2,
    seed = 42
):
    df = pd.read_csv(data_path)
    y = df.pop(y_var)
    X_train, X_test, y_train, y_test = train_test_split(
        df, y, test_size=split_ratio, random_state=seed
    )
    regr = RandomForestRegressor(max_depth=2, random_state=seed)
    regr.fit(X_train, y_train)
    train_score = regr.score(X_train, y_train) * 100
    test_score = regr.score(X_test, y_test) * 100
    importances = regr.feature_importances_
    labels = df.columns
    feature_df = pd.DataFrame(
        list(zip(labels, importances)), columns=["feature", "importance"]
    )
    feature_df = feature_df.sort_values(
        by="importance",
        ascending=False,
    )
    y_pred = regr.predict(X_test) + np.random.normal(0, 0.25, len(y_test))
    y_jitter = y_test + np.random.normal(0, 0.25, len(y_test))
    res_df = pd.DataFrame(list(zip(y_jitter, y_pred)), columns=["true", "pred"])
    return {"residuals_data": res_df.to_dict(orient="list"),"feature_importance_data": feature_df.to_dict(orient="list"),"train_score": train_score,"test_score": test_score}

@app.task(name="train_model_job")
def train_model_job(model_name, split_ratio, model_id):
    model_train_data_init = {"model_id": model_id, "status": "processing", "model_name":model_name}
    r = requests.post(APPLICATION_SERVICE_URL + "update/", json=model_train_data_init)
    print(r.text)
    delta = 10
    time.sleep(delta)
    model_results =  train_model(split_ratio = split_ratio)
    model_train_data_done = {"model_id": model_id, "status": "done", "model_name":model_name}
    r = requests.post(APPLICATION_SERVICE_URL + "update/", json=model_train_data_done)
    print(r.text)
    return_value = {"model_id": model_id, "status": "done", "model_name":model_name, "model_result":model_results}
    pickled_object = pickle.dumps(return_value)
    redis_store.set(model_id, pickled_object)
    return return_value