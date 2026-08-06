# A1 Artefact Pool, instructor staging file

Twelve chart-and-dataset pairs across twelve domains, curated for: reliable
public data (instructor caches the CSV once), genuine editorial choices worth
critiquing, and **no overlap with material already used in the course**, no
climate stripes or temperature anomaly charts (atlas entries, Week 1 deck),
no transport ridership (the lab dataset's domain), nothing adjacent to the
Keeling/emissions atlas entries, and no population pyramids.

**Do not release this file to students yet.** Before release, verify every
link resolves, add the exact chart URL and publication date, cache each
dataset as CSV into `pool_data/<id>.csv`, and screenshot each chart into
`pool_charts/<id>.png`: the pool ships with its data so no student inherits
a six-hour digitisation job.

**Selection rule (no sign-up, no approvals, no bring-your-own):** each
student selects **three artefacts from this pool, from three different
domains**, one as their **primary**. The primary is locked in the supervised
window: its pool ID goes on the supervised sheet, and `META_1` must match.
More than one student may use the same artefact; their critiques,
reconstructions, redesigns and claim audit remain individual.

Release only rows that pass this checklist:

```text
[ ] Exact chart URL, creator/publisher and publication date recorded
[ ] Screenshot cached and source credited
[ ] Data CSV cached, opens cleanly and contains at least 6 usable rows
[ ] Units and any reconstruction documented
[ ] No personal, sensitive or culturally restricted data
[ ] Confirmed the chart (and its canonical form) is not already used in
    course materials: atlas entries, decks, lab datasets
[ ] A staff member has completed a trial redesign and claim audit
```

| ID | Domain | Chart (published artefact) | Publisher / where found | Data source | Why it's in the pool |
|---|---|---|---|---|---|
| POOL-01 | economy | Monthly CPI indicator bar chart | ABS media release graphic | ABS data explorer CSV | Exact series downloadable; media-release framing choices to critique |
| POOL-02 | politics | 2023 Referendum results by state | AEC Tally Room graphic / news wrap | AEC results downloads | Part-to-whole and map-vs-bar choices; clean official data |
| POOL-03 | housing | Dwelling approvals trend chart | ABS Building Approvals release / news graphic | ABS data explorer CSV | Volatile monthly series: smoothing and window choices to critique |
| POOL-04 | health | Respiratory surveillance (flu/COVID) weekly chart | NSW Health surveillance report | NSW Health report tables (cached to CSV) | Seasonal axis-window rhetoric; topical |
| POOL-05 | music | Top-streamed artists/songs bar chart | Spotify Charts weekly (as republished) | spotifycharts.com CSV export | Ranking domain; engaging; trivially obtainable data |
| POOL-06 | sport | AFL/NRL attendance or ladder chart | League site / news graphic | austadiums.com attendance tables (cached) | Ranking vs magnitude tension; familiar to cohort |
| POOL-07 | labour market | Job vacancies vs unemployment chart | ABS/SEEK commentary graphic | ABS Labour Force + Job Vacancies CSV | Two series joined: dual-axis temptation is the critique |
| POOL-08 | energy | NEM electricity generation fuel-mix chart | OpenNEM / AEMO as republished in news | OpenNEM CSV export | Stacked-area part-to-whole rhetoric; rich public data |
| POOL-09 | road safety | Road fatalities trend chart | BITRE Road Deaths Australia bulletin | BITRE monthly CSV | Clean official CSV; denominator (per-capita) critique built in |
| POOL-10 | tourism | Overseas arrivals recovery chart | ABS Overseas Arrivals and Departures release | ABS data explorer CSV | Dramatic COVID shape: baseline and recovery framing choices |
| POOL-11 | water | Dam storage levels over time | WaterNSW / BOM water storage dashboard | WaterNSW storage CSV | Percent-of-capacity vs volume encoding choice; clean data |
| POOL-12 | global development | Life expectancy over time, selected countries | Our World in Data (as republished in news) | OWID grapher CSV export | Country-selection rhetoric; clean CSV; global counterweight to the Australian rows |
