#!/usr/bin/env python3
"""Validate the optional neutral connectivity record without contacting providers."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
from urllib.parse import urlsplit

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "specs/040-private-connectivity/contracts/private-connectivity/binding.schema.json"


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
    if any(validator.iter_errors(binding)):
        return ["binding-shape-invalid"]
    context = manifest.get("installation", {})
    if not isinstance(context, dict):
        return ["installation-context-required"]
    if any(binding[key] != context.get(key) for key in ("installation_id", "customer_id", "environment")):
        return ["binding-context-mismatch"]
    return endpoint_errors(binding["endpoint"]) or state_errors(binding, now)


def endpoint_errors(value):
    try:
        endpoint = urlsplit(value)
        endpoint.port
    except ValueError:
        return ["endpoint-invalid"]
    if (any(char.isspace() for char in value) or endpoint.scheme != "https" or not endpoint.hostname or endpoint.username
            or endpoint.password or endpoint.query or endpoint.fragment or endpoint.path not in ("", "/")):
        return ["endpoint-invalid"]
    return []


def state_errors(binding, now):
    state = binding["state"]
    if state in ("requested", "unready", "revoked"):
        return []
    approval = binding.get("approval")
    if not approved(approval, binding, now):
        return ["approval-unavailable"]
    if not same_access(approval["scope"], binding["access"]):
        return ["approval-scope-mismatch"]
    if binding["routes"] and not routes_approved(binding, now):
        return ["route-approval-unavailable"]
    enrollment = binding.get("enrollment")
    if state in ("enrolled", "ready") and (not enrollment or enrollment["network_ref"] != binding["network_ref"]):
        return ["enrollment-unavailable"]
    return readiness_errors(binding) if state == "ready" else []


def routes_approved(binding, now):
    route = binding.get("route_approval")
    return (approved(route, binding, now) and same_access(route["scope"], binding["access"])
            and set(route["routes"]) == set(binding["routes"]))


def readiness_errors(binding):
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
    if any(record[key] != binding[key] for key in ("installation_id", "customer_id", "environment", "network_ref", "endpoint")):
        return False
    try:
        expires = datetime.fromisoformat(record["expires_at"].replace("Z", "+00:00"))
        return expires.tzinfo is not None and expires > now
    except (ValueError, TypeError):
        return False


def checked_manifest(value):
    resolved = os.path.realpath(value)
    base = os.path.realpath(os.getcwd())
    prefix = base if base.endswith(os.sep) else base + os.sep
    if resolved != base and not resolved.startswith(prefix):
        raise ValueError("manifest outside working directory")
    path = Path(resolved)
    if not path.is_file() or Path(value).is_symlink():
        raise ValueError("ordinary manifest file required")
    return resolved


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest")
    parser.add_argument("--now", help="UTC time for deterministic fixture checks")
    args = parser.parse_args(argv)
    try:
        now = datetime.fromisoformat(args.now.replace("Z", "+00:00")) if args.now else datetime.now(timezone.utc)
        if now.tzinfo is None:
            raise ValueError("timezone required")
        manifest = json.loads(Path(checked_manifest(args.manifest)).read_text(encoding="utf-8"), object_pairs_hook=duplicate_guard)
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
