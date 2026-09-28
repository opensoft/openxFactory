"""The two routes that once ran openxFactory's NotebookLM suite with the
hermeticity guard switched OFF are guarded (finding 17, wave 2). Proposed as
NAMED tests of F11.1's `COMPOSITION_TESTS` (R1Q2 (a); T007 batch E).

MOVED HERE by plan 034 T035 (opensoft/openDox-code#51, landed `80acead1`).
The three cases left `tests/test_hermeticity.py` at openDox-code `68be484a`
(`:604-621`, `:640-660` and `:663-674`, with `_probe_run` at `:595-601`).
They drive a probe that is openxFactory's, not openDox's:
`tests/notebooklm/test_hermeticity_guard.py`, the repository-root
`pytest.ini` that anchors the rootdir, and `tests/hermetic_unittest.py`, all
three `not_moved` rows that stayed here. So they run here, against this
repository's own tree. #51 records that they are not compositions: they touch
no openDox file.

RESOLVED, not left open: T007 batch E (openxFactory#1183) reversed this
file's provisional membership in `COMPOSITION_TESTS` after a Copilot finding —
it pins nothing about the composition, and that set is a PERMANENT allow-list,
so admitting it would quietly widen what every future Arc landing may touch
there, forever. It lands here instead as its own plain, non-Arc-trailered
openxFactory PR (T066's precedent) — the hermeticity-probe repair that also
repoints `tests/notebooklm/test_hermeticity_guard.py`'s stale
`find_spec("ideation_dashboard.workbench")` probe and installs the carved
reach in `tests/hermetic_unittest.py`. Two of the three cases below were RED
before that repair (P1-G decision 5, "the find_spec probe goes silent") and
are what re-measurement here is proving.

NOT PLACED AT `tests/ideation-dashboard/`, unlike the pre-shed original.
That directory is a declared `moved_paths:` prefix in
`docs/opendox-carve-manifest.yaml`, and `scripts/validate-carve-manifest.py`
refuses (`carve-file-undeclared`) any file under a `moved_paths:` prefix that
carries no manifest row — measured, and the same reason T034/T035's other
four relocated cases land under `tests/domain_profile/` instead (T007 batch
E's finding 5). `tests/domain_profile/` carries no such row and no conftest
of its own, so `REPO_ROOT` is computed locally here — the same pattern
`tests/domain_profile/test_openxfactory_profile.py` already uses — rather
than imported `from conftest import REPO_ROOT` as the openDox-code source did
(that import resolved there through `tests/ideation-dashboard/conftest.py`,
which this directory does not have). This is one of two adaptations from
#51's text; the three cases' bodies below are otherwise verbatim.

The rootdir-anchor case beside them
(`test_the_rootdir_anchor_is_what_puts_the_hookup_in_scope`) stayed in
openDox-code, rewritten for that leg's own anchor.

THE SECOND ADAPTATION, `_bare_environ()`. `test_the_bare_unittest_route_is_
detected_as_unguarded` proves nothing if its child inherits protection from
the very session proving its absence — and it does, unless corrected: THIS
file's own three tests are collected under `tests/`, so `tests/hermeticity.
py`'s session-scoped `hermetic_binary_path` fixture is ALREADY active for
the OUTER pytest process by the time any of them runs, and `subprocess.run`
inherits `os.environ` — PATH included — by default. MEASURED: the bare
`unittest discover` child then resolved `nlm` to the OUTER session's OWN
shim (not the real binary), so `shutil.which` found the marker and the
"unguarded" assertion started passing for the wrong reason — invisible
while `test_the_in_process_runners_are_the_refusals` (the OTHER guard case)
ALSO reliably errored on a bare `find_spec` for an unrelated cause (Copilot
review, PR #1195), which alone made the child report FAILED regardless.
Once that unrelated error started skipping cleanly instead, this one had
nothing left to hide behind. `_bare_environ()` strips any PATH entry under
the system temp directory — where every `tmp_path`-rooted guard shim lives
and no real installed binary ever does — so the bare route sees the PATH a
genuinely pytest-less, guard-less host would.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# --------------------------------------------------------------------------
# finding 17, wave 2 — the two routes that ran with the guard switched OFF
# --------------------------------------------------------------------------

PROBE = "tests/notebooklm/test_hermeticity_guard.py"
PROBE_DIR = "tests/notebooklm"


def _probe_run(args, *, cwd, env=None) -> subprocess.CompletedProcess:
    """Run a child interpreter over the conftest-less-directory probe.

    `-p no:cacheprovider` because this writes nothing into the real checkout, and
    the probe itself only READS `PATH` and two module attributes. `env=None`
    inherits this process's own environment, same as before — the bare-unittest
    case below is the one caller that must NOT."""
    return subprocess.run([sys.executable, *args], cwd=str(cwd),
                          capture_output=True, text=True, timeout=300, env=env)


def _bare_environ() -> dict[str, str]:
    """This process's own environment, minus any PATH entry under the system
    temp directory — see the module docstring's "SECOND ADAPTATION"."""
    env = dict(os.environ)
    tmp = tempfile.gettempdir()
    kept = [p for p in env.get("PATH", "").split(os.pathsep) if not p.startswith(tmp)]
    env["PATH"] = os.pathsep.join(kept)
    return env


