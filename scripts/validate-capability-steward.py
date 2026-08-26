#!/usr/bin/env python3
"""Canonical validator for the capability-steward record family (add-capability-steward).

Validates the seven record kinds — `crystallized_capability` (the registry
record), `dispatch_record`, `adjudication_record`, `sentinel_policy`,
`capability_health_report`, `savings_entry`, `calibration_score` — against
their schemas plus the deterministic policy rules the shapes deliberately
do not express (shape in the schema, policy here; the family split shared
with validate-pattern-ledger.py and validate-crystallizer-contracts.py).

Run from the openxFactory checkout:

    python3 scripts/validate-capability-steward.py [RECORDS_DIR]

Two layers run: packaged reference examples (`examples/capability-steward/`;
positives must pass, negatives must fail for their first-line
`# expected_failure:` reason — the `mvp-packet-capture/` positives complete
the MVP fixture corpus), then optional real records under RECORDS_DIR.

Named policy rules (stable tokens used by negative fixtures):
  digests-only            a registry record carries digests and refs, never
                          embedded episode/corpus/artifact content
  status-transition       `active` is reachable only through the proof
                          stages (a history without `shadow` cannot serve)
  authority-status        authority.serving true only at canary or active
  demotion-bundle         a serving capability carries an armed demotion
                          trigger bundle — authority without a wired exit
                          is a gate failure
  effect-class-admission  the junction serves only pure/idempotent (D11)
  fallback-cause          an AI-path record for a family with a matched
                          capability carries a cause from the taxonomy
  postconditions-required a crystallized-path record carries evaluated
                          post-conditions
  provenance-required     a crystallized-path record carries provenance
  sentinel-floor          sentinel epsilon floor is strictly above zero and
                          current never sits below the floor
  savings-anchor          a `verified` savings entry cites a fresh sentinel
                          anchor — no self-graded savings
  adjudication-pairing    verdict and consequence pair (capability_wrong ->
                          corpus_counterexample, ai_wrong -> episode_relabel,
                          spec_underdetermined -> spec_revision)
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
EXAMPLES_DIR = REPO_ROOT / "examples" / "capability-steward"
NEGATIVE_DIR = EXAMPLES_DIR / "negative"

KIND_TO_SCHEMA = {
    "crystallized_capability": "crystallized-capability-registry.schema.yaml",
    "dispatch_record": "dispatch-record.schema.yaml",
    "adjudication_record": "adjudication-record.schema.yaml",
    "sentinel_policy": "sentinel-policy.schema.yaml",
    "capability_health_report": "capability-health-report.schema.yaml",
    "savings_entry": "savings-entry.schema.yaml",
    "calibration_score": "calibration-score.schema.yaml",
}

FORBIDDEN_EMBED_KEYS = {
    "episode_payloads", "episode_content", "corpus_content", "artifact_bytes",
}
VERDICT_CONSEQUENCE = {
    "capability_wrong": "corpus_counterexample",
    "ai_wrong": "episode_relabel",
    "spec_underdetermined": "spec_revision",
}
EXPECTED_RE = re.compile(r"^#\s*expected_failure:\s*(.+?)\s*$")


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


def policy_errors(doc: dict) -> list[str]:
    errs: list[str] = []
    kind = doc.get("kind")

    if kind == "crystallized_capability":
        embedded = FORBIDDEN_EMBED_KEYS & set(doc)
        for key in sorted(embedded):
            errs.append(f"digests-only: registry records carry digests and "
                        f"references, never embedded content ({key!r}) — a "
                        "registry leak must leak no tenant data")
        history = [t.get("to") for t in (doc.get("status_history") or [])
                   if isinstance(t, dict)]
        if "active" in history:
            active_at = history.index("active")
            if "shadow" not in history[:active_at]:
                errs.append("status-transition: `active` was reached without "
                            "a prior `shadow` stage — the proof ladder cannot "
                            "be skipped")
        authority = doc.get("authority") or {}
        serving = authority.get("serving") is True
        status = doc.get("status")
        if serving and status not in ("canary", "active"):
            errs.append(f"authority-status: serving=true at status "
                        f"{status!r} — authority exists only at canary or "
                        "active")
        if (serving or status in ("canary", "active")) and not doc.get("demotion_triggers_ref"):
            errs.append("demotion-bundle: a serving capability must carry an "
                        "armed demotion trigger bundle — authority without a "
                        "wired exit is a gate failure")

    elif kind == "dispatch_record":
        path_value = doc.get("path")
        effect = doc.get("effect_class")
        if path_value in ("crystallized", "dual") and effect in ("compensable", "irreversible"):
            errs.append(f"effect-class-admission: the junction admits only "
                        f"pure/idempotent capabilities in v1; {effect!r} "
                        "families route to the AI path (D11)")
        if (path_value == "ai" and doc.get("capability_ref")
                and not doc.get("fallback_cause")):
            errs.append("fallback-cause: an AI-path record for a family with "
                        "a matched capability must carry a cause from the "
                        "controlled taxonomy — fallbacks are frontier "
                        "evidence, not noise")
        if path_value == "crystallized":
            postconditions = doc.get("postconditions") or {}
            if postconditions.get("evaluated") is not True:
                errs.append("postconditions-required: a crystallized output "
                            "counts as done only after its post-conditions "
                            "are evaluated")
            if not doc.get("provenance"):
                errs.append("provenance-required: a crystallized-path record "
                            "must carry its served-by provenance — the only "
                            "difference an auditor sees between paths")

    elif kind == "sentinel_policy":
        epsilon = doc.get("epsilon") or {}
        floor = epsilon.get("floor")
        current = epsilon.get("current")
        if isinstance(floor, (int, float)) and floor <= 0:
            errs.append("sentinel-floor: the sentinel floor is strictly "
                        "above zero while a capability holds authority — "
                        "drift detection, corpus freshness, and "
                        "counterfactuals all die at zero")
        if (isinstance(floor, (int, float)) and isinstance(current, (int, float))
                and current < floor):
            errs.append("sentinel-floor: epsilon.current sits below the "
                        "declared floor")

    elif kind == "savings_entry":
        counterfactual = doc.get("counterfactual") or {}
        if doc.get("verdict") == "verified" and (
                not counterfactual.get("anchor_ref")
                or not counterfactual.get("anchored_at")):
            errs.append("savings-anchor: a verified savings entry requires a "
                        "fresh sentinel-anchored counterfactual — stale or "
                        "missing anchors report unverifiable, never an "
                        "estimate dressed as fact")

    elif kind == "adjudication_record":
        verdict = doc.get("verdict")
        expected = VERDICT_CONSEQUENCE.get(verdict)
        if expected and doc.get("consequence") != expected:
            errs.append(f"adjudication-pairing: verdict {verdict!r} pairs "
                        f"with consequence {expected!r}, got "
                        f"{doc.get('consequence')!r}")

    return errs


def validate_doc(doc, validators: dict[str, Draft202012Validator]) -> list[str]:
    if not isinstance(doc, dict):
        return ["schema: document is not a mapping"]
    kind = doc.get("kind")
    if kind not in validators:
        return [f"schema: unknown capability-steward kind {kind!r}"]
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

    print(f"capability-steward validation: {positives} positive example file(s), "
          f"{negatives} negative fixture(s), {checked_real} real record(s)")
    if problems:
        for p in problems:
            print(f"FAIL {p}")
        return 1
    print("OK all positives pass; all negatives fail for their intended reasons")
    return 0


if __name__ == "__main__":
    sys.exit(main())
