"""A1 autograder: scores the automated rubric items (60/100) for
"Reading Claims and Designing Alternatives" submissions, and doubles as the student self-check.

Structure: THREE artefacts across three distinct domains (all with a full
critique, Decision Record and claim audit; artefact 1 is the supervised primary),
three alternative views spanning at least two Visual Vocabulary categories.

Marker use:   python a1_autograder.py path/to/submission.ipynb
Batch use:    python a1_autograder.py path/to/folder/
Student use:  the template's final cell calls self_check(globals()).

SECURITY: this executes student code. Run it in a sandbox/VM, not on a
machine holding anything you care about.
"""

from __future__ import annotations

import json
import hashlib
import os
import re
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

# Full critique: Critique 1 frame + the visible/interpretation split
# + the repaired caption from the Seeing Data Critique and Repair sheet.
CRITIQUE_KEYS = ["main_claim", "audience", "visual_task", "directly_visible",
                 "interpretation_not_observation", "what_is_omitted",
                 "what_misleads", "what_needs_verifying", "repaired_caption"]

# The Chart Choice Decision Record from the Choosing Visual Forms studio.
DECISION_KEYS = ["intended_audience", "question_they_need_answered",
                 "decision_supported", "vocabulary_category",
                 "required_comparison", "selected_form", "why_it_fits",
                 "rejected_alternative", "reason_for_rejection"]

# The five-question AI disclosure taught in every class notebook.
DISCLOSURE_KEYS = ["which_assistants", "what_contributed",
                   "accepted_modified_rejected", "how_verified",
                   "limitations_remaining"]

PLACEHOLDERS = ("...", "…", "TODO", "your answer")

ARTEFACTS = (1, 2, 3)
POOL_IDS = {f"POOL-{n:02d}" for n in range(1, 13)}
POOL_DOMAINS = {
    "POOL-01": "climate science",
    "POOL-02": "public health",
    "POOL-03": "astronomy",
    "POOL-04": "wellbeing",
    "POOL-05": "economics",
    "POOL-06": "energy",
    "POOL-07": "economics",
    "POOL-08": "ecology",
    "POOL-09": "astronomy",
    "POOL-10": "energy",
    "POOL-11": "geophysics",
    "POOL-12": "transportation",
}
POOL_CHART_SHA256 = {
    "POOL-01": "f474e33a9806d641a7085d36f32ce18ec821ff27dd9f60328459427a712dd085",
    "POOL-02": "324186a6336553a3931345fdb0bcfc46be07028b6782f82598f47e602118319c",
    "POOL-03": "736779da9c9b8fb8c5d8e5d09cbbc5eb2dd81702c836ca2ccf810f1641a2edab",
    "POOL-04": "15b6160ad38f2c5cd94bebf4ff14864bcdd594bea17ec9102d3d056bcbdc735f",
    "POOL-05": "2f9d79a0ad28fbecdc52a989ce61192d50fd5197ee2f6f6417d7270dfaa45ada",
    "POOL-06": "440d148d9a45e980c62b2f77a46f839fb799af46bf27d307f05fa0957043bb41",
    "POOL-07": "25c56f0cfab022ff5c25842101c370c710becaf03cb5ff5cf80c3658225be2fd",
    "POOL-08": "67e2af3a6fd60a082571450e201475e1362a93186c4ad1c007e2d58a625951be",
    "POOL-09": "b536a9e656652a6735ef8d34f7ade1442e7c83474de731d35e557fff092d01f4",
    "POOL-10": "21bf1ad157635d0ab86440e60e08f27871b64c51926e54d4618b4b568cdbf493",
    "POOL-11": "06a4b465f352d23b0df7380c79cec9c51663621ca3a7ede8a46450e64cb2cef4",
    "POOL-12": "fd339491fedbef77d99dc3021efc099da2637d483b772d7c4028b56c9839999e",
}
POOL_DATA_SHA256 = {
    "POOL-01": "9513e0f38fb7c7405440c891d8043297aa6238f7e436e1d726057d7aa0701140",
    "POOL-02": "a03e43f26b599adf2561b72f5cc08459997bdef93f3ba717713ab5904788794a",
    "POOL-03": "cc25f9de8cba1a877fe1da28881c93ce0d231bd276a98c0d9cc10d2a873c51c9",
    "POOL-04": "f096dd0a5c957bd790f1ba2995a171eca93a1174ce7cb8f4f2db60abde863e95",
    "POOL-05": "69b47ba1fffabd4fec0bb9addb6c80378975d2ead6186ea4d0d67d5e0a0f88e7",
    "POOL-06": "8aabb132ee28c875ab894984f04192853b9fd137ce6170edb9ede389c3a27a12",
    "POOL-07": "d653f9ef0c6a548580744cc2ac6749d01b2f0f85c09fae3d14db6a34509f96d1",
    "POOL-08": "c1dda27bb635e2839e4200f8d58815a6eeefb3b7e1674b07586da937a1da3d15",
    "POOL-09": "4d0f3827ff95512cfef37294f773bb0056fb109ea21c0770554f9165bc25850d",
    "POOL-10": "92ddc4978213dfc7965010404cb8e2f0d95fd687a61b21df87c474dab6cfaf95",
    "POOL-11": "bff1b802ed148777a58a7dd0f6382a696991dc59bde57a65cbb84194994e7b5f",
    "POOL-12": "96482ea9d23f0726495388c44c1bfbefcff8d8fe388e7046cecf5276b735d3dd",
}
RUBRIC_MAX = 100
CANVAS_POINTS_POSSIBLE = 100


