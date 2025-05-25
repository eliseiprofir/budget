FROM python:3.10-slim

WORKDIR /app

COPY budget/requirements/base.txt requirements/base.txt
COPY budget/requirements/local.txt requirements/local.txt
COPY budget/requirements/test.txt requirements/test.txt
COPY budget/requirements/production.txt requirements/production.txt

RUN mkdir -p requirements

ARG ENVIRONMENT=production
ENV ENVIRONMENT=${ENVIRONMENT}

RUN if [ "$ENVIRONMENT" = "local" ]; then \
        pip install --no-cache-dir -r requirements/local.txt -r requirements/test.txt ; \
    else \
        pip install --no-cache-dir -r requirements/production.txt ; \
    fi

COPY . .

EXPOSE 8000

CMD sh -c "if [ \"$ENVIRONMENT\" = \"local\" ]; then \
             python budget/manage.py runserver 0.0.0.0:8000 ; \
           else \
             gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} ; \
           fi"