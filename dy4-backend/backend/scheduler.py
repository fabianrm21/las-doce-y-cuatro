import boto3
import json
from datetime import datetime
from django.conf import settings


def schedule_global_playback(playback_utc_datetime):
    scheduler = boto3.client("scheduler",
                             region_name=settings.AWS_REGION,
                             aws_access_key_id=settings.AWS_ACCESS_KEY,
                             aws_secret_access_key=settings.AWS_SECRET_KEY,)
    schedule_name = f"playback-{int(playback_utc_datetime.timestamp())}"

    response = scheduler.create_schedule(
        Name=schedule_name,
        ScheduleExpression=f"at({playback_utc_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')})",
        FlexibleTimeWindow={"Mode": "OFF"},
        Target={
            "Arn": settings.AWS_API_DEST_ARN,
            "RoleArn": settings.AWS_ROLE_ARN,
            "Input": json.dumps({
                "secret": settings.DTMF_ENDPOINT_KEY,
                "trigger": "global",
            })
        },
        State="ENABLED",
    )

    return response