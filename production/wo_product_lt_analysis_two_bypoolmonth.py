import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Path of the file to read
data_filepath = "../dataset/wo_commit_comparison.csv"

# Read the file into a variable fifa_data
data = pd.read_csv(data_filepath, index_col="WO")

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
# ax_pool.patches: This attribute contains a list of all the rectangle objects (bars) in the bar plot.
# Each rectangle represents a bar in the bar chart.
for p in ax_pool.patches:
    # to add annotations to the plot
    ax_pool.annotate(
        # convert the height of the bar to a string
        str(p.get_height()),
        # to specify the (x,y) coordinates where the annotation should be placed
        # get_x() returns the x-coodinate of the lower left corner of the rectangle (bar)
        # p.get_width() return the width of the rectangle (bar)
        (p.get_x() + p.get_width() / 2., p.get_height()),
        # ha for horizontal alignment va for vertical alignment
        ha='center',
        va='center',
        # offset for the text. it moves the text 10 points vertically above the top of the bar
        xytext=(0, 10),
        # 'offset points' specifies that the xytext offset should be interpreted as being in points
        textcoords='offset points'
    )

plt.title('Count of NUMERATOR_ACTUAL by WO_END_YM for PROD_POOL_ID "9090"')
plt.xlabel('WO_END_YM')
plt.ylabel('Count')
plt.legend(title='NUMERATOR_ACTUAL')
plt.xticks(rotation=0)  # Rotates x-axis labels if necessary

plt.show()

