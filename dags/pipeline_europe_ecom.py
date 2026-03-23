from airflow.decorators import dag, task
from pendulum import datetime


@dag(
    dag_id="pipeline_europe_ecom",
    start_date=datetime(2026, 3, 1),
    schedule="@daily",
    catchup=True,
    is_paused_upon_creation=False
)

def pipeline_europe_ecom():

    @task
    def file_avalibility_checker(**kwargs):
        print("loading dependencies")

        import os
        file_path_with_name = "/opt/airflow/data/data.csv"
        if os.path.exists("/opt/airflow/data/data.csv"):
            print("file exists")
        else:
            print("file does not exist")
        ti=kwargs["ti"]
        ti.xcom_push(key="file_path",value=file_path_with_name)
        return "file_check_success"


    @task
    def data_load_from_customer_access_path_to_internal_location(**kwargs):
        import pandas as pd
        import os
        ti=kwargs["ti"]
        file_path=ti.xcom_pull(key="file_path",task_ids="file_avalibility_checker")
        df =pd.read_csv(file_path)
        df.to_csv("/opt/airflow/data/data_loaded.csv")
        ti=kwargs["ti"]
        ti.xcom_push(key="file_path_internal_location",value="/opt/airflow/data/data_loaded.csv")
        return "data_load_success"

    @task
    def data_transformation(**kwargs):
        import pandas as pd
        ti=kwargs["ti"]
        file_path_internal_location=ti.xcom_pull(key="file_path_internal_location",task_ids="data_load_from_customer_access_path_to_internal_location")
        df=pd.read_csv(file_path_internal_location)
        df["country"]="Europe"
        df.to_csv("/opt/airflow/data/data_transformed.csv")
        return "data_transformation_success"


        #write to destination

    file_avalibility_checker=file_avalibility_checker()
    data_load_from_customer_access_path_to_internal_location=data_load_from_customer_access_path_to_internal_location()
    data_transformation=data_transformation()

    file_avalibility_checker >> data_load_from_customer_access_path_to_internal_location >> data_transformation
pipeline_europe_ecom()