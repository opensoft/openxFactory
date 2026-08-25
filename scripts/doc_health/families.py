"""The contract check families.

Each family is a function fam_<id>(ctx) -> list[Finding] | Skip. WHAT each
family verifies is owned by the openxFactory `doc-health` contract; the
tag-hygiene grammar is owned by `document-lifecycle` and enforced here by
reference (the regexes below transcribe, never extend, that grammar).
`document_catalog.py` owns the thirteenth family's own implementation
(add-document-cataloging), `ideation_routing.py` owns the fourteenth
(add-cross-factory-ideation-routing), `proposal_origin.py` owns the
fifteenth (add-proposal-origin-contract),
`client_identity_composition.py` owns the sixteenth
(add-client-identity-roster), and `promotion_fidelity.py` owns the
eighteenth (add-promotion-fidelity-check); all five are only registered
below.

The count is deliberately no longer written into this docstring's first
line. It was wrong for three months — `staged-topic-template` registered on
2026-08-15 and the "sixteen" here and in the promoted requirement both
stayed put until `govern-openspec-corpus-membership` caught them — and a
number that only a human re-reads is a number that drifts. `FAMILIES` at the
bottom of this module is the count.
"""

from __future__ import annotations

import hashlib
import json
import re
import tarfile
from datetime import date
from pathlib import Path

from . import (AUTO_FIXABLE, CONTESTED, CRITICAL, ERROR, WARNING, INFO,
               TAXONOMY, Finding, Skip, recorded_rel)
from . import (client_identity_composition, corpus, document_catalog,
               ideation_routing, promotion_fidelity, proposal_origin)
from .lines import split_keepends

# Per-family resolution class defaults (doc-health contract): contested
# families suggest state-changing edits; everything else is mechanical.
#
# "document-catalog" is deliberately ABSENT here (research D6): its
# twelve finding classes are a mix of mechanical/auto-fixable checks
# (coverage, duplicate-key, stale-entry, artifact-type, immutable-path,
# recursion) and always-contested ones (taxonomy/controlled-value,
# resolution, confidence, provenance, override-standing, pending-aging).
# A single table entry here would force one resolution onto every
# class, contradicting D6. document_catalog.py sets `resolution=` per
# finding instead — see its module docstring.
#
# "ideation-routing" is ABSENT for the same reason (add-cross-factory-
# ideation-routing): only its `path-normalization` class is auto-fixable
# (delta "safe mechanical defects") and its `external-path` skips are
# informational; every other class is `contested`. ideation_routing.py
# sets `resolution=` per finding — a table entry would force one class.
FAMILY_RESOLUTION = {
    "location-conformance": CONTESTED,
    "standard-backing": CONTESTED,
    "register-lifecycle-consistency": CONTESTED,
    "record-immutability": CONTESTED,
    "staged-candidate-aging": CONTESTED,
    "uncited-resolution": CONTESTED,
}

# ---------------------------------------------------------------- helpers


def _link_targets(line: str) -> list[str]:
    """Markdown link targets plus bare path-like tokens — a Backed by:
    line may reference its spec either way."""
    targets = re.findall(r"\]\(([^)#]+)", line)
    body = line.split(":", 1)[1] if ":" in line else line
    targets += [t for t in re.findall(r"[\w.-]+(?:/[\w.-]+)+", body)
                if "/" in t]
    return targets


def _resolves(doc_dir: Path, repo_path: Path, target: str) -> bool:
    target = target.strip()
    if target.startswith(("http://", "https://")):
        return True  # external references are not checked by this pass
    return (doc_dir / target).exists() or (repo_path / target).exists()


def _header_lines(doc, prefix: str) -> list[str]:
    """EVERY `prefix`-matching REAL line within the doc's header window.

    Real lines (CR/LF/CRLF only — `doc_health.lines`), not
    `str.splitlines()` pseudo-lines: this is a reader of the SAME lifecycle
    header `corpus.parse_status`/`parse_kind` read, and a wider splitting
    rule here than there is exactly the divergence
    `align-status-reader-to-real-lines` closes — demonstrated as a false
    CRITICAL `ratified-provenance` finding ("Ratified by: missing") on a
    document whose real header plainly carries the line, inflated past the
    window by an exotic separator. Widened to every reader of the header by
    the change's ruling (2026-08-19): the delta's "SHALL hold for every
    reader of that header" governs.

    All matches, not the first: a rule that says a document carries EXACTLY
    ONE of something cannot be enforced by a reader that stops at the first
    one. `fam_ratified_provenance` counts with this; the single-line readers
    below keep first-match semantics via `_header_line`.
    """
    return [body for body, _ending
            in split_keepends(doc.text)[:corpus.STATUS_SCAN_LINES]
            if body.startswith(prefix)]


def _header_line(doc, prefix: str) -> str | None:
    """First `prefix`-matching REAL line within the doc's header window,
    or None. See `_header_lines` for the real-line rule this inherits."""
    lines = _header_lines(doc, prefix)
    return lines[0] if lines else None


