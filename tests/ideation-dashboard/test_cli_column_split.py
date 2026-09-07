"""THE CLI SPLIT, and the three things it could have broken silently
(`split-opendox-two-layer-product` § 2.4, PR 4 of 4).

`cli.py`'s verbs moved into three column modules — `cli_gate.py` (openXdox,
contributed through the subcommand extension point), `cli_project.py` and
`cli_model_binding.py` (openDox, fixed core) — while the shared spine stayed
put. The parser is byte-identical (`test_extension_point_parity.py`'s golden)
and every existing behavioural test passes unmodified, which is most of the
proof. This file covers what neither of those can see:

  1. **LATE BINDING.** A moved verb reaches the spine through `_core()`,
     resolved when it RUNS. Written as `from ideation_dashboard.cli import
     _notebook_port` instead, the reference would freeze at import and the
     thirteen `monkeypatch.setattr(cli_mod, ...)` sites the suite injects fakes
     through would stop reaching the verb — with every test still green. That is
     the failure mode this refactor has to avoid above all others, so it is
     asserted twice: structurally (no such import exists) and LIVE (a patch on
     the core is observed inside a moved body).

  2. **THE SCANS THAT LOST THEIR SUBJECT.** Three landed tests are closed-world
     sweeps over `cli.py`'s own source — every `HumanGate` construction
     authenticates first (`test_trust_gaps.py`), and no bypass flag exists
     (`test_create_document_cli.py`, `test_session_verbs.py`). Six of the nine
     gate constructions and the whole gate parser tree left that file, so those
     sweeps still pass over a SMALLER WORLD. Nothing went red and something was
     lost: the same rules are mirrored here over the modules the surface moved
     to, with a non-vacuity floor so the mirror cannot itself go quiet.

  3. **RE-EXPORT COMPLETENESS.** `build_parser` sets `func=` to the moved
     functions and the suite asserts `args.func is cli_mod.cmd_gate_edit_document`.
     Rather than re-listing the names a future move might forget, the parser is
     WALKED and every dispatchable verb is required to be the same object on the
     core module.
"""

from __future__ import annotations

import argparse
import ast
import inspect
from pathlib import Path

import pytest

from conftest import REPO_ROOT

import subcommand_extension
from ideation_dashboard import cli as cli_mod
from ideation_dashboard import cli_gate, cli_model_binding, cli_project
from ideation_dashboard import profile_openxfactory

PACKAGE = REPO_ROOT / "scripts" / "ideation_dashboard"

#: The modules the § 2.4 CLI split created. `profile_openxfactory` is the
#: composition point and is deliberately allowed to name the core's siblings;
#: the three COLUMN modules are the ones that must not reach back eagerly.
COLUMN_MODULES = (cli_gate, cli_project, cli_model_binding)

#: The shared spine: DEFINED in `cli.py`, reached by the moved verbs at call
#: time, and patched by name in the existing suite. Every entry here is a
#: module-level patch site somewhere under `tests/ideation-dashboard/`.
SPINE = (
    "_gate_actor", "_gate_snapshot", "_human_gate", "_lens_gate",
    "_commission_cli", "_parse_pairs", "_notebook_port", "_pull_request_port",
    "_session_identity_gate", "_session_registry", "_session_repository_key",
    "_unwind_cli_session", "cli_provenance", "console_presence",
    "human_console_present", "_generate_and_write", "_report", "_validate",
    "_locate_validator",
)

#: The one patch site that is an IMPORTED name rather than a defined one:
#: `test_lens_gate_cli.py` and `test_wheel_verbs_cli.py` patch
#: `cli.generate_snapshot`, and it works because the only reader is
#: `_gate_snapshot`, which reads it out of `cli`'s own globals. Move that reader
#: and the patch stops reaching the gate verbs, so the reader is what is pinned.
SPINE_READ_THROUGH = {"generate_snapshot": "_gate_snapshot"}

