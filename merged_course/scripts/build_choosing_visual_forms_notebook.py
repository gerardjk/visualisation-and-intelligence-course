"""Build the single student notebook for Choosing Visual Forms."""

from copy import deepcopy
from pathlib import Path
import re

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = (
    ROOT
    / "merged_course"
    / "classes"
    / "02-visual-forms"
    / "notebooks"
    / "choosing_visual_forms.ipynb"
)
SOLUTION_OUTPUT = OUTPUT.with_name("choosing_visual_forms_solution.ipynb")


def md(source):
    return nbf.v4.new_markdown_cell(source.strip())


def code(source):
    return nbf.v4.new_code_cell(source.strip())


def build_solution(student_notebook):
    """Create the section-matched instructor solution from the student notebook."""
    notebook = deepcopy(student_notebook)
    notebook.cells[0].source = notebook.cells[0].source.replace(
        "# Choosing Visual Forms", "# Choosing Visual Forms — solution", 1
    ).replace(
        "This is the single notebook for the class.",
        "This is the instructor solution for the single class notebook.",
    )

    replacements = {
        "**Your intervention:** Remove both filled regions": r"""
**Example solution:** Without the fills, the reader must repeatedly estimate the
vertical gap between the two lines. Two fills make the sign immediately visible;
one neutral fill preserves difference magnitude but weakens the distinction between
surplus and deficit. Line position encodes the two values. Fill side/hue encodes the
sign of `exports - imports`.
""",
        "**Your intervention:** Remove the population colours": r"""
**Example solution:** Position alone still reveals the main sequence and the two
secondary clusters, although their boundaries are less explicit. The historical
diagram avoids suggesting that the populations are clean, known classes; the modern
colour version makes teaching the groups easier but adds a categorical interpretation.
""",
        "**Your intervention:** Sort the categories alphabetically": r"""
**Example solution:** Alphabetical order supports lookup by name. Magnitude order
supports the ranking question because adjacent positions represent adjacent ranks.
Dots retain the rank because common-scale position carries the value; a zero baseline
is mandatory for bar length but not for dot position.
""",
        "**Your intervention:** Sort the age bands alphabetically": r"""
**Example solution:** Alphabetical sorting destroys the ordinal age sequence, so the
silhouette no longer represents a distribution through age. The mirrored form makes
the overall shapes and sex difference at each age visible; grouped bars make exact
within-age comparisons easier but weaken the continuous silhouette.
""",
        "**Your intervention:** Plot only 2021 onward": r"""
**Example solution:** The short window enlarges the seasonal oscillation relative to
the visible vertical range and hides most of the long-run accumulation. The full
record makes the persistent rise dominant. Both use the same observations; the time
window changes the comparison the reader can make.
""",
        "**Your intervention:** Reconstruct the monthly totals as a polar area chart": r"""
**Example solution:** Similar months are harder to compare in the polar version
because readers compare areas at different angles rather than lengths on one baseline.
Stacking causes keeps the monthly total visible but adds a composition task: only the
bottom segment has a common baseline, so component magnitudes are less precise.
""",
        "**Your intervention:** Recreate the shares as a single 100% stacked bar": r"""
**Example solution:** The 100% stacked bar makes European versus African easier because
the shares are read as lengths, although only the first segment begins at zero. Use
part-to-whole when the common denominator matters; use ranked bars when comparing the
individual category values is the primary task.
""",
        "**Your intervention:** Shade by raw `enrolled` counts": r"""
**Example solution:** Mapping raw counts makes high-population regions dark even when
their enrolment proportion is ordinary. Rates support regional comparison. Five
classes suppress within-class differences and introduce abrupt visual boundaries at
the chosen thresholds.
""",
        "**Your intervention:** Give every route segment the same line width": r"""
**Example solution:** Equal width removes troop strength, a quantitative ratio field
encoded by line width. Removing colour makes advance and retreat, a nominal direction
field, harder to distinguish; route position and sequence still show movement.
""",
        "Choose one audience: transport operations manager": r"""
## Audience and question

- **Audience:** transport operations manager
- **Question:** Which mode carries the most passengers overall in 2025?
- **Decision supported:** Where should capacity monitoring be prioritised?
- **Likely Visual Vocabulary family:** magnitude, with ranking through sorting
""",
        "Complete the table before drawing anything.": r"""
## Field combinations and task families

| Question | Fields and data types | Required comparison | Task family |
|---|---|---|---|
| Which mode carries the most passengers overall? | mode: nominal; passengers: ratio | absolute totals and ordered position | magnitude / ranking |
| How does use change through the year? | month: temporal; passengers: ratio | trend and turning points | change over time |
| Do months with more passengers also have longer delays? | passengers: ratio; delay: ratio | paired association | correlation |
| Which mode has the most variable delays? | mode: nominal; delay: ratio | spread and outliers by group | distribution |
| How is total patronage divided among modes? | mode: nominal; passengers: ratio parts of one total | share of total | part-to-whole |
""",
        "## Compare, select and reject": r"""
## Compare, select and reject — example

| Candidate | Question answered | Easy comparison | Information hidden | Audience risk |
|---|---|---|---|---|
| Ranked bars | Which mode carries most passengers? | totals and order | monthly variation and missing month | aggregation can conceal seasonal pressure |
| Lines | How does patronage change? | trend and turning points | precise overall rank | line continuity may overstate an isolated missing value |
| Scatterplot | Are passengers and delay associated? | paired association and outliers | temporal sequence | association may be read as causation |

- **Selected form:** ranked horizontal bars.
- **Why it fits:** the operations manager's stated question requires total magnitude and order.
- **Plausible alternative rejected:** line chart.
- **Reason:** it answers a change-over-time question rather than the stated total-capacity question.
- **Remaining limitation:** annual aggregation hides monthly peaks and the missing train observation.
""",
        "## Explain and disclose": r"""
## Explain and disclose — example

In the reshape, each `melt` changes twelve source rows into thirty-six
month–mode observations. `pd.to_numeric` changes passenger strings to a numeric
type while retaining `..` as missing. The `groupby` and sort determine the
comparison in the ranked-bar candidate. A new mode would require matching passenger
and delay column names; the chart loop and colour dictionary would also need a colour.

- **Tool used:** example AI coding assistant.
- **Contribution:** proposed the two `melt` operations and first chart draft.
- **Accepted, modified or rejected:** retained the reshape; added explicit missing-value handling, `min_count=1`, labels and a zero baseline.
- **Verification:** ran the assertions, checked the September bus value manually and inspected all axes and missing values.
- **Remaining limitations:** synthetic data; no operational or causal claim can be generalised beyond the exercise.
""",
    }

    tidy_solution = r"""
passenger_cols = [c for c in messy.columns if c.endswith(" passengers")]
delay_cols = [c for c in messy.columns if c.endswith(" delay min")]

passengers = messy.melt(
    id_vars="Month", value_vars=passenger_cols,
    var_name="source", value_name="passengers",
)
passengers["mode"] = passengers["source"].str.removesuffix(" passengers")
passengers["passengers"] = pd.to_numeric(
    passengers["passengers"].str.replace(",", "", regex=False).replace("..", np.nan),
    errors="coerce",
)

delays = messy.melt(
    id_vars="Month", value_vars=delay_cols,
    var_name="source", value_name="average_delay_minutes",
)
delays["mode"] = delays["source"].str.removesuffix(" delay min")

tidy = passengers[["Month", "mode", "passengers"]].merge(
    delays[["Month", "mode", "average_delay_minutes"]],
    on=["Month", "mode"], validate="one_to_one",
)
tidy["month"] = pd.to_datetime(tidy.pop("Month"), format="%b-%Y")
tidy = tidy[["month", "mode", "passengers", "average_delay_minutes"]]
tidy.head()
"""
    chart_solution = r"""
mode_colours = {"Bus": "#18678f", "Train": "#e66852", "Ferry": "#30a8b1"}

totals = (tidy.groupby("mode", as_index=False)["passengers"]
          .sum(min_count=1).sort_values("passengers"))
fig, ax_rank = plt.subplots(figsize=(7, 4))
ax_rank.barh(totals["mode"], totals["passengers"],
             color=[mode_colours[m] for m in totals["mode"]])
ax_rank.set(xlabel="passengers", title="Train carries the most passengers in 2025")
ax_rank.set_xlim(left=0)
plt.show()

fig, ax_change = plt.subplots(figsize=(9, 4.5))
for mode, group in tidy.groupby("mode", sort=False):
    ax_change.plot(group["month"], group["passengers"], marker="o",
                   color=mode_colours[mode], label=mode)
ax_change.set(xlabel="month", ylabel="passengers",
              title="Monthly patronage varies by transport mode")
ax_change.legend(frameon=False)
plt.show()

fig, ax_corr = plt.subplots(figsize=(7, 5))
for mode, group in tidy.groupby("mode", sort=False):
    valid = group.dropna(subset=["passengers", "average_delay_minutes"])
    ax_corr.scatter(valid["passengers"], valid["average_delay_minutes"],
                    color=mode_colours[mode], label=mode, s=45, alpha=0.8)
ax_corr.set(xlabel="passengers", ylabel="average delay (minutes)",
            title="Passenger volume and delay by mode")
ax_corr.legend(frameon=False)
plt.show()

assert ax_rank.get_xlim()[0] == 0
assert len(ax_change.lines) == 3
assert len(ax_corr.collections) == 3
print("✓ ranked magnitude, temporal change and paired association views verified")
"""

    synthesis = r"""
## Synthesis: from data type to visual vocabulary — example

| Reconstruction | Field types / roles | Task | Main channels | Difference from the original |
|---|---|---|---|---|
| Playfair exports/imports | time + two numeric measures + reference | deviation | position, line, filled difference | simplified representative values and modern colour |
| Russell | ordered spectral proxy + numeric magnitude | correlation | paired position | simulated points and categorical population colours |
| Playfair bars | category + numeric total | ranking | ordered position and length | representative values and one combined total |
| Age–sex plate | ordinal age + numeric count + nominal sex | distribution | mirrored length and position | representative values and one summary panel |
| Keeling | time + numeric measure | change over time | connected position | modern code styling; measured source data retained |
| Nightingale | month + numeric mortality rates + cause | magnitude | common-scale length in reconstruction | bars replace the original polar-area encoding |
| Playfair pie | category + shares of one total | part-to-whole | angle and area | approximate shares and modern labels |
| Dupin | spatial region + numeric rate | spatial | position and lightness | abstract grid rather than French geometry |
| Minard | source/target route + weight + sequence | flow | position, direction, width and colour | simplified transcription and geography |
"""

    for cell in notebook.cells:
        source = cell.get("source", "")
        if cell.cell_type == "code" and source.startswith("# TODO: reshape messy"):
            cell.source = tidy_solution.strip()
            continue
        if cell.cell_type == "code" and source.startswith("mode_colours =") and "candidate_magnitude" in source:
            cell.source = chart_solution.strip()
            continue
        if cell.cell_type == "markdown" and source.startswith("## Synthesis"):
            cell.source = synthesis.strip()
            continue
        if cell.cell_type == "markdown":
            for marker, replacement in replacements.items():
                if marker in source:
                    cell.source = replacement.strip()
                    break

    return notebook


