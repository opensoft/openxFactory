"""ZERO BEHAVIOUR CHANGE, asserted rather than claimed
(`split-opendox-two-layer-product` § 2.4, PR 1 of 4).

The extension points land BEFORE anything is extracted through them, which is
the only sequencing under which "nothing moved" is checkable at all: this PR
adds one clause to each dispatch and one keyword to each builder, and the whole
of its risk is that the clause or the keyword changed something on the way in.
So both surfaces get a golden, taken from `origin/main` BEFORE the wiring was
written and pinned here:

  1. **The command line**, as its own help text, for the root parser and every
     one of its 30 subcommands and sub-subcommands. Text, not a hash: a golden
     whose failure says only "the digest differs" is a golden nobody can act on,
     and the whole reason to snapshot a parser is that the diff names the
     argument that moved. Pinned at `COLUMNS=100`, because `argparse` wraps to
     the terminal and a golden that depended on the runner's terminal width
     would be a flake, not a proof.

  2. **The route dispatch table**, as the ORDERED arms of `_route` and
     `do_POST` that branch on the request path, each with the handler methods
     it reaches — read out of the syntax tree, so the assertion is about the
     dispatch itself and not about a line number or a comment above it.

WHY THE DISPATCH TABLE IS READ AND NOT EXERCISED. Every core route already has
behavioural tests, and this file must not become a second, worse copy of them.
What those tests cannot see is an arm that quietly moved: reordering
`/source`'s prefix arm above an exact sibling, or dropping an arm whose own test
happens to be skipped in this environment, changes the TABLE while every
surviving test still passes. Order is the property here, so order is what is
pinned.

WHY THE EXTENSION CLAUSE IS EXCLUDED BY A RULE AND NOT BY A COUNT. The core arms
are exactly those that branch on `path`; the contributed-route clause branches on
whether a binding matched. That is a real distinction and not a convenience —
the core dispatch is a fixed table of paths, and the extension point is
deliberately not one — so the scan keeps working when the clause is edited, and
still fails when a core arm is. The clause's own presence is asserted separately
below, so it cannot be deleted without this file noticing either.
"""

from __future__ import annotations

import argparse
import ast
import http.server

import pytest

from conftest import FIXTURES, REPO_ROOT  # noqa: F401  (sys.path side effect)

from carved_reach import source as carved_source

from opendox import cli as cli_mod

# POST-SHED (§ 5.2, RULED (a)): `serve.py` is a moved row; this parity test is a
# `stays_openxfactory_adapter` row that still reads the serve's SOURCE TEXT.
SERVE = carved_source("scripts/ideation_dashboard/serve.py")

#: The width the golden was taken at. `argparse` asks `shutil.get_terminal_size`,
#: which honours `COLUMNS`, so pinning it makes the snapshot a property of the
#: parser rather than of the runner.
GOLDEN_COLUMNS = "100"

#: Where the golden lives. Text, for a readable diff — see the module docstring.
HELP_GOLDEN = FIXTURES / "cli-help-tree.golden.txt"

#: Non-vacuity floor for the walk. Measured at 31 entry points (the root, six
#: top-level subcommands, nineteen `gate` verbs and five `model-binding` verbs);
#: the floor sits below that so an ordinary deletion does not fail the build,
#: while a walk that lost the subcommand tree does.
MIN_ENTRY_POINTS = 25

# ---------------------------------------------------------------------------
# THE PINNED CORE DISPATCH TABLE, taken from origin/main at 0f9361e0.
#
# Each entry is (the arm's test as source, the handler methods it reaches,
# sorted). Sorted rather than in call order because the walk that collects them
# is a tree walk: a set that changed is the finding, and an ordering that
# depended on the shape of an `if` inside an arm would be noise.
# ---------------------------------------------------------------------------

