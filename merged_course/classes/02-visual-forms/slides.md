# Choosing Visual Forms, slide content

## Choosing Visual Forms

**Core question:** What visual task are we performing?

Speaker direction: show one dataset and ask students to propose questions before proposing charts.

---

## Start with the question

Weak workflow:

```text
DATA → FAVOURITE CHART
```

Stronger workflow:

```text
AUDIENCE → QUESTION → VISUAL TASK → DATA SHAPE → VISUAL FORM
```

---

## One dataset, several legitimate tasks

A transport dataset might support:

- Which mode carries the most passengers?, magnitude or ranking
- How has use changed?, change over time
- Which modes are most variable?, distribution
- Do delays rise with passenger volume?, correlation
- How is the total divided?, part-to-whole

The topic is the same. The visual task changes.

---

## Data types and roles constrain comparisons

Classify fields by what comparisons their values support, not merely by their
software dtype:

| Type or role | Legitimate reading | Example |
|---|---|---|
| nominal | same or different; no inherent order | mode, region |
| ordinal | higher or lower; spacing is not known | service tier, rating |
| quantitative, interval | differences are meaningful; zero is arbitrary | temperature in °C |
| quantitative, ratio | differences, ratios and true zero are meaningful | passengers, dollars |
| temporal | sequence, interval and duration | month, timestamp |
| spatial or relational | location, connection or transfer | coordinates, source → target |

Discrete and continuous are useful implementation distinctions within
quantitative data, but interval versus ratio tells us more about whether a
zero baseline or ratio claim is meaningful.

---

## Types constrain; the question selects the task

The same transport table can support several valid readings:

| Fields | Required comparison | Vocabulary task | Candidate form |
|---|---|---|---|
| mode + passengers | order totals | ranking | sorted dot or bar |
| month + passengers | compare positions through time | change over time | line or small multiples |
| passengers + delay | compare paired values | correlation | scatterplot |
| mode + subtotal + known total | compare shares | part-to-whole | stacked bar |

Use the full chain:

```text
QUESTION → FIELD TYPES/ROLES → REQUIRED COMPARISON
→ VISUAL VOCABULARY TASK → CHANNEL → FORM
```

A data type can rule out an invalid comparison. It cannot select one chart
without an audience and a question.

---

## Visual Vocabulary

Work through each family using its required fields, comparison, suitable forms
and an original example:

- deviation;
- correlation;
- ranking;
- distribution;
- change over time;
- magnitude;
- part-to-whole;
- spatial;
- flow.

---

## Sort by task, not chart name

Give groups question cards and chart cards separately.

Prompt: What must a reader compare, locate, trace or estimate?

---

## Visual channels are not equally precise

Approximate comparison hierarchy:

```text
position on a common scale
→ position on separate scales
→ length
→ angle and slope
→ area
→ volume
→ colour saturation
```

The hierarchy is a design aid, not a law detached from audience and task.

---

## Magnitude and ranking

Useful forms:

- bars;
- dots;
- ordered tables;
- small multiples.

Ask: Is a zero baseline required for the visual claim?

---

## Distribution

Useful forms:

- histogram;
- dot plot;
- box plot;
- density or violin plot.

Ask: Which features: centre, spread, clusters or outliers, remain visible?

---

## Correlation

Use scatterplots to inspect form, direction, strength and exceptions.

Warnings:

- association is not causation;
- aggregation can create or hide patterns;
- a fitted line can conceal subgroups.

---

## Change over time

Useful forms:

- line chart;
- slope chart;
- indexed series;
- small multiples.

Check time intervals, missing periods and methodological breaks.

---

## Hue, lightness and chroma do different jobs

- **Hue** primarily signals identity or category. Different hues have no
  natural order.
- **Lightness/value** can carry ordered magnitude when it changes
  monotonically from light to dark.
- **Chroma/saturation** controls salience and emphasis, but is coarse for
  quantitative comparison.

Colour is contextual and imprecise. Let position or length carry exact values.

---

## Palette family follows data type and task

- **Categorical:** distinct hues of roughly equal visual weight for nominal
  categories; do not imply an order.
- **Sequential:** monotonic lightness for ordinal or quantitative values from
  low to high.
- **Diverging:** two ordered arms around a meaningful midpoint for deviation.
- **Highlight:** one accent colour for the claim, with context in grey.

The midpoint must come from the meaning of the measure—zero, a target or a
reference—not from the palette designer.

---

## Colour must survive without colour

- add redundant cues: direct labels, shape, position or line style;
- test common colour-vision deficiencies rather than relying on red/green;
- test text and mark contrast against the actual background;
- distinguish missing, zero and out-of-range values;
- avoid rainbow palettes whose non-monotonic lightness invents boundaries;
- label directly where possible to reduce legend search and hue memory.

Colour should add information without being the only way to recover it.

---

## Palette check

Before choosing actual colours, classify each case and name one redundant cue:

- ridership low → high;
- change versus the 2019 baseline;
- four transport modes;
- a missing value.

For each, state the data semantics, palette family or special-value treatment,
and how the reading survives without hue.

---

## Tidy data

- each variable is a column;
- each observation is a row;
- each value is a cell.

Tidy structure supports reproducible filtering, grouping and chart generation.

---

## Copilot can transform data, and silently change it

After any generated transformation, check:

- row counts and unique identifiers;
- data types;
- missing values;
- category labels;
- aggregation level;
- totals before and after.

---

## Compare before selecting

Create several plausible forms using the same cleaned data.

For each form, record:

- the question it answers well;
- the comparison it makes easy;
- information it hides;
- likely audience risk.

---

## Reject one alternative

A strong design record explains not only what was selected, but why another plausible option was rejected.

“It looked worse” is not sufficient.

---

## A1 Part B: the same pipeline for every artefact

1. State a claim the supplied data can support.
2. Name the audience, question and required comparison.
3. Design an alternative view that communicates that claim.
4. Explain what becomes easier and harder to see than in the original.

---

## A full Decision Record for every artefact

Record the intended audience, question, decision supported, Vocabulary
category, required comparison and supporting field types/roles, selected form,
why it fits, a genuine rejected
alternative and the specific reason for rejection.

---

## Alternative does not mean universally better

A different claim changes what the design should make easy to see. Compare the
alternative with the original and connect the differences to the stated claim.

---

## Notebook

Use `choosing_visual_forms.ipynb` for the complete class practical: nine
reconstructions followed by tidy data, task classification and chart selection.

Students will:

- name an audience, question and decision before choosing a chart;
- specify and verify a tidy transformation;
- build candidate views that answer different questions;
- select a claim-led alternative and reject one plausible form;
- explain what becomes easier and harder than in the starting view.

---

## Exit ticket

Complete:

- My audience needs to answer …
- This is primarily a ___ visual task.
- I selected ___ because …
- I rejected ___ because …

Complete the separate open-book diagnostic in Canvas after class. It is
ungraded and completed without an assistant.
