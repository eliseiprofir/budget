FROM python:3.10-slim

WORKDIR /app

COPY budget/requirements/base.txt requirements/base.txt
COPY budget/requirements/local.txt requirements/local.txt
COPY budget/requirements/test.txt requirements/test.txt
COPY budget/requirements/production.txt requirements/production.txt

RUN mkdir -p requirements

ARG ENVIRONMENT=production
ENV ENVIRONMENT=${ENVIRONMENT}

# Install dependencies based on the environment variable
RUN if [ "$ENVIRONMENT" = "local" ]; then \
        pip install --no-cache-dir -r requirements/local.txt -r requirements/test.txt ; \
    else \
        pip install --no-cache-dir -r requirements/production.txt ; \
    fi

COPY . .

ENV PYTHONPATH=/app/budget:$PYTHONPATH

# Collect static files, run migrations and create a superuser
RUN if [ "$ENVIRONMENT" = "production" ]; then \
        cd budget && python manage.py collectstatic --noinput; \
        cd budget && python manage.py makemigrations; \
        cd budget && python manage.py migrate; \
        cd budget && python manage.py createdefaultsuperuser; \
    fi

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
