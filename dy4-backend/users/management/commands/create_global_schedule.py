from django.core.management.base import BaseCommand
from django.conf import settings
from backend.startup_utils import calculate_global_playback_start
from users.models import GlobalPlaybackSchedule


class Command(BaseCommand):
    help = "Create the one-time global EventBridge schedule for DTMF playback"

    def handle(self, *args, **options):
        playback_utc = calculate_global_playback_start()
        GlobalPlaybackSchedule.objects.create(
            playback_time=playback_utc,
        )
        self.stdout.write(f"Schedule global playback at {playback_utc.isoformat()}")