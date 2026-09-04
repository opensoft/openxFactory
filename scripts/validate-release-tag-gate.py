#!/usr/bin/env python3
"""THE RELEASE-TAG GATE: the same obligation, asked at the cutting pull request.

WHAT MOVED, AND WHY. `tests/doc-health/test_release_tag_publication.py`'s
self-gate asserted, inside the REQUIRED `pytest-suite`, that THIS repository
reads ZERO `release-tag-publication` findings. The family flags a bundle that
`contracts/manifest.yaml` (or an inventory under `contracts/releases/`)
declares without a published annotated tag — and the tag is published AFTER the
cutting pull request merges, by a second actor with tag rights. So the window
between the two acts turned EVERY pull request in the repository red, not just
the one that opened it. Measured 2026-09-03/04 (openxFactory #664): PR #628
declared `contract-v3.3` untagged at 22:27Z; main and every open lane failed on
that one test until the tag was published after PR #636, five and a half hours
later. Brett Heap ruled on 2026-09-04 that the assertion MOVES rather than
goes: out of the suite every lane runs, into a gate that runs on the pull
request that changes the release surface.

THE SAME BAR, NOT A SECOND ONE — and that is the whole design. The pin asserted
"no `error` and no `warning` from this family". This gate asserts exactly that,
against the PULL REQUEST'S MERGE TREE instead of against published `main`, and
only when the pull request touches `contracts/manifest.yaml` or
`contracts/releases/**`. One family, one definition of "published", two
moments. Nothing here re-implements what a published tag is, re-grades a
distance, or invents a severity: `#614`'s ONE CLOCK, NOT TWO, applied to a
family whose clock is already written down.

WHY THE NEW BUNDLE'S OWN TAG IS NOT REQUIRED HERE, and why that is honest
rather than a hole. The tag cannot exist yet. Measured over every
`contract-v3.x` cut this repository has made, the annotated tag is created
AFTER the merge and points AT THE MERGE COMMIT — v3.1 six seconds after, v3.2
twenty-three, v3.3 forty-four, v3.4 sixty-eight. A pre-merge gate that demanded
it would be unsatisfiable by construction, which is a gate people route around.
The family already answers this correctly and needs no help: a bundle whose
EARLIEST DECLARING COMMIT IS THE TIP is at distance zero and emits NO FINDING
(promoted scenario *The declaring commit is still the published tip*). On a
merge tree the cutting commit IS the tip, so the bundle this pull request cuts
is silent — and the silence is not a discharge. The obligation is RECORDED, in
the check summary and as an annotation on the pull request, and the nightly
doc-health run goes on reporting it at its ratified severity until the tag
exists.

WHAT IT REFUSES ON, ALL OF IT PRE-MERGE-DECIDABLE:

  1. `gate-findings` — any `error` or `warning` the family reports over the
     merge tree. In practice this is the STALE untagged bundle: a bundle cut
     earlier, still unpublished, while this pull request touches the release
     surface again. The window the family grants a fresh cut is for landings
     that DO NOT touch that surface; a pull request that touches it is
     asserting the surface is in order, so it carries the red.
  2. `gate-version-reuse` — this pull request MOVES the declaration to a bundle
     whose tag is ALREADY PUBLISHED AND PEELS ELSEWHERE THAN THIS TREE. That is
     a number being cut twice, and it is the one release defect the family
     cannot see: at a tip where the declaration and the tag agree it reads
     `ok`. It is asked only after the family has had its say, so that a tag
     pointing at the WRONG commit is reported in the family's own ratified
     MISPLACED words rather than in this tool's. The versioning policy's
     realization order says a cut "recheck[s] bundle/tag availability and
     allocate[s] the NEXT AVAILABLE version", and its Immutable Tag Correction
     rule says a version number "is never reused". ONE EXCEPTION, and it is
     not a loophole: a tag that peels to THE VERY TREE UNDER JUDGMENT is the
     obligation met early, not a second cut, so it is recorded and allowed —
     which is also what lets this gate be re-run against a merge commit after
     the cut landed and still report the truth about it.
  3. `gate-unaskable` — the family could not ask its question (published refs
     unlistable, a blob unreadable, a declaring commit unresolvable). FAIL
     CLOSED. The nightly may honestly skip; this gate is now the enforcing
     moment, and an unasked question is not a pass.
  4. `gate-unreadable-*` — the gate could not resolve the head, the base, or
     the diff between them. Fail closed for the same reason.

EXIT CODES: 0 the gate is satisfied (including the short-circuit), 2 ANY
refusal and any environment failure. There is deliberately NO exit 1, on
`scripts/validate-openreposhape-pin.py`'s stated rule: the gate's only question
is "may this pull request proceed", and the answer is the same for "a bundle is
unpublished" and "the bytes could not be resolved". A two-valued failure invites
a workflow that treats one of them as a warning.

WHAT THIS GATE DOES NOT CHECK, said here so nobody infers it does. It does not
verify that the release inventory reproduces from the tree, nor that the
manifest and the inventories agree — `release-inventory-drift`,
`scripts/validate-manifest-digests.py` and the `manifest_digests` suite already
do, inside the same required `pytest-suite`, and a second implementation here
would be the second clock this design exists to avoid. It does not anchor on
tags for drift; `release-surface-integrity` deliberately does not, so that its
obligation stays evaluable in the window before a tag exists.

Usage:
    validate-release-tag-gate.py [REPO_ROOT] [--head REV] [--base REV]
                                 [--repo-name NAME] [--summary PATH]

REPO_ROOT defaults to the current directory. `--head` defaults to `HEAD`, which
on a `pull_request` run is the MERGE COMMIT GitHub builds; `--base` defaults to
the head's FIRST PARENT, which on that same merge commit is the base branch tip,
so the diff is exactly this pull request's net change.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from doc_health import ERROR, WARNING, Skip  # noqa: E402
from doc_health import release_tag_publication as rtp  # noqa: E402
from doc_health.corpus import RealGit  # noqa: E402

MANIFEST = rtp.MANIFEST
RELEASES_PREFIX = rtp.RELEASES + "/"

PASS = 0
REFUSE = 2

#: Every refusal this tool can make, as (code, one-line meaning). Enumerated so
#: a reader of the workflow log and a reader of the tests see the same closed
#: set, and so a new refusal cannot be added without appearing here.
REFUSALS = {
    "gate-findings": "the family reports an error or a warning over the merge "
                     "tree",
    "gate-version-reuse": "this pull request moves the declaration to a bundle "
                          "whose tag is already published",
    "gate-unaskable": "the family could not ask its question",
    "gate-unreadable-head": "the head revision could not be resolved",
    "gate-unreadable-base": "the base revision could not be resolved",
    "gate-unreadable-diff": "the changed paths could not be listed",
    "gate-unreadable-manifest": "the manifest could not be read at the head or "
                                "at the base",
}


class MergeTreeGit(RealGit):
    """`RealGit` whose PUBLISHED TIP is the tree under judgment.

    ONE OVERRIDE AND NO OTHER. The family resolves the tip it reads at with
    `remote_main_sha`, which asks the remote for `refs/heads/main` — the right
    question for the nightly and the wrong one here, because the tree this gate
    judges is not published yet and is the whole point. Every other read stays
    exactly as the nightly makes it, INCLUDING the tag read, which goes on
    consulting `ls-remote origin` deliberately: the obligation is about a
    PUBLISHED tag, and a local ref can be an unpushed tag on the author's
    machine.
    """

    def __init__(self, head_sha: str):
        self.head_sha = head_sha

    def remote_main_sha(self, repo: Path) -> str:  # noqa: D102
        return self.head_sha


class Ctx:
    """The family's context object, one repository wide."""

    def __init__(self, repo_name: str, repo_path: Path, git):
        self.repo_paths = {repo_name: repo_path}
        self.git = git


