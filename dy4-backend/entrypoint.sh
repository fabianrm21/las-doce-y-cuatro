#!/bin/sh

python manage.py makemigrations
python manage.py migrate --run-syncdb
python manage.py create_global_schedule
python manage.py createsuperuser --noinput --username "$DJANGO_SUPERUSER_USERNAME" --email "$DJANGO_SUPERUSER_EMAIL" || true

exec "$@"
