"""ui/questions.py — Sample questions viewer with search and bookmarks."""

import tkinter as tk
from utils.theme import FONTS, SUBJECT_COLORS
from utils.file_handler import load_questions, list_question_chapters
from utils.bookmark_manager import toggle_bookmark, is_bookmarked


class QuestionsFrame(tk.Frame):
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

        # Top controls
        ctrl = tk.Frame(self, bg=p["bg"])
        ctrl.pack(fill=tk.X, padx=16, pady=(10, 4))

        # Chapter selector
        chapters = list_question_chapters(self.subject)
        self._ch_var = tk.StringVar(value=self.chapter)
        if chapters:
            om = tk.OptionMenu(ctrl, self._ch_var, *chapters,
                               command=lambda _: self._reload())
            om.config(bg=p["btn"], fg=p["btn_fg"], relief="flat",
                      font=FONTS["body_bold"], bd=0, padx=8)
            om.pack(side=tk.LEFT)

        # Search
        tk.Label(ctrl, text="🔍", bg=p["bg"], fg=p["fg2"],
                 font=FONTS["body"]).pack(side=tk.LEFT, padx=(12, 4))
        self._sv = tk.StringVar()
        self._sv.trace_add("write", lambda *a: self._highlight())
        entry = tk.Entry(ctrl, textvariable=self._sv,
                         bg=p["input_bg"], fg=p["input_fg"],
                         relief="flat", font=FONTS["body"],
                         insertbackground=p["fg"], width=30)
        entry.pack(side=tk.LEFT, ipady=5)

        # Bookmark button
        is_bm = is_bookmarked("question", self.subject, self.chapter, self.chapter)
        self._bm_text = tk.StringVar(value="★ Bookmarked" if is_bm else "☆ Bookmark Chapter")
        bm_btn = tk.Button(ctrl, textvariable=self._bm_text,
                           command=self._toggle_bm,
                           bg=p["card"], fg="#FFB703" if is_bm else p["fg2"],
                           relief="flat", font=FONTS["small"], cursor="hand2")
        bm_btn.pack(side=tk.RIGHT, padx=8)
        self._bm_btn = bm_btn

        # Text area
        text_frame = tk.Frame(self, bg=p["bg"])
        text_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=8)

        self._text = tk.Text(text_frame, bg=p["card"], fg=p["fg"],
                             font=("Consolas", 11), wrap=tk.WORD,
                             relief="flat", bd=0, padx=16, pady=12,
                             selectbackground=p["accent"],
                             selectforeground=p["accent_fg"])
        sb = tk.Scrollbar(text_frame, command=self._text.yview)
        self._text.config(yscrollcommand=sb.set)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self._text.pack(fill=tk.BOTH, expand=True)

        # Tags for highlight
        self._text.tag_config("highlight", background="#FFB703",
                              foreground="#000000")
        self._text.tag_config("heading", foreground=color,
                              font=FONTS["heading3"])

        self._reload()

    def _reload(self):
        ch = self._ch_var.get()
        self.chapter = ch
        content = load_questions(self.subject, ch)
        self._text.config(state=tk.NORMAL)
        self._text.delete("1.0", tk.END)
        lines = content.splitlines()
        for line in lines:
            if line.startswith("=") or line.isupper() or line.endswith("==="):
                self._text.insert(tk.END, line + "\n", "heading")
            else:
                self._text.insert(tk.END, line + "\n")
        self._text.config(state=tk.DISABLED)
        self._highlight()

    def _highlight(self):
        self._text.tag_remove("highlight", "1.0", tk.END)
        q = self._sv.get().strip()
        if not q:
            return
        start = "1.0"
        while True:
            pos = self._text.search(q, start, stopindex=tk.END, nocase=True)
            if not pos:
                break
            end = f"{pos}+{len(q)}c"
            self._text.tag_add("highlight", pos, end)
            start = end

    def _toggle_bm(self):
        p = self.app.palette
        result = toggle_bookmark("question", self.subject, self.chapter,
                                 self.chapter)
        self._bm_text.set("★ Bookmarked" if result else "☆ Bookmark Chapter")
        self._bm_btn.config(fg="#FFB703" if result else p["fg2"])
