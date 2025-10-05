# Apache Airflow with Docker Compose

This repository provides a simple shell script to set up and run **Apache Airflow** using **Docker Compose**.  
It downloads the official `docker-compose.yaml` from the Airflow project, prepares the environment, and starts all services.

## Prerequisites

- **Docker** and **Docker Compose** installed
- At least **4 GB RAM** allocated to Docker

## Usage

### 1. Setup and Run Airflow

```bash
chmod +x setup_airflow.sh
AIRFLOW_VERSION=3.1.0 ./setup_airflow.sh
```

This will:

- Download the official `docker-compose.yaml` for the given Airflow version
- Create required folders: `dags/`, `logs/`, `plugins/`
- Initialize the Airflow database
- Start all services in the background

### 2. Access the Airflow UI

Once started, open:

👉 [http://localhost:8080](http://localhost:8080)

Default credentials:

- **Username:** `airflow`
- **Password:** `airflow`

### 3. Stop and Clean Up

To stop all containers, remove volumes, and delete generated files:

```bash
./setup_airflow.sh clean
```

This will remove:

- Containers, networks, and volumes
- Folders: `dags/`, `logs/`, `plugins/`
- Files: `.env`, `docker-compose.yaml`

## Notes

- Change `AIRFLOW_VERSION` to any [supported release](https://airflow.apache.org/docs/) (e.g., `3.1.0`, `2.8.4`).
- Ensure you re-run the setup script after cleaning if you want to start fresh.

## Example

```bash
# Setup Airflow 3.1.0
AIRFLOW_VERSION=3.1.0 ./setup_airflow.sh

# Clean everything
./setup_airflow.sh clean
```
