from __future__ import annotations

import unittest
from typing import ClassVar

from tests.notebooklm._test_validate_hosting_support import (
    BASE,
    NO_CUSTODY,
    validate_text,
)


class SecretMaterialRefusalTests(unittest.TestCase):
    """Nothing secret-shaped, in EITHER case, anywhere in the record."""

    SECRET_FIELDS: ClassVar[tuple[str, ...]] = (
        "password",
        "totp_seed",
        "recovery_code",
        "cookie",
        "session",
        "profile",
        "private_key",
        "api_key",
    )

    def test_each_secret_shaped_field_is_refused(self) -> None:
        for field in self.SECRET_FIELDS:
            with self.subTest(field=field):
                text = BASE.replace(
                    "  nlm_profile: company\n",
                    f"  nlm_profile: company\n  {field}: some-value\n",
                )
                errors = validate_text(text)
                self.assertTrue(any(field in e for e in errors), (field, errors))

    def test_the_refusal_names_the_binding_not_redaction(self) -> None:
        """A redacted secret is a secret that was already committed."""
        text = BASE.replace(
            "  nlm_profile: company\n", "  nlm_profile: company\n  password: hunter2\n"
        )
        joined = " ".join(validate_text(text))
        self.assertIn("NOT REDACTION IN PLACE", joined)
        self.assertIn("rotate", joined)

    def test_secret_material_is_refused_in_the_self_hosted_case_too(self) -> None:
        """The self-hosted exemption is from DECLARING custody, never from
        keeping secrets out of the repository."""
        text = NO_CUSTODY.replace("case: operator_hosted", "case: self_hosted")
        text = text.replace(
            "  nlm_profile: company\n", "  nlm_profile: company\n  password: hunter2\n"
        )
        errors = validate_text(text)
        self.assertTrue(any("password" in e for e in errors), errors)

    def test_a_nested_secret_is_refused(self) -> None:
        """Material does not care which key it was filed under."""
        text = BASE.replace(
            "    session_state_in_custody: false\n",
            "    session_state_in_custody: false\n    password: hunter2\n",
        )
        errors = validate_text(text)
        self.assertTrue(any("password" in e for e in errors), errors)

    def test_secret_ref_is_refused_as_binding_detail(self) -> None:
        """Not secret material — binding detail. Carrying it here invites the
        rest of the binding to follow (review note, 2026-08-23)."""
        text = BASE.replace(
            "    binding_id: notebook_projection_hosting\n",
            "    binding_id: notebook_projection_hosting\n    secret_ref: xfactor001-password\n",
        )
        errors = validate_text(text)
        self.assertTrue(any("secret_ref" in e for e in errors), errors)
        self.assertIn("BINDING DETAIL", " ".join(errors))

    def test_the_profile_NAME_is_not_mistaken_for_an_exported_profile(self) -> None:
        """`nlm_profile: company` names a CLI profile and must keep passing.

        The refusal is keyed on the exact field name, not a substring, or the
        record's own required field would be refused as secret material.
        """
        self.assertEqual(validate_text(BASE), [])

    def test_a_reference_alone_obtains_nothing(self) -> None:
        """§ 2.3's third test, stated structurally.

        The record carries the binding's IDENTITY and no part of its
        resolution: no provider, no vault, no secret_ref, no value. Resolving
        it requires the binding instance, which lives in the consuming install.
        """
        import re

        custody_block = BASE.split("  custody:\n", 1)[1].split("\n#", 1)[0]
        custody = set(re.findall(r"^    ([a-z_]+):", custody_block, flags=re.MULTILINE))
        for resolving_field in (
            "provider",
            "vault",
            "secret_ref",
            "value",
            "secret",
            "password",
            "url",
            "endpoint",
        ):
            self.assertNotIn(resolving_field, custody)
        self.assertEqual(
            set(custody) & {"binding_kind", "binding_client", "binding_id"},
            {"binding_kind", "binding_client", "binding_id"},
        )
