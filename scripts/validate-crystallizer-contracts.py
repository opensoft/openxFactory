#!/usr/bin/env python3
"""Canonical validator for the crystallizer record family (add-crystallizer-contracts).

Validates the four record kinds — `crystallization_decision`,
`crystallization_spec`, `crystallization_build`, `crystallization_consent`
— against their schemas (`contracts/schemas/crystallization-*.schema.yaml`)
plus the deterministic policy rules the shapes deliberately do not express
(shape in the schema, policy here; same split as
scripts/validate-pattern-ledger.py). Crystallized-executor bindings and
rung ceilings are overlay content validated by
scripts/validate-omnigent-contracts.py, not here.

Run from the openxFactory checkout:

    python3 scripts/validate-crystallizer-contracts.py [RECORDS_DIR]

Two layers run (mirroring the pattern-ledger validator):

1. Packaged reference examples (`examples/crystallizer/`): every YAML
   document outside `negative/` must pass; every file under `negative/`
   must fail for its INTENDED reason (first-line `# expected_failure:`
   header). The `mvp-packet-capture/` positives continue the MVP fixture
   corpus: the funded L3 decision, the spec mined from the three real
   packet-capture episodes, and the consent grants for the family the
   pattern ledger already nominates.
2. Optional real records under RECORDS_DIR: YAML documents whose `kind`
   is a crystallizer kind validate fully; other kinds are skipped;
   absence is not a failure.

Named policy rules (stable tokens used by negative fixtures):
  candidate-required      a decision must reference an open candidate
  ceiling-exceeded        valuation rows only at or below the ceiling
  funded-rung             the funded rung must be a valued, eligible rung
  outcome-shape           funded/not_yet blocks match the outcome exactly
                          (spend fields on a not_yet outcome are invalid)
  braid-complete          funding needs domain fitness + tenant budget +
                          automation consent — no single layer suffices
  ladder-maturity         an EV (rung 3) decision needs calibration refs
  valuation-discounting   every valuation row carries deflation and
                          survival factors (savings are a melting asset)
  counterexample-floor    a spec with zero counterexamples fails intake
  evidence-citation       every mined element cites at least one episode
  byte-golden             a byte-equality comparator is always rejected
                          (structural-exact is the legitimate exact form)
  effect-class-missing    a spec must declare its effect class
  automation-scope        an automation grant is scoped to one family
                          category; other tiers carry no scope
  schema                  structural nonconformance to the record schema
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = REPO_ROOT / "contracts" / "schemas"
EXAMPLES_DIR = REPO_ROOT / "examples" / "crystallizer"
NEGATIVE_DIR = EXAMPLES_DIR / "negative"

KIND_TO_SCHEMA = {
    "crystallization_decision": "crystallization-decision.schema.yaml",
    "crystallization_spec": "crystallization-spec.schema.yaml",
    "crystallization_build": "crystallization-build.schema.yaml",
    "crystallization_consent": "crystallization-consent.schema.yaml",
}

RUNGS = ["L0", "L1", "L2", "L3", "L4", "L5", "L6"]
EXPECTED_RE = re.compile(r"^#\s*expected_failure:\s*(.+?)\s*$")


def rung_index(value) -> int:
    return RUNGS.index(value) if value in RUNGS else -1


def load_validators() -> dict[str, Draft202012Validator]:
    validators: dict[str, Draft202012Validator] = {}
    for kind, name in KIND_TO_SCHEMA.items():
        path = SCHEMA_DIR / name
        if not path.exists():
            sys.exit(f"FATAL missing schema: {path}")
        schema = yaml.safe_load(path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        validators[kind] = Draft202012Validator(schema)
    return validators


# ---------------------------------------------------------------------------
# Deterministic policy rules the schemas deliberately do not express.
# ---------------------------------------------------------------------------

def policy_errors(doc: dict) -> list[str]:
    errs: list[str] = []
    kind = doc.get("kind")

    if kind == "crystallization_decision":
        if not doc.get("candidate_ref"):
            errs.append("candidate-required: a decision must reference the "
                        "open pattern-ledger candidate it consumes")
        ceiling = (doc.get("ceiling") or {}).get("rung")
        ceiling_i = rung_index(ceiling)
        valued_rungs = []
        for i, row in enumerate(doc.get("valuation") or []):
            if not isinstance(row, dict):
                continue
            rung = row.get("rung")
            valued_rungs.append(rung)
            if ceiling_i >= 0 and rung_index(rung) > ceiling_i:
                errs.append(
                    f"ceiling-exceeded: valuation[{i}] rung {rung} is above "
                    f"the resolved ceiling {ceiling} — ceilings resolve "
                    "before valuation, and ineligible rungs are never valued")
            if row.get("deflation_factor") is None or row.get("survival_factor") is None:
                errs.append(
                    f"valuation-discounting: valuation[{i}] must carry "
                    "deflation_factor and survival_factor — undiscounted "
                    "savings systematically overstate ROI")
        outcome = doc.get("outcome")
        funded = doc.get("funded")
        not_yet = doc.get("not_yet")
        if outcome == "funded" and (funded is None or not_yet is not None):
            errs.append("outcome-shape: a funded outcome carries the funded "
                        "block and no not_yet block")
        if outcome == "not_yet" and (not_yet is None or funded is not None):
            errs.append("outcome-shape: a not_yet outcome carries the "
                        "not_yet block and no spend fields — a declined "
                        "candidate never carries rung or budget")
        if outcome == "funded" and isinstance(funded, dict):
            frung = funded.get("rung")
            if frung not in valued_rungs:
                errs.append(f"funded-rung: funded rung {frung} was never "
                            "valued — the decision selects only from "
                            "eligible, valued rungs")
            elif ceiling_i >= 0 and rung_index(frung) > ceiling_i:
                errs.append(f"funded-rung: funded rung {frung} exceeds the "
                            f"ceiling {ceiling}")
            approvals = doc.get("approvals") or {}
            consent = (approvals.get("consent_check") or {}).get("automation_tier")
            if (not approvals.get("domain_fitness_ref")
                    or not approvals.get("tenant_budget_ref")
                    or consent not in ("granted", "conditional")):
                errs.append("braid-complete: funding requires the Domain "
                            "fitness reference, the Tenant budget/clearance "
                            "reference, AND automation consent — no single "
                            "layer's approval can substitute for another's")
        if doc.get("decision_ladder_rung") == 3 and not doc.get("calibration_refs"):
            errs.append("ladder-maturity: an expected-value (rung 3) "
                        "decision requires calibration evidence (scored "
                        "forecasts / estimate actuals)")

    elif kind == "crystallization_spec":
        mined = doc.get("mined") or {}
        if not mined.get("counterexamples"):
            errs.append("counterexample-floor: a spec with zero "
                        "counterexamples cannot define refusal behavior and "
                        "fails intake")
        for group in ("invariants", "parameters", "branches", "counterexamples"):
            for i, element in enumerate(mined.get(group) or []):
                if isinstance(element, dict) and not element.get("episode_refs"):
                    errs.append(f"evidence-citation: mined.{group}[{i}] "
                                "cites no episodes — specs cite evidence, "
                                "not vibes")
        corpus = doc.get("acceptance_corpus") or {}
        for i, predicate in enumerate(corpus.get("equivalence_predicates") or []):
            if isinstance(predicate, dict) and predicate.get("comparator") == "byte-equality":
                errs.append(f"byte-golden: equivalence_predicates[{i}] "
                            "declares byte-equality — byte goldens rot on "
                            "the first cosmetic change; structural-exact is "
                            "the legitimate exact comparator")
        if not doc.get("effect_class"):
            errs.append("effect-class-missing: a spec must declare its "
                        "effect class (pure | idempotent | compensable | "
                        "irreversible) — dispatch admission depends on it")

    elif kind == "crystallization_consent":
        tier = doc.get("tier")
        scope = doc.get("scope")
        if tier == "automation":
            if not isinstance(scope, dict) or not scope.get("family_category"):
                errs.append("automation-scope: an automation grant is "
                            "scoped to exactly one family category, never "
                            "global")
        elif scope is not None:
            errs.append(f"automation-scope: a {tier} grant carries no "
                        "family-category scope")

    return errs


def validate_doc(doc, validators: dict[str, Draft202012Validator]) -> list[str]:
    if not isinstance(doc, dict):
        return ["schema: document is not a mapping"]
    kind = doc.get("kind")
    if kind not in validators:
        return [f"schema: unknown crystallizer kind {kind!r}"]
    errs = policy_errors(doc)
    errs.extend(
        f"schema: {error.json_path}: {error.message}"
        for error in validators[kind].iter_errors(doc)
    )
    return errs


def iter_docs(path: Path):
    for doc in yaml.safe_load_all(path.read_text(encoding="utf-8")):
        if doc is not None:
            yield doc


def main() -> int:
    validators = load_validators()
    problems: list[str] = []
    positives = negatives = 0

    if not EXAMPLES_DIR.exists():
        sys.exit(f"FATAL missing packaged examples: {EXAMPLES_DIR}")

    for path in sorted(EXAMPLES_DIR.rglob("*.yaml")):
        rel = path.relative_to(REPO_ROOT)
        if NEGATIVE_DIR in path.parents:
            negatives += 1
            first_line = path.read_text(encoding="utf-8").splitlines()[0]
            match = EXPECTED_RE.match(first_line)
            if not match:
                problems.append(f"{rel}: negative lacks '# expected_failure:' first-line header")
                continue
            expected = match.group(1)
            errs = [e for doc in iter_docs(path) for e in validate_doc(doc, validators)]
            if not errs:
                problems.append(f"{rel}: negative passed unexpectedly (expected: {expected})")
            elif not any(expected in e for e in errs):
                problems.append(
                    f"{rel}: negative failed, but not for its intended reason "
                    f"{expected!r}; got: {errs[0]}")
        else:
            positives += 1
            for doc in iter_docs(path):
                for err in validate_doc(doc, validators):
                    problems.append(f"{rel}: {err}")

    checked_real = 0
    if len(sys.argv) > 1:
        records_dir = Path(sys.argv[1])
        if records_dir.exists():
            for path in sorted(records_dir.rglob("*.yaml")):
                for doc in iter_docs(path):
                    if isinstance(doc, dict) and doc.get("kind") in validators:
                        checked_real += 1
                        for err in validate_doc(doc, validators):
                            problems.append(f"{path}: {err}")

    print(f"crystallizer validation: {positives} positive example file(s), "
          f"{negatives} negative fixture(s), {checked_real} real record(s)")
    if problems:
        for p in problems:
            print(f"FAIL {p}")
        return 1
    print("OK all positives pass; all negatives fail for their intended reasons")
    return 0


if __name__ == "__main__":
    sys.exit(main())
