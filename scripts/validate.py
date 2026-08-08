#!/usr/bin/env python3
"""Validate DeployerX world hierarchy (lightweight, no deps)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    raise SystemExit(1)


def main() -> None:
    registry = ROOT / "locale-packs/_registry.yaml"
    if not registry.exists():
        fail("missing locale-packs/_registry.yaml")

    global_constraints = ROOT / "locale-packs/_global/constraints.md"
    if not global_constraints.exists():
        fail("missing L0 global constraints")

    hierarchy = ROOT / "schema/hierarchy.md"
    if not hierarchy.exists():
        fail("missing schema/hierarchy.md")

    india_meta = ROOT / "locale-packs/in/_meta.yaml"
    if not india_meta.exists():
        fail("missing India L1 _meta.yaml")

    l2_index = ROOT / "locale-packs/in/l2/_index.yaml"
    if not l2_index.exists():
        fail("missing India L2 index")

    l3 = ROOT / "locale-packs/in/l2/uttar-pradesh/l3/varanasi"
    for name in ("README.md", "constraints.md", "examples.md"):
        if not (l3 / name).exists():
            fail(f"L3 varanasi missing {name}")

    for playbook_id in ("whatsapp-shop-faq", "clinic-whatsapp-faq"):
        playbook = ROOT / "playbooks" / playbook_id
        for name in ("README.md", "decide.md", "deploy.md", "cost.md"):
            if not (playbook / name).exists():
                fail(f"playbook {playbook_id} missing {name}")

    template = ROOT / "locale-packs/_templates/l3/README.md"
    if not template.exists():
        fail("missing world L3 template")

    l2_metas = list((ROOT / "locale-packs/in/l2").glob("*/_meta.yaml"))
    if len(l2_metas) < 36:
        fail(f"expected ≥36 India L2 metas, got {len(l2_metas)}")

    l3_readmes = list((ROOT / "locale-packs/in/l2").glob("*/l3/*/README.md"))
    if len(l3_readmes) < 11:
        fail(f"expected ≥11 L3 packs, got {len(l3_readmes)}")

    # Import resolve smoke test
    sys.path.insert(0, str(ROOT))
    from decision.resolve import LocaleRef, resolve

    r = resolve(LocaleRef("in", "uttar-pradesh", "varanasi"))
    if len(r.layers) < 4:
        fail(f"expected 4 cascade layers for Varanasi, got {len(r.layers)}")

    print("OK: DeployerX world hierarchy validated")
    print(f"ROOT={ROOT}")
    print(f"India L2 metas={len(l2_metas)} L3 packs={len(l3_readmes)}")
    print(f"resolve(in/uttar-pradesh/varanasi) layers={len(r.layers)}")


if __name__ == "__main__":
    main()
