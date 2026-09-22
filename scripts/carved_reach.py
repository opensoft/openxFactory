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

AND THE ROWS A RULING HAS RETIRED (RULED 5656343213, `#656` comment
`5656343213`). A moved row may carry a `retired:` block saying that a ruling
DELETED its arrival at the leg — not moved it, as RULED Q6's `re_destined:`
does, but removed it, because the surface the arrived file needed is at no leg
at all. The row keeps every field the carve wrote, so this module can still
compute a perfectly well-formed path for it under a materialized leg — and
that path would name a file `verify-carve-arrival.py` has just finished
proving ABSENT. So `source()` refuses with `CarveRowRetired` (a subclass of
`ShedModuleHasNoDestination`, so callers that already handle "at no
destination" need no change), `module()` and `shed_relpath()` refuse through
it, and `sources_under()` OMITS such a row exactly as it omits the
`deleted_at_carve` one: a caller that NAMES a retired file has the wrong file,
and a caller SWEEPING a tree must not be stopped by one row that is nowhere.
"""

from __future__ import annotations

import functools
import importlib
import importlib.abc
import os
import re
import subprocess
import sys
import tempfile
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

#: WHERE CPython KEEPS THE COMPILED BYTECODE for everything imported after the
#: legs go on the path — and the requirement is about where it does NOT go.
#: `install()` makes two PINNED submodule checkouts importable, and CPython's
#: default cache location is a `__pycache__` INSIDE the directory the module
#: was read from, so the first import out of a leg writes into a tree this
#: repository pins by commit (46 `.pyc` files under the two `src/` roots from
#: a single test module, measured). Two consequences, and the second is the
#: one that made this a finding:
#:
#:   * a consumer that has to establish that a leg IS the commit it is pinned
#:     at — `scripts/verify-snapshot-equivalence.py`'s cleanliness sweep —
#:     was left passing over a class of file its own imports created; and
#:   * CPython VALIDATES a cached `.pyc` against the mtime and size recorded
#:     in its header, so a crafted cache whose header still matches the
#:     tracked source is loaded and EXECUTED. That is bytes in no commit
#:     running out of a tree every pin check calls clean (Copilot,
#:     openxFactory PR #1115, discussion `r4049745762`).
#:
#: `sys.pycache_prefix` closes both at once: with it set CPython neither READS
#: nor writes a `__pycache__` beside the source. `sys.dont_write_bytecode` is
#: NOT the remedy and was not proposed as one — it stops the writing and
#: leaves the READING, which is the half the finding is about.
#:
#: INSIDE THE CHECKOUT, deliberately. The threat model this closes needs a
#: writer in the working tree, and such a writer could edit THIS FILE — so a
#: cache under the repository root is no weaker than the code that reads it,
#: while a fixed path under a shared `/tmp` would be a directory another user
#: can create first and fill with exactly the crafted caches above. The root
#: `.gitignore` already ignores `*.py[cod]`, so every file written here is
#: ignored and `git status` is unchanged (measured); nothing needs adding to
#: it. If the directory cannot be written, CPython silently skips caching —
#: the failure mode is a slower import and never a broken one.
BYTECODE_HOME = REPO_ROOT / ".pycache"

#: The mounted submodules a bytecode cache must never land INSIDE. The two
#: assembly roots, because every mount in `MOUNTS` is at or under one of them
#: — and `openXdox`'s own root is not a `MOUNTS` key (no manifest row arrives
#: there), so a set derived from `MOUNTS` alone would miss it. openxFactory's
#: suite holds this tuple to `MOUNTS` rather than anyone remembering.
_PINNED_MOUNTS: tuple[Path, ...] = (REPO_ROOT / "openDox",
                                    REPO_ROOT / "openXdox")

INIT_COMMAND = "git submodule update --init --recursive openDox openXdox"

#: The remedy for a leg whose object store exists but cannot answer for the
#: pinned commit, or for the tree/blobs under it — every `CarveReachUnavailable`
#: raise below that reaches this point shares this text verbatim, and so does
#: `doc_health.release_inventory`'s own `LegUnavailable` (`#1048` round 4,
#: Copilot on PR #1051, `carved_reach.py:921` / `release_inventory.py:290`).
#: `git fetch --unshallow` ALONE WAS WRONG HERE: it is the fix for a
#: GENUINELY SHALLOW clone only (`git rev-parse --is-shallow-repository`
#: prints `true`) — MEASURED, git 2.43.0: a `--filter=tree:0`/`blob:none`
#: store is not shallow, and `--unshallow` there only answers `fatal:
#: --unshallow on a complete repository does not make sense` and fixes
#: nothing, because the two are orthogonal git features and a partial clone
#: never went shallow to begin with.
INCOMPLETE_STORE_REMEDY = (
    f"Run `{INIT_COMMAND}` from the repository root. A store that is "
    f"GENUINELY SHALLOW (`git rev-parse --is-shallow-repository` prints "
    f"`true`) needs its own `git fetch --unshallow` first; a "
    f"`--filter=tree:0` or `blob:none` PARTIAL store is not shallow, and "
    f"`--unshallow` there only answers `fatal: --unshallow on a complete "
    f"repository does not make sense` — fetch the pinned objects from a "
    f"remote that still carries them instead (`git -C <store> fetch "
    f"origin <sha>`, or `git fetch --refetch`), or re-run the command "
    f"above to re-initialize the leg.")


class CarveReachUnavailable(ImportError):
    """A pinned leg's object store is missing, incomplete, or otherwise
    unreadable — the query was unanswerable, not answered.

    THREE PATHS RAISE THIS, all inside `shed_commit_object`'s gitlink walk
    (`#1048` round 5, Copilot on PR #1051, `carved_reach.py:1105`, widening
    this from the original "not materialized" alone): the leg is NOT
    MATERIALIZED — `_leg_object_store` finds no Git object store on disk at
    all; the store IS materialized but INCOMPLETE — it exists but does not
    carry the pinned commit; or the TREE that would record the gitlink itself
    could not be READ — an unresolvable revision, a `--filter=tree:0` clone
    whose promisor remote is unreachable, or (round 5) a probe that hit its
    30s timeout rather than answering. Every path means the same thing to a
    caller: nothing was learned, so the caller's own absence finding must
    never stand in for it.
    """


class ShedModuleHasNoDestination(ImportError):
    """A shed module that left for NO destination was asked for by its old name."""


class CarveRowRetired(ShedModuleHasNoDestination):
    """A row a RULING has RETIRED at its leg was asked for (RULED 5656343213).

    A SUBCLASS and not a sibling, deliberately. To every caller that already
    handles "this file is at no destination" the two cases are one answer —
    ask for something else — and an existing `except ShedModuleHasNoDestination`
    goes on working unchanged the day a row is first retired. To a caller that
    wants the distinction the class carries it: `deleted_at_carve` is a file
    the carve never placed anywhere, and a RETIREMENT is a file the carve DID
    place and a later ruling deleted. Different causes, different remedies,
    one supertype.
    """


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


def _resolved(path: Path) -> Path | None:
    """`path.resolve()`, or `None` when the filesystem will not answer.

    MEASURED on this repository's own interpreter, CPython 3.12.3:
    `Path.resolve()` raises `RuntimeError: Symlink loop from …` on a cyclic
    link, with `strict=False` as well as `strict=True` — `os.path.realpath()`
    swallows it and `resolve()` does not (Copilot, PR #1132 round 3). A
    cyclic `<repo>/.pycache`, or a cyclic `PYTHONPYCACHEPREFIX`, would
    therefore have raised out of `install()` — in every conftest in this
    repository — which is precisely the failure the fallback exists to avoid.

    `None` FAILS SAFE at the one caller: a path that cannot be shown to be
    outside every pinned mount is treated as inside, so the cache goes to the
    freshly created directory rather than to a path nothing could resolve.
    """
    try:
        return path.resolve()
    except (OSError, RuntimeError, ValueError):
        return None


def _inside_a_pinned_mount(prefix: str) -> bool:
    """Whether a bytecode prefix would put the cache INSIDE a pinned mount.

    A RELATIVE prefix counts as inside, and that is not pedantry: CPython
    joins the prefix with the SOURCE FILE'S OWN directory at write time, and a
    relative head is resolved against whatever the working directory is then —
    so where it lands is not knowable here, and a guarantee that cannot be
    checked is not a guarantee. Symlinks are resolved on both sides, because a
    link into a leg is the same placement under another name.
    """
    candidate = Path(prefix)
    if not candidate.is_absolute():
        return True
    resolved = _resolved(candidate)
    if resolved is None:
        return True
    for mount in _PINNED_MOUNTS:
        target = _resolved(mount)
        if target is None or resolved.is_relative_to(target):
            return True
        # AND WHERE THE BYTES WOULD ACTUALLY LAND, WHICH IS NOT THE PREFIX
        # ITSELF (Copilot, PR #1132 round 4). In prefix mode CPython does not
        # put the cache AT the prefix: `cache_from_source()` builds the
        # directory as `_path_join(sys.pycache_prefix, head.lstrip(
        # path_separators))` — the source's own absolute directory appended
        # to the prefix — and drops the `__pycache__` component entirely. So
        # the filesystem ROOT maps a leg module straight back BESIDE ITS OWN
        # SOURCE, inside the pin. MEASURED: with `PYTHONPYCACHEPREFIX=/`,
        # `cache_from_source(<leg>/src/openxdox/generator.py)` is
        # `<leg>/src/openxdox/generator.cpython-312.pyc`. A predicate about
        # where a prefix IS cannot answer that; this one asks where the
        # bytes GO, so the root is refused as the case it is rather than as
        # a special one.
        mapped = _resolved(resolved / str(target).lstrip("/"))
        if mapped is None or mapped.is_relative_to(target):
            return True
    return False


def _bytecode_out_of_the_legs() -> None:
    """Send CPython's bytecode cache to `BYTECODE_HOME`, BEFORE either leg is
    importable — the one line that keeps this repository from writing into a
    tree it pins, and from executing a `.pyc` it has not read.

    A PREFIX THE PROCESS ALREADY CHOSE IS KEPT — `PYTHONPYCACHEPREFIX`, or a
    host that has set its own — UNLESS it resolves inside a pinned mount, in
    which case it defeats the very thing it is being kept for and is replaced.
    "Any prefix at all satisfies this" was the first rule here and it was
    wrong (Copilot, openxFactory PR #1132): a prefix at a LEG ROOT puts the
    cache inside the pin AND outside the `src` the cleanliness sweep scans, so
    a crafted cache there is both read — before `verify_pins()` runs, since the
    legs are imported first — and invisible to the check that would have
    reported it. Replacing rather than refusing is `GIT_ATTR_NOSYSTEM`'s
    precedent one file over: an ambient variable that would weaken a guarantee
    is overridden, not made into a required gate's refusal.

    Idempotent, and called from `install()`, which `module()` calls in turn
    — so every route THROUGH THIS MODULE passes through it, which is not the
    same as every route into a leg and must not be written as though it
    were (Copilot, PR #1132 round 6, on a sentence that said the second).
    MEASURED, by this act, and it is why the snapshot-equivalence sweep
    still passes over unreachable bytecode rather than counting on emptiness:
    `scripts/corpus_adapter_openxfactory/` puts `openDox/code/src` on
    `sys.path` itself and imports `opendox.corpus_adapter` without coming
    through here at all (RULED OQ-Q, `#872`). What this function guarantees
    is that no importer REACHING THROUGH `carved_reach` reads or writes
    bytecode inside a pinned mount; a direct importer is registered for a
    successor act, not silently covered by this docstring.
    """
    chosen = sys.pycache_prefix
    if chosen is not None and not _inside_a_pinned_mount(chosen):
        return
    # AND THE FALLBACK IS HELD TO THE SAME RULE IT ENFORCES (Copilot,
    # openxFactory PR #1132 round 2): `BYTECODE_HOME` is a PATH, and a
    # pre-existing `<repo>/.pycache` that is a SYMLINK into a pinned mount
    # would put the cache exactly where this function exists to keep it out
    # of. A directory this process has just created cannot hold a crafted
    # cache to read, so `mkdtemp()` is the last resort rather than a raise:
    # `install()` runs in every conftest in this repository, and a stray
    # symlink in one checkout must not become an ImportError in all of them.
    home = str(BYTECODE_HOME)
    if _inside_a_pinned_mount(home):
        # AND THE FRESH DIRECTORY IS CREATED SOMEWHERE THIS RUN HAS CHECKED
        # (Copilot, PR #1132 round 6). `mkdtemp()` honours `TMPDIR`, so an
        # inherited temp directory inside — or symlinked into — a pinned
        # mount would put the last resort in the pin, unchecked. The PARENT
        # is chosen first and only then written in: the temp directory when
        # it is outside every mount, and otherwise the repository root,
        # which CONTAINS the mounts and so cannot be inside one. A child
        # `mkdtemp()` creates there is a real directory and not a symlink,
        # so a parent that resolves outside the pins has children that do.
        parent = tempfile.gettempdir()
        if _inside_a_pinned_mount(parent):
            parent = str(REPO_ROOT)
        home = tempfile.mkdtemp(prefix="openxfactory-bytecode-", dir=parent)
    sys.pycache_prefix = home


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
    _bytecode_out_of_the_legs()
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


def effective_arrival(row: dict) -> tuple[str, str]:
    """`(destination key, destination path)` a MOVED row resolves at TODAY —
    `re_destined.to`/`to_path` where RULED Q6 has re-destined the placement,
    else the row's own `destination`/`destination_path`.

    THE SAME THREE-LINE PREDICATE LIVES IN `scripts/validate-carve-manifest.py`
    and `scripts/verify-carve-arrival.py`, and this is a THIRD copy rather than
    an import of either: both are hyphenated entry points loaded by
    `importlib.util.spec_from_file_location`, and this module is itself loaded
    BARE at some call sites (`scripts/ideation-dashboard-serve.py` puts only
    `scripts/` on `sys.path`), so none of the three can import another — the
    same precedent `_closed_relative_path` already set against those same two
    tools. `tests/carve_arrival/test_verify_carve_arrival.py
    ::test_both_tools_read_the_effective_arrival_identically` asserts this
    copy equal to theirs rather than trusting three definitions to agree —
    RULED Q-L8 (c)'s lesson about two tools and one definition, now for three.

    `source()` resolves every MOVED row through this — and `sources_under()`
    and `shed_destination()` through `source()` in turn — because reading a
    row's raw `destination`/`destination_path` once it carries a
    `re_destined:` block answers where the § 5.2 shed FIRST placed the file,
    not where a later ruling actually put it. `PRRT_kwDOTAvnrs6h1nYE` named
    the consequence: the dashboard compositor's `sources_under()` sweep would
    link a path the paired leg has since VACATED instead of the one the file
    arrived at.
    """
    re_destined = row.get("re_destined")
    if isinstance(re_destined, dict):
        to = re_destined.get("to")
        to_path = re_destined.get("to_path")
        if isinstance(to, str) and isinstance(to_path, str):
            return to, to_path
    return row.get("destination"), row.get("destination_path")


# THE CLOSED KEY SET, HERE TOO, because this predicate ENFORCES it and cannot
# import the copy in `scripts/validate-carve-manifest.py` (that file is a
# hyphenated entry point loaded by `spec_from_file_location`; this one is
# imported bare). A block carrying a key outside it — a misspelled `notes:`, a
# field somebody invented — reads as NO retirement and the arrival stays owed,
# on the same fail-closed reasoning the four required keys already have: a
# document this predicate cannot fully read is one the manifest validator must
# be run against before anything acts on it.
RETIRED_KEYS = frozenset({"at", "at_path", "ruling", "surface", "note"})


def retired_at(row: dict) -> tuple:
    """`(destination key, destination path)` a RULING has RETIRED this row's
    arrival at (RULED 5656343213, `#656` comment `5656343213`) — or
    `(None, None)` where the row carries no usable retirement.

    THE THIRD COPY of a three-line predicate, exactly as `effective_arrival`
    above is, and for the same reason: `validate-carve-manifest.py` and
    `verify-carve-arrival.py` are hyphenated entry points loaded by
    `spec_from_file_location`, this module is loaded BARE at some call sites,
    and none of the three can import another.
    `tests/carve_arrival/test_verify_carve_arrival.py::test_all_three_tools_read_the_retirement_identically`
    asserts the three equal over a table rather than trusting them to agree.

    `source()` refuses on it — and `module()`, `shed_relpath()` and
    `shed_destination()` through or beside it — because the alternative is
    worse than a refusal: a retired row's `destination_path` still resolves
    to a perfectly well-formed path under a materialized leg, and returning it
    would hand a caller a `Path` to a file the floor has just finished proving
    is NOT THERE. That is the silent-nothing this module's own docstring
    refuses to degrade into.

    ALL FOUR REQUIRED KEYS ARE THE GUARD, not the two a placement needs
    (Copilot review of PR #1032, round 2). `retired: {at, at_path}` is half a
    block: `validate-carve-manifest.py` refuses it — `carve-retired-unruled`,
    then `carve-shape-invalid` on the missing `surface` — but THIS predicate is
    read by tools that never run that validator. `verify-carve-arrival.py` is
    run at a leg against a `--dest-root` and `carved_reach` is imported by
    every retained consumer, so "the validator would have caught it" is not
    true at the moment of reading; a half-written block would silence a
    required arrival before anyone validated the document. Four non-empty
    strings or no retirement — the same closed key set (`at`, `at_path`,
    `ruling`, `surface`, and the optional `note`) the form itself declares.

    AND THE OPTIONAL KEY IS READ AS THE GRAMMAR WRITES IT, not as a type
    (Copilot review of PR #1032, round 7). `_check_retired_shape` refuses a
    PRESENT `note:` that is not a non-empty string — *a note is prose or it is
    absent* — and this predicate asked only `isinstance`, so `note: ""` and
    `note: "   "` read as usable retirements here and as `carve-shape-invalid`
    there. That is the fail-OPEN direction again, arriving through the one key
    the form makes OPTIONAL: a block the validator would refuse silenced this
    row's arrival check at a leg that had not run the validator. ABSENT, OR
    PROSE — the same rule, in the same words, in all three copies and in the
    grammar, held together by
    `test_the_note_is_prose_or_absent_in_the_grammar_and_in_all_three_readers`.
    """
    retired = row.get("retired")
    if isinstance(retired, dict) and set(retired) <= RETIRED_KEYS:
        at = retired.get("at")
        at_path = retired.get("at_path")
        ruling = retired.get("ruling")
        surface = retired.get("surface")
        if (all(isinstance(value, str) and value.strip()
                for value in (at, at_path, ruling, surface))
                and ("note" not in retired
                     or (isinstance(retired["note"], str)
                         and retired["note"].strip()))):
            return at, at_path
    return None, None


def source(path: str | Path) -> Path:
    """The file `path` NAMES TODAY, wherever the § 5.2 shed left it.

    `path` is repository-relative and PRE-SHED — the name the file had here,
    which is the name every retained reader already spells and the only name the
    manifest is keyed by. The answer is derived from that file's row:

      * a MOVED row resolves at its declared destination's mount
        (`openDox/code`, `openDox/spec`, `openXdox/code`, `openXdox/spec`),
        at `effective_arrival(row)`'s path — the row's own `destination_path`,
        unless a `re_destined:` block (RULED Q6) says a ruling moved the
        placement afterwards, in which case its `to_path` — which is NOT
        always the same relative path either way, and is exactly why this is
        a lookup and not a prefix substitution;
      * a `not_moved` row resolves HERE, unchanged, so a caller that sweeps a
        mixed set does not have to know which of its members stayed;
      * the one `deleted_at_carve` row raises `ShedModuleHasNoDestination`,
        the same named refusal its import gets;
      * a row a RULING has RETIRED at its leg (RULED 5656343213) raises
        `CarveRowRetired`, a subclass of that same refusal: the carve DID
        place this file and a later ruling DELETED that placement, so the
        well-formed path this function could still compute would name
        nothing. It is the ARRIVAL that is refused, and the refusal says so:
        a row may ALSO declare `also_replicated_to:` copies, which RULED OQ-C
        makes the legs' own placements and which no retirement touches;
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
    at, at_path = retired_at(row)
    if at_path is not None:
        retired = row["retired"]
        replicas = row.get("also_replicated_to") or []
        raise CarveRowRetired(
            f"{key} was RETIRED at {at}:{at_path} by ruling "
            f"{retired.get('ruling')!r} (RULED 5656343213), because the "
            f"surface it needed ({retired.get('surface')!r}) arrived at no "
            "leg. The row still records the move the carve made — that is "
            "what the manifest is for — but the ARRIVAL this function "
            "resolves is gone, and a path computed from the row would name a "
            "file the arrival verifier has just finished proving absent. Ask "
            "for whatever replaced the surface, or for nothing."
            + (f" (This says nothing about the row's `also_replicated_to` "
               f"copies at {sorted(str(r) for r in replicas)!r}: RULED OQ-C "
               "makes those the LEGS' own placements, declared with "
               "`--replica-at` and governed on their own terms — a "
               "retirement deletes ONE placement, the one named above.)"
               if replicas else ""))
    destination, destination_path = effective_arrival(row)
    mount = MOUNTS[destination]
    if not (mount / ".git").exists() and not any(mount.glob("*")):
        raise CarveReachUnavailable(
            f"the pinned {destination} leg is not materialized: "
            f"{mount.relative_to(REPO_ROOT)} is empty, so {key} cannot be read "
            f"from the destination the carve manifest declares for it. Run "
            f"`{INIT_COMMAND}` from the repository root.")
    return mount / _closed_relative_path(destination_path, source_path=key)


def module(path: str | Path):
    """The IMPORTED module for the file that used to be at `path`.

    `source()`'s answer in the import direction, and for the same readers: a
    caller that loads a dashboard module BY NAME at runtime — `scripts/
    sync-notebooklm-books.py`'s `_dashboard_module()` is the one this exists
    for — had a package name baked into an f-string, and after the shed some of
    those names live at one leg, some at the other and some still here. The
    dotted name is DERIVED from the row instead:

      * a MOVED row's `effective_arrival(row)` `destination_path`
        (`src/opendox/workbench.py`) becomes the dotted name the leg's `src/`
        makes importable (`opendox.workbench`): the row's own, unless a
        `re_destined:` block (RULED Q6) says a ruling has since moved the
        placement, in which case its `to_path` — `source()`'s own precedent,
        read here for the same reason, and why the day a row moves between
        the two legs, or is re-destined between them afterward, no caller
        changes;
      * a `not_moved` row keeps the spelling it has HERE
        (`scripts/ideation_dashboard/intent_feed.py` → the
        `ideation_dashboard.intent_feed` that `SCRIPTS_DIR` on the path serves);
      * the `deleted_at_carve` row raises `ShedModuleHasNoDestination`, a
        RETIRED row raises `CarveRowRetired`, and a path in no row raises
        `NotACarvedPath`, exactly as `source()` does.

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
        if retired_at(row)[1] is not None:
            source(key)  # raises CarveRowRetired with the sentence for it
        destination, relative = effective_arrival(row)
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

    A RETIRED ROW RAISES `CarveRowRetired` rather than answering (RULED
    5656343213), on `source()`'s reasoning and not in spite of the paragraph
    above: the caller's `exists()` would answer False for a file that is not
    merely un-materialized but DELETED BY RULING, and "not here yet" and
    "never again" are the two answers a marker must not confuse. Raising does
    not require a leg to be materialized, so the property this function exists
    for is kept.
    """
    key = str(path).replace("\\", "/")
    row = _rows().get(key)
    if row is None or row["disposition"] == "not_moved":
        return None
    if retired_at(row)[1] is not None:
        source(key)  # raises CarveRowRetired with the sentence for it
    destination, destination_path = effective_arrival(row)
    mount = MOUNTS[destination].relative_to(REPO_ROOT)
    return (mount / _closed_relative_path(destination_path, source_path=key)).as_posix()


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


def _git_run(repo: Path, *arguments: str):
    """The ONE scrubbed, replacement-free `git -C <repo> ...` invocation every
    reader below shares — the finished process, or `None` when git could not be
    run at all, OR WHEN IT DID NOT ANSWER IN TIME.

    Runs with `--no-replace-objects` and a sanitized environment (Copilot,
    `PRRT_kwDOTAvnrs6hjE-c`): a `<revision>:<path>` otherwise resolves through
    ambient `GIT_DIR`/alternate-object-directory/replace-ref configuration,
    which could make this read a leg commit the root commit does not actually
    name — and the same scrub is what makes the `--git-common-dir` read below
    answer for the directory this module points git AT rather than for whatever
    an ambient `GIT_COMMON_DIR` names.

    BOUNDED AT `timeout=30`, THE SAME 30 SECONDS `scripts/hermes_runtime_
    validation/content.py:103-116` already gives its own equivalent read
    (`#1048` round 5, Copilot on PR #1051, `carved_reach.py:826`). The
    `cat-file -e`/`ls-tree` probes this function serves are exactly the reads a
    partial clone or an unreachable promisor remote can make HANG rather than
    fail, and every caller above this one exists to turn a git FAILURE into an
    answer — `_tree_entry_absent`'s whole taxonomy, `_leg_object_store`'s
    materialization check, the incomplete-store probe in the walk below — none
    of which get a turn if the process never returns. `subprocess.TimeoutExpired`
    is therefore caught beside `OSError` and answered with the SAME `None` a
    missing git binary already produces, so every reader above this line
    reaches its EXISTING unavailable path unchanged: a probe that timed out is
    a query that went UNANSWERED, never the tree's own answer that an entry is
    absent — the phantom-absence thesis `#1048` exists to refuse, one layer
    lower than every other case in this module.
    """
    try:
        return subprocess.run(
            ["git", "--no-replace-objects", "-C", str(repo), *arguments],
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
            env=_sanitized_git_environment(),
        )
    except subprocess.TimeoutExpired:
        return None
    except OSError:  # pragma: no cover - no git on PATH is the caller's problem
        return None


def _git_text(repo: Path, *arguments: str) -> str | None:
    """The stripped stdout of one `git -C <repo> ...` read, or `None` when
    git declines — for the reads that ANSWER IN STDOUT."""
    done = _git_run(repo, *arguments)
    if done is None:
        return None
    value = done.stdout.strip()
    return value if done.returncode == 0 and value else None


def _git_ok(repo: Path, *arguments: str) -> bool:
    """Whether a git probe SUCCEEDED — for the reads that answer by EXIT CODE
    and print nothing.

    `cat-file -e` is the one this module needs and `_git_text` cannot serve it:
    there an empty stdout is indistinguishable from a failure, so a commit that
    IS present would read as absent. Separate function rather than a flag,
    because the two return types are what keep that confusion impossible.
    """
    done = _git_run(repo, *arguments)
    return done is not None and done.returncode == 0


def _git_object_id(repo: Path, revision: str, path: str) -> str | None:
    """`git -C <repo> rev-parse <revision>:<path>`, or `None` when that read
    DID NOT ANSWER — which is not the same fact as "it is not there".

    `None` IS TWO FACTS AND THE CALLER MUST SEPARATE THEM (`#1048` round 2).
    One is the ANSWER the one caller wants: that commit's tree carries no such
    entry, which is exactly the case of a commit from BEFORE the § 5.2 shed —
    there the file is still in this repository's own tree and the caller's
    ordinary read already found it. The other is a FAILURE: the tree object
    this read has to walk is not in the store, and a `--filter=tree:0` clone
    whose promisor remote is unreachable is the everyday shape of that. git
    spells the two IDENTICALLY to a reader of stdout — exit 128 and nothing
    printed, differing only in a `fatal:` line — so `_tree_entry_absent` below
    asks which one arrived, and this `None` is never read as an absence alone.
    """
    return _git_text(repo, "rev-parse", f"{revision}:{path}")


def _tree_entry_absent(repo: Path, revision: str,
                       path: str) -> tuple[bool, str]:
    """Did `revision`'s tree ANSWER that it carries no entry at `path`?

    `(True, "")` for git's own unambiguous answer, `(False, <what git said>)`
    for every other outcome. MEASURED, git 2.43.0, in a throwaway store — the
    four shapes this separates:

      A PATH GENUINELY NOT IN THE TREE. `rev-parse <commit>:<path>` exits 128
      (`fatal: path 'x' does not exist in 'HEAD'`); `ls-tree <commit> --
      <path>` EXITS 0 AND PRINTS NOTHING. This is the answer, and the only
      shape that returns one.

      THE COMMIT'S ROOT TREE OBJECT MISSING — a `--filter=tree:0` clone whose
      promisor remote is unreachable, or a pruned store. `rev-parse` exits 128
      again (`fatal: path 'leg' exists on disk, but not in 'HEAD'`), the same
      empty stdout for the opposite fact; `ls-tree` exits 128 (`fatal: not a
      tree object`, or git's own `could not fetch <tree> from promisor
      remote`). `cat-file -e <commit>^{commit}` still exits 0 there, which is
      why the commit probe in `shed_commit_object` passes and this case
      reaches the walk at all.

      A SUBTREE MISSING UNDER A READABLE ROOT TREE. `ls-tree` exits 1
      (`error: Could not read <sha>`) while `cat-file -e <commit>^{tree}`
      exits 0 — which is why the root-tree probe is NOT the discriminator
      here: it passes on a store that cannot answer for the path.

      AN UNRESOLVABLE REVISION. `ls-tree` exits 128 (`fatal: not a tree
      object`), so an unreadable commit lands here as a failure rather than as
      an absence, which is the taxonomy's "git unavailable or commit
      unresolvable" arm rather than its "member absent" one.

    EXIT 0 WITH OUTPUT IS A FAILURE TOO. The tree listed an entry that
    `rev-parse` could not resolve; two reads that disagree have established
    nothing, and the one thing this function may never do is manufacture an
    absence out of a disagreement.

    AND IT ASKS ABOUT THE PATH THE OTHER READ ASKED ABOUT (`#1048` round 3,
    Copilot on PR #1051, `carved_reach.py:746`). `git ls-tree` resolves its
    pathspec RELATIVE TO THE CURRENT PREFIX unless `--full-tree` is given,
    while `git rev-parse <revision>:<path>` — the read this probe exists to
    explain — is relative to the ROOT of the tree always. Under any non-empty
    prefix the two are asking about DIFFERENT paths, so this one's answer is
    not evidence about the other's entry at all. MEASURED, git 2.43.0: in a
    module store whose `core.worktree` resolves to a directory CONTAINING the
    store, `rev-parse --show-prefix` answers `.git/modules/leg/` and
    `ls-tree <pin> -- spec` then EXITS 0 AND PRINTS NOTHING for a `spec`
    gitlink that tree really carries — git's own unambiguous "no such entry",
    returned for an entry that is there, which is precisely the phantom
    absence this function was added to refuse. `--full-tree` with a
    `:(literal)` pathspec is the root-relative form every other tree reader
    here already uses (`scripts/hermes_runtime_validation/content.py:148-155`),
    and `:(literal)` is what makes the segment a NAME rather than a pathspec
    expression — MEASURED on the same git: `ls-tree --full-tree HEAD -- :!leg`
    exits 128 with `pathspec magic not supported by this command: 'exclude'`
    where `:(literal):!leg` exits 0, so a segment beginning with `:` would
    otherwise arrive here as an unreadable tree rather than as its own name.
    """
    done = _git_run(repo, "ls-tree", "--full-tree", revision, "--",
                    f":(literal){path}")
    if done is None:
        # `_git_run` answers this SAME `None` for a missing git binary and for
        # a probe that hit its 30s timeout (`#1048` round 5) — indistinguishable
        # from here, so the text says both rather than misnaming a timeout as
        # the rarer "no git on PATH" case or silently dropping the commoner one.
        return False, "git could not be run, or the probe timed out after 30s"
    if done.returncode != 0:
        said = " ".join(done.stderr.split())
        return False, said or f"`git ls-tree` exited {done.returncode}"
    if done.stdout.strip():
        return False, (f"`git ls-tree` lists an entry at {path} that "
                       f"`git rev-parse {revision}:{path}` could not resolve")
    return True, ""


def _leg_object_store(parent: Path, segment: str) -> Path | None:
    """Where the `segment` submodule's OBJECT STORE is under `parent` — the
    checked-out working tree when there is one, else the superproject's own
    copy of it — or `None` when this checkout cannot reach it at all.

    WHY THIS IS NOT `(parent / segment / ".git").exists()`, which is the test
    the caller used to make inline (`#1048`). That question is "is the leg's
    WORKING TREE checked out HERE", and a linked worktree never checks a
    submodule out: `git worktree add` writes the superproject's own tracked
    files and leaves every gitlink an empty directory. The store is not missing
    there, it is merely somewhere else — git keeps a submodule's objects in the
    SUPERPROJECT's common git directory at `modules/<name>`, and every linked
    worktree of that superproject shares it. The old test therefore answered
    "not materialized" for a checkout that could read the leg perfectly well,
    and `doc-health`'s release-inventory family turned that refusal into four
    members of `contract-v4.0` reported ABSENT AT HEAD from a worktree and
    present from the checkout the worktree was made from: one commit, two
    verdicts, neither of them about the release.

    The working tree is preferred whenever it IS checked out, so an ordinary
    checkout resolves exactly what it resolved before this existed.
    `--git-common-dir` is asked OF GIT rather than assembled from `.git` by
    hand, because the caller walks a CHAIN — `openXdox/spec` is a submodule of
    a submodule — so `parent` is itself a module store at every level past the
    first, and because this repository is mounted as a submodule in the
    aggregation workspace, where its own `.git` is a file and its common
    directory is `<agg>/.git/modules/openxFactory`.
    """
    checkout = parent / segment
    if (checkout / ".git").exists():
        return checkout
    common = _git_text(parent, "rev-parse", "--git-common-dir")
    if common is None:
        return None
    root = Path(common)
    store = (root if root.is_absolute() else parent / root) / "modules" / segment
    # `HEAD` is git's own first test for "this directory IS a git directory",
    # and it is what separates a real module store from the empty `modules/`
    # skeleton that a never-initialized submodule can leave behind. It proves
    # THE DIRECTORY and nothing about its contents, which is why the caller
    # asks separately whether the pinned commit is actually in it (Copilot on
    # PR #1051, `carved_reach.py:718`): a shallow or partially fetched store
    # passes this test and still cannot answer for the commit.
    return store if (store / "HEAD").is_file() else None


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
    at BY THIS COMMIT, and `effective_arrival(row)`'s `destination_path`: the
    row's own, unless a `re_destined:` block (RULED Q6) says a ruling has since
    moved the placement, in which case its `to_path` — `source()`'s own
    precedent, read here for the same reason. The answer is therefore as exact
    as the caller's: a commit that pinned an older leg reads the older leg's
    bytes, and nothing is read from the working tree.

    It answers `None` — and the caller's own answer stands — for a path in no
    row, a `not_moved` row, and a commit whose tree ANSWERS that it carries no
    such gitlink, which is every commit from BEFORE the shed: there the file is
    still in this repository's own tree and the ordinary read already
    succeeded.

    THAT ABSENCE IS CONFIRMED RATHER THAN INFERRED (`#1048` round 2). A
    `rev-parse <revision>:<segment>` that answers nothing says either "this
    tree has no such entry" or "this tree could not be read", and a store
    cloned `--filter=tree:0` whose promisor is unreachable is the second while
    looking exactly like the first — the commit object present, the tree
    object not. Taking that for an absence returned `None` here, which
    `release_inventory` reports as the member being ABSENT AT THE COMMIT: the
    phantom absence this path exists to refuse, arriving through the one read
    that had no probe. `_tree_entry_absent` above asks `ls-tree` which fact it
    is, and only the tree's own "no such entry" still answers `None`.

    It RAISES `CarveReachUnavailable` when the gitlink IS recorded and the leg's
    object store is not reachable from this checkout AT ALL — neither checked
    out here nor held as the superproject's own `modules/<name>` copy — for the
    reason the module docstring gives: an object store that is not on disk
    cannot be read, and a reader that quietly found nothing reports as a green
    bar. A LINKED WORKTREE IS NOT THAT CASE, and was refused as one until
    `#1048`; `_leg_object_store` above carries the why. The MOUNT path is
    tracked alongside the store so the refusal still names `openXdox` or
    `openXdox/spec` — the thing a reader can go and initialize — rather than a
    git directory nobody ever checked out.

    A STORE THAT EXISTS IS NOT YET A STORE THAT ANSWERS, and the pinned commit
    is verified in it before the walk moves on (Copilot on PR #1051). A shallow
    clone, an interrupted fetch, or a gitlink advanced past what the store was
    fetched at all leave a real git directory that simply does not carry the
    commit; without the probe the next level's `rev-parse` — or, at the last
    level, the caller's own blob read — would answer a plain `None`, and
    `release_inventory` would report the member ABSENT AT THE COMMIT. That is
    the same misattribution this whole path exists to prevent, arriving one
    layer lower, so it raises here and becomes the same repository-level skip.

    A RETIRED ROW IS NOT GUARDED HERE, AND THE DIVERGENCE FROM `source()` IS
    DELIBERATE (Copilot review of PR #1032, which asked for the guard). This
    is the one resolver whose question is TIME-INDEXED. `source()` answers
    about the working tree — one tree, the one that exists now — so a row a
    ruling has deleted has no answer and refusing is the only honest one. This
    function answers about THE COMMIT THE CALLER NAMES, through the leg THAT
    COMMIT pins. A retirement is an EVENT: the deletion lands at the leg at
    some commit, and every commit before it pins a leg that still carries the
    file. The `retired:` block, meanwhile, is read from the manifest in the
    WORKING TREE and says nothing about when the deletion landed — so a guard
    here would apply today's retirement to every commit ever asked about, and
    would break the exact property `scripts/hermes_runtime_validation/
    release.py` is built on: verifying an OLDER commit reads the leg that
    commit pinned, where the member is present and the read is correct.

    At a commit whose pinned leg no longer carries the file, this answers a
    path with no blob there, and the caller's own absence finding is the right
    verdict and the one it already produces: `scripts/doc_health/
    release_inventory.py` reports the member as VANISHED at that commit, and
    `hermes_runtime_validation.content.resolve_git_object` raises its own
    error. Neither is silent, and neither needs this function to decide for
    it. `tests/carve_manifest/test_carve_manifest.py::
    test_the_exact_commit_resolver_answers_for_a_retired_row_on_purpose` pins
    the divergence so it stays a decision rather than an omission.
    """
    key = str(path).replace("\\", "/")
    row = _rows().get(key)
    if row is None or row["disposition"] == "not_moved":
        return None
    destination, destination_path = effective_arrival(row)
    repo = REPO_ROOT
    mount = REPO_ROOT
    revision = commit
    for segment in MOUNTS[destination].relative_to(REPO_ROOT).parts:
        mount = mount / segment
        gitlink = _git_object_id(repo, revision, segment)
        if gitlink is None:
            absent, said = _tree_entry_absent(repo, revision, segment)
            if not absent:
                raise CarveReachUnavailable(
                    f"the pinned {destination} leg cannot be located "
                    f"at this commit: the tree {revision} names could not be "
                    f"read where {mount.relative_to(REPO_ROOT)}'s gitlink is "
                    f"recorded, so whether that gitlink is there is "
                    f"UNESTABLISHED rather than answered, and {key} cannot be "
                    f"read at the commit that pins it — git said: {said}. "
                    f"{INCOMPLETE_STORE_REMEDY}")
            return None
        store = _leg_object_store(repo, segment)
        if store is None:
            raise CarveReachUnavailable(
                f"the pinned {destination} leg is not materialized: "
                f"{mount.relative_to(REPO_ROOT)} carries no Git object store, so "
                f"{key} cannot be read at the commit that pins it. Run "
                f"`{INIT_COMMAND}` from the repository root.")
        if not _git_ok(store, "cat-file", "-e", f"{gitlink}^{{commit}}"):
            raise CarveReachUnavailable(
                f"the pinned {destination} leg is materialized but "
                f"incomplete: {mount.relative_to(REPO_ROOT)}'s object store "
                f"carries no commit {gitlink}, which is what the recorded "
                f"gitlink names, so {key} cannot be read at the commit that "
                f"pins it. {INCOMPLETE_STORE_REMEDY}")
        repo = store
        revision = gitlink
    return repo, revision, destination_path


def sources_under(prefix: str) -> dict[str, Path]:
    """Every manifest row under `prefix`, mapped to where its file is TODAY.

    For the readers that walk a TREE rather than name a file — the import-
    direction scanners, the serve-surface sweeps. Keyed by the pre-shed
    repository-relative path, so a caller's own reporting still names the path
    a reader of this repository's history will recognise. The
    `deleted_at_carve` row is omitted: it is nowhere, and a sweep is not the
    place to raise about it. A RETIRED row (RULED 5656343213) is omitted for
    exactly that reason and no other — it is nowhere too, and one retired row
    must not take a whole compositor sweep down with it. The refusal is kept
    for the callers that NAME a file (`source()`, `module()`,
    `shed_relpath()`), where asking for that one file is the caller's own
    mistake rather than an incident of walking a tree.
    """
    prefix = prefix.rstrip("/") + "/"
    out: dict[str, Path] = {}
    for key, row in _rows().items():
        if not key.startswith(prefix):
            continue
        if row.get("reason") == "deleted_at_carve":
            continue
        # THE RETIREMENT OMISSION IS A MOVED ROW'S, and the disposition test is
        # load-bearing rather than defensive (Copilot review of PR #1032,
        # round 6). `retired:` on a `not_moved` row is a document
        # `validate-carve-manifest.py` refuses (`carve-retired-not-moved`) —
        # but this module is imported by consumers that never run it, and
        # `source()` above resolves a `not_moved` row HERE, unconditionally,
        # before it reads any retirement. Omitting on `retired_at` alone made
        # this sweep disagree with `source()` about the same row and, worse,
        # silently drop a file that is RETAINED in this tree.
        if (row.get("disposition") != "not_moved"
                and retired_at(row)[1] is not None):
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