# NARROWED ONCE, DELIBERATELY, BY § 2.4 PR 3 OF 4 — the one legitimate edit to
# this pinned table, disclosed in that PR's body.
#
# PR 3 moved four read arms and five write arms OUT of the fixed tables and
# registered them as contributed `RouteBinding`s instead (`serve_gate.py`,
# `serve_projection.py`, `serve_openxfactory_lanes.py`, assembled in
# `profile_openxfactory.py`). The pin therefore records the new FIXED set. It is
# the same assertion at the same strength: every surviving arm keeps its exact
# position, its exact test source and its exact reached-name set, so a
# reordering, a retargeting or a silent drop still fails here. What left is not
# untested — `test_serve_column_split.py` pins the contributed table the same
# way, tuple for tuple, and each moved write route has its own off-loopback
# parity test.
#
# `path == self.snapshot_route` STAYS. Its test is a per-server class attribute
# fed by `build_server(snapshot_route=…)`, and a `RouteBinding.pattern` is a
# frozen string — contributing that route would have broken the keyword in
# silence. The HANDLER moved to `serve_projection.py` with its neighbours; the
# ARM did not, and this line is where that decision is visible.
ROUTE_ARMS = (
    ("path == self.snapshot_route", ("_serve_snapshot",)),
    ("path == PROJECT_REGISTER_ROUTE", ("_serve_project_register",)),
    ("path == CAPABILITIES_ROUTE",
     ("_send_json", "_serve_bytes", "_session_repository",
      "_trusted_console_host")),
    ("path == WORKBENCH_MODEL_CATALOG_ROUTE",
     ("_handle_workbench_model_catalog",)),
    ("path == WORKBENCH_MODEL_INTAKE_ROUTE",
     ("_handle_workbench_model_intake_surface",)),
    ("path == WORKBENCH_THREAD_ROUTE", ("_handle_workbench_thread",)),
)

DO_POST_ARMS = (
    ("path == ACTIONS_NOTEBOOK_ROUTE", ("_handle_notebook_action",)),
    ("path == ACTIONS_EDIT_ROUTE", ("_handle_edit_action",)),
    ("path == ACTIONS_WORKBENCH_CHAT_TURN_ROUTE",
     ("_handle_workbench_chat_turn",)),
    ("path == ACTIONS_WORKBENCH_DOCUMENT_ABSTRACT_ROUTE",
     ("_handle_workbench_document_abstract",)),
    ("path == ACTIONS_WORKBENCH_MODEL_INTAKE_ROUTE",
     ("_handle_workbench_model_intake",)),
    ("path == ACTIONS_WORKBENCH_MODEL_APPROVAL_ROUTE",
     ("_handle_workbench_model_approval",)),
)


# ---------------------------------------------------------------------------
# the parser walk
# ---------------------------------------------------------------------------


def walk_parser(parser, path):
    """Every entry point in a parser tree, depth-first, subcommands sorted.

    Sorted rather than in `argparse`'s own declaration order on purpose: the
    golden must fail when an argument or a help string changes, and must NOT
    fail merely because a subcommand was declared in a different place in the
    builder. Declaration order is asserted where it is actually observable —
    in the root parser's own usage line, which is part of the golden text.
    """
    yield " ".join(path), parser.format_help()
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            for name, sub in sorted(action.choices.items()):
                yield from walk_parser(sub, path + [name])


def help_tree(parser) -> str:
    chunks = [f"===== {name} =====\n{text}"
              for name, text in walk_parser(parser, ["ideation-dashboard"])]
    return "\n".join(chunks)


@pytest.fixture
def pinned_columns(monkeypatch):
    monkeypatch.setenv("COLUMNS", GOLDEN_COLUMNS)


