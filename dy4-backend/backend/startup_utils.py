import os
import requests
from datetime import datetime, timedelta, timezone
from django.conf import settings


def get_app_access_token(client_id: str, client_secret: str) -> str:
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        auth=(client_id, client_secret),
    )
    response.raise_for_status()
    return response.json()["access_token"]


def calculate_global_playback_start():
    client_id = settings.SPOTIFY_CLIENT_ID
    client_secret = settings.SPOTIFY_CLIENT_SECRET

    access_token = get_app_access_token(client_id, client_secret)
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://api.spotify.com/v1/albums/{settings.DTMF_ALBUM_ID}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()


    tracks = data.get("tracks")["items"]
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