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

## 🧠 Notes

- This setup is intended **only for local development and testing**.
- For production or multi-user environments, use the [official Airflow docker-compose.yaml](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html) with a PostgreSQL and Redis setup.
