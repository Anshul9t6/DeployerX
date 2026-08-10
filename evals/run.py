"""DeployerX eval runner — grade playbook behavior before customer-facing use.

Modes:
  prepare   Path A (zero paid API): write a paste bundle for a browser model
            plus a responses skeleton to fill in by hand.
  score     Grade a responses file with the deterministic checks.
  api       Generate replies via the Anthropic API, save them, then grade.
  selftest  Grade the bundled fixtures (no network) — wired into `make check`.

The system prompt under test is the playbook prompt with the sample FAQ merged
in, plus the locale cascade (`--locale in/rajasthan/jaipur`) when given —
the same assembly an operator does by hand in deploy.md.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from decision.resolve import LocaleRef, merged_constraints
from evals.cases import ROOT, EvalSuite, list_suites, load_suite
from evals.checks import CheckResult, score_reply

FAQ_PLACEHOLDER = "<<<FAQ>>>"
DEFAULT_MODEL = "claude-opus-5"
DEFAULT_OUT_DIR = ROOT / "eval-run"


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
    """Assemble a deployable system prompt: playbook prompt + FAQ + locale cascade."""
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


def build_system_prompt(suite: EvalSuite, locale: LocaleRef | None) -> str:
    return assemble_prompt(suite.prompt_path.read_text(encoding="utf-8"), suite.faq, locale)


def score_suite(suite: EvalSuite, responses: dict[str, str]) -> dict[str, list[CheckResult]]:
    return {
        case.id: score_reply(
            case.expect,
            responses.get(case.id, ""),
            suite.faq,
            case.message,
            suite.escalation_markers,
        )
        for case in suite.cases
    }


def format_scorecard(
    suite: EvalSuite, results: dict[str, list[CheckResult]], label: str
) -> tuple[str, bool]:
    lines = [f"Eval: {suite.playbook} — {len(suite.cases)} cases — {label}"]
    passed = 0
    for case in suite.cases:
        case_results = results[case.id]
        ok = all(r.passed for r in case_results)
        passed += ok
        lines.append(f"  {'PASS' if ok else 'FAIL'}  {case.id}")
        for r in case_results:
            if not r.passed:
                lines.append(f"        - {r.name}: {r.detail}")
    lines.append(f"Summary: {passed}/{len(suite.cases)} passed")
    return "\n".join(lines), passed == len(suite.cases)


def print_scorecard(suite: EvalSuite, results: dict[str, list[CheckResult]], label: str) -> bool:
    text, ok = format_scorecard(suite, results, label)
    print(text)
    return ok


def _load_responses(path: Path) -> dict[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    responses = data.get("responses", data)
    if not isinstance(responses, dict):
        raise SystemExit(f"{path}: expected a mapping of case id -> reply")
    return {str(k): str(v) for k, v in responses.items()}


# ---------------------------------------------------------------- commands


def cmd_list(_: argparse.Namespace) -> int:
    suites = list_suites()
    if not suites:
        print("no eval suites found")
        return 1
    for playbook_id in suites:
        suite = load_suite(playbook_id)
        print(f"{playbook_id}: {len(suite.cases)} cases ({suite.path.relative_to(ROOT)})")
    return 0


def cmd_prepare(args: argparse.Namespace) -> int:
    suite = load_suite(args.playbook)
    locale = parse_locale(args.locale) if args.locale else None
    system_prompt = build_system_prompt(suite, locale)

    out_dir = Path(args.out_dir) if args.out_dir else DEFAULT_OUT_DIR / suite.playbook
    out_dir.mkdir(parents=True, exist_ok=True)
    bundle = out_dir / "bundle.txt"
    responses = out_dir / "responses.json"

    lines = [
        f"DeployerX eval bundle — {suite.playbook} (Path A, zero paid API)",
        "",
        "1. Paste everything between BEGIN/END SYSTEM PROMPT into a browser model",
        "   (Claude or ChatGPT) as its instructions / first message.",
        "2. Send each QUESTION below as its own message.",
        f"3. Copy each reply into {responses.relative_to(ROOT)} under the matching id.",
        f"4. Grade: python3 -m evals.run score {suite.playbook} --responses {responses.relative_to(ROOT)}",
        "",
        "----- BEGIN SYSTEM PROMPT -----",
        system_prompt.rstrip(),
        "----- END SYSTEM PROMPT -----",
        "",
    ]
    for i, case in enumerate(suite.cases, 1):
        lines.append(f"QUESTION {i} [{case.id}]: {case.message}")
    bundle.write_text("\n".join(lines) + "\n", encoding="utf-8")

    skeleton = {
        "playbook": suite.playbook,
        "locale": args.locale or None,
        "model": "browser (Path A)",
        "responses": {case.id: "" for case in suite.cases},
    }
    responses.write_text(
        json.dumps(skeleton, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(f"wrote {bundle.relative_to(ROOT)} ({len(suite.cases)} questions)")
    print(f"wrote {responses.relative_to(ROOT)} — fill in the replies, then run:")
    print(f"  python3 -m evals.run score {suite.playbook} --responses {responses.relative_to(ROOT)}")
    return 0


def cmd_score(args: argparse.Namespace) -> int:
    suite = load_suite(args.playbook)
    responses = _load_responses(Path(args.responses))
    results = score_suite(suite, responses)
    ok = print_scorecard(suite, results, label=f"responses: {args.responses}")
    return 0 if ok else 1


def _generate_via_api(suite: EvalSuite, system_prompt: str, model: str) -> dict[str, str]:
    try:
        import anthropic
    except ImportError:
        raise SystemExit(
            "api mode needs the Anthropic SDK: pip install anthropic\n"
            "(zero-cost alternative: `prepare` + a browser model + `score`)"
        )

    client = anthropic.Anthropic()
    # Opus 5 / Fable 5 classifiers can decline a request; the server-side
    # fallback beta re-runs those on Anthropic's recommended substitute.
    use_fallbacks = model in ("claude-opus-5", "claude-fable-5")
    system = [{"type": "text", "text": system_prompt, "cache_control": {"type": "ephemeral"}}]

    responses: dict[str, str] = {}
    for case in suite.cases:
        try:
            if use_fallbacks:
                message = client.beta.messages.create(
                    model=model,
                    max_tokens=16000,
                    betas=["server-side-fallback-2026-07-01"],
                    fallbacks="default",
                    system=system,
                    messages=[{"role": "user", "content": case.message}],
                )
            else:
                message = client.messages.create(
                    model=model,
                    max_tokens=16000,
                    system=system,
                    messages=[{"role": "user", "content": case.message}],
                )
        except anthropic.APIError as exc:
            print(f"  [{case.id}] API error: {exc}")
            responses[case.id] = ""
            continue

        if message.stop_reason == "refusal":
            print(f"  [{case.id}] request declined (stop_reason=refusal)")
            responses[case.id] = ""
            continue
        responses[case.id] = "".join(b.text for b in message.content if b.type == "text")
    return responses


def cmd_api(args: argparse.Namespace) -> int:
    suite = load_suite(args.playbook)
    locale = parse_locale(args.locale) if args.locale else None
    system_prompt = build_system_prompt(suite, locale)

    label = f"model: {args.model}" + (f", locale: {args.locale}" if args.locale else "")
    print(f"generating {len(suite.cases)} replies ({label}) ...")
    responses = _generate_via_api(suite, system_prompt, args.model)

    save_path = (
        Path(args.save) if args.save else DEFAULT_OUT_DIR / suite.playbook / "responses-api.json"
    )
    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.write_text(
        json.dumps(
            {
                "playbook": suite.playbook,
                "locale": args.locale or None,
                "model": args.model,
                "responses": responses,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"saved replies to {save_path.relative_to(ROOT)}\n")

    results = score_suite(suite, responses)
    ok = print_scorecard(suite, results, label=label)
    return 0 if ok else 1


def cmd_selftest(_: argparse.Namespace) -> int:
    """Grade bundled fixtures and assert the scorer reaches the expected verdicts."""
    suites = list_suites()
    if not suites:
        print("SELFTEST FAIL: no eval suites found")
        return 1

    failures: list[str] = []
    checked = 0
    for playbook_id in suites:
        suite = load_suite(playbook_id)

        prompt = build_system_prompt(suite, None)
        if suite.faq.strip().splitlines()[0] not in prompt:
            failures.append(f"{playbook_id}: FAQ not merged into system prompt")
        localized = build_system_prompt(suite, LocaleRef("in", "uttar-pradesh", "varanasi"))
        if "Local context" not in localized:
            failures.append(f"{playbook_id}: locale constraints not merged into system prompt")

        fixtures = sorted(suite.fixtures_dir.glob("*.json"))
        if not fixtures:
            failures.append(f"{playbook_id}: no fixtures under {suite.fixtures_dir.relative_to(ROOT)}")
            continue
        for fixture_path in fixtures:
            fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
            results = score_suite(suite, fixture["responses"])
            for case_id, expected in fixture["expected"].items():
                if case_id not in results:
                    failures.append(f"{fixture_path.name}: unknown case id '{case_id}'")
                    continue
                verdict = "pass" if all(r.passed for r in results[case_id]) else "fail"
                checked += 1
                if verdict != expected:
                    detail = "; ".join(
                        f"{r.name}: {r.detail}" for r in results[case_id] if not r.passed
                    )
                    failures.append(
                        f"{playbook_id}/{fixture_path.name}: {case_id} expected {expected}, "
                        f"got {verdict}" + (f" ({detail})" if detail else "")
                    )

    # MCP tool layer — the server wiring needs the optional `mcp` SDK, but the
    # tool implementations are stdlib and must stay importable and correct.
    from deployerx_mcp import tools as mcp_tools

    catalog = mcp_tools.playbook_catalog()
    for playbook_id in suites:
        if playbook_id not in catalog:
            failures.append(f"mcp: playbook_catalog missing {playbook_id}")
    if "varanasi" not in mcp_tools.locale_context("in", "uttar-pradesh", "varanasi"):
        failures.append("mcp: locale_context missing varanasi cascade")
    mcp_prompt = mcp_tools.system_prompt(
        suites[0], faq="MARKER-FAQ", country="in", l2="uttar-pradesh", l3="varanasi"
    )
    if "MARKER-FAQ" not in mcp_prompt or "Local context" not in mcp_prompt:
        failures.append("mcp: system_prompt assembly broken")
    for playbook_id in suites:
        suite = load_suite(playbook_id)
        compliant = suite.fixtures_dir / "compliant.json"
        if compliant.exists():
            fixture = json.loads(compliant.read_text(encoding="utf-8"))
            scorecard = mcp_tools.eval_responses(playbook_id, fixture["responses"])
            if f"{len(suite.cases)}/{len(suite.cases)} passed" not in scorecard:
                failures.append(f"mcp: eval_responses wrong verdict for {playbook_id}")

    if failures:
        print(f"SELFTEST FAIL: {len(failures)} problem(s)")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(
        f"OK: eval selftest — {checked} fixture verdicts verified across {len(suites)} suites; "
        "MCP tool layer OK"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python3 -m evals.run", description="Run DeployerX playbook evals."
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="list playbooks that have eval suites").set_defaults(fn=cmd_list)

    p = sub.add_parser("prepare", help="write a Path A paste bundle + responses skeleton")
    p.add_argument("playbook")
    p.add_argument("--locale", help="cc/l2-slug/l3-slug, e.g. in/rajasthan/jaipur")
    p.add_argument("--out-dir", help=f"output directory (default: {DEFAULT_OUT_DIR.name}/<playbook>/)")
    p.set_defaults(fn=cmd_prepare)

    p = sub.add_parser("score", help="grade a responses file")
    p.add_argument("playbook")
    p.add_argument("--responses", required=True, help="JSON file with case id -> reply")
    p.set_defaults(fn=cmd_score)

    p = sub.add_parser("api", help="generate replies via the Anthropic API, then grade")
    p.add_argument("playbook")
    p.add_argument("--locale", help="cc/l2-slug/l3-slug, e.g. in/rajasthan/jaipur")
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--save", help="where to save generated replies (JSON)")
    p.set_defaults(fn=cmd_api)

    sub.add_parser("selftest", help="grade bundled fixtures (no network)").set_defaults(
        fn=cmd_selftest
    )

    args = parser.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
