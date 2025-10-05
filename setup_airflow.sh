#!/bin/bash
set -e

# Check if AIRFLOW_VERSION is set (not needed for clean)
if [ "$1" != "clean" ] && [ -z "$AIRFLOW_VERSION" ]; then
  echo "❌ Please set AIRFLOW_VERSION environment variable. Example:"
  echo "   AIRFLOW_VERSION=2.9.3 ./setup_airflow.sh"
  exit 1
fi

if [ "$1" = "clean" ]; then
  echo "🧹 Stopping and cleaning up Airflow..."
  docker compose down -v --remove-orphans
  rm -rf dags logs plugins .env docker-compose.yaml
  echo "✅ Airflow environment cleaned."
  exit 0
fi

echo "🚀 Setting up Apache Airflow version $AIRFLOW_VERSION with Docker Compose..."

# Download docker-compose.yaml for the specified version
curl -LfO "https://airflow.apache.org/docs/apache-airflow/$AIRFLOW_VERSION/docker-compose.yaml"

# Create required directories
mkdir -p ./dags ./logs ./plugins

# Create .env file with proper UID
echo "AIRFLOW_UID=$(id -u)" > .env

# Initialize the Airflow database
echo "🔧 Initializing Airflow database..."
docker compose up airflow-init

# Start Airflow
echo "▶️ Starting Airflow services..."
docker compose up -d

echo "✅ Apache Airflow $AIRFLOW_VERSION is now running!"
echo "👉 Access the UI at: http://localhost:8080"
echo "   Username: airflow | Password: airflow"
