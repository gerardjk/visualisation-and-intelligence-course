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
2. Classify fields as nominal, ordinal, interval, ratio, temporal, spatial or
   relational, and state which comparisons those types and roles permit.
3. Translate an analytical question into a visual task and classify it with
   the FT Visual Vocabulary.
4. Map a visual task to candidate chart forms and name each form's risks.
5. Choose a categorical, sequential or diverging palette from the data
   semantics, and add redundant cues for accessibility.
6. Reshape wide data to tidy long form, by hand and with an AI assistant.
7. Verify AI-wrangled data: identifiers, row counts, types, missing values,
   totals.
8. Compare several valid charts and justify a selection, and a rejection,
   for a stated audience.

## Preparation

Students need `pandas`, `matplotlib` and `numpy`. The notebook creates its own
deliberately messy transport dataset so it does not depend on network access.

Instructor materials:

- the Choosing Visual Forms deck (`beamer/choosing-visual-forms.pdf`) and `slides.md`;
- the student notebook, `notebooks/choosing_visual_forms.ipynb`, and the matching
  `notebooks/choosing_visual_forms_solution.ipynb`, opened and run once;
- printed or digital Chart Choice Decision Record and Visual Vocabulary cards
  (`activities/`);
- the nine original examples used in the task-family sequence. None is drawn
  from the released A1 pool.

## Three-hour run sheet

| Time | Segment | Teaching purpose |
|---|---|---|
| 0:00–0:10 | Premise and goals | Chart choice depends on the required comparison |
| 0:10–0:25 | Data types and field roles | Nominal, ordinal, interval, ratio, temporal, spatial and relational fields |
| 0:25–0:35 | Field combinations | Connect field combinations to comparisons and task families |
| 0:35–0:47 | Channel precision | Position, length, angle, area and colour |
| 0:47–1:15 | Visual Vocabulary | Nine families; one original example per family |
| 1:15–1:30 | Colour as data | Hue/lightness/chroma; categorical/sequential/diverging; accessibility and redundant cues |
| 1:30–1:40 | Tidy-data worked demonstration | Connect field types, data structure and available charts |
| 1:40–1:50 | Break | — |
| 1:50–2:25 | Notebook (`notebooks/choosing_visual_forms.ipynb`) | Reconstruct, clean, verify, chart and compare |
| 2:25–2:50 | Studio: claim → candidates → Decision Record | Each pair frames a supported claim, sketches two plausible forms, selects one, rejects one and compares the alternative with the original |
| 2:50–2:57 | Gallery walk | Test whether charts answer their stated question |
| 2:57–3:00 | Exit ticket | Name the task, selected form, rejected alternative and verification performed |

Timing note: the Vocabulary gallery is deliberately over-provisioned. Cut from
the middle if discussion runs hot, but preserve the data-type bridge, colour
sequence, A1 pipeline and baseline discussion. This class now carries the
course's core colour theory; later classes should apply and revisit it rather
than assuming a separate colour unit.

## Content topics

- visual channels and perceptual precision (Cleveland & McGill ranking)
- measurement types and semantic roles: nominal, ordinal, interval, ratio,
  temporal, spatial and relational
- question → field types/roles → required comparison → task → channel → form
- FT Visual Vocabulary: nine task families
- task-to-chart mapping, illustrated with canonical figures
- colour dimensions: hue, lightness/value and chroma/saturation
- palette semantics: categorical, sequential, diverging and highlight/context
- colour accessibility: contrast, colour-vision checks and redundant encoding
- tidy data and the wide-to-long reshape
- AI-assisted wrangling and the five-check verification pass

## Facilitation notes

- Keep returning to the question the audience must answer.
- Accept that several charts may be defensible; assess the reasoning rather
  than a single canonical answer.
- Ask students to name the visual channel, not just the chart type.
- When a student says a column is “numeric,” ask whether it is an identifier,
  interval measure or ratio measure and which operations are meaningful.
- Do not let field type become a chart lookup table: ask for the audience's
  required comparison before accepting the Visual Vocabulary category.
- For every palette, ask which data semantics justify its order or midpoint
  and how the reading survives without hue.
- Require a check after every assistant-proposed data transformation.
- If the assistant suggests a pie chart or dual axis, use it as a comparison
  opportunity rather than banning it without analysis.

## Notebook

The class uses one student notebook, `choosing_visual_forms.ipynb`, with a
section-matched instructor solution, `choosing_visual_forms_solution.ipynb`.
Core exercises:

1. Reconstruct the nine original examples in Visual Vocabulary order.
2. Wide → tidy reshape of the transport table, with the five checks as
   assertions.
3. Classify analytical questions from their field types and required comparisons.
4. Compare candidate views that answer different questions from the same tidy
   transport data.
5. Select one claim-led alternative, reject one plausible form and explain what
   becomes easier and harder to see than in the starting view.

## Studio

**Visual Vocabulary sort and claim-led alternative view**
(`activities/activity_visual_vocabulary_sort.md`, with
`activities/visual_vocabulary_cards.md`), closed out with the **Chart Choice
Decision Record** (`activities/activity_chart_choice.md`): an explicit
selection and one rejected alternative with a specific reason. Students also
compare the selected view with the original. This is a direct rehearsal for
A1 Part B using a synthetic transport artefact rather than an A1 pool chart.

## Evidence of learning

Collect: verified tidy dataset; candidate charts; completed full Chart Choice
Decision Record; comparison with the original; exit ticket.

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
