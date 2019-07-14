FROM python:3.7-alpine
COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN apk --no-cache add curl && \
    pip install --no-cache-dir -r requirements.txt