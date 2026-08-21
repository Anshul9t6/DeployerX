"""Load machine-checkable eval suites from playbooks/<id>/evals/cases*.json."""

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
    fixtures_dir: Path
    escalation_markers: list[str] = field(default_factory=list)
    cases: list[EvalCase] = field(default_factory=list)

    @property
    def label(self) -> str:
        return f"{self.playbook}/{self.path.name}"


def fixtures_dir_for(cases_path: Path) -> Path:
    """cases.json → fixtures/; cases-pt.json → fixtures-pt/."""
    stem = cases_path.stem
    if stem == "cases":
        return cases_path.parent / "fixtures"
    suffix = stem.removeprefix("cases-")
    return cases_path.parent / f"fixtures-{suffix}"


def list_suite_paths() -> list[Path]:
    return sorted(PLAYBOOKS.glob("*/evals/cases*.json"))


def list_suites() -> list[str]:
    return sorted({p.parent.parent.name for p in PLAYBOOKS.glob("*/evals/cases.json")})


def load_suite_file(path: Path) -> EvalSuite:
    if not path.exists():
        raise SystemExit(f"no eval suite at {path}")

    playbook_id = path.parent.parent.name
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
        fixtures_dir=fixtures_dir_for(path),
        escalation_markers=data.get("escalation_markers", []),
        cases=cases,
    )


def load_suite(playbook_id: str, cases_file: str = "cases.json") -> EvalSuite:
    path = PLAYBOOKS / playbook_id / "evals" / cases_file
    if not path.exists():
        known = ", ".join(list_suites()) or "(none)"
        raise SystemExit(f"no eval suite at {path.relative_to(ROOT)} — known suites: {known}")
    return load_suite_file(path)