def _words(text):
    return len(str(text).split())


def _filled(text, min_words=1):
    t = str(text).strip()
    return (_words(t) >= min_words
            and not any(p.lower() in t.lower() for p in PLACEHOLDERS))


def _file_sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canvas_grade(rubric_total):
    """Return the rubric total on Canvas's matching 100-point scale."""
    if not 0 <= rubric_total <= RUBRIC_MAX:
        raise ValueError(f"rubric total must be between 0 and {RUBRIC_MAX}")
    return rubric_total * CANVAS_POINTS_POSSIBLE / RUBRIC_MAX


def _is_axes(obj):
    return obj is not None and hasattr(obj, "get_ylim") and hasattr(obj, "get_title")


def _includes_zero(limits):
    """Return whether zero is visible, including on a reversed axis."""
    lo, hi = sorted(limits)
    return lo <= 0 <= hi


def _bar_orientations(ax):
    """Find bar orientations without confusing a categorical axis with the baseline."""
    orientations = {
        orientation
        for container in getattr(ax, "containers", [])
        if (orientation := getattr(container, "orientation", None))
        in {"vertical", "horizontal"}
    }
    if orientations:
        return orientations

    # Fallback for bar-like Rectangle patches not stored in a BarContainer.
    patches = [
        patch for patch in getattr(ax, "patches", [])
        if all(hasattr(patch, attr) for attr in ("get_x", "get_y", "get_width", "get_height"))
    ]
    if len(patches) < 3:
        return set()
    spans_y_zero = sum(
        min(patch.get_y(), patch.get_y() + patch.get_height()) <= 0
        <= max(patch.get_y(), patch.get_y() + patch.get_height())
        for patch in patches
    )
    spans_x_zero = sum(
        min(patch.get_x(), patch.get_x() + patch.get_width()) <= 0
        <= max(patch.get_x(), patch.get_x() + patch.get_width())
        for patch in patches
    )
    return {"vertical" if spans_y_zero >= spans_x_zero else "horizontal"}


def _axes_ok(ax, notes, name):
    """Titled, and honest baseline if it is a bar-family chart."""
    ok = True
    if not _is_axes(ax):
        notes.append(f"{name}: did not return a matplotlib Axes")
        return False
    if not _filled(ax.get_title()) or len(str(ax.get_title()).strip()) < 15:
        notes.append(f"{name}: title the finding with at least 15 characters")
        ok = False
    orientations = _bar_orientations(ax)
    if "vertical" in orientations and not _includes_zero(ax.get_ylim()):
        notes.append(f"{name}: vertical bar chart without a visible zero baseline")
        ok = False
    if "horizontal" in orientations and not _includes_zero(ax.get_xlim()):
        notes.append(f"{name}: horizontal bar chart without a visible zero baseline")
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


def _matches_csv(df, path):
    """Return whether data_n is the supplied CSV, allowing harmless dtype inference."""
    try:
        import pandas as pd
        supplied = pd.read_csv(path)
        pd.testing.assert_frame_equal(
            df.reset_index(drop=True),
            supplied.reset_index(drop=True),
            check_dtype=False,
            check_like=False,
        )
        return True
    except (AssertionError, OSError, ValueError, TypeError):
        return False


# ---------------------------------------------------------------- checks
# Each check: (id, max_points, description, fn(ns, exec_errors) -> (points, notes))

