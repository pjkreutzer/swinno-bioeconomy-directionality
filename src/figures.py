import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
from cmcrameri import cm

# Set global options for all Plotly plots

royal_blue_800 = "#283aa4"
gray_600 = "#878f97"


def plot_bioeconomy_trends_interactive(data, y):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data["year"],
            y=data[y],
            mode="lines",
            name="Yearly",
            line=dict(dash="dash", color=gray_600),
        )
    )

    # Rolling mean
    rolling_mean = data[y].rolling(window=5).mean()
    fig.add_trace(
        go.Scatter(
            x=data["year"],
            y=rolling_mean,
            mode="lines",
            name="5-Year Moving Average",
            line=dict(color=royal_blue_800),
        )
    )
    fig.update_xaxes(type="date")
    fig.update_layout(
        showlegend=False,
        xaxis_range=["1965", "2025"],
        font=dict(family="Atkinson Hyperlegible"),
        height=550,
        hovermode="x unified",
    )

    return fig


def plot_count(data):
    fig, ax = plt.subplots()
    ax.plot(
        data["year"],
        data["bioeconomy_count"],
        label="Yearly",
    )

    # Calculate rolling mean and plot on same axis
    rolling_mean = data["bioeconomy_count"].rolling(window=5).mean()
    ax.plot(
        data["year"], rolling_mean, label="5-year moving average", linestyle="dashed"
    )

    ax.set_xticks(data["year"][::10])
    ax.tick_params(labelsize=10)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(frameon=False)

    plt.show()


def plot_share(data):
    fig, ax = plt.subplots()
    ax.plot(data["year"], data["bioeconomy_share"], label="Yearly")
    ax.set_xticks(data["year"][::10])
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))
    ax.tick_params(which="major", labelsize=10)

    # Calculate rolling mean and plot on same axis
    rolling_mean = data["bioeconomy_share"].rolling(window=5).mean()
    ax.plot(
        data["year"], rolling_mean, label="5-year moving average", linestyle="dashed"
    )
    ax.set_ylim((0, 0.5))
    ax.legend(frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.show()


def plot_bv_trends(df):
    palette = sns.color_palette("colorblind")[:5]

    # Create a custom palette with a default light gray color for "not bio" hue
    custom_palette = {
        hue: color
        if bioeconomy_vision != "No Bioeconomy Vision"
        else (0.7, 0.7, 0.7, 0.6)
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
        linewidth=2,
    )

    chart.tick_params(labelsize=10)

    # Customize x-axis tick labels
    years = df["year"].unique()
    chart.set_xticks(years[::10])
    chart.set_xticklabels(years[::10])
    chart.set_xlabel(None)
    chart.set_ylabel(None)

    # Create a custom legend with colored labels (no lines)
    handles, labels = chart.get_legend_handles_labels()

    # Set font color for legend labels based on the hue
    legend = chart.legend(
        bbox_to_anchor=(0.5, -0.1), loc="upper center", ncol=2, frameon=False
    )
    for text, label in zip(legend.texts, labels):
        if label == "No Bioeconomy Vision":
            text.set_color((0.4, 0.4, 0.4))
        else:
            text.set_color(custom_palette[label])

    sns.despine()

    plt.show()


def plot_bv_trends_interactive(df):
    color_map = {
        "No Bioeconomy Vision": "rgb(0.8, 0.8, 0.8)",  # Gray
        "Bioecology Vision": "#cc78bc",  # Purple
        "Bioresource Vision": "#de8f05",  # Orange
        "Biotechnology Vision": "#029e73",  # Green
    }

    traces = []

    for bv, bioeconomy_vision in df.groupby("bioeconomy_vision"):
        traces.append(
            go.Scatter(
                x=bioeconomy_vision["year"],
                y=bioeconomy_vision["count"],
                name=bv,
                mode="markers+lines",
                line=dict(color=color_map[bv]),  # Set line color based on the color_map
                visible="legendonly",
            )
        )

    fig = go.Figure(data=traces)
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            font=dict(size=30, family="Atkinson Hyperlegible"),
        ),
        hovermode="x unified",
        height=550,
        xaxis_range=["1965", "2015"],
        font=dict(family="Atkinson Hyperlegible"),
    )
    return fig


