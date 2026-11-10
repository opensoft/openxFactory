#!/usr/bin/env python3
"""Verify feature 040 evidence records. This command never runs owner commands."""

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import sys


CASES = {
    "T003": "lab-scope operators custody windows",
    "T004": "binding-shape binding-scope readiness credential-custody routes",
    "T005": "retries changed-input reauthorization credentials revocation-replay",
    "T006": "offline candidate-pins deny-baseline probe-control",
    "T007": "local-package local-endpoint local-ops",
    "T008": "new-local existing-local unbound local-scope local-unready",
    "T009": "standalone-entitlement dedicated-instance provision-retry",
    "T010": "policy-before-enroll managed-credential route-approval share-scoped share-denied detach subscription-end terminate",
    "T011": "backup upgrade quarantine-restore",
    "T012": "standalone-a-b retry-one-network enroll-and-revoke cross-customer wrong-environment wrong-endpoint wrong-credential wrong-port routes direct relay terminate-isolated",
    "T013": "local-managed partial-enrollment local-detach migration-rehearsal",
    "T014": "new-local existing-local unbound local-managed invalid-binding managed-retry shared-distinct-grants detach subscription-end",
    "T015": "hosted-new hosted-reuse hosted-unbound hosted-authorization hosted-failed-step hosted-retry",
    "T016": "domain-inventory profile-evidence catalog-deny",
    "T017": "hosted-new hosted-reuse hosted-unbound hosted-retry hosted-unready cross-customer public-ingress application-auth hosted-detach catalog-scope",
    "T018": "direct-existing direct-new relay-existing relay-new disconnected-peer",
    "T019": "service-loss relay-loss upgrade restore-timing backup-age fence-and-quarantine restored-identity-and-grants revocation-survives neighbor-available",
    "T020": "cutover-source-revoked rollback-timing partial-target-revoked prior-binding-valid prior-binding-revoked",
    "T021": "four-paths gate-chain drills incidents-closed owner-signoff rollout-decision",
}
DEPENDENCIES = {
    "T003": ["T001"], "T004": ["T001"], "T005": ["T004"],
    "T006": ["T003", "T005"], "T007": ["T004"], "T008": ["T007"],
    "T009": ["T004"], "T010": ["T009"], "T011": ["T009"],
    "T012": ["T006", "T010", "T011"], "T013": ["T008", "T010"],
    "T014": ["T006", "T012", "T013"], "T015": ["T004", "T010"],
    "T016": ["T004"], "T017": ["T014", "T015", "T016"],
    "T018": ["T017"], "T019": ["T018"], "T020": ["T019"],
    "T021": ["T006", "T012", "T014", "T017", "T018", "T019", "T020"],
}
TASK_SCOPE = {
    "T003": "evidence_tooling", "T004": "neutral_binding",
    "T005": "neutral_binding", "T006": "evidence_tooling",
    "T007": "headscale_install", "T008": "installer",
    "T009": "hosted_product", "T010": "hosted_product", "T011": "ops",
    "T012": "hosted_product", "T013": "installer", "T014": "installer",
    "T015": "hosted_product", "T016": "hosted_domain",
    "T017": "hosted_domain", "T018": "ops", "T019": "ops", "T020": "installer",
    "T021": "evidence_tooling",
}
SUBCHECKS = {
    ("T003", "lab-scope"): "account region budget synthetic-fixtures",
    ("T003", "operators"): "rollout-lead signoff-owner rollback-owner",
    ("T003", "windows"): "limits sampling sustained-denial",
    ("T004", "binding-scope"): "wrong-customer wrong-environment wrong-endpoint wrong-approval",
    ("T004", "readiness"): "approval enrollment effective-policy",
    ("T004", "credential-custody"): "binding logs support",
    ("T005", "retries"): "interrupted-provision interrupted-enroll duplicate",
    ("T005", "credentials"): "expired replayed",
    ("T008", "local-unready"): "endpoint authorization policy redacted-error prior-state",
    ("T010", "share-scoped"): "two-installations distinct-grants explicit-approval",
    ("T010", "subscription-end"): "affected-revoked unrelated-retained entitlement-retained",
    ("T012", "standalone-a-b"): "instance-a instance-b policy-a-before-enroll policy-b-before-enroll",
    ("T012", "cross-customer"): "administration enrollment traffic",
    ("T012", "routes"): "unapproved-denied approved-route",
    ("T012", "direct"): "allowed denied",
    ("T012", "relay"): "allowed denied",
    ("T014", "invalid-binding"): "endpoint selection policy destination port",
    ("T014", "shared-distinct-grants"): "two-installations distinct-grants explicit-approval",
    ("T014", "subscription-end"): "affected-revoked unrelated-retained entitlement-retained",
    ("T015", "hosted-failed-step"): "policy enrollment redacted-error unready",
    ("T016", "profile-evidence"): "domain revision tenant deployment lifecycle connectivity",
    ("T016", "catalog-deny"): "missing stale unqualified wrong-domain",
    ("T017", "hosted-unready"): "policy enrollment redacted-error unready",
    ("T019", "fence-and-quarantine"): "prior-writer-fenced no-early-activation",
    ("T019", "restored-identity-and-grants"): "network-identity allowed-grants",
    ("T021", "four-paths"): "local-headscale local-managed standalone hosted-factory",
}
DENIAL_CASES = {
    "changed-input", "reauthorization", "credentials", "share-denied",
    "cross-customer", "wrong-environment", "wrong-endpoint", "wrong-credential",
    "wrong-port", "catalog-deny", "public-ingress", "application-auth",
    "prior-binding-revoked",
}
LIVE_TASKS = {"T006", "T012", "T014", "T017", "T018", "T019", "T020", "T021"}
GATE_TASKS = {"T006", "T012", "T014", "T017", "T021"}
IMPLEMENTATION_TASKS = set(CASES) - {"T003", "T006", "T021"}
SCOPE_NAMES = {
    "neutral_binding", "installer", "ops", "headscale_install",
    "hosted_product", "hosted_domain", "evidence_tooling",
}
LIMIT_NAMES = {
    "revocation_seconds", "restore_seconds", "backup_age_seconds",
    "rollback_seconds", "probe_interval_seconds", "sustained_denial_seconds",
}
IMMUTABLE_REF = re.compile(
    r"(?:sha256:[a-f0-9]{64}|git:[a-f0-9]{40}:[^\s]+|"
    r"https://github\.com/[^/\s]+/[^/\s]+/(?:blob|commit)/[a-f0-9]{40}(?:/[^\s]+)?)"
)
SECRET = re.compile(
    r"-----BEGIN (?:[A-Z ]*PRIVATE KEY)-----|"
    r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"
)


