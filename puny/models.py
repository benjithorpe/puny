from uuid import uuid4
from datetime import datetime

from flask_login import UserMixin

from puny import login_manager, db


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    # Converts the uuid to string, take 15 values then convert to int
    id = db.Column(db.Integer, default=lambda: int(str(uuid4().int)[:15]),
                        primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    profile_image = db.Column(db.String(20), nullable=False,
                              default="default.jpg")
    bio = db.Column(db.String(300), default="Less is More")
    is_admin = db.Column(db.Boolean(), default=False)

    # Relationships
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Post(db.Model):
    id = db.Column(db.String, primary_key=True, default=lambda: uuid4().hex)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)

    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"),
                        nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Comment:
    pass


db.create_all()
