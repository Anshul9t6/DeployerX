"""DeployerX CLI — recommend a playbook + locale cascade from operator constraints."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from decision.playbooks import pick_playbook
from decision.resolve import LocaleRef, explain, format_constraints_excerpt, resolve

ROOT = Path(__file__).resolve().parents[1]


@dataclass
class Answers:
    country: str
    l2: str
    l3: str
    language: str
    channel: str
    has_engineer: bool
    budget: int
    use_case: str


def recommend(a: Answers) -> str:
    ref = LocaleRef(country=a.country, l2=a.l2 or None, l3=a.l3 or None)
    resolved = resolve(ref)
    pb = pick_playbook(a.use_case, a.channel)

    lines = [
        "DeployerX recommendation",
        "",
        f"locale:   {resolved.id}",
        f"layers:   {len(resolved.layers)}",
    ]
    for layer in resolved.layers:
        lines.append(f"          {layer.relative_to(ROOT)}")
    lines.append(f"language: {a.language}")
    lines.append("")

    if pb:
        lines += [
            f"playbook: {pb.id}",
            f"          {pb.path}",
            f"why:      {pb.when}",
        ]
    else:
        lines += [
            "playbook: (no exact match)",
            "          add an entry to playbooks/_registry.yaml or adjust use_case/channel",
        ]

    lines.append("")
    lines.append("constraints")
    if a.budget <= 0:
        lines.append("- budget: zero → browser model + manual send; approval required")
    elif a.budget <= 2000:
        lines.append("- budget: low → keep approval; light API only after clean week")
    else:
        lines.append("- budget: mid+ → still run approval for 7 days before automation")
    if not a.has_engineer:
        lines.append("- staffing: no engineer → avoid custom servers in week one")
    if a.language in {"hi", "hindi", "hinglish"}:
        tip = pb.id if pb else "whatsapp-shop-faq"
        lines.append(f"- prompts: playbooks/{tip}/prompts/system.hi.md")
    lines.append("- safety: never invent prices, stock, discounts, or medical/legal advice")
    lines += [
        "",
        "next",
        "1. open playbook deploy.md → Path A",
        "2. overlay locale-packs/<cc>/l2/<l2>/l3/<l3>/",
        "3. run evals before customer-facing use:",
        "   python3 -m evals.run prepare <playbook>   (zero cost)",
        "   python3 -m evals.run api <playbook>       (Anthropic API)",
        "",
        explain(ref),
        "",
        format_constraints_excerpt(ref),
    ]
    return "\n".join(lines)


def _ask(prompt: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{prompt}{suffix}: ").strip()
    return value or default


def _ask_bool(prompt: str, default: bool = False) -> bool:
    raw = _ask(f"{prompt} (y/n)", "y" if default else "n").lower()
    return raw in {"y", "yes", "1", "true"}


def main() -> None:
    print("DeployerX — locale-aware playbook recommender")
    print("country (L1) → L2 → L3 · playbooks stay global\n")

    answers = Answers(
        country=_ask("country (ISO)", "in").lower(),
        l2=_ask("L2 slug", "rajasthan").lower(),
        l3=_ask("L3 slug (optional)", "jaipur").lower(),
        language=_ask("customer language", "hi").lower(),
        channel=_ask("channel", "whatsapp").lower(),
        has_engineer=_ask_bool("engineer on staff?", False),
        budget=int(_ask("monthly budget (local units)", "0") or "0"),
        use_case=_ask("use case (shop_faq|clinic|lab|…)", "shop_faq").lower(),
    )
    print()
    print(recommend(answers))


if __name__ == "__main__":
    main()
