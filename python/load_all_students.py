import codd


# Collect credentials for user and server
username = codd.username
password = codd.getLoginCredentials()[1]
server = codd.server
database = codd.database
port = codd.port

# Connect to codd
dburi, inspector = codd.connect(password)

# Define table locations for convenience
students_table = '../Schema/Students/Students.csv'


# majors = [ [location, name], ... ]
students = [[students_table, 'students']]


def drop_all_students():
    for student in students:
        codd.drop(student[1], dburi)

    print('Tables:', codd.get_tables(inspector))


def load_all_students():
    # Print table list
    print('Original Table List:')
    print(codd.get_tables(inspector),
          end='\n-----------------------------------\n')
    # Create tables and insert for each major
    for student in students:
        # Unpack file location and name from major
        location, name = student
        print(f'location = {location} :: name = {name}')
        try:
            # Create table and insert from location to dburi
            status = codd.create_and_populate(location, name, dburi)
            print(status.strip())
        except:
            print(f'Error: file named {name} could not be found.')

    # Print table list
    print('-----------------------------------\nTable List After Insertions:')
    print(codd.get_tables(inspector))


def main():
    # drop_all_courses()
    load_all_students()


if __name__ == "__main__":
    main()
