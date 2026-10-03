from __future__ import annotations

import unittest
from typing import ClassVar

from tests.notebooklm._test_validate_hosting_support import BASE, validate_text


class ApprovalLaneValidationTests(unittest.TestCase):
    """Task 2.4's designation, ENFORCED rather than declared (review, PR #414).

    The block shipped unenforced: `validate()` read the hosting map and the
    roster and nothing else, so the whole `approval:` block could be deleted,
    scalar-ized, or have `automated_approval` flipped true and the record still
    passed. A declaration nothing checks is the CPL-1b shape this change family
    keeps refusing — a control asserted somewhere no rule holds it.
    """

    APPROVAL: ClassVar[str] = (
        "approval:\n  designated_actor: Brett Heap\n  acts_in: the hosting account's own NotebookLM interface\n  automated_approval: false\n"
    )

    def _rec(
        self,
        approval: str | None = None,
        share_out: str = "share_out: []\n",
        case: str = "operator_hosted",
    ) -> str:
        import re as _re

        base = BASE.replace("case: operator_hosted", "case: " + case)
        base = base.replace("share_out: []\n", "")
        base = _re.sub(
            "(?m)^# The approval designation.*?(?=^share_out|\\Z)",
            "",
            base,
            flags=_re.DOTALL,
        )
        base = _re.sub("(?m)^approval:\\n(?:  .*\\n)*", "", base)
        return base + (self.APPROVAL if approval is None else approval) + share_out

    def test_a_conforming_approval_block_passes(self) -> None:
        self.assertEqual(validate_text(self._rec()), [])

    def test_an_operator_hosted_record_without_approval_is_refused(self) -> None:
        errors = validate_text(self._rec(approval=""))
        self.assertTrue(any("approval" in e for e in errors), errors)
        self.assertIn("whoever happens to read the account's mail", " ".join(errors))

    def test_a_self_hosted_record_needs_no_approval(self) -> None:
        """Same asymmetry as custody: no operator, no governance gap."""
        errors = [
            e
            for e in validate_text(self._rec(approval="", case="self_hosted"))
            if "approval" in e
        ]
        self.assertEqual(errors, [])

    def test_a_scalar_approval_is_refused(self) -> None:
        errors = validate_text(self._rec(approval="approval: Brett Heap\n"))
        self.assertTrue(any("approval" in e for e in errors), errors)

    def test_an_empty_designated_actor_is_refused(self) -> None:
        errors = validate_text(
            self._rec(approval=self.APPROVAL.replace("Brett Heap", ""))
        )
        self.assertTrue(any("designated_actor" in e for e in errors), errors)

    def test_automated_approval_must_be_present_and_false(self) -> None:
        """The ratified posture: the approval stays a governed human act."""
        for bad in ("automated_approval: true\n", ""):
            with self.subTest(variant=bad or "<absent>"):
                errors = validate_text(
                    self._rec(
                        approval=self.APPROVAL.replace(
                            "  automated_approval: false\n", bad
                        )
                    )
                )
                self.assertTrue(any("automated_approval" in e for e in errors), errors)

    def test_acts_in_must_say_where(self) -> None:
        errors = validate_text(
            self._rec(
                approval=self.APPROVAL.replace(
                    "  acts_in: the hosting account's own NotebookLM interface\n", ""
                )
            )
        )
        self.assertTrue(any("acts_in" in e for e in errors), errors)
