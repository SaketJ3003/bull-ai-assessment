import os
import matplotlib.pyplot as plt

def create_financial_chart(
    title,
    categories,
    values,
    secondary_values=None,
    primary_label="",
    secondary_label="",
    output_path="chart.png",
):
    if not categories or not values:
        return None

    fig, ax1 = plt.subplots(figsize=(5.15, 2.38), dpi=180)
    fig.patch.set_facecolor("#F8FAFE")
    ax1.set_facecolor("#F8FAFE")

    x = list(range(len(categories)))
    cleaned_values = [value if value is not None else 0 for value in values]

    bars = ax1.bar(
        x, cleaned_values, width=0.56,
        color="#557FE0", edgecolor="#3F65BD", linewidth=0.5, zorder=3
    )
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories, fontsize=7, color="#536078")
    ax1.tick_params(axis="y", labelsize=6, colors="#6A7588")
    ax1.tick_params(axis="x", length=0, pad=5)
    ax1.set_title(title, fontsize=9.5, fontweight="bold",
                  color="#172033", loc="left", pad=9)

    if primary_label:
        ax1.set_ylabel(primary_label, fontsize=6.5, color="#657087")

    ax1.grid(axis="y", color="#DDE4EF", linewidth=0.55, alpha=0.85, zorder=0)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.spines["left"].set_color("#D8DFEA")
    ax1.spines["bottom"].set_color("#D8DFEA")

    for bar, value in zip(bars, cleaned_values):
        try:
            label = f"{float(value):,.0f}" if abs(float(value)) >= 10 else f"{float(value):g}"
        except (TypeError, ValueError):
            label = str(value)
        ax1.text(
            bar.get_x() + bar.get_width() / 2, bar.get_height(), label,
            ha="center", va="bottom", fontsize=5.5,
            color="#3D4C68", fontweight="bold", clip_on=True
        )

    if secondary_values:
        ax2 = ax1.twinx()
        cleaned_secondary = [value if value is not None else 0 for value in secondary_values]
        ax2.plot(
            x, cleaned_secondary,
            color="#D86A73", marker="o", markerfacecolor="#FFFFFF",
            markeredgecolor="#D86A73", markeredgewidth=1.2,
            linewidth=1.7, markersize=4.2, zorder=5
        )
        if secondary_label:
            ax2.set_ylabel(secondary_label, fontsize=6.5, color="#A35B63")
        ax2.tick_params(axis="y", labelsize=6, colors="#A35B63")
        ax2.spines["top"].set_visible(False)
        ax2.spines["left"].set_visible(False)
        ax2.spines["right"].set_color("#E5CDD0")

    fig.tight_layout(pad=1.0)
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    fig.savefig(output_path, dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    return output_path
