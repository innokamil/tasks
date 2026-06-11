import os 
from pathlib import Path

# NOTE: The Container [name/image] variables MIGHT be changed to match
# those on the host system 
DBT_CONTAINER_NAME: str = "dbt_instance"
DBT_IMAGE: str = "dbt-practice-dbt-image-instance:latest"
# NOTE: Put there path on your local system where the .dbt catalog is
DBT_DEFAULT_CREDENTIALS_LOCATION: Path = Path("/home/innowise/.dbt")
# NOTE: Sync connection ids MUST be changed to match those on the host system
AIRBYTE_PAGILA_SYNC_CONN_ID: str = "90161709-31dd-4b0f-b24a-7a27a517983a"
AIRBYTE_SAKILA_SYNC_CONN_ID: str = "15ed00a9-caeb-4c08-ae41-dd9818355d98"

SQL_PAGILA_FILES_LOCATION: Path = Path(os.getenv("SQL_PAGILA_FILES", ""))
PAGILA_SCHEMA_FILE_URL = "https://raw.githubusercontent.com/devrimgunduz/pagila/refs/heads/master/pagila-schema.sql"
PAGILA_DATA_FILE_URL = "https://raw.githubusercontent.com/devrimgunduz/pagila/refs/heads/master/pagila-insert-data.sql"

SQL_SAKILA_FILES_LOCATION: Path = Path(os.getenv("SQL_SAKILA_FILES", ""))
SAKILA_SCHEMA_FILE_URL = "https://raw.githubusercontent.com/jOOQ/sakila/refs/heads/main/postgres-sakila-db/postgres-sakila-schema.sql"
SAKILA_DATA_FILE_URL = "https://raw.githubusercontent.com/jOOQ/sakila/refs/heads/main/postgres-sakila-db/postgres-sakila-insert-data.sql"

SQL_SCHEMA_EXISTS_QUERY: str = """SELECT NOT EXISTS (
SELECT 1 FROM information_schema.tables 
WHERE table_schema = 'public');
"""
