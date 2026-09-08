#!/usr/bin/env python3
"""openxFactory pin reconciliation check (domain-conformance-checks capability).

Runs from the pinned openxFactory checkout against a DomainxFactory repo,
never copied into it (adopted from codexFactory's conformance-gate,
adopt-neutral-utility-pack; the overlap with
``validate-domain-openxfactory-pins.py`` is a deliberately deferred merge —
design D3 of that change).

Aggregation-scope only: compares stack.yaml ``xfactory.contract_ref``
against the aggregation repository's recorded openxFactory submodule
pointer.

- ERROR when the pin is not an ancestor of the submodule pointer
  (divergent — the declared contract is off the submodule's history);
- WARN when the pin is a proper ancestor (stale-behind — legal, the
  aggregation pointer may deliberately track ahead, but it must be
  visible); the warning includes the refresh instruction;
- PASS on equality;
- SKIP with notice outside an aggregation checkout.

Tenant records are exempt by design: per-tenant openxFactory pinning is
legitimate by contract and is not inspected here.

SECOND USE OF THE WARNING TIER — the relocation notice (split-openxwallet-repo
P2.5, design D5). When the bundle a domain pins carries manifest rows with a
``relocating:`` mapping, this check names each relocating artifact with its
target repository and tag, and STAYS GREEN. The manifest is read AT THE
CONSUMER'S PINNED COMMIT, because the question is "what does the bundle this
domain actually consumes say", not "what does this checkout happen to hold now".
The removal version and the migration path are NOT read from the row — the row
deliberately carries neither, per ``docs/contract-versioning-policy.md``
lines 246-248, which put both in ``contracts/CHANGELOG.md``.

WHY THIS SCRIPT AND NOT ITS SIBLING. ``validate-domain-openxfactory-pins.py``
carries no ``warn`` token in its 138 lines, so making it emit would force a
relocation notice to be an ERROR and red every domain that pinned the
deprecation minor — a perfectly legal bundle. That is precisely the failure the
manifest-carried marker was chosen to avoid, so this script, the only candidate
with a warning tier, is the emitter and that one is deliberately left alone.
``scripts/validate-openxwallet.py`` is likewise not the emitter and is not
edited: the consumer runs it ``--strict`` (which reds on any warning) while
openxFactory's own gate runs it WITHOUT ``--strict`` (so nothing required would
surface it anyway).
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

import yaml

PASS, WARN, ERROR, SKIP = "PASS", "WARN", "ERROR", "SKIP"

MANIFEST_PATH = "contracts/manifest.yaml"


class RelocatingRow(NamedTuple):
    """One manifest row whose canonical home is moving to another repository."""

    artifact_id: str
    to: str
    tag: str


def classify(pin: str, pointer: str, is_ancestor) -> tuple[str, str]:
    """Pure decision: (verdict, message). ``is_ancestor(a, b)`` -> bool."""
    if pin == pointer:
        return PASS, f"stack pin matches aggregation submodule pointer ({pin[:12]})"
    if is_ancestor(pin, pointer):
        return WARN, (
            f"stack pin {pin[:12]} is stale-behind the aggregation submodule "
            f"pointer {pointer[:12]}; refresh with: update stack.yaml "
            f"xfactory.contract_ref to {pointer} and contract_declared_at to today"
        )
    return ERROR, (
        f"stack pin {pin[:12]} is not an ancestor of the aggregation submodule "
        f"pointer {pointer[:12]}: the declared contract is off the submodule's history"
    )


def relocating_rows(manifest) -> list[RelocatingRow]:
    """Pure: the relocating rows of ``manifest``, in MANIFEST ORDER.

    Manifest order rather than sorted order because the relocating rows are one
    authored block and reading them back in another order would misrepresent the
    file. Anything unreadable yields an empty list rather than an exception: this
    is a notice, and it must never be the reason a conformance run fails.
    """
    if not isinstance(manifest, dict):
        return []
    entries = manifest.get("contracts")
    if not isinstance(entries, list):
        return []
    rows: list[RelocatingRow] = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        marker = entry.get("relocating")
        if not isinstance(marker, dict):
            continue
        artifact_id, to, tag = entry.get("id"), marker.get("to"), marker.get("tag")
        if not (artifact_id and to and tag):
            continue
        rows.append(RelocatingRow(str(artifact_id), str(to), str(tag)))
    return rows


def relocation_notice(manifest) -> str | None:
    """Pure: the WARN-tier relocation notice, or ``None`` when nothing relocates.

    Names every relocating artifact with its target repository and tag — a count
    alone would not tell a migrator where to go. Does NOT state a removal
    version: the row carries none by design, so the notice points at the
    changelog, which is where the policy puts it.
    """
    rows = relocating_rows(manifest)
    if not rows:
        return None
    bundle = manifest.get("contract_bundle_version") or "(unnamed bundle)"
    header = (
        f"{WARN}: the pinned openxFactory bundle {bundle} carries {len(rows)} "
        f"relocating contract row(s); each artifact's canonical home is moving "
        f"and it is removed at a later major bundle — read "
        f"contracts/CHANGELOG.md at this pin for the removal version and "
        f"the migration path:"
    )
    listing = [f"  {row.artifact_id} -> {row.to} @ {row.tag}" for row in rows]
    return "\n".join([header, *listing])


def manifest_at_commit(openx_root: Path, commit: str):
    """The manifest as of ``commit``, or ``None`` if the question can't be asked.

    A commit absent from this checkout, a manifest absent at that commit, bytes
    that are not YAML, or a document that is not a mapping are all the same
    answer — the release-inventory family's own doctrine, reused: a question that
    could not be asked is not a finding.
    """
    try:
        result = subprocess.run(
            ["git", "-C", _git_dir_arg(openx_root), "show", f"{commit}:{MANIFEST_PATH}"],
            capture_output=True, text=True, check=False, timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    try:
        document = yaml.safe_load(result.stdout)
    except yaml.YAMLError:
        return None
    return document if isinstance(document, dict) else None


def find_aggregation_root(repo_root: Path) -> Path | None:
    candidate = repo_root.parent.parent
    gitmodules = candidate / ".gitmodules"
    if gitmodules.is_file() and "openxFactory" in gitmodules.read_text(encoding="utf-8"):
        return candidate
    return None


def _git_dir_arg(root: Path) -> str:
    """Absolute form of a directory handed to ``git -C``.

    Both roots can come from the command line, and a relative path that began
    with a dash would be read by git as an option rather than a directory.
    Resolving first removes that shape entirely.
    """
    return str(Path(root).resolve())


def recorded_pointer(aggregation_root: Path) -> str:
    out = subprocess.run(
        ["git", "-C", _git_dir_arg(aggregation_root), "ls-tree", "HEAD", "openxFactory"],
        capture_output=True, text=True, check=True,
    ).stdout.split()
    return out[2]


def git_is_ancestor(openx_root: Path):
    root_arg = _git_dir_arg(openx_root)

    def _is_ancestor(ancestor: str, descendant: str) -> bool:
        return subprocess.run(
            ["git", "-C", root_arg, "merge-base", "--is-ancestor", ancestor, descendant],
            capture_output=True,
        ).returncode == 0
    return _is_ancestor


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    # Required on purpose: this script's own repo (openxFactory, the
    # publisher) is not a domain repo, so a self-repo default would be a
    # wrong-target default. The known consumers already pass the path.
    parser.add_argument(
        "repo_root",
        type=Path,
        help="domain repo root to check",
    )
    parser.add_argument(
        "--aggregation-root",
        type=Path,
        default=None,
        help="aggregation repo root override (default: repo_root/../..)",
    )
    args = parser.parse_args()

    aggregation_root = args.aggregation_root or find_aggregation_root(args.repo_root)
    if aggregation_root is None:
        print("SKIP: pin reconciliation skipped (not an aggregation checkout)")
        return 0

    with (args.repo_root / "stack.yaml").open(encoding="utf-8") as handle:
        pin = yaml.safe_load(handle)["xfactory"]["contract_ref"]
    pointer = recorded_pointer(aggregation_root)

    openx_root = aggregation_root / "openxFactory"
    verdict, message = classify(pin, pointer, git_is_ancestor(openx_root))
    print(f"{verdict}: {message}", file=sys.stderr if verdict == ERROR else sys.stdout)

    # The relocation notice is ADDITIVE to the verdict above, never a
    # replacement for it: an ERROR pin and a relocating bundle are independent
    # facts and both are reported. It goes to stdout unconditionally because it
    # is never an error, and it does not touch the return expression — WARN has
    # always exited 0 and this is a WARN.
    notice = relocation_notice(manifest_at_commit(openx_root, pin))
    if notice:
        print(notice)

    return 1 if verdict == ERROR else 0


if __name__ == "__main__":
    raise SystemExit(main())
