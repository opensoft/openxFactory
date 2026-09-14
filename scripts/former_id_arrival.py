#!/usr/bin/env python3
"""The LANDING validator for `former_ids:` — the reader half.

`release-realization` § *An undeclared rename arrival is refused at its
landing* (`add-declared-former-id`, ratified 2026-09-13), realized as
`tasks.md` § 2.4 and § 4 direct: a module under `scripts/`, a validator CLI
beside it (`validate-former-id-arrival.py`) and a test suite exercising both
over fixtures and over the live corpus — the shape
`gate-realization-axis-vocabulary` established and this repository already
runs for `target_release:`.

WHY THE REFUSAL IS HERE AND NOT AT THE ARCHIVE GATE (`design.md` D3, RULED
(a)). The archive gate runs at ARCHIVE. A rename that sheds a ratification
does its damage at the RENAME, and the packet may not archive for weeks. The
ruling put the refusal *"at that hop's landing (each hop is one commit when it
lands, so no chain-walking is ever needed)"*, which is also the only place the
question is cheap and the only place the author who made the move is still the
author being asked.

WITHOUT THIS READER THE DECLARATION IS AN HONOUR SYSTEM. The archive-gate half
(`proposal-support.py`, `add-declared-former-id` slices 1 and 2) resolves a
baseline across the identities a packet DECLARES — which protects the author
who writes a declaration. The failure the capability exists to catch is a
rename that sheds a ratification, which is by construction a rename whose
author would not declare it. So the UNDECLARED case is the refused case, and
this module is what refuses it.

────────────────────────────────────────────────────────────────────────────
WHAT IT READS, AND WHAT IT DOES NOT

ONE COMMIT AT A TIME, NEVER A CHAIN. For every commit in the pull request's
own range the gate asks a single question: did a change packet directory
arrive HERE by a move from another change packet directory? A move lands as
one commit, so the answer never needs a second commit, a lineage walk or a
similarity score carried across hops. The chain scenario
(*A rename chain is attempted one hop at a time*) is answered by refusing the
FIRST hop at its own landing, so the later hops are never created.

THE SOURCE IDENTITY IS THE SOURCE PACKET'S WHOLE DECLARED LINEAGE — its own id
together with every id it declares in `former_ids:` AT THE COMMIT'S PARENT —
and the "ever ratified" qualification is taken over all of them. That is still
ONE BLOB AT ONE COMMIT and not a history walk: the source packet's own
declaration is read once, and every id it names is then asked directly,
exactly as `ratifying_baseline` asks them. Reading the source id alone would
lose a packet that has already moved once lawfully (X ratified, X→Y declared
and the header returned to draft, then Y→Z undeclared): Y's own id never
declared `Status: ratified`, so a test over Y alone would pass the second
landing and Z would stand with no lineage at all.

THE QUALIFICATION IS **EVER**, over the source identity's whole history up to
that commit, and NEVER its blob at the parent. A packet renamed and un-ratified
in ONE commit is back in DRAFT for every later hop, so a test taken at the
parent would exempt exactly the shape this refusal exists to catch.

THE ARRIVING LIST IS THE SOURCE'S LIST WITH THE SOURCE ID APPENDED — every
entry the source carried, in the order it carried them, then the id the move
came from. A move that drops an entry the source declared sheds a lineage,
which is the same defect as never declaring one, and is refused by the same
status.

THE ARCHIVE RELOCATION IS EXCEPTED BY ID, AND IT IS THE ONLY EXCEPTION. A
destination `openspec/changes/archive/<YYYY-MM-DD>-<id>/` whose id equals the
source's id is the archive wrapper's own relocation: it PRESERVES the identity
rather than changing it, it is recognizable from the ids alone, and a packet
that declared it would be declaring that it used to be itself.

NO BYPASS FLAG (#690, and D3 in as many words). *"A flag would be the
declaration nobody writes."* `--base` / `--head` NAME the range and are not a
bypass: they cannot silence a refusal the gate would otherwise take, the
corpus arm below runs whatever they say, and the workflow passes neither —
CI derives the range from the checkout GitHub built.

MERGE COMMITS PERFORM NO MOVE OF THEIR OWN and are skipped, which is a
correctness rule and not an optimization. A merge's diff against its first
parent is every change the merged branch carried, so judging one would ask
this gate to re-adjudicate commits that either sit in this same range (and are
asked directly, on their own author's behalf) or are already on the base
branch (and were asked at their own landing). Judging them here would also
red a pull request for history it did not write, which is the one thing a
required gate must never do.

────────────────────────────────────────────────────────────────────────────
THE TWO ARMS, AND WHY THERE ARE TWO (`design.md` D3)

PRIMARY — GIT'S OWN RENAME PAIRING at that commit
(`git diff-tree -r -M -l0 <commit>^ <commit>`), which is the only read that
names a SOURCE for a DESTINATION. `-M` is passed EXPLICITLY so a repository
`diff.renames=false` cannot switch the gate off from a config file (measured:
an explicit `-M` overrides it), and `-l0` lifts the rename LIMIT so detection
cannot silently give up on a large commit and hand back a vacuous pass. The
pairing is aggregated over EVERY file of the packet rather than off
`proposal.md` alone: measured on a fixture whose `proposal.md` was rewritten
as it moved, git paired `.openspec.yaml` at R100 and reported `proposal.md` as
a plain D + A, so a gate keyed on the proposal alone would have seen no move.

FAIL-CLOSED — THE TREE (`git ls-tree`), which answers whether a packet
directory exists at a commit and at its parent, needs no blob, and is
available on exactly the checkouts where the pairing is not (`design.md` M1,
M2). Where the pairing read cannot be performed AND the tree at that commit
shows both a packet directory arriving and one leaving, the gate refuses
CANNOT RUN naming the read. IT DOES NOT PAIR THEM FROM THE TREE: a commit that
withdraws one packet and creates an unrelated other has exactly the same tree
shape, so the honest answer is a refusal to answer and not a guess.

AND THE RATIFICATION LOOKUP IS A SECOND READ, NOT A COROLLARY OF THE FIRST.
Deciding whether the source lineage has EVER declared `Status: ratified` reads
history at every identity in that lineage, and a checkout that cannot produce
those blobs returns the same silence as a lineage that was never ratified —
which would pass an undeclared landing on the one checkout where nothing can
be proved. So ABSENT and UNREADABLE are separated on the same terms the
archive gate's baseline read uses, and an unreadable history REFUSES naming
the identity and the read rather than resolving to "never ratified".

Measured on git 2.43.0 against a `--filter=blob:none --no-checkout` clone
whose promisor remote is unreachable — the same probe `_tree_rows` documents:
`git ls-tree` prints the row and exits 0 for a path whose blob is unavailable,
`git show <rev>:<path>` exits 128, and `git diff-tree -M` exits 128 the moment
inexact rename detection needs a blob. That asymmetry is what makes both
fail-closed arms testable with real git rather than with a stubbed seam, and
`tests/former_id_arrival/test_former_id_arrival.py` builds exactly that clone.

────────────────────────────────────────────────────────────────────────────
WHAT THIS READER DOES NOT JUDGE, NAMED RATHER THAN IMPLIED

A MOVE GIT DOES NOT PAIR IS NOT JUDGED. `-M -l0` lifts the rename LIMIT but not
the similarity THRESHOLD: a relocation whose every file is also rewritten below
it lands as plain D and A rows, and this gate reads no move. The fail-closed arm
does not reach it and is not meant to — that arm exists for a pairing read the
checkout CANNOT PERFORM, and here the read was performed and answered. Pairing
from the TREE instead is the answer `design.md` D3 declined by name: a commit
that withdraws one packet and creates an unrelated other has exactly that tree
shape, and a required gate refusing it refuses a lawful landing. Closing this is
a threshold ruling and a new refusal class on a gate with no bypass flag, so it
belongs to a change that says so — the shape `tasks.md` § 6.4 uses for the
shallow-checkout class. (Raised by Copilot on PR #1039; refused there with this
reason.)

AN EVIL MERGE IS NOT JUDGED. Merges are skipped for the reason above, which
holds for every merge carrying only what its parents carried. A conflict
resolution that introduces a move — or rewrites a declaration — relative to BOTH
parents is carried by no other commit in the range, so no commit this gate reads
contains it. Judging it needs a COMBINED diff (`git diff-tree -c`), whose rename
reporting is not the `-M` pairing every refusal here rests on; that is a
different read and a different ruling from D3's *one commit, never a chain*.
Named here, not taken here. (Also Copilot, PR #1039.)

────────────────────────────────────────────────────────────────────────────
THE READERS THIS MODULE CONSUMES, AND WHY THAT IS THE POINT

`add-declared-former-id`'s slices 1 and 2 landed four readers in
`scripts/proposal-support.py` that had NO CALLER outside their own tests —
`former_id_problems`, `append_only_problems`, `standing_former_id_problems`
and `former_identity_ownership_problems`. A slice that adds a reader and names
nobody to call it is the defect this packet's own design review named
(`design.md` D11(2), *"§ 5.1 built a resolver and named nobody to call it"*).
THIS MODULE IS THEIR CONSUMER:

* `former_id_problems` — through `declared_former_ids`, on every packet this
  gate reads at a commit, and directly over every packet in the working tree
  (`corpus_problems`).
* `append_only_problems` — per commit, over the list the packet carried at the
  parent versus the list it carries here (§ 2.5).
* `standing_former_id_problems` — over the working tree (§ 2.3).
* `former_identity_ownership_problems` — the whole-corpus ownership sweep
  (§ 2.6), called from the corpus arm. That placement is the realization
  plan's Q3 recommendation (a), taken on its own terms: the landing validator
  already walks the corpus and already refuses, and two callers for one sweep
  is two places to keep in step.

`scripts/proposal-support.py` IS NOT EDITED BY THIS MODULE. It is imported.

THE ONE READER SPELLED AGAIN HERE, AND WHY. `_identity_paths_at` below is
`proposal_support.identity_paths_at`'s FAIL-CLOSED spelling: the shared one
used to treat a `_tree_rows` read failure as "no row" (its own docstring said
so, and named `tasks.md` § 3.4 as the slice that changes it), which would have
collapsed an UNREADABLE presence read into an ABSENT one and let this gate
resolve an unreadable identity to "never ratified". Everything else is
reused — `_tree_rows` itself, `_ARCHIVE_ROOT`, `_ARCHIVE_DIR_RE`, the
two-candidate rule and the ambiguity refusal.

§ 3.4 HAS LANDED (main at `701c8fde`) AND THE SWAP IS STILL NOT TAKEN, because
landing it changed what the shared reader answers without changing what it
RAISES to say so: `proposal_support.identity_paths_at` now fails closed
through `_rows_or_refuse`, but that raises `OriginRetentionError` — a
`SupportError`/`ValueError`, built for the archive gate's own four origin-
retention conditions — and never this gate's `ArrivalCannotRun`, a
`RuntimeError` this module owns so `validate-former-id-arrival.py` can catch
exactly one exception for exit 2. Calling the shared reader here directly
would let an unreadable read escape that `except fia.ArrivalCannotRun` as an
uncaught `OriginRetentionError` — a traceback where the documented exits are
1 and 2, the same defect class this slice's own review round refused for
`load_packet` (`d053b38e`) rather than a refusal. DELETE `_identity_paths_at`
AND CALL THE SHARED READER only once a caller here can turn
`OriginRetentionError` into `ArrivalCannotRun` at the boundary — an adapter,
not a one-line call-site swap — which is left to whichever slice takes it,
named rather than taken silently here.

────────────────────────────────────────────────────────────────────────────
STATUSES AND EXITS (`design.md` D3, ratified)

`former-id-undeclared`           exit 1  names the commit, the source path,
                                         the destination path, and the one
                                         repair.
`former-id-arrival-unreadable`   exit 2  CANNOT RUN, naming the read that
                                         could not be performed.

The declaration refusals this gate also carries — the `former_ids:` shape
(§ 2.1), a declared id that still stands (§ 2.3), an entry added by a commit
that moves nothing (§ 2.4), a list rewritten across commits (§ 2.5) and a
former identity claimed twice (§ 2.6) — belong to the sibling requirement
*A moved packet declares the identity it was ratified under*, which names no
status token of its own. They are reported under that requirement's own name
and exit 1 beside the arrival findings; NO THIRD STATUS TOKEN IS INVENTED
HERE, because a token no ratified text names is a token a ruleset cannot pin
and a reader cannot be held to.
"""
from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

