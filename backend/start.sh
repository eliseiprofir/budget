#!/bin/bash

# Run migrations
cd budget
python manage.py makemigrations
python manage.py migrate
python manage.py migrate django_q

# Collect static files
python manage.py collectstatic --noinput

# Create default superuser
python manage.py createdefaultsuperuser

# (Re)Create demo user
python manage.py cleardemo
python manage.py seeddemo

# Start command
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000