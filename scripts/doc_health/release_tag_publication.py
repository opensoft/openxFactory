"""The release-tag publication family (`add-release-tag-publication-check`).

WHAT IT ANSWERS. `docs/contract-versioning-policy.md` holds that "a bundle is
not published until its tag exists" and that "the tag SHALL point to that
realized commit". Nothing checked either. No workflow calls the release
validator; `verify_tag` is exercised only by unit tests over synthetic
repositories; `release-surface-integrity` deliberately does not anchor on tags
so its own drift obligation stays evaluable in the window before one exists; and
`tag-hygiene` is `document-lifecycle`'s PROSE-tag grammar over document text,
which is the trap in its name. The declaring commit and the published tag are
two acts by two actors with nothing joining them.

THE CLASS IS NOT HYPOTHETICAL — IT HAPPENED TWICE, and both catches were human.
`contract-v1.33`, `contract-v1.35` and `contract-v1.39` went untagged for weeks
and were discharged only on a ruling of 2026-08-25. `contract-v2.3` and
`contract-v2.4` repeated it on 2026-08-30/31, and the cut that landed the second
wrote a careful disposition subsection for the FIRST one's missing tag while
standing in the same gap — which is what a process with no place to notice looks
like.

WHY DISTANCE AND NOT TIME. The interval between declaring a bundle and tagging
it is legitimate: a cut declares, the owner tags afterwards. A family that fired
on the declaration would redden every correct release, and a family nobody can
leave green gets configured away. Distance is counted in FIRST-PARENT COMMITS ON
PUBLISHED `main`, never wall time, because landings are what the policy's own
retro-publication rule counts and wall time punishes a quiet week.

WHY THE TWO FAILURES ARE DIFFERENT FINDINGS. An ABSENT tag is an incomplete
release. A tag that peels to a commit NOT declaring the bundle is MISPLACED: it
satisfies every check that asks only whether a tag exists, it is what consumers
pin, and it is worse than absence because it looks like completion. Reported
alike, the common one would hide the serious one.

WHAT THIS FAMILY DOES NOT PROVE, disclosed rather than hidden (proposal D4). The
policy's target is "the EARLIEST FIRST-PARENT COMMIT on published `main` that
DECLARES the bundle and at which `verify-commit` PASSES". The second conjunct is
a digest verification per candidate and is out of scope here, so a tag on a
LATER declaring commit passes this family and remains a defect under the policy.

NOT BUILT ON `verify_tag`, deliberately (proposal D5). That helper cannot
distinguish "I have not fetched" from "this tag is unreachable from `main`":
`git merge-base --is-ancestor` exits 128 when an argument is not a commit in the
local object store and that is folded in with the genuine negative (#338).
Observed live, it fails identically on `contract-v2.2`, whose tag is correct. A
family built on it would report the benign case in the serious case's words.

THE THIRD STATE — SPENT (`declare-spent-bundle-state`, ratified 2026-09-02;
openxFactory issue #575). Between *published* and *owes a tag* sits a number
that was cut, was never publishable, and never will be: `contract-v2.6`, whose
one first-parent declaring commit fails `verify-commit` five ways and which
declares change class ADDITIVE over a tree that refuses three shapes
`contract-v2.5` accepted. The action the SUPERSEDED finding prescribes —
retro-publication — is UNPERFORMABLE for it by anyone, and a finding whose only
prescribed action cannot be taken is one a reader learns to skip.

SILENCE IS NEVER A DECLARATION, and that sentence carries the whole of this
state's fail-closed character. A superseded untagged bundle no declaration names
reads exactly as it did before this state existed, at `error` and in the same
words. The state is entered ONLY by an explicit reserved-form line in
`contracts/CHANGELOG.md` at the PUBLISHED TIP, written inside the changelog entry
of the bundle that superseded it — so the declaring act is the LATER CUT that
allocates the replacement, and a bundle can never declare itself spent.

AND THE SUCCESSOR GUARD IS WHAT MAKES IT UNABUSABLE (ruled by Brett Heap,
2026-09-02). A declaration is quiet only where the superseding bundle it names is
itself CUT, itself PUBLISHED, and STRICTLY LATER — so the only way to retire a
number is to publish its replacement's tag, which is the very act this family
exists to compel. Cut but unpublished is PROVISIONAL: one `warning`, and the
superseded `error` is suppressed in its favour, because the successor is the
bundle the manifest now declares and is graded by the distance arm on its own
account. Never cut, not later, malformed, duplicated, in the wrong entry, or
naming the live bundle: `error`, accepting nothing, with the superseded `error`
standing alongside so a bad declaration removes nothing.

WHY THE FINDINGS OF THIS STATE LEAVE `contracts/manifest.yaml`. A finding's
identity is `(family, repo, path)` and ignores its rule text. Every other finding
here lands on the manifest, so a spent state landed there would share an identity
with all of them and its disappearance would be masked by any surviving sibling;
two bundles declared spent would share `contracts/CHANGELOG.md` for the same
reason. The per-bundle inventory `contracts/releases/<bundle>.digests.yaml` is the
one path unique to the bundle BY CONSTRUCTION — it is the artifact whose existence
made the bundle enumerable in `cut_bundles` at all. ONE finding has no such path
to land on and keeps the changelog: a declaration whose SUBJECT was never cut
disposes nothing.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from . import ERROR, INFO, WARNING, Finding, Skip

FAMILY = "release-tag-publication"
MANIFEST = "contracts/manifest.yaml"
RELEASES = "contracts/releases"

# THE SPENT STATE'S RECORD, and the only document it is read from
# (`declare-spent-bundle-state` OD-1). Three facts pick it: it is a member of
# every release digest inventory, so the record travels with the bundle a
# consumer pins; it is one of the THREE EDITORIAL MEMBERS the versioning policy
# allows to move between cuts, so a disposition can be written when the fact
# arises rather than waiting for a bundle that may never be cut; and it is
# already where this estate records supersessions. NOT `health/dispositions.yaml`
# — that file keys on `(family, repo, path)`, so one row would suppress every
# finding this family could ever raise about a repository, and it lives at the
# aggregation root where a `--single-repo` self-gate cannot see it at all.
CHANGELOG = "contracts/CHANGELOG.md"

# Mandatory publication begins at contract-v1.7; contract-v1.0 through v1.6 are
# an explicitly recovered legacy sequence and carry no tags BY DESIGN, per the
# changelog's own baseline note. Reporting them would emit seven permanent
# findings nobody may act on, which is how a report teaches its readers to stop
# reading it.
ENFORCEMENT_FLOOR = (1, 7)

# RULED BY BRETT HEAP, 2026-08-31: five first-parent landings. The calibration
# it answers to: `contract-v2.3` sat untagged across SIX first-parent landings
# before a human noticed, so any threshold above five would have stayed silent
# through the recurrence this family exists to catch.
DEFAULT_THRESHOLD = 5

_BUNDLE = re.compile(r"^contract_bundle_version:\s*(\S+)\s*$", re.M)
_VERSION = re.compile(r"^contract-v(\d+)\.(\d+)$")

_SUPERSEDED_ACTION = (
    "publish the annotated tag retrospectively at the commit the versioning "
    "policy's rule identifies — RETRO-PUBLISHED, NOT RE-DATED, as the "
    "2026-08-25 discharge did for contract-v1.33, v1.35 and v1.39")
_ABSENT_ACTION = (
    "publish the annotated tag at the commit the versioning policy's rule "
    "identifies — the earliest first-parent commit on published main that "
    "declares the bundle and at which verify-commit passes — never edit the "
    "manifest, the changelog or the inventory to match the absence")
_MISPLACED_ACTION = (
    "re-point the annotated tag at a commit that declares this bundle, or "
    "withdraw it; a tag on a commit declaring something else is what "
    "consumers will pin")
_LIGHTWEIGHT_ACTION = (
    "replace the lightweight ref with an ANNOTATED tag; the policy requires "
    "one, and a lightweight ref carries no tagger, no date and no message")

# --- the SPENT state's four actions ----------------------------------------
#
# BESIDE the four above rather than folded into them. The absent-tag action
# prescribes publishing a tag; none of these does, because the whole subject of
# this state is a number for which that act is unperformable.
_SPENT_ACCEPTED_ACTION = (
    "no action, and this is NOT the tag obligation having been met — it was "
    "EXTINGUISHED, by an owner act, at the cost of a version number, and the "
    "record says which; the state is permanent, and never edit the manifest, "
    "the changelog or the inventory to stop it being reported")
_SPENT_UNPROVEN_ACTION = (
    "publish the SUPERSEDING bundle's annotated tag at the commit the "
    "versioning policy's rule identifies; a bundle is not published until its "
    "tag exists, so until then this supersession is a claim and not evidence — "
    "and the superseding bundle is graded on its own account meanwhile")
_SPENT_REFUSED_ACTION = (
    "repair the SPENT declaration in contracts/CHANGELOG.md or withdraw it — "
    "one reserved-form line, inside the superseding bundle's own entry, naming "
    "a cut, published and STRICTLY LATER bundle, its cause, the ruling's author "
    "and date, and the measurement of record; the superseded bundle stays "
    "reported until a declaration is ACCEPTED, and never edit the manifest, the "
    "changelog or the inventory to match the absence")
_SPENT_ORPHAN_ACTION = (
    "correct the SUBJECT of the SPENT declaration in contracts/CHANGELOG.md: as "
    "written it names a bundle this repository never cut, so it disposes "
    "nothing, and the bundle it was meant to name is still reported by this "
    "family")


def parse_bundle(manifest: bytes | str | None) -> str | None:
    """The declared bundle, or None where the manifest does not declare one.

    ACCEPTS BYTES, because `blobs_at` answers raw Git blob bytes — the release
    inventory's identity rule is computed over them and naming text
    canonicalization an invalid digest source, so the shared reader hands every
    caller bytes. A version string is the one thing in that file it is safe to
    decode, and decoding with `replace` keeps a mis-encoded byte elsewhere in
    the manifest from turning a readable declaration into a crash.
    """
    if not manifest:
        return None
    if isinstance(manifest, bytes):
        manifest = manifest.decode("utf-8", errors="replace")
    found = _BUNDLE.search(manifest)
    return found.group(1) if found else None


def inventory_path(bundle: str) -> str:
    """The release inventory that made `bundle` enumerable, which is where every
    finding of the SPENT state lands but one. Unique to the bundle BY
    CONSTRUCTION, which is the whole of OD-5's argument."""
    return f"{RELEASES}/{bundle}.digests.yaml"