_SUPPORT_PATH = _SCRIPTS / "proposal-support.py"


def _load_support():
    """`scripts/proposal-support.py`, loaded by path because it is hyphenated.

    The same `importlib.util.spec_from_file_location` route
    `tests/target_release/test_target_release_gate.py` uses for
    `scripts/target_release.py`, with one addition: an already-registered
    module of the same name and the same file is REUSED rather than
    re-executed. The house test suite loads this module under exactly that
    name, and two live copies would give two distinct `FormerIdError` classes
    — so an `except support.FormerIdError` here would not catch the one a
    caller's copy raised.
    """
    existing = sys.modules.get("proposal_support")
    if existing is not None and getattr(existing, "__file__", None) == str(
            _SUPPORT_PATH):
        return existing
    spec = importlib.util.spec_from_file_location(
        "proposal_support", _SUPPORT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


support = _load_support()

CHANGES_ROOT = "openspec/changes"
ARCHIVE_ROOT = support._ARCHIVE_ROOT           # "openspec/changes/archive/"
ARCHIVE_DIR_RE = support._ARCHIVE_DIR_RE

UNDECLARED = "former-id-undeclared"
UNREADABLE = "former-id-arrival-unreadable"

#: The sibling requirement whose refusals this gate also carries. It names no
#: status token, and this reader does not invent one for it.
DECLARATION_REQUIREMENT = (
    "A moved packet declares the identity it was ratified under")


class ArrivalCannotRun(RuntimeError):
    """`former-id-arrival-unreadable` — exit 2, and never a finding.

    ONE EXCEPTION FOR EVERY UNREADABLE READ, deliberately, for the reason
    `OriginRetentionError`'s docstring gives for the same choice: what the
    arms share is the only thing a caller can act on — THE GATE CANNOT BE
    SHOWN TO HAVE READ WHAT IT JUDGES — and the message names which read it
    was every time.
    """


@dataclass(frozen=True)
class Finding:
    """One refusal, with the status token it is reported under.

    `status` is `None` for the declaration refusals, which belong to a
    requirement that names no token; see the module docstring.
    """

    message: str
    status: str | None = None
    commit: str | None = None


@dataclass
class Report:
    """What one run read and what it refuses. The CLI only prints this."""

    base: str | None = None
    head: str | None = None
    range_note: str = ""
    commits_read: int = 0
    commits_skipped_merges: int = 0
    moves_seen: int = 0
    moves_excepted_archive: int = 0
    moves_unqualified: int = 0
    active_packets: int = 0
    archived_packets: int = 0
    findings: list[Finding] = field(default_factory=list)

    @property
    def refuses(self) -> bool:
        return bool(self.findings)


# --------------------------------------------------------------------------
# PATHS AND IDENTITIES
# --------------------------------------------------------------------------


def packet_dir_of(rel: str) -> str | None:
    """The change packet directory a repository-relative path belongs to, or
    None where it belongs to none.

    Two locations, the two this estate already resolves a packet by:
    `openspec/changes/<id>/…` and
    `openspec/changes/archive/<YYYY-MM-DD>-<id>/…`. A path that IS the
    directory (no file under it) answers None: every read here is driven from
    a diff, which names files.
    """
    parts = rel.split("/")
    if len(parts) < 4 or parts[0] != "openspec" or parts[1] != "changes":
        return None
    if parts[2] == "archive":
        if len(parts) < 5 or not ARCHIVE_DIR_RE.match(parts[3]):
            return None
        return "/".join(parts[:4])
    return "/".join(parts[:3])


def change_id_of_dir(packet_dir: str) -> str:
    """The change ID a packet directory addresses, archive date stripped —
    AND STRIPPED ONLY UNDER THE ARCHIVE ROOT.

    `openspec/changes/add-x` and `openspec/changes/archive/2026-09-09-add-x`
    are the same IDENTITY at two moments of its life, which is the whole
    reason the archive relocation is never a declared move. THE DATE PREFIX
    MEANS THAT AND ONLY THAT, so it is stripped only where the convention puts
    it. `CHANGE_ID_RE` admits an ACTIVE id that merely begins the same way
    (`2026-09-14-example` is a legal change id), and stripping it there would
    hand this gate a source identity no packet has ever carried: `ever_ratified`
    would walk the wrong pathspecs, answer "never ratified", and pass an
    undeclared rename — and the archive exception, which compares the two ids,
    would stop recognizing that packet's own relocation. (Copilot, PR #1039.)
    """
    name = packet_dir.rsplit("/", 1)[-1]
    if not is_archived_dir(packet_dir):
        return name
    return support._ARCHIVE_DATE_RE.sub("", name)


def is_archived_dir(packet_dir: str) -> bool:
    return packet_dir.startswith(ARCHIVE_ROOT)


def _short(revision: str) -> str:
    return revision[:12]


# --------------------------------------------------------------------------
# THE GIT READS
# --------------------------------------------------------------------------


def _run(root: Path, *args: str) -> str | None:
    """A git read, or None where git could not perform it.

    NON-ZERO IS None AND NEVER AN EMPTY STRING, which is the distinction every
    fail-closed arm in this module rests on.
    """
    done = subprocess.run(  # NOSONAR: argv is allowlisted; shell is disabled
        ["git", "-C", str(root.resolve()), *args],
        capture_output=True, text=True, check=False,
    )
    if done.returncode != 0:
        return None
    return done.stdout


def resolve(root: Path, revision: str) -> str | None:
    """`revision` as a commit hash, or None when it resolves to no commit."""
    out = _run(root, "rev-parse", "--verify", "--end-of-options",
               f"{revision}^{{commit}}")
    return out.strip() if out else None


def commit_parents(root: Path, commit: str) -> list[str] | None:
    """The parents of `commit`, or None when the read could not be performed.

    An EMPTY LIST is an ANSWER: a root commit has no parent, and so does a
    commit at a shallow checkout's grafted boundary. Neither can have brought
    a packet in by a move that this gate could pair, and REFUSING every
    shallow checkout outright is a new refusal class on a gate with no bypass
    flag — `tasks.md` § 6.4 names it NOT TAKEN, and names the change that
    would have to say so.
    """
    out = _run(root, "log", "-1", "--format=%P", "--end-of-options", commit)
    if out is None:
        return None
    return out.split()


@dataclass(frozen=True)
class CommitDiff:
    """One commit against its parent: the renames git paired, and every path
    either side of the diff."""

    renames: tuple[tuple[str, str], ...]
    paths: tuple[str, ...]


def diff_at(root: Path, parent: str, commit: str) -> CommitDiff | None:
    """The name-status diff with rename detection, or None where the read
    could not be performed — the PRIMARY arm.

    `-M` EXPLICITLY (a `diff.renames=false` in the repository configuration
    must not be able to switch this gate off), `-l0` to lift the rename limit
    (detection that silently gives up is a vacuous pass), `-r` so a directory
    move is reported as the file renames it is, and NO PATHSPEC: limiting the
    diff is how a pairing gets filtered out before detection runs, which
    `renamed_from`'s own docstring measures.

    ONLY `R` COUNTS AS A MOVE. Copy detection is not requested and `C` rows
    are not treated as moves if a configuration produces them: a "rename" that
    leaves the source directory standing is a FORK, and the requirement is
    explicit that a fork by copy declares nothing and is not refused.
    """
    out = _run(root, "diff-tree", "-r", "-M", "-l0", "--name-status",
               "--no-commit-id", "--end-of-options", parent, commit)
    if out is None:
        return None
    renames: list[tuple[str, str]] = []
    paths: list[str] = []
    for row in out.splitlines():
        if not row.strip():
            continue
        fields = row.split("\t")
        status = fields[0]
        if status.startswith("R") and len(fields) == 3:
            renames.append((fields[1], fields[2]))
            paths.extend((fields[1], fields[2]))
        elif len(fields) >= 2:
            paths.append(fields[-1])
    return CommitDiff(tuple(renames), tuple(paths))


def _tree_rows_or_refuse(root: Path, revision: str, path: str,
                         what: str) -> list[str]:
    """`_tree_rows`, with a None turned into the CANNOT RUN this gate owes.

    The shared reader returns None for a read it could not perform and `[]`
    for a path that is genuinely absent — the distinction its docstring exists
    to preserve — and every caller HERE must refuse on the first and answer on
    the second.
    """
    rows = support._tree_rows(root, revision, path)
    if rows is None:
        raise ArrivalCannotRun(
            f"REFUSE {UNREADABLE}: {what} CANNOT RUN. The read that could not "
            f"be performed is `git ls-tree {_short(revision)} -- {path}`. A "
            f"presence read that fails is not a path that is absent, and this "
            f"gate never reads the one as the other.")
    return rows


def _tree_dirs(root: Path, revision: str, path: str) -> list[str] | None:
    """The DIRECTORY entries one level under `path` at `revision`, or None
    where the listing could not be performed.

    TYPE-AWARE, unlike `_tree_rows`, because this read answers "which packet
    DIRECTORIES are here" and a file dropped beside them is not one. Nothing
    but a tree entry can be a packet, and the corpus carries no blob directly
    under `openspec/changes/` or under the archive today — measured — so this
    is a guard against a future file rather than a filter with work to do.
    """
    out = _run(root, "ls-tree", "--end-of-options", revision, "--", path)
    if out is None:
        return None
    found: list[str] = []
    for row in out.splitlines():
        head, _, name = row.partition("\t")
        fields = head.split()
        if len(fields) >= 2 and fields[1] == "tree" and name.strip():
            found.append(name.strip())
    return found


def packet_dirs_at(root: Path, revision: str) -> list[str] | None:
    """Every change packet directory at `revision`, active and archived, or
    None where the listing could not be read.

    THE TREE IS THE FAIL-CLOSED ARM: it needs no blob, so it answers on
    exactly the checkouts where the pairing does not. It says which packet
    directories ARRIVED and which LEFT between two commits, and it is never
    used to PAIR one with the other.
    """
    rows = _tree_dirs(root, revision, f"{CHANGES_ROOT}/")
    if rows is None:
        return None
    found = [row for row in rows if row != ARCHIVE_ROOT.rstrip("/")]
    archived = _tree_dirs(root, revision, ARCHIVE_ROOT)
    if archived is None:
        return None
    for row in archived:
        name = row.rstrip("/").rsplit("/", 1)[-1]
        if ARCHIVE_DIR_RE.match(name):
            found.append(f"{ARCHIVE_ROOT}{name}")
    return sorted(found)


def _identity_paths_at(root: Path, revision: str, identity: str, *,
                       archive_rows: list[str] | None = None) -> list[str]:
    """EVERY path `identity`'s `proposal.md` occupies at `revision`, FAILING
    CLOSED on a read this checkout cannot perform.

    THE RULE IS `proposal_support.identity_paths_at`'s AND IS NOT RESTATED
    HERE: the active location first, then a dated archive directory carrying
    the same id, resolved by IDENTITY and never by history. What differs is
    one line of None-handling — the shared reader treats a `_tree_rows`
    failure as "no row", which its own docstring names as today's behaviour
    and hands to `tasks.md` § 3.4 — and this gate cannot afford it: an
    unreadable presence read would resolve an unreadable identity to "never
    ratified" and pass an undeclared landing on the one checkout where nothing
    can be proved.

    § 3.4 HAS LANDED and the shared reader now fails closed too — but by
    raising `OriginRetentionError`, not this module's `ArrivalCannotRun`
    (module docstring above has the measurement). DELETE THIS AND CALL THE
    SHARED READER once a caller here adapts that exception at the boundary;
    not sooner.
    """
    found: list[str] = []
    active = f"{CHANGES_ROOT}/{identity}/proposal.md"
    what = f"the presence of identity `{identity}` at {_short(revision)}"
    if _tree_rows_or_refuse(root, revision, active, what):
        found.append(active)
    if archive_rows is None:
        archive_rows = _tree_rows_or_refuse(
            root, revision, ARCHIVE_ROOT,
            f"the archive listing at {_short(revision)}")
    for row in archive_rows:
        name = row.rstrip("/").rsplit("/", 1)[-1]
        match = ARCHIVE_DIR_RE.match(name)
        if match is None or match.group("id") != identity:
            continue
        archived = f"{ARCHIVE_ROOT}{name}/proposal.md"
        if _tree_rows_or_refuse(root, revision, archived, what):
            found.append(archived)
    return found


def proposal_path_at(root: Path, revision: str, identity: str, *,
                     archive_rows: list[str] | None = None) -> str | None:
    """The ONE path `identity` occupies at `revision`, or None for none.

    Refuses CANNOT RUN over more than one, on `proposal_path_at`'s own terms:
    two locations for one id is an AMBIGUITY to report and not a collision to
    settle by preferring one.
    """
    found = _identity_paths_at(root, revision, identity,
                               archive_rows=archive_rows)
    if len(found) > 1:
        raise ArrivalCannotRun(
            f"REFUSE {UNREADABLE}: the arrival gate CANNOT RUN. At commit "
            f"{_short(revision)} identity `{identity}` resolves to MORE THAN "
            f"ONE location — " + ", ".join(f"`{p}`" for p in found) +
            " — and an identity chosen from a set is chosen by the resolver "
            "rather than by an author.")
    return found[0] if found else None


def ever_ratified(root: Path, tip: str, identity: str, *,
                  cache: dict | None = None) -> bool:
    """Has `identity` EVER declared `Status: ratified` at or before `tip`?

    THE QUALIFICATION THE WHOLE REFUSAL TURNS ON, and it is EVER rather than
    NOW. A packet renamed and un-ratified in one commit is back in DRAFT for
    every later hop, so a test taken off the parent's blob would exempt
    exactly the shape this gate exists to catch.

    ONE `git log --full-history` over the identity's own two pathspecs, then
    the identity re-resolved at each visited commit by the rule above and its
    `proposal.md` read. `--topo-order` is not asked for and no commit DATES
    are compared: the question is a boolean over the whole set, not an
    ordering, and the walk stops at the first `ratified` it finds.

    AND IT FAILS CLOSED AT EVERY READ. A history that cannot be listed, a
    presence that cannot be read and a blob that the tree LISTS but the
    checkout cannot produce each refuse CANNOT RUN naming the identity and the
    read. None of them is ever resolved to "never ratified": that silence and
    a lineage that genuinely never ratified are the same value to a probe that
    collapses them, and collapsing them passes an undeclared landing on the
    one checkout where nothing can be proved.
    """
    key = (tip, identity)
    if cache is not None and key in cache:
        return cache[key]
    pathspecs = support._identity_pathspecs(identity)
    listed = _run(root, "log", "--full-history", "--format=%H",
                  "--end-of-options", tip, "--", *pathspecs)
    if listed is None:
        raise ArrivalCannotRun(
            f"REFUSE {UNREADABLE}: the ratification lookup for identity "
            f"`{identity}` CANNOT RUN. The read that could not be performed "
            f"is `git log --full-history {_short(tip)} -- "
            f"{' '.join(pathspecs)}`. An unreadable history is never resolved "
            f"to \"never ratified\": that would pass an undeclared landing on "
            f"the one checkout where nothing can be proved.")
    answer = False
    for revision in listed.split():
        archive_rows = _tree_rows_or_refuse(
            root, revision, ARCHIVE_ROOT,
            f"the ratification lookup for identity `{identity}` at "
            f"{_short(revision)}")
        resolved = proposal_path_at(root, revision, identity,
                                    archive_rows=archive_rows)
        if resolved is None:
            continue
        blob = support.git_show_text(root, revision, resolved)
        if blob is None:
            raise ArrivalCannotRun(
                f"REFUSE {UNREADABLE}: the ratification lookup for identity "
                f"`{identity}` CANNOT RUN. The read that could not be "
                f"performed is `git show {_short(revision)}:{resolved}` — the "
                f"tree at {_short(revision)} LISTS that path, so it is "
                f"PRESENT and its content is unavailable, which is not the "
                f"same as an identity that was never ratified. This gate "
                f"refuses rather than resolving an unreadable history to "
                f"\"never ratified\".")
        if support.declares_ratified(blob):
            answer = True
            break
    if cache is not None:
        cache[key] = answer
    return answer


def declared_at(root: Path, revision: str, packet_dir: str,
                change: str) -> list[str]:
    """The lineage the packet at `packet_dir` declares at `revision`.

    `[]` where the packet carries no `.openspec.yaml` at all, or carries one
    declaring no `former_ids:` — the ordinary case, and the corpus is almost
    entirely such packets. REFUSES CANNOT RUN where the manifest is PRESENT in
    the tree and its content cannot be read, which is the same distinction the
    ratification lookup draws and for the same reason. Raises
    `proposal_support.FormerIdError` — through `declared_former_ids`, which is
    `former_id_problems`'s one caller here — where the declaration is present
    and malformed.
    """
    rel = f"{packet_dir}/.openspec.yaml"
    what = f"the declaration `{rel}` at {_short(revision)}"
    if not _tree_rows_or_refuse(root, revision, rel, what):
        return []
    text = support.git_show_text(root, revision, rel)
    if text is None:
        raise ArrivalCannotRun(
            f"REFUSE {UNREADABLE}: {what} CANNOT RUN. The read that could not "
            f"be performed is `git show {_short(revision)}:{rel}` — the tree "
            f"LISTS that path, so the manifest is PRESENT and its content is "
            f"unavailable, which is not the same as a packet that declares "
            f"nothing.")
    if support.yaml is None:
        raise ArrivalCannotRun(
            f"REFUSE {UNREADABLE}: {what} CANNOT RUN. PyYAML is not available "
            f"in this environment, so a declaration cannot be parsed and a "
            f"packet that declares one cannot be told from a packet that "
            f"declares none.")
    try:
        data = support.yaml.safe_load(text)
    except support.yaml.YAMLError as exc:
        raise support.FormerIdError(
            f"{change}: `{rel}` at {_short(revision)} is not parseable YAML "
            f"({exc.__class__.__name__}), so the declaration it carries "
            f"cannot be read") from exc
    if not isinstance(data, dict):
        # A PRESENT MANIFEST THAT IS NOT A MAPPING IS MALFORMED, NOT EMPTY.
        # `yaml.safe_load` answers None for an empty document and a list for a
        # sequence, and passing either on as "no packet" would hand
        # `declared_former_ids` the same value an ABSENT manifest gives it —
        # so a draft rename or an append-only update carrying a broken
        # `.openspec.yaml` would pass this arm while the corpus arm refuses
        # the identical state. Read as it is written instead. (Copilot, #1039.)
        kind = ("an empty document" if data is None
                else f"a {type(data).__name__}")
        raise support.FormerIdError(
            f"{change}: `{rel}` at {_short(revision)} is PRESENT and did not "
            f"read as a mapping — it parsed as {kind} — so any `former_ids:` "
            f"it carries cannot be read, and an unreadable declaration is not "
            f"a packet that declares nothing")
    return support.declared_former_ids(change, data)


# --------------------------------------------------------------------------
# THE ARRIVAL QUESTION, ONE COMMIT AT A TIME
# --------------------------------------------------------------------------


def moves_at(diff: CommitDiff) -> list[tuple[str, str]]:
    """The packet-directory moves a commit performs — `(source, destination)`
    directory pairs, deduplicated and ordered.

    AGGREGATED OVER EVERY FILE OF THE PACKET rather than off `proposal.md`
    alone: a move that rewrites the proposal as it travels pairs some other
    file of the packet instead, and a gate keyed on the proposal would report
    no move at all (measured; the module docstring names the fixture).
    """
    seen: list[tuple[str, str]] = []
    for source, destination in diff.renames:
        left = packet_dir_of(source)
        right = packet_dir_of(destination)
        if left is None or right is None or left == right:
            continue
        if (left, right) not in seen:
            seen.append((left, right))
    return sorted(seen)


def relocations_at(diff: CommitDiff, before: list[str],
                   after: list[str]) -> list[tuple[str, str]]:
    """The packet-directory RELOCATIONS a commit performs — the pairings of
    `moves_at` that the TREE confirms are a directory leaving and a directory
    arriving.

    A FILE THAT CROSSES TWO STANDING PACKETS IS NOT A PACKET MOVING. Without
    this, one `design.md` relocated from a ratified packet into another packet
    that is also standing reads as an arrival from a ratified identity, and the
    gate refuses an ordinary edit — a required gate refusing a landing nobody
    can repair by declaring anything, because nothing moved. So a pairing
    counts only where the SOURCE directory was present at the parent and is
    gone here, and the DESTINATION was absent at the parent and is present
    here. (Copilot, PR #1039.)

    THIS IS NOT PAIRING FROM THE TREE, which `design.md` D3 declined by name.
    The pairing is still git's and only git's; the tree is asked one further
    question about a pairing git has already made. A source that still stands
    is the COPY shape the requirement says declares nothing, and a destination
    that already stood is not a packet directory being BROUGHT IN.
    """
    return [(source, destination)
            for source, destination in moves_at(diff)
            if source in before and source not in after
            and destination in after and destination not in before]


def _undeclared_finding(commit: str, source: str, destination: str,
                        qualifying: str, expected: list[str],
                        declared: list[str]) -> Finding:
    """The refusal, naming the commit, both paths and the ONE repair."""
    dropped = [entry for entry in expected if entry not in declared]
    extra = [entry for entry in declared if entry not in expected]
    detail = ""
    if dropped and declared:
        detail = (
            f" This move SHEDS the lineage {dropped!r} the source carried: a "
            f"move that drops an entry the source declared is the same defect "
            f"as never declaring one.")
    elif extra:
        detail = (
            f" It declares {extra!r}, which the source did not carry and this "
            f"move did not bring.")
    elif declared and declared != expected:
        detail = (
            " Its entries are the source's, in an order the source did not "
            "carry them in.")
    return Finding(
        status=UNDECLARED,
        commit=commit,
        message=(
            f"REFUSE {UNDECLARED}: commit {_short(commit)} brings "
            f"`{destination}/` in by a MOVE from `{source}/`, whose identity "
            f"`{qualifying}` HAS declared `Status: ratified`, and "
            f"`{destination}/.openspec.yaml` does not declare that move — it "
            f"declares {declared!r} where the arriving list must be "
            f"{expected!r}.{detail} THE ONE REPAIR: declare the source id in "
            f"the destination packet's `former_ids:` IN THE SAME COMMIT, as "
            f"the top-level list {expected!r} — every entry the source "
            f"carried, in the order it carried them, then the id the move "
            f"came from. `former_ids:` is a SIBLING of `origin:` and never a "
            f"member of it."))


def _bound_entry_finding(commit: str, packet_dir: str, change: str,
                         entry: str, source: str | None) -> Finding:
    """§ 2.4 — an entry added by a commit that moves nothing into this
    packet."""
    from_note = (
        f"the only move this commit performs into it comes from "
        f"`{source}`, so `{change_id_of_dir(source)}` is the only entry it "
        f"may add"
        if source else
        "this commit performs NO move into that packet")
    return Finding(
        commit=commit,
        message=(
            f"{change}: commit {_short(commit)} adds former id {entry!r} to "
            f"`{packet_dir}/.openspec.yaml`, and {from_note}. AN ENTRY IS "
            f"ADDED ONLY BY THE COMMIT THAT PERFORMS THE MOVE IT RECORDS. "
            f"Absence of a live directory is NOT proof of predecessorship — "
            f"an id that has archived and an id that never existed both lack "
            f"one — so a rule that only checked for one would let a standing "
            f"packet append an unrelated identity in an ordinary edit, "
            f"acquire that identity's ratification as its baseline, and "
            f"capture every reference written under it."))


def judge_commit(root: Path, commit: str, *,
                 cache: dict | None = None,
                 report: Report | None = None) -> list[Finding]:
    """Every refusal ONE commit earns. Raises `ArrivalCannotRun` for a read
    this checkout cannot perform.

    The whole of the landing question, asked of one commit and of nothing
    else: no predecessor is followed, no successor is consulted, and no state
    carries between commits but the memoized `ever_ratified` answers.
    """
    findings: list[Finding] = []
    parents = commit_parents(root, commit)
    if parents is None:
        raise ArrivalCannotRun(
            f"REFUSE {UNREADABLE}: commit {_short(commit)} CANNOT RUN. Its "
            f"parents could not be listed (`git log -1 --format=%P "
            f"{_short(commit)}`), so neither the pairing nor the tree "
            f"comparison the fail-closed arm needs can be performed.")
    if len(parents) > 1:
        if report is not None:
            report.commits_skipped_merges += 1
        return findings
    if not parents:
        return findings
    parent = parents[0]

    diff = diff_at(root, parent, commit)
    if diff is None:
        before = packet_dirs_at(root, parent)
        after = packet_dirs_at(root, commit)
        read = (f"`git diff-tree -r -M -l0 {_short(parent)} "
                f"{_short(commit)}`")
        if before is None or after is None:
            raise ArrivalCannotRun(
                f"REFUSE {UNREADABLE}: the arrival pairing at commit "
                f"{_short(commit)} CANNOT RUN. The read that could not be "
                f"performed is {read}, and the tree listing that would say "
                f"whether a packet arrived and another left could not be "
                f"performed either.")
        arriving = [d for d in after if d not in before]
        leaving = [d for d in before if d not in after]
        if arriving and leaving:
            raise ArrivalCannotRun(
                f"REFUSE {UNREADABLE}: the arrival pairing at commit "
                f"{_short(commit)} CANNOT RUN. The read that could not be "
                f"performed is {read}. The TREE at that commit shows a packet "
                f"directory ARRIVING (" +
                ", ".join(f"`{d}`" for d in arriving) +
                ") and one LEAVING (" +
                ", ".join(f"`{d}`" for d in leaving) +
                "), so a silence here cannot be told from an answer. This "
                "gate does NOT pair them from the tree — a commit that "
                "withdraws one packet and creates an unrelated other has the "
                "same tree shape — it refuses to answer.")
        return findings

    if not any(path.startswith(f"{CHANGES_ROOT}/") for path in diff.paths):
        return findings

    before = packet_dirs_at(root, parent)
    after = packet_dirs_at(root, commit)
    if before is None or after is None:
        raise ArrivalCannotRun(
            f"REFUSE {UNREADABLE}: the arrival qualification at commit "
            f"{_short(commit)} CANNOT RUN. The packet directories at that "
            f"commit or at its parent could not be listed, so a file that "
            f"crossed two STANDING packets cannot be told from a packet "
            f"directory that MOVED, and this gate does not guess which it was.")
    moves = relocations_at(diff, before, after)
    # EVERY SOURCE, NOT THE LAST ONE READ. Git can pair files from more than
    # one source packet into a single newly created destination, and a mapping
    # that kept one of them would let the LEXICAL ORDER of two ids decide which
    # newly added former id § 2.4 allows — an answer that changes if the
    # packets are renamed and nothing else. (Copilot, PR #1039.)
    arrivals: dict[str, list[str]] = {}
    for source, destination in moves:
        arrivals.setdefault(destination, []).append(source)

    for source, destination in moves:
        if report is not None:
            report.moves_seen += 1
        source_id = change_id_of_dir(source)
        destination_id = change_id_of_dir(destination)
        # THE ARCHIVE RELOCATION, EXCEPTED BY ID, AND IT IS THE ONLY
        # EXCEPTION: the id is preserved, so the identity did not change.
        if is_archived_dir(destination) and destination_id == source_id:
            if report is not None:
                report.moves_excepted_archive += 1
            continue
        # THE SOURCE'S WHOLE DECLARED LINEAGE, read as ONE BLOB at ONE COMMIT.
        inherited = declared_at(root, parent, source, source_id)
        lineage = list(inherited) + [source_id]
        qualifying = next(
            (identity for identity in lineage
             if ever_ratified(root, commit, identity, cache=cache)), None)
        if qualifying is None:
            # A MOVE OF A PACKET THAT HAS NEVER BEEN RATIFIED IS OUT OF SCOPE
            # AND STAYS LAWFUL — renaming a draft is an ordinary authoring act
            # and `docs/document-lifecycle.md` promises it is unaffected.
            if report is not None:
                report.moves_unqualified += 1
            continue
        expected = list(inherited) + [source_id]
        try:
            declared = declared_at(root, commit, destination, destination_id)
        except support.FormerIdError as exc:
            findings.append(Finding(commit=commit, message=str(exc)))
            continue
        if declared != expected:
            findings.append(_undeclared_finding(
                commit, source, destination, qualifying, expected, declared))

    findings += _declaration_findings(root, commit, parent, diff, arrivals,
                                      after)
    return findings


def _declaration_findings(root: Path, commit: str, parent: str,
                          diff: CommitDiff, arrivals: dict[str, list[str]],
                          present: list[str]) -> list[Finding]:
    """§ 2.4 and § 2.5 over every packet this commit touched.

    § 2.5 IS ASKED OF EVERY TOUCHED PACKET AND NOT ONLY OF AN ARRIVING ONE,
    which is the whole of `append_only_problems`'s reason to exist: the
    arrival check only ever runs at a MOVE, so without this a lawful move
    could be declared at its landing and the declaration deleted the day
    after, in a commit no arrival check ever looks at.

    § 2.4 IS THE SAME READ FROM THE OTHER SIDE: the entries this commit ADDS
    must be exactly the source of the move it performs, and a commit that adds
    one while moving nothing into that packet is refused whether the id it
    names has archived, never existed, or stands somewhere else entirely.
    """
    findings: list[Finding] = []
    touched: list[str] = []
    for path in diff.paths:
        packet_dir = packet_dir_of(path)
        if packet_dir is not None and packet_dir not in touched:
            touched.append(packet_dir)
    for packet_dir in sorted(set(touched) & set(present)):
        change = change_id_of_dir(packet_dir)
        sources = arrivals.get(packet_dir, [])
        if len(sources) > 1:
            findings += _multi_source_findings(
                root, commit, parent, packet_dir, change, sources)
            continue
        source = sources[0] if sources else None
        # THE ESTABLISHED LIST TRAVELS WITH THE PACKET: where this commit
        # moved it, the list it carried at the parent is the SOURCE's, read
        # under the source's own id.
        was_dir = source if source is not None else packet_dir
        try:
            established = declared_at(root, parent, was_dir,
                                      change_id_of_dir(was_dir))
            current = declared_at(root, commit, packet_dir, change)
        except support.FormerIdError as exc:
            findings.append(Finding(commit=commit, message=str(exc)))
            continue
        for problem in support.append_only_problems(
                change, established, current):
            findings.append(Finding(
                commit=commit,
                message=f"commit {_short(commit)}: {problem}"))
        if current[:len(established)] != established:
            # The append-only refusal above already names it; the "which
            # entries are new" question has no honest answer over a rewritten
            # list.
            continue
        allowed = change_id_of_dir(source) if source is not None else None
        for entry in current[len(established):]:
            if entry != allowed:
                findings.append(_bound_entry_finding(
                    commit, packet_dir, change, entry, source))
    return findings


def _multi_source_findings(root: Path, commit: str, parent: str,
                           packet_dir: str, change: str,
                           sources: list[str]) -> list[Finding]:
    """§ 2.4 over a destination this commit brought in from MORE THAN ONE
    source — bound to every source, and to none of them by name.

    THE ESTABLISHED LIST IS THE QUESTION THAT HAS NO SINGLE ANSWER HERE. The
    requirement's list is *the source's list with the source id appended*, and
    a destination with two sources has two candidate lists; the append-only
    comparison, which asks what this packet carried BEFORE, therefore has no
    honest reading and is not taken. What survives is the rule that matters:
    AN ENTRY IS ADDED ONLY BY THE COMMIT THAT PERFORMS THE MOVE IT RECORDS, so
    every entry the destination declares must be one a source of THIS commit's
    moves carried, or a source's own id.

    AND THE ARRIVAL ARM STILL JUDGES EACH SOURCE ON ITS OWN: a destination
    whose list satisfies one qualifying source does not satisfy a second, so a
    two-source arrival of two ratified packets is refused there, by name, with
    both paths. This function exists so that the SECOND question — which newly
    added entry is bound to a move — is not answered by the lexical order of
    two ids. (Copilot, PR #1039.)
    """
    findings: list[Finding] = []
    allowed: list[str] = []
    for source in sources:
        source_id = change_id_of_dir(source)
        try:
            carried = declared_at(root, parent, source, source_id)
        except support.FormerIdError as exc:
            findings.append(Finding(commit=commit, message=str(exc)))
            return findings
        for entry in list(carried) + [source_id]:
            if entry not in allowed:
                allowed.append(entry)
    try:
        current = declared_at(root, commit, packet_dir, change)
    except support.FormerIdError as exc:
        findings.append(Finding(commit=commit, message=str(exc)))
        return findings
    for entry in current:
        if entry not in allowed:
            findings.append(Finding(
                commit=commit,
                message=(
                    f"{change}: commit {_short(commit)} brings "
                    f"`{packet_dir}/` in by moves from MORE THAN ONE packet "
                    f"directory (" + ", ".join(f"`{s}`" for s in sources) +
                    f"), and its `former_ids:` names {entry!r}, which none of "
                    f"them carried and none of them is. AN ENTRY IS ADDED "
                    f"ONLY BY THE COMMIT THAT PERFORMS THE MOVE IT RECORDS. "
                    f"With two sources there is no single lawful list — the "
                    f"requirement's list is the SOURCE's list with the SOURCE "
                    f"id appended — so this gate binds the entries to the "
                    f"union of what the sources carried rather than letting "
                    f"the order of two ids decide, and the arrival refusal "
                    f"above says which move went undeclared.")))
    return findings


# --------------------------------------------------------------------------
# THE RANGE, AND THE CORPUS
# --------------------------------------------------------------------------


def commits_in(root: Path, base: str, head: str) -> list[str] | None:
    """The commits of `base..head`, oldest first, MERGES OMITTED.

    `--no-merges` is the module docstring's rule made mechanical: a merge
    performs no move of its own, and every move it carries either sits in this
    same range under its own author or is already on the base branch.
    """
    out = _run(root, "rev-list", "--no-merges", "--reverse",
               "--end-of-options", f"{base}..{head}")
    if out is None:
        return None
    return out.split()


def merges_in(root: Path, base: str, head: str) -> int | None:
    """How many commits of `base..head` `commits_in` dropped as merges.

    Counted rather than inferred so the run's own report says a TRUE thing
    about what it did not read. A gate that quietly skips commits and reports
    a clean range is the vacuous pass this module's tests exist to make
    impossible.
    """
    out = _run(root, "rev-list", "--merges", "--count", "--end-of-options",
               f"{base}..{head}")
    if out is None:
        return None
    return int(out.strip() or "0")


def resolve_range(root: Path, base: str | None, head: str | None,
                  env: dict | None = None) -> tuple[str, str]:
    """The commit range this run judges, resolved to two commit hashes.

    THREE ROUTES, AND THE THIRD IS NOT A PASS. An explicit `--base`/`--head`
    names the range (what the test suite drives). On a GitHub `pull_request`
    run the checkout `actions/checkout@v4` leaves is the MERGE COMMIT GitHub
    built, whose FIRST PARENT is the base tip and whose SECOND is the pull
    request head — so `HEAD^1..HEAD^2` is this pull request's own commits and
    nothing else, and no event payload need be parsed to find them. That is
    `release-tag-gate`'s own derivation, which states the same fact about the
    same checkout.

    A `pull_request` run whose range does NOT resolve REFUSES. `fetch-depth: 0`
    is what makes it resolve, and a checkout without history must refuse
    rather than pass blind — which is exactly what `release-tag-gate` does
    with `gate-unreadable-base` for the same reason.
    """
    env = os.environ if env is None else env
    pull_request = env.get("GITHUB_EVENT_NAME") == "pull_request"
    if base is None and head is None and pull_request:
        base, head = "HEAD^1", "HEAD^2"
    if base is None and head is None:
        raise LookupError("no range")
    base_rev = base or "HEAD^1"
    head_rev = head or "HEAD"
    base_sha = resolve(root, base_rev)
    head_sha = resolve(root, head_rev)
    if base_sha is None or head_sha is None:
        unresolved = [rev for rev, sha in ((base_rev, base_sha),
                                           (head_rev, head_sha))
                      if sha is None]
        raise ArrivalCannotRun(
            f"REFUSE {UNREADABLE}: the arrival gate CANNOT RUN over this "
            f"checkout. " + " and ".join(f"`{rev}`" for rev in unresolved) +
            " does not resolve to a commit. On a `pull_request` run the "
            "checkout is the merge commit GitHub built, whose first parent is "
            "the base tip and whose second is the pull request head, so a "
            "checkout WITHOUT HISTORY cannot be judged — check out with "
            "`fetch-depth: 0`. A gate that cannot read the range it judges "
            "refuses rather than passing blind.")
    return base_sha, head_sha


def corpus_problems(root: Path, report: Report | None = None) -> list[str]:
    """The whole-tree declaration sweep — §§ 2.1, 2.3 and 2.6, over the
    WORKING TREE this gate was given.

    THE THREE READERS SLICE 1 LANDED AND NOBODY CALLED ARE CALLED HERE.
    `former_id_problems` reads each packet's declaration for shape;
    `standing_former_id_problems` refuses a declared id that STILL STANDS as a
    live directory (a packet that still stands was COPIED and not moved); and
    `former_identity_ownership_problems` is the corpus sweep that says a
    former identity has EXACTLY ONE OWNER.

    THE OWNERSHIP SWEEP IS CALLED HERE AND NOWHERE ELSE — the realization
    plan's Q3, recommendation (a), taken on its own terms. This validator
    already walks the corpus and already refuses, and two callers for one
    whole-corpus sweep is two places to keep in step. `proposal-support.py
    verify` is deliberately NOT the second caller.
    """
    problems: list[str] = []
    changes = root / "openspec" / "changes"
    # THE SAME RULE AT THE ANCESTORS, asked BEFORE `is_dir()`, which follows a
    # link like everything else here. A symlinked `openspec/` or
    # `openspec/changes/` moves the WHOLE corpus somewhere no commit carries,
    # and every per-packet check below would then read files the tree arm
    # cannot see while never seeing a symlink itself. Nothing under it is read
    # and nothing is reported about it: the run says the corpus was not read.
    # (Copilot, PR #1039.)
    for ancestor, spelling in ((root / "openspec", "openspec/"),
                               (changes, "openspec/changes/")):
        if ancestor.is_symlink():
            problems.append(
                f"`{spelling}` is a SYMLINK. Git stores one as a blob whose "
                f"content is a path, so `git ls-tree` reports no directory "
                f"there and the commit-range arm of this gate sees no corpus "
                f"at that path. This arm will not walk one through it: no "
                f"declaration, no standing id and no ownership question was "
                f"answered over this tree. Replace it with the directory "
                f"itself, or remove it")
            return problems
    if not changes.is_dir():
        return problems
    live: list[Path] = []
    for entry in sorted(changes.iterdir()):
        if entry.name == "archive":
            continue
        # A SYMLINK IS NOT A PACKET DIRECTORY TO THIS GATE, and saying so is
        # not pedantry: git stores one as a BLOB whose content is a path, so
        # `git ls-tree` — the read the range arm and the fail-closed arm both
        # use — reports no tree there and sees no packet. Following it here
        # would make the corpus arm adjudicate a directory the other arms
        # cannot see, possibly outside the checkout entirely, and report a
        # clean or a refusing corpus on evidence no commit carries. Reported
        # rather than skipped, because a silence is what this arm refuses.
        # (Copilot, PR #1039.)
        if entry.is_symlink():
            problems.append(_symlink_problem(entry, "a change packet"))
            continue
        if entry.is_dir():
            live.append(entry)
    archive = changes / "archive"
    archived: list[Path] = []
    if archive.is_symlink():
        problems.append(_symlink_problem(archive, "the packet archive"))
    elif archive.is_dir():
        for entry in sorted(archive.iterdir()):
            if entry.is_symlink():
                problems.append(_symlink_problem(entry, "an archived packet"))
                continue
            if entry.is_dir():
                archived.append(entry)
    if report is not None:
        report.active_packets = len(live)
        report.archived_packets = len(archived)
    for directory in live + archived:
        change = support.change_id_of(directory)
        rel = f"{support._corpus_rel(directory)}/.openspec.yaml"
        manifest = directory / ".openspec.yaml"
        if manifest.is_symlink():
            # THE SAME RULE ONE LEVEL DOWN, and it catches the DANGLING link
            # too — `exists()` follows the link and answers False for one, so
            # a manifest that is present in the tree would read as no manifest
            # at all. `is_symlink()` is asked FIRST, so nothing is ever read
            # THROUGH a link. (Copilot, PR #1039.)
            problems.append(
                f"{change}: `{rel}` is a SYMLINK. Git stores one as a blob "
                f"whose content is a path, so the declaration this packet "
                f"would carry is not in this tree and this gate will not read "
                f"one through a link — a dangling link would read as no "
                f"manifest at all, and a live one as a file no commit "
                f"carries: replace it with the file itself, or remove it")
            continue
        try:
            packet = support.load_packet(directory)
        except (UnicodeDecodeError, OSError) as exc:
            # A READ THAT RAISES IS STILL A READ THAT FAILED, and it leaves
            # this gate with an exit code its own contract does not name.
            # `load_packet` decodes as UTF-8 and catches only `YAMLError`, so
            # a manifest carrying bytes that are not UTF-8 comes out of it as
            # an exception rather than as None — a crash where the two
            # documented exits are 1 and 2. (Copilot, PR #1039.)
            problems.append(
                f"{change}: `{rel}` is PRESENT and could not be read at all "
                f"({exc.__class__.__name__}), so any `former_ids:` it carries "
                f"cannot be read and none of the declaration refusals could "
                f"be taken over it: repair the file, or remove it")
            continue
        if packet is None and (directory / ".openspec.yaml").exists():
            # AN UNREADABLE MANIFEST IS NOT A PACKET THAT DECLARES NOTHING.
            # `load_packet` answers None for FOUR states — absent, unparseable
            # YAML, a top-level that is not a mapping, and a path that is not
            # a regular file — and only the first is an answer. Handing the
            # others to `former_id_problems` as a packet with no declaration
            # is the vacuous read this gate exists to refuse: a malformed
            # `former_ids:` would be swallowed by the parser that could not
            # reach it. `exists()` rather than `is_file()` because a path that
            # is PRESENT and not a regular file is the same defect wearing a
            # different shape, and reading it as absent is the silence this
            # arm refuses. The commit-range arm draws the same distinction
            # (`declared_at` raises rather than returning `[]`); this is that
            # rule over the working tree. (Copilot, PR #1039.)
            problems.append(
                f"{change}: `{rel}` is PRESENT and did not read as a mapping "
                f"— unparseable YAML, a top-level that is not one, or a path "
                f"that is not a regular file — so any `former_ids:` it "
                f"carries cannot be read and none of the declaration refusals "
                f"could be taken over it. An unreadable manifest is not a "
                f"packet that declares nothing: repair the file, or remove it")
            continue
        shape = support.former_id_problems(change, packet)
        problems += shape
        if shape:
            continue
        declared = support.declared_former_ids(change, packet)
        if declared:
            problems += support.standing_former_id_problems(
                root, change, declared)
    if any("is a SYMLINK" in problem for problem in problems):
        # THE SWEEP WALKS THE WORKING TREE ITSELF, in a shared reader this
        # slice imports and does not edit. At this arm's own head the walk
        # FOLLOWED the link this arm has just refused — measured:
        # `former_identity_claimants` read the target's `former_ids:` and
        # claimed an identity from outside this checkout. PR #1038 (merged
        # to main at `701c8fde`) closed that exact hole in the shared reader
        # too, with the same containment guard this arm carries; re-measured
        # after that merge, the claim for THIS scenario is
        # `{'change-a': [...]}`, not `change-from-outside`. The skip stands
        # anyway: this arm does not review that module's changes, so a
        # refusal already reached here should not start depending on staying
        # in step with a guard it does not own. The run is already refusing,
        # so nothing is lost by saying which question went unanswered instead
        # of trusting an imported walk over a tree this arm has already
        # refused. (Copilot, PR #1039; re-measured against PR #1038, 2026-09-14.)
        problems.append(
            "the ownership sweep over this corpus was NOT run: a symlink "
            "stands where a packet directory or a manifest would be (named "
            "above), and the sweep re-reads the corpus through the working "
            "tree — through that link included. Whether every declared former "
            "identity has EXACTLY ONE OWNER is therefore not established over "
            "this tree: repair the link and run again")
        return problems
    try:
        problems += support.former_identity_ownership_problems(root)
    except (UnicodeDecodeError, OSError) as exc:
        # THE SWEEP RE-READS EVERY MANIFEST ITSELF, in a module this slice
        # imports and does not edit, so the same unreadable file reaches it a
        # second time and raises there too. Turned into a refusal here rather
        # than left to leave the gate with an undocumented exit: the packet
        # itself is already named by the loop above, and this says which
        # question went unanswered because of it. (Copilot, PR #1039.)
        problems.append(
            f"the ownership sweep over this corpus could not be completed "
            f"({exc.__class__.__name__}): a packet manifest it re-reads is "
            f"present and unreadable, so whether every declared former "
            f"identity has EXACTLY ONE OWNER was not established. The "
            f"unreadable manifest is named above")
    return problems


def _symlink_problem(entry: Path, what: str) -> str:
    """One refusal for a symlink standing where a packet directory would be.

    Written once because the three places it can happen — an active packet,
    the archive root, an archived packet — differ only in what they are called.
    """
    return (
        f"`{support._corpus_rel(entry)}` is a SYMLINK where {what} directory "
        f"would be. Git stores a symlink as a BLOB whose content is a path, so "
        f"`git ls-tree` reports no directory there and the commit-range arm of "
        f"this gate cannot see a packet at that path; reading through it here "
        f"would adjudicate a tree no commit carries, possibly outside this "
        f"checkout. Replace it with the directory itself, or remove it")


def scan(root: Path, *, base: str | None = None, head: str | None = None,
         env: dict | None = None) -> Report:
    """The whole gate, as a value. The CLI below only prints it.

    THE FIRST THING IT DOES IS REFUSE A RUN THAT COULD ONLY PASS VACUOUSLY.
    Without PyYAML no declaration can be parsed, `load_packet` answers None for
    every packet in the corpus, and `former_id_problems` then has nothing to
    refuse — so the whole-tree sweep would report a clean corpus it never read.
    A green check that proves nothing was read is the class of defect the
    sibling gate's own workflow adds an assertion step for; here the reader
    refuses it at the source, so the refusal holds however the gate is invoked
    and not only through the workflow that installs the dependency.
    """
    if support.yaml is None:
        raise ArrivalCannotRun(
            f"REFUSE {UNREADABLE}: the arrival gate CANNOT RUN. PyYAML is not "
            f"available in this environment, so no `.openspec.yaml` can be "
            f"parsed — every packet would read as declaring nothing and the "
            f"whole-tree sweep would report a clean corpus it never read. "
            f"Install `pyyaml` rather than reading this silence as an answer.")
    report = Report()
    try:
        report.base, report.head = resolve_range(root, base, head, env=env)
    except LookupError:
        report.range_note = (
            "no commit range: this run is not a `pull_request` event and "
            "named no `--base`/`--head`, so no arrival was judged and only "
            "the whole-tree declaration sweep ran")
    else:
        commits = commits_in(root, report.base, report.head)
        if commits is None:
            raise ArrivalCannotRun(
                f"REFUSE {UNREADABLE}: the arrival gate CANNOT RUN. The "
                f"commits of `{_short(report.base)}..{_short(report.head)}` "
                f"could not be listed, so the range this pull request "
                f"carries is unknown and no landing in it was judged.")
        merges = merges_in(root, report.base, report.head)
        if merges is None:
            raise ArrivalCannotRun(
                f"REFUSE {UNREADABLE}: the arrival gate CANNOT RUN. The merge "
                f"commits of `{_short(report.base)}..{_short(report.head)}` "
                f"could not be counted, so this run cannot say which commits "
                f"of the range it did not read.")
        report.commits_skipped_merges += merges
        cache: dict = {}
        for commit in commits:
            report.commits_read += 1
            report.findings += judge_commit(root, commit, cache=cache,
                                            report=report)
        report.range_note = (
            f"{report.commits_read} commit(s) of "
            f"`{_short(report.base)}..{_short(report.head)}` judged "
            f"({report.commits_skipped_merges} merge commit(s) skipped: a "
            f"merge performs no move of its own, and every move one carries "
            f"is either in this same range under its own author or already "
            f"on the base branch)")
    for problem in corpus_problems(root, report):
        report.findings.append(Finding(message=problem))
    return report
