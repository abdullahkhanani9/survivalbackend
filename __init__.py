from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
"""
These object can be used throughout project.
1.) Objects from this file can be included in many blueprints
2.) Isolating these object definitions avoids duplication and circular dependencies
"""

# Setup of key Flask object (app)
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://jplip.github.io"}})
# Setup SQLAlchemy object and properties for the database (db)
dbURI = 'sqlite:///volumes/sqlite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = dbURI
app.config['SECRET_KEY'] = 'SECRET_KEY'
db = SQLAlchemy()
Migrate(app, db)

# Images storage
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # maximum size of uploaded content
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']  # supported file types
app.config['UPLOAD_FOLDER'] = 'volumes/uploads/'  # location of user uploaded content

# Instantiate Login Manager
login_manager = LoginManager()
login_manager.login_view = "user_api.authenticate"  # Set the view for login
login_manager.init_app(app)  # Initialize app with login manager

from model.users import User

# Tell login manager how to get a user from the database
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Assuming user_id is an integer

# The load_user function should accept the user ID (user identifier) as an argument
# and return the corresponding user object from the database