import pyodbc
import json


def get_database_config(filename):
    with open(filename, 'r') as file:
        config = json.load(file)
    return config


def get_data_from_db_by_sqlString(config, sqlString):
    # Extract configuration parameters
    server = config['server']
    database = config['database']
    username = config['username']
    password = config['password']

    # Establish a connection to the MSSQL database
    connection = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    
    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    # Execute a SQL query to select PRODUCT_ID and PRODUCT_NAME from the Product table
    cursor.execute(sqlString)

    # Fetch all rows from the result set
    products = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    return products


# Example usage:
# config_filename = 'config.json'
# config = get_database_config(config_filename)
# sqlString = "select top 100 ITEM_ID, ITEM_NAME from usv_Ax_InventTable"
# products = get_data_from_db_by_sqlString(config, sqlString)
# print(products)