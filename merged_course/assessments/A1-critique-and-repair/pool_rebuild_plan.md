# A1 pool rebuild: acceptance plan

Status: built and validated locally; ready for Canvas publication.

## Category balance

The twelve-entry pool will represent every Financial Times Visual Vocabulary
category at least once. The three additional entries strengthen categories
that support accessible, comparable coding tasks.

| Category | Target |
|---|---:|
| Deviation | 1 |
| Correlation | 2 |
| Ranking | 1 |
| Distribution | 2 |
| Change over time | 2 |
| Magnitude | 1 |
| Part-to-whole | 1 |
| Spatial | 1 |
| Flow | 1 |
| **Total** | **12** |

The pool manifest will declare one primary category for each published chart.
Students may choose a different category for their alternative view when their
claim and explanation justify it.

## Required contents of every pool entry

Each `POOL-nn/` directory must contain:

- `original_chart.<ext>`: the publisher's downloadable chart, an exact crop
  from the publisher's document, or one of the explicitly approved printable
  chart-card reproductions;
- `source_data.csv`: a tidy extract derived from the publisher's corresponding
  data, not values transcribed from the chart;
- `data_dictionary.md`: column definitions, units, missing-value conventions,
  and any filters or derived fields;
- `provenance.md`: chart title, publisher, publication date, chart URL, data
  URL, licence/copyright note, download date, and exact extraction steps;
- `checks.json`: row and column counts, file hashes, source-to-extract checks,
  and repository non-reuse result.

## Acceptance checks

An entry is eligible only when all of these are true:

1. The original is visibly attributable to an authoritative publisher.
2. The data source corresponds to the quantities in the published chart.
3. The supplied CSV is small enough for an introductory notebook (currently
   6–259 data rows and 2–9 columns) and requires no specialist parser.
4. A clean Python process can load the CSV, and the fields used by the
   published chart are present in the corresponding source dataset.
5. The original chart image is absent from the published Week 1–3 teaching
   decks. The unpublished printable chart-card activity is the explicit
   exception approved for this pool. Gapminder and the exoplanet transit are
   excluded.
6. The coding burden is comparable with the other entries: no API key,
   scraping, geocoding, specialist scientific parser, or manual digitisation
   is required of students.
7. The chart and data can be distributed inside the Canvas subject under their
   stated licence or the educational criticism/review basis documented in the
   provenance sheet.

## Assignment consequence

The brief must describe Part B as an alternative view for a stated claim, not
as reconstruction or a universally better repair. Students use the supplied
CSV, preserve its source columns, disclose transformations, and explain what
their design makes easier and harder to see than the original.
