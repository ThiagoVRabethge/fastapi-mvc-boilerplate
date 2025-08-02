from sqlmodel import Session

from src.config.database import engine


def post(row):
    with Session(engine) as session:
        session.add(row)

        session.commit()

        session.refresh(row)

        return row
