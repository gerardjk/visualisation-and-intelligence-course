# A1. Reading Claims and Designing Alternatives

| | |
|---|---|
| **Weight** | 30% of the subject · individual |
| **Covers** | Sessions 1-3 |
| **Released** | August 8 |
| **Supervised component** | 25-minute AI-restricted window in the fourth live session · Thursday 27 August 2026 |
| **Due** | **Friday 28 August 2026, 11:59pm** (Sydney time) |
| **Submit** | One ZIP: `A1_template.ipynb`, the three supplied datasets in the `data/` folder, and the three supplied chart images renamed `original_chart_1.png` to `original_chart_3.png` |

## The task

You will take **three sourced chart artefacts from the released pool, from
three different domains**, and work them through the course pipeline: *see* what each
claims, develop an alternative view with the Visual Vocabulary, and *verify* a machine's
interpretation of the data. For **each artefact**, complete a full 9-field
critique, an alternative view, a full Chart Choice Decision Record, and a claim
audit. Artefact 1 is the **primary artefact**: the one whose critique is
completed in the supervised, AI-restricted window. That supervised critique is
the only requirement that differs across the three.

- **Part A. Seeing (the critiques).** For each artefact, complete
  the full 9-field critique: main claim; audience; visual task; directly
  visible; interpretation rather than observation; what is omitted; what
  misleads; what needs verifying; and a repaired caption. For artefact 1,
  address all nine fields by hand in the supervised, AI-restricted window on
  27 August. Transcribe and edit that critique for clarity without AI in the
  notebook's `critique_1` cell. Complete `critique_2` and `critique_3` outside
  the supervised component.

  **Critique field guide:** *main claim* is the one-sentence message; *audience*
  is the intended reader; *visual task* is what that reader must do (such as
  compare, rank, locate or track change); *directly visible* is literally
  encoded in marks, labels and scales; *interpretation rather than observation*
  is invited but not directly shown; *what is omitted* is missing data, context,
  uncertainty or comparison; *what misleads* considers selection, encoding and
  framing—including title, caption, annotation and baseline; *what needs
  verifying* identifies a source, calculation or inference to check; and the
  *repaired caption* states the supported finding and its important limit.
- **Part B. Choosing (the alternative views).** For each artefact, use the
  supplied source-data extract and state a claim that can be supported by that
  data. Create an alternative view designed to communicate that claim. Across
  the three artefacts, the alternatives must use valid Visual Vocabulary
  categories and represent **at least two different categories**. If you use
  the same category more than once, explain in each Decision Record why it is
  the best fit for that artefact's claim. For each one, explain the differences between your
  design and the published original: what your design makes easier to see,
  what it makes harder to see, and how those differences follow from your
  stated claim. Complete the full **Chart Choice Decision Record** for each
  artefact (`decision_record_1` to `decision_record_3`).

  **Decision Record field guide:** identify the intended audience, the question
  they need answered, the decision supported, the Visual Vocabulary category,
  the required comparison and the selected chart form. Explain why the form
  fits, name one genuine alternative, and give a specific reason for rejecting
  it.
- **Part C. Verifying (three claim audits).** Generate an interpretation of
  each dataset using the **supplied prompt**
  (verbatim, in the template).
  Classify **every claim** with the four-way taxonomy from the Seeing Data lab:

  | Label | Meaning |
  |---|---|
  | `supported` | the data directly backs it, attach an evidence probe |
  | `plausible but unverified` | sounds right; this dataset cannot settle it |
  | `unsupported` | asserted with no evidence in this data either way |
  | `contradicted` | the data shows otherwise, attach an evidence probe |

  Probes are zero-argument functions returning the evidence (a filtered or
  aggregated DataFrame/Series): required for every `supported` and
  `contradicted` claim. Each audit must contain at least one claim that can be
  tested with a probe; do not manufacture other claim types simply to fill a
  quota. Finish with the five-question AI disclosure.

  Each claim is a short paraphrase used as the matching key in both the
  classification dictionary and, when required, the probe dictionary.

## Your artefacts

