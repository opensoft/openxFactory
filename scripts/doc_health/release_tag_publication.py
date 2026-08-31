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
"""

from __future__ import annotations

import re
from pathlib import Path

from . import ERROR, INFO, WARNING, Finding, Skip

FAMILY = "release-tag-publication"
MANIFEST = "contracts/manifest.yaml"

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


def _finding(sev, repo, rule, action, resolution="auto-fixable"):
    return Finding(sev, FAMILY, repo, MANIFEST, rule, action,
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


def check_repo(repo: str, repo_path: Path, git,
               threshold: int = DEFAULT_THRESHOLD):
    """One repository. `Skip` where the question could not be asked, a list of
    findings otherwise — empty when the obligation is met."""
    tip = git.remote_main_sha(repo_path)
    if tip is None:
        return Skip(FAMILY, f"{repo}: published main could not be resolved, so "
                            f"no landing distance can be counted")
    blobs = git.blobs_at(repo_path, tip, [MANIFEST])
    if blobs is None:
        return Skip(FAMILY, f"{repo}: version control could not be consulted "
                            f"for {MANIFEST}")
    bundle = parse_bundle(blobs.get(MANIFEST))
    if bundle is None:
        return Skip(FAMILY, f"{repo}: no contract bundle declared")
    version = version_of(bundle)
    if version is None:
        return Skip(FAMILY, f"{repo}: declared bundle {bundle!r} is not of the "
                            f"contract-v<major>.<minor> shape this family "
                            f"compares against the enforcement floor")
    if version < ENFORCEMENT_FLOOR:
        return []

    ref = git.tag_ref(repo_path, bundle)
    if ref is None:
        return Skip(FAMILY, f"{repo}: tag refs could not be listed")
    objecttype, peeled = ref

    if objecttype is None:
        distance = distance_from_tip(git, repo_path, bundle, tip, threshold + 2)
        if distance is None:
            return Skip(FAMILY, f"{repo}: the earliest commit declaring "
                                f"{bundle} could not be resolved")
        if distance == 0:
            # The declaring commit is still the published tip. The owner's tag
            # act legitimately follows it, and this is not a pass: the
            # obligation is owed and simply not yet late.
            return []
        if distance <= threshold:
            return [_finding(
                WARNING, repo,
                f"{bundle} is declared and has no published annotated tag, "
                f"{distance} first-parent landing(s) after the commit that "
                f"declared it",
                _ABSENT_ACTION)]
        return [_finding(
            ERROR, repo,
            f"{bundle} is declared and has no published annotated tag more "
            f"than {threshold} first-parent landings after the commit that "
            f"declared it — under the versioning policy it is NOT PUBLISHED, "
            f"and its presence in the manifest is not a release",
            _ABSENT_ACTION)]

    if objecttype != "tag":
        return [_finding(
            ERROR, repo,
            f"the ref named {bundle} is a LIGHTWEIGHT tag, not an annotated "
            f"one, so it does not satisfy the policy's requirement",
            _LIGHTWEIGHT_ACTION)]

    target = git.blobs_at(repo_path, peeled, [MANIFEST])
    if target is None:
        return Skip(FAMILY, f"{repo}: the commit {bundle}'s tag peels to could "
                            f"not be read")
    declared_there = parse_bundle(target.get(MANIFEST))
    if declared_there == bundle:
        return []
    return [_finding(
        ERROR, repo,
        f"{bundle}'s annotated tag is MISPLACED: it peels to {peeled[:9]}, "
        f"which declares "
        + (f"{declared_there}" if declared_there else "no bundle at all")
        + f", not {bundle} — a tag on the wrong commit satisfies every check "
          f"that asks only whether a tag exists, and it is what consumers pin",
        _MISPLACED_ACTION, resolution="contested")]


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
