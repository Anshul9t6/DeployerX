"""MCP tool layer: faq_path uses the same FAQ reader as decision.prompt."""

import tempfile
import unittest
from pathlib import Path

from deployerx_mcp import tools


class SystemPromptFromPath(unittest.TestCase):
    def test_txt_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "faq.txt"
            path.write_text("Shop: Path Kirana\nAtta 1kg: ₹45\n", encoding="utf-8")
            out = tools.system_prompt(
                "whatsapp-shop-faq",
                faq_path=str(path),
                country="in",
                l2="rajasthan",
                l3="jaipur",
                language="hi",
            )
        self.assertIn("Path Kirana", out)
        self.assertIn("Local context", out)
        self.assertNotIn("SAMPLE FAQ", out)

    def test_csv_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "faq.csv"
            path.write_text("question,answer\nDelivery?,2 km ₹30\n", encoding="utf-8")
            out = tools.system_prompt("whatsapp-shop-faq", faq_path=str(path), language="hi")
        self.assertIn("2 km ₹30", out)

    def test_faq_path_wins_over_pasted_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "faq.txt"
            path.write_text("FROM-FILE\n", encoding="utf-8")
            out = tools.system_prompt(
                "whatsapp-shop-faq", faq="FROM-PASTE", faq_path=str(path), language="en"
            )
        self.assertIn("FROM-FILE", out)
        self.assertNotIn("FROM-PASTE", out)

    def test_missing_path_exits(self):
        with self.assertRaises(SystemExit):
            tools.system_prompt("whatsapp-shop-faq", faq_path="/no/such/faq.txt")


if __name__ == "__main__":
    unittest.main()
