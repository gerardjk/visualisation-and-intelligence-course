"""Build the Crayola and historical PC-palette figures used in the slides."""

from __future__ import annotations

import colorsys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "beamer" / "figs"


def build_crayola_figure() -> None:
    """Place the current 64-count box beside its 64 photographed swatches."""

    product = Image.open(FIGURES / "crayola-64-product-source.jpg").convert("RGB")
    swatches = Image.open(FIGURES / "crayola-64-swatches-source.jpg").convert("RGB")

    # The official product image arranges the swatches in five rows of eleven
    # and a final row of nine. Crop those photographs and reflow them as 8 x 8.
    x_regular = [137, 229, 321, 413, 505, 597, 689, 781, 873, 965, 1057]
    y_regular = [455, 566, 677, 788, 899]
    x_final = [228, 320, 412, 504, 596, 688, 780, 872, 964]
    centres = [(x, y) for y in y_regular for x in x_regular]
    centres.extend((x, 985) for x in x_final)
    assert len(centres) == 64

    tile_size = 104
    crop_radius = 44
    grid = Image.new("RGB", (8 * tile_size, 8 * tile_size), "white")
    for index, (x, y) in enumerate(centres):
        crop = swatches.crop(
            (x - crop_radius, y - crop_radius, x + crop_radius, y + crop_radius)
        )
        crop = ImageOps.contain(crop, (88, 88), Image.Resampling.LANCZOS)
        column = index % 8
        row = index // 8
        left = column * tile_size + (tile_size - crop.width) // 2
        top = row * tile_size + (tile_size - crop.height) // 2
        grid.paste(crop, (left, top))

    canvas = Image.new("RGB", (1760, 900), "white")
    product = ImageOps.contain(product, (790, 790), Image.Resampling.LANCZOS)
    grid = ImageOps.contain(grid, (820, 820), Image.Resampling.LANCZOS)
    canvas.paste(product, (20, (canvas.height - product.height) // 2))
    canvas.paste(grid, (900, (canvas.height - grid.height) // 2))
    canvas.save(FIGURES / "fig-crayola-chart.png", optimize=True)


def _sort_palette(colours: list[tuple[float, float, float]]) -> list[tuple[float, float, float]]:
    def key(rgb: tuple[float, float, float]) -> tuple[float, float, float]:
        hue, saturation, value = colorsys.rgb_to_hsv(*rgb)
        if saturation < 0.05:
            return (-1.0, 0.0, value)
        return (hue, saturation, value)

    return sorted(colours, key=key)


def _draw_swatches(
    ax: plt.Axes,
    colours: list[tuple[float, float, float]],
    y: float,
    *,
    height: float = 0.62,
) -> None:
    x0, x1 = 0.26, 0.975
    width = (x1 - x0) / len(colours)
    for index, colour in enumerate(colours):
        ax.add_patch(
            Rectangle(
                (x0 + index * width, y - height / 2),
                width,
                height,
                facecolor=colour,
                edgecolor="#dddddd",
                linewidth=0.25,
            )
        )


def build_retro_palette_figure() -> None:
    """Separate VGA's 16-colour and 256-colour display modes."""

    rgbi_hex = [
        "#000000", "#0000aa", "#00aa00", "#00aaaa",
        "#aa0000", "#aa00aa", "#aa5500", "#aaaaaa",
        "#555555", "#5555ff", "#55ff55", "#55ffff",
        "#ff5555", "#ff55ff", "#ffff55", "#ffffff",
    ]
    rgbi = [tuple(int(value[i : i + 2], 16) / 255 for i in (1, 3, 5)) for value in rgbi_hex]
    cga_four = [rgbi[index] for index in (0, 11, 13, 15)]

    ega_levels = [0.0, 1 / 3, 2 / 3, 1.0]
    ega = _sort_palette([(r, g, b) for r in ega_levels for g in ega_levels for b in ega_levels])

    # Any 256 entries could be loaded into VGA's indexed palette. This is one
    # illustrative selection from its 18-bit (64 x 64 x 64) colour gamut.
    vga_256 = [colorsys.hsv_to_rgb(index / 256, 0.92, 0.95) for index in range(256)]
    true_colour = [colorsys.hsv_to_rgb(index / 512, 1.0, 1.0) for index in range(512)]

    rows = [
        ("1981 · CGA 320×200\n4 at once, from 16", cga_four),
        ("1984 · EGA 640×350\n16 at once, from 64", ega),
        ("1987 · VGA 640×480\n16 at once, from 262,144", rgbi),
        ("1987 · VGA 320×200\n256 at once, from 262,144", vga_256),
        ("since ~1995 · 24-bit true colour\n16,777,216 at once", true_colour),
    ]

    fig, ax = plt.subplots(figsize=(16, 8.6))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 5.6)
    ax.axis("off")
    ax.text(0.62, 5.34, "What a PC could show", ha="center", va="center", fontsize=22, weight="bold")

    for y, (label, colours) in zip([4.55, 3.55, 2.55, 1.55, 0.55], rows):
        ax.text(0.235, y, label, ha="right", va="center", fontsize=13.5)
        _draw_swatches(ax, colours, y)

    fig.savefig(FIGURES / "fig-retro-palettes.png", dpi=160, bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)


if __name__ == "__main__":
    build_crayola_figure()
    build_retro_palette_figure()
