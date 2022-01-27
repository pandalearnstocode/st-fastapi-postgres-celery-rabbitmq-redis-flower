from app.api.models import ModelMetaDataSchema
from app.db import modelmetadata, database


async def post(payload: ModelMetaDataSchema):
    query = modelmetadata.insert().values(model_name=payload.model_name, model_status=payload.model_status)
    return await database.execute(query=query)


async def get(model_id: str):
    query = modelmetadata.select().where(model_id == modelmetadata.c.model_id)
    return await database.fetch_one(query=query)


async def get_all():
    query = modelmetadata.select()
    return await database.fetch_all(query=query)


async def put(model_id: str, payload: ModelMetaDataSchema):
    query = (
        modelmetadata
        .update()
        .where(model_id == modelmetadata.c.model_id)
        .values(model_name=payload.model_name, model_status=payload.model_status)
        .returning(modelmetadata.c.model_id)
    )
    return await database.execute(query=query)


async def delete(model_id: str):
    query = modelmetadata.delete().where(model_id == modelmetadata.c.model_id)
    return await database.execute(query=query)