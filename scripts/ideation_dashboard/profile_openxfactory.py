"""WHAT THIS ASSEMBLY IS BUILT WITH: the in-tree openxFactory profile
(`split-opendox-two-layer-product` § 2.4).

The composition point. `cli.py` and `serve.py` declare the extension POINTS and
know nothing about what fills them; this module names the contributions THIS
repository's entrypoints are assembled with, and it is the one file the § 3
carve deletes rather than moves — after the carve openXdox declares its own
profile and openDox's core has no line naming any.

Deliberately minimal and additive: a tuple per extension point, nothing else. PR
3 of § 2.4 adds `ROUTE_EXTENSIONS` beside `SUBCOMMAND_EXTENSIONS` for the route
point, which is why this is a module of constants and not a class with a
constructor to negotiate.
"""

from __future__ import annotations

# Relative, like the core's own imports of the modules the § 2.4 split created:
# this tree is importable under two package spellings, and the profile must
# contribute the column belonging to the SAME spelling as the core that is
# assembling the parser — otherwise the verbs it registers are a different
# column's, bound to a different core (see `cli.py`'s note above its own
# relative import, and `cli_gate._core()`).
from . import cli_gate

#: The subcommand contributions this assembly's command line carries, in the
#: order they are registered — which is the order `--help` reads in, so the
#: tuple is the observable declaration and not an incidental one.
#:
#: One member today: the gate console, openXdox's column. It registers at the
#: ordinal `_add_gate_subcommands` used to occupy, so the parser this profile
#: builds is byte-identical to the one that preceded the seam.
SUBCOMMAND_EXTENSIONS: tuple = (cli_gate.GateSubcommands(),)
