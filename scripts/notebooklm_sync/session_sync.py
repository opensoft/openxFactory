from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from pathlib import Path
from typing import Protocol, runtime_checkable

from .models import SessionSync, SessionTarget
from .nlm_client import JsonValue
from .session_targets import SessionGit, SessionGitFactory


class SessionActionResult(Protocol):
    ok: bool
    skipped: bool
    detail: str


class SessionListingResult(Protocol):
    ok: bool
    detail: str
    rows: Iterable[Mapping[str, JsonValue]]


class SessionAdapter(Protocol):
    def available(self) -> bool: ...

    def retire(self, alias: str) -> SessionActionResult: ...

    def list_sessions_result(self) -> SessionListingResult: ...


class ProjectDocuments(Protocol):
    def __call__(
        self,
        adapter: SessionAdapter,
        alias: str,
        documents: list[tuple[str, str]],
    ) -> SessionActionResult: ...


@runtime_checkable
class SessionGitModule(Protocol):
    @property
    def SessionGit(self) -> SessionGitFactory: ...


@runtime_checkable
class BranchSessionModule(Protocol):
    @property
    def NOTEBOOK_PREFIX(self) -> str: ...

    def live_session_worktree(
        self, git: SessionGit, checkout: Path, branch: str
    ) -> Path | None: ...

    def notebook_alias(self, repository: str, branch: str) -> str: ...

    def sessions_root(self, checkout: Path) -> Path: ...

    def live_session_branches_of(
        self, git: SessionGit, checkout: Path
    ) -> tuple[Iterable[str], Iterable[str]]: ...


@runtime_checkable
class SessionDocumentsModule(Protocol):
    def session_documents(
        self, worktree: Path, *, repository: str | None = None
    ) -> list[tuple[str, str]]: ...


@runtime_checkable
class SessionWorkbenchModule(Protocol):
    @property
    def NotebookAdapter(self) -> type[SessionAdapter]: ...

    def session_documents(
        self, worktree: Path, *, repository: str | None = None
    ) -> list[tuple[str, str]]: ...

    def project_documents(
        self,
        adapter: SessionAdapter,
        alias: str,
        documents: list[tuple[str, str]],
    ) -> SessionActionResult: ...


def session_source_set(
    target: SessionTarget,
    documents: Callable[[Path, str], list[tuple[str, str]]],
) -> list[tuple[str, str]]:
    return documents(target.worktree, target.repository)


def sync_session_notebook(
    root: Path,
    branch: str,
    apply: bool,
    *,
    repository: str | None,
    retire: bool,
    adapter: SessionAdapter,
    resolve_target: Callable[[Path, str, str | None], SessionTarget],
    source_set: Callable[[SessionTarget], list[tuple[str, str]]],
    display_path: Callable[[Path, Path], Path],
    project_documents: ProjectDocuments,
    source_cap: int,
) -> SessionSync:
    target = resolve_target(root, branch, repository)
    relative = display_path(target.worktree, root.resolve())
    if not adapter.available():
        print(f"[session] {target.alias} SKIPPED (nlm unavailable)")
        return SessionSync(
            target=target,
            skipped=True,
            detail="nlm unavailable — notebook action skipped, not blocked",
        )
    if retire:
        return retire_session_notebook(target, apply, adapter)
    documents = source_set(target)
    paths = tuple(path for path, _text in documents)
    print(
        f"[session] SYNC {target.alias} <- {len(paths)} worktree source(s) "
        + f"({relative})"
    )
    for path in paths:
        print(f"[session]   source {path}")
    if len(paths) > source_cap:
        print(
            f"[session] {target.alias} REFUSED: {len(paths)} desired sources "
            + f"exceed the provider's {source_cap}-source per-notebook cap by "
            + f"{len(paths) - source_cap}. Applying would die mid-run; scope the "
            + "session membership rule down or split the projection first (see "
            + "split-ideation-book-per-repo). Nothing was created, added, or retired."
        )
        return SessionSync(
            target=target,
            documents=paths,
            skipped=True,
            detail=f"{len(paths)} desired sources exceed the {source_cap}-source provider cap",
        )
    if not apply:
        print("[session] dry-run: re-run with --apply to sync")
        return SessionSync(target=target, documents=paths, detail="sync planned")
    result = project_documents(adapter, target.alias, documents)
    print(f"[session] {target.alias}: {result.detail}")
    return SessionSync(
        target=target,
        documents=paths,
        applied=True,
        skipped=bool(result.skipped),
        detail=result.detail,
    )


def retire_session_notebook(
    target: SessionTarget, apply: bool, adapter: SessionAdapter
) -> SessionSync:
    print(
        f"[session] RETIRE {target.alias} (the session is over; the "
        + "notebook is not re-pointed at main)"
    )
    if not apply:
        print("[session] dry-run: re-run with --apply to retire")
        return SessionSync(target=target, detail="retire planned")
    result = adapter.retire(target.alias)
    print(f"[session] {target.alias}: {result.detail}")
    return SessionSync(
        target=target,
        applied=True,
        retired=bool(result.ok and not result.skipped),
        skipped=bool(result.skipped),
        detail=result.detail,
    )
