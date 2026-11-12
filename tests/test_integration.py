"""End-to-end checks: one input, every module, both languages."""
import time
import unittest
from pathlib import Path

from src.brd import brd_markdown
from src.i18n import detect_language
from src.process import analyze_process
from src.requirements import extract_requirements, requirements_to_rows
from src.uat import make_uat_cases

DENTAL = (
    "Jadwal dokter sering bentrok karena dicatat di buku. "
    "Pasien harus menelepon untuk mendaftar dan sering mengulang data. "
    "Kasir menghitung pembayaran manual sehingga struk sering salah. "
    "Manajer tidak bisa melihat laporan kunjungan harian."
)

SAMPLE_NOTES = Path(__file__).resolve().parents[1] / "samples" / "procurement-stakeholder-notes.md"


def pipeline(problem: str, lang: str) -> str:
    reqs = extract_requirements(problem, lang)
    process = analyze_process(problem, "", lang)
    cases = make_uat_cases(reqs, lang)
    return brd_markdown(
        "Clinic Booking", problem, "Reduce double bookings.", "Clinic manager",
        "Booking; payments; reports", "Insurance claims", reqs, lang, process,
    )


class EndToEndTests(unittest.TestCase):
    def test_dental_pipeline_in_english(self):
        reqs = extract_requirements(DENTAL, "en")
        cases = make_uat_cases(reqs, "en")
        text = pipeline(DENTAL, "en")

        self.assertEqual(len(cases), len(reqs))
        self.assertTrue(all(req.statement.startswith("The system shall") for req in reqs))
        self.assertIn("## 1. Executive summary", text)
        for leftover in ("ERP", "supplier", "approval matrix", "cost center"):
            self.assertNotIn(leftover, text)
        for header in ("Statement", "Test ID"):
            self.assertIn(header, text)

    def test_dental_pipeline_in_indonesian(self):
        reqs = extract_requirements(DENTAL, "id")
        cases = make_uat_cases(reqs, "id")
        text = pipeline(DENTAL, "id")

        self.assertEqual(len(cases), len(reqs))
        self.assertTrue(all(req.statement.startswith("Sistem harus") for req in reqs))
        self.assertIn("## 1. Ringkasan eksekutif", text)
        self.assertNotIn("The system shall", text)
        self.assertEqual(text.count("| UAT-"), len(reqs))

    def test_rows_follow_language(self):
        reqs = extract_requirements(DENTAL, "en")
        english = requirements_to_rows(reqs, "en")
        indonesian = requirements_to_rows(reqs, "id")
        self.assertEqual(set(english[0]), {
            "ID", "Type", "Category", "Statement", "Priority", "Status",
        })
        self.assertEqual(set(indonesian[0]), {
            "ID", "Tipe", "Kategori", "Pernyataan", "Prioritas", "Status",
        })

    def test_same_requirements_both_languages(self):
        english = [req.category for req in extract_requirements(DENTAL, "en")]
        indonesian = [req.category for req in extract_requirements(DENTAL, "id")]
        self.assertEqual(english, indonesian)


class EdgeCaseTests(unittest.TestCase):
    def test_blank_inputs(self):
        for text in ("", "   ", "\n\n", "ok"):
            with self.subTest(text=text):
                self.assertEqual(extract_requirements(text, "en"), [])
                draft = pipeline(text, "en")
                self.assertIn("No candidate requirement was extracted", draft)
                self.assertNotIn("Traceback", draft)

    def test_very_long_input_is_fast(self):
        sentence = "Managers need a weekly report for each department. "
        paragraph = sentence * (5000 // len(sentence))
        started = time.perf_counter()
        reqs = extract_requirements(paragraph, "en")
        elapsed = time.perf_counter() - started

        self.assertLess(elapsed, 2.0)
        self.assertEqual(len(reqs), 1)
        self.assertEqual(reqs[0].category, "reporting")

    def test_mixed_indonesian_and_english(self):
        text = (
            "Pasien harus menelepon untuk mendaftar. "
            "Managers need a dashboard for weekly status. "
            "Kasir menghitung pembayaran manual."
        )
        reqs = extract_requirements(text, "en")
        categories = {req.category for req in reqs}
        self.assertTrue({"intake", "reporting", "payment"} <= categories)
        self.assertEqual(detect_language(text), "id")

    def test_sample_notes_produce_a_usable_draft(self):
        notes = SAMPLE_NOTES.read_text(encoding="utf-8")
        reqs = extract_requirements(notes, "en")
        draft = pipeline(notes, "en")
        categories = {req.category for req in reqs}

        self.assertGreaterEqual(len(reqs), 4)
        self.assertTrue({"approval", "tracking", "notification"} <= categories)
        self.assertIn("## 7. Candidate requirements", draft)
        self.assertIn("| REQ-001 |", draft)
        self.assertIn("## 10. Open questions", draft)
        self.assertTrue(all("Sample Stakeholder Notes" not in req.source_sentence for req in reqs))


if __name__ == "__main__":
    unittest.main()
