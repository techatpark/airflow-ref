import requests
from typing import Optional

class GithubClient:
    def __init__(self, username: str, token: Optional[str] = None):
        self.username = username
        self.token = token
        self.headers = {"Authorization": f"token {token}"} if token else {}

    def fetch_github_repos(self):
        rows = []
        page = 1

        while True:
            url = (
                f"https://api.github.com/users/{self.username}/repos"
                f"?per_page=100&page={page}"
            )
            resp = requests.get(url, headers=self.headers)

            if resp.status_code != 200:
                raise Exception(f"GitHub API error {resp.status_code}: {resp.text}")

            data = resp.json()
            if not data:
                break

            for r in data:
                rows.append(
                    (
                        r["name"],
                        r["full_name"],
                        r["html_url"],
                        r.get("description"),
                        r.get("language"),
                        r.get("created_at"),
                        r.get("updated_at"),
                    )
                )
            page += 1

        return rows
