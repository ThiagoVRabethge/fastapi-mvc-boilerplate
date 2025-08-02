from sqlmodel import Session, select

from src.config.database import engine


def get_by_column(model, attribute, attribute_value, quantity="single"):
    with Session(engine) as session:
        column = getattr(model, attribute)

        query = select(model).where(column == attribute_value)

        result = session.exec(query)

        if quantity == "multiple":
            return result.all()

        else:
            return result.first()
