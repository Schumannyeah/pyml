import pandas as pd
import matplotlib.pyplot as plt

def plot_pool_chart(pool_id, pool_data):
    # Group by WO_END_YM and calculate counts of NUMERATOR_ACTUAL
    pool_grouped_data = pool_data.groupby('WO_END_YM')['NUMERATOR_ACTUAL'].value_counts().unstack(fill_value=0)

    # Calculate percentage
    total_counts = pool_grouped_data.sum(axis=1)
    percentage_data = pool_grouped_data.div(total_counts, axis=0) * 100

    # Plotting as clustered column chart
    fig, ax_pool = plt.subplots(figsize=(16, 6))

    # Plotting bar chart
    pool_grouped_data.plot(kind='bar', ax=ax_pool)

    # Adding data labels to each column
    for p in ax_pool.patches:
        ax_pool.annotate(str(p.get_height()),
                         (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='center',
                         xytext=(0, 10), textcoords='offset points')

    # Creating secondary y-axis for percentage line
    ax_percentage = ax_pool.twinx()

    # Plotting percentage line
    percentage_data.plot(kind='line', marker='o', ax=ax_percentage, linewidth=2)

    # Formatting the plot
    ax_pool.set_title(f'Count of WO COMMIT % by WO_END_YM for PROD_POOL_ID "{pool_id}"')
    ax_pool.set_xlabel('PRODUCTION ORDER ENDING YEAR MONTH')
    ax_pool.set_ylabel('Count')
    ax_percentage.set_ylabel('Percentage')
    ax_pool.legend(title='WO COMMIT SUCCESS & FAIL')
    ax_percentage.legend(title='Percentage', loc='upper left')
    ax_pool.set_xticks(range(len(pool_grouped_data)))
    ax_pool.set_xticklabels(pool_grouped_data.index, rotation=0)  # Rotates x-axis labels if necessary

    plt.show()
