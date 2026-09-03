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
import importlib.util
import io
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "sync-notebooklm-books.py"
MODULE = "sync_notebooklm_books"

# Share the module with `test_sync_notebooklm_books.py` when that file loaded it
# first: the script is a hyphenated path, so it must be loaded by location, and
# executing it twice under one name would leave two module objects whose
# `patch.object` targets differ.
if MODULE in sys.modules:
    sync = sys.modules[MODULE]
else:
    _spec = importlib.util.spec_from_file_location(MODULE, SCRIPT)
    sync = importlib.util.module_from_spec(_spec)
    assert _spec.loader is not None
    sys.modules[MODULE] = sync
    _spec.loader.exec_module(sync)


REGISTRY = "openxFactory/examples/lifecycle-notebook-workspaces.yaml"

LEGACY_ID = "b83e63e3-262a-4dfe-9b9f-332b3d27d1bb"
NEW_ID = "991f0af7-2077-4c26-ac1d-d92e2af9f99c"
OTHER_ID = "2c2ba7ae-65e1-436a-ba4c-0a5f8f2a99bb"

# Shaped like the real registry: the header comments that carry the migration
# record (one line of which is cited verbatim elsewhere and therefore frozen),
# a RETIRED record kept as a commented block, and two live records whose ids
# share a prefix — `…-ideation` is a prefix of `…-ideation-opsxfactory`.
REGISTRY_TEXT = """\
# Workspace records for the lifecycle notebook projection.
# Model: docs/notebooklm-source-workspaces.md section 6.
workspaces:
# HOSTING MIGRATION 2026-08-24 — frozen wording, cited by the step-8 runbook.
#   - kind: external_source_workspace
#     schema_version: 1
#     id: workspace-xfactory-lifecycle-ideation
#     provider: notebooklm
#     provider_notebook_id: 27b1880b-6974-4cfe-a76f-4318f6021608
  - kind: external_source_workspace
    schema_version: 1
    id: workspace-xfactory-lifecycle-drafts
    provider: notebooklm
    provider_notebook_id: {legacy}
    owner_layer: domain_hermes
    scope:
      domain_id: xfactory
      client_id: null
      customer_id: null
    purpose: derived projection of draft governance docs
    default_authority_level: L1_notebook_synthesis
    created_at: "2026-07-08T20:00:00Z"
    managed_by: openxFactory/scripts/sync-notebooklm-books.py
  - kind: external_source_workspace
    schema_version: 1
    id: workspace-xfactory-lifecycle-ideation-opsxfactory
    provider: notebooklm
    provider_notebook_id: {other}
    owner_layer: domain_hermes
    scope:
      domain_id: xfactory
      client_id: null
      customer_id: null
    purpose: derived projection of brainstorm and staged governance docs (OpsxFactory)
    default_authority_level: L1_notebook_synthesis
    created_at: "2026-08-10T07:13:30Z"
    managed_by: openxFactory/scripts/sync-notebooklm-books.py
""".format(legacy=LEGACY_ID, other=OTHER_ID)


def _write_registry(root: Path, text: str = REGISTRY_TEXT) -> Path:
    path = root / REGISTRY
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _run(root: Path, spec, notebook_id: str, apply: bool) -> str:
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        sync.ensure_workspace_record(root, spec, notebook_id, apply)
    return out.getvalue()


