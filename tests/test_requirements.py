import unittest

from src.requirements import (
    Requirement,
    extract_requirements,
    requirements_to_rows,
)

DENTAL = (
    "Jadwal dokter sering bentrok karena dicatat di buku. "
    "Pasien harus menelepon untuk mendaftar dan sering harus mengulang data. "
    "Kasir menghitung pembayaran manual sehingga struk sering salah. "
    "Manajer tidak bisa melihat laporan kunjungan harian."
)


class RequirementTests(unittest.TestCase):
    def test_dental_categories(self):
        reqs = extract_requirements(DENTAL, "en")
        categories = {req.category for req in reqs}
        self.assertTrue({"scheduling", "payment", "reporting"} <= categories)
        self.assertNotIn("integration", categories)
        self.assertNotIn("inventory", categories)

    def test_english_statements(self):
        reqs = extract_requirements(DENTAL, "en")
        statements = [req.statement for req in reqs if req.category != "unclassified"]
        self.assertTrue(statements)
        for statement in statements:
            self.assertTrue(statement.startswith("The system shall"), statement)
            self.assertTrue(statement.endswith("."), statement)

    def test_indonesian_statements(self):
        reqs = extract_requirements(DENTAL, "id")
        statements = [req.statement for req in reqs if req.category != "unclassified"]
        self.assertTrue(statements)
        for statement in statements:
            self.assertTrue(statement.startswith("Sistem harus"), statement)

    def test_consolidation_statement_for_scheduling(self):
        req = extract_requirements("Jadwal sering bentrok karena dicatat di buku.", "en")[0]
        self.assertEqual(req.category, "scheduling")
        self.assertEqual(
            req.statement,
            "The system shall consolidate appointment scheduling so that one source of truth is used.",
        )

    def test_language_independent_of_machine_values(self):
        req = extract_requirements("Managers need a dashboard for weekly status.", "id")[0]
        self.assertEqual(req.category, "reporting")
        self.assertEqual(req.type, "Functional")
        self.assertEqual(req.priority, "Medium")
        self.assertTrue(req.statement.startswith("Sistem harus"), req.statement)

    def test_ids_are_sequential_and_unique(self):
        reqs = extract_requirements(DENTAL, "en")
        self.assertEqual([req.id for req in reqs], [f"REQ-{i:03d}" for i in range(1, len(reqs) + 1)])
        self.assertEqual(len({req.id for req in reqs}), len(reqs))

    def test_unclassified_gets_review_status_and_question(self):
        reqs = extract_requirements("Pasien harus menelepon untuk mendaftar.", "id")
        self.assertEqual(len(reqs), 1)
        req = reqs[0]
        self.assertEqual(req.category, "unclassified")
        self.assertEqual(req.status, "needs_review")
        self.assertIn("Pasien harus menelepon", req.clarification)
        self.assertTrue(req.statement.startswith("Sistem harus mendukung:"), req.statement)

    def test_audit_is_nonfunctional(self):
        req = extract_requirements("The system must provide audit logs", "en")[0]
        self.assertEqual(req.type, "Non-functional")
        self.assertEqual(req.category, "audit")
        self.assertEqual(req.priority, "High")
        self.assertEqual(req.status, "draft")

    def test_nfr_category(self):
        req = extract_requirements("Response time under 2 seconds", "en")[0]
        self.assertEqual(req.type, "Non-functional")
        self.assertEqual(req.category, "nfr_performance")
        self.assertTrue(req.statement.startswith("The system shall keep response time"), req.statement)

    def test_functional_wins_over_nfr(self):
        req = extract_requirements("Sistem harus cepat menampilkan laporan", "id")[0]
        self.assertEqual(req.category, "reporting")
        self.assertEqual(req.type, "Functional")

    def test_priority_table(self):
        reqs = extract_requirements(
            "The finance team needs payment reconciliation. Managers need a weekly report.", "en"
        )
        by_category = {req.category: req for req in reqs}
        self.assertEqual(by_category["payment"].priority, "High")
        self.assertEqual(by_category["reporting"].priority, "Medium")

    def test_empty_and_short_input(self):
        self.assertEqual(extract_requirements("", "en"), [])
        self.assertEqual(extract_requirements("   \n ", "en"), [])
        self.assertEqual(extract_requirements("ok", "en"), [])
        self.assertEqual(extract_requirements("halo", "en"), [])
        self.assertEqual(extract_requirements("halo semuanya", "en"), [])

    def test_duplicate_sentences_are_merged(self):
        reqs = extract_requirements(
            "Managers need a weekly report. Managers need a weekly report.", "en"
        )
        self.assertEqual(len(reqs), 1)

    def test_rows_are_localized(self):
        reqs = extract_requirements("Kasir mencatat pembayaran manual.", "id")
        rows = requirements_to_rows(reqs, "id")
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["ID"], "REQ-001")
        self.assertEqual(row["Kategori"], "Pembayaran")
        self.assertEqual(row["Prioritas"], "Tinggi")
        self.assertTrue(row["Pernyataan"].startswith("Sistem harus"))

    def test_rows_keep_machine_keys_out_of_display(self):
        reqs = extract_requirements(DENTAL, "en")
        rows = requirements_to_rows(reqs, "en")
        self.assertTrue(all("needs_review" not in row["Status"] for row in rows))

    def test_requirement_is_frozen(self):
        req = extract_requirements("Kasir mencatat pembayaran.", "en")[0]
        self.assertIsInstance(req, Requirement)
        with self.assertRaises(Exception):
            req.statement = "changed"


if __name__ == "__main__":
    unittest.main()
