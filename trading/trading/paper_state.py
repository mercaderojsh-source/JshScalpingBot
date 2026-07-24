import json
import os

STATE_FILE = "paper_account.json"


def load_state():

    if not os.path.exists(STATE_FILE):
        return None

    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)

    except Exception:
        return None


def save_state(state):

    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)