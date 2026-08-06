> **SUPERSEDED:** the canonical A1 now lives in
> `merged_course/assessments/A1-critique-and-repair/` — reconciled to the
> merged course conventions (30%, four-way claim taxonomy, Chart Choice
> Decision Record, five-question disclosure). Do not distribute this copy.

# A1 — Critique and Repair

**Individual assessment · covers Classes 1–2 · suggested weight 20%**
**Due:** start of Class 3. **Submit:** one completed `A1_template.ipynb`, your data file(s) in `data/`, and a PNG/screenshot of the original chart.

## The task

You will take one published chart from the wild and work it through the course
pipeline: *see* what it claims, *repair* it with the Visual Vocabulary, and
*verify* a machine's interpretation of its data.

- **Part A — Seeing (the critique).** What does the chart show, and what does
  it claim? Selection, encoding, framing, omission — in course vocabulary,
  using the "the chart shows / this suggests" discipline. **Drafted in the
  Class 2 studio under supervision, AI-restricted**; you then transcribe your
  studio draft into the notebook's `critique` cell.
- **Part B — Choosing (the repair).** Obtain or faithfully reconstruct the
  chart's underlying data. Then produce **three redesigns**: your *best form*
  — the chart the original should have been, with a defence — plus **two
  alternatives serving different Visual Vocabulary tasks**. The defence is
  what is marked; the alternatives prove you considered the space.
- **Part C — Verifying (the claim audit).** Generate an interpretation of
  your dataset using the **supplied prompt** (verbatim, in the template).
  Classify every claim as `supported` / `unsupported` / `unverifiable`, and
  attach an executable probe for every claim you say the data can settle.
  Complete the disclosure block.

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

Part A is drafted AI-free in studio. Parts B and C expect assistant use — the
notebook contract is the same as class: docstrings first, accept or reject
completions, and nothing counts until the checks pass. The disclosure block is
assessed; "no AI was used" in a notebook full of idiomatic generated code will
be treated as a disclosure failure, not a virtue.

## Submission contract (read this twice)

The template notebook defines named variables and functions
(`META`, `critique`, `original_data`, `redesign_best` … `disclosure`). The
autograder executes your notebook top-to-bottom on a clean machine and inspects
those names. **Run the self-check cell before submitting** — it is the same
code the marker runs. A notebook that does not execute end-to-end scores 0 on
the automated items until resubmitted (one resubmission, capped at 80%).

---

## Rubric — 100 marks

### Automated (60 marks, scored by `a1_autograder.py`)

| ID | Item | Marks | Check |
|---|---|---|---|
| G0 | Notebook executes end-to-end, no errors | 6 | all cells run clean |
| G1 | Metadata complete and valid | 6 | `META` fields present; URL well-formed; `data_status` ∈ {obtained, reconstructed} |
| G2 | Data provenance | 10 | `original_data` loads; ≥ 12 rows × ≥ 2 columns; no empty columns; reconstruction note ≥ 30 words when reconstructed |
| G3 | Redesign mechanics | 16 | three Axes returned; three **distinct** Vocabulary categories, all valid; bar-family charts include a zero baseline; every chart titled with ≥ 15 characters |
| G4 | Claim-audit structure | 14 | interpretation ≥ 400 chars from the supplied prompt; ≥ 6 claims; every label valid; ≥ 1 claim in **each** of the three categories; an executable, non-empty probe for every supported/unsupported claim |
| G5 | Critique structure | 4 | all 8 critique fields present, each 10–150 words |
| G6 | Disclosure | 4 | all 4 fields completed, none placeholder |

### Human-marked (40 marks, anchored 0/1/2 per item — target 5 minutes per student)

Markers read the autograder report first, then judge only these five items.
Score 0, 1 or 2 per item; multiply by the item weight.

| ID | Item (weight ×) | 0 | 1 | 2 |
|---|---|---|---|---|
| H1 | Critique insight (×5) | Restates the chart | Correctly identifies the claim and one real omission | Also separates *shows* from *suggests* and names the framing device, in course vocabulary |
| H2 | Reconstruction fidelity (×2.5) | Data unrelated to the original's quantities | Plausible magnitudes and units | Matches the original's visible values, or deviations explicitly disclosed |
| H3 | Best-form defence (×5) | No argument, or category label only | Correct task category with a generic justification | Ties the reader's task → channel precision → audience; names what the original owed its readers |
| H4 | Redesign craft (×5) | Unreadable or misleading | Honest defaults, readable | Titles state findings; scales honest; labels carry the argument |
| H5 | Audit judgement (×2.5) | Classifications mostly wrong | Right labels, thin probes | Probes genuinely discriminate — they could have falsified the claim |

**Marker workflow:** run `python a1_autograder.py <notebook>` (or batch mode on
a folder), open the generated report beside the notebook, score H1–H5 on the
anchors, done. The report surfaces the three redesign images, the claims table,
and word counts so the human never hunts through cells.

### Process requirements (not marked, but gates)

- Part A studio draft handed in during Class 2 (photo or paper). Missing draft
  → H1 capped at 1.
- Artefact unique in tutorial; approval recorded for bring-your-own.
- One resubmission permitted for G0 failures, capped at 80% overall.

## What good looks like

A strong A1 reads like the Class 1–2 notebooks: the critique names the claim
in one sentence, the best-form defence argues from the reader's task rather
than from taste, the reconstruction note is boringly specific, at least one
probe *fails to support* a fluent-sounding claim, and the disclosure block
says exactly what the assistant drafted and how you caught its mistakes.
