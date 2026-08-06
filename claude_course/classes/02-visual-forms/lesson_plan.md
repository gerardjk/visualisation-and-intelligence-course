# Class 2 — Choosing Visual Forms: Encoding, Tidy Data, and the Visual Vocabulary

## Core question

What visual task are we performing?

## Learning outcomes

By the end of this session students should be able to:

1. Rank visual channels by the precision with which readers decode them.
2. Classify an analytical question into an FT Visual Vocabulary category.
3. Map a visual task to candidate chart forms and name each form's risks.
4. Reshape wide data to tidy long form, by hand and with an AI assistant.
5. Verify AI-wrangled data: identifiers, row counts, types, missing values, totals.

## 3-hour run sheet

| Time | Segment | Detail | Materials |
|---|---|---|---|
| 0:00–0:10 | Recap + premise | Exit tickets from last class; task before form | Slides 1–3 |
| 0:10–0:25 | Channel precision | Cleveland & McGill ranking; Mohs as the cautionary tale | Slides 4–5 |
| 0:25–0:45 | The Vocabulary | Nine families; gallery: box plot, Keeling, H–R diagram, Minard | Slides 6–11 |
| 0:45–1:00 | Colour + honesty rules | Climate stripes; six colour cards; Zipf, pyramid, Sankey, choropleth; baselines and aspect | Slides 12–18 |
| 1:00–1:10 | Think · pair · share | Sketch the form for six-region ridership; compare | Slide 19 |
| 1:10–2:05 | Notebook | Exercises 1–5 core, 6 started; circulate and triage | Slides 20–22, notebook |
| 2:05–2:15 | Break | — | Slide 23 |
| 2:15–2:25 | Common mistake | Impressive form vs needed form; set up the studio | Slide 24 |
| 2:25–2:50 | Studio: Redesign ×3 | Finish Exercise 6 as the studio artefact; four phases | Slide 25, activity brief |
| 2:50–3:00 | Quiz + exit ticket | Quiz (open book, closed assistant); exit ticket | Slides 27–28 |

Timing note: the gallery (slides 8–18) is deliberately over-provisioned — cut
from the middle (pyramid, Sankey) if discussion runs hot; never cut colour or
baselines. Exercise 6 spans notebook and studio by design.

## Content topics

- visual channels and perceptual precision (Cleveland & McGill ranking)
- FT Visual Vocabulary: nine task families
- task-to-chart mapping, illustrated from the atlas (box plot, Keeling,
  Hertzsprung–Russell, Minard, climate stripes)
- colour as encoding: sequential, diverging, categorical
- tidy data and the wide-to-long reshape
- AI-assisted wrangling and the five-check verification pass

## Notebook

`visual_forms_activities.ipynb` — six exercises, AI assistant expected:

1. Channel precision: the same values in five encodings; judge and compare.
2. Wide → tidy reshape of the transport table, with the five checks as assertions.
3. Vocabulary sort: classify six analytical questions, draft one chart.
4. Aspect ratio and baseline: same data, three impressions; assertions inspect the axes.
5. Colour: classify three palette scenarios, then prove the diverging one with a centred heatmap.
6. Redesign a deliberately weak chart three ways, one category per redesign (doubles as the studio artefact).

## Studio activity

Visual Vocabulary sort and Redesign ×3 (see `activity_visual_vocabulary_sort.md`).

## Exit ticket

```text
One design decision I made today:
One risk or limitation I noticed:
One thing I need to verify before next class:
```

## References

Required: Financial Times Visual Vocabulary; Franconeri et al., "The Science of
Visual Data Communication"; Wickham, "Tidy Data".

Recommended: Cleveland & McGill, "Graphical Perception"; Heer & Bostock,
"Crowdsourcing Graphical Perception"; Long & Kay, "To Cut or Not To Cut?";
Crameri et al., "The Misuse of Colour in Science Communication"; Ware, Stone &
Szafir, "Rainbow Colormaps Are Not All Bad".
