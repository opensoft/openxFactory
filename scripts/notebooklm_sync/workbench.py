from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from pathlib import Path
from typing import Protocol

from .nlm_client import JsonValue

V1_WORKBENCH_DIR = "openxFactory/ideation/workbench/"


class NotebookListing(Protocol):
    ok: bool
    detail: str
    rows: Iterable[Mapping[str, JsonValue]]


class WorkbenchAdapter(Protocol):
    def available(self) -> bool: ...

    def list_scratch_result(self) -> NotebookListing: ...


class SweepResult(Protocol):
    skipped: bool
    detail: str
    deleted: Sequence[str] | None
    kept: Sequence[str] | None


def out_of_scope_workbench_dirs(
    root: Path, pinned_paths: Callable[[Path], Iterable[str]]
) -> list[Path]:
    directories = [root / "ideation" / "workbench"]
    directories.extend(
        root / relative / "ideation" / "workbench" for relative in pinned_paths(root)
    )
    return [directory for directory in directories if directory.is_dir()]


def orphan_sweep(
    root: Path,
    apply: bool,
    adapter: WorkbenchAdapter,
    *,
    pinned_paths: Callable[[Path], Iterable[str]],
    live_aliases: Callable[[Path, str], set[str]],
    notebook_title: Callable[[Mapping[str, JsonValue]], str | None],
    apply_sweep: Callable[[Path, WorkbenchAdapter, str], SweepResult],
) -> None:
    resolved_root = root.resolve()
    if not adapter.available():
        print("[workbench] orphan sweep SKIPPED (nlm unavailable)")
        return
    strays = [
        directory
        for directory in out_of_scope_workbench_dirs(resolved_root, pinned_paths)
        if any(directory.glob("*.workbench.yaml"))
    ]
    if strays:
        relatives = ", ".join(
            str(directory.relative_to(resolved_root)) for directory in strays
        )
        print(
            "[workbench] orphan sweep SKIPPED (manifests outside the v1 "
            + f"openxFactory scope: {relatives}; extend the sweep scope before "
            + "enabling)"
        )
        return
    if not apply:
        live = live_aliases(resolved_root, V1_WORKBENCH_DIR)
        listing = adapter.list_scratch_result()
        if not listing.ok:
            print(
                "[workbench] orphan sweep plan UNAVAILABLE (the notebook list "
                + "could not be read, so nothing is known about orphans — this "
                + f"is NOT an empty account: {listing.detail})"
            )
            return
        pending = 0
        for notebook in listing.rows:
            title = notebook_title(notebook)
            if not title:
                continue
            if title in live:
                print(f"[workbench] KEEP  {title} (bound by a live manifest)")
            else:
                pending += 1
                print(f"[workbench] SWEEP {title} (orphan; removed on --apply)")
        if pending:
            print(
                f"[workbench] dry-run: {pending} orphan(s) pending; "
                + "re-run with --apply to sweep"
            )
        return
    result = apply_sweep(resolved_root, adapter, V1_WORKBENCH_DIR)
    if result.skipped:
        print(f"[workbench] orphan sweep SKIPPED ({result.detail})")
        return
    print(
        f"[workbench] {result.detail}; "
        + f"deleted={result.deleted or []} kept={result.kept or []}"
    )
