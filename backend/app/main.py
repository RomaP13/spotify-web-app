import base64
from urllib.parse import urlencode

import requests
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

from app.core.config import settings

app = FastAPI()


@app.get("/")
def read_root():
    return {
        "Hello": "World",
        "REDIRECT_URI": settings.redirect_uri,
        "SPOTIFY_CLIENT_ID": settings.spotify_client_id,
        "SPOTIFY_CLIENT_SECRET": settings.spotify_client_secret,
    }


@app.get("/login")
def login() -> RedirectResponse:
    spotify_auth_url = "https://accounts.spotify.com/authorize"
    scope = "user-library-read user-read-private user-read-email"
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


@app.get("/callback")
def callback(request: Request):
    print("Callback function triggered")
    code = request.query_params.get("code")
    # state = request.query_params.get("state")

    # TODO: Compare the state parameter with the state parameter
    #       it originally provided from login function

    token_url = "https://accounts.spotify.com/api/token"
    request_string = (
        settings.spotify_client_id.get_secret_value()
        + ":"
        + settings.spotify_client_secret.get_secret_value()
    )
    encoded_bytes = base64.b64encode(request_string.encode("utf-8"))
    encoded_string = str(encoded_bytes, "utf-8")
    headers = {
        # Format: Authorization: Basic <base64 encoded client_id:client_secret>
        "Authorization": "Basic " + encoded_string,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    form_data: dict[str, str] = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.redirect_uri,
    }

    api_response = requests.post(token_url, data=form_data, headers=headers)
    print(f"API Response status: {api_response.status_code}")
    if api_response.status_code == 200:
        json_data = api_response.json()

        print(json_data.get("access_token"))
        print(json_data.get("token_type"))
        print(json_data.get("scope"))
        print(json_data.get("expires_in"))
        print(json_data.get("refresh_token"))

    response = RedirectResponse("/")
    return response
