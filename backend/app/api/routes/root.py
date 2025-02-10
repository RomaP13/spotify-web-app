from fastapi import APIRouter, Request

from app.api.dependencies.session import SessionDep
from app.core.config import settings
from app.models import SpotifyToken

router = APIRouter()


@router.get("/")
def read_root(request: Request):
    if request.state.is_authenticated:
        return {"message": "Welcome back, authenticated user!"}
    else:
        return {"message": "Hello, please log in to access more features."}
