"""Shared, non-collectable support for NotebookLM sync tests."""

from __future__ import annotations

import importlib.util
import itertools
import re
import sys
from collections.abc import Iterable, Mapping
from pathlib import Path
from types import ModuleType
from typing import Protocol, final, runtime_checkable

from notebooklm_sync.nlm_client import JsonValue, ProviderResult
from opendox import branch_session as bs
from opendox.workbench import NotebookAdapter

from tests.notebooklm import _sync_world_support as world
from tests.notebooklm._sync_world_support import HarnessFailure

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "sync-notebooklm-books.py"
STAGED_DOC = world.STAGED_DOC


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


@runtime_checkable
class SyncModule(Protocol):
    BOOKS: Mapping[str, Mapping[str, str]]

    def workbench_orphan_sweep(
        self, root: Path, apply: bool, adapter: NotebookAdapter | None = None
    ) -> None: ...


def load_sync_module() -> SyncModule:
    """Load the public hyphenated entry point and verify its test contract."""
    existing = sys.modules.get("sync_notebooklm_books")
    module = (
        existing
        if existing is not None and existing.__file__ == str(SCRIPT)
        else load_script_module("sync_notebooklm_books", SCRIPT)
    )
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
    if not isinstance(module, SyncModule):
        raise TestSupportError("NotebookLM sync entry point has an invalid contract")
    return module


sync = load_sync_module()

SYNC_OP = re.compile(r"^\[[^\]]+\]\s+(ADD|DEL|UPD)\s")
LIFECYCLE_BOOKS: list[dict[str, str]] = [
    {"id": "b1", "title": "xf-ideation"},
    {"id": "b2", "title": "xf-drafts"},
    {"id": "b3", "title": "xf-canon"},
]
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


@final
class FakeNlm:
    """Typed, isolated runner for the NotebookLM verbs used by the tests."""

    def __init__(
        self,
        notebooks: Iterable[Mapping[str, JsonValue]] = (),
        *,
        quota: int | None = None,
    ) -> None:
        self.calls: list[tuple[str, ...]] = []
        self.notebooks: list[dict[str, str]] = [
            {"id": str(notebook["id"]), "title": str(notebook["title"])}
            for notebook in notebooks
        ]
        self.sources: dict[str, list[dict[str, str]]] = {
            notebook["id"]: [] for notebook in self.notebooks
        }
        self.quota: int | None = quota
        self._ids: itertools.count[int] = itertools.count(1)

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
                    "nlm notebook create: the account's notebook limit is reached (quota exhausted)"
                )
            notebook = {"id": f"nb{next(self._ids)}", "title": title}
            self.notebooks.append(notebook)
            self.sources[notebook["id"]] = []
            return dict(notebook)
        if head == ("notebook", "delete"):
            self.notebooks = [row for row in self.notebooks if row["id"] != args[2]]
            _ = self.sources.pop(args[2], None)
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


_boom = world.boom
_session_world = world.session_world
_FakeRegistry = world.FakeRegistry
_dashboard_registry = world.dashboard_registry
_declare_hosting = world.declare_hosting
_profile_runner = world.profile_runner
