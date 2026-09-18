#!/usr/bin/env python3
"""THE CITATION REMAINDER, REPORTED — a corpus-wide reading of every packet
citation this repository's resolution rule cannot resolve
(`packet-citation-report`, openxFactory `add-citation-remainder-report`, issue
#1053).

WHAT THIS IS, AND WHAT IT IS NOT. `release-realization`'s *A packet reference
resolves by identity, not by path* is the RULE; `scripts/packet_reference.py`
is that rule's shipped resolver, imported here UNCHANGED and consumed as a
library; `scripts/validate-pin-registrations.py`'s `check_citations` is the one
GATE that consumes it, over one field of registered pins. This is the REPORT.
It is not a gate, it is not a doc-health family, and it is NOT AN EDITOR: a
reference that resolves owes the citing record no edit, and this report states
that sentence's other half — **a reference that does NOT resolve owes the
citing record no edit FROM THIS REPORT EITHER**. There is no `--fix`, no
suggested spelling, no patch output, and nothing here writes any file it read.

THE READING IS DECLARED, NOT ASSUMED. Two readings taken by different recipes
are not comparable and this capability exists to produce a SERIES, so the file
population, the extraction pattern, the normalizations and the three choices
that decide which number is printed are all stated in the requirement and are
printed in every reading's own header. A reading that applied a different
pattern or a different choice is not a later point in the same series.

EXIT. Zero whatever it finds — nothing in the reported population has been
ruled a defect, and a tool able to exit non-zero acquires the meaning of a gate
the first time anybody wires it into a required check. A NON-ZERO exit means
the report COULD NOT RUN (an unreadable tree, a root that is not a git work
tree), never that it found something. There is no option that converts a
finding into a failure.

WHY THE RESOLVER IS THIS SCRIPT'S OWN SIBLING AND NOT THE SCANNED TREE'S. The
hand instrument this report reproduces loaded the resolver out of the tree it
measured, because it measured two revisions of THIS repository and "the same
reference answers differently against two roots" is equally true between two
revisions of one rule. A shipped report is a different case: it is one version
of one rule, it ships beside the resolver it consumes, and its own unit tests
read throwaway fixture trees that carry no `scripts/` at all. So the resolver
is loaded from this script's own directory, and the reading a run produces is
the reading THIS pair of files produces.

NO PATH UNDER THE CHANGES ROOT IS SPELLED IN THIS FILE. `scripts/` is inside
the file population, so every citation-shaped string written here would be a
token this report then counts — the mechanism the design measured at +1
remainder for vendoring its own measurement instrument. Every example below is
therefore written with an angle-bracket placeholder, a shape the extraction
pattern cannot match, and every literal prefix this script needs is built from
`CHANGES_ROOT` rather than spelled.

Run: `python3 scripts/report-citation-remainder.py [REPO_ROOT] [--json]
[--all] [--tokens] [--history] [--include PREFIX ...] [--exclude PREFIX ...]`.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# THE RESOLVER, LOADED BY LOCATION.
#
# `scripts/packet_reference.py` is importable by name, but it is loaded the way
# every other consumer in this estate loads a `scripts/` sibling — by location,
# with `scripts/` on `sys.path` first so its own hyphenated dependency resolves
# — so that this script runs identically from any working directory.
# ---------------------------------------------------------------------------

SCRIPTS_DIR = Path(__file__).resolve().parent


def _load_resolver():
    loaded = sys.modules.get("packet_reference")
    if loaded is not None and hasattr(loaded, "resolve"):
        return loaded
    path = SCRIPTS_DIR / "packet_reference.py"
    if str(SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPTS_DIR))
    spec = importlib.util.spec_from_file_location("packet_reference", path)
    if spec is None or spec.loader is None:  # pragma: no cover - defensive
        raise ImportError(f"cannot locate the packet resolver at {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["packet_reference"] = module
    spec.loader.exec_module(module)
    return module


packet_reference = _load_resolver()

RESOLVED = packet_reference.RESOLVED
DANGLING = packet_reference.DANGLING
AMBIGUOUS = packet_reference.AMBIGUOUS
NOT_A_PACKET_REFERENCE = packet_reference.NOT_A_PACKET_REFERENCE
IDENTITY_HALF = packet_reference.IDENTITY_HALF
FILE_HALF = packet_reference.FILE_HALF
CHANGES_ROOT = packet_reference.CHANGES_ROOT


class CouldNotRun(Exception):
    """The one non-zero exit this capability has.

    Raised where the report cannot READ the tree at all — never where it found
    something. The two are different facts wanting different repairs, and
    reporting them under one code sends a reader to the wrong one.
    """


# ===========================================================================
# § POPULATION — the file population, its exclusions, its refinements and the
# FOUR terms its arithmetic closes over (`packet-citation-report`, *The
# reported population is derived from a stated recipe*).
# ===========================================================================

#: The three default exclusions, each excluded for a stated reason: the
#: ARCHIVED corpus is frozen record whose citations may not be repaired; the
#: TEST corpus deliberately carries synthetic ids and deliberately-absent
#: files; SPEC KIT FEATS are another tool's artifacts citing packets
#: illustratively. The archive prefix is BUILT rather than spelled, for the
#: reason the module docstring gives.
DEFAULT_EXCLUSIONS = (
    f"{CHANGES_ROOT}/archive",
    "tests",
    "specs",
)

EXCLUSION_REASONS = {
    f"{CHANGES_ROOT}/archive": "frozen record; an archived packet's citations "
                               "may not be repaired",
    "tests": "fixtures; synthetic ids and deliberately-absent files",
    "specs": "Spec Kit feats; another tool's artifacts, citing illustratively",
}

#: THE ONE PATH NO REFINEMENT MAY REACH. A report that lists remainder
#: citations writes one citation token per remainder line, so a committed
#: report is read by the next run as a record citing every packet it reported
#: on — the report counting its own output and the series drifting upward by
#: its own act. The exclusion is declared BEFORE any such output is committed
#: and not after the first inflated reading: under the nightly wiring this
#: capability ships with, the reading is a workflow artifact written OUTSIDE
#: the scanned root and nothing is committed at all, so this fence is
#: structural today and live the day that changes. `health/` is the artifact
#: home this repository already keeps; the bare root spellings are where a
#: local run's redirect lands.
OUTPUT_PATH_EXCLUSIONS = (
    "health/citation-remainder.md",
    "health/citation-remainder.json",
    "citation-remainder.md",
    "citation-remainder.json",
)

#: A tracked entry's git mode, for the ONE entry class the population must read
#: out of the INDEX rather than off the filesystem. The link mode is not among
#: them and is deliberately not named here: every link this population meets is
#: decided by where its path RESOLVES, and a mode that answered "is this a
#: link?" beside a predicate that never asks would be a second, silent rule.
GITLINK_MODE = "160000"

#: The three skip terms, named once so the extent rule below and the arithmetic
#: that closes over them cannot drift apart.
TERM_NON_FILE = "non_file"
TERM_OUT_OF_ROOT = "link_leaving_root"
TERM_UNDECODABLE = "undecodable"


def git(root: Path, *args: str) -> str:
    """`git -C root …`, or `CouldNotRun`.

    Every git this report runs is a READ. A git that fails is a tree this
    report cannot read, which is the one non-zero exit it has.
    """
    code, out, err = git_status(root, *args)
    if code != 0:
        raise CouldNotRun(
            f"`git {' '.join(args)}` failed in {root}: "
            f"{err.strip() or 'no message'}")
    return out


#: THE AMBIENT GIT ENVIRONMENT THIS REPORT REFUSES TO INHERIT, and the estate's
#: own list rather than a second one — `scripts/carved_reach.py:796-807`, put
#: there for the same reason by Copilot `PRRT_kwDOTAvnrs6hjE-c`. Every figure
#: this report prints is read out of ONE index and ONE object store, and each
#: variable below can silently point git at another: `GIT_DIR`,
#: `GIT_COMMON_DIR` and `GIT_WORK_TREE` move the repository out from under
#: `-C`; `GIT_INDEX_FILE` answers `ls-files` from a different index;
#: `GIT_OBJECT_DIRECTORY` and `GIT_ALTERNATE_OBJECT_DIRECTORIES` move the
#: object store `diff` and `log` read; `GIT_REPLACE_REF_BASE` and replace refs
#: rewrite what an object IS. A reading taken through any of them is not a
#: reading of the root the caller named, and this capability's whole purpose is
#: a reproducible series.
SCRUBBED_GIT_ENVIRONMENT = (
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

INDEXED_GIT_CONFIG_ENVIRONMENT = re.compile(r"GIT_CONFIG_(?:KEY|VALUE)_[0-9]+")


def sanitized_git_environment() -> dict:
    """The environment every git this report runs is given.

    The scrub above, plus `GIT_NO_REPLACE_OBJECTS` beside the
    `--no-replace-objects` flag, because the two answer different halves: the
    flag covers the process this report starts and the variable covers any git
    that process starts for itself.

    THE USER'S GLOBAL AND SYSTEM CONFIG ARE NOT READ EITHER. Nothing this
    report does needs them — every git it runs is a read of a named root — and
    an ambient `core.quotePath`, `core.symlinks` or a pathspec alias would
    otherwise reach the enumeration this whole population is derived from.
    """
    environment = {
        name: value for name, value in os.environ.items()
        if name not in SCRUBBED_GIT_ENVIRONMENT
        and INDEXED_GIT_CONFIG_ENVIRONMENT.fullmatch(name) is None
    }
    environment["GIT_CONFIG_GLOBAL"] = os.devnull
    environment["GIT_CONFIG_SYSTEM"] = os.devnull
    environment["GIT_CONFIG_NOSYSTEM"] = "1"
    environment["GIT_NO_REPLACE_OBJECTS"] = "1"
    return environment


def git_status(root: Path, *args: str):
    """`git -C root …` returning `(returncode, stdout, stderr)`.

    A separate entry point because ONE of this report's gits is asked for its
    EXIT CODE rather than its output — `diff --quiet HEAD`, whose non-zero is
    the answer "the tracked content differs from the head" and not a failure to
    read the tree.

    THE ROOT IS RESOLVED TO AN ABSOLUTE PATH BEFORE IT REACHES `git`, AT THE
    SINK AND NOT ONLY AT THE CALLER. `REPO_ROOT` is caller-supplied text and
    every one of this report's gits is this one call, so the one place the
    normalization cannot be forgotten is here: an absolute path cannot begin
    with `-` and therefore cannot be read by git as an option however the
    caller spelled it. The refusal below is unreachable for a resolved path and
    is kept as the assertion it is — a root that somehow reached `git` as an
    option would be a run this report could not take, which is the one
    non-zero exit it has.
    """
    where = str(Path(root).resolve())
    if where.startswith("-"):  # pragma: no cover - an absolute path cannot
        raise CouldNotRun(
            f"refusing a repository root that reads as an option: {root!r}")
    try:
        result = subprocess.run(
            ["git", "--no-replace-objects", "-C", where, *args],
            capture_output=True, text=True,
            env=sanitized_git_environment())
    except OSError as error:
        raise CouldNotRun(f"git could not be run: {error}") from error
    return result.returncode, result.stdout, result.stderr


def work_tree_root(path: Path) -> Path:
    """The WORK-TREE ROOT containing `path` — the root this report reads.

    `--is-inside-work-tree` ANSWERS TRUE FOR A SUBDIRECTORY, AND A SUBDIRECTORY
    IS NOT THIS POPULATION. `git ls-files` run in one enumerates that subtree
    alone and returns paths relative to it, and `PacketIndex` then looks for the
    changes root BENEATH it, so every citation the subtree carries reads as
    DANGLING. Measured at `docs/` in this repository: 79 distinct tokens, 78 of
    them in the remainder, against 601 and 81 at the root — a reading that is
    WRONG rather than one the report declined to take, published at exit 0.
    (Copilot `PRRT_kwDOTAvnrs6jtYen`.)

    SO THE NAMED PATH IS RESOLVED TO ITS WORK-TREE TOP RATHER THAN REFUSED. The
    operand names the repository and DEFAULTS TO THE WORKING DIRECTORY, so a
    refusal would fail the ordinary run taken from anywhere but the top; and the
    two-case exit contract keeps the non-zero exit for a report that COULD NOT
    RUN, which a report standing inside a repository plainly can. A path inside
    no work tree at all still cannot, and still exits there.

    THE IDIOM IS THE ESTATE'S AND NOT A SECOND ONE WRITTEN HERE:
    `scripts/sequenced_after.py`'s `_git_toplevel` and `scripts/scope_globs.py`'s
    `_git_toplevel` resolve a caller-named path exactly this way and convert
    both failure arms — inside no work tree, and git not runnable at all — into
    their own "could not run" finding. `git()` above already converts both.
    """
    return Path(git(path, "rev-parse", "--show-toplevel").strip())


def segment_match(path: str, prefix: str) -> bool:
    """Whether `path` stands under `prefix`, matched ON SEGMENT BOUNDARIES.

    A path matches where it EQUALS the prefix with any trailing `/` removed, or
    begins with that plus `/`. This is the estate's own idiom rather than a new
    one — `scripts/validate-carve-manifest.py`'s `in_surface`, whose docstring
    states the reason in one line: *"Segment-aware: `scripts/ideation_dashboard`
    does not swallow `scripts/ideation_dashboard_old/x.py`, which a bare
    `startswith` would."* A bare string prefix swallows a sibling directory
    whose name merely begins the same way, and the population would then differ
    between two readings by a directory neither reader named.
    """
    stem = prefix.rstrip("/")
    if not stem:
        return False
    return path == stem or path.startswith(stem + "/")


def matches_any(path: str, prefixes) -> bool:
    return any(segment_match(path, prefix) for prefix in prefixes)


@dataclass(frozen=True)
class TrackedEntry:
    """One row of the tracked-entry listing: its path and its git mode."""

    path: str
    mode: str


@dataclass
class Population:
    """What the report read, and what it skipped, term by term.

    THE POPULATION IS TWO NUMBERS AND NEVER ONE. A report that skips entries it
    counted has two different populations — the tracked ENTRIES the exclusions
    leave and the FILES it actually read — and a single "files in scope" figure
    is ambiguous between them by exactly the number of entries skipped.

    AND THE CLOSURE HAS THREE SKIP TERMS, NOT TWO. A symbolic link whose target
    leaves the root is a tracked FILE that reaches no decoder: it is not the
    submodule link the non-file term is about, which IS a directory and has no
    text, and it never reaches a decoder, so it belongs to neither of the other
    two terms. Its term is PRINTED EVEN WHERE IT IS ZERO, for the reason the
    AMBIGUOUS row is: a term omitted whenever nothing lands in it teaches its
    readers not to look for it, and this is the term whose non-zero value means
    the report DECLINED to read text a naive implementation would have reported
    as this corpus's.

    AND EACH TERM IS DEFINED BY ITS EXTENT AND NOT BY ITS NAME, SO THAT NO
    TRACKED ENTRY FALLS BETWEEN TWO OF THEM. The OUT-OF-ROOT-LINK term owns
    exactly the tracked LINKS whose resolved path stands outside the root. The
    NON-FILE term owns every OTHER tracked entry that is not a readable regular
    file once resolved — the submodule gitlink, a directory, and every tracked
    link the first term does not take: one resolving inside the root to
    something missing, one resolving inside the root to a DIRECTORY, and one
    with no resolved path at all because its chain loops or cannot be read. A
    name is not an extent, and this is where the difference is paid: a link
    that dangles inside the root is none of the three things the terms are
    NAMED for, so an arithmetic resting on the names alone has nowhere to put
    it and fails to close on an entry class the population rule itself admits.

    A FOURTH TERM IS DECLINED, and the decline is the mirror of the third
    term's keep: the third term earns its own row because a non-zero value in
    it is a fact a reader needs — the report DECLINED to read text a naive
    implementation would have reported as this corpus's — while a link reaching
    no readable file inside the root offers text to NO implementation and would
    tell a reader only that the tree carries a broken link, which is a fact
    about the tree and not about this corpus's citations. It contributes no
    token for the reason the gitlink contributes none, and it is counted where
    the gitlink is counted.
    """

    tracked_entries_total: int = 0
    entries_in_scope: int = 0
    files_read: int = 0
    skipped_non_file: list = field(default_factory=list)
    skipped_link_leaving_root: list = field(default_factory=list)
    skipped_undecodable: list = field(default_factory=list)
    exclusions: tuple = ()
    include: tuple = ()
    exclude: tuple = ()
    output_paths_excluded: tuple = ()
    refinement_named_output_path: tuple = ()

    @property
    def arithmetic_closes(self) -> bool:
        return self.entries_in_scope == (
            self.files_read + len(self.skipped_non_file)
            + len(self.skipped_link_leaving_root)
            + len(self.skipped_undecodable))


#: A LINK CHAIN IS WALKED HERE RATHER THAN HANDED TO `Path.resolve()`, because
#: the term's extent is a fact about the PATH and `resolve()` answers a
#: question about what STANDS at one. The cap bounds a chain no cycle catches.
MAX_LINK_HOPS = 64


def resolved_entry_path(root: Path, rel: str):
    """The path a tracked entry's own chain JOINS TO, read step by step.

    A TRACKED PATH'S RESOLVED PATH IS A FACT ABOUT THE PATH ITSELF AND NOT
    ABOUT WHETHER ANYTHING STANDS AT IT: every step is read in turn — the
    entry's own last component and every PARENT directory's, in the one lexical
    walk — each link replaced by its own target text resolved from the
    directory the link stands in, and `..` and `.` resolved away as they are
    reached, so an entry whose own target or whose parent's target is simply
    MISSING still has a resolved path and stands wherever that join lands. That is the whole reason this walk is here and `Path.resolve()`
    is not: `resolve()` is a filesystem answer, and a term whose extent is "the
    links that leave the root" must take a DANGLING link that leaves the root
    and leave a dangling link that does not.

    EVERY COMPONENT OF A TARGET IS READ, NOT ONLY ITS LAST. A target is a PATH
    and its own intermediate segments may be links in turn: where `nested`
    points outside the root and a tracked `link` points at `nested/file`, a
    walk that joined the target lexically and then asked only whether the
    JOINED path was itself a link would answer `<root>/nested/file`, pass the
    containment test, and read a file outside the repository as this corpus's.
    So the target's segments are pushed back onto the walk and resolved like
    any others, which is also why `..` is applied to what has been resolved so
    far rather than cancelled against unread text. (Copilot
    `PRRT_kwDOTAvnrs6jshPX`.)

    Returns `None` — NO resolved path at all — only where the report cannot
    itself walk the chain: it exceeds the hop bound, which a loop always does,
    or it carries, AT ANY COMPONENT, a link whose own target text cannot be
    read. Such an entry is
    not a link that leaves the root; it is an entry that is not a readable
    regular file once resolved, and the non-file term owns it.
    """
    anchor = Path(root.anchor) if root.anchor else Path(root.root or "/")
    current = root
    # `pending` IS A STACK AND NOT A QUEUE: it is built REVERSED and popped from
    # its END, so its LAST element is the NEXT component to walk. A target's
    # components are therefore `extend`ed — appended, which is pushed onto the
    # TOP — and are walked BEFORE the suffix still waiting beneath them, which
    # is the order the walk needs. Spelled out because the orientation reads
    # backwards at a glance and has been read backwards in review.
    pending = [part for part in reversed(rel.split("/")) if part]
    hops = 0
    while pending:
        part = pending.pop()
        if part == ".":
            continue
        if part == "..":
            current = current.parent
            continue
        candidate = current / part
        try:
            is_link = candidate.is_symlink()
        except OSError:  # pragma: no cover - an unreadable path component
            return None
        if not is_link:
            current = candidate
            continue
        hops += 1
        if hops > MAX_LINK_HOPS:
            return None
        try:
            target = os.readlink(candidate)
        except OSError:
            return None
        if target.startswith("/"):
            current = anchor
        # Pushed onto the TOP of the stack, reversed so the target's FIRST
        # component is popped first — `[…, suffix] + [last, …, first]`.
        pending.extend(part for part in reversed(target.split("/")) if part)
    return current


def inside_root(root: Path, path: Path) -> bool:
    """Whether a resolved path still stands under the repository root."""
    try:
        return path.is_relative_to(root)
    except (OSError, ValueError):  # pragma: no cover - defensive
        return False


def tracked_entries(root: Path) -> list:
    """Every tracked entry in the tree, with its mode.

    `git ls-files` returns TRACKED ENTRIES and not files — a mode-160000
    submodule gitlink is an entry with no text of its own — which is why the
    mode is read here rather than inferred from the filesystem afterwards.
    """
    rows = []
    for line in git(root, "ls-files", "-s", "-z").split("\0"):
        if not line:
            continue
        meta, _, path = line.partition("\t")
        if not path:
            continue
        rows.append(TrackedEntry(path=path, mode=meta.split(" ", 1)[0]))
    return rows


#: The three verdicts `admits` returns. The middle one is a path EXCLUDED
#: whatever a refinement said, whose naming is still reported back to the
#: caller so a run states what it was asked for as well as what it did.
ADMITTED = "admitted"
EXCLUDED = "excluded"
REFUSED_OUTPUT_PATH = "refused-output-path"


def admits(path: str, include, exclude) -> str:
    """Whether one tracked entry's path stands in the population.

    THE REFINEMENT SEMANTICS ARE THE SPECIFICATION'S AND NOT THIS
    REALIZATION'S: a prefix matches on path-segment boundaries; an admission
    RE-ADMITS into the stated population rather than replacing it; a removal is
    applied LAST and WINS over any admission naming the same path, so the pair
    is order-independent.
    """
    if matches_any(path, DEFAULT_EXCLUSIONS) and not matches_any(path, include):
        return EXCLUDED
    if matches_any(path, exclude):
        return EXCLUDED
    if matches_any(path, OUTPUT_PATH_EXCLUSIONS):
        # NEITHER FLAG CAN RE-ADMIT THE REPORT'S OWN OUTPUT. The exclusion is
        # kept rather than the refinement refused, because a refusal would be a
        # run that did not happen and the only non-zero exit this capability
        # has means the report could not run at all.
        return (REFUSED_OUTPUT_PATH if matches_any(path, include)
                else EXCLUDED)
    return ADMITTED


def output_paths_named_by(include) -> list:
    """The report's own output paths a refinement named, whether or not the
    tree carries one — a caller is told its refinement was declined either
    way."""
    return [output_path
            for prefix in include
            for output_path in OUTPUT_PATH_EXCLUSIONS
            if segment_match(output_path, prefix)]


def build_population(entries, include=(), exclude=()):
    """The tracked entries in scope, before any file is opened.

    THE REFINEMENT SEMANTICS ARE THE SPECIFICATION'S AND NOT THIS
    REALIZATION'S: a prefix matches on path-segment boundaries; an admission
    RE-ADMITS into the stated population rather than replacing it; a removal is
    applied LAST and WINS over any admission naming the same path, so the pair
    is order-independent. And the report's own output path is the one path no
    refinement may reach — it is kept excluded under every one of them.

    Returns `(population, in_scope_entries)`.
    """
    in_scope = []
    named_output = []
    for entry in entries:
        verdict = admits(entry.path, include, exclude)
        if verdict is ADMITTED:
            in_scope.append(entry)
        elif verdict is REFUSED_OUTPUT_PATH:
            named_output.append(entry.path)
    named_output.extend(
        path for path in output_paths_named_by(include)
        if path not in named_output)
    population = Population(
        tracked_entries_total=len(entries),
        entries_in_scope=len(in_scope),
        exclusions=DEFAULT_EXCLUSIONS,
        include=tuple(include),
        exclude=tuple(exclude),
        output_paths_excluded=OUTPUT_PATH_EXCLUSIONS,
        refinement_named_output_path=tuple(sorted(set(named_output))),
    )
    return population, in_scope


def entry_disposition(root: Path, entry: TrackedEntry):
    """Which of the three skip terms one tracked entry belongs to, or the
    target to read it from — decided by EXTENT, in one place.

    Returns `(term, target)`: `term` is `None` where the entry is a readable
    regular file inside the root and `target` is the path to read it from;
    otherwise `term` names the skip term and `target` is `None`.
    """
    if entry.mode == GITLINK_MODE:
        # A submodule gitlink names a directory with no text of its own, and
        # the mode is read from the INDEX because the working tree may carry
        # nothing at that path at all.
        return TERM_NON_FILE, None
    target = resolved_entry_path(root, entry.path)
    if target is None:
        # A chain that loops or cannot be read has NO resolved path, so it is
        # not an entry that LEAVES the root — it is an entry that is not a
        # readable regular file once resolved.
        return TERM_NON_FILE, None
    if not inside_root(root, target):
        # THE OUT-OF-ROOT TERM IS A PREDICATE OVER THE WHOLE TRACKED PATH and
        # not over an entry that happens to be a link itself: a tracked entry
        # REACHED THROUGH one leaves the root exactly as a link that is one
        # does, a PARENT directory component included. A tracked regular file
        # under a directory that has since become a link out of the tree is the
        # case that pays for it — its own last component is no link, it stands
        # outside the root all the same, and counting it among the non-files
        # would say the report declined it for carrying no text when what it
        # declined was text that is not this corpus's.
        return TERM_OUT_OF_ROOT, None
    if not target.is_file():
        # Missing inside the root, or a DIRECTORY inside the root: neither is a
        # readable regular file once resolved.
        return TERM_NON_FILE, None
    return None, target


def read_population_text(root: Path, in_scope, population: Population):
    """Each in-scope entry's TEXT, as it stands, with every skip counted.

    Three skips, each its own term and each defined by its EXTENT. A TRACKED
    ENTRY THAT IS NOT A READABLE REGULAR FILE ONCE RESOLVED has no text this
    report can read, and counting one as an unreadable file both misstates the
    population's size and invites an implementation to recover text from it. A
    TRACKED ENTRY WHOSE RESOLVED PATH LEAVES THE REPOSITORY ROOT is refused
    before it is read, ANY tracked entry and not only one that is itself a
    link: the ordinary "is this a file?" test FOLLOWS a symbolic link — at the
    entry's own last component and at every PARENT component alike — and
    answers about what stands at the end of them, so an implementation that
    asks only that question reports text that is not this corpus's as this
    corpus's citations.
    AND A FILE THAT DOES NOT DECODE is skipped, counted and reported: never
    replacement-decoded, because bytes that are not text can yield matches no
    record wrote, and never fatal.

    A read that fails for a reason that is not a DECODE failure is not the
    undecodable term's: that term exists to record text the report DECLINED to
    read, and an entry it could not open offered none.
    """
    buckets = {
        TERM_NON_FILE: population.skipped_non_file,
        TERM_OUT_OF_ROOT: population.skipped_link_leaving_root,
        TERM_UNDECODABLE: population.skipped_undecodable,
    }
    texts = []
    for entry in in_scope:
        term, target = entry_disposition(root, entry)
        if term is not None:
            buckets[term].append(entry.path)
            continue
        try:
            text = target.read_bytes().decode("utf-8")
        except UnicodeDecodeError:
            buckets[TERM_UNDECODABLE].append(entry.path)
            continue
        except OSError:
            buckets[TERM_NON_FILE].append(entry.path)
            continue
        population.files_read += 1
        texts.append((entry.path, text))
    for bucket in buckets.values():
        bucket.sort()
    return texts


# ===========================================================================
# § TOKEN GRAMMAR — the extraction pattern, the normalizations it applies and
# the order those are applied in (*The reported population is derived from a
# stated recipe*).
# ===========================================================================

#: THE EXTRACTION PATTERN, written here because a requirement that promised a
#: stated grammar and then stated only what the grammar is afterwards corrected
#: for would not have stated it. Two implementations can honour every
#: normalization and still extract different tokens, and their remainders are
#: then incomparable for a reason neither report can show.
TOKEN_RE = re.compile(CHANGES_ROOT + r"/[A-Za-z0-9][A-Za-z0-9._\-/]*")

#: The estate's canonical change-id grammar, restated rather than imported so
#: this section reads as one rule: `scripts/proposal-support.py`'s
#: `CHANGE_ID_RE`. It admits an identifier ending in a letter, a digit, `.`,
#: `_` or `-`, and admits `/` in no identifier at all — which is the whole
#: predicate the resolve-first safeguard below is written against.
GRAMMAR_ADMITTED_TRAILING = tuple("._-")

#: The two normalizations this specification names, and their names in a
#: reading's own normalization record.
SEPARATOR_STRIPPED = "trailing-path-separator-stripped"
FULL_STOP_STRIPPED = "trailing-full-stop-stripped"

#: The characters a path may be spelled out of, for the probe that reads a
#: LONGER path off a citing line.
#: The characters a path run is made of. THE RUN IS SCANNED AND NOT MATCHED: a
#: `[...]*$` pattern searched over a prefix retries at every start position and
#: is super-linear on a long line, while the same answer read backwards from the
#: end is one pass.
PATH_RUN_CHARACTERS = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-/")


def trailing_path_run(text: str) -> str:
    """The longest run of path characters ENDING `text`."""
    index = len(text)
    while index and text[index - 1] in PATH_RUN_CHARACTERS:
        index -= 1
    return text[index:]


def strip_trailing_separator(spelled: str):
    """The ONE unconditional strip, and it is unconditional because the GRAMMAR
    makes it one: no identifier may carry `/`, so stripping it can suppress no
    valid citation, and the deduplication choice depends on it — a directory
    citation and its unslashed sibling are ONE token and not two.
    """
    stripped = spelled.rstrip("/")
    return stripped, (stripped != spelled)


def has_traversal_segment(token: str) -> bool:
    """Whether a token carries a `..` segment — a path that walks UP.

    `scripts/packet_reference.py:349` refuses such a path outright, which is a
    containment rule and not a spelling preference: a reference that walks out
    of the directory it names is the caller's question and never this reader's.
    """
    return any(part == ".." for part in token.split("/"))


def normalise_token(spelled: str, resolves):
    """One raw match, normalized — and the ORDER is the specification's.

    RESOLUTION IS TRIED FIRST BEFORE ANY TRAILING CHARACTER THE CHANGE-ID
    GRAMMAR ADMITS IS STRIPPED, and a token that resolves AS EXTRACTED is
    reported as it resolved, carries no normalization record and takes no
    normalization class. The predicate is the GRAMMAR'S and not a list of
    punctuation marks: a trailing full stop can be an identifier's own last
    character exactly as a trailing hyphen can, and a report that stripped it
    unconditionally would rewrite a VALID packet id and report the citing
    record as dangling — invisibly, and for a fact about a regular expression
    rather than about the record. A trailing character the grammar admits and
    this specification names no normalization for is LEFT WHERE IT STANDS: `-`,
    `_`, a letter and a digit are all admitted and none is stripped here, the
    hyphen's own suspicion being a CLASS the class predicates below decide and
    never a strip.

    Returns `(token, normalizations)`.
    """
    token = spelled
    normalizations: list[str] = []
    while True:
        token, separator = strip_trailing_separator(token)
        if separator and SEPARATOR_STRIPPED not in normalizations:
            normalizations.append(SEPARATOR_STRIPPED)
        if not token.endswith("."):
            break
        if has_traversal_segment(token):
            # A `..` SEGMENT IS NOT AN IDENTIFIER'S LAST CHARACTER, and this
            # normalization is for a SENTENCE'S full stop caught on the end of
            # a citation. Stripping one dot off `..` turns a path that walks UP
            # into one the resolver accepts — it refuses `..` deliberately
            # (`scripts/packet_reference.py:349`), and its own `_normalised`
            # then drops the surviving `.` segment — so `<root>/<id>/..`, which
            # names the changes root, would be reported as a citation OF `<id>`,
            # resolved or dangling according to whether that packet happens to
            # stand here. A report that rewrites a traversal into a citation is
            # inventing the citation, which is the one thing this report may
            # never do. (Copilot `PRRT_kwDOTAvnrs6jsy7w`.)
            break
        if resolves(token):
            break
        candidate = token[:-1]
        if candidate.endswith(CHANGES_ROOT) or candidate.endswith(CHANGES_ROOT + "/"):
            break  # a token that is only the changes root is not a citation
        token = candidate
        if FULL_STOP_STRIPPED not in normalizations:
            normalizations.append(FULL_STOP_STRIPPED)
    return token, tuple(normalizations)


@dataclass(frozen=True)
class Occurrence:
    """One citation, at one line of one file, exactly as it was written there.

    `raw` IS A PER-OCCURRENCE VALUE AND NEVER A SINGULAR FIELD ON THE TOKEN:
    normalization happens before deduplication, so raw spellings that differ —
    a slash-terminated citation and its unslashed sibling — do collapse into
    one token, and it is the OCCURRENCE that owns `raw` so every raw spelling
    survives beside its own `path:line`. `raw == token` at an occurrence where
    no normalization fired.
    """

    path: str
    line: int
    raw: str
    normalizations: tuple = ()
    signals: tuple = ()
    truncation_probes: tuple = ()
    truncation_evidence: str | None = None

    @property
    def at(self) -> str:
        return f"{self.path}:{self.line}"


# ===========================================================================
# § PREDICATES AND SIGNAL MATCHERS — the whole of what this report ASSERTS and
# what it SUSPECTS, one function each, in one delimited section so that a
# reader checking a class total or a flag against the requirement reads one
# place. Every rule below is promoted `SHALL` text in
# `specs/packet-citation-report/spec.md`; none of it is this realization's.
#
# The section is a SECTION and not a second module on purpose: the packet names
# ONE script file three times (`tasks.md` § 2.1, `proposal.md`'s
# `code_surface:` gloss, `design.md` D2) and a module split is a scope move
# that takes a ruling rather than a writer's own judgment.
# ===========================================================================

#: THE REPOSITORY-NAME VOCABULARY, CLOSED. It is stated rather than derived
#: because this repository carries no machine-readable enumeration of its
#: siblings: the estate's repository identifiers are the aggregation's
#: `.gitmodules` submodule paths and that file is not in this tree. The last
#: two names are ONE estate under the two spellings this corpus writes it in.
#: An implementation SHALL NOT widen this set; a corpus needing a wider one
#: takes a RULING, exactly as the fixture-path location set does.
REPOSITORY_VOCABULARY = frozenset({
    "codexfactory",
    "opsxfactory",
    "ledgerxfactory",
    "openxwallet",
    "hermes-install",
    "xfactory-hermes-install",
})

#: THIS repository, in the two spellings a qualifier can name it by. A
#: qualifier naming THIS repository fires NO signal: a citation qualified by
#: one of them is an IN-TREE citation, and every trailing parenthetical of that
#: shape measured in this corpus names this repository.
OWN_REPOSITORY_SPELLINGS = frozenset({"openxfactory", "opensoft/openxfactory"})

#: The decoration a bare qualifier word may carry in prose, stripped from both
#: ends before the vocabulary is consulted. It is
#: `scripts/validate-pin-registrations.py`'s `_TOKEN_DECORATION` widened by `*`
#: and `_`, because that constant was written for a YAML `cited_to:` line and
#: this report reads MARKDOWN PROSE, where emphasis markers are decoration on a
#: word in exactly the way backticks are decoration on a word in YAML.
TOKEN_DECORATION = "`'\"“”()[]{}<>,;§*_"

#: The characters that continue a NAME, for the one boundary the path-joined
#: signal is written against: a longer word that merely ENDS in a vocabulary
#: name is not that repository.
NAME_CHARS = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                 "abcdefghijklmnopqrstuvwxyz0123456789._-")

#: A forge blob-or-tree URL, anchored so that it must run straight into the
#: token: scheme, the `github.com` host, ONE owner segment, ONE repository
#: segment, `/blob/` or `/tree/`, ONE ref segment and `/`. It is the REPOSITORY
#: segment that is matched and never the OWNER segment, because a transfer
#: moves the owner segment alone and a repository's own name is unchanged by
#: one.
FORGE_URL_RE = re.compile(
    r"https?://github\.com/"
    r"(?P<owner>[A-Za-z0-9._\-]+)/(?P<repo>[A-Za-z0-9._\-]+)"
    r"/(?:blob|tree)/(?P<ref>[A-Za-z0-9._\-]+)/\Z")

#: The custody-locator scheme this corpus writes OpsxFactory citations in:
#: the literal prefix, ONE owner segment, `/`. The scheme names its repository
#: ITSELF rather than by any word, which is why it is in the signal set at all;
#: the same prefix followed by a command name, a subject or a workflow locator
#: fires nothing, because neither is an owner segment followed by a path.
#:
#: THE OWNER IS ONE SEGMENT, which is what makes an owner CONTAINING `:` or `/`
#: no owner: the class below admits neither, and the pattern must then run out
#: at the token's own start (`\Z` over `line[:start]`), so `opsx:own:er/` and
#: `opsx:own/er/` each fail to match rather than matching some shorter thing.
#: An EMPTY owner fails on the `+`.
CUSTODY_SCHEME_RE = re.compile(
    r"(?:^|(?a:\W))opsx:(?P<owner>[A-Za-z0-9._\-]+)/\Z")

#: The character class BOTH halves of the locator are drawn from, spelled once.
LOCATOR_SEGMENT_CHARACTERS = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-")


def locator_path(text: str) -> bool:
    """Whether the text standing where the locator's PATH stands is one.

    THE PATH IS THE CITED TOKEN ITSELF, which is what "the token is immediately
    preceded by the scheme, one owner segment and `/`" makes it: the prefix ends
    where the token begins, so everything the locator's path is made of is the
    token. So the grammar's second half is a predicate over the token AS IT WAS
    WRITTEN — one or more `/`-separated segments, each of one or more characters
    from the class above.

    AN EMPTY SEGMENT IS THE ARM THAT DOES THE WORK: a repeated slash inside the
    path and a trailing slash at the end of it each leave one, and neither is a
    locator. The character arm is stated because the grammar states it, and is
    the boundary this report keeps against its own extraction pattern, which
    admits the same class and `/` and nothing else — a later widening of that
    pattern must not widen the locator silently.
    """
    return bool(text) and all(
        segment and not (set(segment) - LOCATOR_SEGMENT_CHARACTERS)
        for segment in text.split("/"))

#: A trailing parenthetical: at most ONE space, then `(`, then its content,
#: then `)`. More than one space, any further content inside the parentheses,
#: or a parenthetical that is not the next thing after the token fires nothing.
TRAILING_PARENTHETICAL_RE = re.compile(r"^ ?\((?P<inner>[^()]*)\)")

#: The five signal ids, in the order the requirement names them.
SIGNAL_PATH_JOINED = "path-joined-prefix"
SIGNAL_FORGE_URL = "forge-url"
SIGNAL_QUALIFIER_WORD = "bare-qualifier-word"
SIGNAL_CUSTODY_SCHEME = "custody-locator-scheme"
SIGNAL_TRAILING_PAREN = "trailing-parenthetical"

SIGNALS = (SIGNAL_PATH_JOINED, SIGNAL_FORGE_URL, SIGNAL_QUALIFIER_WORD,
           SIGNAL_CUSTODY_SCHEME, SIGNAL_TRAILING_PAREN)

#: THE WINDOW, fixed and closed: the citing LINE plus the THREE LINES ABOVE it.
#: It is a property of the CAPABILITY and not of a run — no caller option
#: varies it — because a suspicion whose reach moves between runs makes two
#: readings of one corpus disagree for a reason neither reading records.
WINDOW_LINES_ABOVE = 3

#: The one flag this report carries. A CLASS is what the report ASSERTS; a FLAG
#: is what it SUSPECTS, and a flag is never written into the class field and
#: never counted in a class total.
FLAG_CROSS_REPO = "possibly-cross-repo"

#: The class vocabulary, CLOSED at four members. An implementation SHALL NOT
#: add a member to it or rename one.
CLASS_TRUNCATED = "truncated"
CLASS_PUNCTUATION_STRIPPED = "punctuation-stripped"
CLASS_FIXTURE_PATH = "fixture-path"
CLASS_UNCLASSIFIED = "unclassified"

CLASS_VOCABULARY = (CLASS_TRUNCATED, CLASS_PUNCTUATION_STRIPPED,
                    CLASS_FIXTURE_PATH, CLASS_UNCLASSIFIED)

#: The three probes that decide `truncated`, named by their spec letters.
PROBE_LONGER_PATH = "longer-path-on-the-line"
PROBE_PLACEHOLDER = "placeholder-opens-after-the-token"
PROBE_SPLIT_LITERAL = "rejoined-across-a-split-string-literal"

#: The `fixture-path` locations, MEASURED rather than an author's list — the
#: probe that caught 17 of 18 hand-classified fixture entries with ZERO false
#: positives, with the nested-`tests/` location carrying the entries whose
#: citing test ASSERTS the cited file's absence. CLOSED: an implementation
#: SHALL NOT widen it.
FIXTURE_TOP_LEVEL = "examples"
FIXTURE_GATE_RECORDS = "ideation/dashboard/gate-records"
FIXTURE_CONTRACTS_ROOT = "contracts"
FIXTURE_NESTED_TESTS = "tests"


def _is_vocabulary_name(word: str) -> bool:
    """Whether a bare word names a repository in the closed vocabulary.

    A NAME MATCHES WITHOUT REGARD TO CASE. Exact case is the rule this corpus
    does not keep — one estate's name is written in six different cases and
    another's is written in lower case more often than in its canonical one —
    and case-insensitive matching is what this estate's own qualifier reader
    already does.
    """
    return word.strip(TOKEN_DECORATION).lower() in REPOSITORY_VOCABULARY


def _names_this_repository(word: str) -> bool:
    """Whether a bare word names THIS repository, which fires no signal."""
    return word.strip(TOKEN_DECORATION).lower() in OWN_REPOSITORY_SPELLINGS


def signal_path_joined_prefix(line: str, start: int) -> bool:
    """(1) A PATH-JOINED PREFIX naming another repository.

    Fires where the citing line carries, ending immediately before the token, a
    vocabulary name followed by `/`, the character before that name being
    absent or NOT one of `A-Z`, `a-z`, `0-9`, `.`, `_` or `-`. The name matched
    is the SEGMENT immediately before the token, so an enclosing directory
    prefix does not prevent the match and a longer word that merely ends in a
    vocabulary name fires nothing.
    """
    before = line[:start]
    if not before.endswith("/"):
        return False
    stem = before[:-1]
    for name in REPOSITORY_VOCABULARY:
        if len(stem) < len(name):
            continue
        if stem[-len(name):].lower() != name:
            continue
        boundary = stem[:-len(name)]
        if boundary and boundary[-1] in NAME_CHARS:
            continue
        return True
    return False


def signal_forge_url(line: str, start: int) -> bool:
    """(2) A GITHUB BLOB OR TREE URL naming another repository.

    Fires where the token is immediately preceded on the citing line by
    `http://` or `https://`, the host `github.com`, ONE owner segment, ONE
    repository segment naming a vocabulary member, `/blob/` or `/tree/`, ONE
    ref segment, and `/`. A URL whose repository segment names THIS repository
    fires nothing, and a forge URL alone — without a repository segment the
    vocabulary recognizes — is no signal.
    """
    match = FORGE_URL_RE.search(line[:start])
    if match is None:
        return False
    return match.group("repo").lower() in REPOSITORY_VOCABULARY


def word_immediately_before(before: str) -> str:
    """The WORD immediately before the token, decoration and all.

    A word is a whitespace-delimited run, and DECORATION IS NOT PART OF ONE:
    the decoration set is stripped from the text between the word and the token
    before the run is read, so that `` <name> `<token>` `` — the spelling this
    corpus actually writes a qualified citation in, the qualifier and the token
    separated by a backtick rather than by a space — reads the qualifier as the
    word immediately before the token. A run that is nothing BUT decoration is
    not a word; the word before it is.

    A GLUED PATH PREFIX IS NOT A WORD EITHER, and needs no special case: `/` is
    not decoration, so `xFactories/LedgerxFactory/` survives the strip whole,
    fails the vocabulary as the path it is, and is judged by the path-joined
    signal, which is the signal written for it.
    """
    trimmed = before.rstrip(TOKEN_DECORATION + " \t")
    words = trimmed.split()
    return words[-1] if words else ""


def signal_bare_qualifier_word(lines, lineno: int, start: int) -> bool:
    """(3) A BARE QUALIFIER WORD naming another repository, inside the window.

    A word is a whitespace-delimited run, stripped at both ends of the
    decoration set and read without regard to case. ON THE CITING LINE it is
    the word IMMEDIATELY BEFORE the token; ON EACH OF THE THREE LINES ABOVE it
    is ANY word on the line, because "immediately before" names nothing on a
    line the token does not stand on. This is the ONLY one of the five that can
    fire off the citing line; the other four are relations to the token itself.

    `lines` is the file's lines, `lineno` the citing line's 1-based number.
    """
    line = lines[lineno - 1]
    previous = word_immediately_before(line[:start])
    if previous and _is_vocabulary_name(previous) \
            and not _names_this_repository(previous):
        return True
    first = max(0, lineno - 1 - WINDOW_LINES_ABOVE)
    for above in lines[first:lineno - 1]:
        for word in above.split():
            if _is_vocabulary_name(word) and not _names_this_repository(word):
                return True
    return False


def signal_custody_locator(line: str, start: int, end: int) -> bool:
    """(4) THE CUSTODY-LOCATOR SCHEME, which carries its qualifier INSIDE the
    token rather than beside it.

    Fires where the token is immediately preceded on the citing line by the
    literal scheme prefix followed by one owner segment and `/`, AND the token
    standing after that `/` is the locator's own PATH: the whole of it, read as
    one locator and never stopped at its first segment. The same prefix followed
    by anything else — a command name, a subject, a workflow locator — fires
    nothing, and so does a locator that is malformed at either end.
    """
    if CUSTODY_SCHEME_RE.search(line[:start]) is None:
        return False
    return locator_path(line[start:end])


def signal_trailing_parenthetical(line: str, end: int) -> bool:
    """(5) A TRAILING `(RepoName)` PARENTHETICAL.

    Fires where the characters immediately following the token on the citing
    line are at most ONE space, then `(`, then a vocabulary member under the
    decoration and case rules, then `)`. More than one space, any further
    content inside the parentheses, a parenthetical naming THIS repository, or
    a parenthetical that is not the next thing after the token fires nothing.
    """
    match = TRAILING_PARENTHETICAL_RE.match(line[end:])
    if match is None:
        return False
    inner = match.group("inner").strip()
    if not inner or _names_this_repository(inner):
        return False
    return _is_vocabulary_name(inner)


def signals_at(lines, lineno: int, start: int, end: int) -> tuple:
    """Every one of the five signals that fires at ONE occurrence, in the order
    the requirement names them."""
    line = lines[lineno - 1]
    fired = []
    if signal_path_joined_prefix(line, start):
        fired.append(SIGNAL_PATH_JOINED)
    if signal_forge_url(line, start):
        fired.append(SIGNAL_FORGE_URL)
    if signal_bare_qualifier_word(lines, lineno, start):
        fired.append(SIGNAL_QUALIFIER_WORD)
    if signal_custody_locator(line, start, end):
        fired.append(SIGNAL_CUSTODY_SCHEME)
    if signal_trailing_parenthetical(line, end):
        fired.append(SIGNAL_TRAILING_PAREN)
    return tuple(fired)


def probe_longer_path(root: Path, line: str, start: int, raw: str):
    """(i) A LONGER PATH ON THE SAME LINE ENDS WITH THE TOKEN AND STANDS IN
    THIS TREE — the citation is that longer path and the token is only its
    tail, because the extraction pattern is anchored on the changes root and
    cannot reach a head written before it.

    This is the probe the trailing-character rules cannot reach at all: such a
    token is severed at its FRONT and carries no punctuation to notice.

    Returns the longer path where the probe fires, else `None`.
    """
    prefix = trailing_path_run(line[:start])
    if not prefix:
        return None
    longer = prefix + raw
    target = packet_reference._contained(root, root / longer)  # noqa: SLF001
    if target is not None and target.exists():
        return longer
    return None


def probe_placeholder_follows(line: str, end: int) -> bool:
    """(ii) THE CHARACTER IMMEDIATELY FOLLOWING THE TOKEN IS `<` — the path
    continues into a placeholder whose opening character the grammar admits
    nowhere, so the extraction stopped short of the path's end rather than at
    it."""
    return line[end:end + 1] == "<"


#: The two characters probe (iii) reads a literal by. A BACKTICK IS NOT ONE OF
#: THEM and neither is any other delimiter: the rule is closed, and a probe two
#: realizations match differently is a class total two readings cannot be
#: compared by.
PROBE_QUOTES = ('"', "'")


def _opening_quote_index(text: str, quote: str):
    """Where the literal `quote` left OPEN by `text` was opened, or `None`.

    An odd count of `quote` in `text` is a literal still open at its end, and
    the LAST such character is the one that opened it. A TRIPLE QUOTE, a
    REPEATED quote and a PREFIXED or RAW literal are refused here rather than
    admitted and corrected later: the rule names no language and asks nothing
    of one, which is how it reaches the shape the measurement caught without
    admitting the shapes it did not.
    """
    if text.count(quote) % 2 == 0:
        return None
    index = text.rfind(quote)
    if text[index:index + 3] == quote * 3:
        return None
    if index > 0 and text[index - 1] == quote:
        return None
    if index > 0 and text[index - 1].isalpha():
        return None
    return index


def probe_split_string_literal(lines, lineno: int, end: int, token: str,
                               resolves):
    """(iii) THE TOKEN IS CLOSED BY A QUOTE AT THE END OF ITS SOURCE LINE, THE
    NEXT LINE OPENS WITH THE SAME QUOTE, AND THE PATH REJOINED ACROSS THE TWO
    RESOLVES — an implicit string concatenation split one path across two
    source lines, and the rejoin is what proves it rather than a reader's
    guess.

    THE RULE IS LEXICAL AND IT IS CLOSED. *"Inside a string literal"* is no
    predicate over a corpus written in several languages, each with its own
    delimiters and escape syntaxes. The probe fires where, and only where, the
    occurrence is followed on its own line by ONE quote character — `"` or `'`,
    not repeated and no other delimiter — which is the last non-whitespace
    character of that line and closes a literal the same character opened
    earlier on that same line; the first non-whitespace character of the next
    line is that same quote character, again not repeated, opening the
    continuation; and the token followed by the continuation literal's content,
    up to the next occurrence of that same character, RESOLVES. A triple quote,
    a backtick, a prefixed or raw literal, a BACKSLASH anywhere in either
    literal, and a continuation opened by the OTHER quote character are not
    probe (iii), even where the path rejoined across the two lines would
    resolve.

    The shape this rule is measured against is `scripts/doc_health/
    pin_class.py:1248-1249`, where a `path=` argument ends its line at the
    literal's closing double quote and the next line opens the continuation
    with one of its own, the rejoined path standing in this tree.

    Returns the rejoined path where the probe fires, else `None`.
    """
    line = lines[lineno - 1]
    if lineno >= len(lines):
        return None
    closing = line[end:].rstrip()
    if closing not in PROBE_QUOTES:
        return None
    quote = closing
    opened_at = _opening_quote_index(line[:end], quote)
    if opened_at is None:
        return None
    if "\\" in line[opened_at:end]:
        return None
    following = lines[lineno].lstrip()
    if following[:1] != quote or following[1:2] == quote:
        return None
    content, separator, _ = following[1:].partition(quote)
    if not separator or not content or "\\" in content:
        return None
    rejoined = token + content
    return rejoined if resolves(rejoined) else None


def under_fixture_location(path: str) -> bool:
    """Whether ONE occurrence's citing file stands in a location this corpus
    keeps fixtures and worked examples in — the CLOSED four.

    The fourth location is a `tests/` directory NESTED BENEATH the population's
    own top-level `tests/` exclusion: any directory literally named `tests`
    found anywhere else in the tree, never the repository's own top-level
    `tests/`, which the population excludes entirely and which therefore
    contributes no occurrence in the first place.
    """
    if segment_match(path, FIXTURE_TOP_LEVEL):
        return True
    if segment_match(path, FIXTURE_GATE_RECORDS):
        return True
    segments = path.split("/")
    if segments and segments[0] == FIXTURE_CONTRACTS_ROOT:
        if FIXTURE_TOP_LEVEL in segments[1:-1]:
            return True
    if FIXTURE_NESTED_TESTS in segments[1:-1]:
        return True
    return False


def classify(record) -> str:
    """The one class a remainder entry takes, decided in the order the
    requirement fixes.

    A class about the report's own NORMALIZATION beats one about a LOCATION; and
    where two normalization classes both fit, `truncated` beats
    `punctuation-stripped`, because a token stripped, tried and still resolving
    to nothing is SEVERED, which is the later verdict and the stronger
    statement. Nothing is lost by the precedence: every normalization the report
    applied is reported in the entry's own normalization record whatever class
    the entry lands in.
    """
    if truncated_predicate(record):
        return CLASS_TRUNCATED
    if punctuation_stripped_predicate(record):
        return CLASS_PUNCTUATION_STRIPPED
    if fixture_path_predicate(record):
        return CLASS_FIXTURE_PATH
    return CLASS_UNCLASSIFIED


def truncated_predicate(record) -> bool:
    """`truncated` CARRIES A PREDICATE RATHER THAN A DESCRIPTION, CLOSED: EVERY
    ONE of an entry's occurrences satisfies at least one of the three probes, OR
    the token ends in `-` and does not resolve under the order this
    specification already fixes.

    THE OCCURRENCE RULE IS **ALL**, NEVER **ANY**, for the reason
    `fixture-path`'s is: an occurrence at which the token stands as the whole
    citation is a citation this corpus really carries, and an entry carrying one
    is not an artifact of the tool.
    """
    if record.occurrences and all(o.truncation_probes for o in record.occurrences):
        return True
    return record.token.endswith("-")


def punctuation_stripped_predicate(record) -> bool:
    """`punctuation-stripped` CARRIES ITS FIRING CONDITION: the report stripped
    a trailing character from the token UNDER THE GRAMMAR'S NORMALIZATION, the
    stripped token still resolved to nothing, and the `truncated` predicate did
    not fire.

    A TOKEN THAT RESOLVES IS NOT A REMAINDER ENTRY AND TAKES NO CLASS AT ALL,
    which is why this predicate is only ever asked of a remainder entry. The
    grammar-admitted character is the FULL STOP: a trailing path separator is
    the one character the grammar admits in NO identifier, its strip is
    unconditional for that reason, and an entry is not labelled for a strip that
    could suppress no valid citation.
    """
    return any(FULL_STOP_STRIPPED in o.normalizations for o in record.occurrences)


def fixture_path_predicate(record) -> bool:
    """`fixture-path` WHERE EVERY ONE of an entry's occurrences stands under one
    of the four named locations — ALL, never ANY: one occurrence outside every
    named location is a citation carried by ordinary prose, and an entry
    carrying one takes whatever other mechanical class its evidence supports, or
    `unclassified`.
    """
    return bool(record.occurrences) and all(
        under_fixture_location(o.path) for o in record.occurrences)


def fixture_path_evidence(record) -> tuple:
    """The occurrence locations a `fixture-path` verdict rests on, so a reader
    can check it."""
    return tuple(sorted({o.path for o in record.occurrences}))


# ===========================================================================
# § THE READING — one record per TOKEN, and the counts the requirement fixes.
# ===========================================================================


@dataclass
class TokenRecord:
    """One remainder ENTRY, which is a TOKEN.

    A REMAINDER ENTRY IS A TOKEN — never an identity, and never the TRACKED
    ENTRY the population is counted in. An entry's class and its flags are
    properties of THAT TOKEN; two tokens addressing one identity are never
    merged, and grouping by identity NESTS them beneath the identity they
    address, changing the ORDER a reading lists things in and never what is
    listed.
    """

    token: str
    occurrences: list
    status: str = ""
    half: str | None = None
    identity: str | None = None
    remainder: str = ""
    report: str = ""
    relocated: bool = False
    raw_path_present: bool = False
    classification: str | None = None
    class_evidence: tuple = ()
    flags: tuple = ()

    @property
    def is_remainder(self) -> bool:
        """Whether this token stands in the remainder.

        The remainder is what the RESOLUTION RULE could not resolve — DANGLING
        or AMBIGUOUS — over the tokens whose raw path is absent from the tree.
        `NOT_A_PACKET_REFERENCE` SITS OUTSIDE IT and is counted beside it: it is
        the rule handing a path back to its caller, never a citation the rule
        failed on.
        """
        return (not self.raw_path_present
                and self.status in (DANGLING, AMBIGUOUS))

    @property
    def flagged(self) -> bool:
        return FLAG_CROSS_REPO in self.flags

    @property
    def normalizations(self) -> tuple:
        seen = []
        for occurrence in self.occurrences:
            for name in occurrence.normalizations:
                if name not in seen:
                    seen.append(name)
        return tuple(seen)


@dataclass
class Reading:
    """One reading of one tree, taken at one head, under one recipe."""

    root: Path
    head: str
    tree_unmodified: bool
    population: Population
    records: list
    history: dict = field(default_factory=dict)
    history_probed: bool = False

    @property
    def remainder(self) -> list:
        return [r for r in self.records if r.is_remainder]


def extract_occurrences(texts, root: Path, resolves):
    """Every occurrence of the extraction pattern in the population's text,
    normalized and grouped onto ONE record per distinct TOKEN.

    NORMALIZATION HAPPENS BEFORE DEDUPLICATION, so one citation spelled both
    with and without a trailing separator is ONE token and not two — and it is
    the OCCURRENCE that keeps the raw spelling, so nothing is lost to the merge.
    """
    grouped: dict[str, list] = {}
    for path, text in texts:
        if CHANGES_ROOT + "/" not in text:
            continue
        lines = text.splitlines()
        for lineno, line in enumerate(lines, start=1):
            for match in TOKEN_RE.finditer(line):
                raw = match.group(0)
                token, normalizations = normalise_token(raw, resolves)
                probes, evidence = truncation_probes_at(
                    root, lines, lineno, match.start(), match.end(), raw,
                    token, resolves)
                occurrence = Occurrence(
                    path=path, line=lineno, raw=raw,
                    normalizations=normalizations,
                    signals=signals_at(lines, lineno, match.start(),
                                       match.end()),
                    truncation_probes=probes,
                    truncation_evidence=evidence)
                grouped.setdefault(token, []).append(occurrence)
    return grouped


def truncation_probes_at(root: Path, lines, lineno: int, start: int, end: int,
                         raw: str, token: str, resolves):
    """Which of the three `truncated` probes fire at ONE occurrence, and the
    evidence a reader checks the verdict by."""
    line = lines[lineno - 1]
    fired = []
    evidence = None
    longer = probe_longer_path(root, line, start, raw)
    if longer is not None:
        fired.append(PROBE_LONGER_PATH)
        evidence = longer
    if probe_placeholder_follows(line, end):
        fired.append(PROBE_PLACEHOLDER)
    rejoined = probe_split_string_literal(lines, lineno, end, token, resolves)
    if rejoined is not None:
        fired.append(PROBE_SPLIT_LITERAL)
        if evidence is None:
            evidence = rejoined
    return tuple(fired), evidence


def class_evidence_for(record) -> tuple:
    """The evidence a class verdict rests on, so a reader can check it — one
    kind per class, and nothing where the class rests on the token alone."""
    if record.classification == CLASS_FIXTURE_PATH:
        return fixture_path_evidence(record)
    if record.classification == CLASS_TRUNCATED:
        return tuple(sorted({o.truncation_evidence for o in record.occurrences
                             if o.truncation_evidence}))
    if record.classification == CLASS_PUNCTUATION_STRIPPED:
        return record.normalizations
    return ()


def record_for(root: Path, token: str, occurrences, resolution) -> TokenRecord:
    """One token's whole record: the resolver's outcome, its occurrences, its
    flags, and — only where it IS a remainder entry — its class.

    A TOKEN THAT RESOLVES IS NO REMAINDER ENTRY AND TAKES NO CLASS AT ALL,
    which is why `classify` is asked here and not of every token.
    """
    raw = packet_reference._contained(root, root / token)  # noqa: SLF001
    record = TokenRecord(
        token=token,
        occurrences=sorted(occurrences, key=lambda o: (o.path, o.line)),
        status=resolution.status,
        half=resolution.half,
        identity=resolution.identity,
        remainder=resolution.remainder,
        report=resolution.report,
        relocated=resolution.relocated,
        raw_path_present=raw is not None and raw.exists(),
    )
    record.flags = ((FLAG_CROSS_REPO,)
                    if any(o.signals for o in record.occurrences) else ())
    if record.is_remainder:
        record.classification = classify(record)
        record.class_evidence = class_evidence_for(record)
    return record


#: `git diff --quiet HEAD`'S OWN TWO ANSWERS, AND NOTHING ELSE IT CAN EXIT WITH
#: IS ONE OF THEM. `0` is "no tracked file differs from the head" and `1` is "at
#: least one does". EVERY OTHER STATUS IS GIT REPORTING THAT IT COULD NOT TAKE
#: THE COMPARISON AT ALL, which is a different fact and belongs to the one
#: non-zero exit this capability has. Measured rather than reasoned: with a head
#: ref naming an object that does not stand in the store, `git diff --quiet
#: HEAD` exits `128` with `fatal: bad object HEAD` — and a reader of every
#: non-zero as "modified" would publish a tree state it never measured, beside a
#: head it could not read. (Copilot `PRRT_kwDOTAvnrs6js_9D`.)
DIFF_TREE_CLEAN = 0
DIFF_TREE_MODIFIED = 1

#: `git rev-parse --verify --quiet HEAD`'s answer where the branch carries no
#: commit yet: `1`, and silently. THE `--verify --quiet` FORM IS ASKED FOR
#: RATHER THAN A BARE `rev-parse HEAD` for the same reason the two statuses
#: above are separated: the bare form exits `128` for an unborn HEAD and `128`
#: again for a tree it cannot read, and those are different facts.
REV_PARSE_NO_SUCH_REF = 1


def head_and_tree_state(root: Path) -> tuple:
    """The head this reading stands on, and whether the tracked content read
    stands UNMODIFIED at it.

    HOW "STANDS UNMODIFIED AT THAT HEAD" IS COMPUTED IS THIS REALIZATION'S OWN
    CHOICE — the requirement fixes the outward behavior and not the mechanism.
    `diff --quiet HEAD` answers exactly "does at least one TRACKED file differ
    from the head, staged or unstaged", which is the question the requirement
    asks; `status --porcelain` would answer a wider one, marking the tree
    modified over UNTRACKED files this report never reads at all.

    A STATUS NEITHER GIT DOCUMENTS AS AN ANSWER IS A RUN THIS REPORT COULD NOT
    TAKE, AND NEVER A TREE STATE IT MEASURED. Each of the two gits below is read
    for the answers it actually has — an unborn head, a clean tree, a modified
    tree — and anything else raises `CouldNotRun` carrying git's own stderr, so
    the caller gets the two-case contract's non-zero exit and the reason, rather
    than a reading whose header states a fact nothing established.
    """
    code, out, error = git_status(root, "rev-parse", "--verify", "--quiet",
                                  "HEAD")
    if code == REV_PARSE_NO_SUCH_REF:
        # A branch carrying no commit yet: there is no head, and no tracked
        # content stands unmodified at one.
        return "(no commit at HEAD)", False
    if code != 0:
        raise CouldNotRun(
            f"`git rev-parse --verify --quiet HEAD` failed in {root} with "
            f"status {code}: {error.strip() or 'no message'}")
    status, _, error = git_status(root, "diff", "--quiet", "HEAD")
    if status == DIFF_TREE_CLEAN:
        return out.strip(), True
    if status == DIFF_TREE_MODIFIED:
        return out.strip(), False
    raise CouldNotRun(
        f"`git diff --quiet HEAD` failed in {root} with status {status}: "
        f"{error.strip() or 'no message'}")


def take_reading(root: Path, *, include=(), exclude=()) -> Reading:
    """The whole reading, from the tracked-entry listing to the classified
    remainder."""
    if not root.exists():
        raise CouldNotRun(f"{root} does not exist")
    # THE ROOT IS THE WORK-TREE TOP AND IS ABSOLUTE FROM HERE DOWN, so every
    # path this reading joins onto it and every containment test the resolver
    # applies to one answers about the same tree, whatever directory inside it
    # the report was named at or run from.
    root = work_tree_root(root).resolve()
    head, tree_unmodified = head_and_tree_state(root)

    entries = tracked_entries(root)
    population, in_scope = build_population(entries, include, exclude)
    texts = read_population_text(root, in_scope, population)

    index = packet_reference.PacketIndex(root)
    resolutions: dict[str, object] = {}

    def resolution_of(token: str):
        if token not in resolutions:
            resolutions[token] = packet_reference.resolve(root, token,
                                                          index=index)
        return resolutions[token]

    def resolves(token: str) -> bool:
        return resolution_of(token).status == RESOLVED

    grouped = extract_occurrences(texts, root, resolves)

    records = [record_for(root, token, grouped[token], resolution_of(token))
               for token in sorted(grouped)]

    return Reading(root=root, head=head, tree_unmodified=tree_unmodified,
                   population=population, records=records)


def probe_history(root: Path, records) -> dict:
    """`git log --all --diff-filter=A --reverse` PER IDENTITY, cached.

    OPT-IN ON A MEASURED COST: in the evidence run the probe was 17.0 of 19.0
    seconds — 90% of the whole run — and returned empty for 33 of the 38
    identities, which the resolver had already answered. It decides exactly ONE
    thing the resolver cannot: an id that STOOD here and was renamed before
    former-id tracking, against one that never stood here at all.

    THE PATHSPEC IS THE CORRECTED ONE. Git matches a wildcard pathspec under
    `WM_PATHNAME`, where `*` does not cross a `/`, so the archive spelling must
    end in `/*` or it matches nothing on any input. `--reverse` so the FIRST
    line is the OLDEST add-event, `--abbrev=8` so both shas are eight
    characters everywhere.

    `records` IS WHAT THE READING WILL LIST AND NEVER EVERY TOKEN IN THE
    CORPUS. The probe is opt-in on a measured cost, and probing the identities
    of the hundreds of tokens a reading COUNTS rather than lists would multiply
    that cost by an order of magnitude to answer a question about entries the
    output does not carry. Under `--all` the listing is every token, and the
    probe follows it there.

    A PROBE THAT FAILS IS NOT A PROBE THAT FOUND NOTHING. An empty log and a
    `git log` this report could not run are two different facts, and reporting
    the second as the first states `ever_tracked: false` — *this id never stood
    here* — on the strength of a history the report never read. So the probe
    goes through `git`, whose contract is this module's own: a git that fails
    is a tree this report cannot read, which is the one non-zero exit this
    capability has, carrying git's own message. (Copilot
    `PRRT_kwDOTAvnrs6jdTNb`.)
    """
    probed: dict[str, dict] = {}
    for record in records:
        identity = record.identity
        if identity is None or identity in probed:
            continue
        out = git(
            root, "log", "--all", "--diff-filter=A", "--reverse",
            "--abbrev=8", "--format=%h", "--",
            f"{CHANGES_ROOT}/{identity}",
            f"{CHANGES_ROOT}/archive/*-{identity}/*")
        lines = [line.strip() for line in out.splitlines() if line.strip()]
        probed[identity] = {
            "probed": True,
            "ever_tracked": bool(lines),
            "first_commit": lines[0] if lines else None,
            "last_commit": lines[-1] if lines else None,
        }
    return probed


# ===========================================================================
# § THE COUNTS — every figure the requirement fixes, computed once and printed
# by both formats, because a figure that differs between two formats of one run
# is two readings nobody asked for.
# ===========================================================================


def counts_of(reading: Reading) -> dict:
    """Every headline figure, the outcome rows, the two arithmetic identities
    and the class totals."""
    records = reading.records
    remainder = reading.remainder
    raw_absent = [r for r in records if not r.raw_path_present]

    repaired = sum(1 for r in raw_absent if r.status == RESOLVED)
    identity_half = sum(1 for r in raw_absent
                        if r.status == DANGLING and r.half == IDENTITY_HALF)
    file_half = sum(1 for r in raw_absent
                    if r.status == DANGLING and r.half == FILE_HALF)
    ambiguous = sum(1 for r in raw_absent if r.status == AMBIGUOUS)
    npr_absent = sum(1 for r in raw_absent
                     if r.status == NOT_A_PACKET_REFERENCE)

    inclusive_identities = sorted({r.identity for r in remainder
                                   if r.identity is not None})
    flagged_entries = [r for r in remainder if r.flagged]
    filtered = [r for r in remainder if not r.flagged]
    filtered_identities = sorted({r.identity for r in filtered
                                  if r.identity is not None})

    classes = {name: sum(1 for r in remainder if r.classification == name)
               for name in CLASS_VOCABULARY}

    return {
        "distinct_tokens": len(records),
        "outcomes": {
            "resolved": sum(1 for r in records if r.status == RESOLVED),
            "resolved_relocated": sum(1 for r in records if r.relocated),
            "dangling_identity_half": sum(
                1 for r in records
                if r.status == DANGLING and r.half == IDENTITY_HALF),
            "dangling_file_half": sum(
                1 for r in records
                if r.status == DANGLING and r.half == FILE_HALF),
            "ambiguous": sum(1 for r in records if r.status == AMBIGUOUS),
            "not_a_packet_reference": sum(
                1 for r in records if r.status == NOT_A_PACKET_REFERENCE),
        },
        "raw_path_absent": {
            "total": len(raw_absent),
            "repaired_by_the_identity_rule": repaired,
            "dangling_identity_half": identity_half,
            "dangling_file_half": file_half,
            "ambiguous": ambiguous,
            "not_a_packet_reference_with_no_raw_path": npr_absent,
            "total_holding_not_a_packet_reference_out": len(raw_absent) - npr_absent,
            "closes": len(raw_absent) == (repaired + identity_half + file_half
                                          + ambiguous + npr_absent),
        },
        "remainder_inclusive_tokens": len(remainder),
        "remainder_inclusive_identities": len(inclusive_identities),
        "remainder_filtered_tokens": len(filtered),
        "remainder_filtered_identities": len(filtered_identities),
        "flagged_remainder_entries": len(flagged_entries),
        "flagged_tokens_corpus_wide": sum(1 for r in records if r.flagged),
        "classes": classes,
    }


def population_block(population: Population) -> dict:
    return {
        "tracked_entries_total": population.tracked_entries_total,
        "tracked_entries_in_scope": population.entries_in_scope,
        "files_read": population.files_read,
        "skipped_not_a_file": len(population.skipped_non_file),
        "skipped_link_leaving_the_root": len(population.skipped_link_leaving_root),
        "skipped_undecodable": len(population.skipped_undecodable),
        "arithmetic_closes": population.arithmetic_closes,
        "exclusions": list(population.exclusions),
        "include": list(population.include),
        "exclude": list(population.exclude),
        "output_paths_excluded": list(population.output_paths_excluded),
        "refinement_named_output_path": list(
            population.refinement_named_output_path),
    }


def reading_block() -> dict:
    """THE READING, DECLARED. A reading that applied a different pattern or a
    different choice is not a later point in the same series, so every reading
    carries its own recipe in its own header."""
    return {
        "extraction_pattern": TOKEN_RE.pattern,
        "choice_1_normalization_before_deduplication": True,
        "choice_2_not_a_packet_reference_outside_the_remainder": True,
        "choice_3_cross_repository_flag_set_by_any_qualified_occurrence": True,
        "window_lines_above_the_citing_line": WINDOW_LINES_ABOVE,
        "signals": list(SIGNALS),
        "class_vocabulary": list(CLASS_VOCABULARY),
    }


# ===========================================================================
# § OUTPUT — two parts in a fixed order, and CLASS IS NEVER A GROUPING LEVEL in
# either grouping mode or either part.
# ===========================================================================

TREE_UNMODIFIED = "the tracked content read stands UNMODIFIED at this head"
TREE_MODIFIED = ("the tracked content read stands MODIFIED at this head — this "
                 "reading is NOT a later point in the series taken at it")


def occurrence_json(occurrence: Occurrence) -> dict:
    return {"at": occurrence.at, "path": occurrence.path,
            "line": occurrence.line, "raw": occurrence.raw,
            "normalizations": list(occurrence.normalizations),
            "signals": list(occurrence.signals)}


def record_json(record: TokenRecord) -> dict:
    """ONE OBJECT PER TOKEN. `raw` is a PER-OCCURRENCE value and never a
    singular field on the token: `token` is the normalized form the resolver was
    actually asked about, carried once."""
    return {
        "token": record.token,
        "status": record.status,
        "half": record.half,
        "identity": record.identity,
        "remainder": record.remainder,
        "occurrences": [occurrence_json(o) for o in record.occurrences],
        "class": record.classification,
        "class_evidence": list(record.class_evidence),
        "flags": list(record.flags),
        "normalizations": list(record.normalizations),
        "raw_path_present": record.raw_path_present,
        "relocated": record.relocated,
        "in_remainder": record.is_remainder,
        "report": record.report,
    }


def listed_records(reading: Reading, show_all: bool) -> list:
    """What a reading ITEMIZES. The remainder always; `RESOLVED` and
    `NOT_A_PACKET_REFERENCE` only under `--all`, which the default output COUNTS
    rather than lists."""
    if show_all:
        return list(reading.records)
    return reading.remainder


def grouped_by_identity(records) -> list:
    """The default grouping: the IDENTITY is the row and ITS TOKENS are listed
    beneath it. Grouping NESTS and never collapses — every token appears in
    every mode."""
    groups: dict[str, list] = {}
    for record in records:
        groups.setdefault(record.identity or "", []).append(record)
    return [(identity or None, groups[identity])
            for identity in sorted(groups)]


def _with_history(entry: dict, reading: Reading, identity) -> dict:
    """The `history` key, ABSENT rather than `null` where `--history` was not
    given, so two readings taken under different flags are not mistaken for two
    readings of different trees."""
    if reading.history_probed and identity in reading.history:
        entry["history"] = reading.history[identity]
    return entry


def json_reading(reading: Reading, show_all: bool, by_token: bool) -> dict:
    counts = counts_of(reading)
    body: dict = {
        "root": str(reading.root),
        "head": reading.head,
        "tree_unmodified_at_head": reading.tree_unmodified,
        "tree_state": (TREE_UNMODIFIED if reading.tree_unmodified
                       else TREE_MODIFIED),
        "reading": reading_block(),
        "population": population_block(reading.population),
        "counts": counts,
        "grouping": "token" if by_token else "identity",
        "listed": "all-tokens" if show_all else "remainder-only",
    }
    records = listed_records(reading, show_all)
    if by_token:
        body["tokens"] = [_with_history(record_json(record), reading,
                                        record.identity)
                          for record in sorted(records, key=lambda r: r.token)]
    else:
        body["identities"] = [
            _with_history({"identity": identity,
                           "tokens": [record_json(r) for r
                                      in sorted(held, key=lambda r: r.token)]},
                          reading, identity)
            for identity, held in grouped_by_identity(records)]
    return body


def print_human(reading: Reading, show_all: bool, by_token: bool,
                out=None) -> None:
    """PART 1 IS THE COUNTS BLOCK, PART 2 IS THE ITEMIZED REMAINDER, in that
    fixed order, and neither part ever headers a group with a class name.

    `out` IS RESOLVED AT CALL TIME AND NOT AT IMPORT TIME: a default argument
    spelled `sys.stdout` binds the stream this module was imported with, which
    is the wrong stream for any caller that redirects one — the suite's own
    readers do.
    """
    counts = counts_of(reading)
    write = (out if out is not None else sys.stdout).write
    _print_header(write, reading)
    _print_population(write, reading.population)
    _print_counts(write, counts)
    _print_itemized(write, reading, show_all, by_token)


def _print_header(write, reading: Reading) -> None:
    """The reading's own declaration: what it stands on, and every fixed choice
    that decides which number it prints."""
    write("CITATION REMAINDER\n")
    write(f"  root                 {reading.root}\n")
    write(f"  head                 {reading.head}\n")
    write(f"  tree state           "
          f"{TREE_UNMODIFIED if reading.tree_unmodified else TREE_MODIFIED}\n")
    write(f"  extraction pattern   {TOKEN_RE.pattern}\n")
    write("  choice (1)           normalization happens BEFORE deduplication\n")
    write("  choice (2)           NOT-A-PACKET-REFERENCE sits OUTSIDE the "
          "remainder\n")
    write("  choice (3)           the cross-repository flag is set where ANY "
          "one occurrence carries a signal\n")
    write(f"  window               the citing line plus the "
          f"{WINDOW_LINES_ABOVE} lines above it\n")
    write(f"  signals              {', '.join(SIGNALS)}\n")


def _print_population(write, population: Population) -> None:
    """The population actually read, its three skip terms, and the refinements
    the run was given."""
    write("\nPOPULATION\n")
    write(f"  tracked entries          {population.tracked_entries_total}\n")
    write(f"  tracked ENTRIES in scope {population.entries_in_scope}\n")
    write(f"  FILES read               {population.files_read}\n")
    write(f"  skipped, not a file      {len(population.skipped_non_file)}\n")
    write(f"  skipped, link leaving the root "
          f"{len(population.skipped_link_leaving_root)}\n")
    write(f"  skipped, undecodable     {len(population.skipped_undecodable)}\n")
    write(f"  arithmetic               {population.entries_in_scope} entries in "
          f"scope = {population.files_read} files read + "
          f"{len(population.skipped_non_file)} not a file + "
          f"{len(population.skipped_link_leaving_root)} link leaving the root + "
          f"{len(population.skipped_undecodable)} undecodable"
          f"{'' if population.arithmetic_closes else '  [DOES NOT CLOSE]'}\n")
    for prefix in population.exclusions:
        write(f"  excluded                 {prefix}/ — "
              f"{EXCLUSION_REASONS.get(prefix, 'stated exclusion')}\n")
    write(f"  output paths excluded    "
          f"{', '.join(population.output_paths_excluded)}\n")
    if population.include:
        write(f"  --include                {' '.join(population.include)} "
              f"(re-admitted BESIDE the stated population, never in place of "
              f"it)\n")
    if population.exclude:
        write(f"  --exclude                {' '.join(population.exclude)} "
              f"(applied last, and wins)\n")
    if population.refinement_named_output_path:
        write(f"  refinement named the report's own output "
              f"{', '.join(population.refinement_named_output_path)} — KEPT "
              f"EXCLUDED; no refinement may re-admit it\n")


def _print_counts(write, counts: dict) -> None:
    """PART 1, the COUNTS BLOCK: the population figures and the arithmetic
    rows, then the class totals counted in TOKENS beside the labelled identity
    count. CLASS IS NEVER A GROUPING LEVEL — it is a total here and a per-entry
    label below, never a heading."""
    write("\nTOKENS AND OUTCOMES\n")
    write(f"  distinct tokens          {counts['distinct_tokens']}\n")
    outcomes = counts["outcomes"]
    write(f"  RESOLVED                 {outcomes['resolved']} "
          f"({outcomes['resolved_relocated']} resolved somewhere other than "
          f"the path they were spelled as)\n")
    write(f"  DANGLING, identity half  "
          f"{outcomes['dangling_identity_half']}\n")
    write(f"  DANGLING, file half      {outcomes['dangling_file_half']}\n")
    write(f"  AMBIGUOUS                {outcomes['ambiguous']}\n")
    write(f"  NOT A PACKET REFERENCE   "
          f"{outcomes['not_a_packet_reference']}\n")

    absent = counts["raw_path_absent"]
    write("\nRAW-PATH-ABSENT ARITHMETIC (tokens)\n")
    write(f"  {absent['total']} raw-path-absent = "
          f"{absent['repaired_by_the_identity_rule']} repaired by the identity "
          f"rule + {absent['dangling_identity_half']} identity half + "
          f"{absent['dangling_file_half']} file half + {absent['ambiguous']} "
          f"ambiguous + "
          f"{absent['not_a_packet_reference_with_no_raw_path']} not a packet "
          f"reference{'' if absent['closes'] else '  [DOES NOT CLOSE]'}\n")
    # AND THE SAME SET UNDER CHOICE (2), WHICH IS THE ONE EARLIER READINGS OF
    # THIS POPULATION PUBLISH. The five-term identity above closes over every
    # token with no raw path; the figure a reader compares against an earlier
    # point in this series holds the resolver's fifth answer out of it, and a
    # report printing only one of the two invites the wrong comparison.
    write(f"  {absent['total_holding_not_a_packet_reference_out']} of those "
          f"raw-path-absent tokens under choice (2), which holds NOT-A-PACKET-"
          f"REFERENCE out of the remainder population\n")

    write("\nREMAINDER\n")
    write(f"  INCLUSIVE remainder      "
          f"{counts['remainder_inclusive_tokens']} TOKENS\n")
    write(f"  remainder IDENTITIES     "
          f"{counts['remainder_inclusive_identities']} IDENTITIES "
          f"(the identity count, labelled)\n")
    write(f"  FILTERED remainder       "
          f"{counts['remainder_filtered_tokens']} TOKENS "
          f"(every entry carrying the cross-repository flag removed)\n")
    write(f"  filtered IDENTITIES      "
          f"{counts['remainder_filtered_identities']} IDENTITIES "
          f"(the identity count, labelled; the identity figures are two "
          f"labelled readings of one population and never an arithmetic row)\n")
    write(f"  arithmetic               "
          f"{counts['remainder_inclusive_tokens']} inclusive = "
          f"{counts['remainder_filtered_tokens']} filtered + "
          f"{counts['flagged_remainder_entries']} REMAINDER ENTRIES carrying "
          f"the flag\n")
    write(f"  (tokens carrying the flag corpus-wide: "
          f"{counts['flagged_tokens_corpus_wide']} — a larger and a different "
          f"quantity, and never the arithmetic row's term)\n")

    write("\nCLASSES (counted in TOKENS)\n")
    for name in CLASS_VOCABULARY:
        write(f"  {name:<24} {counts['classes'][name]}\n")


def _print_itemized(write, reading: Reading, show_all: bool,
                    by_token: bool) -> None:
    """PART 2, the ITEMIZED remainder: grouped by IDENTITY by default and by
    TOKEN under `--tokens`, every token appearing in either mode because
    grouping changes the ORDER a reading lists things in and never what is
    listed."""
    write("\n")
    records = listed_records(reading, show_all)
    if not records:
        write("NOTHING TO ITEMIZE\n")
        return
    if by_token:
        write("REMAINDER, ITEMIZED BY TOKEN\n")
        for record in sorted(records, key=lambda r: r.token):
            _print_record(write, record, reading, indent="  ",
                          with_history=True)
    else:
        write("REMAINDER, ITEMIZED BY IDENTITY\n")
        for identity, held in grouped_by_identity(records):
            write(f"\n  {identity or '(no identity)'} "
                  f"({len(held)} token{'' if len(held) == 1 else 's'})\n")
            if reading.history_probed and identity in reading.history:
                write(f"    {_history_line(reading.history[identity])}\n")
            for record in sorted(held, key=lambda r: r.token):
                _print_record(write, record, reading, indent="    ",
                              with_history=False)


def _history_line(history: dict) -> str:
    if not history.get("ever_tracked"):
        return "history: never tracked"
    return (f"history: tracked {history['first_commit']}.."
            f"{history['last_commit']}")


def _print_record(write, record: TokenRecord, reading: Reading, indent: str,
                  with_history: bool) -> None:
    labels = []
    if record.classification:
        labels.append(f"class={record.classification}")
    labels.append(f"status={record.status}"
                  + (f"({record.half})" if record.half else ""))
    if record.flags:
        labels.append(f"flags={','.join(record.flags)}")
    write(f"{indent}{record.token}  [{'  '.join(labels)}]\n")
    if with_history and reading.history_probed \
            and record.identity in reading.history:
        write(f"{indent}  {_history_line(reading.history[record.identity])}\n")
    if record.normalizations:
        # EVERY NORMALIZATION THE REPORT APPLIES IS PRINTED IN ITS OWN ROW, and
        # it is printed whatever class the entry lands in — a reader who cannot
        # see that the tool changed the token cannot check the tool.
        write(f"{indent}  normalizations: "
              f"{', '.join(record.normalizations)}\n")
    if record.report:
        write(f"{indent}  {record.report}\n")
    if record.class_evidence:
        write(f"{indent}  evidence: {', '.join(record.class_evidence)}\n")
    for occurrence in record.occurrences:
        shown = ("" if occurrence.raw == record.token
                 else f"  (raw: {occurrence.raw})")
        write(f"{indent}  cited at {occurrence.at}{shown}\n")


# ===========================================================================
# § THE COMMAND — the argument surface, fixed, and the two-case exit contract.
# ===========================================================================


def parser() -> argparse.ArgumentParser:
    """The argument surface, and there is deliberately no `--fail-on` on it.

    THE REPORT EXITS SUCCESSFULLY WHATEVER IT FINDS and offers no option that
    converts a finding into a failure; the only non-zero exit means the report
    COULD NOT RUN. A tool able to exit non-zero on a finding acquires the
    meaning of a gate the first time anybody wires it into a required check, and
    nothing in the reported population has been ruled a defect.
    """
    ap = argparse.ArgumentParser(
        prog="report-citation-remainder.py",
        description=("Report every packet citation this repository's "
                     "resolution rule cannot resolve. Advisory: it gates "
                     "nothing, edits nothing and exits 0 whatever it finds."))
    ap.add_argument("root", nargs="?", default=".", metavar="REPO_ROOT",
                    help="repository root to scan (default: the current "
                         "directory)")
    ap.add_argument("--json", action="store_true",
                    help="machine-readable output instead of the human table; "
                         "written to STDOUT, which a caller redirects")
    ap.add_argument("--all", action="store_true",
                    help="also list RESOLVED and NOT-A-PACKET-REFERENCE "
                         "tokens, which the default output only COUNTS")
    ap.add_argument("--tokens", action="store_true",
                    help="group by TOKEN; the default groups by IDENTITY")
    ap.add_argument("--history", action="store_true",
                    help="opt-in: probe each identity's add-history. OFF by "
                         "default, on a measured cost")
    ap.add_argument("--include", nargs="+", default=[], metavar="PREFIX",
                    help="re-admit tracked entries under these prefixes BESIDE "
                         "the stated population")
    ap.add_argument("--exclude", nargs="+", default=[], metavar="PREFIX",
                    help="remove tracked entries under these prefixes; applied "
                         "last, and wins")
    return ap


def main(argv=None) -> int:
    args = parser().parse_args(argv)
    try:
        reading = take_reading(Path(args.root), include=tuple(args.include),
                               exclude=tuple(args.exclude))
        if args.history:
            reading.history_probed = True
            reading.history = probe_history(
                reading.root, listed_records(reading, args.all))
    except CouldNotRun as error:
        print(f"THE REPORT DID NOT RUN: {error}", file=sys.stderr)
        print("This is not a finding. No reading was taken.", file=sys.stderr)
        return 2
    if args.json:
        json.dump(json_reading(reading, args.all, args.tokens), sys.stdout,
                  indent=2, sort_keys=False)
        sys.stdout.write("\n")
    else:
        print_human(reading, args.all, args.tokens)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
