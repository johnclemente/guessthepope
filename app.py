# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import json
import os
from pathlib import Path
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "votes.db"
CARDINALS_PATH = BASE_DIR / "cardinals_with_images.json"

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "conclave2025prayfortheworld")  # Change in production

# Fix for running behind proxy
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

# --------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create table and seed rows on first run."""
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS votes (
                cardinal TEXT PRIMARY KEY,
                count    INTEGER NOT NULL DEFAULT 0
            )""")
        # seed rows only if table is empty
        row = db.execute("SELECT COUNT(*) AS c FROM votes").fetchone()
        if row["c"] == 0:
            with open(CARDINALS_PATH, "r") as f:
                cardinals = json.load(f)
            db.executemany(
                "INSERT INTO votes(cardinal, count) VALUES(?,0)",
                [(c["name"],) for c in cardinals],
            )
        db.commit()

def update_vote(cardinal_name):
    with get_db() as db:
        db.execute(
            "UPDATE votes SET count = count + 1 WHERE cardinal = ?",
            (cardinal_name,),
        )
        db.commit()

def fetch_all_votes():
    with get_db() as db:
        rows = db.execute("SELECT cardinal, count FROM votes ORDER BY count DESC").fetchall()
        return {row["cardinal"]: row["count"] for row in rows}

def fetch_cardinals():
    with open(CARDINALS_PATH) as f:
        return json.load(f)

# --------------------------------------------------------------------
# routes
# --------------------------------------------------------------------
# Initialize database when app starts
with app.app_context():
    init_db()

@app.route("/", methods=["GET", "POST"])
def vote():
    cardinals = fetch_cardinals()

    # Handle POST (submit vote)
    if request.method == "POST":
        selected = request.form.get("cardinal")
        if selected is None:
            flash("Please select a cardinal to vote for 🙏", "warning")
            return redirect(url_for("vote"))

        # stop double‑voting per session
        if session.get("voted_for"):
            flash(f"You already voted for {session['voted_for']}.", "info")
            return redirect(url_for("results"))

        update_vote(selected)
        session["voted_for"] = selected
        flash(f"Thank you for casting your vote for {selected}!", "success")
        return redirect(url_for("results"))

    return render_template("vote.html", cardinals=cardinals)

@app.route("/results")
def results():
    votes = fetch_all_votes()
    total_votes = sum(votes.values())
    
    # Get cardinals with images and titles
    cardinals_data = {cardinal["name"]: cardinal for cardinal in fetch_cardinals()}
    
    return render_template("results.html", votes=votes, total_votes=total_votes, cardinals=cardinals_data)

# tiny health endpoint for uptime checks
@app.route("/health")
def health():
    return "ok", 200

if __name__ == "__main__":
    # In production use gunicorn or uwsgi instead
    is_dev = os.getenv("FLASK_ENV") == "development"
    app.run(debug=is_dev, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
