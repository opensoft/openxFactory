#!/usr/bin/env python3
"""The re-pin lane's decision code: advance the pinned decision core, or refuse.

REALIZES `mirror-floor-regeneration-automation` (ratified 2026-09-06, record
`openspec/changes/mirror-floor-regeneration-automation/review/ratification-2026-09-06.md`),
whose eight ADDED requirements this module and
`.github/workflows/review-lane-repin.yml` split between them: the workflow holds
the triggers, the identity and the pull request; every JUDGMENT lives here, in
functions that take their inputs as arguments and touch no network.

WHY THE SPLIT IS DRAWN THERE. A `run:` block is testable only by grepping its
own text, and a lane whose refusals live in shell is a lane whose refusals are
asserted rather than measured. So the workflow reads the two repositories with
`gh` — visible in the run log, re-runnable by a reviewer with the same two API
calls — and hands this module PURE INPUTS: the resolved default branch, the
candidate commit, whether that commit is reachable from that branch, and the
floor document's BYTES. Every requirement's refusal is then a unit test with a
fixture, not a workflow that has to be fired to be believed.

WHAT THIS MODULE MAY NOT DO, and it is the packet's own list:

  * It never merges, never approves, and never writes to `main` (requirement 1).
    Nothing here shells out to `gh` at all.
  * It never reads a trigger payload (requirement 2). The candidate commit
    arrives as an argument the workflow resolved from codexFactory's default
    branch at run time; there is no code path from `client_payload` to a
    checkout, a write, or a pin value.
  * It moves ALL FIVE SITES or it opens nothing, and it proves the move by
    RE-READING each site from disk afterwards rather than by trusting that its
    own `re.sub` matched (requirement 3, decision M-2).
  * It COPIES the vendored snapshot and computes the snapshot's `sha256` and
    `entry_count` FROM THE BYTES IT WROTE — never from a report, a pull-request
    body, or any other claim made by the repository being witnessed
    (requirement 4, decision M-3).
  * It writes nothing outside the five sites (requirement 1, decision M-7).

THE FIVE SITES ARE ONE LIST, `PINNED_SITES`, and that is deliberate. The hand
path's failure mode is a sixth site appearing that nobody remembers to move;
`tests/review_lane_pin/test_repin_lane.py` sweeps the tree for a pin-shaped
VALUE line naming the core commit and requires the set it finds to equal this
list exactly, so a site added later fails a test instead of silently going
stale.
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import pathlib
import re
import sys

import yaml


# ---------------------------------------------------------------------------
# The pinned repository and the document this lane mirrors.
# ---------------------------------------------------------------------------

SOURCE_REPOSITORY = "codeXfactory/codexFactory"

# Where the pinned core keeps the authoritative floor document. Restated as
# literals rather than read out of the pin, for the reason
# `tests/review_lane_pin/test_floor_snapshot.py` gives about its own copy of
# this constant: a value read from the artifact it is used to check makes the
# check a tautology.
#
# AN ORDERED LIST, AND IT IS A MIGRATION WINDOW RATHER THAN A FEATURE.
# `relocate-review-authority-floor-mirror` (ratified 2026-09-08, PR #817)
# realizes M-1 step (1): codexFactory is relocating this document off every
# CODEOWNERS prefix (`relocate-review-authority-floor`, codexFactory #293), and
# a two-repository move cannot be atomic — if codexFactory moved first, every
# firing of this lane would refuse `floor_document_unobtainable`. So the lane
# resolves the document through the candidates BELOW, IN ORDER, and takes the
# FIRST one obtained.
#
# THE PATH IN FORCE IS FIRST, AND THAT IS THE WHOLE SAFETY ARGUMENT (M-2).
# Until codexFactory actually moves the file, candidate one always resolves and
# this lane behaves EXACTLY as it did with a single path — so landing this ahead
# of another repository's change is an observable no-op rather than a leap.
# Newest-first would change behaviour on the day this landed instead of on the
# day the document moved.
#
# IT RETURNS TO ONE ENTRY (M-1 step (3)). Once one advance has been observed
# against the successor, the superseded entry is deleted and this is a
# single-path constant again. A standing list of two would mean the lane no
# longer knows where the document lives, and a file reappearing at the abandoned
# path — by a revert, a bad cherry-pick, or an author who did not read the
# relocation — would be byte-copied into this repository's witnessed snapshot.
#
# THE LANE NEVER SEARCHES (M-7). It resolves ONLY these paths, in this order. No
# lookup by `kind: repository_gate_floor`, by basename, or by code search: a
# discovered file is one an author elsewhere can plant, and what is found here is
# copied verbatim into `contracts/review-lane-floor-snapshot.yaml`.
FLOOR_IN_SOURCE_CANDIDATES: tuple[str, ...] = (
    # The path in force today.
    "scripts/merge_master/openxfactory-review-authority-floor.yaml",
    # The successor `relocate-review-authority-floor` D-1 names.
    "floor/openxfactory-review-authority-floor.yaml",
)

# The head of the list: the path in force. Kept as its own name because every
# message that names ONE path means this one, and because a reader looking for
# the old single-valued constant finds it still saying what it always said.
FLOOR_IN_SOURCE = FLOOR_IN_SOURCE_CANDIDATES[0]

SHA40_RE = re.compile(r"^[0-9a-f]{40}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

# The generated block writes the openxFactory commit it enumerated at into a
# YAML COMMENT, not a data field. Same expression as the freshness verifier's,
# for the same reason.
GENERATED_AT_RE = re.compile(
    r"^\s*#\s*generated_at:\s*([0-9a-f]{40})\s*$", re.MULTILINE)


@dataclasses.dataclass(frozen=True)
class PinnedSite:
    """One place in this repository that names the pinned decision core.

    `pattern` matches the whole LINE and captures the value in group 2, with
    group 1 the prefix and group 3 the suffix, so a rewrite is a substitution
    that cannot reach a comment. That matters here more than it usually would:
    `contracts/review-lane-pin.yaml` and
    `.github/workflows/merge-master-approval.yml` both carry the current core
    commit MANY times over in their advance-history comments, and those
    occurrences are a record of what happened rather than a claim about what is
    pinned. A blind string replacement would rewrite history — literally.
    """

    label: str
    path: str
    pattern: re.Pattern
    kind: str  # "commit" | "sha256" | "count" | "bytes"


def _commit_line(key: str) -> re.Pattern:
    r"""`  <key>: "<40 hex>"` and nothing else on the line, comments excluded.

    The leading `\s*` cannot reach a `#`, so an advance-history comment naming
    the same commit is unreachable by every rewrite this module performs.
    """
    return re.compile(rf"^(\s*{key}: \")([0-9a-f]{{40}})(\")$", re.MULTILINE)


PIN_FILE = "contracts/review-lane-pin.yaml"
SNAPSHOT_FILE = "contracts/review-lane-floor-snapshot.yaml"
MERGE_MASTER_WORKFLOW = ".github/workflows/merge-master-approval.yml"
PYTEST_SUITE_WORKFLOW = ".github/workflows/pytest-suite.yml"

# THE FIVE SITES, and the two derived witnesses the fifth carries. The
# enumeration is the ratified requirement "The mirror is inert until the pin
# carries the rule, and the pin moves as one act"'s, restated as code:
#
#   1  contracts/review-lane-pin.yaml            core_commit
#   2  .github/workflows/merge-master-approval.yml   PINNED_CORE_COMMIT
#   3  .github/workflows/merge-master-approval.yml   the core checkout `ref:`
#   4  .github/workflows/pytest-suite.yml            the core checkout `ref:`
#   5  contracts/review-lane-floor-snapshot.yaml     the byte copy
#      ...and, declared beside the pin, that copy's `sha256` and `entry_count`.
PINNED_SITES: tuple[PinnedSite, ...] = (
    PinnedSite("pin.core_commit", PIN_FILE,
               re.compile(r"^(core_commit: \")([0-9a-f]{40})(\")$", re.MULTILINE),
               "commit"),
    PinnedSite("merge-master-approval.PINNED_CORE_COMMIT", MERGE_MASTER_WORKFLOW,
               _commit_line("PINNED_CORE_COMMIT"), "commit"),
    PinnedSite("merge-master-approval.core-checkout-ref", MERGE_MASTER_WORKFLOW,
               _commit_line("ref"), "commit"),
    PinnedSite("pytest-suite.core-checkout-ref", PYTEST_SUITE_WORKFLOW,
               _commit_line("ref"), "commit"),
    PinnedSite("snapshot.bytes", SNAPSHOT_FILE, re.compile(r"(?!)"), "bytes"),
)

# The fifth site's two DERIVED declarations. They live in the pin file beside
# `floor_snapshot.path`, and they are computed from the bytes written to the
# snapshot — never carried across from codexFactory.
SNAPSHOT_WITNESS_SITES: tuple[PinnedSite, ...] = (
    PinnedSite("pin.floor_snapshot.sha256", PIN_FILE,
               re.compile(r"^(\s*sha256: \")([0-9a-f]{64})(\")$", re.MULTILINE),
               "sha256"),
    PinnedSite("pin.floor_snapshot.entry_count", PIN_FILE,
               re.compile(r"^(\s*entry_count: )(\d+)()$", re.MULTILINE),
               "count"),
)

# Every file this lane is permitted to write. Requirement 1's third scenario —
# "every changed file is one of the sites that name the pinned core commit" —
# is enforced against this set, and the workflow stages exactly these paths.
WRITABLE_PATHS: tuple[str, ...] = (
    PIN_FILE, SNAPSHOT_FILE, MERGE_MASTER_WORKFLOW, PYTEST_SUITE_WORKFLOW)


# ---------------------------------------------------------------------------
# Outcomes. Three of them, and the lane's whole decision is which one it is.
# ---------------------------------------------------------------------------

@dataclasses.dataclass(frozen=True)
class Refusal:
    stage: str
    reason: str

    def as_dict(self) -> dict:
        return {"action": "refuse", "stage": self.stage, "reason": self.reason}


@dataclasses.dataclass(frozen=True)
class NoOp:
    reason: str

    def as_dict(self) -> dict:
        return {"action": "noop", "reason": self.reason}


@dataclasses.dataclass(frozen=True)
class Witnesses:
    """What a snapshot's bytes say about themselves, computed from the bytes."""

    sha256: str
    entry_count: int
    generated_at: str | None
    block_entry_count: int | None

    def as_dict(self) -> dict:
        return {"sha256": self.sha256, "entry_count": self.entry_count,
                "generated_at": self.generated_at,
                "block_entry_count": self.block_entry_count}


