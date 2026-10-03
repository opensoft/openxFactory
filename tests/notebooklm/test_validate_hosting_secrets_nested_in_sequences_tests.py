from __future__ import annotations

import unittest

from tests.notebooklm._test_validate_hosting_support import BASE, validate_text


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
        return validate_text(
            BASE.replace("  nlm_profile: company\n", "  nlm_profile: company\n" + extra)
        )

    def test_a_secret_inside_a_list_is_refused(self) -> None:
        errors = self._with("  some_list:\n    - password: hunter2\n")
        self.assertTrue(any("password" in e for e in errors), errors)

    def test_a_secret_inside_a_list_of_lists_is_refused(self) -> None:
        errors = self._with("  outer:\n    - - password: hunter2\n")
        self.assertTrue(any("password" in e for e in errors), errors)

    def test_a_secret_beside_innocent_keys_in_a_list_entry_is_refused(self) -> None:
        """The realistic shape: a roster-like list whose entries carry a cookie."""
        errors = self._with("  share_like:\n    - name: a\n      cookie: abc\n")
        self.assertTrue(any("cookie" in e for e in errors), errors)

    def test_a_secret_four_levels_down_through_mixed_containers(self) -> None:
        errors = self._with(
            "  deep:\n    - a:\n        - b:\n            totp_seed: x\n"
        )
        self.assertTrue(any("totp_seed" in e for e in errors), errors)

    def test_the_error_path_names_the_list_index(self) -> None:
        """A refusal the operator cannot locate is only half a refusal."""
        errors = self._with("  some_list:\n    - password: hunter2\n")
        self.assertTrue(any("some_list[0]" in e for e in errors), errors)

    def test_lists_without_secrets_still_pass(self) -> None:
        """The complement — the walk must not refuse sequences as such."""
        self.assertEqual(self._with("  harmless:\n    - name: a\n    - name: b\n"), [])
