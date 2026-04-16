# stats_engine.py
from data_paths import get_path
import re
LOG_FILE = get_path("history.log")

def _parse_active_time(part: str):
    """Extract active minutes float from a segment like ' Active Time: 12.34m '"""
    m = re.search(r"([0-9]*\.?[0-9]+)m", part)
    if m:
        try:
            return float(m.group(1))
        except:
            return 0.0
    return 0.0

def _parse_pauses(part: str):
    """Extract pauses from ' Pauses: 2 ' or 'Pauses 2' style"""
    m = re.search(r"Pauses[:\s]*([0-9]+)", part)
    if m:
        try:
            return int(m.group(1))
        except:
            return 0
    return 0

def calculate_stats(path=LOG_FILE):
    sessions = 0
    minutes = 0.0
    pauses = 0

    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("---"):
                    continue
                # Expecting format: [timestamp] Session: X | Status: ... | Active Time: Ym | Pauses: Z | Last Ex: ...
                sessions += 1
                parts = [p.strip() for p in line.split("|")]
                for p in parts:
                    if "Active Time" in p:
                        minutes += _parse_active_time(p)
                    if "Pauses" in p:
                        pauses += _parse_pauses(p)
    except Exception:
        # If file missing or corrupt, return zeros
        pass

    return {
        "sessions": sessions,
        "minutes": round(minutes, 2),
        "pauses": pauses
    }