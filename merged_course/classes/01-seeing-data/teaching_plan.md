# Class 1 — Seeing Data: Visualisation, Intelligence, and Interpretation

## Core question

How do charts create meaning?

## Core message

A chart is a claim about how the world is organised. The claim is produced
through selection, encoding, comparison, framing and omission.

## Learning outcomes

By the end of this session students should be able to:

1. Explain how selection, encoding and framing turn data into meaning.
2. Distinguish data, encoding, observation, insight and narrative — and a
   fluent interpretation from a justified insight.
3. Explain why identical summary statistics can conceal different structures.
4. Separate a visible pattern from an unsupported causal claim.
5. Use an AI assistant to produce a chart and verify every claim it makes
   about the data.
6. Critique a human-made chart and an AI-generated interpretation using course
   terminology, including representation and governance questions.
7. Record significant intelligent-tool use with the course disclosure block.

## Preparation

Students need a Python notebook environment with `pandas`, `matplotlib` and
`numpy`. An AI assistant is expected but every task remains possible without
one.

Instructor materials:

- the Seeing Data deck (`Seeing-Data.pptx`) and `slides.md` speaker directions;
- the lab notebook opened and run once before class;
- the Critique and Repair activity sheet and critique pack (`activities/`);
- selected Atlas figures: Anscombe, Snow, AIATSIS, Bertin.

## Three-hour run sheet

| Time | Segment | Teaching purpose |
|---|---|---|
| 0:00–0:10 | Silent chart reading | Students write what they see before hearing an explanation |
| 0:10–0:30 | Anscombe prediction and reveal | Establish that summaries are selective |
| 0:30–0:45 | Evidence, encoding, claim and narrative | Establish shared vocabulary |
| 0:45–1:05 | Snow worked example | Separate spatial pattern, inference and causal evidence |
| 1:05–1:15 | AI interpretation comparison | Show that fluency does not guarantee validity |
| 1:15–1:25 | Break | — |
| 1:25–2:20 | Notebook lab (`notebooks/seeing_data_lab.ipynb`) | Calculate, plot, prompt, test and repair |
| 2:20–2:45 | Studio: Critique and Repair | Apply the framework to an unfamiliar example |
| 2:45–2:55 | Pair exchange (Critique 1 frame) | Test whether claims are supported and specific |
| 2:55–3:00 | Exit ticket | Record a decision, a risk and a verification need |

## Content topics

- visualisation as selection and interpretation
- human and machine intelligence in visualisation
- generated charts and hallucinated insight
- the five-step verification ladder for generated output
- data governance from the start (Indigenous Data Sovereignty)

## Facilitation notes

- Do not show Anscombe's plots before students predict their appearance.
- Ask students to use "the chart shows" only for visible evidence. Reserve
  "this suggests" for interpretation.
- Avoid presenting Snow's map as proof by itself. Ask what additional evidence
  supports causation.
- Treat the AIATSIS material as a governance discussion, not merely another
  map example.
- During assistant use, require students to retain their initial prediction
  and prompt summary.

## Notebook

Three tiers in `notebooks/`: distribute `seeing_data_lab.ipynb` at the start of
the lab; hold `seeing_data_starter.ipynb` as an intervention for students
blocked by syntax; keep `seeing_data_instructor.ipynb` until the activity and
any related assessment have concluded. Core exercises:

1. Summary statistics vs the picture (Anscombe).
2. Assistant-generated chart of the transport dataset plus verification checks.
3. Claim audit of a generated interpretation: supported / unsupported /
   unverifiable.

## Studio

Primary: **Critique and Repair** (`activities/activity_critique_and_repair.md`
with `activities/critique_pack.md`) — read, test, verify, repair, with the
responsibility checkpoint.

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
Feminism* (selected chapter); Maiam nayri Wingara & AIGI, *Indigenous Data
Sovereignty Communique*.

Recommended: Munzner, "A Nested Model for Visualization Design and Validation";
Hicks, Humphries & Slater, "ChatGPT is bullshit"; Bender et al., "On the
Dangers of Stochastic Parrots".
