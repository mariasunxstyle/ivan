import json
import os
from datetime import datetime, timedelta

USERS_FILE = "users.json"

def save_user_if_new(user_id, username):
    users = load_users()
    now = datetime.utcnow().isoformat()
    if str(user_id) not in users:
        users[str(user_id)] = {"username": username, "joined": now, "last_active": now}
    else:
        users[str(user_id)]["last_active"] = now
    save_users(users)

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def get_all_users():
    return load_users()

def get_recent_users():
    users = load_users()
    today = datetime.utcnow().date()
    return [
        data["username"]
        for data in users.values()
        if "last_active" in data and datetime.fromisoformat(data["last_active"]).date() == today
    ]