def check_g0(ns, errors):
    notes = [f"cell {i}: {e}" for i, e in errors]
    return (6 if not errors else 0), notes


def check_g1(ns, errors):
    """6 = valid identity/metadata/images (4) + distinct IDs/domains (2)."""
    notes, complete = [], 0
    domains, pool_ids = [], []
    student_id_ok = _filled(ns.get("STUDENT_ID", ""))
    if not student_id_ok:
        notes.append("STUDENT_ID is missing or still a placeholder")
    for n in ARTEFACTS:
        meta = ns.get(f"META_{n}")
        if not isinstance(meta, dict):
            notes.append(f"META_{n} dict missing")
            continue
        missing = [k for k in META_KEYS if not _filled(meta.get(k, ""))]
        bad_url = not str(meta.get("source_url", "")).startswith("http")
        bad_status = meta.get("data_status") != "supplied"
        if missing:
            notes.append(f"META_{n} incomplete: " + ", ".join(missing))
        if bad_url:
            notes.append(f"META_{n}: source_url is not a URL")
        if bad_status:
            notes.append(f"META_{n}: data_status must be 'supplied'")
        pool_id = str(meta.get("artefact_id", "")).strip().upper()
        bad_pool_id = not re.fullmatch(r"POOL-\d{2}", pool_id) or pool_id not in POOL_IDS
        domain = str(meta.get("domain", "")).strip().lower()
        expected_domain = POOL_DOMAINS.get(pool_id)
        bad_domain = expected_domain is None or domain != expected_domain
        image_path = Path(f"original_chart_{n}.png")
        missing_image = not image_path.is_file() or image_path.stat().st_size == 0
        wrong_image = (not missing_image and pool_id in POOL_CHART_SHA256
                       and _file_sha256(image_path) != POOL_CHART_SHA256[pool_id])
        if bad_pool_id:
            notes.append(f"META_{n}: artefact_id must be one of POOL-01 to POOL-12")
        elif bad_domain:
            notes.append(f"META_{n}: domain must exactly match the pool value for {pool_id}: {expected_domain!r}")
        if missing_image:
            notes.append(f"required chart image missing or empty: {image_path.name}")
        elif wrong_image:
            notes.append(f"{image_path.name} does not match {pool_id}'s supplied chart")
        if not missing and not bad_url and not bad_status and not bad_pool_id and not bad_domain and not missing_image and not wrong_image:
            complete += 1
        domains.append(domain)
        pool_ids.append(pool_id)
    pts = [0, 1, 2, 4][complete]
    if not student_id_ok and pts == 4:
        pts = 3
    domains_distinct = len([d for d in domains if d]) == 3 and len(set(domains)) == 3
    domains_canonical = all(POOL_DOMAINS.get(pool_id) == domain
                            for pool_id, domain in zip(pool_ids, domains))
    ids_distinct = len(pool_ids) == 3 and len(set(pool_ids)) == 3 and all(p in POOL_IDS for p in pool_ids)
    if domains_distinct and domains_canonical and ids_distinct:
        pts += 2
    else:
        if not domains_distinct or not domains_canonical:
            notes.append(f"the three artefacts must come from three DISTINCT domains, got: {domains}")
        if not ids_distinct:
            notes.append(f"the three artefacts must use three DISTINCT valid pool IDs, got: {pool_ids}")
    return min(pts, 6), notes


def check_g2(ns, errors):
    """9 = 3 per artefact: supplied file + usable data (2), disclosure (1)."""
    notes, pts = [], 0
    for n in ARTEFACTS:
        df = ns.get(f"data_{n}")
        if not _is_df(df):
            notes.append(f"data_{n} is not a DataFrame")
            continue
        pool_id = str((ns.get(f"META_{n}") or {}).get("artefact_id", "")).strip().upper()
        source_path = Path("data") / f"{pool_id}_source_data.csv"
        expected_hash = POOL_DATA_SHA256.get(pool_id)
        source_ok = (expected_hash is not None and source_path.is_file()
                     and source_path.stat().st_size > 0
                     and _file_sha256(source_path) == expected_hash)
        data_matches_source = source_ok and _matches_csv(df, source_path)
        if len(df) >= 6 and df.shape[1] >= 2 and not df.isna().all().any() and data_matches_source:
            pts += 2
        else:
            if not source_ok:
                notes.append(f"artefact {n}: missing or modified supplied file {source_path}")
            elif not data_matches_source:
                notes.append(f"artefact {n}: data_{n} must remain the unchanged DataFrame loaded from {source_path}")
            if not (len(df) >= 6 and df.shape[1] >= 2 and not df.isna().all().any()):
                notes.append(f"data_{n} too small or has empty columns: shape {getattr(df, 'shape', '?')}")
        status = (ns.get(f"META_{n}") or {}).get("data_status")
        note = ns.get(f"TRANSFORMATION_NOTE_{n}", "")
        if status == "supplied" and _filled(note):
            pts += 1
        else:
            notes.append(f"artefact {n}: supplied data requires a completed transformation note")
        # invalid status already flagged by G1
    return min(pts, 9), notes


