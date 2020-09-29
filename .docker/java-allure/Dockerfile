# openjdk-14-allure-2.13.1
FROM openjdk:14-alpine
ARG ALLURE_VERSION='2.13.1'

RUN wget https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/$ALLURE_VERSION/allure-commandline-${ALLURE_VERSION}.zip \
    && unzip allure-commandline-${ALLURE_VERSION}.zip \
    && rm -fv allure-commandline-${ALLURE_VERSION}.zip

ENV PATH=/app/allure-${ALLURE_VERSION}/bin:$PATH