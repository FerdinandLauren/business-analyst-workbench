import unittest

from src.brd import brd_markdown
from src.process import analyze_process
from src.requirements import extract_requirements

DENTAL = (
    "Jadwal dokter sering bentrok karena dicatat di buku. "
    "Pasien harus menelepon untuk mendaftar dan sering harus mengulang data. "
    "Kasir menghitung pembayaran manual sehingga struk sering salah. "
    "Manajer tidak bisa melihat laporan kunjungan harian."
)

PROCUREMENT = (
    "Employees submit purchase requests through email and spreadsheets. "
    "Required information is sometimes missing, so the procurement team must ask for corrections. "
    "Approvals are handled through separate email conversations. "
    "Requesters cannot easily track request status."
)


def dental_brd(lang="en"):
    reqs = extract_requirements(DENTAL, lang)
    return brd_markdown(
        "Dental Clinic Booking",
        DENTAL,
        "Reduce double bookings and manual payment work.",
        "Clinic manager; Dentist; Front desk",
        "Appointment booking; payment records; daily reports",
        "Insurance claim processing",
        reqs,
        lang,
    )


class BrdTests(unittest.TestCase):
    def test_dental_brd_has_no_procurement_leftovers(self):
        text = dental_brd("en").lower()
        for leftover in ("erp", "supplier", "approval matrix", "cost center"):
            self.assertNotIn(leftover, text)

    def test_dental_brd_uses_detected_categories(self):
        text = dental_brd("en")
        self.assertIn("appointment scheduling", text)
        self.assertIn("payment and billing records", text)
        self.assertIn("management reports", text)

    def test_procurement_brd_mentions_approval_thresholds(self):
        reqs = extract_requirements(PROCUREMENT, "en")
        text = brd_markdown(
            "Procurement", PROCUREMENT, "Centralise requests.", "Procurement; Managers",
            "Intake; approval; tracking", "Supplier payment execution", reqs, "en",
        )
        self.assertIn("Approval thresholds", text)

    def test_traceability_pairs_every_requirement(self):
        reqs = extract_requirements(DENTAL, "en")
        text = dental_brd("en")
        rows = [
            line for line in text.splitlines()
            if line.startswith("| REQ-") and line.count("|") == 3
        ]
        self.assertEqual(len(rows), len(reqs))
        self.assertIn("| REQ-001 | UAT-001 |", text)

    def test_indonesian_headings(self):
        text = dental_brd("id")
        self.assertIn("## 1. Ringkasan eksekutif", text)
        self.assertIn("## 7. Kandidat kebutuhan", text)
        self.assertIn("Sistem harus", text)

    def test_empty_requirements_still_render(self):
        text = brd_markdown("Empty", "", "", "", "", "", [], "en")
        self.assertIn("## 1. Executive summary", text)
        self.assertIn("No candidate requirement was extracted", text)
        self.assertNotIn("| REQ-", text)
        self.assertNotIn("Traceback", text)

    def test_process_unspecified_adds_open_question(self):
        reqs = extract_requirements(DENTAL, "en")
        process = analyze_process("Email and spreadsheet", "Online booking", "en")
        text = brd_markdown(
            "Dental", DENTAL, "Objective", "Manager", "Booking", "Claims",
            reqs, "en", process=process,
        )
        self.assertIn("Which stakeholder can confirm whether", text)
        self.assertIn("Auditability", text)

    def test_nfr_only_input_does_not_raise(self):
        reqs = extract_requirements("Data must be encrypted and backed up daily.", "en")
        text = brd_markdown(
            "Security", "Data must be encrypted and backed up daily.", "Protect data.",
            "IT", "Encryption", "None", reqs, "en",
        )
        self.assertIn("Non-functional targets", text)

    def test_summary_counts_match(self):
        reqs = extract_requirements(DENTAL, "en")
        text = dental_brd("en")
        self.assertIn(f"{len(reqs)} candidate requirements", text)
        self.assertIn(f"{len(reqs)} matching UAT scenarios", text)


if __name__ == "__main__":
    unittest.main()
