#!/usr/bin/env python3
"""Offline declaration validation, never a runtime conformance certificate."""
import argparse
from collections import Counter
import errno
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
import unicodedata
from urllib.parse import urlsplit

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "contracts/factory-mcp/declaration.schema.json"
INPUT_LIMIT = 262144
ARTIFACT_LIMIT = 1048576
DEPTH_LIMIT = 128

# RFC 6901: an array index is `0` or an ASCII digit run without a leading zero.
# `[0-9]`, never `\d`: Python's `\d` also matches non-ASCII decimal digits.
ARRAY_INDEX = re.compile(r"0|[1-9][0-9]*")
BAD_ESCAPE = re.compile(r"~(?![01])")

# Keywords whose values are subschemas. Data keywords (`examples`, `default`,
# `const`, `enum`) are never interpreted as schemas.
SCHEMA_MAPS = ("$defs", "definitions", "properties", "patternProperties", "dependentSchemas",
               "dependencies")
SCHEMA_SINGLE = ("items", "additionalItems", "contains", "additionalProperties", "propertyNames",
                 "unevaluatedProperties", "unevaluatedItems", "not", "if", "then", "else",
                 "contentSchema")
SCHEMA_LISTS = ("allOf", "anyOf", "oneOf", "prefixItems")
# `$defs` and `definitions` hold schemas that apply only when referenced.
STORAGE = ("$defs", "definitions")
# Subschemas an outcome never lives in: a negation, a condition that only
# selects `then` or `else`, and keywords a 2020-12 evaluator never applies
# (`contentSchema` is an annotation; `additionalItems` and `dependencies` are
# older drafts'). Reachability and coverage do not enter them; the reference
# walk still does, so a remote reference under them is still refused.
NOT_OUTCOMES = ("not", "if", "contentSchema", "additionalItems", "dependencies")
UNIONS = ("oneOf", "anyOf")
# Constraints that may narrow a vocabulary; never infer exhaustiveness through them.
NARROWING = ("allOf", "not", "if", "then", "else", "pattern", "minLength", "maxLength",
             "dependentSchemas", "dependencies", "patternProperties")

REFERENCE_FIELDS = ("input", "output", "error")
UNREADABLE = ("snapshot_unavailable", "input_unreadable", "reference_unreadable")
CHECK_STATE = {None: "not run", True: "pass", False: "fail"}


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


def bounded_read(path, limit, code):
    with Path(path).open("rb") as stream:
        raw = stream.read(limit + 1)
    if len(raw) > limit:
        raise Invalid(code)
    return raw


def location(parts):
    return "/" + "/".join(str(p).replace("~", "~0").replace("/", "~1") for p in parts)


def decode_pointer(value):
    if not value:
        return []
    if not value.startswith("/"):
        raise Invalid("invalid_pointer")
    parts = []
    for raw in value[1:].split("/"):
        if BAD_ESCAPE.search(raw):
            raise Invalid("invalid_pointer")
        parts.append(raw.replace("~1", "/").replace("~0", "~"))
    return parts


def step(node, part):
    if isinstance(node, list):
        if not ARRAY_INDEX.fullmatch(part):
            raise Invalid("invalid_pointer")
        index = int(part)
        if index >= len(node):
            raise Invalid("unresolved_pointer")
        return node[index]
    if isinstance(node, dict) and part in node:
        return node[part]
    raise Invalid("unresolved_pointer")


def pointer_state(state, part, node):
    """What a JSON Pointer step lands on: a schema object, a map or list of
    schemas, or data that is not a schema at all."""
    if state == "schema":
        if part in SCHEMA_MAPS:
            state = "map"
        elif part in SCHEMA_LISTS:
            state = "list"
        elif part not in SCHEMA_SINGLE:
            return "data"
    elif state in ("map", "list"):
        state = "schema"
    else:
        return "data"
    if state == "schema" and not isinstance(node, (dict, bool)):
        return "list" if isinstance(node, list) else "data"
    return state


