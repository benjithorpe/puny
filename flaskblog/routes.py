from flask import render_template, redirect, url_for, flash

from flaskblog import app, db, bcrypt
from flaskblog.forms import LoginForm, RegistrationForm
from flaskblog.models import User, Post


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
        # Hash the user's password from the form
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        # Create a new user to be added to the database
        user = User(username=form.username.data, email=form.email.data,
                    password=hashed_password)
        # Adds the user to the database
        db.session.add(user)
        db.session.commit()
        flash(f"Account Created, you are now able to log in!", "success")
        return redirect(url_for("login_page"))

    return render_template("register.html", form=form)
