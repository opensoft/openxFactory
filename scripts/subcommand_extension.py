"""The subcommand extension point: how a layer above the command line
CONTRIBUTES a subcommand instead of forking the parser
(`split-opendox-two-layer-product` § 2.4, design § D2).

The route extension point's twin, and it exists for the same reason D2 gives:
the command line "splits the same way, with openXdox contributing subcommands".
Without it the integration layer copies `build_parser` — a fork rather than a
profile, which is the rule `domain-descendant-boundary` states one level down
(*A descendant carries profile, never fork*: what the profile cannot express is
an upstream change, "rather than a local edit"). A copied parser is the worst
kind of fork, too, because the copy keeps working while it drifts: two spellings
of one command, and the help text stops being a description of anything.

WHY THIS MODULE SITS AT THE TOP OF `scripts/` AND BELONGS TO NEITHER PACKAGE.
The three justifications `corpus_adapter.py` records, unchanged: both sides of
the eventual carve consume it, it travels with the carve to a repository where
the checker package does not exist, and it therefore imports NOTHING from either
package — stdlib and `typing` only, asserted by PARSING
(`tests/ideation-dashboard/test_subcommand_extension.py`, over
`tests/import_scan.py`) rather than left as a property of the current body.

WHY A `runtime_checkable` `Protocol` AND NOT AN ABC: so an extension authored in
the repository that pins this one conforms structurally, without importing
anything from here. Same argument, same precedent
(`corpus_adapter.CorpusAdapter`, `doxbench_model.WorkbenchModelPort`).

CLOSED MEMBERSHIP, ONE MEMBER, AND IT IS A METHOD, so `MEMBERS` is a closure a
companion test reads `__protocol_attrs__` against, and `isinstance` and
`issubclass` both work.

WHAT `register` RECEIVES, AND WHY IT IS THE SUBPARSERS ACTION ITSELF. An
extension is handed the SAME `argparse` subparsers action every core subcommand
is added through, and attaches with the same two calls — `add_parser(...)` and
`set_defaults(func=...)`. Nothing is wrapped, adapted or re-declared, so:

  * the dispatch needs no clause of its own — the entrypoint still calls
    `args.func(args)`, and a contributed command is dispatched by the identical
    line as a core one;
  * `--help` composes for free, including the contributed rows, because there is
    one parser and it is the real one;
  * a contributed command cannot acquire an argument shape the core parser
    cannot express, which is the analogue of the route point's "no privileged
    route": one parser, one dispatch, no side door.

The cost of that directness is that an extension could, in principle, reach past
its own subcommand and mutate the parser it was handed. That is not defended
against here, and deliberately so: an extension is CODE THE SERVER WAS ASSEMBLED
WITH, not input, and a wrapper that could only be a partial defence would buy
nothing but the appearance of one. What is defended is the honest failure — an
object that does not conform is refused where it is wired, not discovered when a
command line is parsed.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

#: The closed member set. A companion test reads
#: `SubcommandExtension.__protocol_attrs__` against this tuple, so growing the
#: surface is a two-file act somebody has to mean.
MEMBERS: tuple[str, ...] = ("register",)


class SubcommandExtensionError(ValueError):
    """An extension that cannot contribute, refused where it is WIRED.

    One exception for every wiring defect, because a caller does nothing
    different for any of them: the parser must not be built.
    """


@runtime_checkable
class SubcommandExtension(Protocol):
    """One method. Nothing else, ever — see `MEMBERS`."""

    def register(self, subparsers) -> None:
        """Attach this extension's subcommands to the parser being built.

        `subparsers` is the `argparse._SubParsersAction` the core subcommands
        were added through. An implementation calls `subparsers.add_parser(...)`
        and `set_defaults(func=...)` on the result, exactly as the core does,
        and returns nothing: the parser it was handed IS the return value.

        Called ONCE while the parser is built, never per invocation.
        """


def register_all(extensions, subparsers) -> None:
    """Register every extension, in declaration order, refusing a non-conformer.

    Order is the caller's and is preserved: `argparse` lists subcommands in the
    order they were added, so the tuple an entrypoint declares is the order the
    help text reads in — and a help text whose order depended on a dict
    iteration would make the golden parity proof this seam ships with worthless.
    """
    for extension in extensions:
        if not isinstance(extension, SubcommandExtension):
            raise SubcommandExtensionError(
                f"{extension!r} does not conform to SubcommandExtension: it "
                f"must declare {list(MEMBERS)}")
        extension.register(subparsers)
