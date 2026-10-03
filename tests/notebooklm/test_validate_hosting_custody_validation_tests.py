from __future__ import annotations

import unittest

from tests.notebooklm._test_validate_hosting_support import (
    BASE,
    NO_CUSTODY,
    validate_text,
)


class CustodyValidationTests(unittest.TestCase):
    """add-notebook-hosting-credential-custody § 2 — custody BY REFERENCE ONLY.

    Two obligations, and they are asymmetric on purpose: the operator-hosted
    case must NAME its binding, while NEITHER case may carry secret material.
    """

    def test_a_conforming_custody_reference_passes(self) -> None:
        self.assertEqual(validate_text(BASE), [])

    def test_an_operator_hosted_record_without_custody_is_refused(self) -> None:
        errors = validate_text(NO_CUSTODY)
        self.assertTrue(any("hosting.custody" in e for e in errors), errors)
        joined = " ".join(errors)
        self.assertIn("undocumented rather than governed", joined)

    def test_a_self_hosted_record_needs_no_custody(self) -> None:
        """The two-case model: no operator, no obligation."""
        text = NO_CUSTODY.replace("case: operator_hosted", "case: self_hosted")
        errors = [e for e in validate_text(text) if "custody" in e]
        self.assertEqual(errors, [], "self-hosted must not be asked for custody")

    def test_a_partial_binding_reference_is_refused(self) -> None:
        """All three fields, or the reference cannot be resolved at all."""
        for field in ("binding_kind", "binding_client", "binding_id"):
            with self.subTest(missing=field):
                text = "\n".join(
                    line
                    for line in BASE.splitlines()
                    if not line.strip().startswith(field + ":")
                )
                errors = validate_text(text)
                self.assertTrue(any(field in e for e in errors), errors)

    def test_covers_must_name_the_secrets(self) -> None:
        text = BASE.replace(
            "    covers:\n      - account_password\n      - totp_seed\n",
            "    covers: []\n",
        )
        errors = validate_text(text)
        self.assertTrue(any("covers" in e for e in errors), errors)
        self.assertIn("single point of failure", " ".join(errors))

    def test_an_interactive_step_must_be_named_when_declared(self) -> None:
        text = BASE.replace(
            "    interactive_step: Google sign-in is an interactive browser flow.\n", ""
        )
        errors = validate_text(text)
        self.assertTrue(any("interactive_step" in e for e in errors), errors)

    def test_silence_about_the_interactive_step_is_refused(self) -> None:
        """Silence reads as 'unattended' to an operator planning automation."""
        text = BASE.replace("    interactive_step_remains: true\n", "")
        errors = validate_text(text)
        self.assertTrue(any("interactive_step_remains" in e for e in errors), errors)
