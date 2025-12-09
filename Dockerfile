# Use a lightweight Python base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only backend code and install dependencies
COPY dy4-backend/ /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Collect static files for Django admin and other apps
RUN python manage.py collectstatic --noinput

# Apply migrations
RUN python manage.py makemigrations
RUN python manage.py migrate --run-syncdb
RUN python manage.py create_global_schedule

# Expose port 8000 (to match your Django setup)
EXPOSE 8000

# Run the Django app with Gunicorn and WhiteNoise
# CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
CMD ["bash", "-c", "python manage.py startup_script && gunicorn backend.wsgi:application --bind 0.0.0.0:8000"]
