from airflow.decorators import dag, task
from pendulum import datetime


@dag(
    dag_id="conditional_dag",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False
)
def conditional_dag():
    @task
    def first():
        return "Starting..."

    @task
    def second():
        return 5

    @task
    def third():
        return 11

    # Pass the result of 'third' as an argument
    @task.branch
    def decider_task(value_from_third):
        if value_from_third > 6:
            return "fourth"  # Return the task_id as a string
        else:
            return "fifth"  # Return the task_id as a string

    @task
    def fourth():
        return "Branch 4 Successful"

    @task
    def fifth():
        return "Branch 5 Successful"

    # Define the flow
    t1 = first()
    t2 = second()
    t3 = third()

    # Instantiate branch and leaf tasks
    t4 = fourth()
    t5 = fifth()

    # Set dependencies using TaskFlow style
    t1 >> t2 >> t3 >> decider_task(t3) >> [t4, t5]


conditional_dag()
