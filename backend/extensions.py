"""
Flask extensions initialization
This file prevents circular imports by centralizing extension initialization
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()