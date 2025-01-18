import requests
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from app.api.dependencies import SessionDep
from app.api.spotify.auth_headers import get_basic_auth_headers
from app.api.spotify.user import update_or_create_user_tokens
from app.api.utils.session_utils import generate_secure_session_id
from app.core.config import settings
from app.models import SpotifyTokenData

router = APIRouter()


@router.get("/callback")
def callback(request: Request, session: SessionDep):
    code = request.query_params.get("code")
    state = request.query_params.get("state")
    session_state = request.session.get("state")

    if state != session_state:
        return {"error": "State mismatch"}, 400

    token_url = "https://accounts.spotify.com/api/token"
    headers = get_basic_auth_headers()
    form_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.redirect_uri,
    }

    api_response = requests.post(token_url, data=form_data, headers=headers)
    if api_response.status_code == 200:
        user_session_id = generate_secure_session_id()
        user_session_id_str = str(user_session_id)
        token_data = SpotifyTokenData(**api_response.json())
        update_or_create_user_tokens(session, token_data, user_session_id)

        # Set HTTP-only cookie
        response = RedirectResponse("http://localhost:5173/")
        response.set_cookie(
            key="user_session_id",
            value=user_session_id_str,
            httponly=True,
            secure=False,
            samesite="lax",
        )
        return response
