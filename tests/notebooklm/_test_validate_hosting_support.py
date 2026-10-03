"""The hosting-declaration and share-out-roster validator.

Covers the refusals the ratified requirements name: the two-case vocabulary,
the Workspace-user rule for the operator-hosted case, the platform constraint
that no service account can host a projection, the pending-migration fields the
sync binds to, and — the one the whole Q3 disposition rests on — that roster
uniqueness is the stable (hosting_account, user, book_or_alias) triple, so a
re-decision updates one live entry instead of asserting a stale grant beside a
current one.
"""

from __future__ import annotations

import functools
from collections.abc import Callable
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Protocol, runtime_checkable

from tests.notebooklm._sync_test_support import TestSupportError, load_script_module
from tests.notebooklm.typed_sync_contracts import TypedSyncModule, load_typed_sync

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "validate-notebook-projection-hosting.py"


@runtime_checkable
class HostingValidator(Protocol):
    is_example: Callable[[Path], bool]
    DEFAULT_REL: str
    ENTRY_FIELDS: tuple[str, ...]

    def main(self, arguments: list[str] | None = None) -> int: ...

    HOSTING_ENV: str
    HOSTING_CONFIG_REL: str
    HOSTING_EXAMPLE_MARKER: str

    def validate(self, path: Path) -> list[str]: ...
    def hosting_declaration_path(self, root: Path) -> Path | None: ...


module = load_script_module("validate_hosting", SCRIPT)
if not isinstance(module, HostingValidator):
    raise TestSupportError("hosting validator lacks its test contract")
validator = module


@functools.cache
def sync_module() -> TypedSyncModule:
    return load_typed_sync()


BASE = 'schema_version: 1\nkind: notebook_projection_hosting\nhosting:\n  case: operator_hosted\n  account: projection-host@example.invalid\n  account_type: google_workspace_user\n  domain: example.invalid\n  nlm_profile: company\n  custody:\n    binding_kind: xfactory_credential_binding_template\n    binding_client: opensoft\n    binding_id: notebook_projection_hosting\n    covers:\n      - account_password\n      - totp_seed\n    interactive_step_remains: true\n    interactive_step: Google sign-in is an interactive browser flow.\n    session_state_in_custody: false\n# The approval designation is part of a CONFORMING operator-hosted record since\n# task 2.4 (review, PR #414): an operated account with no named decider is the\n# failure the ratified requirement forbids. In the base fixture for the same\n# reason custody is — every other test here asserts against "an otherwise\n# conforming record".\napproval:\n  designated_actor: Brett Heap\n  acts_in: the hosting account\'s own NotebookLM interface\n  automated_approval: false\nshare_out: []\n'
NO_CUSTODY = BASE[: BASE.index("  custody:")] + BASE[BASE.index("share_out: []") :]


def validate_text(text: str) -> list[str]:
    with TemporaryDirectory() as td:
        path = Path(td) / "notebook-projection-hosting.yaml"
        _ = path.write_text(text, encoding="utf-8")
        return validator.validate(path)


APPROVAL = "approval:\n  designated_actor: Brett Heap\n  acts_in: the hosting account's own NotebookLM interface\n  automated_approval: false\n"

is_example = validator.is_example
