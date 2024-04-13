import pymssql

# Connect to MSSQL server
connection = pymssql.connect(
    server='MESCHZHE01',
    user='pbilogin',
    password='kmcj123456',
    database='ofbiz'
)

# Create a cursor object
cursor = connection.cursor()

# Insert sample data into the projects table
cursor.execute("""select top 100 ITEM_ID, ITEM_NAME from usv_Ax_InventTable
""")

# Commit changes to the database
connection.commit()

# Close the connection
connection.close()
