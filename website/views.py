from unicodedata import category
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from numpy import deprecate
from .models import Course
from . import db
import json

# Initialize blueprint called names
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    # Check for new course added
    if request.method == 'POST':
        # note = request.form.get('note')
        department = request.form.get('department')
        course_number = request.form.get('course_number')
        if len(department) != 4:
            flash('Department name should be 4 digits.', category='error')
        elif len(course_number) != 3:
            flash('Course number should be 3 digits.', category='error')
        else:
            new_course = Course(
                department=department, course_number=course_number, user_id=current_user.id)
            db.session.add(new_course)
            db.session.commit()
            flash('Course added!', category='success')
    return render_template("account.html", user=current_user)


@views.route('/delete-course', methods=['POST'])
def delete_course():
    # Take stringified data and turn to python dict.
    course = json.loads(request.data)
    courseId = course['courseId']
    course = Course.query.get(courseId)
    # If we found a note
    if course:
        # If this is the current user's note
        if course.user_id == current_user.id:
            db.session.delete(course)
            db.session.commit()
    # Need to return something, so return empty data
    return jsonify({})
