from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import (DataRequired, Length, EqualTo, Email,
                                ValidationError)
from flask_login import current_user

from flaskblog.models import User


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(),
                           Length(min=4, max=20),
                        ])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[
                                     DataRequired(),
                                     EqualTo("password",
                                        message="Passwords must be equal."),
                                     ])
    submit = SubmitField("Register")

    def validate_username(self, username):
        """Checks if the username already exists in the database
        Raise ValidationError if available else None/empty list
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already taken!")

    def validate_email(self, email):
        """Checks if the email already exists in the database
        Raise ValidationError if available else None/empty list
        """
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("Email already exists!")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(),
                           Length(min=4, max=20),
                        ])
    email = StringField("Email", validators=[DataRequired(), Email()])
    profile_picture = FileField("Update Profile Picture", validators=[
                                FileAllowed(["png", "jpg", "jpeg", "svg"])
                                ])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username already taken!")

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError("Email already exists!")
