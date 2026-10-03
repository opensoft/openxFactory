from __future__ import annotations

import unittest
from typing import ClassVar

from tests.notebooklm._test_validate_hosting_support import (
    APPROVAL,
    BASE,
    validate_text,
)


class GrantActorCrossCheckTests(unittest.TestCase):
    """The cross-check with teeth: who MAY decide and who DID must agree."""

    APPROVAL: ClassVar[str] = APPROVAL

    def _with_grant(self, granted_by: str) -> str:
        base = BASE.replace("share_out: []\n", "")
        return (
            base
            + self.APPROVAL
            + f"share_out:\n  - hosting_account: projection-host@example.invalid\n    user: someone@example.invalid\n    book_or_alias: xf-canon\n    role: viewer\n    granted_at: '2026-08-27'\n    granted_by: {granted_by}\n"
        )

    def test_a_grant_by_the_designated_actor_passes(self) -> None:
        self.assertEqual(validate_text(self._with_grant("Brett Heap")), [])

    def test_a_grant_by_anyone_else_is_refused(self) -> None:
        errors = validate_text(self._with_grant("Not The Designated Actor"))
        self.assertTrue(any("granted_by" in e for e in errors), errors)

    def test_the_refusal_names_BOTH_values(self) -> None:
        """So the reader can see which one is wrong instead of guessing."""
        joined = " ".join(validate_text(self._with_grant("Someone Else")))
        self.assertIn("Someone Else", joined)
        self.assertIn("Brett Heap", joined)
