import unittest
from src.analyzer import classify_requirement, extract_candidate_requirements, analyze_process, make_uat_cases

class AnalyzerTests(unittest.TestCase):
    def test_nonfunctional_classification(self):
        self.assertEqual(classify_requirement("The system must provide audit logs"), "Non-functional")

    def test_functional_classification(self):
        self.assertEqual(classify_requirement("The system routes requests for approval"), "Functional")

    def test_extract_requirements(self):
        result = extract_candidate_requirements("Managers need a dashboard.\nUsers need status tracking.")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "REQ-001")

    def test_process_analysis_returns_five_areas(self):
        result = analyze_process("Email approval", "Workflow approval with status dashboard and audit log")
        self.assertEqual(len(result), 5)

    def test_uat_cases_match_requirements(self):
        reqs = extract_candidate_requirements("The system sends notifications.")
        cases = make_uat_cases(reqs)
        self.assertEqual(cases[0]["requirement_id"], reqs[0]["id"])

if __name__ == "__main__":
    unittest.main()
