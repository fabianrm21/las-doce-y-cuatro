import boto3
import json
from datetime import timezone
from django.conf import settings


def schedule_global_playback(playback_utc_datetime, target_url: str):
    scheduler = boto3.client("scheduler",
                             region_name=settings.AWS_REGION,
                             aws_access_key=settings.AWS_ACCESS_KEY,
                             aws_secret_access_key=settings.AWS_SECRET_KEY,
                             )
    schedule_name = f"play-dtmf-{int(playback_utc_datetime.timestamp())}"

    response = scheduler.create_schedule(
        Name=schedule_name,
        ScheduleExpression=f"at({playback_utc_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')})",
        FlexibleTimeWindow={"Mode": "OFF"},
        Target={
            "Arn": target_url,
            "RoleArn": settings.AWS_ROLE_ARN,
            "Input": json.dumps({"trigger": "global"}),
            "HttpParameters": {
                "HeaderParameters": {},
                "Body": json.dumps({"trigger": "global"}),
            },
        },
        State="ENABLED",
    )

    return response