def plot_heatmap(data):
    fig, ax = plt.subplots(1, 1)
    ax = sns.heatmap(
        data,
        annot=True,
        cmap="Blues",
        fmt="g",
        cbar=False,
        annot_kws={"fontsize": 9},
        square=True,
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
        "Acquisition of machinery and software": "Machinery & Software Acquisition",
        "Component number reduction": "Component Number Reduction",
        "Cooperation with stakeholders": "Stakeholder Cooperation",
        "Elimination of dirty components": "Eliminate Dirty Components",
        "Environmental audit": "Environmental Audit",
        "Environmental-friendly technologies": "Eco-Friendly Technologies",
        "Green design packaging": "Green Packaging Design",
        "Keep waste to a minimum": "Waste Minimization",
        "Longer life cycle of downstream product": "Extended Downstream Product Life",
        "Longer life cycle of product itself": "Extended Product Life",
        "Longer life cycle products": "Extended Product Lifespan",
        "New systems (remanufacturing systems and transport systems)": "New Systems",
        "Not Eco-Innovation": "Not Eco-Innovation",
        "Protection of timber harvest": "Timber Harvest Protection",
        "Recyclability of product": "Product Recyclability",
        "Recycle waste, water or materials": "Waste Recycling",
        "Reduce Chemical Waste": "Chemical Waste Reduction",
        "Reduce Use of Energy": "Energy Use Reduction",
        "Reduce Use of Water": "Water Use Reduction",
        "Reduced Air Pollution": "Air Pollution Reduction",
        "Reduced Other Pollution": "Other Pollution Reduction",
        "Reduced Water Pollution": "Water Pollution Reduction",
        "Reduction / optimization of raw material use": "Raw Material Optimization",
        "Replace fossil engery source with electrical energy": "Use Electric Energy",
        "Replace fossil input with bio input": "Use Bio Input",
        "Replace plastic with bio source": "Use Bio Plastic",
        "Returnable/reusable packaging": "Returnable/Reusable Packaging",
        "Unsure": "Uncertain",
        "Use new cleaner material or new input with lower environmental impact": "Cleaner Material Adoption",
        "Use of recycled materials": "Recycled Material Usage",
    }
    label_mapping = label_lookup["Category"].to_dict()
    plot_labels = {
        str(k): short_labels[v] for k, v in label_mapping.items() if v in short_labels
    }
    return plot_labels


def plot_eco_innovation_by_bioeconomy_vision(data, label_lookup):
    label_mapping = create_label_mapping(label_lookup)

    data["innovation_type_label"] = data["innovation_type_code"].map(label_mapping)

    palette = cm.batlowS.colors

    # Set font to IBM Plex Sans
    plt.rcParams["font.family"] = "IBM Plex Sans"

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
        ax.tick_params(axis="y", labelsize=10)

        # Remove spines
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["left"].set_visible(False)

        # Add x-grid lines for every tick
        ax.xaxis.grid(True, linestyle="-")

    fig.set_titles("{col_name}")
    fig.set_axis_labels("", "")
    fig._legend.set_title(None)

    # plt.show()

    return fig


def plot_eco_innovation_by_bioeconomy_vision_interactive(data, codes_df):
    label_map = create_label_mapping(codes_df)

    data["innovation_type_label"] = data["innovation_type_code"].map(label_map)

    fig = px.bar(
        x=data["count"],
        y=data["innovation_type_label"],
        color=data["innovation_type_group"],
        facet_col=data["bioeconomy_vision"],
        facet_col_wrap=4,
    )

    fig.for_each_annotation(
        lambda a: a.update(text=a.text.split("=")[-1].strip(" Vision"))
    )
    fig.update_layout(
        showlegend=False,
        font=dict(family="Atkinson Hyperlegible"),
        margin=dict(l=150),
        yaxis=dict(autorange="reversed"),
    )
    fig.update_traces(hovertemplate="<b>%{x}</b> %{y} Innovations")

    # hide subplot y-axis titles and x-axis titles
    for axis in fig.layout:
        if type(fig.layout[axis]) == go.layout.YAxis:
            fig.layout[axis].title.text = ""
            fig.layout[axis].tickfont = dict(size=10)
        if type(fig.layout[axis]) == go.layout.XAxis:
            fig.layout[axis].title.text = ""
            fig.layout[axis].tickfont = dict(size=12)
    return fig
