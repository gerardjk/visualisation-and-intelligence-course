# A1 — Critique and Repair

**Individual assessment · 30% · covers Weeks 1–2**
**Released:** in the Seeing Data session (Thursday 30 July 2026).
**Supervised component:** 25-minute window at the start of the
Dashboards-session studio (Thursday 13 August 2026).
**Due:** **Monday 24 August 2026, 11:59pm** (Sydney time).
**Submit:** one completed `A1_template.ipynb`, your data files in
`data/`, and a PNG/screenshot of each original chart
(`original_chart_1..3.png`).

## The task

You will take **three published charts from the wild — from three different
domains** — and work them through the course pipeline: *see* what each
claims, *repair* it with the Visual Vocabulary, and *verify* a machine's
interpretation of the data. One artefact is your **primary** (full treatment);
the other two are **supporting** (compact treatment). The first two sessions
rehearse every part of this: the Seeing Data studio (Critique and Repair
sheet, Critique 1) rehearses Parts A and C; the Choosing Visual Forms studio
(Redesign ×3, Chart Choice Decision Record) rehearses Part B.

- **Part A — Seeing (the critiques).** For the **primary artefact**: the full
  9-field critique — selection, encoding, framing, omission, keeping the
  discipline from Seeing Data (*directly visible* vs *interpretation rather
  than observation*), ending with a repaired caption. **Drafted by hand in
  the supervised, AI-restricted window in the Dashboards session**, then
  transcribed into the notebook's `critique_1` cell. For each **supporting
  artefact**: a compact 4-field critique (main claim, visible vs
  interpretation, what misleads, repaired caption).
- **Part B — Choosing (the repairs).** For each of the three artefacts:
  obtain or faithfully reconstruct its underlying data and produce **one
  redesign** — the chart that original should have been. Across the three
  artefacts the redesigns must serve **three distinct Visual Vocabulary
  categories**. Defend the primary redesign with a full **Chart Choice
  Decision Record** (the same form as the Choosing Visual Forms studio,
  including the rejected alternative and the specific reason); defend each
  supporting redesign with its category and a one-line justification
  (`WHY_2`, `WHY_3`).
- **Part C — Verifying (the claim audit, primary artefact).** Generate an
  interpretation of your **primary** dataset using the **supplied prompt**
  (verbatim, in the template).
  Classify **every claim** with the four-way taxonomy from the Seeing Data lab:

  | Label | Meaning |
  |---|---|
  | `supported` | the data directly backs it — attach an evidence probe |
  | `plausible but unverified` | sounds right; this dataset cannot settle it |
  | `unsupported` | asserted with no evidence in this data either way |
  | `contradicted` | the data shows otherwise — attach an evidence probe |

  Probes are zero-argument functions returning the evidence (a filtered or
  aggregated DataFrame/Series) — required for every `supported` and
  `contradicted` claim. Finish with the five-question AI disclosure.

## Your artefacts

Choose **three artefacts from three different domains**: at least two from
the **released, verified** pool; at most one may be your own found-in-the-wild
chart (a real published chart, a named publisher and date, and an obtainable
or reasonably reconstructable data source — approval required). Record your
three choices, and which is your **primary**, by **Monday 10 August 2026**
(Canvas). Two students may study the same source chart, but every submission
must be individual and independently produced.

