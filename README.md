# Apache Airflow - Single Instance Setup (Docker Compose)

This project provides a minimal **single-instance Apache Airflow setup** using Docker Compose.  
It’s ideal for learning, experimentation, and small-scale DAG testing — running both the **webserver** and **scheduler** in the same container with a local `dags/` folder.

## 🏗️ Project Structure

```
airflow-ref/
├── docker-compose.yml
└── dags/
└── example_dag.py

```

- `docker-compose.yml` – Defines a single Airflow container (webserver + scheduler).
- `dags/` – Place your DAG Python files here.
- `example_dag.py` – Sample DAG included to verify the setup.

## Getting Started

### 1. Prerequisites

Make sure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)

### 2. Start Airflow

From the project root directory, run:

```bash
docker compose up
```

This will:

- Initialize the Airflow database (SQLite)
- Start both the webserver and scheduler

Once started, open your browser and visit:

```
http://localhost:8080
```

**Login credentials:**

- Username: `admin`
- Password: `admin`

## 📁 Adding Your Own DAGs

Simply place your DAG Python files inside the `dags/` folder.
Airflow automatically detects and loads them.

Example:

```bash
airflow/dags/my_first_dag.py
```

---

## 🧩 Example DAG

The included example DAG runs a simple Bash command daily:

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="example_dag",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    hello = BashOperator(
        task_id="say_hello",
        bash_command="echo 'Hello from Airflow!'"
    )
```

---

## 🧹 Stopping and Cleaning Up

To stop the container:

```bash
docker compose down
```

To remove volumes and reset Airflow:

```bash
docker compose down -v
```

## 🧠 Notes

- This setup is intended **only for local development and testing**.
- For production or multi-user environments, use the [official Airflow docker-compose.yaml](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html) with a PostgreSQL and Redis setup.
