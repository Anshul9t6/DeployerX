"""Decision CLI must work without a terminal (agents, CI, piped stdin)."""

import io
import unittest
from contextlib import redirect_stdout

from decision.cli import Answers, main, recommend


class Recommend(unittest.TestCase):
    def test_hindi_shop_points_at_hi_prompt_and_prompt_command(self):
        text = recommend(Answers("in", "rajasthan", "jaipur", "hi", "whatsapp", False, 0, "shop_faq"))
        self.assertIn("playbook: whatsapp-shop-faq", text)
        self.assertIn("prompts/system.hi.md", text)
        self.assertIn("python3 -m decision.prompt whatsapp-shop-faq", text)
        self.assertIn("--locale in/rajasthan/jaipur", text)
        self.assertIn("jaipur/constraints.md", text)

    def test_portuguese_clinic_adds_pt_cases_flag(self):
        text = recommend(Answers("br", "sao-paulo", "sao-paulo", "pt", "whatsapp", False, 0, "clinic"))
        self.assertIn("playbook: clinic-whatsapp-faq", text)
        self.assertIn("system.pt.md", text)
        self.assertIn("--cases cases-pt.json", text)

    def test_unknown_use_case_says_so(self):
        text = recommend(Answers("in", "rajasthan", "", "hi", "whatsapp", False, 0, "astrology"))
        self.assertIn("no exact match", text)

    def test_budget_band_lines(self):
        zero = recommend(Answers("in", "rajasthan", "jaipur", "hi", "whatsapp", False, 0, "shop_faq"))
        low = recommend(Answers("in", "rajasthan", "jaipur", "hi", "whatsapp", False, 1500, "shop_faq"))
        mid = recommend(Answers("in", "rajasthan", "jaipur", "hi", "whatsapp", True, 5000, "shop_faq"))
        self.assertIn("budget: zero", zero)
        self.assertIn("budget: low", low)
        self.assertIn("budget: mid+", mid)
        self.assertNotIn("staffing:", mid)


class NonInteractive(unittest.TestCase):
    def test_flags_run_without_prompting(self):
        out = io.StringIO()
        with redirect_stdout(out):
            code = main(["--country", "in", "--l2", "rajasthan", "--l3", "jaipur", "--language", "hi"])
        self.assertEqual(code, 0)
        self.assertIn("locale:   in/rajasthan/jaipur", out.getvalue())

    def test_no_input_uses_defaults(self):
        out = io.StringIO()
        with redirect_stdout(out):
            code = main(["--no-input"])
        self.assertEqual(code, 0)
        self.assertIn("whatsapp-shop-faq", out.getvalue())


if __name__ == "__main__":
    unittest.main()
