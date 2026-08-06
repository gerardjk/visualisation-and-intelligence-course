"""A1 autograder — scores the automated rubric items (60/100) for
"Critique and Repair" submissions, and doubles as the student self-check.

Structure: THREE artefacts across three distinct domains (artefact 1 primary
with full critique, Decision Record and claim audit; artefacts 2–3 supporting
with compact critiques), three redesigns spanning three distinct Visual
Vocabulary categories.

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

# The four-way taxonomy taught in the Seeing Data lab notebook.
CLAIM_LABELS = {"supported", "plausible but unverified", "unsupported",
                "contradicted"}
PROBED_LABELS = {"supported", "contradicted"}  # evidence for / evidence against

META_KEYS = ["artefact_id", "domain", "source_url", "publisher",
             "publication_date", "data_status"]

# Full critique (primary): Critique 1 frame + the visible/interpretation split
# + the repaired caption from the Seeing Data Critique and Repair sheet.
CRITIQUE_KEYS = ["main_claim", "audience", "visual_task", "directly_visible",
                 "interpretation_not_observation", "what_is_omitted",
                 "what_misleads", "what_needs_verifying", "repaired_caption"]

# Compact critique (supporting artefacts 2 and 3).
COMPACT_KEYS = ["main_claim", "visible_vs_interpretation", "what_misleads",
                "repaired_caption"]

# The Chart Choice Decision Record from the Choosing Visual Forms studio.
DECISION_KEYS = ["intended_audience", "question_they_need_answered",
                 "decision_supported", "vocabulary_category",
                 "required_comparison", "selected_form", "why_it_fits",
                 "rejected_alternative", "reason_for_rejection"]

# The five-question AI disclosure taught in every class notebook.
DISCLOSURE_KEYS = ["which_assistants", "what_contributed",
                   "accepted_modified_rejected", "how_verified",
                   "limitations_remaining"]

PLACEHOLDERS = ("...", "…", "TODO", "<", "your answer")

ARTEFACTS = (1, 2, 3)


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


def _is_df(obj):
    try:
        import pandas as pd
        return isinstance(obj, pd.DataFrame)
    except ImportError:
        return obj is not None


# ---------------------------------------------------------------- checks
# Each check: (id, max_points, description, fn(ns, exec_errors) -> (points, notes))

def check_g0(ns, errors):
    notes = [f"cell {i}: {e}" for i, e in errors]
    return (6 if not errors else 0), notes


def check_g1(ns, errors):
    """6 = three METAs complete and valid (4) + three distinct domains (2)."""
    notes, complete = [], 0
    domains = []
    for n in ARTEFACTS:
        meta = ns.get(f"META_{n}")
        if not isinstance(meta, dict):
            notes.append(f"META_{n} dict missing")
            continue
        missing = [k for k in META_KEYS if not _filled(meta.get(k, ""))]
        bad_url = not str(meta.get("source_url", "")).startswith("http")
        bad_status = meta.get("data_status") not in {"obtained", "reconstructed"}
        if missing:
            notes.append(f"META_{n} incomplete: " + ", ".join(missing))
        if bad_url:
            notes.append(f"META_{n}: source_url is not a URL")
        if bad_status:
            notes.append(f"META_{n}: data_status must be 'obtained' or 'reconstructed'")
        if not str(meta.get("artefact_id", "")).strip().upper().startswith("POOL-"):
            notes.append(f"META_{n}: artefact_id must be a pool ID (POOL-xx)")
            bad_status = True  # counts against completeness
        if not missing and not bad_url and not bad_status:
            complete += 1
        domains.append(str(meta.get("domain", "")).strip().lower())
    pts = [0, 1, 2, 4][complete]
    if len([d for d in domains if d]) == 3 and len(set(domains)) == 3:
        pts += 2
    else:
        notes.append(f"the three artefacts must come from three DISTINCT domains, got: {domains}")
    return min(pts, 6), notes


def check_g2(ns, errors):
    """9 = 3 marks per artefact: usable data (2) + provenance note/status (1)."""
    notes, pts = [], 0
    for n in ARTEFACTS:
        df = ns.get(f"data_{n}")
        if not _is_df(df):
            notes.append(f"data_{n} is not a DataFrame")
            continue
        if len(df) >= 6 and df.shape[1] >= 2 and not df.isna().all().any():
            pts += 2
        else:
            notes.append(f"data_{n} too small or has empty columns: shape {getattr(df, 'shape', '?')}")
        status = (ns.get(f"META_{n}") or {}).get("data_status")
        note = ns.get(f"RECONSTRUCTION_NOTE_{n}", "")
        if status == "reconstructed":
            if _words(note) >= 30:
                pts += 1
            else:
                notes.append(f"artefact {n}: reconstructed data requires a note ≥ 30 words")
        elif status == "obtained":
            pts += 1
        # invalid status already flagged by G1
    return min(pts, 9), notes


def check_g3(ns, errors):
    """15 = axes quality 3×3 (9) + all categories valid (2) + distinct (4)."""
    notes, pts = [], 0
    cats = []
    for n in ARTEFACTS:
        ax = ns.get(f"ax_{n}")
        if _axes_ok(ax, notes, f"redesign_{n}"):
            pts += 3
        cats.append(str(ns.get(f"CATEGORY_{n}", "")).strip().lower())
    if all(c in VOCAB for c in cats):
        pts += 2
    else:
        notes.append(f"categories must come from the Vocabulary, got: {cats}")
    if len(set(cats)) == 3:
        pts += 4
    else:
        notes.append("the three redesigns must serve three DISTINCT categories")
    return min(pts, 15), notes


def check_g4(ns, errors):
    """14 — claim audit on the primary artefact's data (unchanged shape)."""
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
        notes.append("labels must be: supported / plausible but unverified / "
                     "unsupported / contradicted")
    coverage = ("supported" in labels
                and "plausible but unverified" in labels
                and ("unsupported" in labels or "contradicted" in labels))
    if coverage:
        pts += 2
    else:
        notes.append("need ≥ 1 supported, ≥ 1 plausible but unverified, and "
                     "≥ 1 unsupported or contradicted")
    checkable = [c for c, v in claims.items()
                 if str(v).strip().lower() in PROBED_LABELS]
    if not isinstance(probes, dict):
        return pts, notes + ["probes dict missing"]
    if not checkable:
        return pts, notes + ["no supported/contradicted claims — nothing to probe"]
    probe_pts = 6
    for c in checkable:
        fn = probes.get(c)
        if not callable(fn):
            notes.append(f"no probe for claim needing evidence: {c[:60]}")
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
    """6 = full primary critique (2) + compact critiques 2–3 (1 each) +
    full Decision Record (1) + supporting defences WHY_2/WHY_3 (1)."""
    notes, pts = [], 0
    critique = ns.get("critique_1")
    if isinstance(critique, dict):
        bad = [k for k in CRITIQUE_KEYS
               if not _filled(critique.get(k, ""))
               or not 5 <= _words(critique.get(k, "")) <= 150]
        if bad:
            notes.append("critique_1 fields missing or outside 5–150 words: "
                         + ", ".join(bad))
        else:
            pts += 2
    else:
        notes.append("critique_1 dict missing")
    for n in (2, 3):
        c = ns.get(f"critique_{n}")
        if isinstance(c, dict):
            bad = [k for k in COMPACT_KEYS
                   if not _filled(c.get(k, ""))
                   or not 5 <= _words(c.get(k, "")) <= 150]
            if bad:
                notes.append(f"critique_{n} fields missing or outside 5–150 words: "
                             + ", ".join(bad))
            else:
                pts += 1
        else:
            notes.append(f"critique_{n} dict missing")
    record = ns.get("decision_record")
    if isinstance(record, dict):
        bad = [k for k in DECISION_KEYS if not _filled(record.get(k, ""))]
        thin = [k for k in ("why_it_fits", "reason_for_rejection")
                if _words(record.get(k, "")) < 10]
        if bad or thin:
            if bad:
                notes.append("decision_record incomplete: " + ", ".join(bad))
            if thin:
                notes.append("decision_record needs ≥ 10 words for: " + ", ".join(thin))
        else:
            pts += 1
    else:
        notes.append("decision_record dict missing")
    whys_ok = all(_words(ns.get(f"WHY_{n}", "")) >= 10
                  and _filled(ns.get(f"WHY_{n}", "")) for n in (2, 3))
    if whys_ok:
        pts += 1
    else:
        notes.append("WHY_2 and WHY_3 must each defend the redesign in ≥ 10 words")
    return min(pts, 6), notes