class EvidenceError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise EvidenceError(message)


def object_pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON field: {key}")
        result[key] = value
    return result


def reference(value, label):
    require(isinstance(value, str) and IMMUTABLE_REF.fullmatch(value), f"{label}: immutable reference required")
    require(not any(word in value.lower() for word in ("placeholder", "todo", "tbd", "example.invalid")), f"{label}: placeholder")


def positive_number(value, label):
    require(type(value) in (int, float) and math.isfinite(value) and value > 0, f"{label}: positive finite number required")


def inspect_strings(value):
    if isinstance(value, str):
        require(not SECRET.search(value), "credential material in evidence")
    elif isinstance(value, dict):
        for item in value.values():
            inspect_strings(item)
    elif isinstance(value, list):
        for item in value:
            inspect_strings(item)


def read_record(path, task):
    require(path.name == task + ".json", f"{task}: filename mismatch")
    require(path.is_file() and not path.is_symlink(), f"{task}: ordinary evidence file required")
    for parent in path.parents:
        require(not parent.is_symlink(), f"{task}: symlinked evidence directory")
    try:
        data = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=object_pairs)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise EvidenceError(f"{task}: unreadable JSON: {error}") from error
    require(isinstance(data, dict), f"{task}: object required")
    inspect_strings(data)
    require(data.get("task") == task, f"{task}: task ID mismatch")
    require(data.get("verdict") == "pass", f"{task}: verdict is not pass")
    return data


