"""Figure coverage checker.

Every canonical course figure (quarto-book/_book/atlas_files/figure-html/) must
be used somewhere across the six sessions, in a deck, a sprint, or a card
pack. This script scans the sources of truth, writes FIGURE_COVERAGE.md, and
lists what is still unassigned (to be absorbed by sessions 3-6 as they are
built).

Run:  python figure_coverage.py          # report + write FIGURE_COVERAGE.md
      python figure_coverage.py --check  # exit 1 if any figure is unassigned
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIGS = ROOT.parent / "quarto-book" / "_book" / "atlas_files" / "figure-html"

SOURCES = {
    "Seeing Data: deck": ROOT / "classes" / "01-seeing-data" / "beamer" / "seeing-data.tex",
    "Choosing Visual Forms: deck": ROOT / "scripts" / "build_class02_deck.py",
    "card packs": ROOT / "scripts" / "build_figure_cards.py",
}

FIG_RE = re.compile(r"fig-[a-z0-9-]+-output-\d\.png")

# Removed from the course by explicit decision, not counted as unassigned.
EXCLUDED = {"fig-aiatsis"}


def normalise(name):
    """Collapse -output-N variants onto the figure's base name."""
    return re.sub(r"-output-\d\.png$", "", name)


def main(check=False):
    all_figs = sorted({normalise(p.name) for p in FIGS.glob("fig-*.png")} - EXCLUDED)
    used = {}
    for label, path in SOURCES.items():
        for m in FIG_RE.findall(path.read_text()):
            used.setdefault(normalise(m), []).append(label)

    unassigned = [f for f in all_figs if f not in used]
    lines = [
        "# Figure coverage",
        "",
        f"Canonical figures: **{len(all_figs)}** · assigned: **{len(used)}** · "
        f"unassigned: **{len(unassigned)}**",
        "",
        "Regenerate with `python scripts/figure_coverage.py`.",
        "",
        "## Assigned",
        "",
        "| Figure | Where |",
        "|---|---|",
    ]
    for f in sorted(used):
        lines.append(f"| {f} | {' · '.join(sorted(set(used[f])))} |")
    lines += ["", "## Unassigned (absorb into sessions 3–6 as they are built)", ""]
    lines += [f"- {f}" for f in unassigned] or ["*(none, full coverage)*"]
    (ROOT / "FIGURE_COVERAGE.md").write_text("\n".join(lines) + "\n")

    print(f"figures: {len(all_figs)}  assigned: {len(used)}  unassigned: {len(unassigned)}")
    if unassigned:
        print("unassigned:", ", ".join(unassigned))
    if check and unassigned:
        sys.exit(1)


if __name__ == "__main__":
    main(check="--check" in sys.argv)
