FROM python:3.13.3-alpine3.22 AS dev

WORKDIR /app

COPY requirements.txt ./
RUN apk add bash g++

RUN pip install --no-cache-dir dbt-snowflake

COPY . .