def safe_path(root, relative):
    path = PurePosixPath(relative)
    if (not relative or path.is_absolute() or ".." in path.parts
            or any(c in relative for c in (":", "\\", "%", "?", "#", "\x00"))
            or str(path) != relative):
        raise Invalid("unsafe_reference_path")
    try:
        root = Path(root).resolve(strict=True)
        target = (root / relative).resolve(strict=True)
    except RuntimeError:
        # Python 3.12 reports a symlink loop as RuntimeError, later versions as ELOOP.
        raise Invalid("unsafe_reference_path") from None
    except OSError as error:
        if error.errno == errno.ELOOP:
            raise Invalid("unsafe_reference_path") from None
        raise
    if not target.is_relative_to(root):
        raise Invalid("escaping_reference_path")
    if not target.is_file():
        raise Invalid("reference_not_a_file")
    return target


def references(declaration):
    """Every pinned artifact citation, with its location in the declaration."""
    for i, ref in enumerate(declaration["source"]["artifacts"]):
        yield f"/source/artifacts/{i}", ref
    for i, tool in enumerate(declaration["tools"]):
        for name in REFERENCE_FIELDS:
            yield f"/tools/{i}/{name}", tool[name]
    for i, record in enumerate(declaration["evidence"]):
        yield f"/evidence/{i}/source", record["source"]


def admits(kind, wanted, only):
    """Whether a JSON Schema `type` admits `wanted`; with `only`, nothing else."""
    kinds = kind if isinstance(kind, list) else [kind]
    return wanted in kinds and (not only or set(kinds) == {wanted})


def union_of(parts):
    """The union of finite vocabularies, or None when any one is unresolved."""
    parts = list(parts)
    return set().union(*parts) if all(p is not None for p in parts) else None


def ref_key(ref):
    return (ref["repository"], ref["revision"], ref["path"])


def children(node, skip=()):
    """The subschemas directly under a schema object, as (keyword, child) pairs."""
    for keyword in SCHEMA_MAPS:
        values = node.get(keyword) if keyword not in skip else None
        if isinstance(values, dict):
            for child in values.values():
                yield keyword, child
    for keyword in SCHEMA_SINGLE:
        if keyword in node and keyword not in skip:
            yield keyword, node[keyword]
    for keyword in SCHEMA_LISTS:
        values = node.get(keyword) if keyword not in skip else None
        if isinstance(values, list):
            for child in values:
                yield keyword, child


