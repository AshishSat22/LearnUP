"""main.py — Entry point with animated splash screen for LearnUP."""

import tkinter as tk
from tkinter import font as tkfont
import time
import threading


def _run_splash_then_app():
    splash = tk.Tk()
    splash.overrideredirect(True)
    splash.configure(bg="#1A1A2E")
    w, h = 480, 300
    sw = splash.winfo_screenwidth()
    sh = splash.winfo_screenheight()
    splash.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    # Canvas for animated gradient circle
    c = tk.Canvas(splash, width=w, height=h, bg="#1A1A2E", highlightthickness=0)
    c.pack(fill=tk.BOTH, expand=True)

    # Draw decorative rings
    for i, col in enumerate(["#1A2566","#243377","#2E4499","#3855CC"]):
        r = 90 - i*18
        c.create_oval(w//2-r, h//2-r-30, w//2+r, h//2+r-30,
                      outline=col, width=2+i)

    c.create_text(w//2, h//2-30, text="⚡", font=("Segoe UI Emoji", 44),
                  fill="#4CC9F0")
    c.create_text(w//2, h//2+36, text="LearnUP", fill="#FFFFFF",
                  font=("Segoe UI", 28, "bold"))
    c.create_text(w//2, h//2+70, text="CBSE Class 12 — Your Smart Study Companion",
                  fill="#A0A0C0", font=("Segoe UI", 10))

    # Loading bar
    bar_bg = c.create_rectangle(60, h-50, w-60, h-34, fill="#2D2D50", outline="")
    bar_fill = c.create_rectangle(60, h-50, 60, h-34, fill="#4CC9F0", outline="")
    pct_text = c.create_text(w//2, h-25, text="Loading...", fill="#A0A0C0",
                              font=("Segoe UI", 9))

    def animate(step=0):
        if step > 100:
            splash.destroy()
            _launch_app()
            return
        bar_w = int((w-120) * step / 100)
        c.coords(bar_fill, 60, h-50, 60+bar_w, h-34)
        c.itemconfig(pct_text, text=f"Loading... {step}%")
        splash.after(20, lambda: animate(step + 2))

    splash.after(100, animate)
    splash.mainloop()


def _launch_app():
    from app import App
    app = App()
    app.mainloop()


if __name__ == "__main__":
    _run_splash_then_app()
