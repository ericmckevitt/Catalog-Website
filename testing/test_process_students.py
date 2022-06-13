import pytest
import sys
from python import process_students

# py -m pytest testing/test_process_students.py

def test_get_classes_taken_by_cwid():

    # making test data
    
    # course data
        # Create Course row and add to database
    testUser1 = User(
                id = 00000000)
    new_course = Course(
                department = 'TEST', course_number=000, course_name="test course name", credit_hours = 0.0, is_taken="False", user_id = testUser1.id)
    db.session.add(new_course)
    db.session.commit()

    class_list = process_students.get_classes_taken_by_cwid(12345678)
    print(class_list)
    assert(False)