# trainer.py
import threading
import os

from workout_loader import load_workout
from session_tracker import safe_load_session, increment_session, write_session
from progression import apply_progression
from audio_system import AudioSystem
from ui_display import UIDisplay
from workout_engine import WorkoutEngine

from safe_logger import log_session
from backup_manager import backup_history
from stats_engine import calculate_stats

# CONFIG
TEST_MODE = False

if TEST_MODE:
    TIMES = [1, 3, 2, 0]   # sets, rest_between_ex, rest_between_set, prep_time
else:
    TIMES = [3, 35, 60, 10]

def main():
    # 1. Load workout data (safe)
    workout = load_workout("workout.json")

    # 2. Load session number (safe)
    session = safe_load_session()

    # 3. Apply progression
    workout_prog = apply_progression(workout, session)

    # 4. Setup subsystems
    audio = AudioSystem()
    display = UIDisplay("Foundation Trainer")

    # 5. Create engine
    engine = WorkoutEngine(workout_prog, TIMES, display, audio)

    # 6. Bind keys
    display.bind("<space>", lambda e: engine.toggle_pause(e))
    def on_escape(e):
        engine.request_stop()
        display.root.after(2500, display.root.destroy)
    display.bind("<Escape>", on_escape)

    # 7. Run engine in a separate thread
    result_container = {}

    def engine_runner():
        summary = engine.run()
        result_container['summary'] = summary

    t = threading.Thread(target=engine_runner, daemon=True)
    t.start()

    # 8. Start tkinter main loop (UI thread)
    try:
        display.root.mainloop()
    except Exception:
        engine.request_stop()
        t.join(timeout=5)

    # 9. After UI closed, ensure engine finished and log results
    summary = result_container.get('summary')
    if summary is None:
        summary = {
            "status": "Incomplete/Force Quit",
            "active_minutes": 0.0,
            "pauses": engine.pause_count,
            "last_exercise": engine.current_exercise or "None"
        }

    # 10. Log (crash-safe)
    log_session(session, summary["status"], summary["active_minutes"], summary["pauses"], summary["last_exercise"])

    # 11. Backup history (best-effort)
    backup_history()

    # 12. Show stats (console)
    stats = calculate_stats()
    print("\nWORKOUT STATS")
    print("----------------")
    print("Sessions:", stats["sessions"])
    print("Total Minutes:", stats["minutes"])
    print("Total Pauses:", stats["pauses"])

    # 13. Increment session if completed
    if summary["status"] == "Completed":
        increment_session()
    else:
        write_session(session)

    print("Session summary:", summary)


if __name__ == "__main__":
    main()