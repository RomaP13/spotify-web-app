import hashlib
import os
import uuid

from fastapi import HTTPException, Request


def generate_secure_session_id() -> uuid.UUID:
    """Generates a cryptographically secure, random session ID as a hex string."""
    return uuid.uuid4()


def get_user_session_id(request: Request) -> uuid.UUID:
    user_session_id = getattr(request.state, "user_session_id", None)
    if not user_session_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user_session_id


def generate_state_token():
    """
    Generate a secure state token.

    Returns:
        str: The generated state token.
    """
    state = hashlib.sha256(os.urandom(1024)).hexdigest()
    return state
