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

THE THIRD STATE — SPENT (`declare-spent-bundle-state`, ratified 2026-09-02).
Between *published* and *owes a tag* sits a number that was cut, was never
publishable, and never will be: `contract-v2.6`, declared at `bbbbeda9`, never
verifiable there, and superseded by `contract-v3.0`. For such a bundle the
action above is UNPERFORMABLE BY ANYONE, and a finding whose only prescribed
action cannot be taken is one a reader learns to skip.

SILENCE IS NEVER A DECLARATION, and that carries the whole of this state's
fail-closed character. The state is entered ONLY by an explicit reserved line
in `contracts/CHANGELOG.md` AT THE PUBLISHED TIP, read in the same `blobs_at`
call as the manifest and under the same guard. A bundle does not become spent
by being old, ignored, inconvenient, or by any absence whatsoever: where no
declaration names a superseded untagged bundle, this module behaves exactly as
it did before this state existed.

WHY THE CHANGELOG AND NOT `health/dispositions.yaml`. That file suppresses by
`(family, repo, path)` and every finding this family raised before this state
landed passes `MANIFEST`, so one row would suppress every absent-tag,
misplaced-tag and lightweight-ref finding about that repository — including the
next genuinely abandoned bundle. It also lives at the aggregation root, so it is
unreachable from a `--single-repo` run, which is the scope this family's own
self-gate uses. The changelog is on the release surface a consumer pins, is one
of the three EDITORIAL members that may legitimately move between cuts, and is
already where this estate records supersessions.

THE THREE OUTCOMES, AND THE MIDDLE ONE IS NOT A REFUSAL. ACCEPTED (every
element present, the named successor cut, published, and STRICTLY LATER) is one
`info`, classed `contested`, on the spent bundle's OWN release inventory.
PROVISIONAL (well formed, the later successor cut but not yet published) is one
`warning` that SUPPRESSES the superseded `error` for that bundle — one finding,
not two — the obligation having MOVED onto the successor, which the distance arm
grades on its own account. REFUSED is an `error` BESIDE the superseded `error`,
which still stands, because a bad declaration must remove nothing.

