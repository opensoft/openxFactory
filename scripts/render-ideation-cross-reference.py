#!/usr/bin/env python3
"""Render the ideation cross-reference index projection (add-ideation-cross-reference-readiness).

Change task 2.4: `ideation/cross-reference.yaml` is the SOURCE OF TRUTH (C2);
`ideation/cross-reference.md` is a GENERATED human projection over it — never
hand-edited (the notebook-projection / doc-health-report precedent). This is the
small single-purpose renderer that projects the YAML to Markdown deterministically:
the same YAML always yields byte-identical Markdown, so the projection can be
regenerated and diffed. Later worker waves (codexFactory scorer, task 3.x) reuse
this renderer after they rewrite the YAML with real scores.

Usage:
    python3 scripts/render-ideation-cross-reference.py [IN.yaml] [OUT.md]
    # defaults: ideation/cross-reference.yaml -> ideation/cross-reference.md
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR PyYAML is required", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_IN = ROOT / "ideation" / "cross-reference.yaml"
DEFAULT_OUT = ROOT / "ideation" / "cross-reference.md"

TIER_NAMES = ("domain", "company", "project")


def _fit_line(fit: dict) -> str:
    if not isinstance(fit, dict):
        return "extension fit: (missing)"
    if fit.get("has_promoted_fit"):
        spec = fit.get("promoted_spec", "?")
        how = fit.get("how_extends", "")
        tail = f" — {how}" if how else ""
        return f"extends promoted `{spec}`{tail}"
    statement = fit.get("statement", "")
    return f"no promoted fit — {statement}" if statement else "no promoted fit"


def _readiness_line(readiness: Any) -> str:
    if not isinstance(readiness, dict):
        return "readiness: not scored"
    by_tier = {t.get("tier"): t for t in readiness.get("tiers") or [] if isinstance(t, dict)}
    parts = []
    for name in TIER_NAMES:
        t = by_tier.get(name)
        if not isinstance(t, dict):
            parts.append(f"{name} —")
        elif isinstance(t.get("score"), int):
            parts.append(f"{name} {t['score']}")
        else:
            reason = t.get("unscored_reason", "unscored")
            parts.append(f"{name} unscored ({reason})")
    return "readiness: " + "; ".join(parts)


def _recommendation_line(readiness: Any) -> str | None:
    if not isinstance(readiness, dict):
        return None
    rec = readiness.get("recommendation")
    if not isinstance(rec, dict) or "flagged" not in rec:
        return None
    verb = "FLAGGED propose-for-authorization" if rec.get("flagged") else "not flagged"
    disp = rec.get("disposition", "pending_review")
    summary = rec.get("summary")
    tail = f" — {summary}" if summary else ""
    return f"recommendation: {verb} ({disp}){tail}"


def render_markdown(index: dict) -> str:
    gen = index.get("generation") or {}
    entries = index.get("topic_entries") or []
    lines: list[str] = []
    lines.append("# Ideation Cross-Reference Readiness Index")
    lines.append("")
    # NOT `record`: this file is rewritten in place from the YAML on every
    # run, so it has no captured state to be immutable against, and canon
    # already says so — `ideation-cross-reference` names "the cross-reference
    # index and its rendered twin" as generated artifacts that are NOT records
    # (declare-generated-projection-status, 2026-08-28).
    lines.append("Status: projection")
    lines.append("Kind: report")
    lines.append("Repository context: openxFactory")
    lines.append("")
    lines.append(
        "**GENERATED FILE — do not edit by hand.** This is a deterministic Markdown "
        "projection of the source-of-truth `ideation/cross-reference.yaml`, produced by "
        "`scripts/render-ideation-cross-reference.py`. Edit the YAML and re-render; per the "
        "`add-ideation-cross-reference-readiness` spec the index is a generated projection over "
        "governed documents. See `ideation/README.md` for how this surface relates to the promoted "
        "requirements and to `staging/INDEX.md`."
    )
    lines.append("")
    lines.append(f"- Source revision: `{gen.get('source_revision', '?')}`")
    if gen.get("generated_at"):
        lines.append(f"- Generated at: {gen['generated_at']}")
    if gen.get("generator_version"):
        lines.append(f"- Generator: `{gen['generator_version']}`")
    lines.append(f"- Topic clusters: {len(entries)}")
    if "possibles_register" not in index:
        lines.append(
            "- Possibles register: absent (consolidated via the ideation-dashboard flows in a "
            "later wave; when present its entries are validated by "
            "`validate-ideation-dashboard-contracts.py`)."
        )
    lines.append("")

    for entry in entries:
        if not isinstance(entry, dict):
            continue
        eid = entry.get("id", "?")
        name = entry.get("name") or eid
        lines.append(f"## {name}")
        lines.append("")
        lines.append(f"- id: `{eid}`")
        lines.append(f"- topics: {', '.join(entry.get('topics') or [])}")
        lines.append(f"- tag sources: {', '.join(entry.get('tag_sources') or [])}")
        if entry.get("origin"):
            lines.append(f"- origin: {entry['origin']}")
        lines.append(f"- {_fit_line(entry.get('extension_fit'))}")
        lines.append(f"- {_readiness_line(entry.get('readiness'))}")
        rec_line = _recommendation_line(entry.get("readiness"))
        if rec_line:
            lines.append(f"- {rec_line}")
        for c in entry.get("conflict_flags") or []:
            if isinstance(c, dict):
                lines.append(
                    f"- conflict: {c.get('kind', '?')} spread={c.get('spread', '?')} "
                    f"{c.get('detail', '')}".rstrip()
                )
        lines.append("")
        lines.append("| Member | Stage | Matched tags |")
        lines.append("| --- | --- | --- |")
        for m in entry.get("members") or []:
            if not isinstance(m, dict):
                continue
            path = m.get("path", "?")
            repo = m.get("repository")
            path_cell = f"{repo}:{path}" if repo else path
            stage = m.get("stage", "?")
            tags = ", ".join(m.get("matched_tags") or [])
            lines.append(f"| `{path_cell}` | {stage} | {tags} |")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str]) -> int:
    in_path = Path(argv[1]).resolve() if len(argv) > 1 else DEFAULT_IN
    out_path = Path(argv[2]).resolve() if len(argv) > 2 else DEFAULT_OUT
    if not in_path.is_file():
        print(f"ERROR input not found: {in_path}", file=sys.stderr)
        return 2
    with in_path.open(encoding="utf-8") as fh:
        index = yaml.safe_load(fh)
    if not isinstance(index, dict):
        print(f"ERROR {in_path} is not a mapping", file=sys.stderr)
        return 2
    out_path.write_text(render_markdown(index), encoding="utf-8")
    print(f"rendered {out_path} from {in_path} ({len(index.get('topic_entries') or [])} clusters)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
