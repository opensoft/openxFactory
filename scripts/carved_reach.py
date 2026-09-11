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
`profile_openxfactory`), and `scripts/opendox_host.py` is what REGISTERS it —
the openxFactory half of RULED ASK-2 option (2), now that openDox-code's lazy
proxy has landed (#11, `a99eba03`). This module carried the stand-in for it
until then: `bind_composition_point()`, an import hook that bound the module
into `opendox.serve` and `opendox.cli` as they loaded, which its own docstring
said would "become the single `register(profile)` call the ruling describes"
the day the proxy landed. It has, and it did.

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
import os
import re
import subprocess
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
        "the pinned legs — import THAT. Both consumers now reach it through "
        "openDox-code's own lazy proxy (§ 4.3, RULED ASK-2 option (2), `#656` "
        "comment `5628886636`; openDox-code #11 `a99eba03`), which resolves "
        "whatever profile the host registered at process start — here, "
        "`scripts/opendox_host.py`'s `register_openxfactory()`."),
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
    path, or arrange for the carved NAMES to refuse when a leg is missing.

    Idempotent: safe to call from a conftest, from a script's module body and
    from a test that re-enters it. `tests=True` additionally APPENDS the two
    legs' own `tests/` trees, for the helper modules that moved there.

    IT DELIBERATELY DOES NOT REGISTER THE DOMAIN PROFILE, and the reason is a
    cycle rather than a preference. `scripts/opendox_host.py` reaches
    `scripts/profile_openxfactory.py`, which imports
    `ideation_dashboard.serve_openxfactory_lanes` — a module whose own body
    calls THIS function. Folding the registration in here makes that column's
    import re-enter the profile while the column is still half-executed
    (`AttributeError: partially initialized module … has no attribute
    'LaneRoutesExtension'`, measured). The division that falls out is the right
    one anyway: a COLUMN installs the reach, an ASSEMBLY POINT also calls
    `opendox_host.register_openxfactory()`, and the assembly points are named
    in that function's own docstring.
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
    if "openxdox" not in missing:
        bind_openxdox_column()


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
# THE `openxdox` COLUMN'S OWN § 4.3 HOLE — three declared import rewrites the
# carve could not express
# --------------------------------------------------------------------------

#: `docs/opendox-carve-manifest.yaml` files `scripts/ideation_dashboard/
#: gate_routes.py` as `moved_with_declared_edit`, and its `import rewrites`
#: class names lines 911, 950, 1046/1047 and 3428. ONE of those four — line 911,
#: the only one that names none but MOVED modules — reads `from opendox import
#: lens, workbench as wb` at the pinned `openXdox/code` leg. The other three are
#: still verbatim there (`src/openxdox/gate_routes.py:951`, `:1047`, `:3429`),
#: and the reason is structural rather than an oversight: each of the three
#: reaches a NOT_MOVED openxFactory module (`lens_submission`, `human_seen`)
#: alongside a moved one, and a rewrite to `from opendox import ...` cannot
#: spell a name that stayed HERE. Line 911 is the proof the rewrite pass ran;
#: these three are the residue it had no destination to express.
#:
#: The manifest says as much at its `lens_submission.py` row: RULING OQ-B keeps
#: that module in-tree and files "its two remaining reaches (:57 lens, :58
#: workbench) as import rewrites reached THROUGH openXdox at the carve — a
#: not_moved row cannot carry an edit, so the reach is recorded here."
#:
#: Pre-shed the three lines resolved because `.` was openxFactory's own
#: `ideation_dashboard` package, which carried all four names. Post-shed `.` is
#: the leg's `openxdox`, which carries none of them, and the § 5.2 shed is what
#: makes that visible — `ImportError: cannot import name 'lens' from 'openxdox'`
#: on the five lens-gate tests, measured at `80e8af35`.
#:
#: So this is the same § 4.3 shape as `profile_openxfactory` below, one layer
#: up, and it gets the same answer: openxFactory REGISTERS the real modules with
#: the consumer that names them, in that consumer's own namespace, where an
#: unqualified `from . import X` looks first. `openxdox` is a NAMESPACE package
#: (no `__init__.py` at the leg), so the registration is a PEP 562 module
#: `__getattr__` rather than an assignment into an `__init__`. LAZY on purpose:
#: a server process that never executes a lens or human-seen gate verb pays for
#: none of these four imports, exactly as it paid for none of them before.
#:
#: THE DAY THIS GOES AWAY: when openXdox-code carries the three lines rewritten
#: — each split into its moved half (`from opendox import ...`) and its retained
#: half reached through openxFactory — this mapping and its binder are deleted.
#: That is a LEG act plus a pin bump, and RULED (a) post-shed mode moves no leg,
#: so it is recorded as owed rather than taken here.
OPENXDOX_COLUMN_BINDINGS: dict[str, str] = {
    "lens": "opendox.lens",                                   # gate_routes :951
    "workbench": "opendox.workbench",                          # :951, :1047
    "lens_submission": "ideation_dashboard.lens_submission",   # :951
    "human_seen": "ideation_dashboard.human_seen",             # :1047, :3429
}