class Offline:
    def __init__(self, roots, pins):
        self.roots = roots
        self.pins = pins
        self.documents = {}
        self.reach_cache = {}
        self.finite_cache = {}
        self.checked_targets = set()

    def read(self, key):
        repository, revision, path = key
        root = self.roots.get((repository, revision))
        if root is None or not Path(root).is_dir():
            raise Unavailable("snapshot_unavailable")
        if key not in self.pins:
            raise Invalid("unpinned_local_reference")
        try:
            target = safe_path(root, path)
            raw = bounded_read(target, ARTIFACT_LIMIT, "artifact_size_limit")
        except FileNotFoundError:
            raise Invalid("missing_artifact") from None
        if hashlib.sha256(raw).hexdigest() != self.pins[key]:
            raise Invalid("digest_mismatch")
        return raw

    def document(self, key):
        if key not in self.documents:
            try:
                document = json_loads(self.read(key))
            except Invalid:
                raise
            except (json.JSONDecodeError, UnicodeDecodeError):
                raise Invalid("malformed_schema_json") from None
            except RecursionError:
                raise Invalid("schema_depth_limit") from None
            except ValueError:
                raise Invalid("json_number_limit") from None
            try:
                Draft202012Validator.check_schema(document)
            except RecursionError:
                raise Invalid("schema_depth_limit") from None
            except Exception:
                raise Invalid("invalid_json_schema") from None
            self.documents[key] = document
        return self.documents[key]

    def embedded(self, key, node):
        """A schema object carrying its own `$id`, below its document root, is an
        embedded resource: fragment references inside it resolve against it."""
        return (isinstance(node, dict) and isinstance(node.get("$id"), str)
                and node is not self.document(key))

    @staticmethod
    def locate(base, fragment):
        """Follow a JSON Pointer from the schema `base` to a schema location,
        tracking the nearest enclosing schema resource of the node it reaches.
        A pointer that ends in annotation data (`examples`, `enum`, `required`)
        or on a map or list of subschemas does not name a schema."""
        node, resource, state = base, base, "schema"
        for part in decode_pointer(fragment):
            node = step(node, part)
            state = pointer_state(state, part, node)
            if state == "schema" and isinstance(node, dict) and isinstance(node.get("$id"), str):
                resource = node
        if state != "schema":
            raise Invalid("reference_to_non_schema")
        return node, resource

    def resolve(self, key, ref, resource):
        if not isinstance(ref, str) or any(c in ref for c in (":", "\\", "%", "?", "\x00")):
            raise Invalid("remote_or_unsafe_schema_reference")
        path, sep, fragment = ref.partition("#")
        if sep and fragment and not fragment.startswith("/"):
            raise Invalid("unsupported_schema_anchor")
        if path:
            if resource is not self.document(key):
                raise Invalid("relative_reference_in_embedded_resource")
            if self.document(key).get("$id"):
                raise Invalid("unsupported_schema_base_uri")
            if PurePosixPath(path).is_absolute() or ".." in PurePosixPath(path).parts:
                raise Invalid("unsafe_schema_reference")
            key = key[:2] + (str(PurePosixPath(key[2]).parent / path),)
            resource = self.document(key)
        node, resource = self.locate(resource, fragment)
        return key, node, resource

    def check_schema_graph(self, key):
        seen = set()

        def visit(current_key, node, resource, depth):
            if depth > DEPTH_LIMIT:
                raise Invalid("schema_depth_limit")
            if isinstance(node, list):
                for child in node:
                    visit(current_key, child, resource, depth + 1)
                return
            if not isinstance(node, dict):
                return
            if self.embedded(current_key, node):
                resource = node
            token = (current_key, id(node), id(resource))
            if token in seen:
                return
            seen.add(token)
            if "$dynamicRef" in node or "$recursiveRef" in node:
                raise Invalid("unsupported_dynamic_reference")
            if "$ref" in node:
                dest, target, target_resource = self.resolve(current_key, node["$ref"], resource)
                self.check_target(target)
                visit(dest, target, target_resource, depth + 1)
            for _, child in children(node):
                visit(current_key, child, resource, depth + 1)

        document = self.document(key)
        visit(key, document, document, 0)

    def check_target(self, target):
        """A reference must land on a schema: a boolean, or an object the
        metaschema accepts. Annotation data (`examples`, `required`, an `enum`
        array) is not a schema even inside a valid document."""
        if isinstance(target, bool) or id(target) in self.checked_targets:
            return
        if not isinstance(target, dict):
            raise Invalid("reference_to_non_schema")
        try:
            Draft202012Validator.check_schema(target)
        except RecursionError:
            raise Invalid("schema_depth_limit") from None
        except Exception:
            raise Invalid("invalid_referenced_schema") from None
        self.checked_targets.add(id(target))

    def finite(self, key, node, resource, discriminator=None, required=frozenset(), seen=frozenset(),
               typed=False):
        """The finite string vocabulary at `node`, or None when it cannot be proved.

        With a `discriminator`, `node` is an object schema, or a union of them
        (directly or through `$ref`), and the vocabulary is the union of each
        branch's required `properties.<discriminator>` constants or enums.
        Completed resolutions are memoized, so shared references cost once.
        """
        memo = (key, id(node), id(resource), discriminator, frozenset(required), typed)
        if memo in self.finite_cache:
            return self.finite_cache[memo]
        result = self.resolve_finite(key, node, resource, discriminator, required, seen, typed)
        if (key, id(node), discriminator) not in seen:
            self.finite_cache[memo] = result
        return result

    def resolve_finite(self, key, node, resource, discriminator, required, seen, typed):
        if not isinstance(node, dict):
            return None
        if self.embedded(key, node):
            resource = node
        token = (key, id(node), discriminator)
        if token in seen or any(k in node for k in NARROWING):
            return None
        # A value vocabulary needs strings; a discriminated one, objects only.
        if "type" in node and not admits(node["type"], "string" if discriminator is None else "object",
                                         only=discriminator is not None):
            return None
        names = node.get("required", [])
        if not isinstance(names, list) or not all(isinstance(name, str) for name in names):
            return None
        seen = seen | {token}
        required = required | set(names)
        typed = typed or ("type" in node and admits(node["type"], "object", only=True))
        if "$ref" in node:
            if any(k in node for k in ("enum", "const", *UNIONS)) or (
                    discriminator is not None and "properties" in node):
                return None
            dest, target, target_resource = self.resolve(key, node["$ref"], resource)
            return self.finite(dest, target, target_resource, discriminator, required, seen, typed)
        if discriminator is None:
            return self.finite_values(key, node, resource, seen)
        return self.finite_branches(key, node, resource, discriminator, required, seen, typed)

    def finite_values(self, key, node, resource, seen):
        """A value vocabulary: `enum`, `const`, or a union of them. Under `oneOf`
        a value is valid only when exactly one branch accepts it."""
        unions = [u for u in UNIONS if u in node]
        if len(unions) > 1 or (unions and ("enum" in node or "const" in node)):
            return None
        if unions:
            if not isinstance(node[unions[0]], list):
                return None
            parts = [self.finite(key, item, resource, None, frozenset(), seen) for item in node[unions[0]]]
            if any(p is None for p in parts):
                return None
            if unions[0] == "anyOf":
                return set().union(*parts)
            counts = Counter(value for part in parts for value in part)
            return {value for value, count in counts.items() if count == 1}
        values = node.get("enum")
        if values is not None and not isinstance(values, list):
            return None
        if "const" in node:
            if "enum" in node and node["const"] not in node["enum"]:
                return None
            values = [node["const"]]
        if values is not None:
            return set(values) if all(isinstance(v, str) for v in values) else None
        return None

    def finite_branches(self, key, node, resource, discriminator, required, seen, typed):
        """A discriminated vocabulary: each object branch's required property value.
        A branch must be object-only (`type: object` on it or an ancestor): an
        untyped branch also admits `null` and other values that carry no code."""
        if "enum" in node or "const" in node or all(u in node for u in UNIONS):
            return None
        properties = node.get("properties")
        for union in UNIONS:
            if union in node:
                if (isinstance(properties, dict) and discriminator in properties) or not isinstance(node[union], list):
                    return None
                return union_of(self.finite(key, item, resource, discriminator, required, seen, typed)
                                for item in node[union])
        if not typed or not isinstance(properties, dict):
            return None
        if discriminator not in properties or discriminator not in required:
            return None
        return self.finite(key, properties[discriminator], resource, None, frozenset(), seen)

    def reach(self, key, node, resource):
        """Identities of every schema object that applies to an instance of `node`,
        in place or to a part of it, following `$ref` and never entering `$defs`."""
        cache_key = (key, id(node))
        if cache_key not in self.reach_cache:
            self.reach_cache[cache_key] = {(k, id(n)) for k, n, _ in self.walk(key, node, resource)}
        return self.reach_cache[cache_key]

    def walk(self, key, node, resource):
        """(key, schema object, resource) for every object `reach` describes."""
        found, stack, out = set(), [(key, node, resource)], []
        while stack:
            current_key, current, current_resource = stack.pop()
            if isinstance(current, list):
                stack.extend((current_key, child, current_resource) for child in current)
                continue
            if not isinstance(current, dict):
                continue
            if self.embedded(current_key, current):
                current_resource = current
            identity = (current_key, id(current))
            if identity in found:
                continue
            found.add(identity)
            out.append((current_key, current, current_resource))
            if "$ref" in current:
                dest, target, target_resource = self.resolve(current_key, current["$ref"], current_resource)
                stack.append((dest, target, target_resource))
            for _, child in children(current, skip=STORAGE + NOT_OUTCOMES):
                stack.append((current_key, child, current_resource))
        return out

    def member_hold(self, key, member, resource, own, every):
        """How one union member stands: holding one of `own`, holding another
        inventory on the file, bare, or a boolean schema (`empty`/`open`)."""
        if member is False:
            return "empty"
        if not isinstance(member, dict):
            return "open"
        reach = self.reach(key, member, resource)
        if reach & own:
            return "own"
        return "held" if reach & every else "bare"

    def uncovered_branches(self, key, own, every, gapped):
        """Members of a reachable union that hold no inventory while a sibling holds one of `own`.

        An inventory inside ONE member of a union (one result variant, one
        constant of a code union) maps only that member's vocabulary, so every
        other member must hold an inventory as well: any inventory on this
        schema file (`every`), so one file carrying both the result and the error
        variants is covered by its result and error inventories together. A
        `false` member admits no instance and needs none; a `true` member admits
        any instance and cannot hold one, so only a declared outcomes gap on
        this schema file answers it.
        """
        document = self.document(key)
        uncovered = []
        for union_key, node, resource in self.walk(key, document, document):
            for keyword in UNIONS:
                members = node.get(keyword)
                if not isinstance(members, list):
                    continue
                holds = [self.member_hold(union_key, member, resource, own, every) for member in members]
                if "own" in holds:
                    uncovered += [(union_key, id(node), keyword, m) for m, hold in enumerate(holds)
                                  if hold == "bare" or (hold == "open" and not gapped)]
        return uncovered


