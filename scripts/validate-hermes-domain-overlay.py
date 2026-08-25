#!/usr/bin/env python3
"""Validate the hermes-domain-overlay contract family (add-hermes-domain-overlay-contract).

The openxFactory-owned canonical validator for the family's document kinds —
`hermes_domain_overlay`, `hermes_subject_overlay`, `hermes_overlay_descriptor`
and `hermes_domain_content_manifest`
(`contracts/hermes-domain-overlay/*.schema.yaml`). Run from the pinned
openxFactory checkout, never copied into domain repos:

    python3 scripts/validate-hermes-domain-overlay.py [DOMAIN_REPO_PATH]

Two layers run:

1. Packaged reference examples (`contracts/hermes-domain-overlay/examples/`):
   every `*.example.yaml` must pass; every file under `negative/` must fail
   for its INTENDED reason (declared in its `# expected_failure:` header) —
   the self-test fails closed if any negative stops failing for its reason
   or any positive example fails. Repo-SHAPED negatives are directories under
   `negative/` (a repo needs more than one file to be wrong in the ways that
   matter): a directory carrying an ontology starter marker is checked for
   generated-domain completeness, and a directory carrying an overlay
   descriptor is walked exactly as a real repo's declared paths are, with the
   `# expected_failure:` header read from the document at its declared
   subject path.
2. Optional real artifacts under DOMAIN_REPO_PATH: every descriptor-declared
   path (or the documented convention `hermes/domain/overlay.yaml` when no
   descriptor exists) is dispatched BY THE KIND of the document found there;
   a descriptor, when present, is validated including path existence.

Deterministic checks the schema shape cannot express:
  - `authority_boundaries` carries exactly one domain-owned list named
    `<domain.id>_owns`, non-empty;
  - the no-overlap rule: no authority item appears in more than one
    boundary list;
  - descriptor role keys are limited to domain/client/customer, and every
    declared path exists when a repo path is supplied;
  - subject-overlay address self-consistency and uniqueness (every `policies`
    key equals its `policy_id`; every policy's `policy_namespace` equals the
    subject's; no address declared twice), the prohibited-block list (a
    subject adds constraints and never grants, widens, or waives), and
    cross-document identity conformance against the DOMAIN's own
    `hermes/subject/template.yaml` — skipped with notice where a repository
    ships no subject template (add-subject-overlay-contract).
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTRACT_DIR = REPO_ROOT / "contracts" / "hermes-domain-overlay"
EXAMPLES_DIR = CONTRACT_DIR / "examples"
NEGATIVE_DIR = EXAMPLES_DIR / "negative"
DESCRIPTOR_ROLES = {"domain", "client", "customer"}
CONVENTION_PATHS = {"domain": "hermes/domain/overlay.yaml"}
DESCRIPTOR_FILE = "hermes/overlay-descriptor.yaml"
CONTENT_MANIFEST_FILE = "hermes/domain/content-manifest.yaml"
# The domain's own subject-kind template, at the documented convention path —
# the same convention-then-contract idiom the family already uses for the
# domain overlay. Absent template => the cross-document identity check is
# skipped with notice, never turned into a new refusal class.
SUBJECT_TEMPLATE_FILE = "hermes/subject/template.yaml"
# Kinds this canonical validator OWNS at a declared path. Anything else keeps
# the skip-with-notice: a kind owned by another canonical validator must not be
# double-validated here, because two implementations of one rule fork canonical
# meaning (add-subject-overlay-contract).
FAMILY_VALIDATED_KINDS = {"hermes_domain_overlay", "hermes_subject_overlay"}
ROLE_KINDS = {"domain": "hermes_domain_overlay", "customer": "hermes_subject_overlay"}
FOREIGN_KIND_VALIDATORS = {"hermes_client_overlay": "scripts/validate-client-content.py"}
SUBJECT_RELATIONS = {"additive_constraints_only"}
# The Domain layer's enforceable slice. A subject overlay carrying any of these
# would be legislating for the domain from the subject seat; the invariant is
# `a subject may add constraints, never grant, widen, or waive`, enforced
# structurally on the document rather than by a comparability engine whose
# partial orders have no counterpart key for an additive named constraint.
PROHIBITED_SUBJECT_BLOCKS = {
    "authority_boundaries", "approval_scope_kinds", "required_approval_fields",
}
# Credential-shaped keys whose value would be key material rather than policy.
# A `*_ref` / `*_binding` key is deliberately absent: reference-delivered
# credentials are the governed form and must stay expressible.
CREDENTIAL_VALUE_KEYS = {
    "secret", "secrets", "token", "password", "passphrase", "api_key", "apikey",
    "private_key", "client_secret", "credential", "credentials",
}
# Explicit issuer markers only. No entropy or base64-shape heuristic: a false
# refusal on a long opaque identifier would be a new refusal class this
# contract never declared.
RAW_SECRET_MARKERS = ("-----BEGIN", "ghp_", "github_pat_", "gho_", "ghs_", "AKIA")
CONTENT_KINDS = {
    "role_authority", "policy_position", "escalation_rule", "deliberation_mix",
    "review_council", "memory_boundary", "practice_adoption",
    # Additive kind ratified by add-domain-ontology-layer (task 5.1's
    # vocabulary half): a directory holding an xFactory ontology package,
    # validated by scripts/validate-domain-ontology.py before seeding.
    "domain_ontology",
}


def _fail(findings: list[str], message: str) -> None:
    findings.append(message)


def validate_overlay(doc: object, findings: list[str]) -> None:
    if not isinstance(doc, dict):
        return _fail(findings, "overlay document is not a mapping")
    if doc.get("kind") != "hermes_domain_overlay":
        return _fail(findings, "kind is not hermes_domain_overlay")
    if not isinstance(doc.get("schema_version"), int) or doc["schema_version"] < 1:
        _fail(findings, "schema_version must be an integer >= 1")
    domain = doc.get("domain")
    if not isinstance(domain, dict):
        return _fail(findings, "missing required block: domain")
    for field in ("id", "display_name"):
        if not isinstance(domain.get(field), str) or not domain.get(field):
            _fail(findings, f"missing or empty domain.{field}")
    for field in ("approval_scope_kinds", "required_approval_fields"):
        value = domain.get(field)
        if not isinstance(value, list) or not value:
            _fail(findings, f"missing or empty {field}")
        elif not all(isinstance(item, str) and item for item in value):
            _fail(findings, f"{field} entries must be non-empty strings")
    boundaries = domain.get("authority_boundaries")
    if not isinstance(boundaries, dict):
        return _fail(findings, "missing required block: authority_boundaries")
    for required_list in ("xfactory_owns", "repository_owns"):
        value = boundaries.get(required_list)
        if not isinstance(value, list) or not value:
            _fail(findings, f"missing or empty authority_boundaries.{required_list}")
    domain_id = domain.get("id")
    expected_key = f"{domain_id}_owns" if isinstance(domain_id, str) else None
    extra_keys = [k for k in boundaries if k not in ("xfactory_owns", "repository_owns")]
    if expected_key is None or expected_key not in boundaries:
        _fail(findings, f"missing domain-owned list: expected authority_boundaries.{expected_key}")
    elif not isinstance(boundaries[expected_key], list) or not boundaries[expected_key]:
        _fail(findings, f"domain-owned list {expected_key} must be a non-empty list")
    for key in extra_keys:
        if key != expected_key:
            _fail(findings, f"unexpected boundary list {key}: the domain-owned list must be named {expected_key}")
    # no-overlap rule across all boundary lists
    seen: dict[str, str] = {}
    for list_name, value in boundaries.items():
        if not isinstance(value, list):
            continue
        for item in value:
            if item in seen and seen[item] != list_name:
                _fail(findings, f"authority item in more than one boundary list: {item} ({seen[item]} and {list_name})")
            seen.setdefault(item, list_name)


def _walk_entries(node: object, path: str):
    """Yield (dotted_path, key, value) for every mapping entry in a document,
    so a prohibited block cannot hide one level deeper than the check."""
    if isinstance(node, dict):
        for key, value in node.items():
            here = f"{path}.{key}" if path else str(key)
            yield here, key, value
            yield from _walk_entries(value, here)
    elif isinstance(node, list):
        for index, item in enumerate(node):
            yield from _walk_entries(item, f"{path}[{index}]")


def _prohibited_subject_content(doc: dict, findings: list[str]) -> None:
    for where, key, value in _walk_entries(doc, ""):
        if key in PROHIBITED_SUBJECT_BLOCKS:
            _fail(findings,
                  f"prohibited block for a subject overlay: {where} — a subject "
                  f"adds constraints and never grants, widens, or waives "
                  f"({key} is the Domain layer's enforceable slice)")
        if key in CREDENTIAL_VALUE_KEYS and isinstance(value, str) and value.strip():
            _fail(findings,
                  f"prohibited credential value at {where}: a subject overlay "
                  "carries policy, never key material")
        if isinstance(value, str) and any(m in value for m in RAW_SECRET_MARKERS):
            _fail(findings,
                  f"prohibited credential value at {where}: the value carries a "
                  "raw-secret marker")


def _validate_subject_template(subject: dict, findings: list[str], repo_path: Path) -> None:
    """Cross-document identity conformance (add-subject-overlay-contract D4):
    the DOMAIN's own subject_hermes_template decides which subject kinds exist
    and which identity fields each one requires, so no engineering (or
    clinical, or accounting) field name ever enters a domain-neutral contract.
    A repository shipping no template is skipped with notice."""
    template_path = repo_path / SUBJECT_TEMPLATE_FILE
    if not template_path.is_file():
        print(f"note: no subject template at {SUBJECT_TEMPLATE_FILE}; "
              "skipping cross-document subject identity conformance")
        return
    try:
        template = yaml.safe_load(template_path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        return _fail(findings, f"unparseable subject template {SUBJECT_TEMPLATE_FILE}: {exc}")
    if not isinstance(template, dict) or template.get("kind") != "subject_hermes_template":
        return _fail(findings, f"{SUBJECT_TEMPLATE_FILE} is not a subject_hermes_template")
    block = template.get("subject_hermes")
    if not isinstance(block, dict):
        return _fail(findings, f"{SUBJECT_TEMPLATE_FILE} carries no subject_hermes block")
    subject_kind = subject.get("subject_kind")
    declared = block.get("subject_kinds")
    if not isinstance(declared, list) or not declared:
        return _fail(findings, f"{SUBJECT_TEMPLATE_FILE} declares no subject_kinds")
    if subject_kind not in declared:
        return _fail(findings,
                     f"undeclared subject_kind {subject_kind}: the domain template "
                     f"declares {sorted(str(k) for k in declared)}")
    required_fields = block.get("required_subject_fields")
    required = required_fields.get(subject_kind) if isinstance(required_fields, dict) else None
    for field in required or []:
        value = subject.get(field)
        if value is None or (hasattr(value, "__len__") and len(value) == 0):
            _fail(findings,
                  f"template-required field missing or empty on subject: {field} "
                  f"(required by required_subject_fields.{subject_kind})")


def validate_subject_overlay(doc: object, findings: list[str], repo_path: Path | None) -> None:
    if not isinstance(doc, dict):
        return _fail(findings, "subject overlay document is not a mapping")
    if doc.get("kind") != "hermes_subject_overlay":
        return _fail(findings, "kind is not hermes_subject_overlay")
    if not isinstance(doc.get("schema_version"), int) or doc["schema_version"] < 1:
        _fail(findings, "schema_version must be an integer >= 1")
    _prohibited_subject_content(doc, findings)
    subject = doc.get("subject")
    if not isinstance(subject, dict):
        return _fail(findings, "missing required block: subject")
    for field in ("id", "subject_kind", "display_name", "policy_namespace"):
        value = subject.get(field)
        if not isinstance(value, str) or not value.strip():
            _fail(findings, f"missing or empty subject.{field}")
    relation = subject.get("relation_to_baseline")
    if relation is None or (isinstance(relation, str) and not relation.strip()):
        _fail(findings,
              "missing or empty subject.relation_to_baseline: a subject overlay "
              "DECLARES its relation to the baseline and none is inferred by default")
    elif relation not in SUBJECT_RELATIONS:
        _fail(findings,
              f"subject.relation_to_baseline must be one of {sorted(SUBJECT_RELATIONS)}, "
              f"got {relation!r}")
    policies = subject.get("policies")
    if not isinstance(policies, dict) or not policies:
        _fail(findings,
              "missing or empty subject.policies: a subject overlay declares at "
              "least one named policy")
    else:
        namespace = subject.get("policy_namespace")
        seen_addresses: dict[str, str] = {}
        for key, policy in policies.items():
            if not isinstance(policy, dict):
                _fail(findings, f"subject.policies.{key} must be a mapping")
                continue
            policy_id = policy.get("policy_id")
            if not isinstance(policy_id, str) or not policy_id.strip():
                _fail(findings, f"missing or empty policy_id for subject.policies.{key}")
            elif policy_id != key:
                _fail(findings,
                      f"policies key {key} does not match its declared policy_id "
                      f"{policy_id}: the key IS the address")
            policy_namespace = policy.get("policy_namespace")
            if not isinstance(policy_namespace, str) or not policy_namespace.strip():
                _fail(findings, f"missing or empty policy_namespace for subject.policies.{key}")
            elif isinstance(namespace, str) and policy_namespace != namespace:
                _fail(findings,
                      f"policy namespace mismatch for subject.policies.{key}: the policy "
                      f"declares {policy_namespace}, the subject declares {namespace}")
            if isinstance(policy_id, str) and isinstance(policy_namespace, str):
                address = f"{policy_namespace}/{policy_id}"
                if address in seen_addresses:
                    _fail(findings,
                          f"duplicate policy address {address}: declared by "
                          f"subject.policies.{seen_addresses[address]} and "
                          f"subject.policies.{key}")
                seen_addresses.setdefault(address, str(key))
    if repo_path is not None:
        _validate_subject_template(subject, findings, repo_path)


def validate_descriptor(doc: object, findings: list[str], repo_path: Path | None) -> None:
    if not isinstance(doc, dict):
        return _fail(findings, "descriptor document is not a mapping")
    if doc.get("kind") != "hermes_overlay_descriptor":
        return _fail(findings, "kind is not hermes_overlay_descriptor")
    if not isinstance(doc.get("schema_version"), int) or doc["schema_version"] < 1:
        _fail(findings, "schema_version must be an integer >= 1")
    paths = doc.get("overlay_paths")
    if not isinstance(paths, dict) or not paths:
        return _fail(findings, "missing or empty overlay_paths")
    for role, path in paths.items():
        if role not in DESCRIPTOR_ROLES:
            _fail(findings, f"unknown role in overlay_paths: {role} (allowed: {sorted(DESCRIPTOR_ROLES)})")
        if not isinstance(path, str) or not path:
            _fail(findings, f"overlay_paths.{role} must be a non-empty path string")
        elif repo_path is not None and not (repo_path / path).is_file():
            _fail(findings, f"dangling declared path for role {role}: {path}")


def validate_content_manifest(doc: object, findings: list[str], repo_path: Path | None) -> None:
    if not isinstance(doc, dict):
        return _fail(findings, "content manifest is not a mapping")
    if doc.get("kind") != "hermes_domain_content_manifest":
        return _fail(findings, "kind is not hermes_domain_content_manifest")
    if not isinstance(doc.get("schema_version"), int) or doc["schema_version"] < 1:
        _fail(findings, "schema_version must be an integer >= 1")
    content_set = doc.get("content_set")
    if not isinstance(content_set, dict) or not content_set:
        return _fail(findings, "missing or empty content_set")
    for kind_name, location in content_set.items():
        if kind_name not in CONTENT_KINDS:
            _fail(findings, f"unknown content kind: {kind_name} (allowed: {sorted(CONTENT_KINDS)})")
        if not isinstance(location, dict):
            _fail(findings, f"content_set.{kind_name} must be a mapping")
            continue
        forms = [form for form in ("path", "directory") if location.get(form)]
        extra = set(location) - {"path", "directory"}
        if len(forms) != 1 or extra:
            _fail(findings, f"content_set.{kind_name} must declare exactly one of path or directory")
            continue
        declared = location[forms[0]]
        if not isinstance(declared, str) or not declared:
            _fail(findings, f"content_set.{kind_name}.{forms[0]} must be a non-empty string")
        elif repo_path is not None:
            target = repo_path / declared
            exists = target.is_file() if forms[0] == "path" else target.is_dir()
            if not exists:
                _fail(findings, f"dangling declared {forms[0]} for {kind_name}: {declared}")
    omnigent = doc.get("omnigent_overlay_path")
    if omnigent is not None:
        if not isinstance(omnigent, str) or not omnigent:
            _fail(findings, "omnigent_overlay_path must be a non-empty string")
        elif repo_path is not None and not (repo_path / omnigent).is_file():
            _fail(findings, f"dangling omnigent_overlay_path: {omnigent}")


def validate_document(path: Path, repo_path: Path | None) -> list[str]:
    findings: list[str] = []
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        return [f"unparseable YAML: {exc}"]
    kind = doc.get("kind") if isinstance(doc, dict) else None
    if kind == "hermes_domain_overlay":
        validate_overlay(doc, findings)
    elif kind == "hermes_subject_overlay":
        validate_subject_overlay(doc, findings, repo_path)
    elif kind == "hermes_overlay_descriptor":
        validate_descriptor(doc, findings, repo_path)
    elif kind == "hermes_domain_content_manifest":
        validate_content_manifest(doc, findings, repo_path)
    else:
        findings.append(f"unknown kind: {kind}")
    return findings


def expected_failure(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# expected_failure:"):
            return line.split(":", 1)[1].strip()
    raise SystemExit(f"negative fixture missing '# expected_failure:' header: {path}")


def self_test() -> int:
    checked = 0
    for example in sorted(EXAMPLES_DIR.glob("*.example.yaml")):
        findings = validate_document(example, repo_path=None)
        if findings:
            print(f"FAIL positive example {example.name}: {findings}", file=sys.stderr)
            return 1
        print(f"example ok: {example.name}")
        checked += 1
    for negative in sorted(NEGATIVE_DIR.glob("*.yaml")):
        reason = expected_failure(negative)
        findings = validate_document(negative, repo_path=None)
        if not findings:
            print(f"FAIL negative fixture passed: {negative.name}", file=sys.stderr)
            return 1
        if not any(reason in finding for finding in findings):
            print(
                f"FAIL negative fixture {negative.name} failed for the wrong reason: "
                f"expected '{reason}', got {findings}",
                file=sys.stderr,
            )
            return 1
        print(f"negative ok ({reason}): {negative.name}")
        checked += 1
    for negative_dir in sorted(p for p in NEGATIVE_DIR.iterdir() if p.is_dir()):
        marker = negative_dir / ONTOLOGY_STARTER_MARKER
        if marker.is_file():
            reason = expected_failure(marker)
            findings = validate_generated_domain(negative_dir)
            if not findings or not any(reason in f for f in findings):
                print(f"FAIL repo negative {negative_dir.name}: expected '{reason}', "
                      f"got {findings}", file=sys.stderr)
                return 1
            print(f"negative ok ({reason}): {negative_dir.name}/")
            checked += 1
            continue
        if (negative_dir / DESCRIPTOR_FILE).is_file():
            # A repo-shaped negative for the rules that only exist ACROSS
            # documents: kind dispatch at a descriptor-declared path, and
            # identity conformance against the repo's own subject template.
            # The expected failure is declared on the document at the declared
            # subject path — the document the fixture is about.
            findings = repo_shaped_findings(negative_dir)
            role_paths, _, _ = resolve_role_paths(negative_dir)
            subject_rel = role_paths.get("customer")
            if subject_rel is None:
                print(f"FAIL repo negative {negative_dir.name}: descriptor declares "
                      "no customer role path", file=sys.stderr)
                return 1
            reason = expected_failure(negative_dir / subject_rel)
            if not findings or not any(reason in f for f in findings):
                print(f"FAIL repo negative {negative_dir.name}: expected '{reason}', "
                      f"got {findings}", file=sys.stderr)
                return 1
            print(f"negative ok ({reason}): {negative_dir.name}/")
            checked += 1
    print(f"self-test ok: {checked} fixture(s)")
    return 0


ONTOLOGY_STARTER_MARKER = "hermes/domain/ontology/STARTER.yaml"


def validate_generated_domain(repo_path: Path) -> list[str]:
    """Generated-domain completeness (add-domain-ontology-layer, task 5.1):
    a repo recording an ontology-aware starter version MUST declare
    `domain_ontology` in its content manifest — the check is keyed on the
    recorded marker, never inferred. Legacy repos without the marker stay on
    the documented convention with no new refusal class."""
    findings: list[str] = []
    marker_path = repo_path / ONTOLOGY_STARTER_MARKER
    if not marker_path.is_file():
        return findings
    try:
        marker = yaml.safe_load(marker_path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        return [f"unparseable ontology starter marker: {exc}"]
    if not marker.get("ontology_aware"):
        return findings
    manifest_path = repo_path / CONTENT_MANIFEST_FILE
    if not manifest_path.is_file():
        return ["ontology-aware starter marker without a content manifest: "
                "the semantic scaffold is incomplete"]
    try:
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return []  # the manifest's own validation reports the parse failure
    content_set = manifest.get("content_set")
    if not isinstance(content_set, dict) or "domain_ontology" not in content_set:
        findings.append(
            "ontology-aware starter marker without a domain_ontology "
            "declaration: the semantic scaffold is incomplete")
    return findings


def resolve_role_paths(repo_path: Path) -> tuple[dict[str, str], bool, list[str]]:
    """Resolve role -> path for a repo: the documented convention, overridden by
    the descriptor's declarations when one is shipped. Returns the mapping, a
    descriptor-present flag, and any descriptor findings (a bad descriptor is
    fatal for the walk, so callers stop on a non-empty list)."""
    descriptor_path = repo_path / DESCRIPTOR_FILE
    role_paths = dict(CONVENTION_PATHS)
    if not descriptor_path.is_file():
        return role_paths, False, []
    findings = validate_document(descriptor_path, repo_path)
    if findings:
        return role_paths, True, findings
    declared = yaml.safe_load(descriptor_path.read_text(encoding="utf-8"))["overlay_paths"]
    role_paths.update(declared)
    return role_paths, True, []


def validate_declared_paths(repo_path: Path, role_paths: dict[str, str],
                            descriptor_present: bool,
                            notices: list[str]) -> tuple[list[str], int]:
    """Dispatch every declared (or conventional) overlay path BY THE KIND of the
    document found there, replacing the pre-add-subject-overlay-contract blanket
    skip of everything that was not a domain overlay. A kind this family does not
    own keeps the skip-with-notice; a family-owned kind sitting at the wrong
    role's path is a finding, not a silent pass.

    Returns (findings, validated_count)."""
    findings: list[str] = []
    validated = 0
    for role, rel_path in sorted(role_paths.items()):
        overlay_path = repo_path / rel_path
        if not overlay_path.is_file():
            if role in CONVENTION_PATHS and not descriptor_present:
                notices.append(f"note: no overlay at convention path for role {role}: {rel_path}")
                continue
            findings.append(f"role {role}: declared overlay missing at {rel_path}")
            continue
        try:
            doc = yaml.safe_load(overlay_path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            findings.append(f"{rel_path}: unparseable YAML: {exc}")
            continue
        kind = doc.get("kind") if isinstance(doc, dict) else None
        if kind not in FAMILY_VALIDATED_KINDS:
            owner = FOREIGN_KIND_VALIDATORS.get(kind)
            if owner:
                notices.append(f"skip role {role}: {rel_path} carries kind {kind} "
                               f"(canonical owner: {owner})")
            else:
                notices.append(f"skip role {role}: {rel_path} carries kind {kind} "
                               "(no canonical validator in this family)")
            continue
        expected = ROLE_KINDS.get(role)
        if expected is not None and kind != expected:
            findings.append(f"{rel_path}: wrong kind at declared path for role {role}: "
                            f"{kind} (the {role} role is governed by {expected})")
            continue
        doc_findings = validate_document(overlay_path, repo_path)
        if doc_findings:
            findings.extend(f"{rel_path}: {finding}" for finding in doc_findings)
            continue
        notices.append(f"overlay ok ({role}): {rel_path}")
        validated += 1
    return findings, validated


def repo_shaped_findings(repo_path: Path) -> list[str]:
    """Every finding a repo-SHAPED fixture raises across its documents: the
    descriptor's own findings, then the kind-dispatched walk of its declared
    paths. Used by the self-test so a repo-shaped negative is checked through
    exactly the code a real domain repo runs."""
    role_paths, descriptor_present, findings = resolve_role_paths(repo_path)
    if findings:
        return findings
    notices: list[str] = []
    path_findings, _ = validate_declared_paths(
        repo_path, role_paths, descriptor_present, notices)
    return path_findings


def validate_repo(repo_path: Path) -> int:
    descriptor_path = repo_path / DESCRIPTOR_FILE
    role_paths, descriptor_present, descriptor_findings = resolve_role_paths(repo_path)
    if descriptor_findings:
        for finding in descriptor_findings:
            print(f"FAIL {descriptor_path}: {finding}", file=sys.stderr)
        return 1
    if descriptor_present:
        print(f"descriptor ok: {DESCRIPTOR_FILE}")
    else:
        print(f"no descriptor at {DESCRIPTOR_FILE}; using documented convention")
    manifest_path = repo_path / CONTENT_MANIFEST_FILE
    if manifest_path.is_file():
        findings = validate_document(manifest_path, repo_path)
        if findings:
            for finding in findings:
                print(f"FAIL {CONTENT_MANIFEST_FILE}: {finding}", file=sys.stderr)
            return 1
        print(f"content manifest ok: {CONTENT_MANIFEST_FILE}")
    else:
        print(f"no content manifest at {CONTENT_MANIFEST_FILE}; consumers use the documented convention")
    completeness = validate_generated_domain(repo_path)
    if completeness:
        for finding in completeness:
            print(f"FAIL generated-domain completeness: {finding}", file=sys.stderr)
        return 1
    if (repo_path / ONTOLOGY_STARTER_MARKER).is_file():
        print("generated-domain completeness ok: domain_ontology declared")
    notices: list[str] = []
    findings, validated = validate_declared_paths(
        repo_path, role_paths, descriptor_present, notices)
    for notice in notices:
        print(notice)
    if findings:
        for finding in findings:
            print(f"FAIL {finding}", file=sys.stderr)
        return 1
    print(f"repo validation ok: {validated} overlay(s) validated")
    return 0


def main() -> int:
    status = self_test()
    if status:
        return status
    if len(sys.argv) > 1:
        repo_path = Path(sys.argv[1]).resolve()
        if not repo_path.is_dir():
            print(f"not a directory: {repo_path}", file=sys.stderr)
            return 2
        return validate_repo(repo_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
