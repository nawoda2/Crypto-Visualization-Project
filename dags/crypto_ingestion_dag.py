from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

with DAG(
    "crypto_ingestion_dag",
    default_args=default_args,
    description="Ingest cryptocurrency data into PostgreSQL",
    schedule_interval="@hourly",
    start_date=datetime(2025, 1, 1),
    catchup=False
) as dag:


    run_ingestion = DockerOperator(
        task_id="run_ingestion_container",
        image="ingestion-container:latest",
        force_pull=False,
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="crypto_project_default",
        mount_tmp_dir=False,
    )

    run_ingestion