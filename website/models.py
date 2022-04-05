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
    # Foreign key relationship on semester.id (1 semester to Many courses relationship) (FK = lowercase 'semester')
    semester_id = db.Column(db.Integer, db.ForeignKey('semester.id'))


class Semester(db.Model):
    # Make a semester_id as primary key
    id = db.Column(db.Integer, primary_key=True)
    # Make a semester_name as unique
    semester_name = db.Column(db.String(64), unique=True)
    # make a user_id as foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # make a semester_number
    semester_number = db.Column(db.Integer, unique=True)
    # make a list of courses as a relationship
    courses = db.relationship('Course')


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
    # Major
    major = db.Column(db.String(150))
    # Credits taken TODO: Make this NUMERIC
    credits_taken = db.Column(db.String(10))
    # Class standing
    class_standing = db.Column(db.String(10))
    # Each time a course is added, add to courses list in courses field (relationship = capital 'Course')
    courses = db.relationship('Course')
    # Each time a semester is added, add to semesters list in semesters field (relationship = capital 'Semester')
    semesters = db.relationship('Semester')
    # Number of semesters
    num_semesters = db.Column(db.Integer)
