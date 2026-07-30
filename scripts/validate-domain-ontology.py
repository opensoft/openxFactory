#!/usr/bin/env python3
"""Validate the domain-ontology contract family (add-domain-ontology-layer).

The openxFactory-owned canonical validator for the eighteen family kinds
(package manifest, concepts, relations, external mappings, source
inventory, candidate, release, migration map, semantic context, quality
report, stewardship policy, maintenance input/report, semantic-context
profile, review fixtures, coverage-gap report, starter provenance, and
consumer-impact report)
(`contracts/domain-ontology/*.schema.yaml`). Run from the openxFactory
checkout:

    python3 scripts/validate-domain-ontology.py [REPO_PATH] [--strict]
    python3 scripts/validate-domain-ontology.py --determinism

Two layers run (change tasks 3.1-3.7):

1. The core kernel package (`contracts/domain-ontology/core/`) and the
   packaged reference examples (`contracts/domain-ontology/examples/`): every
   positive package and loose artifact must pass schema conformance AND every
   cross-shape rule; every unit under `examples/negative/` must FAIL for its
   INTENDED reason, declared in an `# expected_failure:` header (in the
   package.yaml for package dirs, in the file for loose artifacts) and
   optionally pinned by `# expected_failure_detail:`. The self-test fails
   closed if a positive fails or a negative stops failing for its reason.
2. Optional real artifacts under REPO_PATH: every package dir (a directory
   holding a family package.yaml) and loose family-kind `*.y*ml` outside the
   packaged examples is validated; a `hermes/domain/content-manifest.yaml`
   declaring `domain_ontology` has its declared tree validated as a package
   (fail closed on a missing or invalid declaration target).

The rules the shapes cannot express (stable finding codes):

  ONT-DIGEST            inventory sha256 or package digest mismatch; loading
                        fails closed on drift
  ONT-INVENTORY-FOREIGN an inventoried file whose kind is not an
                        ontology-family kind (mirrored terminologies included)
  ONT-NAMESPACE         a term id outside the package namespace, or
                        package_id disagreement across package files
  ONT-ID-DUP            duplicate term identifier within the package
  ONT-LABEL-COLLISION   a label or alias equal to another term's label/alias
                        in the same namespace
  ONT-PARENT-MISSING    a parent reference that resolves to neither the
                        package nor its imported kernel
  ONT-CYCLE             a specialization cycle
  ONT-RELATION-RANGE    a relation domain/range concept that does not resolve
  ONT-KERNEL-IMPORT     kernel_import missing on a domain package, present on
                        the kernel, or digest-mismatched against the resolved
                        kernel
  ONT-ADOPTION          a published kernel (or kernel term) without two
                        independent resolvable adopters; pending adoption on
                        a published kernel
  ONT-SOURCE-MISSING    a term/mapping source or steward reference that is
                        not registered
  ONT-MAPPING-UNREGISTERED  an external mapping whose system is unregistered
                        or not an external source kind
  ONT-LICENSE           quoted definition without a registered
                        definition_quote permitted use
  ONT-COMPAT            a non-initial package without compatibility.previous,
                        or breaking/retiring without a migration map
  ONT-TERM-LIFECYCLE    a draft term in a published/deprecated package, a
                        term lifecycle moving backward across revisions, or
                        a retired term in a profile or current-pin context
  ONT-TERM-VERSION      meaning-bearing term content changed without an
                        effective_version bump, or effective_version moving
                        backward
  ONT-RETENTION         a referenced superseded/previous version whose
                        retained bytes are missing or digest-drifted
  ONT-PRIVATE           subject-instance URNs, tenant endpoints, or
                        identifier-bearing values in ontology content
  ONT-FLOOR             a term-level quality signal below the aggregation
                        floor, or a sub-two subject floor without a recorded
                        exception
  ONT-AUTHORITY-FIELD   an unknown field whose name matches the reserved
                        authority vocabulary (effect/permission/grant/...)
  ONT-AUTHORITY-TARGET  an authority-plane instance reference
                        (urn:xfactory:* other than subject) in content
  ONT-CANDIDATE         model extraction without extraction_run_id, or an
                        accepted candidate without a steward disposition, or
                        a worker/agent-attributed acceptance
  ONT-RELEASE           a publication not decided by an accountable steward,
                        a worker/agent-attributed publication, a breaking
                        release without migration evidence, or a release
                        digest that does not match its package
  ONT-QUALITY           a fixture_accuracy signal without its pinned
                        fixture-set digest
  ONT-CONTEXT-CLOSURE   a semantic context that is neither closed over
                        ancestors and relation endpoints nor explicitly
                        truncated
  ONT-CONTEXT-PIN       a semantic context whose package pin does not match
                        the resolved package
  ONT-BINDING           a tenant binding pinned to a different package than
                        the context
  ONT-POLICY            a stewardship policy whose council members do not
                        resolve to the manifest roster or whose quorum
                        exceeds the council
  ONT-MAINTENANCE       a maintenance report whose fired triggers lack their
                        mode/candidate refs or whose drift flag disagrees
  ONT-MANIFEST-PIN      a domain content manifest declaring an ontology tree
                        that is missing or invalid
  ONT-SCHEMA            any other schema conformance failure

Exit codes: 0 ok, 1 findings, 2 harness error.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR PyYAML is required", file=sys.stderr)
    sys.exit(2)

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover
    print("ERROR jsonschema is required", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_DIR = ROOT / "contracts" / "domain-ontology"
CORE_DIR = CONTRACT_DIR / "core"
EXAMPLES_DIR = CONTRACT_DIR / "examples"
NEGATIVE_DIR = EXAMPLES_DIR / "negative"

SCHEMA_FILES = {
    "xfactory_ontology_package_manifest": "ontology-package-manifest.schema.yaml",
    "xfactory_ontology_concepts": "ontology-concepts.schema.yaml",
    "xfactory_ontology_relations": "ontology-relations.schema.yaml",
    "xfactory_ontology_external_mappings": "ontology-external-mappings.schema.yaml",
    "xfactory_ontology_source_inventory": "ontology-source-inventory.schema.yaml",
    "xfactory_ontology_candidate_record": "ontology-candidate-record.schema.yaml",
    "xfactory_ontology_release_record": "ontology-release-record.schema.yaml",
    "xfactory_ontology_migration_map": "ontology-migration-map.schema.yaml",
    "xfactory_semantic_context": "semantic-context.schema.yaml",
    "xfactory_ontology_quality_report": "ontology-quality-report.schema.yaml",
    "xfactory_ontology_stewardship_policy": "ontology-stewardship-policy.schema.yaml",
    "xfactory_ontology_maintenance_input": "ontology-maintenance-input.schema.yaml",
    "xfactory_ontology_maintenance_report": "ontology-maintenance-report.schema.yaml",
    "xfactory_semantic_context_profile": "semantic-context-profile.schema.yaml",
    "xfactory_ontology_review_fixtures": "ontology-review-fixtures.schema.yaml",
    "xfactory_ontology_coverage_gap_report": "ontology-coverage-gap-report.schema.yaml",
    "xfactory_ontology_starter_provenance": "ontology-starter-provenance.schema.yaml",
    "xfactory_ontology_consumer_impact_report": "ontology-consumer-impact-report.schema.yaml",
}
FAMILY_KINDS = set(SCHEMA_FILES)
# Package CONTENT is inventoried and digest-covered. RECORD kinds reference
# the package digest (a release names it; a context pins it), so they attach
# BESIDE the inventory rather than inside it — inventorying them would make
# the digest self-referential.
PACKAGE_CONTENT_KINDS = {
    "xfactory_ontology_concepts",
    "xfactory_ontology_relations",
    "xfactory_ontology_external_mappings",
    "xfactory_ontology_source_inventory",
    "xfactory_ontology_migration_map",
    "xfactory_ontology_stewardship_policy",
    "xfactory_semantic_context_profile",
}
PACKAGE_RECORD_KINDS = {
    "xfactory_ontology_candidate_record",
    "xfactory_ontology_release_record",
    "xfactory_semantic_context",
    "xfactory_ontology_quality_report",
    "xfactory_ontology_maintenance_report",
    "xfactory_ontology_maintenance_input",
    "xfactory_ontology_review_fixtures",
    "xfactory_ontology_coverage_gap_report",
    "xfactory_ontology_starter_provenance",
    "xfactory_ontology_consumer_impact_report",
}
PACKAGE_FILE_KINDS = PACKAGE_CONTENT_KINDS

# Aligned with the runtime's reserved extension-property vocabulary
# (contracts/hermes-runtime/shared-definitions.schema.yaml safe_extension_
# property_name) plus the ontology change's own additions.
RESERVED_FIELD_NAMES = {
    "effect", "permission", "permissions", "grant", "grants", "credential",
    "credentials", "scope", "scopes", "route", "routing", "routing_decision",
    "token", "secret", "principal", "trust", "binding", "bindings",
    "authority_grant", "approval_effect", "executable_rule", "rule",
}
LIFECYCLE_ORDER = {"draft": 0, "published": 1, "deprecated": 2, "retired": 3}
SUBJECT_URN = re.compile(r"urn:xfactory:subject:")
OTHER_URN = re.compile(r"urn:xfactory:(?!subject:)")
ENDPOINTISH = re.compile(r"://|\.internal\b|\.local\b|\.corp\b")


@dataclass(frozen=True)
class Finding:
    code: str
    path: str
    message: str

    def line(self) -> str:
        return f"{self.code} {self.path}: {self.message}"


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text())


def load_schemas() -> dict[str, Draft202012Validator]:
    out = {}
    for kind, fname in SCHEMA_FILES.items():
        schema = load_yaml(CONTRACT_DIR / fname)
        out[kind] = Draft202012Validator(schema)
    return out


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def schema_findings(validator: Draft202012Validator, doc, path: Path) -> list[Finding]:
    found = []
    for err in sorted(validator.iter_errors(doc), key=lambda e: str(e.absolute_path)):
        loc = "/".join(str(p) for p in err.absolute_path) or "$"
        if err.validator == "additionalProperties":
            names = re.findall(r"'([^']+)'", err.message)
            reserved = sorted(n for n in names if n.lower() in RESERVED_FIELD_NAMES)
            if reserved:
                found.append(Finding(
                    "ONT-AUTHORITY-FIELD", rel(path),
                    f"{loc}: reserved authority field(s) {', '.join(reserved)} "
                    "rejected by the closed vocabulary"))
                continue
        found.append(Finding("ONT-SCHEMA", rel(path), f"{loc}: {err.message}"))
    return found


def walk_strings(node, trail=""):
    if isinstance(node, dict):
        for k, v in node.items():
            yield from walk_strings(v, f"{trail}/{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk_strings(v, f"{trail}[{i}]")
    elif isinstance(node, str):
        yield trail, node


PROSE_TRAIL_KEYS = {
    "definition", "notes", "label", "quoted_definition", "name", "term_form",
    "code", "description", "text", "position", "applicability", "realization",
    "note", "detail", "purpose",
}
IDENTIFIER_PATTERNS = [
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),          # SSN-shaped
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),  # email
    re.compile(r"\d{7,}"),                         # long digit run (MRN-shaped)
]


def prose_trail(trail: str) -> bool:
    last = trail.rsplit("/", 1)[-1]
    last = last.split("[", 1)[0]
    return last in PROSE_TRAIL_KEYS


def value_scan(doc, path: Path) -> list[Finding]:
    found = []
    for trail, value in walk_strings(doc):
        if SUBJECT_URN.search(value):
            found.append(Finding("ONT-PRIVATE", rel(path),
                                 f"{trail}: subject-instance reference in ontology content"))
        elif OTHER_URN.search(value):
            found.append(Finding("ONT-AUTHORITY-TARGET", rel(path),
                                 f"{trail}: authority-plane instance reference in ontology content"))
        if prose_trail(trail):
            if ENDPOINTISH.search(value):
                found.append(Finding("ONT-PRIVATE", rel(path),
                                     f"{trail}: endpoint/hostname-shaped value in prose content"))
            for pat in IDENTIFIER_PATTERNS:
                if pat.search(value):
                    found.append(Finding("ONT-PRIVATE", rel(path),
                                         f"{trail}: identifier-bearing value in prose content"))
                    break
    return found


class Package:
    def __init__(self, pkg_dir: Path, manifest: dict):
        self.dir = pkg_dir
        self.manifest = manifest
        self.files: dict[str, dict] = {}
        self.concepts: dict[str, dict] = {}
        self.relations: dict[str, dict] = {}
        self.mappings: list[dict] = []
        self.sources: dict[str, dict] = {}
        self.candidates: list[tuple[Path, dict]] = []
        self.releases: list[tuple[Path, dict]] = []
        self.migrations: list[tuple[Path, dict]] = []
        self.contexts: list[tuple[Path, dict]] = []
        self.quality: list[tuple[Path, dict]] = []
        self.policy: dict | None = None
        self.maintenance: list[tuple[Path, dict]] = []
        self.profiles: list[tuple[Path, dict]] = []
        self.maintenance_inputs: list[tuple[Path, dict]] = []
        self.impacts: list[tuple[Path, dict]] = []

    @property
    def package_id(self) -> str:
        return self.manifest.get("package_id", "?")

    @property
    def is_kernel(self) -> bool:
        return bool(self.manifest.get("is_kernel"))


def compute_package_digest(entries: list[tuple[str, str]]) -> str:
    lines = sorted(f"{p} {d}" for p, d in entries)
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()


PACKAGE_REGISTRY: dict[str, list["Package"]] = {}
# Sibling-family kinds that may legitimately sit beside an ontology package
# without being this validator's jurisdiction (finding N2). Everything else
# with a kind is flagged and scanned.
ALLOWED_SIBLING_KINDS = {"hermes_domain_overlay"}


def load_package(pkg_dir: Path, schemas, findings: list[Finding],
                 resolve_kernel) -> Package | None:
    manifest_path = pkg_dir / "package.yaml"
    manifest = load_yaml(manifest_path)
    if not isinstance(manifest, dict) or manifest.get("kind") != "xfactory_ontology_package_manifest":
        findings.append(Finding("ONT-SCHEMA", rel(manifest_path), "not a package manifest"))
        return None
    findings.extend(schema_findings(schemas["xfactory_ontology_package_manifest"], manifest, manifest_path))
    pkg = Package(pkg_dir, manifest)

    # Digest closure — fail closed on drift.
    entries = []
    drifted = False
    for item in manifest.get("inventory", []):
        fpath = pkg_dir / item.get("path", "")
        if not fpath.is_file():
            findings.append(Finding("ONT-DIGEST", rel(manifest_path),
                                    f"inventoried file missing: {item.get('path')}"))
            drifted = True
            continue
        actual = hashlib.sha256(fpath.read_bytes()).hexdigest()
        if actual != item.get("sha256"):
            findings.append(Finding("ONT-DIGEST", rel(fpath),
                                    "content differs from recorded sha256; loading fails closed"))
            drifted = True
        entries.append((item.get("path", ""), item.get("sha256", "")))
    if not drifted and manifest.get("package_digest") != compute_package_digest(entries):
        findings.append(Finding("ONT-DIGEST", rel(manifest_path),
                                "package_digest does not match inventory"))
        drifted = True
    if drifted:
        return None

    # Digest-true packages join the shared registry (the resolution
    # substrate for loose contexts, loose governance records, and kernel
    # domain_package adoption — release-review finding N1: reading an
    # unpopulated registry made three rules dead code). Deduped by
    # directory so the registration prepass and the validation pass never
    # double-register.
    known = PACKAGE_REGISTRY.get(pkg.package_id, [])
    if not any(existing.dir == pkg.dir for existing in known):
        PACKAGE_REGISTRY.setdefault(pkg.package_id, []).append(pkg)

    # Inventory membership: ontology-family documents only.
    for item in manifest.get("inventory", []):
        fpath = pkg_dir / item["path"]
        try:
            doc = load_yaml(fpath)
        except yaml.YAMLError:
            findings.append(Finding("ONT-SCHEMA", rel(fpath), "unparseable YAML"))
            continue
        kind = doc.get("kind") if isinstance(doc, dict) else None
        if kind not in PACKAGE_FILE_KINDS:
            findings.append(Finding("ONT-INVENTORY-FOREIGN", rel(fpath),
                                    f"inventoried kind {kind!r} is not an ontology-family document"))
            continue
        findings.extend(schema_findings(schemas[kind], doc, fpath))
        findings.extend(value_scan(doc, fpath))
        pkg.files[item["path"]] = doc
        if kind == "xfactory_ontology_concepts":
            for c in doc.get("concepts", []):
                pkg.concepts.setdefault(c["id"], c)
        elif kind == "xfactory_ontology_relations":
            for r in doc.get("relations", []):
                pkg.relations.setdefault(r["id"], r)
        elif kind == "xfactory_ontology_external_mappings":
            pkg.mappings.extend(doc.get("mappings", []))
        elif kind == "xfactory_ontology_source_inventory":
            for s in doc.get("sources", []):
                pkg.sources.setdefault(s["system_id"], s)
        elif kind == "xfactory_ontology_migration_map":
            pkg.migrations.append((fpath, doc))
        elif kind == "xfactory_ontology_stewardship_policy":
            pkg.policy = doc
        elif kind == "xfactory_semantic_context_profile":
            pkg.profiles.append((fpath, doc))

    # Beside-the-inventory records: candidates, releases, contexts, quality
    # reports found in the package dir attach without being digest-covered. A
    # CONTENT-kind file that is not inventoried is a byte-completeness
    # violation.
    inventoried = {item["path"] for item in manifest.get("inventory", [])}
    for fpath in sorted(pkg_dir.glob("*.y*ml")):
        name = fpath.name
        if name == "package.yaml" or name in inventoried:
            continue
        try:
            doc = load_yaml(fpath)
        except yaml.YAMLError as exc:
            findings.append(Finding("ONT-SCHEMA", rel(fpath),
                                    f"unparseable YAML beside the package: {exc}"))
            continue
        kind = doc.get("kind") if isinstance(doc, dict) else None
        if kind in PACKAGE_CONTENT_KINDS:
            findings.append(Finding("ONT-DIGEST", rel(fpath),
                                    "package content file is not inventoried"))
        elif kind in PACKAGE_RECORD_KINDS:
            findings.extend(schema_findings(schemas[kind], doc, fpath))
            findings.extend(value_scan(doc, fpath))
            if kind == "xfactory_ontology_candidate_record":
                pkg.candidates.append((fpath, doc))
            elif kind == "xfactory_ontology_release_record":
                pkg.releases.append((fpath, doc))
            elif kind == "xfactory_semantic_context":
                pkg.contexts.append((fpath, doc))
            elif kind == "xfactory_ontology_quality_report":
                pkg.quality.append((fpath, doc))
            elif kind == "xfactory_ontology_maintenance_report":
                pkg.maintenance.append((fpath, doc))
            elif kind == "xfactory_ontology_maintenance_input":
                pkg.maintenance_inputs.append((fpath, doc))
            elif kind == "xfactory_ontology_consumer_impact_report":
                pkg.impacts.append((fpath, doc))
        elif kind is None or kind in ALLOWED_SIBLING_KINDS:
            # Kind-less files (comment-only, lockfiles) and declared sibling
            # families are other jurisdictions, not blind spots of this one
            # (release-review finding N2).
            continue
        else:
            # An unrecognized kind beside a package is a finding, never a
            # blind spot — and it is scanned regardless (release-review
            # finding 4).
            findings.append(Finding("ONT-INVENTORY-FOREIGN", rel(fpath),
                                    f"unrecognized kind {kind!r} beside the package"))
            findings.extend(value_scan(doc, fpath))

    check_package(pkg, findings, resolve_kernel)
    return pkg


def check_candidate_record(cand: dict, fpath: Path, steward_ids: dict,
                           findings: list[Finding]) -> None:
    prov = cand.get("provenance", {})
    if prov.get("method") == "model_extraction" and not prov.get("extraction_run_id"):
        findings.append(Finding("ONT-CANDIDATE", rel(fpath),
                                "model extraction requires an extraction_run_id"))
    if cand.get("review_state") == "accepted":
        disp = cand.get("disposition")
        if not disp:
            findings.append(Finding("ONT-CANDIDATE", rel(fpath),
                                    "accepted candidate has no recorded disposition"))
        else:
            steward = steward_ids.get(disp.get("decided_by"))
            if steward is None:
                findings.append(Finding("ONT-CANDIDATE", rel(fpath),
                                        f"disposition decided_by {disp.get('decided_by')!r} is not a "
                                        "manifest steward"))
            elif steward.get("identity_kind") in ("worker", "agent"):
                findings.append(Finding("ONT-CANDIDATE", rel(fpath),
                                        "a worker/agent identity cannot accept a candidate"))


def check_release_record(relrec: dict, fpath: Path, steward_ids: dict,
                         findings: list[Finding]) -> None:
    # DECISION (round-4 review observation): a roster MAY list an agent
    # identity, even as accountable_steward — preparation is worker work by
    # design. The invariant lives HERE, at every consequential usage:
    # publication and disposition check identity_kind and fail closed.
    steward = steward_ids.get(relrec.get("decided_by"))
    if steward is None:
        findings.append(Finding("ONT-RELEASE", rel(fpath),
                                f"decided_by {relrec.get('decided_by')!r} is not a manifest steward"))
    elif steward.get("role") != "accountable_steward":
        findings.append(Finding("ONT-RELEASE", rel(fpath),
                                f"decided_by {relrec.get('decided_by')!r} is not an accountable steward"))
    elif steward.get("identity_kind") in ("worker", "agent"):
        findings.append(Finding("ONT-RELEASE", rel(fpath),
                                "a worker/agent identity cannot publish a package"))
    if relrec.get("compatibility_class") in ("breaking", "retiring") and \
            not relrec.get("migration_map_ref"):
        findings.append(Finding("ONT-RELEASE", rel(fpath),
                                "breaking/retiring release requires migration_map_ref"))
    # Per-signal quality exceptions (release-review finding 9): an exception
    # releases ONE named threshold, never the measurement itself.
    exceptions = relrec.get("quality_exceptions") or []
    if exceptions and not relrec.get("quality_report_ref"):
        findings.append(Finding("ONT-RELEASE", rel(fpath),
                                "quality_exceptions release thresholds, never the measurement — "
                                "quality_report_ref is required beside them"))
    seen_signals: set[str] = set()
    for exc in exceptions:
        sig = str(exc.get("signal"))
        if sig in seen_signals:
            findings.append(Finding("ONT-RELEASE", rel(fpath),
                                    f"duplicate quality exception for signal {sig}"))
        seen_signals.add(sig)


def duplicate_ids(pkg: Package) -> list[str]:
    seen: set[str] = set()
    dups: list[str] = []
    for doc in pkg.files.values():
        for term in doc.get("concepts", []) + doc.get("relations", []):
            tid = term["id"]
            if tid in seen:
                dups.append(tid)
            seen.add(tid)
    return dups


def check_package(pkg: Package, findings: list[Finding], resolve_kernel) -> None:
    manifest = pkg.manifest
    mpath = pkg.dir / "package.yaml"
    ns = manifest.get("namespace", "")
    lifecycle = manifest.get("lifecycle_state")

    # Kernel-import posture.
    kernel = None
    if pkg.is_kernel:
        if "kernel_import" in manifest:
            findings.append(Finding("ONT-KERNEL-IMPORT", rel(mpath),
                                    "the kernel package must not import a kernel"))
    else:
        ki = manifest.get("kernel_import")
        if not ki:
            findings.append(Finding("ONT-KERNEL-IMPORT", rel(mpath),
                                    "domain package missing exact kernel_import"))
        else:
            kernel = resolve_kernel()
            if kernel is not None:
                if kernel.manifest.get("package_digest") != ki.get("package_digest"):
                    findings.append(Finding("ONT-KERNEL-IMPORT", rel(mpath),
                                            "kernel_import digest does not match the resolved kernel"))

    # F15: the declared namespace IS the package identity, xf/core is
    # kernel-only, and the openxfactory owner layer is kernel-only.
    if manifest.get("namespace") != pkg.package_id:
        findings.append(Finding("ONT-NAMESPACE", rel(mpath),
                                f"namespace {manifest.get('namespace')!r} must equal package_id"))
    if manifest.get("namespace") == "xf/core" and not pkg.is_kernel:
        findings.append(Finding("ONT-NAMESPACE", rel(mpath),
                                "a domain package cannot squat the kernel namespace xf/core"))
    if (manifest.get("owner", {}).get("layer") == "openxfactory") != pkg.is_kernel:
        findings.append(Finding("ONT-NAMESPACE", rel(mpath),
                                "owner layer openxfactory is kernel-only (and required for the kernel)"))

    # package_id agreement across files + namespace ownership of every term.
    for fname, doc in pkg.files.items():
        if doc.get("package_id") not in (None, pkg.package_id):
            findings.append(Finding("ONT-NAMESPACE", rel(pkg.dir / fname),
                                    f"package_id {doc.get('package_id')!r} disagrees with manifest {pkg.package_id!r}"))
    for tid in list(pkg.concepts) + list(pkg.relations):
        if not tid.startswith(ns + "/"):
            findings.append(Finding("ONT-NAMESPACE", rel(mpath),
                                    f"term {tid} is outside package namespace {ns}"))

    for dup in duplicate_ids(pkg):
        findings.append(Finding("ONT-ID-DUP", rel(mpath), f"duplicate identifier {dup}"))

    # Term-level lifecycle discipline (add-ontology-term-lifecycle-enforcement):
    # publication is a per-term steward decision — a published/deprecated
    # package carries no draft term. A draft package stays the workshop.
    if lifecycle in ("published", "deprecated"):
        for tid, term in sorted(list(pkg.concepts.items()) + list(pkg.relations.items())):
            if term.get("lifecycle_state") == "draft":
                findings.append(Finding("ONT-TERM-LIFECYCLE", rel(mpath),
                                        f"{lifecycle} package carries draft term {tid}; "
                                        "mark each term published (or retire it) before "
                                        "release"))

    # Label/alias uniqueness within the namespace.
    labels: dict[str, str] = {}
    for tid, term in list(pkg.concepts.items()) + list(pkg.relations.items()):
        for name in [term.get("label", "")] + list(term.get("aliases", [])):
            key = name.strip().lower()
            if not key:
                continue
            if key in labels and labels[key] != tid:
                findings.append(Finding("ONT-LABEL-COLLISION", rel(mpath),
                                        f"label/alias {name!r} collides between {labels[key]} and {tid}"))
            labels.setdefault(key, tid)

    def resolvable(tid: str) -> bool:
        if tid in pkg.concepts or tid in pkg.relations:
            return True
        if not pkg.is_kernel and tid.startswith("xf/core/"):
            k = resolve_kernel()
            return k is not None and (tid in k.concepts or tid in k.relations)
        return False

    # Parents resolve; specialization is acyclic.
    for tid, term in pkg.concepts.items():
        for parent in term.get("parents", []):
            if not resolvable(parent):
                findings.append(Finding("ONT-PARENT-MISSING", rel(mpath),
                                        f"{tid}: parent {parent} does not resolve"))
    state: dict[str, int] = {}

    def visit(tid: str, stack: tuple[str, ...]) -> None:
        if state.get(tid) == 2:
            return
        if state.get(tid) == 1:
            cycle = " -> ".join(stack[stack.index(tid):] + (tid,))
            findings.append(Finding("ONT-CYCLE", rel(mpath), f"specialization cycle: {cycle}"))
            return
        state[tid] = 1
        for parent in pkg.concepts.get(tid, {}).get("parents", []):
            if parent in pkg.concepts:
                visit(parent, stack + (tid,))
        state[tid] = 2

    for tid in sorted(pkg.concepts):
        visit(tid, ())

    # Relation domain/range resolve.
    for tid, rdef in pkg.relations.items():
        for end in ("domain", "range"):
            for cid in rdef.get(end, []):
                if not resolvable(cid):
                    findings.append(Finding("ONT-RELATION-RANGE", rel(mpath),
                                            f"{tid}: {end} concept {cid} does not resolve"))

    # Source/steward completeness.
    steward_ids = {s["steward_id"]: s for s in manifest.get("stewards", [])}
    for tid, term in list(pkg.concepts.items()) + list(pkg.relations.items()):
        for src in term.get("sources", []):
            if src not in pkg.sources:
                findings.append(Finding("ONT-SOURCE-MISSING", rel(mpath),
                                        f"{tid}: source {src!r} not registered in the source inventory"))
        stw = term.get("steward")
        if stw and stw not in steward_ids:
            findings.append(Finding("ONT-SOURCE-MISSING", rel(mpath),
                                    f"{tid}: steward {stw!r} not in the manifest steward roster"))

    # External mappings: registered, external, licensed.
    for m in pkg.mappings:
        sysid = m.get("system_id")
        src = pkg.sources.get(sysid)
        if src is None:
            findings.append(Finding("ONT-MAPPING-UNREGISTERED", rel(mpath),
                                    f"mapping {m.get('concept_id')}: system {sysid!r} is not registered"))
            continue
        if not str(src.get("source_kind", "")).startswith("external_"):
            findings.append(Finding("ONT-MAPPING-UNREGISTERED", rel(mpath),
                                    f"mapping {m.get('concept_id')}: system {sysid!r} is not an externally identified system"))
        if m.get("quoted_definition") is not None and \
                "definition_quote" not in (src.get("permitted_use") or []):
            findings.append(Finding("ONT-LICENSE", rel(mpath),
                                    f"mapping {m.get('concept_id')}: quoted_definition without a "
                                    f"definition_quote permitted use on {sysid!r}"))
        if m.get("concept_id") not in pkg.concepts and not (
                not pkg.is_kernel and m.get("concept_id", "").startswith("xf/core/")):
            findings.append(Finding("ONT-RELATION-RANGE", rel(mpath),
                                    f"mapping concept {m.get('concept_id')} does not resolve"))

    # Compatibility, migration, retention.
    compat = manifest.get("compatibility", {})
    if compat.get("class") not in (None, "initial") and "previous" not in compat:
        findings.append(Finding("ONT-COMPAT", rel(mpath),
                                f"compatibility class {compat.get('class')} requires previous"))
    if compat.get("class") in ("breaking", "retiring"):
        mm = compat.get("migration_map")
        if not mm:
            findings.append(Finding("ONT-COMPAT", rel(mpath),
                                    "breaking/retiring revision requires a migration map"))
        elif not (pkg.dir / mm).is_file():
            findings.append(Finding("ONT-COMPAT", rel(mpath),
                                    f"migration map {mm} not found in the package"))
    retained_refs = list(manifest.get("supersedes", []) or [])
    if compat.get("previous"):
        retained_refs.append(compat["previous"])
    for ref in retained_refs:
        version = ref.get("package_version", "?")
        retained = pkg.dir / "retained" / version / "package.yaml"
        if not retained.is_file():
            findings.append(Finding("ONT-RETENTION", rel(mpath),
                                    f"superseded version {version} is referenced but its retained "
                                    "bytes are missing"))
            continue
        prev = load_yaml(retained)
        if prev.get("package_digest") != ref.get("package_digest"):
            findings.append(Finding("ONT-RETENTION", rel(retained),
                                    f"retained version {version} digest differs from the reference"))
            continue
        # F3: retained bytes are VERIFIED, not trusted — recompute every
        # retained file digest and the package digest so rewritten history
        # fails as a retention violation.
        rentries = []
        rdrift = False
        for item in prev.get("inventory", []):
            rf = retained.parent / item.get("path", "")
            if not rf.is_file():
                findings.append(Finding("ONT-RETENTION", rel(retained),
                                        f"retained file missing: {item.get('path')}"))
                rdrift = True
                continue
            actual = hashlib.sha256(rf.read_bytes()).hexdigest()
            if actual != item.get("sha256"):
                findings.append(Finding("ONT-RETENTION", rel(rf),
                                        "retained bytes differ from the recorded sha256; "
                                        "history is rewritten"))
                rdrift = True
            rentries.append((item.get("path", ""), item.get("sha256", "")))
        if not rdrift and compute_package_digest(rentries) != ref.get("package_digest"):
            findings.append(Finding("ONT-RETENTION", rel(retained),
                                    f"retained version {version} inventory does not "
                                    "reproduce the referenced digest"))

    # Revision comparison: when the compatibility.previous version's retained
    # content is resolvable, prior terms load for EVERY class — term
    # lifecycle/version discipline (add-ontology-term-lifecycle-enforcement)
    # applies to breaking and retiring revisions too. The edge rubric (a
    # parent set change on a published concept, a relation domain/range
    # change in EITHER direction, or a term removal is breaking) stays
    # gated to non-breaking declared classes.
    prev_ref = compat.get("previous")
    if prev_ref:
        prev_dir = pkg.dir / "retained" / prev_ref.get("package_version", "?")
        prev_manifest = prev_dir / "package.yaml"
        prior_concepts: dict[str, dict] = {}
        prior_relations: dict[str, dict] = {}
        prior_loaded = False
        if prev_manifest.is_file():
            prior = load_yaml(prev_manifest)
            prior_loaded = True
            for item in prior.get("inventory", []):
                fp = prev_dir / item.get("path", "")
                if not fp.is_file():
                    continue
                doc = load_yaml(fp)
                if not isinstance(doc, dict):
                    continue
                for c in doc.get("concepts", []) or []:
                    prior_concepts.setdefault(c["id"], c)
                for r in doc.get("relations", []) or []:
                    prior_relations.setdefault(r["id"], r)
        if prior_loaded:
            # Term lifecycle moves only forward; meaning-bearing change bumps
            # effective_version, which never moves backward (F18).
            def semver(value) -> tuple:
                try:
                    return tuple(int(part) for part in str(value).split("."))
                except ValueError:
                    return (0,)

            def check_term_discipline(tid: str, prev_term: dict, cur: dict,
                                      meaning_fields: tuple) -> None:
                old_state = prev_term.get("lifecycle_state")
                new_state = cur.get("lifecycle_state")
                if old_state in LIFECYCLE_ORDER and new_state in LIFECYCLE_ORDER \
                        and LIFECYCLE_ORDER[new_state] < LIFECYCLE_ORDER[old_state]:
                    findings.append(Finding("ONT-TERM-LIFECYCLE", rel(mpath),
                                            f"{tid}: lifecycle moved backward "
                                            f"({old_state} -> {new_state}); retirement is "
                                            "permanent and identity reuse is breaking "
                                            "under a new identifier"))
                changed = []
                for field in meaning_fields:
                    old_v, new_v = prev_term.get(field), cur.get(field)
                    if isinstance(old_v, list) or isinstance(new_v, list):
                        if set(old_v or []) != set(new_v or []):
                            changed.append(field)
                    elif old_v != new_v:
                        changed.append(field)
                old_ver = semver(prev_term.get("effective_version"))
                new_ver = semver(cur.get("effective_version"))
                if new_ver < old_ver:
                    findings.append(Finding("ONT-TERM-VERSION", rel(mpath),
                                            f"{tid}: effective_version moved backward "
                                            f"({prev_term.get('effective_version')} -> "
                                            f"{cur.get('effective_version')})"))
                elif changed and new_ver == old_ver:
                    findings.append(Finding("ONT-TERM-VERSION", rel(mpath),
                                            f"{tid}: meaning-bearing content changed "
                                            f"({', '.join(changed)}) without an "
                                            "effective_version bump"))

            for tid, prev_term in sorted(prior_concepts.items()):
                cur = pkg.concepts.get(tid)
                if cur is not None:
                    check_term_discipline(tid, prev_term, cur,
                                          ("label", "aliases", "definition", "parents"))
            for tid, prev_rel in sorted(prior_relations.items()):
                cur = pkg.relations.get(tid)
                if cur is not None:
                    check_term_discipline(tid, prev_rel, cur,
                                          ("label", "definition", "domain", "range",
                                           "characteristics", "parents"))
        if prior_loaded and compat.get("class") not in ("breaking", "retiring"):
            for tid, prev_term in sorted(prior_concepts.items()):
                cur = pkg.concepts.get(tid)
                if cur is None:
                    findings.append(Finding("ONT-COMPAT", rel(mpath),
                                            f"{tid} was removed; removal requires breaking, "
                                            f"declared {compat.get('class')}"))
                    continue
                if set(cur.get("parents", [])) != set(prev_term.get("parents", [])):
                    findings.append(Finding("ONT-COMPAT", rel(mpath),
                                            f"{tid}: parent change on a published concept requires "
                                            f"breaking, declared {compat.get('class')}"))
            for tid, prev_rel in sorted(prior_relations.items()):
                cur = pkg.relations.get(tid)
                if cur is None:
                    findings.append(Finding("ONT-COMPAT", rel(mpath),
                                            f"{tid} was removed; removal requires breaking, "
                                            f"declared {compat.get('class')}"))
                    continue
                for end in ("domain", "range"):
                    if set(cur.get(end, [])) != set(prev_rel.get(end, [])):
                        findings.append(Finding("ONT-COMPAT", rel(mpath),
                                                f"{tid}: {end} change in either direction requires "
                                                f"breaking, declared {compat.get('class')}"))

    # Kernel adoption evidence at publication (F14: relations included,
    # adopters deduped by identity, domain_package refs resolved against the
    # shared registry).
    if pkg.is_kernel and lifecycle != "draft":
        units = [("package", manifest.get("adoption"))] + \
                [(tid, term.get("adoption"))
                 for tid, term in list(pkg.concepts.items()) + list(pkg.relations.items())]
        for name, adoption in units:
            adoption = adoption or {}
            adopters = adoption.get("adopters", [])
            distinct = {(a.get("kind"), a.get("ref")) for a in adopters}
            if adoption.get("status") != "evidenced" or len(distinct) < 2:
                findings.append(Finding("ONT-ADOPTION", rel(mpath),
                                        f"published kernel {name}: needs two independent "
                                        f"resolvable adopters, found {len(distinct)} distinct "
                                        f"({adoption.get('status', 'absent')})"))
                continue
            for kind_a, ref in sorted(distinct):
                if kind_a == "shared_subsystem_contract" and not (ROOT / str(ref)).exists():
                    findings.append(Finding("ONT-ADOPTION", rel(mpath),
                                            f"published kernel {name}: adopter {ref} does not resolve"))
                if kind_a == "domain_package" and not PACKAGE_REGISTRY.get(str(ref)):
                    findings.append(Finding("ONT-ADOPTION", rel(mpath),
                                            f"published kernel {name}: domain_package adopter "
                                            f"{ref} does not resolve to a scanned package"))

    # Candidate rules.
    for fpath, cand in pkg.candidates:
        check_candidate_record(cand, fpath, steward_ids, findings)

    # Release rules.
    for fpath, relrec in pkg.releases:
        check_release_record(relrec, fpath, steward_ids, findings)
        if relrec.get("package_id") == pkg.package_id and \
                relrec.get("package_version") == pkg.manifest.get("package_version") and \
                relrec.get("package_digest") != pkg.manifest.get("package_digest"):
            findings.append(Finding("ONT-RELEASE", rel(fpath),
                                    "release digest does not match the package it publishes"))

    # Stewardship-policy rules (ONT-POLICY / ONT-FLOOR).
    policy_floor = None
    if pkg.policy is not None:
        for member in pkg.policy.get("council", {}).get("members", []):
            if member not in steward_ids:
                findings.append(Finding("ONT-POLICY", rel(mpath),
                                        f"council member {member!r} is not in the manifest steward roster"))
        quorum = pkg.policy.get("council", {}).get("quorum", 1)
        if quorum > len(pkg.policy.get("council", {}).get("members", [])):
            findings.append(Finding("ONT-POLICY", rel(mpath),
                                    "council quorum exceeds the member count"))
        policy_floor = pkg.policy.get("aggregation_floor", {})
        if policy_floor.get("distinct_subjects", 0) < 2 and \
                not policy_floor.get("floor_exception_ref"):
            findings.append(Finding("ONT-FLOOR", rel(mpath),
                                    "policy declares a distinct-subject floor below two without a "
                                    "recorded, reviewed exception"))

    # Worker-profile rules (ONT-PROFILE): every required term resolves in
    # the package or its kernel, so a compiled worker context is well-defined
    # — and none of them is retired (retired terms refuse new compilation).
    for fpath, prof in pkg.profiles:
        for tid in prof.get("required_terms", []):
            if not resolvable(tid):
                findings.append(Finding("ONT-PROFILE", rel(fpath),
                                        f"profile {prof.get('profile_id')}: required term "
                                        f"{tid} does not resolve"))
                continue
            tdef = pkg.concepts.get(tid) or pkg.relations.get(tid)
            if tdef is None and not pkg.is_kernel and tid.startswith("xf/core/"):
                k = resolve_kernel()
                if k is not None:
                    tdef = k.concepts.get(tid) or k.relations.get(tid)
            if tdef is not None and tdef.get("lifecycle_state") == "retired":
                findings.append(Finding("ONT-TERM-LIFECYCLE", rel(fpath),
                                        f"profile {prof.get('profile_id')}: required term "
                                        f"{tid} is retired; retired terms refuse new "
                                        "worker contexts"))

    # Maintenance-report rules (ONT-MAINTENANCE): a fired trigger names its
    # mode and the candidate(s) it opened.
    for fpath, mreport in pkg.maintenance:
        for entry in mreport.get("triggers_evaluated", []):
            if entry.get("fired") and not (entry.get("mode") and entry.get("candidate_refs")):
                findings.append(Finding("ONT-MAINTENANCE", rel(fpath),
                                        f"fired trigger {entry.get('trigger')} must name its mode "
                                        "and candidate_refs"))
        fired_any = any(e.get("fired") for e in mreport.get("triggers_evaluated", []))
        if mreport.get("drift_found") != fired_any:
            findings.append(Finding("ONT-MAINTENANCE", rel(fpath),
                                    "drift_found disagrees with the evaluated triggers"))

    # Quality report rules.
    for fpath, q in pkg.quality:
        floor = q.get("aggregation_floor", {})
        fs = floor.get("distinct_subjects", 0)
        ft = floor.get("distinct_tenants", 0)
        if fs < 2 and not floor.get("floor_exception_ref"):
            findings.append(Finding("ONT-FLOOR", rel(fpath),
                                    "a distinct-subject floor below two requires a recorded, "
                                    "reviewed exception"))
        if policy_floor:
            if fs < policy_floor.get("distinct_subjects", 1) or \
                    ft < policy_floor.get("distinct_tenants", 1):
                findings.append(Finding("ONT-FLOOR", rel(fpath),
                                        "report floor is weaker than the policy's standing "
                                        "aggregation floor"))
        for sig in q.get("term_signals", []) or []:
            if sig.get("distinct_subjects", 0) < fs or sig.get("distinct_tenants", 0) < ft:
                findings.append(Finding("ONT-FLOOR", rel(fpath),
                                        f"term signal {sig.get('term_form')!r} is below the "
                                        "aggregation floor and must be withheld"))
        for sig in q.get("signals", []):
            if sig.get("signal") == "fixture_accuracy" and not sig.get("fixture_set_digest"):
                findings.append(Finding("ONT-QUALITY", rel(fpath),
                                        "fixture_accuracy requires the pinned fixture-set digest"))

    # Beside-package maintenance INPUTS respect the policy's standing
    # floor (release-review finding 6, validator leg).
    if policy_floor:
        for fpath, mi in pkg.maintenance_inputs:
            for entry in mi.get("unknown_terms") or []:
                if entry.get("distinct_subjects", 0) < policy_floor.get("distinct_subjects", 1) \
                        or entry.get("distinct_tenants", 0) < policy_floor.get("distinct_tenants", 1):
                    findings.append(Finding("ONT-FLOOR", rel(fpath),
                                            f"maintenance input term {entry.get('term_form')!r} "
                                            "is below the policy aggregation floor"))

    # F16: breaking/retiring releases carry their consumer-impact report.
    for fpath, relrec in pkg.releases:
        if relrec.get("compatibility_class") in ("breaking", "retiring"):
            ciref = relrec.get("consumer_impact_ref")
            if not ciref:
                findings.append(Finding("ONT-RELEASE", rel(fpath),
                                        "breaking/retiring release requires consumer_impact_ref"))
            elif not (pkg.dir / str(ciref)).is_file():
                findings.append(Finding("ONT-RELEASE", rel(fpath),
                                        f"consumer_impact_ref {ciref} not found beside the package"))

    # Semantic contexts compiled against this package.
    for fpath, ctx in pkg.contexts:
        check_context(ctx, fpath, pkg, resolve_kernel, findings)


def check_context(ctx: dict, fpath: Path, pkg: Package | None, resolve_kernel,
                  findings: list[Finding]) -> None:
    pin = ctx.get("package_pin", {})
    closure = ctx.get("closure", {})
    # Package-independent rules run FIRST (release-review finding 7): a
    # travelling context is checked wherever it lands.
    if closure.get("status") == "truncated" and not (closure.get("omitted") or []):
        findings.append(Finding("ONT-CONTEXT-CLOSURE", rel(fpath),
                                "truncated context must itemize each omitted member"))
    kctx = resolve_kernel()
    kpin = ctx.get("kernel_pin", {})
    if kctx is not None and kpin.get("package_digest") not in (
            None, kctx.manifest.get("package_digest")):
        findings.append(Finding("ONT-CONTEXT-PIN", rel(fpath),
                                "kernel pin digest does not match the resolved kernel"))
    binding = ctx.get("tenant_binding")
    if binding and binding.get("package_id") != pin.get("package_id"):
        findings.append(Finding("ONT-BINDING", rel(fpath),
                                f"tenant binding is pinned to {binding.get('package_id')} but the "
                                f"context is compiled against {pin.get('package_id')}"))
    if pkg is None:
        # Loose context: resolve its package through the shared registry.
        candidates = PACKAGE_REGISTRY.get(str(pin.get("package_id")), [])
        match = next((c for c in candidates
                      if c.manifest.get("package_digest") == pin.get("package_digest")), None)
        if match is not None:
            pkg = match
        elif candidates:
            findings.append(Finding("ONT-CONTEXT-PIN", rel(fpath),
                                    "package pin digest does not match any scanned package "
                                    f"with id {pin.get('package_id')}"))
            return
        else:
            return  # package not present in this tree; closure unverifiable here
    if pin.get("package_id") == pkg.package_id and \
            pin.get("package_digest") != pkg.manifest.get("package_digest"):
        findings.append(Finding("ONT-CONTEXT-PIN", rel(fpath),
                                "package pin digest does not match the resolved package"))
    kernel = resolve_kernel() if not pkg.is_kernel else pkg

    def lookup_concept(tid: str) -> dict | None:
        if tid in pkg.concepts:
            return pkg.concepts[tid]
        if kernel is not None and tid in kernel.concepts:
            return kernel.concepts[tid]
        return None

    def lookup_relation(tid: str) -> dict | None:
        if tid in pkg.relations:
            return pkg.relations[tid]
        if kernel is not None and tid in kernel.relations:
            return kernel.relations[tid]
        return None

    terms = set(ctx.get("terms", []))
    # Retired terms refuse new compilation: a context at the CURRENT package
    # digest cannot carry one (add-ontology-term-lifecycle-enforcement);
    # contexts pinned at prior digests keep their original interpretation.
    if pin.get("package_digest") == pkg.manifest.get("package_digest"):
        for tid in sorted(terms):
            tdef = lookup_concept(tid) or lookup_relation(tid)
            if tdef is not None and tdef.get("lifecycle_state") == "retired":
                findings.append(Finding("ONT-TERM-LIFECYCLE", rel(fpath),
                                        f"context subset includes retired term {tid}; "
                                        "retired terms refuse new compilation"))
    closure = ctx.get("closure", {})
    omitted = set(closure.get("omitted", []) or [])
    missing: list[str] = []
    for tid in sorted(terms):
        cdef = lookup_concept(tid)
        if cdef is not None:
            queue = list(cdef.get("parents", []))
            while queue:
                parent = queue.pop()
                if parent in terms or parent in omitted:
                    continue
                missing.append(f"{tid}: ancestor {parent}")
                pdef = lookup_concept(parent)
                if pdef:
                    queue.extend(pdef.get("parents", []))
            continue
        rdef = lookup_relation(tid)
        if rdef is not None:
            for end in ("domain", "range"):
                for cid in rdef.get(end, []):
                    if cid not in terms and cid not in omitted:
                        missing.append(f"{tid}: {end} concept {cid}")
    if missing and closure.get("status") == "closed":
        findings.append(Finding("ONT-CONTEXT-CLOSURE", rel(fpath),
                                "subset declared closed but omits closure members: "
                                + "; ".join(sorted(missing))))


def expected_failure(path: Path) -> tuple[str | None, str | None]:
    code = detail = None
    for line in path.read_text().splitlines():
        if line.startswith("# expected_failure:"):
            code = line.split(":", 1)[1].strip()
        elif line.startswith("# expected_failure_detail:"):
            detail = line.split(":", 1)[1].strip()
    return code, detail


def discover_units(base: Path):
    """Yield (kind, path) units: ('package', dir) or ('loose', file)."""
    packages = []
    loose = []
    for manifest in sorted(base.rglob("package.yaml")):
        if "retained" in manifest.parts:
            continue
        packages.append(manifest.parent)
    pkg_dirs = set(packages)
    for f in sorted(list(base.rglob("*.yaml")) + list(base.rglob("*.yml"))):
        if ".template." in f.name:
            continue  # instantiation stubs carry placeholders by design
        if any(parent in pkg_dirs for parent in f.parents):
            continue
        try:
            doc = load_yaml(f)
        except yaml.YAMLError:
            continue
        if isinstance(doc, dict) and (
                doc.get("kind") in FAMILY_KINDS
                or "semantic_context" in doc
                or any(isinstance(v, dict) and "semantic_context" in v
                       for v in doc.values() if isinstance(v, dict))):
            loose.append(f)
    for d in packages:
        yield "package", d
    for f in loose:
        yield "loose", f


def validate_unit(kind: str, path: Path, schemas, resolve_kernel) -> list[Finding]:
    findings: list[Finding] = []
    if kind == "package":
        load_package(path, schemas, findings, resolve_kernel)
    else:
        doc = load_yaml(path)
        doc_kind = doc.get("kind")
        if doc_kind not in FAMILY_KINDS:
            # A non-family document carrying an embedded semantic_context
            # block (task 6.4): the ontology rules govern the BLOCK, not the
            # host document (release-review finding 2) — packet fields like
            # subject_refs are the memory-gateway contract's jurisdiction.
            blocks = []
            if isinstance(doc.get("semantic_context"), dict):
                blocks.append(doc["semantic_context"])
            for v in doc.values():
                if isinstance(v, dict) and isinstance(v.get("semantic_context"), dict):
                    blocks.append(v["semantic_context"])
            for block in blocks:
                for key in ("semantic_context_id", "content_digest",
                            "kernel_pin", "package_pin"):
                    if key not in block:
                        findings.append(Finding(
                            "ONT-CONTEXT-PIN", rel(path),
                            f"embedded semantic_context missing {key}; artifacts "
                            "using domain semantics retain their exact identity"))
                findings.extend(value_scan(block, path))
            return findings
        findings.extend(schema_findings(schemas[doc_kind], doc, path))
        findings.extend(value_scan(doc, path))
        if doc_kind in ("xfactory_ontology_release_record",
                        "xfactory_ontology_candidate_record"):
            # F10: governance records are governed by ARTIFACT, not location —
            # resolve the roster through the registry and apply the same
            # rules. Resolution is by EXACT DIGEST for release records and by
            # unambiguous package_id for candidates (which carry no digest);
            # an arbitrary first-entry roster re-opened the bypass as
            # roster confusion (release-review finding N4).
            code = ("ONT-RELEASE" if doc_kind.endswith("release_record")
                    else "ONT-CANDIDATE")
            pkgs = PACKAGE_REGISTRY.get(str(doc.get("package_id")), [])
            match = None
            if not pkgs:
                findings.append(Finding(code, rel(path),
                                        f"record for {doc.get('package_id')!r} does not "
                                        "resolve to any package in the scanned tree"))
            elif doc_kind.endswith("release_record"):
                match = next((p for p in pkgs
                              if p.manifest.get("package_digest")
                              == doc.get("package_digest")), None)
                if match is None:
                    findings.append(Finding(code, rel(path),
                                            "record digest does not match any scanned "
                                            f"package with id {doc.get('package_id')!r}; a "
                                            "loose record resolves by exact digest, never "
                                            "by first match"))
            elif len(pkgs) == 1:
                match = pkgs[0]
            else:
                findings.append(Finding(code, rel(path),
                                        f"{len(pkgs)} scanned packages share id "
                                        f"{doc.get('package_id')!r}; a loose candidate "
                                        "cannot prove its roster and fails closed"))
            if match is not None:
                roster = {s["steward_id"]: s
                          for s in match.manifest.get("stewards", [])}
                if doc_kind.endswith("release_record"):
                    check_release_record(doc, path, roster, findings)
                else:
                    check_candidate_record(doc, path, roster, findings)
        if doc_kind == "xfactory_semantic_context":
            check_context(doc, path, None, resolve_kernel, findings)
        if doc_kind == "xfactory_ontology_quality_report":
            fake = Package(path.parent, {"stewards": []})
            fake.quality.append((path, doc))
            check_package_quality_only(fake, findings)
    return findings


def check_package_quality_only(pkg: Package, findings: list[Finding]) -> None:
    for fpath, q in pkg.quality:
        floor = q.get("aggregation_floor", {})
        fs = floor.get("distinct_subjects", 0)
        ft = floor.get("distinct_tenants", 0)
        if fs < 2 and not floor.get("floor_exception_ref"):
            findings.append(Finding("ONT-FLOOR", rel(fpath),
                                    "a distinct-subject floor below two requires a recorded, "
                                    "reviewed exception"))
        for sig in q.get("term_signals", []) or []:
            if sig.get("distinct_subjects", 0) < fs or sig.get("distinct_tenants", 0) < ft:
                findings.append(Finding("ONT-FLOOR", rel(fpath),
                                        f"term signal {sig.get('term_form')!r} is below the "
                                        "aggregation floor and must be withheld"))
        for sig in q.get("signals", []):
            if sig.get("signal") == "fixture_accuracy" and not sig.get("fixture_set_digest"):
                findings.append(Finding("ONT-QUALITY", rel(fpath),
                                        "fixture_accuracy requires the pinned fixture-set digest"))


def run_suite(repo_path: Path | None) -> tuple[list[Finding], list[str]]:
    PACKAGE_REGISTRY.clear()
    schemas = load_schemas()
    errors: list[Finding] = []
    notes: list[str] = []
    kernel_cache: list[Package | None] = []

    def resolve_kernel() -> Package | None:
        if not kernel_cache:
            side: list[Finding] = []
            kernel_cache.append(load_package(CORE_DIR, schemas, side, lambda: None))
        return kernel_cache[0]

    # Registration prepass (finding N1): the registry is complete BEFORE
    # any unit validates, so resolution never depends on discovery order —
    # the real kernel's domain_package adopters live in the examples/pilot
    # tree that would otherwise load after it. Findings are discarded here;
    # every package is re-validated for real in its own pass.
    def prepass(dirs: list[Path]) -> None:
        for pdir in dirs:
            discard: list[Finding] = []
            try:
                load_package(pdir, schemas, discard, resolve_kernel)
            except Exception:
                pass  # a broken unit registers nothing; its own pass reports it

    if EXAMPLES_DIR.is_dir():
        prepass([p for k, p in discover_units(EXAMPLES_DIR)
                 if k == "package" and NEGATIVE_DIR not in p.parents
                 and p != NEGATIVE_DIR])

    # Core kernel package validates positive.
    core_findings: list[Finding] = []
    load_package(CORE_DIR, schemas, core_findings, lambda: None)
    if core_findings:
        errors.extend(core_findings)
    notes.append("core kernel package validated")

    # Positive examples.
    pos_count = 0
    if EXAMPLES_DIR.is_dir():
        for kind, path in discover_units(EXAMPLES_DIR):
            if NEGATIVE_DIR in path.parents or path == NEGATIVE_DIR:
                continue
            found = validate_unit(kind, path, schemas, resolve_kernel)
            if found:
                errors.append(Finding("ONT-SELFTEST", rel(path),
                                      "positive example failed: " + "; ".join(f.line() for f in found)))
            pos_count += 1
    notes.append(f"{pos_count} positive example unit(s)")

    # Negative examples must fail for their declared reason.
    neg_count = 0
    if NEGATIVE_DIR.is_dir():
        for kind, path in discover_units(NEGATIVE_DIR):
            header_file = path / "package.yaml" if kind == "package" else path
            code, detail = expected_failure(header_file)
            if not code:
                errors.append(Finding("ONT-SELFTEST", rel(path),
                                      "negative fixture missing # expected_failure header"))
                continue
            found = validate_unit(kind, path, schemas, resolve_kernel)
            hits = [f for f in found if f.code == code]
            if detail:
                hits = [f for f in hits if detail in f.message]
            if not hits:
                got = "; ".join(sorted({f.code for f in found})) or "no findings"
                errors.append(Finding("ONT-SELFTEST", rel(path),
                                      f"negative fixture no longer fails as {code}"
                                      + (f" (detail {detail!r})" if detail else "")
                                      + f"; got: {got}"))
            neg_count += 1
    if neg_count < 49:
        errors.append(Finding("ONT-SELFTEST", rel(NEGATIVE_DIR),
                              f"negative fixture count {neg_count} fell below the "
                              "pinned minimum of 49"))
    notes.append(f"{neg_count} negative fixture(s) asserted")

    # Layer 2: optional repo scan. The scan gets its OWN registry scope
    # (release-review finding N4): a consumer's loose records must resolve
    # against the consumer's packages only — never against openxFactory's
    # example fixtures, whose rosters have nothing to do with the record.
    if repo_path is not None:
        PACKAGE_REGISTRY.clear()
        prepass([p for k, p in discover_units(repo_path)
                 if k == "package" and CONTRACT_DIR not in p.parents
                 and p != CORE_DIR])
        scanned = 0
        for kind, path in discover_units(repo_path):
            if CONTRACT_DIR in path.parents or path == CORE_DIR:
                continue
            errors.extend(validate_unit(kind, path, schemas, resolve_kernel))
            scanned += 1
        for cm in sorted(repo_path.rglob("hermes/domain/content-manifest.yaml")):
            doc = load_yaml(cm)
            content_set = (doc or {}).get("content_set") if isinstance(doc, dict) else None
            decl = content_set.get("domain_ontology") if isinstance(content_set, dict) else None
            if decl:
                # Declared locations are repo-root-relative; the manifest
                # lives at <repo>/hermes/domain/content-manifest.yaml.
                repo_root = cm.parent.parent.parent
                target = repo_root / decl.get("directory", decl.get("path", ""))
                if not (target / "package.yaml").is_file():
                    errors.append(Finding("ONT-MANIFEST-PIN", rel(cm),
                                          f"declared domain_ontology target {decl} has no package"))
                else:
                    sub: list[Finding] = []
                    load_package(target, schemas, sub, resolve_kernel)
                    if sub:
                        errors.append(Finding("ONT-MANIFEST-PIN", rel(cm),
                                              "declared ontology package is invalid: "
                                              + "; ".join(f.line() for f in sub)))
        notes.append(f"repo scan: {scanned} unit(s)")

    return sorted(errors, key=lambda f: (f.code, f.path, f.message)), notes


def readiness(pkg_dir: Path) -> int:
    """Generated-domain readiness (task 5.6): `ontology_ready` only when the
    package validates clean, is published by an accountable release record,
    carries no placeholder stewards/concepts, ships a stewardship policy,
    and satisfies the policy's quality gate (or the release records a
    reviewed exception). Anything less is `domain_scaffold_required` — the
    non-operational state consumers key on. Exit 0 ready, 3 scaffold."""
    schemas = load_schemas()
    findings: list[Finding] = []
    kernel_cache: list = []

    def resolve_kernel():
        if not kernel_cache:
            side: list[Finding] = []
            kernel_cache.append(load_package(CORE_DIR, schemas, side, lambda: None))
        return kernel_cache[0]

    pkg = load_package(pkg_dir, schemas, findings, resolve_kernel)
    reasons: list[str] = []
    if findings:
        reasons.append(f"package has {len(findings)} validation finding(s)")
    if pkg is None:
        reasons.append("package failed to load (digest drift fails closed)")
    else:
        m = pkg.manifest
        if m.get("lifecycle_state") != "published":
            reasons.append(f"lifecycle_state is {m.get('lifecycle_state')!r}, not published")
        for s in m.get("stewards", []):
            if "UNASSIGNED" in str(s.get("name", "")):
                reasons.append(f"steward {s.get('steward_id')} is an unassigned placeholder")
        for tid, c in sorted(pkg.concepts.items()):
            if tid.endswith("/placeholder_subject") or c.get("label") == "Placeholder Subject":
                reasons.append(f"placeholder concept {tid} awaits Domain Hermes review")
        if pkg.policy is None:
            reasons.append("no stewardship policy is inventoried in the package")
        for fpath, cand in pkg.candidates:
            if cand.get("review_state") in ("open", "in_review") and cand.get("conflicts"):
                reasons.append(
                    f"candidate {cand.get('candidate_id')} carries unresolved "
                    "conflicts; structured imports take precedence and the "
                    "conflict blocks readiness until dispositioned")
        current = m.get("package_digest")
        release_recs = [r for _, r in pkg.releases if r.get("package_digest") == current]
        if not release_recs:
            reasons.append("no release record publishes the current package digest")
        else:
            rel_rec = release_recs[0]
            gate = (pkg.policy or {}).get("quality_gate", {})
            if gate.get("required_signals"):
                # Per-signal exceptions (release-review finding 9): each
                # releases exactly one signal's threshold; the measurement —
                # a quality report over the CURRENT digest — is never excused.
                excepted = {str(e.get("signal"))
                            for e in rel_rec.get("quality_exceptions") or []}
                qreports = [q for _, q in pkg.quality
                            if q.get("package_digest") == current]
                if not qreports:
                    reasons.append("no quality report covers the current package digest "
                                   "(an exception releases a threshold, never the measurement)")
                else:
                    sigmap: dict[str, float] = {}
                    for q in qreports:
                        for sig in q.get("signals", []):
                            den = sig.get("denominator") or 0
                            if den:
                                sigmap[sig.get("signal")] = sig.get("numerator", 0) / den
                    for req in gate["required_signals"]:
                        name = req.get("signal")
                        if name in excepted:
                            continue
                        value = sigmap.get(name)
                        if value is None:
                            reasons.append(f"required quality signal {name} is missing "
                                           "(a per-signal reviewed exception would release "
                                           "this block)")
                            continue
                        if "min_value" in req and value < req["min_value"]:
                            reasons.append(f"quality signal {name} {value:.3f} below "
                                           f"required {req['min_value']}")
                        if "max_value" in req and value > req["max_value"]:
                            reasons.append(f"quality signal {name} {value:.3f} above "
                                           f"allowed {req['max_value']}")
    if reasons:
        print("READINESS domain_scaffold_required")
        for r in sorted(set(reasons)):
            print(f"REASON {r}")
        return 3
    print("READINESS ontology_ready")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("repo_path", nargs="?", default=None)
    ap.add_argument("--strict", action="store_true",
                    help="reserved for parity with sibling validators; all checks already error")
    ap.add_argument("--determinism", action="store_true",
                    help="run the suite twice and fail on any output difference")
    ap.add_argument("--readiness", metavar="PKG_DIR",
                    help="evaluate generated-domain ontology readiness for one "
                         "package dir (exit 0 ontology_ready, 3 domain_scaffold_required)")
    args = ap.parse_args()
    if args.readiness:
        return readiness(Path(args.readiness).resolve())

    repo = Path(args.repo_path).resolve() if args.repo_path else None
    findings, notes = run_suite(repo)
    if args.determinism:
        findings2, _ = run_suite(repo)
        if [f.line() for f in findings] != [f.line() for f in findings2]:
            print("ERROR determinism check failed: repeated validation differed", file=sys.stderr)
            return 2
        notes.append("determinism: identical findings on repeat")

    for note in notes:
        print(f"NOTE {note}")
    for f in findings:
        print(f"FINDING {f.line()}")
    if findings:
        print(f"FAIL {len(findings)} finding(s)")
        return 1
    print("OK domain-ontology family valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
