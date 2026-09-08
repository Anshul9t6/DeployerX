"""Paste-ready prompt assembly: playbook prompt + owner FAQ + locale cascade."""

import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from decision.prompt import (
    FAQ_PLACEHOLDER,
    assemble_prompt,
    available_languages,
    build_prompt,
    main,
    parse_locale,
)
from decision.resolve import LocaleRef

FAQ = "दुकान: टेस्ट किराना\nआटा 1kg: ₹45"


class Assemble(unittest.TestCase):
    def test_placeholder_replaced(self):
        out = assemble_prompt(f"rules\n\n{FAQ_PLACEHOLDER}\n", FAQ, None)
        self.assertNotIn(FAQ_PLACEHOLDER, out)
        self.assertIn("₹45", out)

    def test_no_placeholder_appends_faq(self):
        out = assemble_prompt("rules only", FAQ, None)
        self.assertTrue(out.startswith("rules only"))
        self.assertIn("₹45", out)

    def test_locale_cascade_appended_leaf_last(self):
        out = assemble_prompt("rules", FAQ, LocaleRef("in", "rajasthan", "jaipur"))
        self.assertIn("## Local context", out)
        self.assertLess(out.index("_global/constraints.md"), out.index("jaipur/constraints.md"))

    def test_missing_l3_falls_back_without_error(self):
        out = assemble_prompt("rules", FAQ, LocaleRef("in", "rajasthan", "no-such-district"))
        self.assertIn("locale-packs/in/constraints.md", out)


class Build(unittest.TestCase):
    def test_languages_listed_for_both_playbooks(self):
        for pb in ("whatsapp-shop-faq", "clinic-whatsapp-faq"):
            self.assertTrue({"en", "hi", "pt"} <= set(available_languages(pb)), pb)

    def test_build_hi_prompt_contains_owner_faq_and_rules(self):
        out = build_prompt("whatsapp-shop-faq", FAQ, LocaleRef("in", "rajasthan", "jaipur"), "hi")
        self.assertIn("टेस्ट किराना", out)
        self.assertIn("मालिक", out)
        self.assertIn("Jaipur", out)

    def test_empty_faq_refused(self):
        with self.assertRaises(SystemExit):
            build_prompt("whatsapp-shop-faq", "   ", None, "hi")

    def test_unknown_language_refused(self):
        with self.assertRaises(SystemExit):
            build_prompt("whatsapp-shop-faq", FAQ, None, "xx")

    def test_unknown_playbook_refused(self):
        with self.assertRaises(SystemExit):
            build_prompt("no-such-playbook", FAQ, None, "hi")

    def test_parse_locale_shapes(self):
        self.assertEqual(parse_locale("in"), LocaleRef("in", None, None))
        self.assertEqual(parse_locale("br/sao-paulo/sao-paulo"), LocaleRef("br", "sao-paulo", "sao-paulo"))
        with self.assertRaises(SystemExit):
            parse_locale("a/b/c/d")


class Cli(unittest.TestCase):
    def test_writes_out_file_and_prints_to_stderr_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            faq = Path(tmp) / "faq.txt"
            faq.write_text(FAQ, encoding="utf-8")
            out = Path(tmp) / "prompt.txt"
            stdout, stderr = io.StringIO(), io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                code = main(
                    ["whatsapp-shop-faq", "--faq", str(faq), "--locale", "in/rajasthan/jaipur", "--out", str(out)]
                )
            self.assertEqual(code, 0)
            self.assertEqual(stdout.getvalue(), "")
            self.assertIn("wrote", stderr.getvalue())
            self.assertIn("₹45", out.read_text(encoding="utf-8"))

    def test_stdout_mode_emits_only_the_prompt(self):
        with tempfile.TemporaryDirectory() as tmp:
            faq = Path(tmp) / "faq.txt"
            faq.write_text(FAQ, encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                main(["clinic-whatsapp-faq", "--faq", str(faq), "--lang", "pt"])
            self.assertTrue(stdout.getvalue().startswith("# Instruções"))


if __name__ == "__main__":
    unittest.main()
