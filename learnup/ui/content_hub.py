"""ui/content_hub.py — 3-tab hub (Videos | Questions | Quiz) for a chapter."""

import tkinter as tk
from tkinter import ttk
from utils.theme import FONTS, SUBJECT_COLORS


class ContentHubFrame(tk.Frame):
    def __init__(self, parent, app, subject, chapter):
        self.app = app
        self.subject = subject
        self.chapter = chapter
        p = app.palette
        super().__init__(parent, bg=p["bg"])
        self._build()

    def _build(self):
        p = self.app.palette
        color = SUBJECT_COLORS.get(self.subject, p["accent"])

        # Header
        hdr = tk.Frame(self, bg=color, height=60)
        hdr.pack(fill=tk.X)
        hdr.pack_propagate(False)
        tk.Label(hdr, text=f"  📖  {self.chapter}", bg=color, fg="#fff",
                 font=FONTS["heading2"]).pack(side=tk.LEFT, padx=16, expand=True)
        tk.Label(hdr, text=self.subject, bg=color, fg="#ffffffaa",
                 font=FONTS["small"]).pack(side=tk.RIGHT, padx=16)

        # Tab bar
        tab_bar = tk.Frame(self, bg=p["bg2"], height=44)
        tab_bar.pack(fill=tk.X)
        tab_bar.pack_propagate(False)

        self._tab_btns = {}
        self._content_frames = {}
        self._active_tab = tk.StringVar(value="Videos")

        for tab_name in ["▶ Videos", "📝 Questions", "🧠 Quiz"]:
            key = tab_name.split(" ", 1)[1] if " " in tab_name else tab_name
            btn = tk.Label(tab_bar, text=tab_name, bg=p["bg2"], fg=p["fg2"],
                           font=FONTS["body_bold"], padx=20, pady=10, cursor="hand2")
            btn.pack(side=tk.LEFT)
            self._tab_btns[key] = btn
            btn.bind("<Button-1>", lambda e, k=key: self._switch_tab(k))

        # Content area
        self._area = tk.Frame(self, bg=p["bg"])
        self._area.pack(fill=tk.BOTH, expand=True)

        self._switch_tab("Videos")

    def _switch_tab(self, key):
        p = self.app.palette
        color = SUBJECT_COLORS.get(self.subject, p["accent"])

        # Update tab styling
        for k, btn in self._tab_btns.items():
            if k == key:
                btn.config(bg=p["bg"], fg=color,
                           relief="flat", borderwidth=0)
                # underline using a frame trick
            else:
                btn.config(bg=p["bg2"], fg=p["fg2"])

        # Clear area
        for w in self._area.winfo_children():
            w.destroy()

        if key == "Videos":
            from ui.videos import VideosFrame
            f = VideosFrame(self._area, self.app, self.subject, self.chapter)
        elif key == "Questions":
            from ui.questions import QuestionsFrame
            f = QuestionsFrame(self._area, self.app, self.subject, self.chapter)
        else:  # Quiz
            from ui.quiz import QuizFrame
            f = QuizFrame(self._area, self.app, self.subject, self.chapter)

        f.pack(fill=tk.BOTH, expand=True)
