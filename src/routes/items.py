from fastapi import APIRouter, Depends

from src.controllers.items import handle_get_items
from src.security.verify_jwt_token import verify_jwt_token

items_routes = APIRouter(dependencies=[Depends(verify_jwt_token)])


@items_routes.get("/items")
def get_items():
    return handle_get_items()
