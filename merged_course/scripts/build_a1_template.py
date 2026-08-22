"""Generate the A1 submission template notebook.

The notebook contract is three artefacts from distinct domains. Each artefact
has identifying information, supplied data, a full critique, an alternative
view, a full Decision Record and a claim audit. Artefact 1 is the supervised
primary; that supervised critique is the only structural difference.
"""

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
# ---- Artefact {n} identifying information (META_{n}, G1), {role} ----
# META means metadata: information identifying the chart. The _{n} means artefact {n}.
META_{n} = {{
    "artefact_id": "...",          # from the released pool, e.g. "POOL-03"
    "domain": "...",               # copy the exact domain from the pool row/provenance sheet
    "source_url": "...",           # where the original chart was published
    "publisher": "...",
    "publication_date": "...",     # copy the pool row/provenance value
    "data_status": "supplied",     # keep as "supplied"
}}\
''')


def critique_cell(n):
    return code(f'''\
# ---- Full 9-field critique, artefact {n} (G5 structure, H1 insight) ----
critique_{n} = {{
    "main_claim": "...",
    "audience": "...",
    "visual_task": "...",
    "directly_visible": "...",
    "interpretation_not_observation": "...",
    "what_is_omitted": "...",
    "what_misleads": "...",
    "what_needs_verifying": "...",
    "repaired_caption": "...",
}}\
''')


def data_cell(n):
    return code(f'''\
# ---- Artefact {n} data (G2, H2) ----
data_{n} = pd.read_csv("data/POOL-XX_source_data.csv")  # TODO: use your pool ID

# Describe every filter, reshape, derived field or other transformation.
# If none, state that you used the supplied rows and fields unchanged.
TRANSFORMATION_NOTE_{n} = "..."
data_{n}.head()\
''')


def redesign_cell(n):
    return code(f'''\
CATEGORY_{n} = "..."


def redesign_{n}(data_{n}: pd.DataFrame):
    """Alternative view of artefact {n} designed for your stated claim.

    State the reader's task in one sentence here. RETURN the Axes.
    """
    # TODO
    raise NotImplementedError


ax_{n} = redesign_{n}(data_{n})\
''')


def decision_record_cell(n):
    # Artefact 1 carries the per-field annotations; 2 and 3 refer back to it.
    if n == 1:
        return code('''\
decision_record_1 = {
    "intended_audience": "...",             # who will use the view
    "question_they_need_answered": "...",   # the question your view answers
    "decision_supported": "...",            # what they can decide or conclude
    "vocabulary_category": "...",        # must match CATEGORY_1
    "required_comparison": "...",           # values/groups/times they must compare
    "selected_form": "...",                 # chart form you chose
    "why_it_fits": "...",                # explain why this form fits
    "rejected_alternative": "...",
    "reason_for_rejection": "...",       # give a specific reason
}''')
    return code(f'''\
decision_record_{n} = {{
    "intended_audience": "...",
    "question_they_need_answered": "...",
    "decision_supported": "...",
    "vocabulary_category": "...",        # must match CATEGORY_{n}
    "required_comparison": "...",
    "selected_form": "...",
    "why_it_fits": "...",                # explain why this form fits
    "rejected_alternative": "...",
    "reason_for_rejection": "...",       # give a specific reason
}}\
''')


def audit_cells(n):
    return [
        md(f"""\
### Claim audit — artefact {n}

Paste the assistant's response to the supplied prompt, then classify every
distinct factual claim.\
"""),
        code(f'''\
generated_interpretation_{n} = """
...
"""\
'''),
        code(f'''\
# ---- Claims (G4, H5). Keys are short paraphrases of each claim. ----
claims_{n} = {{
    "example claim one": "...",   # supported / plausible but unverified / unsupported / contradicted
    "example claim two": "...",
}}

probes_{n} = {{
    # required for every supported/contradicted claim:
    # "example claim one": lambda: data_{n}.groupby(...)...,
}}\
'''),
    ]


cells = [
    md("""\
# A1. Reading Claims and Designing Alternatives

**Before you start:** read the A1 brief PDF in Canvas. This notebook is a
*contract*: the autograder executes it top-to-bottom and inspects the named
variables and functions below. Do not rename them. Run the self-check cell
(last cell) before submitting, then Kernel → Restart & Run All one final time.

You work with **three artefacts from the released pool, from three different
domains**. Each receives a full 9-field critique, alternative view, Chart
Choice Decision Record and claim audit. **Artefact 1 is the primary**: the one
whose critique you complete in the supervised class activity. That is the only
requirement that differs across the three. Across the three views, use valid
Visual Vocabulary categories and represent **at least two different
categories**. If you use the same category more than once, explain in each
Decision Record why it is the best fit for that artefact's claim.

Put your data files in a `data/` folder next to this notebook, and rename the
three supplied chart images `original_chart_1.png`, `original_chart_2.png` and
`original_chart_3.png`.\
"""),
    code('''\
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

