"""Shared, non-collectable support for NotebookLM sync tests."""

from __future__ import annotations

import importlib.util
import itertools
import re
import subprocess
import sys
from collections.abc import Callable, Iterable, Mapping
from pathlib import Path
from types import ModuleType
from typing import NoReturn, Protocol

from ideation_dashboard import branch_session as bs
from ideation_dashboard.snapshot_registry import SnapshotRegistry
from notebooklm_sync.nlm_client import JsonValue, ProviderResult

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "sync-notebooklm-books.py"


class TestSupportError(RuntimeError):
    pass


def load_script_module(name: str, path: Path) -> ModuleType:
    """Load a script as a module after checking the importlib result."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise TestSupportError(f"cannot load script module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_sync_module() -> ModuleType:
    """Load the public hyphenated entry point and verify its test contract."""
    module = load_script_module("sync_notebooklm_books", SCRIPT)
    required = (
        "main",
        "scan",
        "sync_book",
        "sync_session_notebook",
        "enforce_hosting_profile",
    )
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        joined = ", ".join(missing)
        raise TestSupportError(f"NotebookLM sync entry point lacks: {joined}")
    return module


sync = load_sync_module()

SYNC_OP = re.compile(r"^\[[^\]]+\]\s+(ADD|DEL|UPD)\s")
LIFECYCLE_BOOKS: list[dict[str, str]] = [
    {"id": "b1", "title": "xf-ideation"},
    {"id": "b2", "title": "xf-drafts"},
    {"id": "b3", "title": "xf-canon"},
]
STAGED_DOC = "ideation/staging/demo-topic/README.md"
SESSION_ALIAS = bs.notebook_alias("openxFactory", "draft/demo-topic")
CODEX_SESSION_ALIAS = bs.notebook_alias("codexFactory", "draft/demo-topic")

HOSTING_DECLARED = """schema_version: 1
kind: notebook_projection_hosting
hosting:
  case: operator_hosted
  account: xFactor001@opensoft.one
  account_type: google_workspace_user
  domain: opensoft.one
  nlm_profile: company
  declared_at: "2026-08-23"
  declared_by: Brett Heap
share_out: []
"""

HOSTING_PENDING = """schema_version: 1
kind: notebook_projection_hosting
hosting:
  case: operator_hosted
  account: xFactor001@opensoft.one
  account_type: google_workspace_user
  domain: opensoft.one
  nlm_profile: company
  migration:
    state: pending
    from_account: brettheap@gmail.com
    from_nlm_profile: personal
