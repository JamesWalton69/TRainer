# safe_logger.py
import datetime
import os
from data_paths import get_path

LOG_FILE = get_path("history.log")

def ensure_history_exists(path=LOG_FILE):
    if not os.path.exists(path):
        try:
            with open(path, "a", encoding="utf-8") as f:
                f.write(f"--- WORKOUT HISTORY INITIATED {datetime.datetime.now().strftime('%Y-%m-%d')} ---\n")
                f.flush()
                try:
                    os.fsync(f.fileno())
                except Exception:
                    pass
        except Exception:
            pass

def log_session(session, status, active_time, pauses, last_ex, path=LOG_FILE):
    """
    Crash-safe append: write, flush, fsync.
    Values are written in a simple, parseable format.
    """
    ensure_history_exists(path)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    line = (f"[{timestamp}] Session: {session} | Status: {status} | "
            f"Active Time: {round(active_time,2)}m | Pauses: {pauses} | Last Ex: {last_ex}\n")
    try:
        # buffering=1 -> line buffered
        with open(path, "a", buffering=1, encoding="utf-8") as f:
            f.write(line)
            f.flush()
            try:
                os.fsync(f.fileno())
            except Exception:
                # fsync may fail on some platforms; ignore but don't crash
                pass
    except Exception:
        # Never let logging crash the app
        pass