import unittest

from src.process import AREA_KEYS, analyze_process


class ProcessAnalysisTests(unittest.TestCase):
    def test_improve_when_only_in_to_be(self):
        result = analyze_process("Email and spreadsheet", "The system shows request status", "en")
        rows = {row["area"]: row for row in result["rows"]}
        self.assertEqual(rows["visibility"]["severity"], "improve")
        self.assertIn("Potential improvement", rows["visibility"]["observation"])

    def test_regression_when_only_in_as_is(self):
        result = analyze_process("Approvals are sent by email for approval", "", "en")
        rows = {row["area"]: row for row in result["rows"]}
        self.assertEqual(rows["approval"]["severity"], "regression")
        self.assertIn("Potential regression", rows["approval"]["observation"])

    def test_clarify_when_in_both(self):
        result = analyze_process("Approval by email", "Approval in the new workflow", "en")
        rows = {row["area"]: row for row in result["rows"]}
        self.assertEqual(rows["approval"]["severity"], "clarify")

    def test_unspecified_when_in_neither(self):
        result = analyze_process("Email, spreadsheet", "Online form", "en")
        rows = {row["area"]: row for row in result["rows"]}
        self.assertEqual(rows["auditability"]["severity"], "unspecified")

    def test_evidence_is_the_matched_term(self):
        result = analyze_process("Requests are approved by email", "", "en")
        rows = {row["area"]: row for row in result["rows"]}
        self.assertEqual(rows["approval"]["evidence"], "as-is: approve | to-be: -")

    def test_manual_marker_count_is_distinct(self):
        result = analyze_process("Email, spreadsheet, dan telepon", "", "id")
        self.assertEqual(result["summary"]["manual_steps"], 3)

    def test_handoff_count(self):
        result = analyze_process("Permintaan diteruskan lewat email", "", "id")
        self.assertEqual(result["summary"]["handoffs"], 1)

    def test_empty_inputs(self):
        result = analyze_process("", "", "en")
        self.assertEqual(len(result["rows"]), len(AREA_KEYS))
        self.assertTrue(all(row["severity"] == "unspecified" for row in result["rows"]))
        self.assertEqual(
            result["summary"],
            {"manual_steps": 0, "handoffs": 0, "areas_to_improve": 0},
        )

    def test_row_shape(self):
        result = analyze_process("email", "status", "en")
        for row in result["rows"]:
            self.assertEqual(set(row), {"area", "severity", "observation", "evidence"})

    def test_localized_observation(self):
        result = analyze_process("", "Sistem menampilkan status", "id")
        rows = {row["area"]: row for row in result["rows"]}
        self.assertIn("Potensi perbaikan", rows["visibility"]["observation"])

    def test_areas_to_improve_counts_improve_rows(self):
        result = analyze_process("", "status and notification", "en")
        self.assertEqual(result["summary"]["areas_to_improve"], 2)


if __name__ == "__main__":
    unittest.main()