@dataclasses.dataclass(frozen=True)
class Advance:
    candidate_commit: str
    core_before: str
    source_default_branch: str
    reachability_evidence: str
    before: Witnesses
    after: Witnesses
    clears: tuple[str, ...]
    #: The candidate path the document was ACTUALLY obtained from. Carried on
    #: the outcome rather than re-derived where the body is built, so the
    #: witness a reviewer reads and the path the lane read are the same value
    #: and cannot drift apart during the migration window.
    floor_source_path: str = FLOOR_IN_SOURCE

    def as_dict(self) -> dict:
        return {"action": "advance",
                "candidate_commit": self.candidate_commit,
                "core_before": self.core_before,
                "source_repository": SOURCE_REPOSITORY,
                "source_default_branch": self.source_default_branch,
                "reachability_evidence": self.reachability_evidence,
                "floor_source_path": self.floor_source_path,
                "before": self.before.as_dict(),
                "after": self.after.as_dict(),
                "clears": list(self.clears)}


Outcome = Refusal | NoOp | Advance


# ---------------------------------------------------------------------------
# Measurement helpers. Every one of them reads BYTES and returns a number or a
# string; none of them takes anybody's word for anything.
# ---------------------------------------------------------------------------

def floor_entry_count(document_bytes: bytes) -> int:
    """`floor.never_clearable_paths`, counted, from the bytes handed in.

    Deliberately NOT `len(re.findall(...))` over the block: the count the pin
    declares is the count of DECLARED ENTRIES, which is the eight hand-reasoned
    paths plus the generated block, and only the parser knows where one ends.
    """
    document = yaml.safe_load(document_bytes.decode("utf-8"))
    if not isinstance(document, dict):
        raise ValueError("the floor document is not a YAML mapping")
    floor = document.get("floor")
    if not isinstance(floor, dict):
        raise ValueError("the floor document declares no `floor` mapping")
    entries = floor.get("never_clearable_paths")
    if not isinstance(entries, list) or not entries:
        raise ValueError(
            "the floor document declares no non-empty `never_clearable_paths`")
    return len(entries)


