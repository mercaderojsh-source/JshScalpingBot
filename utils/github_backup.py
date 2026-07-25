import os
import base64
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Backup Repository
OWNER = "mercaderojsh-source"
REPO = "JshScalpingBot-Backup"
BRANCH = "main"


def upload_file(local_path, repo_path):

    print(f"DEBUG: upload_file({local_path}, {repo_path})")

    if not GITHUB_TOKEN:
        print("⚠ No GitHub token configured.")
        return

    print("DEBUG: GitHub token found")

    if not os.path.exists(local_path):
        print(f"DEBUG: File not found -> {local_path}")
        return

    print("DEBUG: File exists")

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

    print(f"DEBUG: GET status = {r.status_code}")

    if r.status_code == 200:
        sha = r.json()["sha"]
        print("DEBUG: Existing file found.")

    elif r.status_code == 404:
        print("DEBUG: File does not exist yet.")

    else:
        print(f"DEBUG GET ERROR: {r.text}")
        return

    payload = {
        "message": f"Backup {repo_path}",
        "content": content,
        "branch": BRANCH
    }

    if sha:
        payload["sha"] = sha

    r = requests.put(
        url,
        headers=headers,
        json=payload
    )

    print(f"DEBUG: PUT status = {r.status_code}")

    if r.status_code in (200, 201):
        print(f"☁ Backed up {repo_path}")

    else:
        print(f"DEBUG PUT ERROR: {r.text}")