def bind_openxdox_column() -> None:
    """Give the pinned `openxdox` package the four names its own `from . import`
    lines still spell, resolving each to the module's real post-shed home.

    Idempotent, and it imports NOTHING until one of the four names is actually
    asked for: every other attribute — including every dunder — raises
    `AttributeError` out of the hook and resolves exactly as it did before, so
    the leg's real submodules (`gate_console`, `generator`, `kickoff`, ...) are
    untouched and nothing is shadowed.
    """
    openxdox = importlib.import_module("openxdox")
    if getattr(openxdox, "_carved_reach_column_bound", False):
        return

    def __getattr__(name: str):
        target = OPENXDOX_COLUMN_BINDINGS.get(name)
        if target is None:
            raise AttributeError(f"module 'openxdox' has no attribute {name!r}")
        module = importlib.import_module(target)
        setattr(openxdox, name, module)   # bind once; later reads are plain
        return module

    openxdox.__getattr__ = __getattr__
    openxdox._carved_reach_column_bound = True


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


class ManifestPathUnsafe(ValueError):
    """A carve-manifest row's `destination_path` is not a closed relative
    path — refused before it is joined onto a mount, never after."""


#: Every `destination_path` join site below calls `_closed_relative_path`
#: FIRST. Copilot review, `PRRT_kwDOTAvnrs6hjzVm`, 2026-09-11:
#: `destination_path` was type-checked as a non-empty string only, by
#: `scripts/validate-carve-manifest.py`'s shape check (now closed there too —
#: same predicate, so a row this resolver would refuse never lands); an
#: absolute value replaces the mount outright under `Path.__truediv__`, and a
#: `../` segment walks out of it, either way redirecting a read outside the
#: leg the manifest declares. Pure string canonicalisation closes both: a
#: value with no leading `/` and no `..`/`.`/empty segment cannot escape ANY
#: mount it is joined onto, absolute or relative — which is why this is
#: checked once here rather than with a `Path.resolve()`/`relative_to()`
#: guard after each join (one of the two join sites below joins onto a mount
#: already made relative to `REPO_ROOT`, where `resolve()` would resolve
#: against the process's CWD, not `REPO_ROOT`, and answer the wrong
#: question). NOT restricted to an ASCII alphabet — a `destination_path` may
#: legitimately carry any Unicode filename (`tests/carve_manifest/
#: test_carve_manifest.py::test_the_row_order_is_bytewise_and_not_by_code_point`
#: exercises one with U+E000), unlike `scripts/hermes_runtime_validation/
#: content.py`'s `normalize_repository_path`, whose narrower alphabet this
#: does not otherwise try to match.
def _closed_relative_path(value: str, *, source_path: str) -> str:
    """`value`, unchanged, or refused as unsafe to join onto a mount."""
    if (not value or value.startswith("/") or value.startswith(":")
            or "\\" in value
            or any(ord(character) < 32 or ord(character) == 127 for character in value)):
        raise ManifestPathUnsafe(
            f"{source_path}'s row declares `destination_path: {value!r}`, "
            "which is not a canonical relative path")
    if any(part in {"", ".", ".."} for part in value.split("/")):
        raise ManifestPathUnsafe(
            f"{source_path}'s row declares `destination_path: {value!r}`, "
            "which contains a `.`, `..` or empty segment — exactly what "
            "would let this row's destination escape its own mount")
    return value


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
    return mount / _closed_relative_path(row["destination_path"], source_path=key)


