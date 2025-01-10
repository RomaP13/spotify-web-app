from fastapi import APIRouter

from app.api.routes import callback, login, root

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(callback.router)
api_router.include_router(root.router)
