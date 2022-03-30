from .models import User
from werkzeug.security import generate_password_hash


def addUser(db, cwid, email, first_name, last_name, major, credits_taken, class_standing, password):
    # Create User object
    new_user = User(cwid=cwid, email=email, first_name=first_name, last_name=last_name, major=major,
                    credits_taken=credits_taken, class_standing=class_standing, password=generate_password_hash(
                        password, method='sha256'))
    # Add to Database
    db.session.add(new_user)
    db.session.commit()


def addUserByPrompts(db):
    # Collect data from user
    cwid = int(input('CWID:'))
    email = input('email:')
    first_name = input('first name:')
    last_name = input('last name:')
    major = input('major:')
    credits_taken = input('number of credits taken:')
    class_standing = input('class standing:')
    password = input('password:')

    response = input('\nWould you like to store this user?')
    if 'y' in response:
        addUser(db, cwid, email, first_name, last_name, major,
                credits_taken, class_standing, password)
    else:
        print('The user was not added.')
