# from asyncio.windows_events import NULL
from multiprocessing import synchronize
from tabnanny import check
from unicodedata import category
# from winreg import REG_QWORD
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Course, Semester
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from . import db_controller as controller

# Initialize blueprint called auth
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # If user is logging in, collect data
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if user email is valid and in database
        user = User.query.filter_by(email=email).first()
        # If user found with this email
        if user:
            # If no password has been entered, have user try again
            if len(password) < 1:
                flash('Please enter your password.', category='error')
                return render_template("login.html", user=current_user)

            # Check if password is correct
            if check_password_hash(user.password, password):
                flash('Login Successful!', category='success')
                # Log in the user, remember so that user doesn't need to login each time
                login_user(user, remember=True)
                # Redirect user to home page
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('There is no account set up with this email.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    # @login_required : asserts that user can't access page until logged in
    # Log out user and send to login page
    flash('Logged out.', category='success')
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    # adding test users 1, 2, 3
    if User.query.filter_by(cwid=10101010).count() == 1:
        # testing, remove this later
        #not sure if this woks yet
        #db.session = 1
        temp_user = User.query.filter_by(cwid=10101010).first()
        merged_object = db.session.merge(temp_user)
        db.session.delete(merged_object)
        db.session.commit()
    if User.query.filter_by(cwid=10101010).count() == 0:
        controller.addUser(db, 10101010, 'testUser1@mines.edu', 'test1f', 'test1l', 'TEST MAJOR1', 69, 'Freshman', 'test1password')
        #adding classes and semesters for user 1

        user1 = User.query.filter_by(cwid=10101010).first()
        user1_id = user1.id # getting the user id
        print(user1_id)

        semester_number = 1 # number for this specific user

        semester_id = Semester.query.count() + semester_number + 1 # getting semeseter id, +1 because we want the next one
        semester_name = "testUser1 semester #" + str(semester_number)

        courses = [] # courses empty for now

        # add_semester(db, id, semester_name, user_id, semester_number, courses)
        # making sure there is no duplicates
        controller.delete_semesters_by_name(db, "testUser1 semester #1")
        controller.delete_semesters_by_null_id(db)

        controller.add_semester(db, semester_id, semester_name, user1_id, semester_number, courses)

        #user1.add_semester()

    if User.query.filter_by(cwid=20202020).count() == 0:
        controller.addUser(db, 20202020, 'testUser2@mines.edu', 'test2f', 'test2l', 'TEST MAJOR2', 420, 'Sophomore', 'test2password')
    if User.query.filter_by(cwid=30303030).count() == 0:
        controller.addUser(db, 30303030, 'testUser3@mines.edu', 'test3f', 'test3l', 'TEST MAJOR3', 69420, 'Junior', 'test3password')

    
        #adding classes and semesters for user 2

        #adding classes and semesters for user 3
    #

    if request.method == 'POST':
        # Collect form data from POST request
        cwid = request.form.get('cwid')
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        major = 'None'
        credits_taken = '0.0'
        class_standing = 'None'

        # Check if this user exists already
        user = User.query.filter_by(email=email).first()
        if user:
            flash('An account with this email already exists.', category='error')
        # Check if data is valid
        elif cwid.isdigit() == False or len(cwid) != 8:
            flash('CWID must be an 8-digit number.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif '@mines.edu' not in email:
            flash('Email must be an @mines.edu account.', category='error')
        elif len(first_name) < 1:
            flash('First name must be at least 1 character.', category='error')
        elif len(last_name) < 1:
            flash('Last name must be at least 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # add user to database
            # Define the user and hash their password using sha256 hash function
            new_user = User(cwid=cwid, email=email, first_name=first_name, last_name=last_name, major=major,
                            credits_taken=credits_taken, class_standing=class_standing, password=generate_password_hash(
                                password1, method='sha256'), num_semesters=0)

            # Add the user and commit changes
            db.session.add(new_user)
            db.session.commit()

            # Log in the user, remember so that user doesn't need to login each time
            # TODO check if this should be user or new_user
            login_user(new_user, remember=True)

            # Flash success message to user on front end
            flash('Account created!', category='success')

            # Redirect user to home page
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
