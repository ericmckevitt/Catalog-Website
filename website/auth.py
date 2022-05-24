from tabnanny import check
from unicodedata import category
# from winreg import REG_QWORD
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Course, Semester
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

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
