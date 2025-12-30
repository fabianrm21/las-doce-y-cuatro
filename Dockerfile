# Use a lightweight Python base image
# FROM python:3.12-slim

# # Set the working directory inside the container
# WORKDIR /app

# # Copy only backend code and install dependencies
# COPY dy4-backend/ /app/

# # Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Collect static files for Django admin and other apps
# RUN python manage.py collectstatic --noinput

# # Apply migrations
# RUN python manage.py makemigrations
# RUN python manage.py migrate --run-syncdb
# # RUN python manage.py create_global_schedule

# # Expose port 8000 (to match your Django setup)
# EXPOSE 8000

# # Run the Django app with Gunicorn and WhiteNoise
# # CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
# CMD ["bash", "-c", "python manage.py create_global_schedule && gunicorn backend.wsgi:application --bind 0.0.0.0:8000"]




# Use a lightweight Python base image
# FROM python:3.12-slim

# # Set the working directory
# WORKDIR /app

# # Copy backend code into the container
# COPY dy4-backend/ /app/

# # Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Collect static files
# RUN mkdir -p /app/static
# RUN python manage.py collectstatic --noinput

# # Copy entrypoint and give it execute permissions
# COPY dy4-backend/entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh

# # Expose Django/Gunicorn port
# EXPOSE 8000

# # Use entrypoint to run migrations + schedule creation
# ENTRYPOINT ["/entrypoint.sh"]

# # Run gunicorn
# CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]



FROM python:3.12-slim

WORKDIR /app

COPY dy4-backend/ /app/

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/static
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
