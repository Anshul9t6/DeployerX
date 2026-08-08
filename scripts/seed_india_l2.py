#!/usr/bin/env python3
"""Seed missing India L2 _meta.yaml stubs from l2/_index.yaml (no third-party deps)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "locale-packs/in/l2/_index.yaml"
L2_ROOT = ROOT / "locale-packs/in/l2"


def parse_entries(text: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for line in text.splitlines():
        if re.match(r"^\s+- slug:", line):
            if current:
                entries.append(current)
            current = {"slug": line.split(":", 1)[1].strip()}
        elif current and re.match(r"^\s+(name|code|languages|l3_count):", line):
            key, val = line.split(":", 1)
            current[key.strip()] = val.strip()
    if current:
        entries.append(current)
    return entries


def render_meta(e: dict[str, str]) -> str:
    langs = e.get("languages", "[]")
    return f"""level: 2
country: in
l2: {e['slug']}
name: {e.get('name', e['slug'])}
code: {e.get('code', '')}
languages: {langs}
status: listed
maintainers: []

# {e.get('name', e['slug'])} (L2)

Status: **listed** — stub seeded from `l2/_index.yaml`.

## Help wanted

1. Upgrade `status` to `seeded` after adding regional notes
2. Add L3 packs under `l3/` using `locale-packs/_templates/l3/`
3. Target ~{e.get('l3_count', '?')} districts (approx; PRs welcome to correct)

## Priority playbooks (global)

- `whatsapp-shop-faq`
- `clinic-whatsapp-faq`
"""


def main() -> None:
    entries = parse_entries(INDEX.read_text())
    created = 0
    skipped = 0
    for e in entries:
        path = L2_ROOT / e["slug"] / "_meta.yaml"
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            skipped += 1
            continue
        path.write_text(render_meta(e))
        created += 1
    print(f"OK: L2 entries={len(entries)} created={created} skipped_existing={skipped}")


if __name__ == "__main__":
    main()
