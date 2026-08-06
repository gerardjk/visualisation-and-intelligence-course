# Seeing Data: Visualisation, Intelligence, and Interpretation

## Core question

How do charts create meaning?

## Core message

A chart is a claim about how the world is organised. The claim is produced
through selection, encoding, comparison, framing and omission.

## Learning outcomes

By the end of this session students should be able to:

1. Explain how selection, encoding and framing turn data into meaning.
2. Distinguish data, encoding, observation, insight and narrative, and a
   fluent interpretation from a justified insight.
3. Explain why identical summary statistics can conceal different structures.
4. Separate a visible pattern from an unsupported causal claim.
5. Use an AI assistant to produce a chart and verify every claim it makes
   about the data.
6. Critique a human-made chart and an AI-generated interpretation using course
   terminology.
7. Record significant intelligent-tool use with the course disclosure block.

## Preparation

Students need a Python notebook environment with `pandas`, `matplotlib` and
`numpy`. An AI assistant is expected but every task remains possible without
one.

Instructor materials:

- the Seeing Data deck (`beamer/seeing-data.pdf`; rebuild with `lualatex
  seeing-data.tex` in `beamer/`) and `slides.md` speaker directions;
- the lab notebook opened and run once before class;
- the Critique and Repair activity sheet and critique pack (`activities/`);
- the chart card pack (`activities/chart_cards.pdf`) printed single-sided, 
  each pair draws three cards in the studio;
- originals embedded in the deck: Snow 1854 (public domain) and the Hawkins
  warming stripes (CC BY-SA 4.0); every other figure is a course reproduction
  generated from data.

## Three-hour run sheet (matches the deck order)

| Time | Segment | Deck slides | Teaching purpose |
|---|---|---|---|
| 0:00–0:08 | Private Canvas preference survey + subject workflow | 3–4 | Complete the private preference task; state permitted AI workflow and boundaries |
| 0:08–0:15 | Premise and outcomes | 5–7 | A chart is a claim; five decisions produce it |
| 0:15–0:30 | Anscombe prediction and reveal | 8–9 | Establish that summaries are selective |
| 0:30–0:38 | Vocabulary: data → encoding → observation → insight → narrative | 10 | Establish shared vocabulary |
| 0:38–0:50 | Claim sprint: twelve charts, 40 seconds each | 11–23 | Every chart is a claim; students write two "the chart shows…" sentences; debrief two |
| 0:50–1:05 | Snow worked example + the shows/suggests debrief | 24–26 | Separate spatial pattern, inference and causal evidence |
| 1:05–1:13 | Six ways a true chart misleads | 27–28 | Accurate charts can still deceive; the window is part of the claim |
| 1:13–1:22 | AI interpretation and the verification ladder | 29–32 | Fluency does not guarantee validity |
| 1:22–1:30 | Think · pair · share | 33 | A found chart against the six mechanisms |
| 1:30–1:40 | Break | 34 |, |
| 1:40–2:30 | Notebook lab (`notebooks/seeing_data_lab.ipynb`) | 35 | Calculate, plot, generate, verify, repair |
| 2:30–2:50 | Studio: chart cards + Critique and Repair | 36 | Three cards per pair: claim, audience, what could mislead; then the repair artefact |
| 2:50–2:55 | Pair exchange (Critique 1 frame) | 37 | Test whether claims are supported and specific |
| 2:55–3:00 | Close the loop + exit ticket | 38 | Record a decision, a risk and a verification need |

The diagnostic quiz runs on Canvas after class, open book, closed assistant,
ungraded; it calibrates the cohort, not marks.

## Content topics

- visualisation as selection and interpretation
- human and machine intelligence in visualisation
- generated charts and hallucinated insight
- the five-step verification ladder for generated output

## Facilitation notes

- Do not show Anscombe's plots before students predict their appearance.
- Ask students to use "the chart shows" only for visible evidence. Reserve
  "this suggests" for interpretation.
- Avoid presenting Snow's map as proof by itself. Ask what additional evidence
  supports causation.
- During assistant use, require students to retain their initial prediction
  and prompt summary.

## Notebook

Three tiers in `notebooks/`: distribute `seeing_data_lab.ipynb` at the start of
the lab; hold `seeing_data_starter.ipynb` as an intervention for students
blocked by syntax; keep `seeing_data_instructor.ipynb` until the activity and
any related assessment have concluded. Core exercises:

1. Summary statistics vs the picture (Anscombe).
2. Assistant-generated chart of the transport dataset plus verification checks.
3. Claim audit of a generated interpretation, four-way: supported directly /
   plausible but unverified / unsupported / contradicted.

Bertin's visual variables are introduced only as a bridge here; channel
precision and visual-task selection are taught in depth in Choosing Visual Forms.

## Studio

Primary: **Critique and Repair** (`activities/activity_critique_and_repair.md`
with `activities/critique_pack.md`). Warm-up: each pair draws three cards from
`activities/chart_cards.pdf` and answers, per card: the claim, the audience,
one way it could mislead. Then the full read–test–verify–repair cycle on the
satisfaction artefact, with the responsibility checkpoint.

Pair exchange uses the **Critique 1** frame
(`activities/critique_1_human_vs_ai.md`): one human-made chart vs one
AI-generated interpretation. This is the direct rehearsal for A1 parts A and C.

## Evidence of learning

Collect: completed notebook checks; one repaired caption; the Critique and
Repair sheet; the exit ticket.

## Exit ticket

```text
One design decision I made today:
One risk or limitation I noticed:
One thing I need to verify before next class:
```

## References

Required: Cairo, *How Charts Lie* (selected chapter); D'Ignazio & Klein, *Data
Feminism* (selected chapter).

Recommended: Munzner, "A Nested Model for Visualization Design and Validation";
Hicks, Humphries & Slater, "ChatGPT is bullshit"; Bender et al., "On the
Dangers of Stochastic Parrots".
