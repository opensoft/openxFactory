#!/usr/bin/env python3
from __future__ import annotations

import subprocess as _subprocess
import sys
import time
from collections.abc import Iterable
from pathlib import Path
from types import ModuleType

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from notebooklm_sync import corpus as _corpus
from notebooklm_sync import corpus_titles as _corpus_titles
from notebooklm_sync import hosting as _hosting
from notebooklm_sync import hosting_paths as _hosting_paths
from notebooklm_sync import import_execution as _execution
from notebooklm_sync import imports as _imports
from notebooklm_sync import lifecycle as _lifecycle
from notebooklm_sync import models as _models
from notebooklm_sync import nlm_client as _nlm_client
from notebooklm_sync import session as _session
from notebooklm_sync import source_adoption as _source_adoption
from notebooklm_sync import source_digests as _source_digests
from notebooklm_sync import workbench as _workbench
from notebooklm_sync.cli import run as _run_cli
from notebooklm_sync.compat_errors import CLI_OPERATION_ERRORS
from notebooklm_sync.compat_imports import ImportFacade
from notebooklm_sync.compat_modules import DashboardModules
from notebooklm_sync.compat_projection import ProjectionFacade
from notebooklm_sync.compat_provider import CompatProvider, ProfileFacade
from notebooklm_sync.compat_sessions import SessionFacade

subprocess = _subprocess

HOSTING_ENV = _hosting_paths.HOSTING_ENV
HOSTING_CONFIG_REL = _hosting_paths.HOSTING_CONFIG_REL
hosting_declaration_path = _hosting_paths.hosting_declaration_path
_content_digest = content_digest = _source_digests.content_digest
_normalized_digest = normalized_digest = _source_digests.normalized_digest

BOOKS = _models.BOOKS
CAP_WARN_HEADROOM = _models.CAP_WARN_HEADROOM
CHARTER = _models.CHARTER
CHARTER_TITLE = _models.CHARTER_TITLE
CHAT_PROMPT = _models.CHAT_PROMPT
EXPORT_RE = _models.EXPORT_RE
GROUNDING = _models.GROUNDING
HOSTING_MIGRATION_SCALARS = _models.HOSTING_MIGRATION_SCALARS
HOSTING_REL = EXAMPLE_REL = _models.HOSTING_REL
HOSTING_SCALARS = _models.HOSTING_SCALARS
HYBRID_CHARTER_TITLE = _models.HYBRID_CHARTER_TITLE
IDEATION_ALIAS_PREFIX = _models.IDEATION_ALIAS_PREFIX
IDEATION_KEY_PREFIX = _models.IDEATION_KEY_PREFIX
README_FLOOR_SEGMENTS = _corpus_titles.README_FLOOR_SEGMENTS
STRAY_TEMP_TITLE_RE = _source_adoption.STRAY_TEMP_TITLE_RE
V1_WORKBENCH_DIR = _workbench.V1_WORKBENCH_DIR
IDEATION_STATUSES = _models.IDEATION_STATUSES
IDEATION_TITLE_PREFIX = _models.IDEATION_TITLE_PREFIX
MANAGED_SOURCE_PREFIXES = _models.MANAGED_SOURCE_PREFIXES
MAX_TEXT_ARG_BYTES = _models.MAX_TEXT_ARG_BYTES
NOTEBOOK_SOURCE_CAP = _models.NOTEBOOK_SOURCE_CAP
SESSION_ALIAS_PREFIX = _models.SESSION_ALIAS_PREFIX
SESSION_CONTAINER_SUFFIX = _models.SESSION_CONTAINER_SUFFIX
SESSION_DEAD = _models.SESSION_DEAD
SESSION_FOREIGN = _models.SESSION_FOREIGN
SESSION_LIVE = _models.SESSION_LIVE
SKIP_PARTS = _models.SKIP_PARTS
SOURCE_ID_ECHO_RE = _models.SOURCE_ID_ECHO_RE
SOURCE_ID_RE = _models.SOURCE_ID_RE
STATIC_BOOKS = _models.STATIC_BOOKS
STATUS_RE = _models.STATUS_RE
BookSpec = _models.BookSpec
ExportPlan = _models.ExportPlan
ExportTarget = _models.ExportTarget
ImportTarget = _models.ImportTarget
OversizedSourceUploadError = _models.OversizedSourceUploadError
SessionNotebookRefused = _models.SessionNotebookRefused
SessionSweepRefused = _models.SessionSweepRefused
SessionSync = _models.SessionSync
SessionTarget = _models.SessionTarget
ideation_spec = _models.ideation_spec
static_spec = _models.static_spec

