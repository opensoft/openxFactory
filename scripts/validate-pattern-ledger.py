#!/usr/bin/env python3
"""Canonical validator for the pattern-ledger record family (add-pattern-ledger).

Validates the five sensing record kinds of recurrence crystallization —
`episode`, `outcome_label`, `recurrence_family`, `recurrence_forecast`,
`crystallization_candidate` — against their schemas
(`contracts/schemas/pattern-ledger-*.schema.yaml`) plus the deterministic
policy rules the shapes deliberately do not express (the schema owns shape,
this validator owns policy; see the candidate schema's description).

Run from the openxFactory checkout:

    python3 scripts/validate-pattern-ledger.py [LEDGER_DIR]

Two layers run (mirroring scripts/validate-derived-models.py):

1. Packaged reference examples (`examples/pattern-ledger/`): every YAML
   document outside `negative/` must pass; every file under `negative/`
   must fail for its INTENDED reason (declared in its first-line
   `# expected_failure:` header) — the self-test fails closed if a
   negative stops failing for its reason or any positive fails. The
   `mvp-packet-capture/` positives are the MVP fixture corpus (staging
   decision D8): episodes hand-derived from the real packet-capture runs
   of 2026-07-28/29.
2. Optional real records under LEDGER_DIR: every YAML document whose
   `kind` is a pattern-ledger kind validates fully; other kinds are
   skipped; absence of the directory or of ledger records is not a
   failure (the ledger is opt-in until the sweep lane realizes).

Named policy rules (stable tokens used by negative fixtures):
  consent-tiers             episode consent must explicitly carry all three
                            tiers (episode_use, automation, pooling) —
                            default deny is explicit, never implied
  mutable-verdict           an episode must not store quality/verdict —
                            quality is a fold over its outcome_label stream
  tenant-mismatch           a family member's tenant_ref must equal the
                            family's tenant_ref (families never mix tenants)
  transition-order          family transition timestamps must not decrease
  idempotency-missing       a candidate must carry an idempotency_key
  idempotency-family-mismatch  the key must be '<family_ref>+<digest>'
  candidate-evidence        a candidate must cite episode refs AND a
                            forecast — praise-only rationales are invalid
  forecast-min-evidence     a forecast needs >= MIN_FORECAST_EVIDENCE
                            instances in its evidence window (staged dial
                            `min_family_forecast`, default 3)
  score-pairing             score_ref and scored_at are set together, and
                            scored_at never precedes matures_at
  schema                    structural nonconformance to the record schema
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = REPO_ROOT / "contracts" / "schemas"
EXAMPLES_DIR = REPO_ROOT / "examples" / "pattern-ledger"
NEGATIVE_DIR = EXAMPLES_DIR / "negative"

KIND_TO_SCHEMA = {
    "episode": "pattern-ledger-episode.schema.yaml",
    "outcome_label": "pattern-ledger-outcome-label.schema.yaml",
    "recurrence_family": "pattern-ledger-recurrence-family.schema.yaml",
    "recurrence_forecast": "pattern-ledger-recurrence-forecast.schema.yaml",
    "crystallization_candidate": "pattern-ledger-crystallization-candidate.schema.yaml",
}

# Staged default from the recurrence-crystallization dials register
# (`min_family_forecast`); becomes tenant/domain policy when the dials
# contract realizes — a constant here is the wave-one posture.
MIN_FORECAST_EVIDENCE = 3

EXPECTED_RE = re.compile(r"^#\s*expected_failure:\s*(.+?)\s*$")


def load_schemas() -> dict[str, dict]:
    schemas: dict[str, dict] = {}
    for kind, name in KIND_TO_SCHEMA.items():
        path = SCHEMA_DIR / name
        if not path.exists():
            sys.exit(f"FATAL missing schema: {path}")
        schemas[kind] = yaml.safe_load(path.read_text(encoding="utf-8"))
    return schemas


# ---------------------------------------------------------------------------
# Minimal JSON-Schema (draft 2020-12 subset) structural checker.
# Supported keywords: $ref (#/$defs/... local), type (incl. lists and
# "null"), const, enum, pattern, minLength, minimum, maximum, minItems,
# minProperties, required, properties, additionalProperties (false), items.
# Kept dependency-free on purpose: repo validators import yaml only.
# ---------------------------------------------------------------------------

def _type_ok(value, tname: str) -> bool:
    if tname == "object":
        return isinstance(value, dict)
    if tname == "array":
        return isinstance(value, list)
    if tname == "string":
        return isinstance(value, str)
    if tname == "boolean":
        return isinstance(value, bool)
    if tname == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if tname == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if tname == "null":
        return value is None
    return False


def check_schema(value, schema: dict, root: dict, path: str = "$") -> list[str]:
    errs: list[str] = []
    if "$ref" in schema:
        ref = schema["$ref"]
        if not ref.startswith("#/$defs/"):
            return [f"schema: {path}: unsupported $ref {ref!r}"]
        target = root.get("$defs", {}).get(ref.split("/")[-1])
        if target is None:
            return [f"schema: {path}: unresolved $ref {ref!r}"]
        return check_schema(value, target, root, path)

    t = schema.get("type")
    if t is not None:
        types = t if isinstance(t, list) else [t]
        if not any(_type_ok(value, x) for x in types):
            return [f"schema: {path}: expected type {types}, got {type(value).__name__}"]

    if "const" in schema and value != schema["const"]:
        errs.append(f"schema: {path}: expected const {schema['const']!r}, got {value!r}")
    if "enum" in schema and value not in schema["enum"]:
        errs.append(f"schema: {path}: {value!r} not in enum {schema['enum']}")
    if "pattern" in schema and isinstance(value, str):
        if not re.search(schema["pattern"], value):
            errs.append(f"schema: {path}: {value!r} does not match pattern {schema['pattern']!r}")
    if "minLength" in schema and isinstance(value, str) and len(value) < schema["minLength"]:
        errs.append(f"schema: {path}: shorter than minLength {schema['minLength']}")
    if "minimum" in schema and isinstance(value, (int, float)) and not isinstance(value, bool):
        if value < schema["minimum"]:
            errs.append(f"schema: {path}: {value} < minimum {schema['minimum']}")
    if "maximum" in schema and isinstance(value, (int, float)) and not isinstance(value, bool):
        if value > schema["maximum"]:
            errs.append(f"schema: {path}: {value} > maximum {schema['maximum']}")

    if isinstance(value, dict):
        if "minProperties" in schema and len(value) < schema["minProperties"]:
            errs.append(f"schema: {path}: fewer than minProperties {schema['minProperties']}")
        props = schema.get("properties", {})
        for req in schema.get("required", []):
            if req not in value:
                errs.append(f"schema: {path}: missing required field {req!r}")
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in props:
                    errs.append(f"schema: {path}: unexpected field {key!r}")
        for key, sub in props.items():
            if key in value:
                errs.extend(check_schema(value[key], sub, root, f"{path}.{key}"))

    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errs.append(f"schema: {path}: fewer than minItems {schema['minItems']}")
        items = schema.get("items")
        if isinstance(items, dict):
            for i, item in enumerate(value):
                errs.extend(check_schema(item, items, root, f"{path}[{i}]"))

    return errs


# ---------------------------------------------------------------------------
# Deterministic policy rules the schemas deliberately do not express.
# ---------------------------------------------------------------------------

def policy_errors(doc: dict) -> list[str]:
    errs: list[str] = []
    kind = doc.get("kind")

    if kind == "episode":
        consent = doc.get("consent")
        tiers = {"episode_use", "automation", "pooling"}
        if not isinstance(consent, dict) or not tiers <= set(consent):
            errs.append(
                "consent-tiers: episode consent must explicitly carry "
                "episode_use, automation, and pooling (default deny is "
                "explicit, never implied)")
        for forbidden in ("quality", "verdict", "outcome"):
            if forbidden in doc:
                errs.append(
                    f"mutable-verdict: episode must not store {forbidden!r} "
                    "— quality is a fold over the outcome_label stream")

    elif kind == "recurrence_family":
        fam_tenant = doc.get("tenant_ref")
        for i, member in enumerate(doc.get("members") or []):
            if not isinstance(member, dict):
                continue
            m_tenant = member.get("tenant_ref")
            if m_tenant is not None and m_tenant != fam_tenant:
                errs.append(
                    f"tenant-mismatch: member[{i}] tenant_ref {m_tenant!r} "
                    f"!= family tenant_ref {fam_tenant!r} — families never "
                    "mix tenants")
        ats = [t.get("at") for t in (doc.get("transitions") or [])
               if isinstance(t, dict) and isinstance(t.get("at"), str)]
        if any(a > b for a, b in zip(ats, ats[1:])):
            errs.append("transition-order: transition timestamps must be "
                        "non-decreasing (recorded history, not re-sorted)")

    elif kind == "crystallization_candidate":
        key = doc.get("idempotency_key")
        family_ref = doc.get("family_ref")
        if not key:
            errs.append("idempotency-missing: a candidate must carry an "
                        "idempotency_key (family ref + evidence-window "
                        "digest) so regeneration suppresses to a no-op")
        elif isinstance(family_ref, str) and not key.startswith(family_ref + "+"):
            errs.append("idempotency-family-mismatch: idempotency_key must "
                        f"start with {family_ref + '+'!r}")
        evidence = doc.get("evidence") or {}
        episode_refs = evidence.get("episode_refs") if isinstance(evidence, dict) else None
        if not episode_refs or not doc.get("forecast_ref"):
            errs.append("candidate-evidence: nomination must cite episode "
                        "refs AND a forecast record — praise-only "
                        "rationales are insufficient evidence for anything "
                        "that leads to spend")

    elif kind == "recurrence_forecast":
        window = doc.get("evidence_window") or {}
        instances = window.get("instances") if isinstance(window, dict) else None
        if isinstance(instances, int) and instances < MIN_FORECAST_EVIDENCE:
            errs.append(
                f"forecast-min-evidence: evidence window has {instances} "
                f"instance(s) < {MIN_FORECAST_EVIDENCE} "
                "(staged dial min_family_forecast) — the family stays "
                "forming instead")
        score_ref, scored_at = doc.get("score_ref"), doc.get("scored_at")
        if (score_ref is None) != (scored_at is None):
            errs.append("score-pairing: score_ref and scored_at must be "
                        "null together or set together")
        elif score_ref is not None:
            matures_at = doc.get("matures_at")
            if isinstance(matures_at, str) and isinstance(scored_at, str) and scored_at < matures_at:
                errs.append("score-pairing: scored_at precedes matures_at — "
                            "a forecast is scored only after it matures")

    return errs


def validate_doc(doc, schemas: dict[str, dict]) -> list[str]:
    if not isinstance(doc, dict):
        return ["schema: document is not a mapping"]
    kind = doc.get("kind")
    if kind not in schemas:
        return [f"schema: unknown pattern-ledger kind {kind!r}"]
    errs = policy_errors(doc)
    errs.extend(check_schema(doc, schemas[kind], schemas[kind]))
    return errs


def iter_docs(path: Path):
    for doc in yaml.safe_load_all(path.read_text(encoding="utf-8")):
        if doc is not None:
            yield doc


def main() -> int:
    schemas = load_schemas()
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
            errs = [e for doc in iter_docs(path) for e in validate_doc(doc, schemas)]
            if not errs:
                problems.append(f"{rel}: negative passed unexpectedly (expected: {expected})")
            elif not any(expected in e for e in errs):
                problems.append(
                    f"{rel}: negative failed, but not for its intended reason "
                    f"{expected!r}; got: {errs[0]}")
        else:
            positives += 1
            for doc in iter_docs(path):
                for err in validate_doc(doc, schemas):
                    problems.append(f"{rel}: {err}")

    checked_real = 0
    if len(sys.argv) > 1:
        ledger_dir = Path(sys.argv[1])
        if ledger_dir.exists():
            for path in sorted(ledger_dir.rglob("*.yaml")):
                for doc in iter_docs(path):
                    if isinstance(doc, dict) and doc.get("kind") in schemas:
                        checked_real += 1
                        for err in validate_doc(doc, schemas):
                            problems.append(f"{path}: {err}")

    print(f"pattern-ledger validation: {positives} positive example file(s), "
          f"{negatives} negative fixture(s), {checked_real} real record(s)")
    if problems:
        for p in problems:
            print(f"FAIL {p}")
        return 1
    print("OK all positives pass; all negatives fail for their intended reasons")
    return 0


if __name__ == "__main__":
    sys.exit(main())
