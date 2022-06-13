from asyncio.windows_events import NULL
from .models import User, Semester
from werkzeug.security import generate_password_hash


def addUser(db, cwid, email, first_name, last_name, major, credits_taken, class_standing, password):
    # Create User object
    new_user = User(cwid=cwid, email=email, first_name=first_name, last_name=last_name, major=major,
                    credits_taken=credits_taken, class_standing=class_standing, password=generate_password_hash(
                        password, method='sha256'))
    # Add to Database
    db.session.add(new_user)
    db.session.commit()
    
def add_semester(db, id, semester_name, user_id, semester_number, courses):
    new_semester = Semester(id=id, semester_name=semester_name, user_id=user_id, semester_number=semester_number, courses=courses)

    db.session.add(new_semester)
    db.session.commit()
    print("successfully committed")

def delete_semesters_by_name(db, semester_name_input):
    semesters_to_delete = Semester.query.filter_by(semester_name = semester_name_input).all()
    for semester in semesters_to_delete:
        merged_object = db.session.merge(semester)
        db.session.delete(merged_object)
        db.session.commit()
def delete_semesters_by_null_id(db):
    semesters_to_delete = Semester.query.filter_by(user_id = NULL).all()
    for semester in semesters_to_delete:
        merged_object = db.session.merge(semester)
        db.session.delete(merged_object)
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

def delete_user(db, user):
    db.session.delete(user)