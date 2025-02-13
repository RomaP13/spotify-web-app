from typing import Any
from uuid import UUID

from app.api.dependencies.session import SessionDep
from app.api.spotify.request import execute_spotify_api_request
from app.api.utils.token_utils import calculate_expiry_duration
from app.models import SpotifyToken, SpotifyTokenData


def get_user_id(access_token: str) -> str:
    """
    Get Spotify user ID using the access token.

    Args:
        access_token (str): Access token for Spotify API.

    Returns:
        str: User ID from Spotify API response.
    """
    data = execute_spotify_api_request(
        access_token, endpoint="me", method="GET"
    )
    return data.get("id")


def get_user_tokens(
    session: SessionDep, user_session_id: UUID
) -> SpotifyToken | None:
    """
    Retrieve user tokens from the database.

    Args:
        session (SessionDep): Database session dependency.
        user_session_id (UUID): User session ID.

    Returns:
        SpotifyToken | None: User tokens or None if not found.
    """
    user_tokens: SpotifyToken | None = session.get(
        SpotifyToken, user_session_id
    )
    if user_tokens:
        return user_tokens
    return None


def update_or_create_user_tokens(
    session: SessionDep,
    token_data: SpotifyTokenData,
    user_session_id: UUID,
) -> None:
    """
    Update or create user tokens in the database.

    Args:
        session (SessionDep): Database session dependency.
        token_data (SpotifyTokenData): Token data to store.
        user_session_id (UUID): User session ID.
    """
    tokens: SpotifyToken | None = get_user_tokens(session, user_session_id)
    token_data_dict: dict[str, Any] = token_data.model_dump(exclude_unset=True)

    # Calculate expiry timestamp
    token_data_dict["expires_at"] = calculate_expiry_duration(
        seconds=token_data.expires_in
    )
    # Remove expires_in since we're using expires_at
    del token_data_dict["expires_in"]

    if tokens:
        tokens.sqlmodel_update(token_data_dict)
    else:
        tokens = SpotifyToken(
            user_session_id=user_session_id, **token_data_dict
        )

    session.add(tokens)
    session.commit()
    session.refresh(tokens)
