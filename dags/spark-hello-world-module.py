from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime, timedelta

###############################################
# Parameters
###############################################
spark_master = "spark://spark:7077"
csv_file = "/usr/local/spark/resources/data/movies.csv"

###############################################
# DAG Definition
###############################################
now = datetime.now()

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(now.year, now.month, now.day),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1)
}

dag = DAG(
    dag_id="spark-hello-world-module",
    description="This DAG runs a Pyspark app that uses modules.",
    default_args=default_args,
    schedule_interval=timedelta(1)
)

start = EmptyOperator(task_id="start", dag=dag)

spark_job = SparkSubmitOperator(
    task_id="spark_job",
    application="/usr/local/spark/app/hello-world-module.py", # Spark application path created in airflow and spark cluster
    name="hello-world-module",
    conn_id="spark_default",
    verbose=1,
    conf={"spark.master":spark_master},
    application_args=[csv_file],
    dag=dag
)

end = EmptyOperator(task_id="end", dag=dag)

start >> spark_job >> end