class Result:
    """A gate verdict: an exit code, a refusal code where it refused, and the
    lines a human reads."""

    def __init__(self, code: int, refusal: str | None, lines: list[str],
                 obligation: str | None = None):
        self.code = code
        self.refusal = refusal
        self.lines = lines
        self.obligation = obligation

    @property
    def passed(self) -> bool:
        return self.code == PASS


def _run(repo: Path, *args: str) -> str | None:
    """git, degraded to None on failure — the seam `RealGit` already uses."""
    proc = subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True)
    return proc.stdout if proc.returncode == 0 else None


def resolve(repo: Path, rev: str) -> str | None:
    out = _run(repo, "rev-parse", "--verify", f"{rev}^{{commit}}")
    return out.strip() if out and out.strip() else None


def is_release_surface(path: str) -> bool:
    """Whether one changed path is part of the release surface this gate guards.

    The manifest and the release inventories, and nothing else. `contracts/`
    generally is NOT the surface: a contract file changing is an ordinary
    change until a cut declares a bundle over it, and a gate that fired on
    every contract edit would be the collateral this design removes, moved one
    directory down.
    """
    return path == MANIFEST or path.startswith(RELEASES_PREFIX)


def changed_paths(repo: Path, base: str, head: str) -> list[str] | None:
    """Paths differing between `base` and `head`, or None where git failed.

    A PLAIN TWO-POINT DIFF, not the three-dot form. `head` on a
    `pull_request` run is the merge commit GitHub built, whose FIRST PARENT is
    the base tip, so `base..head` already is this pull request's net change
    against the branch it would land on. The three-dot form would ask a
    different question (changes since the merge base), which on a merge commit
    is the same answer by a longer route and a different one on any other
    revision a caller passes.
    """
    out = _run(repo, "diff", "--name-only", base, head)
    if out is None:
        return None
    return [line.strip() for line in out.splitlines() if line.strip()]


