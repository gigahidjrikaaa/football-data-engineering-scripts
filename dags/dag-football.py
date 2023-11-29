from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator

# Import your scripts
from script.clean_webscraped import clean_webscraped_data
from script.extract_market_value import extract_mv
from script.extract_matches import extract_matches
from script.load_to_sql import load_joined_tables_to_sql
from script.transform_jointables import tr_join_tables
from script.transform_nameconsistency import tr_name_consistency
from script.webscrape import scrape_premier_league_data

# Define default_args dictionary to specify the default parameters for the DAG
default_args = {
    'owner': 'your_name',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Instantiate a DAG
dag = DAG(
    'your_dag_id',
    default_args=default_args,
    description='Your DAG description',
    schedule_interval='@daily',  # Set the schedule interval for your DAG
)

# Define tasks using PythonOperator for each script
clean_webscraped_task = PythonOperator(
    task_id='clean_webscraped',
    python_callable=clean_webscraped_data,
    dag=dag,
)

extract_market_value_task = PythonOperator(
    task_id='extract_market_value',
    python_callable=extract_mv,
    dag=dag,
)

extract_matches_task = PythonOperator(
    task_id='extract_matches',
    python_callable=extract_matches,
    dag=dag,
)

load_to_sql_task = PythonOperator(
    task_id='load_to_sql',
    python_callable=load_joined_tables_to_sql,
    dag=dag,
)

transform_jointables_task = PythonOperator(
    task_id='transform_jointables',
    python_callable=tr_join_tables,
    dag=dag,
)

transform_nameconsistency_task = PythonOperator(
    task_id='transform_nameconsistency',
    python_callable=tr_name_consistency,
    dag=dag,
)

webscrape_task = PythonOperator(
    task_id='webscrape',
    python_callable=scrape_premier_league_data,
    dag=dag,
)

# Define task dependencies
clean_webscraped_task >> extract_market_value_task >> extract_matches_task >> transform_jointables_task
transform_nameconsistency_task >> load_to_sql_task

if __name__ == "__main__":
    dag.cli()
