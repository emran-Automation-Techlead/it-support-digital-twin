import json
import os
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
USERS_FILE = DATA_DIR / "users.json"
TICKETS_FILE = DATA_DIR / "tickets.json"


def _atomic_write(path: Path, data):
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp_path, path)


def load_users():
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(users):
    _atomic_write(USERS_FILE, users)


def find_user(username: str):
    users = load_users()
    for user in users:
        if user["username"].lower() == username.lower():
            return user
    return None


def update_user(username: str, **fields):
    users = load_users()
    for user in users:
        if user["username"].lower() == username.lower():
            user.update(fields)
            save_users(users)
            return user
    return None


def load_tickets():
    with open(TICKETS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tickets(tickets):
    _atomic_write(TICKETS_FILE, tickets)


def add_ticket(ticket: dict):
    tickets = load_tickets()
    tickets.append(ticket)
    save_tickets(tickets)
    return ticket
