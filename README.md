# Europe_Ecom_Data_Pipeline

![Python](https://img.shields.io/badge/Python-3.14+-3776AB?logo=python&logoColor=white)
![Airflow](https://img.shields.io/badge/Apache%20Airflow-Local%20Dev-blue?logo=apache-airflow&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)

A local Apache Airflow project for experimenting with data pipelines that ingest CSV / JSON data, perform lightweight transformation, and load results into PostgreSQL.

## What’s inside

This repository includes multiple Airflow DAGs that demonstrate:

- source file availability checks
- CSV loading and transformation with `pandas`
- loading transformed data into PostgreSQL
- simple branching logic
- a small JSON-based pipeline example

It is designed for local development and learning, not production use.

## Project layout

## DAG overview


### `pipeline_europe_ecom_2`
A task flow end-to-end pipeline that:

- checks for the source file
- loads it into a working location
- cleans data types
- stores the transformed data in PostgreSQL


## Data files

The `data/` directory contains both input files and generated outputs.

- `data.csv` — source dataset
- `data_loaded.csv` — intermediate loaded dataset
- `data_transformed.csv` — transformed dataset
- `iris.json` — sample JSON input
- `intermediate.csv` — experimental/intermediate file

## Tech stack

- Python 3.14+
- Apache Airflow
- PostgreSQL
- Redis
- Docker / Docker Compose
- Python libraries such as:
  - `pandas`
  - `sqlalchemy`
  - `requests`
  - `numpy`
  - `openpyxl`

## Requirements

Before running the project, make sure you have:

- Docker installed
- Docker Compose available
- enough local resources for Airflow containers
- a valid `.env` file if your setup requires one

## Quick start

### 1) Clone the repository



### 2) Review environment configuration
Check the `.env` file and adjust values if needed for your machine.

### 3) Start the Airflow stack


### 4) Open Airflow
Once the services are healthy, open the Airflow UI in your browser.

### 5) Trigger a DAG
- enable the DAG you want to run
- trigger it manually, or wait for the schedule

## How the pipeline works

The pipeline pattern in this project generally follows this flow:

1. check input file availability
2. load source data
3. apply transformations
4. write results to a shared data folder and/or PostgreSQL

Airflow XComs are used to pass file paths between tasks.

## Expected runtime locations

Inside the Airflow containers, files are mounted in shared locations such as:

- `/opt/airflow/dags`
- `/opt/airflow/data`
- `/opt/airflow/logs`
- `/opt/airflow/plugins`
- `/opt/airflow/config`

## Troubleshooting

### Input file missing
If a DAG fails because the source file is missing, verify that the required file exists in `data/` and is mounted into the container correctly.

### Database load fails
If loading into PostgreSQL fails, check that:

- the PostgreSQL container is running
- the Airflow stack is healthy
- the connection details match the Docker Compose service configuration

### DAG does not appear in Airflow
Confirm that:

- the DAG file is inside `dags/`
- there are no Python syntax errors
- Airflow has finished parsing the DAG folder

## Development notes

- This project is intended for local experimentation.
- Generated CSV files may be overwritten when pipelines run.
- The included DAGs are good starting points for building more robust ETL workflows.

## Result 


## License

This project is licensed under the Apache License 2.0. See `LICENSE` for details.