# --- ratification citation spellings (`document-lifecycle`) -------------
#
# TWO sanctioned spellings, read as TWO distinct prefixes and deliberately
# never as one shorter prefix (sanction-ratified-record-spelling, design
# D2). `_header_line` matches with `body.startswith(prefix)`, so a prefix of
# `"Ratified"` would also match body prose that merely opens with the word —
# a section label (`Ratified: YAML-serialized JSON-Schema contracts under…`)
# or a sentence (`Ratified together with the two decisions…`). Both such
# lines sit well below the header window in today's corpus, which is exactly
# what makes the short prefix dangerous: it would pass every test written
# against today's corpus and mis-fire on the first document whose HEADER
# window opens with one.
#
# The two prefixes are disjoint by construction — a `Ratified by:` line does
# not start with `Ratified:` — which is what keeps the two rules separable:
# change-id resolution runs for the primary spelling, the three-way floor
# runs for the record-citing one.
_RATIFIED_BY_PREFIX = "Ratified by:"     # primary: names an approving change
_RATIFIED_RECORD_PREFIX = "Ratified:"    # record-citing: no approving change

# The floor's DATE axis. ISO calendar dates are the only date shape the
# corpus's citation lines write, and the only one this reads.
_CITATION_DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")

# The floor's APPROVER axis: a `by <Proper Name>` clause, as in
# `Ratified: 2026-08-10 by Brett Heap — in-session, verbatim: "ratified"`.
# A heuristic, and deliberately a narrow one — there is no roster of
# approvers to resolve against, so this reads the one shape the corpus
# actually writes. Citations that name their approver some other way (inside
# a record parenthetical, say) are carried by the other two axes; the floor
# is disjunctive precisely so a narrow axis costs nothing.
#
# DISCLOSED NARROWING, not an oversight: `by <Name>` is the ONLY approver
# spelling this axis recognizes. A line naming its approver in another form
# — `Ratified: ruling round (Brett Heap presiding)`, design D1's row-3
# shape — is not read as naming an approver, and must clear the floor on the
# date or record axis instead. The remedy for an author is to write
# `by <Name>`, never to invent a date the record does not carry (OQ-3), and
# `docs/document-lifecycle.md` § Status Claim Rules states the recognized
# form so an author reads it at authoring time rather than discovering it
# from a finding. Widening this pattern to guess at approver names inside
# free prose would trade a disclosed narrow rule for an undisclosed
# guess — the invention the floor exists to prevent.
_CITATION_APPROVER = re.compile(r"\bby\s+[A-Z][\w.'-]*")


def _lifecycle_scope(ctx):
    """The document scope of the FOUR lifecycle families, and of no others.

    `govern-openspec-corpus-membership` (ruled 2026-08-23) declares two
    document sets. `ctx.docs` is the governed corpus, which every family
    reads. `ctx.lifecycle_docs` is the lifecycle scan set — each OpenSpec
    change packet's `proposal.md` and its `review/` records — which only
    `fam_status_validity`, `fam_standard_backing`, `fam_ratified_provenance`
    and `fam_succession_integrity` read, because those four check a claim of
    STANDING and a proposal makes one.

    ONE accessor, not four copies of the concatenation, for two reasons the
    ruling names. A fifth reader becomes a one-line opt-in: swap `ctx.docs`
    for `_lifecycle_scope(ctx)` in that family. And an audit finds every
    reader by call site — `grep -n _lifecycle_scope` is the complete list,
    which is what makes the "the other twelve families do not read the scan
    set" test enforceable rather than aspirational.

    A finding lands on the document's own path either way: the same `Doc`
    shape, the same `doc.repo` key into `ctx.repo_paths`, so nothing
    downstream of a family needs to know which set a document came from.
    """
    return [*ctx.docs, *ctx.lifecycle_docs]


def _age_days(as_of: date, when: date | None) -> int | None:
    return (as_of - when).days if when else None


def _strip_inline_code(line: str) -> str:
    return re.sub(r"`[^`]*`", "", line)


def _scan_lines(text: str):
    """Yield (lineno, line, in_code_fence) with ``` fence tracking.

    Real lines (CR/LF/CRLF only — `doc_health.lines`), not unbounded
    `str.splitlines()`: before `align-status-reader-to-real-lines`'s wide
    ruling, THIS FUNCTION was a live second Python line rule, disagreeing
    with `round_trip.py`'s split on any form-feed/U+2028/NEL heading
    fixture. Fixing it here does not make the corpus's "reduces the Python
    side to one" claim true in general — TWO further unbounded
    `str.splitlines()` scanners over document text carry the identical
    pattern, independently, and remain unconverted (deliberately out of
    this change's every-*header*-reader scope; see `tasks.md` §7 and
    `doc_health.lines`'s module docstring): `_template_gaps` in this same
    module, and `doc_health.ideation_routing._scan_lines` (finding F6, an
    unconverted copy of this very function as it existed before this
    change). The "reduces the Python side to one" claim is true for
    lifecycle-header readers specifically, which is the claim this change
    makes — not for every line-splitting rule in the corpus. Line NUMBERS
    are unaffected for every document this repository's baseline measured
    (zero exotic separators across 1227 governed aggregation files), since
    real-line and pseudo-line numbering agree wherever no such separator
    appears.
    """
    fenced = False
    for i, (line, _ending) in enumerate(split_keepends(text), start=1):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            yield i, line, True
            continue
        yield i, line, fenced


