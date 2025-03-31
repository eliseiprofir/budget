FROM python:3.10-slim

WORKDIR /app

COPY budget/requirements/base.txt requirements/base.txt
COPY budget/requirements/local.txt requirements/local.txt
RUN mkdir -p requirements
RUN pip install -r requirements/local.txt

COPY . .

EXPOSE 8000

CMD ["python", "budget/manage.py", "runserver", "0.0.0.0:8000"]