def bootstrap_scopes(data):
    scopes = data.get("scopes")
    require(isinstance(scopes, dict) and set(scopes) == SCOPE_NAMES, "T001: seven scopes required")
    for name, scope in scopes.items():
        require(isinstance(scope, dict), f"T001: invalid scope {name}")
        for field in ("owner", "repository", "approval_ref", "file_scope", "release_path", "verify"):
            require(isinstance(scope.get(field), str) and scope[field].strip(), f"T001: missing {name}.{field}")
        reference(scope["approval_ref"], f"T001 {name} approval")
    return scopes


def verify_cases(data, task):
    cases = data.get("cases")
    expected_cases = set(CASES[task].split())
    require(isinstance(cases, dict) and set(cases) == expected_cases, f"{task}: case inventory mismatch")
    for name, case in cases.items():
        expected = "denied" if name in DENIAL_CASES else "verified"
        require(isinstance(case, dict), f"{task}/{name}: object required")
        require(case.get("expected") == expected and case.get("observed") == expected, f"{task}/{name}: unexpected outcome")
        reference(case.get("evidence_ref"), f"{task}/{name}")
        checks = case.get("checks")
        required_checks = set(SUBCHECKS.get((task, name), "result").split())
        require(isinstance(checks, dict) and set(checks) == required_checks, f"{task}/{name}: subcheck inventory mismatch")
        for check, outcome in checks.items():
            require(isinstance(check, str) and check.strip(), f"{task}/{name}: invalid subcheck")
            require(isinstance(outcome, dict) and outcome.get("passed") is True, f"{task}/{name}/{check}: failed subcheck")
            reference(outcome.get("evidence_ref"), f"{task}/{name}/{check}")


def number_at_most(value, maximum, label):
    require(type(value) in (int, float) and math.isfinite(value) and 0 <= value <= maximum, f"{label}: outside approved window")


def verify_timing(data, task, limits):
    cases = data["cases"]
    if task == "T018":
        for name, case in cases.items():
            metrics = case.get("metrics", {})
            number_at_most(metrics.get("elapsed_seconds"), limits["revocation_seconds"], name)
            number_at_most(metrics.get("max_probe_gap_seconds"), limits["probe_interval_seconds"], name)
            duration = metrics.get("sustained_denial_seconds")
            positive_number(duration, name)
            require(duration >= limits["sustained_denial_seconds"], f"{name}: insufficient sustained denial")
            require(metrics.get("allowed_after_deadline") is False, f"{name}: usable connection after deadline")
            require(metrics.get("quarantine_used") is False, f"{name}: quarantine is not network revocation evidence")
    if task == "T019":
        number_at_most(cases["restore-timing"].get("elapsed_seconds"), limits["restore_seconds"], "restore")
        number_at_most(cases["backup-age"].get("elapsed_seconds"), limits["backup_age_seconds"], "backup age")
    if task == "T020":
        number_at_most(cases["rollback-timing"].get("elapsed_seconds"), limits["rollback_seconds"], "rollback")


