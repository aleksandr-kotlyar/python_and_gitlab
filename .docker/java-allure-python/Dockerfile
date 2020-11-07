FROM openjdk:14-alpine

ARG ALLURE_VERSION=2.13.6

RUN apk --no-cache add \
    curl \
    gcc \
    libc-dev \
    unzip \
    && wget https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/${ALLURE_VERSION}/allure-commandline-${ALLURE_VERSION}.zip \
    && unzip allure-commandline-${ALLURE_VERSION}.zip \
    && rm -fv allure-commandline-${ALLURE_VERSION}.zip
ENV PATH=/allure-${ALLURE_VERSION}/bin:$PATH

COPY --from=python:3.7-alpine / /
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt