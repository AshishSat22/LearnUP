"""
quiz_logic.py — Quiz state machine for LearnUP.
"""

import os
import json
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESUME_PATH = os.path.join(BASE_DIR, "data", "resume.json")


class QuizSession:
    """Manages a single quiz attempt."""

    def __init__(self, questions, subject, chapter, difficulty="All"):
        self.subject = subject
        self.chapter = chapter
        self.difficulty = difficulty
        # Filter by difficulty
        if difficulty != "All":
            filtered = [q for q in questions if q.get("difficulty", "Medium") == difficulty]
            self.questions = filtered if filtered else questions
        else:
            self.questions = questions
        self.total = len(self.questions)
        self.index = 0
        self.score = 0
        self.answers = []  # list of (chosen, correct, is_correct)
        self.completed = False

    # ── Navigation ──────────────────────────────────────────────────────────

    def current_question(self):
        if self.index < self.total:
            return self.questions[self.index]
        return None

    def submit_answer(self, chosen_option):
        """Submit answer for current question. Returns True if correct."""
        q = self.current_question()
        if q is None:
            return False
        correct = q.get("answer", "")
        is_correct = (chosen_option == correct)
        if is_correct:
            self.score += 1
        self.answers.append({
            "question": q.get("question", ""),
            "chosen": chosen_option,
            "correct": correct,
            "is_correct": is_correct,
        })
        self.index += 1
        if self.index >= self.total:
            self.completed = True
        return is_correct

    def skip_question(self):
        q = self.current_question()
        if q:
            self.answers.append({
                "question": q.get("question", ""),
                "chosen": None,
                "correct": q.get("answer", ""),
                "is_correct": False,
            })
            self.index += 1
            if self.index >= self.total:
                self.completed = True

    def is_complete(self):
        return self.completed

    def progress_fraction(self):
        if self.total == 0:
            return 1.0
        return self.index / self.total

    def get_results(self):
        return {
            "subject": self.subject,
            "chapter": self.chapter,
            "score": self.score,
            "total": self.total,
            "accuracy": round(self.score / self.total * 100, 1) if self.total else 0,
            "answers": self.answers,
            "difficulty": self.difficulty,
        }

    # ── Resume ───────────────────────────────────────────────────────────────

    def save_resume(self):
        """Save current quiz progress for resume later."""
        if self.completed:
            _clear_resume()
            return
        data = {
            "subject": self.subject,
            "chapter": self.chapter,
            "difficulty": self.difficulty,
            "index": self.index,
            "score": self.score,
            "answers": self.answers,
        }
        os.makedirs(os.path.dirname(RESUME_PATH), exist_ok=True)
        with open(RESUME_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def restore_from_resume(self, resume_data):
        """Restore state from a saved resume dict."""
        self.index = resume_data.get("index", 0)
        self.score = resume_data.get("score", 0)
        self.answers = resume_data.get("answers", [])
        if self.index >= self.total:
            self.completed = True


def load_resume():
    """Return resume dict if one exists, else None."""
    if not os.path.isfile(RESUME_PATH):
        return None
    try:
        with open(RESUME_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if data.get("subject") and data.get("chapter"):
            return data
    except Exception:
        pass
    return None


def _clear_resume():
    if os.path.isfile(RESUME_PATH):
        os.remove(RESUME_PATH)


def clear_resume():
    _clear_resume()
