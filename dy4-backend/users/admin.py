from django.contrib import admin
from .models import SpotifyAuth, GlobalPlaybackSchedule

admin.site.register(SpotifyAuth)
admin.site.register(GlobalPlaybackSchedule)