def test_the_help_text_of_every_entry_point_is_unchanged(pinned_columns):
    """The golden: the whole parser tree's help, byte for byte.

    `build_parser()` with no extensions must produce exactly what it produced
    before the extension point existed. The keyword defaults to `()` and the
    registration call is a no-op over an empty tuple, so any diff here is a real
    change to the command line — which this PR promised not to make.
    """
    got = help_tree(cli_mod.build_parser())
    expected = HELP_GOLDEN.read_text(encoding="utf-8")
    if got != expected:
        # A pytest assertion over 50KB of text prints unusably; name the entry
        # points that differ, which is what a reader needs first.
        def sections(text):
            out, name = {}, None
            for line in text.splitlines(keepends=True):
                if line.startswith("===== ") and line.rstrip().endswith(" ====="):
                    name = line.strip().strip("= ").strip()
                    out[name] = []
                elif name is not None:
                    out[name].append(line)
            return {k: "".join(v) for k, v in out.items()}

        mine, theirs = sections(got), sections(expected)
        added = sorted(set(mine) - set(theirs))
        removed = sorted(set(theirs) - set(mine))
        changed = sorted(k for k in set(mine) & set(theirs) if mine[k] != theirs[k])
        pytest.fail(
            "the command line changed, and this PR's whole claim is that it did "
            f"not. Entry points added: {added}; removed: {removed}; changed: "
            f"{changed}. Regenerate the golden ONLY with a ruling that the "
            f"change is intended: {HELP_GOLDEN}")


def test_the_parser_walk_actually_reaches_the_subcommand_tree(pinned_columns):
    """Non-vacuity. A walk that found only the root would also find no diff."""
    names = [name for name, _ in walk_parser(cli_mod.build_parser(),
                                             ["ideation-dashboard"])]
    assert len(names) >= MIN_ENTRY_POINTS, (
        f"only {len(names)} entry points walked (floor {MIN_ENTRY_POINTS}) — "
        f"the golden above is asserting over almost nothing. Walked: {names}")
    # the three levels the tree actually has, so a collapse to two is caught
    assert "ideation-dashboard gate ratify" in names
    assert "ideation-dashboard model-binding add" in names


def test_the_golden_was_taken_at_the_pinned_width(monkeypatch):
    """A golden that silently depended on the runner's terminal is a flake.

    Taking the same tree at a DIFFERENT width must produce different text —
    otherwise `COLUMNS` is not what pinned it and the fixture above proves less
    than it appears to.
    """
    monkeypatch.setenv("COLUMNS", GOLDEN_COLUMNS)
    at_pinned = help_tree(cli_mod.build_parser())
    monkeypatch.setenv("COLUMNS", "60")
    at_narrow = help_tree(cli_mod.build_parser())
    assert at_pinned != at_narrow, (
        "help text did not change with COLUMNS — the golden's width pin is not "
        "doing anything, and the fixture may have been taken at whatever width "
        "the authoring terminal had")


# ---------------------------------------------------------------------------
# the route dispatch table
# ---------------------------------------------------------------------------


def _handler_class_node():
    tree = ast.parse(SERVE.read_text(encoding="utf-8"), filename=str(SERVE))
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == "DashboardHandler":
            return node
    raise AssertionError(f"no DashboardHandler in {SERVE}")


def _method(name):
    for node in _handler_class_node().body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    raise AssertionError(f"DashboardHandler has no {name}()")


def _branches_on_path(node) -> bool:
    return any(isinstance(n, ast.Name) and n.id == "path" for n in ast.walk(node))


def core_arms(method_name):
    """The ordered core dispatch arms of one method, with what each reaches.

    A core arm is a top-level `if` whose TEST branches on the request path —
    the fixed table. The contributed-route clause branches on whether a binding
    matched and is deliberately not one of these; see the module docstring.
    """
    arms = []
    for stmt in _method(method_name).body:
        if not isinstance(stmt, ast.If) or not _branches_on_path(stmt.test):
            continue
        reached = sorted({
            n.func.attr for n in ast.walk(stmt)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
            and isinstance(n.func.value, ast.Name) and n.func.value.id == "self"
        })
        arms.append((ast.unparse(stmt.test), tuple(reached)))
    return tuple(arms)


