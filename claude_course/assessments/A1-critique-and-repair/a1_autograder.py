"""A1 autograder — scores the automated rubric items (60/100) for
"Critique and Repair" submissions, and doubles as the student self-check.

Marker use:   python a1_autograder.py path/to/submission.ipynb
Batch use:    python a1_autograder.py path/to/folder/
Student use:  the template's final cell calls self_check(globals()).

SECURITY: this executes student code. Run it in a sandbox/VM, not on a
machine holding anything you care about.
"""

from __future__ import annotations

import json
import sys
import traceback
from pathlib import Path

VOCAB = {"deviation", "correlation", "ranking", "distribution",
         "change over time", "magnitude", "part-to-whole", "spatial", "flow"}
CLAIM_LABELS = {"supported", "unsupported", "unverifiable"}
META_KEYS = ["student_id", "artefact_id", "source_url", "publisher",
             "publication_date", "data_status"]
CRITIQUE_KEYS = ["main_claim", "audience", "visual_task", "chart_shows",
                 "this_suggests", "what_is_omitted", "what_misleads",
                 "what_needs_verifying"]
DISCLOSURE_KEYS = ["tool_contributed", "how_checked", "i_decided", "would_not_trust"]
PLACEHOLDERS = ("...", "…", "TODO", "<", "your answer")


def _words(text):
    return len(str(text).split())


def _filled(text, min_words=1):
    t = str(text).strip()
    return (_words(t) >= min_words
            and not any(p.lower() in t.lower() for p in PLACEHOLDERS))


def _is_axes(obj):
    return obj is not None and hasattr(obj, "get_ylim") and hasattr(obj, "get_title")


def _axes_ok(ax, notes, name):
    """Titled, and honest baseline if it is a bar-family chart."""
    ok = True
    if not _is_axes(ax):
        notes.append(f"{name}: did not return a matplotlib Axes")
        return False
    if len(ax.get_title()) < 15:
        notes.append(f"{name}: title too short — title the finding, not the axes")
        ok = False
    if len(ax.patches) >= 3:  # bar-family
        if not (ax.get_ylim()[0] <= 0 or ax.get_xlim()[0] <= 0):
            notes.append(f"{name}: bar chart without a zero baseline")
            ok = False
    if not (ax.lines or ax.patches or ax.collections or ax.get_images()):
        notes.append(f"{name}: no marks drawn")
        ok = False
    return ok


# ---------------------------------------------------------------- checks
# Each check: (id, max_points, description, fn(ns, exec_errors) -> (points, notes))

def check_g0(ns, errors):
    notes = [f"cell {i}: {e}" for i, e in errors]
    return (6 if not errors else 0), notes


def check_g1(ns, errors):
    meta = ns.get("META")
    notes, pts = [], 0
    if not isinstance(meta, dict):
        return 0, ["META dict missing"]
    missing = [k for k in META_KEYS if not _filled(meta.get(k, ""))]
    if missing:
        notes.append("META incomplete: " + ", ".join(missing))
    else:
        pts += 4
    if str(meta.get("source_url", "")).startswith("http"):
        pts += 1
    else:
        notes.append("source_url is not a URL")
    if meta.get("data_status") in {"obtained", "reconstructed"}:
        pts += 1
    else:
        notes.append("data_status must be 'obtained' or 'reconstructed'")
    return pts, notes


def check_g2(ns, errors):
    notes, pts = [], 0
    df = ns.get("original_data")
    try:
        import pandas as pd
        good_df = isinstance(df, pd.DataFrame)
    except ImportError:
        good_df = df is not None
    if not good_df:
        return 0, ["original_data is not a DataFrame"]
    if len(df) >= 12 and df.shape[1] >= 2:
        pts += 4
    else:
        notes.append(f"original_data too small: {df.shape}")
    if len(df) > 0 and not df.isna().all().any():
        pts += 2
    else:
        notes.append("original_data is empty or has entirely-empty columns")
    status = (ns.get("META") or {}).get("data_status")
    note = ns.get("RECONSTRUCTION_NOTE", "")
    if status == "reconstructed":
        if _words(note) >= 30:
            pts += 4
        else:
            notes.append("reconstructed data requires a reconstruction note ≥ 30 words")
    else:
        pts += 4 if _filled(note, 5) or status == "obtained" else 0
    return pts, notes


