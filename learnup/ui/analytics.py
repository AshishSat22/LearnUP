"""ui/analytics.py — Quiz analytics with canvas bar chart."""

import tkinter as tk
from utils.theme import FONTS, SUBJECT_COLORS
from utils.score_manager import get_analytics, load_scores
from utils.file_handler import list_subjects


class AnalyticsFrame(tk.Frame):
    def __init__(self, parent, app):
        self.app = app
        p = app.palette
        super().__init__(parent, bg=p["bg"])
        self._build()

    def _build(self):
        p = self.app.palette

        # Header
        hdr = tk.Frame(self, bg="#FFB703", height=54)
        hdr.pack(fill=tk.X)
        hdr.pack_propagate(False)
        tk.Label(hdr, text="📈 Quiz Analytics", bg="#FFB703",
                 fg="#000", font=FONTS["heading2"]).pack(side=tk.LEFT, padx=20, expand=True)

        # Filter
        ctrl = tk.Frame(self, bg=p["bg"])
        ctrl.pack(fill=tk.X, padx=20, pady=10)
        subjects = ["All"] + list_subjects("resources")
        self._subj_var = tk.StringVar(value="All")
        om = tk.OptionMenu(ctrl, self._subj_var, *subjects,
                           command=lambda _: self._reload())
        om.config(bg=p["btn"], fg=p["btn_fg"], relief="flat", font=FONTS["body"], bd=0)
        om.pack(side=tk.LEFT)

        # Summary stats
        self._stats_lbl = tk.Label(self, text="", bg=p["bg"], fg=p["fg"],
                                   font=FONTS["body_bold"])
        self._stats_lbl.pack(pady=4)

        # Canvas for chart
        self._canvas = tk.Canvas(self, bg=p["bg"], highlightthickness=0, height=300)
        self._canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=8)

        # Table below chart
        self._table_frame = tk.Frame(self, bg=p["bg"])
        self._table_frame.pack(fill=tk.BOTH, padx=20, pady=4)

        self._reload()

    def _reload(self):
        p = self.app.palette
        filt = self._subj_var.get()
        analytics = get_analytics(subject_filter=None if filt == "All" else filt)
        all_scores = load_scores()
        if filt != "All":
            all_scores = [s for s in all_scores if s.get("subject") == filt]

        # Summary
        total_attempts = len(all_scores)
        overall_avg = round(sum(s.get("accuracy", 0) for s in all_scores) / total_attempts, 1) \
            if total_attempts else 0
        best = max((s.get("accuracy", 0) for s in all_scores), default=0)
        self._stats_lbl.config(
            text=f"Total Attempts: {total_attempts}  |  Avg Accuracy: {overall_avg}%  |  Best: {best}%")

        # Draw bar chart
        self._canvas.delete("all")
        if not analytics:
            self._canvas.create_text(400, 150, text="No quiz data yet. Take some quizzes!",
                                     fill=p["fg2"], font=FONTS["body"])
            return

        items = list(analytics.items())[:8]  # max 8 bars
        cw = max(self._canvas.winfo_width(), 700)
        ch = 280
        margin_l, margin_b, margin_t = 60, 50, 30
        bar_area_w = cw - margin_l - 20
        bar_w = max(20, bar_area_w // len(items) - 10)
        max_acc = 100

        # Axis
        self._canvas.create_line(margin_l, margin_t, margin_l, ch - margin_b,
                                 fill=p["fg2"], width=2)
        self._canvas.create_line(margin_l, ch - margin_b, cw - 10, ch - margin_b,
                                 fill=p["fg2"], width=2)
        # Y gridlines
        for pct in [25, 50, 75, 100]:
            y = ch - margin_b - int((ch - margin_b - margin_t) * pct / max_acc)
            self._canvas.create_line(margin_l, y, cw - 10, y, fill=p["separator"], dash=(4, 4))
            self._canvas.create_text(margin_l - 6, y, text=f"{pct}%",
                                     fill=p["fg2"], font=FONTS["small"], anchor="e")

        for i, (topic, data) in enumerate(items):
            x = margin_l + 10 + i * (bar_w + 10)
            avg_acc = data.get("avg_acc", 0)
            bar_h = int((ch - margin_b - margin_t) * avg_acc / max_acc)
            y_top = ch - margin_b - bar_h
            subj = data.get("subject", "Physics")
            color = SUBJECT_COLORS.get(subj, p["accent"])

            # Bar
            self._canvas.create_rectangle(x, y_top, x + bar_w, ch - margin_b,
                                          fill=color, outline="")
            # Best score marker
            best_acc = data.get("best", 0)
            best_y = ch - margin_b - int((ch - margin_b - margin_t) * best_acc / max_acc)
            self._canvas.create_line(x, best_y, x + bar_w, best_y,
                                     fill="#FFB703", width=2, dash=(3, 3))

            # Label on bar
            self._canvas.create_text(x + bar_w // 2, y_top - 8,
                                     text=f"{avg_acc}%", fill=p["fg"],
                                     font=FONTS["small"])
            # X label (short)
            short = topic.split("—")[-1].strip()[:12]
            self._canvas.create_text(x + bar_w // 2, ch - margin_b + 16,
                                     text=short, fill=p["fg2"],
                                     font=("Segoe UI", 8), angle=0)
            self._canvas.create_text(x + bar_w // 2, ch - margin_b + 30,
                                     text=f"×{data['attempts']}", fill=p["fg2"],
                                     font=("Segoe UI", 8))

        # Legend
        self._canvas.create_rectangle(cw - 160, margin_t, cw - 140, margin_t + 14,
                                      fill=p["accent"], outline="")
        self._canvas.create_text(cw - 136, margin_t + 7, text="Avg Accuracy",
                                 fill=p["fg2"], font=FONTS["small"], anchor="w")
        self._canvas.create_line(cw - 160, margin_t + 28, cw - 140, margin_t + 28,
                                 fill="#FFB703", width=2, dash=(3, 3))
        self._canvas.create_text(cw - 136, margin_t + 28, text="Best Score",
                                 fill=p["fg2"], font=FONTS["small"], anchor="w")

        # Table
        for w in self._table_frame.winfo_children():
            w.destroy()

        hdr_row = tk.Frame(self._table_frame, bg=p["bg2"])
        hdr_row.pack(fill=tk.X)
        for col, w in [("Topic", 280), ("Attempts", 80), ("Avg %", 80), ("Best %", 80)]:
            tk.Label(hdr_row, text=col, bg=p["bg2"], fg=p["fg"],
                     font=FONTS["body_bold"], width=w//8, anchor="w").pack(side=tk.LEFT, padx=8, pady=4)

        for topic, data in list(analytics.items()):
            row = tk.Frame(self._table_frame, bg=p["card"],
                           highlightbackground=p["separator"], highlightthickness=1)
            row.pack(fill=tk.X, pady=2)
            subj = data.get("subject", "")
            color = SUBJECT_COLORS.get(subj, p["accent"])
            for val, wt, fg in [
                (topic, 280, p["fg"]),
                (str(data["attempts"]), 80, p["fg2"]),
                (f"{data['avg_acc']}%", 80, color),
                (f"{data['best']}%", 80, "#FFB703"),
            ]:
                tk.Label(row, text=val, bg=p["card"], fg=fg,
                         font=FONTS["body"], width=wt//8, anchor="w").pack(
                    side=tk.LEFT, padx=8, pady=3)
