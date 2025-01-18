from uuid import UUID

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.spotify.auth import is_spotify_authenticated
from app.core.database import get_session


class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        user_session_id_str = request.cookies.get("user_session_id")

        if user_session_id_str:
            try:
                # Attempt to convert the string to a UUID
                user_session_id = UUID(user_session_id_str)
                session = next(get_session())
                if is_spotify_authenticated(session, user_session_id):
                    request.state.user_session_id = user_session_id
            except ValueError:
                # Handle the invalid UUID format
                print("Invalid session_id format.")

        response = await call_next(request)
        return response