def generated_at_of(document_bytes: bytes) -> str | None:
    match = GENERATED_AT_RE.search(document_bytes.decode("utf-8"))
    return match.group(1) if match else None


BLOCK_BEGIN_RE = re.compile(
    r"^\s*#\s*=+\s*BEGIN MACHINE-GENERATED BLOCK.*$", re.MULTILINE)
BLOCK_END_RE = re.compile(
    r"^\s*#\s*=+\s*END MACHINE-GENERATED BLOCK.*$", re.MULTILINE)


def block_entry_count(document_bytes: bytes) -> int | None:
    """How many entries lie BETWEEN the generated block's own markers.

    COUNTED, not read out of the block's `entry_count:` comment. The comment is
    the generator's claim about the block; this is the block. They agree on
    every honest document, and the point of measuring rather than reading is
    that a reviewer is told the number nobody wrote down.
    """
    text = document_bytes.decode("utf-8")
    begin, end = BLOCK_BEGIN_RE.search(text), BLOCK_END_RE.search(text)
    if not begin or not end or end.start() < begin.end():
        return None
    inside = text[begin.end():end.start()]
    return sum(1 for line in inside.splitlines()
               if re.match(r"^\s*- \S", line))


def floor_entries(document_bytes: bytes) -> list[str]:
    document = yaml.safe_load(document_bytes.decode("utf-8"))
    return list(document["floor"]["never_clearable_paths"])


