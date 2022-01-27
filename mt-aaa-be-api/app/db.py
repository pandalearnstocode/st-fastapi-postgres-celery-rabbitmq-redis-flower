import os
from uuid import uuid4

from sqlalchemy import (
    Column,
    MetaData,
    String,
    Table,
    create_engine
)

from databases import Database
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()
modelmetadata = Table(
    "modelmetadata",
    metadata,
    Column("model_id", String, primary_key=True, default=uuid4),
    Column("model_status", String(50), nullable=False),
    Column("model_name", String(50), nullable=False),
)

# databases query builder
database = Database(DATABASE_URL)