Choose **three artefacts from the released pool, from three different
domains**. Each of the twelve entries contains a published or source-linked
chart image, a tidy extract of corresponding source data, a data dictionary,
and a provenance sheet. The approved printable chart-card examples are the
only course-reproduction exception. Use the supplied extract for analysis;
do not transcribe values from the image. Choose your primary before the
supervised session and complete the data preparation, alternative view and
other preparation in advance. On 27 August, record its pool ID on the supervised
sheet. The pool ID entered for artefact 1 in the notebook—for example,
`POOL-03`—must match the pool ID written on that sheet. Two
students may study the same source chart, but every submission must be
individual and independently produced.

Use the following canonical domain labels exactly in `META_n`:

| Pool ID | Domain | Pool ID | Domain |
|---|---|---|---|
| `POOL-01` | climate science | `POOL-07` | economics |
| `POOL-02` | public health | `POOL-08` | ecology |
| `POOL-03` | astronomy | `POOL-09` | astronomy |
| `POOL-04` | wellbeing | `POOL-10` | energy |
| `POOL-05` | economics | `POOL-11` | geophysics |
| `POOL-06` | energy | `POOL-12` | transportation |

**Known source limitations.** `POOL-04`'s chart card shows ranks 1–48 while
the supplied source contains all 143 ranked countries and does not contain
the simultaneous rank intervals drawn in the chart. In `POOL-06`, a few
published Sankey component labels do not add exactly to the displayed node
totals; treat this as a documented source-chart limitation, not as a student
calculation error. `POOL-12` contains undirected historical airport-pair
records: its two endpoints are alphabetically ordered, and
`airline_record_count` is neither passenger nor flight volume. The individual
provenance sheets repeat these details.

**Background research and domain knowledge.** The chart, source data and pool
notes are starting points, not a complete package of everything you may need.
Answering some questions well may require modest background reading about the
topic, measures and context represented in the visualisation. You are not
expected to become a domain expert, but you should learn enough to engage
intelligently with the chart's claims, assumptions and limitations. You may
use web search, library resources, reports and other credible sources for this
purpose. If you use an AI system to locate or explain background information,
independently verify its factual claims against credible sources. Keep a record
of the sources that inform your analysis and cite them where relevant.
You should also search for other visualisations of the same or closely related
data to see how other designers have framed, filtered and encoded it and to
develop ideas for your own alternative. Do not copy a design. If another
visualisation materially influences your choices, identify it briefly in the
relevant Decision Record—normally under `why_it_fits` or
`reason_for_rejection`—and provide a working URL. A separate reference list is
not required.
Background research should support your own analysis of the chart; it does not
replace close examination of the visualisation and its data.

**Data-use rule.** Copy the supplied CSV for each chosen artefact into your
submission's `data/` folder, rename it with its pool ID, and load that filename
in `data_n`. Copy the publisher, publication value and source URL from the
provenance sheet into the corresponding identifying-information block
(`META_n`). Keep `data_n` as the unchanged DataFrame loaded from that exact
file. You may reshape, filter or derive separately named variables in the
notebook, but must preserve the supplied source columns and document every
transformation. Do not add values inferred
from the image or present derived values as source measurements. Data handling
and disclosure are judged under H2.

**Reconstruction limit.** The supplied extract may not reproduce every detail
of the published original. Establish which components are supported by the
supplied fields and which depend on unavailable data, transformations,
modelling, annotations or design assets. Use this judgement when critiquing the
original and explaining your alternative.

**Copyright note.** Include only the chart image needed for criticism and
review, cite its publisher, creator (where known), date and source URL, and do
not republish the assessment beyond the subject site. Follow any additional
UTS library or copyright guidance supplied with the task.

## AI policy

Part A's primary critique is drafted AI-free in the supervised window and may
be edited for clarity without AI after transcription. An assistant may be used
for Part B's coding and alternative-view work; you remain responsible for checking and
accepting or rejecting its output. Part C requires three assistant-generated
interpretations. Report your use or non-use of AI accurately. False or
misleading disclosure is an academic-integrity issue.

## Submission requirements

