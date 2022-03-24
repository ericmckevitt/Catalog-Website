from matplotlib.contour import ContourSet
from parso import parse
import codd
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


def get_courses_by_departement(dep):
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
    SELECT prerequisites FROM {dep}_courses WHERE CONCAT(department, course_number) = '{course}';
    '''

    # Stores the return data as a string, still need to process logic
    prereqs = codd.read_query(QUERY, dburi)['prerequisites'].values[0]

    # Split along &
    prereqs = prereqs.split('&')

    # Remove parenthesis from each element now that it's split
    for i, prereq in enumerate(prereqs):
        prereqs[i] = prereq.replace('(', '')
        prereqs[i] = prereqs[i].replace(')', '')

        # Split along |
        if '|' in prereqs[i]:
            prereqs[i] = prereqs[i].split('|')

    return prereqs

# Take arrays and make them human-readable


def parse_prereqs(prereqs):
    for prereq in prereqs:
        if type(prereq) == str:
            print(prereq)
        if type(prereq) == list:
            print('Take one of:')
            for option in prereq:
                print('\t', option)


def main():
    # courses = get_courses_by_departement('CSCI')
    # print(courses)

    prereqs = get_course_prereqs('csci', 406)
    print(prereqs)
    print()
    parse_prereqs(prereqs)


if __name__ == "__main__":
    main()
