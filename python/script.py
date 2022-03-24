from numpy import insert
import codd

# This file shows how to write scripts using the
# library defined in main.py.

# Collect credentials for user and server
username = codd.username
password = codd.getLoginCredentials()[1]
server = codd.server
database = codd.database
port = codd.port

# Connect to codd
dburi, inspector = codd.connect(password)

# Define table locations for convenience
cscimajor = './Schema/Majors/CSCIMajor.csv'


def shared_major_classes(major1, major2):
    Query = f"""
    SELECT DISTINCT {major1}.course_name FROM {major1}
    JOIN {major2} ON {major1}.course_name = {major2}.course_name;
    """
    print(f'Question: What classes do both {major1} and {major2} take?\n')

    answer = codd.read_query(Query, dburi)
    print(answer)


def script2():
    Query = """
    SELECT DISTINCT one.course_name FROM csci_minor1 one 
    JOIN csci_minor2 two ON one.course_name = two.course_name;
    """
    print('Question: What classes must be taken for a CS minor regardless of what minor track they choose?')
    answer = codd.read_query(Query, dburi)
    print(answer)


def script3(current_major, desired_minor):
    # TODO Come up with the SQL command for this
    current_major = 'csci_major'
    desired_minor = 'robotics_minor'
    print(
        f'Question: How many classes on top of a {current_major} major do you have to take to get a minor in {desired_minor}?')


def main():
    # Call your script something more descriptive than 'script'
    # script()
    # print()
    # script2()
    dburi, inspector = codd.connect(password)

    # QUERY = """
    # SELECT * FROM compeng_minor;
    # """
    # table = codd.read_query(QUERY, dburi)
    # print(table)

    print(codd.get_tables(inspector))
    print()

    shared_major_classes('ceen_major', 'phgn_major')

    # You can also script directly in main(), but it's good practice
    # to section off a script in a function if you can.


if __name__ == "__main__":
    main()
