from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from script.clean_webscraped import clean_webscraped_data
from script.extract_market_value import extract_mv
from script.extract_matches import extract_matches
from script.load_to_sql import load_joined_tables_to_sql
from script.transform_jointables import join_tables
from script.transform_nameconsistency import transform_tables
from script.webscrape import scrape_premier_league_data

default_args = {
    'owner': 'your_name',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'all_scripts_dag',
    default_args=default_args,
    description='DAG for running all scripts',
    schedule_interval=timedelta(days=1),  # Adjust the schedule interval as needed
)

task_clean_webscraped = PythonOperator(
    task_id='task_clean_webscraped',
    python_callable=clean_webscraped_data,
    dag=dag,
)

task_extract_market_value = PythonOperator(
    task_id='task_extract_market_value',
    python_callable=extract_mv,
    dag=dag,
)

task_extract_matches = PythonOperator(
    task_id='task_extract_matches',
    python_callable=extract_matches,
    dag=dag,
)

task_load_to_sql = PythonOperator(
    task_id='task_load_to_sql',
    python_callable=load_joined_tables_to_sql,
    dag=dag,
)

task_transform_jointables = PythonOperator(
    task_id='task_transform_jointables',
    python_callable=join_tables,
    dag=dag,
)

task_transform_nameconsistency = PythonOperator(
    task_id='task_transform_nameconsistency',
    python_callable=transform_tables,
    dag=dag,
)

task_webscrape = PythonOperator(
    task_id='task_webscrape',
    python_callable=scrape_premier_league_data,
    dag=dag,
)

# Set up task dependencies if applicable
task_webscrape >> task_clean_webscraped
task_clean_webscraped >> task_transform_nameconsistency
task_extract_matches >> task_transform_nameconsistency
task_extract_market_value >> task_transform_nameconsistency
task_transform_nameconsistency >> task_transform_jointables
task_transform_jointables >> task_load_to_sql