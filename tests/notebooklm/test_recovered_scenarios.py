"""Additional recovered scenarios over the same focused case support."""

from __future__ import annotations

from tests.notebooklm import _test_lifecycle_books_support as _group_3


class SplitIdeationBookTests(_group_3.SplitIdeationBookTests):
    def test_oversized_source_refuses_a_silent_rename_failure(self) -> None: self.scenario_oversized_source_refuses_a_silent_rename_failure()
