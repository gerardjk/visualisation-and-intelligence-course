# Choosing Visual Forms, instructor guide

## What makes this a complete three-hour session

This session uses repeated classification and comparison rather than a long chart taxonomy lecture. Students work with the same transport data through several questions so they experience the difference between topic, task and form.

| Block | Minimum completion | Extension if the room moves quickly |
|---|---|---|
| Visual Vocabulary sort | Classify the core question cards | Write an ambiguous question and defend two classifications |
| Tidy-data demonstration | Convert one passenger column pair | Generalise the transformation to a new mode |
| Notebook | Verified tidy data and two candidate charts | Complete all three charts and test an alternative palette |
| Decision record | Select one and reject one | Redesign for a second audience |

## Before class

- Open and run `notebooks/choosing_visual_forms_solution.ipynb`.
- Put only `choosing_visual_forms.ipynb` and its `data` folder in the student LMS area;
  retain the solution for teaching staff.
- Print one set of `visual_vocabulary_cards.md` per group.
- Print or distribute `activity_chart_choice.md`.
- Prepare a board with three headings: audience, question and visual task.

## Worked demonstration

Use `worked_demonstration.md` to model a small wide-to-tidy transformation. Narrate the expected row count before writing code. Treat the row-count prediction as part of the analysis, not an afterthought.

Before selecting a form, annotate the fields: `mode` is nominal, `month` is
temporal and `passengers` is a quantitative ratio measure. Ask which comparisons
each field supports, then change the question while leaving the fields fixed.
Use the board chain: question → types/roles → comparison → task → channel → form.

For the colour sequence, do not spend time naming hues on a wheel. Ask what
happens when the swatches are printed in greyscale, then require students to
identify the palette family, its ordering or midpoint, and one redundant cue.

## Notebook checkpoints

| Time | Expected position | Intervention |
|---|---|---|
| 10 minutes | Audience, question and expected tidy shape recorded | Challenge questions that already name a chart |
| 25 minutes | Tidy dataset passes structural assertions | Release the transformation helper from the starter notebook |
| 38 minutes | Visual-task table complete and first chart visible | Limit struggling students to magnitude and time candidates |
| 50 minutes | Two candidate charts complete | Stop decorative styling and move to comparison |
| 55 minutes | Provisional selection recorded | Move everyone to the studio; complete the full Decision Record there |

## Suggested classifications

| Question | Primary task | Likely form |
|---|---|---|
| Which mode carries the most passengers overall? | Magnitude or ranking | Ordered bar or dot plot |
| How does use change through the year? | Change over time | Line chart or small multiples |
| Do busier months also have longer delays? | Correlation | Scatterplot, grouped by mode |
| Which mode has the most variable delays? | Distribution | Box plot, dot plot or small multiples |
| How is total patronage divided among modes? | Part-to-whole | Stacked bar or a direct magnitude comparison |

Several answers can be valid. Judge whether the stated comparison is supported.

## Common misconceptions and responses

| Misconception | Instructor response |
|---|---|
| “The dataset determines the chart.” | Ask what the audience must compare; the same data supports several tasks. |
| “It is numeric, so arithmetic is valid.” | Ask whether it is a measure or an identifier, and whether zero and ratios are meaningful. |
| “Ordinal categories are equally spaced.” | Higher/lower is valid; the distance between adjacent labels is not established. |
| “Tidy means no missing values.” | Tidy describes structure. Missingness may remain meaningful and must not be silently erased. |
| “A more complex chart contains more insight.” | Ask whether the additional encoding supports a required task. |
| “Pie charts are always wrong.” | Ask what comparison is required and whether angle or area supports it well enough. |
| “A line chart is always appropriate for months.” | A line implies an ordered, connected sequence; ask whether that implication fits. |
| “Copilot cleaning is correct if the code runs.” | Require invariants: expected rows, modes, missingness, types and totals. |
| “Colourful means accessible.” | Test contrast, common colour-vision deficiencies and redundant encoding. |
| “A diverging palette looks balanced, so zero belongs in the middle.” | The midpoint must come from the measure: zero, target, average or another defensible reference. |

## Assessment connection

| Session output | Assessment evidence |
|---|---|
| Audience and question | User story and purpose |
| Visual Vocabulary classification | Task-to-form reasoning |
| Verified tidy transformation | Technical reliability |
| Candidate comparison | Design judgement |
| Rejected alternative | Defence of design choice |
| Provenance record | Responsible intelligent-tool use |

## Exit ticket review

Look for answers that name only a chart without explaining the comparison. Return those as prompts for revision before the dashboard session.
