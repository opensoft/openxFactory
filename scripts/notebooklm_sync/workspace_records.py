from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .models import IDEATION_TITLE_PREFIX, BookSpec


def _is_record_id_line(line: str, record_id: str) -> bool:
    stripped = line.strip()
    if stripped.startswith("#"):
        return False
    return stripped == f"id: {record_id}"


def _record_item_span(lines: list[str], idx: int) -> tuple[int, int]:
    start = idx
    while start > 0 and (not lines[start].lstrip().startswith("- ")):
        start -= 1
    end = idx + 1
    while end < len(lines):
        line = lines[end]
        if line.lstrip().startswith("- "):
            break
        if line.strip() and (not line[0].isspace()) and (not line.startswith("#")):
            break
        end += 1
    return (start, end)


def ensure_workspace_record(
    root: Path, spec: BookSpec, notebook_id: str, apply: bool
) -> None:
    path = root / "openxFactory/examples/lifecycle-notebook-workspaces.yaml"
    record_id = f"workspace-xfactory-lifecycle-{spec.key}"
    if not path.is_file():
        print(
            f"[{spec.key}] NOTICE workspace registry missing at {path}; record {record_id} not written"
        )
        return
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    hit = next(
        (i for i, line in enumerate(lines) if _is_record_id_line(line, record_id)), None
    )
    if hit is not None:
        start, end = _record_item_span(lines, hit)
        field = next(
            (
                i
                for i in range(start, end)
                if not lines[i].lstrip().startswith("#")
                and lines[i].strip().startswith("provider_notebook_id:")
            ),
            None,
        )
        if field is None:
            print(
                f"[{spec.key}] NOTICE workspace record {record_id} carries no provider_notebook_id line — reconcile by hand"
            )
            return
        current = lines[field].split(":", 1)[1].strip()
        if current == notebook_id:
            return
        if not apply:
            print(
                f"[{spec.key}] REPLACE workspace record {record_id}: {current} -> {notebook_id} (re-pointed on --apply)"
            )
            return
        indent = lines[field][: len(lines[field]) - len(lines[field].lstrip())]
        lines[field] = f"{indent}provider_notebook_id: {notebook_id}"
        _ = path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(
            f"[{spec.key}] REPLACED workspace record {record_id}: {current} -> {notebook_id} in {path.relative_to(root)} (one active record per live book; commit it with the migration evidence)"
        )
        return
    if not apply:
        print(
            f"[{spec.key}] REGISTER workspace record {record_id} -> {notebook_id} (written on --apply)"
        )
        return
    created = (
        datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    )
    repo = spec.title.removeprefix(IDEATION_TITLE_PREFIX)
    block = f'  - kind: external_source_workspace\n    schema_version: 1\n    id: {record_id}\n    provider: notebooklm\n    provider_notebook_id: {notebook_id}\n    owner_layer: domain_hermes\n    scope:\n      domain_id: xfactory\n      client_id: null\n      customer_id: null\n    purpose: derived projection of brainstorm and staged governance docs ({repo})\n    default_authority_level: L1_notebook_synthesis\n    created_at: "{created}"\n    managed_by: openxFactory/scripts/sync-notebooklm-books.py\n'
    _ = path.write_text(text.rstrip("\n") + "\n" + block, encoding="utf-8")
    print(
        f"[{spec.key}] workspace record {record_id} -> {path.relative_to(root)} (commit it with the migration evidence)"
    )
