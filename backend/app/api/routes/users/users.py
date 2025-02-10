from fastapi import APIRouter

from app.api.dependencies.session import SessionDep
from app.api.dependencies.user import CurrentUserDep
from app.api.spotify.request import execute_spotify_api_request

router = APIRouter()


@router.get("/me")
def get_current_user_profile(session: SessionDep, user: CurrentUserDep):
    data = execute_spotify_api_request(
        user.access_token, endpoint="me", method="GET"
    )
    return data


@router.get("/user/top/{type}")
def playlist(type: str, session: SessionDep, user: CurrentUserDep):
    endpoint = f"me/top/{type}"
    playlist_tracks = execute_spotify_api_request(
        user.access_token, endpoint, method="GET"
    )
    return playlist_tracks
