from sqlmodel import Session, select
from src.config.database import engine
from fastapi import HTTPException


def get_all(model_class):
    with Session(engine) as session:
        return session.exec(select(model_class)).all()


def get_by_id(model_class, id: int):
    with Session(engine) as session:
        item = session.get(model_class, id)
        if not item:
            raise HTTPException(
                status_code=404, detail=f"{model_class.__name__} not found"
            )
        return item


def create(model_instance):
    with Session(engine) as session:
        session.add(model_instance)
        session.commit()
        session.refresh(model_instance)
        return model_instance


def update(model_class, id: int, new_data):
    with Session(engine) as session:
        db_item = session.get(model_class, id)
        if not db_item:
            raise HTTPException(
                status_code=404, detail=f"{model_class.__name__} not found"
            )
        for key, value in new_data.dict().items():
            setattr(db_item, key, value)
        session.commit()
        session.refresh(db_item)
        return db_item


def partial_update(model_class, id: int, data: dict):
    with Session(engine) as session:
        db_item = session.get(model_class, id)
        if not db_item:
            raise HTTPException(
                status_code=404, detail=f"{model_class.__name__} not found"
            )
        for key, value in data.items():
            setattr(db_item, key, value)
        session.commit()
        session.refresh(db_item)
        return db_item


def delete(model_class, id: int):
    with Session(engine) as session:
        item = session.get(model_class, id)
        if not item:
            raise HTTPException(
                status_code=404, detail=f"{model_class.__name__} not found"
            )
        session.delete(item)
        session.commit()
        return {"success": True}