def report(diagnostics, gaps):
    unique = {(d["dimension"], d["location"], d["code"]): d for d in diagnostics}
    diagnostics = [unique[k] for k in sorted(unique)]
    checks = {dimension: not any(d["dimension"] == dimension for d in diagnostics)
              for dimension in ("structure", "references", "semantics")}
    if not checks["structure"]:
        checks["references"] = checks["semantics"] = None
    elif not checks["references"]:
        checks["semantics"] = None
    status = "invalid" if diagnostics else ("valid-with-gaps" if gaps else "valid")
    return {"status": status, "exit_code": 2 if any(d["code"] in UNREADABLE for d in diagnostics)
            else (1 if diagnostics else 0),
            "checks": checks, "diagnostics": diagnostics, "gaps": gaps,
            "verified_conformance": False}


def resource_uri_ok(uri):
    """An absolute https URI of printable ASCII (an internationalized host is
    written in its ASCII form) with a host, and no userinfo, fragment or backslash."""
    if any(not 0x21 <= ord(c) <= 0x7E for c in uri) or "#" in uri or "\\" in uri:
        return False
    try:
        parsed = urlsplit(uri)
        _ = parsed.port  # raises ValueError on an out-of-range or malformed port
    except ValueError:
        return False
    return (parsed.scheme == "https" and bool(parsed.hostname)
            and "@" not in parsed.netloc and not parsed.fragment)


