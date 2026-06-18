ARG ALLURE_VERSION=2.43.0

FROM python:3.14-alpine AS compile-image

WORKDIR /app
RUN apk --no-cache add \
    gcc \
    libc-dev \
    && rm -rf /var/cache/apk/*

COPY requirements.txt /app/requirements.txt
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"
RUN python -m venv "${VIRTUAL_ENV}"
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

FROM python:3.14-alpine AS build-image
ARG ALLURE_VERSION
COPY --from=compile-image /opt/venv /opt/venv

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"

RUN apk --no-cache add \
    git \
    openjdk25-jre-headless \
    curl \
    && rm -rf /var/cache/apk/*

RUN wget https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/${ALLURE_VERSION}/allure-commandline-${ALLURE_VERSION}.tgz
RUN tar -zxf allure-commandline-${ALLURE_VERSION}.tgz
RUN rm allure-commandline-${ALLURE_VERSION}.tgz
ENV PATH="/allure-${ALLURE_VERSION}/bin:${PATH}"

WORKDIR /app
