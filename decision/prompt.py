"""Assemble the paste-ready system prompt for a Path A deployment.

    python3 -m decision.prompt whatsapp-shop-faq --faq faq.txt --locale in/rajasthan/jaipur

Output = playbook prompt (in the chosen language) + the owner's real FAQ +
the merged locale cascade. This is exactly what deploy.md tells an operator
to paste into a browser model, without hand-editing the <<<FAQ>>> marker.
Same assembly is used by the eval runner and the MCP server.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from decision.resolve import LocaleRef, merged_constraints

ROOT = Path(__file__).resolve().parents[1]
PLAYBOOKS = ROOT / "playbooks"
FAQ_PLACEHOLDER = "<<<FAQ>>>"
DEFAULT_LANGUAGE = "en"


def parse_locale(raw: str) -> LocaleRef:
    parts = [p for p in raw.strip("/").split("/") if p]
    if not 1 <= len(parts) <= 3:
        raise SystemExit(f"locale must be cc[/l2[/l3]], got: {raw}")
    return LocaleRef(
        country=parts[0],
        l2=parts[1] if len(parts) > 1 else None,
        l3=parts[2] if len(parts) > 2 else None,
    )


def assemble_prompt(prompt_text: str, faq: str, locale: LocaleRef | None) -> str:
    """Playbook prompt + FAQ + locale cascade. Locale constraints append root→leaf."""
    if FAQ_PLACEHOLDER in prompt_text:
        prompt_text = prompt_text.replace(FAQ_PLACEHOLDER, faq.strip())
    else:
        prompt_text = f"{prompt_text.rstrip()}\n\n{faq.strip()}\n"
    if locale is not None:
        constraints = merged_constraints(locale)
        if constraints:
            prompt_text = (
                f"{prompt_text.rstrip()}\n\n"
                f"## Local context (merged from locale packs)\n\n{constraints}\n"
            )
    return prompt_text


def available_languages(playbook_id: str) -> list[str]:
    prompts = PLAYBOOKS / playbook_id / "prompts"
    return sorted(p.stem.removeprefix("system.") for p in prompts.glob("system.*.md"))


def prompt_path(playbook_id: str, language: str) -> Path:
    path = PLAYBOOKS / playbook_id / "prompts" / f"system.{language}.md"
    if not path.exists():
        known = ", ".join(available_languages(playbook_id)) or "(none)"
        raise SystemExit(
            f"no prompt for language '{language}' in {playbook_id} — available: {known}"
        )
    return path


def build_prompt(
    playbook_id: str,
    faq: str,
    locale: LocaleRef | None = None,
    language: str = DEFAULT_LANGUAGE,
) -> str:
    if not (PLAYBOOKS / playbook_id).is_dir():
        known = ", ".join(sorted(p.name for p in PLAYBOOKS.glob("*/") if not p.name.startswith("_")))
        raise SystemExit(f"unknown playbook '{playbook_id}' — known: {known}")
    if not faq.strip():
        raise SystemExit("FAQ is empty — write the owner's real prices/hours/never-list first")
    return assemble_prompt(prompt_path(playbook_id, language).read_text(encoding="utf-8"), faq, locale)


def _read_faq(source: str) -> str:
    if source == "-":
        return sys.stdin.read()
    path = Path(source)
    if not path.exists():
        raise SystemExit(f"FAQ file not found: {source}")
    return path.read_text(encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python3 -m decision.prompt",
        description="Write the paste-ready Path A system prompt from the owner's FAQ.",
    )
    parser.add_argument("playbook", help="e.g. whatsapp-shop-faq")
    parser.add_argument("--faq", required=True, help="path to the owner's FAQ text, or - for stdin")
    parser.add_argument("--locale", help="cc[/l2[/l3]], e.g. in/rajasthan/jaipur")
    parser.add_argument("--lang", default=None, help="prompt language (hi, en, pt). Default: first of hi/en")
    parser.add_argument("--out", help="write the prompt here instead of stdout")
    args = parser.parse_args(argv)

    language = args.lang
    if language is None:
        langs = available_languages(args.playbook)
        language = "hi" if "hi" in langs else (langs[0] if langs else DEFAULT_LANGUAGE)

    locale = parse_locale(args.locale) if args.locale else None
    prompt = build_prompt(args.playbook, _read_faq(args.faq), locale, language)

    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(prompt, encoding="utf-8")
        print(f"wrote {out} ({language}, locale={locale.country + '/' + '/'.join(p for p in (locale.l2, locale.l3) if p) if locale else 'none'})", file=sys.stderr)
        print("Paste it into a browser model as instructions. Owner approves every reply for 7 days.", file=sys.stderr)
    else:
        sys.stdout.write(prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
