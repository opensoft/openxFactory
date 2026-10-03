"""Typed, non-collectable adapters for session-sweep tests."""

from __future__ import annotations

import subprocess
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Protocol, TypeAlias, TypedDict, runtime_checkable

from opendox import branch_session as bs

from tests.notebooklm import _sync_test_support as raw

SweepVerdict: TypeAlias = Literal["live", "dead", "out-of-scope"]
SweepCall: TypeAlias = tuple[Literal["list"]] | tuple[Literal["retire"], str]


class SessionRow(TypedDict):
    title: str
    source_count: int


@dataclass(frozen=True, slots=True)
class Listing:
    rows: list[SessionRow]
    ok: bool
    detail: str = ""


@dataclass(frozen=True, slots=True)
class RetireResult:
    ok: bool
    detail: str


class SessionListingAdapter(Protocol):
    def list_sessions_result(self) -> Listing: ...


class RecordingAdapter:
    def __init__(
        self, titles: Sequence[str], calls: list[SweepCall], *, ok: bool
    ) -> None:
        self._titles: tuple[str, ...] = tuple(titles)
        self._calls: list[SweepCall] = calls
        self._ok: bool = ok

    def list_sessions_result(self) -> Listing:
        self._calls.append(("list",))
        rows = [SessionRow(title=title, source_count=7) for title in self._titles]
        return Listing(
            rows if self._ok else [],
            self._ok,
            "" if self._ok else "nlm notebook list failed",
        )


class RecordingRetiringAdapter(RecordingAdapter):
    def retire(self, alias: str) -> RetireResult:
        self._calls.append(("retire", alias))
        return RetireResult(True, "retired")


class SessionTarget(Protocol):
    repository: str
    branch: str


@runtime_checkable
class SweepSync(Protocol):
    def classify_session_notebooks(
        self,
        titles: Sequence[str],
        live: set[str],
        slugs: Sequence[str],
    ) -> list[tuple[str, SweepVerdict]]: ...

    def session_notebook_sweep(
        self, root: Path, apply: bool, adapter: SessionListingAdapter
    ) -> int: ...

    def live_session_aliases(
        self,
        root: Path,
        pairs: Sequence[tuple[str, Path]] | None = None,
    ) -> tuple[set[str], list[str]]: ...

    def live_session_targets(
        self, root: Path, branch: str, repository: str
    ) -> list[SessionTarget]: ...

    def session_repositories(self, root: Path) -> list[tuple[str, Path]]: ...


def sweep_sync() -> SweepSync:
    assert isinstance(raw.sync, SweepSync)
    return raw.sync


def session_in_feature_worktree(root: Path) -> Path:
    canonical = root / "openxFactory"
    canonical.mkdir()

    def git(*args: str, cwd: Path = canonical) -> None:
        _ = subprocess.run(
            ["git", *args],
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
        )

    git("init", "--initial-branch=main")
    git("config", "user.email", "h@example.invalid")
    git("config", "user.name", "Harness")
    git("config", "commit.gpgsign", "false")
    _ = (canonical / "seed.md").write_text("# seed\n", encoding="utf-8")
    git("add", "seed.md")
    git("commit", "-m", "seed")
    feature = root / "openxFactory-worktrees" / "feature-x"
    git("worktree", "add", "-b", "feature-x", str(feature))
    session = bs.sessions_root(feature) / bs.flatten_branch("draft/topic")
    session.parent.mkdir(parents=True, exist_ok=True)
    git("worktree", "add", "-b", "draft/topic", str(session))
    return canonical