def test_a_pytest_run_started_inside_a_conftestless_directory_is_guarded():
    """Residue (1) of finding 17, closed. `tests/notebooklm/` has no conftest.py of
    its own, and with no inifile anywhere a run started THERE made that directory
    the rootdir — so `confcutdir` excluded `tests/conftest.py` and neither layer of
    the guard was installed. Measured: `which nlm` resolved to a real-binary
    stand-in, three invocations landed, and the refusal ledger stayed empty.

    The repo-root `pytest.ini` anchors rootdir at the repository instead, so the
    hookup is always in the conftest chain. The oracle is the probe TestCase living
    in that directory: it asserts both layers, and it fails when the anchor is
    removed (measured in a scratch copy with a stand-in `nlm` on PATH — the
    stand-in's own text is what the assertion reports)."""
    proc = _probe_run(["-m", "pytest", "-q", "-p", "no:cacheprovider",
                       "test_hermeticity_guard.py"],
                      cwd=REPO_ROOT / PROBE_DIR)

    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "2 passed" in proc.stdout


def test_the_unittest_fallback_route_installs_the_same_guard():
    """Residue (2), closed. Before PR #49 finding 17's fix (2026-07-27),
    codexFactory's `scripts/validate-docs.sh` fell back to bare `unittest
    discover` on these tests when they lived in codexFactory and pytest was
    unavailable — a conftest fixture cannot apply to a runner that loads no
    conftests: a unittest-style probe in `tests/notebooklm/` reached the
    real-binary stand-in TWICE with no ledger entry. The fix replaced that bare
    fallback with codexFactory's own guarded runner — the original
    `tests/hermetic_unittest.py` was later copied from; the doc-health
    relocation (adopt-neutral-tooling-home, 2026-08-03) then copied it here and
    moved these tests, after which codexFactory's script stopped running them
    at all — but this tree still needs the same guarantee for any pytest-less
    host that runs it directly.

    `tests/hermetic_unittest.py` installs the same two layers from the SAME
    declarations (`install_binary_shim`, `runner_seams`), so the routes cannot
    guard different seams, and runs the identical discovery."""
    proc = _probe_run(["tests/hermetic_unittest.py", PROBE_DIR], cwd=REPO_ROOT)

    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "OK" in proc.stderr, proc.stderr        # unittest reports on stderr


def test_the_bare_unittest_route_is_detected_as_unguarded():
    """The negative control that makes the test above mean something: the SAME
    probe, run through bare `python3 -m unittest`, FAILS — which is what the gate's
    old fallback was doing silently. If this ever starts passing, either the probe
    stopped asserting anything or the guard became ambient (and then the assertion
    above proves nothing)."""
    proc = _probe_run(["-m", "unittest", "discover", "-s", PROBE_DIR,
                       "-t", PROBE_DIR, "-p", "test_hermeticity_guard.py"],
                      cwd=REPO_ROOT, env=_bare_environ())

    assert proc.returncode != 0
    assert "FAILED" in proc.stderr, proc.stderr