def verify_file(path, task, cache=None):
    path = Path(path).absolute()
    if cache is None:
        cache = {}
    key = (str(path), task)
    if key in cache:
        return cache[key]
    data = read_record(path, task)
    if task == "T001":
        bootstrap_scopes(data)
        cache[key] = data
        return data
    require(task in CASES, f"unsupported task {task}")
    scopes = bootstrap_scopes(read_record(path.parent / "T001.json", "T001"))
    scope = TASK_SCOPE[task]
    require(data.get("scope") == scope, f"{task}: wrong approval scope")
    require(data.get("approval_ref") == scopes[scope]["approval_ref"], f"{task}: approval does not match T001")
    require(data.get("owner") == scopes[scope]["owner"], f"{task}: owner does not match scope")
    revision = data.get("decision_ref") if task in {"T003", "T006", "T021"} else data.get("revision_ref")
    reference(revision, f"{task}: revision or decision")
    verify_cases(data, task)
    if task in IMPLEMENTATION_TASKS:
        check = data.get("owner_check")
        require(isinstance(check, dict) and isinstance(check.get("command"), str) and check["command"].strip(), f"{task}: missing owner command")
        require(check["command"] == scopes[scope]["verify"], f"{task}: command does not match approved scope")
        require(type(check.get("exit_status")) is int and check["exit_status"] == 0, f"{task}: owner check failed")
        reference(check.get("output_ref"), f"{task}: owner output")
    deps = data.get("dependencies")
    require(isinstance(deps, dict) and set(deps) == set(DEPENDENCIES[task]), f"{task}: dependency inventory mismatch")
    for dependency, digest in deps.items():
        dependency_path = path.parent / (dependency + ".json")
        require(dependency_path.is_file() and not dependency_path.is_symlink(), f"{task}: missing dependency {dependency}")
        actual = hashlib.sha256(dependency_path.read_bytes()).hexdigest()
        require(digest == actual, f"{task}: superseded dependency {dependency}")
        verify_file(dependency_path, dependency, cache)
    if task == "T003":
        limits = data.get("limits")
        require(isinstance(limits, dict) and set(limits) == LIMIT_NAMES, "T003: complete approved limits required")
        for name, value in limits.items():
            positive_number(value, name)
        require(limits["probe_interval_seconds"] <= 10, "T003: probe interval exceeds 10 seconds")
    if task in LIVE_TASKS:
        reference(data.get("run_ref"), f"{task}: run")
        pins = data.get("candidate_pins")
        require(isinstance(pins, dict) and pins, f"{task}: candidate pins required")
        for name, pin in pins.items():
            require(isinstance(name, str) and name.strip(), "invalid pin name")
            reference(pin, f"{task}: {name} pin")
        baseline = data.get("policy_baseline")
        require(isinstance(baseline, dict) and baseline, f"{task}: policy baseline required")
        for name, pin in baseline.items():
            reference(pin, f"{task}: policy {name}")
        if task != "T006":
            g0 = verify_file(path.parent / "T006.json", "T006", cache)
            require(data["run_ref"] == g0["run_ref"] and pins == g0["candidate_pins"] and baseline == g0["policy_baseline"], f"{task}: pilot run, pins or policy baseline mismatch")
            for dependency in DEPENDENCIES[task]:
                prior = cache[(str(path.parent / (dependency + ".json")), dependency)]
                if dependency in LIVE_TASKS:
                    require(prior["run_ref"] == data["run_ref"], f"{task}: dependency from different run")
            limits = verify_file(path.parent / "T003.json", "T003", cache)["limits"]
            verify_timing(data, task, limits)
        if task in {"T012", "T014", "T017", "T018", "T019", "T020"}:
            controls = data.get("positive_controls")
            require(isinstance(controls, dict) and set(controls) == set(baseline), f"{task}: positive control required for every boundary")
            for name, control in controls.items():
                require(isinstance(control, dict) and control.get("reachable") is True, f"{task}: control failed for {name}")
                reference(control.get("evidence_ref"), f"{task}: control {name}")
        if task == "T021":
            signoffs = data.get("signoffs")
            require(isinstance(signoffs, dict) and set(signoffs) == {"rollout_lead", "installer", "ops", "hosted_product", "hosted_domain"}, "T021: owner sign-offs required")
            for role, ref in signoffs.items():
                reference(ref, f"T021: {role}")
    cache[key] = data
    return data


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True, choices=["T001"] + list(CASES))
    parser.add_argument("evidence", type=Path)
    args = parser.parse_args(argv)
    try:
        verify_file(args.evidence, args.task)
    except (EvidenceError, OSError, UnicodeError) as error:
        print(f"FAIL {args.task}: {error}", file=sys.stderr)
        return 1
    print(f"PASS {args.task}: evidence structure and prerequisite records verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
