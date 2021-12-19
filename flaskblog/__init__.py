import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or "secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flaskblog.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


from flaskblog import routes