def _staged_exit_changes(text: str, change_ids: set[str]) -> list[str]:
    """Return change ids used as lifecycle exits, not evidence citations."""
    lifecycle_lines = []
    in_exit = False
    for line in text.splitlines():
        if line.startswith("## "):
            in_exit = line.strip().lower() == "## exit"
        if in_exit or line.startswith((
                "Proposed by:", "Proposal:", "Exit:", "Exits via:")):
            lifecycle_lines.append(line)
    lifecycle_text = "\n".join(lifecycle_lines)
    return sorted(change for change in change_ids if change in lifecycle_text)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_support_manifest(path: Path) -> dict | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) and value.get("format_version") == 1 else None


def _active_support_findings(repo: str, repo_path: Path) -> list[Finding]:
    findings = []
    changes = repo_path / "openspec" / "changes"
    if not changes.is_dir():
        return findings
    for change in sorted(p for p in changes.iterdir()
                         if p.is_dir() and p.name != "archive"):
        support = change / "supporting-docs"
        if not support.is_dir():
            continue
        rel = str(support.relative_to(repo_path))
        manifest = _load_support_manifest(support / "manifest.yaml")
        if manifest is None:
            findings.append(Finding(
                ERROR, "location-conformance", repo, rel,
                "active proposal support lacks a valid manifest.yaml",
                "create the proposal supporting-document manifest"))
        for path in sorted(support.rglob("*.md")):
            # `source-snapshots/` holds BYTE-EXACT copies of the staged files as
            # they were at the move, and the manifest proves that with a
            # per-file sha256. Their `Status: staged` is therefore CORRECT — it
            # is what the source said — and the usual remedy ("change proposed
            # prose to draft") would falsify the snapshot and break the very
            # checksum it exists to support. Proposal prose beside them is still
            # checked; only the immutable record is exempt.
            if "source-snapshots" in path.relative_to(support).parts:
                continue
            if corpus.parse_status(path.read_text(errors="replace")) == "staged":
                findings.append(Finding(
                    ERROR, "location-conformance", repo,
                    str(path.relative_to(repo_path)),
                    "staged status under active proposal support",
                    "change proposed prose to draft or immutable evidence to record"))
        if manifest is not None:
            for entry in manifest.get("files", []):
                path = support / recorded_rel(entry.get("path", ""))
                if (not path.is_file()
                        or _sha256(path) != entry.get("sha256")):
                    findings.append(Finding(
                        ERROR, "location-conformance", repo, rel,
                        f"active proposal support checksum mismatch: {entry.get('path')}",
                        "refresh or correct the supporting-document manifest"))
    return findings


def _archive_support_findings(repo: str, repo_path: Path) -> list[Finding]:
    findings = []
    archive = repo_path / "openspec" / "changes" / "archive"
    if not archive.is_dir():
        return findings
    for change in sorted(path for path in archive.iterdir() if path.is_dir()):
        manifest_path = change / "supporting-docs.manifest.yaml"
        bundle = change / "supporting-docs.tar.gz"
        if not manifest_path.exists() and not bundle.exists():
            continue
        rel = str(change.relative_to(repo_path))
        manifest = _load_support_manifest(manifest_path)
        if manifest is None or not bundle.is_file():
            findings.append(Finding(
                ERROR, "location-conformance", repo, rel,
                "archived proposal support is incomplete",
                "restore both the readable manifest and compressed bundle"))
            continue
        if _sha256(bundle) != manifest.get("bundle", {}).get("sha256"):
            findings.append(Finding(
                ERROR, "location-conformance", repo, rel,
                "archived proposal support bundle checksum mismatch",
                "rebuild the deterministic bundle and manifest"))
            continue
        expected = {recorded_rel(item.get("path")): item.get("sha256")
                    for item in manifest.get("files", [])}
        actual = {}
        try:
            with tarfile.open(bundle, "r:gz") as tar:
                for member in tar.getmembers():
                    if not member.isfile():
                        continue
                    stream = tar.extractfile(member)
                    if stream is not None:
                        actual[member.name] = hashlib.sha256(stream.read()).hexdigest()
        except (OSError, tarfile.TarError):
            actual = {}
        if actual != expected:
            findings.append(Finding(
                ERROR, "location-conformance", repo, rel,
                "archived proposal support member inventory or hashes mismatch",
                "restore or rebuild the archive from verified proposal support"))
    return findings


# ---------------------------------------------------------------- families


def fam_status_validity(ctx):
    findings = []
    for doc in _lifecycle_scope(ctx):
        if doc.status is None:
            findings.append(Finding(
                ERROR, "status-validity", doc.repo, doc.path,
                "missing status header",
                "add a Status: header from the controlled taxonomy"))
        elif doc.status not in TAXONOMY:
            findings.append(Finding(
                ERROR, "status-validity", doc.repo, doc.path,
                f"free-form status {doc.status!r}",
                "replace with a controlled taxonomy value"))
    return findings


def fam_standard_backing(ctx):
    findings = []
    for doc in _lifecycle_scope(ctx):
        if doc.status != "standard":
            continue
        line = _header_line(doc, "Backed by:")
        repo_path = ctx.repo_paths[doc.repo]
        doc_dir = (repo_path / doc.path).parent
        ok = bool(line) and any(
            _resolves(doc_dir, repo_path, t) for t in _link_targets(line))
        if not ok:
            findings.append(Finding(
                CRITICAL, "standard-backing", doc.repo, doc.path,
                "standard claim without resolvable backing",
                "add a Backed by: line resolving to a promoted spec or "
                "canonical contract, or demote to draft"))
    return findings


