import unittest

from src.requirements import extract_requirements
from src.uat import make_uat_cases


def req(category: str, priority: str = "Medium") -> object:
    """Build a minimal stand-in with the fields the generator reads."""
    from src.requirements import Requirement

    return Requirement(
        id="REQ-001",
        type="Non-functional" if category.startswith("nfr_") else "Functional",
        category=category,
        statement="The system shall do the thing.",
        priority=priority,
        status="draft",
        clarification="",
        source_sentence="A source sentence.",
    )


class UatTests(unittest.TestCase):
    def test_category_specific_steps(self):
        approval = make_uat_cases([req("approval")], "en")[0]
        reporting = make_uat_cases([req("reporting")], "en")[0]
        self.assertNotEqual(approval["steps"], reporting["steps"])
        self.assertTrue(approval["steps"].startswith("1."))
        self.assertTrue(reporting["steps"].startswith("1."))

    def test_requirement_id_and_priority_are_copied(self):
        cases = make_uat_cases([req("payment", "High")], "en")
        self.assertEqual(cases[0]["requirement_id"], "REQ-001")
        self.assertEqual(cases[0]["priority"], "High")

    def test_case_shape_and_ids(self):
        cases = make_uat_cases([req("approval"), req("reporting")], "en")
        self.assertEqual([case["test_id"] for case in cases], ["UAT-001", "UAT-002"])
        self.assertEqual(
            set(cases[0]),
            {
                "test_id", "requirement_id", "scenario", "preconditions", "steps",
                "expected_result", "priority", "status",
            },
        )

    def test_unclassified_and_nfr_have_content(self):
        for category in ("unclassified", "nfr_security", "inventory", "support"):
            with self.subTest(category=category):
                case = make_uat_cases([req(category)], "en")[0]
                self.assertTrue(case["steps"].strip())
                self.assertTrue(case["preconditions"].strip())
                self.assertTrue(case["expected_result"].strip())

    def test_empty_list(self):
        self.assertEqual(make_uat_cases([], "en"), [])

    def test_indonesian_wording(self):
        cases = make_uat_cases([req("approval"), req("reporting")], "id")
        joined = " ".join(case["steps"] for case in cases)
        self.assertIn("Masuk", joined)
        self.assertNotIn("Sign in", joined)

    def test_scenario_contains_statement(self):
        case = make_uat_cases([req("approval")], "en")[0]
        self.assertIn("The system shall do the thing.", case["scenario"])

    def test_end_to_end_with_extracted_requirements(self):
        reqs = extract_requirements("Kasir mencatat pembayaran manual.", "id")
        cases = make_uat_cases(reqs, "id")
        self.assertEqual(len(cases), len(reqs))
        self.assertEqual(cases[0]["requirement_id"], reqs[0].id)


if __name__ == "__main__":
    unittest.main()
