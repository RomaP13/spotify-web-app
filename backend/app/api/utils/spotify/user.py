import requests


def get_user_id(access_token: str) -> str:
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://api.spotify.com/v1/me", headers=headers)
    return response.json().get("id")
