from fastapi import APIRouter, Request

from app.api.dependencies import SessionDep
from app.api.spotify.request import execute_spotify_api_request
from app.api.spotify.user import get_user_tokens

router = APIRouter()


@router.get("/playlist/{playlist_id}")
def playlist(playlist_id: str, request: Request, session: SessionDep):
    if request.state.is_authenticated:
        user_id = request.session.get("spotify_user_id")
        endpoint = f"playlists/{playlist_id}/tracks"
        access_token = get_user_tokens(session, user_id).access_token
        print(f"ACC: {access_token}")
        playlist_tracks = execute_spotify_api_request(
            access_token, endpoint, method="GET"
        )
        return playlist_tracks
    else:
        return {"message": "Hello, please log in to access more features."}
