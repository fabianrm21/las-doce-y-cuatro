import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dy4-backend.backend.settings')

app = Celery('dy4-backend')

# Load settings from Django settings file, using CELERY_ namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all registered Django app configs
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "play-dtmf": {
        "task": "dy4-backend.users.tasks.play_dtmf",
        "schedule": crontab(minute="*/30"),  # TODO: calculate exact time to start
    }
}