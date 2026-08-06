"""Build starter and instructor notebook variants for the developed sessions."""

from __future__ import annotations

import json
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def markdown(text: str) -> dict:
    cell_id = hashlib.sha1(("markdown:" + text).encode("utf-8")).hexdigest()[:12]
    return {"cell_type": "markdown", "id": cell_id, "metadata": {}, "source": text.splitlines(keepends=True)}


def code(text: str, tags: list[str] | None = None) -> dict:
    metadata = {"tags": tags} if tags else {}
    cell_id = hashlib.sha1(("code:" + text).encode("utf-8")).hexdigest()[:12]
    return {
        "cell_type": "code",
        "id": cell_id,
        "execution_count": None,
        "metadata": metadata,
        "outputs": [],
        "source": text.splitlines(keepends=True),
    }


def notebook(cells: list[dict]) -> dict:
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


IMPORTS = """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8-whitegrid')
pd.set_option('display.precision', 3)
"""

ANSCOMBE_DATA = """x_common = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]
x_four = [8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8]
values = {
    'A': (x_common, [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]),
    'B': (x_common, [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74]),
    'C': (x_common, [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73]),
    'D': (x_four,   [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89]),
}
anscombe = pd.concat(
    [pd.DataFrame({'dataset': label, 'x': x, 'y': y}) for label, (x, y) in values.items()],
    ignore_index=True,
)
anscombe.head()
"""

SUMMARY_SOLUTION = """summary_rows = []
for label, group in anscombe.groupby('dataset'):
    slope, intercept = np.polyfit(group['x'], group['y'], 1)
    summary_rows.append({
        'dataset': label,
        'x_mean': group['x'].mean(),
        'y_mean': group['y'].mean(),
        'x_variance': group['x'].var(ddof=1),
        'y_variance': group['y'].var(ddof=1),
        'correlation': group['x'].corr(group['y']),
        'slope': slope,
        'intercept': intercept,
    })
summary = pd.DataFrame(summary_rows)
summary
"""

SUMMARY_CHECK = """assert summary.shape == (4, 8)
assert set(summary['dataset']) == {'A', 'B', 'C', 'D'}
assert np.allclose(summary['x_mean'], 9.0, atol=0.01)
assert np.allclose(summary['y_mean'], 7.5, atol=0.01)
assert np.allclose(summary['correlation'], 0.816, atol=0.01)
print('Summary checks passed.')
"""

ANSCOMBE_PLOT = """fig, axes = plt.subplots(2, 2, figsize=(10, 8), sharex=True, sharey=True)
for ax, (label, group) in zip(axes.flat, anscombe.groupby('dataset')):
    slope, intercept = np.polyfit(group['x'], group['y'], 1)
    line_x = np.array([3, 20])
    ax.scatter(group['x'], group['y'], s=55, color='#18678f')
    ax.plot(line_x, slope * line_x + intercept, color='#e66852', linewidth=2)
    ax.set_title(f'Dataset {label}', fontweight='bold')
    ax.set_xlim(3, 20)
    ax.set_ylim(2, 14)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
fig.suptitle('Similar summaries, different structures', fontsize=16, fontweight='bold')
fig.tight_layout()
plt.show()
"""

ANSCOMBE_MISLEAD = """dataset_c = anscombe.query("dataset == 'C'")
fig, (left, right) = plt.subplots(1, 2, figsize=(11, 4.2))
left.scatter(dataset_c['x'], dataset_c['y'], color='#e66852', s=55)
left.set(xlim=(3, 20), ylim=(2, 14), title='Misleading crop: outlier removed from view', xlabel='x', ylabel='y')
left.set_ylim(4, 10)

right.scatter(dataset_c['x'], dataset_c['y'], color='#18678f', s=55)
right.set(xlim=(3, 20), ylim=(2, 14), title='Repair: full common scale', xlabel='x', ylabel='y')
fig.tight_layout()
plt.show()
"""


