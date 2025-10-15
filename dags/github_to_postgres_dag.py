from airflow import DAG
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models import Variable
from datetime import datetime, timedelta
import requests

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="github_to_postgres_dag",
    default_args=default_args,
    schedule_interval="@daily",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["github", "postgres"],
) as dag:

    @task()
    def fetch_github_repos():
        username = Variable.get("GITHUB_USERNAME")
        token = Variable.get("GITHUB_TOKEN", default_var=None)
        headers = {"Authorization": f"token {token}"} if token else {}
        rows = []
        page = 1
        while True:
            url = f"https://api.github.com/users/{username}/repos?per_page=100&page={page}"
            resp = requests.get(url, headers=headers)
            if resp.status_code != 200:
                raise Exception(f"GitHub API error {resp.status_code}: {resp.text}")
            data = resp.json()
            if not data:
                break
            for r in data:
                rows.append((
                    r["name"],
                    r["full_name"],
                    r["html_url"],
                    r.get("description"),
                    r.get("language"),
                    r.get("created_at"),
                    r.get("updated_at"),
                ))
            page += 1
        return rows

    @task()
    def write_to_postgres(repo_rows):
        hook = PostgresHook(postgres_conn_id="github_postgres")
        create_sql = """
        CREATE TABLE IF NOT EXISTS github_repos (
            id SERIAL PRIMARY KEY,
            name TEXT,
            full_name TEXT UNIQUE,
            html_url TEXT,
            description TEXT,
            language TEXT,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        );
        """
        hook.run(create_sql)

        upsert_sql = """
        INSERT INTO github_repos
        (name, full_name, html_url, description, language, created_at, updated_at)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (full_name) DO UPDATE SET
          name = EXCLUDED.name,
          html_url = EXCLUDED.html_url,
          description = EXCLUDED.description,
          language = EXCLUDED.language,
          created_at = EXCLUDED.created_at,
          updated_at = EXCLUDED.updated_at;
        """
        conn = hook.get_conn()
        cur = conn.cursor()
        for row in repo_rows:
            cur.execute(upsert_sql, row)
        conn.commit()
        cur.close()
        conn.close()

    repos = fetch_github_repos()
    write_to_postgres(repos)
