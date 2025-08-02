from sqlmodel import Session, select

from src.config.database import engine


def get_all(model):
    with Session(engine) as session:
        rows = session.exec(select(model)).all()

        return rows
