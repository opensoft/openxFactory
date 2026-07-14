#!/usr/bin/env python3
"""Validate ideation-routing contract artifacts (add-cross-factory-ideation-routing).

Change task 2.3 (`openspec/changes/add-cross-factory-ideation-routing/tasks.md`):
strict openxFactory validation for the four schemas under
`contracts/schemas/xfactory-idea-routing-*.schema.yaml` /
`xfactory-ideation-*.schema.yaml`, plus the cross-cutting deterministic
invariants the frozen stage-1 schemas explicitly leave to this validator
(each schema's own description says so): central Idea-ID allocation and
uniqueness, one canonical routing record per idea, claim-ID prefix agreement
and uniqueness, append-only transition-history contiguity, destination-owner
acceptance completeness, structured repository-reference resolution against
the aggregation `.gitmodules`, paired-document Idea-ID agreement, and
prospective legacy compatibility (ordinary documents without a routing
sidecar are never reported).

It never chooses an owner, splits a claim, accepts a destination, moves a
document, disposes an organizer recommendation, or promotes policy (design
decision 6). Aging (30/90-day), the xFactory aggregation-root backlog
boundary, strict-gate submodule *materialization*, and the nightly
skipped-external-path result are the fourteenth deterministic doc-health
family's job in codexFactory (change tasks 4.2/4.3), not this openxFactory
contract validator.

Usage:
    python3 scripts/validate-ideation-routing.py [REPO] [--strict]

Two layers always run:

1. Packaged reference examples (`examples/ideation-routing/`, task 2.2):
   every `*.example.yaml` must validate against the schema its `kind`
   (or, for the pure-`$defs` reference kernel, its documented fragment
   shape) names; every file under `negative/` must fail. Each shipped VALID
   record/index/organizer example is additionally run through the
   per-artifact deterministic checks this validator owns, proving they do
   not false-positive on real valid data. This is the GATES self-test.
2. Real artifacts under REPO (default: this checkout):
   `ideation/routing-index.yaml`, every `ideation/**/routing.yaml` record,
   and every `health/ideation-organizer/**/*.yaml`. Absent paths are
   reported as skipped, never silently omitted (doc-health convention;
   `scripts/validate-document-catalog.py` and siblings do the same). Over
   the collected corpus it runs the cross-file checks (central allocation,
   one canonical record per idea, cross-record claim uniqueness, paired
   documents).

Repository IDs resolve as the spec defines: reserved root `xFactory`, or an
aggregation-relative `.gitmodules` submodule path. The aggregation
`.gitmodules` is discovered by walking up from REPO (an openxFactory checkout
is a submodule *under* the aggregation root); when found, resolution is exact
membership. When REPO is a standalone openxFactory clone with no aggregation
ancestor, resolution falls back to the recognized aggregation-layout
convention (`openxFactory`, `xFactories/<Name>`, `installs/<name>`) and the
mode is disclosed — full gitlink materialization remains codexFactory task 4.3.

Exit codes: 0 ok, 1 findings, 2 harness error.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any, Iterator

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR PyYAML is required", file=sys.stderr)
    sys.exit(2)

try:
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
    from referencing.jsonschema import DRAFT202012
except ImportError:  # pragma: no cover
    print("ERROR jsonschema>=4.18 and referencing are required", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = ROOT / "contracts" / "schemas"
EXAMPLES_DIR = ROOT / "examples" / "ideation-routing"

SCHEMA_FILENAMES = [
    "xfactory-idea-routing-reference.schema.yaml",
    "xfactory-idea-routing-record.schema.yaml",
    "xfactory-ideation-routing-index.schema.yaml",
    "xfactory-ideation-organizer-recommendations.schema.yaml",
]

KIND_TO_SCHEMA = {
    "xfactory_idea_routing_record": "xfactory-idea-routing-record.schema.yaml",
    "xfactory_ideation_routing_index": "xfactory-ideation-routing-index.schema.yaml",
    "ideation_organizer_recommendations": "xfactory-ideation-organizer-recommendations.schema.yaml",
}

# The reference kernel is a pure `$defs` schema (never a whole top-level
# document; see its own description). Its packaged examples wrap fragment
# instances under a plain container key.
FRAGMENT_DEFS = {
    "repository-reference.example.yaml": (
        "xfactory-idea-routing-reference.schema.yaml", "committed_reference", "references",
    ),
    "proposal-provenance.example.yaml": (
        "xfactory-idea-routing-reference.schema.yaml", "ideation_provenance_entry", "ideation_provenance",
    ),
}
NEGATIVE_FRAGMENT_DEFS = {
    "proposal-provenance-pending-capture.yaml": (
        "xfactory-idea-routing-reference.schema.yaml", "ideation_provenance_entry",
    ),
}

IDEA_ID_RE = re.compile(r"^XFI-[0-9]{4}-[0-9]{3}$")
IDEA_ID_HEADER_RE = re.compile(r"^Idea ID:\s*(\S+)\s*$", re.IGNORECASE)
CONVENTION_DOMAIN_RE = re.compile(r"^xFactories/[^/]+$")
CONVENTION_INSTALL_RE = re.compile(r"^installs/[^/]+$")

# Paired human-readable document names a routing.yaml may sit beside
# (`inbox/<idea-id>/idea.md`; `cross-domain/<idea-id>/routing-summary.md`).
PAIRED_DOC_NAMES = ("idea.md", "routing-summary.md")


class Findings:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.notes: list[str] = []

    def error(self, code: str, msg: str) -> None:
        self.errors.append(f"ERROR [{code}] {msg}")

    def warn(self, code: str, msg: str) -> None:
        self.warnings.append(f"WARN  [{code}] {msg}")

    def note(self, msg: str) -> None:
        self.notes.append(f"note  {msg}")


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


# --------------------------- schema registry ---------------------------

def build_registry() -> tuple[Registry, dict[str, dict]]:
    """Offline referencing.Registry over the four schemas (same approach as
    scripts/validate-document-catalog.py / validate-avatar-client.py). Each
    schema's `$id` is its own filename, so cross-file `$ref`s resolve by
    filename."""
    resources = []
    docs: dict[str, dict] = {}
    for name in SCHEMA_FILENAMES:
        doc = load_yaml(SCHEMAS_DIR / name)
        docs[name] = doc
        rid = doc.get("$id", name)
        resources.append((rid, Resource.from_contents(doc, default_specification=DRAFT202012)))
    return Registry().with_resources(resources), docs


def doc_validator(schema_name: str, registry: Registry, docs: dict[str, dict]) -> Draft202012Validator:
    return Draft202012Validator(docs[schema_name], registry=registry)


def def_validator(schema_name: str, def_name: str, registry: Registry) -> Draft202012Validator:
    """Validator for one named `$def` inside the pure-kernel schema, resolved
    through the registry exactly as the other three schemas `$ref` it."""
    return Draft202012Validator({"$ref": f"{schema_name}#/$defs/{def_name}"}, registry=registry)


def iter_errors(validator: Draft202012Validator, instance: Any):
    return sorted(validator.iter_errors(instance), key=lambda e: [str(p) for p in e.absolute_path])


# --------------------------- repository-ID resolution ---------------------------

def parse_gitmodules_paths(gm: Path) -> list[str]:
    paths: list[str] = []
    for line in gm.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("path"):
            _, _, val = stripped.partition("=")
            val = val.strip()
            if val:
                paths.append(val)
    return paths


def resolve_known_repositories(repo_root: Path) -> tuple[set[str], str, Path | None]:
    """Discover the aggregation `.gitmodules` by walking up from `repo_root`.
    A candidate qualifies only if it declares an `openxFactory` submodule or
    any `xFactories/*` submodule — this distinguishes the aggregation
    `.gitmodules` from openxFactory's own (which lists only its internal
    install submodule). Returns (known_paths, mode, gitmodules_path)."""
    p = repo_root
    while True:
        gm = p / ".gitmodules"
        if gm.is_file():
            paths = parse_gitmodules_paths(gm)
            if any(x == "openxFactory" or x.startswith("xFactories/") for x in paths):
                known = set(paths) | {"openxFactory", "xFactory"}
                return known, "gitmodules", gm
        if p.parent == p:
            break
        p = p.parent
    return {"openxFactory", "xFactory"}, "convention", None


def repository_unknown_reason(repo: str, known: set[str], mode: str) -> str | None:
    """Reason `repo` is not a resolvable aggregation repository ID, or None if
    it resolves (spec requirement "Structured repository references and
    resolvable provenance": reserved `xFactory` root or an aggregation-relative
    `.gitmodules` submodule path)."""
    if repo == "xFactory":
        return None
    if mode == "gitmodules":
        if repo in known:
            return None
        return (f"repository {repo!r} is neither the reserved 'xFactory' root nor a known "
                f"aggregation .gitmodules submodule path")
    # convention fallback (standalone openxFactory clone): accept the
    # recognized aggregation-layout shapes; membership is codexFactory task 4.3.
    if repo == "openxFactory" or CONVENTION_DOMAIN_RE.match(repo) or CONVENTION_INSTALL_RE.match(repo):
        return None
    return (f"repository {repo!r} is not a recognized aggregation repository id "
            f"(reserved 'xFactory', 'openxFactory', 'xFactories/<Name>', or 'installs/<name>')")


def iter_repo_refs(node: Any) -> Iterator[dict]:
    """Yield every structured reference object (any mapping carrying a string
    `repository` key) anywhere in `node`: sources, destinations,
    committed_references, path_references, ideation_provenance routing_records,
    organizer source_refs, and structured evidence_refs. Bare owner/candidate
    strings (`proposed_owner`, `candidate_owners`, `accepted_owner`) are not
    references and are never yielded."""
    if isinstance(node, dict):
        if isinstance(node.get("repository"), str):
            yield node
        for v in node.values():
            yield from iter_repo_refs(v)
    elif isinstance(node, list):
        for v in node:
            yield from iter_repo_refs(v)


def check_reference_resolution(
    f: Findings, label: str, doc: Any, known: set[str], mode: str,
) -> None:
    """Task-2.3 check "structured repository references": every structured
    reference's repository ID must resolve (spec "Structured repository
    references and resolvable provenance"; scenario "Unknown repository")."""
    for ref in iter_repo_refs(doc):
        reason = repository_unknown_reason(ref["repository"], known, mode)
        if reason is not None:
            f.error("unknown-repository", f"{label}: {reason}")