def check_g3(ns, errors):
    """15 = axes quality 3×3 (9) + all categories valid (2) + at least two categories (4)."""
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
    if all(c in VOCAB for c in cats) and len(set(cats)) >= 2:
        pts += 4
    else:
        notes.append("the three alternative views must represent at least TWO valid Vocabulary categories")
    return min(pts, 15), notes


def check_g4(ns, errors):
    """14: complete claim audits for all three artefacts."""
    notes, pts, all_checkable = [], 0, True
    for n in ARTEFACTS:
        interp = str(ns.get(f"generated_interpretation_{n}", ""))
        claims = ns.get(f"claims_{n}")
        probes = ns.get(f"probes_{n}")
        interpretation_words = _words(interp)
        if _filled(interp) and 150 <= interpretation_words <= 250:
            pts += 1
        else:
            notes.append(f"generated_interpretation_{n} must contain 150–250 words; got {interpretation_words}")
        if not isinstance(claims, dict) or len(claims) < 4:
            notes.append(f"claims_{n} must contain at least 4 claims")
            all_checkable = False
            continue
        labels = [str(v).strip().lower() for v in claims.values()]
        if all(label in CLAIM_LABELS for label in labels):
            pts += 1
        else:
            notes.append(f"claims_{n} contains an invalid taxonomy label")
        checkable = [claim for claim, label in claims.items()
                     if str(label).strip().lower() in PROBED_LABELS]
        if not checkable or not isinstance(probes, dict):
            notes.append(f"audit {n} needs supported/contradicted claims and probes")
            all_checkable = False
            continue
        probes_ok = True
        for claim in checkable:
            fn = probes.get(claim)
            if not callable(fn):
                notes.append(f"audit {n}: no probe for {claim[:50]}")
                probes_ok = False
                continue
            try:
                result = fn()
                if result is None or (hasattr(result, "__len__") and len(result) == 0):
                    notes.append(f"audit {n}: empty probe for {claim[:50]}")
                    probes_ok = False
            except Exception as exc:
                notes.append(f"audit {n}: probe crashed ({type(exc).__name__})")
                probes_ok = False
        if probes_ok:
            pts += 2
        else:
            all_checkable = False
    if all_checkable:
        pts += 2
    return min(pts, 14), notes


def check_g5(ns, errors):
    """6 = three full critiques (1 each) + three Decision Records (1 each)."""
    notes, pts = [], 0
    for n in ARTEFACTS:
        c = ns.get(f"critique_{n}")
        if isinstance(c, dict):
            bad = [k for k in CRITIQUE_KEYS if not _filled(c.get(k, ""))]
            if bad:
                notes.append(f"critique_{n} fields missing or incomplete: "
                             + ", ".join(bad))
            else:
                pts += 1
        else:
            notes.append(f"critique_{n} dict missing")
    for n in ARTEFACTS:
        record = ns.get(f"decision_record_{n}")
        if isinstance(record, dict):
            bad = [k for k in DECISION_KEYS if not _filled(record.get(k, ""))]
            record_category = str(record.get("vocabulary_category", "")).strip().lower()
            expected_category = str(ns.get(f"CATEGORY_{n}", "")).strip().lower()
            if record_category != expected_category:
                bad.append("vocabulary_category (must match CATEGORY_" + str(n) + ")")
            if bad:
                notes.append(f"decision_record_{n} incomplete: " + ", ".join(bad))
            else:
                pts += 1
        else:
            notes.append(f"decision_record_{n} dict missing")
    return min(pts, 6), notes


def check_g6(ns, errors):
    d = ns.get("disclosure")
    if not isinstance(d, dict):
        return 0, ["disclosure dict missing"]
    bad = [k for k in DISCLOSURE_KEYS if not _filled(d.get(k, ""), min_words=3)]
    return (4 if not bad else 0), (["disclosure incomplete: " + ", ".join(bad)] if bad else [])


