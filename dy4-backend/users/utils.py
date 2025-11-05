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
    # disabling shuffle
    shuffle_url = "https://api.spotify.com/v1/me/player/shuffle?state=false"
    requests.put(shuffle_url, headers={"Authorization": f"Bearer {access_token}"})


    url = "https://api.spotify.com/v1/me/player/play"
    headers = {"Authorization": f"Bearer {access_token}",
               "Content-Type": "application/json"}
    data = {"context_uri": f"spotify:album:{settings.DTMF_ALBUM_ID}",
            "position_ms": 0}

    response = requests.put(url, headers=headers, json=data)


def calculate_playback_time(refresh_token: str):
    access_token = get_valid_token(refresh_token)

    url = f"https://api.spotify.com/v1/albums/{settings.DTMF_ALBUM_ID}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    response_dict = response.json()

    # print("response from getting dtmf:", response_dict)

    tracks = response_dict.get("tracks")["items"]
    total_duration = 0
    for track in tracks:
        if track["name"] == "PIToRRO DE COCO":
            # only add the time until the magic words (53 seconds in)
            total_duration += 53000 
            break
        total_duration += track["duration_ms"]


    ast = timezone(timedelta(hours=-4))
    las_doce_y_cuatro_ast = datetime(2026, 1, 1, 0, 4, 0, tzinfo=ast)  # January 1st, 2026, 12:04 AM

    playback_time = las_doce_y_cuatro_ast - timedelta(milliseconds=total_duration)
    return playback_time