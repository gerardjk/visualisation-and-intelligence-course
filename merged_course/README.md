# Merged course materials

Canonical six-class teaching materials for 36104 Data Visualisation and
Narratives, merged from the `claude_course/` and `codex_course/` drafts.
See [COURSE_PLAN.md](COURSE_PLAN.md) for the full plan and assessment map.

## What lives where

Each developed class folder contains:

- `teaching_plan.md` — outcomes, run sheet, facilitation notes, evidence of learning;
- `slides.md` — slide-by-slide content and speaker direction;
- an editable PowerPoint deck, regenerable from `scripts/`;
- `instructor_guide.md` and `worked_demonstration.md`;
- `notebooks/` — three tiers (below);
- `activities/` — studio briefs, packs and cards;
- `assets/` — activity artefacts.

## Notebook tiers and distribution rules

| Tier | File pattern | Distribute |
|---|---|---|
| Lab (primary) | `*_lab.ipynb` | At the start of the lab |
| Starter (intervention) | `*_starter.ipynb` | Only to students blocked by syntax |
| Instructor (solutions) | `*_instructor.ipynb` | Never before the related activity and assessment have concluded |

Lab and starter notebooks end with the course AI-disclosure block; students
complete it before submitting or sharing.

## Rebuilding decks and notebooks

Class 1's canonical deck is LaTeX/Beamer, mixing public-domain originals
(Nightingale 1858, Snow 1854), the attributed AIATSIS map, and course-atlas
reproductions:

```bash
cd merged_course/classes/01-seeing-data/beamer
lualatex seeing-data.tex && lualatex seeing-data.tex   # → seeing-data.pdf
```

Class 2 still uses the python-pptx pipeline (to be migrated to Beamer):

```bash
cd merged_course/scripts
python build_class02_deck.py     # writes classes/02-visual-forms/Choosing-Visual-Forms.pptx
python build_notebooks.py        # optional single-notebook variants (notebooks/)
```

Atlas reproductions come from `quarto-book/_book/atlas_files/figure-html/` —
run `quarto render` in `quarto-book/` first if figures are missing.

## Provenance

- Six-class skeleton, assessment anchoring, deck pipeline: `claude_course/`.
- Three-tier notebooks, worked demonstrations, instructor guides, facilitation
  notes: `codex_course/`.
- Classes 03–06 are specified in the course plan and follow the same folder
  pattern as 01 and 02.
