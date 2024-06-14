import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime

server = "MESCHZHE01"
database = "ofbiz"
username = "pbilogin"
password = "kmcj123456"

# Specify the ODBC driver as "SQL Server"
driver = "SQL Server"

# Construct the connection string
connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Create an SQLAlchemy engine with the specified driver
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={connection_string}")

# SQL query to select data from the view
sql_query = text("SELECT * FROM usv_Ofbiz_SCM_Safety_Stock")

# Execute the query and load data into a DataFrame
with engine.connect() as conn:
    result = conn.execute(sql_query)
    df = pd.DataFrame(result.fetchall(), columns=result.keys())

# Generate the current date in the format YYYYMMDD
current_date = datetime.now().strftime("%Y%m%d")

# Construct the file name with the current date
excel_file_path = f"//filechzhe01/03822/ProcurementTeam/99-SafetyStock/{current_date}.xlsx"

# Export DataFrame to Excel
df.to_excel(excel_file_path, index=False)