@pytest.mark.parametrize("method_name,pinned", [
    ("_route", ROUTE_ARMS),
    ("do_POST", DO_POST_ARMS),
])
def test_the_core_dispatch_table_is_unchanged(method_name, pinned):
    """The fixed arms, in order, each reaching what it reached at 0f9361e0."""
    assert core_arms(method_name) == pinned, (
        f"the fixed core dispatch of {method_name}() changed. This PR adds ONE "
        "clause after the last core arm and before the fallback, and moves "
        "nothing: an arm that was reordered, retargeted or dropped is either a "
        "mistake or a decision that belongs in its own PR with its own ruling.")


@pytest.mark.parametrize("method_name", ["_route", "do_POST"])
def test_each_dispatch_consults_the_extension_point_exactly_once(method_name):
    """The clause exists, once, and it is the LAST thing before the fallback.

    Placement is the whole safety argument (`route_extension`'s docstring): the
    core arms have already returned, so a contributed route cannot shadow one,
    and the fallback still runs for a path no binding claims. A clause that
    drifted upward would silently invert both halves of that.
    """
    body = _method(method_name).body
    consults = [i for i, stmt in enumerate(body)
                if any(isinstance(n, ast.Attribute) and n.attr == "match"
                       and isinstance(n.value, ast.Name)
                       and n.value.id == "route_extension"
                       for n in ast.walk(stmt))]
    assert len(consults) == 1, (
        f"{method_name}() consults route_extension.match {len(consults)} times; "
        "the extension point is one clause, and two would mean two dispatch "
        "orders nobody can read")
    # everything after the consult is the FALLBACK, never another path arm
    after = body[consults[0]:]
    assert not any(isinstance(stmt, ast.If) and _branches_on_path(stmt.test)
                   for stmt in after[1:]), (
        f"{method_name}() branches on the request path AFTER the extension "
        "point. A core arm below the clause can be shadowed by a contributed "
        "route, which is exactly the ordering the seam promises cannot happen.")


def test_the_dispatch_scan_would_notice_a_moved_arm():
    """The negative control, because the two assertions above prove an ABSENCE.

    A scan pointed at the wrong method, or one whose arm rule stopped matching,
    would return `()` and keep passing forever against a pinned `()`. So: a
    hand-built dispatch with a reordered arm must come back reordered.
    """
    source = (
        "class DashboardHandler:\n"
        "    def _route(self, head_only):\n"
        "        if path == B_ROUTE:\n"
        "            self._serve_b(head_only)\n"
        "            return True\n"
        "        if path == A_ROUTE:\n"
        "            self._serve_a(head_only)\n"
        "            return True\n"
        "        matched = route_extension.match(self.route_bindings, 'GET', path)\n"
        "        if matched is not None:\n"
        "            return True\n"
        "        return False\n"
    )
    tree = ast.parse(source)
    fn = tree.body[0].body[0]
    arms = []
    for stmt in fn.body:
        if isinstance(stmt, ast.If) and _branches_on_path(stmt.test):
            reached = sorted({
                n.func.attr for n in ast.walk(stmt)
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                and isinstance(n.func.value, ast.Name)
                and n.func.value.id == "self"})
            arms.append((ast.unparse(stmt.test), tuple(reached)))
    assert arms == [("path == B_ROUTE", ("_serve_b",)),
                    ("path == A_ROUTE", ("_serve_a",))], arms
    assert arms != [("path == A_ROUTE", ("_serve_a",)),
                    ("path == B_ROUTE", ("_serve_b",))], (
        "the arm reader is order-insensitive — the pinned table above would "
        "not catch a reordering, which is the failure it exists for")