def declared_at(git, repo: Path, sha: str) -> tuple[bool, str | None]:
    """`(read_succeeded, bundle or None)` for the manifest at `sha`.

    THE TWO FALSE ANSWERS ARE KEPT APART, which is the conflation this family's
    own module documents at length: a manifest that could not be READ is not a
    manifest declaring NOTHING, and a gate that treated them alike would pass a
    pull request whose bytes it never obtained.
    """
    blobs = git.blobs_at(repo, sha, [MANIFEST])
    if blobs is None:
        return (False, None)
    raw = blobs.get(MANIFEST)
    if raw is None:
        # An ANSWER: there is no manifest at that commit. A repository before
        # its first cut, and a base that predates the file, both read this way.
        return (True, None)
    return (True, rtp.parse_bundle(raw))


def evaluate(repo: Path, head: str = "HEAD", base: str | None = None,
             repo_name: str = "openxFactory", git=None,
             threshold: int | None = None) -> Result:
    """The whole gate, as a value. The CLI below only prints it."""
    head_sha = resolve(repo, head)
    if head_sha is None:
        return Result(REFUSE, "gate-unreadable-head",
                      [f"the head revision {head!r} does not resolve to a "
                       f"commit in {repo}"])
    base_rev = base if base is not None else f"{head_sha}^1"
    base_sha = resolve(repo, base_rev)
    if base_sha is None:
        return Result(REFUSE, "gate-unreadable-base",
                      [f"the base revision {base_rev!r} does not resolve to a "
                       f"commit in {repo} — on a pull_request run the head is "
                       f"a merge commit and its first parent is the base tip, "
                       f"so a checkout without history cannot be judged"])

    paths = changed_paths(repo, base_sha, head_sha)
    if paths is None:
        return Result(REFUSE, "gate-unreadable-diff",
                      [f"the changed paths between {base_sha[:9]} and "
                       f"{head_sha[:9]} could not be listed"])
    touched = [p for p in paths if is_release_surface(p)]
    if not touched:
        return Result(PASS, None,
                      [f"no release surface change: none of the {len(paths)} "
                       f"changed path(s) between {base_sha[:9]} and "
                       f"{head_sha[:9]} is {MANIFEST} or under "
                       f"{RELEASES_PREFIX}",
                       "the release-tag obligation is unaffected by this pull "
                       "request and is not evaluated against it"])

    git = git if git is not None else MergeTreeGit(head_sha)
    lines = [f"release surface touched by this pull request "
             f"({len(touched)} path(s)):"]
    lines += [f"  - {p}" for p in touched]

    read_ok, head_declared = declared_at(git, repo, head_sha)
    if not read_ok:
        return Result(REFUSE, "gate-unreadable-manifest",
                      lines + [f"{MANIFEST} could not be read at the head "
                               f"{head_sha[:9]}"])
    base_ok, base_declared = declared_at(git, repo, base_sha)
    if not base_ok:
        return Result(REFUSE, "gate-unreadable-manifest",
                      lines + [f"{MANIFEST} could not be read at the base "
                               f"{base_sha[:9]}"])
    lines.append(f"declared bundle: {base_declared or '(none)'} at the base "
                 f"{base_sha[:9]} -> {head_declared or '(none)'} at the head "
                 f"{head_sha[:9]}")

    # (1) and (3) THE FAMILY ITSELF, unmodified, over the merge tree — and it
    # runs FIRST, so that every condition it already has ratified words for is
    # reported in those words rather than in this tool's.
    ctx = Ctx(repo_name, repo, git)
    if threshold is not None:
        ctx.tag_publication_threshold = threshold
    outcome = rtp.fam_release_tag_publication(ctx)
    if isinstance(outcome, Skip):
        return Result(REFUSE, "gate-unaskable",
                      lines + [f"the release-tag-publication family could not "
                               f"ask its question over the merge tree: "
                               f"{outcome.reason}",
                               "this gate fails closed: the nightly may "
                               "honestly skip, but a pull request that changes "
                               "the release surface is the enforcing moment "
                               "and an unasked question is not a pass"])

    blocking = [f for f in outcome if f.severity in (ERROR, WARNING)]
    other = [f for f in outcome if f.severity not in (ERROR, WARNING)]
    for finding in other:
        lines.append(f"  [{finding.severity}] {finding.rule}")
    if blocking:
        lines.append(f"{len(blocking)} blocking finding(s) over the merge tree "
                     f"{head_sha[:9]}:")
        for finding in blocking:
            lines.append(f"  [{finding.severity}] {finding.path}: "
                         f"{finding.rule}")
            lines.append(f"      action: {finding.action}")
        return Result(REFUSE, "gate-findings", lines)

    # (2) VERSION REUSE, and it is asked AFTER the family has had its say.
    # The family cannot answer this one: where a tag exists and peels to a
    # commit that declares the same bundle, `_tag_state` reads `ok` and the
    # reuse is invisible. But where the tag peels SOMEWHERE ELSE the family
    # DOES speak, in its own ratified MISPLACED words, and those are the more
    # precise ones — so the family goes first and this arm reports only what
    # it left unsaid. The condition is narrow on purpose: the declaration has
    # to MOVE in this pull request, so a pull request editing the manifest for
    # any other reason never reaches it.
    cutting = head_declared is not None and head_declared != base_declared
    if cutting and rtp._at_or_above_floor(head_declared):
        ref = git.tag_ref(repo, head_declared)
        if ref is None:
            return Result(REFUSE, "gate-unaskable",
                          lines + [f"the published refs for {head_declared} "
                                   f"could not be consulted, so bundle/tag "
                                   f"availability could not be rechecked"])
        objecttype, peeled = ref
        if objecttype is not None and peeled == head_sha:
            # PRE-PUBLISHED AT THIS EXACT TREE, which is not reuse and must not
            # be refused as it. Two real situations reach this arm and both are
            # correct: a tag published at the head before merge (openXwallet's
            # `wallet-v1.4` flow), and THIS GATE RE-RUN AFTER THE CUT LANDED —
            # on the merge commit the tag now names. A rule that refused here
            # would make the gate un-replayable, which is how a check stops
            # being trusted as a report of the tree it was pointed at.
            lines.append(f"{head_declared} is PRE-PUBLISHED: its annotated tag "
                         f"already peels to the tree under judgment "
                         f"{head_sha[:9]}, which is the obligation met early "
                         f"rather than a number cut twice")
        elif objecttype is not None:
            return Result(
                REFUSE, "gate-version-reuse",
                lines + [
                    f"{head_declared} ALREADY HAS A PUBLISHED TAG "
                    f"({objecttype}, {(peeled or '')[:9]}), and this pull "
                    f"request moves the declaration onto it: that is one "
                    f"version number cut twice",
                    "the versioning policy's realization order allocates the "
                    "NEXT AVAILABLE version after rechecking bundle/tag "
                    "availability, and Immutable Tag Correction holds that a "
                    "version number is never reused — a defective release is "
                    "corrected by a SUPERSEDING one",
                    "action: rebase onto the current tip, recheck availability, "
                    "and allocate the next unused bundle version across the "
                    "manifest, the changelog and the release inventory "
                    "together"])

    # PASSED — and the obligation, if one is owed, is RECORDED rather than
    # silently satisfied. This is the case the ruling names: the bundle this
    # pull request cuts has no tag and cannot have one yet.
    obligation = None
    if head_declared is not None and rtp._at_or_above_floor(head_declared):
        kind, _ = rtp._tag_state(git, repo, head_declared)
        if kind == "absent":
            obligation = (
                f"TAG OWED: `{head_declared}` has no published annotated tag. "
                f"Publishing it is an act after this pull request merges, at "
                f"the merge commit, per the versioning policy's realization "
                f"order step 5. Until it exists the nightly doc-health run "
                f"reports this bundle, and the NEXT pull request that touches "
                f"the release surface will be refused by this gate.")
    lines.append("the release-tag obligation holds over the merge tree "
                 f"{head_sha[:9]}: no error, no warning")
    return Result(PASS, None, lines, obligation)