# --- the SPENT declaration reader -------------------------------------------
#
# THE RESERVED OPENER. No other text in `contracts/CHANGELOG.md` may begin a
# line with it, and a line that begins with it and does not complete the form is
# a MALFORMED DECLARATION rather than prose to be ignored — which is why the
# reader below REPORTS what it could not read instead of skipping the line. The
# form, whole:
#
#     **SPENT BUNDLE:** `<bundle>` — SUPERSEDED BY `<superseding bundle>` — CAUSE: <text> — RULED BY <author>, <YYYY-MM-DD> — MEASUREMENT: <citation>
#
# A HANDLE ON THE RECORD AND NOT A SECOND RECORD: it is written INSIDE the human
# disposition subsection the cut writes anyway, in the pattern
# `document-lifecycle`'s reserved `Modified over` marker already sets.
SPENT_OPENER = "**SPENT BUNDLE:**"

# The containing entry. `contracts/CHANGELOG.md`'s bundle entries are `##`
# headings whose first token is the bundle name; the declaring act is the
# SUPERSEDING bundle's own entry, so this is what decides whether a declaration
# was written by the cut that allocated the replacement or by somebody else.
_ENTRY_HEADING = re.compile(r"^##\s+(contract-v\d+\.\d+)")

_SUBJECT_PROBE = re.compile(re.escape(SPENT_OPENER) + r"\s*`([^`]+)`")
_RULING_PROBE = re.compile(r"^(?P<author>.+?),\s*(?P<ruled_on>\d{4}-\d{2}-\d{2})$")
_RULING_DATE = re.compile(r"(\d{4}-\d{2}-\d{2})\s*$")