# ---------------------------------------------------------------------------
# the mixin base order (`split-opendox-two-layer-product` § 2.4, PR 2 of 4)
# ---------------------------------------------------------------------------
#
# PR-2's own decision 1 states, as a safety property, that "the mixins precede
# `SimpleHTTPRequestHandler` so `do_GET` resolution is unchanged" — a claim
# about MRO order that nothing enforced. Today it is unobservable either way:
# `WorkbenchRoutes` and `ProjectRoutes` share zero member names with the whole
# `http.server` chain, so the order the base list is written in does not yet
# change what any name resolves to. The exposure is a LATER member added to
# either mixin that happens to share a name with something up the chain
# (`send_head`, `list_directory`, `log_message`, `translate_path`,
# `guess_type`, `do_GET`, `end_headers`, …) — it would silently lose to
# `http.server` with nothing red. Both halves of decision 1 are pinned below:
# the order itself, and the disjointness that makes today's order harmless.


def test_the_mixins_precede_simplehttprequesthandler_in_the_mro():
    """Decision 1's ordering claim, checked rather than taken on faith.

    WIDENED by § 2.4 PR 3 of 4, never narrowed: the base list grew from two
    mixins to five (`serve_gate.GateRoutes`, `serve_projection.ProjectionRoutes`
    and `serve_openxfactory_lanes.LaneRoutes` joined PR 2's pair), so the pinned
    prefix grew with it. The property is unchanged and strictly stronger — every
    mixin must still precede `SimpleHTTPRequestHandler`, and now the ORDER OF
    ALL FIVE is pinned rather than of two.

    RESPELLED, NOT RELAXED, for the § 4.1 INVERSION. Two of the five bases are
    openXdox's columns, and openDox-code stopped naming openXdox at class-
    definition time: `DashboardHandler` now mixes
    `consumer_reach.LateGateRoutes` and `consumer_reach.LateProjectionRoutes`,
    the late `route_column` stand-ins that carry the same methods and resolve
    to the real classes on first CALL. A stand-in class brings its own shared
    base (`_LateConsumerColumn`) into the MRO with it, so the pinned prefix is
    eight entries rather than seven. Both halves of the original claim are
    still asserted and one is added: the order of the five columns is pinned,
    every one of them still precedes `SimpleHTTPRequestHandler`, and the two
    stand-ins are checked to BE the gate and projection columns — by the
    module and class each declares it stands in for — so a stand-in pointed at
    the wrong column fails here rather than at a route.
    """
    from opendox import serve as serve_mod
    from ideation_dashboard import serve_openxfactory_lanes
    from opendox import consumer_reach, serve_project, serve_workbench
    from openxdox import serve_gate, serve_projection

    mro = serve_mod.DashboardHandler.__mro__
    assert mro[:8] == (
        serve_mod.DashboardHandler,
        serve_workbench.WorkbenchRoutes,
        serve_project.ProjectRoutes,
        consumer_reach.LateGateRoutes,
        consumer_reach.LateProjectionRoutes,
        consumer_reach._LateConsumerColumn,
        serve_openxfactory_lanes.LaneRoutes,
        http.server.SimpleHTTPRequestHandler,
    ), (
        "DashboardHandler's MRO no longer starts "
        "(DashboardHandler, WorkbenchRoutes, ProjectRoutes, LateGateRoutes, "
        "LateProjectionRoutes, _LateConsumerColumn, LaneRoutes, "
        "SimpleHTTPRequestHandler) — decision 1's ordering claim no longer "
        "holds, and a mixin member sharing a name with the http.server chain "
        f"would now resolve to the WRONG implementation. Got: {mro[:8]}")
    # The two stand-ins ARE the openXdox columns they name, so the respelling
    # above did not quietly drop a column out of the chain.
    assert repr(consumer_reach.LateGateRoutes).count("GateRoutes")
    assert serve_gate.GateRoutes.__name__ == "GateRoutes"
    assert serve_projection.ProjectionRoutes.__name__ == "ProjectionRoutes"
    for late, real in ((consumer_reach.LateGateRoutes, serve_gate.GateRoutes),
                       (consumer_reach.LateProjectionRoutes,
                        serve_projection.ProjectionRoutes)):
        for name in ("_handle_gate_action", "_serve_source"):
            if hasattr(real, name):
                assert hasattr(late, name), (
                    f"{late.__name__} does not carry {name}, which "
                    f"{real.__name__} defines — the stand-in is not standing "
                    "in for the column it names")


