from django.urls import path
from .views import LinkSpotifyAccount, SpotifyCallback, GetPlaybackTime, PlayDTMF

urlpatterns = [
    path("users/link-account/", LinkSpotifyAccount.as_view(), name="link-spotify-account"),
    path("spotify/callback/", SpotifyCallback.as_view(), name="spotify-callback"),
    path("playback-time/", GetPlaybackTime.as_view(), name="get-playback-time"),
    path("play-dtmf/", PlayDTMF.as_view(), name="play-dtmf"),
]