def fam_ratified_provenance(ctx):
    """Both sanctioned ratification citation spellings, each under its own
    rule (`document-lifecycle`, sanction-ratified-record-spelling).

    `Ratified by:` keeps the change-id resolution it has always had.
    `Ratified:` — legal only where no approving change exists to name — is
    held to the three-way floor instead: an approver, a date, or a
    resolvable record path, ANY ONE of which makes the claim checkable by a
    reader. The floor is never applied to `Ratified by:`, whose named change
    is itself the resolvable record; doing so would convert every governed
    document that names its change and nothing else into a CRITICAL finding
    in one commit. Every violation here is CRITICAL: the header asserts an
    approval that nothing backs, however it is spelled.

    "Exactly one citation" is counted as ONE TOTAL across both spellings,
    which is what the requirement says and what OQ-4 ruled ("EXACTLY ONE
    citation line per document"). Two lines in the SAME spelling carry the
    identical defect as one of each — nothing on the page says which is
    current — so the count, not the pair, is what fires: one shared,
    count-based rule string for every shape of duplicate, mixed-spelling
    pair or same-spelling repeat alike.
    """
    findings = []
    for doc in _lifecycle_scope(ctx):
        if doc.status != "ratified":
            continue
        by_lines = _header_lines(doc, _RATIFIED_BY_PREFIX)
        record_lines = _header_lines(doc, _RATIFIED_RECORD_PREFIX)

        count = len(by_lines) + len(record_lines)
        if count > 1:
            findings.append(Finding(
                CRITICAL, "ratified-provenance", doc.repo, doc.path,
                f"carries {count} ratification citation lines, not one",
                "keep exactly one: Ratified by: where an approving OpenSpec "
                "change exists, Ratified: where none does"))
            continue

        by_line = by_lines[0] if by_lines else None
        record_line = record_lines[0] if record_lines else None

        if by_line:
            body = by_line.split(":", 1)[1]
            names = set(re.findall(r"[\w][\w-]{3,}", body))
            ids = set().union(*ctx.change_ids.values()) if ctx.change_ids else set()
            ok = bool(names & ids)
            if not ok:
                repo_path = ctx.repo_paths[doc.repo]
                doc_dir = (repo_path / doc.path).parent
                ok = any(_resolves(doc_dir, repo_path, t)
                         for t in _link_targets(by_line))
            if not ok and "openxFactory" in body and \
                    "openxFactory" not in ctx.repo_paths:
                ok = True  # cross-repo provenance; unverifiable in this
                # scope, verified by full aggregation runs
            if not ok:
                findings.append(Finding(
                    CRITICAL, "ratified-provenance", doc.repo, doc.path,
                    "Ratified by: missing or does not resolve to an OpenSpec change",
                    "point Ratified by: at an existing active or archived change"))
            continue

        if record_line:
            # The floor, cheapest axis first — mirroring the primary path's
            # own shape (a cheap read, then `_resolves` only if it fails).
            # The RECORD axis is read exactly as every other citation family
            # reads one, `_link_targets` + `_resolves`: a markdown link
            # target or a bare slash-bearing token that exists relative to
            # the document's directory or the repo root. That is what
            # "resolvable record path" means mechanically — a path-shaped
            # token the repo actually contains — and reusing the shared
            # helpers keeps it from becoming a second resolution rule.
            body = record_line.split(":", 1)[1]
            ok = bool(_CITATION_APPROVER.search(body)
                      or _CITATION_DATE.search(body))
            if not ok:
                repo_path = ctx.repo_paths[doc.repo]
                doc_dir = (repo_path / doc.path).parent
                ok = any(_resolves(doc_dir, repo_path, t)
                         for t in _link_targets(record_line))
            if not ok:
                findings.append(Finding(
                    CRITICAL, "ratified-provenance", doc.repo, doc.path,
                    "Ratified: names none of an approver, a date, or a "
                    "resolvable record path",
                    "name at least one of an approver, a date, or a "
                    "resolvable record path — or cite the approving change "
                    "with Ratified by: if one exists"))
            continue

        findings.append(Finding(
            CRITICAL, "ratified-provenance", doc.repo, doc.path,
            "ratified header carries no citation in either sanctioned "
            "spelling",
            "add Ratified by: <change> where an approving OpenSpec change "
            "exists, otherwise Ratified: naming an approver, a date, or a "
            "resolvable record path"))
    return findings


def fam_succession_integrity(ctx):
    findings = []
    for doc in _lifecycle_scope(ctx):
        if doc.status == "superseded":
            line = _header_line(doc, "Superseded by:")
            repo_path = ctx.repo_paths[doc.repo]
            doc_dir = (repo_path / doc.path).parent
            ok = bool(line) and any(
                _resolves(doc_dir, repo_path, t) for t in _link_targets(line))
            if not ok:
                findings.append(Finding(
                    ERROR, "succession-integrity", doc.repo, doc.path,
                    "superseded without resolvable successor",
                    "add a Superseded by: line naming the successor document"))
        elif doc.status == "retired":
            if not (_header_line(doc, "Retired:")
                    or _header_line(doc, "Reason:")):
                findings.append(Finding(
                    ERROR, "succession-integrity", doc.repo, doc.path,
                    "retired without a stated reason",
                    "add a Retired:/Reason: line naming the reason or "
                    "decision record"))
    return findings


def fam_location_conformance(ctx):
    findings = []
    for doc in ctx.docs:
        if doc.status == "brainstorm" and not doc.path.startswith(
                "ideation/brainstorm/"):
            findings.append(Finding(
                ERROR, "location-conformance", doc.repo, doc.path,
                "brainstorm document outside ideation/brainstorm/",
                "move it under ideation/brainstorm/ or change its status"))
        if (doc.status == "staged" and not doc.path.startswith("ideation/")
                and doc.kind != "register"):
            # candidate registers are a promoted organized-state home
            # (document-lifecycle: ideation/staging/ OR a candidate register)
            findings.append(Finding(
                ERROR, "location-conformance", doc.repo, doc.path,
                "staged fragment outside ideation/",
                "move it under ideation/staging/ or change its status"))
        if doc.status == "staged" and doc.path.startswith("ideation/staging/"):
            ids = ctx.change_ids.get(doc.repo, set())
            cited = _staged_exit_changes(doc.text, ids)
            if cited:
                findings.append(Finding(
                    ERROR, "location-conformance", doc.repo, doc.path,
                    f"staged material already cites proposal {cited[0]}",
                    "move selected material into the proposal supporting-docs folder"))
    for repo, repo_path in sorted(ctx.repo_paths.items()):
        findings.extend(_active_support_findings(repo, repo_path))
        findings.extend(_archive_support_findings(repo, repo_path))
        specs = repo_path / "openspec" / "specs"
        if specs.is_dir():
            for path in sorted(specs.rglob("supporting-docs.tar.gz")):
                findings.append(Finding(
                    ERROR, "location-conformance", repo,
                    str(path.relative_to(repo_path)),
                    "historical proposal support bundle under canonical specs",
                    "move the bundle beside its archived OpenSpec change"))
    return findings


def fam_record_immutability(ctx):
    findings = []
    is_record = lambda text: corpus.parse_status(text) == "record"
    for doc in ctx.docs:
        if doc.status != "record":
            continue
        blob = ctx.git.capture_blob(
            ctx.repo_paths[doc.repo], doc.path, is_record)
        if blob is None or blob == doc.text:
            continue
        # Link fixes are excepted: ignore changed line pairs where both
        # sides carry markdown link syntax.
        old = [l for l in blob.splitlines() if l not in doc.text.splitlines()]
        new = [l for l in doc.text.splitlines() if l not in blob.splitlines()]
        substantive = ([l for l in old if "](" not in l]
                       or [l for l in new if "](" not in l])
        if substantive:
            findings.append(Finding(
                CRITICAL, "record-immutability", doc.repo, doc.path,
                "record document changed after capture",
                "revert the content edit or re-issue as a new record"))
    return findings


def fam_staged_candidate_aging(ctx):
    findings = []
    th = ctx.thresholds

    def aged(kind, days, warn, err):
        if days is None:
            return None
        if err and days >= err:
            return ERROR
        if days >= warn:
            return WARNING
        return None

    # Staged topics: ideation/staging/<topic>/ untouched.
    for repo, repo_path in ctx.repo_paths.items():
        staging = repo_path / "ideation" / "staging"
        if not staging.is_dir():
            continue
        for topic in sorted(p for p in staging.iterdir() if p.is_dir()):
            rel = topic.relative_to(repo_path).as_posix()
            days = _age_days(ctx.as_of,
                             ctx.git.last_commit_date(repo_path, rel))
            sev = aged("staged", days, th["staged_warning_days"],
                       th["staged_error_days"])
            if sev:
                findings.append(Finding(
                    sev, "staged-candidate-aging", repo, rel,
                    f"staged topic untouched {days} days",
                    "progress the topic to a proposal or mark it deferred"))

    # Candidate blocks and supersedes markers age by their line's commit.
    for doc in ctx.docs:
        repo_path = ctx.repo_paths[doc.repo]
        for lineno, line, fenced in _scan_lines(doc.text):
            if fenced:
                continue
            bare = _strip_inline_code(line)
            if "xspec:candidate" in bare and "/xspec:candidate" not in bare:
                days = _age_days(ctx.as_of, ctx.git.line_commit_date(
                    repo_path, doc.path, lineno))
                sev = aged("candidate", days, th["candidate_warning_days"],
                           th["candidate_error_days"])
                if sev:
                    findings.append(Finding(
                        sev, "staged-candidate-aging", doc.repo, doc.path,
                        f"candidate block untouched {days} days (line {lineno})",
                        "convert the block via an OpenSpec change or drop it"))
            if "xspec:supersedes" in bare and "change=" not in bare:
                days = _age_days(ctx.as_of, ctx.git.line_commit_date(
                    repo_path, doc.path, lineno))
                sev = aged("supersedes", days, th["supersedes_warning_days"],
                           th["supersedes_error_days"])
                if sev:
                    findings.append(Finding(
                        sev, "staged-candidate-aging", doc.repo, doc.path,
                        f"supersedes without change= for {days} days "
                        f"(line {lineno})",
                        "create the OpenSpec change and add its change= id"))

    # Draft ages: distribution is report data; only the 60-day warning and
    # one aggregate info item per repo become findings, so the ranked plan
    # is not flooded (contract: age always reported, warning at 60).
    for repo, repo_path in ctx.repo_paths.items():
        ages = []
        for doc in ctx.docs:
            if doc.repo != repo or doc.status != "draft":
                continue
            days = _age_days(ctx.as_of,
                             ctx.git.last_commit_date(repo_path, doc.path))
            if days is None:
                continue
            ages.append(days)
            if days >= th["draft_warning_days"]:
                findings.append(Finding(
                    WARNING, "staged-candidate-aging", repo, doc.path,
                    f"draft without transition for {days} days",
                    "ratify, supersede, or retire the draft"))
        if ages:
            findings.append(Finding(
                INFO, "staged-candidate-aging", repo, "(drafts)",
                f"draft age distribution days: min={min(ages)} "
                f"max={max(ages)} n={len(ages)}",
                "trend data — no action required"))
    return findings


REGISTER_ALIASES = {"seed", "staged", "openspec", "implemented", "adopted",
                    "rejected", "deferred"}
REGISTER_PATH = "docs/domain-neutralization-candidate-register.md"


def fam_register_lifecycle_consistency(ctx):
    if "openxFactory" not in ctx.repo_paths:
        return Skip("register-lifecycle-consistency",
                    "openxFactory checkout not in scope")
    repo_path = ctx.repo_paths["openxFactory"]
    reg = repo_path / REGISTER_PATH
    if not reg.is_file():
        return Skip("register-lifecycle-consistency",
                    f"{REGISTER_PATH} not found")
    findings = []
    for line in reg.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*(DTN-\d+)\s*\|", line)
        if not m:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 6:
            findings.append(Finding(
                ERROR, "register-lifecycle-consistency", "openxFactory",
                REGISTER_PATH, f"{m.group(1)}: malformed register row",
                "restore the six-column register row shape"))
            continue
        status = cells[4].strip("`")
        if status not in REGISTER_ALIASES:
            findings.append(Finding(
                ERROR, "register-lifecycle-consistency", "openxFactory",
                REGISTER_PATH,
                f"{m.group(1)}: status {status!r} is not a documented alias",
                "use a documented lifecycle alias"))
        if status == "adopted" and not _resolves(
                repo_path, repo_path, cells[5].strip("`")):
            findings.append(Finding(
                WARNING, "register-lifecycle-consistency", "openxFactory",
                REGISTER_PATH,
                f"{m.group(1)}: adopted without resolvable artifact",
                "point the adopted entry at its promoted artifact"))
    return findings


# Canonical marker grammar — owned by document-lifecycle, transcribed by
# reference. Any grammar change is an upstream delta; update these regexes
# to follow, never to extend.
_CAND_OPEN = re.compile(
    r"^<!--\s*xspec:candidate((?:\s+[\w-]+=[^\s>]+)*)\s*-->$")
_CAND_CLOSE = re.compile(r"^<!--\s*/xspec:candidate\s*-->$")
_SUPERSEDES = re.compile(
    r"^<!--\s*xspec:supersedes((?:\s+[\w-]+=[^\s>]+)*)\s*-->$")
_ATTR = re.compile(r"([\w-]+)=(\S+)")
_HEADING = re.compile(r"^#{1,6}\s")


def _resolve_capability(ctx, repo: str, cap: str) -> bool:
    for name in (repo, "openxFactory"):
        if cap in ctx.capabilities.get(name, set()):
            return True
    return False


def _resolve_change(ctx, repo: str, change: str) -> bool:
    for name in (repo, "openxFactory"):
        if change in ctx.change_ids.get(name, set()):
            return True
    return False


