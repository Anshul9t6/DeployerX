#!/usr/bin/env python3
"""Refresh STATUS.md metrics block from docs/data/progress.json and print a session brief."""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "STATUS.md"
PROGRESS = ROOT / "docs" / "data" / "progress.json"
ROADMAP = ROOT / "ROADMAP.md"


def _progress() -> dict:
    if not PROGRESS.exists():
        return {}
    return json.loads(PROGRESS.read_text())


def _metrics_block(data: dict) -> str:
    s = data.get("stats", {})
    lines = [
        "```",
        f"generated_at:     {data.get('generated_at', 'n/a')}",
        f"countries:        {s.get('countries', 0)}",
        f"playbooks:        {s.get('playbooks', 0)}",
        f"india_l2_seeded:  {s.get('india_l2_seeded', 0)} / index {s.get('india_l2', 0)}",
        f"india_l3_seeded:  {s.get('india_l3_seeded', 0)}",
        f"india_l3_draft:   {s.get('india_l3_draft', 0)}",
        f"glossaries:       {s.get('glossaries', 0)} seeded · {s.get('glossaries_stub', 0)} stub",
        f"field_notes:      {s.get('field_notes', 0)}  ← must be >0 before Phase 1 complete",
        "```",
    ]
    return "\n".join(lines)


def _roadmap_open() -> list[str]:
    if not ROADMAP.exists():
        return []
    open_items: list[str] = []
    phase = ""
    for line in ROADMAP.read_text().splitlines():
        if line.startswith("## Phase"):
            phase = line.removeprefix("## ").strip()
        if line.startswith("- [ ]"):
            open_items.append(f"{phase}: {line[6:].strip()}")
    return open_items[:8]


def refresh_status_file(data: dict) -> None:
    text = STATUS.read_text()
    metrics = _metrics_block(data)
    text, n = re.subn(
        r"<!-- status:metrics -->.*?<!-- /status:metrics -->",
        f"<!-- status:metrics -->\n{metrics}\n<!-- /status:metrics -->",
        text,
        count=1,
        flags=re.S,
    )
    if n != 1:
        raise SystemExit("STATUS.md missing <!-- status:metrics --> markers")

    # bump Updated date in meta block
    text = re.sub(
        r"(\*\*Updated:\*\* )(\d{4}-\d{2}-\d{2})",
        rf"\g<1>{date.today().isoformat()}",
        text,
        count=1,
    )
    STATUS.write_text(text)


def brief(data: dict) -> str:
    s = data.get("stats", {})
    open_items = _roadmap_open()
    lines = [
        "=== DeployerX session brief ===",
        f"field_notes={s.get('field_notes', 0)}  l3_seeded={s.get('india_l3_seeded', 0)}  l3_draft={s.get('india_l3_draft', 0)}",
        f"phase critical path: real Path A field note" if s.get("field_notes", 0) == 0 else "phase: continue ROADMAP Phase 1/2",
        "",
        "Next open roadmap items:",
    ]
    for item in open_items:
        lines.append(f"  - {item}")
    lines += ["", "Files: STATUS.md · ROADMAP.md", "Commands: make status | make site | make check"]
    return "\n".join(lines)


def main() -> None:
    # Ensure progress.json exists / fresh enough for metrics
    gen = ROOT / "scripts" / "generate_site_data.py"
    if gen.exists():
        import subprocess

        subprocess.run(["python3", str(gen)], check=True, cwd=ROOT)
    data = _progress()
    refresh_status_file(data)
    print(brief(data))
    print(f"\nUpdated metrics in {STATUS.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
