from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.api.main import api_router
from app.api.middlewares import AuthenticationMiddleware
from app.core.database import create_db_and_tables

app = FastAPI()

app.add_middleware(AuthenticationMiddleware)

app.add_middleware(
    SessionMiddleware,
    secret_key="your-random-secret-key",
)


app.include_router(api_router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