**Data rule.** If the exact data is not published, reconstruct it faithfully
(digitise, or synthesise to match the chart's visible quantities) and say so:
set `data_status = "reconstructed"` and write the reconstruction note. This is
the atlas book's own method — representative data, never passed off as the
original measurement. Undisclosed reconstruction is an academic-integrity
issue. Disclosed reconstruction remains eligible for full marks; its fidelity
and limitations are judged under H2. The rule applies per artefact
(`data_status` in each `META_n`).

**Copyright note.** Include only the chart image needed for criticism and
review, cite its publisher, creator (where known), date and source URL, and do
not republish the assessment beyond the subject site. Follow any additional
UTS library or copyright guidance supplied with the task.

## AI policy

Part A's primary critique is drafted AI-free in the supervised window. An
assistant may be used in Part B under the notebook contract: docstrings first, accept or reject
completions, and nothing counts until the checks pass. Part C requires an
assistant-generated interpretation; students who cannot or do not wish to use
an assistant can request a course-supplied generated interpretation. The
disclosure block is assessed: report use accurately, including legitimate
non-use in Part B. False or misleading disclosure is an academic-integrity
issue.

## Submission contract (read this twice)

The template notebook defines named variables and functions per artefact
(`META_1..3`, `critique_1..3`, `data_1..3`, `redesign_1..3`,
`decision_record`, `claims`, `disclosure` …). The
autograder executes your notebook top-to-bottom on a clean machine and inspects
those names. **Run the self-check cell before submitting** — it is the same
code the marker runs. A notebook that does not execute end-to-end scores 0 on
the automated items until resubmitted (one resubmission, capped at 80%).

---

## Rubric — 100 marks (scaled to 30% of the course)

### Automated (60 marks, scored by `a1_autograder.py`)

| ID | Item | Marks | Check |
|---|---|---|---|
| G0 | Notebook executes end-to-end, no errors | 6 | all cells run clean |
| G1 | Three artefacts: metadata valid, domains distinct | 6 | `META_1..3` fields present; URLs well-formed; `data_status` valid; three **distinct** domains |
| G2 | Data provenance ×3 | 9 | each `data_n` loads; ≥ 6 rows × ≥ 2 columns; no empty columns; reconstruction note ≥ 30 words when reconstructed |
| G3 | Redesign mechanics ×3 | 15 | each redesign returns its Axes; three **distinct** Vocabulary categories, all valid; bar-family charts include a zero baseline; every chart titled with ≥ 15 characters |
| G4 | Claim-audit structure (primary artefact) | 14 | interpretation ≥ 400 chars from the supplied prompt; ≥ 6 claims; every label from the four-way taxonomy; ≥ 1 `supported`, ≥ 1 `plausible but unverified`, ≥ 1 `unsupported` **or** `contradicted`; an executable, non-empty probe for every `supported`/`contradicted` claim |
| G5 | Critiques + Decision Record structure | 6 | full 9-field primary critique 5–150 words each; compact critiques 2–3 complete; all 9 Decision Record fields, defence fields ≥ 10 words; `WHY_2`/`WHY_3` ≥ 10 words |
| G6 | Five-question AI disclosure | 4 | all 5 answers completed, none placeholder |

### Human-marked (40 marks, anchored 0/1/2 per item — target 5 minutes per student)

Markers read the autograder report first, then judge only these five items.

| ID | Item (weight ×) | 0 | 1 | 2 |
|---|---|---|---|---|
| H1 | Critique insight — primary critique (×5) | Restates the chart | Correctly identifies the claim and one real omission | Also separates *directly visible* from *interpretation*, names the framing device, and the repaired caption actually repairs |
| H2 | Reconstruction fidelity, across artefacts (×2.5) | Data unrelated to the original's quantities | Plausible magnitudes and units | Matches the original's visible values, or deviations explicitly disclosed |
| H3 | Decision Record + supporting defences (×5) | No argument, or category labels only | Correct task category with a generic justification | Ties audience → task → channel precision; the rejected alternative is real and the reason specific |
| H4 | Redesign craft, across the three (×5) | Unreadable or misleading | Honest defaults, readable | Titles state findings; scales honest; labels carry the argument |
| H5 | Audit judgement (×2.5) | Classifications mostly wrong | Right labels, thin probes | Probes genuinely discriminate — a `contradicted` probe could have exonerated the claim; `plausible but unverified` used precisely, not as a dodge |

**Marker workflow:** run `python a1_autograder.py <notebook>` (or batch mode on
a folder), open the generated report beside the notebook, score H1–H5 on the
anchors, done. The report surfaces the redesigns, the claims table, and word
counts so the human never hunts through cells.

### Process requirements (not marked, but gates)

- Part A supervised draft handed in during the Dashboards-session window (paper or
  photo). Missing draft → H1 capped at 1.
- Three artefact choices (and the primary) recorded by Monday 10 August;
  approval recorded for any bring-your-own.
- One resubmission permitted for G0 failures, capped at 80% overall.

## What good looks like

A strong A1 reads like the class notebooks: the critique names the claim in
one sentence and the repaired caption says what the original's should have
said; the Decision Record argues from the reader's task rather than from
taste, and its rejected alternative is one you genuinely considered; the
reconstruction note is boringly specific; at least one probe shows a
fluent-sounding claim to be `contradicted`; and the disclosure says exactly
what the assistant drafted, what you rejected, and how you caught its
mistakes.
