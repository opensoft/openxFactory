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
# So the claim this list makes is the narrow, checkable one: none of the eight
# modules that carry a TURN, a SAVE, a COMPACTION, or a SCHEDULED doxBench task
# can reach a remote write. The SHARE verb appears nowhere here either — it
# lives in `gate_routes.py`, beside `open-pr` — and that placement is what lets
# this list stay a pure absence.
#
# WIDENED, NEVER NARROWED (`split-opendox-two-layer-product` § 2.4, OQ-1).
# `doxbench_status_exemption.py` is the lifecycle-status read carved out of
# `doxbench_packet.py`; the sweep follows the code rather than the filename, so
# splitting a listed module adds the piece that left instead of quietly
# shrinking what the negative covers. `test_doxbench_share.py` self-asserts
# that §11's four are still a subset, which is the half of this rule a test can
# keep on its own.
# --------------------------------------------------------------------------

NO_IMPLICIT_PUSH_MODULES: tuple[str, ...] = (
    "serve.py", "doxbench_threads.py", "doxbench_bridge.py", "doxbench_mcp.py",
    "doxbench_turns.py", "doxbench_packet.py", "nightly_lane.py",
    # WIDENED by `split-opendox-two-layer-product` § 2.4 (PR 2 of 4), which
    # moved the doxBench workbench routes, the project/notebook/edit routes and
    # the shared wire vocabulary out of `serve.py` into three sibling modules.
    # `serve_workbench.py` is REQUIRED here — it carries the TURN, which is
    # exactly the scope §12 names, and a list that stayed at "serve.py" would
    # have let a file move evade the absence without anything noticing. The
    # other two carry no turn, save, compaction or scheduled task, and are
    # listed anyway: the whole of the surface `serve.py` used to be is now four
    # files, and a sweep over three of them is a sweep with a seam in it.
    "serve_workbench.py", "serve_project.py", "serve_wire.py",
    # WIDENED by § 2.4 OQ-1 (PR #741, landed on `main` after this branch split
    # from it): `doxbench_status_exemption.py` is the lifecycle-status read
    # carved out of `doxbench_packet.py`, so the sweep follows the code rather
    # than the filename.
    "doxbench_status_exemption.py",
    # WIDENED AGAIN by § 2.4 (PR 3 of 4), which moved the gate console's door,
    # the projection/snapshot routes and this repository's own lane routes out
    # of `serve.py` into three more sibling modules. `serve_gate.py` is the
    # load-bearing one: `_handle_gate_action` dispatches the SESSION-BEARING
    # verbs, so a list left at PR 2's five would have let the file move evade
    # the §12 absence with nothing red. The other two carry no turn, save,
    # compaction or scheduled task and are listed for the same reason PR 2
    # listed its quiet pair — a sweep over some of the files the serve is made
    # of is a sweep with a seam in it.
    "serve_gate.py", "serve_projection.py", "serve_openxfactory_lanes.py",
)

# --------------------------------------------------------------------------
# THE SERVE SURFACE (`split-opendox-two-layer-product` § 2.4, PR 2 of 4).
#
# Several suites assert against `serve.py`'s SOURCE rather than over the wire,
# and say why at each site: a route whose alternative proof needs a live
# provider, an absence that no positive test can demonstrate, a call site whose
# enclosing `try` is the property. Those assertions are about THE SERVE, and
# the serve is now seven files rather than one.
#
# So the readers below span the whole surface. This is the same widen-never-
# narrow move `NO_IMPLICIT_PUSH_MODULES` just made, and for the same reason: an
# assertion pinned to one filename silently stops asserting the moment the code
# it was about moves to the next file along, and it keeps passing while it does
# it. Nothing here weakens an assertion — every scan sees strictly more code
# than it saw before — and a module added to the split must be added here.
# --------------------------------------------------------------------------

