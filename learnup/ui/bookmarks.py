"""ui/bookmarks.py — Bookmark manager: view and remove saved videos/questions."""

import tkinter as tk
import webbrowser
from utils.theme import FONTS, SUBJECT_COLORS
from utils.bookmark_manager import load_bookmarks, remove_bookmark


class BookmarksFrame(tk.Frame):
    def __init__(self, parent, app):
        self.app = app
        p = app.palette
        super().__init__(parent, bg=p["bg"])
        self._build()

    def _build(self):
        p = self.app.palette

        # Header
        hdr = tk.Frame(self, bg="#FF6B6B", height=54)
        hdr.pack(fill=tk.X)
        hdr.pack_propagate(False)
        tk.Label(hdr, text="🔖 Bookmarks", bg="#FF6B6B",
                 fg="#fff", font=FONTS["heading2"]).pack(side=tk.LEFT, padx=20, expand=True)

        # Type filter
        ctrl = tk.Frame(self, bg=p["bg"])
        ctrl.pack(fill=tk.X, padx=20, pady=10)
        self._type_var = tk.StringVar(value="All")
        for t in ["All", "Videos", "Questions"]:
            tk.Radiobutton(ctrl, text=t, variable=self._type_var, value=t,
                           bg=p["bg"], fg=p["fg"], selectcolor=p["card"],
                           activebackground=p["bg"], font=FONTS["body"],
                           command=self._reload).pack(side=tk.LEFT, padx=8)

        self._count_lbl = tk.Label(self, text="", bg=p["bg"], fg=p["fg2"],
                                   font=FONTS["small"])
        self._count_lbl.pack(anchor="w", padx=20)

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
        p = self.app.palette
        for w in self._inner.winfo_children():
            w.destroy()

        bms = load_bookmarks()
        filt = self._type_var.get()
        if filt == "Videos":
            bms = [b for b in bms if b.get("type") == "video"]
        elif filt == "Questions":
            bms = [b for b in bms if b.get("type") == "question"]

        self._count_lbl.config(text=f"{len(bms)} bookmark(s)")

        if not bms:
            tk.Label(self._inner, text="No bookmarks yet.\nStar videos and questions to save them here.",
                     bg=p["bg"], fg=p["fg2"], font=FONTS["body"],
                     justify="center").pack(pady=60)
            return

        for bm in bms:
            self._bookmark_row(bm)

    def _bookmark_row(self, bm):
        p = self.app.palette
        rtype = bm.get("type", "video")
        color = SUBJECT_COLORS.get(bm.get("subject", ""), p["accent"])

        row = tk.Frame(self._inner, bg=p["card"],
                       highlightbackground=p["card_border"], highlightthickness=1)
        row.pack(fill=tk.X, pady=4, ipady=8)

        # Type strip
        badge = "▶" if rtype == "video" else "📝"
        tk.Label(row, text=f"  {badge}  ", bg=color, fg="#fff",
                 font=FONTS["body"]).pack(side=tk.LEFT, fill=tk.Y)

        # Info
        info = tk.Frame(row, bg=p["card"])
        info.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        tk.Label(info, text=bm.get("title", ""), bg=p["card"],
                 fg=p["fg"], font=FONTS["body_bold"]).pack(anchor="w")
        tk.Label(info, text=f"{bm.get('subject','')} › {bm.get('chapter','')}",
                 bg=p["card"], fg=p["fg2"], font=FONTS["small"]).pack(anchor="w")

        # Remove button
        def on_remove(b=bm, r=row):
            remove_bookmark(b["type"], b["subject"], b["chapter"], b["title"])
            r.destroy()
            bms = load_bookmarks()
            self._count_lbl.config(text=f"{len(bms)} bookmark(s)")

        tk.Button(row, text="✕ Remove", command=on_remove,
                  bg=p["danger"], fg="#fff", relief="flat",
                  font=FONTS["small"], padx=8, pady=4,
                  cursor="hand2").pack(side=tk.RIGHT, padx=12)

        # Click to open
        def on_open(e, b=bm):
            if b.get("type") == "video" and b.get("url"):
                webbrowser.open(b["url"])
            else:
                from ui.content_hub import ContentHubFrame
                self.app.push_frame(
                    ContentHubFrame(self.app.content, self.app,
                                    b["subject"], b["chapter"]),
                    title=b["chapter"])

        for w in [row, info] + list(info.winfo_children()):
            w.bind("<Button-1>", on_open)
            w.bind("<Enter>", lambda e, r=row: r.config(bg=p["highlight"]))
            w.bind("<Leave>", lambda e, r=row: r.config(bg=p["card"]))