def seeing_starter() -> dict:
    cells = [
        markdown("""# Seeing Data — supported starter

Use this version if you need help with syntax. The reasoning, interpretation and provenance decisions remain yours."""),
        markdown("""## Prediction

Record what you expect before running the summaries or plots. Similar statistics do not guarantee similar visual structure."""),
        code(IMPORTS),
        code(ANSCOMBE_DATA),
        markdown("""## Grouped summary

The helper below calculates a row for one group. Complete the loop that applies it to all four datasets."""),
        code("""def summarise_group(label, group):
    slope, intercept = np.polyfit(group['x'], group['y'], 1)
    return {
        'dataset': label,
        'x_mean': group['x'].mean(),
        'y_mean': group['y'].mean(),
        'x_variance': group['x'].var(ddof=1),
        'y_variance': group['y'].var(ddof=1),
        'correlation': group['x'].corr(group['y']),
        'slope': slope,
        'intercept': intercept,
    }

# TODO: call summarise_group for every dataset and create summary.
# summary_rows = [...]
# summary = pd.DataFrame(summary_rows)
"""),
        code(SUMMARY_CHECK, ["verification"]),
        markdown("""## Common-scale plots

The axes and line calculation are supplied. Complete the scatterplot and labels."""),
        code("""fig, axes = plt.subplots(2, 2, figsize=(10, 8), sharex=True, sharey=True)
for ax, (label, group) in zip(axes.flat, anscombe.groupby('dataset')):
    slope, intercept = np.polyfit(group['x'], group['y'], 1)
    line_x = np.array([3, 20])
    # TODO: add points and the fitted line.
    ax.set_xlim(3, 20)
    ax.set_ylim(2, 14)
    # TODO: add a neutral title and axis labels.
fig.tight_layout()
plt.show()
"""),
        markdown("""## Claim audit

Classify this statement clause by clause:

> All four datasets demonstrate a strong, consistent linear relationship, confirming that x reliably predicts y.

Use: supported directly, plausible but unverified, unsupported, or contradicted."""),
        markdown("""## Repair and provenance

Create one misleading view without changing the data, then repair it. Record the prompt, accepted output, changes, checks and remaining limitation."""),
    ]
    return notebook(cells)


def seeing_instructor() -> dict:
    cells = [
        markdown("""# Seeing Data — instructor solution

This executable version supplies the technical solution and suggested interpretation. Use it for demonstration and troubleshooting, not as a replacement for student reasoning."""),
        code(IMPORTS),
        code(ANSCOMBE_DATA),
        markdown("## Shared summaries"),
        code(SUMMARY_SOLUTION),
        code(SUMMARY_CHECK, ["verification"]),
        markdown("## Common-scale small multiples"),
        code(ANSCOMBE_PLOT),
        markdown("""## Suggested interpretation

- A resembles a conventional linear relationship.
- B is curved, so the fitted line misses systematic structure.
- C is strongly influenced by one vertical outlier.
- D is strongly influenced by one high-leverage horizontal point.
- Similar summary statistics do not establish similar data-generating structure.

Suggested repair of generated prose:

> The datasets share similar summary statistics and fitted lines, but their plots reveal different structures, including curvature and influential outliers; the summaries alone do not justify a common model."""),
        markdown("## Deliberately misleading view and repair"),
        code(ANSCOMBE_MISLEAD),
        markdown("""## Provenance model

Record the tool and model, prompt purpose, output used, modifications, verification and what the tool missed. A complete record explains decisions rather than pasting a transcript."""),
    ]
    return notebook(cells)


TRANSPORT_IMPORTS = """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8-whitegrid')
rng = np.random.default_rng(36104)
"""

TRANSPORT_DATA = """months = pd.date_range('2025-01-01', periods=12, freq='MS')
messy = pd.DataFrame({
    'Month': months.strftime('%b-%Y'),
    'Bus passengers': rng.integers(820, 1280, 12).astype(str),
    'Train passengers': rng.integers(1050, 1650, 12).astype(str),
    'Ferry passengers': rng.integers(180, 430, 12).astype(str),
    'Bus delay min': np.round(rng.normal(7.5, 1.6, 12), 1),
    'Train delay min': np.round(rng.normal(5.5, 1.2, 12), 1),
    'Ferry delay min': np.round(rng.normal(4.0, 1.0, 12), 1),
})
messy.loc[4, 'Train passengers'] = '..'
messy.loc[8, 'Bus passengers'] = '1,204'
messy.loc[10, 'Ferry delay min'] = np.nan
messy
"""

