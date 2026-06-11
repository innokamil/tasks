FROM python:3.14.4-alpine3.22 AS dev
WORKDIR /app

COPY requirements.txt ./
RUN apk add bash curl
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV DATA_DIRECTORY=/app/data
ENV AIRFLOW_HOME=/app
ENV SQL_PAGILA_FILES=${DATA_DIRECTORY}/pagila
ENV SQL_SAKILA_FILES=${DATA_DIRECTORY}/sakila
ENV AIRFLOW_CONN_FS_DEFAULT="file:///?"
ENV AIRFLOW_CONN_SAKILA_DEFAULT="postgresql://postgres:root@sakila-db:5432/sakila"
ENV AIRFLOW_CONN_PAGILA_DEFAULT="postgresql://postgres:postgres@pagila-db:5432/pagila"


EXPOSE 8080
CMD ["airflow", "standalone"]
