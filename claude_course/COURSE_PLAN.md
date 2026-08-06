# Visualisation and Intelligence — Six-Class Plan

**Course:** 36104 Data Visualisation and Narratives
**Format:** six 3-hour classes, each combining lecture, hands-on notebook work, and studio critique.
**Workflow taught throughout:**

```text
User story → Visual task → Visual form → Interaction → Deployment → Disclosure → Review → Defence
```

The FT Visual Vocabulary is the shared language for visual-task classification and chart selection. Every class pairs a slide deck with a Copilot-friendly Jupyter notebook: students work in VS Code with an AI assistant, and every generated artefact must pass the verification steps built into the notebook before it counts.

---

## The six classes

| # | Class | Core question | Studio output | Assessment attached |
|---|-------|---------------|---------------|---------------------|
| 1 | **Seeing Data — Visualisation, Intelligence, and Interpretation** | How do charts create meaning? | Critique 1: one human-made chart vs one AI-generated interpretation | Diagnostic quiz; Critique 1 draft |
| 2 | **Choosing Visual Forms — Encoding, Tidy Data, and the Visual Vocabulary** | What visual task are we performing? | Visual Vocabulary sort; redesign a weak chart three ways | Quiz; Critique 2 draft |
| 3 | **Dashboards, Personas, and User Stories — Tableau Public** | Who is this for and what do they need to do? | Tableau dashboard build and persona defence | Quiz; dashboard submission (A3) |
| 4 | **From Streamlit Prototype to Public Data Product** | How does an app become a trustworthy public artefact? | Build local Streamlit MVP, deploy it, add disclosure, test user stories | Two-part quiz; group plan; public-product checkpoint (A4) |
| 5 | **Web Visualisation Studio — Maps, Flows, Animation, 3D, and JavaScript Literacy** | When is a specialised form worth its cost? | Specialised visualisation decision and optional extension | Quiz; specialised decision draft |
| 6 | **Responsible Interpretation, Quality Review, Present and Defend** | Does the work survive scrutiny? | Peer quality review, revision, group presentation, individual oral defence | Quality review (A6); Critique 3; final app (A5); oral defence (A7) |

### Why this shape

- Classes 1 and 2 stay separate: they are the intellectual spine (interpretation, then encoding), each with a full studio, and the rest of the course leans on them.
- The Streamlit build and its deployment/disclosure are one arc, so they share Class 4: an hour of build, an hour of deploy-and-disclose, an hour of studio.
- The web studio keeps its own class. It is literacy plus optional extension — it must not become a JavaScript assignment.
- Quality review and defence are both "step back and judge the work" sessions, so they share Class 6: review and revise in the first half, present and defend in the second.

### Timing consequences

- Groups form by the end of Class 3.
- A local Streamlit prototype and a deployed app both land in Class 4; the deployed-app deadline is one session earlier than in the original design, so the Class 5 studio doubles as deployment triage for groups that are behind.
- Class 6 is long on assessment: peer review runs in hour 1, revisions in hour 2, presentations and defences in hour 3 (with overflow scheduled outside class if the cohort is large).

---

## Standard class rhythm (3 hours)

| Time | Segment | Purpose |
|---|---|---|
| 0:00–0:15 | Opening example | Ground the class in a concrete visual artefact |
| 0:15–1:00 | Concept | Key ideas and vocabulary, from the slide deck |
| 1:00–2:00 | Notebook | Guided, Copilot-assisted exercises with built-in verification |
| 2:00–2:45 | Studio | Critique, repair, or milestone work |
| 2:45–3:00 | Exit ticket | One decision made, one risk noticed, one thing to verify |

## Notebook design principles (Copilot-friendly)

Every class notebook follows the same contract:

1. **Context before code.** Each exercise starts with a markdown cell that states the task, the data, and the acceptance criteria — enough context that an AI assistant can generate a useful first draft.
2. **Scaffolded cells.** Code cells contain function signatures, typed docstrings, and `# TODO` comments written as prompts. Students may hand-write or accept AI completions.
3. **Verification is not optional.** Every exercise ends with an assertion cell or a "check yourself" cell. Generated code that fails the check is a teaching moment, not a submission.
4. **Disclosure built in.** Each notebook ends with the course AI-disclosure block: what the assistant contributed and how it was checked.

## Materials layout

```text
claude_course/
  COURSE_PLAN.md              ← this file
  scripts/                    ← python-pptx deck builders (regenerable)
  classes/
    01-seeing-data/
    02-visual-forms/
    03-tableau-dashboards/    (to build)
    04-streamlit-public-product/  (to build)
    05-web-visualisation-studio/  (to build)
    06-review-present-defend/     (to build)
```

Each class folder contains: `lesson_plan.md`, the slide deck (`.pptx`), the activity brief, and the class notebook (`.ipynb`). Decks are generated by the scripts in `scripts/` and embed figures from the atlas book (`quarto-book/_book/atlas_files/figure-html/`).

## Assessment arc

Three assessments, one arc: repair someone else's chart alone → build for a
user alone → tell a story together and defend it. In-class quizzes remain
formative (diagnostic, ungraded) — they calibrate, they don't count.

- **A1 — Critique and Repair** (individual, ~20%, due Class 3). One published
  chart worked through the Classes 1–2 pipeline: supervised critique, data
  reconstruction, best-form redesign with defence plus two alternatives, and
  an audited AI interpretation. Fully specified in
  `assessments/A1-critique-and-repair/` — brief, artefact pool, template
  notebook, and an autograder that scores 60 of 100 marks and generates the
  marker report for the five anchored human items.
- **A2 — Build for a user** (individual, spanning Classes 3–5): dashboard or
  app for a persona with user stories, deployment, and disclosure. Brief to
  be drafted when Classes 3–5 are built.
- **A3 — Tell and defend** (group build + individual oral defence, Class 6).
  Brief to be drafted with Class 6.
