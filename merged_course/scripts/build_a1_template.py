"""Generate the A1 submission template notebook (merged-course conventions:
three artefacts across three domains — one primary, two supporting —
four-way claim taxonomy, Chart Choice Decision Record, five-question
disclosure)."""

from pathlib import Path

import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assessments" / "A1-critique-and-repair" / "A1_template.ipynb"


def md(source):
    return nbf.v4.new_markdown_cell(source)


def code(source):
    return nbf.v4.new_code_cell(source)


def meta_cell(n, role):
    return code(f'''\
# ---- Artefact {n} metadata (G1) — {role} ----
META_{n} = {{
    "artefact_id": "...",          # from the released pool, e.g. "POOL-03"
    "domain": "...",               # the pool row's domain, e.g. "energy"
    "source_url": "...",           # where the original chart was published
    "publisher": "...",
    "publication_date": "...",     # as printed on the artefact
    "data_status": "...",          # "obtained" or "reconstructed"
}}\
''')


def data_cell(n):
    return code(f'''\
# ---- Artefact {n} data (G2, H2) ----
data_{n} = pd.DataFrame()  # TODO: load from data/ or build your reconstruction

RECONSTRUCTION_NOTE_{n} = """
...
"""
data_{n}.head()\
''')


def redesign_cell(n, doc):
    return code(f'''\
CATEGORY_{n} = "..."


def redesign_{n}(data_{n}: pd.DataFrame):
    """{doc}

    State the reader's task in one sentence here. RETURN the Axes.
    """
    # TODO
    raise NotImplementedError


ax_{n} = redesign_{n}(data_{n})\
''')


def compact_critique_cell(n):
    return code(f'''\
# ---- Compact critique, artefact {n} (G5) ----
critique_{n} = {{
    "main_claim": "...",
    "visible_vs_interpretation": "...",   # what is literally encoded vs the leap invited
    "what_misleads": "...",
    "repaired_caption": "...",
}}

# One-line defence of this redesign (G5): category is CATEGORY_{n} above.
WHY_{n} = "..."   # ≥ 10 words: why this form fits this audience and task\
''')


