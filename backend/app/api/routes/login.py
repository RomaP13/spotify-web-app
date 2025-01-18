from urllib.parse import urlencode

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from app.api.utils.session_utils import generate_state_token
from app.core.config import settings

router = APIRouter()


@router.get("/login")
def login(request: Request) -> RedirectResponse:
    spotify_auth_url = "https://accounts.spotify.com/authorize"
    scope = "user-library-read user-read-private user-read-email user-top-read"

    # Generate a secure state token using the utility function
    state = generate_state_token()
    request.session["state"] = state

    params: dict[str, str] = {
        "client_id": settings.spotify_client_id.get_secret_value(),
        "response_type": "code",
        "redirect_uri": settings.redirect_uri,
        "state": state,
        "scope": scope,
        "show_dialog": "true",
    }

    # Redirect to Spotify's authorization page
    return RedirectResponse(f"{spotify_auth_url}?{urlencode(params)}")
