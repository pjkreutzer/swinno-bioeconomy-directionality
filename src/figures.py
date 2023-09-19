import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as po
import plotly.express as px

def plot_bv_trends(df, title):
    chart = sns.lineplot(
        data=df,
        x="year",
        y="count",
        hue="bioeconomy_vision",
        palette="colorblind",
        linewidth=2.5,
    )
    chart.set_title(title, fontdict={"fontsize": 16, "fontweight": "bold"})
    chart.set_xlabel("Year", fontdict={"fontsize": 12, "fontweight": "bold"})
    chart.set_ylabel("Count", fontdict={"fontsize": 12, "fontweight": "bold"})
    chart.tick_params(labelsize=10)
    plt.legend(title="Vision", fontsize=10, title_fontsize=12)
    plt.tight_layout()

    # Customize x-axis tick labels
    years = df["year"].unique()
    chart.set_xticks(years[::5])
    chart.set_xticklabels(years[::5], rotation=45, ha="right")

    return chart


def plot_heatmap(data, title):
    fig, ax = plt.subplots(1, 1)
    ax = sns.heatmap(
        data, annot=True, cmap="Blues", fmt="g", cbar=False, annot_kws={"fontsize": 10}
    )
    ax.set(title=title, ylabel=None, xlabel=None)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")

    plt.show()


def prepare_heatmap_data(df, index_col, cols_col, values_col, ascending=False):
    """
    Prepare data for a heatmap visualization by pivoting and sorting a dataframe.

    Args:
    - df: input dataframe
    - index_col: column name for the index of the pivoted dataframe
    - cols_col: column name for the columns of the pivoted dataframe
    - values_col: column name for the values of the pivoted dataframe
    - ascending: boolean to specify whether to sort in ascending or descending order (default: False)

    Returns:
    - pivoted and sorted dataframe
    """
    # Pivot the data to create a matrix
    matrix = df.pivot(index=index_col, columns=cols_col, values=values_col)

    # Sort the matrix by descending order of values in the column with the highest value
    highest_col = matrix.idxmax(axis=1).values[0]
    matrix = matrix.sort_values(highest_col, ascending=ascending)

    return matrix

