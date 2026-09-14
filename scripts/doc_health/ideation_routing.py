"""Fourteenth deterministic doc-health family: ideation-routing integrity
(add-cross-factory-ideation-routing; change tasks 4.1-4.4).

Realizes the openxFactory `ideation-routing` and related `document-lifecycle`
requirements' deterministic surface by reference (doc-health delta
"Ideation-routing checks enforced by reference"): validates the routing
records, the central Idea-ID allocation ledger, structured repository
references, Markdown provenance pointers, and proposal provenance against the
promoted routing contract — never choosing an owner, splitting a claim,
accepting a destination, moving a document, disposing an organizer
recommendation, or promoting policy (delta: those decisions are `contested`,
never auto-fixed).

The controlled vocabularies, transition graphs, and shape rules below are
TRANSCRIBED by reference from the four promoted openxFactory schemas
(`contracts/schemas/xfactory-idea-routing-record.schema.yaml`,
`xfactory-idea-routing-reference.schema.yaml`,
`xfactory-ideation-routing-index.schema.yaml`,
`xfactory-ideation-organizer-recommendations.schema.yaml`) and the promoted
`ideation-routing` / `document-lifecycle` specs — never extended here. This
mirrors how `families.py` transcribes the document-lifecycle tag grammar and
how `document_catalog.py` transcribes the catalog controlled vocabularies: the
owning requirement is followed by reference, and a later OpenSpec change that
edits the promoted contract is followed by updating these transcriptions, never
a stale staged fragment (delta scenario "Routing contract evolves").

Finding classes, encoded as a ``[<class>] `` prefix on each finding's ``rule``
(the same convention `document_catalog.py` uses so tests and report consumers
can select one check's findings — the ``Finding`` dataclass has no dedicated
check field):

    schema, transition, transition-chain, claim-id, duplicate-claim,
    duplicate-idea, central-allocation, blocker, routed-acceptance, reference,
    path-normalization, paired-document, destination-provenance, copied-record,
    staged-pointer, proposal-provenance, aggregation-backlog, external-path,
    aging

Resolution semantics (delta "Ideation-routing checks enforced by reference"):
the family MAY auto-fix ONLY safe mechanical defects — path-separator
normalization — so ``path-normalization`` findings are ``auto-fixable`` and the
purely informational ``external-path`` skips carry no state change; every other
class requires a reviewed routing decision (choosing an owner, accepting a
destination, splitting a claim, or otherwise editing a governed routing record)
and is therefore ``contested`` and never auto-fixed (delta scenario "Ownership
decision is incomplete"). Because the classes are a deliberate mix, this family
is intentionally ABSENT from ``families.FAMILY_RESOLUTION`` (which would force a
single resolution onto every class); it sets ``resolution`` per finding, exactly
like ``document_catalog.py``.

Scope (delta "Deterministic check families" / repository-resolution rules): the
family scans the governed openxFactory and DomainxFactory corpus for routing
artifacts, inspects the xFactory aggregation root ONLY for forbidden ideation
placement and locator integrity, and resolves referenced install/runtime paths
without treating those repositories as governance corpora. Ordinary documents
and known-owner brainstorms with no routing sidecar are invisible to this family
(delta scenario "Ordinary document lacks routing metadata"; spec "Prospective
compatibility and migration").
"""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

from . import (AUTO_FIXABLE, CONTESTED, ERROR, INFO, WARNING, Finding, Skip)
from .corpus import ROOT_LEVEL_GOVERNED_PRODUCTS

try:  # PyYAML is the suite's one optional dependency (runner/semantic do the same).
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

FAMILY = "ideation-routing"

# --- transcribed contract constants (by reference; never extended here) -------

RECORD_KIND = "xfactory_idea_routing_record"
INDEX_KIND = "xfactory_ideation_routing_index"
# Organizer recommendation evidence (kind `ideation_organizer_recommendations`)
# is validated by the separate ideation-organizer lane's own output validator
# (add-cross-factory-ideation-routing tasks 5-7), not this deterministic family
# — the delta's enumerated family checks do not include organizer output.

# Controlled vocabularies (record schema `scope` / `routing_status` enums; claim
# `disposition` enum). Routing metadata MUST NOT replace the document `Status:`
# taxonomy — these are a separate controlled set.
SCOPES = frozenset({"unclassified", "domain", "cross_domain",
                    "neutral_candidate", "mixed"})
ROUTING_STATUSES = frozenset({"intake", "triaging", "split", "routed",
                              "deferred", "rejected"})
CLAIM_DISPOSITIONS = frozenset({"unresolved", "proposed", "routed",
                                "deferred", "rejected"})

# Append-only transition graphs (record schema `routing_transition` /
# `claim_transition` per-edge `allOf`). Key `None` is the initial edge.
ROUTING_EDGES = {
    None: {"intake"},
    "intake": {"triaging", "deferred", "rejected"},
    "triaging": {"split", "routed", "deferred", "rejected"},
    "split": {"triaging", "routed", "deferred", "rejected"},
    "routed": {"triaging"},
    "deferred": {"triaging"},
    "rejected": {"triaging"},
}
CLAIM_EDGES = {
    None: {"unresolved"},
    "unresolved": {"proposed", "deferred", "rejected"},
    "proposed": {"routed", "deferred", "rejected"},
    "routed": {"unresolved"},
    "deferred": {"unresolved"},
    "rejected": {"unresolved"},
}

# Routing statuses that age as unresolved work (aging-threshold defaults). A
# `split` record ages only while incomplete (any active claim). `routed`,
# `rejected`, and explicitly `deferred` records SHALL NOT age.
AGING_ALWAYS = frozenset({"intake", "triaging"})
ACTIVE_CLAIM_DISPOSITIONS = frozenset({"unresolved", "proposed"})

# Identity grammars (reference kernel `$defs`).
IDEA_ID_RE = re.compile(r"^XFI-[0-9]{4}-[0-9]{3}$")
CLAIM_ID_RE = re.compile(r"^XFI-[0-9]{4}-[0-9]{3}-C[0-9]{2}$")
FULL_REVISION_RE = re.compile(r"^([0-9a-f]{40}|[0-9a-f]{64})$")
PASSAGE_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
PENDING_CAPTURE = "pending_capture"

# Aggregation-layout convention fallback (standalone clone with no aggregation
# `.gitmodules` ancestor) — same shapes the openxFactory validator accepts.
CONVENTION_DOMAIN_RE = re.compile(r"^xFactories/[^/]+$")
CONVENTION_INSTALL_RE = re.compile(r"^installs/[^/]+$")

