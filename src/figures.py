import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as po
import plotly.express as px


def plot_counts(
    df1, df2, category_col, y, show_legend=True, legend_cols=None, y_label="Count"
):
    categories = df1[category_col].astype(str).unique()
    categories.sort()

    legend_ncols = len(categories) if legend_cols is None else legend_cols

    colors = sns.color_palette("colorblind", len(categories))
    palette = dict(zip(categories, colors))

    fig, axes = plt.subplots(
        ncols=1, nrows=2, sharex=False, sharey=True, layout="tight"
    )

    marker_size = 100
    df1 = df1.sort_values(by=category_col)
    df2 = df2.sort_values(by=category_col)

    sns.scatterplot(
        x=df1.index,
        y=y,
        hue=category_col,
        data=df1,
        ax=axes[0],
        palette=palette,
        s=marker_size,
    )

    sns.scatterplot(
        x=df2.index,
        y=y,
        hue=category_col,
        data=df2,
        ax=axes[1],
        palette=palette,
        s=marker_size,
    )

    for axs in axes:
        axs.set_ylabel(y_label)
        axs.set_xlabel("Year")
        axs.legend().remove()

    axes[0].set_title("Including Uncertains")
    axes[0].title.set_position([0.5, 1.05])  # adjust the position of the title

    axes[1].set_title("Excluding Uncertains")
    axes[1].title.set_position([0.5, 1.05])  # adjust the position of the title

    if not show_legend:
        fig.legend().remove()
    else:
        handles, labels = axes[0].get_legend_handles_labels()
        fig.legend(
            handles,
            labels,
            loc="lower center",
            ncol=legend_ncols,
            frameon=False,
            bbox_to_anchor=(0.5, -0.1),
        )  # adjust the position of the legend

    plt.subplots_adjust(bottom=0.2)

    plt.show()


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

