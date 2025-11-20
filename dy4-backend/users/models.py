from django.db import models

class SpotifyAuth(models.Model):
    # device_id = models.UUIDField()
    refresh_token = models.TextField()
    spotify_user_id = models.CharField(max_length=255, unique=True)


class LinkedDevice(models.Model):
    id = models.UUIDField(primary_key=True)
    spotify_account = models.ForeignKey(SpotifyAuth, on_delete=models.CASCADE, null=True, blank=True)


class GlobalPlaybackSchedule(models.Model):
    schedule_name = models.CharField(max_length=200, unique=True)
    schedule_arn = models.CharField(max_length=512)
    playback_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)