class Diagnostics(list):
    def add(self, dimension, code, path=""):
        self.append({"dimension": dimension, "code": code, "location": path or "/"})


def check_input(declaration, found):
    """The value must serialize as JSON, finitely, within the input bound."""
    try:
        # Compact UTF-8 is the smallest file any serialization of this value can be.
        text = json.dumps(declaration, ensure_ascii=False, separators=(",", ":"))
        try:
            json.dumps(declaration, allow_nan=False)
        except ValueError:
            found.add("structure", "non_json_number")
            return
        # A lone surrogate is written as a six-byte `\uXXXX` escape.
        if len(text.encode("utf-8", "backslashreplace")) > INPUT_LIMIT:
            found.add("structure", "input_size_limit")
    except RecursionError:
        found.add("structure", "json_depth_limit")
    except (TypeError, ValueError):
        found.add("structure", "invalid_json_value")


def check_structure(declaration, found):
    schema = json_loads(SCHEMA.read_bytes())
    for error in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(declaration):
        found.add("structure", "schema_" + str(error.validator), location(error.absolute_path))


def read_failure(offline, key):
    """The code an artifact read fails with, or None."""
    try:
        offline.read(key)
    except Unavailable:
        return "snapshot_unavailable"
    except Invalid as error:
        return str(error)
    except OSError:
        return "reference_unreadable"
    except (ValueError, TypeError):
        return "invalid_reference"
    return None


