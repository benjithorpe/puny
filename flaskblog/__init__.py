import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or "secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flaskblog.db"

# Initialize the extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# redirect un-authenticated users to login page
login_manager.login_view = "login_page"
login_manager.login_message = "Please log in to access that page."
login_manager.login_message_category = "primary"

from flaskblog import routes
