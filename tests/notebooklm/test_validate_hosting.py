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
# The approval designation is part of a CONFORMING operator-hosted record since
# task 2.4 (review, PR #414): an operated account with no named decider is the
# failure the ratified requirement forbids. In the base fixture for the same
# reason custody is — every other test here asserts against "an otherwise
# conforming record".
approval:
  designated_actor: Brett Heap
  acts_in: the hosting account's own NotebookLM interface
  automated_approval: false
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
        # Anchored on `approval:` — the first TOP-LEVEL key after the hosting
        # map — so the indented `migration:` lands under `hosting` where it
        # belongs. Anchoring on `share_out:` used to work and stopped when the
        # approval block landed between them, filing migration under `approval`
        # and silently disarming this test.
        errors = _validate(BASE.replace("approval:", """  migration:
    state: pending
approval:"""))
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


class ApprovalLaneValidationTests(unittest.TestCase):
    """Task 2.4's designation, ENFORCED rather than declared (review, PR #414).

    The block shipped unenforced: `validate()` read the hosting map and the
    roster and nothing else, so the whole `approval:` block could be deleted,
    scalar-ized, or have `automated_approval` flipped true and the record still
    passed. A declaration nothing checks is the CPL-1b shape this change family
    keeps refusing — a control asserted somewhere no rule holds it.
    """

    APPROVAL = ("approval:\n"
                "  designated_actor: Brett Heap\n"
                "  acts_in: the hosting account's own NotebookLM interface\n"
                "  automated_approval: false\n")

    def _rec(self, approval=None, share_out="share_out: []\n", case="operator_hosted"):
        import re as _re
        base = BASE.replace("case: operator_hosted", "case: " + case)
        base = base.replace("share_out: []\n", "")
        # BASE now carries its own approval block; strip it so this helper
        # substitutes rather than appends a second one.
        base = _re.sub(r"(?m)^# The approval designation.*?(?=^share_out|\Z)", "",
                       base, flags=_re.S)
        base = _re.sub(r"(?m)^approval:\n(?:  .*\n)*", "", base)
        return base + (self.APPROVAL if approval is None else approval) + share_out

    def test_a_conforming_approval_block_passes(self):
        self.assertEqual(_validate(self._rec()), [])

    def test_an_operator_hosted_record_without_approval_is_refused(self):
        errors = _validate(self._rec(approval=""))
        self.assertTrue(any("approval" in e for e in errors), errors)
        self.assertIn("whoever happens to read the account's mail", " ".join(errors))

    def test_a_self_hosted_record_needs_no_approval(self):
        """Same asymmetry as custody: no operator, no governance gap."""
        errors = [e for e in _validate(self._rec(approval="", case="self_hosted"))
                  if "approval" in e]
        self.assertEqual(errors, [])

    def test_a_scalar_approval_is_refused(self):
        errors = _validate(self._rec(approval="approval: Brett Heap\n"))
        self.assertTrue(any("approval" in e for e in errors), errors)

    def test_an_empty_designated_actor_is_refused(self):
        errors = _validate(self._rec(
            approval=self.APPROVAL.replace("Brett Heap", "")))
        self.assertTrue(any("designated_actor" in e for e in errors), errors)

    def test_automated_approval_must_be_present_and_false(self):
        """The ratified posture: the approval stays a governed human act."""
        for bad in ("automated_approval: true\n", ""):
            with self.subTest(variant=bad or "<absent>"):
                errors = _validate(self._rec(
                    approval=self.APPROVAL.replace("  automated_approval: false\n", bad)))
                self.assertTrue(
                    any("automated_approval" in e for e in errors), errors)

    def test_acts_in_must_say_where(self):
        errors = _validate(self._rec(
            approval=self.APPROVAL.replace(
                "  acts_in: the hosting account's own NotebookLM interface\n", "")))
        self.assertTrue(any("acts_in" in e for e in errors), errors)


