from __future__ import annotations

from collections.abc import Callable, Sequence
from pathlib import Path
from types import ModuleType
from typing import Protocol, runtime_checkable

from .compat_errors import DashboardCompatibilityError
from .import_execution import (
    append_import,
    import_exported_sources,
    import_new_sources,
    plan_exports,
    plan_new_sources,
    source_content_text,
)
from .imports import (
    export_destination,
    imported_source_ids,
    parse_export_title,
    target_from_path,
)
from .models import (
    CHARTER_TITLE,
    HYBRID_CHARTER_TITLE,
    MANAGED_SOURCE_PREFIXES,
    ExportPlan,
    ImportTarget,
    SessionTarget,
)
from .nlm_client import SourceRow
from .session_imports import SessionCommitGit, commit_session_import


@runtime_checkable
class _ImportWorkbenchModule(Protocol):
    def parse_managed_source_title(self, title: str) -> tuple[str, str] | None: ...


@runtime_checkable
class _ImportSessionGitModule(Protocol):
    @property
    def SessionGit(self) -> Callable[[Path], SessionCommitGit]: ...


@runtime_checkable
class _ImportBranchSessionModule(Protocol):
    @property
    def SessionRefused(self) -> type[Exception]: ...

    def assert_git_holds_branch(
        self, git: SessionCommitGit, worktree: Path, branch: str, *, during: str
    ) -> None: ...


class ImportFacade:
    def __init__(
        self,
        *,
        list_sources: Callable[[str], list[SourceRow]],
        run_text: Callable[[tuple[str, ...]], str],
        dashboard: Callable[[str], ModuleType],
        bind_session: Callable[[Path, str, ImportTarget], SessionTarget | None],
    ) -> None:
        self._list_sources: Callable[[str], list[SourceRow]] = list_sources
        self._run_text: Callable[[tuple[str, ...]], str] = run_text
        self._dashboard: Callable[[str], ModuleType] = dashboard
        self._bind_session: Callable[
            [Path, str, ImportTarget], SessionTarget | None
        ] = bind_session

    def _workbench(self) -> _ImportWorkbenchModule:
        module = self._dashboard("workbench")
        if not isinstance(module, _ImportWorkbenchModule):
            raise DashboardCompatibilityError("workbench")
        return module

    def _session_git(self) -> _ImportSessionGitModule:
        module = self._dashboard("session_git")
        if not isinstance(module, _ImportSessionGitModule):
            raise DashboardCompatibilityError("session git")
        return module

    def _branch_session(self) -> _ImportBranchSessionModule:
        module = self._dashboard("branch_session")
        if not isinstance(module, _ImportBranchSessionModule):
            raise DashboardCompatibilityError("branch session")
        return module

    def export_plan(
        self, root: Path, notebook: str, imported_on: str
    ) -> list[ExportPlan]:
        return plan_exports(
            root,
            imported_on,
            self._list_sources(notebook),
            imported_source_ids(root),
            parse_title=parse_export_title,
            destination=export_destination,
        )

    def is_seed_source(self, title: str) -> bool:
        parser = self._workbench().parse_managed_source_title
        return (
            title in {CHARTER_TITLE, HYBRID_CHARTER_TITLE}
            or title.startswith(MANAGED_SOURCE_PREFIXES)
            or parser(title) is not None
        )

    def new_source_plan(
        self,
        root: Path,
        notebook: str,
        target: ImportTarget,
        imported_on: str,
    ) -> list[ExportPlan]:
        return plan_new_sources(
            imported_on,
            self._list_sources(notebook),
            imported_source_ids(root, extra_roots=(target.path,)),
            target,
            is_seed=self.is_seed_source,
        )

    def import_exported_sources(
        self, root: Path, notebook: str, apply: bool, imported_on: str
    ) -> int:
        return import_exported_sources(
            root,
            notebook,
            apply,
            self.export_plan(root, notebook, imported_on),
            fetch=self._fetch,
            append=append_import,
        )

    def import_new_sources(
        self,
        root: Path,
        notebook: str,
        target_path: str,
        apply: bool,
        imported_on: str,
    ) -> int:
        target = target_from_path(root, target_path)
        session = self._bind_session(root, notebook, target)
        return import_new_sources(
            root,
            notebook,
            apply,
            self.new_source_plan(root, notebook, target, imported_on),
            session,
            fetch=self._fetch,
            append=append_import,
            commit=lambda bound, written, source: self.commit_session_import(
                bound, written, notebook=source
            ),
        )

    def commit_session_import(
        self,
        session: SessionTarget,
        written: Sequence[Path],
        *,
        notebook: str,
    ) -> str | None:
        branch_session = self._branch_session()
        session_git = self._session_git()
        return commit_session_import(
            session,
            written,
            notebook=notebook,
            git_factory=session_git.SessionGit,
            assert_branch=lambda git, worktree, branch, during: (
                branch_session.assert_git_holds_branch(
                    git, worktree, branch, during=during
                )
            ),
            operation_errors=(
                branch_session.SessionRefused,
                AttributeError,
                OSError,
                RuntimeError,
                TypeError,
                ValueError,
            ),
        )

    def _fetch(self, source_id: str) -> str:
        return source_content_text(self._run_text(("source", "content", source_id)))
