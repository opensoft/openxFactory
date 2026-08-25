#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import time
from importlib import import_module
from pathlib import Path
from types import ModuleType
from typing import Literal, overload

from notebooklm_sync import corpus as _corpus
from notebooklm_sync import hosting as _hosting
from notebooklm_sync import import_execution as _execution
from notebooklm_sync import imports as _imports
from notebooklm_sync import lifecycle as _lifecycle
from notebooklm_sync import models as _models
from notebooklm_sync import nlm_client as _nlm_client
from notebooklm_sync import session as _session
from notebooklm_sync.cli import run as _run_cli
from notebooklm_sync.compat_imports import ImportFacade
from notebooklm_sync.compat_projection import ProjectionFacade
from notebooklm_sync.compat_sessions import SessionFacade

BOOKS = _models.BOOKS
CAP_WARN_HEADROOM = _models.CAP_WARN_HEADROOM
CHARTER = _models.CHARTER
CHARTER_TITLE = _models.CHARTER_TITLE
CHAT_PROMPT = _models.CHAT_PROMPT
EXPORT_RE = _models.EXPORT_RE
GROUNDING = _models.GROUNDING
HOSTING_MIGRATION_SCALARS = _models.HOSTING_MIGRATION_SCALARS
HOSTING_REL = _models.HOSTING_REL
HOSTING_SCALARS = _models.HOSTING_SCALARS
HYBRID_CHARTER_TITLE = _models.HYBRID_CHARTER_TITLE
IDEATION_ALIAS_PREFIX = _models.IDEATION_ALIAS_PREFIX
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
assert_still_bound = _nlm_client.assert_still_bound
bind_profile = _nlm_client.bind_profile
bound_profile = _nlm_client.bound_profile
clear_profile_cache = _nlm_client.clear_profile_cache
configured_nlm_profile = _nlm_client.configured_nlm_profile
parse_notebook_rows = _nlm_client.parse_notebook_rows
parse_source_rows = _nlm_client.parse_source_rows
profile_account = _hosting.profile_account
reset_profile_state = _nlm_client.reset_profile_state

in_nested_checkout = _corpus.in_nested_checkout
pinned_factory_paths = _corpus.pinned_factory_paths
scan = _corpus.scan
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


@overload
def nlm(*args: str, parse: Literal[False]) -> str: ...


@overload
def nlm(*args: str, parse: Literal[True] = True) -> ProviderResult: ...


def nlm(*args: str, parse: bool = True) -> ProviderResult:
    provider = _nlm_client.NlmCliProvider()
    return provider.invoke(*args, parse=parse)


def _dashboard_module(name: str) -> ModuleType:
    scripts_dir = Path(__file__).resolve().parent
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    return import_module(f"ideation_dashboard.{name}")


_projection = ProjectionFacade(
    run_json=lambda args: nlm(*args),
    run_text=lambda args: nlm(*args, parse=False),
    sleep=lambda seconds: time.sleep(seconds),
    dashboard=_dashboard_module,
    source_cap=lambda: NOTEBOOK_SOURCE_CAP,
    warn_headroom=lambda: CAP_WARN_HEADROOM,
    max_text_bytes=lambda: MAX_TEXT_ARG_BYTES,
)
list_sources = _projection.list_sources
list_notebooks = _projection.list_notebooks
_ensure_alias = _projection.ensure_alias
resolve_or_create_book = _projection.resolve_or_create_book
_add_with_one_retry = _projection.add_with_one_retry
add_text_source = _projection.add_text_source
sync_book = _projection.sync_book
_out_of_scope_workbench_dirs = _projection.out_of_scope_workbench_dirs
workbench_orphan_sweep = _projection.workbench_orphan_sweep

_sessions = SessionFacade(
    dashboard=_dashboard_module,
    source_cap=lambda: NOTEBOOK_SOURCE_CAP,
    scan=scan,
    list_notebooks=list_notebooks,
    list_sources=list_sources,
    resolve_book=resolve_or_create_book,
    profile_account=lambda profile: profile_account(profile),
    repositories_hook=lambda root: session_repositories(root),
    live_targets_hook=lambda root, branch, repository: live_session_targets(
        root, branch, repository
    ),
    resolve_target_hook=lambda root, branch, repository: resolve_session_target(
        root, branch, repository
    ),
    target_for_alias_hook=lambda root, notebook: session_target_for_alias(
        root, notebook
    ),
    worktree_of_hook=lambda root, path: _session_worktree_of(root, path),
    source_set_hook=lambda target: session_source_set(target),
    live_aliases_hook=lambda root, repositories: live_session_aliases(
        root, repositories
    ),
)
session_repositories = _sessions.session_repositories
live_session_targets = _sessions.live_session_targets
resolve_session_target = _sessions.resolve_session_target
session_target_for_alias = _sessions.session_target_for_alias
bind_session_import = _sessions.bind_session_import
_session_worktree_of = _sessions.session_worktree_of
session_source_set = _sessions.session_source_set
sync_session_notebook = _sessions.sync_session_notebook
live_session_aliases = _sessions.live_session_aliases
session_notebook_sweep = _sessions.session_notebook_sweep
active_nlm_profile = _sessions.active_nlm_profile
enforce_hosting_profile = _sessions.enforce_hosting_profile
parity_report = _sessions.parity_report

_importer = ImportFacade(
    list_sources=list_sources,
    run_text=lambda args: nlm(*args, parse=False),
    dashboard=_dashboard_module,
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
        operation_errors=(
            OSError,
            RuntimeError,
            ValueError,
            TypeError,
            KeyError,
            subprocess.SubprocessError,
        ),
    )


if __name__ == "__main__":
    main()
