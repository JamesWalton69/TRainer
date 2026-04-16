# audio_system.py
import threading

try:
    import pyttsx3
except Exception:
    pyttsx3 = None

try:
    import winsound
except Exception:
    winsound = None

class AudioSystem:
    def __init__(self):
        self.engine = None
        if pyttsx3:
            try:
                self.engine = pyttsx3.init()
                self.engine.setProperty("rate", 150)
            except Exception:
                self.engine = None

    def speak(self, text):
        if not self.engine:
            return
        # run in separate thread so TTS doesn't block short timings
        t = threading.Thread(target=self._speak_blocking, args=(text,), daemon=True)
        t.start()

    def _speak_blocking(self, text):
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception:
            pass

    def beep_high(self):
        if winsound:
            try:
                winsound.Beep(1500, 120)
            except Exception:
                pass

    def beep_low(self):
        if winsound:
            try:
                winsound.Beep(500, 120)
            except Exception:
                pass