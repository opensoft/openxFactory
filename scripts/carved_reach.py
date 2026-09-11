"""THE ONE PLACE openxFactory REACHES INTO THE TWO PINNED CARVE DESTINATIONS.

`split-opendox-two-layer-product` § 5.2, RULED (a) POST-SHED MODE (`#656`
comment `5625573095`) and RULED Q7 (`#656` comment `5626248666`, verbatim
"SECOND SUBMODULE — openxFactory mounts the openDox assembly root").

WHAT THE SHED DID AND WHY THIS FILE EXISTS. The § 5.2 shed deleted the 319
paths `docs/opendox-carve-manifest.yaml` declares — 318 moved rows plus the one
`deleted_at_carve` row. 38 files that STAY here still named 39 of those modules
at 125 import sites. A module that left is not gone: it is at a destination
this repository now pins by commit and mounts as a submodule, and the lawful
way to read it is through that pin. This module is the only place that reach is
spelled, so there is exactly one file to read to know what openxFactory imports
from outside itself, and exactly one file to change if a leg ever moves.

THE REACH IS BOTH LEGS, TOGETHER, AND THAT IS MEASURED — not a convenience.
`ideation/brainstorm/opendox-shed-exit-a-post-shed-mode-measured.md` measured
importability of the 17 `openxdox` modules three ways: 3 of 17 resolve with the
openXdox leg alone, 7 of 17 with `scripts/doc_health` additionally reachable,
and 17 of 17 only with BOTH legs' `src/` present. openXdox's modules import
openDox's and openDox's reach back; a single-leg install would appear to work
and then fail on the seventeenth import. So `install()` installs both or
refuses, and it puts this repository's own `scripts/` on the path with them —
`scripts/doc_health` is reachable from here, which is the open clause § 4.1
left, and it is what makes the `doc_health` importers among those modules
resolve when they are run from openxFactory.

IT REFUSES RATHER THAN DEGRADES. An uninitialized gitlink raises
`CarveReachUnavailable` naming the leg, the missing path and the exact command
that fixes it. It does NOT fall back to a skip: `.github/workflows/
pytest-suite.yml` pins `EXPECT_SKIPPED` as an exact SUM precisely because a
directory that quietly turned into skips reports as a green bar, and
`tests/clearing/conftest.py` already refuses the same way for openXwallet. The
workflow initialises `openDox` and `openXdox` RECURSIVELY for this reason — the
non-recursive init that preceded § 5.2 left `openDox/code` empty on the runner.

THE ONE MODULE THAT REACHES NOWHERE. `scripts/ideation_dashboard/
profile_openxfactory.py` is the manifest's single `deleted_at_carve` row: it is
openxFactory's OWN composition point (§ 2.4's profile — the tuple of route and
subcommand contributions THIS assembly is built with), it exists at NO
destination by construction, and § 4.3 owes it a post-shed home. Asking for it
through the shed's old name gets a named refusal from `_ShedGone` below rather
than a bare `ModuleNotFoundError` that reads like a typo.
"""

from __future__ import annotations

import importlib.abc
import importlib.machinery
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

#: The two direct upstreams, in the order RULED Q7 names them. Each entry is
#: `(gitlink, leg, src directory, the package that directory must carry)`.
LEGS: tuple[tuple[str, str, Path, str], ...] = (
    ("openDox", "code", REPO_ROOT / "openDox" / "code" / "src", "opendox"),
    ("openXdox", "code", REPO_ROOT / "openXdox" / "code" / "src", "openxdox"),
)

#: The two legs' own `tests/` trees, for the four test-helper modules that moved
#: there and that retained test modules still import by their bare names
#: (`session_fixtures`, `test_doxbench_packet`, `test_gate_console`,
#: `test_project_aggregates`, `test_workbench`). APPENDED, never prepended:
#: pytest's default prepend import mode puts a test file's own directory at
#: `sys.path[0]`, so openxFactory's own modules keep winning every name they
#: still carry — which matters for the 20 `replicated_at_destination` rows,
#: whose basenames exist on both sides on purpose.
LEG_TESTS: tuple[Path, ...] = (
    REPO_ROOT / "openDox" / "code" / "tests",
    REPO_ROOT / "openXdox" / "code" / "tests",
)

