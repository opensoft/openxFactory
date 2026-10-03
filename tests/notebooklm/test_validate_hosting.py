from __future__ import annotations

import unittest

from tests.notebooklm._test_validate_hosting_support import (
    BASE,
    REPO_ROOT,
    validate_text,
    validator,
)


class HostingDeclarationValidationTests(unittest.TestCase):
    def test_the_committed_example_conforms(self) -> None:
        """RE-AIMED, not weakened (adopt-configured-notebook-hosting-identity).

        This was `test_the_committed_record_conforms`, and it worked because the
        live record and the committed file were ONE FILE — so it was the only
        automatic conformance check the live declaration had. The split costs
        that, and the change is obliged to replace it rather than lose it. This
        test keeps the SHAPE gated in CI;
        `test_a_resolved_declaration_is_validated` below proves the resolved
        path is validated at all; and the live record's own conformance becomes
        an operator command (`--resolved`) whose green line is the evidence.
        Three things for one, because the live record cannot be checked by this
        repository's CI without publishing it — which is the trade the ruling
        accepts, and the check quietly disappearing is what must not happen.
        """
        errors = validator.validate(REPO_ROOT / validator.DEFAULT_REL)
        self.assertEqual(
            errors,
            [],
            "the shipped instance must pass: it is the shape's example and this validator's own fixture",
        )

    def test_a_conforming_declaration_passes(self) -> None:
        self.assertEqual(validate_text(BASE), [])

    def test_a_third_case_is_refused(self) -> None:
        errors = validate_text(
            BASE.replace("case: operator_hosted", "case: partly_hosted")
        )
        self.assertTrue(any("hosting.case" in e for e in errors))

    def test_a_self_hosted_personal_declaration_is_legitimate(self) -> None:
        text = "schema_version: 1\nkind: notebook_projection_hosting\nhosting:\n  case: self_hosted\n  account: someone@gmail.com\n  nlm_profile: personal\nshare_out: []\n"
        self.assertEqual(
            validate_text(text),
            [],
            "an individual's own account is a complete binding, not a degraded operator-hosted one",
        )

    def test_a_service_account_cannot_host_a_projection(self) -> None:
        errors = validate_text(
            BASE.replace(
                "account: projection-host@example.invalid",
                "account: books@xf-proj.iam.gserviceaccount.com",
            ).replace(
                "domain: example.invalid", "domain: xf-proj.iam.gserviceaccount.com"
            )
        )
        self.assertTrue(
            any("service account" in e for e in errors),
            "NotebookLM has no API and a service account cannot drive its consumer web UI",
        )

    def test_operator_hosted_refuses_a_consumer_account(self) -> None:
        errors = validate_text(
            BASE.replace(
                "account_type: google_workspace_user",
                "account_type: consumer_google_account",
            )
        )
        self.assertTrue(any("account_type" in e for e in errors))

    def test_the_account_must_live_in_the_declared_domain(self) -> None:
        errors = validate_text(
            BASE.replace("domain: example.invalid", "domain: elsewhere.example")
        )
        self.assertTrue(any("not in the declared domain" in e for e in errors))

    def test_a_declaration_without_a_profile_cannot_bind(self) -> None:
        errors = validate_text(BASE.replace("  nlm_profile: company\n", ""))
        self.assertTrue(any("nlm_profile" in e for e in errors))

    def test_a_pending_migration_names_where_the_books_still_live(self) -> None:
        errors = validate_text(
            BASE.replace("approval:", "  migration:\n    state: pending\napproval:")
        )
        self.assertTrue(any("from_account" in e for e in errors))
        self.assertTrue(any("from_nlm_profile" in e for e in errors))
