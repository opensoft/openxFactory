"""`ensure_workspace_record()` — the workspace-record REPLACEMENT (issue #536).

The invariant under test is `lifecycle-notebook-projection`'s: **exactly one
active record per live book**. A hosting-account migration re-derives a book
under a NEW provider notebook id while the record id — derived from the book's
KEY — is unchanged, so the record IS still the live book's registration and what
gets retired is the legacy PROVIDER NOTEBOOK. Before this, the function found
its own record holding a different id, printed `reconcile by hand` and returned;
retiring the legacy record on top of that left the company-hosted book with no
registration at all. The 2026-08-24 migration performed the replacement by hand
(`docs/notebook-projection-migration-evidence-2026-08-24.md`, step 6).

Nothing here touches a notebook: these tests drive the registry FILE only, in a
temporary directory, and the suite-wide hermeticity guard (`tests/hermeticity.py`)
makes the real `nlm` unreachable regardless.
"""

from __future__ import annotations

import contextlib
import io
from pathlib import Path

from notebooklm_sync.models import BookSpec

from tests.notebooklm.typed_sync_contracts import load_typed_sync

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "sync-notebooklm-books.py"
MODULE = "sync_notebooklm_books"
sync = load_typed_sync()
REGISTRY = "openxFactory/examples/lifecycle-notebook-workspaces.yaml"
LEGACY_ID = "b83e63e3-262a-4dfe-9b9f-332b3d27d1bb"
NEW_ID = "991f0af7-2077-4c26-ac1d-d92e2af9f99c"
OTHER_ID = "2c2ba7ae-65e1-436a-ba4c-0a5f8f2a99bb"
REGISTRY_TEXT = f'# Workspace active_records for the lifecycle notebook projection.\n# Model: docs/notebooklm-source-workspaces.md section 6.\nworkspaces:\n# HOSTING MIGRATION 2026-08-24 — frozen wording, cited by the step-8 runbook.\n#   - kind: external_source_workspace\n#     schema_version: 1\n#     id: workspace-xfactory-lifecycle-ideation\n#     provider: notebooklm\n#     provider_notebook_id: 27b1880b-6974-4cfe-a76f-4318f6021608\n  - kind: external_source_workspace\n    schema_version: 1\n    id: workspace-xfactory-lifecycle-drafts\n    provider: notebooklm\n    provider_notebook_id: {LEGACY_ID}\n    owner_layer: domain_hermes\n    scope:\n      domain_id: xfactory\n      client_id: null\n      customer_id: null\n    purpose: derived projection of draft governance docs\n    default_authority_level: L1_notebook_synthesis\n    created_at: "2026-07-08T20:00:00Z"\n    managed_by: openxFactory/scripts/sync-notebooklm-books.py\n  - kind: external_source_workspace\n    schema_version: 1\n    id: workspace-xfactory-lifecycle-ideation-opsxfactory\n    provider: notebooklm\n    provider_notebook_id: {OTHER_ID}\n    owner_layer: domain_hermes\n    scope:\n      domain_id: xfactory\n      client_id: null\n      customer_id: null\n    purpose: derived projection of brainstorm and staged governance docs (OpsxFactory)\n    default_authority_level: L1_notebook_synthesis\n    created_at: "2026-08-10T07:13:30Z"\n    managed_by: openxFactory/scripts/sync-notebooklm-books.py\n'


def write_registry(root: Path, text: str = REGISTRY_TEXT) -> Path:
    path = root / REGISTRY
    path.parent.mkdir(parents=True, exist_ok=True)
    _ = path.write_text(text, encoding="utf-8")
    return path


def run_record(root: Path, spec: BookSpec, notebook_id: str, apply: bool) -> str:
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        sync.ensure_workspace_record(root, spec, notebook_id, apply)
    return out.getvalue()


def active_records(text: str) -> list[dict[str, str]]:
    """Every ACTIVE record in the registry, as id -> provider id pairs.

    Deliberately a plain reader rather than a YAML load: the assertions below
    are about what is written in the file, comments and all.
    """
    active_records: list[dict[str, str]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#") or ":" not in stripped:
            continue
        key, _, value = stripped.partition(":")
        key = key.removeprefix("- ").strip()
        if key == "kind":
            active_records.append({})
        elif key in {"id", "provider_notebook_id"} and active_records:
            active_records[-1][key] = value.strip()
    return active_records