# Paired human-readable document names a routing.yaml sits beside
# (`inbox/<idea-id>/idea.md`; `cross-domain/<idea-id>/routing-summary.md`).
PAIRED_DOC_NAMES = ("idea.md", "routing-summary.md")

ROUTING_WARNING_DAYS_DEFAULT = 30
ROUTING_ERROR_DAYS_DEFAULT = 90

# Markdown provenance headers (organize gate + document-lifecycle delta).
_IDEA_ID_HEADER_RE = re.compile(r"^Idea ID:\s*(\S+)\s*$")
_SOURCE_IDEA_IDS_RE = re.compile(r"^Source Idea IDs:\s*(.+?)\s*$")
_CLAIM_IDS_RE = re.compile(r"^Claim IDs:\s*(.+?)\s*$")
_ROUTING_RECORDS_RE = re.compile(r"^Routing records:\s*(.+?)\s*$")


def _finding(cls, severity, repo, path, detail, action,
             resolution=CONTESTED):
    return Finding(severity, FAMILY, repo, path, f"[{cls}] {detail}", action,
                   resolution=resolution)


# --- YAML loading (malformed data is reported, never fatal) -------------------

class _RoutingParseError(Exception):
    pass


def _load_yaml(path: Path):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:  # type: ignore[union-attr]
        raise _RoutingParseError(str(exc)) from exc


# --- structured-reference iteration and repository resolution -----------------

def _iter_refs(node):
    """Yield every structured reference object (any mapping carrying a string
    `repository` key) anywhere in `node`: sources, destinations,
    committed/path references, ideation-provenance routing records, organizer
    source refs, and structured evidence refs. Bare owner/candidate strings are
    never references and are never yielded (validator `iter_repo_refs`
    precedent)."""
    if isinstance(node, dict):
        if isinstance(node.get("repository"), str):
            yield node
        for value in node.values():
            yield from _iter_refs(value)
    elif isinstance(node, list):
        for item in node:
            yield from _iter_refs(item)


def _parse_gitmodules_paths(gm: Path) -> list[str]:
    paths = []
    try:
        text = gm.read_text(encoding="utf-8")
    except OSError:
        return paths
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("path"):
            _, _, value = stripped.partition("=")
            value = value.strip()
            if value:
                paths.append(value)
    return paths


def _known_repositories(ctx):
    """(known_ids, mode, agg_root). Repository IDs resolve as the spec defines:
    reserved root `xFactory`, or an exact aggregation-relative `.gitmodules`
    submodule path resolved through its gitlink. With an aggregation checkout
    (`ctx.agg_root`) the `.gitmodules` membership is authoritative; a single-repo
    self-gate falls back to the recognized aggregation-layout convention and the
    mode is disclosed so the external-path/materialization checks report skips
    rather than silent passes."""
    agg = ctx.agg_root
    if agg is not None:
        gm = Path(agg) / ".gitmodules"
        if gm.is_file():
            paths = _parse_gitmodules_paths(gm)
            if any(p == "openxFactory" or p.startswith("xFactories/")
                   for p in paths):
                known = set(paths) | {"openxFactory", "xFactory"}
                return known, "gitmodules", Path(agg)
    # Convention fallback: the governed repos in scope, the recognized
    # aggregation-layout shapes accepted by pattern, and the root-level neutral
    # products, which have no pattern to be accepted by — their aggregation
    # id is a BARE NAME, indistinguishable by shape from a typo, so the
    # allowlist is the only thing that can admit them (membership beyond scope
    # is a strict-gate concern reported as skipped).
    known = (set(ctx.repo_paths) | {"openxFactory", "xFactory"}
             | set(ROOT_LEVEL_GOVERNED_PRODUCTS))
    return known, "convention", (Path(agg) if agg is not None else None)


def _governed_repo_ids(ctx) -> set[str]:
    """Aggregation-relative repository IDs of the governed doc repos in scope:
    openxFactory, `xFactories/<Name>` for each DomainxFactory
    (`corpus.discover_repos` convention), and every root-level neutral product
    on `corpus.ROOT_LEVEL_GOVERNED_PRODUCTS`. References into these are
    resolvable without materialization; only pinned install/runtime repositories
    are `external` and subject to the nightly-skip / strict-materialization
    check.

    WHY THE ROOT PRODUCTS ARE ADMITTED UNCONDITIONALLY, not derived from
    `ctx.repo_paths` like the other two. `discover_repos` widened at `804a9170`
    (PR #890, closing #869) to enumerate every materialized product on
    `ROOT_LEVEL_GOVERNED_PRODUCTS`, so a root-level product now DOES appear in
    `repo_paths` whenever this run has it checked out — but membership is still
    sourced from the allowlist, not derived from that fact. The allowlist is a
    statement about the aggregation's TOPOLOGY, which is true whether or not
    this particular run has the product checked out; the materialization
    question is asked separately and by a different check.

    The `repo_paths` loop tolerates an allowlisted name defensively rather than
    prefixing it `xFactories/`: if `discover_repos` is ever widened to sweep a
    root-level product's own documents, the two sites must not disagree about
    that product's ID, and a silent `xFactories/openXwallet` would be a
    repository that exists nowhere.
    """
    ids = set(ROOT_LEVEL_GOVERNED_PRODUCTS)
    for name in ctx.repo_paths:
        if name == "openxFactory" or name in ROOT_LEVEL_GOVERNED_PRODUCTS:
            ids.add(name)
        else:
            ids.add(f"xFactories/{name}")
    return ids


def _repository_unknown_reason(repo, known, mode) -> str | None:
    """Reason `repo` is not a resolvable aggregation repository ID, or None if it
    resolves (spec "Structured repository references and resolvable provenance":
    reserved `xFactory` root or an aggregation-relative `.gitmodules` submodule
    path)."""
    if repo == "xFactory":
        return None
    if mode == "gitmodules":
        if repo in known:
            return None
        return (f"repository {repo!r} is neither the reserved 'xFactory' root "
                "nor a known aggregation .gitmodules submodule path")
    if (repo in known or repo == "openxFactory"
            or CONVENTION_DOMAIN_RE.match(repo)
            or CONVENTION_INSTALL_RE.match(repo)):
        return None
    return (f"repository {repo!r} is not a recognized aggregation repository id "
            "(reserved 'xFactory', 'openxFactory', 'xFactories/<Name>', "
            "'installs/<name>', or a root-level neutral product: "
            + ", ".join(repr(n) for n in ROOT_LEVEL_GOVERNED_PRODUCTS) + ")")


