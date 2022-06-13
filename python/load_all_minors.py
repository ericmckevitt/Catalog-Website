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
csci_minor1 = '../Schema/Minors/CSCIMinor1.csv'
csci_minor2 = '../Schema/Minors/CSCIMinor2.csv'
compeng_minor = '../Schema/Minors/COMPENGMinor.csv'
dsci_minor1 = '../Schema/Minors/DSCIMinor1.csv'
dsci_minor2 = '../Schema/Minors/DSCIMinor2.csv'
dsci_minor_electives = '../Schema/Minors/DSCIMinorElectives.csv'
robotics_minor = '../Schema/Minors/ROBOTICSMinor.csv'

# majors = [ [location, name], ... ]
minors = [[csci_minor1, 'csci_minor1'], [
    csci_minor2, 'csci_minor2'], [compeng_minor, 'compeng_minor'], [dsci_minor1, 'dsci_minor1'],
    [dsci_minor2, 'dsci_minor2'], [dsci_minor_electives, 'dsci_minor_electives'], [robotics_minor, 'robotics_minor']]

# Maps major tables to their respective table names
minor_map = {
    'Computer Science': ['csci_minor1', 'csci_minor2'],
    'Computer Engineering': 'compeng_minor',
    'Data Science': ['dsci_minor1', 'dsci_minor2'],
    'Robotics': 'robotics_minor'
}


def drop_all_minors():
    for minor in minors:
        try:
            codd.drop(minor[1], dburi)
        except:
            print(f'Failed to drop {minors[1]}')

    print('Tables:', codd.get_tables(inspector))


def load_all_minors():
    # Print table list
    print('Original Table List:')
    print(codd.get_tables(inspector),
          end='\n-----------------------------------\n')
    # Create tables and insert for each major
    for minor in minors:
        # Unpack file location and name from major
        location, name = minor
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
    # drop_all_minors()
    load_all_minors()


if __name__ == "__main__":
    main()
