# workout_loader.py
import json
import os

DEFAULT_WORKOUT = [
    {"name": "Incline Pushups", "reps": 10, "tension": 2, "reset": 0.4},
    {"name": "Bodyweight Squats", "reps": 15, "tension": 2, "reset": 0.4},
    {"name": "Glute Bridges", "reps": 15, "tension": 3, "reset": 0.4},
    {"name": "Superman", "reps": 10, "tension": 3.5, "reset": 0.6},
    {"name": "Plank", "reps": 1, "tension": 40, "reset": 10}
]

def safe_load_json(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        # If file corrupt, return default (do not crash UI)
        return default

def load_workout(path="workout.json"):
    return safe_load_json(path, DEFAULT_WORKOUT)