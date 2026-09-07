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
     (`test_create_document_cli.py`, `test_session_verbs.py`). Those sweeps were
     closed over the WHOLE CLI because the whole CLI was one file. Six of the
     nine gate constructions and the whole gate parser tree left it, so they
     still pass over a SMALLER WORLD. Nothing went red and something was lost,
     so the rules are re-stated here over `CLI_SURFACE` — the core AND every
     module the split created — with non-vacuity floors so the mirror cannot
     itself go quiet. A rule that used to span the CLI must span it still; a
     mirror that read one column would have left the others unswept.

  3. **RE-EXPORT COMPLETENESS.** `build_parser` sets `func=` to the moved
     functions and the suite asserts `args.func is cli_mod.cmd_gate_edit_document`.
     Rather than re-listing the names a future move might forget, the parser is
     WALKED and every dispatchable verb is required to be the same object on the
     core module.

  4. **THE TWO DOCUMENTED INVOCATIONS.** `cli.py`'s own docstring says it runs
     both as a script and with `-m`, and in both the file is loaded under the
     name `__main__` — while a moved verb reaches the core through `_core()`,
     which imports `ideation_dashboard.cli`. That is a SECOND module object,
     with its own `RepoRootRefused` and `GeneratedAtRefused` classes, and the
     `except` clauses in one copy's `main` cannot catch the other copy's
     exception: every refusal degraded to a traceback the moment a raising verb
     moved out. No in-process test can see it — `main([...])` called from the
     suite has only ever one module object — so this file runs the CLI as an
     OPERATOR runs it, in a real process, in both invocations.
"""

from __future__ import annotations

import argparse
import ast
import inspect
import os
import re
import subprocess
import sys
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

#: THE WHOLE CLI SURFACE: the core, the three columns, and the composition
#: point. The closed-world sweeps in section 2 read THIS tuple and not one file,
#: because that is what the rules they mirror used to mean — before the split
#: `cli.py` WAS the command line, so a sweep over `cli.py` was closed over all
#: of it. Add a module to the CLI and add it here; a sweep that reads a subset
#: of the surface is a sweep that has quietly stopped being closed-world.
CLI_SURFACE = (cli_mod, *COLUMN_MODULES, profile_openxfactory)

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
#: this file mirrors (`test_create_document_cli.py`, `test_session_verbs.py`) —
#: their union, applied to the whole surface.
#:
#: `--content` is spelled WITHOUT the trailing space the landed sweeps carry.
#: `"--content "` cannot match a declaration (`add_argument("--content", ...)`
#: has no space before the closing quote), so as a bare substring it matched
#: nothing at all — while a bare `"--content"` would have matched
#: `--content-file`, the flag the rule deliberately KEEPS. The boundary, not the
#: space, is what the rule means: see `declares_flag` below.
BYPASS_FLAGS = ("--force", "--override", "--overwrite", "--no-record",
                "--skip-gate", "--no-gate", "--content", "--delete",
                "--token", "--gh-token", "--github-token", "--merge",
                "--approve", "--admin", "--auto-merge", "--squash")

#: The two names `test_trust_gaps.py`'s sweep exempts, carried over verbatim:
#: they ARE the authentication (`_session_identity_gate` runs `_gate_actor`), so
#: requiring them to call themselves would be circular. Every other function on
#: the surface that builds a gate must reach one of them.
AUTHENTICATORS = ("_gate_actor", "_session_identity_gate")


def source_of(module) -> str:
    return Path(module.__file__).read_text(encoding="utf-8")


def declares_flag(source: str, flag: str) -> bool:
    """True when `flag` appears as a WHOLE option string, not as a prefix.

    `--content-file` is not `--content`; `--no-gate` is not `--no-gate-x`. The
    boundary is the rule, and it is why the sweep can be widened without
    inheriting the landed spelling's blind spot."""
    return re.search(re.escape(flag) + r"(?![-\w])", source) is not None


# ===========================================================================
# 1. late binding — the failure that would have been GREEN
# ===========================================================================

#: Every spelling of the core module, both package paths. `tests/import_scan.py`
#: carries the same two-spelling rationale: this tree is importable as
#: `ideation_dashboard.x` (with `scripts/` on the path, which `cli.py` arranges)
#: and as `scripts.ideation_dashboard.x`, and a rule that knows only one of them
#: is a rule with a hole in it.
CORE_MODULE_PATHS = ("ideation_dashboard.cli", "scripts.ideation_dashboard.cli",
                     "cli")
CORE_PACKAGE_PATHS = ("ideation_dashboard", "scripts.ideation_dashboard")