SERVE_SURFACE_MODULES: tuple[str, ...] = (
    "serve_wire.py", "serve_workbench.py", "serve_project.py",
    # WIDENED by § 2.4 (PR 3 of 4): the openXdox gate and projection columns and
    # the openxFactory lane column. Same rule, same direction — every scan over
    # this tuple now sees strictly more code than it saw before.
    "serve_gate.py", "serve_projection.py", "serve_openxfactory_lanes.py",
    "serve.py",
)

# `profile_openxfactory.py` is DELIBERATELY ABSENT from both this tuple and
# `NO_IMPLICIT_PUSH_MODULES` above, though PR 3 of § 2.4 makes it part of the
# serve surface too — `build_server` imports it and its `ROUTE_EXTENSIONS`
# tuple determines the whole contributed route table. It is left out because
# it is RELATIVE-IMPORT-ONLY BY DESIGN (`from . import serve_gate` etc., the
# same idiom `cli.py` uses for its own profile import — see the module's own
# docstring for why): the D12 relative-import guard these tuples feed
# (`test_serve_module_uses_no_relative_imports`) would fail on those three
# lines for a reason it does not exist to catch, so scanning it there is not
# a widening — it is asking the wrong question of the file. This is not a
# first exception: `snapshot_registry.py` is imported directly by both
# `serve.py` and `serve_projection.py` and has never been in either tuple
# either, so "every file the dashboard serve is made of" has never meant
# "every module `serve.py` transitively imports" — only "every module the
# CONTENT scans below (the credential-free walk, the hosted-session-arrival
# scan, the no-implicit-push sweep) should see."


def serve_surface_paths() -> tuple[Path, ...]:
    """Every file the dashboard serve is made of, in import-graph order.

    Dependency-first: `serve_wire.py` imports no sibling; `serve_workbench.py`,
    `serve_project.py`, `serve_gate.py` and `serve_projection.py` each import
    from `serve_wire` and from no other sibling; `serve_openxfactory_lanes.py`
    imports from `serve_projection` and from `serve_wire` NOT AT ALL any more
    (OQ-B re-plumb B-2, ruled on `#656` 2026-09-09: `hosted_ref_refused` was
    re-homed into `serve_projection.py` and the three fixed wire strings into
    the neutral `scripts/wire_messages.py`, so openxFactory's own adapter
    column stopped importing an openDox module) — which the tuple's order
    already accommodates, `serve_projection.py` sitting ahead of it;
    `serve.py` imports all six. No reader of
    `serve_surface_paths()` /
    `serve_surface_source()` depends on this particular order (every scan
    below is a per-file loop, a `.read_text()` join checked for
    substring/absence, or a `.index()` search that resolves within a single
    file's own content) — only the docstring claim above does.
    """
    runtime = REPO_ROOT / "scripts" / "ideation_dashboard"
    return tuple(runtime / name for name in SERVE_SURFACE_MODULES)


def serve_surface_source() -> str:
    """The whole serve surface as one text, for a source-level assertion.

    Concatenated with a newline between files. This guarantees only that a
    SINGLE-newline literal cannot match across a boundary that does not exist
    in any real file — each file already ends in its own trailing newline, so
    the join places TWO newlines between files, and a pattern containing a
    blank line (two consecutive newlines) can still match spuriously across a
    boundary. No assertion over this surface currently uses such a pattern.
    """
    return "\n".join(path.read_text(encoding="utf-8")
                     for path in serve_surface_paths())


FORBIDDEN_PUSH_TOKENS: tuple[str, ...] = (".push(", "open_or_update(", "git push")


# `claim_conftest_slot` re-installs THIS module as the ambient `conftest` for
# nodes under this directory only, so a multi-directory invocation
# (`pytest tests/doc-health tests/ideation-dashboard`) no longer depends on
# argument order — see its docstring in `tests/hermeticity.py` for the
# mechanism, and never add the call to `tests/conftest.py` (issue #305).
claim_conftest_slot(globals())
