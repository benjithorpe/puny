import os

from flask import Flask, render_template, redirect, url_for, flash

from forms import LoginForm, RegistrationForm


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or "secret key"

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


@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        if form.email.data == "jack@m.com" and form.password.data == "pass":
            flash("You have been logged in successfully", "success")
            print("successfully posted")
            return redirect(url_for("index_page"))
        else:
            flash("Invalid Email or Password, Try again!!...", "danger")

    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegistrationForm()

    if form.validate_on_submit():
        flash(f"Account Created for {form.username.data}!!!", "success")
        return redirect(url_for("index_page"))

    return render_template("register.html", form=form)