SCRIPTS_DIR = REPO_ROOT / "scripts"

INIT_COMMAND = "git submodule update --init --recursive openDox openXdox"


class CarveReachUnavailable(ImportError):
    """A pinned leg is not materialized, so a shed module cannot be read."""


class ShedModuleHasNoDestination(ImportError):
    """A shed module that left for NO destination was asked for by its old name."""


#: Old dotted name -> the sentence that explains where it went. Only the
#: manifest's `deleted_at_carve` row is here; every MOVED module has a real
#: destination and resolves normally once `install()` has run.
NO_DESTINATION: dict[str, str] = {
    "ideation_dashboard.profile_openxfactory": (
        "`scripts/ideation_dashboard/profile_openxfactory.py` is the carve "
        "manifest's single `deleted_at_carve` row and it exists at NO "
        "destination: it is openxFactory's OWN § 2.4 composition point (the "
        "`ROUTE_EXTENSIONS` / `SUBCOMMAND_EXTENSIONS` tuples naming what THIS "
        "assembly's entrypoints are built with), and its own docstring called "
        "it \"the one file the § 3 carve deletes rather than moves\". openDox's "
        "core names no profile and openXdox declares its own, so there is "
        "nothing to re-point this import at. A post-shed home for "
        "openxFactory's composition point is § 4.3's, and it is OWED — see "
        "`openspec/changes/split-opendox-two-layer-product/tasks.md` § 5.2."),
}


class _ShedGone(importlib.abc.MetaPathFinder):
    """Turns a bare `ModuleNotFoundError` into the sentence above.

    Last in `sys.meta_path`, so it only ever sees a name nothing else could
    resolve — it can never shadow a module that really is importable.
    """

    def find_spec(self, fullname, path=None, target=None):  # noqa: D102
        reason = NO_DESTINATION.get(fullname)
        if reason is None:
            return None
        raise ShedModuleHasNoDestination(
            f"{fullname} left openxFactory in the § 5.2 shed and has no "
            f"destination to be read from. {reason}")


def _require(gitlink: str, leg: str, src: Path, package: str) -> None:
    # A DIRECTORY WITH MODULES IN IT, not an `__init__.py`: `opendox` is a
    # regular package and `openxdox` is a NAMESPACE package (no `__init__.py`
    # at either the leg's `src/` or the package directory), exactly as
    # `ideation_dashboard` was here — so the marker has to be a module file,
    # not the package initialiser one of the two legs does not have.
    marker = src / package
    if marker.is_dir() and any(marker.glob("*.py")):
        return
    raise CarveReachUnavailable(
        f"the pinned {gitlink} {leg} leg is not materialized: "
        f"{marker.relative_to(REPO_ROOT)} carries no module. openxFactory reads "
        f"the modules the § 5.2 shed removed from this leg through its own "
        f"pin (RULED Q7), so this is a checkout that cannot run the suite "
        f"rather than a condition to skip past. Run `{INIT_COMMAND}` from the "
        f"repository root.")


def install(*, tests: bool = False) -> None:
    """Put both pinned legs' `src/` — and this repository's `scripts/` — on the
    path, or refuse naming the leg that is missing.

    Idempotent: safe to call from a conftest, from a script's module body and
    from a test that re-enters it. `tests=True` additionally APPENDS the two
    legs' own `tests/` trees, for the helper modules that moved there.
    """
    for gitlink, leg, src, package in LEGS:
        _require(gitlink, leg, src, package)
    for _, _, src, _ in LEGS:
        if str(src) not in sys.path:
            sys.path.insert(0, str(src))
    if str(SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPTS_DIR))
    if tests:
        for helpers in LEG_TESTS:
            if helpers.is_dir() and str(helpers) not in sys.path:
                sys.path.append(str(helpers))
    if not any(isinstance(finder, _ShedGone) for finder in sys.meta_path):
        sys.meta_path.append(_ShedGone())
