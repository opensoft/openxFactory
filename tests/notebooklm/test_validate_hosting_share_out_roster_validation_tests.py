from __future__ import annotations

import unittest
from typing import ClassVar

from tests.notebooklm._test_validate_hosting_support import (
    BASE,
    validate_text,
    validator,
)


class ShareOutRosterValidationTests(unittest.TestCase):
    ENTRY: ClassVar[str] = (
        'share_out:\n  - hosting_account: projection-host@example.invalid\n    user: reader@example.invalid\n    book_or_alias: xf-canon\n    role: viewer\n    granted_at: "2026-08-24"\n    granted_by: Brett Heap\n'
    )

    def _with_roster(self, roster: str) -> list[str]:
        return validate_text(BASE.replace("share_out: []", roster))

    def test_a_complete_entry_passes(self) -> None:
        self.assertEqual(self._with_roster(self.ENTRY), [])

    FIELDS: ClassVar[dict[str, str]] = {
        "hosting_account": "projection-host@example.invalid",
        "user": "reader@example.invalid",
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

    def test_every_one_of_the_six_fields_is_required(self) -> None:
        for field in validator.ENTRY_FIELDS:
            with self.subTest(field=field):
                errors = self._with_roster(self._roster_without(field))
                self.assertTrue(
                    any(field in e for e in errors), f"{field} must be required"
                )

    def test_two_people_on_one_book_are_distinct_entries(self) -> None:
        roster = (
            self.ENTRY
            + '  - hosting_account: projection-host@example.invalid\n    user: second@example.invalid\n    book_or_alias: xf-canon\n    role: viewer\n    granted_at: "2026-08-24"\n    granted_by: Brett Heap\n'
        )
        self.assertEqual(
            self._with_roster(roster),
            [],
            "the grantee is part of the key — this is the case that broke the client-identity roster",
        )

    def test_a_re_decision_must_update_rather_than_add_a_second_entry(self) -> None:
        roster = (
            self.ENTRY
            + '  - hosting_account: projection-host@example.invalid\n    user: reader@example.invalid\n    book_or_alias: xf-canon\n    role: editor\n    granted_at: "2026-08-25"\n    granted_by: Someone Else\n'
        )
        errors = self._with_roster(roster)
        self.assertTrue(
            any("duplicate share-out key" in e for e in errors),
            "role, grant time and actor are ATTRIBUTES: two live entries would assert a stale grant beside a current one",
        )

    def test_an_entry_for_another_hosting_account_is_refused(self) -> None:
        roster = self.ENTRY.replace(
            "hosting_account: projection-host@example.invalid",
            "hosting_account: someone@gmail.com",
        )
        errors = self._with_roster(roster)
        self.assertTrue(any("declared hosting account" in e for e in errors))

    def test_an_unknown_role_is_refused(self) -> None:
        errors = self._with_roster(self.ENTRY.replace("role: viewer", "role: owner"))
        self.assertTrue(any("role" in e for e in errors))
