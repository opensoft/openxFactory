from __future__ import annotations

import subprocess
import unittest
from unittest.mock import patch

from notebooklm_sync.nlm_client import (
    NlmCliProvider,
    ProviderPayloadError,
    parse_notebook_rows,
    parse_source_rows,
)


class ProviderBoundaryTests(unittest.TestCase):
    def test_malformed_json_is_refused_instead_of_becoming_an_empty_account(
        self,
    ) -> None:
        completed = subprocess.CompletedProcess(
            args=["nlm", "notebook", "list", "--json"],
            returncode=0,
            stdout="provider warning before payload\n[]\n",
            stderr="",
        )

        with (
            patch("notebooklm_sync.nlm_client.subprocess.run", return_value=completed),
            self.assertRaisesRegex(ProviderPayloadError, "valid JSON"),
        ):
            _ = NlmCliProvider(assert_bound=lambda: None).invoke(
                "notebook", "list", "--json"
            )

    def test_valid_json_without_the_expected_collection_is_refused(self) -> None:
        cases = (
            (parse_notebook_rows, "notebooks"),
            (parse_source_rows, "sources"),
        )
        for parse_rows, collection in cases:
            with (
                self.subTest(collection=collection),
                self.assertRaisesRegex(ProviderPayloadError, collection),
            ):
                _ = parse_rows({"error": "unauthorized"})


if __name__ == "__main__":
    _ = unittest.main()