def fam_tag_hygiene(ctx):
    findings = []

    def hit(sev, doc, rule, action):
        findings.append(Finding(sev, "tag-hygiene", doc.repo, doc.path,
                                rule, action))

    for doc in ctx.docs:
        open_line = None
        for lineno, line, fenced in _scan_lines(doc.text):
            if fenced:
                continue
            bare = _strip_inline_code(line).strip()
            if "xspec:" not in bare:
                if open_line and _HEADING.match(line):
                    hit(ERROR, doc,
                        f"candidate block crosses heading at line {lineno} "
                        f"(opened line {open_line})",
                        "close the fence before the heading "
                        "(document-lifecycle grammar)")
                    open_line = None
                continue
            if m := _CAND_OPEN.match(bare):
                attrs = dict(_ATTR.findall(m.group(1)))
                if open_line:
                    hit(ERROR, doc,
                        f"nested candidate fence at line {lineno}",
                        "candidate blocks cannot nest "
                        "(document-lifecycle grammar)")
                open_line = lineno
                target = attrs.get("target")
                if not target:
                    hit(ERROR, doc,
                        f"candidate open without target= at line {lineno}",
                        "add target=<capability> (document-lifecycle grammar)")
                elif not _resolve_capability(ctx, doc.repo, target):
                    hit(ERROR, doc,
                        f"unresolved target={target} at line {lineno}",
                        "name a capability under openspec/specs/ or an "
                        "active change (document-lifecycle grammar)")
                if doc.status == "record":
                    hit(ERROR, doc,
                        f"candidate block in a record document (line {lineno})",
                        "records are excluded from the conversion queue")
            elif _CAND_CLOSE.match(bare):
                if not open_line:
                    hit(ERROR, doc,
                        f"unmatched candidate close at line {lineno}",
                        "remove or pair the close fence "
                        "(document-lifecycle grammar)")
                open_line = None
            elif m := _SUPERSEDES.match(bare):
                attrs = dict(_ATTR.findall(m.group(1)))
                spec = attrs.get("spec")
                if not spec or "/" not in spec:
                    hit(ERROR, doc,
                        f"supersedes without spec=<capability>/<requirement> "
                        f"at line {lineno}",
                        "add the spec= attribute (document-lifecycle grammar)")
                elif not _resolve_capability(ctx, doc.repo,
                                             spec.split("/", 1)[0]):
                    hit(ERROR, doc,
                        f"unresolved supersedes spec={spec} at line {lineno}",
                        "name an existing capability "
                        "(document-lifecycle grammar)")
                change = attrs.get("change")
                if change and not _resolve_change(ctx, doc.repo, change):
                    hit(ERROR, doc,
                        f"unresolved change={change} at line {lineno}",
                        "name an existing active or archived change "
                        "(document-lifecycle grammar)")
            else:
                hit(ERROR, doc,
                    f"malformed xspec: marker at line {lineno}",
                    "use one of the three canonical marker forms "
                    "(document-lifecycle grammar)")
        if open_line:
            hit(ERROR, doc,
                f"unclosed candidate fence opened at line {open_line}",
                "add the matching /xspec:candidate close fence "
                "(document-lifecycle grammar)")

    # No doc-level candidacy status anywhere.
    for doc in ctx.docs:
        if doc.status == "spec-candidate":
            hit(ERROR, doc, "doc-level spec-candidate status",
                "candidacy is block-level only; remove the status value")
    return findings


def fam_submodule_pin_drift(ctx):
    if ctx.agg_root is None:
        return Skip("submodule-pin-drift",
                    "single-repo run: no aggregation checkout")
    pins = ctx.git.gitlink_pins(ctx.agg_root)
    if pins is None:
        return Skip("submodule-pin-drift",
                    "aggregation checkout is not a git repository")
    findings = []
    for path, pinned in sorted(pins.items()):
        sub = ctx.agg_root / path
        remote = ctx.git.remote_main_sha(sub)
        if remote is None:
            findings.append(Finding(
                INFO, "submodule-pin-drift", "xFactory", path,
                "remote main unreachable; drift not checked",
                "re-run with network access to the submodule remote"))
        elif remote != pinned:
            findings.append(Finding(
                WARNING, "submodule-pin-drift", "xFactory", path,
                f"pin {pinned[:12]} differs from remote main {remote[:12]}",
                "sync the submodule pointer or push the submodule"))
    return findings


def fam_contract_copy_drift(ctx):
    openx = ctx.repo_paths.get("openxFactory")
    if openx is None:
        return Skip("contract-copy-drift",
                    "openxFactory checkout not in scope")
    head = ctx.git.head_sha(openx)
    if head is None:
        return Skip("contract-copy-drift", "openxFactory git state unreadable")
    findings = []
    for repo, repo_path in sorted(ctx.repo_paths.items()):
        stack = repo_path / "stack.yaml"
        if repo == "openxFactory" or not stack.is_file():
            continue
        m = re.search(r"^\s*contract_ref:\s*([0-9a-f]{40})\s*$",
                      stack.read_text(encoding="utf-8"), re.M)
        if m and m.group(1) != head:
            findings.append(Finding(
                WARNING, "contract-copy-drift", repo, "stack.yaml",
                f"openxFactory pin {m.group(1)[:12]} differs from canonical "
                f"HEAD {head[:12]}",
                "review upstream contract changes and re-pin"))
    return findings


_SYNC_OP = re.compile(r"^\[[^\]]+\]\s+(ADD|DEL|UPD)\s")


def fam_notebook_projection_drift(ctx):
    output = ctx.notebook_dryrun()
    if output is None:
        return Skip("notebook-projection-drift",
                    "nlm unauthenticated or sync unavailable; family runs "
                    "in operator-triggered runs only")
    ops = [l for l in output.splitlines() if _SYNC_OP.match(l)]
    if not ops:
        return []
    return [Finding(
        WARNING, "notebook-projection-drift", "xFactory",
        "(lifecycle notebooks)",
        f"projection dry-run reports {len(ops)} pending operations",
        "run the lifecycle notebook sync with --apply")]


# --------------------------------------------------------------------------
# staged-topic-template (add-staged-topic-outline-template, ratified 2026-08-15)
#
# A staged topic's primary fragment carries a required template so its live
# state is extractable without opening the whole folder. This family reports
# non-conformance and DELIBERATELY NEVER BLOCKS A GATE — Q2's ruling was
# "doc-health treats non-conformance as a nudge, never a gate-blocking
# finding", so every finding here is WARNING even for a topic where conformance
# is REQUIRED. The required/opt-in distinction lives in the rule TEXT, which is
# what a reader acts on, rather than in a severity that would fail a run.
# Escalating this family to ERROR needs a new ruling, not a judgement call.

