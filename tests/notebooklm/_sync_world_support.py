from __future__ import annotations

import subprocess
from collections.abc import Callable
from pathlib import Path
from typing import NoReturn, Protocol, final

from notebooklm_sync.nlm_client import ProviderResult
from opendox import branch_session as bs
from openxdox.snapshot_registry import SnapshotRegistry

STAGED_DOC = "ideation/staging/demo-topic/README.md"


class HarnessFailure(RuntimeError):
    pass


class RegistryEntry(Protocol):
    repository: str
    ref: str


def _doc(body: str) -> str:
    return f"# Demo Topic\n\nStatus: staged\nKind: staging-packet\n\n{body}\n"


def boom(*args: str, **kwargs: bool) -> NoReturn:
    del args, kwargs
    raise AssertionError("the real nlm runner must never be called in tests")


def _git(cwd: Path, *args: str) -> str:
    done = subprocess.run(
        ["git", *args], cwd=cwd, text=True, capture_output=True, check=True
    )
    return done.stdout.strip()


def _init_repo(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    _ = _git(root, "init", "--initial-branch=main")
    _ = _git(root, "config", "user.email", "harness@example.invalid")
    _ = _git(root, "config", "user.name", "Notebook Harness")
    _ = _git(root, "config", "commit.gpgsign", "false")


def _seed_checkout(checkout: Path, *, text: str) -> None:
    _init_repo(checkout)
    target = checkout / STAGED_DOC
    target.parent.mkdir(parents=True, exist_ok=True)
    _ = target.write_text(text, encoding="utf-8")
    _ = _git(checkout, "add", "--", STAGED_DOC)
    _ = _git(checkout, "commit", "-m", "Seed the scratch corpus")


def _add_worktree(checkout: Path, branch: str) -> Path:
    path = bs.worktree_path(checkout, branch)
    path.parent.mkdir(parents=True, exist_ok=True)
    _ = _git(checkout, "worktree", "add", "-b", branch, str(path), "main")
    return path


def session_world(
    root: Path,
    *,
    repository: str = "openxFactory",
    branch: str = "draft/demo-topic",
    main_text: str = "main body",
    worktree_text: str = "worktree body",
    nested: bool = False,
) -> tuple[Path, Path]:
    checkout = root / ("xFactories/" + repository if nested else repository)
    _seed_checkout(checkout, text=_doc(main_text))
    worktree = _add_worktree(checkout, branch)
    _ = (worktree / STAGED_DOC).write_text(_doc(worktree_text), encoding="utf-8")
    return checkout, worktree


@final
class FakeRegistry:
    def __init__(self) -> None:
        self.entries: dict[tuple[str, str], RegistryEntry] = {}

    def get(self, repository: str, ref: str) -> RegistryEntry | None:
        return self.entries.get((repository, ref))

    def register(self, entry: RegistryEntry) -> RegistryEntry:
        self.entries[(entry.repository, entry.ref)] = entry
        return entry

    def keys(self) -> list[tuple[str, str]]:
        return list(self.entries)

    def drop(self, repository: str, ref: str) -> None:
        _ = self.entries.pop((repository, ref), None)


def dashboard_registry() -> SnapshotRegistry:
    return SnapshotRegistry()


def declare_hosting(root: Path, text: str) -> None:
    path = root / "openxFactory/examples/notebook-projection-hosting.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    _ = path.write_text(text, encoding="utf-8")
    config = root / ".xfactory/notebook-hosting.yaml"
    config.parent.mkdir(parents=True, exist_ok=True)
    _ = config.write_text(
        "declaration_path: openxFactory/examples/notebook-projection-hosting.yaml\n",
        encoding="utf-8",
    )


def profile_runner(active: str | None) -> Callable[..., ProviderResult]:
    def run(*args: str, parse: bool = True) -> ProviderResult:
        del parse
        if args[:3] == ("config", "get", "auth.default_profile"):
            if active is None:
                raise HarnessFailure("nlm config get: no configuration")
            return active
        return {}

    return run