WHY THE FINDINGS LAND ON `contracts/releases/<bundle>.digests.yaml`. A
finding's identity here is `(family, repo, path)` and ignores the rule text
(`Finding.match_key`). On `MANIFEST` a spent `info` would share an identity with
every other finding of this family about the repository and its disappearance
would be masked by any surviving sibling; on `contracts/CHANGELOG.md` two spent
bundles would share one identity, which is the same defect one step over (found
by Codex on PR #578). The per-bundle inventory is unique to the bundle BY
CONSTRUCTION — it is the artifact whose existence made the bundle enumerable in
`cut_bundles`. ONE finding of this state has no per-bundle inventory to land on
and keeps the changelog path: a declaration whose SUBJECT is a bundle this
repository never cut disposes nothing.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, replace
from pathlib import Path

from . import ERROR, INFO, WARNING, Finding, Skip

FAMILY = "release-tag-publication"
MANIFEST = "contracts/manifest.yaml"
RELEASES = "contracts/releases"
# The one document a SPENT declaration may be read from, and the reason it is a
# read at the PUBLISHED TIP rather than of the working tree: the declaration
# travels with the bundle a consumer pins, so what a consumer can see is what
# this family reads.
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

# --- the SPENT state's four action constants, beside the four above ---------
#
# FOUR NEW NAMES RATHER THAN REUSES, for the reason the module already applies
# to its severity constants: each of these answers a different act, and a
# shared constant would move all four when one of them was rewritten.
_SPENT_ACTION = (
    "no action is owed on this bundle — the obligation was not MET but "
    "EXTINGUISHED, by an owner act, at the cost of a version number, and the "
    f"record is the reserved SPENT declaration in {CHANGELOG}; NEVER delete "
    "that declaration or this inventory to stop this finding being reported, "
    "which is the one way the state can be made to disappear")
_SPENT_PROVISIONAL_ACTION = (
    "publish the SUPERSEDING bundle's annotated tag at the commit the "
    "versioning policy's rule identifies — until it exists the supersession is "
    "UNPROVEN, and this bundle's obligation has MOVED ONTO THE SUCCESSOR "
    "rather than been discharged")
_SPENT_REFUSED_ACTION = (
    f"repair or withdraw the SPENT declaration in {CHANGELOG} — it is refused, "
    "so it disposes nothing, and the superseded-and-never-published finding on "
    "this bundle stands beside this one because a bad declaration must remove "
    "nothing")
_SPENT_CURRENT_ACTION = (
    f"withdraw the SPENT declaration in {CHANGELOG} — it names the bundle "
    f"{MANIFEST} still DECLARES, which asserts two incompatible things about "
    f"one number; this bundle's own tag obligation is unchanged and is graded "
    f"by landing distance exactly as it was before the declaration was written")
_SPENT_ORPHAN_ACTION = (
    f"correct the SUBJECT of the SPENT declaration in {CHANGELOG} — it names a "
    "bundle this repository never cut, so it disposes nothing, and whichever "
    "bundle actually owes a tag is still reported by this family")

# THE RESERVED OPENER. No other line in `contracts/CHANGELOG.md` may BEGIN with
# it, and a line that does begin with it and does not complete the form is a
# MALFORMED DECLARATION rather than prose to be ignored — which is what makes
# the state readable at all: a family that fell back to "not a declaration"
# would let a typo in the record read as no record.
SPENT_OPENER = "**SPENT BUNDLE:**"
# The element separator, and it is RESERVED WITHIN THE LINE. A CAUSE or a
# MEASUREMENT that contains it splits the line into a segment this reader does
# not recognize, and that is reported as malformed rather than guessed at — the
# alternative is a family whose reading of a record depends on the record's
# punctuation.
_SPENT_SEP = re.compile(r"\s+—\s+")
_SPENT_SUBJECT = re.compile(r"^\s+`([^`]*)`(?=(?:\s|$))")
# TWO PATTERNS, NOT ONE, AND THE SECOND IS THE ONE THAT MAKES CONTAINMENT
# SOUND — found by Codex on PR #584 as a P1. A LEVEL-TWO heading ENDS whatever
# entry was open, whether or not it opens a new one; only a heading naming a
# bundle OPENS an entry. With one pattern, `## contract-v3.0` … `## Notes` …
# declaration left `entry` reading `contract-v3.0` for a line that is not in
# that entry at all, so the containment rule could ACCEPT a declaration sitting
# outside its successor's entry — which is the guard, not a detail of it.
# `(?!#)` keeps a `### subsection` from closing the entry it lives inside,
# which matters because the reserved line is written INSIDE one.
_LEVEL_TWO_HEADING = re.compile(r"^##(?!#)\s")
# THE VERSION TOKEN MUST BE COMPLETE, AND `\b` IS NOT THAT TEST — found by
# Codex on PR #584 as a SECOND P1, on the fix for the first. `\b` matches
# between `0` and `.`, so `## contract-v3.0.1` and `## contract-v3.0-notes`
# both OPENED an entry named `contract-v3.0`, and a declaration below either
# would have been contained by an entry that is not the one it names. The
# lookahead demands whitespace or end-of-line, so the captured token is the
# WHOLE bundle name rather than a prefix of a longer one.
_ENTRY_HEADING = re.compile(r"^##(?!#)\s+(contract-v\d+\.\d+)(?=\s|$)")
_RULED_BY = re.compile(r"^(?P<author>.*?),\s*(?P<date>\d{4}-\d{2}-\d{2})\s*$")

# The four elements owed, in the order the reserved form writes them. The KEY
# is the segment's literal prefix; the VALUE is the element's name as a finding
# reports it, because "which element is missing" is what the scenario asks the
# finding to say.
_SPENT_ELEMENTS = (
    ("SUPERSEDED BY", "superseding bundle"),
    ("CAUSE:", "cause"),
    ("RULED BY", "ruling"),
    ("MEASUREMENT:", "measurement of record"),
)


@dataclass(frozen=True)
class SpentDeclaration:
    """One reserved SPENT line, as READ — never as judged.

    The reader's whole job is to say what the line contains and what it is
    missing. Every acceptance question — is the successor cut, is it published,
    is it later, is it the entry that contains the line — is asked by
    `spent_refusal` and by `check_repo`, so the parse is testable without a
    repository and the judgment is testable without a parser.
    """
    subject: str | None
    entry: str | None
    superseding: str | None
    cause: str | None
    author: str | None
    date: str | None
    measurement: str | None
    lineno: int
    missing: tuple[str, ...] = ()
    defect: str | None = None
    count: int = 1

    @property
    def ruling(self) -> str | None:
        if not self.author or not self.date:
            return None
        return f"{self.author}, {self.date}"


def _element_prefix(segment: str, prefix: str) -> bool:
    """Does `segment` open with the element keyword `prefix`?

    A BARE `startswith` IS NOT ENOUGH for the two keywords that end in a
    letter rather than a colon: `RULED BYE 2026-01-01` would match `RULED BY`
    and yield the value `E 2026-01-01`, so a misspelling would be read as a
    ruling. A colon-terminated keyword needs no such guard, because the colon
    is already the boundary.
    """
    if not segment.startswith(prefix):
        return False
    if prefix.endswith(":"):
        return True
    rest = segment[len(prefix):]
    return rest == "" or rest[0].isspace()


def _parse_spent_line(line: str, lineno: int,
                      entry: str | None) -> SpentDeclaration:
    """One line that BEGINS with the reserved opener, parsed or diagnosed.

    Never returns None: a line beginning with the opener is a declaration by
    construction, so what comes back is either complete, or complete enough to
    name what it owes, or a `defect` saying the subject itself could not be
    read.
    """
    rest = line[len(SPENT_OPENER):]
    subject_match = _SPENT_SUBJECT.match(rest)
    if subject_match is None:
        return SpentDeclaration(
            None, entry, None, None, None, None, None, lineno,
            defect="the reserved opener is used but no backtick-quoted bundle "
                   "name follows it, so the line names no subject at all")
    subject = subject_match.group(1).strip() or None
    if subject is None:
        # AN EMPTY BACKTICK PAIR IS A DEFECT AND NOT MERELY A MISSING ELEMENT.
        # It keys under `None` like an unreadable subject, so it MUST carry a
        # `defect` — the orphan sweep reports that string, and a None there
        # would print the word "None" into a finding a human has to act on.
        return SpentDeclaration(
            None, entry, None, None, None, None, None, lineno,
            defect="the reserved opener is followed by an EMPTY backtick pair, "
                   "so the line names no subject at all")
    tail = rest[subject_match.end():]
    segments = [s for s in _SPENT_SEP.split(tail) if s.strip()] if tail.strip() \
        else []

    values: dict[str, str] = {}
    missing: list[str] = []
    unrecognized: list[str] = []
    remaining = list(segments)
    for prefix, name in _SPENT_ELEMENTS:
        for index, segment in enumerate(remaining):
            if _element_prefix(segment, prefix):
                value = segment[len(prefix):].strip()
                if value:
                    values[name] = value
                else:
                    missing.append(name)
                # EVERYTHING BEFORE THE MATCH IS UNRECOGNIZED, and it is kept
                # rather than skipped past: a segment sitting where no element
                # is defined is the signature of a separator inside an element,
                # which is the one ambiguity this form cannot tolerate.
                unrecognized.extend(remaining[:index])
                del remaining[:index + 1]
                break
        else:
            missing.append(name)
    # OUT OF ORDER IS MALFORMED, NOT MERELY INCOMPLETE, and the segments that
    # caused it are KEPT here rather than filtered back out. A line whose CAUSE
    # precedes its SUPERSEDED BY leaves the cause segment unrecognized AND the
    # cause missing; `spent_refusal` reads the defect first, so the finding
    # says MALFORMED — which is true — instead of "omits the cause", which
    # would send a reader looking for text that is right there.
    unrecognized.extend(remaining)

    superseding = values.get("superseding bundle")
    if superseding is not None:
        # THE BACKTICKS ARE THE FORM'S, NOT THE NAME'S. The reserved line
        # quotes both bundle names, and a reader that compared the quoted text
        # against a bundle name would never match anything. An unquoted name is
        # taken as written rather than refused: it resolves to the same bundle,
        # and refusing a correct disposition on its punctuation would report a
        # defect that is not there.
        unwrapped = superseding.strip()
        if len(unwrapped) > 1 and unwrapped[0] == "`" and unwrapped[-1] == "`":
            unwrapped = unwrapped[1:-1].strip()
        values["superseding bundle"] = unwrapped or None
        if not unwrapped:
            missing.append("superseding bundle")

    author = date = None
    ruling = values.get("ruling")
    if ruling is not None:
        ruled = _RULED_BY.match(ruling)
        if ruled is None:
            missing.append("ruling date")
        else:
            author = ruled.group("author").strip() or None
            date = ruled.group("date")
            if author is None:
                missing.append("ruling author")
    if subject is None:
        missing.append("spent bundle")

    defect = None
    if unrecognized:
        defect = (
            "the line carries a segment the reserved form does not define, "
            f"{unrecognized[0]!r} — the ' — ' separator is reserved WITHIN the "
            "line, so no element may contain it")
    return SpentDeclaration(
        subject, entry, values.get("superseding bundle"), values.get("cause"),
        author, date, values.get("measurement of record"), lineno,
        tuple(dict.fromkeys(missing)), defect)


def read_spent_declarations(changelog: bytes | str | None
                            ) -> dict[str | None, SpentDeclaration]:
    """`{spent bundle: declaration}` from the changelog's raw bytes.

    ONE PURE FUNCTION, BYTES IN, per the module's existing rule that `blobs_at`
    answers raw blob bytes and that a version string is the one thing in a
    release member it is safe to decode. Decoding with `replace` keeps a
    mis-encoded byte elsewhere in a 1,200-line changelog from turning a
    readable declaration into a crash.

    REJECT RATHER THAN SKIP. Every line beginning with `SPENT_OPENER` comes
    back, including the ones that do not complete the form — those carry
    `missing` or `defect` and are REFUSED by the ladder. A reader that dropped
    them would make a typo in the record indistinguishable from no record.

    A declaration whose SUBJECT could not be read is keyed under `None`, which
    the ladder reports on the changelog itself: it is the one line of this
    state that names no bundle, so no per-bundle inventory exists to land it on.
    DUPLICATES ARE COUNTED, NOT COLLAPSED: the first declaration naming a
    bundle is the one returned and its `count` says how many were found, which
    is what lets two records of one disposition be refused as such.
    """
    if not changelog:
        return {}
    if isinstance(changelog, bytes):
        changelog = changelog.decode("utf-8", errors="replace")
    out: dict[str | None, SpentDeclaration] = {}
    counts: dict[str | None, int] = {}
    entry: str | None = None
    for lineno, line in enumerate(changelog.splitlines(), 1):
        if _LEVEL_TWO_HEADING.match(line):
            # EVERY level-two heading CLOSES the open entry; only one that
            # names a bundle OPENS a new one. A declaration under a
            # non-release `##` section is then contained by NO entry, which is
            # a containment refusal rather than a silent inheritance of the
            # previous release's authority (Codex P1, PR #584).
            heading = _ENTRY_HEADING.match(line)
            entry = heading.group(1) if heading is not None else None
            continue
        if not line.startswith(SPENT_OPENER):
            continue
        declaration = _parse_spent_line(line.rstrip(), lineno, entry)
        key = declaration.subject
        counts[key] = counts.get(key, 0) + 1
        if key not in out:
            out[key] = declaration
    return {key: replace(declaration, count=counts[key])
            for key, declaration in out.items()}


def spent_refusal(declaration: SpentDeclaration, subject: str,
                  cut: set[str]) -> str | None:
    """The reason this declaration is REFUSED, or None where every check a
    changelog read can perform has passed.

    PURE, AND DELIBERATELY SHORT OF THE PUBLICATION TEST. Everything here is
    answerable from the declaration, the bundle and the set of cut bundles;
    whether the successor's TAG is published is a git question and belongs to
    `check_repo`, which is also the only place that can turn an unlistable ref
    into a skip. Splitting them keeps the refusal ladder testable without a
    repository.
    """
    if declaration.count > 1:
        return (f"{declaration.count} SPENT declarations name {subject} in "
                f"{CHANGELOG}, and NONE of them is accepted — two records of "
                f"one disposition is how they come to disagree")
    if declaration.defect:
        return (f"the SPENT declaration naming {subject} at {CHANGELOG} line "
                f"{declaration.lineno} is MALFORMED: {declaration.defect}")
    if declaration.missing:
        owed = ", ".join(declaration.missing)
        return (f"the SPENT declaration naming {subject} at {CHANGELOG} line "
                f"{declaration.lineno} OMITS an element it owes ({owed}), so "
                f"it is not accepted — a malformed declaration is worse than "
                f"none because it looks like a record")
    superseding = declaration.superseding
    if superseding == subject:
        return (f"the SPENT declaration naming {subject} names {subject} as "
                f"its own superseding bundle: a bundle cannot declare ITSELF "
                f"spent, because a bundle that could would be able to decline "
                f"to be published")
    if declaration.entry != superseding:
        where = (f"the {declaration.entry} entry" if declaration.entry
                 else "no release entry at all")
        return (f"the SPENT declaration naming {subject} sits in {where} while "
                f"naming {superseding} as the superseding bundle: the act that "
                f"spends a number is the LATER CUT that allocates its "
                f"replacement, so the declaration is only accepted inside that "
                f"cut's own changelog entry")
    if superseding not in cut:
        return (f"the SPENT declaration naming {subject} names {superseding} "
                f"as its superseding bundle and this repository holds no "
                f"release inventory for {superseding} — it was NEVER CUT, and "
                f"retiring a number by pointing at one that does not exist is "
                f"the abuse this state is most exposed to")
    subject_version = version_of(subject)
    superseding_version = version_of(superseding)
    if superseding_version is None:
        return (f"the SPENT declaration naming {subject} names {superseding} "
                f"as its superseding bundle, which is not of the "
                f"contract-v<major>.<minor> shape this family can compare, so "
                f"the successor cannot be shown to be LATER")
    if not (subject_version is not None
            and superseding_version > subject_version):
        return (f"the SPENT declaration naming {subject} names {superseding} "
                f"as its superseding bundle, which is NOT STRICTLY LATER: a "
                f"tag that already existed before {subject} was cut is not a "
                f"replacement for it, and a guard satisfied by an earlier "
                f"release has been walked around backwards rather than met")
    return None


def inventory_path(bundle: str) -> str:
    """The one path unique to a bundle BY CONSTRUCTION, and this state's
    finding identity. Constructed rather than looked up, so the declared
    bundle — whose inventory may be written by the same cut — has a stable
    identity too."""
    return f"{RELEASES}/{bundle}.digests.yaml"


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


def _finding(sev, repo, rule, action, resolution="auto-fixable",
             path=MANIFEST):
    """`path` DEFAULTS to the manifest so that every finding predating the
    SPENT state keeps the identity it had. The state's own findings pass a
    per-bundle inventory instead, which is the whole of OD-5."""
    return Finding(sev, FAMILY, repo, path, rule, action,
                   resolution=resolution)


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
    without grading — UNLESS AN ACCEPTED OR PROVISIONAL SPENT DECLARATION NAMES
    IT, which is the third state and the only thing that changes that arm.
    """
    tip = git.remote_main_sha(repo_path)
    if tip is None:
        return Skip(FAMILY, f"{repo}: published main could not be resolved, so "
                            f"no landing distance can be counted")
    # ONE READ, AT ONE COMMIT. The changelog joins the manifest in the SAME
    # `blobs_at` call at the SAME tip, so the declaration and the declared
    # bundle can never be read from two different trees — a family that read
    # them at two commits could accept a declaration about a bundle the
    # manifest had already moved past, or refuse one it had not yet reached.
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
    declared = parse_bundle(manifest)
    if declared is None:
        return Skip(FAMILY, f"{repo}: no contract bundle declared")
    if version_of(declared) is None:
        return Skip(FAMILY, f"{repo}: declared bundle {declared!r} is not of "
                            f"the contract-v<major>.<minor> shape this family "
                            f"compares against the enforcement floor")

    changelog = blobs.get(CHANGELOG)
    if changelog is None:
        # THE SAME GUARD AS THE MANIFEST READ, ONE DOCUMENT OVER, and the same
        # conflation it exists to refuse: `blobs_at` answers None PER PATH, so
        # "I could not read the changelog" and "the changelog carries no
        # declaration" arrive identically and mean opposite things. Not fetched
        # is not an answer, in either direction (#338).
        #
        # PLACED AFTER the declared-bundle skips rather than beside the
        # manifest read, deliberately: a repository declaring no bundle is
        # better described by its own reason than by a changelog it was never
        # going to be asked about, and both orderings answer the scenario,
        # which asks for a skip NAMING THAT READ.
        # THE MESSAGE NAMES BOTH CAUSES, and Copilot was right that it owed
        # them: `blobs_at` answers None per path both where the commit is not
        # in the local object store AND where the repository simply has no
        # `contracts/CHANGELOG.md` at that tip. The second is the COMMON case
        # for a bundle-declaring repository that keeps no changelog, and a skip
        # reason naming only the first sends its reader to look for a fetch
        # problem that is not there.
        return Skip(FAMILY, f"{repo}: {CHANGELOG} could not be read at the "
                            f"published tip {tip[:9]} — either this "
                            f"repository has no {CHANGELOG} at that commit, or "
                            f"the commit is not present locally; neither is "
                            f"the same fact as carrying no SPENT declaration, "
                            f"so the question is declined rather than answered")
    declarations = read_spent_declarations(changelog)

    cut = cut_bundles(git, repo_path, tip)
    if cut is None:
        return Skip(FAMILY, f"{repo}: the release inventories under "
                            f"{RELEASES}/ could not be listed, so the set of "
                            f"cut bundles is unknown")
    findings: list[Finding] = []
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

        # absent
        #
        # THE SPENT LADDER LIVES HERE AND NOWHERE ELSE, and it is placed AFTER
        # the `ok`, `lightweight` and `misplaced` branches so that the scope
        # rule holds BY CONSTRUCTION rather than by care: those three arms have
        # already `continue`d, so no declaration can reach a tag that exists.
        # A SPENT state answers "this number will never be published"; it does
        # not answer "whatever ref exists under this name is acceptable".
        declaration = declarations.get(bundle)
        if bundle != declared:
            # BUILT ONCE AND EMITTED FROM TWO PLACES — the no-declaration arm
            # and the refusal arm — because those two must report the SAME
            # words: "a REFUSED declaration leaves this scenario in force" is
            # only true if the finding it leaves standing is the finding
            # silence would have raised.
            superseded = _finding(
                ERROR, repo,
                f"{bundle} was cut and SUPERSEDED without ever being "
                f"published: it has a release inventory, the manifest has "
                f"moved on to {declared}, and it has no published annotated "
                f"tag — under the versioning policy it was never released, "
                f"and its window closed when the next cut replaced it",
                _SUPERSEDED_ACTION)
            if declaration is None:
                # SILENCE IS NEVER A DECLARATION. Unchanged behaviour, in the
                # same words, for every bundle no declaration names — which is
                # every bundle in the estate's history but one.
                findings.append(superseded)
                continue
            refusal = spent_refusal(declaration, bundle, cut)
            if refusal is not None:
                findings.append(_finding(
                    ERROR, repo, refusal, _SPENT_REFUSED_ACTION,
                    path=inventory_path(bundle)))
                # AND THE SUPERSEDED ERROR STILL STANDS. A bad declaration
                # removes nothing; if it did, the cheapest way to quiet a
                # bundle would be to write a broken record about it.
                findings.append(superseded)
                continue
            successor_kind, _ = _tag_state(git, repo_path,
                                           declaration.superseding)
            if successor_kind == "unlistable":
                return Skip(FAMILY, f"{repo}: the published refs for "
                                    f"{declaration.superseding}, named as "
                                    f"{bundle}'s superseding bundle, could not "
                                    f"be consulted")
            if successor_kind == "ok":
                findings.append(_finding(
                    INFO, repo,
                    f"{bundle} is SPENT: it was cut, was never publishable, "
                    f"and is declared spent by the reserved SPENT declaration "
                    f"at {CHANGELOG} line {declaration.lineno}, inside the "
                    f"{declaration.superseding} entry — {declaration.superseding} "
                    f"superseded it and carries a published annotated tag on a "
                    f"commit that declares it. Ruled by {declaration.ruling}; "
                    f"cause: {declaration.cause}; measurement of record: "
                    f"{declaration.measurement}. This is NOT the tag "
                    f"obligation having been MET — it was EXTINGUISHED, by an "
                    f"owner act, at the cost of a version number",
                    _SPENT_ACTION, resolution="contested",
                    path=inventory_path(bundle)))
                continue
            # PROVISIONAL, WHICH IS NOT A REFUSAL — and it reports ONE finding
            # rather than two. The superseded `error` is SUPPRESSED here
            # because the ruling for this case is a `warning`, and a family
            # reporting both would be contradicting it. Nothing is lost: the
            # successor is graded on its own account by the arms above, so the
            # obligation has MOVED rather than been discharged.
            findings.append(_finding(
                WARNING, repo,
                f"{bundle} is declared SPENT at {CHANGELOG} line "
                f"{declaration.lineno} and the supersession is UNPROVEN: "
                f"{declaration.superseding} is cut but has no published "
                f"annotated tag on a commit that declares it, and a bundle is "
                f"not published until its tag exists — so the successor cannot "
                f"yet be shown to have carried anything forward",
                _SPENT_PROVISIONAL_ACTION, path=inventory_path(bundle)))
            continue
        if declaration is not None:
            # A REPOSITORY DECLARING A BUNDLE IT ALSO CALLS SPENT ASSERTS TWO
            # INCOMPATIBLE THINGS ABOUT ONE NUMBER. Refused — and the bundle
            # falls through to the distance grading below, exactly as it is
            # graded today.
            findings.append(_finding(
                ERROR, repo,
                f"the SPENT declaration at {CHANGELOG} line "
                f"{declaration.lineno} names {bundle}, which is the bundle "
                f"{MANIFEST} DECLARES at the published tip: a repository "
                f"cannot declare a bundle and call it spent, and this bundle "
                f"continues to be graded by distance",
                # NOT `_SPENT_REFUSED_ACTION` — found by Codex on PR #584 as a
                # P2, and it is a real misdirection rather than a wording
                # nicety. That constant promises the reader that "the
                # superseded-and-never-published finding on this bundle stands
                # beside this one", which is true of every OTHER refusal and
                # false here: this arm creates no such finding, it falls
                # through to the distance grading, and where the declaring
                # commit is still the tip that grading emits NOTHING. The
                # reader would have been sent looking for a companion error
                # that does not exist.
                _SPENT_CURRENT_ACTION, path=inventory_path(bundle)))
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

    # THE ONE FINDING OF THIS STATE THAT HAS NO BUNDLE TO LAND ON. A
    # declaration whose SUBJECT this repository never cut is not visited by the
    # loop above — there is no inventory to enumerate it from — so it is swept
    # here, and it is reported ON THE CHANGELOG because a bundle that does not
    # exist has no per-bundle inventory. It MUST NOT be read as disposing any
    # other bundle: a mistyped subject leaves the real bundle undeclared, and
    # that bundle is still reported by the arms above, which is the fail-closed
    # behaviour a typo must not be able to defeat.
    enumerable = cut | {declared}
    for subject, declaration in sorted(
            declarations.items(), key=lambda kv: (kv[0] is not None, kv[0])):
        if subject is None:
            more = ("" if declaration.count == 1 else
                    f" ({declaration.count} such lines were found; the first "
                    f"is named)")
            findings.append(_finding(
                ERROR, repo,
                f"the reserved SPENT opener is used at {CHANGELOG} line "
                f"{declaration.lineno} on a line that names no bundle: "
                f"{declaration.defect}{more} — a line beginning with "
                f"'{SPENT_OPENER}' is a MALFORMED DECLARATION, never prose to "
                f"be ignored, and this one disposes nothing",
                _SPENT_ORPHAN_ACTION, path=CHANGELOG))
            continue
        if subject in enumerable:
            continue
        findings.append(_finding(
            WARNING, repo,
            f"the SPENT declaration at {CHANGELOG} line {declaration.lineno} "
            f"names {subject} as its subject and this repository holds no "
            f"release inventory for {subject} — it was never cut, so the "
            f"declaration DISPOSES NOTHING, and whichever bundle actually owes "
            f"a tag is still reported",
            _SPENT_ORPHAN_ACTION, path=CHANGELOG))
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
