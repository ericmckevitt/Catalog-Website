from tabnanny import check
from matplotlib.pyplot import table

from numpy import require
import codd
import load_all_majors as maj
import load_all_minors as min


# Collect credentials for user and server
username = codd.username
password = codd.getLoginCredentials()[1]
server = codd.server
database = codd.database
port = codd.port

# Connect to codd
dburi, inspector = codd.connect(password)


def get_classes_taken_by_cwid(cwid):
    # This query gets an unprocessed list of classes a student has taken.
    QUERY = f"""
    SELECT DISTINCT courses_taken FROM students WHERE cwid = {cwid};
    """
    # read_query returns pandas dataframe of shape (1,1), and we want the first value (no column titles)
    raw_data = codd.read_query(QUERY, dburi).values[0][0]

    # Process the data
    classes_taken = raw_data.split('|')

    return classes_taken


def get_major_by_cwid(cwid):
    QUERY = f"""
    SELECT major FROM students WHERE cwid = {cwid};
    """
    return codd.read_query(QUERY, dburi).values[0][0]


def check_degree_progress(cwid):
    major = get_major_by_cwid(cwid)
    courses_taken = get_classes_taken_by_cwid(cwid)
    # Look up this major's table name
    major_tablename = maj.major_map[major]

    # Get major's req. classes
    QUERY = f"""
    SELECT CONCAT(department, CAST(course_number AS TEXT) ) FROM {major_tablename};
    """
    major_courses = list(codd.read_query(QUERY, dburi)['concat'].values)

    # Filter out electives, pagn, etc. to get just the classes that are always needed for this major
    required_courses = []
    elective_courses = []
    for course in major_courses:
        if course == 'NULL' or course == 'FREE' or course == 'ELECTIVE' or course == 'PAGN':
            elective_courses.append(course)
        else:
            required_courses.append(course)

    # Check which of these the student has taken
    courses_left = []
    for req_course in required_courses:
        course_complete = False
        # Check if course has been taken by student
        for taken_course in courses_taken:
            if taken_course == req_course:
                course_complete = True

        if not course_complete:
            courses_left.append(req_course)

    # Tell the student which classes they still need to take.
    return courses_left

# Compute number of classes needed to obtain a minor


def distance_to_minor(cwid, minor):
    # Collect list of courses taken
    courses_taken = get_classes_taken_by_cwid(cwid)
    # Get element from minor_map
    minor_tablename = min.minor_map[minor]
    # Check if element is a list or a string
    if type(minor_tablename) == list:
        # print(minor_tablename, end='\n\n')
        # Compute distance to each minor and find the table with minimum distance
        # Junk value that will surely be bigger than any value we encounter. Good enough I guess.
        min_distance = 1000
        min_courses = []
        ideal_table = ''
        for table in minor_tablename:

            # Select list of courses from codd
            # print(table)

            QUERY = f"""
            SELECT CONCAT(department, CAST(course_number AS TEXT) ) FROM {table};
            """
            # All the courses required for this minor, including malleable classes.
            minor_courses = list(codd.read_query(
                QUERY, dburi)['concat'].values)
            # print(minor_courses, end='\n\n')

            # Classes that are 100% required for this minor
            concrete_classes = [
                i for i in minor_courses if 'ELECT' not in i
                and 'NULL' not in i and 'FREE' not in i and 'PAGN' not in i]
            # print(concrete_classes)

            # Classes like electives, pagn, etc., where student can choose from a set of options
            malleable_classes = [
                i for i in minor_courses if 'ELECT' in i
                or 'NULL' in i or 'FREE' in i or 'PAGN' in i
            ]
            # print(malleable_classes)

            # TODO: Handle malleable classes

            # Compute distance from courses_taken to concrete_classes
            distance = 0
            courses_to_take = []
            for course in concrete_classes:
                # Check if this course has been taken yet
                if course not in courses_taken:
                    distance += 1
                    courses_to_take.append(course)
            if distance < min_distance:
                min_distance = distance
                min_courses = courses_to_take
                ideal_table = table
            # Return the list of least distance
            # print(f'{table} courses to take:', courses_to_take)

        # print(f'{ideal_table} distance =', len(min_courses))
        print(
            f'The most ideal path requires you take {len(min_courses)} course(s).')
        print('You need to take ', end='')
        for i, course in enumerate(min_courses):
            if i < len(min_courses) - 1:
                print(course, end=', ')
            else:
                print(course, end='.\n')

    else:
        # Compute distance to this minor
        # print(minor_tablename)

        QUERY = f"""
        SELECT CONCAT(department, CAST(course_number AS TEXT) ) FROM {minor_tablename};
        """
        minor_courses = list(codd.read_query(
            QUERY, dburi)['concat'].values)

        concrete_classes = [
            i for i in minor_courses if 'ELECT' not in i
            and 'NULL' not in i and 'FREE' not in i and 'PAGN' not in i]

        # TODO Handle malleable classes - check all classes that can fit in this spot and see if in courses_taken
        malleable_classes = [
            i for i in minor_courses if 'ELECT' in i
            or 'NULL' in i or 'FREE' in i or 'PAGN' in i
        ]

        courses_to_take = []
        distance = 0
        for course in concrete_classes:
            # Check if this course has been taken yet
            if course not in courses_taken:
                distance += 1
                courses_to_take.append(course)

        print(
            f'This minor requires you take {distance} more course(s).')
        print(f'You need to take ', end='')
        for i, course in enumerate(courses_to_take):
            if i < len(courses_to_take) - 1:
                print(course, end=', ')
            else:
                print(course, end='.\n')


def distance_to_major(cwid, major_name):
    # Collect list of courses taken
    courses_taken = get_classes_taken_by_cwid(cwid)
    # Get element from minor_map
    major_tablename = maj.major_map[major_name]
    QUERY = f"""
        SELECT CONCAT(department, CAST(course_number AS TEXT) ) FROM {major_tablename};
        """
    major_courses = list(codd.read_query(
        QUERY, dburi)['concat'].values)

    concrete_classes = [
        i for i in major_courses if 'ELECT' not in i
        and 'NULL' not in i and 'FREE' not in i and 'PAGN' not in i]

    # TODO Handle malleable classes - check all classes that can fit in this spot and see if in courses_taken
    malleable_classes = [
        i for i in major_courses if 'ELECT' in i
        or 'NULL' in i or 'FREE' in i or 'PAGN' in i
    ]

    courses_to_take = []
    distance = 0
    for course in concrete_classes:
        # Check if this course has been taken yet
        if course not in courses_taken:
            distance += 1
            courses_to_take.append(course)

    print(
        f'This major requires you take {distance} more course(s).')
    print(f'You need to take ', end='')
    for i, course in enumerate(courses_to_take):
        if i < len(courses_to_take) - 1:
            print(course, end=', ')
        else:
            print(course, end='.\n')


def main():
    classes = get_classes_taken_by_cwid(12345678)
    print(classes)

    # print(get_major_by_cwid(12345678))

    distance_to_minor(12345678, 'Computer Science')
    # distance_to_major(12345678, 'Statistics')
    print()

    # print(check_degree_progress(12345678))


if __name__ == "__main__":
    main()
