# ui_display.py
import tkinter as tk

class UIDisplay:
    def __init__(self, title="Foundation Trainer"):
        self.root = tk.Tk()
        self.root.title(title)
        # start fullscreen - caller can change
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="black")

        self.label = tk.Label(self.root, text="", font=("Arial", 68, "bold"), fg="white", bg="black")
        self.label.pack(expand=True, fill="both")

    def show(self, text, color="black"):
        # minimal logic; keep it fast and non-blocking
        try:
            self.root.configure(bg=color)
            self.label.config(text=text, bg=color)
            # force update so UI changes appear even during blocking sleeps
            self.root.update_idletasks()
            self.root.update()
        except Exception:
            pass

    def bind(self, sequence, func):
        self.root.bind(sequence, func)

    def destroy_after(self, ms):
        self.root.after(ms, self.root.destroy)