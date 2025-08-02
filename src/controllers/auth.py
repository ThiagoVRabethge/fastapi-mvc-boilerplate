import re
from datetime import datetime, timedelta

from decouple import config
from jose import jwt
from passlib.hash import sha256_crypt

from src.models.users import Users
from src.repositories.get_by_column import get_by_column
from src.repositories.post import post


def handle_post_auth_register_users(user: Users):
    password = user.password

    if (
        len(password) < 8
        or not re.search(r"[A-Z]", password)
        or not re.search(r"[a-z]", password)
        or not re.search(r"\d", password)
        or not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
    ):
        return {
            "success": False,
            "error": "Senha deve ter no mínimo 8 caracteres, incluindo letras maiúsculas, minúsculas, números e caracteres especiais.",
        }

    user.password = sha256_crypt.hash(password)

    new_user = post(user)

    return {"success": True if new_user else False}


def handle_post_auth_login_users(user: Users):
    db_user = get_by_column(Users, "email", user.email)

    if not db_user:
        return {"success": False, "error": "Usuário não encontrado."}

    if not sha256_crypt.verify(user.password, db_user.password):
        return {"success": False, "error": "Senha incorreta."}

    expire = datetime.utcnow() + timedelta(minutes=60)

    payload = {"sub": str(db_user.id), "email": db_user.email, "exp": expire}

    token = jwt.encode(payload, config("SECRET_KEY"), algorithm=config("ALGORITHM"))

    return {"success": True, "access_token": token, "token_type": "bearer"}
