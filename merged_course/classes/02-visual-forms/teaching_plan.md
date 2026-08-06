# Choosing Visual Forms: Encoding, Tidy Data, and the Visual Vocabulary

## Core question

What visual task are we performing?

## Core message

Chart selection begins with the comparison or judgement a user needs to make,
not with a chart name or visual effect.

## Learning outcomes

By the end of this session students should be able to:

1. Rank visual channels by the precision with which readers decode them, and
   explain why position and length usually beat area and colour.
2. Translate an analytical question into a visual task and classify it with
   the FT Visual Vocabulary.
3. Map a visual task to candidate chart forms and name each form's risks.
4. Reshape wide data to tidy long form, by hand and with an AI assistant.
5. Verify AI-wrangled data: identifiers, row counts, types, missing values,
   totals.
6. Compare several valid charts and justify a selection, and a rejection, 
   for a stated audience.

## Preparation

Students need `pandas`, `matplotlib` and `numpy`. The notebook creates its own
deliberately messy transport dataset so it does not depend on network access.

Instructor materials:

- the Choosing Visual Forms deck (`Choosing-Visual-Forms.pptx`) and `slides.md`;
- the lab notebook opened and run once;
- printed or digital Chart Choice Decision Record and Visual Vocabulary cards
  (`activities/`);
- selected course figures for magnitude, distribution, correlation, time and
  colour (box plot, Keeling, Hertzsprung–Russell, Minard, climate stripes).

## Three-hour run sheet

| Time | Segment | Teaching purpose |
|---|---|---|
| 0:00–0:10 | Recap + same data, different question | Exit tickets from last class; chart choice depends on task |
| 0:10–0:22 | Channel precision | Cleveland & McGill ranking; Mohs as the cautionary tale |
| 0:22–0:32 | Channel sprint: twelve charts, 40 seconds each | Students name the dominant channel per chart; debrief three |
| 0:32–0:48 | The Vocabulary | Nine families; gallery of canonical forms |
| 0:48–1:00 | Colour + honesty rules | Sequential/diverging/categorical; baselines and aspect ratio |
| 1:00–1:15 | Tidy-data worked demonstration | Connect data structure to available charts |
| 1:15–1:25 | Break |, |
| 1:25–2:20 | Notebook lab (`notebooks/choosing_visual_forms_lab.ipynb`) | Clean, verify, chart and compare |
| 2:20–2:45 | Studio: form cards + Redesign ×3 + Decision Record | Warm-up: each pair draws three cards from `activities/form_cards.pdf` and names the task family and working channel; then explicit selection and rejection |
| 2:45–2:55 | Gallery walk | Test whether charts answer their stated question |
| 2:55–3:00 | Exit ticket | Name the task, selected form, rejected alternative and verification performed |

Timing note: the Vocabulary gallery is deliberately over-provisioned, cut from
the middle (pyramid, Sankey) if discussion runs hot; never cut colour or
baselines.

## Content topics

- visual channels and perceptual precision (Cleveland & McGill ranking)
- FT Visual Vocabulary: nine task families
- task-to-chart mapping, illustrated with canonical figures
- colour as encoding: sequential, diverging, categorical
- tidy data and the wide-to-long reshape
- AI-assisted wrangling and the five-check verification pass

## Facilitation notes

- Keep returning to the question the audience must answer.
- Accept that several charts may be defensible; assess the reasoning rather
  than a single canonical answer.
- Ask students to name the visual channel, not just the chart type.
- Require a check after every assistant-proposed data transformation.
- If the assistant suggests a pie chart or dual axis, use it as a comparison
  opportunity rather than banning it without analysis.

## Notebook

Three tiers in `notebooks/` (lab / starter / instructor; same distribution
rules as Seeing Data). Core exercises:

1. Channel precision: the same values in five encodings; judge and compare.
2. Wide → tidy reshape of the transport table, with the five checks as
   assertions.
3. Vocabulary sort: classify six analytical questions, draft one chart.
4. Aspect ratio and baseline: same data, three impressions; assertions inspect
   the axes.
5. Colour: classify three palette scenarios, then prove the diverging one with
   a centred heatmap.
6. Redesign a deliberately weak chart three ways, one category per redesign
   (doubles as the studio artefact).

## Studio

**Visual Vocabulary sort and Redesign ×3**
(`activities/activity_visual_vocabulary_sort.md`, with
`activities/visual_vocabulary_cards.md`), closed out with the **Chart Choice
Decision Record** (`activities/activity_chart_choice.md`): an explicit
selection and one rejected alternative with a specific reason. This is the
direct rehearsal for A1 part B.

## Evidence of learning

Collect: verified tidy dataset; three candidate charts; completed Chart Choice
Decision Record; one rejected alternative with a specific reason; exit ticket.

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
