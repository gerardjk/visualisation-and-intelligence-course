# A1 Candidate Artefact Pool — instructor staging file

Ten candidate chart-and-dataset pairs across seven domains. **Do not release
this file to students yet.** Before release, verify every link resolves, add
the exact chart URL and publication date, cache each dataset as CSV into
`pool_data/<id>.csv`, and screenshot each chart into `pool_charts/<id>.png` —
the pool ships with its data so no student inherits a six-hour digitisation job.
Each student selects **three artefacts from three different domains** (at
least two from this pool, at most one approved bring-your-own), nominating
one as their **primary**, by Monday 10 August 2026. It is acceptable for more
than one student to use the same source artefact; their critiques,
reconstructions, redesigns and claim audit remain individual.

Release only rows that pass this checklist:

```text
[ ] Exact chart URL, creator/publisher and publication date recorded
[ ] Screenshot cached and source credited
[ ] Data CSV cached, opens cleanly and contains at least 6 usable rows
[ ] Units and any reconstruction documented
[ ] No personal, sensitive or culturally restricted data
[ ] A staff member has completed a trial redesign and claim audit
```

| ID | Chart (published artefact) | Publisher / where found | Data source | Reconstruction risk |
|---|---|---|---|---|
| POOL-01 | Monthly CPI indicator bar chart | ABS media release graphic | ABS data explorer CSV | Low — exact series downloadable |
| POOL-02 | Opal patronage recovery line chart | Transport for NSW open data blog | TfNSW Open Data Hub (Opal trips) | Low |
| POOL-03 | Annual mean temperature anomaly stripes/bars | BOM Annual Climate Statement | BOM ACORN-SAT time series | Low |
| POOL-04 | 2023 Referendum results by state | AEC Tally Room graphic / news wrap | AEC results downloads | Low |
| POOL-05 | CO₂ emissions per capita, selected countries | Our World in Data grapher (as republished in news) | OWID grapher CSV export | Low |
| POOL-06 | Dwelling approvals trend chart | ABS Building Approvals release / news graphic | ABS data explorer CSV | Low |
| POOL-07 | Respiratory surveillance (flu/COVID) weekly chart | NSW Health surveillance report | NSW Health report tables (PDF → CSV) | Medium — table extraction |
| POOL-08 | Top-streamed artists/songs bar chart | Spotify Charts weekly (as republished) | spotifycharts.com CSV export | Low |
| POOL-09 | AFL/NRL attendance or ladder chart | League site / news graphic | austadiums.com attendance tables | Medium — scrape/table copy |
| POOL-10 | Job vacancies vs unemployment chart | ABS/SEEK commentary graphic | ABS Labour Force + Job Vacancies CSV | Low — two series to join |

## Bring-your-own approval checklist (recorded in Week 1)

```text
Chart: publisher, date, URL, screenshot attached?
Claim: what does it invite the reader to believe?
Data: exact source, or reconstruction plan (what quantities are readable)?
Risk: any personal, sensitive, or culturally restricted data? (If yes: decline.)
```
