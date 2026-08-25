from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from datetime import datetime, timezone
from pathlib import Path

from .models import (
    CHAT_PROMPT,
    IDEATION_TITLE_PREFIX,
    BookSpec,
    NotebookLifecycleError,
)
from .nlm_client import JsonValue, NotebookRow


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


def ensure_workspace_record(root: Path, spec: BookSpec, notebook_id: str) -> None:
    path = root / "openxFactory/examples/lifecycle-notebook-workspaces.yaml"
    record_id = f"workspace-xfactory-lifecycle-{spec.key}"
    if not path.is_file():
        print(
            f"[{spec.key}] NOTICE workspace registry missing at {path}; "
            f"record {record_id} not written"
        )
        return
    text = path.read_text(encoding="utf-8")
    if f"id: {record_id}" in text:
        if notebook_id not in text:
            print(
                f"[{spec.key}] NOTICE workspace record {record_id} exists "
                "with a DIFFERENT provider_notebook_id — reconcile by hand"
            )
        return
    created = datetime.now(timezone.utc).isoformat(timespec="seconds")
    created = created.replace("+00:00", "Z")
    repository = spec.title.removeprefix(IDEATION_TITLE_PREFIX)
    block = (
        "  - kind: external_source_workspace\n"
        "    schema_version: 1\n"
        f"    id: {record_id}\n"
        "    provider: notebooklm\n"
        f"    provider_notebook_id: {notebook_id}\n"
        "    owner_layer: domain_hermes\n"
        "    scope:\n"
        "      domain_id: xfactory\n"
        "      client_id: null\n"
        "      customer_id: null\n"
        "    purpose: derived projection of brainstorm and staged governance "
        f"docs ({repository})\n"
        "    default_authority_level: L1_notebook_synthesis\n"
        f"    created_at: \"{created}\"\n"
        "    managed_by: openxFactory/scripts/sync-notebooklm-books.py\n"
    )
    path.write_text(text.rstrip("\n") + "\n" + block, encoding="utf-8")
    print(
        f"[{spec.key}] workspace record {record_id} -> {path.relative_to(root)} "
        "(commit it with the migration evidence)"
    )


def ensure_alias(
    spec: BookSpec,
    notebook_id: str,
    run_text: Callable[..., str],
) -> None:
    try:
        run_text("alias", "set", spec.alias, notebook_id)
    except (OSError, RuntimeError, TypeError, ValueError) as exc:
        print(
            f"[{spec.key}] NOTICE alias {spec.alias!r} not registered "
            f"(non-fatal: {exc})"
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
    write_record: Callable[[Path, BookSpec, str], None],
) -> tuple[str | None, bool]:
    rows = notebooks if notebooks is not None else list_notebooks()
    identities = (notebook_identity(row) for row in rows)
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
        return notebook_id, True
    if not apply:
        print(f"[{spec.key}] CREATE {spec.title} (book missing; created on --apply)")
        return None, True
    run_text("notebook", "create", spec.title)
    sleep(2)
    fresh = {row.title: row.notebook_id for row in list_notebooks()}
    notebook_id = fresh.get(spec.title)
    if not notebook_id:
        raise NotebookLifecycleError(
            f"created notebook {spec.title!r} but a fresh listing does not "
            "resolve it by title"
        )
    print(f"[{spec.key}] CREATED {spec.title} ({notebook_id})")
    ok = True
    set_alias(spec, notebook_id)
    try:
        run_text("tag", "add", notebook_id, "--tags", "xfactory,lifecycle")
    except (OSError, RuntimeError, TypeError, ValueError) as exc:
        ok = False
        print(f"[{spec.key}] FAILED tagging {spec.title!r}: {exc}")
    try:
        run_text(
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
    write_record(root, spec, notebook_id)
    sleep(2)
    return notebook_id, ok