def graph_failure(offline, key):
    """The code a tool schema's reference graph fails with, or None."""
    try:
        offline.check_schema_graph(key)
    except Unavailable:
        return "snapshot_unavailable"
    except Invalid as error:
        return str(error)
    except OSError:
        return "reference_unreadable"
    except RecursionError:
        return "schema_depth_limit"
    except (ValueError, TypeError):
        return "invalid_reference_graph"
    return None


def check_references(declaration, snapshots, found):
    """Pin every citation, read each distinct artifact once and report a failure
    at every location that cites it; then walk each tool schema's graph."""
    pins, conflicting = {}, set()
    for path, ref in references(declaration):
        key = ref_key(ref)
        if key in pins and pins[key] != ref["sha256"]:
            found.add("references", "conflicting_digest", path)
            conflicting.add(path)
        pins.setdefault(key, ref["sha256"])
    offline = Offline(snapshots, pins)
    failures = {key: code for key in sorted(pins) if (code := read_failure(offline, key))}
    for path, ref in references(declaration):
        if path not in conflicting and ref_key(ref) in failures:
            found.add("references", failures[ref_key(ref)], path)
    for i, tool in enumerate(declaration["tools"]):
        for name in REFERENCE_FIELDS:
            path = f"/tools/{i}/{name}"
            if path in conflicting or ref_key(tool[name]) in failures:
                continue
            code = graph_failure(offline, ref_key(tool[name]))
            if code:
                found.add("references", code, path)
    return offline


def check_catalog(declaration, found):
    """Identities across the whole declaration, and the service identity."""
    support_ids = set()
    for name in ("evidence", "gaps"):
        for k, record in enumerate(declaration[name]):
            if record["id"] in support_ids:
                found.add("semantics", "duplicate_support_id", f"/{name}/{k}/id")
            support_ids.add(record["id"])
    tool_ids = set()
    for k, tool in enumerate(declaration["tools"]):
        if tool["id"] in tool_ids:
            found.add("semantics", "duplicate_tool_id", f"/tools/{k}/id")
        tool_ids.add(tool["id"])
    source = declaration["source"]
    for k, artifact in enumerate(source["artifacts"]):
        if artifact["repository"] != source["repository"] or artifact["revision"] != source["revision"]:
            found.add("semantics", "source_artifact_identity_mismatch", f"/source/artifacts/{k}")
    service = declaration["service"]
    if service["deployment"] == "deployed" and not resource_uri_ok(service["canonical_resource_uri"]):
        found.add("semantics", "invalid_resource_uri", "/service/canonical_resource_uri")


def check_support(tool, evidence, gap_index, bad):
    """Evidence and gap citations; returns the concerns supported and gapped."""
    supported, gap_concerns = set(), set()
    for name, index in (("evidence_ids", evidence), ("gap_ids", gap_index)):
        if len(tool[name]) != len(set(tool[name])):
            bad("duplicate_support_reference", "/" + name)
        for k, identifier in enumerate(tool[name]):
            if identifier not in index:
                bad("missing_support_reference", f"/{name}/{k}")
                continue
            supported.update(index[identifier]["concerns"])
            if name == "gap_ids":
                gap_concerns.update(index[identifier]["concerns"])
    for concern in ("binding", "effects", "outcomes", "evidence", "repetition", "limits"):
        if concern not in supported:
            bad("unsupported_" + concern, "/evidence_ids")
    return supported, gap_concerns


