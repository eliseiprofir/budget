#!/bin/bash

# Run migrations
cd budget
echo "Making migrations..."
python manage.py makemigrations --noinput
echo "Migrating..."
python manage.py migrate --noinput

echo "Listing applied migrations:"
python manage.py showmigrations

echo "Creating default superuser if needed..."
python manage.py createdefaultsuperuser

# Pornește aplicația
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000