# --------------------------- per-record deterministic checks ---------------------------

def check_transition_chains(f: Findings, label: str, record: dict) -> None:
    """Task-2.3 check "legal transitions", sequence level: the per-edge graph
    is schema-enforced; this validates the append-only history is contiguous
    and terminates at the current state (spec "Routing and claim transition
    integrity"). Record: first `from` is null, each `from` equals the prior
    `to`, and the last `to` equals `routing_status`. Each claim: same, ending
    at its `disposition`."""
    ts = record.get("transitions") or []
    prev_to: Any = "<none>"
    for i, t in enumerate(ts):
        frm = t.get("from")
        if i == 0:
            if frm is not None:
                f.error("transition-chain", f"{label}: first routing transition.from must be null, got {frm!r}")
        elif frm != prev_to:
            f.error("transition-chain",
                    f"{label}: routing transition[{i}].from {frm!r} != previous transition.to {prev_to!r} "
                    f"(history is not append-only/contiguous)")
        prev_to = t.get("to")
    if ts and prev_to != record.get("routing_status"):
        f.error("transition-chain",
                f"{label}: last routing transition.to {prev_to!r} != routing_status {record.get('routing_status')!r}")

    for claim in record.get("claims") or []:
        cid = claim.get("claim_id")
        cts = claim.get("transitions") or []
        prev: Any = "<none>"
        for i, t in enumerate(cts):
            frm = t.get("from")
            if i == 0:
                if frm is not None:
                    f.error("claim-transition-chain",
                            f"{label}: claim {cid} first transition.from must be null, got {frm!r}")
            elif frm != prev:
                f.error("claim-transition-chain",
                        f"{label}: claim {cid} transition[{i}].from {frm!r} != previous transition.to {prev!r} "
                        f"(history is not append-only/contiguous)")
            prev = t.get("to")
        if cts and prev != claim.get("disposition"):
            f.error("claim-transition-chain",
                    f"{label}: claim {cid} last transition.to {prev!r} != disposition {claim.get('disposition')!r}")


