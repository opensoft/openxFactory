#!/usr/bin/env python3
"""Offline declaration validation, never a runtime conformance certificate."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys
from urllib.parse import urlsplit

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "contracts/factory-mcp/declaration.schema.json"
INPUT_LIMIT = 262144
ARTIFACT_LIMIT = 1048576


class Invalid(ValueError):
    pass


class Unavailable(OSError):
    pass


def json_loads(text):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise Invalid("duplicate_json_key")
            result[key] = value
        return result

    def bad_constant(_):
        raise Invalid("non_json_number")

    return json.loads(text, object_pairs_hook=pairs, parse_constant=bad_constant)


def bounded_read(path, limit):
    with Path(path).open("rb") as stream:
        raw = stream.read(limit + 1)
    if len(raw) > limit:
        raise Invalid("size_limit")
    return raw


def location(parts):
    return "/" + "/".join(str(p).replace("~", "~0").replace("/", "~1") for p in parts)


def pointer(doc, value):
    if not value:
        return doc
    if not value.startswith("/"):
        raise Invalid("invalid_pointer")
    for part in value[1:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        try:
            doc = doc[int(part)] if isinstance(doc, list) else doc[part]
        except (ValueError, KeyError, IndexError, TypeError):
            raise Invalid("unresolved_pointer") from None
    return doc


def safe_path(root, relative):
    path = PurePosixPath(relative)
    if (not relative or path.is_absolute() or ".." in path.parts
            or any(c in relative for c in (":", "\\", "%", "?", "#"))
            or str(path) != relative):
        raise Invalid("unsafe_reference_path")
    root = Path(root).resolve(strict=True)
    target = (root / relative).resolve(strict=True)
    if not target.is_relative_to(root) or not target.is_file():
        raise Invalid("escaping_reference_path")
    return target


def refs_in(value):
    if isinstance(value, dict):
        if set(value) == {"repository", "revision", "path", "sha256"}:
            yield value
        else:
            for child in value.values():
                yield from refs_in(child)
    elif isinstance(value, list):
        for child in value:
            yield from refs_in(child)


def ref_key(ref):
    return (ref["repository"], ref["revision"], ref["path"])


class Offline:
    def __init__(self, roots, refs):
        self.roots = roots
        self.pins = {}
        self.documents = {}
        for ref in refs:
            key = ref_key(ref)
            if key in self.pins and self.pins[key] != ref["sha256"]:
                raise Invalid("conflicting_digest")
            self.pins[key] = ref["sha256"]

    def read(self, key):
        repository, revision, path = key
        root = self.roots.get((repository, revision))
        if root is None or not Path(root).is_dir():
            raise Unavailable("snapshot_unavailable")
        if key not in self.pins:
            raise Invalid("unpinned_local_reference")
        try:
            target = safe_path(root, path)
            raw = bounded_read(target, ARTIFACT_LIMIT)
        except FileNotFoundError:
            raise Invalid("missing_artifact") from None
        if hashlib.sha256(raw).hexdigest() != self.pins[key]:
            raise Invalid("digest_mismatch")
        return raw

    def document(self, key):
        if key not in self.documents:
            try:
                self.documents[key] = json_loads(self.read(key))
            except (json.JSONDecodeError, UnicodeDecodeError, RecursionError):
                raise Invalid("malformed_schema_json") from None
            try:
                Draft202012Validator.check_schema(self.documents[key])
            except Exception:
                raise Invalid("invalid_json_schema") from None
        return self.documents[key]

    def resolve(self, key, ref):
        if not isinstance(ref, str) or any(c in ref for c in (":", "\\", "%", "?")):
            raise Invalid("remote_or_unsafe_schema_reference")
        path, sep, fragment = ref.partition("#")
        if path:
            if self.document(key).get("$id"):
                raise Invalid("unsupported_schema_base_uri")
            if PurePosixPath(path).is_absolute() or ".." in PurePosixPath(path).parts:
                raise Invalid("unsafe_schema_reference")
            path = str(PurePosixPath(key[2]).parent / path)
            key = key[:2] + (path,)
        if sep and fragment and not fragment.startswith("/"):
            raise Invalid("unsupported_schema_anchor")
        return key, pointer(self.document(key), fragment)

    def check_schema_graph(self, key):
        seen = set()
        def visit(current_key, node, depth=0):
            if depth > 128:
                raise Invalid("schema_depth_limit")
            token = (current_key, id(node))
            if token in seen:
                return
            seen.add(token)
            if isinstance(node, dict):
                if "$id" in node and node is not self.document(current_key):
                    raise Invalid("unsupported_nested_schema_id")
                if "$dynamicRef" in node or "$recursiveRef" in node:
                    raise Invalid("unsupported_dynamic_reference")
                if "$ref" in node:
                    dest, target = self.resolve(current_key, node["$ref"])
                    visit(dest, target, depth + 1)
                for keyword in ("$defs", "definitions", "properties", "patternProperties", "dependentSchemas"):
                    for child in node.get(keyword, {}).values():
                        visit(current_key, child, depth + 1)
                for keyword in ("items", "contains", "additionalProperties", "propertyNames",
                                "unevaluatedProperties", "unevaluatedItems", "not", "if", "then", "else"):
                    if keyword in node:
                        visit(current_key, node[keyword], depth + 1)
                for keyword in ("allOf", "anyOf", "oneOf", "prefixItems"):
                    for child in node.get(keyword, []):
                        visit(current_key, child, depth + 1)
            elif isinstance(node, list):
                for child in node:
                    visit(current_key, child, depth + 1)
        visit(key, self.document(key))

    def finite(self, key, node, seen=None):
        seen = set() if seen is None else seen
        token = (key, id(node))
        if token in seen or not isinstance(node, dict):
            return None
        seen = seen | {token}
        # Unsupported constraints may narrow a vocabulary; never infer exhaustiveness.
        if any(k in node for k in ("allOf", "not", "if", "then", "else", "pattern",
                                    "minLength", "maxLength")):
            return None
        if "$ref" in node:
            if any(k in node for k in ("enum", "const", "oneOf", "anyOf")):
                return None
            dest, target = self.resolve(key, node["$ref"])
            return self.finite(dest, target, seen)
        values = node.get("enum")
        if "const" in node:
            if "enum" in node and node["const"] not in node["enum"]:
                return None
            values = [node["const"]]
        if values is not None:
            return set(values) if all(isinstance(v, str) for v in values) else None
        for union in ("oneOf", "anyOf"):
            if union in node:
                parts = [self.finite(key, item, seen) for item in node[union]]
                return set().union(*parts) if all(p is not None for p in parts) else None
        return None


def report(diagnostics, gaps):
    diagnostics = sorted(diagnostics, key=lambda d: (d["dimension"], d["location"], d["code"]))
    checks = {dimension: not any(d["dimension"] == dimension for d in diagnostics)
              for dimension in ("structure", "references", "semantics")}
    if not checks["structure"]:
        checks["references"] = checks["semantics"] = None
    elif not checks["references"]:
        checks["semantics"] = None
    status = "invalid" if diagnostics else ("valid-with-gaps" if gaps else "valid")
    return {"status": status, "exit_code": 2 if any(d["code"] in
            ("snapshot_unavailable", "input_unreadable", "reference_unreadable")
            for d in diagnostics) else (1 if diagnostics else 0),
            "checks": checks, "diagnostics": diagnostics, "gaps": gaps,
            "verified_conformance": False}


def validate(declaration, snapshots):
    diagnostics = []
    def issue(dimension, code, path=""):
        diagnostics.append({"dimension": dimension, "code": code, "location": path or "/"})

    try:
        if len(json.dumps(declaration, allow_nan=False).encode()) > INPUT_LIMIT:
            raise Invalid("size_limit")
        schema = json_loads(SCHEMA.read_bytes())
        errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(declaration))
        for error in errors:
            issue("structure", "schema_" + str(error.validator), location(error.absolute_path))
    except (TypeError, ValueError, RecursionError):
        issue("structure", "invalid_json_value")
    if diagnostics:
        return report(diagnostics, [])
    gaps = declaration["gaps"]
    try:
        offline = Offline(snapshots, list(refs_in(declaration)))
        for key in sorted(offline.pins):
            offline.read(key)
        for tool in declaration["tools"]:
            for name in ("input", "output", "error"):
                offline.check_schema_graph(ref_key(tool[name]))
    except Unavailable:
        issue("references", "snapshot_unavailable")
    except Invalid as error:
        issue("references", str(error))
    except OSError:
        issue("references", "reference_unreadable")
    except (ValueError, RecursionError, TypeError):
        issue("references", "invalid_reference_graph")
    if diagnostics:
        return report(diagnostics, gaps)

    evidence = {r["id"]: r for r in declaration["evidence"]}
    gap_index = {r["id"]: r for r in gaps}
    all_ids = [r["id"] for r in declaration["evidence"] + gaps]
    if len(all_ids) != len(set(all_ids)):
        issue("semantics", "duplicate_support_id")
    tool_ids = [t["id"] for t in declaration["tools"]]
    if len(tool_ids) != len(set(tool_ids)):
        issue("semantics", "duplicate_tool_id", "/tools")
    source = declaration["source"]
    if any(r["repository"] != source["repository"] or r["revision"] != source["revision"]
           for r in source["artifacts"]):
        issue("semantics", "source_artifact_identity_mismatch", "/source/artifacts")
    service = declaration["service"]
    if service["deployment"] == "deployed":
        uri = service["canonical_resource_uri"]
        try:
            parsed = urlsplit(uri)
            if (not parsed.scheme or any(c.isspace() for c in uri)
                    or (parsed.scheme in ("http", "https") and not parsed.hostname)):
                raise ValueError("absolute resource URI required")
        except ValueError:
            issue("semantics", "invalid_resource_uri", "/service/canonical_resource_uri")

    for i, tool in enumerate(declaration["tools"]):
        path = f"/tools/{i}"
        def bad(code, suffix=""):
            issue("semantics", code, path + suffix)

        if tool["owner"] != declaration["domain"]:
            bad("owner_domain_mismatch", "/owner")
        supported, gap_concerns = set(), set()
        for name, index in (("evidence_ids", evidence), ("gap_ids", gap_index)):
            if len(tool[name]) != len(set(tool[name])):
                bad("duplicate_support_reference", "/" + name)
            for identifier in tool[name]:
                if identifier not in index:
                    bad("missing_support_reference", "/" + name)
                else:
                    supported.update(index[identifier]["concerns"])
                    if name == "gap_ids":
                        gap_concerns.update(index[identifier]["concerns"])
        for concern in ("binding", "effects", "outcomes", "evidence", "repetition", "limits"):
            if concern not in supported:
                bad("unsupported_" + concern)
        binding = tool["binding"]
        if binding["scope_status"] == "mapped" and not binding["scope_references"]:
            bad("empty_scope_mapping")
        if binding["scope_status"] == "gap" and "scope" not in gap_concerns:
            bad("missing_scope_gap")
        if binding["revocation"] == "unimplemented" and "revocation" not in gap_concerns:
            bad("missing_revocation_gap")
        policy = tool["evidence_policy"]
        if policy["audit"] == "not_implemented" and "audit" not in gap_concerns:
            bad("missing_audit_gap")
        if policy["audit"] == "implemented" and ("audit" not in supported or "audit" in gap_concerns):
            bad("unsupported_audit_claim")
        effects = tool["effects"]
        if effects["execution"] and not (effects["execution_bounded"] and effects["execution_host_controlled"]):
            bad("unbounded_execution")
        mode = tool["repetition"]["mode"]
        if mode == "lease_replay" and not effects["persistence"]:
            bad("replay_without_persistence")
        if mode == "fresh_observation" and not (effects["external_reads"] and policy["observation_time"]):
            bad("freshness_without_observation")

        inventories = tool["outcomes"]["inventories"]
        if {inv["kind"] for inv in inventories} != {"result", "error"}:
            bad("incomplete_inventory_kinds")
        rows = tool["outcomes"]["mapping"]
        seen_rows = set()
        for row in rows:
            pair = (row["inventory"], row["value"])
            if pair in seen_rows:
                bad("duplicate_outcome")
            seen_rows.add(pair)
            if row["inventory"] >= len(inventories):
                bad("unknown_inventory")
                continue
            error = inventories[row["inventory"]]["kind"] == "error"
            if row["is_error"] != error or row["class"] != (
                    "execution_failure" if error else "completed_evaluation"):
                bad("outcome_classification_mismatch")
        for j, inventory in enumerate(inventories):
            if inventory["schema"] != ("error" if inventory["kind"] == "error" else "output"):
                bad("inventory_schema_kind_mismatch")
            key = ref_key(tool[inventory["schema"]])
            try:
                node = pointer(offline.document(key), inventory["pointer"])
                values = offline.finite(key, node)
            except Invalid:
                bad("invalid_inventory_pointer")
                continue
            gap = inventory["gap_id"]
            if values is None:
                if gap not in tool["gap_ids"] or "outcomes" not in gap_index.get(gap, {}).get("concerns", []):
                    bad("unresolved_inventory_without_gap")
            else:
                mapped = {r["value"] for r in rows if r["inventory"] == j}
                if mapped != values:
                    bad("incomplete_outcome_mapping")
                if gap is not None:
                    bad("resolved_inventory_claims_gap")
    return report(diagnostics, gaps)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("declaration", type=Path)
    parser.add_argument("--snapshot", action="append", default=[], metavar="REPOSITORY@REVISION=ROOT")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    roots = {}
    try:
        for item in args.snapshot:
            key, root = item.split("=", 1)
            repository, revision = key.rsplit("@", 1)
            if not repository or not revision or not root or (repository, revision) in roots:
                raise ValueError()
            roots[(repository, revision)] = Path(root)
        declaration = json_loads(bounded_read(args.declaration, INPUT_LIMIT))
        result = validate(declaration, roots)
    except OSError:
        result = report([{"dimension": "structure", "code": "input_unreadable", "location": "/"}], [])
    except (ValueError, UnicodeDecodeError, RecursionError):
        result = report([{"dimension": "structure", "code": "invalid_input", "location": "/"}], [])
    if args.json:
        print(json.dumps(result, sort_keys=True))
    else:
        print(result["status"] + "; offline declaration checks only; verified conformance: false")
        for dimension, passed in result["checks"].items():
            state = "not run" if passed is None else ("pass" if passed else "fail")
            print(f"{dimension}: {state}")
        for diagnostic in result["diagnostics"]:
            print(f"{diagnostic['code']} {diagnostic['location']}")
        for gap in result["gaps"]:
            print(f"gap {gap['id']}: {gap['description']}")
    return result["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
