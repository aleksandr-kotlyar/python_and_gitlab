FROM python:3.7.6-alpine
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN apk --no-cache add curl \
    gcc \
    libc-dev \
    && pip3 install --no-cache-dir -r requirements.txt
