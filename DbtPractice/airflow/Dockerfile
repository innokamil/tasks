FROM python:3.14.4-alpine3.22 AS dev
WORKDIR /app

COPY requirements.txt ./
RUN apk add bash
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV DATA_DIRECTORY=/app/data
ENV AIRFLOW_HOME=/app/code
ENV AIRFLOW_CONN_FS_DEFAULT="file:///?"
ENV AIRFLOW_CONN_SAKILA_DEFAULT="postgresql://postgres:root@sakila-db:5432/sakila"
ENV AIRFLOW_CONN_PAGILA_DEFAULT="postgresql://postgres:postgres@pagila-db:5432/pagila"
ENV SQL_FILES_SAKILA=${DATA_DIRECTORY}/sakila
ENV SQL_FILES_PAGILA=${DATA_DIRECTORY}/pagila

EXPOSE 8080
CMD ["airflow", "standalone"]
