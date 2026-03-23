from airflow.decorators import dag, task
from pendulum import datetime
from airflow.exceptions import AirflowFailException


@dag(
    dag_id="pipeline_europe_ecom_2",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False
)
def pipeline_europe_ecom_2():
    @task
    def file_avalibility_checker(**kwargs):
        import os
        file_path = "/opt/airflow/data/data.csv"
        if os.path.exists(file_path):
            kwargs["ti"].xcom_push(key="file_path", value=file_path)
        else:
            raise AirflowFailException(f"Critical Error: {file_path} is missing!")

    @task
    def data_load_task(**kwargs):
        import pandas as pd
        ti = kwargs["ti"]
        file_path = ti.xcom_pull(key="file_path", task_ids="file_avalibility_checker")
        df = pd.read_csv(file_path, encoding='latin1')
        output_path = "/opt/airflow/data/data_loaded.csv"
        df.to_csv(output_path, index=False)
        ti.xcom_push(key="internal_path", value=output_path)

    @task
    def data_transformation(**kwargs):
        import pandas as pd
        ti = kwargs["ti"]
        internal_path = ti.xcom_pull(key="internal_path", task_ids="data_load_task")
        df = pd.read_csv(internal_path)

        # Data Cleaning
        df["InvoiceNo"] = pd.to_numeric(df["InvoiceNo"], errors="coerce")
        df["InvoiceDate"] = pd.to_datetime(df['InvoiceDate'])

        transformed_path = "/opt/airflow/data/data_transformed.csv"
        df.to_csv(transformed_path, index=False)
        ti.xcom_push(key="transformed_path", value=transformed_path)

    @task
    def load_to_db(**kwargs):
        import pandas as pd
        from sqlalchemy import create_engine
        ti = kwargs["ti"]

        # Pull path from the correct task ID
        internal_path = ti.xcom_pull(key="transformed_path", task_ids="data_transformation")
        df = pd.read_csv(internal_path)

        # Connect to the Postgres service defined in your docker-compose
        engine = create_engine('postgresql+psycopg2://airflow:airflow@postgres:5432/airflow')

        df.to_sql(
            name='europe_ecom_sales',
            con=engine,
            if_exists='replace',
            index=False
        )
        return "Data successfully loaded to Postgres"

    # FIXED: The function name here must match the @task function name above
    file_avalibility_checker() >> data_load_task() >> data_transformation() >> load_to_db()


pipeline_europe_ecom_2()
