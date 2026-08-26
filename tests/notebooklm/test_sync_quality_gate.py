from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from notebooklm_sync.quality import quality_commands

REPO_ROOT = Path(__file__).resolve().parents[2]
QUALITY_COMMAND = REPO_ROOT / "scripts" / "check-notebooklm-sync-quality.py"
PYRIGHT_CONFIG = REPO_ROOT / "pyrightconfig.json"


class SyncQualityGateTests(unittest.TestCase):
    def test_declared_surface_includes_only_notebooklm_sync_python(self) -> None:
        # Given: the repository-local quality command.
        # When: its declared surface is requested without running tools.
        completed = subprocess.run(
            [sys.executable, str(QUALITY_COMMAND), "--show-surface"],
            cwd=REPO_ROOT,
            capture_output=True,
            check=False,
            text=True,
        )

        # Then: production, package, and tests are included, unrelated debt is not.
        self.assertEqual(completed.returncode, 0, completed.stderr)
        surface = set(completed.stdout.splitlines())
        self.assertIn("scripts/sync-notebooklm-books.py", surface)
        self.assertIn("scripts/notebooklm_sync", surface)
        self.assertIn("tests/notebooklm", surface)
        self.assertNotIn("scripts/ideation_dashboard", surface)
        self.assertNotIn("tests/doc-health", surface)

    def test_type_gate_does_not_filter_warning_level_findings(self) -> None:
        commands = quality_commands(Path("checker.py"))
        basedpyright = next(
            command for command in commands if command.name == "basedpyright"
        )
        config = json.loads(PYRIGHT_CONFIG.read_text(encoding="utf-8"))

        self.assertNotIn("--level", basedpyright.arguments)
        self.assertEqual(config["typeCheckingMode"], "basic")
        self.assertIs(config["failOnWarnings"], True)


if __name__ == "__main__":
    unittest.main()
