from urllib.parse import urlencode

from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from app.core.config import settings

router = APIRouter()


@router.get("/login")
def login() -> RedirectResponse:
    spotify_auth_url = "https://accounts.spotify.com/authorize"
    scope = "user-library-read user-read-private user-read-email user-top-read"
    params: dict[str, str] = {
        "client_id": settings.spotify_client_id.get_secret_value(),
        "response_type": "code",
        "redirect_uri": settings.redirect_uri,
        # state
        "scope": scope,
        "show_dialog": "true",
    }

    # Redirect to Spotify's authorization page
    url = f"{spotify_auth_url}?{urlencode(params)}"
    response = RedirectResponse(url)
    return response
