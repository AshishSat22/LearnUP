"""
file_handler.py — All file I/O helpers for LearnUP.
"""

import os
import json
import urllib.parse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


def _data_path(*parts):
    return os.path.join(DATA_DIR, *parts)


# ── Subjects ────────────────────────────────────────────────────────────────

def list_subjects(section="resources"):
    """Return sorted list of subject folder names under data/<section>/."""
    path = _data_path(section)
    if not os.path.isdir(path):
        return []
    return sorted(d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d)))


def list_quiz_subjects():
    return list_subjects("quizzes")


# ── Chapters ─────────────────────────────────────────────────────────────────

def list_chapters(section, subject):
    """Return sorted list of chapter names (without extension) for a subject."""
    path = _data_path(section, subject) if section != "quizzes" else _data_path("quizzes", subject)
    if section == "questions":
        path = _data_path("questions", "sample", subject)
    if not os.path.isdir(path):
        return []
    files = []
    for f in sorted(os.listdir(path)):
        name, ext = os.path.splitext(f)
        if ext in (".txt", ".json"):
            files.append(name)
    return sorted(list(set(files)))


def list_video_chapters(subject):
    return list_chapters("resources", subject)


def list_question_chapters(subject):
    return list_chapters("questions", subject)


def list_quiz_chapters(subject):
    return list_chapters("quizzes", subject)


# ── Videos ──────────────────────────────────────────────────────────────────

def load_videos(subject, chapter):
    """Return list of (title, url) tuples from data/resources/<subject>/<chapter>.txt."""
    chapter = urllib.parse.unquote(chapter).replace("%20", " ")
    path = _data_path("resources", subject, f"{chapter}.txt")
    
    # Sophisticated Fallback: Try case-insensitive and underscore match
    if not os.path.isfile(path):
        subject_path = _data_path("resources", subject)
        if os.path.isdir(subject_path):
            norm_target = chapter.lower().replace(" ", "").replace("_", "")
            for f in os.listdir(subject_path):
                f_name, f_ext = os.path.splitext(f)
                if f_ext == ".txt" and f_name.lower().replace(" ", "").replace("_", "") == norm_target:
                    path = os.path.join(subject_path, f)
                    break

    videos = []
    if not os.path.isfile(path):
        return videos
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "||" in line:
                    parts = line.split("||", 1)
                    title = parts[0].strip()
                    url = parts[1].strip()
                    if title and url:
                        videos.append((title, url))
    except Exception:
        pass
    return videos


def search_videos(query, subject_filter=None):
    """Search across all video files. Returns list of dicts."""
    results = []
    subjects = list_subjects("resources")
    if subject_filter and subject_filter in subjects:
        subjects = [subject_filter]
    q = query.lower()
    for subject in subjects:
        for chapter in list_video_chapters(subject):
            for title, url in load_videos(subject, chapter):
                if q in title.lower() or q in chapter.lower():
                    results.append({
                        "subject": subject, "chapter": chapter,
                        "title": title, "url": url, "type": "video"
                    })
    return results


# ── Questions ────────────────────────────────────────────────────────────────

def load_questions(subject, chapter):
    """Return list of dicts (JSON) or raw text if txt file."""
    chapter = urllib.parse.unquote(chapter).replace("%20", " ")
    json_path = _data_path("questions", "sample", subject, f"{chapter}.json")
    txt_path = _data_path("questions", "sample", subject, f"{chapter}.txt")
    
    # Fallback for questions
    if not os.path.isfile(json_path) and not os.path.isfile(txt_path):
        sub_path = _data_path("questions", "sample", subject)
        if os.path.isdir(sub_path):
            norm_target = chapter.lower().replace(" ", "").replace("_", "")
            for f in os.listdir(sub_path):
                f_name, f_ext = os.path.splitext(f)
                if f_name.lower().replace(" ", "").replace("_", "") == norm_target:
                    if f_ext == ".json": json_path = os.path.join(sub_path, f)
                    if f_ext == ".txt": txt_path = os.path.join(sub_path, f)

    if os.path.isfile(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            return [{"question": f"Error loading JSON: {e}", "answer": ""}]
    elif os.path.isfile(txt_path):
        try:
            with open(txt_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Error reading questions: {e}"
    else:
        return f"No questions found for {subject} > {chapter}."


def search_questions(query, subject_filter=None):
    """Search across all question files (JSON or TXT). Returns list of dicts."""
    results = []
    subjects = list_subjects("questions")
    if subject_filter and subject_filter in subjects:
        subjects = [subject_filter]
    q = query.lower()
    for subject in subjects:
        for chapter in list_question_chapters(subject):
            content = load_questions(subject, chapter)
            if isinstance(content, list):
                # New JSON format
                for i, item in enumerate(content):
                    q_text = item.get("question", "")
                    if q in q_text.lower():
                        results.append({
                            "subject": subject, "chapter": chapter,
                            "snippet": q_text[:120], "type": "question",
                            "line": i
                        })
            elif isinstance(content, str):
                # Old TXT format
                lines = content.splitlines()
                for i, line in enumerate(lines):
                    if q in line.lower():
                        results.append({
                            "subject": subject, "chapter": chapter,
                            "snippet": line.strip()[:120], "type": "question",
                            "line": i
                        })
    return results


# ── Quizzes ──────────────────────────────────────────────────────────────────

def load_quiz(subject, chapter):
    """Return list of question dicts from data/quizzes/<subject>/<chapter>.json."""
    chapter = urllib.parse.unquote(chapter).replace("%20", " ")
    path = _data_path("quizzes", subject, f"{chapter}.json")
    
    if not os.path.isfile(path):
        sub_path = _data_path("quizzes", subject)
        if os.path.isdir(sub_path):
            norm_target = chapter.lower().replace(" ", "").replace("_", "")
            for f in os.listdir(sub_path):
                f_name, f_ext = os.path.splitext(f)
                if f_ext == ".json" and f_name.lower().replace(" ", "").replace("_", "") == norm_target:
                    path = os.path.join(sub_path, f)
                    break

    if not os.path.isfile(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
    except Exception:
        pass
    return []


# ── Config ───────────────────────────────────────────────────────────────────

CONFIG_PATH = os.path.join(BASE_DIR, "data", "config.json")

def load_config():
    if not os.path.isfile(CONFIG_PATH):
        return {"theme": "light"}
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"theme": "light"}


def save_config(cfg):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
