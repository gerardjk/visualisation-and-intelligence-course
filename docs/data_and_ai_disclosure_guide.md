# Data and AI Disclosure Guide

## Purpose

A Data and AI Disclosure is a short, standardised explanation inside the app. It tells users where the data came from, how it was transformed, what the visualisation can and cannot support, and how intelligent tools were used.

Use this student-facing term rather than “Nutrition Label.” The older phrase appears in some data-documentation literature, but this course uses clearer language.

## Required sections

```text
Data source:
Time period:
Unit of analysis:
What the data includes:
What the data excludes:
Cleaning and transformations:
Primary visual task:
FT Visual Vocabulary category:
Known limitations:
AI assistance used:
Human verification performed:
Appropriate use:
Inappropriate use:
```

## Streamlit pattern

```python
with st.expander("About the data and AI use"):
    st.markdown("""
    **Data source:**
    ...
    """)
```

## Quality test

A good disclosure allows a user to answer:

- Can I trust the source?
- What time period is covered?
- What does one row mean?
- What has been excluded?
- What transformations were performed?
- What chart task is the app supporting?
- What conclusions should I avoid?
- Where did intelligent tools affect the work?
- What did humans verify?
