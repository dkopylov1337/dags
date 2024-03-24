from airflow import DAG
from airflow.operators.docker_operator import DockerOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 24),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


dag = DAG(
    'uplift_model_retraining',
    default_args=default_args,
    description='Daily retraining of uplift models',
    schedule_interval=timedelta(days=1),
)


t1 = DockerOperator(
    task_id='train_uplift_model',
    image='streamlit_homework:latest',
    api_version='auto',
    auto_remove=True,
    command='python main.py',
    docker_url='unix://var/run/docker.sock',
    network_mode='bridge',
    dag=dag
)

t1
