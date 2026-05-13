#!/usr/bin/env python3
"""Static checker for the Public Data Product Checkpoint.

The checker automates routine scaffold checks. It deliberately does not grade
visual judgement, ethical reasoning, interpretation quality, or oral defence.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class CheckResult:
    name: str
    passed: bool
    points: int
    max_points: int
    message: str


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(errors="ignore")


def find_file(root: Path, names: Iterable[str]) -> Path | None:
    for name in names:
        p = root / name
        if p.exists():
            return p
    return None


def count_patterns(text: str, patterns: Iterable[str]) -> int:
    return sum(len(re.findall(pattern, text, flags=re.IGNORECASE | re.MULTILINE)) for pattern in patterns)


def check_required_readme_sections(readme_text: str) -> tuple[bool, int]:
    terms = ["purpose", "user", "dataset", "run", "limitations"]
    hits = sum(1 for t in terms if t in readme_text.lower())
    return hits >= 3, hits


def check_repo(root: Path) -> list[CheckResult]:
    results: list[CheckResult] = []

    app = find_file(root, ["app.py", "streamlit_app.py", "main.py"])
    req = root / "requirements.txt"
    readme = root / "README.md"

    results.append(CheckResult("app_file_exists", app is not None, 2 if app else 0, 2, "Found app entry file." if app else "No app.py, streamlit_app.py, or main.py found."))
    results.append(CheckResult("requirements_exists", req.exists(), 2 if req.exists() else 0, 2, "Found requirements.txt." if req.exists() else "requirements.txt missing."))
    results.append(CheckResult("readme_exists", readme.exists(), 1 if readme.exists() else 0, 1, "Found README.md." if readme.exists() else "README.md missing."))

    if readme.exists():
        ok, hits = check_required_readme_sections(read_text(readme))
        results.append(CheckResult("readme_sections", ok, 1 if ok else 0, 1, f"README section terms found: {hits}/5."))
    else:
        results.append(CheckResult("readme_sections", False, 0, 1, "No README to inspect."))

    app_text = ""
    if app:
        app_text = read_text(app)
        try:
            ast.parse(app_text)
            results.append(CheckResult("python_parses", True, 2, 2, "App file parses as Python."))
        except SyntaxError as exc:
            results.append(CheckResult("python_parses", False, 0, 2, f"Syntax error: {exc}"))
    else:
        results.append(CheckResult("python_parses", False, 0, 2, "No app file to parse."))

    if req.exists():
        req_text = read_text(req).lower()
        needed = ["streamlit", "pandas"]
        hits = sum(1 for n in needed if n in req_text)
        results.append(CheckResult("requirements_core_packages", hits == len(needed), hits, len(needed), f"Core packages found: {hits}/{len(needed)}."))
    else:
        results.append(CheckResult("requirements_core_packages", False, 0, 2, "No requirements.txt to inspect."))

    if app_text:
        cache_found = "@st.cache_data" in app_text or "st.cache_data" in app_text
        results.append(CheckResult("cache_data_used", cache_found, 2 if cache_found else 0, 2, "Caching pattern found." if cache_found else "No st.cache_data pattern found."))

        widget_count = count_patterns(app_text, [
            r"st\.(sidebar\.)?selectbox",
            r"st\.(sidebar\.)?multiselect",
            r"st\.(sidebar\.)?slider",
            r"st\.(sidebar\.)?radio",
            r"st\.(sidebar\.)?checkbox",
            r"st\.(sidebar\.)?date_input",
        ])
        results.append(CheckResult("at_least_two_widgets", widget_count >= 2, min(widget_count, 2), 2, f"Found {widget_count} widget references."))

        chart_count = count_patterns(app_text, [
            r"st\.altair_chart",
            r"st\.plotly_chart",
            r"st\.pyplot",
            r"st\.line_chart",
            r"st\.bar_chart",
            r"st\.area_chart",
            r"st\.map",
        ])
        results.append(CheckResult("at_least_three_charts", chart_count >= 3, min(chart_count, 3), 3, f"Found {chart_count} chart output references."))

        validation_found = any(term in app_text.lower() for term in ["required_columns", "missing", "valueerror", "st.error"])
        results.append(CheckResult("data_validation_or_error_handling", validation_found, 2 if validation_found else 0, 2, "Validation/error pattern found." if validation_found else "No obvious validation/error pattern found."))

        empty_state = any(term in app_text.lower() for term in ["st.warning", "st.error", "st.stop", "empty"])
        results.append(CheckResult("empty_or_error_state", empty_state, 2 if empty_state else 0, 2, "Empty/error state pattern found." if empty_state else "No obvious empty/error state pattern found."))

        expander_found = "st.expander" in app_text
        disclosure_terms = ["data source", "ai assistance", "human verification", "known limitations", "appropriate use", "inappropriate use", "what the data excludes"]
        disclosure_hits = sum(1 for term in disclosure_terms if term.lower() in app_text.lower())
        results.append(CheckResult("data_ai_disclosure", expander_found and disclosure_hits >= 5, 3 if expander_found and disclosure_hits >= 5 else 0, 3, f"Expander found: {expander_found}; disclosure terms found: {disclosure_hits}/7."))

        visual_vocab_terms = ["visual vocabulary", "change over time", "ranking", "distribution", "spatial", "flow", "part-to-whole", "deviation", "correlation", "magnitude"]
        visual_hits = sum(1 for term in visual_vocab_terms if term.lower() in app_text.lower())
        results.append(CheckResult("visual_vocabulary_declared", visual_hits >= 2, 2 if visual_hits >= 2 else visual_hits, 2, f"Visual Vocabulary terms found: {visual_hits}."))

        user_story = "user stor" in app_text.lower() or "as a " in app_text.lower()
        results.append(CheckResult("user_story_present", user_story, 1 if user_story else 0, 1, "User story language found." if user_story else "No user story language found."))
    else:
        for name, pts in [
            ("cache_data_used", 2),
            ("at_least_two_widgets", 2),
            ("at_least_three_charts", 3),
            ("data_validation_or_error_handling", 2),
            ("empty_or_error_state", 2),
            ("data_ai_disclosure", 3),
            ("visual_vocabulary_declared", 2),
            ("user_story_present", 1),
        ]:
            results.append(CheckResult(name, False, 0, pts, "No app text available."))

    provenance_candidates = list(root.glob("**/*provenance*.csv")) + list(root.glob("**/*provenance*.md")) + list(root.glob("**/*ai*_matrix*.csv"))
    results.append(CheckResult("provenance_file_exists", bool(provenance_candidates), 2 if provenance_candidates else 0, 2, f"Found {len(provenance_candidates)} provenance file(s)."))

    user_story_candidates = list(root.glob("**/*user*stor*.*"))
    results.append(CheckResult("user_story_file_exists", bool(user_story_candidates), 1 if user_story_candidates else 0, 1, f"Found {len(user_story_candidates)} user story file(s)."))

    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Check a Streamlit public data product scaffold.")
    parser.add_argument("repo", type=Path, help="Path to repository root")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of text")
    args = parser.parse_args()

    repo = args.repo.resolve()
    if not repo.exists():
        raise SystemExit(f"Repository path does not exist: {repo}")

    results = check_repo(repo)
    total = sum(r.points for r in results)
    max_total = sum(r.max_points for r in results)

    if args.json:
        print(json.dumps({"total": total, "max_total": max_total, "checks": [asdict(r) for r in results]}, indent=2))
        return

    print(f"Score: {total}/{max_total}\n")
    for r in results:
        status = "PASS" if r.passed else "FAIL"
        print(f"[{status}] {r.name}: {r.points}/{r.max_points} — {r.message}")


if __name__ == "__main__":
    main()
