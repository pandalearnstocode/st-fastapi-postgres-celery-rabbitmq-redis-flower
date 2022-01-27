from pydantic import BaseModel, Field


class ModelMetaDataSchema(BaseModel):
    model_status: str = Field(..., min_length=3, max_length=50)
    model_name: str = Field(..., min_length=3, max_length=50)


class ModelMetaData(ModelMetaDataSchema):
    model_id: str