TEMPLATE_RATIFIED = date(2026, 8, 15)

# Matched case-insensitively against `## ` headings; a heading may carry a
# parenthetical suffix (the canonical skeleton's own idea-notes heading does).
_TEMPLATE_SECTIONS = (
    ("idea notes", "pre-document idea notes"),
    ("conflicts", "conflicts"),
    ("open questions", "open questions"),
)
_QUESTION_SUBFIELDS = ("Context", "Recommended answer", "Explanation",
                       "Disposition status")


def _primary_fragment(topic: Path) -> Path | None:
    """Mirror of `primaryFragmentPath` in wheel-model.js: the exact
    `<topic>.md` first, else the shallowest markdown file. Path-only, never
    content-sniffed — the one-path rule this template contract preserves."""
    mds = sorted(p for p in topic.rglob("*.md"))
    if not mds:
        return None
    named = f"{topic.name.lower()}.md"
    for path in mds:
        if path.name.lower() == named:
            return path
    return min(mds, key=lambda p: (len(p.relative_to(topic).parts), str(p)))


def _template_gaps(text: str) -> list[str]:
    """Which template obligations this fragment does not meet."""
    gaps = []
    headings, in_fence = [], False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence and line.startswith("## "):
            headings.append(line[3:].strip().lower())
    for needle, label in _TEMPLATE_SECTIONS:
        if not any(needle in h for h in headings):
            gaps.append(f"no {label} section")

    # Every `### Q...` under Open questions carries all four sub-fields. The
    # fragment is scanned outside fences for the same reason the headings are:
    # the canonical skeleton is itself a fenced example.
    in_questions, in_fence, current, seen = False, False, None, {}
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.startswith("## "):
            in_questions = "open questions" in line[3:].strip().lower()
            current = None
        elif in_questions and line.startswith("### "):
            current = line[4:].strip()
            seen[current] = set()
        elif current is not None:
            for field in _QUESTION_SUBFIELDS:
                if line.startswith(f"{field}:"):
                    seen[current].add(field)
    for question, fields in seen.items():
        missing = [f for f in _QUESTION_SUBFIELDS if f not in fields]
        if missing:
            short = question if len(question) <= 48 else question[:45] + "..."
            gaps.append(f"question '{short}' lacks {', '.join(missing)}")
    return gaps


def fam_staged_topic_template(ctx):
    findings = []
    for repo, repo_path in sorted(ctx.repo_paths.items()):
        staging = repo_path / "ideation" / "staging"
        if not staging.is_dir():
            continue
        for topic in sorted(p for p in staging.iterdir() if p.is_dir()):
            primary = _primary_fragment(topic)
            if primary is None:
                continue  # an empty topic folder is another family's business
            rel = primary.relative_to(repo_path).as_posix()
            gaps = _template_gaps(primary.read_text(errors="replace"))
            if not gaps:
                continue
            # Obligation follows the topic's STAGING date, never its last
            # touch: editing an opt-in topic for an unrelated reason must not
            # silently make it required. An unknown date is treated as opt-in.
            staged_on = ctx.git.first_commit_date(repo_path, rel)
            required = staged_on is not None and staged_on >= TEMPLATE_RATIFIED
            scope = ("staged after the template ratified, so conformance is "
                     "REQUIRED") if required else (
                     "staged before the template ratified, so conformance is "
                     "opt-in — rewrite it when the topic is next worked")
            findings.append(Finding(
                WARNING, "staged-topic-template", repo, rel,
                f"primary fragment does not meet the outline template "
                f"({'; '.join(gaps)}) — {scope}",
                "add the missing sections, or give every open question its "
                "Context / Recommended answer / Explanation / Disposition "
                "status sub-fields"))
    return findings


FAMILIES = {
    "status-validity": fam_status_validity,
    "staged-topic-template": fam_staged_topic_template,
    "standard-backing": fam_standard_backing,
    "ratified-provenance": fam_ratified_provenance,
    "succession-integrity": fam_succession_integrity,
    "location-conformance": fam_location_conformance,
    "record-immutability": fam_record_immutability,
    "staged-candidate-aging": fam_staged_candidate_aging,
    "register-lifecycle-consistency": fam_register_lifecycle_consistency,
    "tag-hygiene": fam_tag_hygiene,
    "submodule-pin-drift": fam_submodule_pin_drift,
    "contract-copy-drift": fam_contract_copy_drift,
    "notebook-projection-drift": fam_notebook_projection_drift,
    "document-catalog": document_catalog.fam_document_catalog,
    "ideation-routing": ideation_routing.fam_ideation_routing,
    "proposal-origin": proposal_origin.fam_proposal_origin,
    "client-identity-composition":
        client_identity_composition.fam_client_identity_composition,
    # The eighteenth family (add-promotion-fidelity-check). Deliberately
    # ABSENT from FAMILY_RESOLUTION above: it launches ADVISORY, and a
    # `contested` class would route it back into `report.uncited_resolutions`
    # — an ERROR — the first time one of its findings was resolved. See
    # `promotion_fidelity._LAUNCH_SEVERITY`.
    "promotion-fidelity": promotion_fidelity.fam_promotion_fidelity,
}
