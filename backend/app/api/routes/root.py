from fastapi import APIRouter

from app.api.dependencies import SessionDep
from app.core.config import settings
from app.models import SpotifyToken

router = APIRouter()


@router.get("/")
def read_root(session: SessionDep):
    spotify_token = session.get(SpotifyToken, 1)
    if spotify_token:
        return spotify_token

    return {
        "Hello": "World",
        "REDIRECT_URI": settings.redirect_uri,
        "SPOTIFY_CLIENT_ID": settings.spotify_client_id,
        "SPOTIFY_CLIENT_SECRET": settings.spotify_client_secret,
    }
