from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.spotify.auth import is_spotify_authenticated
from app.core.database import get_session


class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        spotify_user_id = request.session.get("spotify_user_id")

        if not spotify_user_id:
            request.state.is_authenticated = False
        else:
            # Get token from headers
            token = request.headers.get("Authorization")
            print(f"TOKEN: {token}")
            session = next(get_session())
            # TODO: ADD COMMENTS
            # Check if token from headers matches the one in the database
            if not is_spotify_authenticated(session, spotify_user_id):
                request.state.is_authenticated = False
            else:
                request.state.is_authenticated = True

        response = await call_next(request)
        return response
