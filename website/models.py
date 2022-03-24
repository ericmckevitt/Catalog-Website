from email.policy import default
from enum import unique
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    # Define table columns

    # Make id an integer which is the primary key
    id = db.Column(db.Integer, primary_key=True)
    # Make cwid an integer
    cwid = db.Column(db.Integer, unique=True)
    # Max chars of 150, add unique constraint
    email = db.Column(db.String(150), unique=True)
    # Password is String with max length of 150
    password = db.Column(db.String(150))
    # First Name is String with max length of 150
    first_name = db.Column(db.String(150))
    # Last Name is String with max length of 150
    last_name = db.Column(db.String(150))
