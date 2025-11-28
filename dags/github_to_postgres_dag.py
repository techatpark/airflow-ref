from airflow import DAG
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models import Variable
from datetime import datetime, timedelta
from client.github import GithubClient  

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
    def fetch_github_repos_task():
        username = Variable.get("GITHUB_USERNAME")
        token = Variable.get("GITHUB_TOKEN", default_var=None)

        github = GithubClient(username, token)
        return github.fetch_github_repos()

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
    repos = fetch_github_repos_task()
    write_to_postgres(repos)