def check_g3(ns, errors):
    notes, pts = [], 0
    axes = [("redesign_best", ns.get("ax_best"), ns.get("BEST_CATEGORY")),
            ("redesign_alt1", ns.get("ax_alt1"), ns.get("ALT1_CATEGORY")),
            ("redesign_alt2", ns.get("ax_alt2"), ns.get("ALT2_CATEGORY"))]
    cats = [str(c).strip().lower() for _, _, c in axes]
    for name, ax, _ in axes:
        if _axes_ok(ax, notes, name):
            pts += 3
    if all(c in VOCAB for c in cats):
        pts += 3
    else:
        notes.append(f"categories must come from the Vocabulary, got: {cats}")
    if len(set(cats)) == 3:
        pts += 4
    else:
        notes.append("the three redesigns must serve three DISTINCT categories")
    return min(pts, 16), notes


def check_g4(ns, errors):
    notes, pts = [], 0
    interp = str(ns.get("generated_interpretation", ""))
    claims = ns.get("claims")
    probes = ns.get("probes")
    if len(interp) >= 400:
        pts += 2
    else:
        notes.append("generated_interpretation missing or under 400 characters")
    if not isinstance(claims, dict) or not claims:
        return pts, notes + ["claims dict missing"]
    labels = [str(v).strip().lower() for v in claims.values()]
    if len(claims) >= 6:
        pts += 2
    else:
        notes.append(f"need ≥ 6 claims, got {len(claims)}")
    if all(l in CLAIM_LABELS for l in labels):
        pts += 2
    else:
        notes.append("every claim label must be supported/unsupported/unverifiable")
    if all(l in labels for l in CLAIM_LABELS):
        pts += 2
    else:
        notes.append("need at least one claim in EACH of the three categories")
    checkable = [c for c, v in claims.items()
                 if str(v).strip().lower() in {"supported", "unsupported"}]
    if not isinstance(probes, dict):
        return pts, notes + ["probes dict missing"]
    if not checkable:
        return pts, notes + ["no supported/unsupported claims — nothing to probe"]
    probe_pts = 6
    for c in checkable:
        fn = probes.get(c)
        if not callable(fn):
            notes.append(f"no probe for checkable claim: {c[:60]}")
            probe_pts = 0
            continue
        try:
            result = fn()
            empty = result is None or (hasattr(result, "__len__") and len(result) == 0)
            if empty:
                notes.append(f"probe returned nothing for: {c[:60]}")
                probe_pts = min(probe_pts, 3)
        except Exception as e:
            notes.append(f"probe crashed for: {c[:60]} ({type(e).__name__})")
            probe_pts = 0
    pts += probe_pts
    return min(pts, 14), notes


def check_g5(ns, errors):
    critique = ns.get("critique")
    if not isinstance(critique, dict):
        return 0, ["critique dict missing"]
    notes = []
    bad = [k for k in CRITIQUE_KEYS
           if not _filled(critique.get(k, "")) or not 10 <= _words(critique.get(k, "")) <= 150]
    if bad:
        notes.append("critique fields missing or outside 10–150 words: " + ", ".join(bad))
    return (4 if not bad else max(0, 4 - len(bad))), notes


def check_g6(ns, errors):
    d = ns.get("disclosure")
    if not isinstance(d, dict):
        return 0, ["disclosure dict missing"]
    bad = [k for k in DISCLOSURE_KEYS if not _filled(d.get(k, ""), 5)]
    return (4 if not bad else 0), (["disclosure incomplete: " + ", ".join(bad)] if bad else [])


