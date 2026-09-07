"""The SUBCOMMAND EXTENSION POINT (`split-opendox-two-layer-product` § 2.4,
PR 1 of 4).

The route point's twin, and the assertions mirror it:

  1. **A contributed subcommand is dispatched by the same line as a core one.**
     The extension attaches to the SAME subparsers action, sets `func` the same
     way, and `main()` reaches it through the unchanged `args.func(args)` — no
     clause of its own, no wrapper, no second dispatch. That is what makes this
     a profile of the command line rather than a fork of it
     (`domain-descendant-boundary`: *A descendant carries profile, never fork*).
  2. **Without extensions the parser is unchanged.** Asserted here on the
     top-level command set and the shape of `main`'s dispatch; asserted on the
     help TEXT of all 31 entry points, byte for byte, by
     `test_extension_point_parity.py`.
  3. **The interface is neutral and closed** — imports neither package (an AST
     scan over `tests/import_scan.py`), and has exactly one member.

WHAT IS DELIBERATELY NOT DEFENDED, recorded because it is a decision and not an
oversight: an extension is handed the real subparsers action and could, in
principle, reach past its own subcommand and mutate the parser. It is CODE THE
COMMAND LINE WAS ASSEMBLED WITH, not input, and a wrapper that could only ever
be a partial defence would buy the appearance of one. What IS defended is the
honest failure — an object that does not conform is refused where it is wired.
"""

from __future__ import annotations

import argparse
import sys

import pytest

from conftest import REPO_ROOT

sys.path.insert(0, str(REPO_ROOT / "tests"))

import subcommand_extension  # noqa: E402
from import_scan import imported_modules, names_a_forbidden_package  # noqa: E402

from ideation_dashboard import cli as cli_mod  # noqa: E402

MODULE = REPO_ROOT / "scripts" / "subcommand_extension.py"

#: The top-level command set as it stands, in DECLARATION order — which is the
#: order `argparse` prints in the usage line, so this is the observable order
#: and not an incidental one.
CORE_COMMANDS = ("generate", "generate-and-open", "create", "edit",
                 "model-binding", "gate")

#: Both spellings of both packages, for the reason `tests/import_scan.py`
#: states in its own header: `scripts/__init__.py` exists, so a one-spelling
#: forbidden list is a hole.
FORBIDDEN = ("ideation_dashboard", "scripts.ideation_dashboard",
             "doc_health", "scripts.doc_health")


class ProbeExtension:
    """A conforming extension: one subcommand, one `func`, nothing else.

    Structural conformance — it subclasses nothing and imports nothing from the
    command line it extends, which is the property the Protocol exists for.
    """

    def __init__(self, name="probe-verb", record=None):
        self.name = name
        self.record = record if record is not None else []

    def register(self, subparsers):
        parser = subparsers.add_parser(self.name, help="a contributed verb")
        parser.add_argument("--subject", required=True,
                            help="what this contributed verb acts on")
        parser.set_defaults(func=self._run)

    def _run(self, args):
        self.record.append(args.subject)
        return 0


class NotAnExtension:
    """Conforms to nothing. Named for what it is, so the refusal reads."""


def top_level_commands(parser):
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            return tuple(action.choices)
    raise AssertionError("the parser has no subcommands at all")


# ---------------------------------------------------------------------------
# 1. neutrality
# ---------------------------------------------------------------------------


def test_the_extension_point_imports_neither_package():
    """It travels to openDox with the carve, where the checker package does not
    exist. PARSED, not grepped: this module NAMES both packages in prose."""
    offenders = [f"{MODULE.name}:{line} imports {module!r}"
                 for module, line in imported_modules(MODULE)
                 if names_a_forbidden_package(module, FORBIDDEN)]
    assert offenders == [], (
        "the subcommand extension point must import NEITHER reader package. "
        f"Offending imports: {offenders}")


def test_the_extension_point_imports_only_the_standard_library():
    third_party = [f"{module} (line {line})"
                   for module, line in imported_modules(MODULE)
                   if module.split(".")[0] not in sys.stdlib_module_names]
    assert third_party == [], (
        f"the extension point imports non-stdlib modules: {third_party}")


def test_the_neutrality_scan_would_catch_the_import_it_is_meant_to_catch(tmp_path):
    """The negative control, because the scans above prove an ABSENCE."""
    scratch = tmp_path / "would_be_offender.py"
    scratch.write_text(
        "from ideation_dashboard import cli\n"
        "import doc_health\n"
        "import argparse\n", encoding="utf-8")
    caught = [m for m, _ in imported_modules(scratch)
              if names_a_forbidden_package(m, FORBIDDEN)]
    assert caught == ["ideation_dashboard", "doc_health"], caught


# ---------------------------------------------------------------------------
# 2. closure
# ---------------------------------------------------------------------------


def test_the_protocol_is_closed_at_its_declared_members():
    assert set(subcommand_extension.SubcommandExtension.__protocol_attrs__) == \
        set(subcommand_extension.MEMBERS)


