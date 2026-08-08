"""DeployerX decision engine — world-scalable recommendation CLI."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from decision.resolve import LocaleRef, explain, resolve

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


PLAYBOOKS = {
    "whatsapp-shop-faq": {
        "title": "WhatsApp shop FAQ",
        "path": "playbooks/whatsapp-shop-faq/",
        "when": "Repeat customer questions on chat apps for a shop/service",
    },
    "clinic-whatsapp-faq": {
        "title": "Clinic WhatsApp FAQ",
        "path": "playbooks/clinic-whatsapp-faq/",
        "when": "Non-clinical clinic/lab FAQs — never medical advice",
    },
}


def _pick_playbook(use_case: str, channel: str) -> str | None:
    if use_case in {"clinic", "lab", "diagnostic"} and channel == "whatsapp":
        return "clinic-whatsapp-faq"
    if use_case in {"shop_faq", "retail", "kirana"} and channel == "whatsapp":
        return "whatsapp-shop-faq"
    return None


def recommend(a: Answers) -> list[str]:
    ref = LocaleRef(country=a.country, l2=a.l2 or None, l3=a.l3 or None)
    resolved = resolve(ref)

    lines: list[str] = [
        "## DeployerX recommendation",
        "",
        f"- Locale id: `{resolved.id}`",
        f"- Cascade layers found: **{len(resolved.layers)}**",
    ]
    for layer in resolved.layers:
        lines.append(f"  - `{layer.relative_to(ROOT)}`")
    lines.append(f"- Language bias: **{a.language}**")
    lines.append("")

    pb_id = _pick_playbook(a.use_case, a.channel)
    if pb_id:
        pb = PLAYBOOKS[pb_id]
        lines.extend(
            [
                f"### Playbook (global): {pb['title']}",
                f"- Path: `{pb['path']}`",
                f"- Why: {pb['when']}",
                "- Local deltas come from L1/L2/L3 constraints — do not fork the playbook",
            ]
        )
    else:
        lines.extend(
            [
                "### Playbook",
                "- No exact match yet. Try `whatsapp-shop-faq` or `clinic-whatsapp-faq` if chat is the channel.",
                "- Add new recipes as **global** playbooks; keep locale-specific notes in locale packs.",
            ]
        )

    lines.append("")
    lines.append("### Constraints applied")
    if a.budget <= 0:
        lines.append("- Budget **Zero**: browser AI + copy-paste chat; human approval required")
    elif a.budget <= 2000:
        lines.append("- Budget **Low**: keep human approval; light API / quick replies")
    else:
        lines.append("- Budget **Mid+**: still start with approval mode for 7 days before automation")

    if not a.has_engineer:
        lines.append("- No engineer: avoid custom servers in week one")
    if a.language in {"hi", "hindi", "hinglish"}:
        tip_playbook = pb_id or "whatsapp-shop-faq"
        lines.append(
            f"- Hindi prompts: `playbooks/{tip_playbook}/prompts/system.hi.md` + `locale-packs/in/glossary/hi.yaml`"
        )
    lines.append("- Merge constraints root→leaf; never invent prices/discounts")
    lines.extend(
        [
            "",
            "### Next 3 actions",
            "1. Open the playbook `deploy.md` and complete Path A today",
            "2. Seed/improve your L3 pack under `locale-packs/<cc>/l2/<l2>/l3/<l3>/`",
            "3. Run eval examples before customer-facing use",
            "",
            explain(ref),
        ]
    )
    return lines


def _ask(prompt: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{prompt}{suffix}: ").strip()
    return value or default


def _ask_bool(prompt: str, default: bool = False) -> bool:
    raw = _ask(prompt + " (y/n)", "y" if default else "n").lower()
    return raw in {"y", "yes", "1", "true"}


def main() -> None:
    print("DeployerX — forward-deployed AI for the rest of the world")
    print("Hierarchy: country (L1) → state/province (L2) → district (L3)")
    print("Common ships once; local packs only add deltas.\n")

    answers = Answers(
        country=_ask("Country code (ISO)", "in").lower(),
        l2=_ask("L2 slug (state/province)", "uttar-pradesh").lower(),
        l3=_ask("L3 slug (district/county, empty OK)", "varanasi").lower(),
        language=_ask("Customer language (hi, mr, ta, kn, en, ...)", "hi").lower(),
        channel=_ask("Main channel (whatsapp, phone, instagram)", "whatsapp").lower(),
        has_engineer=_ask_bool("Do you have an engineer on staff?", False),
        budget=int(_ask("Monthly budget (local currency units)", "0") or "0"),
        use_case=_ask("Use case (shop_faq, clinic, lab, coaching, other)", "shop_faq").lower(),
    )

    print()
    print("\n".join(recommend(answers)))


if __name__ == "__main__":
    main()