def check_g6(ns, errors):
    d = ns.get("disclosure")
    if not isinstance(d, dict):
        return 0, ["disclosure dict missing"]
    bad = [k for k in DISCLOSURE_KEYS if not _filled(d.get(k, ""), 3)]
    return (4 if not bad else 0), (["disclosure incomplete: " + ", ".join(bad)] if bad else [])


CHECKS = [
    ("G0", 6, "Notebook executes end-to-end", check_g0),
    ("G1", 6, "Three artefacts: metadata valid, domains distinct", check_g1),
    ("G2", 9, "Data provenance ×3", check_g2),
    ("G3", 15, "Redesign mechanics ×3, categories distinct", check_g3),
    ("G4", 14, "Claim-audit structure (four-way taxonomy, primary artefact)", check_g4),
    ("G5", 6, "Critiques (full + 2 compact) and Decision Record", check_g5),
    ("G6", 4, "Five-question AI disclosure", check_g6),
]

HUMAN_ITEMS = [
    ("H1", 10, "Critique insight, judged on the primary critique (0/1/2 × 5)"),
    ("H2", 5, "Reconstruction fidelity across artefacts (0/1/2 × 2.5)"),
    ("H3", 10, "Decision Record + supporting defences (0/1/2 × 5)"),
    ("H4", 10, "Redesign craft across the three (0/1/2 × 5)"),
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
    meta = ns.get("META_1") or {}
    report = {
        "notebook": str(path),
        "student_id": ns.get("STUDENT_ID", "?"),
        "artefacts": [(ns.get(f"META_{n}") or {}).get("artefact_id", "?")
                      for n in ARTEFACTS],
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
