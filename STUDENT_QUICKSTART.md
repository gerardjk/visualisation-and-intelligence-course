# Student Quickstart

## What you will build

By the end of the course your group will deploy a public Streamlit data app. The app will include:

- a public dataset,
- user stories,
- interactive filters,
- at least three visualisations,
- clear interpretation,
- Data and AI Disclosure,
- an AI Provenance Matrix,
- a GitHub repository,
- a deployed Streamlit URL.

## Tools to install or create accounts for

- Tableau Public.
- GitHub.
- GitHub Desktop.
- Python 3.10 or later.
- A code editor such as VS Code.
- Streamlit Community Cloud.
- The approved intelligent tool for this course.

## Running the starter app

```bash
cd starter_app
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Your design workflow

Every important visualisation decision should follow this pattern:

```text
User story → Visual Vocabulary category → chart or interaction → risk → alternative considered
```

Example:

```text
As a transport analyst, I want to compare patronage recovery by mode since 2019, so that I can identify which modes remain below baseline.

Visual Vocabulary category: Change over time.
Chosen chart: Indexed line chart.
Risk: A methodology change may make mode comparisons invalid.
Alternative considered: yearly bar chart, rejected because it hides monthly seasonality.
```

## Intelligent-tool use

You may use approved intelligent tools, but you must document significant use. Do not submit code, text, or interpretations you cannot explain.

Use the AI Provenance Matrix whenever a tool meaningfully affects your work.

## Public data warning

Do not upload private, sensitive, confidential, restricted, or identifiable data to Tableau Public, GitHub, or Streamlit Community Cloud.