def newly_floored_paths(before_bytes: bytes, after_bytes: bytes) -> list[str]:
    """The paths this advance adds to the floor.

    These are exactly the covered-pending paths the advance is expected to
    clear: a path is covered-pending here BECAUSE it is tracked under the
    floored prefix and the pinned floor does not yet name it, so the set the
    advance clears is the set the new document names and the old one did not.
    Measured by difference; nothing is read from a codexFactory report.
    """
    return sorted(set(floor_entries(after_bytes)) - set(floor_entries(before_bytes)))


def witnesses_of(document_bytes: bytes) -> Witnesses:
    """THE WITNESS FUNCTION (requirement 4).

    Everything it returns is derived from `document_bytes` and from nothing
    else. There is no parameter through which a codexFactory report, a
    pull-request body or an event payload could supply a digest or a count, and
    that absence is the requirement: "a witness restated from the party being
    witnessed is not a witness."
    """
    return Witnesses(sha256=hashlib.sha256(document_bytes).hexdigest(),
                     entry_count=floor_entry_count(document_bytes),
                     generated_at=generated_at_of(document_bytes),
                     block_entry_count=block_entry_count(document_bytes))


def read_site_value(root: pathlib.Path, site: PinnedSite) -> str | None:
    """The value a site currently declares, or None when it does not resolve.

    None covers both "the file is missing" and "the line is not there or is
    there twice". A site that matches twice is UNRESOLVED rather than
    ambiguous-but-usable: two `ref:` lines carrying a commit in one workflow
    would make "which one is the core checkout" a guess, and this lane does not
    guess.
    """
    path = root / site.path
    if not path.is_file():
        return None
    if site.kind == "bytes":
        return hashlib.sha256(path.read_bytes()).hexdigest()
    matches = site.pattern.findall(path.read_text(encoding="utf-8"))
    if len(matches) != 1:
        return None
    return matches[0][1]


def declared_core_commit(root: pathlib.Path) -> str | None:
    return read_site_value(root, PINNED_SITES[0])


# ---------------------------------------------------------------------------
# THE DECISION (requirements 2, 4 and 7), as one pure function.
# ---------------------------------------------------------------------------

