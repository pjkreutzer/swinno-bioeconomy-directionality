import string
import polars as pl
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick  # Added missing import
import seaborn.objects as so
from seaborn import axes_style

from cmcrameri import cm
from swinno_bioeconomy_directionality.config import (
    FIGURES_DIR,
    PROCESSED_DATA_DIR,
    RAW_DATA_DIR,
    EXTERNAL_DATA_DIR,
)

from swinno_bioeconomy_directionality.data_handling.io import DataLoader

WIDTH = 12
HEIGHT = 8


def create_figures():
    theme_dict = {
        **axes_style("whitegrid"),
        "grid.linestyle": "-",
        "axes.grid.axis": "y",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.spines.left": False,
    }

    so.Plot().theme(theme_dict)

    bioeconomy_share = pl.read_csv(PROCESSED_DATA_DIR / "swinno_bioeconomy_share.csv")

    bioeconomy_vision_data = DataLoader(RAW_DATA_DIR).load_visions()

    vision_summary = bioeconomy_vision_data.group_by("bioeconomy_vision").agg(
        pl.col("sinno_id").n_unique().alias("sum")
    )

    vision_colormap = create_vision_colormap()

    # Create and save figures
    fig_innovation_trends = plot_innovation_trends(bioeconomy_share)
    save_fig(fig_innovation_trends, "fig_innovation_trends")

    # Pass both required arguments
    fig_bioeconomy_vision_counts = plot_vision_counts(
        bioeconomy_vision_data, vision_colormap
    )
    save_fig(fig_bioeconomy_vision_counts, "fig_bioeconomy_vision_counts")

    fig_vision_producer_counts = plot_firm_counts(
        bioeconomy_vision_data, vision_colormap
    )
    save_fig(fig_vision_producer_counts, "fig_vision_producer_counts")


def save_fig(fig: plt.Figure, title: str):
    if isinstance(fig, so.Plot):
        fig.save(FIGURES_DIR / f"{title}.svg", bbox_inches="tight")
        fig.save(FIGURES_DIR / f"{title}.tex", format="pgf", bbox_inches="tight")
    else:
        fig.savefig(FIGURES_DIR / f"{title}.svg", bbox_inches="tight")
        fig.savefig(FIGURES_DIR / f"{title}.tex", format="pgf", bbox_inches="tight")


def create_vision_colormap():
    bioeconomy_visions = [
        "Bioecology Vision",
        "Biotechnology Vision",
        "Vision Neutral",
        "Bioresource Vision",
    ]

    return dict(zip(bioeconomy_visions, cm.batlowWS.colors[1::]))


def plot_innovation_trends(shares):
    """
    Plots network metrics for innovation and actor counts.

    Parameters:
    shares (polars.DataFrame): DataFrame containing the network metrics.

    Returns:
    matplotlib.figure.Figure: The resulting figure with subplots.
    """
    fig, axes = plt.subplots(
        1,
        3,
        figsize=(WIDTH, HEIGHT),
        constrained_layout=True,
    )

    def _plot_counts(ax, y, label, x=shares["year"]):
        ax.plot(
            x, y, linestyle="--", marker="o", alpha=0.15, label=label, color="black"
        )

    def _plot_ma(ax, y, label, x=shares["year"]):
        ax.plot(x, y, label=label, color="black", linewidth=2)

    metrics = [
        ("n_innovation", "Count"),
        ("n_bioeconomy", "Count"),
        ("pct_bioeconomy", "Share of Innovation"),
    ]
    axes = axes.flatten()
    for i, (metric, ylabel) in enumerate(metrics):
        _plot_counts(axes[i], shares[metric], metric.replace("_", " ").title())
        _plot_ma(axes[i], shares[f"ma5_{metric}"], "5 MA")
        axes[i].set_ylabel(ylabel)
        axes[i].legend()

    for ax in axes.flat:
        ax.set_xticks(shares["year"][::10])
        ax.set_xlabel("Year")

    axes[0].set_ylim(0, 160)
    axes[1].set_ylim(0, 160)
    axes[2].set_ylim(0, 0.5)
    axes[2].yaxis.set_major_formatter(mtick.PercentFormatter(1.0, decimals=0))

    titles = ["All Innovation", "Bioeconomy Innovation", "% Bioeconomy"]
    for i in range(3):
        axes[i].set_title(titles[i])

    for n, ax in enumerate(axes.flat):
        ax.text(
            -0.1,
            1.1,
            string.ascii_lowercase[n],
            transform=ax.transAxes,
            size=14,
        )
    fig.set_constrained_layout_pads(w_pad=0.15, h_pad=0.2, hspace=0.3)
    return fig


