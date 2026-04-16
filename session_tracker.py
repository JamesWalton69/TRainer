# session_tracker.py
import json
import os
from data_paths import get_path

SESSION_FILE = get_path("session.json")

def safe_load_session(path=SESSION_FILE):
    if not os.path.exists(path):
        return 1
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return int(data.get("session", 1))
    except Exception:
        return 1

def write_session(value, path=SESSION_FILE):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"session": int(value)}, f, indent=2)
            f.flush()
            try:
                os.fsync(f.fileno())
            except Exception:
                pass
    except Exception:
        pass

def increment_session(path=SESSION_FILE):
    s = safe_load_session(path)
    s += 1
    write_session(s, path)
    return s