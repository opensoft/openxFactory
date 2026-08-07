"""The fifteenth deterministic family: proposal origin
(add-proposal-origin-contract; doc-health delta "Proposal-origin checks
enforced by reference").

Enforces the promoted origin requirements of `document-lifecycle` and
`release-realization` BY REFERENCE over every pinned repo's
`openspec/changes/` tree (active and archived):

1. **missing-origin** — an active or archived proposal with no origin
   declaration and no recorded migration exemption. Severity is ERROR for
   changes created on or after the contract's approval date and WARNING
   for pre-contract legacy (the family MUST NOT fabricate or infer staging
   history for changes that predate the contract — a pre-contract change
   without a migration record is reported for visibility, never invented).
2. **malformed-origin** — unknown kind, both kinds declared, or a durable
   id that does not match its declared kind's grammar
   (`<repo>:staging:<topic-slug>` / `<repo>:adhoc:<date-or-slug>`).
   Backfilled origins recorded by the migration are validated against that
   record instead of the strict grammar (the 2026-07-12 migration predates
   grammar enforcement and is itself the recorded provenance).
3. **origin-mismatch** — the support manifest's repeated origin fields
   disagree with the packet's `.openspec.yaml` declaration. For an archived
   change the retained manifest is the transition-time record, so a
   disagreement is indistinguishable from post-ratification mutation:
   ERROR with resolution class `contested` (resolving it reverses a gate
   decision).
4. **staged-origin-unresolvable** — a staged origin whose recorded
   provenance does not resolve: the manifest's `source_revision` does not
   contain `origin.path`, or (for an ACTIVE change whose staging folder
   still exists) no document in the folder carries a `Staging ID:` equal to
   `origin.id`. A staging folder that disappeared AFTER transition is legal
   history and reports nothing.
5. **adhoc-provenance-incomplete** — an `ad_hoc` origin lacking a
   non-empty `reason`, `approved_by`, or `approved_on`.

Deterministic: filesystem + git object reads only, no model calls, no
writes. Resolution classes are set per finding (the catalog/routing
precedent): mutation/mismatch findings are `contested`; everything else is
mechanical visibility.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

from . import CONTESTED, ERROR, WARNING, Finding, Skip

FAMILY = "proposal-origin"

# The origin contract's PROMOTION date (enforcement is prospective from the
# promotion of add-proposal-origin-contract, not from the migration's
# 2026-07-12 approval; the UTC stamping of archive folders makes the boundary
# inclusive): a change created AFTER this date has no excuse for a missing
# origin; everything through the promotion day without a migration record is
# pre-contract legacy, reported as WARNING visibility — never fabricated,
# never a regression-gate break.
CONTRACT_DATE = "2026-08-07"

STAGED_ID_RE = re.compile(r"^[A-Za-z0-9_.-]+:staging:[a-z0-9][a-z0-9-]*$")
ADHOC_ID_RE = re.compile(r"^[A-Za-z0-9_.-]+:adhoc:[A-Za-z0-9][A-Za-z0-9-]*$")
_STAGING_HEADER_RE = re.compile(r"^Staging ID:\s*`?([^`\s]+)`?\s*$", re.M)
_ARCHIVE_DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-")

# The recorded migration provenance (spec: "Backfilled origins SHALL be
# validated against recorded migration provenance"). The evidence record
# travels with the owning change (active now, archived later) — resolve it
# wherever the change currently lives.
MIGRATION_EVIDENCE_RELPATHS = (
    "openspec/changes/add-proposal-origin-contract/migration-evidence.md",
)
_MIGRATION_ARCHIVE_GLOB = "openspec/changes/archive/*-add-proposal-origin-contract/migration-evidence.md"
_MIGRATED_CHANGE_RE = re.compile(r"\*\*`(?:archive/)?([A-Za-z0-9._-]+)`\*\*")


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def _load_yaml(path: Path):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return None


def migration_records(openx_root: Path) -> frozenset:
    """Change ids (archive folder names) the recorded migration classified —
    the exemption-and-validation register for backfilled origins."""
    texts = []
    for rel in MIGRATION_EVIDENCE_RELPATHS:
        p = Path(openx_root) / rel
        if p.is_file():
            texts.append(_read(p))
    for p in sorted(Path(openx_root).glob(_MIGRATION_ARCHIVE_GLOB)):
        texts.append(_read(p))
    names = set()
    for text in texts:
        names.update(_MIGRATED_CHANGE_RE.findall(text))
    return frozenset(names)


def _created_date(change_dir: Path, meta) -> str | None:
    """The change's creation date: `.openspec.yaml` `created:` first, else
    the archived folder's date prefix, else unknown."""
    if isinstance(meta, dict) and meta.get("created"):
        return str(meta["created"])
    m = _ARCHIVE_DATE_RE.match(change_dir.name)
    return m.group(1) if m else None