def _posix_path_reason(path: str) -> str | None:
    """Reason a structured reference path is not a POSIX repository-relative
    path, or None (reference kernel `posix_relative_path`: absolute paths,
    `..` traversal, and backslashes are invalid). Backslash is reported
    separately by the caller as a safely normalizable defect."""
    if path.startswith("/"):
        return "absolute path"
    if re.search(r"(^|/)\.\.(/|$)", path):
        return "path traversal (..)"
    return None


# --- per-record deterministic checks ------------------------------------------

def _shape_findings(repo, path, record) -> list[Finding]:
    """Schema/vocabulary conformance transcribed from
    xfactory-idea-routing-record.schema.yaml: envelope, controlled
    vocabularies, per-edge transition legality, intake-only `pending_capture`,
    multi-source deduplication, the routed-record gate, and the claim
    disposition conditionals (blocker / proposed-owner / routed completeness).
    """
    out = []

    def bad(cls, detail, action):
        out.append(_finding(cls, ERROR, repo, path, detail, action))

    if not isinstance(record, dict):
        bad("schema", "routing record is not a YAML mapping",
            "restore the routing-record shape or remove the file")
        return out
    if record.get("kind") != RECORD_KIND:
        bad("schema", f"kind {record.get('kind')!r} is not {RECORD_KIND!r}",
            "declare the canonical routing-record kind")
    if record.get("schema_version") != 1:
        bad("schema",
            f"schema_version {record.get('schema_version')!r} is not 1",
            "pin schema_version: 1 per the promoted routing-record schema")

    idea = record.get("idea_id")
    if not (isinstance(idea, str) and IDEA_ID_RE.match(idea)):
        bad("schema", f"idea_id {idea!r} is not XFI-<year>-<3-digit-sequence>",
            "allocate a central Idea ID matching the promoted grammar")

    scope = record.get("scope")
    if scope not in SCOPES:
        bad("schema", f"scope {scope!r} is outside the controlled vocabulary "
            f"({', '.join(sorted(SCOPES))})",
            "record a controlled routing scope")
    status = record.get("routing_status")
    if status not in ROUTING_STATUSES:
        bad("schema", f"routing_status {status!r} is outside the controlled "
            f"vocabulary ({', '.join(sorted(ROUTING_STATUSES))})",
            "record a controlled routing status")

    sources = record.get("sources")
    if not isinstance(sources, list) or not sources:
        bad("schema", "sources is missing or empty (at least one origin "
            "source is required)",
            "list every source the routing record derives from")
        sources = []
    for i, source in enumerate(sources):
        if not isinstance(source, dict):
            bad("schema", f"sources[{i}] is not a structured reference",
                "record repository/path/revision for every source")
            continue
        revision = source.get("revision")
        if revision == PENDING_CAPTURE:
            if status != "intake":
                bad("schema",
                    f"sources[{i}] uses pending_capture at routing_status "
                    f"{status!r}; it is admissible only during intake",
                    "commit the source revision before leaving intake")
        elif not (isinstance(revision, str) and FULL_REVISION_RE.match(revision)):
            bad("schema",
                f"sources[{i}] revision {revision!r} is not pending_capture nor "
                "a full committed revision",
                "pin a full committed revision (or pending_capture in intake)")

    if isinstance(sources, list) and len(sources) >= 2:
        dedup = record.get("deduplication_rationale")
        if not (isinstance(dedup, str) and dedup.strip()):
            bad("schema", "multiple sources without a deduplication_rationale",
                "record why the sources are one canonical idea")

    claims = record.get("claims") or []
    if not isinstance(claims, list):
        bad("schema", "claims is not a list", "record claims as a list")
        claims = []
    for claim in claims:
        out.extend(_claim_shape_findings(repo, path, idea, claim))

    # Routed-record gate: no active claim may remain unresolved/proposed.
    if status == "routed":
        for claim in claims:
            if isinstance(claim, dict) and \
                    claim.get("disposition") in ACTIVE_CLAIM_DISPOSITIONS:
                bad("schema",
                    f"record is routed while claim {claim.get('claim_id')!r} is "
                    f"{claim.get('disposition')!r}",
                    "resolve or defer every active claim before routing the "
                    "record")

    out.extend(_transition_edge_findings(
        repo, path, "routing", record.get("transitions"), status, ROUTING_EDGES))
    return out


def _claim_shape_findings(repo, path, idea, claim) -> list[Finding]:
    out = []

    def bad(cls, detail, action):
        out.append(_finding(cls, ERROR, repo, path, detail, action))

    if not isinstance(claim, dict):
        bad("schema", "a claim is not a YAML mapping",
            "record each claim as a mapping")
        return out
    cid = claim.get("claim_id")
    if not (isinstance(cid, str) and CLAIM_ID_RE.match(cid)):
        bad("schema", f"claim_id {cid!r} is not <idea-id>-C<2-digit-sequence>",
            "assign a Claim ID derived from the record's Idea ID")
    disposition = claim.get("disposition")
    if disposition not in CLAIM_DISPOSITIONS:
        bad("schema", f"claim {cid!r} disposition {disposition!r} is outside the "
            f"controlled vocabulary ({', '.join(sorted(CLAIM_DISPOSITIONS))})",
            "record a controlled claim disposition")

    # Disposition conditionals (record schema claim `allOf`).
    if disposition == "unresolved":
        blocker = claim.get("blocker")
        if not (isinstance(blocker, str) and blocker.strip()):
            bad("blocker",
                f"unresolved claim {cid!r} names no blocker or blocking question",
                "name the blocker keeping the claim unresolved, or dispose it")
    elif disposition == "proposed":
        if not (isinstance(claim.get("proposed_owner"), str)
                and claim["proposed_owner"].strip()):
            bad("routed-acceptance",
                f"proposed claim {cid!r} names no proposed_owner",
                "name the proposed owner or return the claim to unresolved")
    elif disposition == "routed":
        for field in ("accepted_owner", "target_capability"):
            if not (isinstance(claim.get(field), str) and claim[field].strip()):
                bad("routed-acceptance",
                    f"routed claim {cid!r} has no {field}",
                    "record destination-owner acceptance before routing a claim")
        dest = claim.get("destination")
        if not isinstance(dest, dict):
            bad("routed-acceptance",
                f"routed claim {cid!r} has no structured destination",
                "record the committed destination reference for the routed claim")
        acceptance = claim.get("acceptance")
        if not (isinstance(acceptance, dict)
                and isinstance(acceptance.get("evidence_refs"), list)
                and acceptance.get("evidence_refs")
                and acceptance.get("actor_ref") and acceptance.get("accepted_at")):
            bad("routed-acceptance",
                f"routed claim {cid!r} has no destination-owner acceptance "
                "(actor, time, and evidence)",
                "record the acceptance actor, time, and evidence")

    out.extend(_transition_edge_findings(
        repo, path, f"claim {cid}", claim.get("transitions"), disposition,
        CLAIM_EDGES))
    return out


