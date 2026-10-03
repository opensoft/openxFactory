from __future__ import annotations

from collections.abc import Callable, Iterable
from pathlib import Path
from typing import Protocol

from .models import SESSION_ALIAS_PREFIX, SessionNotebookRefused, SessionTarget


class WorktreeRecord(Protocol):
    path: str | Path
    branch: str | None


class SessionGit(Protocol):
    def worktree_records(self) -> Iterable[WorktreeRecord]: ...


class SessionGitFactory(Protocol):
    def __call__(self, checkout: Path) -> SessionGit: ...


class LiveSessionWorktree(Protocol):
    def __call__(self, git: SessionGit, checkout: Path, branch: str) -> Path | None: ...


class LiveSessionBranches(Protocol):
    def __call__(
        self, git: SessionGit, checkout: Path
    ) -> tuple[Iterable[str], Iterable[str]]: ...


def session_repository_slugs(pairs: Iterable[tuple[str, Path]]) -> list[str]:
    return [name.lower() for name, _checkout in pairs]


def session_repositories(
    root: Path, pinned_paths: Callable[[Path], Iterable[str]]
) -> list[tuple[str, Path]]:
    pairs = [("openxFactory", root / "openxFactory")]
    pairs.extend(
        (Path(relative).name, root / relative) for relative in pinned_paths(root)
    )
    return [(name, path) for name, path in pairs if path.is_dir()]


def live_session_targets(
    root: Path,
    branch: str,
    repository: str | None,
    *,
    repositories: Callable[[Path], list[tuple[str, Path]]],
    git_factory: SessionGitFactory,
    live_worktree: LiveSessionWorktree,
    notebook_alias: Callable[[str, str], str],
) -> list[SessionTarget]:
    found: list[SessionTarget] = []
    for name, checkout in repositories(root.resolve()):
        if repository and name != repository:
            continue
        roots = [checkout]
        try:
            for record in git_factory(checkout).worktree_records():
                candidate = Path(record.path)
                if candidate not in roots:
                    roots.append(candidate)
        except (AttributeError, OSError, RuntimeError, TypeError, ValueError) as exc:
            print(f"[session] NOTICE {name}: could not enumerate worktrees: {exc}")
        for checkout_root in roots:
            try:
                worktree = live_worktree(
                    git_factory(checkout_root), checkout_root, branch
                )
            except (AttributeError, OSError, RuntimeError, TypeError, ValueError):
                worktree = None
            if worktree is not None:
                found.append(
                    SessionTarget(
                        name, branch, worktree, notebook_alias(name, branch), checkout
                    )
                )
    return found


def resolve_session_target(
    root: Path,
    branch: str,
    repository: str | None,
    find_targets: Callable[[Path, str, str | None], list[SessionTarget]],
) -> SessionTarget:
    found = find_targets(root, branch, repository)
    if not found:
        named = f" in repository {repository!r}" if repository else ""
        raise SessionNotebookRefused(
            f"[session] no live session worktree for branch {branch!r}{named} "
            + f"under {root.resolve()}: a session notebook is bound to a LIVE "
            + "session, and liveness is the JOINT worktree+branch signal — a "
            + "directory alone is crash residue or an ended session, never a "
            + "session (FR-036, FR-008, D10). Nothing here creates, re-syncs, or "
            + "retires it"
        )
    if len(found) > 1:
        names = ", ".join(target.repository for target in found)
        paths = ", ".join(str(target.worktree) for target in found)
        advice = (
            "; a session notebook alias is keyed on (repository, branch) "
            + "(FR-037, spec C9), so name one with --session-repository"
            if len({target.repository for target in found}) > 1
            else "; the same branch is live under more than one session container "
            + "IN this repository, which no alias can disambiguate — end or clean "
            + "up all but one before addressing its notebook"
        )
        raise SessionNotebookRefused(
            f"[session] branch {branch!r} names a live session in more than "
            + f"one place ({names}: {paths}){advice}"
        )
    return found[0]


def session_target_for_alias(
    root: Path,
    notebook: str,
    *,
    notebook_prefix: str = SESSION_ALIAS_PREFIX,
    repositories: Callable[[Path], list[tuple[str, Path]]],
    git_factory: SessionGitFactory,
    live_worktree: LiveSessionWorktree,
    notebook_alias: Callable[[str, str], str],
) -> SessionTarget | None:
    alias = notebook.strip()
    if not alias.startswith(notebook_prefix):
        return None
    resolved_root = root.resolve()
    matches: list[SessionTarget] = []
    for name, checkout in repositories(resolved_root):
        try:
            git = git_factory(checkout)
            records = git.worktree_records()
        except (AttributeError, OSError, RuntimeError, TypeError, ValueError):
            continue
        for record in records:
            branch = record.branch
            if not branch or notebook_alias(name, branch) != alias:
                continue
            worktree = live_worktree(git, checkout, branch)
            if worktree is not None:
                matches.append(SessionTarget(name, branch, worktree, alias, checkout))
    if len(matches) > 1:
        names = ", ".join(f"{target.repository}@{target.branch}" for target in matches)
        raise SessionNotebookRefused(
            f"[session] the notebook alias {alias!r} resolves to MORE THAN ONE "
            + f"live session ({names}); FR-037 says two live sessions can never "
            + "share an alias, so this is a collision and an import cannot choose "
            + "between them — end one of the sessions first"
        )
    if not matches:
        raise SessionNotebookRefused(
            f"[session] {alias!r} is an `xf-session-*` notebook but no LIVE branch "
            + f"session under {resolved_root} owns it: liveness is the JOINT "
            + "worktree+branch signal (FR-008, D10), so a session whose worktree is "
            + "gone, whose branch is gone, or whose ending left residue owns nothing. "
            + "An import into a dead session's directory would write governed content "
            + "nothing can ever merge"
        )
    return matches[0]