def _records(text: str) -> list[dict[str, str]]:
    """Every ACTIVE record in the registry, as id -> provider id pairs.

    Deliberately a plain reader rather than a YAML load: the assertions below
    are about what is written in the file, comments and all.
    """
    records: list[dict[str, str]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#") or ":" not in stripped:
            continue
        key, _, value = stripped.partition(":")
        key = key.removeprefix("- ").strip()
        if key == "kind":
            records.append({})
        elif key in {"id", "provider_notebook_id"} and records:
            records[-1][key] = value.strip()
    return records


class WorkspaceRecordReplacementTests(unittest.TestCase):
    """The replace path: the record is RE-POINTED, never duplicated."""

    DRAFTS = sync.static_spec("drafts")

    def test_a_plan_run_prints_the_replacement_and_writes_nothing(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            path = _write_registry(root)
            before = path.read_text(encoding="utf-8")
            text = _run(root, self.DRAFTS, NEW_ID, apply=False)
            after = path.read_text(encoding="utf-8")
        self.assertEqual(before, after,
                         "a plan run that re-points the registry is not a plan")
        self.assertIn("REPLACE", text)
        # BOTH ids are named: an operator has to be able to see that the id
        # being bound is the one they meant, which is the whole reason the
        # re-point is not silent.
        self.assertIn(LEGACY_ID, text)
        self.assertIn(NEW_ID, text)
        self.assertIn("workspace-xfactory-lifecycle-drafts", text)
        # doc-health counts `[book] ADD|DEL|UPD` lines as PENDING projection
        # operations (scripts/doc_health/families.py); the replacement verb
        # must not be mistaken for one.
        for verb in (" ADD ", " DEL ", " UPD "):
            self.assertNotIn(verb, text)

    def test_apply_leaves_exactly_one_active_record_holding_the_new_id(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            path = _write_registry(root)
            text = _run(root, self.DRAFTS, NEW_ID, apply=True)
            written = path.read_text(encoding="utf-8")
        records = _records(written)
        drafts = [r for r in records
                  if r.get("id") == "workspace-xfactory-lifecycle-drafts"]
        self.assertEqual(len(drafts), 1,
                         "exactly one active record per live book: a "
                         "replacement appends nothing")
        self.assertEqual(drafts[0]["provider_notebook_id"], NEW_ID)
        self.assertNotIn(LEGACY_ID, written,
                         "the legacy provider notebook is what gets retired; "
                         "the record must not keep pointing at it")
        self.assertIn("REPLACED", text)
        self.assertIn(LEGACY_ID, text)
        self.assertIn(NEW_ID, text)

    def test_every_other_field_and_every_comment_survives_the_replacement(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            path = _write_registry(root)
            before = path.read_text(encoding="utf-8").splitlines()
            _run(root, self.DRAFTS, NEW_ID, apply=True)
            after = path.read_text(encoding="utf-8").splitlines()
        changed = [(b, a) for b, a in zip(before, after) if b != a]
        self.assertEqual(len(before), len(after),
                         "the replacement rewrites one line in place")
        self.assertEqual(
            changed, [(f"    provider_notebook_id: {LEGACY_ID}",
                       f"    provider_notebook_id: {NEW_ID}")],
            "only provider_notebook_id moves — created_at and the rest are the "
            "record's own history, and the header comments carry the migration "
            "record")

    def test_a_record_with_a_different_key_is_untouched(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            path = _write_registry(root)
            _run(root, self.DRAFTS, NEW_ID, apply=True)
            written = path.read_text(encoding="utf-8")
        opsx = [r for r in _records(written)
                if r.get("id") == "workspace-xfactory-lifecycle-ideation-opsxfactory"]
        self.assertEqual(len(opsx), 1)
        self.assertEqual(opsx[0]["provider_notebook_id"], OTHER_ID,
                         "another book's registration is not this book's to move")

    def test_a_prefix_id_does_not_reach_the_longer_record(self):
        """`…-ideation` must not rewrite `…-ideation-opsxfactory`.

        The retired shared Ideation book's id is a strict prefix of every
        per-repo one, and it survives in the registry as a commented block. A
        substring test finds both; a whole-line test finds neither, which is
        the correct answer — there is no ACTIVE record under that id.
        """
        with TemporaryDirectory() as td:
            root = Path(td)
            path = _write_registry(root)
            retired = sync.BookSpec(key="ideation", alias="xf-ideation",
                                    title="xFactory — Ideation")
            text = _run(root, retired, NEW_ID, apply=True)
            written = path.read_text(encoding="utf-8")
        opsx = [r for r in _records(written)
                if r.get("id") == "workspace-xfactory-lifecycle-ideation-opsxfactory"]
        self.assertEqual(opsx[0]["provider_notebook_id"], OTHER_ID)
        # the commented retired block stays exactly as it was
        self.assertIn("#     provider_notebook_id: "
                      "27b1880b-6974-4cfe-a76f-4318f6021608", written)
        self.assertIn("workspace record workspace-xfactory-lifecycle-ideation ->",
                      text, "no active record under that id: it is REGISTERED, "
                            "not treated as a replacement")


class WorkspaceRecordNoOpTests(unittest.TestCase):
    """The paths that must stay exactly as they were."""

    DRAFTS = sync.static_spec("drafts")

    def test_the_same_id_already_registered_is_a_silent_no_op(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            path = _write_registry(root)
            before = path.read_text(encoding="utf-8")
            plan = _run(root, self.DRAFTS, LEGACY_ID, apply=False)
            applied = _run(root, self.DRAFTS, LEGACY_ID, apply=True)
            after = path.read_text(encoding="utf-8")
        self.assertEqual(before, after)
        self.assertEqual(plan, "")
        self.assertEqual(applied, "",
                         "a book already registered under the id it has is not "
                         "an operation and must not read as one")

    def test_a_missing_registry_is_a_notice_and_not_a_crash(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            text = _run(root, self.DRAFTS, NEW_ID, apply=True)
            self.assertFalse((root / REGISTRY).exists(),
                             "a missing registry is reported, never conjured")
        self.assertIn("NOTICE", text)
        self.assertIn("workspace registry missing", text)

    def test_a_record_without_a_provider_id_line_stays_hand_reconciled(self):
        """The one case that genuinely cannot be replaced.

        Appending a second record would break the one-record invariant, so the
        function reports instead of guessing.
        """
        malformed = (
            "workspaces:\n"
            "  - kind: external_source_workspace\n"
            "    schema_version: 1\n"
            "    id: workspace-xfactory-lifecycle-drafts\n"
            "    provider: notebooklm\n"
        )
        with TemporaryDirectory() as td:
            root = Path(td)
            path = _write_registry(root, malformed)
            text = _run(root, self.DRAFTS, NEW_ID, apply=True)
            after = path.read_text(encoding="utf-8")
        self.assertEqual(after, malformed)
        self.assertIn("reconcile by hand", text)

    def test_an_unregistered_book_is_registered_and_planned_first(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            path = _write_registry(root, "workspaces:\n")
            plan = _run(root, self.DRAFTS, NEW_ID, apply=False)
            self.assertEqual(path.read_text(encoding="utf-8"), "workspaces:\n")
            _run(root, self.DRAFTS, NEW_ID, apply=True)
            written = path.read_text(encoding="utf-8")
        self.assertIn("REGISTER", plan)
        self.assertIn(NEW_ID, plan)
        records = _records(written)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["id"], "workspace-xfactory-lifecycle-drafts")
        self.assertEqual(records[0]["provider_notebook_id"], NEW_ID)


class ResolvedBooksReassertTheirRegistrationTests(unittest.TestCase):
    """The FOUND path re-asserts too, which is where a migration lands.

    A hosting move re-derives the books; the run that CREATES them writes the
    replacement, but every run after that merely RESOLVES them by title. If the
    found path did not check, a registry left stale by a partial or skipped
    migration would never converge — the failure the issue was filed to prevent.
    """

    DRAFTS = sync.static_spec("drafts")

    def _resolve(self, root: Path, apply: bool, notebooks=None) -> str:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            nid, ok = sync.resolve_or_create_book(
                root, self.DRAFTS, apply,
                notebooks if notebooks is not None
                else [{"id": NEW_ID, "title": self.DRAFTS.title}],
                bind_alias=False)
        self.assertTrue(ok)
        return out.getvalue()

    def test_two_notebooks_under_one_title_leave_the_record_alone(self):
        """An arbitrary resolution must not become a governed write.

        `by_title` keeps whichever row the provider returned LAST, so a
        duplicate title resolves to an arbitrary notebook. Projecting into one
        is a pre-existing hazard; re-pointing the record at it would overwrite
        an already-correct registration and flap it as ordering changes.
        """
        with TemporaryDirectory() as td:
            root = Path(td)
            path = _write_registry(root)
            before = path.read_text(encoding="utf-8")
            text = self._resolve(
                root, apply=True,
                notebooks=[{"id": NEW_ID, "title": self.DRAFTS.title},
                           {"id": OTHER_ID, "title": self.DRAFTS.title}])
            after = path.read_text(encoding="utf-8")
        self.assertEqual(before, after,
                         "an ambiguous title is what hand reconciliation is for")
        self.assertIn("NOTICE", text)
        self.assertIn(NEW_ID, text)
        self.assertIn(OTHER_ID, text)
        self.assertNotIn("REPLACED", text)

    def test_a_read_only_resolve_plans_the_replacement_without_writing(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            path = _write_registry(root)
            before = path.read_text(encoding="utf-8")
            text = self._resolve(root, apply=False)
            after = path.read_text(encoding="utf-8")
        self.assertEqual(before, after,
                         "--parity resolves with apply=False: a proof that "
                         "changes the thing it measures is not a proof")
        self.assertIn("REPLACE", text)

    def test_an_apply_resolve_re_points_the_stale_record(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            path = _write_registry(root)
            self._resolve(root, apply=True)
            written = path.read_text(encoding="utf-8")
        drafts = [r for r in _records(written)
                  if r.get("id") == "workspace-xfactory-lifecycle-drafts"]
        self.assertEqual(len(drafts), 1)
        self.assertEqual(drafts[0]["provider_notebook_id"], NEW_ID)


if __name__ == "__main__":                          # pragma: no cover - manual use
    unittest.main()