def _transition_edge_findings(repo, path, label, transitions, terminal,
                              edges) -> list[Finding]:
    """Per-edge transition legality (schema `allOf`) plus append-only history
    contiguity (validator `check_transition_chains`): first `from` is null, each
    `from` equals the previous `to`, every edge is legal, and the last `to`
    equals the current state."""
    out = []
    if not isinstance(transitions, list) or not transitions:
        out.append(_finding(
            "schema", ERROR, repo, path,
            f"{label} has no transition history (at least one is required)",
            "record the append-only transition history"))
        return out
    prev_to = "<none>"
    for i, transition in enumerate(transitions):
        if not isinstance(transition, dict):
            out.append(_finding(
                "schema", ERROR, repo, path,
                f"{label} transition[{i}] is not a mapping",
                "record each transition as a mapping"))
            continue
        frm, to = transition.get("from"), transition.get("to")
        if i == 0:
            if frm is not None:
                out.append(_finding(
                    "transition-chain", ERROR, repo, path,
                    f"{label} first transition.from must be null, got {frm!r}",
                    "begin the append-only history at null"))
        elif frm != prev_to:
            out.append(_finding(
                "transition-chain", ERROR, repo, path,
                f"{label} transition[{i}].from {frm!r} != previous "
                f"transition.to {prev_to!r} (history is not append-only)",
                "keep the transition history contiguous and append-only"))
        allowed = edges.get(frm)
        if allowed is None:
            out.append(_finding(
                "transition", ERROR, repo, path,
                f"{label} transition[{i}] has an unknown from-state {frm!r}",
                "use a controlled transition edge"))
        elif to not in allowed:
            out.append(_finding(
                "transition", ERROR, repo, path,
                f"{label} illegal transition {frm!r} -> {to!r} "
                f"(allowed: {', '.join(sorted(allowed))})",
                "follow the promoted transition graph"))
        prev_to = to
    if prev_to != terminal:
        out.append(_finding(
            "transition-chain", ERROR, repo, path,
            f"{label} last transition.to {prev_to!r} != current state "
            f"{terminal!r}",
            "end the transition history at the current state"))
    return out


def _claim_id_findings(repo, path, record) -> list[Finding]:
    """Claim-ID prefix agreement and intra-record uniqueness (validator
    `check_claim_ids`): each Claim ID derives from the record's Idea ID, and no
    Claim ID is defined twice in one record."""
    out = []
    idea = record.get("idea_id")
    seen: dict[str, int] = {}
    for claim in record.get("claims") or []:
        if not isinstance(claim, dict):
            continue
        cid = claim.get("claim_id")
        if not isinstance(cid, str):
            continue
        if isinstance(idea, str) and not cid.startswith(f"{idea}-C"):
            out.append(_finding(
                "claim-id", ERROR, repo, path,
                f"claim {cid!r} does not derive from record idea_id {idea!r} "
                f"(must be '{idea}-C<NN>')",
                "align the Claim ID prefix with the record's Idea ID"))
        seen[cid] = seen.get(cid, 0) + 1
    for cid, count in sorted(seen.items()):
        if count > 1:
            out.append(_finding(
                "duplicate-claim", ERROR, repo, path,
                f"claim id {cid!r} is defined {count} times in one record",
                "define each Claim ID exactly once"))
    return out


def _reference_findings(repo, path, node, known, mode) -> list[Finding]:
    """Structured repository-reference resolution (validator
    `check_reference_resolution`, extended with the path-separator
    normalization split the delta requires): every reference's repository ID
    resolves and its path is POSIX repository-relative. A backslash-only defect
    is `auto-fixable` (delta scenario "Safe path defect is found"); an absolute
    path or `..` traversal is a `contested` reference defect (scenario
    "Reference escapes a repository")."""
    out = []
    for ref in _iter_refs(node):
        repo_id = ref["repository"]
        reason = _repository_unknown_reason(repo_id, known, mode)
        if reason is not None:
            out.append(_finding(
                "reference", ERROR, repo, path,
                f"structured reference {reason}",
                "point the reference at a resolvable aggregation repository id"))
        ref_path = ref.get("path")
        if not isinstance(ref_path, str) or not ref_path:
            out.append(_finding(
                "reference", ERROR, repo, path,
                f"structured reference into {repo_id!r} has no path",
                "record a POSIX repository-relative path"))
            continue
        if "\\" in ref_path:
            normalized = ref_path.replace("\\", "/")
            if _posix_path_reason(normalized) is None:
                out.append(_finding(
                    "path-normalization", WARNING, repo, path,
                    f"reference path {ref_path!r} uses a backslash separator",
                    "normalize the path separator to POSIX '/'",
                    resolution=AUTO_FIXABLE))
            else:
                out.append(_finding(
                    "reference", ERROR, repo, path,
                    f"reference path {ref_path!r} is not POSIX "
                    "repository-relative even after separator normalization",
                    "record a POSIX repository-relative path"))
            continue
        posix_reason = _posix_path_reason(ref_path)
        if posix_reason is not None:
            out.append(_finding(
                "reference", ERROR, repo, path,
                f"reference path {ref_path!r} is invalid: {posix_reason}",
                "record a POSIX repository-relative path"))
    return out


def _paired_document_findings(ctx, repo, repo_path, rel_path, record) \
        -> list[Finding]:
    """Paired-document identity (validator `check_paired_documents`; spec
    scenario "Routing begins": the human-readable source and routing record MUST
    agree on the Idea ID). A routing.yaml under an Idea-ID-named directory pairs
    with a human-readable document that agrees on the Idea ID; a paired document
    with no `Idea ID:` header at all is left valid (prospective compatibility)."""
    out = []
    idea = record.get("idea_id")
    directory = (repo_path / rel_path).parent
    dirname = directory.name
    if IDEA_ID_RE.match(dirname) and dirname != idea:
        out.append(_finding(
            "paired-document", ERROR, repo, rel_path,
            f"routing record idea_id {idea!r} does not match its directory "
            f"{dirname!r}",
            "align the routing directory name with the record's Idea ID"))
    paired = [directory / name for name in PAIRED_DOC_NAMES
              if (directory / name).is_file()]
    if not paired:
        out.append(_finding(
            "paired-document", ERROR, repo, rel_path,
            "routing record has no paired human-readable document "
            f"({' or '.join(PAIRED_DOC_NAMES)}) in the same directory",
            "add the paired idea.md or routing-summary.md"))
        return out
    for doc_path in paired:
        header = _first_idea_id_header(
            doc_path.read_text(encoding="utf-8", errors="replace"))
        if header is not None and header != idea:
            out.append(_finding(
                "paired-document", ERROR, repo,
                str(doc_path.relative_to(repo_path).as_posix()),
                f"paired document declares Idea ID {header!r} but the routing "
                f"record idea_id is {idea!r}",
                "make the paired document and routing record agree on the "
                "Idea ID"))
    return out


