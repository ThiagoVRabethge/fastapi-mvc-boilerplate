from decouple import config
from fastapi import HTTPException, Request, status
from jose import JWTError, jwt


def verify_jwt_token(request: Request):
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação ausente ou inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(
            token, config("SECRET_KEY"), algorithms=[config("ALGORITHM")]
        )

        sub = payload.get("sub")

        email = payload.get("email")

        if sub is None or email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token JWT malformado: claims obrigatórias ausentes",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload

    except JWTError as e:  # noqa: F841
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token JWT inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
