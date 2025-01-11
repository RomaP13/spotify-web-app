import base64
from datetime import datetime

import requests

from app.api.dependencies import SessionDep
from app.api.spotify.user import get_user_tokens, update_or_create_user_tokens
from app.core.config import settings
from app.models import SpotifyTokenData


def get_basic_auth_headers() -> dict[str, str]:
    """
    Create basic authentication headers using Spotify client credentials.

    Returns:
        dict[str, str]: A dictionary containing the 'Authorization'
                        and 'Content-Type' headers for basic authentication.
    """
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
    return headers


def get_bearer_auth_header(token: str) -> dict[str, str]:
    """
    Create a bearer authorization header using the given token.

    Args:
        token (str): Access token.

    Returns:
        dict[str, str]: A dictionary containing the 'Authorization' header
                        for bearer authentication.
    """
    return {"Authorization": "Bearer " + token}


def is_spotify_authenticated(session: SessionDep, user_id: str) -> bool:
    """
    Check if the user is authenticated.

    Args:
        session (SessionDep): Database session dependency.
        user_id (str): User ID.

    Returns:
        bool: True if authenticated, False otherwise.
    """
    tokens = get_user_tokens(session, user_id)
    # TODO: Check if tokens.access_token == access token from header???
    if tokens:
        expiry = tokens.expires_in
        if expiry <= datetime.utcnow():
            refresh_spotify_token(session, user_id, tokens.refresh_token)
        return True
    return False


def refresh_spotify_token(
    session: SessionDep, user_id: str, refresh_token: str
) -> None:
    """
    Refresh Spotify token and update the database.

    Args:
        session (SessionDep): Database session dependency.
        user_id (str): User ID.
        refresh_token (str): Refresh token.
    """
    headers = get_basic_auth_headers()
    form_data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": settings.spotify_client_id.get_secret_value(),
    }
    api_response = requests.post(
        "https://accounts.spotify.com/api/token",
        data=form_data,
        headers=headers,
    )
    print(f"STATUS: {api_response.status_code}")
    if api_response.status_code == 200:
        json_response = api_response.json()
        if not json_response.get("refresh_token"):
            json_response["refresh_token"] = (
                refresh_token  # Use the existing one
            )
        print(f"JSON: {api_response.json()}")
        token_data = SpotifyTokenData(**json_response)
        update_or_create_user_tokens(session, token_data, user_id)
    # TODO: Redirect user to an error page???
