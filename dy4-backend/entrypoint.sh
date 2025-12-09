#!/bin/sh

python manage.py migrate --noinput
python manage.py create_global_schedule

exec "$@"
