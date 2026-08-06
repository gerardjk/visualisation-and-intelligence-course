"""Build printable chart-card packs for the studio activities.

One card per A4-landscape page: a course figure, a neutral title, and the
session's prompt line. Print, cut nothing, deal pages: each pair draws three.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages

ROOT = Path(__file__).resolve().parents[1]
FIGS = ROOT.parent / "quarto-book" / "_book" / "atlas_files" / "figure-html"
ORIGINALS = ROOT / "shared" / "assets" / "originals"

PACKS = {
    "seeing-data": {
        "out": ROOT / "classes" / "01-seeing-data" / "activities" / "chart_cards.pdf",
        "prompt": "What is the claim?   ·   Who is it for?   ·   What could mislead?",
        "cards": [
            ("fig-yieldcurve-output-1.png", "The yield curve"),
            ("fig-energy-coordinate-output-1.png", "A reaction energy diagram"),
            ("fig-lorenz-output-1.png", "The Lorenz curve"),
            ("fig-abundance-output-1.png", "Cosmic abundance of the elements"),
            ("fig-intervals-output-1.png", "Estimates with error bars"),
            ("fig-gapminder-output-1.png", "Health and wealth of nations"),
            ("fig-heatmap-output-1.png", "A clustered heatmap"),
            ("fig-splom-output-1.png", "A scatterplot matrix"),
            ("fig-hubble-output-1.png", "The Hubble diagram",
             ("hubble-1929.png", "Hubble (1929), public domain")),
            ("fig-kleiber-output-1.png", "Kleiber's law"),
            ("fig-ramachandran-output-1.png", "The Ramachandran plot"),
            ("fig-phase-diagram-output-1.png", "A pressure–temperature phase diagram"),
            ("fig-cosine-output-1.png", "Cosine similarity"),
            ("fig-roc-output-1.png", "An ROC curve"),
            ("fig-permutation-output-1.png", "A permutation test"),
        ],
    },
    "visual-forms": {
        "out": ROOT / "classes" / "02-visual-forms" / "activities" / "form_cards.pdf",
        "prompt": ("Which visual task family?   ·   Which channel does the work?   "
                   "·   What form would you choose instead?"),
        "cards": [
            ("fig-gerrymander-output-1.png", "Two ways to district the same voters"),
            ("fig-outofafrica-output-1.png", "The out-of-Africa migrations"),
            ("fig-carboncycle-output-1.png", "The water and carbon cycles"),
            ("fig-trophic-output-1.png", "A trophic energy pyramid"),
            ("fig-foodweb-output-1.png", "A food web"),
            ("fig-airline-output-1.png", "An airline route network"),
            ("fig-tsne-output-1.png", "A t-SNE projection"),
            ("fig-embeddings-output-1.png", "Word embeddings"),
            ("fig-artmap-output-1.png", "An art-embedding map"),
            ("fig-delta-output-1.png", "Stylometry: Burrows's Delta"),
            ("fig-lda-output-1.png", "A topic model"),
            ("fig-arcs-output-1.png", "Emotional arcs of stories"),
            ("fig-culturenet-output-1.png", "Cultural history as a network"),
            ("fig-lesmis-output-1.png", "A character co-occurrence network"),
            ("fig-tonnetz-output-1.png", "The Tonnetz"),
        ],
    },
}


def build(name, spec):
    missing = [c[0] for c in spec["cards"] if not (FIGS / c[0]).exists()]
    assert not missing, f"{name}: missing figures {missing}"
    with PdfPages(spec["out"]) as pdf:
        for card in spec["cards"]:
            fname, title = card[0], card[1]
            original = card[2] if len(card) > 2 else None
            fig = plt.figure(figsize=(11.69, 8.27))  # A4 landscape
            fig.text(0.5, 0.94, title, ha="center", va="top",
                     fontsize=22, fontweight="bold")
            if original:
                ofile, ocredit = original
                axl = fig.add_axes([0.03, 0.13, 0.46, 0.72])
                axl.imshow(mpimg.imread(ORIGINALS / ofile))
                axl.axis("off")
                axl.set_title(f"original, {ocredit}", fontsize=10, color="#555555")
                axr = fig.add_axes([0.51, 0.13, 0.46, 0.72])
                axr.imshow(mpimg.imread(FIGS / fname))
                axr.axis("off")
                axr.set_title("course reproduction, generated from data",
                              fontsize=10, color="#555555")
            else:
                ax = fig.add_axes([0.06, 0.13, 0.88, 0.74])
                ax.imshow(mpimg.imread(FIGS / fname))
                ax.axis("off")
            fig.text(0.5, 0.05, spec["prompt"], ha="center", fontsize=13,
                     color="#555555")
            pdf.savefig(fig)
            plt.close(fig)
    print(f"{spec['out']}  ({len(spec['cards'])} cards)")


if __name__ == "__main__":
    for name, spec in PACKS.items():
        build(name, spec)
