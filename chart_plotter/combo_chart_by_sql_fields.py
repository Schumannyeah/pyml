import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_combo_chart(data, filter_by, group_by, group_value, title_name):
    # Group by WO_END_YM and calculate counts of NUMERATOR_ACTUAL
    if filter_by == None:
        data_grouped = data
    else:
        data_grouped = data.groupby(group_by)[group_value].value_counts().unstack(fill_value=0)

    # Calculate percentage
    total_counts = data_grouped.sum(axis=1)
    percentage_data = data_grouped.div(total_counts, axis=0) * 100

    # Plotting as clustered column chart
    fig, ax_pool = plt.subplots(figsize=(16, 6))

    # Plotting bar chart
    data_grouped.plot(kind='bar', ax=ax_pool)

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
    ax_pool.set_title(f'Count of "{title_name}" by "{group_by}" for "{filter_by}"')
    ax_pool.set_xlabel(group_by)
    ax_pool.set_ylabel('Count')
    ax_percentage.set_ylabel('Percentage')
    ax_pool.legend(title=title_name)
    ax_percentage.legend(title='Percentage', loc='upper left')
    ax_pool.set_xticks(range(len(data_grouped)))
    ax_pool.set_xticklabels(data_grouped.index, rotation=0)  # Rotates x-axis labels if necessary

    plt.show()



def plot_scatter_chart(data, x_field, y_field, chart_title):
    sns.scatterplot(x=data[x_field], y=data[y_field])
    plt.title(chart_title)
    plt.show()

def plot_distribution_chart(data, x_field, hue_field, chart_title):
    sns.kdeplot(data=data, x=x_field, hue=hue_field, shade=True)
    plt.title(chart_title)
    plt.show()