TIDY_SOLUTION = """passenger_columns = ['Bus passengers', 'Train passengers', 'Ferry passengers']
delay_columns = ['Bus delay min', 'Train delay min', 'Ferry delay min']

passengers = messy.melt(
    id_vars='Month', value_vars=passenger_columns,
    var_name='mode', value_name='passengers',
)
passengers['mode'] = passengers['mode'].str.replace(' passengers', '', regex=False)
passengers['passengers'] = pd.to_numeric(
    passengers['passengers'].str.replace(',', '', regex=False).replace('..', np.nan),
    errors='coerce',
)

delays = messy.melt(
    id_vars='Month', value_vars=delay_columns,
    var_name='mode', value_name='average_delay_minutes',
)
delays['mode'] = delays['mode'].str.replace(' delay min', '', regex=False)

tidy = passengers.merge(delays, on=['Month', 'mode'], validate='one_to_one')
tidy['month'] = pd.to_datetime(tidy.pop('Month'), format='%b-%Y')
tidy = tidy[['month', 'mode', 'passengers', 'average_delay_minutes']].sort_values(['month', 'mode']).reset_index(drop=True)
tidy.head()
"""

TIDY_CHECK = """assert tidy.shape == (36, 4)
assert list(tidy.columns) == ['month', 'mode', 'passengers', 'average_delay_minutes']
assert set(tidy['mode']) == {'Bus', 'Train', 'Ferry'}
assert pd.api.types.is_datetime64_any_dtype(tidy['month'])
assert pd.api.types.is_numeric_dtype(tidy['passengers'])
assert pd.api.types.is_numeric_dtype(tidy['average_delay_minutes'])
assert tidy['passengers'].isna().sum() == 1
assert tidy['average_delay_minutes'].isna().sum() == 1
print('Tidy-data checks passed.')
"""

TRANSPORT_CHARTS = """mode_colours = {'Bus': '#18678f', 'Train': '#e66852', 'Ferry': '#30a8b1'}

annual = tidy.groupby('mode', as_index=False)['passengers'].sum().sort_values('passengers')
fig, ax = plt.subplots(figsize=(7, 4))
ax.barh(annual['mode'], annual['passengers'], color=[mode_colours[m] for m in annual['mode']])
ax.set(title='Which mode carried the most passengers?', xlabel='Annual passengers', ylabel='')
plt.show()

fig, ax = plt.subplots(figsize=(9, 4.5))
for mode, group in tidy.groupby('mode'):
    ax.plot(group['month'], group['passengers'], marker='o', label=mode, color=mode_colours[mode])
ax.set(title='How did passenger use change through the year?', xlabel='', ylabel='Monthly passengers')
ax.legend(frameon=False, ncol=3)
plt.show()

fig, ax = plt.subplots(figsize=(7, 4.5))
for mode, group in tidy.groupby('mode'):
    ax.scatter(group['passengers'], group['average_delay_minutes'], label=mode, color=mode_colours[mode], s=55)
ax.set(title='Do busier months also have longer delays?', xlabel='Monthly passengers', ylabel='Average delay (minutes)')
ax.legend(frameon=False)
plt.show()
"""


