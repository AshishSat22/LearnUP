"""
bookmark_manager.py — Bookmark CRUD for LearnUP.
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOKMARKS_PATH = os.path.join(BASE_DIR, "data", "bookmarks.json")


def load_bookmarks():
    if not os.path.isfile(BOOKMARKS_PATH):
        return []
    try:
        with open(BOOKMARKS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def _save(bookmarks):
    os.makedirs(os.path.dirname(BOOKMARKS_PATH), exist_ok=True)
    with open(BOOKMARKS_PATH, "w", encoding="utf-8") as f:
        json.dump(bookmarks, f, indent=2)


def _key(btype, subject, chapter, title):
    return (btype, subject, chapter, title)


def is_bookmarked(btype, subject, chapter, title):
    bm = load_bookmarks()
    return any(
        b.get("type") == btype and b.get("subject") == subject
        and b.get("chapter") == chapter and b.get("title") == title
        for b in bm
    )


def add_bookmark(btype, subject, chapter, title, url=""):
    if is_bookmarked(btype, subject, chapter, title):
        return
    bm = load_bookmarks()
    bm.append({
        "type": btype,
        "subject": subject,
        "chapter": chapter,
        "title": title,
        "url": url,
    })
    _save(bm)


def remove_bookmark(btype, subject, chapter, title):
    bm = load_bookmarks()
    bm = [
        b for b in bm
        if not (b.get("type") == btype and b.get("subject") == subject
                and b.get("chapter") == chapter and b.get("title") == title)
    ]
    _save(bm)


def toggle_bookmark(btype, subject, chapter, title, url=""):
    if is_bookmarked(btype, subject, chapter, title):
        remove_bookmark(btype, subject, chapter, title)
        return False
    else:
        add_bookmark(btype, subject, chapter, title, url)
        return True
