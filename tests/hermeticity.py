"""Structural test hermeticity: the real `nlm` and `gh` are UNREACHABLE (FR-043).

Why this module exists. FR-043 — "Tests MUST NOT create real NotebookLM
notebooks; the adapter MUST be stubbed" — was enforced only by PER-TEST
DISCIPLINE. `cli._notebook_port()` and `serve._make_adapter()` both DEFAULT to
`workbench.NotebookAdapter()`, whose runner is a real `nlm` subprocess, so a test
that simply forgot to inject its fake reached the SHARED NotebookLM account. It
reached it SILENTLY in both directions, too: every adapter call site wraps the
runner in `except Exception` and degrades to `skipped=True` (FR-042 requires a
notebook never to block a session), so such a test passed identically whether
`nlm` was absent, present-and-failing, or present-and-succeeding. PR #49 review
finding 17 measured three tests doing exactly that — running `nlm notebook
create`, a source upload, and a `notebook delete --confirm` against the live
account. Fixing those three would not fix the class: the next test written
forgets again.

So hermeticity is made structural, in two INDEPENDENT layers:

  1. **PATH** — a shim directory is prepended to `PATH` for the whole session.
     Its `nlm` and `gh` are refusals: each prints the offending test's nodeid and
     exits non-zero. This covers every route to the binary, including a child
     process and `sync-notebooklm-books.nlm`, and it makes the suite behave the
     SAME on a host with the real binaries installed and on one without — the
     ambient-installation dependency was itself part of the defect.
  2. **the in-process seams** — `workbench._default_runner` (the one place `nlm`
     is spoken) and `session_pr.SubprocessCommandRunner.run` (the one place `gh`
     and the branch `git push` are spoken) are replaced by a refusal that RAISES.
     Layer 1 alone would be absorbed: a non-zero exit is precisely the
     degradation signal the adapter exists to swallow, so the escape would still
     pass silently.

`HermeticityViolation` derives from `BaseException` DELIBERATELY. `except
Exception` is what `NotebookAdapter` and `branch_session.open_session_notebook`
use to turn a notebook failure into a notice, and a guard those clauses catch is
a guard that no-ops. A `BaseException` propagates through them to the test runner
as a failure, which is the entire point.

What this does NOT do: it never substitutes a working fake, and it never relaxes
`available()`. A test that legitimately exercises the adapter still INJECTS its
own double explicitly — `NotebookAdapter(runner=..., available=...)`,
`FakeNotebookAdapter`, a monkeypatched `cli._notebook_port`, `adapter_factory=`,
`GhPullRequests(runner=...)`, `FakePullRequests`. Only the DEFAULTS are poisoned,
so no existing assertion is weakened and no test needs editing to stay hermetic.

Registered from EVERY `conftest.py` under `tests/`, not just the suite-wide one,
and — since wave 2 — from every pytest invocation whatever directory it starts in:
a run started inside a test directory used to make that directory the rootdir,
which cut `tests/conftest.py` out of conftest collection. The repo-root
`pytest.ini` anchors `rootdir` instead, which is why the answer is NOT "add a
conftest.py to every directory" (see `CONFTEST_HOOKUPS`).

THE THIRD ROUTE IS NOT PYTEST AT ALL. `scripts/validate-docs.sh` falls back to
`python3 -m unittest discover` when pytest is unavailable, and a fixture cannot
reach that (PR #49 review finding 17, residue 2 — measured reaching a real-binary
stand-in twice with an empty ledger). So the two layers are installable WITHOUT
pytest — `install_binary_shim` and `runner_seams`, used by the fixtures below and
by `tests/hermetic_unittest.py`, which is the runner that gate now invokes — and
`import pytest` is optional in this module BECAUSE the world it must also guard is
by definition a world without pytest.

`tests/ideation-dashboard/test_hermeticity.py` proves the guard: it asserts an
unguarded real-binary invocation is refused, pins the hookup set, and drives
`tests/notebooklm/test_hermeticity_guard.py` — a `TestCase` living in a
conftest-less directory — through both the pytest and the unittest route. Delete
the guard, the anchor or the runner and those tests fail.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

try:
    import pytest
except ModuleNotFoundError:            # pragma: no cover - the no-pytest fallback
    # The `unittest discover` world (`scripts/validate-docs.sh`). Everything above
    # the fixtures works there; the fixtures themselves are pytest's own API and
    # are simply not defined, which no caller in that world asks for.
    pytest = None

TESTS_ROOT = Path(__file__).resolve().parent
REPO_ROOT = TESTS_ROOT.parent
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

# The binaries no test may reach. `nlm` is FR-043 itself; `gh` is the same class
# of escape on the pull-request port (FR-029/FR-034 — the invoking engineer's own
# ambient credential), and it is guarded now rather than after a test forgets.
GUARDED_BINARIES = ("nlm", "gh")

# Every refusal names the requirement, so a failure is self-explaining wherever
# it surfaces — a captured stderr, a raised message, a subprocess exit.
MARKER = "FR-043"
REFUSAL_EXIT_CODE = 97

# The hookups this guard must be registered from (pinned by test_hermeticity):
# EVERY conftest.py under tests/, so no directory is guarded only by luck.
#
# Not one per directory, deliberately. `conftest` is an ambient top-level module
# name and pytest keeps exactly one of them in `sys.modules`, so ADDING a
# conftest.py to a directory hijacks that name for its siblings: a
# `tests/notebooklm/conftest.py` sorted after `tests/doc-health/` broke all 18
# doc-health modules' `from conftest import FakeGit` in `scripts/validate-docs.sh`
# (measured). Directories without a conftest are therefore guarded through
# `tests/conftest.py`, which covers every invocation whose CONFTEST CHAIN reaches
# `tests/`.
#
# WAVE 2 CLOSED THE HOLE THAT LEFT, without adding a module name: the repo-root
# `pytest.ini` anchors `rootdir` (and therefore `confcutdir`) at the repository, so
# `tests/conftest.py` is in the chain even for a run started INSIDE a conftest-less
# directory — which used to be completely unguarded (`which nlm` resolving to a
# real-binary stand-in, three invocations landed, ledger empty; measured in
# `tests/notebooklm/` and `tests/merge-master/`). See `pytest.ini` for why an
# inifile is the right instrument and a per-directory conftest is not.
CONFTEST_HOOKUPS = ("conftest.py", "doc-health/conftest.py",
                    "ideation-dashboard/conftest.py")

# The rootdir anchor's filename, pinned by test_hermeticity: without an inifile
# somewhere at or above the invocation, rootdir falls back to the arguments' common
# ancestor and the hookup above goes out of scope.
ROOTDIR_ANCHOR = "pytest.ini"

# Both layers APPEND every refusal here, so a run leaves a complete inventory of
# what tried to escape and which test tried it — the measurement the review had to
# build a private shim for. A refusal is never silent; this makes it durable too.
REFUSAL_LOG_ENV = "XF_HERMETIC_REFUSAL_LOG"

_SHIM_TEMPLATE = """#!/bin/sh
if [ -n "${{{log_env}:-}}" ]; then
  echo "{name} $* :: ${{PYTEST_CURRENT_TEST:-<unknown>}}" >> "${{{log_env}}}"