class GrantActorCrossCheckTests(unittest.TestCase):
    """The cross-check with teeth: who MAY decide and who DID must agree."""

    APPROVAL = ApprovalLaneValidationTests.APPROVAL

    def _with_grant(self, granted_by):
        base = BASE.replace("share_out: []\n", "")
        return base + self.APPROVAL + (
            "share_out:\n"
            "  - hosting_account: xFactor001@opensoft.one\n"
            "    user: someone@example.com\n"
            "    book_or_alias: xf-canon\n"
            "    role: viewer\n"
            "    granted_at: '2026-08-27'\n"
            f"    granted_by: {granted_by}\n")

    def test_a_grant_by_the_designated_actor_passes(self):
        self.assertEqual(_validate(self._with_grant("Brett Heap")), [])

    def test_a_grant_by_anyone_else_is_refused(self):
        errors = _validate(self._with_grant("Not The Designated Actor"))
        self.assertTrue(any("granted_by" in e for e in errors), errors)

    def test_the_refusal_names_BOTH_values(self):
        """So the reader can see which one is wrong instead of guessing."""
        joined = " ".join(_validate(self._with_grant("Someone Else")))
        self.assertIn("Someone Else", joined)
        self.assertIn("Brett Heap", joined)


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


class SecretsNestedInSequencesTests(unittest.TestCase):
    """Copilot, PR #395 — the walk must cover SEQUENCES, not mappings alone.

    `_refuse_secret_shaped` descended only into dicts, so a secret-shaped key
    inside a list was skipped outright and the record validated CLEAN with
    credential material in it. That is the fail-open family inside the refusal
    written to prevent it: a path that could not answer returned "nothing to
    see" rather than looking.

    YAML nests freely, so these pin the shapes a real record could take rather
    than the one the original walk happened to expect.
    """

    def _with(self, extra: str) -> list[str]:
        return _validate(BASE.replace("  nlm_profile: company\n",
                                      "  nlm_profile: company\n" + extra))

    def test_a_secret_inside_a_list_is_refused(self):
        errors = self._with("  some_list:\n    - password: hunter2\n")
        self.assertTrue(any("password" in e for e in errors), errors)

    def test_a_secret_inside_a_list_of_lists_is_refused(self):
        errors = self._with("  outer:\n    - - password: hunter2\n")
        self.assertTrue(any("password" in e for e in errors), errors)

    def test_a_secret_beside_innocent_keys_in_a_list_entry_is_refused(self):
        """The realistic shape: a roster-like list whose entries carry a cookie."""
        errors = self._with("  share_like:\n    - name: a\n      cookie: abc\n")
        self.assertTrue(any("cookie" in e for e in errors), errors)

    def test_a_secret_four_levels_down_through_mixed_containers(self):
        errors = self._with(
            "  deep:\n    - a:\n        - b:\n            totp_seed: x\n")
        self.assertTrue(any("totp_seed" in e for e in errors), errors)

    def test_the_error_path_names_the_list_index(self):
        """A refusal the operator cannot locate is only half a refusal."""
        errors = self._with("  some_list:\n    - password: hunter2\n")
        self.assertTrue(any("some_list[0]" in e for e in errors), errors)

    def test_lists_without_secrets_still_pass(self):
        """The complement — the walk must not refuse sequences as such."""
        self.assertEqual(
            self._with("  harmless:\n    - name: a\n    - name: b\n"), [])


# MUST STAY LAST. This block sat mid-file, so `python3 tests/.../test_validate_hosting.py`
# called unittest.main() before the custody and secret-refusal classes below were
# defined: it ran 15 of 29 tests and printed OK. A green result that measured half
# the suite is the same fail-open shape as the validator defect fixed alongside it
# (Copilot, PR #395) — the run could not see the rest and said fine rather than
# saying it could not see them.
if __name__ == "__main__":
    unittest.main()