def check_claims(tool, supported, gap_concerns, bad):
    """Binding, audit, effects and repetition claims against their support."""
    binding = tool["binding"]
    if binding["scope_status"] == "mapped" and not binding["scope_references"]:
        bad("empty_scope_mapping", "/binding/scope_references")
    if binding["scope_status"] == "gap" and "scope" not in gap_concerns:
        bad("missing_scope_gap", "/binding/scope_status")
    if binding["revocation"] == "unimplemented" and "revocation" not in gap_concerns:
        bad("missing_revocation_gap", "/binding/revocation")
    policy = tool["evidence_policy"]
    if policy["audit"] == "not_implemented" and "audit" not in gap_concerns:
        bad("missing_audit_gap", "/evidence_policy/audit")
    if policy["audit"] == "implemented" and ("audit" not in supported or "audit" in gap_concerns):
        bad("unsupported_audit_claim", "/evidence_policy/audit")
    effects = tool["effects"]
    if effects["execution"] and not (effects["execution_bounded"] and effects["execution_host_controlled"]):
        bad("unbounded_execution", "/effects/execution")
    mode = tool["repetition"]["mode"]
    if mode == "lease_replay" and not effects["persistence"]:
        bad("replay_without_persistence", "/repetition/mode")
    if mode == "fresh_observation" and not (effects["external_reads"] and policy["observation_time"]):
        bad("freshness_without_observation", "/repetition/mode")


def check_mapping(tool, bad):
    """Mapping rows: unique, pointing at a real inventory, correctly classified."""
    inventories = tool["outcomes"]["inventories"]
    if {inv["kind"] for inv in inventories} != {"result", "error"}:
        bad("incomplete_inventory_kinds", "/outcomes/inventories")
    seen_rows = set()
    for k, row in enumerate(tool["outcomes"]["mapping"]):
        # The schema's `integer` admits `0.0` and `0e0`, which JSON decodes as floats.
        index = int(row["inventory"])
        pair = (index, row["value"])
        if pair in seen_rows:
            bad("duplicate_outcome", f"/outcomes/mapping/{k}")
        seen_rows.add(pair)
        if index >= len(inventories):
            bad("unknown_inventory", f"/outcomes/mapping/{k}/inventory")
            continue
        error = inventories[index]["kind"] == "error"
        expected = "execution_failure" if error else "completed_evaluation"
        if row["is_error"] != error or row["class"] != expected:
            bad("outcome_classification_mismatch", f"/outcomes/mapping/{k}")


def check_inventories(tool, offline, gap_index, bad):
    """Each inventory resolves to a finite vocabulary the mapping exhausts, or
    carries an outcomes gap; then every union member must be covered."""
    rows = tool["outcomes"]["mapping"]
    placed, pointer_failed = [], set()
    for j, inventory in enumerate(tool["outcomes"]["inventories"]):
        here = f"/outcomes/inventories/{j}"
        role = inventory["schema"]
        if role != ("error" if inventory["kind"] == "error" else "output"):
            bad("inventory_schema_kind_mismatch", here + "/schema")
        key = ref_key(tool[role])
        document = offline.document(key)
        try:
            node, resource = offline.locate(document, inventory["pointer"])
        except Invalid:
            bad("invalid_inventory_pointer", here + "/pointer")
            pointer_failed.add(key)
            continue
        if (key, id(node)) not in offline.reach(key, document, document):
            bad("unreachable_inventory", here + "/pointer")
            continue
        try:
            values = offline.finite(key, node, resource, inventory.get("discriminator"))
        except (TypeError, ValueError):
            bad("invalid_inventory_pointer", here + "/pointer")
            pointer_failed.add(key)
            continue
        gap = inventory["gap_id"]
        placed.append((role, key, (key, id(node)), gap is not None))
        if values is None:
            if gap not in tool["gap_ids"] or "outcomes" not in gap_index.get(gap, {}).get("concerns", []):
                bad("unresolved_inventory_without_gap", here + "/gap_id")
            continue
        if {r["value"] for r in rows if int(r["inventory"]) == j} != values:
            bad("incomplete_outcome_mapping", here)
        if gap is not None:
            bad("resolved_inventory_claims_gap", here + "/gap_id")
    for role in ("error", "output"):
        key = ref_key(tool[role])
        own = {target for placed_role, _, target, _ in placed if placed_role == role}
        if not own or key in pointer_failed:
            continue
        every = {target for _, placed_key, target, _ in placed if placed_key == key}
        gapped = any(has_gap for _, placed_key, _, has_gap in placed if placed_key == key)
        if offline.uncovered_branches(key, own, every, gapped):
            bad("uncovered_outcome_branch", "/" + role)


