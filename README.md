# Visualisation and Intelligence

**Narrative, Critique, and Analytics**

This repository is a complete teaching package for an 8-week course in data visualisation. It combines visual reasoning, the FT Visual Vocabulary, Tableau Public, Streamlit, user stories, deployment, web visualisation literacy, responsible interpretation, and AI-aware provenance.

The course is designed for large cohorts. It uses auto-graded quizzes and technical checkpoints where possible, while preserving human assessment for judgement, critique, and individual oral defence.

## Course spine

| Week | Title | Core question |
|---|---|---|
| 1 | Seeing Data: Visualisation, Intelligence, and Interpretation | How do charts create meaning? |
| 2 | Choosing Visual Forms: Encoding, Tidy Data, and the Visual Vocabulary | What visual task are we performing? |
| 3 | Dashboards, Personas, and User Stories: Tableau Public | Who is this for and what do they need to do? |
| 4 | Interactive Data Apps with Streamlit | How does a user interact with the data? |
| 5 | From Prototype to Public Data Product | Can someone else open, understand, trust, and use it? |
| 6 | Web Visualisation Studio: Maps, Flows, Animation, 3D, and JavaScript Literacy | When do we need specialised or web-native visualisation? |
| 7 | Responsible Interpretation and Visualisation Quality Review | Is the interpretation justified, accessible, and responsible? |
| 8 | Present and Defend: Visual Intelligence in Practice | Can students defend the whole product? |

## What is included

```text
visualisation-and-intelligence-course/
├── COURSE_OVERVIEW.md
├── COURSE_OUTLINE.md
├── SCHEDULE.md
├── INSTRUCTOR_GUIDE.md
├── STUDENT_QUICKSTART.md
├── assignments/
├── autograder/
├── datasets/
├── docs/
├── examples/
├── lectures/
├── quizzes/
├── starter_app/
└── templates/
```

## Quick start for instructors

```bash
git init
git add .
git commit -m "Initial course package"
```

Run the starter app locally:

```bash
cd starter_app
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Run the public data product checkpoint autograder:

```bash
python autograder/check_public_data_product.py starter_app
```

The starter app is intentionally built around a synthetic dataset. Students should replace it with an approved public dataset for assessment.

## Pedagogical design

The course is built around a repeated professional routine:

> identify the user story, choose the visual task, build the artefact, deploy it, disclose the data and intelligent-tool use, review the interpretation, repair weaknesses, and defend the judgement.

The course uses a two-lane assessment model:

- **Lane 1: authenticated individual understanding** — supervised critique and oral defence.
- **Lane 2: AI-integrated professional production** — group app, provenance, disclosure, and quality review.

## Key conventions

- Use **Data and AI Disclosure**, not “Nutrition Label,” in student-facing materials.
- Use the **FT Visual Vocabulary** as the recurring chart-choice scaffold.
- Use **user stories** to connect audience, task, chart choice, and app features.
- Treat deployment and caching as conditions of public trust, not merely engineering chores.
- Treat JavaScript as literacy and optional extension, not as a second full technical spine.


## Quarto website and book

This repo is now Quarto-ready.

Preview the course website:

```bash
quarto preview
```

Render the course website:

```bash
quarto render
```

Render the optional book:

```bash
cd book
quarto render
```

Canvas should still be used for graded quizzes, submissions, deadlines, and grades. The Quarto site is the publishing layer for weekly content, code examples, templates, readings, and public course materials.

See `QUARTO_GUIDE.md` for setup and GitHub Pages publishing instructions.