cells = [
    md("""\
# A1 — Critique and Repair

**Before you start:** read `A1_brief.md`. This notebook is a *contract*: the
autograder executes it top-to-bottom and inspects the named variables and
functions below. Do not rename them. Run the self-check cell (last cell)
before submitting, then Kernel → Restart & Run All one final time.

You work with **three artefacts from the released pool, from three
different domains**: **artefact 1 is your primary** (full critique, full
Decision Record, and the Part C claim audit); **artefacts 2 and 3 are
supporting** (compact critique and one redesign each). Across the three
redesigns you must cover **three distinct Visual Vocabulary categories**.

Put your data file(s) in a `data/` folder next to this notebook, and your
screenshots of the original charts in `original_chart_1.png`,
`original_chart_2.png`, `original_chart_3.png`.\
"""),
    code('''\
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

STUDENT_ID = "..."\
'''),
    md("""\
## Artefact 1 — primary

Full pipeline: metadata, data, full critique (transcribed from your
**supervised draft**), best-form redesign, full Chart Choice Decision Record.\
"""),
    meta_cell(1, "PRIMARY"),
    md("""\
### Critique (G5 structure, H1 insight)

Transcribe your **supervised draft** (supervised Dashboards-session window,
AI-restricted) into the dict below. Keep the Seeing Data discipline:
`directly_visible` is what is literally encoded;
`interpretation_not_observation` is the leap the design invites. Finish with
the repaired caption — the caption the original *should* have carried.\
"""),
    code('''\
# ---- Full critique, artefact 1 (G5 structure, H1 insight) ----
critique_1 = {
    "main_claim": "...",
    "audience": "...",
    "visual_task": "...",
    "directly_visible": "...",
    "interpretation_not_observation": "...",
    "what_is_omitted": "...",
    "what_misleads": "...",
    "what_needs_verifying": "...",
    "repaired_caption": "...",
}\
'''),
    md("""\
### Data

Load the chart's underlying data as a **tidy** DataFrame named `data_1`. If
you reconstructed it, set `data_status` in `META_1` and write the
reconstruction note: what you read off the chart, what you synthesised, and
how a marker could compare your table against the original.\
"""),
    data_cell(1),
    md("""\
### Best-form redesign (G3 mechanics, H4 craft)

The chart the original should have been. Categories (exact strings):
`deviation`, `correlation`, `ranking`, `distribution`, `change over time`,
`magnitude`, `part-to-whole`, `spatial`, `flow`.

Rules the autograder enforces on every redesign: the function returns its
Axes; the chart is titled with the finding (≥ 15 characters); bar-family
charts start at zero; and the three categories (artefacts 1–3) are
**distinct**.\
"""),
    redesign_cell(1, "THE chart artefact 1's original should have been."),
    md("""\
### Chart Choice Decision Record (G5 structure, H3 defence)

The same form as the Choosing Visual Forms studio — this is what is marked.
Argue from the audience's task, and be honest: the rejected alternative must
be one you genuinely considered, with a specific reason.\
"""),
    code('''\
decision_record = {
    "intended_audience": "...",
    "question_they_need_answered": "...",
    "decision_supported": "...",
    "vocabulary_category": "...",        # should match CATEGORY_1
    "required_comparison": "...",
    "selected_form": "...",
    "why_it_fits": "...",                # ≥ 10 words
    "rejected_alternative": "...",
    "reason_for_rejection": "...",       # ≥ 10 words, specific
}\
'''),
    md("""\
## Artefact 2 — supporting

Compact critique, data, and one redesign in a **different Vocabulary
category** (and from a **different domain**).\
"""),
    meta_cell(2, "SUPPORTING"),
    data_cell(2),
    redesign_cell(2, "Redesign of artefact 2 — a second Vocabulary category."),
    compact_critique_cell(2),
    md("""\
## Artefact 3 — supporting

As artefact 2: third domain, third Vocabulary category.\
"""),
    meta_cell(3, "SUPPORTING"),
    data_cell(3),
    redesign_cell(3, "Redesign of artefact 3 — a third Vocabulary category."),
    compact_critique_cell(3),
    md("""\
## Part C — Verifying (the claim audit, on your PRIMARY artefact)

Generate an interpretation of **artefact 1's** dataset with your AI assistant
using this prompt **verbatim** (paste `data_1.head()` and `data_1.describe()`
where indicated):

> You are a data journalist. Here is a dataset: [paste head() and describe()].
> Write a confident 150–250 word interpretation of what this data shows,
> including at least six distinct factual claims, covering trends, causes,
> comparisons, and what it means for the future.

Paste the response into `generated_interpretation`, then classify **every**
claim with the four-way taxonomy from the Seeing Data lab:

- `supported` — the data directly backs it → write an evidence probe
- `plausible but unverified` — sounds right; this dataset cannot settle it
- `unsupported` — asserted with no evidence in this data either way
- `contradicted` — the data shows otherwise → write an evidence probe

Probes are zero-argument functions returning the evidence (a filtered or
aggregated DataFrame/Series). You need ≥ 6 claims, with at least one
`supported`, one `plausible but unverified`, and one `unsupported` or
`contradicted`.\
"""),
    code('''\
generated_interpretation = """
...
"""\
'''),
    code('''\
# ---- Claims (G4, H5). Keys: short paraphrase of each claim. ----
claims = {
    "example claim one": "...",   # supported / plausible but unverified / unsupported / contradicted
    "example claim two": "...",
}

probes = {
    # required for every supported/contradicted claim:
    # "example claim one": lambda: data_1.groupby(...)...,
}\
'''),
    md("""\
## AI disclosure (G6)

The five questions from every class notebook, now assessed. Report assistant
use or non-use accurately; false or misleading disclosure is an
academic-integrity issue.\
"""),
    code('''\
disclosure = {
    "which_assistants": "...",
    "what_contributed": "...",              # code, explanation, debugging, text
    "accepted_modified_rejected": "...",    # and why
    "how_verified": "...",                  # checks, tests, manual inspection
    "limitations_remaining": "...",
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
