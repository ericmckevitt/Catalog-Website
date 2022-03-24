from email.policy import default
from enum import unique
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Course(db.Model):
    # Make id an integer which is the primary key
    id = db.Column(db.Integer, primary_key=True)
    # department will be like 'MATH' or 'CSCI'
    department = db.Column(db.String(4))
    # course number will be like '225' or '403'
    course_number = db.Column(db.String(3))
    # course name
    course_name = db.Column(db.String(500))
    # credit hours TODO make this NUMERIC(2,1)
    credit_hours = db.Column(db.String(10))
    # Foreign key relationship on user.id (1 user to Many courses relationship) (FK = lowercase 'user')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


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
    # Each time a course is added, add to courses list in courses field (relationship = capital 'Course')
    courses = db.relationship('Course')