def names_the_core_eagerly(node) -> bool:
    """True when `node` is an import statement that BINDS the core module.

    Four spellings, because the hazard is the binding and not the syntax:
    `import ideation_dashboard.cli`, `from ideation_dashboard.cli import X`,
    `from .cli import X` (relative, `module == "cli"`), and — the one the first
    version of this scan missed, and Copilot caught on PR #742 —
    `from ideation_dashboard import cli`, which is an `ImportFrom` on the
    PACKAGE with `cli` among its names, so neither of the other two branches
    saw it."""
    if isinstance(node, ast.Import):
        return any(alias.name in CORE_MODULE_PATHS for alias in node.names)
    if isinstance(node, ast.ImportFrom):
        if node.module in CORE_MODULE_PATHS:
            return True
        # `from ideation_dashboard import cli` and its relative form
        # `from . import cli` (module is None when the import is purely
        # relative).
        if node.module in CORE_PACKAGE_PATHS or (
                node.module is None and node.level):
            return any(alias.name == "cli" for alias in node.names)
    return False


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
            if names_the_core_eagerly(node) and node.col_offset == 0:
                offenders.append(f"{Path(module.__file__).name}:{node.lineno}")
    assert offenders == [], (
        "a column module imports the core at module level; the spine reference "
        "would freeze at import and stop honouring every "
        f"`monkeypatch.setattr(cli_mod, ...)` in the suite: {offenders}")


def test_the_eager_import_scan_sees_every_spelling_of_the_core():
    """The scan above is only as good as the forms it knows, and the form it
    first missed — `from ideation_dashboard import cli` — is the one a
    contributor is most likely to write, because it is how every OTHER import in
    these modules is spelled (`from ideation_dashboard import gate_console as
    gate_mod`). Each spelling is parsed and put to the scan here, so the rule
    cannot silently narrow to the syntax somebody happened to try."""
    forbidden = (
        "import ideation_dashboard.cli",
        "import scripts.ideation_dashboard.cli",
        "from ideation_dashboard.cli import _human_gate",
        "from scripts.ideation_dashboard.cli import _human_gate",
        "from ideation_dashboard import cli",
        "from ideation_dashboard import cli as _core_module",
        "from . import cli",
        "from .cli import _human_gate",
    )
    for line in forbidden:
        node = ast.parse(line).body[0]
        assert names_the_core_eagerly(node), line
    allowed = (
        "from ideation_dashboard import gate_console as gate_mod",
        "from ideation_dashboard import cli_gate",
        "from ideation_dashboard.boundary import HumanGate",
        "import argparse",
    )
    for line in allowed:
        node = ast.parse(line).body[0]
        assert not names_the_core_eagerly(node), line


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


def test_every_cli_function_that_builds_a_gate_authenticates_its_actor_first():
    """`test_trust_gaps.py`'s closed-world rule, re-stated over the WHOLE CLI
    SURFACE rather than over one file.

    That test scans `cli.py` and covered all nine constructions, because all
    nine were in `cli.py`. Six moved. Reading only the file they moved TO would
    reproduce the same defect one column over: `cli_project.py` and
    `cli_model_binding.py` build no gate today, and nothing would notice the day
    one of them did. So the sweep spans `CLI_SURFACE`: every function anywhere
    on the command line that builds a `HumanGate` must, in its own body, either
    authenticate the actor (`_gate_actor`) or first run the session identity
    gate, which authenticates. The calls read `_core()._gate_actor(...)` in the
    columns — the same control, reached through the core — so the substring pin
    holds across the move."""
    offenders = []
    for module in CLI_SURFACE:
        source = source_of(module)
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            body = ast.get_source_segment(source, node) or ""
            if "HumanGate(" not in body:
                continue
            if node.name in AUTHENTICATORS:
                continue
            if any(f"{name}(" in body for name in AUTHENTICATORS):
                continue
            offenders.append(f"{Path(module.__file__).name}:{node.name}")
    assert offenders == [], (
        "these CLI functions build a HumanGate without authenticating the "
        f"actor claim first: {offenders}")


def test_the_surface_wide_gate_scan_is_not_vacuous():
    """The floor the surface-wide sweep needs and the single-file original never
    had to state, because `cli.py` was self-evidently full of gates. A sweep
    over a world that stopped containing its subject passes for the wrong
    reason, so the count is pinned where the split left it: nine constructions
    in total, exactly the nine `cli.py` held before it — three that stayed on
    the authentication rail and six that moved with the verbs."""
    found = {Path(module.__file__).name: gate_constructions(module)
             for module in CLI_SURFACE}
    total = sum(len(names) for names in found.values())
    assert total >= 9, (
        f"the gate-construction scan found only {total} constructions across "
        f"the whole CLI surface — the sweep above has lost its subject: {found}")
    assert len(found["cli_gate.py"]) >= 6, found
    assert len(found["cli.py"]) >= 3, found


