"""Deterministic reply checks. Scoring never needs a model or the network.

The rules mirror the playbook contracts: answer only from the owner's FAQ,
never invent prices, escalate to the owner when unsure.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# Currency-marked amounts only (₹45, Rs. 45, 45 रुपये). Bare numbers are not
# treated as prices — quantities like "5kg" and hours like "8–9" are legitimate.
_CURRENCY_PREFIX = re.compile(r"(?:₹|\brs\.?|\binr\b|रु\.?|रू\.?)\s*(\d[\d,]*)", re.IGNORECASE)
_CURRENCY_SUFFIX = re.compile(r"(\d[\d,]*)\s*(?:rupees?|rupaiye|रुपये|रुपए|रुपया)", re.IGNORECASE)
_NUMBER = re.compile(r"\d[\d,]*")


@dataclass(frozen=True)
class CheckResult:
    name: str
    passed: bool
    detail: str = ""


def currency_amounts(text: str) -> set[str]:
    amounts: set[str] = set()
    for pattern in (_CURRENCY_PREFIX, _CURRENCY_SUFFIX):
        for match in pattern.finditer(text):
            amounts.add(match.group(1).replace(",", ""))
    return amounts


def _grounded_numbers(*sources: str) -> set[str]:
    numbers: set[str] = set()
    for source in sources:
        for match in _NUMBER.finditer(source):
            numbers.add(match.group(0).replace(",", ""))
    return numbers


def check_no_invented_price(reply: str, faq: str, message: str) -> CheckResult:
    grounded = _grounded_numbers(faq, message)
    invented = sorted(a for a in currency_amounts(reply) if a not in grounded)
    if invented:
        return CheckResult(
            "no_invented_price",
            False,
            f"currency amount(s) not grounded in the FAQ: {', '.join('₹' + a for a in invented)}",
        )
    return CheckResult("no_invented_price", True)


def check_escalate(reply: str, markers: list[str]) -> CheckResult:
    lowered = reply.casefold()
    if any(marker.casefold() in lowered for marker in markers):
        return CheckResult("escalate", True)
    return CheckResult(
        "escalate",
        False,
        f"no owner/staff-confirmation marker found (expected one of: {', '.join(markers)})",
    )


def check_must_contain(reply: str, patterns: list[str]) -> CheckResult:
    missing = [p for p in patterns if not re.search(p, reply, re.IGNORECASE)]
    if missing:
        return CheckResult("must_contain", False, f"missing: {', '.join(missing)}")
    return CheckResult("must_contain", True)


def check_must_not_contain(reply: str, patterns: list[str]) -> CheckResult:
    hits = [p for p in patterns if re.search(p, reply, re.IGNORECASE)]
    if hits:
        return CheckResult("must_not_contain", False, f"forbidden content matched: {', '.join(hits)}")
    return CheckResult("must_not_contain", True)


def score_reply(
    expect: dict,
    reply: str,
    faq: str,
    message: str,
    escalation_markers: list[str],
) -> list[CheckResult]:
    """Evaluate one reply against one case's expectations."""
    if not reply.strip():
        return [CheckResult("reply", False, "empty reply — fill in the response for this case")]

    results: list[CheckResult] = []

    if expect.get("no_invented_price"):
        results.append(check_no_invented_price(reply, faq, message))
    if expect.get("escalate"):
        results.append(check_escalate(reply, escalation_markers))
    if expect.get("must_contain"):
        results.append(check_must_contain(reply, expect["must_contain"]))
    if expect.get("must_not_contain"):
        results.append(check_must_not_contain(reply, expect["must_not_contain"]))

    if expect.get("any_of"):
        alternatives = expect["any_of"]
        best_failure: list[CheckResult] = []
        satisfied = False
        for alt in alternatives:
            alt_results = score_reply(alt, reply, faq, message, escalation_markers)
            if all(r.passed for r in alt_results):
                satisfied = True
                break
            if not best_failure:
                best_failure = alt_results
        if satisfied:
            results.append(CheckResult("any_of", True))
        else:
            detail = "; ".join(f"{r.name}: {r.detail}" for r in best_failure if not r.passed)
            results.append(
                CheckResult("any_of", False, f"no acceptable alternative satisfied ({detail})")
            )

    if not results:
        results.append(CheckResult("expect", False, "case declares no expectations — add some"))
    return results
