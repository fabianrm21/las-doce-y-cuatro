from django.core.management.base import BaseCommand
from django.conf import settings
from backend.startup_utils import calculate_global_playback_start
from backend.scheduler import schedule_global_playback
from users.models import GlobalPlaybackSchedule
import json


class Command(BaseCommand):
    help = "Create the one-time global EventBridge schedule for DTMF playback"

    def handle(self, *args, **options):
        playback_utc = calculate_global_playback_start()
        schedule_name = f"play-dtmf-global"
        if GlobalPlaybackSchedule.objects.filter(schedule_name=schedule_name).exists():
            self.stdout.write("Schedule already exists. Skipping.")
            return
        
        target_url = f"{settings.CALLBACK_URL}/play-dtmf/"
        response = schedule_global_playback(playback_utc, target_url)
        schedule_arn = response.get("ScheduleArn") or response.get("Arn") or response
        GlobalPlaybackSchedule.objects.create(
            schedule_name=schedule_name,
            schedule_arn=schedule_arn if isinstance(schedule_arn, str) else json.dumps(schedule_arn),
            playback_time=playback_utc,
        )
        self.stdout.write(f"Schedule global playback at {playback_utc.isoformat()}")