# READ BY LABEL, IN ORDER, AND NOT BY SPLITTING ON THE SEPARATOR. Splitting a
# line on " — " would misread any declaration whose CAUSE carries an em dash —
# and would then name the WRONG element as the missing one, handing an author the
# wrong repair for a defect that is right there. Each label is found from the end
# of the one before it, so the order the form states is enforced by the search
# itself, and each element's value runs to the next label that was actually
# found.
_SUPERSEDING_LABEL = " — SUPERSEDED BY "
_CAUSE_LABEL = " — CAUSE: "
_RULED_LABEL = " — RULED BY "
_MEASUREMENT_LABEL = " — MEASUREMENT: "
_LABELS = (
    (_SUPERSEDING_LABEL, "the superseding bundle"),
    (_CAUSE_LABEL, "the cause"),
    (_RULED_LABEL, "the ruling"),
    (_MEASUREMENT_LABEL, "the measurement of record"),
)


@dataclass(frozen=True)
class SpentDeclaration:
    """One line of the reserved form, read for PRESENCE and never for truth.

    The family verifies that each element is present and non-empty, and verifies
    the superseding bundle MECHANICALLY. It does NOT and CANNOT verify that a
    cited ruling was really made, and that residue is disclosed rather than
    hidden: what makes the state safe is the successor guard, which cannot be
    satisfied by writing anything.
    """

    subject: str | None
    superseding: str | None
    cause: str | None
    author: str | None
    ruled_on: str | None
    measurement: str | None
    entry: str | None
    missing: tuple[str, ...]
    line: int

    def owed_elements_present(self) -> bool:
        return not self.missing


def _read_elements(line: str) -> tuple[dict[str, str], tuple[str, ...]]:
    """`({label: value}, missing element names)` for one candidate line."""
    found: dict[str, int] = {}
    pos = 0
    for label, _ in _LABELS:
        idx = line.find(label, pos)
        if idx < 0:
            continue
        found[label] = idx
        pos = idx + len(label)
    values: dict[str, str] = {}
    missing: list[str] = []
    labels = [label for label, _ in _LABELS]
    for index, (label, name) in enumerate(_LABELS):
        if label not in found:
            missing.append(name)
            continue
        start = found[label] + len(label)
        end = len(line)
        for later in labels[index + 1:]:
            if later in found:
                end = found[later]
                break
        value = line[start:end].strip()
        if not value:
            missing.append(name)
            continue
        values[label] = value
    return values, tuple(missing)