def _emit(text: str, summary_path: str | None) -> None:
    print(text)
    if summary_path:
        try:
            with open(summary_path, "a", encoding="utf-8") as handle:
                handle.write(text + "\n")
        except OSError:
            # A summary that cannot be written must never change the verdict.
            pass


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="validate-release-tag-gate.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("repo_root", nargs="?", default=".")
    parser.add_argument("--head", default="HEAD",
                        help="the tree under judgment; on a pull_request run "
                             "this is the merge commit (default: HEAD)")
    parser.add_argument("--base", default=None,
                        help="what to diff against (default: the head's first "
                             "parent, which is the base branch tip)")
    parser.add_argument("--repo-name", default="openxFactory",
                        help="the name the family reports findings under")
    parser.add_argument("--summary", default=None,
                        help="a file to append the report to; defaults to "
                             "$GITHUB_STEP_SUMMARY when set")
    args = parser.parse_args(argv)

    summary = args.summary or os.environ.get("GITHUB_STEP_SUMMARY") or None
    repo = Path(args.repo_root).resolve()
    result = evaluate(repo, head=args.head, base=args.base,
                      repo_name=args.repo_name)

    _emit("## release-tag-gate", summary)
    for line in result.lines:
        _emit(line, summary)
    if result.obligation:
        _emit("", summary)
        _emit(result.obligation, summary)
        print(f"::notice title=release-tag-gate::{result.obligation}")
    if result.refusal:
        meaning = REFUSALS.get(result.refusal, "")
        _emit("", summary)
        _emit(f"REFUSED `{result.refusal}` — {meaning}", summary)
        print(f"::error title=release-tag-gate::{result.refusal}: {meaning}")
    return result.code


if __name__ == "__main__":
    sys.exit(main())
