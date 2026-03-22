"""ui/search.py — Global search across videos and questions."""

import tkinter as tk
import webbrowser
from utils.theme import FONTS, SUBJECT_COLORS
from utils.file_handler import search_videos, search_questions, list_subjects


class SearchFrame(tk.Frame):
    def __init__(self, parent, app):
        self.app = app
        p = app.palette
        super().__init__(parent, bg=p["bg"])
        self._build()

    def _build(self):
        p = self.app.palette

        # Header
        hdr = tk.Frame(self, bg=p["sidebar"], height=54)
        hdr.pack(fill=tk.X)
        hdr.pack_propagate(False)
        tk.Label(hdr, text="🔍 Search", bg=p["sidebar"],
                 fg=p["accent"], font=FONTS["heading2"]).pack(side=tk.LEFT, padx=20, expand=True)

        # Search bar
        search_row = tk.Frame(self, bg=p["bg"])
        search_row.pack(fill=tk.X, padx=20, pady=16)

        self._sv = tk.StringVar()
        self._sv.trace_add("write", lambda *a: self._search())
        entry = tk.Entry(search_row, textvariable=self._sv,
                         bg=p["input_bg"], fg=p["input_fg"],
                         insertbackground=p["fg"],
                         relief="flat", font=("Segoe UI", 13),
                         width=50)
        entry.pack(side=tk.LEFT, ipady=8, fill=tk.X, expand=True)
        entry.focus()

        # Subject filter
        subjects = ["All"] + list_subjects("resources")
        self._subj_var = tk.StringVar(value="All")
        om = tk.OptionMenu(search_row, self._subj_var, *subjects,
                           command=lambda _: self._search())
        om.config(bg=p["btn"], fg=p["btn_fg"], relief="flat",
                  font=FONTS["body"], bd=0, padx=8)
        om.pack(side=tk.LEFT, padx=10)

        # Type filter
        self._type_var = tk.StringVar(value="All")
        for t in ["All", "Videos", "Questions"]:
            tk.Radiobutton(search_row, text=t, variable=self._type_var, value=t,
                           bg=p["bg"], fg=p["fg"], selectcolor=p["card"],
                           activebackground=p["bg"], font=FONTS["small"],
                           command=self._search).pack(side=tk.LEFT, padx=4)

        # Results count
        self._count_lbl = tk.Label(self, text="Type to search...", bg=p["bg"],
                                   fg=p["fg2"], font=FONTS["small"])
        self._count_lbl.pack(anchor="w", padx=20)

        # Scrollable results
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

    def _search(self):
        p = self.app.palette
        q = self._sv.get().strip()
        if len(q) < 2:
            self._count_lbl.config(text="Type at least 2 characters to search...")
            for w in self._inner.winfo_children():
                w.destroy()
            return

        filt_s = self._subj_var.get()
        filt_t = self._type_var.get()
        subj_arg = None if filt_s == "All" else filt_s

        results = []
        if filt_t in ("All", "Videos"):
            results += search_videos(q, subject_filter=subj_arg)
        if filt_t in ("All", "Questions"):
            results += search_questions(q, subject_filter=subj_arg)

        self._count_lbl.config(text=f"{len(results)} result(s) for \"{q}\"")
        self._render(results, q)

    def _render(self, results, query):
        p = self.app.palette
        for w in self._inner.winfo_children():
            w.destroy()

        if not results:
            tk.Label(self._inner, text="No results found.",
                     bg=p["bg"], fg=p["fg2"], font=FONTS["body"]).pack(pady=30)
            return

        for r in results[:60]:
            rtype = r.get("type", "")
            color = SUBJECT_COLORS.get(r.get("subject", ""), p["accent"])
            row = tk.Frame(self._inner, bg=p["card"],
                           highlightbackground=p["card_border"], highlightthickness=1)
            row.pack(fill=tk.X, pady=3, ipady=6)

            # Type badge
            badge_text = "▶ Video" if rtype == "video" else "📝 Q"
            badge_bg = color if rtype == "video" else "#06D6A0"
            tk.Label(row, text=f"  {badge_text}  ", bg=badge_bg, fg="#fff",
                     font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, fill=tk.Y)

            info = tk.Frame(row, bg=p["card"])
            info.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

            if rtype == "video":
                tk.Label(info, text=r.get("title", ""), bg=p["card"],
                         fg=p["fg"], font=FONTS["body_bold"],
                         cursor="hand2").pack(anchor="w")
                tk.Label(info, text=f"{r['subject']} › {r['chapter']}",
                         bg=p["card"], fg=p["fg2"], font=FONTS["small"]).pack(anchor="w")

                def on_click(e, url=r.get("url", "")):
                    webbrowser.open(url)
                for w in [row, info] + list(info.winfo_children()):
                    w.bind("<Button-1>", on_click)
            else:
                tk.Label(info, text=r.get("snippet", ""), bg=p["card"],
                         fg=p["fg"], font=FONTS["body"],
                         wraplength=800, justify="left").pack(anchor="w")
                tk.Label(info, text=f"{r['subject']} › {r['chapter']}",
                         bg=p["card"], fg=p["fg2"], font=FONTS["small"]).pack(anchor="w")

                def on_click_q(e, subj=r["subject"], ch=r["chapter"]):
                    from ui.content_hub import ContentHubFrame
                    self.app.push_frame(
                        ContentHubFrame(self.app.content, self.app, subj, ch),
                        title=ch)
                for w in [row, info] + list(info.winfo_children()):
                    w.bind("<Button-1>", on_click_q)

            for w in [row, info]:
                w.bind("<Enter>", lambda e, r=row: r.config(bg=p["highlight"]))
                w.bind("<Leave>", lambda e, r=row: r.config(bg=p["card"]))
