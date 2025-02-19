from uuid import UUID

import requests
from loguru import logger

from app.api.dependencies.session import SessionDep
from app.api.spotify.auth_headers import get_basic_auth_headers
from app.api.spotify.user import get_user_tokens, update_or_create_user_tokens
from app.api.utils.token_utils import is_token_expired
from app.core.config import settings
from app.models import SpotifyToken, SpotifyTokenData


def is_spotify_authenticated(
    session: SessionDep, user_session_id: UUID
) -> bool:
    """Check if the user is authenticated.

    Args:
        session (SessionDep): Database session dependency.
        user_session_id (UUID): User session ID.

    Returns:
        bool: True if authenticated, False otherwise.
    """
    tokens: SpotifyToken | None = get_user_tokens(session, user_session_id)
    if tokens:
        if is_token_expired(tokens.expires_at):
            logger.info("Token was expired. Refreshing...")
            refresh_spotify_token(
                session, user_session_id, tokens.refresh_token
            )
            logger.info("Token was refreshed.")
        return True
    return False


def refresh_spotify_token(
    session: SessionDep, user_session_id: UUID, refresh_token: str
) -> None:
    """Refresh Spotify token and update the database.

    Args:
        session (SessionDep): Database session dependency.
        user_session_id (UUID): User session ID.
        refresh_token (str): Refresh token.
    """
    headers: dict[str, str] = get_basic_auth_headers()
    form_data: dict[str, str] = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": settings.spotify_client_id.get_secret_value(),
    }
    api_response = requests.post(
        "https://accounts.spotify.com/api/token",
        data=form_data,
        headers=headers,
    )
    # TODO: add error handling if status code is not 200
    if api_response.status_code == 200:
        json_response = api_response.json()
        if not json_response.get("refresh_token"):
            json_response["refresh_token"] = (
                refresh_token  # Use the existing one
            )
        token_data = SpotifyTokenData(**json_response)
        update_or_create_user_tokens(session, token_data, user_session_id)
    # TODO: Redirect user to an error page???