#: The flags no verb on this command line may offer, from the two landed sweeps
#: this file mirrors (`test_create_document_cli.py`, `test_session_verbs.py`).
BYPASS_FLAGS = ("--force", "--override", "--overwrite", "--no-record",
                "--skip-gate", "--no-gate", "--content ", "--delete",
                "--token", "--gh-token", "--github-token", "--merge",
                "--approve", "--admin", "--auto-merge", "--squash")


def source_of(module) -> str:
    return Path(module.__file__).read_text(encoding="utf-8")


# ===========================================================================
# 1. late binding — the failure that would have been GREEN
# ===========================================================================

def test_no_column_module_imports_the_core_eagerly():
    """The structural half. A module-level import of the core would bind the
    spine ONCE, at import time; `_core()` binds it per call.

    Parsed rather than grepped, for `tests/import_scan.py`'s own reason: the
    forbidden thing is an import statement, and a string search cannot tell one
    from the prose that documents it — this module's docstring names the exact
    import it forbids."""
    offenders = []
    for module in COLUMN_MODULES:
        tree = ast.parse(source_of(module))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module in (
                    "ideation_dashboard.cli", "cli") and node.col_offset == 0:
                offenders.append(f"{Path(module.__file__).name}:{node.lineno}")
            if isinstance(node, ast.Import) and node.col_offset == 0:
                for alias in node.names:
                    if alias.name in ("ideation_dashboard.cli", "cli"):
                        offenders.append(
                            f"{Path(module.__file__).name}:{node.lineno}")
    assert offenders == [], (
        "a column module imports the core at module level; the spine reference "
        "would freeze at import and stop honouring every "
        f"`monkeypatch.setattr(cli_mod, ...)` in the suite: {offenders}")


def test_the_core_module_is_resolved_at_call_time_not_at_import_time():
    """The other half of the same claim, stated as the mechanism: `_core()` is a
    FUNCTION on each column module and it returns the live core module."""
    for module in (cli_gate, cli_project):
        assert inspect.isfunction(module._core), module.__name__
        assert module._core() is cli_mod, module.__name__
    # the third module reaches nothing at all, and so declares no accessor
    assert not hasattr(cli_model_binding, "_core")


def test_a_patch_on_the_core_reaches_a_moved_gate_verb(monkeypatch, tmp_path):
    """The LIVE proof, and the one that would have caught a frozen reference.

    `cmd_gate_ratify` moved to `cli_gate.py` and builds its gate through the
    core's `_human_gate`. Patching that name on `cli` — exactly what
    `test_lens_gate_cli.py` and the session suites do to inject fakes — must be
    observed inside the moved body."""
    class Reached(Exception):
        pass

    def _patched(repo_root, args):
        raise Reached

    monkeypatch.setattr(cli_mod, "_human_gate", _patched)
    args = argparse.Namespace(repo_root=str(tmp_path), actor="brett",
                              records_dir="records", change_id="add-demo",
                              ratifier=None, date=None)
    with pytest.raises(Reached):
        cli_gate.cmd_gate_ratify(args)


def test_a_patch_on_the_core_reaches_a_moved_project_verb(monkeypatch, tmp_path):
    """The same proof on the other column: `cmd_generate` moved to
    `cli_project.py` and writes through the core's one generation chokepoint."""
    class Reached(Exception):
        pass

    monkeypatch.setattr(cli_mod, "_generate_and_write",
                        lambda args, output: (_ for _ in ()).throw(Reached()))
    args = argparse.Namespace(output=str(tmp_path / "snapshot.json"),
                              repo_root=str(tmp_path))
    with pytest.raises(Reached):
        cli_project.cmd_generate(args)


