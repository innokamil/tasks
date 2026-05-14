FROM python:3.14.4-alpine3.22 AS dev

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV DATA_DIRECTORY=/app/data
ENV AIRFLOW_HOME=/app/code/
ENV AIRFLOW_CONN_FS_DEFAULT="file:///?"
ENV AIRFLOW_CONN_MONGO_DEFAULT="mongo://root:root@mongo:27017/"

EXPOSE 8080
CMD ["airflow", "standalone"]
