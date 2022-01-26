
from fastapi import FastAPI
from app.api.ml_model import model_router
from app.api.db import database, ModelMetaData


app = FastAPI(title="Model API", docs_url="/", version="1.0.0")

app.include_router(
    model_router,
    prefix="/model",
    tags=["model"],
)

@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    # create a dummy entry
    await ModelMetaData.objects.get_or_create(model_id="12345", model_name="seed", status="seed")


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()