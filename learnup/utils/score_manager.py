"""
score_manager.py — Quiz score persistence and export for LearnUP.
"""

import os
import json
import csv
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCORES_PATH = os.path.join(BASE_DIR, "data", "scores.json")


def load_scores():
    """Return list of score dicts from scores.json."""
    if not os.path.isfile(SCORES_PATH):
        return []
    try:
        with open(SCORES_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def save_score(topic, subject, score, total, difficulty="All"):
    """Append a new score record to scores.json."""
    scores = load_scores()
    accuracy = round((score / total * 100), 1) if total > 0 else 0
    entry = {
        "topic": topic,
        "subject": subject,
        "score": score,
        "total": total,
        "accuracy": accuracy,
        "difficulty": difficulty,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    scores.append(entry)
    os.makedirs(os.path.dirname(SCORES_PATH), exist_ok=True)
    with open(SCORES_PATH, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=2)
    return entry


def get_analytics(subject_filter=None):
    """Return per-topic analytics dict."""
    scores = load_scores()
    if subject_filter and subject_filter != "All":
        scores = [s for s in scores if s.get("subject") == subject_filter]
    analytics = {}
    for s in scores:
        key = f"{s['subject']} — {s['topic']}"
        if key not in analytics:
            analytics[key] = {"attempts": 0, "total_acc": 0, "best": 0, "subject": s["subject"]}
        analytics[key]["attempts"] += 1
        analytics[key]["total_acc"] += s.get("accuracy", 0)
        analytics[key]["best"] = max(analytics[key]["best"], s.get("accuracy", 0))
    for k in analytics:
        a = analytics[k]
        a["avg_acc"] = round(a["total_acc"] / a["attempts"], 1)
    return analytics


def export_scores_csv(filepath):
    """Export all scores to a CSV file."""
    scores = load_scores()
    if not scores:
        return False
    fieldnames = ["date", "subject", "topic", "score", "total", "accuracy", "difficulty"]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for s in scores:
            writer.writerow({k: s.get(k, "") for k in fieldnames})
    return True
