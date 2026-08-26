"""The FR-043 hermeticity guard, asserted from INSIDE a conftest-less directory.

Why here, and why a `unittest.TestCase`. `tests/notebooklm/` is one of the seven
directories under `tests/` with no `conftest.py` of its own, and PR #49 review
finding 17 left two ways to run code in it with the guard switched off:

  1. a pytest run STARTED here (the directory became the rootdir, so
     `tests/conftest.py` was outside `confcutdir` and never loaded) — closed by
     the repo-root `pytest.ini` rootdir anchor;
  2. `scripts/validate-docs.sh`'s `python3 -m unittest discover` fallback, taken
     when pytest is unavailable, where a conftest fixture cannot apply at all —
     closed by `tests/hermetic_unittest.py`, the guarded runner the gate now uses.

Both were measured reaching a real-binary stand-in with the refusal ledger empty.
A `TestCase` is collected by pytest AND by `unittest discover`, so ONE probe
answers for both routes; it only READS `PATH` and two module attributes, so it is
safe in any runner and mutates nothing.

If this fails, the run it is in is NOT hermetic: something in it could reach the
real `nlm` or `gh`. Run it through `python3 -m pytest` (any directory) or
`python3 tests/hermetic_unittest.py tests/notebooklm/` — never bare
`python3 -m unittest`, which installs no guard.
"""

from __future__ import annotations

import shutil
import subprocess
import unittest
from pathlib import Path
from typing import Protocol, runtime_checkable

import hermeticity
from ideation_dashboard import workbench as workbench_contracts


@runtime_checkable
class NotebookRunnerProbe(Protocol):
    def list_scratch_result(self) -> workbench_contracts.NotebookListing: ...


@runtime_checkable
class CommandRunnerProbe(Protocol):
    def run(
        self, *args: str, cwd: Path | None = None
    ) -> subprocess.CompletedProcess[str]: ...


def _notebook_candidate(
    value: NotebookRunnerProbe | str,
) -> NotebookRunnerProbe | str:
    return value


def _command_candidate(value: CommandRunnerProbe | str) -> CommandRunnerProbe | str:
    return value


class HermeticityGuardReachesThisDirectoryTests(unittest.TestCase):
    """Both layers of `tests/hermeticity.py`, from a directory with no conftest."""

    def test_the_guarded_binaries_resolve_to_the_guards_own_refusal(self) -> None:
        for binary in hermeticity.GUARDED_BINARIES:
            resolved = shutil.which(binary)
            self.assertIsNotNone(
                resolved,
                f"{binary!r} resolves to nothing, so this run installed no shim: the hermeticity guard is not active (see this module's docstring)")
            if resolved is None:
                self.fail(f"{binary!r} did not resolve")
            text = Path(resolved).read_text(encoding="utf-8", errors="replace")
            self.assertIn(
                hermeticity.MARKER, text,
                f"{binary!r} resolves to {resolved} — a real binary, not the guard's refusal shim: this run is NOT hermetic")

    def test_the_in_process_runners_are_the_refusals(self) -> None:
        # adopt-neutral-tooling-home tranche A: layer 2's seams live in the
        # dashboard package, which arrives with tranche B; until then there
        # is no in-process runner to assert (layer 1 is asserted above).
        # find_spec, not try/except — see tests/hermeticity.py runner_seams.
        # Self-healing on tranche B.
        from importlib.util import find_spec
        if find_spec("ideation_dashboard.workbench") is None:
            self.skipTest(
                "ideation_dashboard arrives with adopt-neutral-tooling-home tranche B"
            )
        import ideation_dashboard.session_pr as session_pr_mod
        import ideation_dashboard.workbench as workbench_mod

        notebook_runner = _notebook_candidate(
            workbench_mod.NotebookAdapter(available=True)
        )
        if not isinstance(notebook_runner, NotebookRunnerProbe):
            self.fail("workbench adapter lacks the scratch-list probe")
        with self.assertRaises(hermeticity.HermeticityViolation):
            _ = notebook_runner.list_scratch_result()

        command_runner = _command_candidate(
            session_pr_mod.SubprocessCommandRunner()
        )
        if not isinstance(command_runner, CommandRunnerProbe):
            self.fail("session command runner lacks its run seam")
        with self.assertRaises(hermeticity.HermeticityViolation):
            _ = command_runner.run("gh", "auth", "status")


if __name__ == "__main__":                          # pragma: no cover - manual use
    _ = unittest.main()
