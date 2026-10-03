from __future__ import annotations

import unittest
from collections.abc import Mapping

from notebooklm_sync.nlm_client import JsonValue

from tests.notebooklm._test_nlm_auth_support import (
    LEGACY,
    STORED,
    AccountMismatchDetails,
    nlm_auth,
)


class MergeCarriesIdentityForward(unittest.TestCase):
    """#543: a refresh must not erase what the store already proves."""

    def merge(
        self,
        existing: Mapping[str, JsonValue],
        *,
        profile: str = "company",
        csrf: str | None = "new-csrf",
        session: str | None = "new-session",
        email: str | None = None,
        build_label: str | None = None,
        force: bool = False,
    ) -> tuple[dict[str, JsonValue], str]:
        return nlm_auth.merge_profile_metadata(
            existing,
            profile=profile,
            csrf=csrf,
            session=session,
            email=email,
            build_label=build_label,
            force=force,
        )

    def test_email_and_build_label_carry_forward_when_the_extraction_has_none(
        self,
    ) -> None:
        existing = {
            "csrf_token": "old",
            "session_id": "old",
            "email": STORED,
            "build_label": "20260824",
            "last_validated": "2026-08-24T00:00:00",
        }
        metadata, note = self.merge(existing)
        self.assertEqual(metadata["email"], STORED)
        self.assertEqual(metadata["build_label"], "20260824")
        self.assertEqual(metadata["csrf_token"], "new-csrf")
        self.assertEqual(metadata["session_id"], "new-session")
        self.assertNotEqual(metadata["last_validated"], "2026-08-24T00:00:00")
        self.assertIn(STORED, note)
        self.assertIn("build_label carried forward", note)

    def test_a_populated_email_is_never_nulled(self) -> None:
        for new_value in (None, "", "   "):
            with self.subTest(extracted=repr(new_value)):
                metadata, _ = self.merge({"email": STORED}, email=new_value)
                self.assertEqual(metadata["email"], STORED)

    def test_a_fresh_profile_writes_the_expected_keys(self) -> None:
        metadata, note = self.merge({})
        self.assertEqual(
            set(metadata),
            {"csrf_token", "session_id", "email", "build_label", "last_validated"},
        )
        self.assertIsNone(metadata["email"])
        self.assertIsNone(metadata["build_label"])
        self.assertIn("no account address recorded", note)

    def test_blank_and_non_string_leftovers_normalise_to_null(self) -> None:
        leftovers: list[JsonValue] = ["", "   ", 17, [], {"a": 1}]
        for junk in leftovers:
            with self.subTest(stored=repr(junk)):
                metadata, note = self.merge({"email": junk, "build_label": junk})
                self.assertIsNone(metadata["email"])
                self.assertIsNone(metadata["build_label"])
                self.assertIn("no account address recorded", note)
                self.assertNotIn("build_label carried forward", note)

    def test_a_new_build_label_wins_over_the_stored_one(self) -> None:
        metadata, note = self.merge({"build_label": "old"}, build_label="new")
        self.assertEqual(metadata["build_label"], "new")
        self.assertNotIn("build_label carried forward", note)

    def test_other_existing_keys_survive(self) -> None:
        existing: dict[str, JsonValue] = {
            "email": STORED,
            "provider": "builtin",
            "quirk": {"a": 1},
        }
        metadata, _ = self.merge(existing)
        self.assertEqual(metadata["provider"], "builtin")
        self.assertEqual(metadata["quirk"], {"a": 1})

    def test_a_captured_address_populates_an_empty_store(self) -> None:
        metadata, note = self.merge({}, email=STORED)
        self.assertEqual(metadata["email"], STORED)
        self.assertIn("captured", note)

    def test_a_case_only_difference_keeps_the_stored_spelling(self) -> None:
        metadata, note = self.merge({"email": STORED}, email=STORED.lower())
        self.assertEqual(metadata["email"], STORED)
        self.assertIn("matches the stored address", note)

    def test_a_different_account_refuses(self) -> None:
        with self.assertRaises(nlm_auth.AccountMismatch) as caught:
            _ = self.merge({"email": STORED}, email=LEGACY)
        assert isinstance(caught.exception, AccountMismatchDetails)
        self.assertEqual(caught.exception.stored, STORED)
        self.assertEqual(caught.exception.captured, LEGACY)
        self.assertEqual(caught.exception.profile, "company")

    def test_force_overwrites_the_recorded_account(self) -> None:
        metadata, note = self.merge({"email": STORED}, email=LEGACY, force=True)
        self.assertEqual(metadata["email"], LEGACY)
        self.assertIn("--force", note)
