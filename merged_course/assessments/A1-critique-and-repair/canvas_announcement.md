# Assignment 1 released: Reading Claims and Designing Alternatives

Assignment 1 is available in **Modules → Assessment 1: Reading Claims and Designing Alternatives**.

## Download these three files

1. **A1 brief (read this first)** — the task, AI policy, submission requirements and full rubric.
2. **A1 starter pack** — a ZIP containing `A1_template.ipynb` and `a1_autograder.py`. Unzip it before working. Keep both files together.
3. **A1 artefact pool** — a ZIP containing twelve folders, `POOL-01` to `POOL-12`. Unzip it and choose three artefacts from three different domains.

Each pool folder contains:

- `original_chart.png` — the published or source-linked chart image;
- `source_data.csv` — the supplied data you must use;
- `data_dictionary.md` — field definitions and extraction notes;
- `provenance.md` — publisher, source links, licence and extraction details.

Each folder also holds `entry.md`, `checks.json` and `source_metadata.json` — build and verification records you may read for extra provenance detail but do not need for the assignment.

## Set up your submission

For each chosen artefact:

1. Read its chart, data dictionary and provenance sheet.
2. Copy its `source_data.csv` into a `data` folder beside `A1_template.ipynb` and rename it with the pool ID, for example `POOL-03_source_data.csv`.
3. Update the corresponding `pd.read_csv(...)` path in the notebook.
4. Copy the chart image beside the notebook and rename the three selected images `original_chart_1.png`, `original_chart_2.png` and `original_chart_3.png`.
5. Enter the pool ID, a concise domain label, publisher, publication information and source URL in the notebook's identifying-information block for that artefact.

Artefact 1 is your **primary artefact**: its nine-field critique is completed during the supervised, AI-restricted activity on **Thursday 27 August**. Choose your primary artefact **before** that session and complete its data preparation and alternative view in advance — the supervised window covers only the handwritten critique. On the day you will record its pool ID on the supervised sheet, and the pool ID entered in the notebook for artefact 1 must match that sheet. This supervised critique is the only requirement that differs across the three artefacts. All three require a full critique, alternative view, Chart Choice Decision Record and claim audit, and across your three alternative views you must represent **at least two different Visual Vocabulary categories**.

Before submitting, run the notebook's final self-check and then use **Kernel → Restart & Run All**. The self-check covers G1–G6; clean execution is checked separately during marking.

**Due:** Friday 28 August 2026, 11:59 pm (Sydney time).

Submit one ZIP containing the completed notebook, the `data` folder and the three renamed original chart images. Keep `a1_autograder.py` locally for the self-check; do not include it in the submission.
