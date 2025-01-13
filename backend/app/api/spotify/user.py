from app.api.dependencies import SessionDep
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
    session: SessionDep, spotify_user_id: str
) -> SpotifyToken | None:
    """
    Retrieve user tokens from the database.

    Args:
        session (SessionDep): Database session dependency.
        spotify_user_id (str): Spotify user ID.

    Returns:
        SpotifyToken | None: User tokens or None if not found.
    """
    user_tokens = session.get(SpotifyToken, spotify_user_id)
    if user_tokens:
        return user_tokens
    return None


def update_or_create_user_tokens(
    session: SessionDep, token_data: SpotifyTokenData, user_id: str
):
    access_token = token_data.access_token
    refresh_token = token_data.refresh_token
    expires_in = calculate_expiry_duration(token_data.expires_in)
    print(f"EXPIRES IN {expires_in}")
    """
    Update or create user tokens in the database.

    Args:
        session (SessionDep): Database session dependency.
        token_data (SpotifyTokenData): Token data to store.
        user_id (str): Spotify user ID.
    """
    tokens = get_user_tokens(session, user_id)
    if tokens:
        print(f"TOKENS BEFORE IF: {get_user_tokens(session, user_id)}")
        tokens.expires_in = expires_in
        tokens.sqlmodel_update(tokens)
        print(f"TOKENS AFTER IF: {get_user_tokens(session, user_id)}")
    else:
        print(f"TOKENS BEFORE ELSE: {tokens}")
        tokens = SpotifyToken(
            user_id=user_id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in,
        )
        print(f"TOKENS AFTER ELSE: {tokens}")

    session.add(tokens)
    session.commit()