def _first_idea_id_header(text: str) -> str | None:
    for _, line, fenced in _scan_lines(text):
        if fenced:
            continue
        m = _IDEA_ID_HEADER_RE.match(_strip_inline_code(line).strip())
        if m:
            return m.group(1)
    return None


# --- corpus (cross-file) checks -----------------------------------------------

def _central_allocation_findings(records, index, index_repo, ctx) \
        -> list[Finding]:
    """Central Idea-ID allocation (validator `check_central_allocation`; spec
    "Canonical routing identity and record"): every routing record's Idea ID is
    allocated in the central `ideation/routing-index.yaml`, duplicate
    allocations are rejected, and an allocation pointer into a materialized repo
    resolves to a real file."""
    out = []
    allocations = (index or {}).get("allocations") or []
    allocated: dict[str, int] = {}
    alloc_records: dict[str, dict] = {}
    for entry in allocations:
        if not isinstance(entry, dict):
            continue
        iid = entry.get("idea_id")
        if not isinstance(iid, str):
            continue
        allocated[iid] = allocated.get(iid, 0) + 1
        alloc_records[iid] = entry.get("routing_record") or {}
    for iid, count in sorted(allocated.items()):
        if count > 1:
            out.append(_finding(
                "central-allocation", ERROR, index_repo or "openxFactory",
                "ideation/routing-index.yaml",
                f"idea {iid!r} is allocated {count} times (collision — the "
                "later change must rebase and allocate a new sequence)",
                "remove the duplicate allocation and rebase"))
    if index is not None:
        for repo, rel, record in records:
            iid = record.get("idea_id")
            if isinstance(iid, str) and iid not in allocated:
                out.append(_finding(
                    "central-allocation", ERROR, repo, rel,
                    f"idea {iid!r} is not allocated in the central "
                    "routing-index",
                    "allocate the Idea ID in openxFactory/ideation/"
                    "routing-index.yaml in the same change"))
    # Allocation pointers into openxFactory (in scope) must resolve to a file.
    openx_path = ctx.repo_paths.get("openxFactory")
    if openx_path is not None:
        for iid, rr in sorted(alloc_records.items()):
            if rr.get("repository") == "openxFactory" and \
                    isinstance(rr.get("path"), str):
                if not (openx_path / rr["path"]).is_file():
                    out.append(_finding(
                        "central-allocation", ERROR,
                        index_repo or "openxFactory",
                        "ideation/routing-index.yaml",
                        f"idea {iid!r} points at openxFactory/{rr['path']} "
                        "which does not exist",
                        "point the allocation at the committed routing record"))
    return out


def _one_canonical_findings(records) -> list[Finding]:
    """One canonical routing record per idea (validator `check_one_canonical`;
    spec "Canonical routing identity and record")."""
    out = []
    by_idea: dict[str, list[tuple[str, str]]] = {}
    for repo, rel, record in records:
        iid = record.get("idea_id")
        if isinstance(iid, str):
            by_idea.setdefault(iid, []).append((repo, rel))
    for iid, locs in sorted(by_idea.items()):
        if len(locs) > 1:
            where = ", ".join(f"{r}:{p}" for r, p in sorted(locs))
            for repo, rel in sorted(locs):
                out.append(_finding(
                    "duplicate-idea", ERROR, repo, rel,
                    f"idea {iid!r} has {len(locs)} canonical routing records "
                    f"({where}); copies drift and create competing routing "
                    "state",
                    "keep exactly one canonical routing record per idea"))
    return out


def _corpus_claim_uniqueness_findings(records) -> list[Finding]:
    """A Claim ID is defined once in the governed corpus (validator
    `check_corpus_claim_uniqueness`). Lightweight Markdown references and fenced
    examples are never definitions and are excluded by construction — only
    claims defined INSIDE routing records are counted."""
    out = []
    seen: dict[str, set[tuple[str, str]]] = {}
    for repo, rel, record in records:
        # Dedupe within a record — an intra-record duplicate is reported by
        # `_claim_id_findings`; this check counts only DISTINCT records so the
        # same defect is never double-reported.
        for cid in {claim.get("claim_id")
                    for claim in record.get("claims") or []
                    if isinstance(claim, dict)
                    and isinstance(claim.get("claim_id"), str)}:
            seen.setdefault(cid, set()).add((repo, rel))
    for cid, locs in sorted(seen.items()):
        if len(locs) > 1:
            where = ", ".join(f"{r}:{p}" for r, p in sorted(locs))
            for repo, rel in sorted(locs):
                out.append(_finding(
                    "duplicate-claim", ERROR, repo, rel,
                    f"claim id {cid!r} is defined in {len(locs)} records "
                    f"({where})",
                    "define each Claim ID in exactly one canonical record"))
    return out


def _aging_findings(ctx, records) -> list[Finding]:
    """Routing aging (aging-threshold defaults): records in `intake`,
    `triaging`, or incomplete `split` state whose latest transition is 30 days
    old are `warning`, escalating to `error` at 90 days. `routed`, `rejected`,
    and explicitly `deferred` records do not age. Non-default thresholds are
    disclosed through the runner's deviation reporting."""
    warn = ctx.thresholds.get("routing_warning_days", ROUTING_WARNING_DAYS_DEFAULT)
    err = ctx.thresholds.get("routing_error_days", ROUTING_ERROR_DAYS_DEFAULT)
    out = []
    for repo, rel, record in records:
        status = record.get("routing_status")
        if status not in AGING_ALWAYS and not (
                status == "split" and _has_active_claim(record)):
            continue
        latest = _latest_transition_date(record.get("transitions"))
        if latest is None:
            continue
        days = (ctx.as_of - latest).days
        if days >= err:
            severity = ERROR
        elif days >= warn:
            severity = WARNING
        else:
            continue
        out.append(_finding(
            "aging", severity, repo, rel,
            f"routing record in {status!r} state untouched {days} days "
            f"(latest transition; warning at {warn}, error at {err})",
            "progress the routing record or record an explicit deferral"))
    return out


