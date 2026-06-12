from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.providers.standard.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.sdk import dag 
import datetime
from config import AIRBYTE_PAGILA_SYNC_CONN_ID, AIRBYTE_SAKILA_SYNC_CONN_ID


@dag(dag_id="airbyte_replication",
     start_date=datetime.datetime(2026, 5, 28),
     schedule="@daily",
     catchup=False)
def airbyte_replication():
    _sync_pagila = AirbyteTriggerSyncOperator(
        task_id="sync_pagila",
        connection_id=AIRBYTE_PAGILA_SYNC_CONN_ID,
        timeout=3600,
        wait_seconds=3,
    )

    _sync_sakila = AirbyteTriggerSyncOperator(
        task_id="sync_sakila",
        connection_id=AIRBYTE_SAKILA_SYNC_CONN_ID,
        timeout=3600,
        wait_seconds=3,
    )

    # They are independent
    _trigger_model_build = TriggerDagRunOperator(task_id="trigger_model_build", 
                                                 trigger_dag_id="dbt_run_models")
    # Task only specifies models for pagila
    _sync_pagila >> _trigger_model_build
    _sync_sakila

airbyte_replication()
