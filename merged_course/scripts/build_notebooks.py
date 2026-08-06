"""Generate the Copilot-friendly class notebooks.

Each notebook follows the course notebook contract:
  1. context before code, 2. scaffolded cells with TODO prompts,
  3. verification cells after every exercise, 4. an AI-disclosure block at the end.
"""

from pathlib import Path

import nbformat as nbf

ROOT = Path(__file__).resolve().parents[2]
CLASSES = ROOT / "merged_course" / "classes"


def md(source):
    return nbf.v4.new_markdown_cell(source)


def code(source):
    return nbf.v4.new_code_cell(source)


def save(cells, path):
    nb = nbf.v4.new_notebook()
    nb.cells = cells
    nb.metadata["kernelspec"] = {
        "display_name": "Python 3", "language": "python", "name": "python3",
    }
    nb.metadata["language_info"] = {"name": "python"}
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        nbf.write(nb, f)
    print(path)


DISCLOSURE = md("""\
## AI disclosure block

Before you close this notebook, complete the course disclosure block. This is
the same block you will attach to every assessed artefact.

```text
What did the intelligent tool contribute?
  (e.g. "generated the first draft of plot_mode_recovery"; "suggested the melt call")
How was each contribution checked?
  (e.g. "ran the verification cell"; "hand-computed the Inner Sydney 2024 total")
What did you write or decide yourself?
What would you not trust the tool to do in this notebook?
```

Write your answers in the cell below.\
""")

DISCLOSURE_ANSWER = md("""\
*Your disclosure:*

- **Tool contributed:** …
- **How checked:** …
- **I wrote/decided:** …
- **Would not trust:** …\
""")


TRANSPORT_SETUP = '''\
# Setup: run this cell, no need to edit it.
# It builds the synthetic public-transport patronage dataset used across this course:
# monthly rider counts for six NSW regions and four transport modes, 2019-2025,
# with a seasonal cycle and a COVID-shaped shock. Teaching data, not real data.
import math
import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

random.seed(42)
np.random.seed(42)

REGIONS = ["Inner Sydney", "Western Sydney", "Northern Beaches",
           "Central Coast", "Newcastle", "Illawarra"]
MODES = ["Train", "Bus", "Ferry", "Light rail"]
BASE = {"Train": 1_000_000, "Bus": 700_000, "Ferry": 90_000, "Light rail": 120_000}
FACTOR = {"Inner Sydney": 1.3, "Western Sydney": 1.1, "Northern Beaches": 0.55,
          "Central Coast": 0.45, "Newcastle": 0.5, "Illawarra": 0.42}

rows = []
for region in REGIONS:
    for mode in MODES:
        base = BASE[mode] * FACTOR[region]
        for date in pd.date_range("2019-01-01", "2025-12-01", freq="MS"):
            season = 1 + 0.08 * math.sin((date.month - 1) / 12 * 2 * math.pi)
            covid = 1.0
            if pd.Timestamp("2020-03-01") <= date <= pd.Timestamp("2021-12-01"):
                covid = 0.35 + 0.3 * (date - pd.Timestamp("2020-03-01")).days / 640
            elif date > pd.Timestamp("2021-12-01"):
                covid = min(1.0, 0.65 + 0.35 * (date - pd.Timestamp("2021-12-01")).days / 1100)
            noise = random.gauss(1, 0.03)
            rows.append({"date": date, "region": region, "mode": mode,
                         "riders": int(base * season * covid * noise)})

transport = pd.DataFrame(rows)
print(f"{len(transport):,} rows")
transport.head()\
'''