def module(path: str | Path):
    """The IMPORTED module for the file that used to be at `path`.

    `source()`'s answer in the import direction, and for the same readers: a
    caller that loads a dashboard module BY NAME at runtime — `scripts/
    sync-notebooklm-books.py`'s `_dashboard_module()` is the one this exists
    for — had a package name baked into an f-string, and after the shed some of
    those names live at one leg, some at the other and some still here. The
    dotted name is DERIVED from the row instead:

      * a MOVED row's `destination_path` (`src/opendox/workbench.py`) becomes
        the dotted name the leg's `src/` makes importable (`opendox.workbench`)
        — which is why the day a row moves between the two legs no caller
        changes;
      * a `not_moved` row keeps the spelling it has HERE
        (`scripts/ideation_dashboard/intent_feed.py` → the
        `ideation_dashboard.intent_feed` that `SCRIPTS_DIR` on the path serves);
      * the `deleted_at_carve` row raises `ShedModuleHasNoDestination`, and a
        path in no row raises `NotACarvedPath`, exactly as `source()` does.

    `install()` is called first, so a caller gets the legs on the path and the
    named refusals without having to remember to arrange them.
    """
    key = str(path).replace("\\", "/")
    row = _rows().get(key)
    if row is None:
        source(key)  # raises NotACarvedPath with the sentence that explains it
    install()
    if row["disposition"] == "not_moved":
        if row.get("reason") == "deleted_at_carve":
            source(key)  # raises ShedModuleHasNoDestination
        relative = key[len("scripts/"):] if key.startswith("scripts/") else key
    else:
        relative = row["destination_path"]
        if relative.startswith("src/"):
            relative = relative[len("src/"):]
    if not relative.endswith(".py"):
        raise NotACarvedPath(
            f"{key} resolves to {relative}, which is not a Python module — "
            f"ask `source()` for it instead.")
    return importlib.import_module(relative[:-3].replace("/", "."))


def shed_relpath(path: str | Path) -> str | None:
    """The REPOSITORY-RELATIVE path a moved row's file has in this checkout
    today — or `None` when the row stayed, or there is no row.

    `shed_destination()` without the leg. The one reader that needs this rather
    than an absolute answer is a MARKER: `doxbench_contracts` decides whether a
    directory is a release by asking whether three files are present in it, and
    the question is asked about OTHER checkouts as well as this one, so what it
    needs is the relative spelling. Deriving it must not require the leg to be
    materialized — the marker is consulted at import time by lanes that
    initialise no gitlinks at all — so this reads the row and stops, and the
    caller's own `exists()` decides presence exactly as it always did.
    """
    key = str(path).replace("\\", "/")
    row = _rows().get(key)
    if row is None or row["disposition"] == "not_moved":
        return None
    mount = MOUNTS[row["destination"]].relative_to(REPO_ROOT)
    return (mount / _closed_relative_path(row["destination_path"], source_path=key)).as_posix()


