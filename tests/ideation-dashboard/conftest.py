"""Test harness for the ideation-dashboard suite.

Puts `scripts/` on the import path (so `import ideation_dashboard...` resolves)
and exposes fixture-tree locations. Mirrors tests/doc-health/conftest.py.

The branch-session harness (007-workbench-branch-sessions T001/T002) lives in
`session_fixtures.py` beside this file; its pytest fixtures are re-exported at
the bottom so `scratch_repo` / `fake_pull_requests` / `fake_notebook_adapter`
resolve by name in any test module in this directory.

The STRUCTURAL hermeticity guard (`tests/hermeticity.py`) is registered here as
well as in `tests/conftest.py`, because a targeted `pytest tests/ideation-dashboard`
run makes this directory the rootdir and pytest's `confcutdir` then excludes the
suite-wide conftest from collection — and this is the directory whose CLI verbs
reached the real `nlm` (FR-043, PR #49 finding 17).
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TESTS_ROOT = HERE.parent
REPO_ROOT = HERE.parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(TESTS_ROOT))

from hermeticity import (  # noqa: E402,F401  (autouse fixture registration)
    claim_conftest_slot,
    hermetic_binary_path,
    hermetic_external_runners,
)

FIXTURES = HERE / "fixtures"
BASE_REPO = FIXTURES / "base-repo"
NEGATIVES = FIXTURES / "negatives"

# The openxFactory validator. Since adopt-neutral-tooling-home (2026-08-03)
# this runtime lives INSIDE openxFactory, so the repo's own validator IS the
# reachable contract; the parent walk to a sibling `openxFactory/` checkout
# remains as a fallback for a checkout of the pre-relocation layout. None when
# no validator is reachable, in which case validator-backed tests skip rather
# than fail.
def find_openxfactory_validator(start: Path | None = None) -> Path | None:
    base = (start or REPO_ROOT).resolve()
    own = base / "scripts" / "validate-ideation-dashboard-contracts.py"
    if own.is_file():
        return own
    rel = Path("openxFactory") / "scripts" / "validate-ideation-dashboard-contracts.py"
    for d in [base, *base.parents]:
        candidate = d / rel
        if candidate.is_file():
            return candidate
    return None


# A stubbed git abstraction for the generator: the fixture base-repo lives INSIDE
# the openxFactory git repo, so a real `RealGit` HEAD is unstable across commits.
# Injecting FakeGit pins `generation.source_revision` and makes any derived
# `generated_at` come from a fixed committer date (never the wall clock), so
# byte-identity is testable (determinism caveat, wave-1 fixture headers).
class FakeGit:
    def __init__(self, head: str = "abcd1234" * 5,
                 date: str = "2026-07-12T00:00:00+00:00") -> None:
        self._head = head
        self._date = date

    def head_sha(self, repo) -> str:
        return self._head

    def commit_date(self, repo, revision: str) -> str:
        return self._date


# The pinned source revision every determinism/conformance test anchors on.
PINNED_REVISION = "abcd1234" * 5


# --------------------------------------------------------------------------
# add-staging-workbench: the staged-topic health fixture shapes, shared by the
# scoring tests, the readiness-gate tests and the branch-session harness so all
# of them exercise ONE definition of "ready", "blocked", and "underdone".
#
# DEFINED in `staging_shapes.py`, re-exported here (PR #49 review finding 19a):
# `session_fixtures.build_scratch_repo` needs the same shapes and used to reach
# them with `from conftest import staging_fragment` executed inside a fixture
# BODY, where the ambient `conftest` name resolves to whichever directory's
# conftest pytest imported last. Test modules keep spelling
# `from conftest import staging_fragment`, which is stable because that import
# runs at module-import time; the harness now imports the plainly named module.
# --------------------------------------------------------------------------

from staging_shapes import (  # noqa: E402,F401  (re-export, one definition)
    staging_fragment,
    thin_fragment,
)


# --------------------------------------------------------------------------
# 007-workbench-branch-sessions: the branch-session harness fixtures (T001,
# T002). Imported for their pytest-fixture side effect — every session test
# builds its world in tmp_path and never touches a real checkout (research R10).
# --------------------------------------------------------------------------

from session_fixtures import (  # noqa: E402,F401  (fixture registration)
    declared_gate_principals,
    declared_human_console,
    fake_cli_notebook,
    fake_notebook_adapter,
    fake_pull_requests,
    scratch_repo,
)


# --------------------------------------------------------------------------
# add-doxbench-editing-phase-b §12.2 — NOTHING PUSHES IMPLICITLY.
#
# ONE canonical list, because two copies of a negative drift apart silently and
# the drift is invisible by construction: both copies keep passing. §11 asserted
# the first four modules (the turn, the thread writer, the harness bridge, the
# MCP server); §12 owns the list now and adds three more — the turn assembler,
# the packet builder, and the nightly lane, which is the "periodic task" the
# requirement names.
#
# WHAT THIS LIST IS AND IS NOT, stated because the earlier wording overclaimed
# (§12 review, P3-5). It is NOT "every place in the package that could reach a
# remote". `register_edit_lane.py` is an automated lane that really does commit
# and push, and it is deliberately absent: it is pre-existing and separately
# ratified (`add-register-edit-lane`), and it pushes the aggregation-owned
# project register by explicit pathspec — never a thread, a buffer, or any
# session artifact, which is exactly what the §12 requirement scopes its
# negative to. `branch_session.py`, `session_git.py`, `session_pr.py` and
# `gate_routes.py` are absent for the plainer reason that they are the governed
# remote-write path itself.
#
# So the claim this list makes is the narrow, checkable one: none of the seven
# modules that carry a TURN, a SAVE, a COMPACTION, or a SCHEDULED doxBench task
# can reach a remote write. The SHARE verb appears nowhere here either — it
# lives in `gate_routes.py`, beside `open-pr` — and that placement is what lets
# this list stay a pure absence.
# --------------------------------------------------------------------------

NO_IMPLICIT_PUSH_MODULES: tuple[str, ...] = (
    "serve.py", "doxbench_threads.py", "doxbench_bridge.py", "doxbench_mcp.py",
    "doxbench_turns.py", "doxbench_packet.py", "nightly_lane.py",
)

FORBIDDEN_PUSH_TOKENS: tuple[str, ...] = (".push(", "open_or_update(", "git push")


# `claim_conftest_slot` re-installs THIS module as the ambient `conftest` for
# nodes under this directory only, so a multi-directory invocation
# (`pytest tests/doc-health tests/ideation-dashboard`) no longer depends on
# argument order — see its docstring in `tests/hermeticity.py` for the
# mechanism, and never add the call to `tests/conftest.py` (issue #305).
claim_conftest_slot(globals())
