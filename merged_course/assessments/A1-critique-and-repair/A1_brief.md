# A1 — Critique and Repair

**Individual assessment · 30% · covers Classes 1–2**
**Assigned:** Class 1 (artefact allocated). **Supervised component:** 25-minute
window at the start of the Class 3 studio. **Due:** end of the week after
Class 3. **Submit:** one completed `A1_template.ipynb`, your data file(s) in
`data/`, and a PNG/screenshot of the original chart.

## The task

You will take one published chart from the wild and work it through the course
pipeline: *see* what it claims, *repair* it with the Visual Vocabulary, and
*verify* a machine's interpretation of its data. Classes 1 and 2 rehearse
every part of this: the Class 1 studio (Critique and Repair sheet, Critique 1)
rehearses Parts A and C; the Class 2 studio (Redesign ×3, Chart Choice
Decision Record) rehearses Part B.

- **Part A — Seeing (the critique).** What does the chart show, and what does
  it claim? Selection, encoding, framing, omission — keeping the discipline
  from Class 1: *directly visible* vs *interpretation rather than
  observation*. Ends with a repaired caption. **Drafted by hand in the
  supervised, AI-restricted window in Class 3**, then transcribed into the
  notebook's `critique` cell.
- **Part B — Choosing (the repair).** Obtain or faithfully reconstruct the
  chart's underlying data. Produce **three redesigns**: your *best form* —
  the chart the original should have been — plus **two alternatives serving
  different Visual Vocabulary tasks**. Defend the best form with a completed
  **Chart Choice Decision Record** (the same form as the Class 2 studio,
  including the rejected alternative and the specific reason). The Decision
  Record is what is marked; the alternatives prove you considered the space.
- **Part C — Verifying (the claim audit).** Generate an interpretation of
  your dataset using the **supplied prompt** (verbatim, in the template).
  Classify **every claim** with the four-way taxonomy from the Class 1 lab:

  | Label | Meaning |
  |---|---|
  | `supported` | the data directly backs it — attach an evidence probe |
  | `plausible but unverified` | sounds right; this dataset cannot settle it |
  | `unsupported` | asserted with no evidence in this data either way |
  | `contradicted` | the data shows otherwise — attach an evidence probe |

  Probes are zero-argument functions returning the evidence (a filtered or
  aggregated DataFrame/Series) — required for every `supported` and
  `contradicted` claim. Finish with the five-question AI disclosure.

## Your artefact

You will be assigned one artefact from the pool (`artefact_pool.md`), unique
within your tutorial. Alternatively, propose your own found-in-the-wild chart
by the end of Class 1: a real published chart, a named publisher and date, and
an obtainable or reasonably reconstructable data source. Approval is required
— the approval conversation is itself a provenance exercise.

**Data rule.** If the exact data is not published, reconstruct it faithfully
(digitise, or synthesise to match the chart's visible quantities) and say so:
set `data_status = "reconstructed"` and write the reconstruction note. This is
the atlas book's own method — representative data, never passed off as the
original measurement. Undisclosed reconstruction is an academic-integrity
issue; disclosed reconstruction is full marks.

**Copyright note.** Including the original chart image in your submission for
the purpose of criticism and review is permitted use. Cite publisher and date.

## AI policy

Part A is drafted AI-free in the supervised window. Parts B and C expect
assistant use — the notebook contract is the same as class: docstrings first,
accept or reject completions, and nothing counts until the checks pass. The
disclosure block is assessed; "no AI was used" in a notebook full of idiomatic
generated code will be treated as a disclosure failure, not a virtue.

## Submission contract (read this twice)

The template notebook defines named variables and functions
(`META`, `critique`, `original_data`, `redesign_best` … `disclosure`). The
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
| G1 | Metadata complete and valid | 6 | `META` fields present; URL well-formed; `data_status` ∈ {obtained, reconstructed} |
| G2 | Data provenance | 10 | `original_data` loads; ≥ 12 rows × ≥ 2 columns; no empty columns; reconstruction note ≥ 30 words when reconstructed |
| G3 | Redesign mechanics | 16 | three Axes returned; three **distinct** Vocabulary categories, all valid; bar-family charts include a zero baseline; every chart titled with ≥ 15 characters |
| G4 | Claim-audit structure | 14 | interpretation ≥ 400 chars from the supplied prompt; ≥ 6 claims; every label from the four-way taxonomy; ≥ 1 `supported`, ≥ 1 `plausible but unverified`, ≥ 1 `unsupported` **or** `contradicted`; an executable, non-empty probe for every `supported`/`contradicted` claim |
| G5 | Critique + Decision Record structure | 4 | all 9 critique fields (incl. repaired caption) 5–150 words; all 9 Decision Record fields present, defence fields ≥ 10 words |
| G6 | Five-question AI disclosure | 4 | all 5 answers completed, none placeholder |

### Human-marked (40 marks, anchored 0/1/2 per item — target 5 minutes per student)

Markers read the autograder report first, then judge only these five items.

| ID | Item (weight ×) | 0 | 1 | 2 |
|---|---|---|---|---|
| H1 | Critique insight (×5) | Restates the chart | Correctly identifies the claim and one real omission | Also separates *directly visible* from *interpretation*, names the framing device, and the repaired caption actually repairs |
| H2 | Reconstruction fidelity (×2.5) | Data unrelated to the original's quantities | Plausible magnitudes and units | Matches the original's visible values, or deviations explicitly disclosed |
| H3 | Decision Record defence (×5) | No argument, or category label only | Correct task category with a generic justification | Ties audience → task → channel precision; the rejected alternative is real and the reason specific |
| H4 | Redesign craft (×5) | Unreadable or misleading | Honest defaults, readable | Titles state findings; scales honest; labels carry the argument |
| H5 | Audit judgement (×2.5) | Classifications mostly wrong | Right labels, thin probes | Probes genuinely discriminate — a `contradicted` probe could have exonerated the claim; `plausible but unverified` used precisely, not as a dodge |

**Marker workflow:** run `python a1_autograder.py <notebook>` (or batch mode on
a folder), open the generated report beside the notebook, score H1–H5 on the
anchors, done. The report surfaces the redesigns, the claims table, and word
counts so the human never hunts through cells.

### Process requirements (not marked, but gates)

- Part A supervised draft handed in during the Class 3 window (paper or
  photo). Missing draft → H1 capped at 1.
- Artefact unique in tutorial; approval recorded for bring-your-own.
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
