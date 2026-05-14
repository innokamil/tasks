from airflow.providers.standard.operators.bash import BashOperator 
from airflow.providers.standard.sensors.filesystem import FileSensor
from airflow.sdk import dag, task, task_group
from utils.paths import get_data_file_path
import datetime
import pandas as pd


@dag(dag_id="extract_and_transform",
     start_date=datetime.datetime(2026, 5, 8),
     schedule="@once",
     catchup=False)
def extract_and_transform_dag():
    @task_group(group_id="transform")
    def transform_tg(df_path):
        @task(task_id="replace_characters")
        def replace_characters(df_path):
            df = pd.read_csv(df_path)
            df.fillna("-", inplace=True)
            new_file_path = get_data_file_path("data_replaced_characters.csv")
            df.to_csv(new_file_path)
            return new_file_path

        @task(task_id="sortby_create_date")
        def sortby_create_date(df_path):
            df = pd.read_csv(df_path)
            df['at'] = pd.to_datetime(df['at'])
            df.sort_values(by="at", inplace=True)
            new_file_path = get_data_file_path("data_sorted.csv")
            df.to_csv(new_file_path)
            return new_file_path


        @task(task_id="sanitize_text")
        def sanitize_text(df_path):
            df = pd.read_csv(df_path)
            for col in df.select_dtypes(include=['object']).columns:
                df[col] = df[col].astype(str).str.replace(r'[^\x20-\x7E]', '', regex=True)
            new_file_path = get_data_file_path("data_sanitized.csv")
            df.to_csv(new_file_path)
            return new_file_path

        _replace_characters = replace_characters(df_path)
        _sortby_create_date = sortby_create_date(_replace_characters)
        _sanitize_text = sanitize_text(_sortby_create_date)
        _replace_characters >> _sortby_create_date >> _sanitize_text

    @task.branch(task_id="transform_or_halt_pipeline")
    def transform_or_halt_pipeline(file_path):
        import os
        return "transform" if os.path.getsize(file_path) > 0 else "halt_pipeline"


    unprocessed_data_csv = get_data_file_path("data.csv")
    _wait_for_file = FileSensor(
            task_id="wait_for_file",
            filepath=unprocessed_data_csv,
            fs_conn_id="fs_default",
            poke_interval=5
            ) 

    _halt_pipeline = BashOperator(
            task_id="halt_pipeline",
            bash_command='echo "File is empty"'
            )
    _transform_or_halt_pipeline = transform_or_halt_pipeline(unprocessed_data_csv)
    # Set dependencies
    _wait_for_file >> _transform_or_halt_pipeline
    _transform_tg = transform_tg(unprocessed_data_csv)
    _transform_or_halt_pipeline >> [_halt_pipeline, _transform_tg]
    
extract_and_transform_dag()
