FROM python:3.7.6-alpine
WORKDIR /app
RUN apk --no-cache -U add curl \
    gcc \
    libc-dev \
    libcrypto1.1=1.1.1g-r0 \
    libssl1.1=1.1.1g-r0 \
    sqlite-libs=3.30.1-r2
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