def parse_spent_declarations(changelog: bytes | str | None
                             ) -> list[SpentDeclaration]:
    """Every line of `contracts/CHANGELOG.md` beginning with the reserved opener.

    ONE PURE FUNCTION FROM BYTES TO DECLARATIONS, taking bytes because
    `blobs_at` answers raw Git blob bytes — the release inventory's identity rule
    is computed over them, so the shared reader hands every caller bytes and
    naming text canonicalization an invalid digest source. Decoded with
    `replace` for the same reason `parse_bundle` is: a mis-encoded byte
    elsewhere in a 4000-line changelog must not turn a readable declaration into
    a crash.

    REJECTS RATHER THAN SKIPS. A line carrying the opener and completing nothing
    is returned WITH its `missing` list rather than dropped, because the opener
    is reserved and a malformed declaration is worse than none: it looks like a
    record.

    NO FENCE TRACKING, deliberately. The requirement reserves the opener over the
    WHOLE document, so a line inside a code block that begins with it is a
    declaration too. That reading is the fail-closed one — it recognizes more
    lines and therefore refuses more of them — and the alternative would let a
    declaration be hidden from the reader by four leading spaces.
    """
    if not changelog:
        return []
    if isinstance(changelog, bytes):
        changelog = changelog.decode("utf-8", errors="replace")
    out: list[SpentDeclaration] = []
    entry: str | None = None
    for number, line in enumerate(changelog.splitlines(), start=1):
        heading = _ENTRY_HEADING.match(line)
        if heading:
            entry = heading.group(1)
            continue
        if not line.startswith(SPENT_OPENER):
            continue
        subject_match = _SUBJECT_PROBE.match(line)
        subject = subject_match.group(1) if subject_match else None
        values, missing = _read_elements(line)
        # THE GAP BETWEEN THE SUBJECT AND THE FIRST LABEL, checked so that junk
        # spliced into the middle of the form is a MALFORMED declaration rather
        # than an accepted one: the form admits exactly the separator there and
        # nothing else. Checked only where both halves were read, because
        # otherwise the missing half is the finding and this would be a second
        # name for it.
        if (subject_match and _SUPERSEDING_LABEL in values
                and not line[subject_match.end():].startswith(
                    _SUPERSEDING_LABEL)):
            missing = missing + ("the reserved form's own shape",)
        superseding = values.get(_SUPERSEDING_LABEL)
        if superseding is not None:
            # A code span, exactly as the subject is. Backticks around an empty
            # name read as the element being absent, which is what it is.
            superseding = superseding.strip("`").strip() or None
            if superseding is None:
                missing = missing + ("the superseding bundle",)
        author = ruled_on = None
        ruling = values.get(_RULED_LABEL)
        if ruling:
            parsed = _RULING_PROBE.match(ruling)
            if parsed:
                author = parsed.group("author").strip() or None
                ruled_on = parsed.group("ruled_on")
            if not (author and ruled_on):
                # THE RULING IS ONE ELEMENT WITH TWO HALVES, and a clause
                # carrying only one of them is named for the half it is MISSING
                # rather than for the element, because the repair for an absent
                # date is not the repair for an absent author. A clause carrying
                # BOTH halves and still not completing the form is named for
                # neither: what is missing there is the separator.
                date = _RULING_DATE.search(ruling)
                named = (ruling[:date.start()] if date else ruling)
                named = named.strip().rstrip(",").strip()
                missing = tuple(m for m in missing if m != "the ruling")
                if not named:
                    missing = missing + ("the ruling's author",)
                if not date:
                    missing = missing + ("the ruling's date",)
                if named and date:
                    missing = missing + ("the ruling's own shape",)
                author = ruled_on = None
        out.append(SpentDeclaration(
            subject=subject,
            superseding=superseding,
            cause=values.get(_CAUSE_LABEL),
            author=author,
            ruled_on=ruled_on,
            measurement=values.get(_MEASUREMENT_LABEL),
            entry=entry,
            missing=missing,
            line=number))
    return out


def version_of(bundle: str | None) -> tuple[int, int] | None:
    """`contract-v2.4` -> (2, 4). None for anything not of that shape, which is
    a bundle name this family cannot compare against the enforcement floor and
    therefore declines to judge."""
    if not bundle:
        return None
    found = _VERSION.match(bundle)
    return (int(found.group(1)), int(found.group(2))) if found else None


