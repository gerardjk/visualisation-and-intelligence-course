"""Remove em dashes and formulaic wording from the current class notebooks."""

from pathlib import Path

import nbformat


NOTEBOOKS = Path(__file__).resolve().parents[1] / "classes" / "02-visual-forms" / "notebooks"

REPLACEMENTS = {
    "# Choosing Visual Forms — solution": "# Choosing Visual Forms: solution",
    "These are **analytic reconstructions, not facsimiles**. The sources differ:":
        "The reconstructions use different kinds of source material:",
    "Part 1 reconstructs the visual\nlogic of nine canonical examples":
        "Part 1 reconstructs nine canonical examples",
    "For each chart: run the reconstruction, verify it, then change one consequential\n"
    "design decision. Do not describe a simulated or representative value as observed.":
        "For each chart, run the reconstruction, verify it, then change one design\n"
        "decision. Label simulated and representative values accurately.",
    "*Atlas #84 — Higgs discovery bump.*": "*Atlas #84: Higgs discovery bump.*",
    "deviation — a signed difference between observed data and a stated reference\n"
    "expectation. The counts below are simulated to reproduce the visual logic of\n"
    "the discovery figure; they are not CMS data and must not be cited as such.":
        "deviation: a signed difference between observed data and a stated reference\n"
        "expectation. The counts below are simulated examples. They are not CMS data.",
    "They are not measurements and must not be cited as a star catalogue.":
        "They are simulated examples, not measurements from a star catalogue.",
    "*Atlas #2 — Mohs hardness scale.*": "*Atlas #2: Mohs hardness scale.*",
    "ordinal reading — the order is real, the spacing is not.":
        "ordinal reading: the order is real, but the spacing is not.",
    "## 4 · The mirrored age–sex form: distribution":
        "## 4 · The mirrored age-sex form: distribution",
    "age–sex silhouette": "age-sex silhouette",
    "*Atlas #55 — Trophic / energy-flow pyramid.*":
        "*Atlas #55: Trophic / energy-flow pyramid.*",
    "The pyramid looks like a part-to-whole chart — explain why it is not.":
        "The pyramid looks like a part-to-whole chart. Explain why it is not.",
    "*Atlas #74 — Genetic code wheel.*": "*Atlas #74: Genetic code wheel.*",
    "The finished code is a genuine part-to-whole structure — 64\n"
    "codons partitioned into 20 amino acids plus stop signals.":
        "The finished code is a part-to-whole structure. Its 64 codons are\n"
        "partitioned into 20 amino acids plus stop signals.",
    "The crucial\noperation is real:": "The required\noperation is:",
    "The course transcription below is deliberately simplified: it is enough to recover\n"
    "the encoding logic but not to make historical estimates from individual points.":
        "The course transcription is simplified. It shows the encoding logic but does\n"
        "not support historical estimates from individual points.",
    "to recover\nthe encoding logic": "to reproduce\nthe encoding",
    "are wildly unequal: on a linear scale diamond (~10,000) dwarfs corundum":
        "are very unequal. On a linear scale diamond (~10,000) is five times as hard as corundum",
    "## Synthesis: from data type to visual vocabulary — example":
        "## Synthesis: from data type to visual vocabulary: example",
    "### AI disclosure — example": "### AI disclosure: example",
    "# Part 2 · Apply the framework": "# Part 2 · Apply the framework",
    "Use one deliberately messy transport dataset to move through the complete class\n"
    "workflow:":
        "Use the transport dataset to complete the class workflow:",
    "# Build the deliberately messy wide table. Run without editing.":
        "# Build the supplied wide table. Run without editing.",
    "Every chart must include an informative title, units, honest missing-value\n"
    "treatment and consistent mode colours. Do not use unsupported causal language.":
        "Every chart must include an informative title, units, documented missing-value\n"
        "treatment and consistent mode colours. Avoid unsupported causal claims.",
    "## Compare, select and reject — example":
        "## Compare, select and reject: example",
    "## Explain and disclose — example": "## Explain and disclose: example",
    "month–mode observations": "month-mode observations",
    "- **Tool used:** example AI coding assistant.":
        "- **Tool used:** coding assistant.",
    "- **What I would not trust the tool to do here:**":
        "- **What requires independent verification:**",
}


def clean(path):
    notebook = nbformat.read(path, as_version=4)
    for cell in notebook.cells:
        source = cell.source
        for old, new in REPLACEMENTS.items():
            source = source.replace(old, new)
        source = source.replace("—", ":")
        cell.source = source
    nbformat.write(notebook, path)


for notebook_path in sorted(NOTEBOOKS.glob("choosing_visual_forms*.ipynb")):
    clean(notebook_path)
    print(notebook_path)
