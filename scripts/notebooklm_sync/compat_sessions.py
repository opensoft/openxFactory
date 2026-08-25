from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from pathlib import Path
from types import ModuleType

from .corpus import DesiredState, pinned_factory_paths
from .hosting import enforce_hosting_profile
from .import_execution import display_path
from .models import BookSpec, ImportTarget, SessionSync, SessionTarget
from .nlm_client import (
    JsonValue,
    NotebookRow,
    SourceRow,
    bind_profile,
    configured_nlm_profile,
)
from .parity import parity_report
from .session import (
    SessionAdapter,
    bind_session_import,
    live_session_aliases,
    live_session_targets,
    resolve_session_target,
    session_notebook_sweep,
    session_repositories,
    session_source_set,
    session_target_for_alias,
    session_worktree_of,
    sync_session_notebook,
)

LegacyRow = Mapping[str, JsonValue]


class SessionFacade:
    def __init__(
        self,
        *,
        dashboard: Callable[[str], ModuleType],
        source_cap: Callable[[], int],
        scan: Callable[[Path], tuple[DesiredState, dict[str, BookSpec]]],
        list_notebooks: Callable[[], list[NotebookRow]],
        list_sources: Callable[[str], list[SourceRow]],
        resolve_book: Callable[..., tuple[str | None, bool]],
        profile_account: Callable[[str], str | None],
        repositories_hook: Callable[[Path], list[tuple[str, Path]]],
        live_targets_hook: Callable[[Path, str, str | None], list[SessionTarget]],
        resolve_target_hook: Callable[[Path, str, str | None], SessionTarget],
        target_for_alias_hook: Callable[[Path, str], SessionTarget | None],
        worktree_of_hook: Callable[[Path, Path], Path | None],
        source_set_hook: Callable[[SessionTarget], list[tuple[str, str]]],
        live_aliases_hook: Callable[
            [Path, Iterable[tuple[str, Path]] | None], tuple[set[str], list[str]]
        ],
    ) -> None:
        self._dashboard = dashboard
        self._source_cap = source_cap
        self._scan = scan
        self._list_notebooks = list_notebooks
        self._list_sources = list_sources
        self._resolve_book = resolve_book
        self._profile_account = profile_account
        self._repositories_hook = repositories_hook
        self._live_targets_hook = live_targets_hook
        self._resolve_target_hook = resolve_target_hook
        self._target_for_alias_hook = target_for_alias_hook
        self._worktree_of_hook = worktree_of_hook
        self._source_set_hook = source_set_hook
        self._live_aliases_hook = live_aliases_hook

    def session_repositories(self, root: Path) -> list[tuple[str, Path]]:
        return session_repositories(root, pinned_factory_paths)

    def live_session_targets(
        self, root: Path, branch: str, repository: str | None = None
    ) -> list[SessionTarget]:
        branch_session = self._dashboard("branch_session")
        session_git = self._dashboard("session_git")
        return live_session_targets(
            root,
            branch,
            repository,
            repositories=self._repositories_hook,
            git_factory=session_git.SessionGit,
            live_worktree=branch_session.live_session_worktree,
            notebook_alias=branch_session.notebook_alias,
        )

    def resolve_session_target(
        self, root: Path, branch: str, repository: str | None = None
    ) -> SessionTarget:
        return resolve_session_target(root, branch, repository, self._live_targets_hook)

    def session_target_for_alias(
        self, root: Path, notebook: str
    ) -> SessionTarget | None:
        branch_session = self._dashboard("branch_session")
        session_git = self._dashboard("session_git")
        return session_target_for_alias(
            root,
            notebook,
            notebook_prefix=branch_session.NOTEBOOK_PREFIX,
            repositories=self._repositories_hook,
            git_factory=session_git.SessionGit,
            live_worktree=branch_session.live_session_worktree,
            notebook_alias=branch_session.notebook_alias,
        )

    def bind_session_import(
        self, root: Path, notebook: str, target: ImportTarget
    ) -> SessionTarget | None:
        return bind_session_import(
            root,
            notebook,
            target,
            session_for_alias=self._target_for_alias_hook,
            worktree_of=self._worktree_of_hook,
            notebook_prefix=self._dashboard("branch_session").NOTEBOOK_PREFIX,
        )

    def session_worktree_of(self, root: Path, path: Path) -> Path | None:
        return session_worktree_of(
            path,
            self._repositories_hook(root.resolve()),
            self._dashboard("branch_session").sessions_root,
        )

    def session_source_set(self, target: SessionTarget) -> list[tuple[str, str]]:
        workbench = self._dashboard("workbench")
        return session_source_set(
            target,
            lambda worktree, repository: workbench.session_documents(
                worktree, repository=repository
            ),
        )

    def sync_session_notebook(
        self,
        root: Path,
        branch: str,
        apply: bool = False,
        *,
        repository: str | None = None,
        adapter: SessionAdapter | None = None,
        retire: bool = False,
    ) -> SessionSync:
        workbench = self._dashboard("workbench")
        selected = adapter if adapter is not None else workbench.NotebookAdapter()
        return sync_session_notebook(
            root,
            branch,
            apply,
            repository=repository,
            retire=retire,
            adapter=selected,
            resolve_target=self._resolve_target_hook,
            source_set=self._source_set_hook,
            display_path=display_path,
            project_documents=workbench.project_documents,
            source_cap=self._source_cap(),
        )

    def live_session_aliases(
        self,
        root: Path,
        adapter_repositories: Iterable[tuple[str, Path]] | None = None,
    ) -> tuple[set[str], list[str]]:
        branch_session = self._dashboard("branch_session")
        session_git = self._dashboard("session_git")
        repositories = (
            adapter_repositories
            if adapter_repositories is not None
            else self._repositories_hook(root)
        )
        return live_session_aliases(
            repositories,
            git_factory=session_git.SessionGit,
            live_branches=branch_session.live_session_branches_of,
            notebook_alias=branch_session.notebook_alias,
        )

    def session_notebook_sweep(
        self, root: Path, apply: bool, adapter: SessionAdapter | None = None
    ) -> int:
        resolved = root.resolve()
        pairs = self._repositories_hook(resolved)
        aliases, errors = self._live_aliases_hook(resolved, pairs)
        workbench = self._dashboard("workbench")
        selected = adapter if adapter is not None else workbench.NotebookAdapter()
        if not hasattr(selected, "retire"):
            print("[session-sweep] REFUSED: adapter exposes no session retire operation")
            return 1
        return session_notebook_sweep(
            pairs,
            aliases,
            errors,
            apply,
            adapter=selected,
            notebook_title=workbench._notebook_title,
        )

    def active_nlm_profile(
        self, runner: Callable[..., str] | None = None
    ) -> str | None:
        if runner is None:
            return configured_nlm_profile()
        try:
            output = runner("config", "get", "auth.default_profile", parse=False)
        except (OSError, RuntimeError, TypeError, ValueError):
            return None
        return output.strip() or None if isinstance(output, str) else None

    def enforce_hosting_profile(
        self, root: Path, *, runner: Callable[..., str] | None = None
    ) -> dict[str, str] | None:
        return enforce_hosting_profile(
            root,
            active_profile=lambda: self.active_nlm_profile(runner),
            account_for=self._profile_account,
            bind=bind_profile,
        )

    def parity_report(
        self,
        root: Path,
        *,
        book: str | None = None,
        notebooks: Sequence[NotebookRow | LegacyRow] | None = None,
    ) -> int:
        return parity_report(
            root,
            book=book,
            notebooks=notebooks,
            scan=self._scan,
            list_notebooks=self._list_notebooks,
            resolve_book=self._resolve_book,
            list_sources=self._list_sources,
        )
