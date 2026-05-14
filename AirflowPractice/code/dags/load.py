from airflow.providers.mongo.hooks.mongo import MongoHook
from airflow.providers.standard.sensors.external_task import ExternalTaskSensor
from airflow.sdk import dag, task
from airflow.sdk.definitions.asset import Dataset
from utils.paths import get_data_file_path
import datetime
import pandas as pd

_schedule = Dataset(f"file://{get_data_file_path("data_sanitized.csv")}")

@dag(dag_id="load",
     start_date=datetime.datetime(2026, 5, 8), 
     schedule=_schedule,
     catchup=False)
def load_dag():
    @task(task_id="load_into_mongo")
    def load_into_mongo(ti=None):
        path = ti.xcom_pull(
                dag_id='extract_and_transform', 
                task_ids='transform.sanitize_text',
                include_prior_dates=True 
                )[0]
        df = pd.read_csv(path)
        data_dict = df.to_dict(orient='records')
        hook = MongoHook(mongo_conn_id='mongo_default')
        hook.insert_many(
                mongo_collection='reviews',
                docs=data_dict,
                mongo_db='airflow_data')

    load_into_mongo()

load_dag()
