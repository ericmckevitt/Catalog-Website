# Imports
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
from sqlalchemy import column, create_engine, inspect, text
import getpass

# Script Globals
username = 'emckevitt'
password = ''
server = 'codd.mines.edu'
database = 'csci403'
port = '5433'


# Set to True to see Queries before they are sent to server
debugger = False

# Can refactor to pass in name and use f-string


def getLoginCredentials():
    return [username, 'Mines6515']  # TODO Change this to function call


# Returns a list of server connection parameters so other files can connect
def getServerIdentifiers():
    return [server, database, port]


def collect_password():
    try:
        # password = getpass.getpass()
        return getpass.getpass()
    except Exception as e:
        print('Error:', e)


def connect(password):
    # Connect to DBMS
    dburi = f'postgresql://{username}:{password}@{server}:{port}/{database}'
    inspector = inspect(create_engine(dburi))
    return dburi, inspector


def get_tables(inspector):
    # Get list from inspector and print
    return list(inspector.get_table_names())


def print_table_data(inspector):
    # Collect table data
    tables = get_tables(inspector)

    # Loop through the tables list and print all of the table names and columns
    for table in tables:
        print("Table name: ", table)  # Print the table name (table)
        # Print the column name and type, think of the column as a dataframe, column['xxx']
        for column in inspector.get_columns(table):
            print("   %s: %s" % (column['name'], column['type']))
            # print('    ', column) # Print all metadata
        print()


def read_csv_data(filename):
    # Read .txt file into DataFrame
    # ./Schema/CSCIMajor.csv
    types = list(pd.read_table(f'{filename}', sep=',').columns)
    for i, type in enumerate(types):
        types[i] = type.replace('|', ',')
    return_types = list(pd.DataFrame(types).T.iloc[0])

    for i, type in enumerate(return_types):
        if 'TEXT' in type:
            return_types[i] = 'TEXT'
        if 'NUMERIC' in type and '.' in type:
            # Find out how many characters after parenthesis
            chars_to_remove = (
                len(return_types[i])) - return_types[i].index(')')
            chars_to_remove -= 1
            return_types[i] = return_types[i][:-chars_to_remove]
        if 'INTEGER' in type:
            return_types[i] = 'INTEGER'

    # TODO Copy if statement for each type in SQL

    data = pd.read_table(f'{filename}', sep=',', skiprows=1)
    return return_types, data


def store_csv_in_dbms(filename, table_name, dburi):
    # Convert csv to dataframe
    types, data = read_csv_data(filename)

    # Collect column titles
    column_titles = list(data.columns)
    # print(column_titles)

    # Create table
    create_query = f"""CREATE TABLE {table_name} (

    """
    # Iterate over types and column_titles to build table
    for i in range(len(types)):
        # Collect type and title for the new column
        type = types[i]
        title = column_titles[i]
        # This part of the query is always to be added
        create_query += f"{title} {type}"
        # If the last column, don't add a comma
        if i != len(types) - 1:
            create_query += ","
    # Close the query
    create_query += ");"

    # For debugging, output finished query
    if debugger:
        print('Create Query:\n', create_query)

    # Sends query to server
    read_query(create_query, dburi)


# filename is csv input, table_name is DBMS table output, dburi is DBMS connection


def insert_csv_into_table(filename, table_name, dburi):
    # Convert csv to dataframe
    types, data = read_csv_data(filename)

    # Store colunn data
    column_titles = list(data.columns)
    if debugger:
        print(column_titles)

    # Store table dimensions
    num_rows = data.shape[0]
    num_cols = data.shape[1]

    insert_query = f"""INSERT INTO {table_name} VALUES 

    """

    # Replace all nan characters with NULL
    data = data.replace(np.nan, 'NULL')

    # Look over DataFrame and add to query
    for i, row in data.iterrows():

        insert_query += "("
        for j, col in enumerate(column_titles):
            # print(row[col], end=', ')

            # Only add comma if it's the last value
            if j == num_cols - 1:
                # Only add single quotes if it's a TEXT type
                current_type = types[j]
                if current_type == 'INTEGER' or 'NUMERIC' in current_type:
                    # Insert into query
                    insert_query += f"{row[col]}"
                else:
                    # Insert into query
                    insert_query += f"'{row[col]}'"
            else:
                # Last item to insert in row
                current_type = types[j]
                if current_type == 'INTEGER' or 'NUMERIC' in current_type:
                    # Insert into query
                    insert_query += f"{row[col]},"
                else:
                    # Insert into query
                    insert_query += f"'{row[col]}',"
        # If it's the last row, don't add comma, use semicolon
        if i == num_rows - 1:
            insert_query += ");"
        else:
            insert_query += "),"

    if debugger:
        print("Insert Query:\n", insert_query)

    read_query(insert_query, dburi)


def read_query(query, dburi):
    try:
        # You can catch this return if you want
        return pd.read_sql_query(query, dburi)
    except:
        pass


def drop(table_name, dburi):
    read_query(f"DROP TABLE IF EXISTS {table_name};", dburi)

# Creates table and inserts from csv in one function call


def create_and_populate(filename, table_name, dburi):
    # Drop table if exists
    drop(table_name, dburi)

    # Create table
    store_csv_in_dbms(filename, table_name, dburi)
    # Insert data from csv (filename) into table
    insert_csv_into_table(filename, table_name, dburi)

    # Check dimensions of table to see if insertion worked
    try:
        table = read_query(f"SELECT * FROM {table_name};", dburi)

        if table.shape[0] == 0:
            return f"\nWARNING: '{table_name}' was created with zero rows.\n"
        elif table.shape[1] == 1:
            return f"\nWARNING: '{table_name}' was created with one row.\n"
        else:
            return f"\nSuccess! '{table_name}' was created with {table.shape[0]} rows and {table.shape[1]} columns.\n"
    except Exception as e:
        print(e)


def update_table(table_name, file):
    # Drop, create and insert into from a csv
    drop(table_name, dburi)
    create_and_populate(file, table_name, dburi)

# Copy table data from one table to another


def copy_table(original, new_table, dburi=connect('Mines6515')):
    original_table = read_query("SELECT * FROM {original}", dburi)
    # TODO Implement rest of algorithm

# Copies table into another and drops original


def rename_table(original, new_table, dburi=connect('Mines6515')):
    copy_table(original, new_table, dburi)
    drop(original, dburi)
    # TODO: Only use this if we actually implement copy_table()

# Takes in DEP+CN and returns all information on this course as a dataframe


def get_course_info(dep, cn, dburi):
    # Query for course
    query = f"SELECT * FROM {dep.lower()}_courses WHERE department = '{dep}' AND course_number = {int(cn)};"
    # query = "SELECT * FROM csci_courses;"
    print(query)
    # Return result of query
    return read_query(query, dburi)


# Save connection and inspector globally so that params can have default
dburi, inspector = connect('Mines6515')


def main():
    # Collect credentials and log into DB
    # password = collect_password()  # TODO Uncomment
    dburi, inspector = connect('Mines6515')  # TODO Use password variable

    # drop('cam_major', dburi)

    # status = create_and_populate('./Schema/Majors/CAMMajor.csv', 'cam_major', dburi)
    # print(status)

    # store_csv_in_dbms('./Schema/Majors/CAMMajor.csv', 'cam_major', dburi)

    # Print list of tables
    # print('\nTables:', get_tables(inspector))
    # print()

    course_info = get_course_info('CSCI', '406', dburi)
    print(course_info)


if __name__ == "__main__":
    main()