share_out: []
"""


class HarnessFailure(RuntimeError):
    pass


class RegistryEntry(Protocol):
    repository: str
    ref: str


def _doc(body: str) -> str:
    return f"# Demo Topic\n\nStatus: staged\nKind: staging-packet\n\n{body}\n"


class FakeNlm:
    """Typed, isolated runner for the NotebookLM verbs used by the tests."""

    def __init__(
        self,
        notebooks: Iterable[Mapping[str, JsonValue]] = (),
        *,
        quota: int | None = None,
    ) -> None:
        self.calls: list[tuple[str, ...]] = []
        self.notebooks = [
            {"id": str(notebook["id"]), "title": str(notebook["title"])}
            for notebook in notebooks
        ]
        self.sources: dict[str, list[dict[str, str]]] = {
            notebook["id"]: [] for notebook in self.notebooks
        }
        self.quota = quota
        self._ids = itertools.count(1)

    def __call__(self, *args: str, parse: bool = True) -> ProviderResult:
        del parse
        self.calls.append(args)
        head = args[:2]
        if head == ("notebook", "list"):
            return [dict(notebook) for notebook in self.notebooks]
        if head == ("notebook", "create"):
            title = args[2]
            if self.quota is not None and len(self.notebooks) >= self.quota:
                raise HarnessFailure(
                    "nlm notebook create: the account's notebook limit is "
                    "reached (quota exhausted)"
                )
            notebook = {"id": f"nb{next(self._ids)}", "title": title}
            self.notebooks.append(notebook)
            self.sources[notebook["id"]] = []
            return dict(notebook)
        if head == ("notebook", "delete"):
            self.notebooks = [row for row in self.notebooks if row["id"] != args[2]]
            self.sources.pop(args[2], None)
            return ""
        if head == ("notebook", "get"):
            return {"id": args[2]}
        if head == ("source", "list"):
            return [dict(source) for source in self.sources.get(args[2], [])]
        if head == ("source", "add"):
            notebook_id, text, title = args[2], args[4], args[6]
            source = {
                "id": f"src{next(self._ids)}",
                "title": title,
                "content": text,
            }
            self.sources.setdefault(notebook_id, []).append(source)
            return ""
        if head == ("source", "delete"):
            for notebook_id, rows in self.sources.items():
                self.sources[notebook_id] = [
                    row for row in rows if row["id"] != args[2]
                ]
            return ""
        return {}

    def titles(self) -> list[str]:
        return sorted(notebook["title"] for notebook in self.notebooks)

    def notebook(self, title: str) -> dict[str, str] | None:
        return next(
            (notebook for notebook in self.notebooks if notebook["title"] == title),
            None,
        )

    def notebook_id(self, title: str) -> str:
        notebook = self.notebook(title)
        if notebook is None:
            raise HarnessFailure(f"fake notebook does not exist: {title}")
        return notebook["id"]

    def sources_of(self, title: str) -> list[dict[str, str]]:
        notebook = self.notebook(title)
        return list(self.sources.get(notebook["id"], [])) if notebook else []

    def added_contents(self) -> list[str]:
        return [call[4] for call in self.calls if call[:2] == ("source", "add")]

    def created_titles(self) -> list[str]:
        return [call[2] for call in self.calls if call[:2] == ("notebook", "create")]

    def deleted_ids(self) -> list[str]:
        return [call[2] for call in self.calls if call[:2] == ("notebook", "delete")]


def _boom(*args: str, **kwargs: bool) -> NoReturn:
    del args, kwargs
    raise AssertionError("the real nlm runner must never be called in tests")


def _git(cwd: Path, *args: str) -> str:
    done = subprocess.run(
        ["git", *args], cwd=cwd, text=True, capture_output=True, check=True
    )
    return done.stdout.strip()


def _init_repo(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    _git(root, "init", "--initial-branch=main")
    _git(root, "config", "user.email", "harness@example.invalid")
    _git(root, "config", "user.name", "Notebook Harness")
    _git(root, "config", "commit.gpgsign", "false")


def _seed_checkout(checkout: Path, *, text: str) -> None:
    _init_repo(checkout)
    target = checkout / STAGED_DOC
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    _git(checkout, "add", "--", STAGED_DOC)
    _git(checkout, "commit", "-m", "Seed the scratch corpus")


def _add_worktree(checkout: Path, branch: str) -> Path:
    path = bs.worktree_path(checkout, branch)
    path.parent.mkdir(parents=True, exist_ok=True)
    _git(checkout, "worktree", "add", "-b", branch, str(path), "main")
    return path


def _session_world(
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
    (worktree / STAGED_DOC).write_text(_doc(worktree_text), encoding="utf-8")
    return checkout, worktree


class _FakeRegistry:
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
        self.entries.pop((repository, ref), None)


def _dashboard_registry() -> SnapshotRegistry:
    return SnapshotRegistry()


def _declare_hosting(root: Path, text: str) -> None:
    path = root / "openxFactory/examples/notebook-projection-hosting.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _profile_runner(active: str | None) -> Callable[..., ProviderResult]:
    def run(*args: str, parse: bool = True) -> ProviderResult:
        del parse
        if args[:3] == ("config", "get", "auth.default_profile"):
            if active is None:
                raise HarnessFailure("nlm config get: no configuration")
            return active
        return {}

    return run
