"""ui/scores.py — Score board with subject filter and CSV export."""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from utils.theme import FONTS, SUBJECT_COLORS
from utils.score_manager import load_scores, export_scores_csv
from utils.file_handler import list_subjects


class ScoresFrame(tk.Frame):
    def __init__(self, parent, app):
        self.app = app
        p = app.palette
        super().__init__(parent, bg=p["bg"])
        self._build()

    def _build(self):
        p = self.app.palette

        # Header
        hdr = tk.Frame(self, bg=p["accent"], height=54)
        hdr.pack(fill=tk.X)
        hdr.pack_propagate(False)
        tk.Label(hdr, text="📊 Score Board", bg=p["accent"],
                 fg=p["accent_fg"], font=FONTS["heading2"]).pack(side=tk.LEFT, padx=20, expand=True)

        # Controls
        ctrl = tk.Frame(self, bg=p["bg"])
        ctrl.pack(fill=tk.X, padx=20, pady=10)

        subjects = ["All"] + list_subjects("resources")
        self._subj_var = tk.StringVar(value="All")
        om = tk.OptionMenu(ctrl, self._subj_var, *subjects,
                           command=lambda _: self._reload())
        om.config(bg=p["btn"], fg=p["btn_fg"], relief="flat", font=FONTS["body"], bd=0)
        om.pack(side=tk.LEFT)

        tk.Button(ctrl, text="⬇ Export CSV",
                  command=self._export,
                  bg=p["success"], fg="#fff", relief="flat",
                  font=FONTS["btn"], padx=14, pady=6, cursor="hand2").pack(side=tk.RIGHT)

        # Treeview
        cols = ("Date", "Subject", "Topic", "Score", "Accuracy", "Difficulty")
        self._tree = ttk.Treeview(self, columns=cols, show="headings",
                                  selectmode="browse")
        for col in cols:
            self._tree.heading(col, text=col)
            w = 180 if col == "Topic" else 100
            self._tree.column(col, width=w, anchor="center" if col != "Topic" else "w")

        sb = ttk.Scrollbar(self, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=sb.set)
        sb.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 4), pady=4)
        self._tree.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 8))

        # Summary row
        self._summary_lbl = tk.Label(self, text="", bg=p["bg"], fg=p["fg2"],
                                     font=FONTS["small"])
        self._summary_lbl.pack(pady=4)

        self._reload()

    def _reload(self):
        p = self.app.palette
        for row in self._tree.get_children():
            self._tree.delete(row)

        scores = load_scores()
        filt = self._subj_var.get()
        if filt != "All":
            scores = [s for s in scores if s.get("subject") == filt]

        scores_rev = list(reversed(scores))
        for s in scores_rev:
            color = SUBJECT_COLORS.get(s.get("subject"), p["accent"])
            acc = s.get("accuracy", 0)
            acc_str = f"{acc}%"
            tag = "good" if acc >= 70 else "mid" if acc >= 40 else "low"
            self._tree.insert("", tk.END, values=(
                s.get("date", ""),
                s.get("subject", ""),
                s.get("topic", ""),
                f"{s.get('score',0)}/{s.get('total',0)}",
                acc_str,
                s.get("difficulty", ""),
            ), tags=(tag,))

        self._tree.tag_configure("good", foreground="#06D6A0")
        self._tree.tag_configure("mid", foreground="#FFB703")
        self._tree.tag_configure("low", foreground="#EF476F")

        total = len(scores)
        if total:
            avg = round(sum(s.get("accuracy", 0) for s in scores) / total, 1)
            self._summary_lbl.config(
                text=f"Total Attempts: {total}  |  Average Accuracy: {avg}%")
        else:
            self._summary_lbl.config(text="No scores yet. Take a quiz!")

    def _export(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            title="Export Scores")
        if not path:
            return
        ok = export_scores_csv(path)
        if ok:
            messagebox.showinfo("Export Successful", f"Scores exported to:\n{path}")
        else:
            messagebox.showwarning("Export Failed", "No scores to export.")
