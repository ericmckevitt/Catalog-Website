from matplotlib.contour import ContourSet
from parso import parse
from . import codd
import numpy as np

# Collect credentials for user and server
username = codd.username
password = codd.getLoginCredentials()[1]
server = codd.server
database = codd.database
port = codd.port

# Connect to codd
dburi, inspector = codd.connect(password)

# Pass in a department (Ex: CSCI) and get a list of classes


def get_courses_by_department(dep):
    QUERY = f'''
    SELECT CONCAT(department, course_number) AS "courses" FROM {dep}_courses;
    '''
    course_list = list(codd.read_query(QUERY, dburi)['courses'].values)
    return course_list

# Pass in a department and course number to get list of it's prereqs


def get_course_prereqs(dep, cn):
    # Transforms inputs from csci, 403 to CSCI403
    course = f'{dep.upper()}{cn}'
    QUERY = f'''
    SELECT prerequisites FROM all_courses WHERE CONCAT(department, course_number) = '{course}';
    '''

    # Stores the return data as a string, still need to process logic
    prereqs = codd.read_query(QUERY, dburi)['prerequisites'].values[0]

    # Split along &
    if prereqs is None:
        return None

    prereqs = prereqs.split('&')

    # Remove parenthesis from each element now that it's split
    for i, prereq in enumerate(prereqs):
        prereqs[i] = prereq.replace('(', '')
        prereqs[i] = prereqs[i].replace(')', '')

        # Split along |
        if '|' in prereqs[i]:
            prereqs[i] = prereqs[i].split('|')
    if prereqs == ['NULL']:
        prereqs = None

    return prereqs


def get_course_coreqs(dep, cn):
    # Transforms inputs from csci, 403 to CSCI403
    course = f'{dep.upper()}{cn}'
    QUERY = f'''
    SELECT corequisites FROM all_courses WHERE CONCAT(department, course_number) = '{course}';
    '''

    # Stores the return data as a string, still need to process logic
    coreqs = codd.read_query(QUERY, dburi)['corequisites'].values[0]

    # Split along &
    if coreqs is None:
        return None

    coreqs = coreqs.split('&')

    # Remove parenthesis from each element now that it's split
    for i, coreq in enumerate(coreqs):
        coreqs[i] = coreq.replace('(', '')
        coreqs[i] = coreqs[i].replace(')', '')

        # Split along |
        if '|' in coreqs[i]:
            coreqs[i] = coreqs[i].split('|')
    if coreqs == ['NULL']:
        coreqs = None

    return coreqs

# Take arrays and make them human-readable


def parse_prereqs(prereqs):
    print(prereqs)
    if prereqs is None or prereqs == []:
        print('No prereqs')
        return
    for prereq in prereqs:
        if type(prereq) == str:
            print(prereq)
        if type(prereq) == list:
            print('Take one of:')
            for option in prereq:
                print('\t', option)


def get_course_info(dep, cn):
    # Gets name, semester hours, prereqs, coreqs
    prereqs = get_course_prereqs(dep, cn)
    coreqs = get_course_coreqs(dep, cn)

    # Get course name
    QUERY = f'''
    SELECT course_title FROM all_courses WHERE CONCAT(department, course_number) = '{dep.upper()}{cn}';
    '''
    name = codd.read_query(QUERY, dburi)['course_title'].values[0]

    # Get course hours
    QUERY = f'''
    SELECT semester_hours FROM all_courses WHERE CONCAT(department, course_number) = '{dep.upper()}{cn}';
    '''
    hours = codd.read_query(QUERY, dburi)['semester_hours'].values[0]

    return name, dep, str(cn), hours, prereqs, coreqs


def main():
    # courses = get_courses_by_department('CSCI')
    # print(courses)

    prereqs = get_course_prereqs('csm', 101)
    print(prereqs)
    print()
    parse_prereqs(prereqs)


if __name__ == "__main__":
    main()
