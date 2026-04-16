# history_logger.py
import datetime
import os

HISTORY_FILE = "history.log"

def ensure_history_exists(path=HISTORY_FILE):
    if not os.path.exists(path):
        try:
            with open(path, "a", encoding="utf-8") as f:
                f.write(f"--- WORKOUT HISTORY INITIATED {datetime.datetime.now().strftime('%Y-%m-%d')} ---\n")
        except Exception:
            pass

def log_session(session, status, active_minutes, pauses, last_exercise, path=HISTORY_FILE):
    ensure_history_exists(path)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    line = (f"[{timestamp}] Session: {session} | Status: {status} | "
            f"Active Time: {round(active_minutes,2)}m | Pauses: {pauses} | Last Ex: {last_exercise}\n")
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        pass