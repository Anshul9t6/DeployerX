"""Resolve locale cascade: L0 _global → L1 country → L2 → L3."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCALE = ROOT / "locale-packs"


@dataclass
class LocaleRef:
    country: str
    l2: str | None = None
    l3: str | None = None


@dataclass
class ResolvedLocale:
    ref: LocaleRef
    layers: list[Path] = field(default_factory=list)
    constraints_files: list[Path] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)

    @property
    def id(self) -> str:
        parts = [self.ref.country]
        if self.ref.l2:
            parts.append(self.ref.l2)
        if self.ref.l3:
            parts.append(self.ref.l3)
        return "/".join(parts)


def _layer_paths(ref: LocaleRef) -> list[tuple[str, Path]]:
    layers: list[tuple[str, Path]] = [("L0", LOCALE / "_global")]
    country = LOCALE / ref.country
    layers.append(("L1", country))
    if ref.l2:
        layers.append(("L2", country / "l2" / ref.l2))
    if ref.l2 and ref.l3:
        layers.append(("L3", country / "l2" / ref.l2 / "l3" / ref.l3))
    return layers


def resolve(ref: LocaleRef) -> ResolvedLocale:
    out = ResolvedLocale(ref=ref)
    for label, path in _layer_paths(ref):
        if path.exists():
            out.layers.append(path)
            constraints = path / "constraints.md"
            if constraints.exists():
                out.constraints_files.append(constraints)
        else:
            out.missing.append(f"{label}:{path.relative_to(ROOT)}")
    return out


def merged_constraints(ref: LocaleRef) -> str:
    """Concatenate constraint files root→leaf. Later files override by appending."""
    r = resolve(ref)
    parts: list[str] = []
    for path in r.constraints_files:
        body = path.read_text().strip()
        if not body:
            continue
        rel = path.relative_to(ROOT)
        parts.append(f"<!-- {rel} -->\n{body}")
    return "\n\n".join(parts)


def format_constraints_excerpt(ref: LocaleRef, max_chars: int = 1600) -> str:
    """Leaf constraints.md — what a deployer actually added. Full stack via --merge."""
    r = resolve(ref)
    if not r.constraints_files:
        return "--- constraints excerpt ---\n(no constraints.md in this cascade)"

    leaf = r.constraints_files[-1]
    body = leaf.read_text().strip()
    if len(body) > max_chars:
        body = body[: max_chars - 1].rstrip() + "…"

    lines = [
        "--- constraints excerpt (leaf wins) ---",
        f"leaf: {leaf.relative_to(ROOT)}",
        "",
        body,
    ]
    if len(r.constraints_files) > 1:
        earlier = ", ".join(str(p.relative_to(ROOT)) for p in r.constraints_files[:-1])
        lines += [
            "",
            f"earlier layers ({len(r.constraints_files) - 1}): {earlier}",
            "full merge: python3 -m decision.resolve <cc> [l2] [l3] --merge",
        ]
    return "\n".join(lines)


def explain(ref: LocaleRef) -> str:
    r = resolve(ref)
    lines = [f"resolve {r.id}", "cascade:"]
    for p in r.layers:
        lines.append(f"  {p.relative_to(ROOT)}")
    if r.constraints_files:
        lines.append("constraints (root→leaf, concatenated):")
        for p in r.constraints_files:
            lines.append(f"  {p.relative_to(ROOT)}")
    if r.missing:
        lines.append("missing (fallback OK):")
        for m in r.missing:
            lines.append(f"  {m}")
    return "\n".join(lines)


if __name__ == "__main__":
    import sys

    flags = {"--merge", "--no-excerpt"}
    positionals = [a for a in sys.argv[1:] if a not in flags]
    country = positionals[0] if len(positionals) > 0 else "in"
    l2 = positionals[1] if len(positionals) > 1 else None
    l3 = positionals[2] if len(positionals) > 2 else None
    ref = LocaleRef(country=country, l2=l2, l3=l3)
    print(explain(ref))
    if "--no-excerpt" not in sys.argv:
        print()
        print(format_constraints_excerpt(ref))
    if "--merge" in sys.argv:
        print("\n--- merged constraints (root→leaf, local wins) ---\n")
        print(merged_constraints(ref))
