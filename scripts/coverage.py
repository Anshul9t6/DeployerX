#!/usr/bin/env python3
"""Report locale coverage for DeployerX (world + India detail)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCALE = ROOT / "locale-packs"


def count_slugs(index: Path) -> int:
    if not index.exists():
        return 0
    return len(re.findall(r"^\s+- slug:", index.read_text(), flags=re.M))


def india_report() -> None:
    l2_root = LOCALE / "in" / "l2"
    index_count = count_slugs(l2_root / "_index.yaml")
    l2_dirs = sorted(
        p for p in l2_root.iterdir() if p.is_dir() and (p / "_meta.yaml").exists()
    )
    l3_packs = list(l2_root.glob("*/l3/*/README.md"))
    seeded_l2 = 0
    for d in l2_dirs:
        text = (d / "_meta.yaml").read_text()
        if "status: listed" not in text:
            seeded_l2 += 1

    print("## India (in)")
    print(f"- L2 in index: {index_count}")
    print(f"- L2 with _meta.yaml: {len(l2_dirs)}")
    print(f"- L2 beyond listed stub: {seeded_l2}")
    print(f"- L3 packs (README): {len(l3_packs)}")
    print("- L3 seeded:")
    for p in sorted(l3_packs):
        rel = p.parent.relative_to(LOCALE / "in" / "l2")
        # rel like uttar-pradesh/l3/varanasi
        parts = rel.parts
        print(f"  - {parts[0]}/{parts[-1]}")


def world_report() -> None:
    registry = LOCALE / "_registry.yaml"
    countries = []
    if registry.exists():
        for line in registry.read_text().splitlines():
            if line.strip().startswith("- code:"):
                countries.append(line.split(":", 1)[1].strip())
    playbooks = sorted(p.name for p in (ROOT / "playbooks").iterdir() if p.is_dir() and not p.name.startswith("_"))
    print("## World")
    print(f"- Countries registered: {len(countries)} → {', '.join(countries) or '—'}")
    print(f"- Global pack: {'yes' if (LOCALE / '_global').exists() else 'no'}")
    print(f"- Playbooks: {len(playbooks)} → {', '.join(playbooks)}")


def main() -> None:
    print("# DeployerX coverage report\n")
    world_report()
    print()
    india_report()


if __name__ == "__main__":
    main()