def _git_path_exists(repo_path: Path, revision: str, rel_path: str) -> bool | None:
    """True/False when git can answer; None when the revision itself is
    unresolvable in this checkout (shallow clone, foreign history) — the
    caller reports nothing rather than guessing."""
    try:
        probe = subprocess.run(
            ["git", "-C", str(repo_path), "cat-file", "-e",
             f"{revision}^{{commit}}"],
            capture_output=True, text=True, timeout=30)
        if probe.returncode != 0:
            return None
        out = subprocess.run(
            ["git", "-C", str(repo_path), "ls-tree", "--name-only",
             revision, "--", rel_path],
            capture_output=True, text=True, timeout=30)
        if out.returncode != 0:
            return None
        return bool(out.stdout.strip())
    except (OSError, subprocess.TimeoutExpired):
        return None


def _staging_header_matches(repo_path: Path, origin_path: str,
                            origin_id: str) -> bool | None:
    """For an ACTIVE staged-origin change whose staging folder still exists:
    does any document in it carry the matching `Staging ID:`? None when the
    folder is gone (legal post-transition history)."""
    folder = Path(repo_path) / origin_path
    if not folder.is_dir():
        return None
    for doc in sorted(folder.glob("*.md")):
        m = _STAGING_HEADER_RE.search(_read(doc))
        if m and m.group(1) == origin_id:
            return True
    return False


def _manifest_origin(change_dir: Path):
    manifest = change_dir / "supporting-docs" / "manifest.yaml"
    if not manifest.is_file():
        manifest = change_dir / "supporting-docs.manifest.yaml"
        if not manifest.is_file():
            return None, None
    data = _load_yaml(manifest)
    if not isinstance(data, dict):
        return None, manifest
    return data, manifest


