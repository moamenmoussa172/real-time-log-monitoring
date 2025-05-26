from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# Define the DAG
with DAG(
    'log_pipeline_dag',
    default_args=default_args,
    description='A DAG to manage the log pipeline',
    schedule_interval='@daily',  # Run daily
    start_date=datetime(2025, 1, 1),
    catchup=False,
) as dag:

    # Task 1: Run the log producer script
    log_producer_task = BashOperator(
        task_id='run_log_producer',
        bash_command='python /opt/airflow/dags/scripts/log_producer.py',
    )

    # Task 2: Run the PySpark processor script
    pyspark_processor_task = BashOperator(
    task_id='run_pyspark_processor',
    bash_command='docker exec pyspark spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1 --jars /home/jovyan/work/jars/postgresql-42.6.0.jar /home/jovyan/work/kafka_pyspark_processor.py',
    )
  

    # Task 3: Run the alert script
    alert_script_task = BashOperator(
        task_id='run_alert_script',
        bash_command='python /opt/airflow/dags/scripts/alert_script.py',
    )

    # Task 4: Clean up old logs in PostgreSQL
    cleanup_task = PostgresOperator(
        task_id='clean_old_logs',
        postgres_conn_id='postgres_default',  # Matches the connection ID in Airflow
        sql="""
            DELETE FROM all_logs WHERE timestamp < NOW() - INTERVAL '1 day';
        """,
    )

    # Define task dependencies
    log_producer_task >> pyspark_processor_task >> alert_script_task >> cleanup_task