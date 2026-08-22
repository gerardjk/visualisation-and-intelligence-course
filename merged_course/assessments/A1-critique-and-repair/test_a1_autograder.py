import os
import shutil
import tempfile
import unittest
from pathlib import Path

import pandas as pd

import a1_autograder as grader


POOL_ROOT = Path(__file__).resolve().parent / "pool"


class FakeAxes:
    lines = [object()]
    patches = []
    collections = []

    def get_ylim(self): return (0, 10)
    def get_xlim(self): return (0, 10)
    def get_title(self): return "A sufficiently detailed finding"
    def get_images(self): return []


class ShortTitleAxes(FakeAxes):
    def get_title(self): return "Clear title"


def valid_namespace():
    ns = {"STUDENT_ID": "12345678"}
    for n in grader.ARTEFACTS:
        pool_id = f"POOL-{n:02d}"
        ns[f"META_{n}"] = {
            "artefact_id": pool_id,
            "domain": grader.POOL_DOMAINS[pool_id],
            "source_url": "https://example.org/chart",
            "publisher": "Publisher",
            "publication_date": "2026",
            "data_status": "supplied",
        }
        ns[f"ax_{n}"] = FakeAxes()
    return ns


class EnforcementTests(unittest.TestCase):
    def setUp(self):
        self.old_cwd = Path.cwd()
        self.tmp = tempfile.TemporaryDirectory()
        os.chdir(self.tmp.name)
        for n in grader.ARTEFACTS:
            pool_id = f"POOL-{n:02d}"
            shutil.copy2(POOL_ROOT / pool_id / "original_chart.png",
                         f"original_chart_{n}.png")
            Path("data").mkdir(exist_ok=True)
            shutil.copy2(POOL_ROOT / pool_id / "source_data.csv",
                         Path("data") / f"{pool_id}_source_data.csv")

    def tearDown(self):
        os.chdir(self.old_cwd)
        self.tmp.cleanup()

    def test_valid_distinct_pool_ids_and_images_receive_full_g1(self):
        points, notes = grader.check_g1(valid_namespace(), [])
        self.assertEqual((points, notes), (6, []))

    def test_duplicate_pool_ids_lose_g1_marks(self):
        ns = valid_namespace()
        ns["META_3"]["artefact_id"] = "POOL-02"
        points, notes = grader.check_g1(ns, [])
        self.assertLess(points, 6)
        self.assertTrue(any("DISTINCT valid pool IDs" in note for note in notes))

    def test_missing_student_id_loses_g1_marks(self):
        ns = valid_namespace()
        ns["STUDENT_ID"] = "..."
        points, notes = grader.check_g1(ns, [])
        self.assertLess(points, 6)
        self.assertTrue(any("STUDENT_ID" in note for note in notes))

    def test_noncanonical_domain_loses_g1_marks(self):
        ns = valid_namespace()
        ns["META_1"]["domain"] = "student invented label"
        points, notes = grader.check_g1(ns, [])
        self.assertLess(points, 6)
        self.assertTrue(any("exactly match" in note for note in notes))

    def test_invalid_pool_id_loses_g1_marks(self):
        ns = valid_namespace()
        ns["META_3"]["artefact_id"] = "POOL-99"
        points, notes = grader.check_g1(ns, [])
        self.assertLess(points, 6)
        self.assertTrue(any("POOL-01 to POOL-12" in note for note in notes))

    def test_missing_original_chart_loses_g1_marks(self):
        Path("original_chart_2.png").unlink()
        points, notes = grader.check_g1(valid_namespace(), [])
        self.assertLess(points, 6)
        self.assertTrue(any("original_chart_2.png" in note for note in notes))

    def test_wrong_original_chart_loses_g1_marks(self):
        Path("original_chart_2.png").write_bytes(b"not the supplied chart")
        points, notes = grader.check_g1(valid_namespace(), [])
        self.assertLess(points, 6)
        self.assertTrue(any("does not match" in note for note in notes))

    def test_distinct_invalid_categories_receive_no_category_points(self):
        ns = valid_namespace()
        for n, category in enumerate(("wrong-a", "wrong-b", "wrong-c"), 1):
            ns[f"CATEGORY_{n}"] = category
        points, notes = grader.check_g3(ns, [])
        self.assertEqual(points, 9)  # axes only: no validity or distinctness marks
        self.assertTrue(any("at least TWO" in note for note in notes))

    def test_two_valid_categories_receive_full_g3(self):
        ns = valid_namespace()
        for n, category in enumerate(("ranking", "correlation", "ranking"), 1):
            ns[f"CATEGORY_{n}"] = category
        points, notes = grader.check_g3(ns, [])
        self.assertEqual((points, notes), (15, []))

    def test_one_valid_category_loses_category_variety_marks(self):
        ns = valid_namespace()
        for n in grader.ARTEFACTS:
            ns[f"CATEGORY_{n}"] = "ranking"
        points, notes = grader.check_g3(ns, [])
        self.assertEqual(points, 11)
        self.assertTrue(any("at least TWO" in note for note in notes))

    def test_title_shorter_than_fifteen_characters_is_rejected(self):
        ns = valid_namespace()
        for n, category in enumerate(("ranking", "correlation", "ranking"), 1):
            ns[f"CATEGORY_{n}"] = category
            ns[f"ax_{n}"] = ShortTitleAxes()
        points, notes = grader.check_g3(ns, [])
        self.assertLess(points, 15)
        self.assertTrue(any("at least 15 characters" in note for note in notes))

    def test_four_claims_satisfy_claim_count(self):
        ns = {}
        for n in grader.ARTEFACTS:
            claim_names = [f"claim {n}-{i}" for i in range(4)]
            ns[f"generated_interpretation_{n}"] = "word " * 150
            ns[f"claims_{n}"] = {
                claim_names[0]: "supported",
                claim_names[1]: "unsupported",
                claim_names[2]: "plausible but unverified",
                claim_names[3]: "unsupported",
            }
            ns[f"probes_{n}"] = {claim_names[0]: lambda: [1]}
        points, notes = grader.check_g4(ns, [])
        self.assertEqual((points, notes), (14, []))

    def test_short_interpretations_lose_g4_marks(self):
        ns = {}
        for n in grader.ARTEFACTS:
            claim_names = [f"claim {n}-{i}" for i in range(4)]
            ns[f"generated_interpretation_{n}"] = "one word"
            ns[f"claims_{n}"] = {
                claim_names[0]: "supported",
                claim_names[1]: "unsupported",
                claim_names[2]: "plausible but unverified",
                claim_names[3]: "unsupported",
            }
            ns[f"probes_{n}"] = {claim_names[0]: lambda: [1]}
        points, notes = grader.check_g4(ns, [])
        self.assertLess(points, 14)
        self.assertTrue(any("150–250 words" in note for note in notes))

    def test_modified_supplied_csv_loses_g2_marks(self):
        ns = valid_namespace()
        for n in grader.ARTEFACTS:
            pool_id = f"POOL-{n:02d}"
            ns[f"data_{n}"] = pd.read_csv(Path("data") / f"{pool_id}_source_data.csv")
            ns[f"TRANSFORMATION_NOTE_{n}"] = "Used supplied rows and fields unchanged."
        Path("data/POOL-02_source_data.csv").write_text("a,b\n1,2\n")
        points, notes = grader.check_g2(ns, [])
        self.assertLess(points, 9)
        self.assertTrue(any("modified supplied file" in note for note in notes))

    def test_data_frame_not_loaded_from_supplied_csv_loses_g2_marks(self):
        ns = valid_namespace()
        for n in grader.ARTEFACTS:
            pool_id = f"POOL-{n:02d}"
            ns[f"data_{n}"] = pd.read_csv(Path("data") / f"{pool_id}_source_data.csv")
            ns[f"TRANSFORMATION_NOTE_{n}"] = "Used supplied rows and fields unchanged."
        ns["data_2"] = ns["data_2"].iloc[:-1].copy()
        points, notes = grader.check_g2(ns, [])
        self.assertLess(points, 9)
        self.assertTrue(any("unchanged DataFrame" in note for note in notes))

    def test_embedded_manifests_match_all_pool_files(self):
        for pool_id in sorted(grader.POOL_IDS):
            source_dir = POOL_ROOT / pool_id
            self.assertEqual(
                grader._file_sha256(source_dir / "original_chart.png"),
                grader.POOL_CHART_SHA256[pool_id],
            )
            self.assertEqual(
                grader._file_sha256(source_dir / "source_data.csv"),
                grader.POOL_DATA_SHA256[pool_id],
            )

    def test_one_word_disclosures_lose_g6_marks(self):
        ns = {"disclosure": {key: "word" for key in grader.DISCLOSURE_KEYS}}
        points, notes = grader.check_g6(ns, [])
        self.assertEqual(points, 0)
        self.assertTrue(any("disclosure incomplete" in note for note in notes))


if __name__ == "__main__":
    unittest.main()
