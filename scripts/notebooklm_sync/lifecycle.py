from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from pathlib import Path

from . import workspace_records
from .models import (
    CHAT_PROMPT,
    BookSpec,
    NotebookLifecycleError,
)
from .nlm_client import JsonValue, NotebookRow

ensure_workspace_record = workspace_records.ensure_workspace_record


def notebook_identity(
    row: NotebookRow | Mapping[str, JsonValue],
) -> tuple[str, str] | None:
    if isinstance(row, NotebookRow):
        return row.title, row.notebook_id
    title = row.get("title")
    notebook_id = row.get("id")
    if isinstance(title, str) and isinstance(notebook_id, str) and notebook_id:
        return title, notebook_id
    return None


def ensure_alias(
    spec: BookSpec,
    notebook_id: str,
    run_text: Callable[..., str],
) -> None:
    try:
        _ = run_text("alias", "set", spec.alias, notebook_id)
    except (OSError, RuntimeError, TypeError, ValueError) as exc:
        print(
            f"[{spec.key}] NOTICE alias {spec.alias!r} not registered "
            + f"(non-fatal: {exc})"
        )


def resolve_or_create_book(
    root: Path,
    spec: BookSpec,
    apply: bool,
    notebooks: Sequence[NotebookRow | Mapping[str, JsonValue]] | None,
    *,
    bind_alias: bool,
    list_notebooks: Callable[[], list[NotebookRow]],
    set_alias: Callable[[BookSpec, str], None],
    run_text: Callable[..., str],
    sleep: Callable[[float], None],
    write_record: Callable[[Path, BookSpec, str, bool], None],
) -> tuple[str | None, bool]:
    rows = notebooks if notebooks is not None else list_notebooks()
    identities = [notebook_identity(row) for row in rows]
    by_title = {
        title: notebook_id
        for item in identities
        if item is not None
        for title, notebook_id in (item,)
    }
    notebook_id = by_title.get(spec.title)
    if notebook_id:
        if bind_alias:
            set_alias(spec, notebook_id)
        titled = {
            item[1] for item in identities if item is not None and item[0] == spec.title
        }
        if len(titled) > 1:
            print(
                f"[{spec.key}] NOTICE {len(titled)} notebooks are titled {spec.title!r} ({', '.join(sorted(titled))}) — the workspace record is left unchanged; resolve the duplicate by hand before trusting this book's registration"
            )
        else:
            write_record(root, spec, notebook_id, apply)
        return notebook_id, True
    if not apply:
        print(f"[{spec.key}] CREATE {spec.title} (book missing; created on --apply)")
        return None, True
    _ = run_text("notebook", "create", spec.title)
    sleep(2)
    fresh = {row.title: row.notebook_id for row in list_notebooks()}
    notebook_id = fresh.get(spec.title)
    if not notebook_id:
        raise NotebookLifecycleError(
            f"created notebook {spec.title!r} but a fresh listing does not "
            + "resolve it by title"
        )
    print(f"[{spec.key}] CREATED {spec.title} ({notebook_id})")
    ok = True
    set_alias(spec, notebook_id)
    try:
        _ = run_text("tag", "add", notebook_id, "--tags", "xfactory,lifecycle")
    except (OSError, RuntimeError, TypeError, ValueError) as exc:
        ok = False
        print(f"[{spec.key}] FAILED tagging {spec.title!r}: {exc}")
    try:
        _ = run_text(
            "chat",
            "configure",
            notebook_id,
            "--goal",
            "custom",
            "--prompt",
            CHAT_PROMPT,
        )
    except (OSError, RuntimeError, TypeError, ValueError) as exc:
        ok = False
        print(f"[{spec.key}] FAILED chat framing for {spec.title!r}: {exc}")
    write_record(root, spec, notebook_id, apply)
    sleep(2)
    return notebook_id, ok
