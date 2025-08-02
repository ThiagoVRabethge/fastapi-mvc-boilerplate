from sqlmodel import Field, SQLModel


class Items(SQLModel, table=True):
    __tablename__ = "items"
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
