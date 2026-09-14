"""Release-inventory drift — the nineteenth deterministic check family.

Realizes `add-release-inventory-drift-check`. The obligation being checked is
`release-surface-integrity`'s ("The declared bundle describes the release
surface"); this module defines only HOW it is checked, the same by-reference
relationship tag hygiene has with `document-lifecycle`'s marker grammar.

WHY IT EXISTS. `scripts/validate-contract-release.py verify-commit` had been
failing on `origin/main` since the `contract-v1.40` tag and nobody knew,
because no gate in any session's set ran it. A release-inventory gate that
nothing runs is a gate in name only. This family is the thing that runs.

THE COMPARISON, per the ratified delta:

  * the DECLARED bundle is read from `contracts/manifest.yaml` AT THE COMMIT;
  * its inventory is resolved as the FILE at that commit — never via the tag,
    because a declared bundle need not have one — `contract-v1.33`,
    `contract-v1.35` and `contract-v1.39` were each declared and UNTAGGED for
    weeks, which is what this rule was written against; they were
    retro-published 2026-08-25 and the design stands on the general fact rather
    than on those three;
  * every member is compared on RAW BYTES digest AND recorded `git_mode`.

THE TAXONOMY IS EXHAUSTIVE AND DISJOINT, which is the part worth reading twice
because three of its five arms were wrong in the first draft and were tightened
by review before any code existed:

  no bundle declared ............................. SKIP
  bundle declared, inventory file absent ......... ERROR   (invalid declaration)
  member absent at the commit .................... ERROR   (non-editorial drift)
  member digest or mode differs .................. ERROR / INFO by editorial set
  every member matches ........................... no finding
  git unavailable or commit unresolvable ......... SKIP    (and never per-member)

The skip is reserved for "the question could not be asked". A declared bundle
naming an inventory that does not exist is an ANSWER — an invalid release
declaration, which is what a mistyped bundle name or a half-created release
looks like — and a deleted member is the strongest form of the drift this
family exists to catch. Collapsing either into a skip would make a defect
indistinguishable from an absent capability.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

from . import ERROR, INFO, Finding, Skip

FAMILY = "release-inventory-drift"

MANIFEST = "contracts/manifest.yaml"

# The three members that legitimately move between cuts. A change touching no
# contract still records itself in the changelog and may still update a
# consumption rule or a per-file digest, and the declared bundle's inventory was
# written before those edits existed. `contracts/README.md` is here BY RULING
# (Brett, 2026-08-24) rather than by observation: it had not drifted in the
# measured window, so its membership is a decision about what may legitimately
# move, not a description of what has.
EDITORIAL = frozenset({
    "contracts/CHANGELOG.md",
    "contracts/manifest.yaml",
    "contracts/README.md",
})

_BUNDLE = re.compile(r"^contract_bundle_version:\s*(\S+)\s*$", re.M)
# The inventory is parsed with regex rather than a YAML load because this
# package is stdlib-only — no `yaml` import appears anywhere in it, and adding
# a dependency for one file is a poor trade.
#
# WHAT ACTUALLY GUARANTEES THE KEY ORDER, stated honestly (PR review P3-1). An
# earlier note here claimed "the schema fixes that shape", which is FALSE: JSON
# Schema cannot constrain key order, and `release-digest-inventory.schema.yaml`
# does not try. What is true is narrower and sufficient: every inventory in this
# repository is MACHINE-WRITTEN by `release.build_release_inventory`, which
# emits `path` before `digest` for every entry, and a sweep of all 190 members
# of the current bundle finds zero counterexamples. A hand-edited inventory is
# already forbidden — the family's own action text says so — so the remaining
# risk is a future writer changing its key order, and `parse_inventory` refuses
# loudly rather than silently mis-attributing if that ever happens.
_ENTRY_PATH = re.compile(r"^\s*-?\s*path:\s*(\S+)\s*$")
_ENTRY_DIGEST = re.compile(r"^\s*digest:\s*sha256:([0-9a-f]{64})\s*$")
_ENTRY_MODE = re.compile(r"^\s*git_mode:\s*'?([0-7]{6})'?\s*$")


def inventory_path_for(bundle_tag: str) -> str:
    return f"contracts/releases/{bundle_tag}.digests.yaml"


def parse_declared_bundle(manifest_text: str) -> str | None:
    m = _BUNDLE.search(manifest_text)
    return m.group(1) if m else None


def parse_inventory(text: str) -> dict[str, dict[str, str]]:
    """`{path: {digest, git_mode}}` from an inventory document.

    A member is emitted only once its path is known, and the path resets on the
    next `path:` line, so a malformed run of keys cannot silently attach a
    digest to the previous member."""
    entries: dict[str, dict[str, str]] = {}
    current: str | None = None
    for line in text.splitlines():
        m = _ENTRY_PATH.match(line)
        if m:
            current = m.group(1)
            entries.setdefault(current, {})
            continue
        m = _ENTRY_DIGEST.match(line)
        if m:
            if current is None:
                # A digest before any path: the writer's key order changed, and
                # guessing which member it belongs to is exactly the silent
                # mis-attribution this parser must not perform.
                raise ValueError(
                    "release inventory: a digest appears before any path — "
                    "the writer's key order is not the one this parser reads")
            entries[current]["digest"] = m.group(1)
            continue
        if current is None:
            continue
        m = _ENTRY_MODE.match(line)
        if m:
            entries[current]["git_mode"] = m.group(1)
    return entries


def _finding(severity: str, repo: str, path: str, rule: str,
             action: str) -> Finding:
    # DELIBERATELY NO `resolution=` OVERRIDE, so the dataclass default
    # (`auto-fixable`) stands. See the registration note in `families.py`: a
    # `contested` class would route these back through
    # `report.uncited_resolutions` as ERRORS the first time a release cut
    # resolved one, which is every correctly performed cut.
    return Finding(severity, FAMILY, repo, path, rule, action)


_CUT_ACTION = ("cut a release through the bundle realization order; never "
               "hand-edit an inventory or contract_bundle_version to make "
               "this comparison pass")


def _shed_member(repo_path: Path, git, commit: str, path: str):
    """A recorded member's bytes and mode at `commit` when the § 5.2 shed moved
    it to a pinned leg — `(blob, git_mode)`, or `(None, None)`.

    RULED (a) POST-SHED MODE (`#656` comment `5625573095`). openxFactory's own
    `contract-v3.0` inventory records three members the shed moved
    (`contracts/schemas/{gate-action-record,xfactory-workbench-chat-turn,
    xfactory-workbench-model-catalog}.schema.yaml`), and every one of them
    arrived at its destination BYTE FOR BYTE, so the digest this family compares
    against is the digest it has always compared against. Without this the
    family would report three `ERROR`s saying a normative member VANISHED at the
    cut — a verdict about the release read off a fact about where the pin now
    holds the bytes.

    Scoped to openxFactory alone and to a commit that actually records the leg's
    gitlink: `carved_reach` resolves rows of THIS repository's manifest, so a
    sibling repository, a commit from before the shed, and a path in no row all
    answer `(None, None)` and the absence finding above stands exactly as it did.
    The reads go through the INJECTED `git` facade, exactly as every other read
    in this family does, so a harness that stubs it keeps answering for the legs
    as it answers for the repository.
    """
    try:
        from carved_reach import REPO_ROOT as CARVE_ROOT, shed_commit_object
    except ImportError:
        return None, None
    try:
        if Path(repo_path).resolve() != CARVE_ROOT.resolve():
            return None, None
        located = shed_commit_object(commit, path)
    except Exception:
        return None, None
    if located is None:
        return None, None
    leg_repo, leg_commit, leg_path = located
    blobs = git.blobs_at(leg_repo, leg_commit, [leg_path])
    if not blobs:
        return None, None
    modes = git.tree_modes(leg_repo, leg_commit) or {}
    return blobs.get(leg_path), modes.get(leg_path)


def check_repo(repo: str, repo_path: Path, git, commit: str = "HEAD"):
    """One repository's verdict: a `Skip`, or a list of `Finding`."""
    blobs = git.blobs_at(repo_path, commit, [MANIFEST])
    if blobs is None:
        return Skip(FAMILY, f"{repo}: version control could not be consulted "
                            f"at {commit}")
    manifest = blobs.get(MANIFEST)
    if manifest is None:
        # WHICH ABSENCE IS THIS? `cat-file --batch` answers `missing` both for
        # a path that does not exist AT a good commit and for a spec whose
        # COMMIT does not resolve at all, so the bare `None` cannot tell them
        # apart — and reporting "no manifest" for an unresolvable commit is a
        # misattribution that would send a reader looking in the wrong place
        # (PR review P3-2). One extra probe distinguishes them, and it runs only
        # on this already-degenerate path.
        if git.tree_modes(repo_path, commit) is None:
            return Skip(FAMILY, f"{repo}: {commit} does not resolve to a "
                                f"readable commit")
        return Skip(FAMILY, f"{repo}: no {MANIFEST} at {commit}, so no "
                            f"contract bundle is declared")

    bundle = parse_declared_bundle(manifest.decode("utf-8", "replace"))
    if bundle is None:
        return Skip(FAMILY, f"{repo}: {MANIFEST} declares no "
                            f"contract_bundle_version")

    inv_rel = inventory_path_for(bundle)
    inv_blobs = git.blobs_at(repo_path, commit, [inv_rel])
    if inv_blobs is None:
        return Skip(FAMILY, f"{repo}: version control could not be consulted "
                            f"at {commit}")
    inv_raw = inv_blobs.get(inv_rel)
    if inv_raw is None:
        # AN ANSWER, NOT AN ABSENT CAPABILITY. The repository declares this
        # bundle; naming an inventory that does not exist is an invalid release
        # declaration, and it is what a mistyped bundle name or a half-created
        # release looks like. The canonical verifier reports the same condition
        # as HGR-RELEASE-INVENTORY-MISSING rather than declining to answer.
        return [_finding(
            ERROR, repo, inv_rel,
            f"declared bundle {bundle!r} has no release digest inventory",
            "declare a bundle whose inventory exists, or create the "
            "inventory through the bundle realization order")]

    members = parse_inventory(inv_raw.decode("utf-8", "replace"))
    if not members:
        return [_finding(
            ERROR, repo, inv_rel,
            f"release digest inventory for {bundle!r} names no members",
            "rebuild the inventory with "
            "scripts/validate-contract-release.py build")]

    modes = git.tree_modes(repo_path, commit)
    if modes is None:
        return Skip(FAMILY, f"{repo}: version control could not be consulted "
                            f"at {commit}")
    paths = sorted(members)
    blobs = git.blobs_at(repo_path, commit, paths)
    if blobs is None:
        return Skip(FAMILY, f"{repo}: version control could not be consulted "
                            f"at {commit}")

    findings: list[Finding] = []
    for path in paths:
        editorial = path in EDITORIAL
        severity = INFO if editorial else ERROR
        recorded = members[path]
        blob = blobs.get(path)
        shed_mode = None
        if blob is None:
            blob, shed_mode = _shed_member(repo_path, git, commit, path)
        if blob is None:
            # ABSENT AT THE COMMIT. Reported as drift, never as a skip: a
            # deleted normative member is the strongest form of what this
            # family looks for, and the blob reader returning None for an
            # absent path is DATA — a git failure would have collapsed the
            # whole call above, which is the distinction that makes this safe.
            #
            # UNCONDITIONALLY `ERROR`, INCLUDING FOR AN EDITORIAL MEMBER. The
            # ratified scenario is unqualified — "a deleted normative member is
            # the strongest form of the drift this family exists to catch" —
            # and the editorial allowance is about members that legitimately
            # MOVE between cuts, not ones that legitimately VANISH. A deleted
            # `contracts/CHANGELOG.md` is not an expected steady state under
            # any reading. The first version of this branch carried
            # `ERROR if not editorial else INFO`, which contradicted both the
            # scenario and this module's own docstring taxonomy (PR review
            # P2-1).
            findings.append(_finding(
                ERROR, repo, path,
                f"inventory member is absent at {commit} but recorded in "
                f"{bundle!r}", _CUT_ACTION))
            continue
        # A MALFORMED ENTRY IS ITS OWN DEFECT, and it is checked BEFORE either
        # comparison because of what the alternative does. Both comparisons were
        # once written as `if recorded.get(field) and ...`, so an entry missing
        # its `digest` skipped the byte check entirely — and if the mode still
        # matched, the family reported the member CLEAN while its bytes had
        # drifted. That is fail-open: the one failure mode a drift check must
        # not have, arriving through a field nobody thought could be absent
        # (PR #324, Codex).
        #
        # AN INVENTORY THAT CANNOT ANSWER THE QUESTION IS NOT A MATCHING
        # INVENTORY. Reported unconditionally at `error`, editorial member or
        # not: the editorial allowance is about members that legitimately MOVE
        # between cuts, and it says nothing about an inventory entry that cannot
        # be read — exactly as an ABSENT member is an error in either band.
        missing_fields = [f for f in ("digest", "git_mode")
                          if not recorded.get(f)]
        if missing_fields:
            findings.append(_finding(
                ERROR, repo, path,
                f"inventory entry in {bundle!r} is missing "
                f"{' and '.join(missing_fields)}, so this member's "
                f"{'bytes' if 'digest' in missing_fields else 'mode'} cannot "
                f"be checked at all",
                "rebuild the inventory with "
                "scripts/validate-contract-release.py build; an entry that "
                "cannot answer is not an entry that matches"))
            continue
        digest = hashlib.sha256(blob).hexdigest()
        if digest != recorded["digest"]:
            findings.append(_finding(
                severity, repo, path,
                f"bytes differ from the digest {bundle!r} records"
                + ("" if not editorial else
                   " (editorial member — expected between cuts)"),
                _CUT_ACTION))
        recorded_mode = recorded["git_mode"]
        actual_mode = modes.get(path) or shed_mode
        if actual_mode and actual_mode != recorded_mode:
            # MODE IS CHECKED SEPARATELY FROM BYTES, because a chmod leaves the
            # digest identical: without this arm a validator could drift
            # executable -> non-executable while the family reported matching.
            findings.append(_finding(
                severity, repo, path,
                f"git_mode {actual_mode} differs from the {recorded_mode} "
                f"that {bundle!r} records", _CUT_ACTION))
    return findings