def check_change(repo: str, repo_path: Path, change_dir: Path,
                 migrated: frozenset, archived: bool) -> list:
    findings = []
    rel = change_dir.relative_to(repo_path).as_posix()
    meta_path = change_dir / ".openspec.yaml"
    meta = None
    if meta_path.is_file():
        meta = _load_yaml(meta_path)
        if meta is None:
            # The packet metadata exists but does not parse — a distinct
            # defect from a missing declaration (the migration itself wrote
            # one such file; the family caught it).
            findings.append(Finding(
                ERROR, FAMILY, repo, rel,
                ".openspec.yaml does not parse as YAML — the origin "
                "declaration is unreadable",
                "repair the packet metadata (quote scalars containing "
                "': '), preserving the declared origin text"))
            return findings
    origin = meta.get("origin") if isinstance(meta, dict) else None

    if not isinstance(origin, dict):
        if change_dir.name in migrated:
            # Recorded migration exemption: the migration classified this
            # change; an APPLIED backfill means the origin exists, so
            # reaching here means the block was later REMOVED — mutation.
            findings.append(Finding(
                ERROR, FAMILY, repo, rel,
                "origin declaration recorded by the 2026-07-12 migration is "
                "absent — a backfilled origin was removed after the fact",
                "restore the origin block recorded in the migration evidence",
                resolution=CONTESTED))
            return findings
        created = _created_date(change_dir, meta)
        pre_contract = created is None or created <= CONTRACT_DATE
        findings.append(Finding(
            WARNING if pre_contract else ERROR, FAMILY, repo, rel,
            "proposal carries no origin declaration"
            + (" (pre-contract legacy, no recorded migration)"
               if pre_contract else ""),
            "declare `origin:` in .openspec.yaml (staged or ad_hoc per the "
            "document-lifecycle origin requirement)"))
        return findings

    kind = origin.get("kind")
    oid = origin.get("id")
    both = "staging:" in str(oid or "") and kind == "ad_hoc" \
        or ("adhoc:" in str(oid or "") and kind == "staged")
    if kind not in ("staged", "ad_hoc"):
        findings.append(Finding(
            ERROR, FAMILY, repo, rel,
            f"unknown origin kind {kind!r}",
            "declare kind: staged or kind: ad_hoc"))
        return findings
    if both:
        findings.append(Finding(
            ERROR, FAMILY, repo, rel,
            "origin id and kind disagree — a proposal declares exactly one "
            "origin kind",
            "make the durable id match the declared kind"))

    grammar = STAGED_ID_RE if kind == "staged" else ADHOC_ID_RE
    if not isinstance(oid, str) or not grammar.match(oid):
        if change_dir.name not in migrated:
            findings.append(Finding(
                ERROR, FAMILY, repo, rel,
                f"malformed durable origin id {oid!r} for kind {kind}",
                "use <repo>:staging:<topic-slug> or <repo>:adhoc:<date>-<slug>"))

    if kind == "ad_hoc":
        for field in ("reason", "approved_by", "approved_on"):
            value = origin.get(field)
            if not value or not str(value).strip():
                findings.append(Finding(
                    ERROR, FAMILY, repo, rel,
                    f"ad-hoc origin lacks required `{field}`",
                    "record the explicit approval provenance the ad-hoc "
                    "exception requires"))

    manifest, manifest_path = _manifest_origin(change_dir)
    if isinstance(manifest, dict) and isinstance(manifest.get("origin"), dict):
        m_origin = manifest["origin"]
        fields = ["kind", "id"] + (["path"] if kind == "staged" else [])
        for field in fields:
            if m_origin.get(field) != origin.get(field):
                findings.append(Finding(
                    ERROR, FAMILY, repo, rel,
                    f"support manifest origin `{field}` "
                    f"({m_origin.get(field)!r}) disagrees with the packet "
                    f"declaration ({origin.get(field)!r})"
                    + (" — for an archived change this is post-ratification "
                       "mutation" if archived else ""),
                    "reconcile the manifest against the declaration recorded "
                    "at transition; resolving reverses a gate decision",
                    resolution=CONTESTED))

    if kind == "staged":
        opath = origin.get("path")
        if not opath:
            findings.append(Finding(
                ERROR, FAMILY, repo, rel,
                "staged origin lacks `path` (the historical transition "
                "source)", "record the original staging folder path"))
        else:
            source_rev = None
            if isinstance(manifest, dict):
                source_rev = manifest.get("source_revision")
            if isinstance(source_rev, str) and re.fullmatch(
                    r"[0-9a-f]{40}|[0-9a-f]{64}", source_rev):
                exists = _git_path_exists(repo_path, source_rev, str(opath))
                if exists is False:
                    findings.append(Finding(
                        ERROR, FAMILY, repo, rel,
                        f"staged origin path {opath!r} does not resolve at "
                        f"the recorded source revision {source_rev[:12]}",
                        "the recorded provenance must contain the staging "
                        "folder; correct the manifest or the declaration",
                        resolution=CONTESTED))
            if not archived:
                linked = _staging_header_matches(repo_path, str(opath),
                                                 str(oid))
                if linked is False:
                    findings.append(Finding(
                        ERROR, FAMILY, repo, rel,
                        f"staging folder {opath!r} still exists but no "
                        f"document carries `Staging ID: {oid}`",
                        "restore the staging-header linkage or record the "
                        "folder's move"))
    return findings


def _iter_change_dirs(repo_path: Path):
    root = Path(repo_path) / "openspec" / "changes"
    if not root.is_dir():
        return
    for entry in sorted(root.iterdir()):
        if entry.name == "archive" or not entry.is_dir():
            continue
        yield entry, False
    archive = root / "archive"
    if archive.is_dir():
        for entry in sorted(archive.iterdir()):
            if entry.is_dir():
                yield entry, True


def fam_proposal_origin(ctx):
    if yaml is None:
        return Skip(FAMILY, "PyYAML unavailable; proposal packets cannot "
                    "be parsed")
    openx_root = None
    for name, path in ctx.repo_paths.items():
        if name == "openxFactory":
            openx_root = Path(path)
    if openx_root is None and ctx.agg_root is None:
        openx_root = Path(next(iter(ctx.repo_paths.values())))
    elif openx_root is None:
        openx_root = Path(ctx.agg_root) / "openxFactory"
    migrated = migration_records(openx_root)

    findings = []
    for repo, repo_path in sorted(ctx.repo_paths.items()):
        for change_dir, archived in _iter_change_dirs(Path(repo_path)):
            findings.extend(check_change(
                repo, Path(repo_path), change_dir, migrated, archived))
    return findings
