from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import subprocess
import sys
import os

# Add the tests directory to the Python path
sys.path.append('/opt/airflow/tests')

def run_tests():
    subprocess.run(["pytest", "/opt/airflow/tests"], check=True, shell=True)

default_args = {
    'owner': 'admin',
    'depends_on_past': False,
    'start_date': datetime(2024, 5, 16),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

my_dag = DAG(
    dag_id='unit_tests',
    description='runs unit tests',
    tags=['unit_tests'],
    schedule_interval='0 0-23/4 * * *',
    default_args={
        'owner': 'airflow',
        'start_date': days_ago(0, minute=1),
    }
)

task_1 = PythonOperator(
    task_id='run_tests',
    python_callable=run_tests,
    dag=my_dag
)