def test_every_member_is_a_method_so_both_checks_work():
    """A non-method member would keep `isinstance` and silently take
    `issubclass` away from every consumer."""
    assert isinstance(ProbeExtension(), subcommand_extension.SubcommandExtension)
    assert issubclass(ProbeExtension, subcommand_extension.SubcommandExtension)
    assert not isinstance(NotAnExtension(),
                          subcommand_extension.SubcommandExtension)


def test_a_non_conforming_extension_is_refused_where_it_is_wired():
    with pytest.raises(subcommand_extension.SubcommandExtensionError):
        cli_mod.build_parser(subcommand_extensions=(NotAnExtension(),))


# ---------------------------------------------------------------------------
# 3. without extensions, the parser is unchanged
# ---------------------------------------------------------------------------


def test_the_default_parser_carries_exactly_the_core_commands():
    assert top_level_commands(cli_mod.build_parser()) == CORE_COMMANDS


def test_the_default_is_an_empty_tuple_and_not_a_mutable_default():
    """A list default would be one shared object every caller could append to —
    and a parser that grew a subcommand from a previous invocation is the
    hardest kind of bug to see."""
    import inspect
    default = inspect.signature(
        cli_mod.build_parser).parameters["subcommand_extensions"].default
    assert default == ()
    assert isinstance(default, tuple)
    main_default = inspect.signature(
        cli_mod.main).parameters["subcommand_extensions"].default
    assert main_default == () and isinstance(main_default, tuple)


def test_registering_no_extensions_over_a_parser_changes_nothing():
    parser = cli_mod.build_parser()
    before = top_level_commands(parser)
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            subcommand_extension.register_all((), action)
    assert top_level_commands(parser) == before


# ---------------------------------------------------------------------------
# 4. with an extension: registered, parsed, and dispatched by the core line
# ---------------------------------------------------------------------------


def test_a_contributed_subcommand_is_added_after_every_core_one():
    """Core first, contributed last — so the help reads core-first and a
    contributed name can never displace a core one (`argparse` refuses a
    duplicate outright, which is the right direction of that refusal)."""
    extension = ProbeExtension()
    parser = cli_mod.build_parser(subcommand_extensions=(extension,))
    assert top_level_commands(parser) == CORE_COMMANDS + ("probe-verb",)


def test_extensions_register_in_declaration_order():
    """`argparse` lists subcommands in the order they were added, so the tuple
    an entrypoint declares is the order the help text reads in."""
    parser = cli_mod.build_parser(subcommand_extensions=(
        ProbeExtension("probe-a"), ProbeExtension("probe-b")))
    assert top_level_commands(parser) == CORE_COMMANDS + ("probe-a", "probe-b")


def test_a_contributed_subcommand_parses_its_own_arguments():
    extension = ProbeExtension()
    parser = cli_mod.build_parser(subcommand_extensions=(extension,))
    args = parser.parse_args(["probe-verb", "--subject", "a-document"])
    assert args.command == "probe-verb"
    assert args.subject == "a-document"
    assert args.func == extension._run


def test_a_contributed_subcommand_enforces_its_own_required_arguments(capsys):
    parser = cli_mod.build_parser(subcommand_extensions=(ProbeExtension(),))
    with pytest.raises(SystemExit):
        parser.parse_args(["probe-verb"])
    assert "--subject" in capsys.readouterr().err


def test_main_dispatches_a_contributed_subcommand_by_the_core_line():
    """THE POINT: `args.func(args)` is unchanged, and it reaches the
    contributed verb. No clause was added to the dispatch, so a contributed
    command cannot acquire behaviour a core one does not have."""
    seen = []
    extension = ProbeExtension(record=seen)
    code = cli_mod.main(["probe-verb", "--subject", "a-document"],
                        subcommand_extensions=(extension,))
    assert code == 0
    assert seen == ["a-document"]


def test_main_without_extensions_still_refuses_an_unknown_command(capsys):
    """The contributed verb exists only where it was declared: a `main()` built
    with no extensions does not know the name at all."""
    with pytest.raises(SystemExit):
        cli_mod.main(["probe-verb", "--subject", "a-document"])
    assert "probe-verb" in capsys.readouterr().err


def test_a_contributed_subcommand_may_carry_its_own_sub_subcommands():
    """The `gate` tree's shape, contributed: the extension is handed the real
    subparsers action, so nothing stops it building the same depth the core
    builds — which is what PR 4 needs for the 19-verb gate tree."""

    class NestedExtension:
        def register(self, subparsers):
            parent = subparsers.add_parser("probe-tree", help="a contributed tree")
            child = parent.add_subparsers(dest="probe_command", required=True)
            leaf = child.add_parser("leaf", help="a contributed leaf verb")
            leaf.set_defaults(func=lambda args: 7)

    parser = cli_mod.build_parser(subcommand_extensions=(NestedExtension(),))
    args = parser.parse_args(["probe-tree", "leaf"])
    assert args.probe_command == "leaf"
    assert args.func(args) == 7
