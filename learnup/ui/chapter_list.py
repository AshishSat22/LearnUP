"""ui/chapter_list.py — Chapter listing with 3-tab content hub navigation."""

import tkinter as tk
from utils.theme import FONTS, SUBJECT_COLORS, SUBJECT_ICONS
from utils.file_handler import list_video_chapters, list_question_chapters, list_quiz_chapters


class ChapterListFrame(tk.Frame):
    def __init__(self, parent, app, subject):
        self.app = app
        self.subject = subject
        p = app.palette
        super().__init__(parent, bg=p["bg"])
        self._build()

    def _build(self):
        p = self.app.palette
        color = SUBJECT_COLORS.get(self.subject, p["accent"])
        icon = SUBJECT_ICONS.get(self.subject, "📖")

        # Header
        hdr = tk.Frame(self, bg=color, height=80)
        hdr.pack(fill=tk.X)
        hdr.pack_propagate(False)
        tk.Label(hdr, text=f"{icon}  {self.subject}", bg=color, fg="#FFFFFF",
                 font=FONTS["heading1"]).pack(expand=True)

        # Subtitle
        tk.Label(self, text="Select a chapter to explore videos, questions & quizzes",
                 bg=p["bg"], fg=p["fg2"], font=FONTS["body"]).pack(pady=(16, 6))

        # Get chapters (union of all sections)
        v_chs = set(list_video_chapters(self.subject))
        q_chs = set(list_question_chapters(self.subject))
        z_chs = set(list_quiz_chapters(self.subject))
        chapters = sorted(v_chs | q_chs | z_chs)

        if not chapters:
            tk.Label(self, text="⚠ No chapters found. Run generate_data.py first.",
                     bg=p["bg"], fg=p["danger"], font=FONTS["body"]).pack(pady=40)
            return

        # Scrollable list
        canvas = tk.Canvas(self, bg=p["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(fill=tk.BOTH, expand=True, padx=24, pady=8)

        inner = tk.Frame(canvas, bg=p["bg"])
        win_id = canvas.create_window((0, 0), window=inner, anchor="nw")

        def on_resize(e):
            canvas.itemconfig(win_id, width=e.width)
        canvas.bind("<Configure>", on_resize)
        inner.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(
            int(-1*(e.delta/120)), "units"))

        for i, chapter in enumerate(chapters):
            self._chapter_row(inner, chapter, i, v_chs, q_chs, z_chs, color)

    def _chapter_row(self, parent, chapter, idx, v_chs, q_chs, z_chs, color):
        p = self.app.palette
        row = tk.Frame(parent, bg=p["card"], highlightbackground=p["card_border"],
                       highlightthickness=1, cursor="hand2")
        row.pack(fill=tk.X, padx=4, pady=5, ipady=10)

        # Number badge
        badge = tk.Label(row, text=f"  {idx+1:02d}", bg=color, fg="#fff",
                         font=FONTS["body_bold"], width=4, anchor="center")
        badge.pack(side=tk.LEFT, fill=tk.Y)

        # Chapter name
        tk.Label(row, text=f"  {chapter}", bg=p["card"], fg=p["fg"],
                 font=FONTS["heading3"]).pack(side=tk.LEFT, padx=8)

        # Tag pills
        pill_frame = tk.Frame(row, bg=p["card"])
        pill_frame.pack(side=tk.LEFT, padx=8)
        if chapter in v_chs:
            self._pill(pill_frame, "▶ Videos", "#4361EE")
        if chapter in q_chs:
            self._pill(pill_frame, "📝 Questions", "#06D6A0")
        if chapter in z_chs:
            self._pill(pill_frame, "🧠 Quiz", "#FF6B6B")

        # Arrow
        tk.Label(row, text="›", bg=p["card"], fg=p["fg2"],
                 font=("Segoe UI", 18, "bold")).pack(side=tk.RIGHT, padx=12)

        def on_click(e, ch=chapter):
            from ui.content_hub import ContentHubFrame
            self.app.push_frame(
                ContentHubFrame(self.app.content, self.app, self.subject, ch),
                title=ch)

        def on_enter(e, r=row):
            r.config(bg=p["highlight"])
            for c in r.winfo_children():
                try:
                    if c.cget("bg") == p["card"]:
                        c.config(bg=p["highlight"])
                except Exception:
                    pass

        def on_leave(e, r=row):
            r.config(bg=p["card"])
            for c in r.winfo_children():
                try:
                    if c.cget("bg") == p["highlight"]:
                        c.config(bg=p["card"])
                except Exception:
                    pass

        for w in [row, badge] + list(row.winfo_children()):
            w.bind("<Button-1>", on_click)
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)

    def _pill(self, parent, text, color):
        tk.Label(parent, text=text, bg=color, fg="#fff",
                 font=("Segoe UI", 8, "bold"), padx=6, pady=2).pack(
            side=tk.LEFT, padx=2)
