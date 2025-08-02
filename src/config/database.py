from decouple import config
from sqlmodel import SQLModel, create_engine

from src.models.items import Items  # noqa: F401
from src.models.users import Users  # noqa: F401

database_url = config("DATABASE_URL")

engine = create_engine(database_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