def check_claim_ids(f: Findings, label: str, record: dict) -> None:
    """Task-2.3 checks "unique canonical definitions" (intra-record claim
    uniqueness) and Claim-ID identity: each Claim ID SHALL be
    `<idea-id>-C<NN>` (spec "Canonical routing identity and record")."""
    idea = record.get("idea_id")
    seen: dict[str, int] = {}
    for claim in record.get("claims") or []:
        cid = claim.get("claim_id")
        if idea and isinstance(cid, str) and not cid.startswith(f"{idea}-C"):
            f.error("claim-id-prefix",
                    f"{label}: claim {cid!r} does not derive from its record idea_id {idea!r} "
                    f"(must be '{idea}-C<NN>')")
        if isinstance(cid, str):
            seen[cid] = seen.get(cid, 0) + 1
    for cid, count in seen.items():
        if count > 1:
            f.error("duplicate-claim-id", f"{label}: claim id {cid!r} defined {count} times in one record")


def check_accepted_destinations(
    f: Findings, label: str, record: dict, known: set[str], mode: str,
) -> None:
    """Task-2.3 check "accepted destinations": destination-owner acceptance
    before a claim is routed (spec "Routing and claim transition integrity";
    scenario "Proposed owner has not accepted"). A routed claim must name an
    accepted owner, target capability, a structured committed destination
    whose repository resolves, and acceptance with at least one evidence
    reference."""
    for claim in record.get("claims") or []:
        if claim.get("disposition") != "routed":
            continue
        cid = claim.get("claim_id")
        if not claim.get("accepted_owner"):
            f.error("routed-acceptance", f"{label}: routed claim {cid} has no accepted_owner")
        if not claim.get("target_capability"):
            f.error("routed-acceptance", f"{label}: routed claim {cid} has no target_capability")
        dest = claim.get("destination")
        if not isinstance(dest, dict):
            f.error("routed-acceptance", f"{label}: routed claim {cid} has no structured destination")
        elif repository_unknown_reason(dest.get("repository") or "", known, mode) is not None:
            f.error("routed-acceptance",
                    f"{label}: routed claim {cid} destination repository {dest.get('repository')!r} does not resolve")
        acc = claim.get("acceptance")
        if not isinstance(acc, dict) or not (acc.get("evidence_refs") or []):
            f.error("routed-acceptance",
                    f"{label}: routed claim {cid} has no destination-owner acceptance evidence")


