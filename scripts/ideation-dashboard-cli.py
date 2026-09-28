#!/usr/bin/env python3
"""Entrypoint wrapper so the dashboard COMMAND LINE runs from THIS repository,
POST-SHED (the twin of `scripts/ideation-dashboard-serve.py`):

    python3 scripts/ideation-dashboard-cli.py generate --repo-root . \\
        --repository openxFactory --output snapshot.json

WHY IT EXISTS. Before `split-opendox-two-layer-product` § 5.2 the command line
was `python3 -m ideation_dashboard.cli` with `PYTHONPATH=scripts`, and the
nightly refresh lane's worker child ran exactly that line inside the sealed
source artifact. The shed moved `cli.py` to openDox-code, so the line names a
module this repository no longer holds (`No module named
ideation_dashboard.cli`, openxFactory #1161). Reaching it lawfully now takes
the same three acts the serve wrapper performs, and in the same order:

  * `carved_reach.require()` — both pinned legs materialized, or a refusal
    naming the leg and the command that fixes it, before anything is built;
  * `carved_reach.install()` — the two legs' `src/` on the path, read through
    THIS repository's own pin (RULED Q7, `#656` `5626248666`);
  * `opendox_host.register_openxfactory()` — the ONE process-start
    registration. `opendox.cli.build_parser()` reads openxFactory's
    contributed subcommands through openDox-code's lazy proxy, which refuses
    unless a host has registered (RULED ASK-2 option (2), `#656`
    `5628886636`), and `openxdox.generator` reads the domain profile through
    the same registration (§ 4.4).

That is the bootstrap `tests/ideation-dashboard/test_cli_column_split.py`
already names as "the only lawful way this repository reaches the command line
after the § 5.2 shed"; this file is the one place a person, a lane or a worker
child runs to get it, rather than each of them re-spelling it.

THE PRODUCT'S OWN ENTRY POINT, UNCHANGED. Everything after the bootstrap is
`opendox.cli.main` — the product's parser, its verbs, its refusals and its exit
codes. Nothing is re-implemented here. It is imported as a module rather than
run with `runpy` under `__main__`, so exactly one `opendox.cli` module object
exists and the command line's refusal classes stay catchable (the hazard
`cli.py`'s own `__main__` block documents).

A CREATED FILE: no row in `docs/opendox-carve-manifest.yaml`, which declares
what LEAVES this repository and never what it assembles (RULED OQ-C).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import carved_reach  # noqa: E402

carved_reach.require()
carved_reach.install()

import opendox_host  # noqa: E402

opendox_host.register_openxfactory()

from opendox.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
