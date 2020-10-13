FROM openjdk:14-alpine

ARG ALLURE_VER=2.13.6
COPY --from=python:3.7-alpine / /
COPY requirements.txt /app/requirements.txt
COPY allure-$ALLURE_VER /
ENV PATH=/allure-$ALLURE_VER/bin:$PATH

WORKDIR /app
RUN apk --no-cache add curl \
    gcc \
    libc-dev \
    unzip \
    && pip install --no-cache-dir -r requirements.txt