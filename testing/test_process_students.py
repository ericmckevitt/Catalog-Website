import pytest
import sys
from python import process_students

# py -m pytest testing/test_process_students.py

def test_get_classes_taken_by_cwid():
    class_list = process_students.get_classes_taken_by_cwid(00000000)
    print(class_list)
    assert(False)