FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Set environment variable (default: local)
ARG ENVIRONMENT=local
ENV ENVIRONMENT=${ENVIRONMENT}

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
