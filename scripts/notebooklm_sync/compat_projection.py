from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from types import ModuleType
from typing import Protocol, runtime_checkable

from .compat_errors import DashboardCompatibilityError
from .corpus import governed_repo_paths
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
from .source_context import SourceContext
from .source_upload import add_text_source, add_with_one_retry
from .workbench import (
    SweepResult,
    WorkbenchAdapter,
    orphan_sweep,
    out_of_scope_workbench_dirs,
)

LegacyRow = Mapping[str, JsonValue]
RunText = Callable[[tuple[str, ...]], str]


@runtime_checkable
class _ProjectionWorkbenchModule(Protocol):
    @property
    def NotebookAdapter(self) -> type[WorkbenchAdapter]: ...

    def live_notebook_aliases(
        self, repo_root: Path, *, workbench_dir: str
    ) -> set[str]: ...

    def orphan_sweep(
        self, repo_root: Path, adapter: WorkbenchAdapter, *, workbench_dir: str
    ) -> SweepResult: ...


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
        source_context: Callable[[], SourceContext],
    ) -> None:
        self._run_json: Callable[[tuple[str, ...]], ProviderResult] = run_json
        self._run_text: RunText = run_text
        self._sleep: Callable[[float], None] = sleep
        self._dashboard: Callable[[str], ModuleType] = dashboard
        self._source_cap: Callable[[], int] = source_cap
        self._warn_headroom: Callable[[], int] = warn_headroom
        self._source_context: Callable[[], SourceContext] = source_context
        self._max_text_bytes: Callable[[], int] = max_text_bytes

    def _workbench(self) -> _ProjectionWorkbenchModule:
        module = self._dashboard("workbench")
        if not isinstance(module, _ProjectionWorkbenchModule):
            raise DashboardCompatibilityError("workbench")
        return module

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
            context=self._source_context(),
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
        return out_of_scope_workbench_dirs(root, governed_repo_paths)

    def workbench_orphan_sweep(
        self, root: Path, apply: bool, adapter: WorkbenchAdapter | None = None
    ) -> None:
        try:
            workbench = self._workbench()
            selected = adapter or workbench.NotebookAdapter()
            live_notebook_aliases = workbench.live_notebook_aliases
            apply_orphan_sweep = workbench.orphan_sweep
        except (
            AttributeError,
            DashboardCompatibilityError,
            ImportError,
            OSError,
            RuntimeError,
        ) as exc:
            print(f"[workbench] orphan sweep SKIPPED (unavailable: {exc})")
            return
        orphan_sweep(
            root,
            apply,
            selected,
            pinned_paths=governed_repo_paths,
            live_aliases=lambda base, directory: live_notebook_aliases(
                base, workbench_dir=directory
            ),
            notebook_title=self._notebook_title,
            apply_sweep=lambda base, target, directory: apply_orphan_sweep(
                base, target, workbench_dir=directory
            ),
        )

    @staticmethod
    def _notebook_title(notebook: LegacyRow) -> str | None:
        for key in ("title", "name", "emoji_title"):
            value = notebook.get(key)
            if isinstance(value, str) and value:
                return value
        return None
