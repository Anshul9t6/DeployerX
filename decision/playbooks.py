"""Load playbook registry from playbooks/_registry.yaml (no PyYAML dependency)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "playbooks" / "_registry.yaml"


@dataclass(frozen=True)
class Playbook:
    id: str
    title: str
    path: str
    when: str
    use_cases: tuple[str, ...]
    channels: tuple[str, ...]


def _parse_list(raw: str) -> tuple[str, ...]:
    return tuple(re.findall(r"[\w-]+", raw))


@lru_cache(maxsize=1)
def load_playbooks() -> tuple[Playbook, ...]:
    if not REGISTRY.exists():
        return ()
    items: list[Playbook] = []
    current: dict[str, str] = {}

    def flush() -> None:
        nonlocal current
        if not current.get("id"):
            current = {}
            return
        items.append(
            Playbook(
                id=current["id"],
                title=current.get("title", current["id"]),
                path=current.get("path", f"playbooks/{current['id']}/"),
                when=current.get("when", ""),
                use_cases=_parse_list(current.get("use_cases", "")),
                channels=_parse_list(current.get("channels", "")),
            )
        )
        current = {}

    for line in REGISTRY.read_text().splitlines():
        if re.match(r"^\s+- id:", line):
            flush()
            current = {"id": line.split(":", 1)[1].strip()}
        elif current and re.match(r"^\s+(title|path|when|use_cases|channels):", line):
            key, val = line.split(":", 1)
            current[key.strip()] = val.strip()
    flush()
    return tuple(items)


def pick_playbook(use_case: str, channel: str) -> Playbook | None:
    for pb in load_playbooks():
        if use_case in pb.use_cases and channel in pb.channels:
            return pb
    return None