def plan_advance(*, current_core: str | None,
                 source_default_branch: str | None,
                 candidate_commit: str | None,
                 candidate_reachable: bool | None,
                 reachability_evidence: str,
                 floor_bytes: bytes | None,
                 snapshot_bytes: bytes | None,
                 floor_source_path: str | None = None) -> Outcome:
    """Decide, from measurements alone, whether an advance is owed.

    THE ORDER OF THE REFUSALS IS THE POINT. Landedness is checked BEFORE the
    documents are compared, so a run that would otherwise have found a
    disagreement still refuses at a non-landed candidate rather than reporting
    an advance it must then throw away — the refusal a reviewer needs to see is
    the FIRST thing that was wrong, not the last.
    """
    if current_core is None or not SHA40_RE.match(current_core):
        return Refusal(
            "pin_unreadable",
            f"`{PIN_FILE}` does not declare exactly one 40-hex `core_commit`; "
            "the lane will not guess which commit this repository is pinned to")

    if not source_default_branch:
        return Refusal(
            "source_default_branch_unresolved",
            f"the default branch of {SOURCE_REPOSITORY} could not be resolved "
            "on this run. The lane refuses rather than pinning at any other "
            "reference")

    if candidate_commit is None or not SHA40_RE.match(candidate_commit or ""):
        return Refusal(
            "source_commit_unresolved",
            f"no 40-hex commit was resolved from "
            f"{SOURCE_REPOSITORY}@{source_default_branch}")

    if candidate_reachable is not True:
        return Refusal(
            "source_commit_not_landed",
            f"{candidate_commit} is not reachable from "
            f"{SOURCE_REPOSITORY}@{source_default_branch}. A pin at a commit "
            "that the default branch does not carry becomes unresolvable the "
            "moment its branch is deleted, and this repository has already "
            "measured that failure on its own history "
            f"(`{PIN_FILE}` lines 375-382). No site is changed")

    if floor_bytes is None:
        # EVERY CANDIDATE IS NAMED, not just the first. The refusal fires only
        # when NONE of the declared paths resolved, so a reader must be able to
        # see the whole set that was tried without going to the workflow — and a
        # migration that has gone wrong in BOTH directions reads as one refusal
        # rather than as a puzzle about which path was meant.
        tried = ", ".join(f"`{c}`" for c in FLOOR_IN_SOURCE_CANDIDATES)
        return Refusal(
            "floor_document_unobtainable",
            f"the authoritative floor document could not be obtained from "
            f"{SOURCE_REPOSITORY}@{candidate_commit} at any declared path "
            f"({tried}). The lane resolves ONLY these paths, in this order, and "
            "never searches for the document. The other four sites are "
            "NOT advanced without it: an advance carrying a stale witness is "
            "worse than no advance")

    if snapshot_bytes is None:
        return Refusal(
            "vendored_snapshot_missing",
            f"`{SNAPSHOT_FILE}` is not on disk; there is nothing to compare "
            "the authoritative document against")

    # THE OBTAINED PATH IS VALIDATED, NOT ECHOED. It arrives from the workflow
    # as a string and is written into the witness lines, the pull-request body
    # and the repeat commands a reviewer runs — so an unnoticed mis-wiring
    # would put a path this lane never resolves in front of the one person
    # checking it. It must be one of the DECLARED candidates: anything else is
    # refused rather than reported, on the same fail-closed footing as the
    # absent document below.
    if floor_source_path and floor_source_path not in FLOOR_IN_SOURCE_CANDIDATES:
        declared = ", ".join(f"`{c}`" for c in FLOOR_IN_SOURCE_CANDIDATES)
        return Refusal(
            "floor_source_path_undeclared",
            f"the lane reported obtaining the floor document from "
            f"`{floor_source_path}`, which is not one of the declared "
            f"candidates ({declared}). A witness naming a path this lane does "
            "not resolve is worse than no witness, and the lane never searches "
            "beyond the declared list, so this is a wiring fault and not a "
            "relocation. No site is changed")

    obtained = floor_source_path or FLOOR_IN_SOURCE

    if floor_bytes == snapshot_bytes:
        return NoOp(
            f"nothing is owed: `{SNAPSHOT_FILE}` is byte-identical to "
            f"`{obtained}` at "
            f"{SOURCE_REPOSITORY}@{source_default_branch} ({candidate_commit}); "
            f"the pin stays at {current_core}")

    return Advance(candidate_commit=candidate_commit,
                   core_before=current_core,
                   source_default_branch=source_default_branch,
                   reachability_evidence=reachability_evidence,
                   floor_source_path=obtained,
                   before=witnesses_of(snapshot_bytes),
                   after=witnesses_of(floor_bytes),
                   clears=tuple(newly_floored_paths(snapshot_bytes,
                                                    floor_bytes)))


