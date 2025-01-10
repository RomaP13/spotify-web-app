import base64

import requests
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from app.api.dependencies import SessionDep
from app.api.spotify.user import update_or_create_user_tokens
from app.core.config import settings
from app.models import SpotifyTokenData

router = APIRouter()


@router.get("/callback")
def callback(request: Request, session: SessionDep):
    code = request.query_params.get("code")

    token_url = "https://accounts.spotify.com/api/token"
    request_string = (
        settings.spotify_client_id.get_secret_value()
        + ":"
        + settings.spotify_client_secret.get_secret_value()
    )
    encoded_bytes = base64.b64encode(request_string.encode("utf-8"))
    encoded_string = str(encoded_bytes, "utf-8")
    headers = {
        "Authorization": "Basic " + encoded_string,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    form_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.redirect_uri,
    }

    api_response = requests.post(token_url, data=form_data, headers=headers)
    if api_response.status_code == 200:
        token_data = SpotifyTokenData(**api_response.json())
        update_or_create_user_tokens(session, token_data)

    return RedirectResponse("/")
