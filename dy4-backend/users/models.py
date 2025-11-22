from django.db import models

class SpotifyAuth(models.Model):
    refresh_token = models.TextField()
    spotify_user_id = models.CharField(max_length=255, unique=True)


class LinkedDevice(models.Model):
    id = models.UUIDField(primary_key=True)
    spotify_account = models.ForeignKey(SpotifyAuth, on_delete=models.CASCADE, null=True, blank=True)


class GlobalPlaybackSchedule(models.Model):
    playback_time = models.DateTimeField()
