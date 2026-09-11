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

IT REFUSES RATHER THAN DEGRADES — AT THE POINT OF USE. An uninitialized gitlink
raises `CarveReachUnavailable` naming the leg, the missing path and the exact
command that fixes it. It does NOT fall back to a skip: `.github/workflows/
pytest-suite.yml` pins `EXPECT_SKIPPED` as an exact SUM precisely because a
directory that quietly turned into skips reports as a green bar, and
`tests/clearing/conftest.py` already refuses the same way for openXwallet. The
workflow initialises `openDox` and `openXdox` RECURSIVELY for this reason — the
non-recursive init that preceded § 5.2 left `openDox/code` empty on the runner.

The refusal fires when a CARVED name is asked for, not when `install()` is
called, and the difference is a real one rather than a nicety: `tests/
conftest.py` is in the conftest chain of EVERY pytest invocation under `tests/`,
including targeted lanes that touch nothing the carve moved
(`.github/workflows/review-lane-repin.yml` runs `pytest tests/review_lane_pin`
over a plain checkout with no gitlinks initialised — Copilot,
`PRRT_kwDOTAvnrs6hVRyB`). An `install()` that refused eagerly would break those
lanes to protect a reach they never make. `_LegMissing` below instead refuses
`opendox`, `openxdox` and the leg test-helper modules BY NAME, so a run that
needs the carve still fails loudly and a run that does not still passes.

THE ONE MODULE THAT REACHES NOWHERE, AND THE COMPOSITION POINT THAT REPLACED IT.
`scripts/ideation_dashboard/profile_openxfactory.py` is the manifest's single
`deleted_at_carve` row: openxFactory's OWN composition point (§ 2.4's profile —
the tuple of route and subcommand contributions THIS assembly is built with),
which exists at NO destination by construction. Asking for it through the shed's
old dotted name gets a named refusal from `_ShedGone` below rather than a bare
`ModuleNotFoundError` that reads like a typo. Its POST-SHED home is
`scripts/profile_openxfactory.py` (importable as the plain top-level
`profile_openxfactory`), and `bind_composition_point()` below registers it with
the two consumers that still name it as a bare global — the openxFactory half of
RULED ASK-2 option (2), standing in for openDox-code's not-yet-built lazy proxy.

