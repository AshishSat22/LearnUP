"""ui/home.py — Dashboard / subject selector for LearnUP."""

import tkinter as tk
from tkinter import ttk
from utils.theme import FONTS, SUBJECT_COLORS, SUBJECT_ICONS
from utils.file_handler import list_subjects
from utils.score_manager import load_scores
from datetime import datetime


class HomeFrame(tk.Frame):
    def __init__(self, parent, app):
        self.app = app
        p = app.palette
        super().__init__(parent, bg=p["bg"])
        self._build()

    def _build(self):
        p = self.app.palette
        # ── Header ──────────────────────────────────────────────────────────
        hdr = tk.Frame(self, bg=p["bg"])
        hdr.pack(fill=tk.X, padx=36, pady=(28, 8))

        today = datetime.now().strftime("%A, %d %B %Y")
        tk.Label(hdr, text=today, bg=p["bg"], fg=p["fg2"],
                 font=FONTS["small"]).pack(anchor="w")
        tk.Label(hdr, text="Welcome back! 📚", bg=p["bg"], fg=p["fg"],
                 font=FONTS["heading1"]).pack(anchor="w")
        tk.Label(hdr, text="What would you like to study today?",
                 bg=p["bg"], fg=p["fg2"], font=FONTS["body"]).pack(anchor="w", pady=(2,0))

        # ── Subject Cards ────────────────────────────────────────────────────
        sec_lbl = tk.Label(self, text="SUBJECTS", bg=p["bg"], fg=p["fg2"],
                           font=("Segoe UI", 9, "bold"))
        sec_lbl.pack(anchor="w", padx=36, pady=(20, 6))

        cards_frame = tk.Frame(self, bg=p["bg"])
        cards_frame.pack(fill=tk.X, padx=32)

        subjects = list_subjects("resources")
        if not subjects:
            subjects = ["Physics", "Chemistry", "Maths"]

        for col, subject in enumerate(subjects):
            self._subject_card(cards_frame, subject, col)
        cards_frame.columnconfigure(list(range(len(subjects))), weight=1)

        # ── Quick Access Row ─────────────────────────────────────────────────
        sec_lbl2 = tk.Label(self, text="QUICK ACCESS", bg=p["bg"], fg=p["fg2"],
                            font=("Segoe UI", 9, "bold"))
        sec_lbl2.pack(anchor="w", padx=36, pady=(28, 6))

        quick = tk.Frame(self, bg=p["bg"])
        quick.pack(fill=tk.X, padx=32)

        quick_items = [
            ("🔍 Search", self.app._open_search, p["accent"]),
            ("🔖 Bookmarks", self.app._open_bookmarks, "#FF6B6B"),
            ("📊 Scores", self.app._open_scores, "#06D6A0"),
            ("📈 Analytics", self._open_analytics, "#FFB703"),
        ]
        for i, (label, cmd, color) in enumerate(quick_items):
            self._quick_btn(quick, label, cmd, color, i)
        quick.columnconfigure([0,1,2,3], weight=1)

        # ── Recent Scores ────────────────────────────────────────────────────
        scores = load_scores()
        if scores:
            recent = scores[-3:][::-1]
            sec_lbl3 = tk.Label(self, text="RECENT SCORES", bg=p["bg"], fg=p["fg2"],
                                font=("Segoe UI", 9, "bold"))
            sec_lbl3.pack(anchor="w", padx=36, pady=(28,6))
            for s in recent:
                self._score_chip(s)

        # ── Shortcut hint ────────────────────────────────────────────────────
        hint = tk.Label(self, text="⌨ Ctrl+F Search  •  Ctrl+B Bookmarks  •  Ctrl+H Home  •  Esc Back",
                        bg=p["bg"], fg=p["fg2"], font=FONTS["small"])
        hint.pack(side=tk.BOTTOM, pady=10)

    # ── Card builders ────────────────────────────────────────────────────────

    def _subject_card(self, parent, subject, col):
        p = self.app.palette
        color = SUBJECT_COLORS.get(subject, p["accent"])
        icon = SUBJECT_ICONS.get(subject, "📖")

        card = tk.Frame(parent, bg=p["card"], relief="flat", bd=0,
                        highlightbackground=color, highlightthickness=2,
                        cursor="hand2")
        card.grid(row=0, column=col, padx=10, pady=4, sticky="nsew", ipady=10)

        # Coloured top strip
        strip = tk.Frame(card, bg=color, height=6)
        strip.pack(fill=tk.X)

        tk.Label(card, text=icon, bg=p["card"], fg=color,
                 font=("Segoe UI Emoji", 30)).pack(pady=(18, 4))
        tk.Label(card, text=subject, bg=p["card"], fg=p["fg"],
                 font=FONTS["heading2"]).pack()
        tk.Label(card, text="Class 12 CBSE", bg=p["card"], fg=p["fg2"],
                 font=FONTS["small"]).pack(pady=(2, 14))

        for w in [card, strip] + card.winfo_children():
            w.bind("<Button-1>", lambda e, s=subject: self._open_subject(s))
            w.bind("<Enter>", lambda e, c=card, cl=color: c.config(bg=p["highlight"]))
            w.bind("<Leave>", lambda e, c=card: c.config(bg=p["card"]))

    def _quick_btn(self, parent, label, cmd, color, col):
        p = self.app.palette
        btn = tk.Frame(parent, bg=p["card"], cursor="hand2",
                       highlightbackground=color, highlightthickness=1)
        btn.grid(row=0, column=col, padx=8, pady=4, sticky="ew", ipady=8)
        tk.Label(btn, text=label, bg=p["card"], fg=p["fg"],
                 font=FONTS["body_bold"]).pack(expand=True)
        for w in [btn] + list(btn.winfo_children()):
            w.bind("<Button-1>", lambda e: cmd())
            w.bind("<Enter>", lambda e, b=btn: b.config(bg=p["highlight"]))
            w.bind("<Leave>", lambda e, b=btn: b.config(bg=p["card"]))

    def _score_chip(self, score):
        p = self.app.palette
        row = tk.Frame(self, bg=p["card"], highlightbackground=p["card_border"],
                       highlightthickness=1)
        row.pack(fill=tk.X, padx=36, pady=3, ipady=6)
        color = SUBJECT_COLORS.get(score.get("subject"), p["accent"])
        tk.Label(row, text=f"  {score['subject']}", bg=p["card"], fg=color,
                 font=FONTS["body_bold"], width=12, anchor="w").pack(side=tk.LEFT)
        tk.Label(row, text=score["topic"], bg=p["card"], fg=p["fg"],
                 font=FONTS["body"]).pack(side=tk.LEFT, padx=8)
        acc = score.get("accuracy", 0)
        acc_col = "#06D6A0" if acc >= 70 else "#FFB703" if acc >= 40 else "#EF476F"
        tk.Label(row, text=f"{score['score']}/{score['total']}  ({acc}%)",
                 bg=p["card"], fg=acc_col, font=FONTS["body_bold"]).pack(side=tk.RIGHT, padx=12)
        tk.Label(row, text=score.get("date",""), bg=p["card"], fg=p["fg2"],
                 font=FONTS["small"]).pack(side=tk.RIGHT, padx=8)

    def _open_subject(self, subject):
        from ui.chapter_list import ChapterListFrame
        self.app.push_frame(ChapterListFrame(self.app.content, self.app, subject),
                            title=subject)

    def _open_analytics(self):
        from ui.analytics import AnalyticsFrame
        self.app.push_frame(AnalyticsFrame(self.app.content, self.app), title="Analytics")