CHECKS = [
    ("G0", 6, "Notebook executes end-to-end", check_g0),
    ("G1", 6, "Metadata complete and valid", check_g1),
    ("G2", 10, "Data provenance", check_g2),
    ("G3", 16, "Redesign mechanics", check_g3),
    ("G4", 14, "Claim-audit structure", check_g4),
    ("G5", 4, "Critique structure", check_g5),
    ("G6", 4, "Disclosure", check_g6),
]

HUMAN_ITEMS = [
    ("H1", 10, "Critique insight (0/1/2 × 5)"),
    ("H2", 5, "Reconstruction fidelity (0/1/2 × 2.5)"),
    ("H3", 10, "Best-form defence (0/1/2 × 5)"),
    ("H4", 10, "Redesign craft (0/1/2 × 5)"),
    ("H5", 5, "Audit judgement (0/1/2 × 2.5)"),
]


def run_checks(ns, errors):
    rows, total = [], 0
    for cid, maxp, desc, fn in CHECKS:
        try:
            pts, notes = fn(ns, errors)
        except Exception as e:
            pts, notes = 0, [f"checker crashed: {e}"]
        rows.append({"id": cid, "item": desc, "points": pts, "max": maxp,
                     "notes": notes})
        total += pts
    return rows, total


def self_check(ns):
    """Call from the notebook: a1_autograder.self_check(globals())."""
    rows, total = run_checks(dict(ns), [])
    print(f"AUTOMATED SCORE (excluding execution check): {total}/60\n")
    for r in rows:
        flag = "✓" if r["points"] == r["max"] else "✗"
        print(f" {flag} {r['id']} {r['item']}: {r['points']}/{r['max']}")
        for n in r["notes"]:
            print(f"      - {n}")
    print("\nG0 (clean end-to-end execution) is verified on the marker's machine:")
    print("Kernel → Restart & Run All must finish without errors before you submit.")
    return total


def execute_notebook(path):
    import matplotlib
    matplotlib.use("Agg")
    import nbformat
    nb = nbformat.read(path, as_version=4)
    ns, errors = {}, []
    for i, cell in enumerate(nb.cells):
        if cell.cell_type != "code":
            continue
        src = cell.source
        if "self_check(globals())" in src:
            continue  # don't recurse
        try:
            exec(compile(src, f"cell{i}", "exec"), ns)
        except Exception as e:
            errors.append((i, f"{type(e).__name__}: {e}"))
    return ns, errors


def grade(path):
    ns, errors = execute_notebook(path)
    rows, total = run_checks(ns, errors)
    meta = ns.get("META") or {}
    report = {
        "notebook": str(path),
        "student_id": meta.get("student_id", "?"),
        "artefact_id": meta.get("artefact_id", "?"),
        "automated_total": total,
        "automated_max": 60,
        "items": rows,
        "execution_errors": [f"cell {i}: {e}" for i, e in errors],
        "human_items_to_mark": [
            {"id": h, "max": m, "item": d, "score": None} for h, m, d in HUMAN_ITEMS],
    }
    out = Path(path).with_suffix(".report.json")
    out.write_text(json.dumps(report, indent=2, default=str))
    print(f"\n=== {Path(path).name} — automated: {total}/60 ===")
    for r in rows:
        flag = "✓" if r["points"] == r["max"] else "✗"
        print(f" {flag} {r['id']} {r['item']}: {r['points']}/{r['max']}")
        for n in r["notes"]:
            print(f"      - {n}")
    print(f"report → {out}")
    return report


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    target = Path(sys.argv[1])
    paths = sorted(target.glob("*.ipynb")) if target.is_dir() else [target]
    for p in paths:
        try:
            grade(p)
        except Exception:
            print(f"FAILED to grade {p}:\n{traceback.format_exc()}")


if __name__ == "__main__":
    main()
