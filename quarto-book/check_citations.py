#!/usr/bin/env python3
"""Citability gate for the Atlas.

Scans atlas.qmd for every `**Canonical introduction:** [@key]` line, extracts
each citation key, and fails the build if any key is absent from
references.bib. Wired as a Quarto pre-render step in _quarto.yml, so an
unfinished entry is a build failure rather than an honour-system promise.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
ATLAS = ROOT / "atlas.qmd"
BIB = ROOT / "references.bib"


def bib_keys(text: str) -> set[str]:
    return set(re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", text))


def canonical_keys(text: str) -> list[tuple[int, str]]:
    """(line number, key) for every canonical-introduction citation."""
    out = []
    pattern = re.compile(r"\*\*Canonical introduction:\*\*.*?\[@([A-Za-z0-9_:+-]+)")
    for lineno, line in enumerate(text.splitlines(), start=1):
        for m in pattern.finditer(line):
            out.append((lineno, m.group(1)))
    return out


def main() -> int:
    if not ATLAS.exists():
        print(f"check_citations: {ATLAS.name} not found", file=sys.stderr)
        return 1

    atlas_text = ATLAS.read_text(encoding="utf-8")
    bib_text = BIB.read_text(encoding="utf-8") if BIB.exists() else ""

    keys = canonical_keys(atlas_text)
    known = bib_keys(bib_text)

    missing = [(lineno, key) for lineno, key in keys if key not in known]

    print(f"check_citations: {len(keys)} canonical-introduction keys found, "
          f"{len(known)} bib entries loaded")

    if missing:
        for lineno, key in missing:
            print(f"  atlas.qmd:{lineno}: unresolved canonical key @{key}",
                  file=sys.stderr)
        print(f"check_citations: FAIL — {len(missing)} unresolved key(s)",
              file=sys.stderr)
        return 1

    print("check_citations: OK — every canonical-introduction key resolves")
    return 0


if __name__ == "__main__":
    sys.exit(main())
