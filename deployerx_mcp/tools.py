"""Tool implementations for the DeployerX MCP server.

Kept SDK-free (stdlib only) so `make check` exercises them without installing
the `mcp` package. Every function reads files inside this repository and
returns text; nothing here touches the network.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from decision.playbooks import load_playbooks, pick_playbook
from decision.prompt import assemble_prompt, read_faq
from decision.resolve import LocaleRef, explain, merged_constraints
from evals.cases import load_suite
from evals.run import format_scorecard, score_suite

LOCALE_PACKS = ROOT / "locale-packs"
PLAYBOOK_GUIDE_FILES = (
    "README.md",
    "decide.md",
    "deploy.md",
    "deploy.hi.md",
    "operator-card.hi.md",
    "cost.md",
)


def _locale_ref(country: str, l2: str, l3: str) -> LocaleRef | None:
    if not country:
        return None
    return LocaleRef(country=country.lower(), l2=l2.lower() or None, l3=l3.lower() or None)


def playbook_catalog() -> str:
    playbooks = load_playbooks()
    if not playbooks:
        return "No playbooks registered."
    lines = ["DeployerX playbooks (global — locale packs overlay them, never fork them):", ""]
    for pb in playbooks:
        lines.append(f"- {pb.id}: {pb.title}")
        lines.append(f"  when: {pb.when}")
        lines.append(f"  use_cases: {', '.join(pb.use_cases)} | channels: {', '.join(pb.channels)}")
    return "\n".join(lines)


def choose_playbook(use_case: str, channel: str) -> str:
    pb = pick_playbook(use_case.lower(), channel.lower())
    if pb is None:
        return (
            f"No playbook matches use_case='{use_case}' channel='{channel}'.\n"
            f"Known options:\n{playbook_catalog()}"
        )
    return (
        f"playbook: {pb.id}\npath: {pb.path}\nwhy: {pb.when}\n"
        f"Next: call get_playbook('{pb.id}') for the full guide, "
        f"then build_system_prompt with the owner's FAQ and locale."
    )


def playbook_guide(playbook_id: str) -> str:
    directory = ROOT / "playbooks" / playbook_id
    if not directory.is_dir():
        known = ", ".join(pb.id for pb in load_playbooks())
        raise ValueError(f"unknown playbook '{playbook_id}' — known: {known}")
    sections: list[str] = []
    for name in PLAYBOOK_GUIDE_FILES:
        path = directory / name
        if path.exists():
            sections.append(f"<!-- {name} -->\n{path.read_text(encoding='utf-8').strip()}")
    prompts = sorted(p.name for p in (directory / "prompts").glob("system.*.md"))
    sections.append(
        "<!-- prompts -->\nAvailable system prompts: "
        + ", ".join(prompts)
        + "\nUse build_system_prompt to get one assembled with the FAQ and locale context."
    )
    return "\n\n".join(sections)


def locale_catalog(country: str = "") -> str:
    if not country:
        countries = sorted(
            p.name for p in LOCALE_PACKS.iterdir() if p.is_dir() and not p.name.startswith("_")
        )
        return (
            "Countries with locale packs: "
            + ", ".join(countries)
            + "\nCall locale_catalog(country='<cc>') to list regions."
        )
    base = LOCALE_PACKS / country.lower()
    if not base.is_dir():
        raise ValueError(f"no locale pack for country '{country}'")
    lines = [f"Locale tree for '{country.lower()}' (L2 regions; L3 districts in brackets):"]
    for l2_dir in sorted((base / "l2").glob("*/")):
        l3 = sorted(p.name for p in (l2_dir / "l3").glob("*/"))
        suffix = f"  [{', '.join(l3)}]" if l3 else ""
        lines.append(f"- {l2_dir.name}{suffix}")
    return "\n".join(lines)


def locale_context(country: str, l2: str = "", l3: str = "") -> str:
    ref = _locale_ref(country, l2, l3)
    if ref is None:
        raise ValueError("country is required (e.g. 'in')")
    constraints = merged_constraints(ref)
    body = constraints if constraints else "(no constraints found for this path)"
    return f"{explain(ref)}\n\n--- merged constraints (root→leaf, local wins) ---\n\n{body}"


def system_prompt(
    playbook_id: str,
    faq: str = "",
    country: str = "",
    l2: str = "",
    l3: str = "",
    language: str = "",
    faq_path: str = "",
) -> str:
    suite = load_suite(playbook_id)
    prompt_path = suite.prompt_path
    if language:
        candidate = ROOT / "playbooks" / playbook_id / "prompts" / f"system.{language}.md"
        if not candidate.exists():
            available = sorted(
                p.name for p in (ROOT / "playbooks" / playbook_id / "prompts").glob("system.*.md")
            )
            raise ValueError(f"no prompt for language '{language}' — available: {', '.join(available)}")
        prompt_path = candidate

    note = ""
    if faq_path.strip():
        faq = read_faq(faq_path.strip())
    if not faq.strip():
        faq = suite.faq
        note = (
            "NOTE: assembled with the playbook's SAMPLE FAQ. For a real deployment, "
            "re-run with the owner's actual FAQ text or faq_path.\n\n"
        )
    prompt = assemble_prompt(
        prompt_path.read_text(encoding="utf-8"), faq, _locale_ref(country, l2, l3)
    )
    return note + prompt


def eval_cases(playbook_id: str) -> str:
    suite = load_suite(playbook_id)
    lines = [
        f"Eval suite for {playbook_id} — {len(suite.cases)} cases.",
        f"Sample FAQ the expectations are written against:\n{suite.faq}",
        "",
        "Send each message to the assistant under test, then call "
        "run_eval with a mapping of case id -> reply.",
        "",
    ]
    for case in suite.cases:
        lines.append(f"- {case.id}: {case.message}")
        if case.note:
            lines.append(f"  expected: {case.note}")
    return "\n".join(lines)


def eval_responses(playbook_id: str, responses: dict[str, str]) -> str:
    suite = load_suite(playbook_id)
    results = score_suite(suite, {str(k): str(v) for k, v in responses.items()})
    text, ok = format_scorecard(suite, results, label="scored via MCP")
    verdict = (
        "All cases passed — safe to proceed to a human-approval pilot."
        if ok
        else "Failures above must be fixed (prompt or FAQ) before any customer-facing use."
    )
    return f"{text}\n\n{verdict}"