def cut_bundles(git, repo_path: Path, tip: str) -> set[str] | None:
    """Every bundle this repository has CUT, from its release inventories.

    WHY NOT JUST THE DECLARED ONE — this is the defect Codex found on PR #544,
    and it is the exact recurrence the family exists for. A bundle is silent
    while its declaring commit is the tip, which is correct; then the NEXT cut
    advances the manifest, and a family that reads only the current declaration
    starts checking the new bundle and never revisits the old one. Run against
    the real incident it would have read ZERO through the whole of it: v2.3
    untagged, v2.4 declared on top, nothing reported.

    An inventory file under `contracts/releases/` is the machine-readable fact
    that a bundle was cut, which is what makes the set enumerable at all.
    """
    paths = git.ls_tree_paths(repo_path, tip, RELEASES)
    if paths is None:
        return None
    bundles = set()
    for path in paths:
        name = path.rsplit("/", 1)[-1]
        if name.endswith(".digests.yaml"):
            bundles.add(name[: -len(".digests.yaml")])
    return bundles


def _finding(sev, repo, rule, action, resolution="auto-fixable", path=MANIFEST):
    return Finding(sev, FAMILY, repo, path, rule, action,
                   resolution=resolution)


# --- the SPENT ladder --------------------------------------------------------
#
# ORDERED, AND EXACTLY ONE STATE PER DECLARATION. Each return below excludes
# every state under it, so one declaration yields at most one finding and a
# reader is never handed a choice between two true descriptions of one defect.
# The order is the requirement's own: what the line IS before what it SAYS
# (unreadable, orphan, duplicated, the live bundle), then whether it is well
# formed, then where it sits, then the successor guard's two halves.
def _declaration_state(decl: SpentDeclaration, count: int, cut: set[str],
                       declared: str) -> tuple[str, str] | None:
    """`(code, why)` for a declaration this family refuses, or None where it is
    well formed, correctly placed, and names a cut and STRICTLY LATER
    superseding bundle. None is NOT yet acceptance — publication of that
    successor is read afterwards, against the refs."""
    if decl.subject is None:
        return ("unreadable", "the line carries the reserved opener and no "
                              "readable subject, so it names no bundle at all")
    if decl.subject not in cut:
        return ("orphan-subject",
                f"this repository holds no release inventory for "
                f"{decl.subject}, so the declaration disposes nothing")
    if count > 1:
        return ("duplicate",
                f"{count} SPENT declarations name {decl.subject}, and two "
                f"records of one disposition is how they come to disagree")
    if decl.subject == declared:
        # BEFORE THE FORM CHECKS, because it is a fact about WHAT is claimed
        # rather than about HOW: a declaration of the number the manifest still
        # declares is refused whatever its shape, and that bundle goes on being
        # graded by distance exactly as it is today.
        return ("live-bundle",
                f"{decl.subject} is the bundle {MANIFEST} declares at the "
                f"published tip, and a repository declaring a bundle it also "
                f"calls spent asserts two incompatible things about one number")
    if decl.missing:
        return ("malformed",
                "the declaration is missing " + ", ".join(decl.missing))
    if decl.entry != decl.superseding:
        return ("wrong-entry",
                f"the declaration names {decl.superseding} as the superseding "
                f"bundle but sits inside "
                + (f"{decl.entry}'s changelog entry" if decl.entry
                   else "no bundle's changelog entry")
                + ", and the act that spends a number is the LATER CUT that "
                  "allocates its replacement")
    if decl.superseding not in cut:
        return ("successor-never-cut",
                f"this repository holds no release inventory for "
                f"{decl.superseding}, so the declaration retires a number by "
                f"pointing at one that was never cut")
    spent_version, next_version = version_of(decl.subject), version_of(
        decl.superseding)
    if (spent_version is None or next_version is None
            or next_version <= spent_version):
        return ("successor-not-later",
                f"{decl.superseding} is not STRICTLY LATER than {decl.subject}, "
                f"and a tag that already existed before {decl.subject} was cut "
                f"is not a replacement for it — a guard satisfied by an earlier "
                f"release has been walked around backwards rather than met")
    return None


_REFUSAL_SEVERITY = {
    "unreadable": ERROR,
    # A WARNING RATHER THAN AN ERROR, and the one finding of this state with no
    # per-bundle inventory to land on: a mistyped subject leaves the REAL bundle
    # undeclared and still reported at `error` by the scenarios above, which is
    # the fail-closed behaviour a typo must not be able to defeat.
    "orphan-subject": WARNING,
    "duplicate": ERROR,
    "live-bundle": ERROR,
    "malformed": ERROR,
    "wrong-entry": ERROR,
    "successor-never-cut": ERROR,
    "successor-not-later": ERROR,
}


