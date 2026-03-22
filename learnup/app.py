"""
app.py — Root App class with navigation, theme management, and keyboard shortcuts.
"""

import tkinter as tk
from tkinter import ttk
from utils.theme import LIGHT, DARK, FONTS
from utils.file_handler import load_config, save_config


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LearnUP — CBSE Class 12")
        self.geometry("1200x760")
        self.minsize(900, 600)
        self.configure(bg="#F4F6FB")

        # Theme
        cfg = load_config()
        self._dark = cfg.get("theme", "light") == "dark"
        self.palette = DARK if self._dark else LIGHT

        # Style setup
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self._apply_ttk_style()

        # Navigation stack
        self._stack = []
        self._current_frame = None

        # Layout: top bar + content
        self._build_topbar()
        self.content = tk.Frame(self, bg=self.palette["bg"])
        self.content.pack(fill=tk.BOTH, expand=True)

        # Keyboard shortcuts
        self.bind("<Escape>", lambda e: self.pop_frame())
        self.bind("<Control-f>", lambda e: self._open_search())
        self.bind("<Control-b>", lambda e: self._open_bookmarks())
        self.bind("<Control-h>", lambda e: self.go_home())

        # Start at home
        from ui.home import HomeFrame
        self.push_frame(HomeFrame(self.content, self), title="Home")

    # ── Top Bar ──────────────────────────────────────────────────────────────

    def _build_topbar(self):
        self.topbar = tk.Frame(self, bg=self.palette["sidebar"], height=54)
        self.topbar.pack(fill=tk.X, side=tk.TOP)
        self.topbar.pack_propagate(False)

        # Logo
        logo = tk.Label(self.topbar, text="⚡ LearnUP", bg=self.palette["sidebar"],
                        fg=self.palette["accent"], font=("Segoe UI", 16, "bold"),
                        padx=18)
        logo.pack(side=tk.LEFT)
        logo.bind("<Button-1>", lambda e: self.go_home())

        # Breadcrumb
        self.breadcrumb_var = tk.StringVar(value="🏠 Home")
        bc = tk.Label(self.topbar, textvariable=self.breadcrumb_var,
                      bg=self.palette["sidebar"], fg=self.palette["fg2"],
                      font=FONTS["small"])
        bc.pack(side=tk.LEFT, padx=8)

        # Right buttons
        btn_style = dict(bg=self.palette["sidebar"], fg=self.palette["accent"],
                         font=("Segoe UI", 13), bd=0, cursor="hand2",
                         activebackground=self.palette["sidebar"],
                         activeforeground=self.palette["btn"])

        self._theme_btn = tk.Button(self.topbar, text="🌙" if not self._dark else "☀️",
                                    command=self.toggle_theme, **btn_style)
        self._theme_btn.pack(side=tk.RIGHT, padx=8)

        tk.Button(self.topbar, text="🔖", command=self._open_bookmarks,
                  **btn_style).pack(side=tk.RIGHT, padx=4)
        tk.Button(self.topbar, text="🔍", command=self._open_search,
                  **btn_style).pack(side=tk.RIGHT, padx=4)
        tk.Button(self.topbar, text="📊", command=self._open_scores,
                  **btn_style).pack(side=tk.RIGHT, padx=4)

    # ── Navigation ───────────────────────────────────────────────────────────

    def push_frame(self, frame, title=""):
        if self._current_frame:
            self._current_frame.pack_forget()
            self._stack.append((self._current_frame, self.breadcrumb_var.get()))
        self._current_frame = frame
        frame.pack(fill=tk.BOTH, expand=True)
        crumb = " › ".join([s[1] for s in self._stack] + [title])
        self.breadcrumb_var.set("🏠 " + crumb if crumb else "🏠 Home")

    def pop_frame(self):
        if not self._stack:
            return
        if self._current_frame:
            self._current_frame.pack_forget()
            try:
                self._current_frame.destroy()
            except Exception:
                pass
        prev_frame, prev_crumb = self._stack.pop()
        self._current_frame = prev_frame
        prev_frame.pack(fill=tk.BOTH, expand=True)
        self.breadcrumb_var.set(prev_crumb)

    def go_home(self):
        # Destroy all stacked frames and go to home
        if self._current_frame:
            self._current_frame.pack_forget()
            try:
                self._current_frame.destroy()
            except Exception:
                pass
        for frame, _ in self._stack:
            try:
                frame.destroy()
            except Exception:
                pass
        self._stack.clear()
        from ui.home import HomeFrame
        frame = HomeFrame(self.content, self)
        self._current_frame = frame
        frame.pack(fill=tk.BOTH, expand=True)
        self.breadcrumb_var.set("🏠 Home")

    # ── Theme ─────────────────────────────────────────────────────────────────

    def toggle_theme(self):
        self._dark = not self._dark
        self.palette = DARK if self._dark else LIGHT
        save_config({"theme": "dark" if self._dark else "light"})
        self._theme_btn.config(text="☀️" if self._dark else "🌙")
        self._apply_ttk_style()
        self.go_home()  # Reload to apply theme everywhere

    def _apply_ttk_style(self):
        p = DARK if self._dark else LIGHT
        self.style.configure("TFrame", background=p["bg"])
        self.style.configure("TLabel", background=p["bg"], foreground=p["fg"])
        self.style.configure("Treeview", background=p["card"], foreground=p["fg"],
                             fieldbackground=p["card"], rowheight=30)
        self.style.configure("Treeview.Heading", background=p["bg2"],
                             foreground=p["fg"], font=FONTS["body_bold"])
        self.style.map("Treeview", background=[("selected", p["accent"])],
                       foreground=[("selected", p["accent_fg"])])
        self.style.configure("TScrollbar", background=p["scrollbar"],
                             troughcolor=p["bg2"])
        self.configure(bg=p["bg"])
        try:
            self.topbar.config(bg=p["sidebar"])
            for w in self.topbar.winfo_children():
                if isinstance(w, (tk.Label, tk.Button)):
                    w.config(bg=p["sidebar"])
        except Exception:
            pass

    # ── Global Panels ────────────────────────────────────────────────────────

    def _open_search(self):
        from ui.search import SearchFrame
        self.push_frame(SearchFrame(self.content, self), title="Search")

    def _open_bookmarks(self):
        from ui.bookmarks import BookmarksFrame
        self.push_frame(BookmarksFrame(self.content, self), title="Bookmarks")

    def _open_scores(self):
        from ui.scores import ScoresFrame
        self.push_frame(ScoresFrame(self.content, self), title="Scores")
