"""ui/videos.py — Video lectures panel with search and bookmarks."""

import tkinter as tk
import webbrowser
from utils.theme import FONTS, SUBJECT_COLORS
from utils.file_handler import load_videos, list_subjects, list_video_chapters, load_videos
from utils.bookmark_manager import toggle_bookmark, is_bookmarked


class VideosFrame(tk.Frame):
    def __init__(self, parent, app, subject=None, chapter=None):
        self.app = app
        self.subject = subject
        self.chapter = chapter
        p = app.palette
        super().__init__(parent, bg=p["bg"])
        self._all_videos = []
        self._build()

    def _build(self):
        p = self.app.palette

        # Search bar
        search_row = tk.Frame(self, bg=p["bg"])
        search_row.pack(fill=tk.X, padx=20, pady=(12, 6))

        tk.Label(search_row, text="🔍", bg=p["bg"], fg=p["fg2"],
                 font=FONTS["body"]).pack(side=tk.LEFT)
        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", lambda *a: self._filter())
        entry = tk.Entry(search_row, textvariable=self._search_var,
                         bg=p["input_bg"], fg=p["input_fg"],
                         insertbackground=p["fg"], relief="flat",
                         font=FONTS["body"], width=40)
        entry.pack(side=tk.LEFT, padx=8, ipady=6, fill=tk.X, expand=True)
        entry.insert(0, "Search videos...")
        entry.bind("<FocusIn>", lambda e: entry.delete(0, tk.END)
                   if entry.get() == "Search videos..." else None)

        # Subject filter (if global view)
        if self.subject is None:
            subjects = ["All"] + list_subjects("resources")
            self._subj_var = tk.StringVar(value="All")
            om = tk.OptionMenu(search_row, self._subj_var, *subjects,
                               command=lambda _: self._reload())
            om.config(bg=p["btn"], fg=p["btn_fg"], relief="flat",
                      font=FONTS["body"], bd=0, activebackground=p["accent"])
            om.pack(side=tk.RIGHT, padx=8)
        else:
            self._subj_var = None

        # Scrollable list
        frame = tk.Frame(self, bg=p["bg"])
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=4)

        self._canvas = tk.Canvas(frame, bg=p["bg"], highlightthickness=0)
        sb = tk.Scrollbar(frame, orient="vertical", command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=sb.set)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self._canvas.pack(fill=tk.BOTH, expand=True)

        self._inner = tk.Frame(self._canvas, bg=p["bg"])
        self._win = self._canvas.create_window((0, 0), window=self._inner, anchor="nw")
        self._canvas.bind("<Configure>", lambda e: self._canvas.itemconfig(
            self._win, width=e.width))
        self._inner.bind("<Configure>", lambda e: self._canvas.configure(
            scrollregion=self._canvas.bbox("all")))
        self._canvas.bind_all("<MouseWheel>", lambda e: self._canvas.yview_scroll(
            int(-1*(e.delta/120)), "units"))

        self._reload()

    def _reload(self):
        self._all_videos = []
        if self.subject and self.chapter:
            for title, url in load_videos(self.subject, self.chapter):
                self._all_videos.append((self.subject, self.chapter, title, url))
        else:
            subj_filter = self._subj_var.get() if self._subj_var else None
            subjects = list_subjects("resources")
            if subj_filter and subj_filter != "All":
                subjects = [subj_filter]
            for s in subjects:
                for ch in list_video_chapters(s):
                    for title, url in load_videos(s, ch):
                        self._all_videos.append((s, ch, title, url))
        self._filter()

    def _filter(self):
        q = self._search_var.get().lower()
        if q == "search videos...":
            q = ""
        results = [(s, ch, t, u) for s, ch, t, u in self._all_videos
                   if q in t.lower() or q in ch.lower() or q in s.lower()]
        self._render(results)

    def _render(self, items):
        p = self.app.palette
        for w in self._inner.winfo_children():
            w.destroy()

        if not items:
            tk.Label(self._inner, text="No videos found.", bg=p["bg"],
                     fg=p["fg2"], font=FONTS["body"]).pack(pady=40)
            return

        for subj, ch, title, url in items:
            color = SUBJECT_COLORS.get(subj, p["accent"])
            self._video_row(subj, ch, title, url, color)

    def _video_row(self, subj, ch, title, url, color):
        p = self.app.palette
        row = tk.Frame(self._inner, bg=p["card"],
                       highlightbackground=p["card_border"], highlightthickness=1)
        row.pack(fill=tk.X, pady=4, padx=2, ipady=8)

        # Left color strip
        tk.Frame(row, bg=color, width=5).pack(side=tk.LEFT, fill=tk.Y)

        # Play icon
        tk.Label(row, text="▶", bg=p["card"], fg=color,
                 font=("Segoe UI", 14)).pack(side=tk.LEFT, padx=10)

        # Info
        info = tk.Frame(row, bg=p["card"])
        info.pack(side=tk.LEFT, fill=tk.X, expand=True)
        title_lbl = tk.Label(info, text=title, bg=p["card"], fg=p["fg"],
                             font=FONTS["body_bold"], anchor="w", cursor="hand2")
        title_lbl.pack(anchor="w")
        if self.subject is None:
            tk.Label(info, text=f"{subj} › {ch}", bg=p["card"], fg=p["fg2"],
                     font=FONTS["small"]).pack(anchor="w")

        # Bookmark star
        is_bm = is_bookmarked("video", subj, ch, title)
        bm_btn = tk.Label(row, text="★" if is_bm else "☆",
                          bg=p["card"], fg="#FFB703" if is_bm else p["fg2"],
                          font=("Segoe UI", 14), cursor="hand2", padx=10)
        bm_btn.pack(side=tk.RIGHT)

        def on_bm(e, b=bm_btn, s=subj, c=ch, t=title, u=url):
            result = toggle_bookmark("video", s, c, t, u)
            b.config(text="★" if result else "☆",
                     fg="#FFB703" if result else p["fg2"])

        bm_btn.bind("<Button-1>", on_bm)

        def on_click(e, u=url):
            webbrowser.open(u)

        for w in [row, title_lbl, info]:
            w.bind("<Button-1>", on_click)
            w.bind("<Enter>", lambda e, r=row: r.config(bg=p["highlight"]))
            w.bind("<Leave>", lambda e, r=row: r.config(bg=p["card"]))
