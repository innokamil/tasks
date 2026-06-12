from airflow.sdk import dag 
from docker.types import Mount
from airflow.providers.docker.operators.docker import DockerOperator
import datetime
from config import DBT_CONTAINER_NAME, DBT_DEFAULT_CREDENTIALS_LOCATION, DBT_IMAGE


@dag(dag_id="dbt_run_models",
     start_date=datetime.datetime(2026, 5, 28),
     schedule=None,
     catchup=False)
def dbt_run_models():
    dbt_instance_op = DockerOperator(task_id="dbt_run",
                                     image=DBT_IMAGE,
                                     container_name=DBT_CONTAINER_NAME,
                                     working_dir='/app/pagila_analytics', 
                                     command='dbt run',
                                     auto_remove="force", # <-- cleans up the container
                                     mounts=[Mount(
                                     source=str(DBT_DEFAULT_CREDENTIALS_LOCATION),
                                     target='/root/.dbt',        
                                     type='bind')])

    dbt_instance_op

dbt_run_models()