def test_no_verb_on_this_command_line_offers_a_bypass_flag():
    """`test_create_document_cli.py`'s and `test_session_verbs.py`'s flag sweeps,
    re-stated the same way and for the same reason: the `gate` parser tree left
    `cli.py`, so a bypass flag added to it would no longer be swept by either.

    One list over the whole surface — the rule was never per-verb, and it was
    never per-file either."""
    offenders = []
    for module in CLI_SURFACE:
        source = source_of(module)
        for flag in BYPASS_FLAGS:
            if declares_flag(source, flag):
                offenders.append(f"{Path(module.__file__).name}: {flag}")
    assert offenders == [], (
        "no flag on this command line may skip the gate, the confinement, the "
        f"record, or the review: {offenders}")


def declared_options(parser, path: str = "") -> list[str]:
    """`gate open-pr --token`-shaped labels for every option the tree declares."""
    out = []
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            for name, sub in action.choices.items():
                out.extend(declared_options(sub, f"{path} {name}".strip()))
        else:
            out.extend(f"{path} {opt}".strip() for opt in action.option_strings)
    return out


def test_the_assembled_parser_declares_no_bypass_flag():
    """The same rule read off the PARSER instead of the source — and the form
    that cannot be spelled around.

    A source sweep knows only the files it is pointed at; this one walks what
    `build_parser` actually assembled, so it covers a flag declared in any
    module, in any spelling, including one a CONTRIBUTED extension adds through
    the subcommand point. The two forms answer different questions — the source
    sweep catches a flag written down anywhere, this catches a flag that reaches
    the command line — and neither subsumes the other."""
    declared = declared_options(cli_mod.build_parser())
    offenders = [opt for opt in declared if opt.split()[-1] in BYPASS_FLAGS]
    assert offenders == [], (
        "these options reach the assembled command line and each of them would "
        f"skip the gate, the confinement, the record, or the review: {offenders}")
    assert len(declared) >= 250, (
        f"the option walk found only {len(declared)} declarations — it is no "
        "longer reaching the whole tree")


def test_the_flag_sweep_still_covers_the_verbs_it_claims_to():
    """Non-vacuity for the source sweep: the module it reads must really hold
    the parser tree it is protecting.

    PARSED, not grepped. Asserting `'"gate"' in source` and counting the literal
    `gsub.add_parser(` made the floor depend on the quote style and on a local
    variable keeping its name — a rename would have turned a true claim red, and
    this file uses AST everywhere else for exactly that reason (see
    `test_no_column_module_imports_the_core_eagerly`). The claim is a SHAPE: the
    `gate` subcommand and its verb tree are declared in `cli_gate.py`."""
    tree = ast.parse(source_of(cli_gate))
    added = [node for node in ast.walk(tree)
             if isinstance(node, ast.Call)
             and isinstance(node.func, ast.Attribute)
             and node.func.attr == "add_parser"]
    assert len(added) >= 15, (
        f"only {len(added)} add_parser calls in cli_gate.py — the gate "
        "subparser tree is no longer there")
    assert [node for node in added
            if node.args and isinstance(node.args[0], ast.Constant)
            and node.args[0].value == "gate"], (
        "cli_gate.py no longer declares the `gate` subcommand itself")
    assert [node for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "add_subparsers"], (
        "cli_gate.py no longer opens the gate verb tree")


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


# ===========================================================================
# 4. the two documented invocations — the SECOND core module, and how it is
#    kept from existing
# ===========================================================================

SCRIPT = PACKAGE / "cli.py"


def run_cli(mode: str, argv: list[str], cwd: Path):
    """The command line as an OPERATOR runs it: a real process, in one of the
    two invocations `cli.py`'s own docstring documents.

    In-process (`cli_mod.main([...])`, which every other CLI test uses) there is
    exactly one `ideation_dashboard.cli` and the hazard below cannot appear —
    which is why it went unnoticed until it was run."""
    command = ([sys.executable, str(SCRIPT)] if mode == "script"
               else [sys.executable, "-m", "ideation_dashboard.cli"])
    env = dict(os.environ, PYTHONPATH=str(REPO_ROOT / "scripts"))
    return subprocess.run(command + argv, capture_output=True, text=True,
                          cwd=str(cwd), env=env)