CHECKS = [
    ("G0", 6, "Notebook executes end-to-end", check_g0),
    ("G1", 6, "Three artefacts: identity, files and domains valid", check_g1),
    ("G2", 9, "Data provenance ×3", check_g2),
    ("G3", 15, "Alternative-view mechanics ×3, at least two categories", check_g3),
    ("G4", 14, "Claim-audit structure ×3", check_g4),
    ("G5", 6, "Three full critiques and Decision Records ×3", check_g5),
    ("G6", 4, "Five-question AI disclosure", check_g6),
]

HUMAN_ITEMS = [
    ("H1", 10, "Critique insight across three artefacts (0/1/2 × 5)"),
    ("H2", 5, "Data handling across artefacts (0/1/2 × 2.5)"),
    ("H3", 10, "Decision Records across three artefacts (0/1/2 × 5)"),
    ("H4", 10, "Alternative-view craft across the three (0/1/2 × 5)"),
    ("H5", 5, "Audit judgement across three artefacts (0/1/2 × 2.5)"),
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
    rows, _ = run_checks(dict(ns), [])
    rows = [row for row in rows if row["id"] != "G0"]
    total = sum(row["points"] for row in rows)
    print(f"SELF-CHECK SCORE (G1–G6): {total}/54\n")
    for r in rows:
        flag = "✓" if r["points"] == r["max"] else "✗"
        print(f" {flag} {r['id']} {r['item']}: {r['points']}/{r['max']}")
        for n in r["notes"]:
            print(f"      - {n}")
    print("\nG0's remaining 6 marks are verified on the marker's machine.")
    print("Kernel → Restart & Run All must finish without errors before you submit.")
    print("An execution error loses G0 and may prevent checks that depend on the affected code.")
    return total


def execute_notebook(path):
    import matplotlib
    matplotlib.use("Agg")
    import nbformat
    path = Path(path).resolve()
    nb = nbformat.read(path, as_version=4)
    ns, errors = {}, []
    marker_cwd = Path.cwd()
    try:
        # Student paths such as data/file.csv are relative to their notebook.
        os.chdir(path.parent)
        for i, cell in enumerate(nb.cells):
            if cell.cell_type != "code":
                continue
            src = cell.source
            if "self_check(globals())" in src:
                continue  # don't recurse
            try:
                exec(compile(src, f"{path.name}:cell{i}", "exec"), ns)
            except Exception as e:
                errors.append((i, f"{type(e).__name__}: {e}"))
    finally:
        os.chdir(marker_cwd)
    return ns, errors


def grade(path):
    path = Path(path).resolve()
    ns, errors = execute_notebook(path)
    marker_cwd = Path.cwd()
    try:
        # G1's file checks (original_chart_n.png) resolve relative to the submission.
        os.chdir(path.parent)
        rows, total = run_checks(ns, errors)
    finally:
        os.chdir(marker_cwd)
    report = {
        "notebook": str(path),
        "student_id": ns.get("STUDENT_ID", "?"),
        "artefacts": [(ns.get(f"META_{n}") or {}).get("artefact_id", "?")
                      for n in ARTEFACTS],
        "automated_total": total,
        "automated_max": 60,
        "rubric_max": RUBRIC_MAX,
        "canvas_points_possible": CANVAS_POINTS_POSSIBLE,
        "canvas_grade_formula": "automated_total + human_total (out of 100); Assignment 1 group weight = 30%",
        "items": rows,
        "execution_errors": [f"cell {i}: {e}" for i, e in errors],
        "human_items_to_mark": [
            {"id": h, "max": m, "item": d, "score": None} for h, m, d in HUMAN_ITEMS],
    }
    out = Path(path).with_suffix(".report.json")
    out.write_text(json.dumps(report, indent=2, default=str))
    print(f"\n=== {Path(path).name}: automated: {total}/60 ===")
    for r in rows:
        flag = "✓" if r["points"] == r["max"] else "✗"
        print(f" {flag} {r['id']} {r['item']}: {r['points']}/{r['max']}")
        for n in r["notes"]:
            print(f"      - {n}")
    print("After H1–H5 are marked, add the human total to the automated total.")
    print("Canvas grade = rubric total out of 100; Assignment 1 contributes 30% through its group weight.")
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
