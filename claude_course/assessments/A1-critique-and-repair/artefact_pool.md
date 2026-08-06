# A1 Artefact Pool

Ten starter chart+dataset pairs across seven domains. **Instructor to-do before
release:** verify every link resolves, cache each dataset as CSV into
`pool_data/<id>.csv`, and screenshot each chart into `pool_charts/<id>.png` —
the pool ships with its data so no student inherits a six-hour digitisation job.
Size the pool to at least the largest tutorial before assigning (duplicate this
list with fresh artefacts rather than reusing within a tutorial).

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

## Bring-your-own approval checklist (recorded at Class 1)

```text
Chart: publisher, date, URL, screenshot attached?
Claim: what does it invite the reader to believe?
Data: exact source, or reconstruction plan (what quantities are readable)?
Unique: no one else in the tutorial has it?
Risk: any personal, sensitive, or culturally restricted data? (If yes: decline.)
```
