from django.db import models

class SpotifyAuth(models.Model):
    device_id = models.UUIDField()
    refresh_token = models.TextField()
    spotify_user_id = models.CharField(max_length=255, unique=True)