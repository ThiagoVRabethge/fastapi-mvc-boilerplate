from fastapi import HTTPException
from src.models.items import Items
from src.repositories.generic_repository import (
    get_all,
    get_by_id,
    create,
    update,
    partial_update,
    delete,
)


def get_all_controller():
    return get_all(Items)


def get_by_id_controller(id: int):
    return get_by_id(Items, id)


def create_controller(data: Items):
    return create(data)


def update_controller(id: int, data: Items):
    return update(Items, id, data)


def partial_update_controller(id: int, data: dict):
    return partial_update(Items, id, data)


def delete_controller(id: int):
    return delete(Items, id)
