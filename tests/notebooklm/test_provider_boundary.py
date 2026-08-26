from __future__ import annotations

import subprocess
import unittest
from unittest.mock import patch

from notebooklm_sync.nlm_client import NlmCliProvider, ProviderPayloadError


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
            patch(
                "notebooklm_sync.nlm_client.subprocess.run", return_value=completed
            ),
            self.assertRaisesRegex(ProviderPayloadError, "valid JSON"),
        ):
            NlmCliProvider(assert_bound=lambda: None).invoke(
                "notebook", "list", "--json"
            )


if __name__ == "__main__":
    unittest.main()
