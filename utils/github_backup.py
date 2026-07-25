import os
import base64
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

OWNER = "mercaderojsh-source"
REPO = "JshScalpingBot"
BRANCH = "main"


def upload_file(local_path, repo_path):
    if not GITHUB_TOKEN:
        print("⚠ No GitHub token configured.")
        return

    if not os.path.exists(local_path):
        return

    with open(local_path, "rb") as f:
        content = base64.b64encode(f.read()).decode()

    url = (
        f"https://api.github.com/repos/"
        f"{OWNER}/{REPO}/contents/{repo_path}"
    )

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    sha = None

    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        sha = r.json()["sha"]

    payload = {
        "message": f"Backup {repo_path}",
        "content": content,
        "branch": BRANCH
    }

    if sha:
        payload["sha"] = sha

    r = requests.put(url, headers=headers, json=payload)

    if r.status_code in (200, 201):
        print(f"☁ Backed up {repo_path}")
    else:
        print(r.text)