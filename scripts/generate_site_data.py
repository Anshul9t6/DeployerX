#!/usr/bin/env python3
"""Generate docs/data/progress.json from the repo (source of truth for GitHub Pages)."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCALE = ROOT / "locale-packs"
OUT = ROOT / "docs" / "data" / "progress.json"
REPO = "https://github.com/Anshul9t6/DeployerX"
SITE = "https://anshul9t6.github.io/DeployerX/"


def _meta_field(text: str, key: str) -> str | None:
    m = re.search(rf"^{re.escape(key)}:\s*(.+)$", text, flags=re.M)
    return m.group(1).strip() if m else None


def _count_slugs(index: Path) -> int:
    if not index.exists():
        return 0
    return len(re.findall(r"^\s+- slug:", index.read_text(), flags=re.M))


def _bold_field(text: str, label: str) -> str | None:
    m = re.search(rf"\*\*{re.escape(label)}:\*\*\s*(.+)", text)
    return m.group(1).strip() if m else None


def _playbooks() -> list[dict]:
    items = []
    root = ROOT / "playbooks"
    for p in sorted(root.iterdir()):
        if not p.is_dir() or p.name.startswith("_"):
            continue
        readme = p / "README.md"
        title = p.name
        blurb = ""
        status = "unknown"
        time_to_win = ""
        audience = ""
        min_budget = "0"
        channels: list[str] = []
        if readme.exists():
            text = readme.read_text()
            status = (_meta_field(text, "status") or status).replace('"', "")
            min_budget = (_meta_field(text, "min_budget_inr") or "0").replace('"', "")
            ch = _meta_field(text, "channels") or "[]"
            channels = [c.strip() for c in re.findall(r"[\w-]+", ch)]
            aud = _meta_field(text, "audience") or "[]"
            audience = ", ".join(re.findall(r"[\w-]+", aud))
            for line in text.splitlines():
                if line.startswith("# "):
                    title = line[2:].strip()
                    break
            time_to_win = _bold_field(text, "Time to first win") or "~30 minutes"
            parts = text.split("\n\n")
            for part in parts:
                clean = part.strip()
                if clean.startswith("#") or clean.startswith("---") or clean.startswith("|"):
                    continue
                if clean.startswith("**"):
                    continue
                if clean and not clean.startswith("id:"):
                    blurb = clean.split("\n")[0].strip()
                    break
        budget_label = "₹0" if str(min_budget) in {"0", "0.0"} else f"from ₹{min_budget}"
        items.append(
            {
                "id": p.name,
                "title": title,
                "blurb": blurb,
                "status": status,
                "time_to_first_win": time_to_win,
                "audience": audience,
                "min_budget_inr": int(re.sub(r"[^\d]", "", str(min_budget)) or 0),
                "budget_label": budget_label,
                "channels": channels,
                "path": f"playbooks/{p.name}/",
                "url": f"{REPO}/tree/main/playbooks/{p.name}",
                "prompt_hi": f"{REPO}/blob/main/playbooks/{p.name}/prompts/system.hi.md",
                "prompt_en": f"{REPO}/blob/main/playbooks/{p.name}/prompts/system.en.md",
                "deploy_url": f"{REPO}/blob/main/playbooks/{p.name}/deploy.md",
            }
        )
    return items


def _countries() -> list[dict]:
    registry = LOCALE / "_registry.yaml"
    countries: list[dict] = []
    if not registry.exists():
        return countries
    current: dict | None = None
    in_countries = False
    for line in registry.read_text().splitlines():
        if line.strip() == "countries:":
            in_countries = True
            continue
        if in_countries and line.startswith("pipeline:"):
            if current:
                countries.append(current)
            break
        if not in_countries:
            continue
        if re.match(r"^\s+- code:", line):
            if current:
                countries.append(current)
            current = {"code": line.split(":", 1)[1].strip()}
        elif current and re.match(r"^\s+(name|path|status|priority|notes):", line):
            key, val = line.split(":", 1)
            current[key.strip()] = val.strip().strip('"')
        elif current and "admin_labels:" in line:
            current["admin_labels_raw"] = line.split(":", 1)[1].strip()
    if current and current not in countries:
        countries.append(current)

    for c in countries:
        code = c["code"]
        c["url"] = f"{REPO}/tree/main/locale-packs/{code}"
        l2_index = LOCALE / code / "l2" / "_index.yaml"
        l2_metas = list((LOCALE / code / "l2").glob("*/_meta.yaml")) if (LOCALE / code / "l2").exists() else []
        l3 = list((LOCALE / code / "l2").glob("*/l3/*/README.md")) if (LOCALE / code / "l2").exists() else []
        c["l2_index_count"] = _count_slugs(l2_index)
        c["l2_meta_count"] = len(l2_metas)
        c["l3_count"] = len(l3)
    return countries


def _india() -> dict:
    l2_root = LOCALE / "in" / "l2"
    l2_dirs = (
        sorted(p for p in l2_root.iterdir() if p.is_dir() and (p / "_meta.yaml").exists())
        if l2_root.exists()
        else []
    )
    l2_items = []
    l3_items = []
    seeded_l2 = 0
    for d in l2_dirs:
        text = (d / "_meta.yaml").read_text()
        status = (_meta_field(text, "status") or "listed").replace('"', "")
        name = (_meta_field(text, "name") or d.name).replace('"', "")
        if status != "listed":
            seeded_l2 += 1
        l3_dirs = sorted((d / "l3").glob("*/README.md")) if (d / "l3").exists() else []
        mtime = max(
            [d.stat().st_mtime] + [r.stat().st_mtime for r in l3_dirs],
            default=d.stat().st_mtime,
        )
        l2_items.append(
            {
                "slug": d.name,
                "name": name,
                "status": status,
                "l3_count": len(l3_dirs),
                "url": f"{REPO}/tree/main/locale-packs/in/l2/{d.name}",
                "mtime": mtime,
            }
        )
        for readme in l3_dirs:
            rtext = readme.read_text()
            l3_status = (_meta_field(rtext, "status") or "draft").replace('"', "")
            title = readme.parent.name
            for line in rtext.splitlines():
                if line.startswith("# "):
                    title = line[2:].strip().replace(" (L3)", "")
                    break
            langs = _meta_field(rtext, "languages") or "[]"
            blurb = ""
            for part in rtext.split("\n\n"):
                clean = part.strip()
                if clean.startswith("#") or clean.startswith("---"):
                    continue
                if clean.startswith("##"):
                    continue
                blurb = clean.split("\n")[0][:160]
                break
            l3_items.append(
                {
                    "l2": d.name,
                    "l2_name": name,
                    "slug": readme.parent.name,
                    "name": title,
                    "status": l3_status,
                    "languages": langs,
                    "blurb": blurb,
                    "url": f"{REPO}/tree/main/locale-packs/in/l2/{d.name}/l3/{readme.parent.name}",
                    "mtime": readme.stat().st_mtime,
                }
            )

    glossaries_all = (
        sorted((LOCALE / "in" / "glossary").glob("*.yaml"))
        if (LOCALE / "in" / "glossary").exists()
        else []
    )
    glossaries_seeded = []
    glossaries_stub = []
    for g in glossaries_all:
        text = g.read_text()
        if "status: stub" in text:
            glossaries_stub.append(g.stem)
        else:
            glossaries_seeded.append(g.stem)
    recent = sorted(l3_items, key=lambda x: x["mtime"], reverse=True)[:5]
    l3_seeded = sum(1 for i in l3_items if i["status"] == "seeded")
    l3_draft = sum(1 for i in l3_items if i["status"] == "draft")

    return {
        "l2_index_count": _count_slugs(l2_root / "_index.yaml") if l2_root.exists() else 0,
        "l2_meta_count": len(l2_dirs),
        "l2_seeded_count": seeded_l2,
        "l3_count": len(l3_items),
        "l3_seeded_count": l3_seeded,
        "l3_draft_count": l3_draft,
        "l3_goal": 780,
        "glossaries": glossaries_seeded,
        "glossaries_stub": glossaries_stub,
        "l2": sorted(l2_items, key=lambda x: (-x["l3_count"], x["name"])),
        "l3": sorted(l3_items, key=lambda x: (x["l2"], x["slug"])),
        "recent_l3": [
            {k: v for k, v in item.items() if k != "mtime"}
            for item in recent
        ],
    }


def _is_real_field_note(path: Path) -> bool:
    name = path.name.lower()
    if name.startswith("_") or name in {"first_deployment.md", "readme.md"}:
        return False
    if "template" in name:
        return False
    text = path.read_text()
    if "First deployment checklist" in text or "Copy to `field-notes/" in text:
        return False
    # Real notes must include Results with at least one non-empty value line
    if "## Results" not in text:
        return False
    block = text.split("## Results", 1)[1].split("\n## ", 1)[0]
    for ln in block.splitlines():
        if ":" in ln and not ln.strip().endswith(":"):
            val = ln.split(":", 1)[1].strip()
            if val and val not in {"…", "...", "(fill)", "TBD"}:
                return True
    return False

def _field_notes() -> list[dict]:
    notes = []
    root = ROOT / "field-notes"
    if not root.exists():
        return notes
    for p in sorted(root.glob("*.md"), reverse=True):
        if not _is_real_field_note(p):
            continue
        text = p.read_text()
        title = p.stem
        for line in text.splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
                break
        locale = ""
        playbook = ""
        m = re.search(r"\*\*Locale id:\*\*\s*`?([^`\n]+)`?", text)
        if m:
            locale = m.group(1).strip()
        m = re.search(r"\*\*Playbook[^:]*:\*\*\s*`?([^`\n]+)`?", text)
        if m:
            playbook = m.group(1).strip()
        excerpt = ""
        if "## Constraints" in text:
            block = text.split("## Constraints", 1)[1].split("##", 1)[0]
            bullets = [ln.strip("- ").strip() for ln in block.splitlines() if ln.strip().startswith("-")]
            excerpt = bullets[0] if bullets else ""
        notes.append(
            {
                "id": p.stem,
                "title": title,
                "locale": locale,
                "playbook": playbook,
                "excerpt": excerpt,
                "url": f"{REPO}/blob/main/field-notes/{p.name}",
                "featured": False,
            }
        )
    if notes:
        notes[0]["featured"] = True
    return notes


def build() -> dict:
    playbooks = _playbooks()
    countries = _countries()
    india = _india()
    # strip mtimes from l2/l3 public payload
    india_public = {
        **india,
        "l2": [{k: v for k, v in i.items() if k != "mtime"} for i in india["l2"]],
        "l3": [{k: v for k, v in i.items() if k != "mtime"} for i in india["l3"]],
    }
    notes = _field_notes()
    return {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "repo": REPO,
        "site": SITE,
        "copy": {
            "en": {
                "mission": "Locale-aware playbooks for deploying AI with non-engineer operators.",
                "lede": "Global recipes. Local deltas. India as the reference implementation — same tree for every country.",
                "promise": "Path A: ~30 minutes, browser model, human approval. No paid API required.",
            },
            "hi": {
                "mission": "बिना इंजीनियर वाले ऑपरेटर्स के लिए लोकल-भाषा AI डिप्लॉयमेंट किट।",
                "lede": "ग्लोबल प्लेबुक्स। लोकल डेल्टा। भारत रेफ़रेंस — हर देश के लिए वही ढाँचा।",
                "promise": "Path A: ~30 मिनट, ब्राउज़र मॉडल, आपकी जाँच। पेड API ज़रूरी नहीं।",
            },
        },
        "mission": "Locale-aware playbooks for deploying AI with non-engineer operators.",
        "stats": {
            "countries": len(countries),
            "playbooks": len(playbooks),
            "india_l2": india["l2_meta_count"],
            "india_l2_seeded": india["l2_seeded_count"],
            "india_l3": india["l3_count"],
            "india_l3_seeded": india["l3_seeded_count"],
            "india_l3_draft": india["l3_draft_count"],
            "glossaries": len(india["glossaries"]),
            "glossaries_stub": len(india["glossaries_stub"]),
            "field_notes": len(notes),
        },
        "playbooks": playbooks,
        "countries": countries,
        "india": india_public,
        "field_notes": notes,
        "path_a": {
            "steps": [
                {"id": "use_case", "title": "Pick a use case", "hint": "Shop FAQ or clinic FAQ"},
                {"id": "language", "title": "Pick language", "hint": "Hindi / English prompts included"},
                {"id": "playbook", "title": "Open the playbook", "hint": "Follow Path A in deploy.md"},
                {"id": "prompt", "title": "Copy the system prompt", "hint": "Paste FAQ · approve before send"},
            ]
        },
        "links": {
            "contribute": f"{REPO}/blob/main/CONTRIBUTING.md",
            "hierarchy": f"{REPO}/blob/main/schema/hierarchy.md",
            "claim_l3": f"{REPO}/issues/new?template=l3_pack.yml",
            "open_country": f"{REPO}/issues/new?template=country_pack.yml",
        },
    }


def main() -> None:
    data = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {OUT.relative_to(ROOT)}")
    print(
        f"stats: countries={data['stats']['countries']} playbooks={data['stats']['playbooks']} "
        f"india_l3={data['stats']['india_l3']}"
    )


if __name__ == "__main__":
    main()
