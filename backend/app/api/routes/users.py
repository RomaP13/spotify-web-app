from uuid import UUID

from fastapi import APIRouter, Request, Response

from app.api.dependencies.session import SessionDep
from app.api.spotify.request import execute_spotify_api_request
from app.api.spotify.user import get_user_tokens

router = APIRouter()


@router.get("/user/data")
def user_data(
    request: Request, session: SessionDep, user_session_id: UserSessionDep
):
    access_token = get_user_tokens(session, user_session_id).access_token
    data = execute_spotify_api_request(
        access_token, endpoint="me", method="GET"
    )
    return data


@router.get("/user/top/{type}")
def playlist(
    type: str,
    request: Request,
    session: SessionDep,
    user_session_id: UserSessionDep,
):
    endpoint = f"me/top/{type}"
    access_token = get_user_tokens(session, user_id).access_token
    playlist_tracks = execute_spotify_api_request(
        access_token, endpoint, method="GET"
    )
    return playlist_tracks
