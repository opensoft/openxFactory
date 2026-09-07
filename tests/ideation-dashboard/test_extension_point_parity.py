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

import pytest

from conftest import FIXTURES, REPO_ROOT

from ideation_dashboard import cli as cli_mod

SERVE = REPO_ROOT / "scripts" / "ideation_dashboard" / "serve.py"

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

ROUTE_ARMS = (
    ("path == self.snapshot_route", ("_serve_snapshot",)),
    ("path == SNAPSHOT_INDEX_ROUTE", ("_serve_index",)),
    ("path == PROJECT_REGISTER_ROUTE", ("_serve_project_register",)),
    ("path == COMMITTED_INTENTS_ROUTE", ("_serve_committed_intents",)),
    ("path == CAPABILITIES_ROUTE",
     ("_send_json", "_serve_bytes", "_session_repository",
      "_trusted_console_host")),
    ("path == WORKBENCH_MODEL_CATALOG_ROUTE",
     ("_handle_workbench_model_catalog",)),
    ("path == WORKBENCH_MODEL_INTAKE_ROUTE",
     ("_handle_workbench_model_intake_surface",)),
    ("path == WORKBENCH_THREAD_ROUTE", ("_handle_workbench_thread",)),
    ("path.startswith(SOURCE_PREFIX)", ("_serve_source",)),
    ("path == '/source' or path == '/source/'", ("send_error",)),
)

DO_POST_ARMS = (
    ("path == ACTIONS_NOTEBOOK_ROUTE", ("_handle_notebook_action",)),
    ("path == ACTIONS_REFRESH_ROUTE", ("_handle_refresh_action",)),
    ("path == ACTIONS_DTN_SEED_ROUTE", ("_handle_dtn_seed",)),
    ("path == ACTIONS_STAGING_SEED_ROUTE", ("_handle_staging_seed",)),
    ("path == ACTIONS_APPLY_REGISTER_EDITS_ROUTE",
     ("_handle_apply_register_edits",)),
    ("path == ACTIONS_EDIT_ROUTE", ("_handle_edit_action",)),
    ("path == ACTIONS_WORKBENCH_CHAT_TURN_ROUTE",
     ("_handle_workbench_chat_turn",)),
    ("path == ACTIONS_WORKBENCH_DOCUMENT_ABSTRACT_ROUTE",
     ("_handle_workbench_document_abstract",)),
    ("path == ACTIONS_WORKBENCH_MODEL_INTAKE_ROUTE",
     ("_handle_workbench_model_intake",)),
    ("path == ACTIONS_WORKBENCH_MODEL_APPROVAL_ROUTE",
     ("_handle_workbench_model_approval",)),
    ("path.startswith(ACTIONS_GATE_PREFIX)", ("_handle_gate_action",)),
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
