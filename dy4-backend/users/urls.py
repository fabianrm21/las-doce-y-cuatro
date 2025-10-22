from django.urls import path
from .views import LinkSpotifyAccount, SpotifyCallback

urlpatterns = [
    path("link-account/", LinkSpotifyAccount.as_view(), name="link-spotify-account"),
    path("spotify/callback/", SpotifyCallback.as_view(), name="spotify-callback"),
]