def _non_dunder(names) -> set[str]:
    """Every name in `names` that is not a Python dunder (`__x__`).

    A hand-picked exclusion list (`__module__`, `__doc__`, ...) goes stale the
    moment either side of the comparison grows a dunder the list did not name
    — `WorkbenchRoutes` already carries `__annotations__` (from its
    `INTAKE_QUERY_FIELDS: tuple[str, ...]` class annotation), and a future
    stdlib release could add one to the `http.server` chain. Excluding by the
    dunder RULE means the test can only fail for a reason it exists to catch.
    """
    return {name for name in names
            if not (name.startswith("__") and name.endswith("__"))}


def _http_server_chain_members() -> set[str]:
    chain_members: set[str] = set()
    for klass in http.server.SimpleHTTPRequestHandler.__mro__:
        chain_members |= set(vars(klass))
    return chain_members


def test_the_mixins_share_no_member_name_with_the_http_server_chain():
    """Decision 1's safety property. Ordering alone does not prove there is no
    collision TODAY — it only proves which side wins if there is one. This
    proves there is none, which is what makes the order currently unobservable
    and therefore safe. A future member added to either mixin that collides
    with the chain must fail HERE, not resolve silently to the wrong method.
    """
    from ideation_dashboard import serve_openxfactory_lanes
    from opendox import serve_project, serve_workbench
    from openxdox import serve_gate, serve_projection

    # WIDENED by § 2.4 PR 3 of 4 with the three columns it added: the sweep
    # follows the mixins, so a member added to any of the five is checked.
    # Dunder exclusion is by RULE (`_non_dunder`), not a hand-listed set —
    # kept from the base branch's independent hardening (see `_non_dunder`'s
    # own docstring for why a hand-picked list goes stale).
    raw_mixin_members: set[str] = set()
    for mixin in (serve_workbench.WorkbenchRoutes, serve_project.ProjectRoutes,
                  serve_gate.GateRoutes, serve_projection.ProjectionRoutes,
                  serve_openxfactory_lanes.LaneRoutes):
        raw_mixin_members |= set(vars(mixin))
    mixin_members = _non_dunder(raw_mixin_members)
    assert mixin_members, (
        "no non-dunder members found on the five route mixins — that means "
        "this reader is looking at the wrong classes, not proving "
        "disjointness against the http.server chain")
    chain_members = _non_dunder(_http_server_chain_members())
    collisions = sorted(mixin_members & chain_members)
    assert not collisions, (
        f"the serve mixins now share member(s) {collisions} with "
        "the http.server chain (BaseRequestHandler -> BaseHTTPRequestHandler "
        "-> StreamRequestHandler -> SimpleHTTPRequestHandler). The mixins are "
        "listed BEFORE SimpleHTTPRequestHandler in DashboardHandler's base "
        "list, so a collision here means the mixin's version silently wins — "
        "if that is intended, name it explicitly; if not, rename the member.")


def test_the_collision_check_would_notice_a_real_collision():
    """The negative control: an empty intersection could also mean the reader
    is looking at the wrong classes entirely. Prove it fires on a real name."""
    class _FakeMixin:
        def send_head(self):  # a real SimpleHTTPRequestHandler method name
            ...

    chain_members = _non_dunder(_http_server_chain_members())
    collisions = _non_dunder(set(vars(_FakeMixin))) & chain_members
    assert collisions == {"send_head"}, (
        "the collision check does not fire on a real shared method name, "
        "which means the two tests above could pass on a broken reader "
        "forever")
