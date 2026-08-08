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
    """Return existing cascade layers and constraint files (root → leaf)."""
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


def explain(ref: LocaleRef) -> str:
    r = resolve(ref)
    lines = [
        f"## Locale resolve: `{r.id}`",
        "",
        "Cascade (root → leaf; local wins):",
    ]
    for p in r.layers:
        lines.append(f"- `{p.relative_to(ROOT)}`")
    if r.constraints_files:
        lines.append("")
        lines.append("Constraints merged from:")
        for p in r.constraints_files:
            lines.append(f"- `{p.relative_to(ROOT)}`")
    if r.missing:
        lines.append("")
        lines.append("Missing (fallback upward is OK):")
        for m in r.missing:
            lines.append(f"- {m}")
    lines.append("")
    lines.append("Playbooks stay global under `playbooks/` — locales only overlay context.")
    return "\n".join(lines)


if __name__ == "__main__":
    import sys

    country = sys.argv[1] if len(sys.argv) > 1 else "in"
    l2 = sys.argv[2] if len(sys.argv) > 2 else None
    l3 = sys.argv[3] if len(sys.argv) > 3 else None
    print(explain(LocaleRef(country=country, l2=l2, l3=l3)))
