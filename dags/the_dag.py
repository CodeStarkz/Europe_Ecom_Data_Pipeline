
from airflow.decorators import dag,task
from pendulum import datetime


@dag(
    dag_id="pipeline",
    schedule="@daily",
    start_date=datetime(2026, 3, 20),
    catchup=True,
    is_paused_upon_creation=False
)
def pipeline():
    @task
    def fetching_from_source():
        import pandas as pd
        df=pd.read_json("/opt/airflow/data/iris.json")



    @task
    def transforming_data():
        return "transforming data"
    @task
    def loading_to_destination():
        return "loading to destination"

    fetching_from_source = fetching_from_source()
    transforming_data=transforming_data()
    loading_to_destination=loading_to_destination()

    fetching_from_source >> transforming_data >> loading_to_destination

pipeline()

