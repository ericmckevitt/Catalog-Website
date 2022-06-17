# from turtle import update
# from unicodedata import category
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
# from numpy import deprecate
from .models import Course, Semester, User
from . import db
import json
# import python.codd as codd
from python.azure_connect import AzureConnection
import python.process_courses as pc
import python.schedule_validation as sv

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

# This will temporarily hold the ID for the semester that is being renamed
new_semester_name_ID = ""


def update_class_standing():
    # Update class standing based on credits taken
    if float(current_user.credits_taken) == 0:
        current_user.class_standing = "None"
    elif float(current_user.credits_taken) < 30:
        current_user.class_standing = "Freshman"
    elif float(current_user.credits_taken) >= 30 and float(current_user.credits_taken) < 60:
        current_user.class_standing = "Sophomore"
    elif float(current_user.credits_taken) >= 60 and float(current_user.credits_taken) < 90:
        current_user.class_standing = "Junior"
    else:
        current_user.class_standing = "Senior"


def compute_degree_progress():
    az = AzureConnection()
    # figure out how many credits are in the current major
    major = current_user.major
    # major = maj.major_map[major]
    query = f"""
        SELECT SUM(credit_hours) FROM {major}_major;
    """
    major_credits = az.execute(query)
    major_credits = major_credits['sum'].values[0]
    print(major_credits)
    user_credits = current_user.credits_taken
    percent = user_credits/major_credits * 100
    print('percentage completion:', percent)
    return percent


@views.route('/explore', methods=['GET', 'POST'])
@login_required
def explore():
    return render_template("explore.html", user=current_user)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # TODO: Implement semester building form
    if request.method == 'POST':
        print('Caught!')

        # Get semester name from form
        try:
            semester_new_name = request.form['semester_new_name']
            print('Reqest to rename semester.')

            # Rename semester
            semester_id = new_semester_name_ID
            print('semester_id:', semester_id)
            semester = Semester.query.filter_by(id=semester_id).first()
            print('Current semester name:', str(semester.semester_name))

            # Set the semester's name to the new name
            semester.semester_name = semester_new_name

            print('New semester name:', str(semester.semester_name))

            db.session.commit()
            print('Semester renamed.')

        except KeyError:
            # Handle adding a new course
            print('Request to add a new course.')

            # Get information from new course form
            department = request.form.get('department')
            course_number = request.form.get('course_number')
            semester_id = request.form.get('semester')
            # Print to console
            print(department)
            print(course_number)
            print(semester_id)

            # Get a codd database connection
            # dburi, inspector = codd.connect('Mines6515')

            # Use codd to get course info
            # course_info = codd.get_course_info(department, course_number, dburi)
            # print(course_info)

            course_info = pc.get_course_info(
                department, int(course_number.strip()))

            print(course_info)

            # extract data from course_info
            course_found = True
            course_name = ""
            course_credits = ""
            try:
                course_name = course_info[0]
                course_credits = course_info[3]
                print('course_name:', course_name)
                print('course credits:', course_credits)
                if course_credits == None or course_credits == "None":
                    course_credits = ""
            except:
                flash('Course not found!', category='error')
                course_found = False

            print("course_name:", course_name, type(course_name))
            print("course credits:", course_credits, type(course_credits))

            # If data is None, flash a message
            if department is None or course_number is None or semester_id is None:
                flash('Please fill out all fields.')
                return render_template('home.html')
            if course_found:
                print('Adding course to database')
                # Create new course object
                new_course = Course(department=department, course_number=course_number,
                                    course_name=course_name, credit_hours=course_credits, is_taken="False", user_id=current_user.id, semester_id=semester_id)
                # Add course to database
                db.session.add(new_course)
                db.session.commit()

    return render_template("home.html", user=current_user)


@views.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    # Check for new course added
    if request.method == 'POST':
        # note = request.form.get('note')
        department = request.form.get('department')
        course_number = request.form.get('course_number')

        print('department:', department)
        print('course_number:', course_number)

        # If submitting a new course
        if department and course_number:
            # Check for valid input
            if len(department) < 3:
                flash('Department name is invalid.', category='error')
            elif len(course_number) != 3:
                flash('Course number should be 3 digits.', category='error')
            else:
                # Check to see if this course has already been added
                for course in current_user.courses:
                    # If this course has already been taken
                    if department == course.department and course_number == course.course_number:
                        flash('You have already added this course.',
                              category='error')
                        return render_template("account.html", user=current_user)

                # If input is valid, try to look up the course name
                course_lookup = department + course_number
                try:
                    # Look up course information from codd
                    # dburi, inspector = codd.connect('Mines6515')
                    course_info = pc.get_course_info(
                        department, int(course_number.strip()))

                    # extract data from course_info
                    course_found = True
                    course_name = ""
                    course_credits = ""
                    try:
                        course_name = course_info[0]
                        course_credits = course_info[3]
                        if course_credits == None or course_credits == "None":
                            course_credits = ""
                    except:
                        flash('Course not found!', category='error')
                        course_found = False

                    print(course_name)
                    print(course_credits)

                    # Increment credits taken by that course's number of credits
                    try:
                        current_user.credits_taken = str(
                            float(current_user.credits_taken) + float(course_credits))
                    except:
                        flash('Course not found!', category='error')
                    # Check if class standing has changed and update it
                    update_class_standing()
                    # degree_progress = compute_degree_progress()
                    # Commit changes
                    db.session.commit()
                except Exception as e:
                    print(e)
                    flash('This is not a registered course in the system.',
                          category='error')
                    return render_template("account.html", user=current_user)
                # If course is not found in database, notify user and reload form
                if course_name == None or course_credits == None:
                    flash('This is not a registered course in the system.',
                          category='error')
                    return render_template("account.html", user=current_user)

                # TODO: Look up class in codd database once we have more courses entered
                # try:
                #     pass
                #     # TODO I can't write this yet because I need to connect to codd which requires Mines WiFi
                # except Exception:
                #     print('Failed to load course name')

                # Create Course row and add to database
                new_course = Course(
                    department=department, course_number=course_number, course_name=course_name, credit_hours=course_credits, is_taken="True", user_id=current_user.id)
                db.session.add(new_course)
                db.session.commit()
                flash('Course added!', category='success')

        major = request.form.get('major')
        if major:
            current_user.major = major
            db.session.commit()

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
            # Decrement credits_taken by this course's credits TODO Change this once I get codd connection
            department = course.department
            course_number = course.course_number
            course_lookup = department + course_number
            course_credits = courses_temp[course_lookup][1]
            if current_user.credits_taken > 0:
                current_user.credits_taken = str(
                    float(current_user.credits_taken) - float(course_credits))

            if current_user.credits_taken < 0:
                current_user.credits_taken = 0

            # Check if class standing has changed and update it
            update_class_standing()

            db.session.delete(course)
            db.session.commit()
    # Need to return something, so return empty data
    return jsonify({})