# ---------------------------------------------------------------------------
# THE WRITE (requirement 3), and the RE-READ that is the only proof it happened.
# ---------------------------------------------------------------------------

def rewrite_site(text: str, site: PinnedSite, new_value: str) -> tuple[str, int]:
    """Replace a site's value in `text`, reporting how many lines it matched.

    The caller requires the count to be exactly 1. Zero means the site moved or
    was renamed; more than one means the pattern reaches somewhere it was not
    meant to. Either way the advance is discarded rather than guessed at.
    """
    matched = 0

    def _sub(match: re.Match) -> str:
        nonlocal matched
        matched += 1
        return f"{match.group(1)}{new_value}{match.group(3)}"

    return site.pattern.sub(_sub, text), matched


def apply_advance(root: pathlib.Path, advance: Advance,
                  floor_bytes: bytes) -> list[str]:
    """Write all five sites. Returns the labels of sites that did NOT match.

    A non-empty return means the caller must discard the whole run: this
    function makes no attempt to roll back, because a lane that repaired its own
    half-written tree would be deciding which half was right.
    """
    unmatched: list[str] = []

    for site in PINNED_SITES:
        if site.kind == "bytes":
            (root / site.path).write_bytes(floor_bytes)
            continue
        path = root / site.path
        text = path.read_text(encoding="utf-8")
        rewritten, matched = rewrite_site(text, site, advance.candidate_commit)
        if matched != 1:
            unmatched.append(f"{site.label} (matched {matched} line(s), wanted 1)")
            continue
        path.write_text(rewritten, encoding="utf-8")

    pin_path = root / PIN_FILE
    pin_text = pin_path.read_text(encoding="utf-8")
    for site, value in ((SNAPSHOT_WITNESS_SITES[0], advance.after.sha256),
                        (SNAPSHOT_WITNESS_SITES[1], str(advance.after.entry_count))):
        pin_text, matched = rewrite_site(pin_text, site, value)
        if matched != 1:
            unmatched.append(f"{site.label} (matched {matched} line(s), wanted 1)")
    pin_path.write_text(pin_text, encoding="utf-8")

    return unmatched


def verify_advance(root: pathlib.Path, advance: Advance) -> list[str]:
    """RE-READ every site from disk (decision M-2). Returns what did not move.

    This is the function the packet is about. The hand path verified the five
    sites "by reading it back rather than by trusting the edit" and recorded
    that it had; an unattended author cannot record a practice, so the practice
    becomes code and the code is what the tests drive.

    It re-reads from DISK on purpose. Checking the in-memory strings the writer
    produced would prove the substitution ran, which is not the claim: the claim
    is that the FILE now says the new commit.
    """
    unmoved: list[str] = []
    for site in PINNED_SITES:
        actual = read_site_value(root, site)
        expected = (advance.after.sha256 if site.kind == "bytes"
                    else advance.candidate_commit)
        if actual != expected:
            unmoved.append(f"{site.label} reads {actual!r}, wanted {expected!r}")
    for site, expected in ((SNAPSHOT_WITNESS_SITES[0], advance.after.sha256),
                           (SNAPSHOT_WITNESS_SITES[1],
                            str(advance.after.entry_count))):
        actual = read_site_value(root, site)
        if actual != expected:
            unmoved.append(f"{site.label} reads {actual!r}, wanted {expected!r}")
    return unmoved


# ---------------------------------------------------------------------------
# IDEMPOTENCE (requirement 7).
# ---------------------------------------------------------------------------

BOT_BRANCH = "bot/review-lane-repin"


