from importlib.resources import path
import codd
import time
import os


# Collect credentials for user and server
username = codd.username
password = codd.getLoginCredentials()[1]
server = codd.server
database = codd.database
port = codd.port

# Connect to codd
dburi, insepctor = codd.connect(password)

# Define table locations for convenience
csci_courses = './Schema/Courses/CSCICourses.csv'
eeng_courses = './Schema/Courses/EENGCourses.csv'
all_courses = './Schema/Courses/all_courses.csv'

# csci_courses = '../Schema/Courses/CSCICourses.csv'


# majors = [ [location, name], ... ]
courses = [[all_courses, 'all_courses']]


def drop_all_courses():
    for course in courses:
        codd.drop(course[1], dburi)

    print('Tables:', codd.get_tables(insepctor))

# To get prereq's: SELECT prereq's and then parse the TEXT using a function
# answer = codd.read_query('SELECT prerequisites FROM csci_courses', dburi).parsePre()
# (CSCI101|CSCI102|CSCI261) & MATH201 & MATH332 # Initial value from .csv
# [(CSCI101|CSCI102|CSCI261), MATH201, MATH332] # Split on delimiter='&' (Splits into list of size = number of classes that need to be taken)
# [[CSCI101, CSCI102, CSCI261], MATH201, MATH332] # Split on delimiter='|' (Splits all OR groups into 2D list items)


def load_all_courses():
    # Print table list
    print('Original Table List:')
    print(codd.get_tables(insepctor),
          end='\n-----------------------------------\n')
    # Create tables and insert for each major
    for course in courses:
        # Unpack file location and name from major
        location, name = course
        try:
            # Create table and insert from location to dburi
            status = codd.create_and_populate(location, name, dburi)
            print(status.strip())
        except:
            print(f'Error: file named {name} could not be found.')

    # Print table list
    print('-----------------------------------\nTable List After Insertions:')
    print(codd.get_tables(insepctor))


def load_course(location, table_name):
    try:
        status = codd.create_and_populate(location, table_name, dburi)
        print(status.strip())
    except:
        print(f'Error: file named {table_name} could not be found.')


def main():
    # drop_all_courses()
    load_all_courses()


if __name__ == "__main__":
    main()
