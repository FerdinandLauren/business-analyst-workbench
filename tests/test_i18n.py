import unittest

from src.i18n import LANGS, STRINGS, detect_language, t

CATEGORY_KEYS = (
    "scheduling", "intake", "approval", "payment", "reporting", "tracking",
    "notification", "validation", "integration", "audit", "search", "access",
    "inventory", "support", "unclassified", "nfr_security", "nfr_performance",
    "nfr_availability", "nfr_compliance", "nfr_usability", "nfr_maintainability",
)

FUNCTIONAL_KEYS = CATEGORY_KEYS[:15]  # includes "unclassified"


class I18nTests(unittest.TestCase):
    def test_languages(self):
        self.assertEqual(LANGS, ("en", "id"))

    def test_key_parity(self):
        en = set(STRINGS["en"])
        id_keys = set(STRINGS["id"])
        self.assertEqual(
            sorted(en - id_keys), [],
            msg="keys missing from 'id': %s" % sorted(en - id_keys),
        )
        self.assertEqual(
            sorted(id_keys - en), [],
            msg="keys missing from 'en': %s" % sorted(id_keys - en),
        )

    def test_format(self):
        self.assertTrue(t("ui.stale_input", "id"))
        self.assertIn("x", t("req.clarification", "en", fragment="x"))
        self.assertIn("x", t("req.clarification", "id", fragment="x"))

    def test_unknown_key_raises(self):
        with self.assertRaises(KeyError):
            t("nope", "en")

    def test_detect_id(self):
        self.assertEqual(detect_language("Pasien mendaftar lewat telepon"), "id")

    def test_detect_en(self):
        self.assertEqual(detect_language("Managers need a dashboard"), "en")

    def test_detect_empty(self):
        self.assertEqual(detect_language(""), "en")
        self.assertEqual(detect_language("   "), "en")

    def test_all_categories_have_labels(self):
        for lang in LANGS:
            for key in CATEGORY_KEYS:
                with self.subTest(lang=lang, key=key):
                    self.assertTrue(STRINGS[lang][f"cat.{key}"].strip())

    def test_every_category_has_uat_and_brd_strings(self):
        for lang in LANGS:
            for key in FUNCTIONAL_KEYS:
                with self.subTest(lang=lang, key=key):
                    self.assertTrue(f"uat.precondition_{key}" in STRINGS[lang])
                    self.assertTrue(f"uat.expected_{key}" in STRINGS[lang])
                    if key != "unclassified":
                        self.assertTrue(f"brd.assumption_{key}" in STRINGS[lang])
            for key in CATEGORY_KEYS[15:]:
                with self.subTest(lang=lang, key=key):
                    self.assertTrue(f"req.{key}" in STRINGS[lang])
            self.assertTrue("brd.assumption_general" in STRINGS[lang])
            self.assertTrue("brd.assumption_nfr" in STRINGS[lang])

    def test_steps_are_numbered(self):
        for lang in LANGS:
            for key in ("approval", "payment", "reporting", "scheduling", "unclassified"):
                with self.subTest(lang=lang, key=key):
                    self.assertTrue(STRINGS[lang][f"uat.steps_{key}"].startswith("1."))


if __name__ == "__main__":
    unittest.main()