def shed_destination(path: str | Path) -> Path | None:
    """Where an ABSOLUTE path INSIDE THIS REPOSITORY is today — or `None`.

    `source()` in the direction the readers that take a ROOT need it. The
    hermes-runtime catalog and release sources, the estate-wide manifest-digest
    sweep and the doc-health schema loader do not name a module: they join a
    path onto a root they were handed and read whatever is there. Post-shed
    five of those joins name a file that MOVED (`contracts/schemas/
    {ideation-dashboard-snapshot,ideation-dashboard-snapshot-index,gate-action-
    record,xfactory-workbench-chat-turn,xfactory-workbench-model-catalog}
    .schema.yaml`), and every one of the five arrived at its destination BYTE
    FOR BYTE — measured 2026-09-11, each leg copy's sha256 equal to the digest
    `contracts/manifest.yaml` already records. So the published contract surface
    does not move at all: the bytes this repository pins are the bytes it always
    pinned, at the path the pinned leg now holds them, and this function is the
    one place that says so.

    It answers `None` — and the caller's own answer stands — for:

      * a root that is NOT this repository (`hermes_runtime_validation` runs in
        candidate mode over domain mirrors, and a mirror's own missing file is
        its own finding, never a silent read out of openxFactory's legs);
      * a path in no manifest row, or one still under this tree;
      * a `not_moved` row.

    It RAISES `CarveReachUnavailable` — it does not answer `None` — when the row
    moved and its leg is not materialized, for the reason the module docstring
    gives: a reader that quietly found nothing reports as a green bar.
    """
    candidate = Path(os.path.normpath(str(path)))
    try:
        key = candidate.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return None
    row = _rows().get(key)
    if row is None or row["disposition"] == "not_moved":
        return None
    return source(key)


#: Ambient environment that would let `git rev-parse <revision>:<path>` below
#: resolve from a DIFFERENT object store than the one `repo` names — the same
#: list `scripts/hermes_runtime_validation/content.py`'s exact-content helper
#: scrubs. Duplicated rather than imported: every OTHER caller of that helper
#: is loaded dotted (`scripts.hermes_runtime_validation....`), a context that
#: guarantees the repository root is on `sys.path`; this module is loaded bare
#: (`import carved_reach`) with only `scripts/` on `sys.path` at some call
#: sites (`scripts/ideation-dashboard-serve.py`), where that dotted import
#: would fail. Keep the two lists equal if either changes.
_INDEXED_GIT_CONFIG_ENVIRONMENT = re.compile(r"GIT_CONFIG_(?:KEY|VALUE)_[0-9]+")
_SCRUBBED_GIT_ENVIRONMENT = (
    "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    "GIT_COMMON_DIR",
    "GIT_CONFIG_COUNT",
    "GIT_CONFIG_PARAMETERS",
    "GIT_DIR",
    "GIT_INDEX_FILE",
    "GIT_OBJECT_DIRECTORY",
    "GIT_REPLACE_REF_BASE",
    "GIT_WORK_TREE",
)


def _sanitized_git_environment() -> dict[str, str]:
    environment = {
        name: value
        for name, value in os.environ.items()
        if name not in _SCRUBBED_GIT_ENVIRONMENT
        and _INDEXED_GIT_CONFIG_ENVIRONMENT.fullmatch(name) is None
    }
    environment["GIT_CONFIG_GLOBAL"] = os.devnull
    environment["GIT_CONFIG_SYSTEM"] = os.devnull
    environment["GIT_CONFIG_NOSYSTEM"] = "1"
    environment["GIT_NO_REPLACE_OBJECTS"] = "1"
    return environment


def _git_object_id(repo: Path, revision: str, path: str) -> str | None:
    """`git -C <repo> rev-parse <revision>:<path>`, or `None` when it is not
    there. `None` is an ANSWER here, not a swallowed error: the one caller uses
    it to mean "that commit's tree carries no such entry", which is exactly the
    case of a commit from BEFORE the § 5.2 shed — where the file is still in
    this repository's own tree and the caller's ordinary read already found it.

    Runs with `--no-replace-objects` and a sanitized environment (Copilot,
    `PRRT_kwDOTAvnrs6hjE-c`): `<revision>:<path>` otherwise resolves through
    ambient `GIT_DIR`/alternate-object-directory/replace-ref configuration,
    which could make this read a leg commit the root commit does not actually
    name.
    """
    try:
        done = subprocess.run(
            ["git", "--no-replace-objects", "-C", str(repo), "rev-parse", f"{revision}:{path}"],
            capture_output=True,
            text=True,
            check=False,
            env=_sanitized_git_environment(),
        )
    except OSError:  # pragma: no cover - no git on PATH is the caller's problem
        return None
    value = done.stdout.strip()
    return value if done.returncode == 0 and value else None


