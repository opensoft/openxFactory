from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from types import ModuleType

from .corpus import pinned_factory_paths
from .lifecycle import ensure_alias, ensure_workspace_record, resolve_or_create_book
from .lifecycle_sync import SyncManifest, sync_book
from .models import BookSpec
from .nlm_client import (
    JsonValue,
    NotebookRow,
    ProviderResult,
    SourceRow,
    parse_notebook_rows,
    parse_source_rows,
)
from .source_upload import add_text_source, add_with_one_retry
from .workbench import WorkbenchAdapter, orphan_sweep, out_of_scope_workbench_dirs

LegacyRow = Mapping[str, JsonValue]
RunText = Callable[[tuple[str, ...]], str]


class ProjectionFacade:
    def __init__(
        self,
        *,
        run_json: Callable[[tuple[str, ...]], ProviderResult],
        run_text: RunText,
        sleep: Callable[[float], None],
        dashboard: Callable[[str], ModuleType],
        source_cap: Callable[[], int],
        warn_headroom: Callable[[], int],
        max_text_bytes: Callable[[], int],
    ) -> None:
        self._run_json = run_json
        self._run_text = run_text
        self._sleep = sleep
        self._dashboard = dashboard
        self._source_cap = source_cap
        self._warn_headroom = warn_headroom
        self._max_text_bytes = max_text_bytes

    def list_sources(self, notebook: str) -> list[SourceRow]:
        return parse_source_rows(self._run_json(("source", "list", notebook, "--json")))

    def list_notebooks(self) -> list[NotebookRow]:
        return parse_notebook_rows(self._run_json(("notebook", "list", "--json")))

    def ensure_alias(self, spec: BookSpec, notebook_id: str) -> None:
        ensure_alias(spec, notebook_id, lambda *args: self._run_text(args))

    def resolve_or_create_book(
        self,
        root: Path,
        spec: BookSpec,
        apply: bool,
        notebooks: Sequence[NotebookRow | LegacyRow] | None = None,
        *,
        bind_alias: bool = True,
    ) -> tuple[str | None, bool]:
        return resolve_or_create_book(
            root,
            spec,
            apply,
            notebooks,
            bind_alias=bind_alias,
            list_notebooks=self.list_notebooks,
            set_alias=self.ensure_alias,
            run_text=lambda *args: self._run_text(args),
            sleep=self._sleep,
            write_record=ensure_workspace_record,
        )

    def add_with_one_retry(self, *args: str) -> str:
        return add_with_one_retry(
            args, run_text=lambda *command: self._run_text(command), sleep=self._sleep
        )

    def add_text_source(self, handle: str, text: str, title: str) -> None:
        add_text_source(
            handle,
            text,
            title,
            run_text=lambda *command: self._run_text(command),
            sleep=self._sleep,
            list_sources=self.list_sources,
            max_text_arg_bytes=self._max_text_bytes(),
        )

    def sync_book(
        self,
        root: Path,
        spec: BookSpec,
        desired: dict[str, str],
        manifest: SyncManifest,
        apply: bool,
        *,
        notebooks: Sequence[NotebookRow | LegacyRow] | None = None,
    ) -> tuple[bool, bool]:
        return sync_book(
            root,
            spec,
            desired,
            manifest,
            apply,
            notebooks,
            resolve_book=lambda base, book, do_apply, rows: self.resolve_or_create_book(
                base, book, do_apply, rows
            ),
            list_sources=self.list_sources,
            run_text=lambda *command: self._run_text(command),
            sleep=self._sleep,
            add_source=self.add_text_source,
            source_cap=self._source_cap(),
            warn_headroom=self._warn_headroom(),
        )

    def out_of_scope_workbench_dirs(self, root: Path) -> list[Path]:
        return out_of_scope_workbench_dirs(root, pinned_factory_paths)

    def workbench_orphan_sweep(
        self, root: Path, apply: bool, adapter: WorkbenchAdapter | None = None
    ) -> None:
        try:
            workbench = self._dashboard("workbench")
        except (ImportError, OSError, RuntimeError) as exc:
            print(f"[workbench] orphan sweep SKIPPED (unavailable: {exc})")
            return
        selected = adapter or workbench.NotebookAdapter()
        orphan_sweep(
            root,
            apply,
            selected,
            pinned_paths=pinned_factory_paths,
            live_aliases=lambda base, directory: workbench.live_notebook_aliases(
                base, workbench_dir=directory
            ),
            notebook_title=workbench._notebook_title,
            apply_sweep=lambda base, target, directory: workbench.orphan_sweep(
                base, target, workbench_dir=directory
            ),
        )
