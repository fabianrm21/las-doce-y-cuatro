from .models import SpotifyAuth
from django.conf import settings
import requests
import base64
from datetime import datetime, timedelta, timezone


def get_valid_token(refresh_token: str):
    token_url = "https://accounts.spotify.com/api/token"
    auth_str = f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    headers = {"Authorization": f"Basic {b64_auth_str}"}
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }

    r = requests.post(token_url, data=data, headers=headers)
    tokens = r.json()
    access_token = tokens.get("access_token")
    return access_token


def play_dtmf_api_call(user: SpotifyAuth, access_token: str):
    # TODO: especificar en el ui que tienen que tener el queue vacío

    # disabling shuffle
    shuffle_url = "https://api.spotify.com/v1/me/player/shuffle?state=false"
    requests.put(shuffle_url, headers={"Authorization": f"Bearer {access_token}"})


    url = "https://api.spotify.com/v1/me/player/play"
    headers = {"Authorization": f"Bearer {access_token}",
               "Content-Type": "application/json"}
    data = {"context_uri": f"spotify:album:{settings.DTMF_ALBUM_ID}",
            "position_ms": 0}

    response = requests.put(url, headers=headers, json=data)