def check_record_self_contained(
    f: Findings, label: str, record: dict, known: set[str], mode: str,
) -> None:
    check_transition_chains(f, label, record)
    check_claim_ids(f, label, record)
    check_accepted_destinations(f, label, record, known, mode)
    check_reference_resolution(f, label, record, known, mode)


# --------------------------- corpus (cross-file) checks ---------------------------

def check_central_allocation(
    f: Findings, records: list[tuple[str, dict]], index: dict | None, repo_root: Path | None,
) -> None:
    """Task-2.3 check "central ID allocation": every routing record's Idea ID
    SHALL be allocated in the central `ideation/routing-index.yaml` in the same
    change (spec "Canonical routing identity and record"; scenario "Concurrent
    allocation collides"). Duplicate allocations are rejected; an allocation's
    `routing_record` pointer must resolve to a real file when it lives in this
    openxFactory checkout."""
    allocated: dict[str, int] = {}
    alloc_records: dict[str, dict] = {}
    for a in (index or {}).get("allocations") or []:
        iid = a.get("idea_id")
        if not isinstance(iid, str):
            continue
        allocated[iid] = allocated.get(iid, 0) + 1
        alloc_records[iid] = a.get("routing_record") or {}
    for iid, count in allocated.items():
        if count > 1:
            f.error("duplicate-idea-allocation",
                    f"routing-index allocates idea {iid!r} {count} times (collision — the later change must rebase)")

    record_ideas = {rec.get("idea_id") for _, rec in records}
    for label, rec in records:
        iid = rec.get("idea_id")
        if index is not None and iid not in allocated:
            f.error("idea-unallocated",
                    f"{label}: idea {iid!r} is not allocated in the central routing-index")

    # An index pointer into this checkout (repository openxFactory) must
    # resolve to a real file; pointers into other repositories are noted, not
    # errored, because this validator holds only the openxFactory tree.
    if repo_root is not None:
        for iid, rr in alloc_records.items():
            repo, path = rr.get("repository"), rr.get("path")
            if repo == "openxFactory" and isinstance(path, str):
                if not (repo_root / path).is_file():
                    f.error("allocation-dangling",
                            f"routing-index idea {iid!r} points at openxFactory/{path} which does not exist")
            elif iid not in record_ideas:
                f.note(f"routing-index idea {iid!r} points into {repo!r} (outside this checkout); "
                       f"record resolution deferred to codexFactory task 4.x")


