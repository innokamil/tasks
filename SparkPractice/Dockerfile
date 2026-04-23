FROM apache/spark AS base 
WORKDIR /code
ENV PYTHONBUFFERED=1

RUN curl -s https://jdbc.postgresql.org/download/postgresql-42.7.2.jar \
      -o /opt/spark/jars/postgresl-42.7.2.jar

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

FROM base as dev
