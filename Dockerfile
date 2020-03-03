FROM python:3.7.6-slim-buster
COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN apt-get update && apt-get install -y curl \
    gcc \
    libc-dev \
    wget \
    gnupg2 \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install --no-cache-dir -r requirements.txt
RUN useradd apps -rm -d /home/apps -s /bin/bash -g root -G sudo -u 1000 apps && mkdir -p /home/apps && chown apps:root /home/apps
ENV DISPLAY=:99.0