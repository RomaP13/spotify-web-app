import logging
from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.api.dependencies.session import SessionDep
from app.api.dependencies.session_user import UserSessionDep
from app.api.spotify.auth import refresh_spotify_token
from app.api.spotify.user import get_user_tokens
from app.api.utils.token_utils import is_token_expired
from app.models import SpotifyToken

logger = logging.getLogger(__name__)


def get_current_user(
    session: SessionDep, user_session_id: UserSessionDep
) -> SpotifyToken:
    user_token = get_user_tokens(session, user_session_id)

    if not user_token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User session not found",
        )

    # Check and refresh token if expired
    if is_token_expired(user_token.expires_at):
        logger.info("Token expired. Refreshing...")
        refresh_spotify_token(
            session, user_session_id, user_token.refresh_token
        )
        user_token = get_user_tokens(session, user_session_id)
        if not user_token:  # Ensure a token is still returned after refresh
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Failed to refresh user session",
            )
        logger.info("Token refreshed successfully.")

    return user_token


CurrentUserDep = Annotated[SpotifyToken, Depends(get_current_user)]
