import requests
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from app.api.dependencies import SessionDep
from app.api.spotify.auth import get_auth_headers
from app.api.spotify.user import get_user_id, update_or_create_user_tokens
from app.core.config import settings
from app.models import SpotifyTokenData

router = APIRouter()


@router.get("/callback")
def callback(request: Request, session: SessionDep):
    code = request.query_params.get("code")
    # state = request.query_params.get("state")

    # TODO: Compare the state parameter with the state parameter
    #       it originally provided from login function

    token_url = "https://accounts.spotify.com/api/token"
    headers = get_auth_headers()
    form_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.redirect_uri,
    }

    api_response = requests.post(token_url, data=form_data, headers=headers)
    if api_response.status_code == 200:
        token_data = SpotifyTokenData(**api_response.json())
        user_id = get_user_id(token_data.access_token)
        update_or_create_user_tokens(session, token_data, user_id)
        request.session["spotify_user_id"] = user_id

    return RedirectResponse("/")
