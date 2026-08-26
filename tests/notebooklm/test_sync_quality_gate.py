from __future__ import annotations

import subprocess
import sys
import unittest
from collections.abc import Mapping
from pathlib import Path
from tempfile import TemporaryDirectory

from notebooklm_sync.nlm_client import JsonValue, decode_json
from notebooklm_sync.quality import quality_commands

REPO_ROOT = Path(__file__).resolve().parents[2]
QUALITY_COMMAND = REPO_ROOT / "scripts" / "check-notebooklm-sync-quality.py"
PYRIGHT_CONFIG = REPO_ROOT / "pyrightconfig.json"


class QualityConfigError(ValueError):
    reason: str

    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(f"invalid pyright quality configuration: {reason}")


def _pyright_settings() -> tuple[str, bool]:
    raw: JsonValue = decode_json(PYRIGHT_CONFIG.read_text(encoding="utf-8"))
    if not isinstance(raw, Mapping):
        raise QualityConfigError("root must be an object")
    mode = raw.get("typeCheckingMode")
    fail_on_warnings = raw.get("failOnWarnings")
    if not isinstance(mode, str) or not isinstance(fail_on_warnings, bool):
        raise QualityConfigError("quality settings have invalid types")
    return mode, fail_on_warnings


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
        mode, fail_on_warnings = _pyright_settings()

        self.assertNotIn("--level", basedpyright.arguments)
        self.assertEqual(mode, "recommended")
        self.assertIs(fail_on_warnings, True)

    def test_warning_level_finding_exits_nonzero(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            config = root / "pyrightconfig.json"
            probe = root / "warning_probe.py"
            _ = config.write_text(
                '{"typeCheckingMode":"recommended","failOnWarnings":true}\n',
                encoding="utf-8",
            )
            _ = probe.write_text(
                "def value() -> int:\n    return 1\n\nvalue()\n",
                encoding="utf-8",
            )
            completed = subprocess.run(
                ["uvx", "basedpyright", "--project", str(config), str(probe)],
                capture_output=True,
                check=False,
                text=True,
            )

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("reportUnusedCallResult", completed.stdout)


if __name__ == "__main__":
    _ = unittest.main()
