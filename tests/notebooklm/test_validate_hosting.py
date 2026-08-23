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

import importlib.util
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "validate-notebook-projection-hosting.py"

spec = importlib.util.spec_from_file_location("validate_hosting", SCRIPT)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = validator
spec.loader.exec_module(validator)

BASE = """schema_version: 1
kind: notebook_projection_hosting
hosting:
  case: operator_hosted
  account: xFactor001@opensoft.one
  account_type: google_workspace_user
  domain: opensoft.one
  nlm_profile: company
share_out: []
"""


def _validate(text: str) -> list[str]:
    with TemporaryDirectory() as td:
        path = Path(td) / "notebook-projection-hosting.yaml"
        path.write_text(text, encoding="utf-8")
        return validator.validate(path)


class HostingDeclarationValidationTests(unittest.TestCase):

    def test_the_committed_record_conforms(self):
        errors = validator.validate(REPO_ROOT / validator.DEFAULT_REL)
        self.assertEqual(errors, [], "this install's own declaration must pass")

    def test_a_conforming_declaration_passes(self):
        self.assertEqual(_validate(BASE), [])

    def test_a_third_case_is_refused(self):
        errors = _validate(BASE.replace("case: operator_hosted",
                                        "case: partly_hosted"))
        self.assertTrue(any("hosting.case" in e for e in errors))

    def test_a_self_hosted_personal_declaration_is_legitimate(self):
        text = """schema_version: 1
kind: notebook_projection_hosting
hosting:
  case: self_hosted
  account: someone@gmail.com
  nlm_profile: personal
share_out: []
"""
        self.assertEqual(_validate(text), [],
                         "an individual's own account is a complete binding, "
                         "not a degraded operator-hosted one")

    def test_a_service_account_cannot_host_a_projection(self):
        errors = _validate(BASE.replace(
            "account: xFactor001@opensoft.one",
            "account: books@xf-proj.iam.gserviceaccount.com").replace(
            "domain: opensoft.one", "domain: xf-proj.iam.gserviceaccount.com"))
        self.assertTrue(any("service account" in e for e in errors),
                        "NotebookLM has no API and a service account cannot "
                        "drive its consumer web UI")

    def test_operator_hosted_refuses_a_consumer_account(self):
        errors = _validate(BASE.replace(
            "account_type: google_workspace_user",
            "account_type: consumer_google_account"))
        self.assertTrue(any("account_type" in e for e in errors))

    def test_the_account_must_live_in_the_declared_domain(self):
        errors = _validate(BASE.replace("domain: opensoft.one",
                                        "domain: elsewhere.example"))
        self.assertTrue(any("not in the declared domain" in e for e in errors))

    def test_a_declaration_without_a_profile_cannot_bind(self):
        errors = _validate(BASE.replace("  nlm_profile: company\n", ""))
        self.assertTrue(any("nlm_profile" in e for e in errors))

    def test_a_pending_migration_names_where_the_books_still_live(self):
        errors = _validate(BASE.replace("share_out: []", """  migration:
    state: pending
share_out: []"""))
        self.assertTrue(any("from_account" in e for e in errors))
        self.assertTrue(any("from_nlm_profile" in e for e in errors))


class ShareOutRosterValidationTests(unittest.TestCase):

    ENTRY = """share_out:
  - hosting_account: xFactor001@opensoft.one
    user: reader@example.com
    book_or_alias: xf-canon
    role: viewer
    granted_at: "2026-08-24"
    granted_by: Brett Heap
"""

    def _with_roster(self, roster: str) -> list[str]:
        return _validate(BASE.replace("share_out: []", roster))

    def test_a_complete_entry_passes(self):
        self.assertEqual(self._with_roster(self.ENTRY), [])

    FIELDS = {
        "hosting_account": "xFactor001@opensoft.one",
        "user": "reader@example.com",
        "book_or_alias": "xf-canon",
        "role": "viewer",
        "granted_at": '"2026-08-24"',
        "granted_by": "Brett Heap",
    }

    @classmethod
    def _roster_without(cls, dropped: str) -> str:
        """One entry carrying every field but `dropped`, built structurally so
        the list marker survives — stripping the first line by text would
        remove the `-` and change the shape instead of the field."""
        kept = [(k, v) for k, v in cls.FIELDS.items() if k != dropped]
        lines = [f"  - {kept[0][0]}: {kept[0][1]}"]
        lines += [f"    {k}: {v}" for k, v in kept[1:]]
        return "share_out:\n" + "\n".join(lines) + "\n"

    def test_every_one_of_the_six_fields_is_required(self):
        for field in validator.ENTRY_FIELDS:
            with self.subTest(field=field):
                errors = self._with_roster(self._roster_without(field))
                self.assertTrue(any(field in e for e in errors),
                                f"{field} must be required")

    def test_two_people_on_one_book_are_distinct_entries(self):
        roster = self.ENTRY + """  - hosting_account: xFactor001@opensoft.one
    user: second@example.com
    book_or_alias: xf-canon
    role: viewer
    granted_at: "2026-08-24"
    granted_by: Brett Heap
"""
        self.assertEqual(self._with_roster(roster), [],
                         "the grantee is part of the key — this is the case "
                         "that broke the client-identity roster")

    def test_a_re_decision_must_update_rather_than_add_a_second_entry(self):
        roster = self.ENTRY + """  - hosting_account: xFactor001@opensoft.one
    user: reader@example.com
    book_or_alias: xf-canon
    role: editor
    granted_at: "2026-08-25"
    granted_by: Someone Else
"""
        errors = self._with_roster(roster)
        self.assertTrue(any("duplicate share-out key" in e for e in errors),
                        "role, grant time and actor are ATTRIBUTES: two live "
                        "entries would assert a stale grant beside a current "
                        "one")

    def test_an_entry_for_another_hosting_account_is_refused(self):
        roster = self.ENTRY.replace("hosting_account: xFactor001@opensoft.one",
                                    "hosting_account: someone@gmail.com")
        errors = self._with_roster(roster)
        self.assertTrue(any("declared hosting account" in e for e in errors))

    def test_an_unknown_role_is_refused(self):
        errors = self._with_roster(self.ENTRY.replace("role: viewer",
                                                      "role: owner"))
        self.assertTrue(any("role" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
