"""Generate the A1 submission template notebook."""

from pathlib import Path

import nbformat as nbf

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "claude_course" / "assessments" / "A1-critique-and-repair" / "A1_template.ipynb"


def md(source):
    return nbf.v4.new_markdown_cell(source)


def code(source):
    return nbf.v4.new_code_cell(source)


cells = [
    md("""\
# A1 — Critique and Repair

**Before you start:** read `A1_brief.md`. This notebook is a *contract*: the
autograder executes it top-to-bottom and inspects the named variables and
functions below. Do not rename them. Run the self-check cell (last cell)
before submitting, then Kernel → Restart & Run All one final time.

Put your data file(s) in a `data/` folder next to this notebook, and your
screenshot of the original chart in `original_chart.png`.\
"""),
    code('''\
# ---- Metadata (G1) ----
META = {
    "student_id": "...",
    "artefact_id": "...",          # e.g. "POOL-03" or "BYO" for approved own chart
    "source_url": "...",           # where the original chart was published
    "publisher": "...",
    "publication_date": "...",     # as printed on the artefact
    "data_status": "...",          # "obtained" or "reconstructed"
}\
'''),
    md("""\
## Part A — Seeing (the critique)

Transcribe your **studio draft** (Class 2, supervised, AI-restricted) into the
dict below. Each field 10–150 words. Keep the "the chart shows / this
suggests" discipline: `chart_shows` is what is literally encoded;
`this_suggests` is the interpretive leap the design invites.\
"""),
    code('''\
# ---- Critique (G5 structure, H1 insight) ----
critique = {
    "main_claim": "...",
    "audience": "...",
    "visual_task": "...",
    "chart_shows": "...",
    "this_suggests": "...",
    "what_is_omitted": "...",
    "what_misleads": "...",
    "what_needs_verifying": "...",
}\
'''),
    md("""\
## Part B — Choosing (the repair)

Load the chart's underlying data as a **tidy** DataFrame named
`original_data`. If you reconstructed it, set `data_status` above and write
the reconstruction note: what you read off the chart, what you synthesised,
and how a marker could compare your table against the original.\
"""),
    code('''\
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ---- Data (G2, H2) ----
original_data = pd.DataFrame()  # TODO: load from data/ or build your reconstruction

RECONSTRUCTION_NOTE = """
...
"""
original_data.head()\
'''),
    md("""\
### The three redesigns (G3 mechanics, H3 defence, H4 craft)

One *best form* — the chart the original should have been — and two
alternatives serving **different** Visual Vocabulary categories. Categories
(exact strings): `deviation`, `correlation`, `ranking`, `distribution`,
`change over time`, `magnitude`, `part-to-whole`, `spatial`, `flow`.

Rules the autograder enforces: each function returns its Axes; every chart is
titled with the finding (≥ 15 characters); bar-family charts start at zero;
the three categories are distinct.\
"""),
    code('''\
BEST_CATEGORY = "..."


def redesign_best(original_data: pd.DataFrame):
    """THE chart the original should have been.

    State the reader's task in one sentence here. RETURN the Axes.
    """
    # TODO
    raise NotImplementedError


ax_best = redesign_best(original_data)\
'''),
    code('''\
ALT1_CATEGORY = "..."


def redesign_alt1(original_data: pd.DataFrame):
    """Alternative 1 — a different Vocabulary task. RETURN the Axes."""
    # TODO
    raise NotImplementedError


ax_alt1 = redesign_alt1(original_data)\
'''),
    code('''\
ALT2_CATEGORY = "..."


def redesign_alt2(original_data: pd.DataFrame):
    """Alternative 2 — a third Vocabulary task. RETURN the Axes."""
    # TODO
    raise NotImplementedError


ax_alt2 = redesign_alt2(original_data)\
'''),
    md("""\
### The defence (H3 — this is what is marked)

Argue which task the original *owed its readers*, and why your best form
serves it. Tie the task to channel precision and to the audience. Then be
honest about your own chart.\
"""),
    code('''\
DEFENCE = {
    "task_the_original_owed": "...",
    "why_best_form_serves_it": "...",
    "what_my_chart_could_mislead": "...",
    "simpler_alternative_considered": "...",
}\
'''),
    md("""\
## Part C — Verifying (the claim audit)

Generate an interpretation of **your** dataset with your AI assistant using
this prompt **verbatim** (paste your data's `head()` and `describe()` where
indicated):

> You are a data journalist. Here is a dataset: [paste head() and describe()].
> Write a confident 150–250 word interpretation of what this data shows,
> including at least six distinct factual claims, covering trends, causes,
> comparisons, and what it means for the future.

Paste the response into `generated_interpretation`, then classify **every**
claim it makes. You need at least six claims and at least one in each
category. For every claim you mark `supported` or `unsupported`, write a
probe: a zero-argument function returning the evidence (a filtered/aggregated
DataFrame or Series). `unverifiable` claims get no probe — that's the point.\
"""),
    code('''\
generated_interpretation = """
...
"""\
'''),
    code('''\
# ---- Claims (G4, H5). Keys: short paraphrase of each claim. ----
claims = {
    "example claim one": "...",   # "supported" / "unsupported" / "unverifiable"
    "example claim two": "...",
}

probes = {
    # "example claim one": lambda: original_data.groupby(...)...,
}\
'''),
    md("""\
## Disclosure (G6)

The block from class, now assessed. Idiomatic generated code with
"no AI used" written here is a disclosure failure.\
"""),
    code('''\
disclosure = {
    "tool_contributed": "...",
    "how_checked": "...",
    "i_decided": "...",
    "would_not_trust": "...",
}\
'''),
    md("""\
## Self-check — run before submitting

This is the same code the marker runs. Fix everything it flags, then
Kernel → Restart & Run All.\
"""),
    code('''\
import a1_autograder
a1_autograder.self_check(globals())\
'''),
]


nb = nbf.v4.new_notebook()
nb.cells = cells
nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python",
                             "name": "python3"}
nb.metadata["language_info"] = {"name": "python"}
OUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUT, "w") as f:
    nbf.write(nb, f)
print(OUT)