def test_the_spine_itself_did_not_move():
    """A patch site is only a patch site while the name is DEFINED here.

    Every name below must be an attribute of `cli` whose function object was
    written in `cli.py` — not re-exported from a column module, which would put
    the definition somewhere a `setattr` on `cli` cannot reach."""
    misplaced = []
    for name in SPINE:
        obj = getattr(cli_mod, name, None)
        if obj is None:
            misplaced.append(f"{name}: absent from cli.py")
        elif inspect.getsourcefile(obj) != cli_mod.__file__:
            misplaced.append(f"{name}: defined in {inspect.getsourcefile(obj)}")
    for name, reader in SPINE_READ_THROUGH.items():
        assert getattr(cli_mod, name, None) is not None, name
        fn = getattr(cli_mod, reader)
        if inspect.getsourcefile(fn) != cli_mod.__file__:
            misplaced.append(f"{name}: its only reader {reader} left cli.py")
        elif f"{name}(" not in inspect.getsource(fn):
            misplaced.append(f"{name}: {reader} no longer reads it")
    assert misplaced == [], (
        "these shared-spine names are no longer defined in cli.py, so a "
        f"`monkeypatch.setattr(cli_mod, ...)` on them reaches nothing: {misplaced}")


# ===========================================================================
# 2. the sweeps that followed the surface out of cli.py
# ===========================================================================

def gate_constructions(module) -> list[str]:
    """Every function in `module` that builds a `HumanGate` in its own body."""
    source = source_of(module)
    tree = ast.parse(source)
    return [node.name for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and "HumanGate(" in (ast.get_source_segment(source, node) or "")]


def test_every_moved_gate_verb_still_authenticates_its_actor_first():
    """`test_trust_gaps.py`'s closed-world rule, MIRRORED over the file the gate
    verbs moved to.

    That test scans `cli.py` and covered nine constructions; six of them are
    here now, and its scan keeps passing over what is left. The rule is the
    thing that must not move, so it is restated over the new surface: every
    function that builds a `HumanGate` either authenticates the actor
    (`_gate_actor`) or first runs the session identity gate, which
    authenticates. The calls read `_core()._gate_actor(...)` here — the same
    control, reached through the core — so the substring pin holds."""
    source = source_of(cli_gate)
    tree = ast.parse(source)
    offenders = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        body = ast.get_source_segment(source, node) or ""
        if "HumanGate(" not in body:
            continue
        if "_gate_actor(" in body or "_session_identity_gate(" in body:
            continue
        offenders.append(node.name)
    assert offenders == [], (
        f"these cli_gate.py functions build a HumanGate without authenticating "
        f"the actor claim first: {offenders}")


def test_the_mirrored_gate_scan_is_not_vacuous():
    """The floor the mirror needs and the original never had to state, because
    `cli.py` was self-evidently full of gates. A sweep over a file that stopped
    containing its subject passes for the wrong reason: this pins the count at
    the six constructions that moved, so deleting or relocating them fails HERE
    rather than going quiet."""
    found = gate_constructions(cli_gate)
    assert len(found) >= 6, (
        f"the gate-construction scan found only {found} in cli_gate.py — the "
        "sweep above has lost its subject")


def test_no_moved_verb_offers_a_bypass_flag():
    """`test_create_document_cli.py`'s and `test_session_verbs.py`'s flag sweeps,
    mirrored the same way and for the same reason: the `gate` parser tree left
    `cli.py`, so a bypass flag added to it would no longer be swept by either.

    One list over all three column modules — the rule was never per-verb."""
    offenders = []
    for module in COLUMN_MODULES:
        source = source_of(module)
        for flag in BYPASS_FLAGS:
            if flag in source:
                offenders.append(f"{Path(module.__file__).name}: {flag}")
    assert offenders == [], (
        "no flag on this command line may skip the gate, the confinement, the "
        f"record, or the review: {offenders}")


