import requests
from airflow.sdk import dag, task 
from pathlib import Path
import datetime
from config import (PAGILA_SCHEMA_FILE_URL, PAGILA_DATA_FILE_URL,
                    SAKILA_SCHEMA_FILE_URL, SAKILA_DATA_FILE_URL,
                    SQL_PAGILA_FILES_LOCATION, SQL_SAKILA_FILES_LOCATION)

@dag(dag_id="databases_download_sql",
     start_date=datetime.datetime(2026, 5, 28),
     schedule=None,
     catchup=False)
def databases_download_sqls():
    @task(task_id="download_file")
    def download_file(url: str, save_location: str | Path):
        try:
            response = requests.get(url)
            match response.status_code:
                case 200:
                    with open(save_location, 'wb') as file:
                        file.write(response.content)
                case _:
                    print("Download failed.")
        except Exception as e:
            print(f"Error: {e}")

    (download_file(PAGILA_SCHEMA_FILE_URL,
                   SQL_PAGILA_FILES_LOCATION.joinpath("pagila-schema.sql")) >> 
        download_file(PAGILA_DATA_FILE_URL,
                      SQL_PAGILA_FILES_LOCATION.joinpath("pagila-data.sql")))

    (download_file(SAKILA_SCHEMA_FILE_URL,
                   SQL_SAKILA_FILES_LOCATION.joinpath("sakila-schema.sql")) >>
        download_file(SAKILA_DATA_FILE_URL,
                      SQL_SAKILA_FILES_LOCATION.joinpath("sakila-data.sql")))


databases_download_sqls()