def _has_active_claim(record) -> bool:
    for claim in record.get("claims") or []:
        if isinstance(claim, dict) and \
                claim.get("disposition") in ACTIVE_CLAIM_DISPOSITIONS:
            return True
    return False


def _latest_transition_date(transitions) -> date | None:
    if not isinstance(transitions, list):
        return None
    latest = None
    for transition in transitions:
        if not isinstance(transition, dict):
            continue
        when = _parse_date(transition.get("occurred_at"))
        if when is not None and (latest is None or when > latest):
            latest = when
    return latest


def _parse_date(value) -> date | None:
    if not isinstance(value, str) or len(value) < 10:
        return None
    try:
        return date.fromisoformat(value[:10])
    except ValueError:
        return None


# --- aggregation-root boundary and external-path resolution -------------------

def _aggregation_backlog_findings(ctx) -> list[Finding]:
    """xFactory aggregation-root backlog boundary (spec "Capture-first
    repository routing"; scenario "Aggregation backlog is created"): the
    aggregation repository MUST NOT host a general ideation backlog. The
    aggregation root owns only workspace assembly and pins, so any ideation
    area placed there is a forbidden backlog."""
    agg = ctx.agg_root
    if agg is None:
        return []
    ideation = Path(agg) / "ideation"
    if ideation.is_dir():
        return [_finding(
            "aggregation-backlog", ERROR, "xFactory", "ideation",
            "the xFactory aggregation repository hosts an ideation area; it "
            "MUST NOT host a general ideation backlog or a monolithic tagged "
            "inbox",
            "capture ideas in openxFactory or the owning DomainxFactory, "
            "never the aggregation repository")]
    return []


def _external_path_findings(ctx, records, index, known, mode) \
        -> list[Finding]:
    """Referenced install/runtime repositories are resolved without treating
    them as governance corpora (repository-resolution rules). A nightly run
    reports an unavailable external path as SKIPPED rather than passed (delta
    scenario "External path is unavailable during nightly validation"); strict
    organize/proposal mode (``ctx.routing_strict``) requires every referenced
    pinned repository to be materialized."""
    agg = ctx.agg_root
    strict = getattr(ctx, "routing_strict", False)
    governed = _governed_repo_ids(ctx) | {"xFactory"}
    external: set[str] = set()
    for _, _, record in records:
        for ref in _iter_refs(record):
            external.add(ref["repository"])
    for ref in _iter_refs(index or {}):
        external.add(ref["repository"])
    external = {
        r for r in external
        if r not in governed
        and _repository_unknown_reason(r, known, mode) is None}
    out = []
    for repo_id in sorted(external):
        materialized = agg is not None and (Path(agg) / repo_id).is_dir()
        if materialized:
            continue
        if strict:
            out.append(_finding(
                "external-path", ERROR, "xFactory", repo_id,
                f"strict organize/proposal validation requires materializing "
                f"referenced pinned repository {repo_id!r} to resolve its path "
                "and revision",
                "materialize the pinned repository (git submodule update) and "
                "re-run the strict gate"))
        else:
            out.append(_finding(
                "external-path", INFO, "xFactory", repo_id,
                f"referenced pinned repository {repo_id!r} is not materialized; "
                "external-path resolution reported as skipped (nightly)",
                "materialize the repository to resolve referenced paths, or "
                "run the strict organize/proposal gate",
                resolution=AUTO_FIXABLE))
    return out


# --- Markdown provenance (source, destination, staged, copied-record) ---------

def _strip_inline_code(line: str) -> str:
    return re.sub(r"`[^`]*`", "", line)


def _scan_lines(text: str):
    """Yield (lineno, line, in_code_fence) with ``` fence tracking. Fenced
    and inline-code examples are ignored by the provenance checks so a
    documented example never reads as a real definition or reference (delta
    scenario "Duplicate-looking references occur").

    NOT the `doc_health.lines`/real-line rule (finding F6, focused
    re-verify, align-status-reader-to-real-lines, 2026-08-19): this is a
    byte-for-byte copy of `families._scan_lines` as it existed BEFORE that
    change converted it, and this copy was never itself converted. Its
    docstring used to point at "families `_scan_lines` precedent" as if
    following that pointer would land on matching behavior — it would not,
    since `families._scan_lines` now scans real lines and this function
    still scans `str.splitlines()` pseudo-lines. Deliberately left
    unconverted: it is not a reader of a document's lifecycle header (it
    scans for provenance references and fence state, never `Status:`/
    `Kind:`/etc.), so it sits outside the wide ruling's every-*header*-
    reader clause; recorded, with `_template_gaps`, in tasks.md §7 as a
    latent (0-of-1227 files diverge) sibling the corrected sweep found.
    """
    fenced = False
    for i, line in enumerate(text.splitlines(), start=1):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            yield i, line, True
            continue
        yield i, line, fenced


def _markdown_provenance_findings(ctx, docs, record_ideas, claim_defs) \
        -> list[Finding]:
    """Lightweight source/destination/staged provenance and the copied-record
    drift check (spec "Organize gate and lightweight destination provenance";
    document-lifecycle delta). Distinguishes canonical definitions from valid
    references and fenced examples: only real routing.yaml records define IDs;
    Markdown headers are references validated against those records; fenced and
    inline-code examples are ignored."""
    out = []
    for doc in docs:
        # Only Markdown under an ideation/ area participates in provenance;
        # ordinary documents with no routing metadata stay invisible.
        if not doc.path.startswith("ideation/"):
            continue
        idea_headers, source_idea_ids, claim_ids, routing_records = \
            [], [], [], []
        embeds_record = False
        for _, raw, fenced in _scan_lines(doc.text):
            if RECORD_KIND in raw:
                # A full routing-record kind appears in the document — a copied
                # record even when fenced (a destination embeds it as fenced
                # YAML). Whether this is drift depends on the document being a
                # destination, decided in _provenance_doc_findings so an
                # illustrative example in a source brainstorm is never flagged
                # (delta scenario "Duplicate-looking references occur").
                embeds_record = True
            if fenced:
                continue
            line = _strip_inline_code(raw).strip()
            if m := _IDEA_ID_HEADER_RE.match(line):
                idea_headers.append(m.group(1))
            elif m := _SOURCE_IDEA_IDS_RE.match(line):
                source_idea_ids = _split_ids(m.group(1))
            elif m := _CLAIM_IDS_RE.match(line):
                claim_ids = _split_ids(m.group(1))
            elif m := _ROUTING_RECORDS_RE.match(line):
                routing_records.append(m.group(1))
        is_staging = doc.path.startswith("ideation/staging/")
        out.extend(_provenance_doc_findings(
            doc, idea_headers, source_idea_ids, claim_ids, routing_records,
            embeds_record, is_staging, record_ideas, claim_defs, ctx))
    return out


