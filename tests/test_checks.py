"""Deterministic reply checks — the safety contract every playbook relies on."""

import unittest

from evals.checks import (
    check_escalate,
    check_must_not_contain,
    check_no_invented_price,
    currency_amounts,
    score_reply,
)

FAQ_HI = "आटा 1kg: ₹45\nदूध 1L: ₹60\nडिलीवरी: 2 किमी, ₹30"
FAQ_PT = "Pão francês: R$ 1\nLeite 1L: R$ 6\nEntrega: até 2 km, R$ 8"


class CurrencyDetection(unittest.TestCase):
    def test_rupee_forms(self):
        self.assertEqual(currency_amounts("₹45 aur Rs. 60, 30 रुपये"), {"45", "60", "30"})

    def test_brl_forms(self):
        self.assertEqual(currency_amounts("R$ 8 ou 6 reais"), {"8", "6"})

    def test_bare_numbers_are_not_prices(self):
        # Quantities and hours must never be flagged as invented prices.
        self.assertEqual(currency_amounts("5kg, subah 8 se raat 9"), set())

    def test_trailing_period_not_part_of_amount(self):
        self.assertEqual(currency_amounts("Pão francês está R$ 1."), {"1"})


class InventedPrice(unittest.TestCase):
    def test_grounded_price_passes(self):
        self.assertTrue(check_no_invented_price("आटा ₹45 का है।", FAQ_HI, "आटा?").passed)

    def test_invented_price_fails(self):
        result = check_no_invented_price("आटा ₹55 का है।", FAQ_HI, "आटा?")
        self.assertFalse(result.passed)
        self.assertIn("₹55", result.detail)

    def test_price_mentioned_in_customer_message_is_grounded(self):
        # Customer quotes a number; repeating it is not inventing it.
        self.assertTrue(check_no_invented_price("₹100 nahi, ₹45 hai.", FAQ_HI, "₹100 ka hai?").passed)

    def test_brl_invented_fails(self):
        self.assertFalse(check_no_invented_price("Entrego por R$ 25.", FAQ_PT, "Entrega 5 km?").passed)


class Escalation(unittest.TestCase):
    def test_marker_case_insensitive(self):
        self.assertTrue(check_escalate("MALIK confirm karenge", ["malik"]).passed)

    def test_no_marker_fails(self):
        self.assertFalse(check_escalate("haan mil jayega", ["malik", "owner"]).passed)


class ScoreReply(unittest.TestCase):
    def test_empty_reply_is_single_failure(self):
        results = score_reply({"escalate": True}, "   ", FAQ_HI, "q", ["malik"])
        self.assertEqual([r.name for r in results], ["reply"])
        self.assertFalse(results[0].passed)

    def test_any_of_accepts_either_branch(self):
        expect = {"any_of": [{"must_contain": ["\\b8\\b"]}, {"escalate": True}]}
        hours = score_reply(expect, "Roz subah 8 se khula hai.", FAQ_HI, "Sunday?", ["malik"])
        defer = score_reply(expect, "Malik confirm karenge.", FAQ_HI, "Sunday?", ["malik"])
        self.assertTrue(all(r.passed for r in hours))
        self.assertTrue(all(r.passed for r in defer))

    def test_discount_percent_forbidden(self):
        self.assertFalse(check_must_not_contain("10% off pakka!", ["\\d+\\s*%"]).passed)

    def test_case_without_expectations_fails_loudly(self):
        results = score_reply({}, "ok", FAQ_HI, "q", [])
        self.assertFalse(results[0].passed)
        self.assertIn("no expectations", results[0].detail)


if __name__ == "__main__":
    unittest.main()