def check_tool(i, tool, declaration, offline, found):
    path = f"/tools/{i}"

    def bad(code, suffix=""):
        found.add("semantics", code, path + suffix)

    source = declaration["source"]
    if tool["owner"] != declaration["domain"]:
        bad("owner_domain_mismatch", "/owner")
    for name in REFERENCE_FIELDS:
        if (tool[name]["repository"], tool[name]["revision"]) != (source["repository"], source["revision"]):
            bad("tool_schema_outside_source", "/" + name)
    evidence = {r["id"]: r for r in declaration["evidence"]}
    gap_index = {r["id"]: r for r in declaration["gaps"]}
    supported, gap_concerns = check_support(tool, evidence, gap_index, bad)
    check_claims(tool, supported, gap_concerns, bad)
    check_mapping(tool, bad)
    check_inventories(tool, offline, gap_index, bad)


def validate(declaration, snapshots):
    found = Diagnostics()
    check_input(declaration, found)
    if found:
        return report(found, [])
    check_structure(declaration, found)
    if found:
        return report(found, [])
    gaps = declaration["gaps"]
    offline = check_references(declaration, snapshots, found)
    if found:
        return report(found, gaps)
    check_catalog(declaration, found)
    for i, tool in enumerate(declaration["tools"]):
        check_tool(i, tool, declaration, offline, found)
    return report(found, gaps)


def printable(text):
    """Text safe for a terminal line: control, format, separator and unassigned
    characters, and the backslash itself, are escaped; other text is unchanged."""
    out = []
    for char in str(text):
        code = ord(char)
        if char == "\\":
            out.append("\\\\")
        elif unicodedata.category(char) in ("Cc", "Cf", "Cs", "Co", "Cn", "Zl", "Zp"):
            if code < 0x100:
                out.append(f"\\x{code:02x}")
            elif code < 0x10000:
                out.append(f"\\u{code:04x}")
            else:
                out.append(f"\\U{code:08x}")
        else:
            out.append(char)
    return "".join(out)


def parse_snapshots(parser, values):
    roots = {}
    for item in values:
        key, separator, root = item.partition("=")
        repository, at, revision = key.rpartition("@")
        if not separator or not at or not repository or not revision or not root:
            parser.error(f"--snapshot {item!r} is not REPOSITORY@REVISION=ROOT")
        if (repository, revision) in roots:
            parser.error(f"--snapshot names {repository}@{revision} twice")
        roots[(repository, revision)] = Path(root)
    return roots


def read_declaration(path):
    try:
        raw = bounded_read(path, INPUT_LIMIT, "input_size_limit")
    except Invalid as error:
        return None, str(error)
    except OSError:
        return None, "input_unreadable"
    try:
        return json_loads(raw), None
    except Invalid as error:
        return None, str(error)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None, "malformed_json"
    except RecursionError:
        return None, "json_depth_limit"
    except ValueError:
        # Python 3.11+ refuses integers past its digit limit with a plain ValueError.
        return None, "json_number_limit"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("declaration", type=Path)
    parser.add_argument("--snapshot", action="append", default=[], metavar="REPOSITORY@REVISION=ROOT")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    roots = parse_snapshots(parser, args.snapshot)
    declaration, code = read_declaration(args.declaration)
    if code is not None:
        result = report([{"dimension": "structure", "code": code, "location": "/"}], [])
    else:
        result = validate(declaration, roots)
    if args.json:
        print(json.dumps(result, sort_keys=True))
    else:
        print(result["status"] + "; offline declaration checks only; verified conformance: false")
        for dimension, passed in result["checks"].items():
            print(f"{dimension}: {CHECK_STATE[passed]}")
        for diagnostic in result["diagnostics"]:
            print(f"{diagnostic['code']} {printable(diagnostic['location'])}")
        for gap in result["gaps"]:
            print(f"gap {printable(gap['id'])}: {printable(gap['description'])}")
    return result["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
