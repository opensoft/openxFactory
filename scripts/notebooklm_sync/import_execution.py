from __future__ import annotations

import json
from collections.abc import Callable, Iterable
from pathlib import Path

from .models import ExportPlan, ExportTarget, ImportTarget, SessionTarget
from .nlm_client import SourceRow, decode_json


def display_path(path: Path, root: Path) -> Path:
    try:
        return path.relative_to(root)
    except ValueError:
        return path


def plan_exports(
    root: Path,
    imported_on: str,
    sources: Iterable[SourceRow],
    seen: set[str],
    *,
    parse_title: Callable[[str], ExportTarget | None],
    destination: Callable[[Path, ExportTarget, str], Path],
) -> list[ExportPlan]:
    planned: list[ExportPlan] = []
    for source in sources:
        target = parse_title(source.title)
        if not source.source_id or target is None:
            continue
        planned.append(
            ExportPlan(
                source.source_id,
                source.title,
                target.status,
                target.repo,
                target.topic,
                target.title,
                destination(root, target, imported_on),
                source.source_id in seen,
            )
        )
    return planned


def plan_new_sources(
    imported_on: str,
    sources: Iterable[SourceRow],
    seen: set[str],
    target: ImportTarget,
    *,
    is_seed: Callable[[str], bool],
) -> list[ExportPlan]:
    planned: list[ExportPlan] = []
    for source in sources:
        source_id = source.source_id
        if not source_id or is_seed(source.title):
            continue
        planned.append(
            ExportPlan(
                source_id,
                source.title,
                target.status,
                target.repo,
                target.topic,
                source.title.strip() or source_id,
                target.path / f"notebooklm-ideas-{imported_on}.md",
                source_id in seen,
            )
        )
    return planned


def imported_file_header(plan: ExportPlan, notebook: str) -> str:
    origin = (
        "NotebookLM source imported from the analysis notebook. Notes enter "
        "this path only after a human converts them to sources; web, file, "
        "Drive, and other added sources enter as sources directly."
    )
    return (
        f"# NotebookLM Ideas: {plan.topic}\n\n"
        f"Status: {plan.status}\n"
        "Kind: reference\n"
        f"Repository context: {plan.repo}\n"
        f"Source workspace: {notebook}\n"
        "Authority: L1 notebook synthesis\n"
        f"Origin: {origin}\n\n"
        "These notes are imported evidence and idea material. They do not "
        "decide policy, memory, release scope, or OpenSpec approval.\n"
    )


def render_imported_entry(plan: ExportPlan, notebook: str, content: str) -> str:
    return (
        f"\n## {plan.title}\n\n"
        f"NotebookLM source id: {plan.source_id}\n"
        f"NotebookLM source title: {plan.source_title}\n"
        f"Source workspace: {notebook}\n\n"
        f"{content.strip()}\n"
    )


def source_content_text(raw: str) -> str:
    try:
        payload = decode_json(raw)
    except json.JSONDecodeError:
        return raw
    if not isinstance(payload, dict):
        return raw
    value = payload.get("value")
    if isinstance(value, dict):
        content = value.get("content")
        if isinstance(content, str):
            return content
    content = payload.get("content")
    return content if isinstance(content, str) else raw


def append_import(root: Path, plan: ExportPlan, notebook: str, content: str) -> None:
    resolved = plan.path.resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise SystemExit(f"refusing to write outside workspace: {plan.path}")
    resolved.parent.mkdir(parents=True, exist_ok=True)
    if not resolved.exists():
        _ = resolved.write_text(imported_file_header(plan, notebook), encoding="utf-8")
    with resolved.open("a", encoding="utf-8") as handle:
        _ = handle.write(render_imported_entry(plan, notebook, content))


def import_exported_sources(
    root: Path,
    notebook: str,
    apply: bool,
    planned: Iterable[ExportPlan],
    *,
    fetch: Callable[[str], str],
    append: Callable[[Path, ExportPlan, str, str], None],
) -> int:
    plans = list(planned)
    if not plans:
        print(f"[exports] no [export:*] sources found in {notebook}")
        return 0
    count = 0
    for plan in plans:
        if plan.already_imported:
            print(f"[exports] SKIP {plan.source_title} (already imported)")
            continue
        print(f"[exports] ADD  {plan.source_title} -> {display_path(plan.path, root)}")
        count += 1
        if apply:
            append(root, plan, notebook, fetch(plan.source_id))
    return count


def import_new_sources(
    root: Path,
    notebook: str,
    apply: bool,
    planned: Iterable[ExportPlan],
    session: SessionTarget | None,
    *,
    fetch: Callable[[str], str],
    append: Callable[[Path, ExportPlan, str, str], None],
    commit: Callable[[SessionTarget, list[Path], str], str | None],
) -> int:
    plans = list(planned)
    if not plans:
        print(f"[sources] no new importable sources found in {notebook}")
        return 0
    count = 0
    written: list[Path] = []
    for plan in plans:
        if plan.already_imported:
            print(f"[sources] SKIP {plan.source_title} (already imported)")
            continue
        print(f"[sources] ADD  {plan.source_title} -> {display_path(plan.path, root)}")
        count += 1
        if not apply:
            continue
        append(root, plan, notebook, fetch(plan.source_id))
        written.append(plan.path.resolve())
    if session is not None and written:
        _ = commit(session, written, notebook)
    return count
