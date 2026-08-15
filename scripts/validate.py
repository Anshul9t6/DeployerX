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

    registry = ROOT / "playbooks/_registry.yaml"
    if not registry.exists():
        fail("missing playbooks/_registry.yaml")

    hierarchy = ROOT / "schema/hierarchy.md"
    if not hierarchy.exists():
        fail("missing schema/hierarchy.md")

    if (ROOT / "schema/architecture.md").exists():
        fail("schema/architecture.md was merged into hierarchy.md — delete it")

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
    if len(l3_readmes) < 1:
        fail("expected ≥1 India L3 pack")

    dead = ROOT / "locale-packs/in/playbooks"
    if dead.exists():
        fail("remove dead locale-packs/in/playbooks/ — playbooks stay global")

    boilerplate = "pick global playbook"
    for examples in (ROOT / "locale-packs/in/l2").glob("*/l3/*/examples.md"):
        text = examples.read_text().lower()
        # thin packs must not claim seeded in sibling README
        readme = examples.parent / "README.md"
        if readme.exists() and "status: seeded" in readme.read_text():
            if text.count(boilerplate) >= 2 and "banarasi" not in text and "pilgrimage" not in text:
                fail(
                    f"{examples.relative_to(ROOT)} looks template-thin but README is seeded — downgrade to draft"
                )

    # Import resolve smoke test
    sys.path.insert(0, str(ROOT))
    from decision.resolve import (
        LocaleRef,
        format_constraints_excerpt,
        merged_constraints,
        resolve,
    )

    r = resolve(LocaleRef("in", "uttar-pradesh", "varanasi"))
    if len(r.layers) < 4:
        fail(f"expected 4 cascade layers for Varanasi, got {len(r.layers)}")
    if not merged_constraints(LocaleRef("in", "uttar-pradesh", "varanasi")):
        fail("merged_constraints returned empty for Varanasi")

    jaipur = format_constraints_excerpt(LocaleRef("in", "rajasthan", "jaipur"))
    if "jaipur/constraints.md" not in jaipur:
        fail("constraint excerpt for Jaipur missing leaf path")
    if "monument" not in jaipur.lower() and "aarti" not in jaipur.lower():
        fail("Jaipur excerpt should surface tourism/timing deltas")

    # Site progress JSON must match repo (GitHub Pages source of truth)
    progress = ROOT / "docs/data/progress.json"
    if not progress.exists():
        fail("missing docs/data/progress.json — run python3 scripts/generate_site_data.py")

    for required_doc in ("STATUS.md", "ROADMAP.md"):
        path = ROOT / required_doc
        if not path.exists():
            fail(f"missing {required_doc}")
    status_text = (ROOT / "STATUS.md").read_text()
    if "<!-- status:metrics -->" not in status_text or "<!-- /status:metrics -->" not in status_text:
        fail("STATUS.md missing status:metrics markers")

    for required in (
        "docs/index.html",
        "docs/app.js",
        "docs/styles.css",
        "docs/favicon.svg",
        "docs/assets/og.jpg",
    ):
        if not (ROOT / required).exists():
            fail(f"missing {required}")

    import importlib.util
    import json

    gen_path = ROOT / "scripts/generate_site_data.py"
    spec = importlib.util.spec_from_file_location("generate_site_data", gen_path)
    if spec is None or spec.loader is None:
        fail("cannot load scripts/generate_site_data.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    expected = mod.build()
    actual = json.loads(progress.read_text())
    # Ignore generated_at timestamp drift for equality of payload shape
    exp = {k: v for k, v in expected.items() if k != "generated_at"}
    act = {k: v for k, v in actual.items() if k != "generated_at"}
    if exp != act:
        fail(
            "docs/data/progress.json is stale — run: python3 scripts/generate_site_data.py"
        )

    print("OK: DeployerX world hierarchy validated")
    print(f"ROOT={ROOT}")
    print(f"India L2 metas={len(l2_metas)} L3 packs={len(l3_readmes)}")
    print(f"resolve(in/uttar-pradesh/varanasi) layers={len(r.layers)}")
    print("OK: docs/data/progress.json in sync")


if __name__ == "__main__":
    main()
