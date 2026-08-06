# Visualisation and Intelligence — Six-Class Plan (merged)

**Course:** 36104 Data Visualisation and Narratives
**Format:** six 3-hour classes, each combining a concise slide story, a worked
demonstration, Copilot-assisted notebook work, and studio critique.

This plan merges two independently developed drafts (`claude_course/` and
`codex_course/`): the six-class skeleton, assessment anchoring and regenerable
deck pipeline come from the first; the three-tier notebooks, worked
demonstrations, facilitation notes and evidence-of-learning collection come
from the second.

**Workflow taught throughout:**

```text
Question → Evidence → Visual task → Visual form → Interaction →
Deployment → Verification → Disclosure → Review → Defence
```

The FT Visual Vocabulary is the shared language for visual-task classification
and chart selection. Students work in notebooks with an AI assistant available;
every generated artefact must pass the verification steps built into the
notebook before it counts, and significant tool use is disclosed.

---

## The six classes

| # | Class | Core question | Studio output | Feeds assessment |
|---|-------|---------------|---------------|------------------|
| 1 | **Seeing Data — Visualisation, Intelligence, and Interpretation** | How do charts create meaning? | Critique and Repair; Critique 1 (human chart vs AI interpretation) | A1 parts A & C |
| 2 | **Choosing Visual Forms — Encoding, Tidy Data, and the Visual Vocabulary** | What visual task are we performing? | Visual Vocabulary sort; redesign a weak chart three ways; Chart Choice Decision Record | A1 part B |
| 3 | **Dashboards, Personas, and User Stories — Tableau Public** | Who is this for and what do they need to do? | Dashboard plan, prepared dataset, persona defence | A2; A3 groups form |
| 4 | **From Streamlit Prototype to Public Data Product** | How does an app become a trustworthy public artefact? | Local Streamlit MVP, deployment, disclosure, user-story tests | A2 due; A3 proposal |
| 5 | **Web Visualisation Studio — Maps, Flows, Animation, 3D, and JavaScript Literacy** | When is a specialised form worth its cost? | Specialised visualisation decision; deployment triage | A3 build |
| 6 | **Responsible Interpretation, Quality Review, Present and Defend** | Does the work survive scrutiny? | Peer quality review, revision, group presentation, individual defence segment | A3 presentation & portfolio |

### Why this shape

- Classes 1 and 2 stay separate: they are the intellectual spine
  (interpretation, then encoding), each with a full studio, and the rest of the
  course leans on them.
- The Streamlit build and its deployment/disclosure are one arc, so they share
  Class 4: an hour of build, an hour of deploy-and-disclose, an hour of studio.
- The web studio keeps its own class. It is literacy plus optional extension —
  it must not become a JavaScript assignment.
- Quality review and defence are both "step back and judge the work" sessions,
  so they share Class 6: review and revise in the first half, present and
  defend in the second.
- Uncertainty, missingness, accessibility and provenance (a standalone session
  in one draft) are distributed instead: uncertainty and missingness into the
  Class 5 studio, provenance/disclosure/accessibility into Class 4 and the
  Class 6 quality review.

---

## Assessment map (Canvas structure: 30 / 30 / 40)

The official Canvas structure is three assessments. The briefs below are the
current working redesign; weights, types and SILO mappings match the approved
structure.

| Assessment | Weight | Type | AI status | Timing |
|---|---:|---|---|---|
| **A1 — Critique and Repair portfolio** | 30% | Individual | Part A supervised & AI-restricted; Part C AI-integrated with claim audit | Assigned Class 1; due after Class 3 |
| **A2 — User Stories & UX Pivot** (exploratory → explanatory build) | 30% | Individual | Allowed with declaration | Assigned Class 3; due after Class 4 |
| **A3 — The Rise of AI: Data Narrative Studio** | 40% | Group | AI-integrated; provenance matrix, disclosure and revision log required | Proposal after Class 4; presentation and portfolio Class 6 |

**A1 — Critique and Repair.** Each student takes one published chart from a
curated multi-domain pool (news, government, climate, health, housing, sport,
culture — never the same artefact twice in a tutorial group). Part A: critique —
what the chart shows vs what it claims (supervised studio component). Part B:
repair — rebuild the data in a notebook and redesign the chart three ways, one
Visual Vocabulary task per redesign, with justification. Part C: verification —
an AI assistant interprets the data; every claim is classified supported /
unsupported / unverifiable, with evidence and the disclosure block.

**A2 — User Stories & UX Pivot.** Take an exploratory artefact (Tableau VOTD or
an approved dataset), define a persona and user stories, and build the
explanatory pivot as a Tableau Public dashboard plus a short justification
report. Individual rehearsal of the full persona → user story → task → form
chain before group work begins.

