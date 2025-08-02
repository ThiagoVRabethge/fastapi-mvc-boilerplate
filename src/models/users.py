from sqlalchemy import Column, String, UniqueConstraint
from sqlmodel import Field, SQLModel


class Users(SQLModel, table=True):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email"),)
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(sa_column=Column(String, unique=True, nullable=False))
    password: str