def check_one_canonical(f: Findings, records: list[tuple[str, dict]]) -> None:
    """Task-2.3 check "unique canonical definitions": every idea SHALL have
    exactly one canonical routing record (spec "Canonical routing identity and
    record")."""
    by_idea: dict[str, list[str]] = {}
    for label, rec in records:
        iid = rec.get("idea_id")
        if isinstance(iid, str):
            by_idea.setdefault(iid, []).append(label)
    for iid, labels in by_idea.items():
        if len(labels) > 1:
            f.error("duplicate-canonical-record",
                    f"idea {iid!r} has {len(labels)} canonical routing records ({', '.join(sorted(labels))}); "
                    f"copies drift and create competing routing state")


def check_corpus_claim_uniqueness(f: Findings, records: list[tuple[str, dict]]) -> None:
    """Task-2.3 check "unique canonical definitions" across records: a Claim ID
    is defined once in the governed corpus (metadata-application-matrix:
    "every Idea ID and Claim ID is unique in the governed repository set")."""
    seen: dict[str, list[str]] = {}
    for label, rec in records:
        for claim in rec.get("claims") or []:
            cid = claim.get("claim_id")
            if isinstance(cid, str):
                seen.setdefault(cid, []).append(label)
    for cid, labels in seen.items():
        if len(labels) > 1:
            f.error("duplicate-claim-id",
                    f"claim id {cid!r} is defined in {len(labels)} records ({', '.join(sorted(labels))})")


def extract_idea_id_header(text: str) -> str | None:
    for line in text.splitlines():
        m = IDEA_ID_HEADER_RE.match(line.strip())
        if m:
            return m.group(1)
    return None


def check_paired_documents(f: Findings, repo_root: Path, path: Path, record: dict) -> None:
    """Task-2.3 check "paired-document agreement": a routing.yaml under an
    Idea-ID-named directory pairs with a human-readable document that agrees on
    the Idea ID (spec "Canonical routing identity and record", scenario
    "Routing begins": "the human-readable source and routing record MUST agree
    on the Idea ID"). A paired document with no `Idea ID:` header at all is not
    flagged, keeping prospective/legacy docs valid."""
    idea = record.get("idea_id")
    directory = path.parent
    rel = path.relative_to(repo_root)
    dirname = directory.name
    if IDEA_ID_RE.match(dirname) and dirname != idea:
        f.error("pair-dir-mismatch",
                f"{rel}: routing record idea_id {idea!r} does not match its directory {dirname!r}")

    paired = [directory / n for n in PAIRED_DOC_NAMES if (directory / n).is_file()]
    if not paired:
        f.error("pair-missing-doc",
                f"{rel}: routing record has no paired human-readable document "
                f"({' or '.join(PAIRED_DOC_NAMES)}) in the same directory")
        return
    for doc_path in paired:
        header_id = extract_idea_id_header(doc_path.read_text(encoding="utf-8"))
        if header_id is not None and header_id != idea:
            f.error("pair-id-mismatch",
                    f"{rel}: paired {doc_path.name} declares Idea ID {header_id!r} but the routing "
                    f"record idea_id is {idea!r}")


# --------------------- layer 1: packaged reference examples ---------------------

