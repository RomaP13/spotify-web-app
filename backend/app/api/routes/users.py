from fastapi import APIRouter, HTTPException, Request

from app.api.dependencies import SessionDep
from app.api.spotify.request import execute_spotify_api_request
from app.api.spotify.user import get_user_tokens

router = APIRouter()


@router.get("/user/data")
def user_data(request: Request, session: SessionDep):
    user_id = request.cookies.get("session_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    access_token = get_user_tokens(session, user_id).access_token
    data = execute_spotify_api_request(
        access_token, endpoint="me", method="GET"
    )
    return data


@router.get("/user/top/{type}")
def playlist(type: str, request: Request, session: SessionDep):
    if request.state.is_authenticated:
        user_id = request.session.get("spotify_user_id")
        endpoint = f"me/top/{type}"
        access_token = get_user_tokens(session, user_id).access_token
        print(f"ACC: {access_token}")
        playlist_tracks = execute_spotify_api_request(
            access_token, endpoint, method="GET"
        )
        return playlist_tracks
    else:
        return {"message": "Hello, please log in to access more features."}
