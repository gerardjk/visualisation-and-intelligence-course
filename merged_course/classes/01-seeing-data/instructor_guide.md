# Seeing Data: instructor guide

## What makes this a complete three-hour session

The session alternates prediction, explanation, computation and critique. Do not deliver the slide deck as a continuous lecture. The planned pauses and student outputs are part of the teaching material.

| Block | Minimum completion | Extension if the room moves quickly |
|---|---|---|
| Anscombe opening | Prediction plus four-panel comparison | Ask students to invent a fifth dataset with similar summaries |
| Snow discussion | Separate observation, association and causal claim | Identify additional historical evidence needed |
| Notebook | Shared statistics, common-scale plots and claim audit | Build an additional robust diagnostic view |
| Critique and Repair | Claim classification and repaired caption | Rebuild the chart with a different audience in mind |

## Before class

- Open and test the instructor notebook.
- Put the student notebook and starter notebook in the LMS.
- Print or distribute `critique_pack.md` and `activity_critique_and_repair.md`.
- Keep the starter notebook available as a recovery route rather than giving it to everyone immediately.
- State the assessment boundary explicitly: assistants are permitted and documented in the Seeing Data notebook, but A1 Part A is completed without an assistant during the supervised window in the Dashboards session. Parts B and C follow the A1 brief.

## Worked demonstration

Use the Anscombe summary and plotting sequence in `worked_demonstration.md`. Think aloud while distinguishing:

- what the code calculates;
- what the plot makes visible;
- what can be stated directly;
- what remains an interpretation;
- what would require contextual evidence.

## Notebook checkpoints

Announce these times relative to the start of the lab:

| Time | Expected position | Intervention |
|---|---|---|
| 10 minutes | Data loaded and prediction recorded | Check kernel and imports |
| 25 minutes | Summary table passes assertions | Release the summary cell from the starter notebook if needed |
| 38 minutes | Four common-scale panels visible | Pair students who have working plots with those debugging |
| 48 minutes | Generated claims classified | Stop further chart styling |
| 55 minutes | Repair and provenance recorded | Move everyone to the studio activity |

## Suggested answers

### Anscombe

- All datasets have approximately the same means, variances, correlation and fitted line.
- Dataset A resembles a conventional linear relationship.
- Dataset B contains a curved relationship that a linear fit represents poorly.
- Dataset C is dominated by a vertical outlier.
- Dataset D is dominated by a high-leverage horizontal outlier.
- “The datasets have the same relationship” is contradicted by the plots.
- “The linear model has similar coefficients” is supported but incomplete.

### Snow

- Direct observation: deaths are spatially concentrated near the Broad Street pump.
- Interpretation: proximity to that pump is associated with cases.
- Causal claim: contaminated water caused disease; this requires evidence beyond the map.
- Useful additional evidence includes household exposure, competing water sources, exceptions and changes after intervention.

### Critique pack

- The deliberately truncated vertical axis exaggerates the difference between two satisfaction rates.
- The title uses causal language not supported by the comparison.
- Sample size, collection method, uncertainty and group composition are absent.
- A zero-based bar chart or a dot plot with uncertainty would support a fairer comparison.
- A defensible caption describes the measured difference without claiming that the program caused it.

## Common misconceptions and responses

| Misconception | Instructor response |
|---|---|
| “Statistics are misleading; pictures are truthful.” | Both are selective representations and both require checking. |
| “Correlation never matters because it is not causation.” | Association is useful evidence; the error is overstating what it establishes. |
| “The chart speaks for itself.” | Ask students to identify the labels, scales, omissions and contextual assumptions doing interpretive work. |
| “AI hallucination means invented numbers only.” | Unsupported framing, causal language and omitted uncertainty are also failures. |
| “A misleading chart must contain false data.” | Honest values can still be framed to encourage an unjustified impression. |
| “Accessibility is separate from accuracy.” | If an audience cannot reliably perceive the encoding, the communication is not accurate for that audience. |

## Assessment connection

This session prepares students for A1. Critique and Repair. Make the relationship explicit:

| Session output | Portfolio criterion |
|---|---|
| One-sentence claim and audience | Main claim and audience identified |
| Visual task and channel identification | Visual Vocabulary and encoding critique |
| Missing context and uncertainty | Limitation identified |
| Repaired chart or caption | Concrete redesign suggestion |
| Anscombe, Snow, Bertin or governance concept | Course concept used correctly |

## Exit ticket review

Sort responses into:

- claims students can already support;
- limitations they recognised;
- verification needs to revisit in Choosing Visual Forms.