def test_the_flag_sweep_still_covers_the_verbs_it_claims_to():
    """Non-vacuity for the sweep above: the modules it reads must really hold
    the parser tree it is protecting."""
    gate_source = source_of(cli_gate)
    assert '"gate"' in gate_source and "add_subparsers" in gate_source
    assert gate_source.count("gsub.add_parser(") >= 15, (
        "the gate subparser tree is no longer in cli_gate.py")


# ===========================================================================
# 3. the contribution, and the re-exports that keep the move invisible
# ===========================================================================

def test_the_gate_verbs_reach_the_parser_as_a_conforming_extension():
    """openXdox's column contributes rather than being wired in: the object the
    profile declares conforms STRUCTURALLY, without `cli_gate.py` importing the
    interface — which is the whole reason it is a `Protocol`."""
    extension = cli_gate.GateSubcommands()
    assert isinstance(extension, subcommand_extension.SubcommandExtension)
    # parsed, not grepped: the header names the interface it conforms to, and a
    # test that forbade describing the rule would be a bad test
    imports = [node for node in ast.walk(ast.parse(source_of(cli_gate)))
               if isinstance(node, (ast.Import, ast.ImportFrom))]
    assert not [n for n in imports
                if "subcommand_extension" in (getattr(n, "module", "") or "")
                or any("subcommand_extension" in a.name for a in n.names)], (
        "cli_gate.py imports the extension interface; conformance here is "
        "STRUCTURAL, which is what lets the column travel to a repository "
        "where that module is not the one it was written against")
    assert len(profile_openxfactory.SUBCOMMAND_EXTENSIONS) == 1
    assert isinstance(profile_openxfactory.SUBCOMMAND_EXTENSIONS[0],
                      cli_gate.GateSubcommands)


def test_the_gate_tree_registers_at_the_ordinal_it_always_had():
    """The contribution is registered where the call it replaced stood, so
    `gate` is still the last top-level command and `model-binding` still
    precedes it. `test_extension_point_parity.py` holds the byte-level proof;
    this states the ORDER as its own claim, because order is what the ordinal
    argument is about."""
    parser = cli_mod.build_parser()
    names = [name for action in parser._actions
             if isinstance(action, argparse._SubParsersAction)
             for name in action.choices]
    assert names[-2:] == ["model-binding", "gate"], names


def dispatchable(parser) -> list:
    """Every `func` a parse of this tree can dispatch to, depth first."""
    out = list(parser.get_default("func") and [parser.get_default("func")] or [])
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            for sub in action.choices.values():
                out.extend(dispatchable(sub))
    return out


def test_every_dispatchable_verb_is_the_same_object_on_the_core_module():
    """RE-EXPORT COMPLETENESS, walked rather than listed.

    `args.func is cli_mod.cmd_gate_edit_document` is asserted by name in the
    session suites; this generalises it, so a verb that moves out of `cli.py`
    without a re-export fails here instead of in whichever suite happens to
    name it."""
    missing = []
    for func in dispatchable(cli_mod.build_parser()):
        if getattr(cli_mod, func.__name__, None) is not func:
            missing.append(f"{func.__name__} ({func.__module__})")
    assert missing == [], (
        "these dispatchable verbs are not reachable as the same object on "
        f"`cli`, so an `args.func is cli.<name>` assertion would fail: {missing}")


def test_the_dispatch_walk_is_not_vacuous():
    """The walk must find the whole command line, not one arm of it."""
    found = dispatchable(cli_mod.build_parser())
    assert len(found) >= 28, f"only {len(found)} verbs walked"
    # all three column modules, plus `cli` itself — which still holds
    # `cmd_generate_and_open`, the CLI's assembly point (see cli_project.py's
    # header for why composition stays in the core).
    assert {f.__module__ for f in found} == {
        "ideation_dashboard.cli", "ideation_dashboard.cli_gate",
        "ideation_dashboard.cli_project",
        "ideation_dashboard.cli_model_binding"}, (
        f"the verb columns moved: {sorted({f.__module__ for f in found})}")