@views.route('/delete-course-from-semester', methods=['GET', 'POST'])
@login_required
def delete_course_from_semester():
    if request.method == 'POST':
        # Collect data from API call
        course_id = json.loads(request.data)['course_id']
        semester_id = json.loads(request.data)['semester_id']

        # Delete this course from this semester
        semester = Semester.query.get(semester_id)

        # Delete this course from this semester
        course = Course.query.get(course_id)
        if course and semester:
            # Delete this course from this semester
            semester.courses.remove(course)
            # Delete this course from the database
            db.session.delete(course)
            db.session.commit()

    return jsonify({})


@views.route('/delete-major', methods=['POST'])
def delete_major():
    current_user.major = 'None'
    db.session.commit()
    # Need to return something, so return empty data
    return jsonify({})


@views.route('/delete-semester', methods=['POST'])
def delete_semester():
    print('Delete Semester!')

    semester_id = json.loads(request.data)['semester_id']
    semester = Semester.query.get(semester_id)

    # Remove this semester from the user's list of semesters
    current_user.semesters.remove(semester)

    # TODO: MAYBE: Delete all courses in this semester
    # Delete all courses in this semester
    for course in semester.courses:
        db.session.delete(course)

    # Change all other semester ids above this id to be one less
    for s in current_user.semesters:
        if s.semester_number > semester.semester_number:
            s.semester_number -= 1
            # db.session.commit()

    db.session.delete(semester)
    # decrement the user's semester count
    current_user.num_semesters -= 1

    # Update the semester name for each to match the new semester number
    for s in current_user.semesters:
        s.semester_name = 'Semester ' + str(s.semester_number)

    db.session.commit()

    return jsonify({})


@views.route('/add-semester', methods=['POST'])
def add_semester():
    # make a new semester
    # add it to the user's list of semesters
    new_semester = Semester(
        user_id=current_user.id,
        semester_name=f'Semester {current_user.num_semesters + 1}',
        semester_number=current_user.num_semesters + 1)
    db.session.add(new_semester)
    # add 1 to the users number of semesters
    current_user.num_semesters += 1
    db.session.commit()
    flash('Semester Added!', category='success')

    print('Add Semester!')

    return jsonify({})


@views.route('/validate-schedule', methods=['GET', 'POST'])
@login_required
def validate_schedule():
    print('Validate Schedule!')

    if request.method == 'POST':
        # Get the current user's ID from the request
        userID = json.loads(request.data)['userID']

        # Get all the semesters for this user
        semesters = Semester.query.filter_by(user_id=userID).all()

        # If there are no semesters, return an error
        if semesters is None:
            flash('There are no semesters to validate!', category='error')
            return jsonify({'error': 'No semesters found'})

        # Make a list to hold all of the semesters
        semester_list = []

        # For each semester, get the courses and add them to the semester list
        for semester in semesters:
            # Get the name of the semester
            semester_name = semester.semester_name
            # make a Semester object from sv
            current_semester = sv.Semester(str(semester_name))

            # Make sure there are no courses in the semester already
            current_semester.set_courses([])

            # Get all the courses for this semester
            course_tables = Course.query.filter_by(
                semester_id=semester.id).all()

            # For each course
            for course in course_tables:
                # Get the course department and number
                course_department = str(course.department)
                course_number = int(course.course_number)

                # Grab the rest of the data from codd
                name, dept, cn, hours, prereqs, coreqs = pc.get_course_info(
                    course_department, course_number)

                # If the course is not found, print an error
                if name is None or name == '':
                    print("Course not found!")

                # Build a Course object from the data
                current_course = sv.Course(
                    name, dept, cn, hours, prereqs, coreqs)

                # Add the course to the current semester
                current_semester.add_course(current_course)

            # Add the semester to the list of semesters
            semester_list.append(current_semester)

        # Make a schedule object
        schedule = sv.Schedule(semester_list)

        # Validate the schedule
        is_schedule_valid, error_msg = schedule.validate_schedule()
        if is_schedule_valid:
            flash(f'Schedule is valid! {error_msg}', category='success')
        else:
            flash(f'Schedule is invalid! {error_msg}', category='error')

        # Get the class that is part of the error (word after "invalid!")
        if error_msg is not None and error_msg != '':
            error_class = error_msg.split(' ')[0]
            print(error_class)

    return jsonify({})


@views.route('/rename-semester', methods=['GET', 'POST'])
@login_required
def rename_semester():
    if request.method == 'POST':
        # Get the semester ID
        global new_semester_name_ID
        new_semester_name_ID = str(json.loads(request.data)['semester_id'])
    return jsonify({})
