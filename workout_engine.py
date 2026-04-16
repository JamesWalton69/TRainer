# workout_engine.py
import time
import threading

class WorkoutEngine:
    """
    Pure engine: runs workout sequences with timing. No file I/O here.
    Interacts with a display and audio objects passed in.
    """
    def __init__(self, workout, timing, display, audio):
        """
        workout: list of dicts {name,reps,tension,reset}
        timing: [sets, rest_between_ex, rest_between_set, prep_time]
        display: object with .show(text, color)
        audio: object with .speak(text), .beep_high(), .beep_low()
        """
        self.workout = workout
        self.timing = timing
        self.display = display
        self.audio = audio

        self.paused = False
        self.pause_count = 0
        self.pause_start = 0
        self.total_pause_duration = 0

        self.quit_status = "Incomplete/Force Quit"
        self.current_exercise = None
        self._stop_requested = False
        self._lock = threading.Lock()

    # public controls
    def toggle_pause(self, event=None):
        with self._lock:
            self.paused = not self.paused
            if self.paused:
                self.pause_count += 1
                self.pause_start = time.time()
                self.display.show("PAUSED", "orange")
            else:
                if self.pause_start:
                    self.total_pause_duration += time.time() - self.pause_start
                self.display.show("RESUMING", "black")

    def request_stop(self, event=None):
        # show will be logged as incomplete; caller handles destroy
        self._stop_requested = True

    def is_stopped(self):
        return self._stop_requested

    def wait_while_paused(self):
        while True:
            with self._lock:
                if not self.paused:
                    return
            time.sleep(0.1)

    def run(self):
        start_time = time.time()
        try:
            sets, rest_between_ex, rest_between_set, prep = self.timing
            if prep > 0:
                self.display.show("GET READY", "gray")
                self.audio.speak("Workout starting.")
                self._sleep_interruptible(prep)
            for idx, ex in enumerate(self.workout):
                if self.is_stopped(): break
                self.current_exercise = ex["name"]
                self.display.show(f"NEXT:\n{ex['name']}", "blue")
                self.audio.speak(f"Next is {ex['name']}.")
                self._sleep_interruptible(2)
                # sets loop
                for s in range(1, sets + 1):
                    if self.is_stopped(): break
                    self.display.show(f"{ex['name']}\nSET {s}", "blue")
                    self.audio.speak(f"Set {s}.")
                    self._sleep_interruptible(1.5)
                    # reps loop
                    for r in range(1, int(ex.get("reps", 0)) + 1):
                        if self.is_stopped(): break
                        self.wait_while_paused()
                        self.display.show(f"REP {r}\nDOWN", "green")
                        self.audio.beep_high()
                        self._sleep_interruptible(float(ex.get("tension", 1)))
                        self.wait_while_paused()
                        self.display.show("UP", "red")
                        self.audio.beep_low()
                        self._sleep_interruptible(max(float(ex.get("reset", 0.2)), 0.2))
                    if s < sets:
                        self.display.show("REST", "black")
                        self.audio.speak("Resting.")
                        self._sleep_interruptible(rest_between_set)
                if idx < len(self.workout) - 1:
                    self.display.show("TRANSITION", "black")
                    self._sleep_interruptible(rest_between_ex)
            if not self.is_stopped():
                self.quit_status = "Completed"
                self.display.show("COMPLETE", "gold")
                self.audio.speak("Session finished.")
        except Exception:
            self.quit_status = "Error/Force Quit"
        finally:
            end_time = time.time()
            active_time_minutes = (end_time - start_time - self.total_pause_duration) / 60.0
            # return a summary dict for caller to log or process
            summary = {
                "status": self.quit_status,
                "active_minutes": round(active_time_minutes, 2),
                "pauses": self.pause_count,
                "last_exercise": self.current_exercise or "None"
            }
        return summary

    def _sleep_interruptible(self, seconds):
        """Sleep in small slices so pause/stop can respond quickly."""
        elapsed = 0.0
        slice_len = 0.1
        while elapsed < seconds:
            if self.is_stopped():
                break
            # if paused, block here until unpaused
            self.wait_while_paused()
            to_sleep = min(slice_len, seconds - elapsed)
            time.sleep(to_sleep)
            elapsed += to_sleep