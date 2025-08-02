from fastapi import APIRouter

from src.controllers.auth import (
    handle_post_auth_login_users,
    handle_post_auth_register_users,
)
from src.models.users import Users

auth_routes = APIRouter()


@auth_routes.post("/auth/register-users")
def post_auth_register_users(user: Users):
    return handle_post_auth_register_users(user)


@auth_routes.post("/auth/login-users")
def post_auth_login_users(user: Users):
    return handle_post_auth_login_users(user)