**A3 — The Rise of AI.** Groups build a deployed interactive narrative
(Streamlit or Tableau + GitHub) answering one arguable question inside the
theme (compute vs algorithms, talent flows, energy cost, adoption vs measured
productivity…), on public data (Stanford AI Index, Epoch AI, OWID, arXiv).
Three parts: proposal (10%) → presentation (10%) → final portfolio (20%).
The presentation includes a short per-student defence segment; peer-contribution
scaling applies. Required artefacts: user story map, Visual Vocabulary planning
table, Data & AI Disclosure, AI Provenance Matrix, revision log after quality
review.

### Operational rules (write these into the subject outline)

- "AI-restricted, supervised" means: completed in studio time, assistants off,
  and the conditions stated in the brief.
- Group marks are adjusted by a declared peer-contribution instrument.
- The provenance matrix is defended live: each student picks one row and
  defends the verification performed.

---

## Standard class rhythm (3 hours)

| Time | Segment | Purpose |
|---|---|---|
| 0:00–0:15 | Opening example | Ground the class in a concrete visual artefact (silent reading before explanation) |
| 0:15–0:45 | Concepts | Key ideas and vocabulary, from the slide deck |
| 0:45–1:15 | Worked demonstration | Model one complete analytical or design decision |
| 1:15–1:25 | Break | — |
| 1:25–2:20 | Notebook lab | Copilot-assisted exercises within explicit constraints and verification checks |
| 2:20–2:50 | Studio | Critique, repair, decision record, or milestone work |
| 2:50–3:00 | Exit ticket | One decision made, one risk noticed, one thing to verify |

## Notebook contract (merged)

Three tiers per class: a **lab** notebook (primary, distributed at the start of
the lab), a **starter** notebook (scaffolded intervention for students blocked
by syntax), and an **instructor** notebook (solutions; never distributed before
the related assessment closes).

Every notebook asks students to:

1. **Context before code.** Each exercise starts with a markdown cell stating
   the task, the data and the acceptance criteria — enough context that an AI
   assistant can generate a useful first draft.
2. **Predict before generating.** Students record an expected output before
   prompting or running generated code.
3. **Bounded prompts, retained.** Copilot receives a bounded task with explicit
   requirements; the prompt or a short summary is retained in the notebook.
4. **Verification is not optional.** Every exercise ends with assertion or
   check-yourself cells: row counts, types, missing values, transformations.
   Generated code that fails the check is a teaching moment, not a submission.
5. **Observation vs interpretation.** "The chart shows" is reserved for visible
   evidence; "this suggests" for interpretation.
6. **Explain one generated block.** At least one accepted completion is
   explained in the student's own words.
7. **Disclosure built in.** Each notebook ends with the course AI-disclosure
   block: what the assistant contributed, what was accepted/modified/rejected,
   how it was checked, and what remains unverified.

## Role of the Atlas

The Atlas (`quarto-book/`) is an example library, not a list to cover
exhaustively. Selected entries perform specific teaching jobs:

| Teaching job | Useful entries |
|---|---|
| Show why looking matters | Anscombe's quartet |
| Show a visual causal argument | John Snow's cholera map |
| Introduce the visual grammar | Bertin's visual variables |
| Discuss data governance and boundaries | AIATSIS Map of Indigenous Australia |
| Compare magnitude and distribution | Population pyramid, box plot, Gaussian, power law |
| Compare relationships and trends | Hertzsprung–Russell, Hubble, Keeling, climate stripes |
| Explain grouping and flow | Networks, trees, Sankey and process flow |
| Discuss uncertainty and prediction | Fan chart, ROC curve and confidence intervals |

## Materials layout

```text
merged_course/
  COURSE_PLAN.md              ← this file
  README.md                   ← distribution rules and orientation
  scripts/                    ← python-pptx deck builders (regenerable)
  classes/
    01-seeing-data/
      teaching_plan.md        ← outcomes, run sheet, facilitation, evidence
      slides.md               ← slide-by-slide speaker directions
      instructor_guide.md
      worked_demonstration.md
      <Deck>.pptx             ← generated by scripts/
      notebooks/              ← lab / starter / instructor tiers
      activities/             ← studio briefs and packs
      assets/
    02-visual-forms/          (same pattern)
    03-tableau-dashboards/        (to build)
    04-streamlit-public-product/  (to build)
    05-web-visualisation-studio/  (to build)
    06-review-present-defend/     (to build)
```

Decks are generated by the scripts in `scripts/` and embed figures from the
atlas book (`quarto-book/_book/atlas_files/figure-html/`); build the book
before rebuilding decks.
