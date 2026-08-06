# Seeing Data: worked demonstration

## Purpose

Model the complete reasoning cycle before students begin the notebook:

```text
predict → calculate → visualise → interpret → verify → qualify
```

## Demonstration script

### Predict

Show only the statement that four datasets have the same mean, variance, correlation and fitted line. Ask students to sketch what they expect.

Do not correct predictions yet.

### Calculate

Run the grouped summary in the instructor notebook. Ask:

- Which quantities are nearly identical?
- What story would be tempting if this were all we had?
- What does the table not describe?

### Visualise

Reveal the common-scale small multiples. Give students thirty silent seconds before inviting observations.

Use two columns on the board:

| Visible evidence | Interpretation |
|---|---|
| A curved point pattern | A nonlinear process may be present |
| One point separated vertically | The point may be an error or exceptional case |
| Most x-values identical in one dataset | The fitted slope depends heavily on one point |

### Audit language

Present this generated statement:

> All four datasets demonstrate a strong, consistent linear relationship, confirming that x reliably predicts y.

Ask students to mark each part:

- “all four”: contradicted by the patterns;
- “strong”: ambiguous without a defined criterion;
- “consistent linear relationship”, contradicted;
- “confirming”: overconfident;
- “reliably predicts”: untested out-of-sample claim.

### Repair

A defensible version is:

> The datasets share similar summary statistics and fitted lines, but their plots reveal different structures, including curvature and influential outliers; the summaries alone do not justify a common model.

## Transition to the lab

Tell students that their task is not merely to reproduce the figure. Their task is to create an evidence trail showing why a sentence is or is not justified.