def forms_starter() -> dict:
    cells = [
        markdown("""# Choosing Visual Forms — supported starter

Use this version if transformation syntax is blocking your progress. You must still state the audience, question, visual task and design decision."""),
        code(TRANSPORT_IMPORTS),
        code(TRANSPORT_DATA),
        markdown("""## Predict the tidy result

Record expected rows, modes, missing values and data types before running the transformation."""),
        code("""passenger_columns = ['Bus passengers', 'Train passengers', 'Ferry passengers']
delay_columns = ['Bus delay min', 'Train delay min', 'Ferry delay min']

passengers = messy.melt(id_vars='Month', value_vars=passenger_columns,
                        var_name='mode', value_name='passengers')
# TODO: clean the mode labels, thousands separators and '..' value.

delays = messy.melt(id_vars='Month', value_vars=delay_columns,
                    var_name='mode', value_name='average_delay_minutes')
# TODO: clean the delay mode labels.

# TODO: merge passengers and delays, parse the month, select the four target columns,
# and store the result as tidy.
"""),
        code(TIDY_CHECK, ["verification"]),
        markdown("""## Candidate charts

The mode palette and annual aggregation are supplied. Complete at least two candidates that answer different questions."""),
        code("""mode_colours = {'Bus': '#18678f', 'Train': '#e66852', 'Ferry': '#30a8b1'}
annual = tidy.groupby('mode', as_index=False)['passengers'].sum().sort_values('passengers')

# TODO: an ordered magnitude or ranking chart.
# TODO: a change-over-time chart.
# Extension: a relationship chart retaining mode.
"""),
        markdown("""## Decision

For each candidate, state the question answered, easy comparison, hidden information and audience risk. Select one and reject one for a specific reason."""),
        markdown("""## Provenance

Record the prompt, accepted code, changes, verification and what the tool missed. Explain one generated code block line by line."""),
    ]
    return notebook(cells)


def forms_instructor() -> dict:
    cells = [
        markdown("""# Choosing Visual Forms — instructor solution

This executable version demonstrates the transformation, checks and three defensible chart candidates."""),
        code(TRANSPORT_IMPORTS),
        code(TRANSPORT_DATA),
        markdown("""## Prediction

Twelve months and three modes should produce 36 observations. One passenger value and one delay value should remain missing. Missing is not equivalent to zero."""),
        code(TIDY_SOLUTION),
        code(TIDY_CHECK, ["verification"]),
        markdown("""## Task classification

- Most passengers overall: magnitude or ranking.
- Pattern through the year: change over time.
- Passengers versus delay: correlation.
- Variability of delay: distribution."""),
        code(TRANSPORT_CHARTS),
        markdown("""## Suggested decision

For an operations manager asking which mode carried the most passengers, select the ordered horizontal bar chart. Position and length on a common scale make the ranking direct. Reject the line chart for this question because it preserves useful temporal detail but makes the annual comparison slower and less direct.

Remaining limitation: summing the available months does not adjust for the missing train observation."""),
        markdown("""## Provenance model

A useful record identifies the requested transformation, notes that missing values were preserved, records the structural assertions, and explains why the generated chart was modified or rejected."""),
    ]
    return notebook(cells)


def write(path: Path, content: dict) -> None:
    path.write_text(json.dumps(content, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(path.relative_to(ROOT))


def normalise_ids(path: Path) -> None:
    content = json.loads(path.read_text(encoding="utf-8"))
    for index, cell in enumerate(content["cells"]):
        if "id" not in cell:
            source = "".join(cell.get("source", []))
            seed = f"{index}:{cell.get('cell_type')}:{source}"
            cell["id"] = hashlib.sha1(seed.encode("utf-8")).hexdigest()[:12]
    write(path, content)


def main() -> None:
    normalise_ids(ROOT / "seeing_data" / "seeing_data_lab.ipynb")
    normalise_ids(ROOT / "choosing_visual_forms" / "choosing_visual_forms_lab.ipynb")
    write(ROOT / "seeing_data" / "seeing_data_starter.ipynb", seeing_starter())
    write(ROOT / "seeing_data" / "seeing_data_instructor.ipynb", seeing_instructor())
    write(ROOT / "choosing_visual_forms" / "choosing_visual_forms_starter.ipynb", forms_starter())
    write(ROOT / "choosing_visual_forms" / "choosing_visual_forms_instructor.ipynb", forms_instructor())


if __name__ == "__main__":
    main()
