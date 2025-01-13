import requests

from app.api.spotify.auth_headers import get_bearer_auth_header


def execute_spotify_api_request(
    access_token: str, endpoint: str, method: str
) -> dict:
    BASE_URL = "https://api.spotify.com/v1/"
    headers = get_bearer_auth_header(access_token)

    if method.upper() == "GET":
        response = requests.get(BASE_URL + endpoint, headers=headers)
    elif method.upper() == "POST":
        response = requests.post(BASE_URL + endpoint, headers=headers)

    return response.json()