def check_examples(
    f: Findings, registry: Registry, docs: dict[str, dict], known: set[str], mode: str,
) -> None:
    """Task-2.3 GATES self-test: every example under examples/ideation-routing/
    validates exactly as its filename and header comment claim (task 2.2), and
    every shipped VALID artifact also passes the per-artifact deterministic
    checks this validator owns."""
    if not EXAMPLES_DIR.is_dir():
        f.error("examples-missing", f"{EXAMPLES_DIR} not found")
        return

    valid_top_level = 0
    for path in sorted(EXAMPLES_DIR.glob("*.example.yaml")):
        if path.name in FRAGMENT_DEFS:
            continue  # handled by check_fragment_examples
        doc = load_yaml(path)
        kind = doc.get("kind") if isinstance(doc, dict) else None
        schema_name = KIND_TO_SCHEMA.get(kind)
        if schema_name is None:
            f.error("example-kind", f"{path.name}: unrecognized kind {kind!r}")
            continue
        errs = iter_errors(doc_validator(schema_name, registry, docs), doc)
        if errs:
            for e in errs:
                loc = "/".join(str(p) for p in e.absolute_path) or "<root>"
                f.error("example-invalid", f"{path.name}: expected valid, got {loc}: {e.message}")
            continue
        valid_top_level += 1
        # deterministic self-test: shipped valid data must not false-positive.
        if kind == "xfactory_idea_routing_record":
            check_record_self_contained(f, path.name, doc, known, mode)
        else:
            check_reference_resolution(f, path.name, doc, known, mode)

    invalid_checked = check_negative_examples(f, registry, docs)
    frag_files = check_fragment_examples(f, registry, docs, known, mode)

    f.note(
        f"examples: {valid_top_level} valid top-level example(s) + {frag_files} fragment file(s) "
        f"confirmed valid, {invalid_checked} negative example(s) confirmed invalid"
    )


def check_negative_examples(f: Findings, registry: Registry, docs: dict[str, dict]) -> int:
    neg_dir = EXAMPLES_DIR / "negative"
    checked = 0
    if not neg_dir.is_dir():
        f.error("examples-missing", f"{neg_dir} not found")
        return checked
    for path in sorted(neg_dir.glob("*.yaml")):
        doc = load_yaml(path)
        if path.name in NEGATIVE_FRAGMENT_DEFS:
            schema_name, def_name = NEGATIVE_FRAGMENT_DEFS[path.name]
            validator = def_validator(schema_name, def_name, registry)
        else:
            kind = doc.get("kind") if isinstance(doc, dict) else None
            schema_name = KIND_TO_SCHEMA.get(kind)
            if schema_name is None:
                f.error("example-kind", f"negative/{path.name}: unrecognized kind {kind!r}")
                continue
            validator = doc_validator(schema_name, registry, docs)
        errs = iter_errors(validator, doc)
        if not errs:
            f.error("example-should-fail", f"negative/{path.name}: expected invalid, validated cleanly")
            continue
        checked += 1
    return checked


def check_fragment_examples(
    f: Findings, registry: Registry, docs: dict[str, dict], known: set[str], mode: str,
) -> int:
    checked = 0
    for filename, (schema_name, def_name, container_key) in FRAGMENT_DEFS.items():
        path = EXAMPLES_DIR / filename
        if not path.is_file():
            f.error("examples-missing", f"{path} not found")
            continue
        validator = def_validator(schema_name, def_name, registry)
        items = (load_yaml(path) or {}).get(container_key) or []
        if not items:
            f.error("fragment-example-empty", f"{filename}: no items under {container_key!r}")
            continue
        ok = True
        for i, item in enumerate(items):
            errs = iter_errors(validator, item)
            if errs:
                ok = False
                f.error("fragment-example-invalid", f"{filename}[{i}]: expected valid: {errs[0].message}")
        if ok:
            check_reference_resolution(f, filename, {"references": items}, known, mode)
            checked += 1
    return checked


# --------------------------- layer 2: real repo tree ---------------------------

