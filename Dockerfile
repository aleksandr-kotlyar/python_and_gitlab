FROM python:3.7.6-slim-buster
COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN apt-get update && apt-get -y install \
    curl \
    gcc \
    libc-dev \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir -r requirements.txt

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable && rm -rf /var/lib/apt/lists/*

RUN adduser apps -system -disabled-password -shell /bin/bash -ingroup sudo && mkdir -p /home/apps && chown apps:root /home/apps
ENV DISPLAY=:99.0
