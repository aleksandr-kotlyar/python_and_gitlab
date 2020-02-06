FROM python:3.7-alpine
COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN apk add --no-cache \
    curl \
    gcc \
    libc-dev

RUN pip3 install --no-cache-dir -r requirements.txt