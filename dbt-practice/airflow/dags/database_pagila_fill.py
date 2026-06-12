from pathlib import Path
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.standard.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.sdk import dag, task 
import datetime
from config import PAGILA_DATA_FILE_LOCATION, PAGILA_SCHEMA_FILE_LOCATION


@dag(dag_id="database_pagila_fill",
     start_date=datetime.datetime(2026, 5, 28),
     schedule="@once",
     catchup=False)
def database_pagila_fill():
    @task(task_id="run_sql")
    def run_sql(db_conn_id: str, sql_filepath: str | Path):
        db_hook = PostgresHook(db_conn_id)
        with open(sql_filepath, "r") as file:
            sql = file.read()
        db_hook.run(sql)

    _trigger_download_sqls = TriggerDagRunOperator(task_id="download_sqls", 
                                                   trigger_dag_id="database_pagila_download_sqls")

    # Pagila
    (_trigger_download_sqls >> 
        run_sql("pagila_default", PAGILA_SCHEMA_FILE_LOCATION) >>
        run_sql("pagila_default", PAGILA_DATA_FILE_LOCATION)
     )

database_pagila_fill()
