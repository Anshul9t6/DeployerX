"""DeployerX CLI — recommend a playbook + locale cascade from operator constraints.

Interactive (default when stdin is a terminal):
    python3 -m decision.cli

Non-interactive (flags, CI, agents, piped stdin):
    python3 -m decision.cli --country in --l2 rajasthan --l3 jaipur --language hi --use-case shop_faq
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

from decision.playbooks import pick_playbook
from decision.resolve import LocaleRef, explain, format_constraints_excerpt, resolve

ROOT = Path(__file__).resolve().parents[1]

DEFAULTS = {
    "country": "in",
    "l2": "rajasthan",
    "l3": "jaipur",
    "language": "hi",
    "channel": "whatsapp",
    "budget": 0,
    "use_case": "shop_faq",
}

PT_ALIASES = {"pt", "pt-br", "portuguese", "português", "portugues"}
HI_ALIASES = {"hi", "hindi", "hinglish"}


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


def _prompt_lang(language: str) -> str | None:
    if language in HI_ALIASES:
        return "hi"
    if language in PT_ALIASES:
        return "pt"
    if language in {"en", "english"}:
        return "en"
    return None


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

    tip = pb.id if pb else "whatsapp-shop-faq"
    lang = _prompt_lang(a.language) or "en"
    lines.append(f"- prompts: playbooks/{tip}/prompts/system.{lang}.md")
    lines.append("- safety: never invent prices, stock, discounts, or medical/legal advice")

    locale_flag = f"--locale {resolved.id}"
    cases_flag = " --cases cases-pt.json" if lang == "pt" else ""
    lines += [
        "",
        "next",
        "1. write the owner's FAQ (prices, hours, never-list) to faq.txt",
        f"2. python3 -m decision.prompt {tip} --faq faq.txt {locale_flag} --lang {lang} --out prompt.txt",
        "3. paste prompt.txt into a browser model; owner approves every reply for 7 days",
        "4. run evals before customer-facing use:",
        f"   python3 -m evals.run prepare {tip} {locale_flag}{cases_flag}   (zero cost)",
        f"   python3 -m evals.run api {tip} {locale_flag}{cases_flag}       (Anthropic API)",
        "",
        explain(ref),
        "",
        format_constraints_excerpt(ref),
    ]
    return "\n".join(lines)


def _ask(prompt: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    try:
        value = input(f"{prompt}{suffix}: ").strip()
    except EOFError:
        print()
        return default
    return value or default


def _ask_bool(prompt: str, default: bool = False) -> bool:
    raw = _ask(f"{prompt} (y/n)", "y" if default else "n").lower()
    return raw in {"y", "yes", "1", "true"}


def _ask_int(prompt: str, default: int) -> int:
    raw = _ask(prompt, str(default))
    try:
        return int(raw)
    except ValueError:
        return default


def interactive(defaults: Answers) -> Answers:
    print("DeployerX — locale-aware playbook recommender")
    print("country (L1) → L2 → L3 · playbooks stay global\n")
    return Answers(
        country=_ask("country (ISO)", defaults.country).lower(),
        l2=_ask("L2 slug", defaults.l2).lower(),
        l3=_ask("L3 slug (optional)", defaults.l3).lower(),
        language=_ask("customer language", defaults.language).lower(),
        channel=_ask("channel", defaults.channel).lower(),
        has_engineer=_ask_bool("engineer on staff?", defaults.has_engineer),
        budget=_ask_int("monthly budget (local units)", defaults.budget),
        use_case=_ask("use case (shop_faq|clinic|lab|…)", defaults.use_case).lower(),
    )


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python3 -m decision.cli",
        description="Recommend a playbook + locale cascade. Interactive on a TTY; flags otherwise.",
    )
    p.add_argument("--country", default=DEFAULTS["country"], help="ISO country code (in, br)")
    p.add_argument("--l2", default=DEFAULTS["l2"], help="state / province slug")
    p.add_argument("--l3", default=DEFAULTS["l3"], help="district slug (optional, '' to skip)")
    p.add_argument("--language", default=DEFAULTS["language"], help="customer language (hi, en, pt)")
    p.add_argument("--channel", default=DEFAULTS["channel"])
    p.add_argument("--engineer", action="store_true", help="an engineer is on staff")
    p.add_argument("--budget", type=int, default=DEFAULTS["budget"], help="monthly budget, local units")
    p.add_argument("--use-case", default=DEFAULTS["use_case"], help="shop_faq | clinic | lab | …")
    p.add_argument(
        "--no-input",
        action="store_true",
        help="never prompt; use flags/defaults (auto when stdin is not a terminal)",
    )
    return p


def answers_from_args(args: argparse.Namespace) -> Answers:
    return Answers(
        country=args.country.lower(),
        l2=args.l2.lower(),
        l3=args.l3.lower(),
        language=args.language.lower(),
        channel=args.channel.lower(),
        has_engineer=bool(args.engineer),
        budget=int(args.budget),
        use_case=args.use_case.lower(),
    )


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    answers = answers_from_args(args)
    explicit = len(sys.argv) > 1 if argv is None else bool(argv)
    if not args.no_input and not explicit and sys.stdin.isatty():
        answers = interactive(answers)
        print()
    print(recommend(answers))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
