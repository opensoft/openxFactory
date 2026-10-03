"""Typed, non-collectable infrastructure shared by session tests."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Protocol, TypedDict, runtime_checkable

from notebooklm_sync.corpus import DesiredState
from notebooklm_sync.models import (
    BookSpec,
    ImportTarget,
    SessionSync,
    SessionTarget,
)
from notebooklm_sync.nlm_client import ProviderResult
from opendox import workbench as wb
from openxdox.snapshot_registry import SnapshotRegistry

from tests.notebooklm import _sync_test_support as raw
from tests.notebooklm import _sync_world_support as world


class NlmCall(Protocol):
    def __call__(self, *args: str, parse: bool = True) -> ProviderResult: ...


class GitCall(Protocol):
    def __call__(self, cwd: Path, *args: str) -> str: ...


class SeedCheckoutCall(Protocol):
    def __call__(self, checkout: Path, *, text: str) -> None: ...


class SessionWorldCall(Protocol):
    def __call__(
        self,
        root: Path,
        *,
        repository: str = "openxFactory",
        branch: str = "draft/demo-topic",
        main_text: str = "main body",
        worktree_text: str = "worktree body",
        nested: bool = False,
    ) -> tuple[Path, Path]: ...


class RegistryEntry(Protocol):
    repository: str
    ref: str


class FakeRegistry(Protocol):
    def get(self, repository: str, ref: str) -> RegistryEntry | None: ...

    def register(self, entry: RegistryEntry) -> RegistryEntry: ...

    def keys(self) -> list[tuple[str, str]]: ...

    def drop(self, repository: str, ref: str) -> None: ...


class _PrivateFixtureContract(Protocol):
    _add_worktree: Callable[[Path, str], Path]
    _doc: Callable[[str], str]
    _git: GitCall
    _seed_checkout: SeedCheckoutCall


@runtime_checkable
class _FixtureContract(_PrivateFixtureContract, Protocol):
    FakeRegistry: type[FakeRegistry]
    dashboard_registry: Callable[[], SnapshotRegistry]
    session_world: SessionWorldCall


class SessionFixture(_PrivateFixtureContract):
    def __init__(self, module: _FixtureContract) -> None:
        self._add_worktree: Callable[[Path, str], Path] = module._add_worktree
        self._dashboard_registry: Callable[[], SnapshotRegistry] = (
            module.dashboard_registry
        )
        self._doc: Callable[[str], str] = module._doc
        self._git: GitCall = module._git
        self._FakeRegistry: type[FakeRegistry] = module.FakeRegistry
        self._seed_checkout: SeedCheckoutCall = module._seed_checkout
        self._session_world: SessionWorldCall = module.session_world

    def add_worktree(self, checkout: Path, branch: str) -> Path:
        return self._add_worktree(checkout, branch)

    def dashboard_registry(self) -> SnapshotRegistry:
        return self._dashboard_registry()

    def doc(self, body: str) -> str:
        return self._doc(body)

    def git(self, cwd: Path, *args: str) -> str:
        return self._git(cwd, *args)

    def registry(self) -> FakeRegistry:
        return self._FakeRegistry()

    def seed_checkout(self, checkout: Path, *, text: str) -> None:
        self._seed_checkout(checkout, text=text)

    def session_world(
        self,
        root: Path,
        *,
        repository: str = "openxFactory",
        branch: str = "draft/demo-topic",
        main_text: str = "main body",
        worktree_text: str = "worktree body",
        nested: bool = False,
    ) -> tuple[Path, Path]:
        return self._session_world(
            root,
            repository=repository,
            branch=branch,
            main_text=main_text,
            worktree_text=worktree_text,
            nested=nested,
        )


@runtime_checkable
class ImportBindingSync(Protocol):
    nlm: NlmCall

    def import_new_sources(
        self,
        root: Path,
        notebook: str,
        target_arg: str,
        apply: bool,
        date: str,
    ) -> int: ...

    def resolve_session_target(self, root: Path, branch: str) -> None: ...

    def is_seed_source(self, title: str) -> bool: ...


@runtime_checkable
class NotebookImportSync(Protocol):
    nlm: NlmCall

    def import_new_sources(
        self,
        root: Path,
        notebook: str,
        target_arg: str,
        apply: bool,
        date: str,
    ) -> int: ...

    def target_from_path(self, root: Path, target_arg: str) -> ImportTarget: ...


class BookConfig(TypedDict):
    alias: str


@runtime_checkable
class LifecycleSync(Protocol):
    __file__: str | None
    NOTEBOOK_SOURCE_CAP: int
    SESSION_CONTAINER_SUFFIX: str
    IDEATION_ALIAS_PREFIX: str
    BOOKS: Mapping[str, BookConfig]
    session_source_set: Callable[[SessionTarget], list[tuple[str, str]]]

    def sync_session_notebook(
        self,
        root: Path,
        branch: str,
        *,
        apply: bool,
        adapter: wb.NotebookAdapter,
    ) -> SessionSync: ...

    def resolve_session_target(
        self,
        root: Path,
        branch: str,
        *,
        repository: str | None = None,
    ) -> SessionTarget: ...

    def workbench_orphan_sweep(
        self, root: Path, apply: bool, *, adapter: wb.NotebookAdapter
    ) -> None: ...

    def out_of_scope_workbench_dirs(self, root: Path) -> list[Path]: ...


class _OutOfScopeContract(Protocol):
    out_of_scope_workbench_dirs: Callable[[Path], list[Path]]


class _OutOfScopeFacade(_OutOfScopeContract):
    def __init__(self, module: _OutOfScopeContract) -> None:
        self.out_of_scope_workbench_dirs: Callable[[Path], list[Path]] = (
            module.out_of_scope_workbench_dirs
        )

    def paths(self, root: Path) -> list[Path]:
        return self.out_of_scope_workbench_dirs(root)


@runtime_checkable
class RefreshSync(Protocol):
    def scan(self, root: Path) -> tuple[DesiredState, dict[str, BookSpec]]: ...

    def pinned_factory_paths(self, root: Path) -> list[str]: ...

    def resolve_session_target(self, root: Path, branch: str) -> SessionTarget: ...

    def session_source_set(self, target: SessionTarget) -> list[tuple[str, str]]: ...

    def sync_session_notebook(
        self,
        root: Path,
        branch: str,
        *,
        apply: bool,
        adapter: wb.NotebookAdapter,
        retire: bool = False,
    ) -> SessionSync: ...


@runtime_checkable
class SessionNamespaceAdapter(Protocol):
    def retire(self, alias: str) -> wb.NotebookResult: ...

    def create_session(self, alias: str) -> wb.NotebookResult: ...


class SessionNamespaceFacade:
    def __init__(self, adapter: SessionNamespaceAdapter) -> None:
        self._adapter: SessionNamespaceAdapter = adapter

    def retire(self, alias: str) -> wb.NotebookResult:
        return self._adapter.retire(alias)

    def create_session(self, alias: str) -> wb.NotebookResult:
        return self._adapter.create_session(alias)


def import_binding_sync() -> ImportBindingSync:
    assert isinstance(raw.sync, ImportBindingSync)
    return raw.sync


def notebook_import_sync() -> NotebookImportSync:
    assert isinstance(raw.sync, NotebookImportSync)
    return raw.sync


def lifecycle_sync() -> LifecycleSync:
    assert isinstance(raw.sync, LifecycleSync)
    return raw.sync


def refresh_sync() -> RefreshSync:
    assert isinstance(raw.sync, RefreshSync)
    return raw.sync


def out_of_scope_workbench_dirs(module: LifecycleSync, root: Path) -> list[Path]:
    return _OutOfScopeFacade(module).paths(root)


fixture_module = world
assert isinstance(fixture_module, _FixtureContract)
fixture = SessionFixture(fixture_module)
FakeNlm = raw.FakeNlm
LIFECYCLE_BOOKS = raw.LIFECYCLE_BOOKS
SESSION_ALIAS = raw.SESSION_ALIAS
CODEX_SESSION_ALIAS = raw.CODEX_SESSION_ALIAS
STAGED_DOC = raw.STAGED_DOC
SYNC_OP = raw.SYNC_OP
SCRIPT = raw.SCRIPT
