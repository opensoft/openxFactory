from __future__ import annotations

from collections.abc import Callable, Iterable
from contextlib import AbstractContextManager
from pathlib import Path
from typing import Protocol

from .models import ImportTarget, SessionNotebookRefused, SessionTarget
from .session_targets import SessionGit


class SessionCommitGit(SessionGit, Protocol):
    def worktree_action_lock(
        self, worktree: Path, *, action: str
    ) -> AbstractContextManager[None]: ...

    def stage(self, worktree: Path, paths: list[str]) -> None: ...

    def commit(self, worktree: Path, message: str, *, only: list[str]) -> str: ...


def commit_session_import(
    session: SessionTarget,
    written: Iterable[Path],
    *,
    notebook: str,
    git_factory: Callable[[Path], SessionCommitGit],
    assert_branch: Callable[[SessionCommitGit, Path, str, str], None],
    operation_errors: tuple[type[Exception], ...],
) -> str | None:
    worktree = session.worktree
    git = git_factory(session.checkout or worktree.parents[2])
    relatives = sorted({path.relative_to(worktree).as_posix() for path in written})
    try:
        with git.worktree_action_lock(
            worktree, action=f"notebooklm import from {notebook}"
        ):
            assert_branch(
                git,
                worktree,
                session.branch,
                f"the notebooklm import from {notebook}",
            )
            git.stage(worktree, relatives)
            sha = git.commit(
                worktree,
                f"notebooklm import: {', '.join(relatives)}\n\n"
                + f"Source-Notebook: {notebook}\n",
                only=relatives,
            )
    except operation_errors as exc:
        print(
            f"[session] NOT COMMITTED on {session.branch}: {exc} — the imported "
            + f"file is in {worktree} but UNTRACKED, and both endings remove that "
            + "worktree with `--force`. Commit it before the session ends (FR-041)"
        )
        return None
    print(f"[session] COMMITTED on {session.branch}: {sha} ({', '.join(relatives)})")
    return sha


def bind_session_import(
    root: Path,
    notebook: str,
    target: ImportTarget,
    *,
    session_for_alias: Callable[[Path, str], SessionTarget | None],
    worktree_of: Callable[[Path, Path], Path | None],
    notebook_prefix: str,
) -> SessionTarget | None:
    session = session_for_alias(root, notebook)
    inside = worktree_of(root, target.path)
    if session is None:
        if inside is None:
            return None
        raise SessionNotebookRefused(
            "[session] --target-path resolves inside the session worktree "
            + f"{inside} but {notebook!r} is not that session's notebook: a session "
            + "worktree holds ONE session's unmerged work, and importing another "
            + "notebook's sources into it would put content nobody projected from "
            + "this branch onto this branch (FR-041). Use "
            + f"{notebook_prefix}… for this session, or a target outside the worktree"
        )
    if inside is None or inside.resolve() != session.worktree.resolve():
        raise SessionNotebookRefused(
            f"[session] {notebook!r} is the notebook of the live session on "
            + f"{session.branch!r}, whose worktree is {session.worktree} — but "
            + f"--target-path resolves to {target.path}, which is not inside it. "
            + "FR-041 requires a session import to write into the origin folder "
            + "INSIDE the session worktree: a target outside it puts one session's "
            + "unmerged synthesis into the served checkout (FR-004) or into another "
            + "session's branch. Nothing was written"
        )
    return session


def session_worktree_of(
    path: Path,
    repositories: Iterable[tuple[str, Path]],
    sessions_root: Callable[[Path], Path],
) -> Path | None:
    resolved = path.resolve()
    for _name, checkout in repositories:
        sessions = sessions_root(checkout)
        try:
            resolved_sessions = sessions.resolve()
            if resolved_sessions not in resolved.parents:
                continue
        except OSError:
            continue
        relative = resolved.relative_to(resolved_sessions)
        return sessions / relative.parts[0]
    return None
