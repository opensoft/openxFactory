#!/usr/bin/env python3
"""Validate the client-content contract family (add-client-layer-tuning-contracts).

The openxFactory-owned canonical validator for the kinds
`client_policy_overrides`, `client_memory_boundaries`,
`client_integration_boundaries`, and `hermes_client_overlay`
(`contracts/client-content/*.schema.yaml`). Run from the pinned openxFactory
checkout, never copied:

    python3 scripts/validate-client-content.py [CLIENT_DOC [BASELINE_DOC]]

Two layers run:

1. Packaged reference examples (`contracts/client-content/examples/`): EVERY
   packaged positive (`*.example.yaml` other than the baseline itself) must
   pass structural + comparability checks against the packaged domain
   baseline; every file under `negative/` must fail for its declared
   `# expected_failure:` reason (self-test, fail-closed).
2. Optional real documents: CLIENT_DOC validated structurally and, when
   BASELINE_DOC is supplied, against the stricter-only comparability spec.

The comparability spec (decided 2026-07-22; one implementation, two
enforcement points — the wizard at write time and the seeder at validation):

* allowlists (`may_touch`, `allowed_families`, `allowed_classes`): client ⊆ baseline
* denylists (`never_touch`, `never_standing`, `standing_forbidden`): client ⊇ baseline
* numeric ceilings (`budget_envelopes.*`): client ≤ baseline
* clearance requirements / conjunctive envelopes: add-only (every baseline
  conjunct present in the client's set)
* ordered enums (`realization.mode` on the declared `realization_order`):
  client at-or-above the baseline's rung
* anything else with no defined partial order: verdict `review_required`,
  never a silent pass

The OPTIONAL Tenant standing-policy block (`client.policies` +
`client.policy_namespace`, declared 2026-08-22 by
declare-client-standing-policy-contract, closing openxFactory#254) is checked
by `_validate_client_policies` — address self-consistency and uniqueness, the
declared-but-empty refusal, the conditional namespace requirement, and a
prohibited-block / credential scan over that subtree. It is orthogonal to the
comparability spec above in both directions: a POSITION is not a deviation,
so it declares no relation and is never compared to the baseline.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTRACT_DIR = REPO_ROOT / "contracts" / "client-content"
EXAMPLES = CONTRACT_DIR / "examples"

ALLOWLIST_KEYS = {"may_touch", "allowed_families", "allowed_classes"}
DENYLIST_KEYS = {"never_touch", "never_standing", "standing_forbidden"}
CEILING_PARENT = "budget_envelopes"
ENVELOPE_KEY = "auto_clear_envelope"
ORDERED = {"realization": ("mode", "realization_order")}
# The example that is the COMPARAND, not a positive: every other
# `*.example.yaml` under examples/ is a positive validated AGAINST it.
BASELINE_EXAMPLE = "domain-baseline.example.yaml"

# --- standing-policy constants (declare-client-standing-policy-contract) ------
#
# PORTED, NOT IMPORTED. These three constants are byte-equal in meaning to
# `PROHIBITED_SUBJECT_BLOCKS` / `CREDENTIAL_VALUE_KEYS` / `RAW_SECRET_MARKERS`
# in `scripts/validate-hermes-domain-overlay.py`. They are duplicated on
# purpose: the canonical validators in this repository are STANDALONE
# entrypoints (no validator imports another; the only cross-module imports in
# `scripts/` are into the shared `scripts/hermes_runtime_validation` package),
# and importing one canonical script into another would make a change to the
# subject family silently re-decide a tenant verdict. Any edit here or there is
# a change to BOTH contracts and must be made in both places on purpose.
#
# NAMING, deliberately: the subject validator calls its list
# PROHIBITED_SUBJECT_BLOCKS, which names the wrong document — the blocks listed
# are the DOMAIN layer's enforceable slice, and the same list now governs two
# seats below it (subject and tenant). hermes-install's mirror of this rule
# already renamed it `_PROHIBITED_DOMAIN_BLOCKS`
# (src/hermes_install/domain/overlay_content.py, add-client-overlay-standing-policy);
# this file adopts that name. The leading underscore is dropped for this file's
# own convention (module constants here carry no sigil: ALLOWLIST_KEYS,
# DENYLIST_KEYS, CEILING_PARENT). Renaming the subject validator's copy is NOT
# done here: that constant is part of a released contract's canonical
# implementation and belongs to its own change.
PROHIBITED_DOMAIN_BLOCKS = {
    "authority_boundaries", "approval_scope_kinds", "required_approval_fields",
}
# Credential-shaped keys whose VALUE would be key material rather than policy.
# A `*_ref` / `*_binding` key is deliberately absent: reference-delivered
# credentials are the governed form (`credential_binding.form: reference_only`)
# and must stay expressible.
CREDENTIAL_VALUE_KEYS = {
    "secret", "secrets", "token", "password", "passphrase", "api_key", "apikey",
    "private_key", "client_secret", "credential", "credentials",
}
# Explicit issuer markers only. No entropy or base64-shape heuristic: a false
# refusal on a long opaque identifier would be a new refusal class no contract
# declared.
RAW_SECRET_MARKERS = ("-----BEGIN", "ghp_", "github_pat_", "gho_", "ghs_", "AKIA")


def _fail(findings: list[str], msg: str) -> None:
    findings.append(msg)


# --- structural checks --------------------------------------------------------


def validate_structure(doc: Any) -> list[str]:
    findings: list[str] = []
    if not isinstance(doc, dict):
        return ["document is not a mapping"]
    kind = doc.get("kind")
    if kind == "hermes_client_overlay":
        client = doc.get("client")
        if not isinstance(client, dict):
            return ["missing required block: client"]
        for req in ("ref", "display_name"):
            if not client.get(req):
                _fail(findings, f"missing or empty client.{req}")
        po = client.get("policy_overrides")
        if not isinstance(po, dict):
            _fail(findings, "missing required block: policy_overrides")
        else:
            findings.extend(validate_structure(po))
        # The OPTIONAL standing-policy block. Reached only when the document
        # actually DECLARES `client.policies`, so an overlay that carries none
        # takes exactly the verdict it took before the block existed
        # (declare-client-standing-policy-contract). `in` rather than a
        # truthiness test: a declared-but-empty block is a refusal, not an
        # absence.
        if "policies" in client:
            _validate_client_policies(client, findings)
    elif kind == "client_policy_overrides":
        if doc.get("relation_to_domain") != "stricter_only":
            _fail(findings, "relation_to_domain must be stricter_only")
        if not isinstance(doc.get("policy"), dict):
            _fail(findings, "missing required block: policy")
        else:
            envelope = doc["policy"].get(ENVELOPE_KEY)
            if envelope is not None and not (envelope.get("conjunctive") or []):
                _fail(findings, "auto_clear_envelope.conjunctive must be non-empty")
    elif kind == "client_memory_boundaries":
        buckets = doc.get("buckets") or {}
        for b in ("client_private_memory", "customer_relationship_memory",
                  "domain_learning_candidates", "current_state_evidence"):
            if b not in buckets:
                _fail(findings, f"missing bucket: {b}")
        if doc.get("invariant") != "tenant_isolated":
            _fail(findings, "invariant must be tenant_isolated")
    elif kind == "client_integration_boundaries":
        if not doc.get("allowed_classes"):
            _fail(findings, "missing or empty allowed_classes")
        if (doc.get("credential_binding") or {}).get("form") != "reference_only":
            _fail(findings, "credential_binding.form must be reference_only")
    else:
        _fail(findings, f"unknown kind: {kind}")
    return findings


# --- standing policy (declare-client-standing-policy-contract) -----------------


def _walk_entries(node: Any, path: str):
    """Yield (dotted_path, key, value) for every mapping entry beneath `node`,
    so a prohibited block cannot hide one level deeper than the check."""
    if isinstance(node, dict):
        for key, value in node.items():
            here = f"{path}.{key}" if path else str(key)
            yield here, key, value
            yield from _walk_entries(value, here)
    elif isinstance(node, list):
        for index, item in enumerate(node):
            yield from _walk_entries(item, f"{path}[{index}]")


def _prohibited_policy_content(node: Any, findings: list[str], path: str) -> None:
    """A seat below the Domain ADDS constraints and never grants, widens, or
    waives, and it carries policy rather than key material.

    SCOPED TO THE `client.policies` SUBTREE, deliberately narrower than the
    subject path's whole-document walk in
    `scripts/validate-hermes-domain-overlay.py::_prohibited_subject_content`,
    and matching hermes-install's `_prohibited_policy_content(..., seat="tenant",
    path="client.policies")`. Two reasons, both load-bearing:

    1. **This change is ADDITIVE.** `hermes_client_overlay` is a released
       contract (contract-v1.17) that has never prohibited these blocks
       anywhere. A whole-document walk would change the verdict of overlays
       that do not use the new block at all — a breaking change wearing an
       additive change's clothes.
    2. **Parity direction.** hermes-install's runtime scan is subtree-scoped.
       A wider canonical scan would mean canon refuses what the runtime
       accepts, inverting the one-directional divergence
       (`hermes-install stricter than canon, never the reverse`) that
       add-client-overlay-standing-policy's ruling was granted on.

    The asymmetry with the subject seat is therefore preserved on purpose: the
    subject kind was NEW when its walk was written, so a whole-document rule
    cost no existing document its verdict.
    """
    for where, key, value in _walk_entries(node, path):
        if key in PROHIBITED_DOMAIN_BLOCKS:
            _fail(findings,
                  f"prohibited block for a tenant overlay: {where} — a tenant "
                  f"adds constraints and never grants, widens, or waives "
                  f"({key} is the Domain layer's enforceable slice)")
        if key in CREDENTIAL_VALUE_KEYS and isinstance(value, str) and value.strip():
            _fail(findings,
                  f"prohibited credential value at {where}: a tenant overlay "
                  "carries policy, never key material")
        if isinstance(value, str) and any(m in value for m in RAW_SECRET_MARKERS):
            _fail(findings,
                  f"prohibited credential value at {where}: the value carries a "
                  "raw-secret marker")


def _validate_client_policies(client: dict[str, Any], findings: list[str]) -> None:
    """The OPTIONAL Tenant standing-policy block, validated like a Subject's.

    A tenant layer may carry FREESTANDING company-wide policy, not only
    deviations from the domain baseline. Six rules, mirroring
    `validate-hermes-domain-overlay.py::validate_subject_overlay` one layer up
    and hermes-install's `_validate_client_policies` in-process:

    1. `client.policies` is a NON-EMPTY mapping. A declared-but-empty block is
       REFUSED rather than treated as absent (ratified 2026-08-22, ruling (c)):
       an empty map would materialize an empty `policy_position` row, and
       readiness clears `materialized_policy:<layer>` on ROW PRESENCE, so the
       block would report a standing-policy veto seat ready with nothing behind
       it. A bare `policies:` parses to `None` and IS a declaration of
       emptiness, so it takes the same finding; a block of some OTHER type is a
       different mistake and says so, because "policies" reads plural and
       telling an author who wrote a list that their block is empty sends them
       to delete it rather than reshape it.
    2. Every entry is a mapping.
    3. Every entry declares a non-empty `policy_id` EQUAL TO ITS KEY — the key
       IS the address.
    4. Every entry restates a non-empty `policy_namespace` equal to
       `client.policy_namespace`, so a materialized row is address-resolvable
       without joining to a sibling row.
    5. `client.policy_namespace` is present and non-empty — required WHEN AND
       ONLY WHEN `policies` is present. The converse is deliberately not an
       error: a namespace declared with no policies is inert, and refusing it
       would be a new refusal class this contract never declared.
    6. No two entries claim one `<policy_namespace>/<policy_id>` address.

    Plus the prohibited-block and credential scan over the `client.policies`
    subtree only (see `_prohibited_policy_content`).

    NO `relation_to_*` FIELD is declared for this block (ratified 2026-08-22,
    ruling (d)): a tenant's standing policy is a POSITION, not a deviation, so
    there is no baseline for it to declare a relation to. That is the one place
    this block deliberately does NOT mirror `subject.relation_to_baseline`.
    """
    policies = client.get("policies")
    _prohibited_policy_content(policies, findings, "client.policies")
    if policies is not None and not isinstance(policies, dict):
        _fail(findings,
              "client.policies must be a mapping of policy id to policy "
              "document, one entry per named standing policy")
        return
    if not policies:
        _fail(findings,
              "empty client.policies: a tenant overlay that DECLARES standing "
              "policy declares at least one named policy (omit the block "
              "entirely to carry none)")
        return
    namespace = client.get("policy_namespace")
    if not isinstance(namespace, str) or not namespace.strip():
        _fail(findings,
              "missing or empty client.policy_namespace: a tenant overlay "
              "carrying standing policy DECLARES the namespace its policies "
              "are addressed in")
        namespace = None
    seen_addresses: dict[str, str] = {}
    for key, policy in policies.items():
        if not isinstance(policy, dict):
            _fail(findings, f"client.policies.{key} must be a mapping")
            continue
        policy_id = policy.get("policy_id")
        if not isinstance(policy_id, str) or not policy_id.strip():
            _fail(findings, f"missing or empty policy_id for client.policies.{key}")
        elif policy_id != key:
            _fail(findings,
                  f"policies key {key} does not match its declared policy_id "
                  f"{policy_id}: the key IS the address")
        policy_namespace = policy.get("policy_namespace")
        if not isinstance(policy_namespace, str) or not policy_namespace.strip():
            _fail(findings, f"missing or empty policy_namespace for client.policies.{key}")
        elif namespace is not None and policy_namespace != namespace:
            _fail(findings,
                  f"policy namespace mismatch for client.policies.{key}: the policy "
                  f"declares {policy_namespace}, the tenant declares {namespace}")
        if isinstance(policy_id, str) and isinstance(policy_namespace, str):
            address = f"{policy_namespace}/{policy_id}"
            if address in seen_addresses:
                _fail(findings,
                      f"duplicate policy address {address}: declared by "
                      f"client.policies.{seen_addresses[address]} and "
                      f"client.policies.{key}")
            seen_addresses.setdefault(address, str(key))


# --- comparability spec -------------------------------------------------------


def compare_policies(client_policy: dict[str, Any],
                     baseline_policy: dict[str, Any]) -> tuple[list[str], list[str]]:
    """(violations, review_required) for a client policy vs its baseline."""
    violations: list[str] = []
    review: list[str] = []

    def walk(cli: Any, base: Any, path: str) -> None:
        if not isinstance(cli, dict) or not isinstance(base, dict):
            return
        for key, base_val in base.items():
            cli_val = cli.get(key)
            here = f"{path}.{key}" if path else key
            if key in ALLOWLIST_KEYS:
                extra = [x for x in (cli_val or []) if x not in (base_val or [])]
                if extra:
                    violations.append(f"allowlist exceeded at {here}: {extra}")
            elif key in DENYLIST_KEYS:
                missing = [x for x in (base_val or []) if x not in (cli_val or [])]
                if missing:
                    violations.append(f"denylist shrunk at {here}: missing {missing}")
            elif key == CEILING_PARENT and isinstance(base_val, dict):
                for name, ceiling in base_val.items():
                    val = (cli_val or {}).get(name)
                    if isinstance(ceiling, (int, float)) and isinstance(val, (int, float)):
                        if val > ceiling:
                            violations.append(
                                f"ceiling raised at {here}.{name}: {val} > {ceiling}")
                    elif val is not None:
                        review.append(f"{here}.{name}")
            elif key == ENVELOPE_KEY and isinstance(base_val, dict):
                base_conj = base_val.get("conjunctive") or []
                cli_conj = (cli_val or {}).get("conjunctive") or []
                removed = [c for c in base_conj if c not in cli_conj]
                if removed:
                    violations.append(
                        f"envelope conjunct removed at {here}: {removed}")
            elif key in ORDERED and isinstance(base_val, dict):
                field, order_key = ORDERED[key]
                order = baseline_policy.get(order_key) or []
                b, c = base_val.get(field), (cli_val or {}).get(field)
                if order and b in order and c in order:
                    if order.index(c) < order.index(b):
                        violations.append(
                            f"ordered field below baseline at {here}.{field}: "
                            f"{c!r} < {b!r}")
                elif c is not None and c != b:
                    review.append(f"{here}.{field}")
            elif isinstance(base_val, dict):
                walk(cli_val or {}, base_val, here)
            elif cli_val is not None and cli_val != base_val:
                review.append(here)  # no partial order defined — never a silent pass

    walk(client_policy, baseline_policy, "")
    return violations, review


def _policy_of(doc: dict[str, Any]) -> dict[str, Any]:
    if doc.get("kind") == "hermes_client_overlay":
        return ((doc.get("client") or {}).get("policy_overrides") or {}).get("policy") or {}
    return doc.get("policy") or {}


def validate_document(doc: Any, baseline: dict[str, Any] | None) -> dict[str, Any]:
    findings = validate_structure(doc)
    violations: list[str] = []
    review: list[str] = []
    if not findings and baseline is not None:
        violations, review = compare_policies(_policy_of(doc), baseline.get("policy") or {})
    ok = not findings and not violations
    return {"ok": ok, "structural": findings, "violations": violations,
            "review_required": review}


# --- self-test + CLI ----------------------------------------------------------


def expected_failure(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# expected_failure:"):
            return line.split(":", 1)[1].strip()
    raise SystemExit(f"negative fixture missing '# expected_failure:' header: {path}")


def self_test() -> int:
    # `domain-baseline.example.yaml` is the COMPARAND, not a positive: it is the
    # `client_policy_baseline` every positive is checked against, and it is not
    # itself a client-content kind. Every OTHER packaged `*.example.yaml` is a
    # positive and is swept — the file list is discovered, not hardcoded, so a
    # new positive cannot be added and silently never run
    # (declare-client-standing-policy-contract).
    baseline = yaml.safe_load(
        (EXAMPLES / BASELINE_EXAMPLE).read_text(encoding="utf-8"))
    positives = [path for path in sorted(EXAMPLES.glob("*.example.yaml"))
                 if path.name != BASELINE_EXAMPLE]
    if not positives:
        print(f"FAIL: no positive examples packaged beside {BASELINE_EXAMPLE}",
              file=sys.stderr)
        return 1
    checked = 0
    for path in positives:
        positive = yaml.safe_load(path.read_text(encoding="utf-8"))
        verdict = validate_document(positive, baseline)
        if not verdict["ok"]:
            print(f"FAIL positive example {path.name}: {verdict}", file=sys.stderr)
            return 1
        print(f"example ok: {path.name}")
        checked += 1
    for negative in sorted((EXAMPLES / "negative").glob("*.yaml")):
        reason = expected_failure(negative)
        doc = yaml.safe_load(negative.read_text(encoding="utf-8"))
        verdict = validate_document(doc, baseline)
        blob = " ".join(verdict["structural"] + verdict["violations"])
        if verdict["ok"]:
            print(f"FAIL negative passed: {negative.name}", file=sys.stderr)
            return 1
        if reason not in blob:
            print(f"FAIL negative {negative.name} failed for the wrong reason: "
                  f"expected {reason!r} in {blob!r}", file=sys.stderr)
            return 1
        print(f"negative ok ({reason}): {negative.name}")
        checked += 1
    print(f"self-test ok: {checked} fixture(s)")
    return 0


def main() -> int:
    status = self_test()
    if status:
        return status
    args = sys.argv[1:]
    if args:
        doc = yaml.safe_load(Path(args[0]).read_text(encoding="utf-8"))
        baseline = None
        if len(args) > 1:
            baseline = yaml.safe_load(Path(args[1]).read_text(encoding="utf-8"))
        verdict = validate_document(doc, baseline)
        print(json.dumps(verdict, indent=2, sort_keys=True))
        return 0 if verdict["ok"] else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