STUDENT_ID = "..."\
'''),
]

for n in (1, 2, 3):
    if n == 1:
        cells.append(md("""\
## Artefact 1: primary (supervised critique)

Complete the full pipeline. Transcribe the nine-field critique from your
supervised draft; complete the remaining work under the AI policy in the
brief.\
"""))
    else:
        cells.append(md(f"""\
## Artefact {n}

Complete the same full pipeline using an artefact from a different domain.
Choose the Visual Vocabulary category that best fits your stated claim. Across
all three artefacts, represent at least two categories.\
"""))

    if n == 1:
        critique_md = md("""\
### Critique — artefact 1 (G5 structure, H1 insight)

Complete all nine fields. Write enough to answer each field clearly; do not pad
short fields to meet an arbitrary length. For artefact 1, transcribe
your supervised, AI-restricted draft and edit it for clarity without AI.

- `main_claim`: the chart's one-sentence message
- `audience`: its intended reader or user
- `visual_task`: what that reader must do (compare, rank, locate, track change, etc.)
- `directly_visible`: what marks, labels and scales literally encode
- `interpretation_not_observation`: what is invited but not directly shown
- `what_is_omitted`: missing data, context, uncertainty or comparison
- `what_misleads`: unjustified impressions created by selection, encoding or framing—including title, caption, annotation or baseline
- `what_needs_verifying`: a source, calculation or inference to check
- `repaired_caption`: the supported finding and its important limit\
""")
    else:
        critique_md = md(f"""\
### Critique — artefact {n} (G5 structure, H1 insight)

Complete all nine fields using the field guide under artefact 1. Write enough
to answer each field clearly. This critique is completed outside the supervised activity. Keep
what is directly visible separate from interpretation and finish with a caption
that states the supported finding and its important limit.\
""")

    cells.extend([
        meta_cell(n, "PRIMARY" if n == 1 else "ARTEFACT"),
        critique_md,
        critique_cell(n),
        md(f"""\
### Data — artefact {n}

Copy the supplied `source_data.csv` into `data/`, rename it with its pool ID,
and load it unchanged as the tidy DataFrame `data_{n}`. Keep `data_status` as
`supplied`. Do not overwrite `data_{n}`; derive any filtered, reshaped or new
data inside `redesign_{n}` or in a separately named variable, and document
every transformation.\
"""),
        data_cell(n),
        md(f"""\
### Alternative view — artefact {n} (G3 mechanics, H4 craft)

State the claim your alternative is designed to communicate. Categories
(exact strings): `deviation`, `correlation`, `ranking`, `distribution`,
`change over time`, `magnitude`, `part-to-whole`, `spatial`, `flow`.

The function must return its Axes; title the finding with at least 15
characters; and show zero for bar-family charts. Across all three artefacts,
represent at least two Visual Vocabulary categories.\
"""),
        redesign_cell(n),
        md("""\
### Chart Choice Decision Record — artefact 1 (G5, H3)

Argue from the audience's task. Identify who will use the view, their question,
the decision it supports, the Vocabulary category, the comparison required and
the selected chart form. Explain why it fits. Name one form you genuinely
considered and give a specific reason for rejecting it. `vocabulary_category`
must match `CATEGORY_1`.\
""") if n == 1 else md(f"""\
### Chart Choice Decision Record — artefact {n} (G5, H3)

Use the same nine-field Decision Record explained under artefact 1. Argue from
the audience's task; `vocabulary_category` must match `CATEGORY_{n}`; and give a
specific reason for rejecting an alternative you genuinely considered.\
"""),
        decision_record_cell(n),
    ])

cells.append(md("""\
## Part C. Verifying — claim audits for all three artefacts

For **each artefact**, generate an interpretation with your AI assistant using
this prompt **verbatim**. Substitute the corresponding dataset's `head()` and
`describe()` output where indicated:

> You are a data journalist. Here is a dataset: [paste head() and describe()].
> Write a confident 150–250 word interpretation of what this data shows,
> including at least four distinct factual claims, covering trends, causes,
> comparisons, and what it means for the future.

Classify every claim using: `supported`, `plausible but unverified`,
`unsupported`, or `contradicted`. Write a zero-argument evidence probe for
every supported or contradicted claim. Each audit needs at least four claims,
at least one supported or contradicted claim, and a non-empty probe result for
every such claim. Classify honestly; do not manufacture labels to fill a quota.\
"""))

cells.append(md('''\
### Claim-audit structure example

Use the same short claim text as the key in both dictionaries. Every
`supported` or `contradicted` claim needs a probe returning the relevant rows
or aggregation.

```python
claims_1 = {
    "Values increased after 2020": "supported",
    "Policy caused the increase": "plausible but unverified",
}
probes_1 = {
    "Values increased after 2020": lambda: data_1.loc[data_1["Year"] >= 2020],
}
```

Adapt the probe to your actual fields and claim. This illustrates structure;
it is not evidence for any pool artefact.\
'''))

for n in (1, 2, 3):
    cells.extend(audit_cells(n))

cells.extend([
    md("""\
## AI disclosure (G6)

Answer all five questions with at least three words. Report assistant use or
non-use accurately; false or misleading disclosure is an academic-integrity
issue.\
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
## Self-check: run before submitting

This runs the marker's G1–G6 checks (54 marks). Fix everything it flags, then
Kernel → Restart & Run All. The marker awards G0's remaining 6 marks only after
clean top-to-bottom execution on the marking system.\
"""),
    code('''\
import a1_autograder
a1_autograder.self_check(globals())\
'''),
])


nb = nbf.v4.new_notebook()
nb.cells = cells
nb.metadata["kernelspec"] = {
    "display_name": "Python 3",
    "language": "python",
    "name": "python3",
}
nb.metadata["language_info"] = {"name": "python"}
OUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUT, "w") as f:
    nbf.write(nb, f)
print(OUT)
