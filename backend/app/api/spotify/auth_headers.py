import base64

from app.core.config import settings


def get_basic_auth_headers() -> dict[str, str]:
    """
    Create basic authentication headers using Spotify client credentials.

    Returns:
        dict[str, str]: A dictionary containing the 'Authorization'
                        and 'Content-Type' headers for basic authentication.
    """
    request_string = (
        settings.spotify_client_id.get_secret_value()
        + ":"
        + settings.spotify_client_secret.get_secret_value()
    )
    encoded_bytes = base64.b64encode(request_string.encode("utf-8"))
    encoded_string = str(encoded_bytes, "utf-8")
    headers = {
        # Format: Authorization: Basic <base64 encoded client_id:client_secret>
        "Authorization": "Basic " + encoded_string,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    return headers


def get_bearer_auth_header(token: str) -> dict[str, str]:
    """
    Create a bearer authorization header using the given token.

    Args:
        token (str): Access token.

    Returns:
        dict[str, str]: A dictionary containing the 'Authorization' header
                        for bearer authentication.
    """
    return {"Authorization": "Bearer " + token}
