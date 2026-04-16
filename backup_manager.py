# backup_manager.py
import shutil
import os
from data_paths import get_path

LOG = get_path("history.log")
BACKUP = get_path("history_backup.log")

def backup_history(log_path=LOG, backup_path=BACKUP):
    """
    Make a simple copy of history.log to history_backup.log.
    Overwrites the backup each time (rotate/backups could be added later).
    """
    try:
        if os.path.exists(log_path):
            # Ensure destination directory exists (get_path already ensures)
            shutil.copyfile(log_path, backup_path)
    except Exception:
        # Do not raise - backups are nice-to-have only
        pass