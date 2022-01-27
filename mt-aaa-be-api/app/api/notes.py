from typing import List

from fastapi import APIRouter, HTTPException, Path

from app.api import crud
from app.api.models import ModelMetaData, ModelMetaDataSchema

router = APIRouter()


@router.post("/", response_model=ModelMetaData, status_code=201)
async def create_note(payload: ModelMetaDataSchema):
    model_id = await crud.post(payload)
    # Model should be created and have an id
    response_object = {
        "model_id": model_id,
        "model_status": payload.model_status,
        "model_name": payload.model_name,
    }
    return response_object


@router.get("/{model_id}/", response_model=ModelMetaData)
async def read_note(model_id: str,):
    model = await crud.get(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return model


@router.get("/", response_model=List[ModelMetaData])
async def read_all_notes():
    return await crud.get_all()


@router.put("/{model_id}/", response_model=ModelMetaData)
async def update_note(payload: ModelMetaDataSchema, model_id: str,):
    model = await crud.get(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    model_id = await crud.put(model_id, payload)
    response_object = {
        "model_id": model_id,
        "model_name": payload.model_name,
        "model_status": payload.model_status,
    }
    return response_object


@router.delete("/{model_id}/", response_model=ModelMetaData)
async def delete_note(model_id: str):
    model = await crud.get(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    await crud.delete(model_id)
    return model