#!/usr/bin/env python3
"""Canonical DomainxFactory conformance validator.

Owned by openxFactory (contracts deliverable). Domain repos run this file
directly from their pinned openxFactory checkout; they must not copy it.

Usage:
    python3 validate-domain-factory.py /path/to/DomainxFactory [--strict]

Checks (errors fail the run; warnings fail only with --strict):
  1.  stack.yaml exists, parses, has canonical top-level shape.
  2.  xfactory contract pin is well-formed (commit SHA or tag).
  3.  hermes.layers declares exactly one static customer, client, and domain
      template (extensions allowed with authority_scope); the one Customer
      template may realize zero or more runtime customer_subject instances.
      Overlay dirs exist and contain at least one YAML file. A stack that
      declares no hermes.layers list is an error: the legacy flat-key
      fallback read was removed at contract-v3.0.
  4.  omnigent.domain_overlay dir exists.
  5.  tenancy declares kinds + isolation; isolation values are from the
      recognized scope vocabulary.
  6.  profiles/*.yaml: every profile declares an identifier (nested
      `profile.id`, or a flat `profile_id` for the domain-specific kinds
      registered in PROFILE_ID_KEY_KINDS); every profile's tenant_kind/
      client_kind is declared in stack tenancy; every declared kind has a
      profile (warning).
  7.  tenants/examples/*.yaml: profile references resolve.
  8.  workflows/*.yaml: every gate has id + owner_layer + requires;
      owner_layer resolves to a declared layer, omnigent, or xfactory.
  9.  Cross-ID consistency (when files exist): tool-routing workflow and
      worker-capability references resolve; workflow credential
      requirements resolve; near-duplicate IDs across the credential
      requirement / worker capability vocabularies (same token modulo
      case/separators) are flagged.
  10. memory_gateway declares providers, bindings, conformance tier, and
      break-glass workflow requirements; Hermes overlay files are checked for
      direct memory provider endpoint or connection refs.
  11. Secret scan across tracked text files.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR: PyYAML is required (pip install pyyaml)")
    sys.exit(2)

COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
TAG_RE = re.compile(r"^v?\d+\.\d+(\.\d+)?([-.][0-9A-Za-z.]+)?$")
DOMAIN_ID_RE = re.compile(r"^[a-z][a-z0-9_]*$")

CANONICAL_ROLES = ("customer", "client", "domain")
# `per_customer_subject` is a FROZEN legacy machine key (contracts/policies/
# layer-vocabulary.yaml legacy_mapping: customer -> subject) and stays
# accepted unrenamed; `per_subject` is the ratified Subject/Tenant/Domain
# spelling and is additive (openxFactory #918).
ISOLATION_SCOPES = {
    "per_tenant", "per_client", "per_customer", "per_customer_subject",
    "per_subject", "per_patient",
    "per_campaign", "per_project", "per_ledger", "shared_with_review",
}
SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (RSA|EC|OPENSSH|PGP) PRIVATE KEY-----"),
    re.compile(r"(?i)\b(password|passwd|secret|token)\s*[:=]\s*['\"]?[A-Za-z0-9+/]{12,}"),
    re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
]
TEXT_SUFFIXES = {".yaml", ".yml", ".md", ".json", ".py", ".sh", ".sql", ".txt"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv",
             # The CI convention checks the openxFactory stack pin out
             # INSIDE the domain workspace; pinned upstream content --
             # including redaction-test fixtures that deliberately
             # carry secret-shaped strings -- is not the domain's own
             # surface and must not fail its validation.
             ".openxfactory-pin"}
# Profile document kinds that key their identifier on a flat top-level
# `profile_id` field instead of nesting `id` under `profile:`. Domain-specific
# profile kinds register here rather than widen the default `profile.id`
# rule for every kind (openxFactory #919; OpsxFactory's cloudpc_worker_profile
# is the first member).
PROFILE_ID_KEY_KINDS = {"cloudpc_worker_profile"}
MEMORY_GATEWAY_TIERS = {"M0", "M1", "M2", "M3", "M4"}
MEMORY_GATEWAY_OPERATIONS = {
    "xfactory.memory.query",
    "xfactory.memory.write",
    "xfactory.memory.context_packet",
    "xfactory.memory.propose_promotion",
    "xfactory.memory.revoke_or_tombstone",
    "xfactory.memory.erase_content",
    "xfactory.memory.audit",
    "xfactory.memory.provider_health",
}
DIRECT_MEMORY_BINDING_RE = re.compile(
    r"(?im)^\s*(memory_provider_endpoint|provider_endpoint|provider_url|"
    r"connection_ref|provider_connection|gbrain_connection|honcho_connection|"
    r"agentmemory_connection|expert_db_connection)\s*:"
)


def snake(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.strip().lower()).strip("_")


def norm_id(token: str) -> str:
    return re.sub(r"[-_]", "", token.strip().lower())


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


def load_yaml(path: Path, rpt: Report):
    try:
        with path.open("r", encoding="utf-8") as fh:
            return yaml.safe_load(fh)
    except Exception as exc:  # noqa: BLE001
        rpt.error(f"{path}: failed to parse YAML: {exc}")
        return None


def check_pin(stack: dict, rpt: Report) -> None:
    xf = stack.get("xfactory")
    if not isinstance(xf, dict):
        rpt.error("stack.yaml: missing xfactory pin block")
        return
    for key in ("contract_repo", "contract_name", "contract_ref_type",
                "contract_ref", "contract_schema_version",
                "contract_declared_at", "contract_source"):
        if key not in xf:
            rpt.error(f"stack.yaml: xfactory.{key} missing")
    ref_type, ref = xf.get("contract_ref_type"), str(xf.get("contract_ref", ""))
    if ref_type == "commit" and not COMMIT_RE.match(ref):
        rpt.error(f"stack.yaml: contract_ref {ref!r} is not a 40-hex commit SHA")
    elif ref_type == "tag" and not TAG_RE.match(ref):
        rpt.error(f"stack.yaml: contract_ref {ref!r} is not a valid tag")
    elif ref_type not in ("commit", "tag"):
        rpt.error(f"stack.yaml: contract_ref_type must be commit|tag, got {ref_type!r}")


def resolve_layers(root: Path, stack: dict, rpt: Report) -> dict[str, dict]:
    """Return the unique static template for each canonical role.

    Runtime Customer Hermes cardinality is governed by the neutral runtime
    topology contract. This static declaration remains singular so duplicate
    role templates cannot create an alternate authority path.
    """
    hermes = stack.get("hermes")
    if not isinstance(hermes, dict):
        rpt.error("stack.yaml: missing hermes block")
        return {}
    layers: dict[str, dict] = {}
    declared = hermes.get("layers")
    if isinstance(declared, list):
        for i, layer in enumerate(declared):
            if not isinstance(layer, dict):
                rpt.error(f"stack.yaml: hermes.layers[{i}] is not a mapping")
                continue
            role = layer.get("role")
            if role not in CANONICAL_ROLES + ("extension",):
                rpt.error(f"stack.yaml: hermes.layers[{i}].role {role!r} invalid")
                continue
            if role == "extension":
                if not layer.get("authority_scope"):
                    rpt.error(f"stack.yaml: extension layer {layer.get('display_name')!r} "
                              "requires authority_scope")
                continue
            if role in layers:
                rpt.error(f"stack.yaml: duplicate hermes layer role {role!r}")
                continue
            if not layer.get("display_name") or not layer.get("overlay"):
                rpt.error(f"stack.yaml: hermes.layers[{i}] needs display_name and overlay")
                continue
            layers[role] = layer
        for role in CANONICAL_ROLES:
            if role not in layers:
                rpt.error(f"stack.yaml: hermes.layers missing required role {role!r}")
    else:
        # The legacy flat-key FALLBACK READ was removed at contract-v3.0
        # (retire-hermes-flat-keys-and-openworkflow-tokens). It is REPLACED by
        # this error rather than merely deleted: the missing-required-role
        # errors above sit inside the `layers`-declared branch, so a bare
        # deletion would let a `layers`-less stack fall through to an EMPTY
        # layer map and produce no finding at all — a silent widening at a
        # major, the exact opposite of the retirement.
        rpt.error("stack.yaml: hermes.layers is missing or is not a list; declare it "
                  "with the canonical roles customer/client/domain (the legacy flat-key "
                  "fallback read was removed at contract-v3.0)")
    for role, layer in layers.items():
        overlay = layer.get("overlay")
        if not overlay:
            continue
        odir = root / overlay
        if not odir.is_dir():
            rpt.error(f"hermes {role} overlay dir missing: {overlay}")
        elif not any(p.suffix in (".yaml", ".yml") for p in odir.rglob("*") if p.is_file()):
            rpt.error(f"hermes {role} overlay dir has no YAML content: {overlay}")
    return layers


def check_tenancy(stack: dict, rpt: Report) -> list[str]:
    tenancy = stack.get("tenancy")
    if not isinstance(tenancy, dict):
        rpt.error("stack.yaml: missing tenancy block")
        return []
    kinds = list(tenancy.get("tenant_kinds") or []) + list(tenancy.get("client_kinds") or [])
    if not kinds:
        rpt.error("stack.yaml: tenancy must declare tenant_kinds or client_kinds")
    isolation = tenancy.get("isolation")
    if not isinstance(isolation, dict) or not isolation:
        rpt.error("stack.yaml: tenancy.isolation missing or empty")
    else:
        for key, val in isolation.items():
            if val not in ISOLATION_SCOPES:
                rpt.error(f"stack.yaml: tenancy.isolation.{key}={val!r} is not a "
                          f"recognized isolation scope {sorted(ISOLATION_SCOPES)}")
    return kinds


def check_profiles(root: Path, kinds: list[str], rpt: Report) -> set[str]:
    profile_ids: set[str] = set()
    covered_kinds: set[str] = set()
    pdir = root / "profiles"
    if not pdir.is_dir():
        rpt.warn("profiles/ directory missing")
        return profile_ids
    for pf in sorted(pdir.glob("*.yaml")):
        data = load_yaml(pf, rpt)
        if not isinstance(data, dict):
            continue
        prof = data.get("profile", data)
        kind_value = data.get("kind")
        if isinstance(kind_value, str) and kind_value in PROFILE_ID_KEY_KINDS:
            # The identifier may sit at the document top level (flat, beside
            # `kind:`) or nested under `profile:` alongside other fields
            # (mixed shape) -- check both rather than assuming one.
            pid = data.get("profile_id") or prof.get("profile_id")
            if not pid:
                rpt.error(f"{pf.name}: profile_id missing")
                continue
        else:
            pid = prof.get("id")
            if not pid:
                rpt.error(f"{pf.name}: profile.id missing")
                continue
        profile_ids.add(pid)
        kind = prof.get("tenant_kind") or prof.get("client_kind")
        if kind:
            covered_kinds.add(kind)
            if kinds and kind not in kinds:
                rpt.error(f"{pf.name}: kind {kind!r} not declared in stack tenancy")
    for kind in kinds:
        if kind not in covered_kinds:
            rpt.warn(f"tenancy kind {kind!r} has no deployment profile")
    return profile_ids


def check_tenants(root: Path, profile_ids: set[str], rpt: Report) -> None:
    tdir = root / "tenants" / "examples"
    if not tdir.is_dir():
        rpt.warn("tenants/examples/ missing (no instantiation examples)")
        return
    for tf in sorted(tdir.glob("*.yaml")):
        data = load_yaml(tf, rpt)
        if not isinstance(data, dict):
            continue
        tenant = data.get("tenant", data)
        ref = tenant.get("profile")
        if ref and profile_ids and ref not in profile_ids:
            rpt.error(f"tenants/examples/{tf.name}: profile {ref!r} does not resolve")


def check_workflows(root: Path, stack: dict, layers: dict, rpt: Report) -> set[str]:
    workflow_ids: set[str] = set()
    wdir = root / "workflows"
    if not wdir.is_dir():
        rpt.warn("workflows/ directory missing")
        return workflow_ids
    domain_id = (stack.get("domain") or {}).get("id", "")
    allowed = set(CANONICAL_ROLES) | {"xfactory", "omnigent", f"{domain_id}_omnigent"}
    for layer in layers.values():
        if layer.get("display_name"):
            allowed.add(snake(layer["display_name"]))
    yaml_files = sorted(wdir.glob("*.yaml"))
    if not yaml_files:
        rpt.warn("workflows/ contains no workflow YAML (prose-only workflow catalog)")
    for wf in yaml_files:
        data = load_yaml(wf, rpt)
        if not isinstance(data, dict):
            continue
        flow = data.get("workflow", data)
        wid = flow.get("id")
        if wid:
            workflow_ids.add(wid)
        gates = flow.get("gates") or []
        if not gates:
            rpt.warn(f"workflows/{wf.name}: no gates declared")
        for gate in gates:
            gid = gate.get("id")
            owner = gate.get("owner_layer")
            if not gid or not owner:
                rpt.error(f"workflows/{wf.name}: gate missing id/owner_layer")
                continue
            if not gate.get("requires"):
                rpt.error(f"workflows/{wf.name}: gate {gid} has empty requires")
            token = snake(str(owner))
            if token not in allowed:
                rpt.error(f"workflows/{wf.name}: gate {gid} owner_layer {owner!r} does "
                          f"not resolve to a declared layer (allowed: {sorted(allowed)})")
    return workflow_ids


def check_cross_ids(root: Path, workflow_ids: set[str], rpt: Report) -> None:
    req_ids: set[str] = set()
    cap_ids: set[str] = set()
    req_file = root / "credentials" / "requirements.yaml"
    if req_file.is_file():
        data = load_yaml(req_file, rpt) or {}
        for item in data.get("requirements", []) or []:
            rid = item.get("id") if isinstance(item, dict) else item
            if rid:
                req_ids.add(rid)
    cap_file = root / "omnigent" / "worker-capabilities.yaml"
    if cap_file.is_file():
        data = load_yaml(cap_file, rpt) or {}
        for item in data.get("capabilities", data.get("worker_capabilities", [])) or []:
            cid = item.get("id") if isinstance(item, dict) else item
            if cid:
                cap_ids.add(cid)
    routing_file = root / "omnigent" / "tool-routing.yaml"
    if routing_file.is_file():
        data = load_yaml(routing_file, rpt) or {}
        for route in data.get("routes", data.get("routing", [])) or []:
            if not isinstance(route, dict):
                continue
            wf_ref = route.get("workflow")
            if wf_ref and workflow_ids and wf_ref not in workflow_ids:
                rpt.error(f"tool-routing: workflow {wf_ref!r} does not resolve")
            cap_ref = route.get("required_worker_capability")
            if cap_ref and cap_ids and cap_ref not in cap_ids:
                rpt.error(f"tool-routing: capability {cap_ref!r} does not resolve")
    # near-duplicate vocabulary check
    for rid in req_ids:
        for cid in cap_ids:
            if rid != cid and norm_id(rid) == norm_id(cid):
                rpt.error(f"identifier drift: credential requirement {rid!r} and worker "
                          f"capability {cid!r} are the same token with different "
                          "separators — unify the vocabulary")
    # partial-overlap warning (e.g. github_org_admin vs github-admin)
    for rid in req_ids:
        for cid in cap_ids:
            nr, nc = norm_id(rid), norm_id(cid)
            if nr != nc and (nr in nc or nc in nr):
                rpt.warn(f"identifier near-miss: requirement {rid!r} vs capability "
                         f"{cid!r} — confirm these are intentionally distinct")


def check_memory_gateway(stack: dict, rpt: Report) -> None:
    gateway = stack.get("memory_gateway")
    if gateway is None:
        rpt.warn("stack.yaml: memory_gateway block missing; governed memory providers "
                 "will be scaffold-only until declared")
        return
    if not isinstance(gateway, dict):
        rpt.error("stack.yaml: memory_gateway must be a mapping")
        return
    tier = gateway.get("conformance_tier")
    if tier not in MEMORY_GATEWAY_TIERS:
        rpt.error(f"stack.yaml: memory_gateway.conformance_tier {tier!r} must be one "
                  f"of {sorted(MEMORY_GATEWAY_TIERS)}")
    contract = str(gateway.get("canonical_contract", ""))
    if "memory-gateway" not in contract:
        rpt.error("stack.yaml: memory_gateway.canonical_contract must reference "
                  "openxFactory/contracts/memory-gateway")
    placeholder = gateway.get("placeholder") is True

    providers = gateway.get("providers")
    if not isinstance(providers, list) or not providers:
        msg = "stack.yaml: memory_gateway.providers must be a non-empty list"
        (rpt.warn if placeholder else rpt.error)(msg)
        providers = []
    provider_ids: set[str] = set()
    expert_provider_ids: set[str] = set()
    for index, provider in enumerate(providers):
        if not isinstance(provider, dict):
            rpt.error(f"stack.yaml: memory_gateway.providers[{index}] must be a mapping")
            continue
        pid = provider.get("provider_id")
        role = provider.get("provider_role")
        profile_ref = provider.get("profile_ref")
        if not pid or not role or not profile_ref:
            rpt.error(f"stack.yaml: memory_gateway.providers[{index}] needs "
                      "provider_id, provider_role, and profile_ref")
            continue
        provider_ids.add(str(pid))
        if str(role).startswith("expert_") or role in {
            "root_truth_db", "vector_index", "graph_store", "source_workspace",
            "playbook_store",
        }:
            expert_provider_ids.add(str(pid))
            if not provider.get("allowed_knowledge_scopes"):
                rpt.error(f"stack.yaml: expert provider {pid!r} missing "
                          "allowed_knowledge_scopes")
            if not provider.get("source_authority_minimum"):
                rpt.error(f"stack.yaml: expert provider {pid!r} missing "
                          "source_authority_minimum")

    bindings = gateway.get("bindings")
    if not isinstance(bindings, list) or not bindings:
        msg = "stack.yaml: memory_gateway.bindings must be a non-empty list"
        (rpt.warn if placeholder else rpt.error)(msg)
        bindings = []
    bound_provider_ids: set[str] = set()
    for index, binding in enumerate(bindings):
        if not isinstance(binding, dict):
            rpt.error(f"stack.yaml: memory_gateway.bindings[{index}] must be a mapping")
            continue
        bid = binding.get("binding_id")
        pid = binding.get("provider_id")
        if not bid or not pid:
            rpt.error(f"stack.yaml: memory_gateway.bindings[{index}] needs "
                      "binding_id and provider_id")
            continue
        if pid not in provider_ids:
            rpt.error(f"stack.yaml: memory_gateway binding {bid!r} references unknown "
                      f"provider_id {pid!r}")
        bound_provider_ids.add(str(pid))
        for key in ("layer_scope", "allowed_operations", "client_scope", "subject_scope"):
            if key in binding and not isinstance(binding.get(key), list):
                rpt.error(f"stack.yaml: memory_gateway binding {bid!r}.{key} must be a list")
        for op in binding.get("allowed_operations", []) or []:
            if op not in MEMORY_GATEWAY_OPERATIONS:
                rpt.error(f"stack.yaml: memory_gateway binding {bid!r} has unknown "
                          f"operation {op!r}")
        ttl = binding.get("grant_ttl_seconds")
        if not isinstance(ttl, int) or ttl <= 0:
            rpt.error(f"stack.yaml: memory_gateway binding {bid!r} needs positive "
                      "grant_ttl_seconds")
    for pid in sorted(provider_ids - bound_provider_ids):
        rpt.warn(f"stack.yaml: memory_gateway provider {pid!r} has no binding")

    expert_gateway = gateway.get("omnigent_expert_memory_gateway")
    if expert_provider_ids and not isinstance(expert_gateway, dict):
        rpt.error("stack.yaml: memory_gateway.omnigent_expert_memory_gateway missing "
                  "while expert providers are declared")
    elif isinstance(expert_gateway, dict):
        if not expert_gateway.get("allowed_knowledge_scopes") and not placeholder:
            rpt.error("stack.yaml: omnigent_expert_memory_gateway.allowed_knowledge_scopes "
                      "missing")
        if not expert_gateway.get("source_authority_minimum") and not placeholder:
            rpt.error("stack.yaml: omnigent_expert_memory_gateway.source_authority_minimum "
                      "missing")
        if expert_gateway.get("audit_required") is not True:
            rpt.error("stack.yaml: omnigent_expert_memory_gateway.audit_required must be true")

    for workflow in gateway.get("break_glass_workflows", []) or []:
        if not isinstance(workflow, dict):
            rpt.error("stack.yaml: memory_gateway.break_glass_workflows entries must be mappings")
            continue
        wid = workflow.get("id", "<unknown>")
        for key in (
            "workflow_ref", "allowed_actor_classes", "subject_scope",
            "minimal_packet_profile", "max_ttl_seconds", "notification_targets",
            "retrospective_review_sla",
        ):
            if key not in workflow:
                rpt.error(f"stack.yaml: break-glass workflow {wid!r} missing {key}")
        if not isinstance(workflow.get("max_ttl_seconds"), int) or workflow.get("max_ttl_seconds", 0) <= 0:
            rpt.error(f"stack.yaml: break-glass workflow {wid!r} needs positive max_ttl_seconds")


def check_hermes_direct_provider_bindings(root: Path, layers: dict, rpt: Report) -> None:
    for role, layer in layers.items():
        overlay = layer.get("overlay")
        if not overlay:
            continue
        odir = root / overlay
        if not odir.is_dir():
            continue
        for path in odir.rglob("*"):
            if not path.is_file() or path.suffix not in {".yaml", ".yml"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if DIRECT_MEMORY_BINDING_RE.search(text):
                rpt.error(f"{path.relative_to(root)}: Hermes {role} overlay contains "
                          "direct memory provider endpoint/connection ref; declare it "
                          "under stack.yaml memory_gateway bindings instead")


def scan_secrets(root: Path, rpt: Report) -> None:
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                rpt.error(f"possible secret in {path.relative_to(root)} "
                          f"(pattern {pattern.pattern[:40]}...)")
                break


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("repo", type=Path, help="Path to the DomainxFactory repo root")
    ap.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    ap.add_argument("--no-secret-scan", action="store_true")
    args = ap.parse_args()

    root = args.repo.resolve()
    rpt = Report()
    stack_file = root / "stack.yaml"
    if not stack_file.is_file():
        print(f"ERROR: {stack_file} not found")
        return 1
    stack = load_yaml(stack_file, rpt)
    if not isinstance(stack, dict):
        rpt.error("stack.yaml did not parse to a mapping")
        stack = {}

    if stack.get("kind") != "xfactory_domain_stack":
        rpt.error(f"stack.yaml: kind must be xfactory_domain_stack, got {stack.get('kind')!r}")
    domain = stack.get("domain") or {}
    if not DOMAIN_ID_RE.match(str(domain.get("id", ""))):
        rpt.error(f"stack.yaml: domain.id {domain.get('id')!r} invalid")

    check_pin(stack, rpt)
    layers = resolve_layers(root, stack, rpt)
    kinds = check_tenancy(stack, rpt)
    omni = (stack.get("omnigent") or {}).get("domain_overlay")
    if not omni or not (root / omni).is_dir():
        rpt.error(f"omnigent domain_overlay dir missing: {omni!r}")
    profile_ids = check_profiles(root, kinds, rpt)
    check_tenants(root, profile_ids, rpt)
    workflow_ids = check_workflows(root, stack, layers, rpt)
    check_cross_ids(root, workflow_ids, rpt)
    check_memory_gateway(stack, rpt)
    check_hermes_direct_provider_bindings(root, layers, rpt)
    if not args.no_secret_scan:
        scan_secrets(root, rpt)

    for msg in rpt.errors:
        print(f"ERROR: {msg}")
    for msg in rpt.warnings:
        print(f"WARN:  {msg}")
    failed = bool(rpt.errors) or (args.strict and bool(rpt.warnings))
    print(f"\n{root.name}: {len(rpt.errors)} error(s), {len(rpt.warnings)} warning(s) "
          f"-> {'FAIL' if failed else 'PASS'}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