fi
echo "{marker} test hermeticity: refusing to run the real '{name}' binary." >&2
echo "  offending test: ${{PYTEST_CURRENT_TEST:-<unknown: not under pytest>}}" >&2
echo "  refused argv:   {name} $*" >&2
echo "  the suite is hermetic by construction (tests/hermeticity.py). Inject a" >&2
echo "  double at the seam instead: FakeNotebookAdapter, NotebookAdapter(runner=)," >&2
echo "  cli._notebook_port, serve adapter_factory=, or FakePullRequests." >&2
exit {code}
"""


class HermeticityViolation(BaseException):
    """A test tried to reach a real external binary.

    A `BaseException` on purpose — see this module's docstring. Every production
    call site that speaks `nlm` catches `Exception` and DEGRADES, so a guard
    raising an ordinary exception would be swallowed and the escape would stay
    invisible.

    This docstring used to assert "nothing in `scripts/ideation_dashboard/` catches
    `BaseException` or uses a bare `except:` (checked)". That went STALE inside one
    day: later repair phases added two `except BaseException` handlers
    (`branch_session._commit_gate_action_locked`, `gate_routes._abandon_session`),
    and the PR #49 completeness critic caught the prose still claiming otherwise.
    Both RE-RAISE, so the guard does still reach the runner — but a comment cannot
    check that, and a future handler that swallowed instead would disable this whole
    mechanism with a green suite. It is a TEST now, not a claim:
    `test_hermeticity.py::test_no_production_handler_swallows_a_baseexception`
    parses the package and requires every `BaseException` handler to re-raise."""


def current_test() -> str:
    """The nodeid pytest is currently running, for the refusal message."""
    return os.environ.get("PYTEST_CURRENT_TEST", "<unknown: no PYTEST_CURRENT_TEST>")


def refusal_message(binary: str, args) -> str:
    return (f"{MARKER} test hermeticity: refusing to run the real '{binary}' "
            f"binary.\n  offending test: {current_test()}\n"
            f"  refused argv:   {binary} {' '.join(str(a) for a in args)}\n"
            "  the suite is hermetic by construction (tests/hermeticity.py). "
            "Inject a double at the seam instead: FakeNotebookAdapter, "
            "NotebookAdapter(runner=), cli._notebook_port, serve "
            "adapter_factory=, or FakePullRequests.")


def refusal_log() -> Path | None:
    """Where refusals are recorded, when a session fixture has declared one."""
    declared = os.environ.get(REFUSAL_LOG_ENV)
    return Path(declared) if declared else None


def record_refusal(binary: str, args) -> None:
    """Append one refusal to the ledger. Best-effort by design: a ledger that
    cannot be written must never become the reason a refusal does not happen."""
    path = refusal_log()
    if path is None:
        return
    line = f"{binary} {' '.join(str(a) for a in args)} :: {current_test()}\n"
    try:
        with path.open("a", encoding="utf-8") as handle:
            handle.write(line)
    except OSError:
        pass


def build_shim_dir(target: Path, names=GUARDED_BINARIES) -> Path:
    """Write executable refusals for `names` into `target` and return it."""
    target.mkdir(parents=True, exist_ok=True)
    for name in names:
        script = target / name
        script.write_text(
            _SHIM_TEMPLATE.format(marker=MARKER, name=name, code=REFUSAL_EXIT_CODE,
                                  log_env=REFUSAL_LOG_ENV),
            encoding="utf-8")
        script.chmod(0o755)
    return target


def install_binary_shim(target: Path):
    """LAYER 1, installable without pytest: build the shim and put it FIRST on
    `PATH`, declaring the refusal ledger unless the environment already named one.

    Returns `(shim_dir, restore)` — `restore()` puts `PATH` and the ledger
    variable back, so the fixture below stays a fixture and the `unittest` runner
    can simply not call it (its process ends anyway)."""
    shim = build_shim_dir(Path(target))
    previous_path = os.environ.get("PATH", "")
    previous_log = os.environ.get(REFUSAL_LOG_ENV)
    os.environ["PATH"] = f"{shim}{os.pathsep}{previous_path}" if previous_path \
        else str(shim)
    if previous_log is None:
        os.environ[REFUSAL_LOG_ENV] = str(shim.parent / "refusals.log")

    def restore() -> None:
        os.environ["PATH"] = previous_path
        if previous_log is None:
            os.environ.pop(REFUSAL_LOG_ENV, None)

    return shim, restore


def runner_seams():
    """LAYER 2's targets, as ONE declaration: `(object, attribute, replacement)`.

    Both installers read this table — the fixture through `monkeypatch` (so it is
    undone per test) and `tests/hermetic_unittest.py` through `setattr` (no
    monkeypatch exists in that world) — so the two routes cannot guard different
    seams. Imported inside the function so the patch targets are the modules the
    tests themselves hold.

    TRANCHE NOTE (adopt-neutral-tooling-home tranche A): both seams live in the
    `ideation_dashboard` package, which arrives with tranche B. Until it lands
    in this repo there is nothing in-process that can speak `nlm` or `gh`, so a
    missing package yields NO seams (layer 1's PATH shim still refuses the
    binaries) rather than an import error in every test. The probe is
    `find_spec`, not try/except ImportError, because this repo's own
    `tests/ideation_dashboard/` suite directory forms a NAMESPACE package of
    the same name once `tests/` is on `sys.path` — the failure mode is then
    "cannot import name ... (unknown location)", not ModuleNotFoundError.
    Self-healing: a regular package always beats a namespace portion, so the
    moment tranche B lands `scripts/ideation_dashboard/`, `find_spec` resolves
    its submodules and both seams are guarded again with no further edit —
    and a landed package that fails to IMPORT still raises loudly."""
    from importlib.util import find_spec

    try:
        dashboard_ready = all(
            find_spec(f"ideation_dashboard.{name}") is not None
            for name in ("session_pr", "workbench"))
    except ModuleNotFoundError:
        dashboard_ready = False
    if not dashboard_ready:
        return ()

    from ideation_dashboard import session_pr as session_pr_mod
    from ideation_dashboard import workbench as workbench_mod

    return (
        (workbench_mod, "_default_runner", refuse_nlm),
        (session_pr_mod.SubprocessCommandRunner, "run", refuse_command),
    )


def refuse_nlm(*args, **kwargs):
    """Stands in for `workbench._default_runner` — the ONE place `nlm` is run."""
    record_refusal("nlm", args)
    raise HermeticityViolation(refusal_message("nlm", args))


def refuse_command(self, *args, **kwargs):
    """Stands in for `session_pr.SubprocessCommandRunner.run` — the ONE place
    `gh` and the session branch's `git push` are run. Both are refused: a push
    to a real remote is the same escape as a `gh pr create`."""
    binary = str(args[0]) if args else "<command>"
    record_refusal(binary, args[1:])
    raise HermeticityViolation(refusal_message(binary, args[1:]))


@pytest.fixture(scope="session", autouse=True)
def hermetic_binary_path(tmp_path_factory):
    """Layer 1: the real `nlm`/`gh` are not on `PATH` for the whole session.

    Yields the shim directory so a test can assert `shutil.which` resolves into
    it rather than to `/usr/local/bin`. The installation itself is
    `install_binary_shim`, shared with the `unittest` runner so the two routes
    install the same layer 1."""
    shim, restore = install_binary_shim(tmp_path_factory.mktemp("hermetic-bin"))
    try:
        yield shim
    finally:
        restore()


@pytest.fixture(autouse=True)
def hermetic_external_runners(monkeypatch, hermetic_binary_path):
    """Layer 2: the in-process default runners RAISE instead of shelling out.

    The seams come from `runner_seams()` — one declaration, two installers — and
    are set with `raising=True` so a rename of either fails this fixture loudly
    rather than leaving the suite unguarded."""
    for target, attribute, replacement in runner_seams():
        monkeypatch.setattr(target, attribute, replacement, raising=True)
