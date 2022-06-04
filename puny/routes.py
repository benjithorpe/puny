from flask import render_template, flash, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required

from puny import app, db
from puny.forms import RegistrationForm, LoginForm, UpdateAccountForm
from puny.models import User, Post


posts = [
  {
    "id": 1,
    "author": "John Doe",
    "date_posted": "January 12, 2021",
    "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
    "content": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
  },
  {
    "id": 2,
    "author": "John Doe",
    "date_posted": "January 12, 2021",
    "title": "qui est esse",
    "content": "est rerum tempore vitae\nsequi sint nihil reprehenderit dolor beatae ea dolores neque\nfugiat blanditiis voluptate porro vel nihil molestiae ut reiciendis\nqui aperiam non debitis possimus qui neque nisi nulla"
  },
  {
    "id": 3,
    "author": "John Doe",
    "date_posted": "January 12, 2021",
    "title": "ea molestias quasi exercitationem repellat qui ipsa sit aut",
    "content": "et iusto sed quo iure\nvoluptatem occaecati omnis eligendi aut ad\nvoluptatem doloribus vel accusantium quis pariatur\nmolestiae porro eius odio et labore et velit aut"
  },
  {
    "id": 4,
    "author": "John Doe",
    "date_posted": "January 12, 2021",
    "title": "eum et est occaecati",
    "content": "ullam et saepe reiciendis voluptatem adipisci\nsit amet autem assumenda provident rerum culpa\nquis hic commodi nesciunt rem tenetur doloremque ipsam iure\nquis sunt voluptatem rerum illo velit"
  },
  {
    "id": 5,
    "author": "John Doe",
    "date_posted": "January 12, 2021",
    "title": "nesciunt quas odio",
    "content": "repudiandae veniam quaerat sunt sed\nalias aut fugiat sit autem sed est\nvoluptatem omnis possimus esse voluptatibus quis\nest aut tenetur dolor neque"
  },
  {
    "id": 6,
    "author": "John Doe",
    "date_posted": "January 12, 2021",
    "title": "dolorem eum magni eos aperiam quia",
    "content": "ut aspernatur corporis harum nihil quis provident sequi\nmollitia nobis aliquid molestiae\nperspiciatis et ea nemo ab reprehenderit accusantium quas\nvoluptate dolores velit et doloremque molestiae"
  },
]

@app.route("/")
def index():
    return render_template("index.html", posts=posts)


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()

    if form.validate_on_submit():
        # Get the first user with the email submitted
        user = User.query.filter_by(email=form.email.data).first()
        # If user exists, log them in, else display error message
        if user and check_password_hash(user.password, form.password.data):
            flash(f"Welcome back {form.email.data}!!",
                  "bg-green-200 text-green-900")
            login_user(user, remember=form.remember.data)

            # Get the next page if it exists
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for("index"))
            # return redirect(next_page) if next_page else redirect(url_for("index"))
        else:
            flash(f"Invalid email and password, Try again", "error")

    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegistrationForm()

    if form.validate_on_submit():
        # Hash the password using werkzeug
        hashed_password = generate_password_hash(form.password.data)
        # Create new user
        user = User(username=form.username.data, email=form.email.data,
                    password=hashed_password)
        # Add user to the database
        db.session.add(user)
        db.session.commit()

        flash(f"Account created for {form.username.data}", "success")
        login_user(user)
        return redirect(url_for("login_page"))

    return render_template("register.html", form=form)


@app.route("/profile")
@login_required
def profile_page():
    profile_img = url_for('static',
                          filename=f"images/{current_user.profile_image}")

    return render_template("profile.html", profile_img=profile_img)


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings_page():
    form = UpdateAccountForm()
    return render_template("settings.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
