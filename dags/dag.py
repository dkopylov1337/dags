from airflow import DAG
from airflow.operators.empty import EmptyOperator
import pendulum
from airflow.providers.docker.operators.docker import DockerOperator


with DAG(
    dag_id="uplift_model_retraining", 
    default_args={
        "owner": "me",
    },
    schedule_interval="@daily", 
    start_date=pendulum.today('Europe/Moscow').subtract(days=1),
    tags=["uplift_model", "streamlit", "docker"],
    catchup=False,
) as dag:
    start = EmptyOperator(task_id="start")

    train_and_evaluate = DockerOperator(
        task_id="train_and_evaluate_models",
        image="streamlit_homework:latest", 
        docker_url='unix://var/run/docker.sock',
        network_mode="bridge",
        command="streamlit run main.py",  
        auto_remove=True,
    )

    end = EmptyOperator(task_id="end")

    start >> train_and_evaluate >> end
