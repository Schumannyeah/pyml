import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from func.func_db import get_database_config, get_data_from_db_by_sqlString

# to read the data table from sql database
# Call the function to query the database
config_filename = '../config.json'
config = get_database_config(config_filename)
sqlString = """
            usp_Ofbiz_PP_CompareEndWoLtWithProdLtByPastDays 60
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
products_df = pd.DataFrame(products_tuples, columns=['WO', 'WO_NAME', 'WO_STATUS','CREATED_DATE', 'WO_POOL_ID',
                                                     'PRODUCT_ID', 'WO_MES_START', 'WO_MES_END','START_MIN_CREATE',
                                                     'WO_LT', 'PRODUCT_LT', 'ITEM_GROUP_ID', 'LT_DEV'])

# Drop rows with null values in 'ON_HAND_COST_PRICE'
# products_df = products_df.dropna(subset=['ON_HAND_COST_PRICE'])

# Convert columns to float
products_df['START_MIN_CREATE'] = products_df['START_MIN_CREATE'].astype(float)
products_df['WO_LT'] = products_df['WO_LT'].astype(float)
products_df['PRODUCT_LT'] = products_df['PRODUCT_LT'].astype(float)
products_df['LT_DEV'] = products_df['LT_DEV'].astype(float)

print("Columns in the DataFrame:", products_df.columns)
print(products_df.head())

# Plot the data
plt.figure(figsize=(16, 8))
# sns.scatterplot(x=products_df['LT_DEV'], y=products_df['PRODUCT_LT'])
# sns.regplot(x=products_df['LT_DEV'], y=products_df['PRODUCT_LT'])

# sns.scatterplot(x=products_df['LT_DEV'], y=products_df['PRODUCT_LT'], hue=products_df['WO_POOL_ID'])
# sns.lmplot(x="LT_DEV", y="PRODUCT_LT", hue="WO_POOL_ID", data=products_df)

sns.swarmplot(x=products_df['WO_POOL_ID'], y=products_df['LT_DEV'])
plt.show()
