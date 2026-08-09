"""Load machine-checkable eval suites from playbooks/<id>/evals/cases.json."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAYBOOKS = ROOT / "playbooks"


@dataclass(frozen=True)
class EvalCase:
    id: str
    message: str
    expect: dict
    note: str = ""


@dataclass(frozen=True)
class EvalSuite:
    playbook: str
    path: Path
    prompt_path: Path
    faq: str
    escalation_markers: list[str] = field(default_factory=list)
    cases: list[EvalCase] = field(default_factory=list)

    @property
    def fixtures_dir(self) -> Path:
        return self.path.parent / "fixtures"


def list_suites() -> list[str]:
    return sorted(p.parent.parent.name for p in PLAYBOOKS.glob("*/evals/cases.json"))


def load_suite(playbook_id: str) -> EvalSuite:
    path = PLAYBOOKS / playbook_id / "evals" / "cases.json"
    if not path.exists():
        known = ", ".join(list_suites()) or "(none)"
        raise SystemExit(f"no eval suite at {path.relative_to(ROOT)} — known suites: {known}")

    data = json.loads(path.read_text(encoding="utf-8"))
    for key in ("playbook", "prompt", "faq", "cases"):
        if key not in data:
            raise SystemExit(f"{path.relative_to(ROOT)}: missing required key '{key}'")
    if data["playbook"] != playbook_id:
        raise SystemExit(f"{path.relative_to(ROOT)}: playbook id mismatch ({data['playbook']})")

    prompt_path = PLAYBOOKS / playbook_id / data["prompt"]
    if not prompt_path.exists():
        raise SystemExit(f"{path.relative_to(ROOT)}: prompt file not found: {data['prompt']}")

    cases: list[EvalCase] = []
    seen: set[str] = set()
    for raw in data["cases"]:
        case = EvalCase(
            id=raw["id"],
            message=raw["message"],
            expect=raw.get("expect", {}),
            note=raw.get("note", ""),
        )
        if case.id in seen:
            raise SystemExit(f"{path.relative_to(ROOT)}: duplicate case id '{case.id}'")
        seen.add(case.id)
        cases.append(case)
    if not cases:
        raise SystemExit(f"{path.relative_to(ROOT)}: no cases defined")

    return EvalSuite(
        playbook=playbook_id,
        path=path,
        prompt_path=prompt_path,
        faq=data["faq"],
        escalation_markers=data.get("escalation_markers", []),
        cases=cases,
    )
