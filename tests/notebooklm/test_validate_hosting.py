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

# The custody block is part of a CONFORMING operator-hosted declaration since
# add-notebook-hosting-credential-custody: an operated identity with no declared
# custody is not governed, it is merely undocumented. It is in the base fixture
# rather than bolted onto the custody tests alone, because every other test here
# asserts against "an otherwise conforming record" and would otherwise be
# asserting against a non-conforming one.
BASE = """schema_version: 1
kind: notebook_projection_hosting
hosting:
  case: operator_hosted
  account: xFactor001@opensoft.one
  account_type: google_workspace_user
  domain: opensoft.one
  nlm_profile: company
  custody:
    binding_kind: xfactory_credential_binding_template
    binding_client: opensoft
    binding_id: notebook_projection_hosting
    covers:
      - account_password
      - totp_seed
    interactive_step_remains: true
    interactive_step: Google sign-in is an interactive browser flow.
    session_state_in_custody: false
share_out: []
"""

#: The same record with the custody block removed — the shape an install had
#: before this requirement, used to prove the refusal actually fires.
NO_CUSTODY = BASE[:BASE.index("  custody:")] + BASE[BASE.index("share_out: []"):]


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


class CustodyValidationTests(unittest.TestCase):
    """add-notebook-hosting-credential-custody § 2 — custody BY REFERENCE ONLY.

    Two obligations, and they are asymmetric on purpose: the operator-hosted
    case must NAME its binding, while NEITHER case may carry secret material.
    """

    def test_a_conforming_custody_reference_passes(self):
        self.assertEqual(_validate(BASE), [])

    def test_an_operator_hosted_record_without_custody_is_refused(self):
        errors = _validate(NO_CUSTODY)
        self.assertTrue(any("hosting.custody" in e for e in errors), errors)
        joined = " ".join(errors)
        self.assertIn("undocumented rather than governed", joined)

    def test_a_self_hosted_record_needs_no_custody(self):
        """The two-case model: no operator, no obligation."""
        text = NO_CUSTODY.replace("case: operator_hosted", "case: self_hosted")
        errors = [e for e in _validate(text) if "custody" in e]
        self.assertEqual(errors, [], "self-hosted must not be asked for custody")

    def test_a_partial_binding_reference_is_refused(self):
        """All three fields, or the reference cannot be resolved at all."""
        for field in ("binding_kind", "binding_client", "binding_id"):
            with self.subTest(missing=field):
                text = "\n".join(
                    line for line in BASE.splitlines()
                    if not line.strip().startswith(field + ":"))
                errors = _validate(text)
                self.assertTrue(any(field in e for e in errors), errors)

    def test_covers_must_name_the_secrets(self):
        text = BASE.replace("    covers:\n      - account_password\n"
                            "      - totp_seed\n", "    covers: []\n")
        errors = _validate(text)
        self.assertTrue(any("covers" in e for e in errors), errors)
        self.assertIn("single point of failure", " ".join(errors))

    def test_an_interactive_step_must_be_named_when_declared(self):
        text = BASE.replace(
            "    interactive_step: Google sign-in is an interactive browser flow.\n",
            "")
        errors = _validate(text)
        self.assertTrue(any("interactive_step" in e for e in errors), errors)

    def test_silence_about_the_interactive_step_is_refused(self):
        """Silence reads as 'unattended' to an operator planning automation."""
        text = BASE.replace("    interactive_step_remains: true\n", "")
        errors = _validate(text)
        self.assertTrue(
            any("interactive_step_remains" in e for e in errors), errors)


class SecretMaterialRefusalTests(unittest.TestCase):
    """Nothing secret-shaped, in EITHER case, anywhere in the record."""

    SECRET_FIELDS = ("password", "totp_seed", "recovery_code", "cookie",
                     "session", "profile", "private_key", "api_key")

    def test_each_secret_shaped_field_is_refused(self):
        for field in self.SECRET_FIELDS:
            with self.subTest(field=field):
                text = BASE.replace(
                    "  nlm_profile: company\n",
                    f"  nlm_profile: company\n  {field}: some-value\n")
                errors = _validate(text)
                self.assertTrue(any(field in e for e in errors), (field, errors))

    def test_the_refusal_names_the_binding_not_redaction(self):
        """A redacted secret is a secret that was already committed."""
        text = BASE.replace("  nlm_profile: company\n",
                            "  nlm_profile: company\n  password: hunter2\n")
        joined = " ".join(_validate(text))
        self.assertIn("NOT REDACTION IN PLACE", joined)
        self.assertIn("rotate", joined)

    def test_secret_material_is_refused_in_the_self_hosted_case_too(self):
        """The self-hosted exemption is from DECLARING custody, never from
        keeping secrets out of the repository."""
        text = NO_CUSTODY.replace("case: operator_hosted", "case: self_hosted")
        text = text.replace("  nlm_profile: company\n",
                            "  nlm_profile: company\n  password: hunter2\n")
        errors = _validate(text)
        self.assertTrue(any("password" in e for e in errors), errors)

    def test_a_nested_secret_is_refused(self):
        """Material does not care which key it was filed under."""
        text = BASE.replace(
            "    session_state_in_custody: false\n",
            "    session_state_in_custody: false\n    password: hunter2\n")
        errors = _validate(text)
        self.assertTrue(any("password" in e for e in errors), errors)

    def test_secret_ref_is_refused_as_binding_detail(self):
        """Not secret material — binding detail. Carrying it here invites the
        rest of the binding to follow (review note, 2026-08-23)."""
        text = BASE.replace(
            "    binding_id: notebook_projection_hosting\n",
            "    binding_id: notebook_projection_hosting\n"
            "    secret_ref: xfactor001-password\n")
        errors = _validate(text)
        self.assertTrue(any("secret_ref" in e for e in errors), errors)
        self.assertIn("BINDING DETAIL", " ".join(errors))

    def test_the_profile_NAME_is_not_mistaken_for_an_exported_profile(self):
        """`nlm_profile: company` names a CLI profile and must keep passing.

        The refusal is keyed on the exact field name, not a substring, or the
        record's own required field would be refused as secret material.
        """
        self.assertEqual(_validate(BASE), [])

    def test_a_reference_alone_obtains_nothing(self):
        """§ 2.3's third test, stated structurally.

        The record carries the binding's IDENTITY and no part of its
        resolution: no provider, no vault, no secret_ref, no value. Resolving
        it requires the binding instance, which lives in the consuming install.
        """
        import yaml  # noqa: PLC0415

        record = yaml.safe_load(BASE)
        custody = record["hosting"]["custody"]
        for resolving_field in ("provider", "vault", "secret_ref", "value",
                                "secret", "password", "url", "endpoint"):
            self.assertNotIn(resolving_field, custody)
        self.assertEqual(
            set(custody) & {"binding_kind", "binding_client", "binding_id"},
            {"binding_kind", "binding_client", "binding_id"})
