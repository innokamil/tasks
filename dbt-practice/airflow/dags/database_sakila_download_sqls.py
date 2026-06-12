import requests
from airflow.sdk import dag, task 
from pathlib import Path
import datetime
from config import (SAKILA_DATA_FILE_LOCATION, SAKILA_SCHEMA_FILE_LOCATION,
                    SAKILA_SCHEMA_FILE_URL, SAKILA_DATA_FILE_URL)


@dag(dag_id="database_sakila_download_sqls",
     start_date=datetime.datetime(2026, 5, 28),
     schedule=None,
     catchup=False)
def database_sakila_download_sqls():
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

    (download_file(SAKILA_SCHEMA_FILE_URL, SAKILA_SCHEMA_FILE_LOCATION) >>
        download_file(SAKILA_DATA_FILE_URL, SAKILA_DATA_FILE_LOCATION)
     )

database_sakila_download_sqls()
