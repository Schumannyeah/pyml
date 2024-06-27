import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from func.func_db import get_database_config, get_data_from_db_by_sqlString

# to read the data table from sql database
# Call the function to query the database
config_filename = '../config.json'
config = get_database_config(config_filename)
sqlString = """
            SELECT TOP 200 ITEM_GROUP_ID, LT_SITE_INV, ON_HAND_COST_PRICE
            FROM usv_Ofbiz_Mes_Products
            WHERE ITEM_GROUP_ID IS NOT NULL AND LT_SITE_INV > 0
            """
products = get_data_from_db_by_sqlString(config, sqlString)
# print("Data returned by the SQL query:", products)

# Debug: Print the type and structure of the data returned
# print("Type of data returned:", type(products))
# if isinstance(products, list) and len(products) > 0:
#     print("Type of first element:", type(products[0]))
#     print("First element:", products[0])

# Convert pyodbc.Row objects to a list of tuples
products_tuples = [tuple(row) for row in products]

# Convert the list of tuples to a pandas DataFrame and specify column names
products_df = pd.DataFrame(products_tuples, columns=['ITEM_GROUP_ID', 'LT_SITE_INV', 'ON_HAND_COST_PRICE'])

# Drop rows with null values in 'ON_HAND_COST_PRICE'
products_df = products_df.dropna(subset=['ON_HAND_COST_PRICE'])

# Convert columns to float
products_df['LT_SITE_INV'] = products_df['LT_SITE_INV'].astype(float)
products_df['ON_HAND_COST_PRICE'] = products_df['ON_HAND_COST_PRICE'].astype(float)

print("Columns in the DataFrame:", products_df.columns)
print(products_df.head())

# Plot the data
plt.figure(figsize=(16, 8))
# sns.scatterplot(x=products_df['ITEM_GROUP_ID'], y=products_df['LT_SITE_INV'])
# sns.regplot(x=products_df['LT_SITE_INV'], y=products_df['ON_HAND_COST_PRICE'])

sns.scatterplot(x=products_df['LT_SITE_INV'], y=products_df['ON_HAND_COST_PRICE'], hue=products_df['ITEM_GROUP_ID'])
# sns.lmplot(x="bmi", y="charges", hue="smoker", data=insurance_data)

# sns.swarmplot(x=products_df['ITEM_GROUP_ID'], y=products_df['LT_SITE_INV'])
plt.show()