def _split_ids(value: str) -> list[str]:
    stripped = value.strip()
    if stripped.startswith("[") and stripped.endswith("]"):
        try:
            parsed = json.loads(stripped)
            if isinstance(parsed, list):
                return [str(v) for v in parsed]
        except json.JSONDecodeError:
            pass
    return [tok for tok in re.split(r"[,\s]+", stripped) if tok]


def _provenance_doc_findings(doc, idea_headers, source_idea_ids, claim_ids,
                             routing_records, embeds_record, is_staging,
                             record_ideas, claim_defs, ctx) -> list[Finding]:
    out = []
    is_destination = bool(source_idea_ids or claim_ids or routing_records)

    # A destination (a staging fragment, or any document carrying provenance
    # pointers) MUST carry lightweight pointers, never a copy of the full
    # routing-record schema (scenario "Destination copies a routing record").
    # An illustrative example in a source brainstorm — neither staged nor
    # carrying provenance pointers — is never flagged.
    if embeds_record and (is_staging or is_destination):
        out.append(_finding(
            "copied-record", ERROR, doc.repo, doc.path,
            "destination document embeds a full routing-record schema instead "
            "of lightweight provenance pointers",
            "replace the copied record with Source Idea IDs / Claim IDs / "
            "Routing records pointers"))

    # Source brainstorms use exactly one `Idea ID:` header; a destination that
    # consolidates ideas MUST NOT declare a misleading singular `Idea ID:`.
    if len(idea_headers) > 1:
        out.append(_finding(
            "destination-provenance", ERROR, doc.repo, doc.path,
            f"document declares {len(idea_headers)} Idea ID headers "
            f"({', '.join(idea_headers)}); a source brainstorm uses exactly one",
            "keep a single Idea ID header, or use Source Idea IDs on a "
            "destination"))
    if idea_headers and is_destination:
        out.append(_finding(
            "destination-provenance", ERROR, doc.repo, doc.path,
            "consolidated destination declares a misleading singular Idea ID "
            "alongside its Source Idea IDs / Claim IDs pointers",
            "drop the singular Idea ID header on a consolidated destination"))

    # A source `Idea ID:` header opts the document into routing; the idea must
    # have a canonical record (prospective docs with no header stay valid).
    for iid in idea_headers:
        if IDEA_ID_RE.match(iid) and iid not in record_ideas:
            out.append(_finding(
                "staged-pointer", ERROR, doc.repo, doc.path,
                f"Idea ID header {iid!r} has no canonical routing record",
                "create the canonical routing record or remove the Idea ID "
                "header"))

    # Destination Source Idea IDs / Claim IDs must resolve to real records/claims.
    for iid in source_idea_ids:
        if IDEA_ID_RE.match(iid) and iid not in record_ideas:
            out.append(_finding(
                "staged-pointer", ERROR, doc.repo, doc.path,
                f"Source Idea ID {iid!r} has no canonical routing record",
                "point Source Idea IDs at real canonical routing records"))
    for cid in claim_ids:
        if CLAIM_ID_RE.match(cid) and cid not in claim_defs:
            out.append(_finding(
                "staged-pointer", ERROR, doc.repo, doc.path,
                f"Claim ID pointer {cid!r} resolves to no canonical claim "
                "definition",
                "point Claim IDs at claims defined in a canonical routing "
                "record"))

    # The `Routing records:` header encodes a compact JSON array of structured
    # repository/path/full-revision references (spec scenario "Destination
    # serializes a routing pointer").
    for value in routing_records:
        parsed = _parse_routing_records_header(value)
        if parsed is None:
            out.append(_finding(
                "destination-provenance", ERROR, doc.repo, doc.path,
                "Routing records header does not parse as a compact JSON array "
                "of structured repository/path/revision references",
                "encode Routing records as the canonical compact JSON array"))
            continue
        for ref in parsed:
            if not (isinstance(ref, dict) and isinstance(ref.get("repository"),
                    str) and isinstance(ref.get("path"), str)
                    and isinstance(ref.get("revision"), str)
                    and FULL_REVISION_RE.match(ref["revision"])):
                out.append(_finding(
                    "destination-provenance", ERROR, doc.repo, doc.path,
                    "Routing records header element is not a committed "
                    "repository/path/full-revision reference",
                    "use the canonical committed_reference object shape"))
    return out


def _parse_routing_records_header(value: str):
    stripped = value.strip()
    if not (stripped.startswith("[") and stripped.endswith("]")):
        return None
    try:
        parsed = json.loads(stripped)
    except json.JSONDecodeError:
        return None
    return parsed if isinstance(parsed, list) else None


# --- proposal provenance ------------------------------------------------------

def _proposal_provenance_findings(ctx, records) -> list[Finding]:
    """Routed proposal provenance (document-lifecycle delta "Proposal-owned
    supporting documents"): every active proposal support manifest carrying an
    `ideation_provenance` block names resolvable Idea IDs, Claim IDs that
    resolve in the pinned routing record, and a committed routing-record
    reference (never `pending_capture`). Proposals with no routed source stay
    valid without the block."""
    out = []
    claims_by_idea: dict[str, set[str]] = {}
    idea_records: dict[str, tuple[str, str]] = {}
    for repo, rel, record in records:
        iid = record.get("idea_id")
        if not isinstance(iid, str):
            continue
        idea_records[iid] = (repo, rel)
        claims_by_idea.setdefault(iid, set())
        for claim in record.get("claims") or []:
            if isinstance(claim, dict) and isinstance(claim.get("claim_id"),
                                                      str):
                claims_by_idea[iid].add(claim["claim_id"])
    for repo, repo_path in sorted(ctx.repo_paths.items()):
        changes = repo_path / "openspec" / "changes"
        if not changes.is_dir():
            continue
        for change in sorted(p for p in changes.iterdir()
                             if p.is_dir() and p.name != "archive"):
            manifest = change / "supporting-docs" / "manifest.yaml"
            if not manifest.is_file():
                continue
            rel = str(manifest.relative_to(repo_path).as_posix())
            try:
                data = _load_yaml(manifest)
            except _RoutingParseError:
                continue  # families.location-conformance owns manifest validity
            if not isinstance(data, dict):
                continue
            provenance = data.get("ideation_provenance")
            if not provenance:
                continue  # no routed source; valid without the block
            if not isinstance(provenance, list):
                out.append(_finding(
                    "proposal-provenance", ERROR, repo, rel,
                    "ideation_provenance is not a list of provenance entries",
                    "record ideation_provenance as a list of entries"))
                continue
            for entry in provenance:
                out.extend(_provenance_entry_findings(
                    repo, rel, entry, claims_by_idea, ctx))
    return out