AND THE PATHS, NOT ONLY THE MODULES. `source()` below answers "where is the file
that used to be at <repository-relative path>" by READING THE MANIFEST ROW, so a
test that asserts over a moved file's SOURCE TEXT — and a dozen of the retained
ones do — names the pre-shed path it has always named and gets the pinned
destination copy. Derived, never transcribed: the destination of
`scripts/ideation_dashboard/lens.py` is openDox-code and of
`scripts/ideation_dashboard/serve_gate.py` is openXdox-code, and no reader of
this module has to know which, or notice the day a row's destination changes.
A per-DIRECTORY constant is exactly the bug this replaces: `scripts/
ideation_dashboard/` split across BOTH legs and partly stayed here.
"""

from __future__ import annotations

import functools
import importlib
import importlib.abc
import importlib.machinery
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

#: The carve manifest — FLOOR PART 1, and the only authority on where a shed
#: path went. `source()` reads it; nothing in this file transcribes a row.
MANIFEST = REPO_ROOT / "docs" / "opendox-carve-manifest.yaml"

#: Where each declared `destinations:` key is MOUNTED in this checkout. The
#: manifest names repositories; a working tree names directories, and this is
#: the only place the two are joined. `opendox_root` carries no rows (a tag cut
#: at the assembly root is not a file that leaves here) and is listed so that a
#: row that ever gains it resolves rather than raising a KeyError.
MOUNTS: dict[str, Path] = {
    "opendox_root": REPO_ROOT / "openDox",
    "opendox_code": REPO_ROOT / "openDox" / "code",
    "opendox_spec": REPO_ROOT / "openDox" / "spec",
    "openxdox_code": REPO_ROOT / "openXdox" / "code",
    "openxdox_spec": REPO_ROOT / "openXdox" / "spec",
}

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
        "core names no profile and openXdox declares its own, so there is no "
        "DESTINATION to re-point this import at. There IS a post-shed home: "
        "`scripts/profile_openxfactory.py`, importable as the plain top-level "
        "`profile_openxfactory`, carrying the same two tuples re-spelled for "
        "the pinned legs — import THAT. What is still owed is § 4.3's lazy "
        "proxy at openDox-code (RULED ASK-2 option (2), `#656` comment "
        "`5628886636`), which is why `carved_reach.bind_composition_point()` "
        "registers the module with `opendox.serve` and `opendox.cli` rather "
        "than those two importing it themselves."),
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


class _LegMissing(importlib.abc.MetaPathFinder):
    """Refuses a CARVED name when its leg is not materialized.

    Last in `sys.meta_path`, so it only ever sees a name nothing else could
    resolve. It is what makes the refusal fire at the point of use rather than
    at `install()` — see the module docstring's second paragraph for why a
    targeted lane that never touches the carve must still be able to run.
    """

    def __init__(self, names: frozenset[str]) -> None:
        self._names = names

    def find_spec(self, fullname, path=None, target=None):  # noqa: D102
        root = fullname.partition(".")[0]
        if root not in self._names:
            return None
        raise CarveReachUnavailable(
            f"{fullname} is read from a pinned carve leg, and no leg in this "
            f"checkout carries it: the `openDox` and/or `openXdox` gitlinks are "
            f"not materialized. openxFactory reads the modules the § 5.2 shed "
            f"removed through its own pin (RULED Q7), so this is a checkout "
            f"that cannot run what asked for this module rather than a "
            f"condition to skip past. Run `{INIT_COMMAND}` from the repository "
            f"root.")


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
    path, or arrange for the carved NAMES to refuse when a leg is missing, and
    register openxFactory's composition point with the two consumers that name
    it.

    Idempotent: safe to call from a conftest, from a script's module body and
    from a test that re-enters it. `tests=True` additionally APPENDS the two
    legs' own `tests/` trees, for the helper modules that moved there.

    IT DELIBERATELY DOES NOT BIND THE COMPOSITION POINT, and the reason is a
    cycle rather than a preference. `bind_composition_point()` below reaches
    `scripts/profile_openxfactory.py`, which imports
    `ideation_dashboard.serve_openxfactory_lanes` — a module whose own body
    calls THIS function. Folding the binding in here makes that column's import
    re-enter the profile while the column is still half-executed
    (`AttributeError: partially initialized module … has no attribute
    'LaneRoutesExtension'`, measured). The division that falls out is the right
    one anyway: a COLUMN installs the reach, an ASSEMBLY POINT also binds the
    profile, and the assembly points are named in `bind_composition_point()`'s
    own docstring.
    """
    missing = []
    for gitlink, leg, src, package in LEGS:
        try:
            _require(gitlink, leg, src, package)
        except CarveReachUnavailable:
            missing.append(package)
        else:
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
    if missing and not any(isinstance(f, _LegMissing) for f in sys.meta_path):
        sys.meta_path.append(_LegMissing(frozenset(missing)))


def require() -> None:
    """Both legs, materialized, or `CarveReachUnavailable` naming the missing
    one — the EAGER refusal, for a caller that is going to reach either way.

    `install()` defers the refusal to the name that is asked for, because it
    runs in every pytest invocation including ones that reach nothing. A
    production entrypoint has no such ambiguity: it is about to serve, sweep or
    sync through a carved module, and finding out now beats finding out in the
    middle of a lane. `scripts/ideation-dashboard-serve.py` is the entrypoint
    this exists for.
    """
    for gitlink, leg, src, package in LEGS:
        _require(gitlink, leg, src, package)


# --------------------------------------------------------------------------
# THE PATH RESOLVER — "where is the file that used to be HERE?"
# --------------------------------------------------------------------------

@functools.lru_cache(maxsize=1)
def _rows() -> dict[str, dict]:
    """The manifest's rows, keyed by `source_path`. Read once per process."""
    import yaml  # local: the manifest is the only reason this module needs it
    with MANIFEST.open(encoding="utf-8") as handle:
        doc = yaml.safe_load(handle)
    return {row["source_path"]: row for row in doc["rows"]}


