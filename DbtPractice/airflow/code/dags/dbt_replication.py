from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.sdk import dag 
import datetime


@dag(dag_id="airbyte_replication",
     start_date=datetime.datetime(2026, 5, 28),
     schedule="@daily",
     catchup=False)
def airbyte_replication():
    sync_pagila = AirbyteTriggerSyncOperator(
        task_id="sync_pagila",
        connection_id="90161709-31dd-4b0f-b24a-7a27a517983a",
        timeout=3600,
        wait_seconds=3,
    )

    sync_sakila = AirbyteTriggerSyncOperator(
        task_id="sync_sakila",
        connection_id="15ed00a9-caeb-4c08-ae41-dd9818355d98",
        timeout=3600,
        wait_seconds=3,
    )

    # They are independent
    sync_pagila
    sync_sakila

airbyte_replication()






