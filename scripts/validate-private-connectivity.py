#!/usr/bin/env python3
"""Validate the optional neutral connectivity record without contacting providers."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "contracts/private-connectivity/binding.schema.json"


def duplicate_guard(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate field")
        result[key] = value
    return result


def validate(manifest, now):
    if not isinstance(manifest, dict):
        return ["manifest-object-required"]
    binding = manifest.get("private_connectivity")
    if binding is None:
        return []
    validator = Draft202012Validator(json.loads(SCHEMA.read_text()), format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(binding), key=lambda error: str(list(error.path)))
    if errors:
        return ["binding-shape-invalid"]
    context = manifest.get("installation", {})
    if not isinstance(context, dict):
        return ["installation-context-required"]
    for key in ("installation_id", "customer_id", "environment"):
        if binding[key] != context.get(key):
            return ["binding-context-mismatch"]
    try:
        endpoint = urlsplit(binding["endpoint"])
        endpoint.port
    except ValueError:
        return ["endpoint-invalid"]
    if (any(char.isspace() for char in binding["endpoint"]) or endpoint.scheme != "https" or not endpoint.hostname or endpoint.username
            or endpoint.password or endpoint.query or endpoint.fragment
            or endpoint.path not in ("", "/")):
        return ["endpoint-invalid"]
    state = binding["state"]
    if state in ("requested", "unready", "revoked"):
        return []
    approval = binding.get("approval")
    if not approved(approval, binding, now):
        return ["approval-unavailable"]
    if not same_access(approval["scope"], binding["access"]):
        return ["approval-scope-mismatch"]
    if binding["routes"]:
        route = binding.get("route_approval")
        if not approved(route, binding, now) or not same_access(route["scope"], binding["access"]) or set(route["routes"]) != set(binding["routes"]):
            return ["route-approval-unavailable"]
    if state in ("enrolled", "ready"):
        enrollment = binding.get("enrollment")
        if not enrollment or enrollment["network_ref"] != binding["network_ref"]:
            return ["enrollment-unavailable"]
    if state == "ready":
        policy = binding.get("policy")
        verification = binding.get("verification")
        if (not policy or policy["network_ref"] != binding["network_ref"]
                or not same_access(policy["scope"], binding["access"]) or not verification
                or verification["policy_revision"] != policy["revision"]):
            return ["effective-policy-unavailable"]
    return []


def same_access(left, right):
    return (left["protocol"] == right["protocol"]
            and all(set(left[key]) == set(right[key]) for key in ("sources", "destinations", "ports")))


def approved(record, binding, now):
    if not record or record["status"] != "active":
        return False
    if any(record[key] != binding[key] for key in ("installation_id", "customer_id", "environment", "network_ref")):
        return False
    expires = datetime.fromisoformat(record["expires_at"].replace("Z", "+00:00"))
    return expires > now


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--now", help="UTC time for deterministic fixture checks")
    args = parser.parse_args(argv)
    try:
        now = datetime.fromisoformat(args.now.replace("Z", "+00:00")) if args.now else datetime.now(timezone.utc)
        if now.tzinfo is None:
            raise ValueError("timezone required")
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"), object_pairs_hook=duplicate_guard)
        findings = validate(manifest, now)
    except (OSError, ValueError, TypeError):
        print("FAIL: unreadable or invalid input", file=sys.stderr)
        return 2
    for finding in findings:
        print(f"FAIL: {finding}", file=sys.stderr)
    if findings:
        return 1
    print("PASS: connectivity declaration conformance")
    return 0


if __name__ == "__main__":
    sys.exit(main())
