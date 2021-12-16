from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

posts = [
    {
        "author": "John Doe",
        "title": "First normal title",
        "content": "This is the first blog content",
        "date_posted": "January 10, 2021",
    },
    {
        "author": "Jane Smith",
        "title": "Second Post title",
        "content": "This is the second blog content",
        "date_posted": "June 20, 2021",
    },
    {
        "author": "Johnny Kane",
        "title": "UIkit is awesome",
        "content": "This is a very long blog content to post here!!",
        "date_posted": "April 12, 2021",
    },
]


@app.route("/")
def index_page():
    return render_template("index.html", posts=posts)

@app.route("/about")
def about_page():
    return render_template("about.html")
