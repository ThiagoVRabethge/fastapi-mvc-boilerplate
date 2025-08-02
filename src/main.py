from fastapi import FastAPI

from src.config.database import create_db_and_tables
from src.public_routes import public_routes

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def docs():
    return {"docs": "see /docs", "redoc": "see /redoc"}


for public_route in public_routes:
    app.include_router(public_route)
