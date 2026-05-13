# Instructor Guide

## What this package is

This repository is designed to be used as a GitHub course repository, LMS source folder, or teaching-team handover package. It contains the course outline, assessment briefs, templates, lecture plans, quiz item examples, a starter Streamlit app, and a lightweight autograder.

## Setup before semester

1. Decide whether students will use Canvas, Moodle, Inspera, Gradescope, or another system for quizzes.
2. Choose approved generative AI tools under institutional policy.
3. Confirm whether Tableau Public is permitted for student use.
4. Confirm public-data policy for Streamlit Community Cloud deployment.
5. Prepare one common dataset for the Tableau checkpoint.
6. Prepare a curated dataset list for group Streamlit projects.
7. Create groups by Week 3.
8. Decide whether oral defences occur in lecture, tutorials, or parallel online sessions.

## Minimum technology assumptions

Students need:

- Tableau Public account.
- Python 3.10+.
- GitHub account.
- GitHub Desktop or equivalent.
- Streamlit Community Cloud access.
- Access to an approved intelligent tool.

## Large cohort model

The package is designed for large classes by automating what can be automated and keeping human assessment focused on judgement.

| Component | Automation strategy |
|---|---|
| Weekly quizzes | LMS auto-graded item bank |
| Tableau checkpoint | structured form + sampling moderation |
| Public Data Product Checkpoint | repository autograder |
| Group app | rubric + automated scaffold checks |
| Visualisation Quality Review | structured form + staff marking |
| Oral defence | short standardised question bank |

## Recommended staffing

For cohorts above 150, run studio and oral defence in tutorials. Use a standard marker guide and question bank. Moderate a sample of oral recordings where institutional policy permits.

## Week 5 teaching note

Do not teach data loading, caching, and deployment as disconnected engineering tasks. Frame them as conditions of public trust:

- If the app fails to load, the visualisation fails as communication.
- If the app is slow, users abandon the story.
- If empty filters show blank charts, users may misinterpret missingness.
- If data provenance is unclear, users cannot verify claims.
- If intelligent-tool use is hidden, users cannot judge reliability.

## Week 6 teaching note

Do not turn Week 6 into a JavaScript assignment. The intended outcome is literacy:

- students can explain what JavaScript does in web visualisation;
- students can recognise D3, Vega-Lite, Plotly.js, Leaflet, deck.gl, and Three.js use cases;
- students can decide whether Streamlit/Altair is sufficient or whether a web-native visualisation is justified.

## Oral defence logistics

Use two or three questions per student. The questions should sample across:

- contribution,
- data transformation,
- code or interaction,
- visual vocabulary choice,
- limitations,
- intelligent-tool use,
- quality review response.

Example:

```text
You classified your main chart as change over time. What would you change if the user story were about ranking instead?
```

## Integrity design

The course does not rely on AI-detection software. It uses:

- supervised critique,
- AI Provenance Matrix,
- Data and AI Disclosure,
- peer quality review,
- individual oral defence.
