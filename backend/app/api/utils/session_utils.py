import hashlib
import os
import uuid

from fastapi import HTTPException, Request


def generate_secure_session_id() -> uuid.UUID:
    """Generates a cryptographically secure, random session ID as a hex string.

    Returns:
        UUID: The generated session ID.
    """
    return uuid.uuid4()


def get_user_session_id(request: Request) -> uuid.UUID:
    """Retrieves the user session ID from the request cookies.

    Args:
        request (Request): The FastAPI request object.

    Returns:
        UUID: The user session ID.

    Raises:
        HTTPException: If the user session ID is not found in the request cookies.
    """
    user_session_id = request.cookies.get("user_session_id")
    if not user_session_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return uuid.UUID(user_session_id)


def generate_state_token() -> str:
    """Generate a secure state token.

    Returns:
        str: The generated state token.
    """
    state = hashlib.sha256(os.urandom(1024)).hexdigest()
    return state
