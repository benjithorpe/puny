from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import (StringField, EmailField, PasswordField, SubmitField,
                     BooleanField, TextAreaField, FileField)
from wtforms.validators import (DataRequired, Length, Email,
                                EqualTo, ValidationError)

from puny.models import User


class RegistrationForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(), Length(min=2, max=15)])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(),
                             Length(min=4)])
    confirm_password = PasswordField("Confirm Password",
                                     validators=[DataRequired(),
                                     EqualTo("password")])
    submit = SubmitField("Register")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email is already taken!")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username is already taken!")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password",
                             validators=[DataRequired(), Length(min=4)])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(), Length(min=2, max=15)])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    # profile_image = FileField("Image File")
    bio = TextAreaField("Bio", validators=[Length(min=4, max=250)])
    submit = SubmitField("Update Account")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Email is already taken!")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username is already taken!")