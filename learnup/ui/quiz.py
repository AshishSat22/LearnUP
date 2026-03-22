"""ui/quiz.py — Full quiz engine: one question at a time, scoring, resume."""

import tkinter as tk
from tkinter import messagebox
from utils.theme import FONTS, DIFFICULTY_COLORS, SUBJECT_COLORS
from utils.file_handler import load_quiz
from utils.quiz_logic import QuizSession, load_resume, clear_resume
from utils.score_manager import save_score


class QuizFrame(tk.Frame):
    def __init__(self, parent, app, subject, chapter):
        self.app = app
        self.subject = subject
        self.chapter = chapter
        p = app.palette
        super().__init__(parent, bg=p["bg"])
        self._session = None
        self._questions = load_quiz(subject, chapter)
        self._selected = tk.StringVar()
        self._build_start_screen()

    # ── Start Screen ─────────────────────────────────────────────────────────

    def _build_start_screen(self):
        p = self.app.palette
        for w in self.winfo_children():
            w.destroy()

        center = tk.Frame(self, bg=p["bg"])
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center, text="🧠", bg=p["bg"],
                 font=("Segoe UI Emoji", 48)).pack()
        tk.Label(center, text="Quiz Time!", bg=p["bg"], fg=p["fg"],
                 font=FONTS["heading1"]).pack(pady=(8, 4))
        tk.Label(center, text=f"{self.subject} › {self.chapter}",
                 bg=p["bg"], fg=p["fg2"], font=FONTS["body"]).pack()
        tk.Label(center, text=f"{len(self._questions)} Questions",
                 bg=p["bg"], fg=p["accent"], font=FONTS["body_bold"]).pack(pady=4)

        if not self._questions:
            tk.Label(center, text="⚠ No questions found for this chapter.",
                     bg=p["bg"], fg=p["danger"], font=FONTS["body"]).pack(pady=10)
            return

        # Difficulty selector
        tk.Label(center, text="Difficulty:", bg=p["bg"], fg=p["fg2"],
                 font=FONTS["small"]).pack(pady=(14, 2))
        self._diff_var = tk.StringVar(value="All")
        diff_row = tk.Frame(center, bg=p["bg"])
        diff_row.pack()
        for d in ["All", "Easy", "Medium", "Hard"]:
            c = DIFFICULTY_COLORS.get(d, p["accent"])
            tk.Radiobutton(diff_row, text=d, variable=self._diff_var, value=d,
                           bg=p["bg"], fg=p["fg"], selectcolor=p["card"],
                           activebackground=p["bg"], font=FONTS["body"],
                           indicatoron=0, padx=12, pady=4,
                           relief="flat", bd=1,
                           highlightbackground=c).pack(side=tk.LEFT, padx=4)

        # Check for resume
        resume = load_resume()
        if (resume and resume.get("subject") == self.subject
                and resume.get("chapter") == self.chapter):
            tk.Button(center, text="▶ Resume Last Quiz",
                      command=lambda: self._start_quiz(resume=resume),
                      bg=p["warning"], fg="#000", font=FONTS["btn"],
                      relief="flat", padx=20, pady=10, cursor="hand2").pack(
                pady=(16, 4))
            tk.Button(center, text="↺ Start Fresh",
                      command=lambda: self._start_quiz(),
                      bg=p["card"], fg=p["fg"], font=FONTS["body"],
                      relief="flat", padx=20, pady=8, cursor="hand2").pack(pady=4)
        else:
            tk.Button(center, text="▶ Start Quiz",
                      command=lambda: self._start_quiz(),
                      bg=p["accent"], fg=p["accent_fg"], font=FONTS["btn"],
                      relief="flat", padx=30, pady=12, cursor="hand2").pack(pady=16)

    def _start_quiz(self, resume=None):
        diff = self._diff_var.get() if hasattr(self, "_diff_var") else "All"
        self._session = QuizSession(self._questions, self.subject,
                                    self.chapter, difficulty=diff)
        if resume:
            self._session.restore_from_resume(resume)
        self._build_question_screen()

    # ── Question Screen ───────────────────────────────────────────────────────

    def _build_question_screen(self):
        p = self.app.palette
        for w in self.winfo_children():
            w.destroy()

        if self._session.is_complete():
            self._build_result_screen()
            return

        q = self._session.current_question()
        color = SUBJECT_COLORS.get(self.subject, p["accent"])
        diff = q.get("difficulty", "Medium")
        diff_color = DIFFICULTY_COLORS.get(diff, p["accent"])

        # Progress bar
        prog_frame = tk.Frame(self, bg=p["progress_bg"], height=6)
        prog_frame.pack(fill=tk.X)
        prog_frame.pack_propagate(False)
        frac = self._session.progress_fraction()
        prog_fill = tk.Frame(prog_frame, bg=p["progress_fill"], height=6)
        prog_fill.place(relwidth=frac, relheight=1)

        # Top info bar
        info_bar = tk.Frame(self, bg=p["bg"])
        info_bar.pack(fill=tk.X, padx=20, pady=(10, 4))
        idx = self._session.index
        total = self._session.total
        tk.Label(info_bar, text=f"Question {idx+1} of {total}",
                 bg=p["bg"], fg=p["fg"], font=FONTS["body_bold"]).pack(side=tk.LEFT)
        tk.Label(info_bar, text=f"Score: {self._session.score}",
                 bg=p["bg"], fg=color, font=FONTS["body_bold"]).pack(side=tk.LEFT, padx=16)
        # Difficulty badge
        tk.Label(info_bar, text=f"  {diff}  ", bg=diff_color,
                 fg="#fff" if diff != "Easy" else "#000",
                 font=("Segoe UI", 9, "bold")).pack(side=tk.RIGHT)

        # Question card
        card = tk.Frame(self, bg=p["card"],
                        highlightbackground=p["card_border"], highlightthickness=1)
        card.pack(fill=tk.X, padx=20, pady=10, ipady=6)

        tk.Label(card, text=q.get("question", ""), bg=p["card"],
                 fg=p["fg"], font=FONTS["heading3"],
                 wraplength=900, justify="left", anchor="w",
                 padx=20, pady=16).pack(fill=tk.X)

        # Options
        self._selected.set("")
        opts_frame = tk.Frame(self, bg=p["bg"])
        opts_frame.pack(fill=tk.X, padx=20, pady=4)

        self._opt_btns = []
        for opt in q.get("options", []):
            btn = tk.Radiobutton(opts_frame, text=f"  {opt}",
                                 variable=self._selected, value=opt,
                                 bg=p["card"], fg=p["fg"],
                                 selectcolor=p["highlight"],
                                 activebackground=p["card"],
                                 font=FONTS["body"], padx=14, pady=8,
                                 wraplength=860,
                                 anchor="w", justify="left",
                                 relief="flat",
                                 highlightbackground=p["card_border"],
                                 highlightthickness=1)
            btn.pack(fill=tk.X, pady=4)
            self._opt_btns.append((btn, opt))

        # Feedback label (hidden)
        self._fb_lbl = tk.Label(self, text="", bg=p["bg"], font=FONTS["body_bold"])
        self._fb_lbl.pack(pady=4)

        # Action buttons
        btn_row = tk.Frame(self, bg=p["bg"])
        btn_row.pack(side=tk.BOTTOM, pady=16, fill=tk.X, padx=20)

        tk.Button(btn_row, text="Skip →",
                  command=self._skip,
                  bg=p["card"], fg=p["fg2"], relief="flat",
                  font=FONTS["body"], padx=16, pady=8, cursor="hand2").pack(side=tk.RIGHT, padx=8)

        self._submit_btn = tk.Button(btn_row, text="Submit Answer",
                                     command=self._submit,
                                     bg=p["accent"], fg=p["accent_fg"],
                                     relief="flat", font=FONTS["btn"],
                                     padx=24, pady=10, cursor="hand2")
        self._submit_btn.pack(side=tk.RIGHT)

        # Save resume on each question
        self._session.save_resume()

    def _submit(self):
        p = self.app.palette
        chosen = self._selected.get()
        if not chosen:
            self._fb_lbl.config(text="⚠ Please select an answer.", fg=p["warning"])
            return

        is_correct = self._session.submit_answer(chosen)
        correct_ans = self._session.answers[-1]["correct"]

        # Colour the options
        for btn, opt in self._opt_btns:
            if opt == correct_ans:
                btn.config(bg="#D4F5ED")
            elif opt == chosen and not is_correct:
                btn.config(bg="#FAD4DD")

        if is_correct:
            self._fb_lbl.config(text="✔ Correct!", fg=p["success"])
        else:
            self._fb_lbl.config(text=f"✘ Wrong. Correct: {correct_ans}", fg=p["danger"])

        self._submit_btn.config(text="Next →", command=self._next)

    def _next(self):
        self._build_question_screen()

    def _skip(self):
        self._session.skip_question()
        self._build_question_screen()

    # ── Result Screen ─────────────────────────────────────────────────────────

    def _build_result_screen(self):
        p = self.app.palette
        results = self._session.get_results()
        clear_resume()
        save_score(self.chapter, self.subject, results["score"],
                   results["total"], results["difficulty"])

        for w in self.winfo_children():
            w.destroy()

        center = tk.Frame(self, bg=p["bg"])
        center.place(relx=0.5, rely=0.5, anchor="center")

        acc = results["accuracy"]
        emoji = "🏆" if acc >= 80 else "👍" if acc >= 50 else "📚"
        color = p["success"] if acc >= 80 else p["warning"] if acc >= 50 else p["danger"]

        tk.Label(center, text=emoji, bg=p["bg"],
                 font=("Segoe UI Emoji", 52)).pack()
        tk.Label(center, text="Quiz Complete!", bg=p["bg"], fg=p["fg"],
                 font=FONTS["heading1"]).pack(pady=(8, 4))
        tk.Label(center, text=f"Score: {results['score']} / {results['total']}",
                 bg=p["bg"], fg=color, font=("Segoe UI", 22, "bold")).pack()
        tk.Label(center, text=f"Accuracy: {acc}%  |  Difficulty: {results['difficulty']}",
                 bg=p["bg"], fg=p["fg2"], font=FONTS["body"]).pack(pady=8)

        # Action buttons
        row = tk.Frame(center, bg=p["bg"])
        row.pack(pady=16)

        tk.Button(row, text="↺ Try Again",
                  command=self._build_start_screen,
                  bg=p["accent"], fg=p["accent_fg"],
                  relief="flat", font=FONTS["btn"],
                  padx=20, pady=10, cursor="hand2").pack(side=tk.LEFT, padx=8)

        tk.Button(row, text="📈 View Analytics",
                  command=self._open_analytics,
                  bg=p["card"], fg=p["fg"],
                  relief="flat", font=FONTS["body"],
                  padx=16, pady=10, cursor="hand2").pack(side=tk.LEFT, padx=8)

        # Answer review
        tk.Label(center, text="Review Answers", bg=p["bg"], fg=p["fg"],
                 font=FONTS["heading3"]).pack(pady=(20, 6))

        rev_frame = tk.Frame(center, bg=p["bg"])
        rev_frame.pack(fill=tk.X)
        for i, ans in enumerate(results["answers"]):
            ic = "✔" if ans["is_correct"] else "✘"
            fc = p["success"] if ans["is_correct"] else p["danger"]
            tk.Label(rev_frame,
                     text=f"{ic} Q{i+1}: {ans['question'][:70]}...",
                     bg=p["bg"], fg=fc, font=FONTS["small"],
                     anchor="w").pack(anchor="w")

    def _open_analytics(self):
        from ui.analytics import AnalyticsFrame
        self.app.push_frame(AnalyticsFrame(self.app.content, self.app),
                            title="Analytics")
