import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as po
import plotly.express as px

def plot_bv_trends(df):
    
    palette = sns.color_palette("colorblind")[:5]

    # Create a custom palette with a default light gray color for "not bio" hue
    custom_palette = {
        hue: color if bioeconomy_vision != "No Bioeconomy Vision" else (0.8, 0.8, 0.8, 0.8)
        for hue, color, bioeconomy_vision in zip(
            df["bioeconomy_vision"], palette, df["bioeconomy_vision"]
        )
    }

    chart = sns.lineplot(
        data=df,
        x="year",
        y="count",
        hue="bioeconomy_vision",
        palette=custom_palette,
        linewidth=2
    )

    chart.set_xlabel("Year", fontdict={"fontsize": 12, "fontweight": "normal"})
    chart.set_ylabel("Count", fontdict={"fontsize": 12, "fontweight": "normal"})
    chart.tick_params(labelsize=10)

    # Customize x-axis tick labels
    years = df["year"].unique()
    chart.set_xticks(years[::10])
    chart.set_xticklabels(years[::10])

    # Create a custom legend with colored labels (no lines)
    handles, labels = chart.get_legend_handles_labels()

    # Set font color for legend labels based on the hue
    legend = chart.legend(
        bbox_to_anchor=(0.5, -0.35), loc="upper center", ncol=2, frameon=False
    )
    for text, label in zip(legend.texts, labels):
        text.set_color(custom_palette[label])

    sns.despine()

    plt.show()


def plot_heatmap(data):
    fig, ax = plt.subplots(1, 1)
    ax = sns.heatmap(
        data, annot=True, cmap="Blues", fmt="g", cbar=False, annot_kws={"fontsize": 9},
        square=True
    )
    ax.set(ylabel=None, xlabel=None)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=9)

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


def create_label_mapping(label_lookup):
    short_labels = {
        'Acquisition of machinery and software': 'Machinery & Software Acquisition',
        'Component number reduction': 'Component Number Reduction',
        'Cooperation with stakeholders': 'Stakeholder Cooperation',
        'Elimination of dirty components': 'Eliminate Dirty Components',
        'Environmental audit': 'Environmental Audit',
        'Environmental-friendly technologies': 'Eco-Friendly Technologies',
        'Green design packaging': 'Green Packaging Design',
        'Keep waste to a minimum': 'Waste Minimization',
        'Longer life cycle of downstream product': 'Extended Downstream Product Life',
        'Longer life cycle of product itself': 'Extended Product Life',
        'Longer life cycle products': 'Extended Product Lifespan',
        'New systems (remanufacturing systems and transport systems)': 'New Systems',
        'Not Eco-Innovation': 'Not Eco-Innovation',
        'Protection of timber harvest': 'Timber Harvest Protection',
        'Recyclability of product': 'Product Recyclability',
        'Recycle waste, water or materials': 'Waste Recycling',
        'Reduce Chemical Waste': 'Chemical Waste Reduction',
        'Reduce Use of Energy': 'Energy Use Reduction',
        'Reduce Use of Water': 'Water Use Reduction',
        'Reduced Air Pollution': 'Air Pollution Reduction',
        'Reduced Other Pollution': 'Other Pollution Reduction',
        'Reduced Water Pollution': 'Water Pollution Reduction',
        'Reduction / optimization of raw material use': 'Raw Material Optimization',
        'Replace fossil engery source with electrical energy': 'Use Electric Energy',
        'Replace fossil input with bio input': 'Use Bio Input',
        'Replace plastic with bio source': 'Use Bio Plastic',
        'Returnable/reusable packaging': 'Returnable/Reusable Packaging',
        'Unsure': 'Uncertain',
        'Use new cleaner material or new input with lower environmental impact': 'Cleaner Material Adoption',
        'Use of recycled materials': 'Recycled Material Usage'
    }
    label_mapping = label_lookup["Category"].to_dict()
    plot_labels = {str(k): short_labels[v] for k, v in label_mapping.items() if v in short_labels}
    return plot_labels


def plot_eco_innovation_by_bioeconomy_vision(data, label_lookup):
    label_mapping = create_label_mapping(label_lookup)

    data["innovation_type_label"] = data["innovation_type_code"].map(label_mapping)

    palette = sns.color_palette("colorblind")

    fig = sns.catplot(
        data=data,
        x="count",
        y="innovation_type_label",
        hue="innovation_type_group",
        col="bioeconomy_vision",
        kind="bar",
        col_wrap=2,
        palette=palette,
        dodge=False,
    )

    for ax in fig.axes.ravel():
        for c in ax.containers:
            ax.bar_label(c, label_type="edge", padding=2, fontsize=8)
        ax.margins(x=0.1)
        ax.tick_params(axis='y', labelsize=10)



    fig.set_titles("{col_name}")
    fig.set_axis_labels("", "")
    fig._legend.set_title(None)

    # plt.show()

    return fig