class NotACarvedPath(KeyError):
    """A path was asked about that the carve manifest declares no row for."""


def source(path: str | Path) -> Path:
    """The file `path` NAMES TODAY, wherever the § 5.2 shed left it.

    `path` is repository-relative and PRE-SHED — the name the file had here,
    which is the name every retained reader already spells and the only name the
    manifest is keyed by. The answer is derived from that file's row:

      * a MOVED row resolves at its declared destination's mount
        (`openDox/code`, `openDox/spec`, `openXdox/code`, `openXdox/spec`),
        at the row's own `destination_path` — which is NOT always the same
        relative path, and is exactly why this is a lookup and not a prefix
        substitution;
      * a `not_moved` row resolves HERE, unchanged, so a caller that sweeps a
        mixed set does not have to know which of its members stayed;
      * the one `deleted_at_carve` row raises `ShedModuleHasNoDestination`,
        the same named refusal its import gets;
      * a path in no row raises `NotACarvedPath`, because a caller asking this
        question about a file the manifest never declared has the wrong file,
        and answering `REPO_ROOT / path` would hide that.

    A missing leg raises `CarveReachUnavailable` naming the leg and the command
    — the same refusal an import of one of its modules gets, and for the same
    reason: a source assertion that silently read nothing would pass.
    """
    key = str(path).replace("\\", "/")
    try:
        row = _rows()[key]
    except KeyError:
        raise NotACarvedPath(
            f"{key} is in no row of {MANIFEST.relative_to(REPO_ROOT)}. The "
            f"manifest declares every file under its `moved_paths:` surface, so "
            f"a path it does not carry either never was under the surface (ask "
            f"for it directly — it never moved) or is misspelled.") from None
    if row["disposition"] == "not_moved":
        if row.get("reason") == "deleted_at_carve":
            reason = NO_DESTINATION.get("ideation_dashboard.profile_openxfactory", "")
            raise ShedModuleHasNoDestination(
                f"{key} is the carve manifest's `deleted_at_carve` row and has "
                f"no destination to read it from. {reason}")
        return REPO_ROOT / key
    mount = MOUNTS[row["destination"]]
    if not (mount / ".git").exists() and not any(mount.glob("*")):
        raise CarveReachUnavailable(
            f"the pinned {row['destination']} leg is not materialized: "
            f"{mount.relative_to(REPO_ROOT)} is empty, so {key} cannot be read "
            f"from the destination the carve manifest declares for it. Run "
            f"`{INIT_COMMAND}` from the repository root.")
    return mount / row["destination_path"]


def sources_under(prefix: str) -> dict[str, Path]:
    """Every manifest row under `prefix`, mapped to where its file is TODAY.

    For the readers that walk a TREE rather than name a file — the import-
    direction scanners, the serve-surface sweeps. Keyed by the pre-shed
    repository-relative path, so a caller's own reporting still names the path
    a reader of this repository's history will recognise. The
    `deleted_at_carve` row is omitted: it is nowhere, and a sweep is not the
    place to raise about it.
    """
    prefix = prefix.rstrip("/") + "/"
    out: dict[str, Path] = {}
    for key, row in _rows().items():
        if not key.startswith(prefix):
            continue
        if row.get("reason") == "deleted_at_carve":
            continue
        out[key] = source(key)
    return out


# --------------------------------------------------------------------------
# THE COMPOSITION POINT — RULED ASK-2 (2), openxFactory's half
# --------------------------------------------------------------------------

#: The two modules at the pinned openDox leg that still name
#: `profile_openxfactory` as a BARE GLOBAL with no import anywhere
#: (`serve.py:1377`'s `build_server`, `cli.py:915`'s `build_parser`). Those two
#: lines are the § 4.3 hole; RULED ASK-2 option (2) (`#656` comment
#: `5628886636`) closes it with a lazy proxy AT openDox-code that openxFactory
#: registers the real module with. The proxy is not built yet, so until it is
#: the registration binds the module into each consumer's own globals, which is
#: where an unqualified name is looked up first.
COMPOSITION_CONSUMERS: tuple[str, ...] = ("opendox.serve", "opendox.cli")