def _refusal_findings(repo: str, decls: list[SpentDeclaration],
                      cut: set[str], declared: str
                      ) -> tuple[list[Finding], dict[str, SpentDeclaration]]:
    """`(findings, {subject: declaration})` for the declarations this run read.

    THE SECOND HALF IS A CANDIDATE SET AND NOT AN ACCEPTED ONE. A declaration
    that survives every check here has said everything it owes; whether the
    bundle it names is actually PUBLISHED is read from the refs afterwards,
    because that is the half nobody can satisfy by writing a sentence.

    THIS PASS RUNS OVER EVERY DECLARATION, whatever the tag state of its
    subject, because these are defects in the RECORD rather than in a bundle's
    publication — a declaration naming the live bundle is two incompatible
    claims about one number whether or not that number happens to be tagged.
    Acceptance, by contrast, reaches the ABSENT-tag arm and nothing else.
    """
    counts: dict[str | None, int] = {}
    for decl in decls:
        counts[decl.subject] = counts.get(decl.subject, 0) + 1
    findings: list[Finding] = []
    candidates: dict[str, SpentDeclaration] = {}
    reported_duplicate: set[str] = set()
    for decl in decls:
        state = _declaration_state(decl, counts[decl.subject], cut, declared)
        if state is None:
            candidates[decl.subject] = decl
            continue
        code, why = state
        if code == "duplicate":
            # ONE finding for the pair, not one per member: the defect is that
            # there are two, and they share a path and would share a rule.
            if decl.subject in reported_duplicate:
                continue
            reported_duplicate.add(decl.subject)
        if code == "unreadable":
            findings.append(_finding(
                _REFUSAL_SEVERITY[code], repo,
                f"a SPENT declaration in {CHANGELOG} (line {decl.line}) is "
                f"MALFORMED: {why} — a line carrying the reserved opener and "
                f"not completing the reserved form is a malformed declaration "
                f"rather than prose to be ignored, and a malformed declaration "
                f"is worse than none because it looks like a record",
                _SPENT_REFUSED_ACTION, path=CHANGELOG))
            continue
        if code == "orphan-subject":
            findings.append(_finding(
                _REFUSAL_SEVERITY[code], repo,
                f"a SPENT declaration in {CHANGELOG} (line {decl.line}) names "
                f"{decl.subject} as the bundle it spends, and {why} — a "
                f"mistyped subject leaves the real bundle undeclared and still "
                f"reported, which is the fail-closed behaviour a typo must not "
                f"defeat",
                _SPENT_ORPHAN_ACTION, path=CHANGELOG))
            continue
        findings.append(_finding(
            _REFUSAL_SEVERITY[code], repo,
            f"{decl.subject}'s SPENT declaration is REFUSED and accepts "
            f"nothing: {why}",
            _SPENT_REFUSED_ACTION, path=inventory_path(decl.subject)))
    return findings, candidates


def distance_from_tip(git, repo_path: Path, bundle: str, tip: str,
                      window: int) -> int | None:
    """First-parent landings on published `main` ABOVE the earliest commit in
    the window that declares `bundle`.

    Bounded on purpose, and the bound is `threshold + 2` for a reason worth
    stating: A LANDING DOES NOT TOUCH THE MANIFEST, so every commit above the
    cut still DECLARES the bundle, and the walk is looking for where the
    declaration STOPS rather than where it starts. A window of `threshold + 1`
    would saturate — "at the threshold" and "far past it" would both come back
    as the window's edge — and the error band would never be reached. With one
    commit of headroom the two are distinguishable, and where the whole window
    declares, the answer is a FLOOR (at least this far) which is all the error
    band needs, since it prints no number. An unbounded walk would read a
    manifest blob per commit over the whole history to answer a question with
    three outcomes.

    Returns None where the walk itself could not be performed, which the caller
    turns into a skip rather than a finding.
    """
    shas = git.first_parent_shas(repo_path, tip, window)
    if not shas:
        return None
    earliest_declaring = None
    for index, sha in enumerate(shas):
        blobs = git.blobs_at(repo_path, sha, [MANIFEST])
        if blobs is None:
            return None
        if parse_bundle(blobs.get(MANIFEST)) == bundle:
            earliest_declaring = index
        else:
            break
    if earliest_declaring is None:
        # The published tip does not declare it. The bundle is declared
        # somewhere this window does not reach, and grading it would be a guess.
        return None
    return earliest_declaring


def _tag_state(git, repo_path: Path, bundle: str):
    """(kind, detail) for one bundle's published tag.

    kind is "unlistable", "absent", "lightweight", "misplaced" or "ok".
    """
    ref = git.tag_ref(repo_path, bundle)
    if ref is None:
        return ("unlistable", None)
    objecttype, peeled = ref
    if objecttype is None:
        return ("absent", None)
    if objecttype != "tag":
        return ("lightweight", None)
    target = git.blobs_at(repo_path, peeled, [MANIFEST])
    if target is None or target.get(MANIFEST) is None:
        # Same conflation guarded at the other read: a tag peeling to a commit
        # this clone has not fetched must not be reported as a tag pointing at
        # a commit that declares nothing.
        return ("unlistable", None)
    declared_there = parse_bundle(target.get(MANIFEST))
    if declared_there == bundle:
        return ("ok", peeled)
    return ("misplaced", (peeled, declared_there))


