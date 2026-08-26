from __future__ import annotations

from pathlib import Path
from typing import Protocol, final, runtime_checkable

from notebooklm_sync.corpus import DesiredState
from notebooklm_sync.lifecycle_sync import SyncManifest
from notebooklm_sync.models import BookSpec, ExportPlan, ExportTarget, ImportTarget
from notebooklm_sync.nlm_client import ProviderResult

from tests.notebooklm._sync_test_support import load_sync_module
from tests.notebooklm._sync_world_support import HarnessFailure


class ProviderRunner(Protocol):
    def __call__(self, *args: str, parse: bool = True) -> ProviderResult: ...


class TimeModule(Protocol):
    def sleep(self, seconds: float) -> None: ...


class SubprocessModule(Protocol):
    run: ProviderRunner


@final
class SyncContractError(RuntimeError):
    def __init__(self, contract: str) -> None:
        self.contract = contract
        super().__init__(f"NotebookLM sync module lacks the {contract} test contract")


@runtime_checkable
class TypedSyncModule(Protocol):
    GROUNDING: tuple[str, ...]
    CHARTER_TITLE: str
    NOTEBOOK_SOURCE_CAP: int
    MAX_TEXT_ARG_BYTES: int
    ExportPlan: type[ExportPlan]
    nlm: ProviderRunner
    profile_account: ProviderRunner
    time: TimeModule
    subprocess: SubprocessModule

    def scan(self, root: Path) -> tuple[DesiredState, dict[str, BookSpec]]: ...
    def sync_book(
        self,
        root: Path,
        spec: BookSpec,
        desired: dict[str, str],
        manifest: SyncManifest,
        apply: bool,
    ) -> tuple[bool, bool]: ...
    def enforce_hosting_profile(
        self, root: Path, *, runner: ProviderRunner
    ) -> dict[str, str] | None: ...
    def read_hosting_declaration(self, root: Path) -> dict[str, str] | None: ...
    def active_nlm_profile(self, runner: ProviderRunner) -> str | None: ...
    def parity_report(self, root: Path) -> int: ...
    def bind_profile(self, profile: str | None) -> None: ...
    def parse_export_title(self, title: str) -> ExportTarget | None: ...
    def import_new_sources(
        self,
        root: Path,
        notebook: str,
        target_path: str,
        apply: bool,
        imported_on: str,
    ) -> int: ...
    def target_from_path(self, root: Path, target_path: str) -> ImportTarget: ...
    def append_import(
        self, root: Path, plan: ExportPlan, notebook: str, content: str
    ) -> None: ...


def load_typed_sync() -> TypedSyncModule:
    module = load_sync_module()
    if not isinstance(module, TypedSyncModule):
        raise SyncContractError("assigned NotebookLM")
    return module


def declare_hosting(root: Path, text: str) -> None:
    path = root / "openxFactory/examples/notebook-projection-hosting.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    _ = path.write_text(text, encoding="utf-8")


def profile_runner(active: str | None) -> ProviderRunner:
    def run(*args: str, parse: bool = True) -> ProviderResult:
        del parse
        if args[:3] == ("config", "get", "auth.default_profile"):
            if active is None:
                raise HarnessFailure("nlm config get: no configuration")
            return active
        return {}

    return run


def constant_runner(value: ProviderResult) -> ProviderRunner:
    def run(*args: str, parse: bool = True) -> ProviderResult:
        del args, parse
        return value

    return run


def no_sleep(_seconds: float) -> None:
    pass
