from fastapi import APIRouter, Depends
from src.controllers.items import (
    get_all_controller,
    get_by_id_controller,
    create_controller,
    update_controller,
    partial_update_controller,
    delete_controller,
)
from src.models.items import Items
from src.security.verify_jwt_token import verify_jwt_token

items_routes = APIRouter(dependencies=[Depends(verify_jwt_token)])


@items_routes.get("/items")
def route_get_all():
    return get_all_controller()


@items_routes.get("/items/{id}")
def route_get_by_id(id: int):
    return get_by_id_controller(id)


@items_routes.post("/items")
def route_create(data: Items):
    return create_controller(data)


@items_routes.put("/items/{id}")
def route_update(id: int, data: Items):
    return update_controller(id, data)


@items_routes.patch("/items/{id}")
def route_partial_update(id: int, data: dict):
    return partial_update_controller(id, data)


@items_routes.delete("/items/{id}")
def route_delete(id: int):
    return delete_controller(id)
