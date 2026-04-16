# progression.py
# Simple progression rules, isolated so we can extend later.

UPGRADES = {
    "Incline Pushups": ("Pushups", 15),
    "Pushups": ("Decline Pushups", 18),
    "Bodyweight Squats": ("Jump Squats", 20)
}

def apply_progression(workout, session):
    """
    Returns a new list (deep-ish copy) with progression applied.
    - +1 rep for each (session // 5)
    - if an exercise reaches an upgrade threshold, swap it and set reps = threshold - 3
    """
    result = []
    rep_add = session // 5
    for ex in workout:
        ex_copy = ex.copy()
        ex_copy["reps"] = int(ex_copy.get("reps", 0)) + rep_add
        name = ex_copy.get("name")
        if name in UPGRADES:
            next_name, threshold = UPGRADES[name]
            if ex_copy["reps"] >= threshold:
                ex_copy["name"] = next_name
                ex_copy["reps"] = threshold - 3
        result.append(ex_copy)
    return result