@pytest.mark.parametrize("mode", ["script", "module"])
def test_a_refused_repo_root_is_reported_and_not_raised(mode, tmp_path):
    """THE REGRESSION THIS SECTION EXISTS FOR.

    `cmd_generate` moved to `cli_project.py`, which reaches the core through
    `_core()` — `ideation_dashboard.cli`. Run as a script or with `-m`, `cli.py`
    is ALSO loaded as `__main__`, so `RepoRootRefused` existed twice and the
    `except RepoRootRefused` in `__main__.main` could not catch the instance
    `ideation_dashboard.cli` raised. The refusal — whose whole job is to say, in
    one operator-facing message, that `--repo-root` names the wrong tree — came
    out as a traceback instead.

    The message is not decoration: `corpus_root_refusal` prints the shape a
    correct invocation has, because the failure it addresses is a path-namespace
    confusion that a traceback tells the operator nothing about."""
    empty = tmp_path / "not-a-corpus"
    empty.mkdir()
    snapshot = tmp_path / "snapshot.json"

    result = run_cli(mode, ["generate", "--repo-root", str(empty),
                            "--repository", "openxFactory",
                            "--output", str(snapshot)], tmp_path)

    assert result.returncode == 1, result.stderr
    assert "--repo-root is not a corpus checkout" in result.stderr
    assert "Traceback" not in result.stderr, result.stderr
    assert not snapshot.exists(), "a refused run left a snapshot behind"


@pytest.mark.parametrize("mode", ["script", "module"])
def test_a_malformed_generated_at_is_reported_and_not_raised(mode, tmp_path):
    """The second refusal raised from the same moved chokepoint, and the same
    story: `GeneratedAtRefused` is REFUSED rather than degraded precisely so the
    operator sees why, and a traceback is not that."""
    snapshot = tmp_path / "snapshot.json"

    result = run_cli(mode, ["generate", "--repo-root", str(REPO_ROOT),
                            "--repository", "openxFactory",
                            "--generated-at", "not-a-date",
                            "--output", str(snapshot)], tmp_path)

    assert result.returncode == 1, result.stderr
    assert "--generated-at is not an RFC 3339 date-time" in result.stderr
    assert "Traceback" not in result.stderr, result.stderr
    assert not snapshot.exists()


@pytest.mark.parametrize("mode", ["script", "module"])
def test_a_contributed_verb_is_reachable_in_both_documented_invocations(
        mode, tmp_path):
    """The contributed column, through a real process rather than through an
    assertion ABOUT a real process.

    The suite quotes `python3 scripts/ideation_dashboard/cli.py ...` in refusal
    text and runbooks in five places and never once runs it, so an import shape
    that only breaks outside pytest — a half-initialised `cli_gate` under the
    script invocation, say — would have been green everywhere."""
    result = run_cli(mode, ["gate", "ratify", "--help"], tmp_path)

    assert result.returncode == 0, result.stderr
    assert "usage: ideation-dashboard gate ratify" in result.stdout
    assert "--change-id" in result.stdout
    assert result.stderr == ""


def test_the_script_bootstrap_runs_the_packages_copy_of_this_module():
    """The STRUCTURAL half of the same claim, so the fix cannot be undone by a
    tidy-up that looks harmless.

    `if __name__ == "__main__": sys.exit(main())` is the obvious line and it is
    the wrong one HERE: it dispatches into `__main__`'s own `main`, whose
    `except` clauses name `__main__`'s exception classes, while every moved verb
    raises the package copy's. The entrypoint therefore imports the package's
    module and calls ITS `main` — one module object doing the work, in every
    invocation."""
    tree = ast.parse(source_of(cli_mod))
    blocks = [node for node in tree.body
              if isinstance(node, ast.If)
              and isinstance(node.test, ast.Compare)
              and isinstance(node.test.left, ast.Name)
              and node.test.left.id == "__name__"
              and any(isinstance(c, ast.Constant) and c.value == "__main__"
                      for c in node.test.comparators)]
    assert len(blocks) == 1, "cli.py has no single `__main__` bootstrap"
    block = blocks[0]

    bound = [alias.asname or alias.name
             for node in ast.walk(block) if isinstance(node, ast.ImportFrom)
             and node.module in CORE_PACKAGE_PATHS
             for alias in node.names if alias.name == "cli"]
    assert bound, (
        "the bootstrap does not import the package's own copy of this module, "
        "so running the file dispatches into `__main__` — a second module "
        "object whose exception classes are not the ones the moved verbs raise")

    through = [node for node in ast.walk(block)
               if isinstance(node, ast.Call)
               and isinstance(node.func, ast.Attribute)
               and node.func.attr == "main"
               and isinstance(node.func.value, ast.Name)
               and node.func.value.id in bound]
    assert len(through) == 1, (
        "the bootstrap must call `main` on the package module it imported")
    assert not [node for node in ast.walk(block)
                if isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "main"], (
        "the bootstrap calls this module's own `main`; run as a script that is "
        "`__main__.main`, and its `except RepoRootRefused` cannot catch the "
        "`ideation_dashboard.cli.RepoRootRefused` a moved verb raises")