#: The name those two modules spell.
COMPOSITION_NAME = "profile_openxfactory"


class _BindProfileAfterExec(importlib.abc.Loader):
    """Wraps a consumer's real loader and binds the profile once it has run."""

    def __init__(self, inner) -> None:
        self._inner = inner

    def create_module(self, spec):  # noqa: D102
        return self._inner.create_module(spec)

    def exec_module(self, module):  # noqa: D102
        self._inner.exec_module(module)
        setattr(module, COMPOSITION_NAME,
                importlib.import_module(COMPOSITION_NAME))

    def __getattr__(self, name):  # everything else (get_source, is_package, …)
        return getattr(self._inner, name)


class _ProfileRegistrar(importlib.abc.MetaPathFinder):
    """Registers openxFactory's profile with each consumer AS IT LOADS.

    FIRST in `sys.meta_path`, because it has to see the import before the path
    finder resolves it; it delegates the actual finding straight to
    `PathFinder` (both consumers are ordinary files under a pinned leg) and
    only decorates the loader, so it shadows nothing and changes no resolution.
    Binding AFTER `exec_module` rather than before is what keeps the import
    graph honest: `profile_openxfactory` imports `openxdox.serve_gate` and
    `openxdox.serve_projection`, which `serve.py` has already imported by then
    as `DashboardHandler`'s mixin bases, so the registration adds no module to
    a server process that did not already carry it — and `cli_gate`, the one
    dependency a server must not pay for, stays behind the profile's PEP 562
    `__getattr__`.
    """

    _busy = False

    def find_spec(self, fullname, path=None, target=None):  # noqa: D102
        if fullname not in COMPOSITION_CONSUMERS or _ProfileRegistrar._busy:
            return None
        _ProfileRegistrar._busy = True
        try:
            spec = importlib.machinery.PathFinder.find_spec(fullname, path, target)
        finally:
            _ProfileRegistrar._busy = False
        if spec is None or spec.loader is None:
            return None
        spec.loader = _BindProfileAfterExec(spec.loader)
        return spec


def bind_composition_point() -> None:
    """Register `scripts/profile_openxfactory.py` with the two consumers.

    Idempotent, and it covers both directions in time: a consumer ALREADY
    imported is bound now, and one imported later is bound as it loads. Calling
    it costs no import of either consumer — which matters, because importing
    `opendox.cli` pulls the CLI column's whole dependency chain and a server
    process must not pay for it.

    WHO CALLS IT, AND WHY THAT IS NOT ONLY THE TESTS (Copilot
    `PRRT_kwDOTAvnrs6hbVwB`). Every ASSEMBLY POINT — a process that is going to
    call `build_server()` or `build_parser()` — and nothing else:

      * `scripts/ideation-dashboard-serve.py`, the serve entrypoint
        `scripts/reserve-dashboard.sh` executes. It is the production caller,
        and its absence was the finding: without this call a real server
        process reaches `NameError: name 'profile_openxfactory' is not
        defined` the moment it builds, which is measured rather than supposed.
      * `tests/conftest.py` and `tests/ideation-dashboard/conftest.py`, for the
        suites that build servers and parsers in-process.

    A COLUMN must NOT call it: `ideation_dashboard/serve_openxfactory_lanes.py`
    is imported BY the profile, so a column that bound the composition point
    would re-enter its own half-executed module. That is why `install()` does
    not fold this in — see its docstring.

    THE DAY THIS SHRINKS. When openDox-code's lazy proxy lands (§ 4.3, RULED
    ASK-2 (2)), the consumers will import the proxy themselves and this becomes
    the single `register(profile)` call the ruling describes; the finder below
    goes away with the hole it covers.
    """
    for name in COMPOSITION_CONSUMERS:
        module = sys.modules.get(name)
        if module is not None and not hasattr(module, COMPOSITION_NAME):
            setattr(module, COMPOSITION_NAME,
                    importlib.import_module(COMPOSITION_NAME))
    if not any(isinstance(f, _ProfileRegistrar) for f in sys.meta_path):
        sys.meta_path.insert(0, _ProfileRegistrar())
