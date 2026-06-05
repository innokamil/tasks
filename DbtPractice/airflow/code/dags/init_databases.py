import os
from airflow.providers.common.sql.operators.sql import BranchSQLOperator, SQLExecuteQueryOperator 
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import dag 
import datetime

SQL_FILES_PAGILA_PATH: str = os.getenv("SQL_FILES_PAGILA", "")
SQL_FILES_SAKILA_PATH: str = os.getenv("SQL_FILES_SAKILA", "")
SQL_SCHEMA_EXISTS_QUERY: str = """SELECT NOT EXISTS (
SELECT 1 FROM information_schema.tables 
WHERE table_schema = 'public');
"""

@dag(dag_id="init_databases",
     start_date=datetime.datetime(2026, 5, 28),
     schedule="@once",
     template_searchpath=[SQL_FILES_PAGILA_PATH, SQL_FILES_SAKILA_PATH],
     catchup=False)
def init_databases():
    # Determines whether Postgres database should initialize Pagila data
    branch_pagila_init = BranchSQLOperator(
            task_id="branch_pagila_init",
            conn_id="pagila_default",
            sql=SQL_SCHEMA_EXISTS_QUERY,
            follow_task_ids_if_true=["initialize_pagila_schema"], 
            follow_task_ids_if_false=["skip_pagila_init"])

    initialize_pagila_schema = SQLExecuteQueryOperator(
            task_id="initialize_pagila_schema",
            conn_id="pagila_default",
            sql=[
                "pagila-schema.sql",
                "pagila-data.sql",
                ], 
            )

    # Determines whether Postgres database should initialize Sakila data
    branch_sakila_init = BranchSQLOperator(
            task_id="branch_sakila_init",
            conn_id="sakila_default",
            sql=SQL_SCHEMA_EXISTS_QUERY,
            follow_task_ids_if_true=["initialize_sakila_schema"], 
            follow_task_ids_if_false=["skip_sakila_init"])


    initialize_sakila_schema = SQLExecuteQueryOperator(
            task_id="initialize_sakila_schema",
            conn_id="sakila_default",
            sql=[
                "sakila-schema.sql",
                "sakila-data.sql",
                ], 
            )
    skip_pagila_init = BashOperator(task_id="skip_pagila_init",
                                    bash_command="echo Pagila data has been already initialized")

    skip_sakila_init = BashOperator(task_id="skip_sakila_init",
                                    bash_command="echo Sakila data has been already initialized")
    branch_pagila_init >> [initialize_pagila_schema, skip_pagila_init]
    branch_sakila_init >> [initialize_sakila_schema, skip_sakila_init]


init_databases()