NLM_CONFIG = _nlm_client.NLM_CONFIG
NotebookRow = _nlm_client.NotebookRow
ProviderResult = _nlm_client.ProviderResult
SourceRow = _nlm_client.SourceRow


_profiles = ProfileFacade(lambda: NLM_CONFIG)
assert_still_bound = _profiles.assert_still_bound


bind_profile = _nlm_client.bind_profile
bound_profile = _nlm_client.bound_profile
clear_profile_cache = _nlm_client.clear_profile_cache


configured_nlm_profile = _profiles.configured_nlm_profile


parse_notebook_rows = _nlm_client.parse_notebook_rows
parse_source_rows = _nlm_client.parse_source_rows
profile_account = _hosting.profile_account
reset_profile_state = _nlm_client.reset_profile_state

in_nested_checkout = _corpus.in_nested_checkout
pinned_factory_paths = _corpus.pinned_factory_paths
derive_stems = _corpus_titles.derive_stems
pinned_root_product_paths = _corpus.pinned_root_product_paths
governed_repo_paths = _corpus.governed_repo_paths
title_segments = _corpus_titles.title_segments
ROOT_LEVEL_GOVERNED_PRODUCTS = _models.ROOT_LEVEL_GOVERNED_PRODUCTS
PROJECTED_STATUSES = _models.PROJECTED_STATUSES


def scan(root: Path) -> tuple[_corpus.DesiredState, dict[str, BookSpec]]:
    return _corpus.scan(root, derive=lambda documents: derive_stems(documents))


read_hosting_declaration = _hosting.read_hosting_declaration
refuse_unusable_declaration = _hosting.refuse_unusable_declaration
append_import = _execution.append_import
display_path = _execution.display_path
imported_file_header = _execution.imported_file_header
render_imported_entry = _execution.render_imported_entry
source_content_text = _execution.source_content_text
export_destination = _imports.export_destination
imported_source_ids = _imports.imported_source_ids
parse_export_title = _imports.parse_export_title
repo_path = _imports.repo_path
session_repository_of = _imports.session_repository_of
slug_part = _imports.slug_part
target_from_path = _imports.target_from_path
ensure_workspace_record = _lifecycle.ensure_workspace_record
notebook_identity = _lifecycle.notebook_identity
classify_session_notebooks = _session.classify_session_notebooks
session_repository_slugs = _session.session_repository_slugs
session_source_count = _session.session_source_count


_provider = CompatProvider(assert_bound=lambda: assert_still_bound())
nlm = _provider.nlm


def _dashboard_module(name: str) -> ModuleType:
    from carved_reach import module as carved_module

    return carved_module(f"scripts/ideation_dashboard/{name}.py")


_dashboard = DashboardModules(
    lambda: _dashboard_module("workbench"),
    lambda: _dashboard_module("session_git"),
    lambda: _dashboard_module("branch_session"),
)


from notebooklm_sync.source_context import SourceContext
from notebooklm_sync.source_readiness import rename_source_when_ready as _rename_ready

RENAME_READY_TIMEOUT_S = 180
RENAME_POLL_INTERVAL_S = 3
RENAME_SETTLE_DELAY_S = 45
ADOPTION_LENGTH_TOLERANCE_BYTES = 4096


def _run_source_text(*args: str) -> str: return nlm(*args, parse=False)


def _source_context() -> SourceContext:
    return SourceContext(
        _run_source_text,
        list_sources,
        lambda seconds: time.sleep(seconds),
        lambda: time.monotonic(),
        RENAME_READY_TIMEOUT_S,
        RENAME_POLL_INTERVAL_S,
        RENAME_SETTLE_DELAY_S,
        ADOPTION_LENGTH_TOLERANCE_BYTES,
    )


def _rename_source_when_ready(handle: str, source_id: str, title: str) -> None: _rename_ready(_source_context(), handle, source_id, title)


