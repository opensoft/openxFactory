#!/usr/bin/env python3
"""Validate the client-content contract family (add-client-layer-tuning-contracts).

The openxFactory-owned canonical validator for the kinds
`client_policy_overrides`, `client_memory_boundaries`,
`client_integration_boundaries`, and `hermes_client_overlay`
(`contracts/client-content/*.schema.yaml`). Run from the pinned openxFactory
checkout, never copied:

    python3 scripts/validate-client-content.py [CLIENT_DOC [BASELINE_DOC]]

Two layers run:

1. Packaged reference examples (`contracts/client-content/examples/`): the
   positive overlay must pass structural + comparability checks against the
   packaged domain baseline; every file under `negative/` must fail for its
   declared `# expected_failure:` reason (self-test, fail-closed).
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
    baseline = yaml.safe_load(
        (EXAMPLES / "domain-baseline.example.yaml").read_text(encoding="utf-8"))
    positive = yaml.safe_load(
        (EXAMPLES / "hermes-client-overlay.example.yaml").read_text(encoding="utf-8"))
    verdict = validate_document(positive, baseline)
    if not verdict["ok"]:
        print(f"FAIL positive example: {verdict}", file=sys.stderr)
        return 1
    print("example ok: hermes-client-overlay.example.yaml")
    checked = 1
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