def decide_idempotent_action(open_pull_requests: list[dict]) -> dict:
    """At most one automated advance is open, and a firing updates it.

    `open_pull_requests` is what `gh pr list --head <BOT_BRANCH> --state open
    --json number,headRefName` returns: a list, possibly empty, of the lane's
    OWN pull requests. A firing that finds one brings it up to date; it never
    opens a second, and it never touches a pull request opened from any other
    branch.
    """
    mine = [pr for pr in open_pull_requests
            if pr.get("headRefName") == BOT_BRANCH]
    if not mine:
        return {"action": "open", "number": None}
    mine.sort(key=lambda pr: pr.get("number") or 0)
    return {"action": "update", "number": mine[0].get("number")}


# ---------------------------------------------------------------------------
# THE WITNESSES A REVIEWER NEEDS (requirement 6).
# ---------------------------------------------------------------------------

def render_pr_body(advance: Advance, *, run_url: str,
                   lane_line: str = "Lane: review-lane-repin-bot") -> str:
    """Every value a reviewer would otherwise have to recompute.

    NOTHING IN HERE IS A CLAIM ONLY THE LANE COULD MAKE. Each row is either a
    commit id both repositories carry, or a digest/count computed from bytes
    that are named alongside it, so the whole body is re-derivable by a second
    party with `gh api` and `sha256sum`. That is requirement 6's third
    scenario, and it is why the body carries no "the lane verified…" sentence:
    a lane's report of its own diligence is exactly the value a reviewer cannot
    check.
    """
    before, after = advance.before, advance.after
    lines = [
        lane_line,
        "",
        "**AUTOMATED PIN ADVANCE — proposal only. This lane never merges and "
        "never approves.**",
        "",
        f"Advances the pinned decision core from `{advance.core_before}` to "
        f"`{advance.candidate_commit}`, moving all five sites in one commit.",
        "",
        "| witness | before | after |",
        "|---|---|---|",
        f"| `{PIN_FILE}` `core_commit` | `{advance.core_before}` | "
        f"`{advance.candidate_commit}` |",
        f"| `{MERGE_MASTER_WORKFLOW}` `PINNED_CORE_COMMIT` | "
        f"`{advance.core_before}` | `{advance.candidate_commit}` |",
        f"| `{MERGE_MASTER_WORKFLOW}` core checkout `ref:` | "
        f"`{advance.core_before}` | `{advance.candidate_commit}` |",
        f"| `{PYTEST_SUITE_WORKFLOW}` core checkout `ref:` | "
        f"`{advance.core_before}` | `{advance.candidate_commit}` |",
        f"| `{SNAPSHOT_FILE}` `sha256` | `{before.sha256}` | `{after.sha256}` |",
        f"| `{SNAPSHOT_FILE}` `entry_count` | {before.entry_count} | "
        f"{after.entry_count} |",
        f"| generated block `generated_at` | `{before.generated_at}` | "
        f"`{after.generated_at}` |",
        f"| generated block entries (counted between the markers) | "
        f"{before.block_entry_count} | {after.block_entry_count} |",
        f"| floor total (declared `never_clearable_paths`) | "
        f"{before.entry_count} | {after.entry_count} |",
        "",
        f"## Covered-pending paths this advance is expected to clear: "
        f"{len(advance.clears)}",
        "",
        *([f"- `{path}`" for path in advance.clears]
          or ["_None: this advance changes the floor document without adding "
              "a floored path._"]),
        "",
        "## How the pinned commit was resolved, and how its landedness was "
        "verified",
        "",
        f"- Source repository: `{SOURCE_REPOSITORY}`, default branch "
        f"`{advance.source_default_branch}`, resolved at run time by this lane "
        "— **not** taken from any event payload.",
        f"- {advance.reachability_evidence}",
        f"- The vendored snapshot is a BYTE COPY of "
        f"`{advance.floor_source_path}` at "
        f"`{advance.candidate_commit}`; its `sha256` and `entry_count` above "
        "are computed from the bytes written to it, not carried across from "
        "codexFactory.",
        "",
        "Repeat the verification:",
        "",
        "```",
        f"gh api repos/{SOURCE_REPOSITORY} --jq .default_branch",
        f"gh api repos/{SOURCE_REPOSITORY}/compare/"
        f"{advance.source_default_branch}...{advance.candidate_commit} "
        "--jq .status",
        f"gh api repos/{SOURCE_REPOSITORY}/contents/"
        f"{advance.floor_source_path}"
        f"?ref={advance.candidate_commit} "
        "-H 'Accept: application/vnd.github.raw' | sha256sum",
        "```",
        "",
        f"Run: {run_url}",
        "",
        "This pull request is judged by the same freshness checks that judge a "
        "hand-authored advance, with no exemption of any kind.",
    ]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# CLI.
