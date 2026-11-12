import unittest

from src.text import (
    GREETINGS,
    MIN_SENTENCE_CHARS,
    detect_categories,
    detect_nfr,
    detect_pain,
    has_term,
    matched_terms,
    normalize,
    split_sentences,
)


class TextHelperTests(unittest.TestCase):
    def test_has_term_ignores_substrings(self):
        self.assertFalse(has_term("kirim lewat WhatsApp", "sap"))
        self.assertFalse(has_term("superb service", "erp"))
        self.assertFalse(has_term("the airport bus", "api"))
        self.assertFalse(has_term("kirim lewat WhatsApp", "app"))
        self.assertTrue(has_term("The system uses SAP", "sap"))
        self.assertTrue(has_term("The system uses SAP ERP", "erp"))

    def test_has_term_handles_multiword_and_case(self):
        self.assertTrue(has_term("Kirim lewat WhatsApp", "WhatsApp"))
        self.assertTrue(has_term("data is Double Booked", "double booked"))
        self.assertTrue(has_term("semua jadwalnya bentrok", "jadwal"))

    def test_detect_categories_whatsapp_is_not_integration(self):
        categories = detect_categories("Pasien mendaftar lewat WhatsApp")
        self.assertIn("notification", categories)
        self.assertNotIn("integration", categories)

    def test_detect_categories_real_integration(self):
        self.assertIn("integration", detect_categories("The system integrates with SAP ERP"))

    def test_detect_categories_order(self):
        self.assertEqual(detect_categories("Jadwal sering bentrok"), ["scheduling"])

    def test_detect_categories_empty(self):
        self.assertEqual(detect_categories(""), [])

    def test_detect_pain(self):
        self.assertEqual(detect_pain("Jadwal sering bentrok"), "consolidation")
        self.assertEqual(detect_pain("Kasir menghitung pembayaran manual"), "automation")
        self.assertEqual(detect_pain("tidak ada yang tahu statusnya"), "visibility")
        self.assertEqual(detect_pain("data sering salah"), "accuracy")
        self.assertEqual(detect_pain("semua berjalan lancar"), "none")

    def test_detect_nfr(self):
        self.assertEqual(detect_nfr("Response time under 2 seconds"), "performance")
        self.assertEqual(detect_nfr("Data harus terenkripsi"), "security")
        self.assertEqual(detect_nfr("Jadwal dokter"), None)

    def test_matched_terms_returns_source_terms(self):
        self.assertEqual(matched_terms("jadwal dan booking", ("jadwal", "booking", "stok")), ["jadwal", "booking"])

    def test_split_sentences(self):
        self.assertEqual(len(split_sentences("Satu. Dua? Tiga!")), 3)
        self.assertEqual(split_sentences(""), [])
        self.assertEqual(split_sentences("A\nB; C"), ["A", "B", "C"])

    def test_normalize(self):
        self.assertEqual(normalize("  Jadwal   Sering  "), "jadwal sering")

    def test_constants(self):
        self.assertEqual(MIN_SENTENCE_CHARS, 10)
        self.assertIn("halo", GREETINGS)


if __name__ == "__main__":
    unittest.main()
