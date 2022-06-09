import os
import secrets

from flask import render_template, flash, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from PIL import Image

from puny import app, db
from puny.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                        CreatePostForm, UpdatePostForm)
from puny.models import User, Post


@app.route("/")
def index():
    posts = Post.query.all()
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
            flash(f"Welcome back {user.username}!!", "success")
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


def resize_image(image, size=(125, 125)):
    resized_image = Image.open(image)
    resized_image.thumbnail(size)
    return resized_image

def delete_image(image):
    print("Image deleted")
    pass


def save_profile(image):
    # Generate random token string
    random_hex = secrets.token_hex(8)
    # Get the extension of the image submitted
    _, file_ext = os.path.splitext(image.filename)
    new_image = random_hex + file_ext
    # Save the new generated image to the uploads folder
    path = os.path.join(app.root_path, "static/uploads", new_image)
    # Delete previous profile image
    delete_image(image)
    # Resize the image (to save server space)
    resized_image = resize_image(image)
    resized_image.save(path)

    return new_image


@app.route("/profile")
@login_required
def profile_page():
    profile_img = url_for('static',
                          filename=f'uploads/{current_user.profile_image}')
    return render_template("profile.html", profile_img=profile_img)


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings_page():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        # Check if user has changed their profile, then update it
        if form.picture.data:
            picture = save_profile(form.picture.data)
            current_user.profile_image = picture

        # Update username, email and bio
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data

        # Save changes to the database
        db.session.commit()
        flash("Your account has been updated successfully", "success")
        return redirect(url_for("profile_page"))
    elif request.method == "GET":
        # Populate the forms
        form.email.data = current_user.email
        form.username.data = current_user.username
        form.bio.data = current_user.bio

    return render_template("settings.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/post/<post_id>")
@login_required
def post_page(post_id):
    post = Post.query.filter_by(id=post_id).first()
    return render_template("post.html", post=post)


@app.route("/post/create", methods=["GET", "POST"])
@login_required
def create_post():
    form = CreatePostForm()

    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data,
                    author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!", "success")
        return redirect(url_for("index"))

    return render_template("create-post.html", form=form)


@app.route("/post/update/<post_id>", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    # Get the post
    post = Post.query.filter_by(id=post_id).first()
    form = UpdatePostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been updated!", "success")
        return redirect(url_for("index"))
        # return redirect(url_for("post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content

    return render_template("create-post.html", form=form)


@app.route("/post/delete/<post_id>", methods=["GET", "POST"])
@login_required
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    flash("Your post has been updated!", "success")
    return redirect(url_for("index"))

