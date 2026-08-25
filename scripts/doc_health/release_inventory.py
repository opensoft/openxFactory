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
    because a declared bundle need not have one (`contract-v1.33`,
    `contract-v1.35` and `contract-v1.39` are declared and untagged);
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
# a dependency to read a file whose shape is fixed by its own schema would be a
# poor trade. Entries are `path:` followed by `digest:` and `git_mode:` within
# the same list item; the schema fixes that shape and the inventory is machine
# written, never hand-edited.
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
        if current is None:
            continue
        m = _ENTRY_DIGEST.match(line)
        if m:
            entries[current]["digest"] = m.group(1)
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


def check_repo(repo: str, repo_path: Path, git, commit: str = "HEAD"):
    """One repository's verdict: a `Skip`, or a list of `Finding`."""
    blobs = git.blobs_at(repo_path, commit, [MANIFEST])
    if blobs is None:
        return Skip(FAMILY, f"{repo}: version control could not be consulted "
                            f"at {commit}")
    manifest = blobs.get(MANIFEST)
    if manifest is None:
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
        if blob is None:
            # ABSENT AT THE COMMIT. Reported as drift, never as a skip: a
            # deleted normative member is the strongest form of what this
            # family looks for, and the blob reader returning None for an
            # absent path is DATA — a git failure would have collapsed the
            # whole call above, which is the distinction that makes this safe.
            findings.append(_finding(
                ERROR if not editorial else INFO, repo, path,
                f"inventory member is absent at {commit} but recorded in "
                f"{bundle!r}", _CUT_ACTION))
            continue
        digest = hashlib.sha256(blob).hexdigest()
        if recorded.get("digest") and digest != recorded["digest"]:
            findings.append(_finding(
                severity, repo, path,
                f"bytes differ from the digest {bundle!r} records"
                + ("" if not editorial else
                   " (editorial member — expected between cuts)"),
                _CUT_ACTION))
        recorded_mode = recorded.get("git_mode")
        actual_mode = modes.get(path)
        if recorded_mode and actual_mode and actual_mode != recorded_mode:
            # MODE IS CHECKED SEPARATELY FROM BYTES, because a chmod leaves the
            # digest identical: without this arm a validator could drift
            # executable -> non-executable while the family reported matching.
            findings.append(_finding(
                severity, repo, path,
                f"git_mode {actual_mode} differs from the {recorded_mode} "
                f"that {bundle!r} records", _CUT_ACTION))
    return findings


def fam_release_inventory_drift(ctx):
    """Every repository in scope that declares a contract bundle."""
    results: list[Finding] = []
    skips: list[str] = []
    scoped = sorted(ctx.repo_paths.items())
    if not scoped:
        return Skip(FAMILY, "no repository in scope")
    for repo, repo_path in scoped:
        outcome = check_repo(repo, Path(repo_path), ctx.git)
        if isinstance(outcome, Skip):
            skips.append(outcome.reason)
            continue
        results.extend(outcome)
    if not results and skips and len(skips) == len(scoped):
        # EVERY repository declined the question, so the family did not run.
        # Reported as a skip naming the reasons rather than as an empty pass,
        # which would read as "checked, nothing wrong".
        return Skip(FAMILY, "; ".join(skips))
    return results
