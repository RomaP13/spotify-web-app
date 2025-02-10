from fastapi import APIRouter

from app.api.routes import root_router
from app.api.routes.auth import callback_router, login_router
from app.api.routes.users import users_router

api_router = APIRouter()

api_router.include_router(root_router, tags=["Root"])

auth_routers: list[APIRouter] = [callback_router, login_router]
for auth_router in auth_routers:
    api_router.include_router(auth_router, tags=["Authentication"])

api_router.include_router(users_router, prefix="/users", tags=["Users"])
