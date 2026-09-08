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
    faq_from_csv,
    looks_like_faq_csv,
    main,
    parse_locale,
    read_faq,
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


class CsvFaq(unittest.TestCase):
    def test_question_answer_header(self):
        text = faq_from_csv("question,answer\nआटा 1kg कितने का?,₹45\nदूध 1L?,₹60\n")
        self.assertIn("आटा 1kg कितने का?", text)
        self.assertIn("₹45", text)
        self.assertIn("₹60", text)

    def test_hindi_headers(self):
        text = faq_from_csv("प्रश्न,उत्तर\nसमय?,सुबह 8 से रात 9\n")
        self.assertIn("सुबह 8 से रात 9", text)

    def test_portuguese_headers(self):
        text = faq_from_csv('pergunta,resposta\nEntrega?,"até 2 km, R$ 8"\n')
        self.assertIn("até 2 km, R$ 8", text)

    def test_two_column_fallback(self):
        text = faq_from_csv("item,price\nAtta 1kg,₹45\n")
        self.assertIn("Atta 1kg", text)
        self.assertIn("₹45", text)

    def test_skips_incomplete_rows(self):
        text = faq_from_csv("question,answer\nkeep,₹1\norphan,\n,₹2\n")
        self.assertIn("keep", text)
        self.assertNotIn("orphan", text)
        self.assertNotIn("₹2", text)

    def test_empty_csv_refused(self):
        with self.assertRaises(SystemExit):
            faq_from_csv("question,answer\n,\n")

    def test_looks_like_detects_header(self):
        self.assertTrue(looks_like_faq_csv("question,answer\nfoo,bar"))
        self.assertFalse(looks_like_faq_csv("Shop: Test\nHours: 8-21"))

    def test_read_faq_csv_extension(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "faq.csv"
            path.write_text("\ufeffquestion,answer\nHours?,8-21\n", encoding="utf-8")
            self.assertIn("8-21", read_faq(str(path)))

    def test_cli_accepts_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            faq = Path(tmp) / "faq.csv"
            faq.write_text("question,answer\nआटा?,₹45\n", encoding="utf-8")
            out = Path(tmp) / "prompt.txt"
            code = main(
                ["whatsapp-shop-faq", "--faq", str(faq), "--locale", "in/rajasthan/jaipur", "--out", str(out)]
            )
            self.assertEqual(code, 0)
            body = out.read_text(encoding="utf-8")
            self.assertIn("₹45", body)
            self.assertNotIn("question,answer", body)


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
