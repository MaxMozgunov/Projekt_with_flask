import os

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

from board.database import get_db

import os
import openai

from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("AI_KEY")

from openai import OpenAI
client= OpenAI()

bp = Blueprint("posts", __name__)

@bp.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        author = request.form['author'] or "NoName"
        message = request.form['message']
        if message:
            db = get_db()
            db.execute("INSERT INTO post (author, message) VALUES (?, ?)",(author, message))
            db.commit()
            current_app.logger.info(f"New post by {author}")
            
            flash(f"Thank you, {author}!", category="success")
            return redirect(url_for("posts.posts"))
        else:
            flash("Something wrong!", category="error")
            current_app.logger.info(f"Don't have message")


    return render_template("posts/create.html")


@bp.route("/posts")
def posts():
    db = get_db()
    posts = db.execute("SELECT author, message, created FROM post ORDER BY created DESC").fetchall()
    return render_template("posts/posts.html", posts = posts)


@bp.route("/generate_message")
def generate_message(prompt):
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=f"Write a post about {prompt}"
    )