# ---------------------------------------------------------------------------

def _read_optional_bytes(path: str | None) -> bytes | None:
    if not path:
        return None
    candidate = pathlib.Path(path)
    return candidate.read_bytes() if candidate.is_file() else None


def _tri_state(value: str | None) -> bool | None:
    if value is None:
        return None
    lowered = value.strip().lower()
    if lowered in {"true", "yes", "1"}:
        return True
    if lowered in {"false", "no", "0"}:
        return False
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".",
                        help="this repository's checkout")
    parser.add_argument("--source-default-branch", default=None,
                        help="codexFactory's default branch, resolved by the "
                             "caller at run time")
    parser.add_argument("--candidate-commit", default=None,
                        help="the commit that resolution named")
    parser.add_argument("--candidate-reachable", default=None,
                        help="true|false — whether the caller VERIFIED the "
                             "candidate is reachable from the default branch")
    parser.add_argument("--reachability-evidence", default="",
                        help="how the caller verified it, quoted into the body")
    parser.add_argument("--floor-document", default=None,
                        help="a file holding the authoritative floor "
                             "document's bytes at the candidate commit")
    parser.add_argument("--floor-source-path", default=None,
                        help="the candidate path the floor document was "
                             "actually obtained from, for the witness lines. "
                             "Absent means the path in force")
    parser.add_argument("--run-url", default="")
    parser.add_argument("--plan-out", default=None)
    parser.add_argument("--body-out", default=None)
    parser.add_argument("--write", action="store_true",
                        help="perform the advance in the checkout. Without it "
                             "the lane measures and reports and writes nothing")
    args = parser.parse_args(argv)

    root = pathlib.Path(args.repo).resolve()
    floor_bytes = _read_optional_bytes(args.floor_document)
    snapshot_path = root / SNAPSHOT_FILE
    snapshot_bytes = (snapshot_path.read_bytes()
                      if snapshot_path.is_file() else None)

    outcome = plan_advance(
        current_core=declared_core_commit(root),
        source_default_branch=args.source_default_branch,
        candidate_commit=args.candidate_commit,
        candidate_reachable=_tri_state(args.candidate_reachable),
        reachability_evidence=args.reachability_evidence,
        floor_bytes=floor_bytes,
        snapshot_bytes=snapshot_bytes,
        floor_source_path=args.floor_source_path)

    payload = outcome.as_dict()

    if isinstance(outcome, Advance) and args.write:
        assert floor_bytes is not None
        unmatched = apply_advance(root, outcome, floor_bytes)
        unmoved = verify_advance(root, outcome) if not unmatched else []
        failures = unmatched + unmoved
        if failures:
            outcome = Refusal(
                "partial_advance_discarded",
                "the advance did not reach every pinned site, so the whole run "
                "is discarded and no pull request is opened. Sites that did "
                "not move: " + "; ".join(failures))
            payload = outcome.as_dict()
        else:
            payload["written"] = list(WRITABLE_PATHS)
            payload["verified"] = [site.label for site in PINNED_SITES] + \
                [site.label for site in SNAPSHOT_WITNESS_SITES]

    if args.plan_out:
        pathlib.Path(args.plan_out).write_text(
            json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    if isinstance(outcome, Advance) and args.body_out:
        pathlib.Path(args.body_out).write_text(
            render_pr_body(outcome, run_url=args.run_url), encoding="utf-8")

    print(json.dumps(payload, indent=2))
    if isinstance(outcome, Refusal):
        print(f"::error title=review-lane-repin::refused at stage "
              f"{outcome.stage}: {outcome.reason}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
