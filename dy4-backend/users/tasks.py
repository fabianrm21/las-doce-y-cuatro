from celery import shared_task
from .models import SpotifyAuth

@shared_task
def play_dtmf():
    users = SpotifyAuth.objects.all()
    for user in users:
        # make request to get access token
        # use access token to make request to player
        # TODO: make sure this won't cause issues with rate-limiting
        pass
    return