def build_seeing_data():
    cells = [
        md("""\
# Seeing Data: class notebook

**36104 Data Visualisation and Narratives · Week 1**

A chart is a claim about how the world is organised. In this notebook you will
make charts, let an AI assistant make charts, and, most importantly, verify
the claims both of you produce.

## How to work in this notebook

- Work in VS Code (or Jupyter) **with your AI assistant enabled**. Every
  exercise is written so that the markdown context plus the code scaffold give
  the assistant what it needs to draft a useful completion.
- You may accept, edit, or ignore any suggestion. What you may **not** do is
  submit code that fails its verification cell.
- A verification cell that fails is a *finding*, not a failure, read the
  error, work out whether the code or the claim is wrong, and fix it.
- Keep the **verification ladder** beside you:
  **1 TRACE** what data/transformation produced the chart →
  **2 CHECK** labels, scales, units, totals →
  **3 TEST** the pattern in another view →
  **4 BOUND** the claim with its limits →
  **5 DISCLOSE** what the tool contributed.\
"""),
        code(TRANSPORT_SETUP),

        # ---- Exercise 1 ----
        md("""\
## Exercise 1. The summary is not the shape

Anscombe's quartet: four small datasets constructed so that their summary
statistics agree almost exactly, while their shapes disagree completely.

**Task.** Compute the summary statistics for each dataset, then draw the four
scatterplots. Watch the moment the numbers stop being enough.

*Copilot works well here if you write the docstring first, then pause.*\
"""),
        code('''\
# Anscombe's quartet: the classic values (Anscombe, 1973).
anscombe = {
    "I":   dict(x=[10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5],
                y=[8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]),
    "II":  dict(x=[10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5],
                y=[9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74]),
    "III": dict(x=[10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5],
                y=[7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73]),
    "IV":  dict(x=[8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8],
                y=[6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89]),
}


def summarise(name: str) -> dict:
    """Return summary statistics for one Anscombe dataset.

    Given the dataset key ("I".."IV"), return a dict with:
      mean_x, mean_y: means of x and y
      var_x, var_y: sample variances (ddof=1)
      corr. Pearson correlation between x and y
    Round every value to 2 decimal places.
    """
    # TODO: implement using numpy (np.mean, np.var with ddof=1, np.corrcoef)
    raise NotImplementedError


for name in anscombe:
    print(name, summarise(name))\
'''),
        code('''\
# Verification: the whole point of the quartet is that these agree.
for name in anscombe:
    s = summarise(name)
    assert abs(s["mean_x"] - 9.0) < 0.01, f"{name}: mean_x should be 9.0, got {s['mean_x']}"
    assert abs(s["mean_y"] - 7.5) < 0.06, f"{name}: mean_y should be ~7.50, got {s['mean_y']}"
    assert abs(s["corr"] - 0.82) < 0.01, f"{name}: corr should be ~0.82, got {s['corr']}"
print("All four datasets agree on the summary statistics. Now look at them.")\
'''),
        code('''\
# Now the picture. Draw the four datasets as a 2x2 grid of scatterplots,
# same axis limits on every panel, one regression line per panel.
def plot_quartet(anscombe: dict) -> None:
    """2x2 scatterplots of Anscombe's quartet with fitted lines.

    Same x/y limits everywhere (x: 2..20, y: 2..14) so the panels are
    directly comparable. Title each panel with its key.
    """
    # TODO: matplotlib subplots; np.polyfit(x, y, 1) for each fitted line
    raise NotImplementedError


plot_quartet(anscombe)\
'''),
        md("""\
**Reflect** (edit this cell): which panel most changes your interpretation of
"correlation ≈ 0.82"? What claim would each panel justify, and what claim
would it forbid?\
"""),

        # ---- Exercise 2 ----
        md("""\
## Exercise 2. Generate a chart, then interrogate it

Now the real dataset. The `transport` DataFrame holds monthly rider counts by
`region` and `mode`, 2019–2025, including a COVID-shaped collapse and recovery.

**Task.** Ask your assistant to draw *"total monthly riders per mode over
time"*: write the docstring below and let it draft the body. Then run the
verification cell, which climbs the first two rungs of the ladder (TRACE and
CHECK) for you. If verification fails, the bug is somewhere between the
assistant's idea of the data and the actual data. Find it.\
"""),
        code('''\
def plot_mode_recovery(transport: pd.DataFrame) -> pd.DataFrame:
    """Line chart of total monthly riders per mode, 2019-2025.

    - Aggregate riders across regions: one monthly total per mode.
    - One line per mode, labelled, with a legend and y-axis in millions.
    - Title the chart with the claim it supports, not a restatement of the axes.
    - RETURN the aggregated DataFrame used for plotting
      (columns: date, mode, riders) so it can be verified.
    """
    # TODO: groupby(["date", "mode"]), then plot one line per mode
    raise NotImplementedError


plotted = plot_mode_recovery(transport)
plotted.head()\
'''),
        code('''\
# Verification. TRACE and CHECK.
# 1 TRACE: the plotted table must reconcile with the source table.
assert plotted["riders"].sum() == transport["riders"].sum(), (
    "Aggregation lost or duplicated riders: plotted total != source total")
# 2 CHECK: every mode present, every month present, no NaNs.
assert set(plotted["mode"]) == set(MODES), "A mode went missing in the aggregation"
assert plotted.groupby("mode")["date"].nunique().eq(84).all(), (
    "Each mode should have 84 monthly points (2019-01..2025-12)")
assert plotted["riders"].notna().all(), "NaNs appeared during aggregation"
# Spot total, hand-derivable: Train riders in Jan 2019 across all six regions.
jan = pd.Timestamp("2019-01-01")
jan_train = plotted[(plotted["mode"] == "Train") & (plotted["date"] == jan)]["riders"].iloc[0]
source_jan_train = transport[(transport["mode"] == "Train") & (transport["date"] == jan)]["riders"].sum()
assert jan_train == source_jan_train, "Spot total disagrees for Train, Jan 2019"
print("TRACE ✓  CHECK ✓, now do TEST yourself: does the recovery story survive a per-region view?")\
'''),
        code('''\
# 3 TEST: does the pattern survive another view?
# Draw the same measure faceted by region (small multiples). If the "recovery"
# claim holds overall but fails for a region, the overall chart compresses that.
def plot_recovery_by_region(transport: pd.DataFrame) -> None:
    """Small-multiple line charts: total riders per month, one panel per region.

    2x3 grid, shared y-axis in millions, panel titled by region.
    """
    # TODO
    raise NotImplementedError


plot_recovery_by_region(transport)\
'''),
        md("""\
**Reflect** (edit this cell): name one claim the overall chart supports that
the per-region view weakens, and one limitation (rung 4, BOUND) you would
attach before publishing either chart.\
"""),

        # ---- Exercise 3 ----
        md("""\
## Exercise 3. Audit a generated interpretation

Below is a fluent, confident, AI-style interpretation of the transport data.
Some of its claims are supported by the data you have; some are contradicted
by it; some *cannot be checked from this dataset at all*.

> "Public transport has fully recovered from the pandemic. Ridership across
> all modes now exceeds pre-COVID levels, driven primarily by the return of
> office workers to the Sydney CBD. Ferry patronage has been the most
> resilient mode throughout, and Western Sydney has overtaken Inner Sydney
> as the busiest region. The data shows that commuters strongly prefer rail
> over road-based transport."

**Task.** Classify each claim, then *prove* your classification for the
checkable ones with a query against `transport`.

- `"supported"`: the dataset agrees
- `"unsupported"`: the dataset disagrees
- `"unverifiable"`: this dataset cannot answer it either way\
"""),
        code('''\
claims = {
    "ridership across all modes now exceeds pre-COVID levels": "...",
    "the recovery is driven by office workers returning to the CBD": "...",
    "ferry patronage has been the most resilient mode throughout": "...",
    "Western Sydney has overtaken Inner Sydney as the busiest region": "...",
    "commuters strongly prefer rail over road-based transport": "...",
}

# TODO: replace each "..." with "supported", "unsupported", or "unverifiable".
# For each claim you mark supported/unsupported, add a query below that shows it.
# Example probe (compare 2025 with 2019, per mode):
# transport[transport["date"] >= pd.Timestamp("2025-01-01")].groupby("mode")["riders"].sum()\
'''),
        code('''\
# Verification: classification sanity check.
allowed = {"supported", "unsupported", "unverifiable"}
assert all(v in allowed for v in claims.values()), (
    "Every claim needs one of: supported / unsupported / unverifiable")

# The motive claim ("driven by office workers...") names a cause the dataset
# does not record; the preference claim infers psychology from counts.
for motive in ["the recovery is driven by office workers returning to the CBD",
               "commuters strongly prefer rail over road-based transport"]:
    assert claims[motive] == "unverifiable", (
        f"Re-read this claim: '{motive}': does ANY column in transport "
        "record causes or preferences?")
print("Classification accepted. Bring your probe queries to the studio discussion.")\
'''),
        md("""\
**The lesson.** The interpretation reads as insight. Two of its five claims
could never be checked from this data, yet nothing in the prose marks them as
different from the rest. That marking is *your* job, every time.\
"""),

        # ---- Exercise 4 ----
        md("""\
## Exercise 4. Make a true chart lie (then fix it)

Every number in a chart can be correct and the impression still wrong. You will
now build two misleading-but-accurate charts of Ferry ridership, then the
honest one. Knowing how the trick is done is the best defence against it.

- **Lie 1, truncated axis**, crop the y-axis so the post-COVID recovery looks
  like an explosion.
- **Lie 2, cherry-picked window**, show only a window in which ferries appear
  to be in permanent decline.
- **Honest**: zero baseline, full 2019–2025 window, title stating the finding.

Each function must **return the Axes object** so the verification cell can
inspect what your chart actually asserts.\
"""),
        code('''\
# Given: monthly Ferry riders across all regions (run, don't edit).
ferry = (transport[transport["mode"] == "Ferry"]
         .groupby("date")["riders"].sum())
ferry.tail()\
'''),
        code('''\
def lie_truncated(ferry: pd.Series):
    """Line chart of 2024-2025 Ferry riders with a savagely cropped y-axis,
    so a modest recovery reads as a boom. Title it like a press release.
    RETURN the Axes."""
    # TODO
    raise NotImplementedError


def lie_window(ferry: pd.Series):
    """Line chart of Ferry riders over a window of at most 18 months chosen
    so the series appears to be declining. Title it pessimistically.
    RETURN the Axes."""
    # TODO
    raise NotImplementedError


def honest(ferry: pd.Series):
    """The fair chart: full 2019-2025 window, y-axis from zero, title that
    states the actual finding (collapse and partial recovery).
    RETURN the Axes."""
    # TODO
    raise NotImplementedError


ax1, ax2, ax3 = lie_truncated(ferry), lie_window(ferry), honest(ferry)\
'''),
        code('''\
# Verification: the axes must actually commit each sin, and the honest
# chart must actually be honest.
assert ax1.get_ylim()[0] > ferry.min() * 0.5, (
    "Lie 1 isn't truncated enough: the y-axis floor should sit well above zero")
span_days = ax2.get_xlim()[1] - ax2.get_xlim()[0]
assert span_days < 560, "Lie 2's window is too wide to be a cherry-pick (<18 months)"
assert ax3.get_ylim()[0] <= 0, "The honest chart must include the zero baseline"
honest_span = ax3.get_xlim()[1] - ax3.get_xlim()[0]
assert honest_span > 2200, "The honest chart must show the full 2019-2025 window"
print("Two effective lies and one honest chart. Screenshot all three for the studio wall.")\
'''),
        md("""\
**Reflect** (edit this cell): which lie was harder to catch when you imagined
it in a news feed? What single sentence of disclosure would defuse each one?\
"""),

        # ---- Exercise 5 (stretch) ----
        md("""\
## Exercise 5 (stretch). Draw the uncertainty

The recovery chart from Exercise 2 shows one line per mode, each drawn with
total confidence. But the monthly values wobble. Show the wobble.

**Task.** For one mode, plot the 12-month rolling mean of riders with a shaded
band of ± one rolling standard deviation. The band is the honesty.\
"""),
        code('''\
def plot_with_uncertainty(transport: pd.DataFrame, mode: str = "Train"):
    """Rolling mean (12 months) of the mode's total riders with a
    +/- 1 rolling-std shaded band (ax.fill_between). RETURN the Axes."""
    # TODO
    raise NotImplementedError


ax_u = plot_with_uncertainty(transport)\
'''),
        code('''\
# Verification: a line and a band must both exist.
assert len(ax_u.lines) >= 1, "Where is the rolling-mean line?"
assert len(ax_u.collections) >= 1, "Where is the shaded uncertainty band (fill_between)?"
print("Uncertainty drawn rather than suppressed. Rung 4 of the ladder, made visible.")\
'''),
        DISCLOSURE,
        DISCLOSURE_ANSWER,
    ]
    save(cells, CLASSES / "01-seeing-data" / "notebooks" / "seeing_data_activities.ipynb")