def check_repo(repo: str, repo_path: Path, git,
               threshold: int = DEFAULT_THRESHOLD):
    """One repository. `Skip` where the question could not be asked, a list of
    findings otherwise — empty when the obligation is met.

    EVERY BUNDLE THIS REPOSITORY HAS CUT IS INSPECTED, not only the one the
    manifest currently declares. The distance grading applies to the CURRENT
    declaration, which is the only one still inside its legitimate window; a
    SUPERSEDED bundle's window closed when the next cut replaced it, so an
    untagged one is unambiguously unpublished and is reported at `error`
    without grading — UNLESS an accepted SPENT declaration names it, which is
    the third state and the only thing that quiets that arm.
    """
    tip = git.remote_main_sha(repo_path)
    if tip is None:
        return Skip(FAMILY, f"{repo}: published main could not be resolved, so "
                            f"no landing distance can be counted")
    blobs = git.blobs_at(repo_path, tip, [MANIFEST, CHANGELOG])
    if blobs is None:
        return Skip(FAMILY, f"{repo}: version control could not be consulted "
                            f"for {MANIFEST}")
    manifest = blobs.get(MANIFEST)
    if manifest is None:
        # NOT "no bundle declared". `blobs_at` answers None PER PATH for a blob
        # it cannot read, and the commonest cause is that the published tip is
        # not in the local object store — a clone that has not fetched it. This
        # is the #338 conflation, and this family repeated it once before this
        # line existed: it reported "no contract bundle declared" against a
        # repository declaring contract-v2.5, because main had advanced past the
        # last fetch. Not fetched is not an answer.
        return Skip(FAMILY, f"{repo}: {MANIFEST} could not be read at the "
                            f"published tip {tip[:9]} — the commit may not be "
                            f"present locally, which is not the same fact as "
                            f"declaring no bundle")
    changelog = blobs.get(CHANGELOG)
    if changelog is None:
        # THE SAME GUARD ONE DOCUMENT OVER, and this family has already been
        # caught by the #338 conflation once. `blobs_at` answers None PER PATH
        # for a blob it cannot read, and the commonest cause is a checkout that
        # has not fetched the published tip. NOT FETCHED IS NOT AN ANSWER — in
        # either direction: the absence of a declaration this run could not look
        # for must never be read as the absence of a declaration, because that
        # reading turns an unfetched clone into an `error` nobody can act on.
        return Skip(FAMILY, f"{repo}: {CHANGELOG} could not be read at the "
                            f"published tip {tip[:9]}, so a SPENT declaration "
                            f"could not be looked for — which is not the same "
                            f"fact as there being none")
    declared = parse_bundle(manifest)
    if declared is None:
        return Skip(FAMILY, f"{repo}: no contract bundle declared")
    if version_of(declared) is None:
        return Skip(FAMILY, f"{repo}: declared bundle {declared!r} is not of "
                            f"the contract-v<major>.<minor> shape this family "
                            f"compares against the enforcement floor")

    cut = cut_bundles(git, repo_path, tip)
    if cut is None:
        return Skip(FAMILY, f"{repo}: the release inventories under "
                            f"{RELEASES}/ could not be listed, so the set of "
                            f"cut bundles is unknown")
    declarations = parse_spent_declarations(changelog)
    findings, candidates = _refusal_findings(repo, declarations, cut, declared)
    for bundle in sorted(cut | {declared}):
        version = version_of(bundle)
        if version is None or version < ENFORCEMENT_FLOOR:
            continue
        kind, detail = _tag_state(git, repo_path, bundle)
        if kind == "unlistable":
            return Skip(FAMILY, f"{repo}: the published refs for {bundle} "
                                f"could not be consulted")
        if kind == "ok":
            continue
        if kind == "lightweight":
            findings.append(_finding(
                ERROR, repo,
                f"the ref named {bundle} is a LIGHTWEIGHT tag, not an "
                f"annotated one, so it does not satisfy the policy's "
                f"requirement",
                _LIGHTWEIGHT_ACTION))
            continue
        if kind == "misplaced":
            peeled, declared_there = detail
            findings.append(_finding(
                ERROR, repo,
                f"{bundle}'s annotated tag is MISPLACED: it peels to "
                f"{peeled[:9]}, which declares "
                + (f"{declared_there}" if declared_there else "no bundle at all")
                + f", not {bundle} — a tag on the wrong commit satisfies every "
                  f"check that asks only whether a tag exists, and it is what "
                  f"consumers pin",
                _MISPLACED_ACTION, resolution="contested"))
            continue

        # absent — AND THE ONLY ARM THE SPENT STATE REACHES. It does not quiet a
        # MISPLACED tag, does not quiet a LIGHTWEIGHT ref, and does not quiet the
        # distance grading of the bundle the manifest currently declares: the
        # branches above have already `continue`d past this point, so the scope
        # rule holds BY CONSTRUCTION rather than by care.
        if bundle != declared:
            decl = candidates.get(bundle)
            if decl is not None:
                kind, _ = _tag_state(git, repo_path, decl.superseding)
                if kind == "unlistable":
                    return Skip(FAMILY,
                                f"{repo}: the published refs for "
                                f"{decl.superseding}, named as {bundle}'s "
                                f"superseding bundle, could not be consulted")
                if kind == "ok":
                    # ACCEPTED. Recorded, never silent — ruled by Brett Heap on
                    # 2026-09-02 on an alternative put to him and declined —
                    # and `contested`, so a spent state that stops being
                    # reported without a cited change is re-raised.
                    findings.append(_finding(
                        INFO, repo,
                        f"{bundle} is declared SPENT: it was cut, has no "
                        f"published annotated tag, and {decl.superseding} — "
                        f"itself cut, itself published and strictly later — "
                        f"superseded it. The record is {CHANGELOG} § "
                        f"{decl.superseding} — RULED BY "
                        f"{decl.author}, {decl.ruled_on}; MEASUREMENT: "
                        f"{decl.measurement}. The tag obligation was not met, "
                        f"it was EXTINGUISHED by an owner act at the cost of a "
                        f"version number",
                        _SPENT_ACCEPTED_ACTION, resolution="contested",
                        path=inventory_path(bundle)))
                    continue
                # PROVISIONAL, not refused: ONE finding and not two. The
                # superseded `error` is SUPPRESSED in favour of this `warning`,
                # which is the ruled outcome for this case, and nothing is lost
                # by the suppression — the successor is the bundle the manifest
                # now declares, so the distance arm grades it on its own
                # account and the obligation has MOVED rather than gone.
                findings.append(_finding(
                    WARNING, repo,
                    f"{bundle} is declared SPENT and the supersession is "
                    f"UNPROVEN: {decl.superseding} has a release inventory and "
                    f"no published annotated tag peeling to a commit that "
                    f"declares it — a bundle is not published until its tag "
                    f"exists, and a successor that is not published cannot yet "
                    f"be shown to have carried anything forward",
                    _SPENT_UNPROVEN_ACTION, path=inventory_path(bundle)))
                continue
            findings.append(_finding(
                ERROR, repo,
                f"{bundle} was cut and SUPERSEDED without ever being "
                f"published: it has a release inventory, the manifest has "
                f"moved on to {declared}, and it has no published annotated "
                f"tag — under the versioning policy it was never released, "
                f"and its window closed when the next cut replaced it",
                _SUPERSEDED_ACTION))
            continue
        distance = distance_from_tip(git, repo_path, bundle, tip, threshold + 2)
        if distance is None:
            return Skip(FAMILY, f"{repo}: the earliest commit declaring "
                                f"{bundle} could not be resolved")
        if distance == 0:
            continue
        if distance <= threshold:
            findings.append(_finding(
                WARNING, repo,
                f"{bundle} is declared and has no published annotated tag, "
                f"{distance} first-parent landing(s) after the commit that "
                f"declared it",
                _ABSENT_ACTION))
        else:
            findings.append(_finding(
                ERROR, repo,
                f"{bundle} is declared and has no published annotated tag "
                f"more than {threshold} first-parent landings after the "
                f"commit that declared it — under the versioning policy it is "
                f"NOT PUBLISHED, and its presence in the manifest is not a "
                f"release",
                _ABSENT_ACTION))
    return findings


