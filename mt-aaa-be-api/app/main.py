
from fastapi import FastAPI
######### OLD API #########
# from app.api.ml_model import model_router
# from app.api.db import database, ModelMetaData
######### NEW API #########
from app.api import notes, ping
from app.db import database, engine, metadata
metadata.create_all(engine)


app = FastAPI(title="Model API", docs_url="/", version="1.0.0")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(notes.router, prefix="/notes", tags=["notes"])

app.include_router(ping.router)


######### OLD API #########
# app.include_router(
#     model_router,
#     prefix="/model",
#     tags=["model"],
# )


# @app.on_event("startup")
# async def startup():
#     if not database.is_connected:
#         await database.connect()
#     # create a dummy entry
#     await ModelMetaData.objects.get_or_create(model_id="12345", model_name="seed", model_status="seed")


# @app.on_event("shutdown")
# async def shutdown():
#     if database.is_connected:
#         await database.disconnect()