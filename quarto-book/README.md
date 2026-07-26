# How the World Is Organised — A Visual Account

A Quarto book whose body is an **Atlas of ~100 canonical scientific
visualisations**, each reproduced from data/code (never reprinted) and each
carrying a citable canonical-introduction reference. One source renders to two
targets: an online book (HTML) and a print edition (LuaLaTeX PDF).

## Structure

```
_quarto.yml          book config: chapters, HTML + PDF (lualatex)
index.qmd            preface / front matter
intro.qmd            the thesis/essay
atlas.qmd            the catalogue: 103 numbered entries + AIATSIS prelude
references.qmd       reference list container
references.bib       bibliography (one @key per cited work)
check_citations.py   pre-render citability gate
requirements.txt     Python dependencies
.github/workflows/publish.yml   CI: render + deploy to GitHub Pages
```

## Build

```bash
pip install -r requirements.txt
# PDF also needs LaTeX: `quarto install tinytex`
quarto preview          # live local preview while writing
quarto render           # build HTML + PDF into _book/
quarto render --to pdf  # PDF only
```

The citability gate runs automatically before every render (`pre-render:
check_citations.py` in `_quarto.yml`): it scans `atlas.qmd` for every
`**Canonical introduction:** [@key]` and fails the build if any key is absent
from `references.bib`. An unfinished entry is a build failure, not an
honour-system promise.

Execution results are cached (`freeze: auto`), so unchanged chapters are not
re-run on every build. Delete `_freeze/` to force a full rerun.

## Publish

Pushes to `main` trigger `.github/workflows/publish.yml`, which renders the
book and deploys it to the `gh-pages` branch. In the repository settings,
enable **Settings → Pages → Build and deployment → Source: Deploy from a
branch → `gh-pages`**. After the first successful Action run the book is live
at `https://gerardjk.github.io/quarto-book/`.

Before first build on a fork, edit `author` and `repo-url` in `_quarto.yml`
and the username in this file.

## Ground rules for entries

- **Data-grounded only** — every Atlas entry depicts measured data or a real
  reproduced instance, never a purely conceptual diagram.
- **Reproduce, don't reprint** — figures are redrawn from data with
  matplotlib; the historical original is described and cited, never pasted.
- **First ≠ canonical** — the earliest attributable instance and the
  publication the field cites are kept distinct.
- **One entry, one headline instance** — genuinely distinct instances get
  separate entries.
- **Citations verified before inclusion** — the pre-render gate enforces that
  every canonical-introduction key resolves.