def build():
    cells = [
        md(r"""
# Choosing Visual Forms

**36104 Data Visualisation and Narratives · Choosing Visual Forms**

This is the single notebook for the class. Part 1 reconstructs the visual logic
of the nine original examples. Part 2 applies the same reasoning to data types,
tidy data and chart selection.

These are **analytic reconstructions, not facsimiles**. The sources differ:

| Chart | Notebook input | Status |
|---|---|---|
| Playfair exports/imports time series | representative trade series | deviation exercise, not digitised 1786 values |
| Russell diagram | simulated star sample | pattern exercise, not measured stars |
| Playfair bar chart | representative trade values | ranking exercise, not digitised 1786 values |
| 1874 age–sex plate | representative age bands | distribution exercise, not digitised 1874 values |
| Keeling curve | NOAA/Scripps monthly CO₂ | measured observations |
| Nightingale mortality diagram | representative monthly rates | magnitude exercise, not digitised 1858 values |
| Playfair pie chart | approximate historical shares | part-to-whole exercise |
| Dupin choropleth | representative regional rates | normalisation and spatial-pattern exercise |
| Minard map | simplified course transcription | approximate route and troop counts |

For each chart: run the reconstruction, verify it, then change one consequential
design decision. Do not describe a simulated or representative value as observed.
"""),
        code(r"""
# Setup: run this cell without editing it.
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import numpy as np
import pandas as pd


def find_notebook_dir():
    # Find this notebook's folder from common launch locations.
    candidates = [
        Path.cwd(),
        Path.cwd() / "merged_course/classes/02-visual-forms/notebooks",
        Path.cwd().parent / "notebooks",
    ]
    for candidate in candidates:
        if (candidate / "data").is_dir():
            return candidate.resolve()
    raise FileNotFoundError(
        "Cannot find the data folder. Launch the notebook from the course repository "
        "or keep the data folder beside the notebook."
    )


NOTEBOOK_DIR = find_notebook_dir()
DATA = NOTEBOOK_DIR / "data"
ORIGINALS = (NOTEBOOK_DIR / "../../../shared/assets/originals").resolve()

plt.rcParams.update({
    "figure.figsize": (9, 5),
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.22,
    "font.size": 11,
})

print("Notebook folder:", NOTEBOOK_DIR)
print("Data files:", sorted(path.name for path in DATA.glob("*.csv")))
"""),
        md(r"""
## 1 · Russell's stellar diagram: correlation

![Russell's 1914 diagram](../../../shared/assets/originals/russell-1914.png)

Russell's published diagram places **spectral class** on the horizontal axis and
**absolute magnitude** on the vertical axis. Magnitude is historically awkward:
more negative means brighter, so the axis must run from bright at the top to dim
at the bottom.

The supplied points below are simulated to reproduce the main visual populations.
They are not measurements and must not be cited as a star catalogue.
"""),
        code(r"""
# Build a deterministic teaching sample with three stellar populations.
rng = np.random.default_rng(36104)
classes = np.array(list("BAFGKM"))

n_main = 220
x_main = rng.uniform(0, 5, n_main)
mag_main = -2.8 + 2.45 * x_main + rng.normal(0, 0.65, n_main)

n_giant = 45
x_giant = rng.uniform(2.8, 5.0, n_giant)
mag_giant = rng.normal(-0.8, 0.75, n_giant)

n_white = 35
x_white = rng.uniform(0.0, 2.4, n_white)
mag_white = rng.normal(10.0, 1.0, n_white)

hr = pd.DataFrame({
    "spectral_position": np.r_[x_main, x_giant, x_white],
    "absolute_magnitude": np.r_[mag_main, mag_giant, mag_white],
    "population": (["main sequence"] * n_main
                   + ["giant"] * n_giant
                   + ["white dwarf"] * n_white),
})

fig, ax = plt.subplots(figsize=(7.0, 6.0))
for label, group in hr.groupby("population", sort=False):
    ax.scatter(group["spectral_position"], group["absolute_magnitude"],
               s=18, alpha=0.62, label=label)

ax.set_xticks(range(len(classes)), classes)
ax.set_xlim(-0.35, 5.35)
ax.set_ylim(13.5, -4.5)  # reverse magnitude: brighter stars are higher
ax.set_xlabel("spectral class (hot → cool)")
ax.set_ylabel("absolute magnitude (bright → dim)")
ax.set_title("Russell diagram: a teaching reconstruction")
ax.legend(frameon=False)
plt.show()
"""),
        code(r"""
# Verification: the reconstruction keeps the unusual axis semantics explicit.
assert list(classes) == ["B", "A", "F", "G", "K", "M"]
assert ax.get_ylim()[0] > ax.get_ylim()[1], "Magnitude axis must run bright-to-dim."
assert set(hr["population"]) == {"main sequence", "giant", "white dwarf"}
print("✓ spectral order, reversed magnitude axis and three simulated populations verified")
"""),
        md(r"""
**Your intervention:** Remove the population colours and legend. Can position alone
still reveal the three groups? Write one sentence explaining what the original gains
or loses by not using modern categorical colour.
"""),
        md(r"""
## 2 · The Keeling curve: change over time

![NOAA/Scripps full Mauna Loa record](../../../shared/assets/originals/keeling-curve-noaa-2026-08-05.png)

This section uses NOAA's downloadable monthly data. `average` retains the seasonal
saw-tooth; `deseasonalized` exposes the underlying trend. Missing early metadata are
negative sentinel values in other columns, so we select only the fields we need.
"""),
        code(r"""
co2 = pd.read_csv(DATA / "co2_mm_mlo.csv", comment="#")
co2["date"] = pd.to_datetime(dict(year=co2["year"], month=co2["month"], day=15))

fig, ax = plt.subplots(figsize=(10, 5.2))
ax.plot(co2["date"], co2["average"], color="#d73027", lw=0.9,
        label="monthly mean")
ax.plot(co2["date"], co2["deseasonalized"], color="#171717", lw=1.35,
        label="seasonally adjusted")
ax.set_xlabel("year")
ax.set_ylabel("atmospheric CO₂ (ppm)")
ax.set_title("Atmospheric CO₂ at Mauna Loa Observatory")
ax.legend(frameon=False)
plt.show()
"""),
        code(r"""
assert co2["date"].is_monotonic_increasing
assert co2["average"].notna().all()
assert co2.loc[co2["year"] == 1958, "average"].mean() < 320
assert co2.loc[co2["year"] == 2025, "average"].mean() > 420
print(f"✓ {len(co2):,} monthly observations; date order and endpoints verified")
"""),
        md(r"""
**Your intervention:** Plot only 2021 onward, then return to the full record. Explain
how the shorter window changes the apparent relative importance of seasonality and
long-run rise. The data do not change; the argument does.
"""),
        md(r"""
## 3 · Minard's march: spatial + flow

![Minard's 1869 flow map](../../../shared/assets/originals/minard-1869.png)

The original combines geography, direction, troop strength and retreat temperature.
The course transcription below is deliberately simplified: it is enough to recover
the encoding logic but not to make historical estimates from individual points.
"""),
        code(r"""
route = pd.DataFrame({
    "longitude": [24.0, 26.8, 28.5, 30.2, 33.2, 36.0, 37.6,
                  37.6, 36.0, 33.2, 30.2, 28.5, 26.8, 24.0],
    "latitude":  [54.9, 54.8, 54.9, 55.1, 54.8, 55.0, 55.8,
                  55.8, 55.0, 54.8, 55.1, 54.9, 54.8, 54.9],
    "survivors_thousands": [340, 300, 280, 240, 180, 145, 100,
                            100, 90, 55, 40, 30, 20, 10],
    "direction": ["advance"] * 7 + ["retreat"] * 7,
})
temperature = pd.DataFrame({
    "longitude": [37.6, 36.0, 33.2, 30.2, 28.5, 26.8, 24.0],
    "temperature_c": [0, -9, -21, -11, -20, -24, -26],
})

fig, (ax_map, ax_temp) = plt.subplots(
    2, 1, figsize=(10, 6.2), sharex=True,
    gridspec_kw={"height_ratios": [3, 1], "hspace": 0.06},
)

colours = {"advance": "#c7a35a", "retreat": "#3a3a3a"}
for direction, group in route.groupby("direction", sort=False):
    group = group.reset_index(drop=True)
    for i in range(len(group) - 1):
        pair = group.iloc[i:i + 2]
        ax_map.plot(pair["longitude"], pair["latitude"],
                    color=colours[direction], solid_capstyle="round",
                    lw=max(1.2, pair.iloc[0]["survivors_thousands"] / 13),
                    alpha=0.92)
ax_map.text(24.0, 54.65, "Kaunas", ha="center")
ax_map.text(37.6, 56.05, "Moscow", ha="center")
ax_map.set_ylabel("latitude (°N)")
ax_map.set_title("Napoleon's 1812 campaign: simplified Minard reconstruction")

ax_temp.plot(temperature["longitude"], temperature["temperature_c"],
             "o-", color="#4269d0", lw=1.5)
for row in temperature.itertuples(index=False):
    ax_temp.annotate(f"{row.temperature_c}°", (row.longitude, row.temperature_c),
                     xytext=(0, -14), textcoords="offset points", ha="center", fontsize=9)
ax_temp.set_xlabel("longitude (°E)")
ax_temp.set_ylabel("°C")
plt.show()
"""),
        code(r"""
assert route.iloc[0]["survivors_thousands"] == 340
assert route.iloc[-1]["survivors_thousands"] == 10
assert set(route["direction"]) == {"advance", "retreat"}
assert temperature["temperature_c"].min() == -26
print("✓ direction, declining band width and linked retreat temperature verified")
"""),
        md(r"""
**Your intervention:** Give every route segment the same line width. What variable
disappears? Then restore width and remove colour. Which distinction is now harder?
Name the data type and visual channel in each answer.
"""),
        md(r"""
## 4 · Playfair's exports and imports: deviation

![Playfair's 1786 time series](../../../shared/assets/originals/playfair-timeseries-1786.png)

Playfair compares two series and labels the balance as being against or in favour
of England. The filled difference is the deviation encoding. The values below are
representative teaching values, not a digitisation of the original plate.
"""),
        code(r"""
years = np.arange(1700, 1781)
t = years - years.min()
imports = 76 + 0.22 * t + 8 * np.sin(t / 8)
exports = 48 + 0.42 * t + 0.035 * np.maximum(t - 48, 0) ** 2 + 6 * np.sin(t / 7 + 1)
balance = pd.DataFrame({"year": years, "exports": exports, "imports": imports})

fig, ax = plt.subplots(figsize=(10, 5.2))
ax.plot(balance["year"], balance["exports"], color="#a23b4a", lw=2, label="exports")
ax.plot(balance["year"], balance["imports"], color="#c78b23", lw=2, label="imports")
ax.fill_between(balance["year"], balance["exports"], balance["imports"],
                where=balance["exports"] >= balance["imports"],
                color="#7aa974", alpha=0.35, label="balance in favour")
ax.fill_between(balance["year"], balance["exports"], balance["imports"],
                where=balance["exports"] < balance["imports"],
                color="#c86b6b", alpha=0.32, label="balance against")
ax.set(xlabel="year", ylabel="representative trade value",
       title="Exports, imports and signed balance: Playfair reconstruction")
ax.legend(frameon=False, ncol=2)
plt.show()
"""),
        code(r"""
signed_difference = balance["exports"] - balance["imports"]
assert balance["year"].is_monotonic_increasing
assert (signed_difference < 0).any() and (signed_difference > 0).any()
assert np.allclose(signed_difference, balance["exports"] - balance["imports"])
print("✓ ordered years and signed difference on both sides of the reference verified")
"""),
        md(r"""
**Your intervention:** Remove both filled regions, then restore them and replace the
two fills with one neutral colour. Which version makes the sign of the balance easiest
to recover? State what the line position and fill hue each encode.
"""),
        md(r"""
## 5 · The mirrored age–sex form: distribution

![Walker's 1874 age-and-sex distribution of deaths](../../../shared/assets/originals/walker-1874-age-sex-deaths.jpg)

The 1874 plate shows the age and sex distribution **of deaths**. It is an early
example of the mirrored age–sex silhouette later used for population counts. The
values below are representative teaching data, not a digitisation of that plate.
"""),
        code(r"""
age_distribution = pd.DataFrame({
    "age": ["0–9", "10–19", "20–29", "30–39", "40–49",
            "50–59", "60–69", "70–79", "80+"],
    "male": [98, 94, 88, 80, 70, 56, 40, 24, 10],
    "female": [94, 90, 86, 79, 71, 59, 45, 30, 16],
})
y = np.arange(len(age_distribution))

fig, ax = plt.subplots(figsize=(8, 5.5))
ax.barh(y, -age_distribution["male"], color="#4269d0", label="male")
ax.barh(y, age_distribution["female"], color="#ff725c", label="female")
ax.set_yticks(y, age_distribution["age"])
ax.set_xlabel("representative count (thousands)")
ticks = ax.get_xticks()
ax.set_xticks(ticks, [f"{abs(int(tick))}" for tick in ticks])
ax.axvline(0, color="#333333", lw=0.8)
ax.set_title("Mirrored age distribution: teaching reconstruction")
ax.legend(frameon=False)
plt.show()
"""),
        code(r"""
assert (age_distribution[["male", "female"]] >= 0).all().all()
assert (ax.patches[0].get_width() < 0) and (ax.patches[-1].get_width() > 0)
assert len(age_distribution) == 9
print("✓ non-negative source values, mirrored signs and nine age bands verified")
"""),
        md(r"""
**Your intervention:** Sort the age bands alphabetically. Why is the resulting chart
invalid even though every number remains correct? Restore semantic age order, then
compare grouped bars with the mirrored form: which comparison does each make easier?
"""),
        md(r"""
## 6 · Playfair's bar chart: ranking

![Playfair's 1786 bar chart](../../../shared/assets/originals/playfair-bar-1786.jpg)

Playfair orders Scottish trade partners by magnitude. The values below are
representative teaching values, not a digitisation of the original plate. Sorting
turns a magnitude display into a direct ranking display.
"""),
        code(r"""
trade_rank = pd.DataFrame({
    "place": ["Ireland", "Poland", "Portugal", "Holland", "Sweden",
              "Germany", "Flanders", "West Indies", "America", "Russia"],
    "exports": [8, 4, 12, 16, 10, 26, 42, 118, 135, 155],
    "imports": [5, 2, 7, 9, 6, 18, 31, 105, 92, 126],
})
trade_rank["total_trade"] = trade_rank["exports"] + trade_rank["imports"]
trade_rank = trade_rank.sort_values("total_trade", ascending=True)

fig, ax = plt.subplots(figsize=(9, 5.8))
ax.barh(trade_rank["place"], trade_rank["total_trade"], color="#222222")
ax.set_xlim(left=0)
ax.set_xlabel("representative total trade value")
ax.set_title("Scottish trade partners ranked by total trade")
plt.show()
"""),
        code(r"""
assert ax.get_xlim()[0] == 0
assert trade_rank["total_trade"].is_monotonic_increasing
assert np.allclose(trade_rank["total_trade"], trade_rank["exports"] + trade_rank["imports"])
print("✓ total calculated, categories sorted and zero baseline verified")
"""),
        md(r"""
**Your intervention:** Sort the categories alphabetically, then restore the magnitude
order. Which question does each order support? Replace bars with dots and state whether
the ranking remains legible without a zero baseline.
"""),
        md(r"""
## 7 · Nightingale's mortality diagram: magnitude

![Nightingale's 1858 mortality diagram](../../../shared/assets/originals/nightingale-mortality-1858.jpg)

Nightingale compares monthly mortality rates by cause using polar areas. The values
below are representative teaching values, not a digitisation of the original plate.
The reconstruction lets you compare an area encoding with a more precise common-scale
length encoding.
"""),
        code(r"""
mortality = pd.DataFrame({
    "month": ["Apr", "May", "Jun", "Jul", "Aug", "Sep",
              "Oct", "Nov", "Dec", "Jan", "Feb", "Mar"],
    "preventable_disease": [80, 95, 120, 160, 210, 245, 225, 190, 150, 125, 105, 90],
    "wounds": [18, 22, 28, 35, 40, 38, 32, 26, 22, 20, 18, 16],
    "other": [12, 14, 16, 20, 24, 22, 20, 18, 16, 14, 12, 11],
})
mortality["total_rate"] = mortality[["preventable_disease", "wounds", "other"]].sum(axis=1)

fig, ax = plt.subplots(figsize=(9, 5.8))
ax.bar(mortality["month"], mortality["total_rate"], color="#8bb8c8")
ax.set_ylim(bottom=0)
ax.set_ylabel("representative mortality rate")
ax.set_title("Monthly mortality magnitude: Nightingale reconstruction")
plt.show()
"""),
        code(r"""
assert ax.get_ylim()[0] == 0
assert (mortality.select_dtypes("number") >= 0).all().all()
assert np.allclose(
    mortality["total_rate"],
    mortality[["preventable_disease", "wounds", "other"]].sum(axis=1),
)
print("✓ non-negative component rates, verified totals and zero baseline")
"""),
        md(r"""
**Your intervention:** Reconstruct the monthly totals as a polar area chart. Which
months are harder to compare than in the bars? Keep the causes separate with stacked
bars and state whether the task has shifted from magnitude toward part-to-whole.
"""),
        md(r"""
## 8 · Playfair's pie chart: part-to-whole

![Playfair's 1801 pie chart](../../../shared/assets/originals/playfair-pie-1801.jpg)

Playfair's *Statistical Breviary* included the earliest generally credited pie
charts. This simplified reconstruction uses approximate shares for the Turkish
Empire's area by continent; it teaches the whole-equals-100% constraint rather than
claiming to reproduce the historical estimates.
"""),
        code(r"""
territory = pd.Series({"Asiatic": 0.66, "European": 0.25, "African": 0.09})

fig, ax = plt.subplots(figsize=(6.5, 6.5))
ax.pie(territory, labels=territory.index, autopct="%1.0f%%", startangle=205,
       colors=["#c7a35a", "#6b8fb3", "#d98262"],
       wedgeprops={"edgecolor": "white", "linewidth": 1.2})
ax.set_title("Territorial share: Playfair reconstruction")
plt.show()
"""),
        code(r"""
assert np.isclose(territory.sum(), 1.0)
assert (territory >= 0).all()
assert territory.index.is_unique
print("✓ mutually exclusive, non-negative shares sum to one")
"""),
        md(r"""
**Your intervention:** Recreate the shares as a single 100% stacked bar. Which form
makes the smaller European-versus-African comparison easier? State when part-to-whole
is genuinely the task and when a ranked bar would be more honest.
"""),
        md(r"""
## 9 · Dupin's choropleth: spatial

![Charles Dupin's 1826 choropleth](../../../shared/assets/originals/dupin-choropleth-1826.jpg)

Dupin shaded French departments by a regional education measure. This reconstruction
uses an abstract teaching geography and representative enrolment counts. The crucial
operation is real: calculate a comparable **rate** before mapping ordered lightness.
"""),
        code(r"""
rng = np.random.default_rng(1826)
cells = [(2, 0), (3, 0), (4, 0),
         (1, 1), (2, 1), (3, 1), (4, 1), (5, 1),
         (1, 2), (2, 2), (3, 2), (4, 2), (5, 2),
         (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3),
         (1, 4), (2, 4), (3, 4), (4, 4),
         (2, 5), (3, 5)]
regions = pd.DataFrame(cells, columns=["x", "y"])
regions["school_age_population"] = rng.integers(18_000, 82_000, len(regions))
north_effect = 0.12 + 0.055 * regions["y"]
regions["enrolled"] = (
    regions["school_age_population"]
    * np.clip(north_effect + rng.normal(0, 0.035, len(regions)), 0.05, 0.55)
).round().astype(int)
regions["enrolment_rate"] = regions["enrolled"] / regions["school_age_population"]

norm_map = Normalize(regions["enrolment_rate"].min(), regions["enrolment_rate"].max())
cmap_map = plt.get_cmap("Greys_r")
fig, ax = plt.subplots(figsize=(7.5, 7))
for row in regions.itertuples(index=False):
    patch = plt.Rectangle((row.x, row.y), 1, 1,
                          facecolor=cmap_map(norm_map(row.enrolment_rate)),
                          edgecolor="white", linewidth=1.4)
    ax.add_patch(patch)
ax.set(xlim=(-0.15, 6.15), ylim=(-0.15, 6.15), aspect="equal")
ax.set_xticks([]); ax.set_yticks([])
ax.set_title("Regional education rate: Dupin choropleth reconstruction")
sm = plt.cm.ScalarMappable(norm=norm_map, cmap=cmap_map)
fig.colorbar(sm, ax=ax, shrink=0.68, label="enrolment rate")
plt.show()
"""),
        code(r"""
assert regions["enrolment_rate"].between(0, 1).all()
assert np.allclose(
    regions["enrolment_rate"],
    regions["enrolled"] / regions["school_age_population"],
)
assert regions.groupby("y")["enrolment_rate"].mean().iloc[-1] > regions.groupby("y")["enrolment_rate"].mean().iloc[0]
print("✓ regional counts normalised to comparable rates before ordered shading")
"""),
        md(r"""
**Your intervention:** Shade by raw `enrolled` counts instead of `enrolment_rate`.
Which large-population regions become misleadingly dark? Restore the rate, then try
five discrete classes. Which spatial differences disappear at the class boundaries?
"""),
        md(r"""
## Synthesis: from data type to visual vocabulary

Complete this table in your own words.

| Reconstruction | Field types / roles | Visual Vocabulary task | Channels doing the work | What the original does that your code does not |
|---|---|---|---|---|
| Russell | … | correlation | … | … |
| Keeling | … | change over time | … | … |
| Minard | … | flow | … | … |
| Playfair exports/imports | … | deviation | … | … |
| Age–sex plate | … | distribution | … | … |
| Playfair bars | … | ranking | … | … |
| Nightingale | … | magnitude | … | … |
| Playfair pie | … | part-to-whole | … | … |
| Dupin | … | spatial | … | … |

### AI disclosure

- **Tool contributed:** …
- **How I checked it:** …
- **What I wrote or decided:** …
- **What I would not trust the tool to do here:** …
"""),
        md(r"""
## Sources and reuse notes

- H. N. Russell, “Relations between the Spectra and Other Characteristics of the Stars,” *Nature* 93 (1914), 252–258. Historical diagram scan via Paris Observatory / ASM.
- X. Lan, NOAA Global Monitoring Laboratory, and R. Keeling, Scripps Institution of Oceanography, Mauna Loa monthly CO₂ record. Data snapshot created 5 August 2026.
- C. J. Minard, *Carte figurative des pertes successives en hommes de l'Armée Française dans la campagne de Russie 1812–1813* (1869), public domain.
- W. Playfair, exports and imports of Denmark and Norway (1786), public domain.
- F. A. Walker, 1874 plate showing distribution by age and sex of deaths. Library of Congress Geography and Map Division; public domain.
- W. Playfair, Scottish exports and imports bar chart (1786), public domain.
- F. Nightingale, *Diagram of the Causes of Mortality in the Army in the East* (1858), public domain.
- W. Playfair, Turkish Empire pie chart, *Statistical Breviary* (1801), public domain.
- C. Dupin, *Carte figurative de l'instruction populaire de la France* (1826), Bibliothèque nationale de France; public domain.
"""),
        md(r"""
# Part 2 · Apply the framework

Use one deliberately messy transport dataset to move through the complete class
workflow:

```text
data types → field combinations → required comparison → task family → visual form
```

The values are synthetic teaching data. Missing values and numeric strings are
intentional and must not be cleaned silently.
"""),
        md(r"""
## Audience and question

Choose one audience: transport operations manager, public information officer,
accessibility advocate or data journalist.

Complete these before naming a chart:

- **Audience:**
- **Question:**
- **Decision supported:**
- **Likely Visual Vocabulary family:**
"""),
        code(r"""
# Build the deliberately messy wide table. Run without editing.
rng = np.random.default_rng(36104)
months = pd.date_range("2025-01-01", periods=12, freq="MS")
messy = pd.DataFrame({
    "Month": months.strftime("%b-%Y"),
    "Bus passengers": rng.integers(820, 1280, 12).astype(str),
    "Train passengers": rng.integers(1050, 1650, 12).astype(str),
    "Ferry passengers": rng.integers(180, 430, 12).astype(str),
    "Bus delay min": np.round(rng.normal(7.5, 1.6, 12), 1),
    "Train delay min": np.round(rng.normal(5.5, 1.2, 12), 1),
    "Ferry delay min": np.round(rng.normal(4.0, 1.0, 12), 1),
})
messy.loc[4, "Train passengers"] = ".."
messy.loc[8, "Bus passengers"] = "1,204"
messy.loc[10, "Ferry delay min"] = np.nan
messy
"""),
        md(r"""
## Data types and tidy structure

Before writing code, record the data type and semantic role of every source field.
Then predict the tidy result:

- expected row count;
- expected unique modes;
- missing values that should remain;
- target type of `month`, `mode`, `passengers` and `average_delay_minutes`.

The tidy dataset must contain one observation per month and transport mode with
exactly these columns:

```text
month · mode · passengers · average_delay_minutes
```
"""),
        code(r"""
# TODO: reshape messy into a DataFrame named tidy.
# Requirements:
# - treat '..' as missing, not zero
# - remove thousands separators before numeric conversion
# - parse Month as a datetime
# - preserve missing delay and passenger values
# - create exactly the four specified columns
# - do not impute or aggregate
"""),
        code(r"""
# Verification: identifiers, rows, types, missing values and a spot check.
assert tidy.shape == (36, 4), "Expected 12 months × 3 modes."
assert list(tidy.columns) == ["month", "mode", "passengers", "average_delay_minutes"]
assert set(tidy["mode"]) == {"Bus", "Train", "Ferry"}
assert pd.api.types.is_datetime64_any_dtype(tidy["month"])
assert pd.api.types.is_numeric_dtype(tidy["passengers"])
assert pd.api.types.is_numeric_dtype(tidy["average_delay_minutes"])
assert tidy["passengers"].isna().sum() == 1
assert tidy["average_delay_minutes"].isna().sum() == 1
bus_sep = tidy.loc[
    (tidy["mode"] == "Bus") & (tidy["month"] == pd.Timestamp("2025-09-01")),
    "passengers",
].iloc[0]
assert bus_sep == 1204, "The thousands separator was not handled correctly."
print("✓ identifiers, rows, types, missing values and spot value verified")
tidy.head()
"""),
        md(r"""
## Field combinations and task families

Complete the table before drawing anything.

| Question | Fields and data types | Required comparison | Task family |
|---|---|---|---|
| Which mode carries the most passengers overall? | | | |
| How does use change through the year? | | | |
| Do months with more passengers also have longer delays? | | | |
| Which mode has the most variable delays? | | | |
| How is total patronage divided among modes? | | | |
"""),
        md(r"""
## Create three candidate forms

Create three charts from `tidy`. They must answer different questions rather
than apply different styling to the same chart.

Every chart must include an informative title, units, honest missing-value
treatment and consistent mode colours. Do not use unsupported causal language.
"""),
        code(r"""
mode_colours = {"Bus": "#18678f", "Train": "#e66852", "Ferry": "#30a8b1"}

# TODO: candidate_magnitude_or_ranking
# Required fields: 1 categorical + 1 numeric.

# TODO: candidate_change
# Required fields: 1 temporal + 1 numeric; retain mode as a group.

# TODO: candidate_correlation
# Required fields: 2 numeric; retain mode as a group.
"""),
        md(r"""
## Compare, select and reject

| Candidate | Question answered | Easy comparison | Information hidden | Audience risk |
|---|---|---|---|---|
| Magnitude or ranking | | | | |
| Change over time | | | | |
| Correlation | | | | |

- **Selected form:**
- **Why it fits the audience and question:**
- **Plausible alternative rejected:**
- **Specific reason for rejection:**
- **Remaining limitation:**
"""),
        md(r"""
## Explain and disclose

Choose one transformation or plotting block and annotate it line by line. State
which line changes the number of observations, which changes a data type, which
determines the visual comparison and what would break if a new mode were added.

Complete the disclosure:

- **Tool used, if any:**
- **What it contributed:**
- **What you accepted, modified or rejected:**
- **How you verified the output:**
- **Remaining limitations or unverified claims:**
"""),
    ]

    # Present the exercises in the same order as the lecture's Visual Vocabulary.
    prefix, sections, suffix = [], [], []
    current = None
    in_suffix = False
    for cell in cells:
        source = cell.get("source", "")
        if cell.cell_type == "markdown" and re.match(r"## \d+ · ", source):
            if current is not None:
                sections.append(current)
            current = [cell]
        elif current is not None and source.startswith("## Synthesis"):
            sections.append(current)
            current = None
            in_suffix = True
            suffix.append(cell)
        elif current is not None:
            current.append(cell)
        elif in_suffix:
            suffix.append(cell)
        else:
            prefix.append(cell)
    if current is not None:
        sections.append(current)

    section_by_title = {
        re.match(r"## \d+ · (.+)", section[0].source).group(1): section
        for section in sections
    }
    desired_order = [
        "Playfair's exports and imports: deviation",
        "Russell's stellar diagram: correlation",
        "Playfair's bar chart: ranking",
        "The mirrored age–sex form: distribution",
        "The Keeling curve: change over time",
        "Nightingale's mortality diagram: magnitude",
        "Playfair's pie chart: part-to-whole",
        "Dupin's choropleth: spatial",
        "Minard's march: spatial + flow",
    ]
    ordered_sections = []
    for number, title in enumerate(desired_order, start=1):
        section = section_by_title[title]
        section[0].source = re.sub(r"## \d+ · ", f"## {number} · ", section[0].source, count=1)
        ordered_sections.extend(section)
    cells = prefix + ordered_sections + suffix

    notebook = nbf.v4.new_notebook(cells=cells)
    notebook.metadata["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    notebook.metadata["language_info"] = {"name": "python", "version": "3"}
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    nbf.write(notebook, OUTPUT)
    print(OUTPUT)
    solution = build_solution(notebook)
    nbf.write(solution, SOLUTION_OUTPUT)
    print(SOLUTION_OUTPUT)


if __name__ == "__main__":
    build()
