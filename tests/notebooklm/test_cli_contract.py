"""Public-path compatibility checks for the NotebookLM sync CLI."""

from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from notebooklm_sync.models import GROUNDING

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "sync-notebooklm-books.py"


def _run(
    *arguments: str,
    provider_bin: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["PATH"] = str(provider_bin) if provider_bin is not None else ""
    return subprocess.run(
        [sys.executable, str(SCRIPT), *arguments],
        cwd=REPO_ROOT,
        env=environment,
        capture_output=True,
        check=False,
        text=True,
    )


def _provider_stub(root: Path, *, call_log: Path | None = None) -> Path:
    binary_directory = root / "bin"
    binary_directory.mkdir()
    executable = binary_directory / "nlm"
    log_call = (
        f"from pathlib import Path\nPath({str(call_log)!r}).open('a').write('call\\n')\n"
        if call_log is not None
        else ""
    )
    _ = executable.write_text(
        f"#!{sys.executable}\n{log_call}print('[]')\n",
        encoding="utf-8",
    )
    executable.chmod(0o755)
    return binary_directory


def _seed_grounding(root: Path) -> None:
    for relative in GROUNDING:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        _ = path.write_text("# Grounding\n", encoding="utf-8")


class SyncCliContractTests(unittest.TestCase):
    def test_help_uses_the_public_script_path(self) -> None:
        completed = _run("--help")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("--session-sweep", completed.stdout)
        self.assertIn("--import-new-sources", completed.stdout)

    def test_empty_workspace_dry_run_is_hermetic(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            _seed_grounding(root)
            completed = _run(temporary, provider_bin=_provider_stub(root))
            manifest_exists = (root / ".claude/nlm-sync-manifest.json").exists()
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertNotIn("Traceback", completed.stderr)
        self.assertIn("NO DECLARED HOSTING IDENTITY", completed.stdout)
        self.assertIn("CREATE", completed.stdout)
        self.assertFalse(manifest_exists)

    def test_missing_import_target_is_an_argparse_refusal(self) -> None:
        with TemporaryDirectory() as temporary:
            completed = _run(
                temporary,
                "--import-new-sources",
                "fake-notebook",
            )
        self.assertEqual(completed.returncode, 2)
        self.assertIn(
            "--target-path is required with --import-new-sources",
            completed.stderr,
        )
        self.assertNotIn("Traceback", completed.stderr)

    def test_malformed_manifest_is_refused_before_any_provider_call(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            _seed_grounding(root)
            manifest = root / ".claude/nlm-sync-manifest.json"
            manifest.parent.mkdir()
            _ = manifest.write_text('{"canon": []}\n', encoding="utf-8")
            call_log = root / "provider-calls.log"

            completed = _run(
                temporary,
                "--apply",
                provider_bin=_provider_stub(root, call_log=call_log),
            )

            provider_was_called = call_log.exists()
        self.assertEqual(completed.returncode, 2)
        self.assertIn("manifest", completed.stderr)
        self.assertFalse(provider_was_called)
        self.assertNotIn("Traceback", completed.stderr)

    def test_non_import_mode_ignores_an_irrelevant_import_date(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            _seed_grounding(root)
            completed = _run(
                temporary,
                "--import-date",
                "not-a-date",
                provider_bin=_provider_stub(root),
            )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertNotIn("Traceback", completed.stderr)


if __name__ == "__main__":
    _ = unittest.main()