def check_repo_tree(
    f: Findings, registry: Registry, docs: dict[str, dict], repo_root: Path, known: set[str], mode: str,
) -> None:
    checked = 0

    index: dict | None = None
    index_path = repo_root / "ideation" / "routing-index.yaml"
    if index_path.is_file():
        doc = load_yaml(index_path)
        errs = iter_errors(doc_validator("xfactory-ideation-routing-index.schema.yaml", registry, docs), doc)
        if errs:
            for e in errs:
                f.error("index-invalid", f"{index_path.relative_to(repo_root)}: {e.message}")
        else:
            checked += 1
            index = doc
            check_reference_resolution(f, str(index_path.relative_to(repo_root)), doc, known, mode)
    else:
        f.note("ideation/routing-index.yaml not present; central-allocation checks skipped")

    records: list[tuple[str, dict]] = []
    record_files: list[tuple[Path, dict]] = []
    ideation_dir = repo_root / "ideation"
    record_paths = sorted(ideation_dir.rglob("routing.yaml")) if ideation_dir.is_dir() else []
    for path in record_paths:
        doc = load_yaml(path)
        if not isinstance(doc, dict) or doc.get("kind") != "xfactory_idea_routing_record":
            continue
        rel = str(path.relative_to(repo_root))
        errs = iter_errors(doc_validator("xfactory-idea-routing-record.schema.yaml", registry, docs), doc)
        if errs:
            for e in errs:
                f.error("record-invalid", f"{rel}: {e.message}")
            continue
        checked += 1
        check_record_self_contained(f, rel, doc, known, mode)
        check_paired_documents(f, repo_root, path, doc)
        records.append((rel, doc))
        record_files.append((path, doc))

    if records or index is not None:
        check_central_allocation(f, records, index, repo_root)
        check_one_canonical(f, records)
        check_corpus_claim_uniqueness(f, records)
    if not record_paths:
        f.note("no ideation/**/routing.yaml records present; routing is prospective "
               "(ordinary documents without a routing sidecar remain valid)")

    org_dir = repo_root / "health" / "ideation-organizer"
    org_files = sorted(org_dir.rglob("*.yaml")) if org_dir.is_dir() else []
    for path in org_files:
        doc = load_yaml(path)
        if not isinstance(doc, dict) or doc.get("kind") != "ideation_organizer_recommendations":
            continue
        rel = str(path.relative_to(repo_root))
        errs = iter_errors(
            doc_validator("xfactory-ideation-organizer-recommendations.schema.yaml", registry, docs), doc)
        if errs:
            for e in errs:
                f.error("organizer-invalid", f"{rel}: {e.message}")
            continue
        checked += 1
        check_reference_resolution(f, rel, doc, known, mode)
    if not org_files:
        f.note("no health/ideation-organizer/ evidence present; skipped "
               "(organizer persistence-path enforcement is codexFactory task 5.4/7.2)")

    f.note(f"repo tree ({repo_root}): {checked} real ideation-routing artifact(s) checked")


# --------------------------- orchestration ---------------------------

def run(repo: Path, strict: bool) -> int:
    f = Findings()
    if not SCHEMAS_DIR.is_dir():
        print(f"ERROR {SCHEMAS_DIR} not found", file=sys.stderr)
        return 2

    registry, docs = build_registry()
    for name, doc in docs.items():
        try:
            Draft202012Validator.check_schema(doc)
        except Exception as exc:  # noqa: BLE001
            f.error("schema-invalid", f"{name}: {exc}")

    known, mode, gm = resolve_known_repositories(repo)
    if mode == "gitmodules":
        f.note(f"repository IDs resolved against aggregation {gm} ({len(known)} known submodule path(s))")
    else:
        f.note("no aggregation .gitmodules ancestor found; repository IDs resolved by aggregation-layout "
               "convention (standalone openxFactory clone) — strict-gate gitlink materialization is "
               "codexFactory task 4.3")

    check_examples(f, registry, docs, known, mode)
    check_repo_tree(f, registry, docs, repo, known, mode)

    for line in f.notes:
        print(line)
    for line in f.warnings:
        print(line)
    for line in f.errors:
        print(line)

    n_e, n_w = len(f.errors), len(f.warnings)
    print(f"\nvalidate-ideation-routing: {n_e} error(s), {n_w} warning(s)")
    if n_e or (strict and n_w):
        return 1
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("repo", nargs="?", default=str(ROOT),
                    help="repo root to scan for real ideation-routing artifacts (default: this checkout)")
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = ap.parse_args()
    try:
        return run(Path(args.repo).resolve(), args.strict)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR harness failure: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