def _provenance_entry_findings(repo, rel, entry, claims_by_idea, ctx) \
        -> list[Finding]:
    out = []
    if not isinstance(entry, dict):
        out.append(_finding(
            "proposal-provenance", ERROR, repo, rel,
            "ideation_provenance entry is not a mapping",
            "record each provenance entry as a mapping"))
        return out
    iid = entry.get("idea_id")
    if not (isinstance(iid, str) and IDEA_ID_RE.match(iid)):
        out.append(_finding(
            "proposal-provenance", ERROR, repo, rel,
            f"ideation_provenance idea_id {iid!r} is not a valid Idea ID",
            "name a valid source Idea ID"))
    elif iid not in claims_by_idea:
        out.append(_finding(
            "proposal-provenance", ERROR, repo, rel,
            f"ideation_provenance names idea {iid!r} with no canonical routing "
            "record in scope",
            "pin the proposal to a real canonical routing record"))
    claim_ids = entry.get("claim_ids")
    if not isinstance(claim_ids, list) or not claim_ids:
        out.append(_finding(
            "proposal-provenance", ERROR, repo, rel,
            f"ideation_provenance entry for {iid!r} names no claim_ids",
            "name every selected Claim ID"))
    else:
        known_claims = claims_by_idea.get(iid, set())
        for cid in claim_ids:
            if isinstance(iid, str) and iid in claims_by_idea and \
                    cid not in known_claims:
                out.append(_finding(
                    "proposal-provenance", ERROR, repo, rel,
                    f"ideation_provenance claim {cid!r} is absent from the "
                    f"pinned routing record for {iid!r}",
                    "select only Claim IDs defined in the pinned routing "
                    "record"))
    rr = entry.get("routing_record")
    if not isinstance(rr, dict):
        out.append(_finding(
            "proposal-provenance", ERROR, repo, rel,
            f"ideation_provenance entry for {iid!r} has no routing_record "
            "reference",
            "record a committed routing-record reference"))
    else:
        revision = rr.get("revision")
        if revision == PENDING_CAPTURE:
            out.append(_finding(
                "proposal-provenance", ERROR, repo, rel,
                "ideation_provenance routing_record uses pending_capture; "
                "proposal provenance requires a full committed revision",
                "pin the full committed routing-record revision"))
        elif not (isinstance(revision, str)
                  and FULL_REVISION_RE.match(revision)):
            out.append(_finding(
                "proposal-provenance", ERROR, repo, rel,
                f"ideation_provenance routing_record revision {revision!r} is "
                "not a full committed revision",
                "pin the full committed routing-record revision"))
    return out


# --- collection ---------------------------------------------------------------

def _collect(ctx):
    """Collect routing artifacts across the governed corpus, plus parse-error
    findings. Returns (records, index, index_repo, parse_findings) where records
    is a list of (repo, relpath, dict). Malformed persisted YAML is reported as
    a finding, never fatal (the suite-wide convention)."""
    records, parse_findings = [], []
    index = index_repo = None
    for repo, repo_path in sorted(ctx.repo_paths.items()):
        ideation = repo_path / "ideation"
        # Central index (openxFactory hosts it; accept from whichever governed
        # repo carries one and disambiguate by openxFactory precedence).
        index_path = ideation / "routing-index.yaml"
        if index_path.is_file():
            try:
                data = _load_yaml(index_path)
                if isinstance(data, dict) and data.get("kind") == INDEX_KIND:
                    if index is None or repo == "openxFactory":
                        index, index_repo = data, repo
            except _RoutingParseError as exc:
                parse_findings.append(_finding(
                    "schema", ERROR, repo, "ideation/routing-index.yaml",
                    f"routing-index is unparseable: {exc}",
                    "repair the routing-index YAML"))
        if ideation.is_dir():
            for record_path in sorted(ideation.rglob("routing.yaml")):
                rel = str(record_path.relative_to(repo_path).as_posix())
                try:
                    data = _load_yaml(record_path)
                except _RoutingParseError as exc:
                    parse_findings.append(_finding(
                        "schema", ERROR, repo, rel,
                        f"routing record is unparseable: {exc}",
                        "repair the routing-record YAML"))
                    continue
                if isinstance(data, dict) and data.get("kind") == RECORD_KIND:
                    records.append((repo, rel, data))
    return records, index, index_repo, parse_findings


# --- entry point --------------------------------------------------------------

def fam_ideation_routing(ctx):
    if yaml is None:
        return Skip(FAMILY, "PyYAML unavailable; routing artifacts cannot be "
                    "parsed")

    known, mode, _ = _known_repositories(ctx)
    records, index, index_repo, parse_findings = _collect(ctx)

    record_ideas = {r.get("idea_id") for _, _, r in records
                    if isinstance(r.get("idea_id"), str)}
    claim_defs = set()
    for _, _, record in records:
        for claim in record.get("claims") or []:
            if isinstance(claim, dict) and isinstance(claim.get("claim_id"),
                                                      str):
                claim_defs.add(claim["claim_id"])

    findings = list(parse_findings)
    for repo, rel, record in records:
        repo_path = ctx.repo_paths[repo]
        findings.extend(_shape_findings(repo, rel, record))
        findings.extend(_claim_id_findings(repo, rel, record))
        findings.extend(_reference_findings(repo, rel, record, known, mode))
        findings.extend(_paired_document_findings(
            ctx, repo, repo_path, rel, record))
    if index is not None:
        findings.extend(_reference_findings(
            index_repo, "ideation/routing-index.yaml", index, known, mode))
    findings.extend(_central_allocation_findings(records, index, index_repo, ctx))
    findings.extend(_one_canonical_findings(records))
    findings.extend(_corpus_claim_uniqueness_findings(records))
    findings.extend(_aging_findings(ctx, records))
    findings.extend(_aggregation_backlog_findings(ctx))
    findings.extend(_external_path_findings(ctx, records, index, known, mode))
    findings.extend(_markdown_provenance_findings(
        ctx, ctx.docs, record_ideas, claim_defs))
    findings.extend(_proposal_provenance_findings(ctx, records))
    return findings
