import os
import secrets

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from flaskblog import app, db, bcrypt
from flaskblog.forms import LoginForm, RegistrationForm, UpdateAccountForm
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
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user, remember=form.remember_me.data)
            # Get next page if user has tried to access the restricted page
            next_page = request.args.get("next")
            flash("You have been logged in successfully", "success")
            if next_page:
                return redirect(next_page)
            return redirect(url_for("index_page"))
        else:
            flash("Invalid Email or Password, Try again!!...", "danger")
            return redirect(url_for("login_page"))

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout_page():
    logout_user()
    return redirect(url_for("index_page"))


@app.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Hash the user's password from the form
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        # Create a new user to be added to the database
        user = User(username=form.username.data, email=form.email.data,
                    password=hashed_password)
        # Add the user to the database
        db.session.add(user)
        db.session.commit()
        flash(f"Account Created, you are now able to log in!", "success")
        return redirect(url_for("login_page"))

    return render_template("register.html", form=form)


def save_profile_image(image):
    random_hex = secrets.token_hex(8)
    _, image_extension = os.path.splitext(image.filename)
    new_image_name = (random_hex + image_extension)
    image_path = os.path.join(app.root_path,
                            f"static/images/profile_pics/{new_image_name}")
    # Save image to the image_path folder specified
    image.save(image_path)

    # Delete previous profile picture if it still exists
    previous_profile_image = os.path.join(app.root_path,
                            f"static/images/profile_pics/"
                            + current_user.profile_picture)
    try:
        if previous_profile_image != os.path.join(app.root_path,
                            "static/images/profile_pics/default_profile.jpg"):
            os.remove(previous_profile_image)
    except FileNotFoundError:
        pass
    # Return the random new image name generated
    return new_image_name

@app.route("/account", methods=["GET", "POST"])
@login_required
def account_page():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # Check if profile image was updated
        if form.profile_picture.data:
            # Rename the picture uploaded then update the database
            updated_image = save_profile_image(form.profile_picture.data)
            current_user.profile_picture = updated_image

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your Account has been updated", "success")
        return redirect(url_for("account_page"))
    # Populate form with user data
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        profile_picture = url_for('static', filename=
                        f"images/profile_pics/{current_user.profile_picture}")
    return render_template("account.html", form=form,
                           profile_picture=profile_picture)