def shed_commit_object(commit: str, path: str | Path) -> tuple[Path, str, str] | None:
    """Where a moved row's bytes are AT AN EXACT COMMIT — `(repo, commit, path)`.

    `shed_destination()` for the readers that must never touch a working tree.
    `scripts/hermes_runtime_validation/release.py` verifies a release from one
    commit and reads every member with `content.resolve_git_object`, which reads
    ONE repository's object store; post-shed three members of this repository's
    own registration are `moved_verbatim` rows whose bytes are in a LEG's object
    store, reachable from that commit only through the gitlink it records.

    So this walks the gitlink chain the mount implies, one `rev-parse
    <revision>:<segment>` per level — `openXdox/spec` is two levels, because
    `openXdox` is a submodule of this repository and `spec` is a submodule of
    THAT — and answers the leg repository, the commit that repository is pinned
    at BY THIS COMMIT, and the row's own `destination_path`. The answer is
    therefore as exact as the caller's: a commit that pinned an older leg reads
    the older leg's bytes, and nothing is read from the working tree.

    It answers `None` — and the caller's own answer stands — for a path in no
    row, a `not_moved` row, and a commit whose tree carries no such gitlink,
    which is every commit from BEFORE the shed: there the file is still in this
    repository's own tree and the ordinary read already succeeded.

    It RAISES `CarveReachUnavailable` when the gitlink IS recorded and the leg is
    not materialized, for the reason the module docstring gives: an object store
    that is not on disk cannot be read, and a reader that quietly found nothing
    reports as a green bar.
    """
    key = str(path).replace("\\", "/")
    row = _rows().get(key)
    if row is None or row["disposition"] == "not_moved":
        return None
    repo = REPO_ROOT
    revision = commit
    for segment in MOUNTS[row["destination"]].relative_to(REPO_ROOT).parts:
        gitlink = _git_object_id(repo, revision, segment)
        if gitlink is None:
            return None
        repo = repo / segment
        revision = gitlink
        if not (repo / ".git").exists():
            raise CarveReachUnavailable(
                f"the pinned {row['destination']} leg is not materialized: "
                f"{repo.relative_to(REPO_ROOT)} carries no Git object store, so "
                f"{key} cannot be read at the commit that pins it. Run "
                f"`{INIT_COMMAND}` from the repository root.")
    return repo, revision, row["destination_path"]


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
# THE COMPOSITION POINT — RULED ASK-2 (2): NOT HERE ANY MORE
# --------------------------------------------------------------------------
#
# `opendox.serve.build_server` and `opendox.cli.build_parser` read
# `profile_openxfactory` through openDox-code's OWN lazy proxy
# (`opendox.profile_proxy`, § 4.3, openDox-code #11 `a99eba03`), which resolves
# the profile the host registered at process start. So this module no longer
# carries a composition point at all: `bind_composition_point()` and the
# `_ProfileRegistrar` meta-path finder under it are DELETED, exactly as that
# function's own docstring said they would be — *"THE DAY THIS SHRINKS. When
# openDox-code's lazy proxy lands (§ 4.3, RULED ASK-2 (2)), the consumers will
# import the proxy themselves and this becomes the single `register(profile)`
# call the ruling describes; the finder below goes away with the hole it
# covers."*
#
# The single call is `scripts/opendox_host.py`'s `register_openxfactory()`, and
# it is made by every assembly point that builds an openDox parser or server.
# It is NOT folded into `install()`, for the reason `install()`'s own docstring
# gives: `profile_openxfactory` imports
# `ideation_dashboard.serve_openxfactory_lanes`, a column whose own body calls
# `install()`, so a column that composed the profile would re-enter its own
# half-executed module. A COLUMN installs the reach; an ASSEMBLY POINT also
# registers the profile.
#
# `bind_openxdox_column()` above is a DIFFERENT hole of the same shape (the
# three declared import rewrites the carve could not express) and is untouched:
# it is recorded as owed against a leg act plus a pin bump, not against § 4.3.
