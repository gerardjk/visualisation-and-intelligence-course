# Quarto guide for this course

Quarto is used here as the publishing layer for the course website and optional book. Canvas should still be used for official quizzes, submissions, announcements, due dates, and the gradebook.

## Install

Download Quarto from <https://quarto.org/docs/get-started/>.

Recommended editor: VS Code with the Quarto extension, or Positron/RStudio if preferred.

## Preview the course website

```bash
quarto preview
```

## Render the course website

```bash
quarto render
```

The rendered site will appear in `_site/`.

## Render the book

```bash
cd book
quarto render
```

The rendered book will appear in `book/_book/`.

## Publish with GitHub Pages

The simplest route is to use GitHub Actions. This repo includes `.github/workflows/quarto-publish.yml`.

To publish:

1. Push the repo to GitHub.
2. In GitHub, go to **Settings → Pages**.
3. Set the source to **GitHub Actions**.
4. Push to `main`.
5. The site will build and deploy automatically.

## Canvas integration

Create weekly Canvas modules that link to the Quarto pages. Keep graded quizzes in Canvas.
