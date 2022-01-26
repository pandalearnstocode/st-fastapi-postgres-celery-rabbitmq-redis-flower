import databases
import ormar
import sqlalchemy

from .settings import settings

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class ModelMetaData(ormar.Model):
    class Meta(BaseMeta):
        tablename = "model_metadata"

    id: int = ormar.Integer(primary_key=True)
    model_id: str = ormar.String(max_length=128, unique=True, nullable=False)
    status: str = ormar.String(max_length=128, unique=False, nullable=False)
    model_name: str = ormar.String(max_length=128, unique=False, nullable=False)

engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)