_projection = ProjectionFacade(
    run_json=lambda args: nlm(*args),
    run_text=lambda args: nlm(*args, parse=False),
    sleep=lambda seconds: time.sleep(seconds),
    dashboard=_dashboard,
    source_cap=lambda: NOTEBOOK_SOURCE_CAP,
    warn_headroom=lambda: CAP_WARN_HEADROOM,
    max_text_bytes=lambda: MAX_TEXT_ARG_BYTES,
    source_context=_source_context,
)
list_sources = _projection.list_sources
list_notebooks = _projection.list_notebooks
_ensure_alias = _projection.ensure_alias
resolve_or_create_book = _projection.resolve_or_create_book
_add_with_one_retry = _projection.add_with_one_retry
add_text_source = _projection.add_text_source
sync_book = _projection.sync_book
_out_of_scope_workbench_dirs = out_of_scope_workbench_dirs = (
    _projection.out_of_scope_workbench_dirs
)
workbench_orphan_sweep = _projection.workbench_orphan_sweep


def _repositories_hook(root: Path) -> list[tuple[str, Path]]: return session_repositories(root)


def _live_targets_hook(root: Path, branch: str, repository: str | None) -> list[SessionTarget]: return live_session_targets(root, branch, repository)


def _resolve_target_hook(
    root: Path, branch: str, repository: str | None
) -> SessionTarget:
    return resolve_session_target(root, branch, repository)


def _target_for_alias_hook(root: Path, notebook: str) -> SessionTarget | None: return session_target_for_alias(root, notebook)


def _worktree_of_hook(root: Path, path: Path) -> Path | None: return _session_worktree_of(root, path)


def _source_set_hook(target: SessionTarget) -> list[tuple[str, str]]: return session_source_set(target)


def _live_aliases_hook(
    root: Path, repositories: Iterable[tuple[str, Path]] | None
) -> tuple[set[str], list[str]]:
    return live_session_aliases(root, repositories)


_sessions: SessionFacade = SessionFacade(
    dashboard=_dashboard,
    source_cap=lambda: NOTEBOOK_SOURCE_CAP,
    scan=scan,
    list_notebooks=list_notebooks,
    list_sources=list_sources,
    resolve_book=resolve_or_create_book,
    profile_account=lambda profile: profile_account(profile),
    repositories_hook=_repositories_hook,
    live_targets_hook=_live_targets_hook,
    resolve_target_hook=_resolve_target_hook,
    target_for_alias_hook=_target_for_alias_hook,
    worktree_of_hook=_worktree_of_hook,
    source_set_hook=_source_set_hook,
    live_aliases_hook=_live_aliases_hook,
)
session_repositories = _sessions.session_repositories
live_session_targets = _sessions.live_session_targets
resolve_session_target = _sessions.resolve_session_target
session_target_for_alias = _sessions.session_target_for_alias
bind_session_import = _sessions.bind_session_import
_session_worktree_of = _sessions.session_worktree_of


def session_source_set(target: SessionTarget) -> list[tuple[str, str]]:
    import opendox_host

    opendox_host.register_openxfactory()
    return _sessions.session_source_set(target)


sync_session_notebook = _sessions.sync_session_notebook
live_session_aliases = _sessions.live_session_aliases
session_notebook_sweep = _sessions.session_notebook_sweep
active_nlm_profile = _sessions.active_nlm_profile
enforce_hosting_profile = _sessions.enforce_hosting_profile
parity_report = _sessions.parity_report

_importer = ImportFacade(
    list_sources=list_sources,
    run_text=lambda args: nlm(*args, parse=False),
    dashboard=_dashboard,
    bind_session=bind_session_import,
)
export_plan = _importer.export_plan
is_seed_source = _importer.is_seed_source
new_source_plan = _importer.new_source_plan
import_exported_sources = _importer.import_exported_sources
import_new_sources = _importer.import_new_sources
commit_session_import = _importer.commit_session_import


def main() -> None:
    _run_cli(
        enforce_profile=enforce_hosting_profile,
        parity_report=parity_report,
        sweep_sessions=session_notebook_sweep,
        sync_session=sync_session_notebook,
        import_exports=import_exported_sources,
        import_new=import_new_sources,
        scan=scan,
        list_notebooks=list_notebooks,
        sync_book=sync_book,
        sweep_workbench=workbench_orphan_sweep,
        operation_errors=CLI_OPERATION_ERRORS,
    )


if __name__ == "__main__":
    main()

HOSTING_EXAMPLE_MARKER = "example"

STEM_SCOPE_EXCLUDES = ("[spec]", "[grounding]")


# Public callable names for the extracted test contract.
rename_source_when_ready = _rename_source_when_ready
