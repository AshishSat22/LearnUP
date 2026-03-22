from flask import Flask, render_template, request, jsonify
import json
import os

from utils.file_handler import (
    list_subjects, list_video_chapters, load_videos, search_videos,
    list_question_chapters, load_questions, search_questions,
    list_quiz_subjects, list_quiz_chapters, load_quiz
)
from utils.score_manager import load_scores, save_score, get_analytics
from utils.bookmark_manager import (
    load_bookmarks, is_bookmarked, toggle_bookmark, 
    add_bookmark, remove_bookmark
)

app = Flask(__name__)

@app.route("/")
def index():
    subjects = list_subjects("resources")
    quiz_subjects = list_quiz_subjects()
    # Merge both subject lists to display in the home page
    all_subjects = sorted(list(set(subjects + quiz_subjects)))
    return render_template("home.html", subjects=all_subjects)

@app.route("/subject/<subject>")
def subject_view(subject):
    video_chapters = list_video_chapters(subject)
    question_chapters = list_question_chapters(subject)
    quiz_chapters = list_quiz_chapters(subject)
    return render_template("chapter_list.html", 
                           subject=subject,
                           video_chapters=video_chapters,
                           question_chapters=question_chapters,
                           quiz_chapters=quiz_chapters)

@app.route("/videos/<subject>/<chapter>")
def videos_view(subject, chapter):
    videos = load_videos(subject, chapter)
    # Check bookmarks
    for i, v in enumerate(videos):
        # v is (title, url)
        bookmarked = is_bookmarked("video", subject, chapter, v[0])
        videos[i] = {"title": v[0], "url": v[1], "bookmarked": bookmarked}
    return render_template("videos.html", subject=subject, chapter=chapter, videos=videos)

@app.route("/questions/<subject>/<chapter>")
def questions_view(subject, chapter):
    content = load_questions(subject, chapter)
    bookmarked = is_bookmarked("question", subject, chapter, chapter)
    return render_template("questions.html", subject=subject, chapter=chapter, content=content, bookmarked=bookmarked)

@app.route("/quiz/<subject>/<chapter>")
def quiz_view(subject, chapter):
    questions = load_quiz(subject, chapter)
    return render_template("quiz.html", subject=subject, chapter=chapter, questions=questions)

@app.route("/api/submit_quiz", methods=["POST"])
def submit_quiz():
    data = request.json
    # data: topic, subject, score, total, difficulty
    entry = save_score(
        topic=data.get("chapter"),
        subject=data.get("subject"),
        score=data.get("score"),
        total=data.get("total"),
        difficulty=data.get("difficulty", "All")
    )
    return jsonify({"success": True, "entry": entry})

@app.route("/scores")
def scores_view():
    scores = load_scores()
    analytics = get_analytics()
    return render_template("scores.html", scores=scores, analytics=analytics)

@app.route("/bookmarks")
def bookmarks_view():
    bookmarks = load_bookmarks()
    return render_template("bookmarks.html", bookmarks=bookmarks)

@app.route("/api/toggle_bookmark", methods=["POST"])
def api_toggle_bookmark():
    data = request.json
    btype = data.get("type")
    subject = data.get("subject")
    chapter = data.get("chapter")
    title = data.get("title")
    url = data.get("url", "")
    added = toggle_bookmark(btype, subject, chapter, title, url)
    return jsonify({"success": True, "added": added})

@app.route("/search")
def search_view():
    query = request.args.get("q", "")
    video_results = search_videos(query) if query else []
    question_results = search_questions(query) if query else []
    return render_template("search.html", query=query, video_results=video_results, question_results=question_results)

@app.route("/official_papers")
def official_papers_index():
    return render_template("official_papers.html", subject=None)

@app.route("/official_papers/<subject>")
def official_papers_view(subject):
    year = request.args.get("year", "2023_24")
    return render_template("official_papers.html", subject=subject, year=year)

@app.route("/external_resources")
def external_resources_view():
    return render_template("external_resources.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