def fam_release_inventory_drift(ctx):
    """Every repository in scope that declares a contract bundle.

    A PER-REPOSITORY SKIP IS REPORTED, NOT DROPPED (PR review P2-2). The
    ratified obligation is per-repository — a family that cannot run "MUST be
    reported as skipped, never silently omitted" — and the family-level `Skip`
    return can only carry the ALL-SKIPPED case. In this factory the everyday
    state is the mixed one: most pinned repositories declare no contract bundle
    at all, so a design that only spoke up when every repository skipped would
    be silent about five of six on every single run, which is the shape of
    "silently omitted" the requirement names.

    Each skipped repository therefore contributes an `info` finding carrying its
    reason. `info` because a repository that declares no bundle is an inventory
    fact rather than a defect — the same band the editorial drift uses, and one
    that reddens no gate. The family-level `Skip` is kept for the case it
    genuinely describes: nothing in scope was askable at all.
    """
    results: list[Finding] = []
    skips: list[str] = []
    scoped = sorted(ctx.repo_paths.items())
    if not scoped:
        return Skip(FAMILY, "no repository in scope")
    for repo, repo_path in scoped:
        outcome = check_repo(repo, Path(repo_path), ctx.git)
        if isinstance(outcome, Skip):
            skips.append(outcome.reason)
            results.append(_finding(
                INFO, repo, MANIFEST,
                f"not checked: {outcome.reason}",
                "no action — this repository's release surface was not "
                "evaluated, and the reason is recorded rather than omitted"))
            continue
        results.extend(outcome)
    if skips and len(skips) == len(scoped):
        # EVERY repository declined the question, so the family did not run at
        # all. Reported as a family-level skip naming the reasons rather than as
        # a list of info findings that would read as "checked, nothing wrong".
        return Skip(FAMILY, "; ".join(skips))
    return results
