"""Generate local teaching figures used by the developed session packs."""

from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "seeing_data" / "assets"


def satisfaction_chart(path: Path, repaired: bool) -> None:
    labels = ["Standard format", "Redesigned format"]
    values = [82, 86]
    colours = ["#8fa6b3", "#e66852"]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(labels, values, color=colours, width=0.58)
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + (0.25 if repaired else 0.05),
                f"{value}%", ha="center", va="bottom", fontsize=13, fontweight="bold")

    if repaired:
        ax.set_ylim(0, 100)
        ax.set_title("Reported satisfaction differed by four percentage points", loc="left", fontweight="bold")
        ax.text(0, -0.25,
                "Sample size, uncertainty and group-assignment information were not supplied.",
                transform=ax.transAxes, color="#5f6c73", fontsize=10)
    else:
        ax.set_ylim(80, 87)
        ax.set_title("Redesign dramatically improves satisfaction", loc="left", fontweight="bold")

    ax.set_ylabel("Respondents satisfied (%)")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def encoding_comparison(path: Path) -> None:
    modes = ["Ferry", "Bus", "Train"]
    values = [310, 1080, 1390]
    colours = ["#30a8b1", "#18678f", "#e66852"]

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
    axes[0].barh(modes, values, color=colours)
    axes[0].set_title("Length on a common scale", loc="left", fontweight="bold")
    axes[0].set_xlabel("Monthly passengers")
    axes[0].spines[["top", "right"]].set_visible(False)

    sizes = [v / 7 for v in values]
    axes[1].scatter([1, 2, 3], [1, 1, 1], s=sizes, color=colours, alpha=0.85)
    axes[1].set_xticks([1, 2, 3], modes)
    axes[1].set_yticks([])
    axes[1].set_title("Area comparison", loc="left", fontweight="bold")
    axes[1].spines[["top", "right", "left"]].set_visible(False)
    axes[1].set_xlim(0.3, 3.7)

    fig.suptitle("The same values can require different perceptual judgements",
                 x=0.05, ha="left", fontsize=15, fontweight="bold")
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    satisfaction_chart(OUTPUT / "program_satisfaction_truncated.png", repaired=False)
    satisfaction_chart(OUTPUT / "program_satisfaction_repaired.png", repaired=True)
    forms_output = ROOT / "choosing_visual_forms" / "assets"
    forms_output.mkdir(parents=True, exist_ok=True)
    encoding_comparison(forms_output / "encoding_precision_comparison.png")
    print("Teaching assets generated.")


if __name__ == "__main__":
    main()
