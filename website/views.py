from unicodedata import category
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from numpy import deprecate
from .models import Course
from . import db
import json

# Initialize blueprint called names
views = Blueprint('views', __name__)

# TODO: Remove this once I can connect to Codd (TEMPORARY SOLUTION)
courses_temp = {
    'MATH111': ['Calculus 1', 4.0],
    'CSM101': ['Freshman Success Seminar', 0.5],
    'CHGN121': ['Principles of Chemistry 1', 4.0],
    'CSCI101': ['Introduction to Computer Science', 3.0],
    'HASS100': ['Nature and Human Values', 4.0],
    'MATH112': ['Calculus 2', 4.0],
    'PHGN100': ['Physics 1', 4.5],
    'EDNS151': ['Design 1', 3.0],
    'CSCI261': ['Programming Concepts', 3.0],
    'CSCI262': ['Data Structures', 3.0],
    'CSCI274': ['Introduction to the Linux Operating System', 1.0],
    'CSCI306': ['Software Engineering', 3.0],

}


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

        # Check for valid input
        if len(department) != 4:
            flash('Department name should be 4 digits.', category='error')
        elif len(course_number) != 3:
            flash('Course number should be 3 digits.', category='error')
        else:
            # If input is valid, try to look up the course name
            course_lookup = department + course_number
            try:
                course_name = courses_temp[course_lookup][0]
                credit_hours = courses_temp[course_lookup][1]
            except KeyError:
                flash('This is not a registered course in the system.',
                      category='error')
                return render_template("account.html", user=current_user)
            # If course is not found in database, notify user and reload form
            if course_name == None or credit_hours == None:
                flash('This is not a registered course in the system.',
                      category='error')
                return render_template("account.html", user=current_user)

            # try:
            #     pass
            #     # TODO I can't write this yet because I need to connect to codd which requires Mines WiFi
            # except Exception:
            #     print('Failed to load course name')

            # Create Course row and add to database
            new_course = Course(
                department=department, course_number=course_number, course_name=course_name, credit_hours=credit_hours, user_id=current_user.id)
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
