from fastapi import APIRouter

from app.api.routes import callback, login, playlists, root, users

api_router = APIRouter()
routes = [
    callback,
    login,
    playlists,
    root,
    users,
]
for r in routes:
    api_router.include_router(r.router)