def plot_vision_counts(bioeconomy_vision_data, vision_colormap):
    yearly_counts, total_counts = create_vision_plotting_data(bioeconomy_vision_data)

    unique_visions = (
        bioeconomy_vision_data.filter(pl.col("bioeconomy_vision") != "Unsure")
        .select("bioeconomy_vision")
        .unique()
        .to_series()
        .to_list()
    )
    unique_visions = sorted(unique_visions)
    num_visions = len(unique_visions)

    cols = 2
    rows = (num_visions + 1) // 2

    # Create figure and subplots
    fig, axes = plt.subplots(
        rows, cols, figsize=(WIDTH, HEIGHT * rows / 2), constrained_layout=True
    )
    axes = axes.flatten() if rows * cols > 1 else [axes]  # Flatten for easier indexing

    # Set x-axis ticks to show every 10 years
    min_year = bioeconomy_vision_data["year"].min()
    max_year = bioeconomy_vision_data["year"].max()
    tick_years = list(
        range(
            (min_year // 10) * 10,  # Round down to nearest decade
            max_year + 10,  # Round up to nearest decade
            10,  # Step by 10 years
        )
    )

    # For each vision, create a subplot
    for i, vision in enumerate(unique_visions):
        # Filter data for this vision
        vision_data = yearly_counts.filter(pl.col("bioeconomy_vision") == vision)

        # Get years and counts as lists for plotting
        years = vision_data["year"].to_list()
        counts = vision_data["count"].to_list()

        # Create the bar plot
        axes[i].bar(
            years,
            counts,
            color=vision_colormap[vision],
            alpha=1,
        )

        # Set title and labels
        axes[i].set_title(vision)
        axes[i].set_xlabel("Year")
        axes[i].set_ylabel("Innovation Count")
        axes[i].set_xticks(tick_years)

        # Calculate total count for this vision
        total = total_counts.filter(pl.col("bioeconomy_vision") == vision)[
            "sum"
        ].to_list()[0]

        # Add total count annotation
        axes[i].annotate(
            f"Total: {total}",
            xy=(0.7, 0.9),
            xycoords="axes fraction",
            fontweight="bold",
            color=vision_colormap[vision],
        )

    # Hide any unused subplots
    for j in range(num_visions, len(axes)):
        axes[j].set_visible(False)

    # Apply theme settings
    for ax in axes:
        if not ax.get_visible():
            continue

        # Set ylim

        ax.set_ylim(top=18)
        ax.set_xlim(1969, 2022)

        # Remove top and right spines
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        # Use whitegrid
        ax.grid(axis="y", linestyle="-", alpha=0.2)
        ax.set_axisbelow(True)

        # Make y-axis spine invisible if needed
        ax.spines["left"].set_visible(False)
    return fig


def create_vision_plotting_data(bioeconomy_vision_data):
    yearly_counts = bioeconomy_vision_data.group_by(["bioeconomy_vision", "year"]).agg(
        pl.col("sinno_id").n_unique().alias("count")
    )

    total_counts = bioeconomy_vision_data.group_by("bioeconomy_vision").agg(
        pl.col("sinno_id").n_unique().alias("sum")
    )
    return yearly_counts, total_counts


def plot_firm_counts(bioeconomy_vision_data, vision_colormap, level: str = "firm"):
    firm_counts = calculate_producer_counts(bioeconomy_vision_data, level)

    unique_visions = firm_counts["bioeconomy_vision"].unique().to_list()
    unique_visions = sorted(unique_visions)

    num_visions = len(unique_visions)

    cols = 2
    rows = (num_visions + 1) // 2

    fig, axes = plt.subplots(
        rows, cols, figsize=(WIDTH, 4 * rows), constrained_layout=True
    )
    axes = axes.flatten()  # Flatten to make indexing easier

    for i, vision in enumerate(unique_visions):
        # Filter data for this vision
        vision_data = firm_counts.filter(pl.col("bioeconomy_vision") == vision)

        # Create histogram
        bars = axes[i].bar(
            x=vision_data["count"],
            height=vision_data["freq"],
            color=vision_colormap[vision],
        )
        axes[i].set_xlabel("Number of Innovations")
        axes[i].set_ylabel("Number of Producers")
        axes[i].set_title(f"{vision}")
        axes[i].set_xticks(range(1, 11))
        max_height = max([bar.get_height() for bar in bars])
        axes[i].set_ylim(0, max_height * 1.15)

        # Remove top and right spines
        axes[i].spines["top"].set_visible(False)
        axes[i].spines["right"].set_visible(False)

        # Use whitegrid
        axes[i].grid(axis="y", linestyle="-", alpha=0.2)
        axes[i].set_axisbelow(True)

        # Make y-axis spine invisible if needed
        axes[i].spines["left"].set_visible(False)
        axes[i].set_axisbelow(True)

        # Add text labels on top of bars
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                axes[i].annotate(
                    f"{int(height)}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # vertical offset
                    textcoords="offset points",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                )

    return fig


def calculate_producer_counts(
    bioeconomy_vision_data, level: str = "firm"
) -> pl.DataFrame:
    vision_producers = prepare_firm_data(bioeconomy_vision_data)

    producers_by_vision = (
        vision_producers.group_by([level, "bioeconomy_vision"])
        .agg(pl.col("sinno_id").n_unique().alias("count"))
        .sort(["bioeconomy_vision", "count"], descending=True)
        .filter(pl.col("bioeconomy_vision") != "Unsure")
    )

    hist = (
        producers_by_vision.group_by(["bioeconomy_vision", "count"])
        .agg(pl.col(level).count().alias("freq"))
        .sort(["bioeconomy_vision", "count"])
        .with_columns(pl.col("count").cast(pl.Int64))
    )

    visions = hist.select("bioeconomy_vision").unique()
    counts = pl.DataFrame({"count": list(range(1, 11))})

    full_grid = pl.concat(
        [
            counts.with_columns(
                pl.lit(vision["bioeconomy_vision"]).alias("bioeconomy_vision")
            )
            for vision in visions.iter_rows(named=True)
        ]
    )

    firm_counts = (
        full_grid.join(hist, on=["bioeconomy_vision", "count"], how="left")
        .fill_null(0)  # fill missing freq with 0
        .sort(["bioeconomy_vision", "count"])
    )

    return firm_counts


def prepare_firm_data(bioeconomy_vision_data):
    firms = DataLoader(EXTERNAL_DATA_DIR).load_aggregated_collaborations()

    all_collaborations = (
        firms.unpivot(index="sinno_id", value_name="node").drop("variable").drop_nulls()
    )
    producers_only = firms.drop(r"^coll.*$")

    vision_producers = bioeconomy_vision_data.join(
        all_collaborations, on="sinno_id", how="left"
    ).join(producers_only, on="sinno_id", how="left")

    return vision_producers


if __name__ == "__main__":
    create_figures()
