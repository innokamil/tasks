from pathlib import Path
from airflow.providers.common.sql.operators.sql import BranchSQLOperator, SQLExecuteQueryOperator 
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.standard.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.sdk import dag, task 
import datetime
from config import SQL_PAGILA_FILES_LOCATION, SQL_SAKILA_FILES_LOCATION



@dag(dag_id="databases_fill",
     start_date=datetime.datetime(2026, 5, 28),
     schedule="@once",
     catchup=False)
def databases_fill():
    @task(task_id="run_sql")
    def run_sql(db_conn_id: str, sql_filepath: str | Path):
        db_hook = PostgresHook(db_conn_id)
        with open(sql_filepath, "r") as file:
            sql = file.read()
        db_hook.run(sql)

    # Pagila
    _trigger_download_sqls = TriggerDagRunOperator(task_id="download_sqls", 
                                                   trigger_dag_id="databases_download_sql")
    (_trigger_download_sqls >> 
        run_sql("pagila_default",
                SQL_PAGILA_FILES_LOCATION.joinpath("pagila-schema.sql")) >>
        run_sql("pagila_default",
                SQL_PAGILA_FILES_LOCATION.joinpath("pagila-data.sql")))

    # Sakila
    (_trigger_download_sqls >> run_sql("sakila_default",
             SQL_SAKILA_FILES_LOCATION.joinpath("sakila-schema.sql")) >>
        run_sql("sakila_default",
                SQL_SAKILA_FILES_LOCATION.joinpath("sakila-data.sql")))



databases_fill()

