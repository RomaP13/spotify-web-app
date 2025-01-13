import requests

from app.api.dependencies import SessionDep
from app.api.spotify.auth_headers import get_bearer_auth_header
from app.api.utils.token_utils import calculate_expiry_duration
from app.models import SpotifyToken, SpotifyTokenData


def get_user_id(access_token: str) -> str:
    headers = get_bearer_auth_header(access_token)
    response = requests.get("https://api.spotify.com/v1/me", headers=headers)
    return response.json().get("id")


def get_user_tokens(
    session: SessionDep, spotify_user_id: str
) -> SpotifyToken | None:
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
