import sys
# changed from: from python import codd
from . import codd


# Collect credentials for user and server
username = codd.username
password = codd.getLoginCredentials()[1]
server = codd.server
database = codd.database
port = codd.port

# Connect to codd
dburi, inspector = codd.connect(password)

# Define table locations for convenience
csci_major = '../Schema/Majors/CSCIMajor.csv'
am_major = '../Schema/Majors/AMMajor.csv'
stat_major = '../Schema/Majors/STATMajor.csv'
ceen_major = '../Schema/Majors/CEENMajor.csv'
phgn_major = '../Schema/Majors/PHGNMajor.csv'

# majors = [ [location, name], ... ]
majors = [[csci_major, 'csci_major'], [
    am_major, 'am_major'], [stat_major, 'stat_major'],
    [ceen_major, 'ceen_major'], [phgn_major, 'phgn_major']]

# Maps major tables to their respective table names
major_map = {
    'Computer Science': 'csci_major',
    'Applied Mathematics': 'am_major',
    'Statistics': 'stat_major',
    'Civil Engineering': 'ceen_major',
    'Physics': 'phgn_major'
}


def drop_all_majors():
    for major in majors:
        codd.drop(major[1], dburi)

    print('Tables:', codd.get_tables(inspector))


def load_all_majors():
    # Print table list
    print('Original Table List:')
    print(codd.get_tables(inspector),
          end='\n-----------------------------------\n')
    # Create tables and insert for each major
    for major in majors:
        # Unpack file location and name from major
        location, name = major
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
    drop_all_majors()
    load_all_majors()


if __name__ == "__main__":
    main()
