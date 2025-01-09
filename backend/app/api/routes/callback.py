import base64
from datetime import datetime, timedelta

import requests
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from app.api.dependencies import SessionDep
from app.api.utils.spotify.user import get_user_id
from app.core.config import settings
from app.models import SpotifyToken

router = APIRouter()


@router.get("/callback")
def callback(request: Request, session: SessionDep):
    # TODO: Add check if user is already exists. Or maybe just update.
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
        json_data = api_response.json()
        access_token = json_data.get("access_token")
        user_id = get_user_id(access_token)

        expires_in = datetime.utcnow() + timedelta(
            seconds=json_data.get("expires_in")
        )

        spotify_token = SpotifyToken(
            spotify_user_id=user_id,
            access_token=access_token,
            refresh_token=json_data.get("refresh_token"),
            expires_in=expires_in,
        )
        session.add(spotify_token)
        session.commit()

    return RedirectResponse("/")
