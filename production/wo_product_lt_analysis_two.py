import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Path of the file to read
data_filepath = "../dataset/wo_commit_comparison.csv"

# Read the file into a variable fifa_data
data = pd.read_csv(data_filepath, index_col="WO")

# Filter the DataFrame where WO_END_YM is "2024-06"
filtered_data = data[data['WO_END_YM'] == '2024-06']

# Group by PROD_POOL_ID and calculate counts of NUMERATOR_ACTUAL
grouped_data = filtered_data.groupby('PROD_POOL_ID')['NUMERATOR_ACTUAL'].value_counts().unstack(fill_value=0)

# # option 1
# # Plotting
# grouped_data.plot(kind='bar', stacked=True, figsize=(10, 6))

# option 2
# Plotting as clustered column chart
ax = grouped_data.plot(kind='bar', figsize=(10, 6))
# Adding data labels to each column
for p in ax.patches:
    ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points')

plt.title('Count of NUMERATOR_ACTUAL by PROD_POOL_ID for WO_END_YM "2024-06"')
plt.xlabel('PROD_POOL_ID')
plt.ylabel('Count')
plt.legend(title='NUMERATOR_ACTUAL')
plt.xticks(rotation=0)  # Rotates x-axis labels if necessary

plt.show()





# Filter the DataFrame where WO_END_YM is "2024-06"
pool_data = data[data['PROD_POOL_ID'] == 9090]
print(pool_data.head())

# Group by PROD_POOL_ID and calculate counts of NUMERATOR_ACTUAL
pool_grouped_data = pool_data.groupby('WO_END_YM')['NUMERATOR_ACTUAL'].value_counts().unstack(fill_value=0)

# # option 1
# # Plotting
# grouped_data.plot(kind='bar', stacked=True, figsize=(10, 6))

# option 2
# Plotting as clustered column chart
ax_pool = pool_grouped_data.plot(kind='bar', figsize=(16, 6))
# Adding data labels to each column
for p in ax_pool.patches:
    ax_pool.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points')

plt.title('Count of NUMERATOR_ACTUAL by WO_END_YM for PROD_POOL_ID "9090"')
plt.xlabel('WO_END_YM')
plt.ylabel('Count')
plt.legend(title='NUMERATOR_ACTUAL')
plt.xticks(rotation=0)  # Rotates x-axis labels if necessary

plt.show()

