from fastapi import APIRouter
import redis
from .settings import *
import uuid
from .training_job import train_model_job
import pickle
import pandas as pd
from .db import ModelMetaData
model_router = APIRouter()

print(f"BE APIs: REDIS_STORE_CONN_URI: {REDIS_STORE_CONN_URI}")
redis_store = redis.Redis.from_url(REDIS_STORE_CONN_URI)

@model_router.get("/ids/")
async def get_model_ids():
    return await ModelMetaData.objects.all()

@model_router.post("/train/")
async def submit_model_train_job(train_payload: TrainModel):
    train_payload_dict =  train_payload.dict()
    model_name = train_payload_dict['model_name']
    model_parameters = train_payload_dict['model_parameters']
    split_ratio = float(model_parameters['split_ratio'])
    model_id = str(uuid.uuid4())
    await ModelMetaData.objects.update_or_create(model_id=model_id, model_status ="submitted",model_name =model_name)
    train_model_job.delay(model_name, split_ratio, model_id)
    return {"model_id": model_id, "model_status": "submitted", "model_name":model_name}

@model_router.post("/update/")
async def update_model_train_job_status(status_payload: ModelMetaData):
    status_payload_dict =  status_payload.dict()
    model_id = status_payload_dict['model_id']
    status = status_payload_dict['status']
    model_name = status_payload_dict['model_name']
    await ModelMetaData.objects.update_or_create(model_id=model_id, status =status, model_name =model_name)
    return {"model_id": model_id, "model_status": status, "model_name":model_name}

@model_router.get("/status/{model_id}")
async def get_model_status(model_id: str):
    try:
        status_dict = pickle.loads(redis_store.get(model_id))
    except Exception as e:
        status_dict = {"model_id": model_id, "model_status": "unknown", "model_name": "unknown"}
    return {"model_id": status_dict['model_id'], "model_status": status_dict['status']}


@model_router.get("/result/{model_id}")
async def get_model_results(model_id: str):
    return pickle.loads(redis_store.get(model_id))

@model_router.post("/aggregate/")
async def aggregate_results(agg_payload: AggregateResults):
    agg_payload_dict =  agg_payload.dict()
    model_id = agg_payload_dict['model_id']
    agg_func = agg_payload_dict['agg_func']
    model_results = pickle.loads(redis_store.get(model_id))
    if model_results['model_status'] == 'done':
        residual_df = pd.DataFrame.from_dict(model_results['model_result']['residuals_data'])
        residual_df_agg = residual_df.agg(agg_func)
        return {"model_id": model_id, "agg_result": residual_df_agg.to_dict()}
    else:
        return {"model_id": model_id, "model_status": model_results['model_status']}