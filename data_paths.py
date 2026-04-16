# data_paths.py
import os

# Use LOCALAPPDATA (AppData\Local) if available; fall back to user home.
BASE = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
APP_FOLDER = os.path.join(BASE, "FoundationTrainer")

def ensure_data_folder():
    if not os.path.exists(APP_FOLDER):
        os.makedirs(APP_FOLDER, exist_ok=True)

def get_path(filename: str) -> str:
    ensure_data_folder()
    return os.path.join(APP_FOLDER, filename)