# python-3.7.6-slim-buster-chrome-85.0.4183.121-1
FROM python:3.7.6-slim-buster

RUN apt-get update && apt-get -y install \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable && rm -rf /var/lib/apt/lists/*