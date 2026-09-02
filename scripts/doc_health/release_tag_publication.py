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
RELEASES = "contracts/releases"

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
    without grading.
    """
    tip = git.remote_main_sha(repo_path)
    if tip is None:
        return Skip(FAMILY, f"{repo}: published main could not be resolved, so "
                            f"no landing distance can be counted")
    blobs = git.blobs_at(repo_path, tip, [MANIFEST])
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
        if bundle != declared:
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