WEAK_CHART = '''\
# The weak chart, run, then diagnose. (Deliberately bad. Do not fix this cell.)
latest = (transport[transport["date"] == pd.Timestamp("2025-12-01")]
          .groupby("region")["riders"].sum())
fig, ax = plt.subplots(figsize=(7, 7))
ax.pie(latest, labels=latest.index, autopct="%1.1f%%", startangle=90,
       colors=plt.cm.rainbow(np.linspace(0, 1, len(latest))),
       explode=[0.1] * len(latest), shadow=True)
ax.set_title("Transport!!!")
plt.show()\
'''


def build_visual_forms():
    cells = [
        md("""\
# Choosing Visual Forms, class notebook

**36104 Data Visualisation and Narratives · Week 2**

Good chart choice begins with the analytical task, not with the visual effect.
In this notebook you will feel the difference between encodings, reshape data
into the form charts want, classify tasks with the FT Visual Vocabulary, and
redesign a weak chart three ways.

## How to work in this notebook

Same contract as Week 1: an AI assistant is available but not required,
docstrings come first, and **nothing counts until its verification cell
passes**. The five wrangling checks from
the lecture: identifiers, row count, types, missing values, spot totals, 
appear here as executable assertions.\
"""),
        code(TRANSPORT_SETUP),

        # ---- Exercise 1 ----
        md("""\
## Exercise 1. Channels are read at different precision

The same five values, encoded five ways. Run the cell, then, *before any
computation*: estimate the ratio of value B to value D from each panel alone,
and record your five estimates.

Cleveland & McGill's ranking predicts your position estimate will be sharpest
and your area/colour estimates worst. Let's test that on you.\
"""),
        code('''\
# Run, then look, do not read the values from the code before estimating!
values = np.array([34, 87, 51, 29, 66])
labels = list("ABCDE")

fig, axes = plt.subplots(1, 5, figsize=(16, 3.2))
axes[0].scatter(values, labels, s=60, color="#18678f")          # position
axes[0].set_title("position"); axes[0].set_xlim(0, 100)
axes[1].barh(labels, values, color="#18678f")                    # length
axes[1].set_title("length"); axes[1].invert_yaxis()
axes[2].pie(values, labels=labels)                               # angle
axes[2].set_title("angle")
axes[3].scatter(range(5), [1] * 5, s=values * 40, color="#18678f")   # area
axes[3].set_title("area"); axes[3].set_yticks([])
for i, lab in enumerate(labels):
    axes[3].annotate(lab, (i, 1.005), ha="center")
axes[4].imshow([values], cmap="Blues", aspect="auto")            # colour value
axes[4].set_title("colour value"); axes[4].set_xticks(range(5))
axes[4].set_xticklabels(labels); axes[4].set_yticks([])
plt.tight_layout(); plt.show()\
'''),
        code('''\
# TODO: your estimates of the ratio B/D, one per encoding, purely by eye:
my_estimates = {
    "position": None,   # e.g. 3.0
    "length": None,
    "angle": None,
    "area": None,
    "colour value": None,
}

# Verification: scores your perceptual error per channel.
true_ratio = 87 / 29
assert all(v is not None for v in my_estimates.values()), "Estimate every panel first"
errors = {k: round(abs(v - true_ratio) / true_ratio * 100) for k, v in my_estimates.items()}
for channel, err in sorted(errors.items(), key=lambda kv: kv[1]):
    print(f"{channel:>13}: {err:3d}% off")
print(f"\\nTrue ratio B/D = {true_ratio:.2f}. "
      "Does your error ordering match the Cleveland & McGill ranking?")\
'''),

        # ---- Exercise 2 ----
        md("""\
## Exercise 2. Wide to tidy, with the five checks

Analysts receive spreadsheets shaped for humans: one row per region, one
column per year. Charts (and Tableau, and pandas plotting, and AI-generated
code) want **tidy** data: each variable a column, each observation a row.

**Task.** The cell below builds the wide table. Reshape it to tidy long form, 
ask your assistant, `pd.melt` is the move, then make the five verification
checks pass. Every assertion is one of the five checks from the lecture.\
"""),
        code('''\
# Build the wide table: annual riders per region (this cell is given).
annual = transport.assign(year=transport["date"].dt.year)
wide = (annual.groupby(["region", "year"])["riders"].sum()
        .unstack("year").reset_index())
wide.columns.name = None
wide\
'''),
        code('''\
def make_tidy(wide: pd.DataFrame) -> pd.DataFrame:
    """Reshape the wide region x year table to tidy long form.

    Returns a DataFrame with exactly three columns: region (str),
    year (int), riders (int), one row per region-year observation.
    """
    # TODO: pd.melt, then fix dtypes
    raise NotImplementedError


tidy = make_tidy(wide)
tidy.head()\
'''),
        code('''\
# Verification: the five wrangling checks, as assertions.
# 1 IDENTIFIERS: no regions invented or dropped.
assert set(tidy["region"]) == set(REGIONS), "Region identifiers changed in the reshape"
# 2 ROW COUNT, 6 regions x 7 years = 42 observations, exactly.
assert len(tidy) == 42, f"Expected 42 rows (6 regions x 7 years), got {len(tidy)}"
# 3 TYPES: year and riders must be integers, not strings.
assert tidy["year"].dtype.kind == "i", "year should be an integer column"
assert tidy["riders"].dtype.kind == "i", "riders should be an integer column"
# 4 MISSING: the reshape must not create NaNs.
assert tidy.notna().all().all(), "NaNs appeared during the reshape"
# 5 SPOT TOTAL, one hand-checkable value survives the round trip.
spot = tidy.query("region == 'Inner Sydney' and year == 2019")["riders"].iloc[0]
expected = transport[(transport["region"] == "Inner Sydney")
                     & (transport["date"] < pd.Timestamp("2020-01-01"))]["riders"].sum()
assert spot == expected, "Inner Sydney 2019 total does not survive the reshape"
print("IDENTIFIERS ✓ ROWS ✓ TYPES ✓ MISSING ✓ SPOT TOTAL ✓, tidy and trustworthy")\
'''),

        # ---- Exercise 3 ----
        md("""\
## Exercise 3. The Visual Vocabulary sort

Classify each analytical question into **one** FT Visual Vocabulary category:

`deviation` · `correlation` · `ranking` · `distribution` · `change over time`
· `magnitude` · `part-to-whole` · `spatial` · `flow`

Then pick one question and draft the chart for it from `tidy` or `transport`.\
"""),
        code('''\
sort = {
    "Which regions have the highest ridership?": "...",
    "How has ridership changed since 2019?": "...",
    "Do train and bus ridership move together across months?": "...",
    "What share of 2025 riders does each mode contribute?": "...",
    "Where on the network are riders concentrated?": "...",
    "How do commuters move between home regions and work regions?": "...",
}
# TODO: replace each "..." with one category (exact strings listed above).\
'''),
        code('''\
# Verification: checks your sort against the answer key (some questions
# genuinely admit one neighbouring alternative; those are accepted).
key = {
    "Which regions have the highest ridership?": {"ranking", "magnitude"},
    "How has ridership changed since 2019?": {"change over time"},
    "Do train and bus ridership move together across months?": {"correlation"},
    "What share of 2025 riders does each mode contribute?": {"part-to-whole"},
    "Where on the network are riders concentrated?": {"spatial"},
    "How do commuters move between home regions and work regions?": {"flow"},
}
wrong = {q for q, cat in sort.items() if cat not in key[q]}
assert not wrong, "Reconsider these questions:\\n- " + "\\n- ".join(sorted(wrong))
print("Sort accepted. Now draft one of these charts below.")\
'''),
        code('''\
# Draft one chart for a question of your choice from the sort above.
# Write the docstring stating the task and the category, then let your
# assistant draft the body, then apply the verification ladder yourself.
def chart_for_question() -> None:
    """<state the question>

    FT Visual Vocabulary category: <state the category>
    Form chosen and why: <one sentence>
    """
    # TODO
    raise NotImplementedError


chart_for_question()\
'''),

        # ---- Exercise 4 ----
        md("""\
## Exercise 4. Aspect ratio and baseline: same data, three impressions

The same series drawn in a wide frame, a tall frame, and as bars decides what
the reader feels before they think. None of these are "lies", but each frame
privileges a different reading, and one of them is conventional for a reason.

**Task.** Implement one plotting function that honours the `figsize` it is
given, then a bar chart that must start at zero. Compare the impressions.\
"""),
        code('''\
inner = (transport[transport["region"] == "Inner Sydney"]
         .groupby("date")["riders"].sum())


def plot_series(series: pd.Series, figsize: tuple):
    """Line chart of the series in a figure of exactly `figsize` inches.
    Label the y-axis in millions. RETURN the Axes."""
    # TODO
    raise NotImplementedError


def plot_annual_bars(tidy: pd.DataFrame):
    """Bar chart of Inner Sydney annual riders from `tidy`.
    Bars encode length, so the y-axis MUST start at zero. RETURN the Axes."""
    # TODO
    raise NotImplementedError


ax_wide = plot_series(inner, (12, 2))
ax_tall = plot_series(inner, (4, 6))
ax_bars = plot_annual_bars(tidy)\
'''),
        code('''\
# Verification: the frames must be what they claim, the bars must be honest.
assert tuple(ax_wide.get_figure().get_size_inches()) == (12, 2), (
    "plot_series must honour the figsize it is given (wide)")
assert tuple(ax_tall.get_figure().get_size_inches()) == (4, 6), (
    "plot_series must honour the figsize it is given (tall)")
assert ax_bars.get_ylim()[0] == 0, "Bars encode length: the axis must start at zero"
print("Same data, three impressions. Which frame would each stakeholder choose?")\
'''),
        md("""\
**Reflect** (edit this cell): the wide frame flattens the COVID collapse; the
tall frame makes it a cliff. Banking to ~45° is the conventional compromise, 
which claim does each frame quietly make?\
"""),

        # ---- Exercise 5 ----
        md("""\
## Exercise 5. Colour is an encoding

Three datasets, three palette decisions. Classify each scenario into the
palette family it needs, `sequential`, `diverging`, or `categorical`, then
prove one of them by drawing it.\
"""),
        code('''\
palette_choice = {
    "monthly ridership totals, low to high": "...",
    "percentage change in ridership vs the 2019 baseline (loss or gain)": "...",
    "the four transport modes on one chart": "...",
}
# TODO: replace each "..." with "sequential", "diverging", or "categorical".\
'''),
        code('''\
# Verification: palette families.
palette_key = {
    "monthly ridership totals, low to high": "sequential",
    "percentage change in ridership vs the 2019 baseline (loss or gain)": "diverging",
    "the four transport modes on one chart": "categorical",
}
wrong = [k for k, v in palette_choice.items() if v != palette_key[k]]
assert not wrong, "Reconsider: " + "; ".join(wrong)
print("Now prove the diverging one below.")\
'''),
        code('''\
def plot_change_heatmap(tidy: pd.DataFrame):
    """Heatmap of percentage change vs 2019, regions x years, with a
    DIVERGING colormap centred on zero (e.g. RdBu_r, vmin=-max, vmax=+max).
    RETURN the Axes."""
    # TODO: pivot tidy, compute pct change vs each region's 2019 value
    raise NotImplementedError


ax_h = plot_change_heatmap(tidy)\
'''),
        code('''\
# Verification: the colormap must actually be diverging and centred.
img = ax_h.get_images()[0] if ax_h.get_images() else None
assert img is not None, "Use imshow/pcolor-style heatmap so the colormap is inspectable"
assert img.get_cmap().name in {"RdBu", "RdBu_r", "coolwarm", "bwr", "seismic",
                               "PiYG", "PRGn", "BrBG", "RdYlBu", "RdYlBu_r"}, (
    f"'{img.get_cmap().name}' is not a diverging colormap")
lo, hi = img.get_clim()
assert abs(lo + hi) < max(abs(lo), abs(hi)) * 0.2, (
    "Centre the scale on zero: vmin and vmax should be symmetric")
print("Diverging, centred, honest. Loss and gain now read as different directions.")\
'''),

        # ---- Exercise 6 ----
        md("""\
## Exercise 6. Redesign ×3

Here is a deliberately weak chart: an exploded, shadowed, rainbow pie of six
nearly-ordered values, titled with an exclamation mark instead of a claim.

**Task.** Diagnose what task the reader actually has, then produce **three
redesigns, each serving a different Visual Vocabulary category** (for example:
`ranking`, `change over time`, `part-to-whole` done honestly). This is the
studio artefact for today, you will present one of the three.\
"""),
        code(WEAK_CHART),
        code('''\
def redesign_ranking() -> None:
    """Redesign 1: category: ranking.

    The reader's task: which regions have the most riders, in order?
    Form: sorted horizontal bar chart from a zero baseline, December 2025.
    Title states the finding, not the axes.
    """
    # TODO
    raise NotImplementedError


redesign_ranking()\
'''),
        code('''\
def redesign_change_over_time() -> None:
    """Redesign 2: category: change over time.

    The reader's task: how did each region's ridership move through COVID
    and recovery? Form: line chart or small multiples from `transport`.
    """
    # TODO
    raise NotImplementedError


redesign_change_over_time()\
'''),
        code('''\
def redesign_third(category: str) -> None:
    """Redesign 3: category: YOUR CHOICE (not ranking, not change over time).

    State the reader's task in one sentence here, choose an honest form,
    and pass the category you chose as `category`.
    """
    # TODO
    raise NotImplementedError


chosen_category = "..."  # TODO: e.g. "part-to-whole", "deviation", "distribution"
redesign_third(chosen_category)\
'''),
        code('''\
# Verification: three distinct categories, none of them the broken original's crime.
assert chosen_category not in {"...", "ranking", "change over time"}, (
    "Redesign 3 must use a category different from redesigns 1 and 2")
allowed = {"deviation", "correlation", "distribution", "magnitude",
           "part-to-whole", "spatial", "flow"}
assert chosen_category in allowed, f"'{chosen_category}' is not a Vocabulary category"
print("Three redesigns, three categories. For each, record: why this fits the "
      "task, what could mislead, and the simpler alternative you considered.")\
'''),
        md("""\
**Studio hand-off.** Pick your strongest redesign. In the studio you will
present it with the four-line justification:

```text
FT Visual Vocabulary category:
Why this fits the task:
What could mislead:
Simpler alternative considered:
```\
"""),
        DISCLOSURE,
        DISCLOSURE_ANSWER,
    ]
    save(cells, CLASSES / "02-visual-forms" / "notebooks" / "visual_forms_activities.ipynb")


if __name__ == "__main__":
    build_seeing_data()
    build_visual_forms()