The template notebook contains a set of required named variables and functions
for each artefact. These include the identifying-information blocks (`META_1`,
`META_2`, and `META_3`), critiques (`critique_1` to `critique_3`), datasets
(`data_1` to `data_3`), alternative views (`redesign_1` to `redesign_3`),
Decision Records, claim audits, evidence probes, and the AI disclosure. **Do not
rename these items**, because the autograder checks them directly. The
autograder executes your notebook top-to-bottom on a clean machine. **Run the
self-check cell before submitting**: it runs the
marker's G1–G6 checks (54 marks). G0's remaining 6 marks are awarded only
after a clean top-to-bottom execution on the marking system. An execution error
loses the G0 marks and may also prevent checks that depend on the affected code;
it does not automatically erase otherwise verifiable marks. If an execution
failure prevents fair assessment, the marker may allow one technical
resubmission within 48 hours of notification. Only changes needed to restore
execution are permitted; the analytical content must remain unchanged.

---

## Rubric, 100 marks (worth 30% of the subject)

The rubric maximum is the sum of the criterion maxima: 60 automated marks plus
40 human-marked marks equals 100. Canvas records both the assignment and rubric
out of 100. The Assignment 1 group contributes 30% of the subject, so no manual
score conversion is required.

### Automated (60 marks, scored by `a1_autograder.py`)

| ID | Item | Marks | Check |
|---|---|---|---|
| G0 | Notebook executes end-to-end, no errors | 6 | all cells run clean |
| G1 | Three artefacts: identity and files valid | 6 | `STUDENT_ID` and all identifying-information blocks complete; three distinct IDs from `POOL-01..12`; the corresponding canonical domains are distinct; URLs and `data_status` valid; each supplied original chart matches its selected pool item |
| G2 | Data provenance ×3 | 9 | each exact supplied `data/POOL-XX_source_data.csv` loads unchanged into `data_n`; ≥ 6 rows × ≥ 2 columns; no empty columns; source and transformations documented |
| G3 | Alternative-view mechanics ×3 | 15 | each alternative view (`redesign_n`) returns its Axes; all categories are valid and at least two different Vocabulary categories are represented across the three artefacts; bar-family charts include a zero baseline; every chart title has at least 15 characters |
| G4 | Claim-audit structure ×3 | 14 | for each artefact: a 150–250-word interpretation from the supplied prompt; ≥ 4 validly labelled claims; at least one `supported` or `contradicted` claim; an executable, non-empty probe for every such claim |
| G5 | Critiques + Decision Records ×3 | 6 | all three 9-field critiques and all three 9-field Decision Records are complete; each `vocabulary_category` matches `CATEGORY_n` |
| G6 | Five-question AI disclosure | 4 | all 5 answers completed; each answer has at least 3 words and is not a placeholder |

### Human-marked (40 marks, anchored 0/1/2 per item)

| ID | Item (weight ×) | 0 | 1 | 2 |
|---|---|---|---|---|
| H1 | Critique insight across three (×5) | Restates the charts | Correctly identifies claims and real omissions | Also separates *directly visible* from *interpretation*, explains how title, caption, annotation or baseline frames the claim where relevant, and the repaired captions actually repair |
| H2 | Data handling, across artefacts (×2.5) | Source data are misread or transformations are undisclosed | Units and transformations are mostly correct | Source fields are preserved; transformations are correct, reproducible and fully disclosed |
| H3 | Decision Records across three (×5) | No argument, or category labels only | Correct task categories with generic justifications | Ties audience → task → channel precision; rejected alternatives are real and reasons specific |
| H4 | Alternative-view craft, across the three (×5) | Unreadable or misleading | Honest defaults, readable | Titles state findings; scales honest; labels carry the argument |
| H5 | Audit judgement across three (×2.5) | Classifications mostly wrong | Labels mostly appropriate, but probes are weak | Labels distinguish evidence from plausibility precisely; every required probe directly tests the claim |

### Process requirements (not marked, but gates)

- Part A supervised notes handed in during the 27 August window. Missing notes
  → H1 capped at 0.
- The pool ID entered for artefact 1 in the notebook must match the pool ID
  written on the supervised sheet (27 August).
