# Choosing Visual Forms, worked demonstration

## Purpose

Model how audience and task determine both the data transformation and the visual form.

## Scenario

A transport operations manager asks:

> Which mode carried the most passengers over the year?

Classify the task as magnitude or ranking. The required comparison is the annual total across modes.

## Predict the transformation

The source has twelve monthly rows and three passenger columns. A tidy passenger table should therefore contain:

```text
12 months × 3 modes = 36 observations
```

State this invariant before generating code.

## Demonstrate the transformation

Show how a wide source such as:

| Month | Bus passengers | Train passengers | Ferry passengers |
|---|---:|---:|---:|
| Jan-2025 | 1000 | 1400 | 280 |

becomes:

| month | mode | passengers |
|---|---|---:|
| 2025-01-01 | Bus | 1000 |
| 2025-01-01 | Train | 1400 |
| 2025-01-01 | Ferry | 280 |

Ask Copilot for a `pandas.melt` transformation with explicit requirements. Then verify:

```python
assert len(passengers_long) == 36
assert set(passengers_long['mode']) == {'Bus', 'Train', 'Ferry'}
assert passengers_long['passengers'].isna().sum() == 1
```

## Demonstrate form selection

Aggregate annual totals and compare:

- unordered bars;
- ordered bars;
- a dot plot.

Ask which form best supports the exact task and why. The answer should refer to position, length and ordering rather than taste.

## Change the question

Replace the manager’s question with:

> When did each mode experience its busiest and quietest periods?

The topic is unchanged, but the task becomes change over time. The annual aggregation is now harmful because it removes the needed structure.

## Transition to the lab

Students choose an audience, state a question, predict the tidy result, and only then ask Copilot for transformation or plotting assistance.

