import json
import os

# Railway persistent volume (if mounted)
STATE_DIR = os.getenv("RAILWAY_VOLUME_MOUNT_PATH", ".")

os.makedirs(STATE_DIR, exist_ok=True)

STATE_FILE = os.path.join(
    STATE_DIR,
    "paper_account.json"
)


def load_state():

    print(f"📂 Paper State File: {STATE_FILE}")

    if not os.path.exists(STATE_FILE):
        print("🆕 No saved paper account found.")
        return None

    try:

        with open(STATE_FILE, "r") as f:
            state = json.load(f)

        print("💾 Paper account restored.")

        return state

    except Exception as e:

        print(f"❌ Failed loading paper account: {e}")

        return None


def save_state(state):

    try:

        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=4)

    except Exception as e:

        print(f"❌ Failed saving paper account: {e}")