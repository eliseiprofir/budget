#!/bin/bash

# Run migrations
cd budget
python manage.py makemigrations
python manage.py migrate

# Create default superuser
python manage.py createdefaultsuperuser

# Pornește aplicația
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000