def fam_release_tag_publication(ctx):
    """Every repository in scope that declares a contract bundle.

    A PER-REPOSITORY SKIP IS REPORTED, NOT DROPPED, for the reason
    `release-inventory-drift` records for the same shape: the ratified
    obligation is per-repository, most pinned repositories declare no bundle at
    all, and a design that only spoke up when EVERY repository skipped would be
    silent about nearly all of them on every run — which is the "silently
    omitted" the requirement forbids. Each skip contributes an `info`, and the
    family-level `Skip` is kept for the case it genuinely describes: nothing in
    scope was askable at all.
    """
    results: list[Finding] = []
    skips: list[str] = []
    scoped = sorted(ctx.repo_paths.items())
    if not scoped:
        return Skip(FAMILY, "no repository in scope")
    threshold = getattr(ctx, "tag_publication_threshold", DEFAULT_THRESHOLD)
    for repo, repo_path in scoped:
        outcome = check_repo(repo, Path(repo_path), ctx.git, threshold)
        if isinstance(outcome, Skip):
            skips.append(outcome.reason)
            results.append(_finding(
                INFO, repo, f"not checked: {outcome.reason}",
                "no action — this repository's tag obligation was not "
                "evaluated, and the reason is recorded rather than omitted",
                resolution="auto-fixable"))
            continue
        results.extend(outcome)
    if len(skips) == len(scoped):
        return Skip(FAMILY, "; ".join(skips))
    return results
