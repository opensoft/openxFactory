"""Synthetic conformance witnesses; no domain code or network is needed.

Every schema here is SYNTHETIC. Two of them are built in the SHAPE of real
domain schemas the validator must accept (a nested `$id` embedded resource,
and error unions whose codes sit in `properties.code.const` of `oneOf`
branches, reached directly or through `$ref`), because those real schemas live
in private repositories and are never copied into this public one.

Assertions name diagnostic CODES and LOCATIONS, not only the overall status:
the ratified scenario *Malformed catalog* requires stable codes and locations,
and *Deterministic validation* requires stable ordering.
"""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import tracemalloc
import unittest
from unittest.mock import patch
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/validate-factory-mcp.py"
EXAMPLES = ROOT / "contracts/factory-mcp/examples"
DRAFT = "https://json-schema.org/draft/2020-12/schema"
SEMANTIC_IDS = ("binding", "effects", "outcomes", "evidence", "limits", "repetition")


def load():
    spec = importlib.util.spec_from_file_location("factory_mcp", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def diagnostics(report):
    return [(d["code"], d["location"]) for d in report["diagnostics"]]


def everywhere(code, *locations):
    """One code at every listed location, in the report's own sort order."""
    return [(code, location) for location in sorted(locations)]


TOOL_REFS = ("/tools/0/error", "/tools/0/input", "/tools/0/output")
ALL_REFS = ("/evidence/0/source", "/source/artifacts/0") + TOOL_REFS
# Feature 039 (the authorization profile): synthetic names under the reserved `.test` domain.
RESOURCE = "https://mcp.example.test/mcp"
ISSUER = "https://issuer.example.test/synthetic"
WELL_KNOWN = "/.well-known/oauth-protected-resource"


class ConformanceTests(unittest.TestCase):
    def setUp(self):
        # The validator is offline by contract; any in-process socket is a defect.
        blocker = patch("socket.socket", side_effect=AssertionError("network forbidden"))
        blocker.start()
        self.addCleanup(blocker.stop)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.revision = "a" * 40
        self.schema = {"$schema": DRAFT,
                       "type": "object", "properties": {
                           "status": {"enum": ["positive", "negative"]},
                           "code": {"oneOf": [{"const": "UNAVAILABLE"}, {"const": "INVALID"}]}}}
        self.write_schema()
        self.doc = self.declaration()
        self.module = load()

    def put(self, name, obj, root=None, repository="synthetic", revision=None):
        data = json.dumps(obj).encode()
        (root or self.root).joinpath(name).write_bytes(data)
        return {"repository": repository, "revision": revision or self.revision,
                "path": name, "sha256": hashlib.sha256(data).hexdigest()}

    def write_schema(self):
        self.ref = self.put("outcome.json", self.schema)

    def declaration(self):
        tool = {
            "id": "sample_check", "owner": "sample", "input": self.ref.copy(),
            "output": self.ref.copy(), "error": self.ref.copy(),
            "binding": {"authority_source": "trusted_host", "principal": "verified",
                "subject": "host-resolved", "operation": "sample_check", "policy": "host policy",
                "scope_references": ["Hermes installation/stack/layer"], "scope_status": "mapped",
                "revocation": "startup_frozen"},
            "effects": {"authority_effect": "none", "external_reads": False,
                "execution": False, "persistence": False, "mutation": False,
                "boundary": "trusted_host", "execution_bounded": False,
                "execution_host_controlled": False},
            "outcomes": {"structured_content": "verbatim", "inventories": [
                {"kind": "result", "schema": "output", "pointer": "/properties/status", "gap_id": None},
                {"kind": "error", "schema": "error", "pointer": "/properties/code", "gap_id": None}],
                "mapping": [
                    {"inventory": 0, "value": v, "class": "completed_evaluation", "is_error": False}
                    for v in ["positive", "negative"]] + [
                    {"inventory": 1, "value": v, "class": "execution_failure", "is_error": True}
                    for v in ["UNAVAILABLE", "INVALID"]]},
            "evidence_policy": {"input_identity": True, "context_identity": True,
                "evaluation_time": True, "observation_time": False,
                "artifact_provenance": "protected_host_record", "allowed_output": ["bounded status"],
                "raw_credentials": False, "raw_provider_payload": False, "audit": "not_implemented"},
            "repetition": {"mode": "reevaluate", "deadline": "host_monotonic",
                "trace_ids_are_authority": False},
            "limits": {"request_bytes": 262144, "result_bytes": 262144, "boundary": "host"},
            "evidence_ids": ["synthetic-observation"], "gap_ids": ["audit-gap"]}
        return {"schema_version": 1, "kind": "factory_mcp_conformance", "profile": "advisory-v1",
            "domain": "sample", "contract_version": "unreleased",
            "source": {"repository": "synthetic", "revision": self.revision, "artifacts": [self.ref.copy()]},
            "service": {"deployment": "not_deployed"}, "tools": [tool],
            "evidence": [{"id": "synthetic-observation",
                "concerns": ["binding", "effects", "outcomes", "evidence", "repetition", "limits"],
                "source": self.ref.copy(), "summary": "Synthetic declaration consistency only."}],
            "gaps": [{"id": "audit-gap", "concerns": ["audit"], "description": "No resolving audit sink."}]}

    def validate(self, roots=None):
        return self.module.validate(self.doc, roots if roots is not None else
                                    {("synthetic", self.revision): self.root})

    def assertDiagnostics(self, expected, roots=None, status="invalid"):
        report = self.validate(roots)
        self.assertEqual(diagnostics(report), expected)
        self.assertEqual(report["status"], status)
        self.assertFalse(report["verified_conformance"])
        return report

    def assertValidWithGaps(self, roots=None):
        return self.assertDiagnostics([], roots, status="valid-with-gaps")

    def tool(self):
        return self.doc["tools"][0]

    def pin(self, ref):
        """Pin an extra artifact in source.artifacts (a cross-file schema target)."""
        self.doc["source"]["artifacts"].append(dict(ref))

    def cli(self, *args):
        env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                              capture_output=True, text=True, encoding="utf-8", cwd=ROOT, env=env)

    # ---- the core report ---------------------------------------------------

    def test_valid_with_gaps_is_not_certification(self):
        report = self.assertValidWithGaps()
        self.assertEqual(report["checks"], {"structure": True, "references": True, "semantics": True})
        self.assertEqual([g["id"] for g in report["gaps"]], ["audit-gap"])
        self.assertEqual(report["exit_code"], 0)
        self.assertEqual(report, self.validate())

    def test_closed_shapes(self):
        for mutate, expected in [
            (lambda t: t["effects"].update(mutation=True), [("schema_const", "/tools/0/effects/mutation")]),
            (lambda t: t["effects"].update(authority_effect="approve"),
             [("schema_const", "/tools/0/effects/authority_effect")]),
            (lambda t: t["binding"].update(authority_source="caller"),
             [("schema_const", "/tools/0/binding/authority_source")]),
            (lambda t: t["limits"].update(request_bytes=True), [("schema_type", "/tools/0/limits/request_bytes")]),
            (lambda t: t["outcomes"].update(structured_content="wrapped"),
             [("schema_const", "/tools/0/outcomes/structured_content")]),
            (lambda t: t["evidence_policy"].update(raw_credentials=True),
             [("schema_const", "/tools/0/evidence_policy/raw_credentials")]),
            (lambda t: t.update(unrecognized=True), [("schema_additionalProperties", "/tools/0")]),
            (lambda t: t.update(owner="other"), [("owner_domain_mismatch", "/tools/0/owner")]),
        ]:
            with self.subTest(expected=expected):
                self.doc = self.declaration()
                mutate(self.tool())
                self.assertDiagnostics(expected)

    def test_unknown_version_and_missing_concern(self):
        self.doc["schema_version"] = 2
        self.assertDiagnostics([("schema_const", "/schema_version")])
        self.doc = self.declaration()
        del self.tool()["limits"]
        self.assertDiagnostics([("schema_required", "/tools/0")])

    def test_tool_id_is_a_bounded_token(self):
        """L3: a tool id is one MCP-style name token, not free text."""
        for bad in ["bad tool", "line\nbreak", "bidi\u202eoverride", "trailing\n", "x" * 81, ""]:
            with self.subTest(tool_id=bad):
                self.doc = self.declaration()
                self.tool()["id"] = bad
                report = self.validate()
                self.assertEqual(report["status"], "invalid")
                self.assertTrue(diagnostics(report))
                self.assertEqual({location for _, location in diagnostics(report)}, {"/tools/0/id"})
        for good in ["sample_check", "ops.dns-check_2"]:
            with self.subTest(tool_id=good):
                self.doc = self.declaration()
                self.tool()["id"] = good
                self.assertValidWithGaps()

    # ---- outcomes ----------------------------------------------------------

    def test_outcomes_exhaustive_and_typed(self):
        for action, expected in [
            ("missing", [("incomplete_outcome_mapping", "/tools/0/outcomes/inventories/1")]),
            ("extra", [("incomplete_outcome_mapping", "/tools/0/outcomes/inventories/0")]),
            ("duplicate", [("duplicate_outcome", "/tools/0/outcomes/mapping/4")]),
            ("class", [("outcome_classification_mismatch", "/tools/0/outcomes/mapping/3")]),
            ("is_error", [("outcome_classification_mismatch", "/tools/0/outcomes/mapping/3")]),
            ("inventory", [("incomplete_outcome_mapping", "/tools/0/outcomes/inventories/0"),
                           ("unknown_inventory", "/tools/0/outcomes/mapping/0/inventory")]),
            ("kinds", [("incomplete_inventory_kinds", "/tools/0/outcomes/inventories")]),
            ("schema", [("inventory_schema_kind_mismatch", "/tools/0/outcomes/inventories/1/schema")]),
        ]:
            with self.subTest(action=action):
                self.doc = self.declaration()
                outcomes = self.tool()["outcomes"]
                rows = outcomes["mapping"]
                if action == "missing": rows.pop()
                elif action == "extra": rows[0]["value"] = "unrecognized"
                elif action == "duplicate": rows.append(rows[0].copy())
                elif action == "class": rows[-1]["class"] = "completed_evaluation"
                elif action == "is_error": rows[-1]["is_error"] = False
                elif action == "kinds": outcomes["inventories"][1]["kind"] = "result"
                elif action == "schema": outcomes["inventories"][1]["schema"] = "output"
                else: rows[0]["inventory"] = 20
                if action == "kinds":
                    # Both inventories now read as results; the error kind is absent.
                    for row in rows:
                        row["class"], row["is_error"] = "completed_evaluation", False
                    outcomes["inventories"][1]["schema"] = "output"
                self.assertDiagnostics(expected)

    def test_unresolvable_vocabulary_requires_gap(self):
        self.schema["properties"]["status"] = {"type": "string"}
        self.write_schema()
        self.doc = self.declaration()
        self.assertDiagnostics([("unresolved_inventory_without_gap", "/tools/0/outcomes/inventories/0/gap_id")])
        self.doc["gaps"].append({"id": "vocab-gap", "concerns": ["outcomes"], "description": "Not finite."})
        t = self.tool()
        t["gap_ids"].append("vocab-gap")
        t["outcomes"]["inventories"][0]["gap_id"] = "vocab-gap"
        self.assertValidWithGaps()

    def test_resolved_inventory_cannot_claim_a_gap(self):
        self.doc["gaps"].append({"id": "vocab-gap", "concerns": ["outcomes"], "description": "Not needed."})
        self.tool()["gap_ids"].append("vocab-gap")
        self.tool()["outcomes"]["inventories"][0]["gap_id"] = "vocab-gap"
        self.assertDiagnostics([("resolved_inventory_claims_gap", "/tools/0/outcomes/inventories/0/gap_id")])

    def test_object_cardinality_and_name_constraints_do_not_claim_exhaustiveness(self):
        """Review r4189280764: `maxProperties: 0` beside required codes admits no
        object, so the codes cannot be projected; object cardinality and property
        name constraints narrow like any other, and an honest gap is accepted."""
        unresolved = [("unresolved_inventory_without_gap", "/tools/0/outcomes/inventories/1/gap_id")]
        for case, where, constraint in [
                ("maxProperties on the union", "error", {"maxProperties": 0}),
                ("minProperties on a branch", "invalidError", {"minProperties": 9}),
                ("propertyNames on the union", "error", {"propertyNames": {"maxLength": 2}})]:
            with self.subTest(case=case):
                self.doc = self.declaration()
                self.error_union(parent_typed=True)
                error = json.loads((self.root / "domain-error.json").read_text())
                error["$defs"][where].update(constraint)
                ref = self.put("domain-error.json", error)
                self.doc = self.declaration()
                self.pin(ref)
                t = self.tool()
                t["error"] = dict(ref)
                t["outcomes"]["inventories"][1].update(pointer="/$defs/error", discriminator="code")
                self.assertDiagnostics(unresolved)
                self.doc["gaps"].append({"id": "vocab-gap", "concerns": ["outcomes"], "description": "Narrowed."})
                t["gap_ids"].append("vocab-gap")
                t["outcomes"]["inventories"][1]["gap_id"] = "vocab-gap"
                self.assertValidWithGaps()

    def test_closed_schemas_that_exclude_a_required_property_are_unresolved(self):
        """Review 5421267903 (previously missed): `additionalProperties: false`
        admits only the names its own `properties` declares, so a closed union
        with no `properties`, or a closed branch requiring an undeclared name, or
        a required property whose schema is `false`, admits no instance. Valid
        closed branches still resolve."""
        unresolved = [("unresolved_inventory_without_gap", "/tools/0/outcomes/inventories/1/gap_id")]

        def closed_union(error):
            error["$defs"]["error"]["additionalProperties"] = False

        def undeclared_required(error):
            error["$defs"]["invalidError"].update(
                properties={"code": {"const": "INVALID"}}, required=["code", "extra"])

        def false_property(error):
            error["$defs"]["invalidError"]["properties"]["retryable"] = False

        for case, change, expected in [("closed union", closed_union, unresolved),
                                       ("undeclared required name", undeclared_required, unresolved),
                                       ("required property is false", false_property, unresolved),
                                       ("valid closed branches", lambda error: None, [])]:
            with self.subTest(case=case):
                self.doc = self.declaration()
                self.error_union(parent_typed=True)
                error = json.loads((self.root / "domain-error.json").read_text())
                change(error)
                ref = self.put("domain-error.json", error)
                self.doc = self.declaration()
                self.pin(ref)
                t = self.tool()
                t["error"] = dict(ref)
                t["outcomes"]["inventories"][1].update(pointer="/$defs/error", discriminator="code")
                self.assertDiagnostics(expected, status="invalid" if expected else "valid-with-gaps")
                if expected:
                    self.doc["gaps"].append({"id": "vocab-gap", "concerns": ["outcomes"], "description": "Closed."})
                    t["gap_ids"].append("vocab-gap")
                    t["outcomes"]["inventories"][1]["gap_id"] = "vocab-gap"
                    self.assertValidWithGaps()

    def test_unanalyzable_branch_constraints_are_unresolved(self):
        """Review 5421477111: a discriminated projection reads only the keywords it
        understands. Closure reached through `$ref`, a required property that is
        `false` through `$ref` or negated, `dependentRequired`, `unevaluatedProperties`,
        an asserting `additionalProperties` schema, or `properties` on an enclosing
        union leave the inventory unresolved, and an honest gap is accepted."""
        unresolved = [("unresolved_inventory_without_gap", "/tools/0/outcomes/inventories/1/gap_id")]

        def branch(error):
            return error["$defs"]["invalidError"]

        def referenced_closure(error):  # r4189572067
            error["$defs"]["deny"] = False
            branch(error).update(properties={"code": {"const": "INVALID"}}, required=["code", "extra"],
                                 additionalProperties={"$ref": "#/$defs/deny"})

        def referenced_false_property(error):  # r4189572117
            error["$defs"]["deny"] = False
            branch(error)["properties"]["retryable"] = {"$ref": "#/$defs/deny"}

        def negated_property(error):  # r4189572117
            branch(error)["properties"]["retryable"] = {"not": {}}

        def dependent_required(error):  # review body
            branch(error).update(properties={"code": {"const": "INVALID"}}, required=["code"],
                                 dependentRequired={"code": ["extra"]})

        def unevaluated(error):  # review body
            del branch(error)["additionalProperties"]
            branch(error).update(unevaluatedProperties=False, required=["code", "retryable", "details", "extra"])

        def asserting_additional(error):
            branch(error).update(required=["code", "retryable", "details", "extra"],
                                 additionalProperties={"type": "integer"})

        def parent_properties(error):  # review body; open branches, so only the parent forbids `extra`
            error["$defs"]["error"].update(required=["extra"], properties={"extra": False})
            for name in ("unavailableError", "invalidError"):
                del error["$defs"][name]["additionalProperties"]

        def open_additional(error):  # guard: a pure reference to `true` leaves extra names open
            error["$defs"]["anything"] = True
            branch(error).update(required=["code", "retryable", "details", "extra"],
                                 additionalProperties={"$ref": "#/$defs/anything"})

        for case, change, expected in [("referenced closure", referenced_closure, unresolved),
                                       ("referenced false property", referenced_false_property, unresolved),
                                       ("negated property", negated_property, unresolved),
                                       ("dependentRequired", dependent_required, unresolved),
                                       ("unevaluatedProperties", unevaluated, unresolved),
                                       ("asserting additionalProperties", asserting_additional, unresolved),
                                       ("parent properties", parent_properties, unresolved),
                                       ("open additionalProperties", open_additional, [])]:
            with self.subTest(case=case):
                self.doc = self.declaration()
                self.error_union(parent_typed=True)
                error = json.loads((self.root / "domain-error.json").read_text())
                change(error)
                ref = self.put("domain-error.json", error)
                self.doc = self.declaration()
                self.pin(ref)
                t = self.tool()
                t["error"] = dict(ref)
                t["outcomes"]["inventories"][1].update(pointer="/$defs/error", discriminator="code")
                self.assertDiagnostics(expected, status="invalid" if expected else "valid-with-gaps")
                if expected:
                    self.doc["gaps"].append({"id": "vocab-gap", "concerns": ["outcomes"], "description": "Unanalyzed."})
                    t["gap_ids"].append("vocab-gap")
                    t["outcomes"]["inventories"][1]["gap_id"] = "vocab-gap"
                    self.assertValidWithGaps()

    def test_required_property_top_level_contradictions_are_unresolved(self):
        """Review r4189769282: `type`, `const` and `enum` along a required property's
        `$ref` chain apply together; a top-level contradiction holds no value, so
        the branch's code cannot be projected. Compatible combinations resolve."""
        unresolved = [("unresolved_inventory_without_gap", "/tools/0/outcomes/inventories/1/gap_id")]
        defs = {"text": {"type": "string"}, "number": {"type": "number"}}
        for case, schema, expected in [
                ("object const false", {"type": "object", "const": False}, unresolved),
                ("string enum of integers", {"type": "string", "enum": [1, 2]}, unresolved),
                ("const outside enum", {"const": "a", "enum": ["b"]}, unresolved),
                ("empty enum", {"enum": []}, unresolved),
                ("contradiction across a link", {"$ref": "#/$defs/text", "type": "integer"}, unresolved),
                ("boolean is not an integer", {"type": "integer", "const": True}, unresolved),
                ("integral number", {"type": "integer", "const": 1.0}, []),
                ("integer is a number", {"$ref": "#/$defs/number", "type": "integer"}, []),
                ("const inside enum", {"const": "a", "enum": ["a", "b"], "type": ["string", "null"]}, []),
                # Review r4189908933: top-level unions are not analyzed.
                ("top-level oneOf", {"oneOf": [{}, {}]}, unresolved),
                ("top-level anyOf", {"anyOf": [False, False]}, unresolved),
                # Review r4189908956: compound values compare recursively, numbers by value.
                ("nested numbers in an array", {"const": [1], "enum": [[1.0]]}, []),
                ("nested numbers in an object", {"const": {"n": 1}, "enum": [{"n": 1.0}]}, []),
                ("nested boolean is not a number", {"const": [True], "enum": [[1]]}, unresolved)]:
            with self.subTest(case=case):
                self.doc = self.declaration()
                self.error_union(parent_typed=True)
                error = json.loads((self.root / "domain-error.json").read_text())
                error["$defs"].update(defs)
                error["$defs"]["invalidError"]["properties"]["retryable"] = schema
                ref = self.put("domain-error.json", error)
                self.doc = self.declaration()
                self.pin(ref)
                t = self.tool()
                t["error"] = dict(ref)
                t["outcomes"]["inventories"][1].update(pointer="/$defs/error", discriminator="code")
                self.assertDiagnostics(expected, status="invalid" if expected else "valid-with-gaps")

    def test_unsupported_constraints_do_not_claim_exhaustiveness(self):
        self.schema["properties"]["status"]["pattern"] = "^positive$"
        self.write_schema()
        self.doc = self.declaration()
        self.assertDiagnostics([("unresolved_inventory_without_gap", "/tools/0/outcomes/inventories/0/gap_id")])

    def test_pointer_indices_are_strict(self):
        """M1: RFC 6901 array indices are `0` or a digit run without a leading zero."""
        for pointer in ["/properties/code/oneOf/-1", "/properties/code/oneOf/01", "/properties/code/oneOf/+1",
                        "/properties/code/oneOf/1.0", "/properties/code/oneOf/ 1", "/properties/code/oneOf/-",
                        "/properties/~2code", "properties/code"]:
            with self.subTest(pointer=pointer):
                self.doc = self.declaration()
                t = self.tool()
                t["outcomes"]["inventories"][1]["pointer"] = pointer
                t["outcomes"]["mapping"] = [r for r in t["outcomes"]["mapping"] if r["value"] != "UNAVAILABLE"]
                self.assertDiagnostics([("invalid_inventory_pointer", "/tools/0/outcomes/inventories/1/pointer")])

    def test_one_member_of_a_union_does_not_cover_the_union(self):
        """M1: an inventory inside ONE union member leaves the others unmapped."""
        # A valid index selecting one constant of the error-code union.
        t = self.tool()
        t["outcomes"]["inventories"][1]["pointer"] = "/properties/code/oneOf/1"
        t["outcomes"]["mapping"] = [r for r in t["outcomes"]["mapping"] if r["value"] != "UNAVAILABLE"]
        self.assertDiagnostics([("uncovered_outcome_branch", "/tools/0/error")])

    def test_every_result_variant_is_covered(self):
        """M1: one inventory per variant covers the union; one variant alone does not."""
        union = {"$schema": DRAFT, "oneOf": [
            {"type": "object", "properties": {"status": {"enum": ["positive", "negative"]}}},
            {"type": "object", "properties": {"status": {"enum": ["stale", "unreadable"]}}}]}
        ref = self.put("union.json", union)
        self.pin(ref)
        t = self.tool()
        t["output"] = dict(ref)
        t["outcomes"]["inventories"][0]["pointer"] = "/oneOf/0/properties/status"
        self.assertDiagnostics([("uncovered_outcome_branch", "/tools/0/output")])
        t["outcomes"]["inventories"].append(
            {"kind": "result", "schema": "output", "pointer": "/oneOf/1/properties/status", "gap_id": None})
        t["outcomes"]["mapping"] += [
            {"inventory": 2, "value": v, "class": "completed_evaluation", "is_error": False}
            for v in ("stale", "unreadable")]
        self.assertValidWithGaps()

    def test_a_definition_reached_only_through_one_variant_does_not_cover_the_union(self):
        """M1: pointing into `$defs` cannot step around a union of `$ref` variants."""
        union = {"$schema": DRAFT,
                 "$defs": {"inspect": {"type": "object", "properties": {"status": {"enum": ["positive"]}}},
                           "verify": {"type": "object", "properties": {"status": {"enum": ["stale"]}}}},
                 "oneOf": [{"$ref": "#/$defs/inspect"}, {"$ref": "#/$defs/verify"}]}
        ref = self.put("defs-union.json", union)
        self.pin(ref)
        t = self.tool()
        t["output"] = dict(ref)
        t["outcomes"]["inventories"][0]["pointer"] = "/$defs/inspect/properties/status"
        t["outcomes"]["mapping"] = [r for r in t["outcomes"]["mapping"] if r["value"] != "negative"]
        self.assertDiagnostics([("uncovered_outcome_branch", "/tools/0/output")])

    def test_a_definition_shared_by_every_variant_covers_the_union(self):
        """A codex-shaped result: two inline variants share one `$defs` classification enum."""
        result = {"$schema": DRAFT, "$id": "https://synthetic.invalid/schemas/result.json",
                  "$defs": {"classification": {"enum": ["positive", "negative"]},
                            "identifier": {"type": "string"}},
                  "oneOf": [
                      {"type": "object", "additionalProperties": False,
                       "required": ["result_type", "classification"],
                       "properties": {"result_type": {"const": "inspect"},
                                      "classification": {"$ref": "#/$defs/classification"}}},
                      {"type": "object", "additionalProperties": False,
                       "required": ["result_type", "classification", "operation_id"],
                       "properties": {"result_type": {"const": "verify"},
                                      "classification": {"$ref": "#/$defs/classification"},
                                      "operation_id": {"$ref": "#/$defs/identifier"}}}]}
        ref = self.put("result.json", result)
        self.pin(ref)
        t = self.tool()
        t["output"] = dict(ref)
        t["outcomes"]["inventories"][0]["pointer"] = "/$defs/classification"
        self.assertValidWithGaps()

    def test_one_file_with_result_and_error_variants_is_covered_by_both(self):
        """A single outcome file `oneOf: [result, error]` cited as output AND error."""
        outcome = {"$schema": DRAFT, "oneOf": [
            {"type": "object", "properties": {"status": {"enum": ["positive", "negative"]}}},
            {"type": "object", "properties": {"code": {"enum": ["UNAVAILABLE", "INVALID"]}}}]}
        ref = self.put("combined.json", outcome)
        self.pin(ref)
        t = self.tool()
        t["output"], t["error"] = dict(ref), dict(ref)
        t["outcomes"]["inventories"][0]["pointer"] = "/oneOf/0/properties/status"
        t["outcomes"]["inventories"][1]["pointer"] = "/oneOf/1/properties/code"
        self.assertValidWithGaps()

    def test_an_inventory_must_be_reachable_from_its_schema(self):
        """Review r4187464441: an unused definition cannot stand in for the outcome."""
        union = {"$schema": DRAFT,
                 "$defs": {"unused": {"enum": ["positive", "negative"]}},
                 "oneOf": [{"type": "object", "properties": {"status": {"const": "stale"}}},
                           {"type": "object", "properties": {"status": {"const": "unreadable"}}}]}
        ref = self.put("unused-def.json", union)
        self.pin(ref)
        t = self.tool()
        t["output"] = dict(ref)
        t["outcomes"]["inventories"][0]["pointer"] = "/$defs/unused"
        self.assertDiagnostics([("unreachable_inventory", "/tools/0/outcomes/inventories/0/pointer")])

    def test_boolean_inventories_are_located_by_place(self):
        """Review r4187849211: `true` is one Python object everywhere, so a boolean
        schema is known by where it sits; a reachable one needs only an outcomes gap."""
        referenced = {"$ref": "#/$defs/used"}
        for case, status, defs, pointer, expected in [
                ("inline", True, {}, "/properties/status", []),
                ("referenced", referenced, {"used": True, "unused": True}, "/$defs/used", []),
                ("unused", referenced, {"used": True, "unused": True}, "/$defs/unused",
                 [("unreachable_inventory", "/tools/0/outcomes/inventories/0/pointer")])]:
            with self.subTest(case=case):
                self.schema = {"$schema": DRAFT, "type": "object", "$defs": defs, "properties": {
                    "status": status, "code": {"oneOf": [{"const": "UNAVAILABLE"}, {"const": "INVALID"}]}}}
                self.write_schema()
                self.doc = self.declaration()
                t = self.tool()
                t["outcomes"]["inventories"][0]["pointer"] = pointer
                if not expected:
                    self.assertDiagnostics(
                        [("unresolved_inventory_without_gap", "/tools/0/outcomes/inventories/0/gap_id")])
                self.doc["gaps"].append({"id": "vocab-gap", "concerns": ["outcomes"], "description": "Unbounded."})
                t["gap_ids"].append("vocab-gap")
                t["outcomes"]["inventories"][0]["gap_id"] = "vocab-gap"
                self.assertDiagnostics(expected, status="invalid" if expected else "valid-with-gaps")

    def test_a_reference_to_false_is_an_empty_member(self):
        """Review r4187849259: a member reaching `false` through `$ref` admits no
        instance, since a `$ref` applies beside its siblings; a cycle is not `false`."""
        variant = {"type": "object", "properties": {"status": {"enum": ["positive", "negative"]}}}
        for case, defs, member, expected in [
                ("direct", {"disabled": False}, {"$ref": "#/$defs/disabled"}, []),
                ("chained", {"disabled": False, "off": {"$ref": "#/$defs/disabled"}}, {"$ref": "#/$defs/off"}, []),
                ("beside siblings", {"disabled": False}, {"$ref": "#/$defs/disabled", "type": "object"}, []),
                ("cycle", {"loop": {"$ref": "#/$defs/loop"}}, {"$ref": "#/$defs/loop"},
                 [("uncovered_outcome_branch", "/tools/0/output")])]:
            with self.subTest(case=case):
                self.doc = self.declaration()
                ref = self.put("false-member.json", {"$schema": DRAFT, "$defs": defs, "oneOf": [variant, member]})
                self.pin(ref)
                t = self.tool()
                t["output"] = dict(ref)
                t["outcomes"]["inventories"][0]["pointer"] = "/oneOf/0/properties/status"
                self.assertDiagnostics(expected, status="invalid" if expected else "valid-with-gaps")

    def test_a_reference_only_chain_to_true_is_an_open_member(self):
        """Review r4188149120: `{"$ref": "#/$defs/open"}` with `open: true`, through
        annotation-only links, admits anything exactly as a literal `true` does, so
        a declared outcomes gap on the file answers it. A constraining sibling or
        a cycle leaves the member bare, and an inventory on the target holds it."""
        variant = {"type": "object", "properties": {"status": {"enum": ["positive", "negative"]}}}
        uncovered = [("uncovered_outcome_branch", "/tools/0/output")]
        cases = [
            ("literal true", {}, True, uncovered, []),
            ("reference", {"open": True}, {"$ref": "#/$defs/open"}, uncovered, []),
            ("chained with annotations", {"open": True, "alias": {"$ref": "#/$defs/open", "description": "any"}},
             {"$ref": "#/$defs/alias", "title": "anything"}, uncovered, []),
            # Review 5421477111: core metadata and storage assert nothing either.
            ("embedded resource", {}, {"$id": "https://synthetic.invalid/open-member.json",
                                       "$defs": {"open": True}, "$ref": "#/$defs/open"}, uncovered, []),
            ("constraining sibling", {"open": True}, {"$ref": "#/$defs/open", "type": "object"}, uncovered, uncovered),
            ("constraining link", {"open": True, "alias": {"$ref": "#/$defs/open", "minProperties": 1}},
             {"$ref": "#/$defs/alias"}, uncovered, uncovered),
            ("cycle", {"loop": {"$ref": "#/$defs/loop"}}, {"$ref": "#/$defs/loop"}, uncovered, uncovered)]
        for case, defs, member, without_gap, with_gap in cases:
            for gapped, expected in ((False, without_gap), (True, with_gap)):
                with self.subTest(case=case, gapped=gapped):
                    self.doc = self.declaration()
                    ref = self.put("open-member.json", {"$schema": DRAFT, "$defs": defs, "oneOf": [variant, member]})
                    self.pin(ref)
                    t = self.tool()
                    t["output"] = dict(ref)
                    t["outcomes"]["inventories"][0]["pointer"] = "/oneOf/0/properties/status"
                    if gapped:
                        self.doc["gaps"].append({"id": "vocab-gap", "concerns": ["outcomes"],
                                                 "description": "The open member is unbounded."})
                        t["gap_ids"].append("vocab-gap")
                        t["outcomes"]["inventories"].append(
                            {"kind": "result", "schema": "output", "pointer": "", "gap_id": "vocab-gap"})
                    self.assertDiagnostics(expected, status="invalid" if expected else "valid-with-gaps")
        # An inventory on the `true` target holds the member before it is judged open.
        self.doc = self.declaration()
        ref = self.put("open-member.json", {"$schema": DRAFT, "$defs": {"open": True},
                                            "oneOf": [variant, {"$ref": "#/$defs/open"}]})
        self.pin(ref)
        t = self.tool()
        t["output"] = dict(ref)
        t["outcomes"]["inventories"][0]["pointer"] = "/oneOf/0/properties/status"
        self.doc["gaps"].append({"id": "vocab-gap", "concerns": ["outcomes"], "description": "Unbounded."})
        t["gap_ids"].append("vocab-gap")
        t["outcomes"]["inventories"].append(
            {"kind": "result", "schema": "output", "pointer": "/$defs/open", "gap_id": "vocab-gap"})
        self.assertValidWithGaps()

    def test_conditional_branches_are_not_outcome_locations(self):
        """Review r4189769221: `then` and `else` apply only beside an `if`, and
        conditional coverage is not modeled, so neither is an outcome location; the
        reference walk still enters them."""
        stale = {"const": "stale"}
        listed = {"properties": {"status": {"enum": ["positive", "negative"]}}}
        unreachable = [("unreachable_inventory", "/tools/0/outcomes/inventories/0/pointer")]
        for case, extra in [("then without if", {"then": listed}),
                            ("if, then and else", {"if": {"required": ["code"]}, "then": listed,
                                                   "else": {"properties": {"status": stale}}})]:
            with self.subTest(case=case):
                self.schema = {"$schema": DRAFT, "type": "object", "properties": {
                    "status": stale, "code": {"oneOf": [{"const": "UNAVAILABLE"}, {"const": "INVALID"}]}}, **extra}
                self.write_schema()
                self.doc = self.declaration()
                self.tool()["outcomes"]["inventories"][0]["pointer"] = "/then/properties/status"
                self.assertDiagnostics(unreachable)
        self.schema = {"$schema": DRAFT, "type": "object", "properties": {
            "status": {"enum": ["positive", "negative"]},
            "code": {"oneOf": [{"const": "UNAVAILABLE"}, {"const": "INVALID"}]}},
            "then": {"$ref": "https://invalid.test/hidden.json"}}
        self.write_schema()
        self.doc = self.declaration()
        self.assertDiagnostics(everywhere("remote_or_unsafe_schema_reference", *TOOL_REFS))

    def test_negated_definitions_do_not_cover_a_variant(self):
        """Review r4187464328: a `$ref` under `not` is not where an outcome lives."""
        union = {"$schema": DRAFT,
                 "$defs": {"status": {"enum": ["positive", "negative"]}},
                 "oneOf": [{"type": "object", "properties": {"status": {"$ref": "#/$defs/status"}}},
                           {"type": "object", "properties": {"status": {
                               "const": "stale", "not": {"$ref": "#/$defs/status"}}}}]}
        ref = self.put("negated.json", union)
        self.pin(ref)
        t = self.tool()
        t["output"] = dict(ref)
        t["outcomes"]["inventories"][0]["pointer"] = "/$defs/status"
        self.assertDiagnostics([("uncovered_outcome_branch", "/tools/0/output")])

    def test_simultaneous_unions_are_unresolved(self):
        """Review r4187464246: `oneOf` and `anyOf` on one node both constrain it."""
        self.schema["properties"]["status"] = {
            "oneOf": [{"const": "positive"}, {"const": "negative"}], "anyOf": [{"const": "positive"}]}
        self.write_schema()
        self.doc = self.declaration()
        self.assertDiagnostics([("unresolved_inventory_without_gap", "/tools/0/outcomes/inventories/0/gap_id")])
        self.schema["properties"]["status"] = {"enum": ["positive", "negative"]}
        self.write_schema()
        self.doc = self.declaration()
        self.error_union()
        error = json.loads((self.root / "domain-error.json").read_text())
        error["$defs"]["error"]["anyOf"] = [{"$ref": "#/$defs/invalidError"}]
        ref = self.put("domain-error.json", error)
        self.doc = self.declaration()
        self.pin(ref)
        self.tool()["error"] = dict(ref)
        self.tool()["outcomes"]["inventories"][1].update(pointer="/$defs/error", discriminator="code")
        self.assertDiagnostics([("unresolved_inventory_without_gap", "/tools/0/outcomes/inventories/1/gap_id")])

    def test_one_of_values_count_only_once(self):
        """Review r4187464294: under `oneOf` a value valid in two branches is invalid."""
        self.schema["properties"]["status"] = {"oneOf": [{"const": "positive"},
                                                         {"enum": ["positive", "negative"]}]}
        self.write_schema()
        self.doc = self.declaration()
        self.assertDiagnostics([("incomplete_outcome_mapping", "/tools/0/outcomes/inventories/0")])
        t = self.tool()
        t["outcomes"]["mapping"] = [r for r in t["outcomes"]["mapping"] if r["value"] != "positive"]
        self.assertValidWithGaps()

    def test_value_vocabulary_respects_type_and_mixed_keywords(self):
        for status in [{"type": "integer", "enum": ["positive", "negative"]},
                       {"enum": ["positive", "negative"], "oneOf": [{"const": "positive"}]}]:
            with self.subTest(status=status):
                self.schema["properties"]["status"] = status
                self.write_schema()
                self.doc = self.declaration()
                self.assertDiagnostics(
                    [("unresolved_inventory_without_gap", "/tools/0/outcomes/inventories/0/gap_id")])

    def test_type_is_checked_before_references_and_unions(self):
        """Review r4187668945: a `type` beside a `$ref` or a union constrains it."""
        self.schema["$defs"] = {"status": {"enum": ["positive", "negative"]}}
        self.schema["properties"]["status"] = {"$ref": "#/$defs/status", "type": "integer"}
        self.write_schema()
        self.doc = self.declaration()
        self.assertDiagnostics([("unresolved_inventory_without_gap", "/tools/0/outcomes/inventories/0/gap_id")])
        self.schema = {"$schema": DRAFT, "type": "object", "properties": {
            "status": {"enum": ["positive", "negative"]},
            "code": {"oneOf": [{"const": "UNAVAILABLE"}, {"const": "INVALID"}]}}}
        self.write_schema()
        self.doc = self.declaration()
        self.error_union()
        error = json.loads((self.root / "domain-error.json").read_text())
        error["$defs"]["error"]["type"] = "string"
        ref = self.put("domain-error.json", error)
        self.doc = self.declaration()
        self.pin(ref)
        self.tool()["error"] = dict(ref)
        self.tool()["outcomes"]["inventories"][1].update(pointer="/$defs/error", discriminator="code")
        self.assertDiagnostics([("unresolved_inventory_without_gap", "/tools/0/outcomes/inventories/1/gap_id")])

    def test_inventory_target_is_checked_before_projection(self):
        """Review r4187669106: malformed data where no evaluator looks never reaches projection."""
        self.schema["properties"]["pair"] = {"type": "array", "additionalItems": {"required": [{}], "enum": ["x"]}}
        self.schema["examples"] = [{"required": [{}]}]
        self.write_schema()
        for pointer, code in [("/properties/pair/additionalItems", "unreachable_inventory"),
                              ("/examples/0", "invalid_inventory_pointer")]:
            with self.subTest(pointer=pointer):
                self.doc = self.declaration()
                self.tool()["outcomes"]["inventories"][0]["pointer"] = pointer
                self.assertDiagnostics([(code, "/tools/0/outcomes/inventories/0/pointer")])

    def test_integral_float_inventory_indexes(self):
        """Review r4187464393: JSON `0.0` and `0e0` are integers to the schema."""
        rows = self.tool()["outcomes"]["mapping"]
        rows[0]["inventory"] = json.loads("0.0")
        rows[2]["inventory"] = json.loads("1e0")
        self.assertValidWithGaps()

    # ---- H3: outcome inventories across union branches ---------------------

    def error_union(self, name="domain-error.json", *, required_code=True, typed=True, parent_typed=False):
        """Codex-shaped: a root object whose `error` is a `$ref` to a `oneOf` of `$ref`
        branches, each an object carrying its code in `properties.code.const`."""
        def branch(code, retryable):
            return {**({"type": "object"} if typed else {}), "additionalProperties": False,
                    "required": ["code", "retryable", "details"] if required_code else ["retryable", "details"],
                    "properties": {"code": {"const": code}, "retryable": {"const": retryable},
                                   "details": {"type": "object"}}}
        schema = {"$schema": DRAFT, "$id": "https://synthetic.invalid/schemas/domain-error.json",
                  "type": "object", "required": ["error"], "additionalProperties": False,
                  "properties": {"error": {"$ref": "#/$defs/error"},
                                 "tool_id": {"oneOf": [{"$ref": "#/$defs/identifier"}, {"type": "null"}]}},
                  "$defs": {"identifier": {"type": "string"},
                            "unavailableError": branch("UNAVAILABLE", True),
                            "invalidError": branch("INVALID", False),
                            "error": {**({"type": "object"} if parent_typed else {}),
                                      "oneOf": [{"$ref": "#/$defs/unavailableError"},
                                                {"$ref": "#/$defs/invalidError"}]}}}
        ref = self.put(name, schema)
        self.pin(ref)
        self.tool()["error"] = dict(ref)
        return ref

    def test_codex_shaped_error_union_needs_a_discriminator(self):
        self.error_union()
        self.tool()["outcomes"]["inventories"][1]["pointer"] = "/$defs/error"
        self.assertDiagnostics([("unresolved_inventory_without_gap", "/tools/0/outcomes/inventories/1/gap_id")])

    def test_codex_shaped_error_union_resolves_by_discriminator(self):
        self.error_union()
        for pointer in ["/$defs/error", "/properties/error"]:
            with self.subTest(pointer=pointer):
                inventory = self.tool()["outcomes"]["inventories"][1]
                inventory["pointer"], inventory["discriminator"] = pointer, "code"
                self.assertValidWithGaps()

    def test_discriminated_union_is_still_exhaustive(self):
        self.error_union()
        t = self.tool()
        t["outcomes"]["inventories"][1].update(pointer="/$defs/error", discriminator="code")
        t["outcomes"]["mapping"] = [r for r in t["outcomes"]["mapping"] if r["value"] != "INVALID"]
        self.assertDiagnostics([("incomplete_outcome_mapping", "/tools/0/outcomes/inventories/1")])

    def test_discriminator_must_be_a_required_string_constant(self):
        for case in ["not_required", "boolean_values", "absent_property"]:
            with self.subTest(case=case):
                self.doc = self.declaration()
                self.error_union(required_code=case != "not_required")
                inventory = self.tool()["outcomes"]["inventories"][1]
                inventory["pointer"] = "/$defs/error"
                inventory["discriminator"] = {"boolean_values": "retryable",
                                              "absent_property": "missing"}.get(case, "code")
                self.assertDiagnostics(
                    [("unresolved_inventory_without_gap", "/tools/0/outcomes/inventories/1/gap_id")])

    def test_discriminated_branches_must_be_object_only(self):
        """Review r4187574996: an untyped branch also admits `null`, which has no code."""
        for typed, parent_typed, expected in [
                (False, False, [("unresolved_inventory_without_gap", "/tools/0/outcomes/inventories/1/gap_id")]),
                (False, True, [])]:
            with self.subTest(typed=typed, parent_typed=parent_typed):
                self.doc = self.declaration()
                self.error_union(typed=typed, parent_typed=parent_typed)
                self.tool()["outcomes"]["inventories"][1].update(pointer="/$defs/error", discriminator="code")
                self.assertDiagnostics(expected, status="invalid" if expected else "valid-with-gaps")

    def test_ops_shaped_root_error_union_resolves_by_discriminator(self):
        """Ops-shaped: the root is a `oneOf` of inline objects with a constant `code`."""
        def branch(code):
            return {"type": "object", "additionalProperties": False,
                    "required": ["schema_version", "code", "message"],
                    "properties": {"schema_version": {"const": 1}, "code": {"const": code},
                                   "message": {"const": f"{code.lower()} message"}}}
        ref = self.put("ops-error.json", {"$schema": DRAFT,
                                          "oneOf": [branch("UNAVAILABLE"), branch("INVALID")]})
        self.pin(ref)
        t = self.tool()
        t["error"] = dict(ref)
        t["outcomes"]["inventories"][1].update(pointer="", discriminator="code")
        self.assertValidWithGaps()
        del t["outcomes"]["inventories"][1]["discriminator"]
        self.assertDiagnostics([("unresolved_inventory_without_gap", "/tools/0/outcomes/inventories/1/gap_id")])

    def test_one_of_branches_sharing_a_code_are_unresolved(self):
        """Review r4187749559: an object matching two `oneOf` branches matches none,
        and object branches can share a code while differing elsewhere, so a shared
        code cannot be proved to be an outcome. Under `anyOf` it still can."""
        unresolved = [("unresolved_inventory_without_gap", "/tools/0/outcomes/inventories/1/gap_id")]
        for keyword, members, expected in [
                ("oneOf", ["invalidError", "invalidError"], unresolved),
                ("oneOf", ["unavailableError", "invalidError", "invalidTwin"], unresolved),
                ("anyOf", ["unavailableError", "invalidError", "invalidTwin"], [])]:
            with self.subTest(keyword=keyword, members=members):
                self.doc = self.declaration()
                self.error_union()
                error = json.loads((self.root / "domain-error.json").read_text())
                twin = copy.deepcopy(error["$defs"]["invalidError"])
                twin["properties"]["retryable"] = {"const": True}
                error["$defs"]["invalidTwin"] = twin
                error["$defs"]["error"] = {keyword: [{"$ref": f"#/$defs/{name}"} for name in members]}
                ref = self.put("domain-error.json", error)
                self.doc = self.declaration()
                self.pin(ref)
                t = self.tool()
                t["error"] = dict(ref)
                t["outcomes"]["inventories"][1].update(pointer="/$defs/error", discriminator="code")
                if "unavailableError" not in members:
                    t["outcomes"]["mapping"] = [r for r in t["outcomes"]["mapping"] if r["value"] != "UNAVAILABLE"]
                self.assertDiagnostics(expected, status="invalid" if expected else "valid-with-gaps")

    # ---- H2: embedded schema resources -------------------------------------

    def request_schema(self, extra=None):
        """Codex-shaped request: a root `$id`, and a `$defs` entry that is an
        EMBEDDED RESOURCE with its own absolute `$id`, referenced by fragment."""
        embedded = {"$id": "https://synthetic.invalid/schemas/embedded-result.json",
                    "type": "object", "additionalProperties": False,
                    "required": ["schema_version", "kind", "result"],
                    "$defs": {"digest": {"type": "string", "pattern": "^[0-9a-f]{64}$"}},
                    "properties": {"schema_version": {"const": 1}, "kind": {"const": "worker_result"},
                                   "result": {"type": "object", "properties": {
                                       "digest": {"$ref": "#/$defs/digest"},
                                       "files": {"type": "array", "items": {"type": "string"}}}}}}
        if extra:
            embedded["properties"]["extra"] = extra
        variant = lambda tool_id, extra_props: {
            "type": "object", "additionalProperties": False,
            "properties": {"tool_id": {"const": tool_id}, "request_id": {"$ref": "#/$defs/identifier"},
                           "worker_result": {"$ref": "#/$defs/embeddedResult"}, **extra_props}}
        schema = {"$schema": DRAFT, "$id": "https://synthetic.invalid/schemas/request.json",
                  "$defs": {"identifier": {"type": "string"}, "embeddedResult": embedded},
                  "oneOf": [variant("sample_inspect", {}),
                            variant("sample_verify", {"idempotency_key": {"$ref": "#/$defs/identifier"}})]}
        ref = self.put("request.json", schema)
        self.pin(ref)
        self.tool()["input"] = dict(ref)

    def test_embedded_resource_with_nested_id_is_accepted(self):
        self.request_schema()
        self.assertValidWithGaps()

    def test_fragment_inside_embedded_resource_resolves_against_that_resource(self):
        # `#/$defs/identifier` exists only at the DOCUMENT root; inside the embedded
        # resource the fragment resolves against the embedded resource, as JSON
        # Schema 2020-12 requires, so it does not resolve.
        self.request_schema(extra={"$ref": "#/$defs/identifier"})
        self.assertDiagnostics([("unresolved_pointer", "/tools/0/input")])

    def test_relative_reference_inside_embedded_resource_is_refused(self):
        sibling = self.put("other.json", {"$schema": DRAFT, "type": "string"})
        self.pin(sibling)
        self.request_schema(extra={"$ref": "other.json"})
        self.assertDiagnostics([("relative_reference_in_embedded_resource", "/tools/0/input")])

    def test_relative_reference_under_a_root_base_uri_is_refused(self):
        sibling = self.put("other.json", {"$schema": DRAFT, "type": "string"})
        self.pin(sibling)
        ref = self.put("based.json", {"$schema": DRAFT, "$id": "https://synthetic.invalid/based.json",
                                      "properties": {"x": {"$ref": "other.json"}}})
        self.pin(ref)
        self.tool()["input"] = dict(ref)
        self.assertDiagnostics([("unsupported_schema_base_uri", "/tools/0/input")])

    def test_local_fragments_may_carry_uri_characters(self):
        """Review 5421899020 (previously missed): `:`, `?` and percent escapes in a
        `$ref` FRAGMENT select keys in a loaded schema; the fragment is strictly
        percent-decoded, while the path keeps its restrictions."""
        self.schema["$defs"] = {"status:legacy": {"enum": ["a"]}, "status?legacy": {"enum": ["b"]},
                                "status legacy": {"enum": ["c"]}}
        for ref, expected in [("#/$defs/status:legacy", None), ("#/$defs/status?legacy", None),
                              ("#/$defs/status%20legacy", None),
                              # Review r4191064701: decode before telling a pointer from an anchor.
                              ("#%2F$defs%2Fstatus%20legacy", None),
                              ("#/$defs/status%2", "invalid_pointer"), ("#/$defs/status%ZZlegacy", "invalid_pointer"),
                              ("#/$defs/status%FFlegacy", "invalid_pointer"),
                              ("other:file.json#/$defs/x", "remote_or_unsafe_schema_reference"),
                              ("a%2E%2E.json#/x", "remote_or_unsafe_schema_reference"),
                              ("x?y.json#/x", "remote_or_unsafe_schema_reference"),
                              ("#/$defs/a#b", "remote_or_unsafe_schema_reference")]:
            with self.subTest(ref=ref):
                self.schema["properties"]["nested"] = {"$ref": ref}
                self.write_schema()
                self.doc = self.declaration()
                if expected:
                    self.assertDiagnostics(everywhere(expected, *TOOL_REFS))
                else:
                    self.assertValidWithGaps()

    def test_dynamic_references_and_named_anchors_are_refused(self):
        for node, code in [({"$dynamicRef": "#meta"}, "unsupported_dynamic_reference"),
                           ({"$ref": "#named"}, "unsupported_schema_anchor")]:
            with self.subTest(code=code):
                self.schema = copy.deepcopy(self.schema)
                self.schema["properties"]["nested"] = node
                self.write_schema()
                self.doc = self.declaration()
                self.assertDiagnostics(everywhere(code, *TOOL_REFS))

    # ---- references --------------------------------------------------------

    def test_reference_integrity(self):
        (self.root / "subdir").mkdir()
        for bad, code in [("/tmp/outcome.json", "unsafe_reference_path"),
                          ("../outcome.json", "unsafe_reference_path"),
                          ("https://invalid.test/s.json", "unsafe_reference_path"),
                          ("./outcome.json", "unsafe_reference_path"),
                          ("absent.json", "missing_artifact"),
                          ("subdir", "reference_not_a_file")]:
            with self.subTest(path=bad):
                self.doc = self.declaration()
                self.tool()["input"]["path"] = bad
                self.assertDiagnostics([(code, "/tools/0/input")])

    def test_digest_mismatch(self):
        """M7: every citation of the file carries the same WRONG digest."""
        wrong = "0" * 64
        self.doc["source"]["artifacts"][0]["sha256"] = wrong
        self.doc["evidence"][0]["source"]["sha256"] = wrong
        for name in ("input", "output", "error"):
            self.tool()[name]["sha256"] = wrong
        self.assertDiagnostics(everywhere("digest_mismatch", *ALL_REFS))

    def test_conflicting_digests_for_one_file(self):
        self.tool()["input"]["sha256"] = "0" * 64
        self.assertDiagnostics([("conflicting_digest", "/tools/0/input")])

    def test_unavailable_snapshot(self):
        report = self.assertDiagnostics(everywhere("snapshot_unavailable", *ALL_REFS), roots={})
        self.assertEqual(report["exit_code"], 2)
        self.assertEqual(report["checks"], {"structure": True, "references": False, "semantics": None})

    def test_oversized_artifact(self):
        self.schema["description"] = "x" * (self.module.ARTIFACT_LIMIT + 1)
        self.write_schema()
        self.doc = self.declaration()
        self.assertDiagnostics(everywhere("artifact_size_limit", *ALL_REFS))

    def test_malformed_and_invalid_schema_files(self):
        for raw, code in [(b"{", "malformed_schema_json"),
                          (b'{"type": "object", "type": "string"}', "duplicate_json_key"),
                          (b'{"type": 7}', "invalid_json_schema")]:
            with self.subTest(code=code, raw=raw):
                (self.root / "outcome.json").write_bytes(raw)
                self.ref = {**self.ref, "sha256": hashlib.sha256(raw).hexdigest()}
                self.doc = self.declaration()
                self.assertDiagnostics(everywhere(code, *TOOL_REFS))

    def test_schema_depth_limit(self):
        node = {"enum": ["positive", "negative"]}
        for _ in range(140):
            node = {"type": "object", "properties": {"deeper": node}}
        self.schema["properties"]["deep"] = node
        self.write_schema()
        self.doc = self.declaration()
        self.assertDiagnostics(everywhere("schema_depth_limit", *TOOL_REFS))

    def test_cumulative_schema_bytes_are_bounded(self):
        """Review r4189908880: each artifact is within its own bound, but together
        the parsed schemas would be retained for the whole run, so the total
        loaded is bounded too, before another document is parsed."""
        filler = "x" * (self.module.ARTIFACT_LIMIT - 4096)
        names = []
        for i in range(6):
            ref = self.put(f"big{i}.json", {"$schema": DRAFT, "description": filler})
            self.pin(ref)
            names.append(ref["path"])
        self.schema["properties"]["big"] = {"allOf": [{"$ref": name} for name in names]}
        self.write_schema()
        self.doc["source"]["artifacts"][0] = self.ref.copy()
        for name in ("input", "output", "error"):
            self.tool()[name] = self.ref.copy()
        self.doc["evidence"][0]["source"] = self.ref.copy()
        self.assertDiagnostics(everywhere("schema_total_size_limit", *TOOL_REFS))
        del self.schema["properties"]["big"]
        self.schema["properties"]["two"] = {"allOf": [{"$ref": name} for name in names[:2]]}
        self.write_schema()
        self.doc["source"]["artifacts"][0] = self.ref.copy()
        for name in ("input", "output", "error"):
            self.tool()[name] = self.ref.copy()
        self.doc["evidence"][0]["source"] = self.ref.copy()
        self.assertValidWithGaps()

    def test_symlink_loop_is_refused_not_raised(self):
        """Review r4187464151: a symlink loop is a refusal, never a crash."""
        (self.root / "loop.json").symlink_to(self.root / "loop.json")
        self.tool()["input"]["path"] = "loop.json"
        self.assertDiagnostics([("unsafe_reference_path", "/tools/0/input")])

    def test_references_must_target_schemas(self):
        """Review r4187464184: a `$ref` into annotation data is not a schema."""
        for target, extra, code in [
                ("#/examples/0", {"examples": [{"type": 7}]}, "reference_to_non_schema"),
                ("#/examples/0", {"examples": [{"enum": ["positive"]}]}, "reference_to_non_schema"),
                ("#/properties", {}, "reference_to_non_schema"),
                ("#/$defs/pair/additionalItems",
                 {"$defs": {"pair": {"type": "array", "additionalItems": {"type": 7}}}},
                 "invalid_referenced_schema"),
                ("#/required", {"required": ["status"]}, "reference_to_non_schema"),
                ("#/properties/status/enum", {}, "reference_to_non_schema")]:
            with self.subTest(target=target):
                self.schema = {"$schema": DRAFT, "type": "object", "properties": {
                    "status": {"enum": ["positive", "negative"]},
                    "code": {"oneOf": [{"const": "UNAVAILABLE"}, {"const": "INVALID"}]},
                    "nested": {"$ref": target}}, **extra}
                self.write_schema()
                self.doc = self.declaration()
                self.assertDiagnostics(everywhere(code, *TOOL_REFS))

    def test_boolean_schema_targets_are_schemas(self):
        self.schema["$defs"] = {"anything": True}
        self.schema["properties"]["nested"] = {"$ref": "#/$defs/anything"}
        self.write_schema()
        self.doc = self.declaration()
        self.assertValidWithGaps()

    def test_inventory_pointer_into_annotation_data_is_refused(self):
        """Review r4187574917: an example is data, never the outcome vocabulary."""
        self.schema["examples"] = [{"enum": ["positive", "negative"]}]
        self.write_schema()
        self.doc = self.declaration()
        self.tool()["outcomes"]["inventories"][0]["pointer"] = "/examples/0"
        self.assertDiagnostics([("invalid_inventory_pointer", "/tools/0/outcomes/inventories/0/pointer")])

    def test_shared_references_resolve_in_linear_work(self):
        """Review r4187575076: shared `anyOf` references must not multiply the work."""
        layers = {"l0": {"enum": ["positive", "negative"]}}
        for i in range(1, 17):
            layers[f"l{i}"] = {"anyOf": [{"$ref": f"#/$defs/l{i - 1}"}, {"$ref": f"#/$defs/l{i - 1}"}]}
        self.schema["$defs"] = layers
        self.schema["properties"]["status"] = {"$ref": "#/$defs/l16"}
        self.write_schema()
        self.doc = self.declaration()
        calls = []
        original = self.module.Offline.finite

        def counted(this, *args, **kwargs):
            calls.append(1)
            return original(this, *args, **kwargs)

        with patch.object(self.module.Offline, "finite", counted):
            self.assertValidWithGaps()
        self.assertLess(len(calls), 500)

    def test_shared_reference_chains_resolve_in_linear_work(self):
        """Review 5421098780 (previously missed): judging every union member must
        not re-walk a shared `$ref` chain per member (quadratic resolver work)."""
        aliases = {"a0": {"type": "object"}}
        for i in range(1, 513):
            aliases[f"a{i}"] = {"$ref": f"#/$defs/a{i - 1}"}
        self.schema["$defs"] = aliases
        self.schema["properties"]["aliased"] = {"anyOf": [{"$ref": f"#/$defs/a{i}"} for i in range(1, 513)]}
        self.write_schema()
        self.assertLess((self.root / "outcome.json").stat().st_size, 65536)
        self.doc = self.declaration()
        calls = []
        original = self.module.Offline.resolve

        def counted(this, *args, **kwargs):
            calls.append(1)
            return original(this, *args, **kwargs)

        with patch.object(self.module.Offline, "resolve", counted):
            self.assertValidWithGaps()
        self.assertLess(len(calls), 8 * 512)

    def test_union_coverage_works_in_linear_memory(self):
        """Review r4188149048: a shallow file of shared-reference union layers must
        not make coverage retain a descendant set per member (quadratic memory)."""
        layers = {"l0": {"type": "object"}}
        for i in range(1, 401):
            layers[f"l{i}"] = {"anyOf": [{"$ref": f"#/$defs/l{i - 1}"}, {"$ref": f"#/$defs/l{i - 1}"}]}
        self.schema["$defs"] = layers
        self.schema["properties"]["layered"] = {"$ref": "#/$defs/l400"}
        self.write_schema()
        self.assertLess((self.root / "outcome.json").stat().st_size, 65536)
        self.doc = self.declaration()
        tracemalloc.start()
        try:
            report = self.validate()
            _, peak = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()
        self.assertEqual(diagnostics(report), [])
        self.assertLess(peak, 8 * 1024 * 1024)

    def test_projection_work_is_bounded_under_changing_inherited_requirements(self):
        """Review 5421601208 (previously missed): two references per `anyOf` layer,
        one adding a required name, give every path its own inherited context, so
        memoization cannot help and the work doubles per layer. Projection stops at
        a located `projection_work_limit`; a shallow stack still resolves."""
        def layered(depth):
            def branch(code):
                return {"type": "object", "required": ["code"], "properties": {"code": {"const": code}}}
            layers = {"l0": {"oneOf": [branch("UNAVAILABLE"), branch("INVALID")]}}
            for i in range(1, depth + 1):
                layers[f"l{i}"] = {"anyOf": [{"$ref": f"#/$defs/l{i - 1}"},
                                             {"$ref": f"#/$defs/l{i - 1}", "required": [f"r{i}"]}]}
            return {"$schema": DRAFT, "type": "object", "required": ["error"],
                    "properties": {"error": {"$ref": f"#/$defs/l{depth}"}}, "$defs": layers}
        for depth, expected in [(4, []),
                                (16, [("projection_work_limit", "/tools/0/outcomes/inventories/1/pointer")])]:
            with self.subTest(depth=depth):
                self.doc = self.declaration()
                ref = self.put("layered-error.json", layered(depth))
                self.pin(ref)
                t = self.tool()
                t["error"] = dict(ref)
                t["outcomes"]["inventories"][1].update(pointer=f"/$defs/l{depth}", discriminator="code")
                calls = []
                original = self.module.Offline.resolve_finite

                def counted(this, *args, **kwargs):
                    calls.append(1)
                    return original(this, *args, **kwargs)

                with patch.object(self.module.Offline, "resolve_finite", counted):
                    self.assertDiagnostics(expected, status="invalid" if expected else "valid-with-gaps")
                self.assertLess(len(calls), 20000)

    def test_a_long_reference_chain_is_a_located_depth_limit(self):
        """Review r4187849153: a shallow file can chain `$ref`s past the depth bound;
        projecting through it is a located diagnostic, never an uncaught error."""
        for length, expected in [(100, []),
                                 (600, [("schema_depth_limit", "/tools/0/outcomes/inventories/0/pointer")])]:
            with self.subTest(length=length):
                layers = {"l0": {"enum": ["positive", "negative"]}}
                for i in range(1, length + 1):
                    layers[f"l{i}"] = {"$ref": f"#/$defs/l{i - 1}"}
                self.schema["$defs"] = layers
                self.schema["properties"]["status"] = {"$ref": f"#/$defs/l{length}"}
                self.write_schema()
                self.doc = self.declaration()
                self.assertDiagnostics(expected, status="invalid" if expected else "valid-with-gaps")
        path = self.root / "declaration.json"
        path.write_text(json.dumps(self.doc))
        result = self.cli(path, "--json", "--snapshot", f"synthetic@{self.revision}={self.root}")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(diagnostics(json.loads(result.stdout)),
                         [("schema_depth_limit", "/tools/0/outcomes/inventories/0/pointer")])

    def test_nul_bytes_are_refused_not_raised(self):
        self.tool()["input"]["path"] = "outcome\x00.json"
        self.assertDiagnostics([("unsafe_reference_path", "/tools/0/input")])
        self.doc = self.declaration()
        self.schema["properties"]["nested"] = {"$ref": "other\x00.json"}
        self.write_schema()
        self.doc = self.declaration()
        self.assertDiagnostics(everywhere("remote_or_unsafe_schema_reference", *TOOL_REFS))

    def test_symlink_escape(self):
        with tempfile.TemporaryDirectory() as outside:
            target = Path(outside) / "outside.json"
            target.write_text("{}")
            (self.root / "escape.json").symlink_to(target)
            self.tool()["input"]["path"] = "escape.json"
            self.assertDiagnostics([("escaping_reference_path", "/tools/0/input")])

    def test_nested_remote_and_bad_local_reference(self):
        for ref, code in [("https://invalid.test/a.json", "remote_or_unsafe_schema_reference"),
                          ("../a.json", "unsafe_schema_reference"),
                          ("/tmp/a.json", "unsafe_schema_reference"),
                          ("#/missing", "unresolved_pointer")]:
            with self.subTest(ref=ref):
                self.schema["properties"]["nested"] = {"$ref": ref}
                self.write_schema()
                self.doc = self.declaration()
                self.assertDiagnostics(everywhere(code, *TOOL_REFS))

    def test_content_schema_and_dependencies_are_walked(self):
        """L5: a remote `$ref` under `contentSchema` or legacy `dependencies` is refused."""
        for place in ["contentSchema", "dependencies", "additionalItems"]:
            with self.subTest(place=place):
                self.schema = {"$schema": DRAFT, "type": "object", "properties": {
                    "status": {"enum": ["positive", "negative"]},
                    "code": {"oneOf": [{"const": "UNAVAILABLE"}, {"const": "INVALID"}]}}}
                remote = {"$ref": "https://invalid.test/hidden.json"}
                if place == "contentSchema":
                    self.schema["properties"]["blob"] = {"type": "string", "contentSchema": remote}
                elif place == "dependencies":
                    self.schema["dependencies"] = {"status": remote, "code": ["status"]}
                else:
                    self.schema["properties"]["pair"] = {"type": "array", "additionalItems": remote}
                self.write_schema()
                self.doc = self.declaration()
                self.assertDiagnostics(everywhere("remote_or_unsafe_schema_reference", *TOOL_REFS))

    def test_recursive_local_schema_without_fetch(self):
        self.schema["properties"]["recursive"] = {"$ref": "#"}
        self.write_schema()
        self.doc = self.declaration()
        self.assertValidWithGaps()

    def test_contained_local_reference_is_pinned(self):
        other = {"type": "string", "enum": ["positive", "negative"]}
        raw = json.dumps(other).encode()
        (self.root / "local.json").write_bytes(raw)
        self.schema["properties"]["status"] = {"$ref": "local.json"}
        self.write_schema()
        self.doc = self.declaration()
        self.assertDiagnostics(everywhere("unpinned_local_reference", *TOOL_REFS))
        self.pin({**self.ref, "path": "local.json", "sha256": hashlib.sha256(raw).hexdigest()})
        self.assertValidWithGaps()

    def test_unsupported_schema_dialects_are_refused(self):
        """Review r4189280837: the analysis applies 2020-12 semantics, so a schema
        resource declaring another dialect, at the root or under a nested `$id`,
        is refused rather than read with the wrong rules."""
        draft7 = "http://json-schema.org/draft-07/schema#"
        for case, change, expected in [
                ("root", lambda s: s.update({"$schema": draft7}), "unsupported_schema_dialect"),
                ("nested $id", lambda s: s.setdefault("$defs", {}).update(
                    legacy={"$id": "https://synthetic.invalid/legacy.json", "$schema": draft7, "type": "object"}),
                 "unsupported_schema_dialect"),
                ("nested without $id", lambda s: s["properties"].update(
                    nested={"$schema": draft7, "type": "object"}), "unsupported_schema_dialect"),
                ("2020-12 with empty fragment", lambda s: s.update({"$schema": DRAFT + "#"}), None),
                ("no $schema", lambda s: s.pop("$schema"), None)]:
            with self.subTest(case=case):
                self.schema = {"$schema": DRAFT, "type": "object", "properties": {
                    "status": {"enum": ["positive", "negative"]},
                    "code": {"oneOf": [{"const": "UNAVAILABLE"}, {"const": "INVALID"}]}}}
                change(self.schema)
                self.write_schema()
                self.doc = self.declaration()
                if expected:
                    self.assertDiagnostics(everywhere(expected, *TOOL_REFS))
                else:
                    self.assertValidWithGaps()

    def test_referenced_document_dialects_are_refused(self):
        """Review r4189416474: a fragment reference into another file visits only
        the target subtree, so that file's root, and any resource the pointer
        passes through, must declare 2020-12 (or nothing) as well."""
        draft7 = "http://json-schema.org/draft-07/schema#"
        target = {"type": "object", "properties": {"code": {"enum": ["INVALID"]}}}
        for case, other, fragment, expected in [
                ("draft-07 root", {"$schema": draft7, "definitions": {"outcome": target}},
                 "#/definitions/outcome", "unsupported_schema_dialect"),
                ("draft-07 resource on the path",
                 {"$schema": DRAFT, "$defs": {"res": {"$id": "https://synthetic.invalid/r.json", "$schema": draft7,
                                                       "$defs": {"outcome": target}}}},
                 "#/$defs/res/$defs/outcome", "unsupported_schema_dialect"),
                ("2020-12 root", {"$schema": DRAFT, "$defs": {"outcome": target}}, "#/$defs/outcome", None)]:
            with self.subTest(case=case):
                self.schema = {"$schema": DRAFT, "type": "object", "properties": {
                    "status": {"enum": ["positive", "negative"]},
                    "code": {"oneOf": [{"const": "UNAVAILABLE"}, {"const": "INVALID"}]},
                    "nested": {"$ref": "legacy.json" + fragment}}}
                self.write_schema()
                self.doc = self.declaration()
                self.pin(self.put("legacy.json", other))
                if expected:
                    self.assertDiagnostics(everywhere(expected, *TOOL_REFS))
                else:
                    self.assertValidWithGaps()

    def test_data_keywords_do_not_execute_references(self):
        self.schema["examples"] = [{"$ref": "https://invalid.test/data-not-a-schema"}]
        self.schema["properties"]["status"]["default"] = {"$id": "https://invalid.test/not-a-resource"}
        self.write_schema()
        self.doc = self.declaration()
        self.assertValidWithGaps()

    def test_reference_checks_never_open_network(self):
        self.schema["properties"]["nested"] = {"$ref": "https://invalid.test/schema"}
        self.write_schema()
        self.doc = self.declaration()
        with patch("socket.create_connection", side_effect=AssertionError("network forbidden")):
            self.assertDiagnostics(everywhere("remote_or_unsafe_schema_reference", *TOOL_REFS))

    def test_tool_schemas_come_from_the_declared_source(self):
        """L4: a tool's schemas come from the repository and revision `source` names."""
        other = self.root / "other"
        other.mkdir()
        foreign = self.put("outcome.json", self.schema, root=other, repository="elsewhere", revision="b" * 40)
        t = self.tool()
        t["output"], t["error"] = dict(foreign), dict(foreign)
        self.assertDiagnostics(
            [("tool_schema_outside_source", "/tools/0/error"), ("tool_schema_outside_source", "/tools/0/output")],
            roots={("synthetic", self.revision): self.root, ("elsewhere", "b" * 40): other})

    # ---- identity, support and the service ---------------------------------

    def test_support_and_unique_identity(self):
        unsupported = [(f"unsupported_{c}", "/tools/0/evidence_ids") for c in sorted(SEMANTIC_IDS)]
        for action, expected in [
            ("duplicate_tool", [("duplicate_tool_id", "/tools/1/id")]),
            ("duplicate_id", [("duplicate_support_id", "/gaps/1/id")]),
            ("missing_id", unsupported + [("missing_support_reference", "/tools/0/evidence_ids/0")]),
            ("repeated_id", [("duplicate_support_reference", "/tools/0/evidence_ids")]),
            ("audit", [("missing_audit_gap", "/tools/0/evidence_policy/audit")]),
            ("audit_claim", [("unsupported_audit_claim", "/tools/0/evidence_policy/audit")]),
            ("execution", [("unbounded_execution", "/tools/0/effects/execution")]),
            ("scope", [("empty_scope_mapping", "/tools/0/binding/scope_references")]),
            ("scope_gap", [("missing_scope_gap", "/tools/0/binding/scope_status")]),
            ("revocation", [("missing_revocation_gap", "/tools/0/binding/revocation")]),
        ]:
            with self.subTest(action=action):
                self.doc = self.declaration()
                t = self.tool()
                if action == "duplicate_tool": self.doc["tools"].append(copy.deepcopy(t))
                elif action == "duplicate_id": self.doc["gaps"].append(copy.deepcopy(self.doc["gaps"][0]))
                elif action == "missing_id": t["evidence_ids"] = ["missing"]
                elif action == "repeated_id": t["evidence_ids"] = ["synthetic-observation"] * 2
                elif action == "audit": t["gap_ids"] = []
                elif action == "audit_claim": t["evidence_policy"]["audit"] = "implemented"
                elif action == "execution": t["effects"]["execution"] = True
                elif action == "scope": t["binding"]["scope_references"] = []
                elif action == "scope_gap": t["binding"]["scope_status"] = "gap"
                elif action == "revocation": t["binding"]["revocation"] = "unimplemented"
                self.assertDiagnostics(expected)

    def test_mapped_scope_cannot_cite_a_scope_gap(self):
        """Review r4189769322: a mapped scope beside a cited gap that says the scope
        mapping is unresolved is a contradiction, not an implemented claim."""
        self.doc["gaps"].append({"id": "scope-gap", "concerns": ["scope"], "description": "Unresolved scope."})
        self.tool()["gap_ids"].append("scope-gap")
        self.assertDiagnostics([("mapped_scope_claims_gap", "/tools/0/binding/scope_status")])
        self.tool()["binding"].update(scope_status="gap", scope_references=[])
        self.assertValidWithGaps()

    def test_source_artifacts_share_the_source_identity(self):
        self.pin({**self.ref, "revision": "b" * 40})
        self.assertDiagnostics([("source_artifact_identity_mismatch", "/source/artifacts/1")],
                               roots={("synthetic", self.revision): self.root, ("synthetic", "b" * 40): self.root})

    def test_repetition_cross_checks(self):
        t = self.tool()
        t["repetition"] = {"mode": "fresh_observation", "deadline": "host_monotonic",
            "trace_ids_are_authority": False, "maximum_age_source": "host",
            "original_timestamps": True, "final_age_check": True}
        self.assertDiagnostics([("freshness_without_observation", "/tools/0/repetition/mode")])
        t["effects"]["external_reads"] = True
        t["evidence_policy"]["observation_time"] = True
        self.assertValidWithGaps()
        t["repetition"] = {"mode": "lease_replay", "deadline": "host_monotonic",
            "trace_ids_are_authority": False, "key_scope": "principal", "conflict": "reject",
            "in_progress": "explicit", "coordination": "atomic_external", "preserve_timestamps": True}
        self.assertDiagnostics([("replay_without_persistence", "/tools/0/repetition/mode")])
        t["effects"]["persistence"] = True
        self.assertValidWithGaps()

    def test_resource_identity_without_optional_format_checker(self):
        """Amended for feature 039 (research R-15). The ratified
        amend-factory-mcp-conformance-auth-profile, design *Compatibility*, reverses
        this test's premise: "A deployed declaration without the block, which is
        valid today, becomes invalid (`hosted_auth_missing`)". The deployed service
        now carries a valid block with an issuer-assigned audience, so the resource
        URI is still judged alone; a URI with a query also reports
        `auth_resource_query`."""
        self.assigned("relative/path")
        with patch.dict(self.module.FormatChecker.checkers, {}, clear=True):
            self.assertDiagnostics([("invalid_resource_uri", "/service/canonical_resource_uri")])
            self.assigned("https://mcp.example.test/")
            self.assertValidWithGaps()
            # Review r4187849299: `urlsplit` does not check percent escapes.
            # Review r4188149170: nor characters RFC 3986 forbids unescaped.
            for uri, valid in [("https://mcp.example.test/a%2Fb%c3%A9", True),
                               ("https://mcp.example.test/%ZZ", False), ("https://mcp.example.test/%4", False),
                               ("https://mcp.example.test/mcp%", False), ("https://mcp.example.test/?q=%G1", False),
                               ("https://mcp.example.test/%7Bscope%7D", True), ("https://mcp.example.test/a%7Cb", True),
                               ("https://mcp.example.test/a;b=c,d+e!$&'()*@:~", True), ("https://[::1]/mcp", True),
                               ("https://mcp.example.test/{scope}", False), ("https://bad|host.example/", False),
                               ("https://mcp.example.test/a^b", False), ("https://mcp.example.test/a`b", False),
                               ("https://mcp.example.test/<a>", False), ('https://mcp.example.test/"a"', False),
                               ("https://mcp.example.test/a[0]", False), ("https://mcp.example.test/?q=[0]", False)]:
                with self.subTest(uri=uri):
                    self.assigned(uri)
                    if valid:
                        self.assertValidWithGaps()
                    else:
                        self.assertDiagnostics(
                            ([("auth_resource_query", "/service/canonical_resource_uri")] if "?" in uri else [])
                            + [("invalid_resource_uri", "/service/canonical_resource_uri")])

    def test_resource_uri_is_https_without_fragment_or_userinfo(self):
        """L2: a canonical resource URI is an absolute https URI with no fragment or userinfo.

        Amended for feature 039 (research R-15): the ratified design *Compatibility*
        makes a deployed declaration without the block invalid
        (`hosted_auth_missing`), so the service carries a valid block with an
        issuer-assigned audience and the URI is still judged alone."""
        self.assigned("https://mcp.example.test/mcp")
        with patch.dict(self.module.FormatChecker.checkers, {}, clear=True):
            self.assertValidWithGaps()
        for uri in ["http://mcp.example.test/mcp", "https://mcp.example.test/mcp#frag",
                    "https://user@mcp.example.test/mcp", "https://user:pw@mcp.example.test/mcp",
                    "javascript:alert(1)", "urn:example:mcp", "https:///mcp", "https://mcp.example.test:99999/",
                    "https://mcp.example.test/m cp", "https://mcp.example.test/\x00",
                    "https://mcp.example.test\\evil", "https://example.test/\u0085",
                    "https://b\u00fccher.example/mcp"]:
            with self.subTest(uri=uri):
                self.assigned(uri)
                with patch.dict(self.module.FormatChecker.checkers, {}, clear=True):
                    self.assertDiagnostics([("invalid_resource_uri", "/service/canonical_resource_uri")])

    # ---- in-memory input, determinism ---------------------------------------

    def test_in_memory_declaration_codes(self):
        """L1: the Python entry point keeps size and number codes distinct."""
        self.doc["gaps"] += [{"id": f"g{i}", "concerns": ["audit"], "description": "x" * 2048}
                             for i in range(140)]
        self.assertDiagnostics([("input_size_limit", "/")])
        self.doc = self.declaration()
        self.tool()["limits"]["request_bytes"] = float("nan")
        self.assertDiagnostics([("non_json_number", "/")])
        self.doc = self.declaration()
        self.doc["gaps"].append(self.doc)
        self.assertDiagnostics([("invalid_json_value", "/")])
        self.doc = self.declaration()
        self.doc["gaps"][0]["description"] = "lone \ud800 surrogate"
        self.assertValidWithGaps()

    def test_lone_surrogates_count_at_their_escaped_size(self):
        """Review r4187669042: a lone surrogate is six bytes of JSON, not three."""
        self.doc["gaps"] += [{"id": f"s{i}", "concerns": ["audit"], "description": "\ud800" * 2048}
                             for i in range(24)]
        self.assertDiagnostics([("input_size_limit", "/")])

    def test_diagnostics_are_deterministic_and_unique(self):
        t = self.tool()
        t["evidence_ids"] = ["nope1", "nope1", "nope2"]
        t["owner"] = "x"
        first = self.validate()
        self.assertEqual(first, self.validate())
        codes = diagnostics(first)
        self.assertEqual(len(codes), len(set(codes)))
        self.assertEqual(codes, sorted(codes, key=lambda c: (c[1], c[0])))

    # ---- the command line ---------------------------------------------------

    def test_cli_exit_codes(self):
        path = self.root / "declaration.json"
        path.write_text(json.dumps(self.doc))
        snapshot = f"synthetic@{self.revision}={self.root}"
        run = self.cli(path, "--json", "--snapshot", snapshot)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)["status"], "valid-with-gaps")
        run = self.cli(path, "--json")
        self.assertEqual(run.returncode, 2)
        self.assertEqual({d["code"] for d in json.loads(run.stdout)["diagnostics"]}, {"snapshot_unavailable"})
        for raw, code in [("{", "malformed_json"), ('{"kind": 1, "kind": 2}', "duplicate_json_key"),
                          ('{"kind": NaN}', "non_json_number"),
                          (json.dumps({"pad": "x" * self.module.INPUT_LIMIT}), "input_size_limit")]:
            with self.subTest(code=code):
                path.write_text(raw)
                run = self.cli(path, "--json", "--snapshot", snapshot)
                self.assertEqual(run.returncode, 1, run.stderr)
                self.assertEqual(diagnostics(json.loads(run.stdout)), [(code, "/")])
        run = self.cli(self.root / "absent.json", "--json")
        self.assertEqual(run.returncode, 2)
        self.assertEqual(diagnostics(json.loads(run.stdout)), [("input_unreadable", "/")])

    def test_cli_output_is_bounded(self):
        """Review 5421601208 (previously missed): escaping can roughly double a
        permitted input in either output format. Output past 256 KiB is replaced
        by a stable `output_size_limit` report (exit 2), never truncated."""
        self.doc["gaps"] += [{"id": f"wide-{i}", "concerns": ["audit"], "description": "\ue000" * 1500}
                             for i in range(40)]
        path = self.root / "declaration.json"
        path.write_text(json.dumps(self.doc, ensure_ascii=False), encoding="utf-8")
        self.assertLess(path.stat().st_size, self.module.INPUT_LIMIT)
        snapshot = f"synthetic@{self.revision}={self.root}"
        self.assertEqual(self.validate()["status"], "valid-with-gaps")
        for flags in (["--json"], []):
            with self.subTest(flags=flags):
                run = self.cli(path, *flags, "--snapshot", snapshot)
                self.assertLessEqual(len(run.stdout.encode("utf-8")), 262144)
                self.assertEqual(run.returncode, 2, run.stdout[:200])
                if flags:
                    self.assertEqual(diagnostics(json.loads(run.stdout)), [("output_size_limit", "/")])
                else:
                    self.assertIn("output_size_limit /", run.stdout)

    def test_overflowing_number_literals_are_refused(self):
        """Reviews r4191064649 and r4191131248: `1e9999` parses to infinity and a
        nonzero `1e-9999` to zero, and referenced schemas never pass `check_input`,
        so such literals are refused where they are parsed, in a referenced schema
        and in the declaration file. Real zero literals are kept."""
        refused = [("json_number_limit", "/tools/0/error")]
        for case, const, enum, expected in [("overflow", "1e9999", "2e9999", refused),
                                            ("underflow", "1e-9999", "0", refused),
                                            ("negative underflow", "-2.5e-400", "0", refused),
                                            ("zero literals", "0e5", "-0.0", [])]:
            with self.subTest(case=case):
                self.doc = self.declaration()
                self.error_union(parent_typed=True)
                error = json.loads((self.root / "domain-error.json").read_text())
                error["$defs"]["invalidError"]["properties"]["retryable"] = {"const": "__C__", "enum": ["__E__"]}
                raw = json.dumps(error).replace('"__C__"', const).replace('"__E__"', enum).encode()
                (self.root / "domain-error.json").write_bytes(raw)
                ref = {"repository": "synthetic", "revision": self.revision, "path": "domain-error.json",
                       "sha256": hashlib.sha256(raw).hexdigest()}
                self.doc = self.declaration()
                self.pin(ref)
                self.tool()["error"] = dict(ref)
                self.tool()["outcomes"]["inventories"][1].update(pointer="/$defs/error", discriminator="code")
                self.assertDiagnostics(expected, status="invalid" if expected else "valid-with-gaps")
        path = self.root / "declaration.json"
        for literal in ("1e9999", "1e-9999"):
            with self.subTest(declaration=literal):
                path.write_text(json.dumps(self.declaration()).replace(
                    '"request_bytes": 262144', '"request_bytes": ' + literal))
                run = self.cli(path, "--json", "--snapshot", f"synthetic@{self.revision}={self.root}")
                self.assertEqual(run.returncode, 1, run.stderr)
                self.assertEqual(diagnostics(json.loads(run.stdout)), [("json_number_limit", "/")])

    def test_cli_oversized_integer_is_a_diagnostic(self):
        """Review r4187669157: Python's integer-digit limit is a refusal, not a traceback."""
        path = self.root / "declaration.json"
        path.write_text('{"schema_version": 1' + "0" * 4300 + "}")
        run = self.cli(path, "--json", "--snapshot", f"synthetic@{self.revision}={self.root}")
        self.assertEqual(run.returncode, 1, run.stderr)
        self.assertEqual(diagnostics(json.loads(run.stdout)), [("json_number_limit", "/")])

    def test_cli_usage_errors_exit_two(self):
        """L1: a malformed --snapshot is a usage error, never an invalid declaration."""
        path = self.root / "declaration.json"
        path.write_text(json.dumps(self.doc))
        good = f"synthetic@{self.revision}={self.root}"
        for snapshots in [["no-equals-sign"], ["norevision=/tmp"], ["@rev=/tmp"], ["repo@=/tmp"],
                          ["repo@rev="], [good, good]]:
            with self.subTest(snapshots=snapshots):
                args = [path, "--json"]
                for snapshot in snapshots:
                    args += ["--snapshot", snapshot]
                run = self.cli(*args)
                self.assertEqual(run.returncode, 2, run.stdout)
                self.assertEqual(run.stdout, "")
                self.assertIn("--snapshot", run.stderr)

    def test_cli_human_output_names_codes_and_gaps(self):
        path = self.root / "declaration.json"
        self.tool()["owner"] = "other"
        path.write_text(json.dumps(self.doc))
        run = self.cli(path, "--snapshot", f"synthetic@{self.revision}={self.root}")
        self.assertEqual(run.returncode, 1)
        self.assertEqual(run.stdout.splitlines(), [
            "invalid; offline declaration checks only; verified conformance: false",
            "structure: pass", "references: pass", "semantics: fail",
            "owner_domain_mismatch /tools/0/owner",
            "gap audit-gap: No resolving audit sink."])

    def test_cli_human_output_escapes_control_characters(self):
        """Review r4187575035: declaration text cannot inject lines or terminal codes."""
        path = self.root / "declaration.json"
        self.doc["gaps"].append({"id": "g\u001b[31m", "concerns": ["audit"],
                                 "description": "line one\nfake: injected\u001b[2J\u202e \\ plain caf\u00e9"})
        path.write_text(json.dumps(self.doc))
        run = self.cli(path, "--snapshot", f"synthetic@{self.revision}={self.root}")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(run.stdout.splitlines()[-1],
                         "gap g\\x1b[31m: line one\\x0afake: injected\\x1b[2J\\u202e \\\\ plain caf\u00e9")
        self.assertNotIn("\u001b", run.stdout)

    def test_packaged_example(self):
        """M7: the shipped example validates exactly as the runbook says."""
        run = self.cli(EXAMPLES / "declaration.example.json", "--json",
                       "--snapshot", f"synthetic@{'a' * 40}={EXAMPLES}")
        self.assertEqual(run.returncode, 0, run.stderr)
        report = json.loads(run.stdout)
        self.assertEqual(report["status"], "valid-with-gaps")
        self.assertEqual(report["diagnostics"], [])
        self.assertFalse(report["verified_conformance"])
        self.assertEqual([g["id"] for g in report["gaps"]], ["audit-gap"])

    # ---- the authorization profile (feature 039) ---------------------------
    #
    # Realizes amend-factory-mcp-conformance-auth-profile (ratified 2026-10-08),
    # specs/039-factory-mcp-auth-profile. Every name below is synthetic: the
    # `.test` top-level domain is reserved (RFC 6761), and no real issuer,
    # tenant, host or domain schema is used.

    @staticmethod
    def metadata_path(uri):
        """RFC 9728 section 3.1 insertion, for the helper's default only; the
        derivation itself is pinned by literal paths in its own test."""
        path = urlsplit(uri).path
        return WELL_KNOWN + ("" if path in ("", "/") else path)

    def hosted(self, uri=RESOURCE, **block):
        """Deploy the synthetic service with a valid block, supported by an `auth` gap."""
        auth = {"issuer": ISSUER, "algorithms": ["RS256"],
                "audience": {"binding": "resource_uri", "value": uri},
                "metadata_path": self.metadata_path(uri), "evidence_ids": [], "gap_ids": ["auth-gap"]}
        auth.update(block)
        self.doc["service"] = {"deployment": "deployed", "installation": "synthetic-install",
                               "environment": "test", "canonical_resource_uri": uri, "auth": auth}
        if not any(gap["id"] == "auth-gap" for gap in self.doc["gaps"]):
            self.doc["gaps"].append({"id": "auth-gap", "concerns": ["auth"],
                                     "description": "Synthetic block; no server's token verification was observed."})
        return auth

    def assigned(self, uri):
        """A deployed service whose audience is issuer-assigned, so that a test of the
        resource URI alone carries no URI-bound audience (039 research R-15)."""
        return self.hosted(uri, audience={"binding": "issuer_assigned", "value": "synthetic-resource-0001"})

    def test_hosted_declaration_without_block(self):
        """039 FR-001, *Hosted declaration without the block*: refused at the service."""
        self.hosted()
        del self.doc["service"]["auth"]
        self.assertDiagnostics([("hosted_auth_missing", "/service")])

    def test_auth_on_an_undeployed_service_is_refused(self):
        """039 FR-002, *Stdio-only declaration*. CHARACTERIZATION: the closed
        not-deployed branch refuses an `auth` field on `main` already. The block cites
        no `auth` record, so nothing else in the declaration differs from `main`'s."""
        block = {"issuer": ISSUER, "algorithms": ["RS256"], "audience": {"binding": "resource_uri", "value": RESOURCE},
                 "metadata_path": WELL_KNOWN + "/mcp", "evidence_ids": [], "gap_ids": []}
        self.doc["service"] = {"deployment": "not_deployed", "auth": block}
        self.assertDiagnostics([("schema_oneOf", "/service")])

    def test_stdio_declaration_needs_no_block(self):
        """039 FR-002, *Stdio-only declaration*. CHARACTERIZATION: a block-free
        not-deployed declaration validates on `main` already."""
        self.assertEqual(self.doc["service"], {"deployment": "not_deployed"})
        self.assertValidWithGaps()

    def test_a_valid_hosted_block_is_accepted(self):
        """039 FR-003, FR-010, FR-012; *EdDSA beside RS256*, *Audience is the server's
        own resource*, *Issuer-assigned audience*. A gap-only block is
        valid-with-gaps and never certified."""
        for case, change in [
                ("gap only, RS256 alone", {}),
                ("RS256 and EdDSA", {"algorithms": ["RS256", "EdDSA"]}),
                ("EdDSA first", {"algorithms": ["EdDSA", "RS256"]}),
                ("issuer-assigned audience", {"audience": {"binding": "issuer_assigned",
                                                           "value": "synthetic-resource-0001"}}),
                ("an assigned value may be a URI", {"audience": {"binding": "issuer_assigned",
                                                                 "value": "api://synthetic-resource"}}),
                ("evidence without auth beside the gap", {"evidence_ids": ["synthetic-observation"]})]:
            with self.subTest(case=case):
                self.doc = self.declaration()
                self.hosted(**change)
                report = self.assertValidWithGaps()
                self.assertEqual([gap["id"] for gap in report["gaps"]], ["audit-gap", "auth-gap"])
        self.doc = self.declaration()
        self.doc["evidence"][0]["concerns"].append("auth")
        self.hosted(evidence_ids=["synthetic-observation"], gap_ids=[])
        self.assertValidWithGaps()

    def test_block_shape_is_closed(self):
        """039 FR-003, design D7 and OQ-6: a block that breaks its closed shape is
        refused as `schema_oneOf` at `/service` (the structure pass does not descend
        into the branches). The valid block comes first, so this test is red on
        `main`, which refuses every block as a whole."""
        self.hosted()
        self.assertValidWithGaps()
        for case, mutate in [
                ("an unknown field", lambda a: a.update(jwks_uri="https://issuer.example.test/keys")),
                ("a client secret", lambda a: a.update(client_secret="not-a-real-secret")),
                ("a token", lambda a: a.update(token="synthetic.token.value")),
                ("a wrong type", lambda a: a.update(algorithms="RS256")),
                ("a binding outside the closed set", lambda a: a["audience"].update(binding="any")),
                ("an unknown audience field", lambda a: a["audience"].update(scope="all")),
                ("an empty algorithm list", lambda a: a.update(algorithms=[])),
                ("a repeated algorithm", lambda a: a.update(algorithms=["RS256", "RS256"])),
                ("an issuer given as a list", lambda a: a.update(
                    issuer=[ISSUER, "https://issuer.example.test/second"])),
                ("a second issuer", lambda a: a.update(issuers=["https://issuer.example.test/second"])),
                ("a missing field", lambda a: a.pop("metadata_path")),
                ("an audience given as a list", lambda a: a.update(
                    audience=[{"binding": "resource_uri", "value": RESOURCE}]))]:
            with self.subTest(case=case):
                self.doc = self.declaration()
                mutate(self.hosted())
                self.assertDiagnostics([("schema_oneOf", "/service")])

    def test_issuer_must_be_an_https_identifier(self):
        """039 FR-004, *Issuer named rather than identified*."""
        for issuer in ["hermes", "synthetic-issuer", "http://issuer.example.test/synthetic",
                       "https://user@issuer.example.test/synthetic",
                       "https://issuer.example.test/synthetic?tenant=x", "https://issuer.example.test/synthetic?",
                       "https://issuer.example.test/synthetic#keys", "urn:example:issuer", "https:///synthetic",
                       "https://issuer.example.test/a b"]:
            with self.subTest(issuer=issuer):
                self.doc = self.declaration()
                self.hosted(issuer=issuer)
                self.assertDiagnostics([("invalid_issuer", "/service/auth/issuer")])
        for issuer in ["https://issuer.example.test", "https://issuer.example.test/synthetic/v2.0",
                       "https://issuer.example.test:8443/tenant/"]:
            with self.subTest(issuer=issuer):
                self.doc = self.declaration()
                self.hosted(issuer=issuer)
                self.assertValidWithGaps()

    def test_metadata_path_is_the_rfc9728_location(self):
        """039 FR-005, *Metadata off the well-known path*: RFC 9728 section 3.1 inserts
        the well-known string before the resource URI's path (design D4, OQ-3)."""
        for uri, path in [("https://mcp.example.test", WELL_KNOWN),
                          ("https://mcp.example.test/", WELL_KNOWN),
                          ("https://mcp.example.test/mcp", WELL_KNOWN + "/mcp"),
                          ("https://mcp.example.test/a/b/", WELL_KNOWN + "/a/b/"),
                          ("https://mcp.example.test:8443/mcp", WELL_KNOWN + "/mcp"),
                          ("https://mcp.example.test/a%2Fb", WELL_KNOWN + "/a%2Fb")]:
            with self.subTest(uri=uri):
                self.doc = self.declaration()
                self.hosted(uri, metadata_path=path)
                self.assertValidWithGaps()
        for uri, path in [(RESOURCE, WELL_KNOWN), (RESOURCE, "/mcp" + WELL_KNOWN), (RESOURCE, WELL_KNOWN + "/mcp/"),
                          (RESOURCE, WELL_KNOWN + "/MCP"), (RESOURCE, "/.well-known/oauth-authorization-server/mcp"),
                          (RESOURCE, WELL_KNOWN[1:] + "/mcp"), (RESOURCE, RESOURCE + WELL_KNOWN),
                          ("https://mcp.example.test/a%2Fb", WELL_KNOWN + "/a%2fb"),
                          ("https://mcp.example.test", WELL_KNOWN + "/")]:
            with self.subTest(uri=uri, path=path):
                self.doc = self.declaration()
                self.hosted(uri, metadata_path=path)
                self.assertDiagnostics([("auth_metadata_path_mismatch", "/service/auth/metadata_path")])
        # A resource URI that is already refused has no RFC 9728 location to compare.
        self.doc = self.declaration()
        self.hosted("https://mcp.example.test/m cp", metadata_path="/elsewhere")
        with patch.dict(self.module.FormatChecker.checkers, {}, clear=True):
            self.assertDiagnostics([("invalid_resource_uri", "/service/canonical_resource_uri")])

    def test_hosted_resource_uri_carries_no_query(self):
        """039 FR-006, *Hosted resource URI with a query*: a `?` before any `#` is a
        query component, even an empty one (RFC 3986 section 3), block or no block."""
        query = [("auth_resource_query", "/service/canonical_resource_uri")]
        for uri in ["https://mcp.example.test/mcp?tenant=x", "https://mcp.example.test/mcp?",
                    "https://mcp.example.test?x"]:
            with self.subTest(uri=uri, block=True):
                self.doc = self.declaration()
                self.hosted(uri)
                self.assertDiagnostics(query)
            with self.subTest(uri=uri, block=False):
                self.doc = self.declaration()
                self.hosted(uri)
                del self.doc["service"]["auth"]
                self.assertDiagnostics([("hosted_auth_missing", "/service")] + query)
        # A `?` inside a fragment is no query; the fragment is refused already.
        self.doc = self.declaration()
        self.assigned("https://mcp.example.test/mcp#a?b")
        with patch.dict(self.module.FormatChecker.checkers, {}, clear=True):
            self.assertDiagnostics([("invalid_resource_uri", "/service/canonical_resource_uri")])

    def test_auth_claims_cite_support(self):
        """039 FR-007, *Unsupported authorization claim*: the block's ids resolve as a
        tool's do, and at least one resolved record carries `auth` (design D5, OQ-4)."""
        unsupported = ("unsupported_auth", "/service/auth/evidence_ids")
        for case, change, expected in [
                ("a gap-only block", {}, []),
                ("nothing cited", {"gap_ids": []}, [unsupported]),
                ("support without auth", {"evidence_ids": ["synthetic-observation"], "gap_ids": ["audit-gap"]},
                 [unsupported]),
                ("a dangling evidence id", {"evidence_ids": ["missing-evidence"]},
                 [("missing_support_reference", "/service/auth/evidence_ids/0")]),
                ("a dangling gap id", {"gap_ids": ["auth-gap", "missing-gap"]},
                 [("missing_support_reference", "/service/auth/gap_ids/1")]),
                ("a repeated evidence id", {"evidence_ids": ["synthetic-observation"] * 2},
                 [("duplicate_support_reference", "/service/auth/evidence_ids")]),
                ("a repeated gap id", {"gap_ids": ["auth-gap"] * 2},
                 [("duplicate_support_reference", "/service/auth/gap_ids")]),
                ("a gap cited as evidence", {"evidence_ids": ["auth-gap"], "gap_ids": []},
                 [unsupported, ("missing_support_reference", "/service/auth/evidence_ids/0")])]:
            with self.subTest(case=case):
                self.doc = self.declaration()
                self.hosted(**change)
                self.assertDiagnostics(expected, status="invalid" if expected else "valid-with-gaps")

    def test_auth_concern_is_admitted_everywhere(self):
        """039 FR-007: the concern vocabulary of evidence and gaps admits `auth`; on a
        not-deployed declaration it is merely admitted."""
        self.doc["evidence"][0]["concerns"].append("auth")
        self.doc["gaps"].append({"id": "auth-note", "concerns": ["auth"], "description": "Admitted, unused."})
        self.assertValidWithGaps()

    def test_rs256_is_required(self):
        """039 FR-008, *RS256 absent*. Algorithm names are case-sensitive (RFC 7515
        section 4.1.1), so `rs256` is not RS256."""
        missing = ("auth_rs256_missing", "/service/auth/algorithms")
        for algorithms, expected in [
                (["EdDSA"], [missing]),
                (["rs256"], [missing, ("auth_algorithm_unadmitted", "/service/auth/algorithms/0")]),
                (["EdDSA", "none"], [missing, ("auth_algorithm_forbidden", "/service/auth/algorithms/1")])]:
            with self.subTest(algorithms=algorithms):
                self.doc = self.declaration()
                self.hosted(algorithms=algorithms)
                self.assertDiagnostics(expected)

    def test_none_and_hmac_are_refused_by_name(self):
        """039 FR-009, *Unsigned or symmetric algorithm*: in any letter case."""
        for name in ["none", "None", "NONE", "nOnE", "HS256", "hs256", "Hs256", "HS384", "hs384", "hS384",
                     "HS512", "hs512", "Hs512"]:
            with self.subTest(name=name):
                self.doc = self.declaration()
                self.hosted(algorithms=["RS256", name])
                self.assertDiagnostics([("auth_algorithm_forbidden", "/service/auth/algorithms/1")])
        self.doc = self.declaration()
        self.hosted(algorithms=["none", "RS256", "HS256"])
        self.assertDiagnostics(everywhere("auth_algorithm_forbidden", "/service/auth/algorithms/0",
                                          "/service/auth/algorithms/2"))

    def test_other_algorithms_are_not_admitted(self):
        """039 FR-010, *An algorithm the profile does not admit* (OQ-2)."""
        for name in ["ES256", "PS256", "RS384", "RS512", "eddsa", "EdDSA ", "Ed25519", "HS1", "ＨS256"]:
            with self.subTest(name=name):
                self.doc = self.declaration()
                self.hosted(algorithms=["RS256", name])
                self.assertDiagnostics([("auth_algorithm_unadmitted", "/service/auth/algorithms/1")])

    def test_audience_is_bound_to_the_server(self):
        """039 FR-011 to FR-013, *Audience names another resource* and *Unbounded
        audience* (design D3): exact comparison; no wildcard; never the issuer."""
        unbound = [("auth_audience_unbound", "/service/auth/audience/value")]
        for case, audience in [
                ("another resource", {"binding": "resource_uri", "value": "https://other.example.test/mcp"}),
                ("a trailing slash", {"binding": "resource_uri", "value": RESOURCE + "/"}),
                ("another letter case", {"binding": "resource_uri", "value": "https://MCP.example.test/mcp"}),
                ("an identifier under resource_uri", {"binding": "resource_uri", "value": "synthetic-resource-0001"}),
                ("a wildcard, issuer-assigned", {"binding": "issuer_assigned", "value": "synthetic-*"}),
                ("a bare wildcard", {"binding": "issuer_assigned", "value": "*"}),
                ("the issuer, issuer-assigned", {"binding": "issuer_assigned", "value": ISSUER})]:
            with self.subTest(case=case):
                self.doc = self.declaration()
                self.hosted(audience=audience)
                self.assertDiagnostics(unbound)
        for case, uri, change in [
                ("a resource URI holding a wildcard", "https://mcp.example.test/a*b", {}),
                ("the issuer, resource_uri", RESOURCE, {"issuer": RESOURCE})]:
            with self.subTest(case=case):
                self.doc = self.declaration()
                self.hosted(uri, **change)
                self.assertDiagnostics(unbound)

    def test_dependency_failure_reported_as_an_error_is_an_execution_failure(self):
        """039 FR-014, M5 as narrowed (*Unavailable dependency*): an error-inventory
        code is an execution failure. CHARACTERIZATION on `main`; red against the
        mutant whose classification comparison is removed (verification.md)."""
        self.assertEqual(self.tool()["outcomes"]["mapping"][2]["value"], "UNAVAILABLE")
        for klass, is_error in [("completed_evaluation", False), ("completed_evaluation", True),
                                ("execution_failure", False)]:
            with self.subTest(klass=klass, is_error=is_error):
                self.doc = self.declaration()
                self.tool()["outcomes"]["mapping"][2].update({"class": klass, "is_error": is_error})
                self.assertDiagnostics([("outcome_classification_mismatch", "/tools/0/outcomes/mapping/2")])

    def test_result_statuses_are_completed_evaluations(self):
        """039 FR-014, the MODIFIED body: a result-schema status is a completed
        evaluation, whatever its name says. CHARACTERIZATION on `main`; red against
        the mutant (verification.md)."""
        self.schema["properties"]["status"]["enum"].append("dependency_unavailable")
        self.write_schema()
        self.doc = self.declaration()
        rows = self.tool()["outcomes"]["mapping"]
        rows.append({"inventory": 0, "value": "dependency_unavailable", "class": "execution_failure",
                     "is_error": True})
        self.assertDiagnostics([("outcome_classification_mismatch", "/tools/0/outcomes/mapping/4")])
        rows[4].update({"class": "completed_evaluation", "is_error": False})
        self.assertValidWithGaps()

    def test_two_domains_share_a_code_name(self):
        """039 FR-015, *Two domains share a code name*: each declaration maps its own
        code through its own inventory; judging one moves nothing in the other.
        CHARACTERIZATION: `main` already never compares declarations."""
        first = self.validate()
        self.assertEqual((first["status"], diagnostics(first)), ("valid-with-gaps", []))

        def branch(code):
            return {"type": "object", "additionalProperties": False, "required": ["code", "retryable"],
                    "properties": {"code": {"const": code}, "retryable": {"const": True}}}
        ref = self.put("other-error.json", {"$schema": DRAFT,
                                            "oneOf": [branch("UNAVAILABLE"), branch("RATE_LIMITED")]})
        other = copy.deepcopy(self.doc)
        other["domain"] = "other"
        other["source"]["artifacts"].append(dict(ref))
        tool = other["tools"][0]
        tool.update(owner="other", error=dict(ref))
        tool["outcomes"]["inventories"][1].update(pointer="", discriminator="code")
        tool["outcomes"]["mapping"] = [row for row in tool["outcomes"]["mapping"] if row["inventory"] == 0] + [
            {"inventory": 1, "value": code, "class": "execution_failure", "is_error": True}
            for code in ("UNAVAILABLE", "RATE_LIMITED")]
        roots = {("synthetic", self.revision): self.root}
        second = self.module.validate(other, roots)
        self.assertEqual((second["status"], diagnostics(second)), ("valid-with-gaps", []))
        self.assertEqual(self.validate(), first)
        tool["outcomes"]["mapping"].pop()
        self.assertEqual(diagnostics(self.module.validate(other, roots)),
                         [("incomplete_outcome_mapping", "/tools/0/outcomes/inventories/1")])
        self.assertEqual(self.validate(), first)

    def test_a_code_no_other_domain_uses(self):
        """039 FR-015, *A code no other domain uses*: judged by its own mapping alone.
        CHARACTERIZATION: there is no neutral code list to refuse it."""
        self.schema["properties"]["code"]["oneOf"].append({"const": "SYNTHETIC_ONLY_CODE"})
        self.write_schema()
        self.doc = self.declaration()
        self.tool()["outcomes"]["mapping"].append(
            {"inventory": 1, "value": "SYNTHETIC_ONLY_CODE", "class": "execution_failure", "is_error": True})
        self.assertValidWithGaps()

    def test_auth_diagnostics_are_deterministic(self):
        """039 FR-016, SC-007: several faults at once, located, sorted, de-duplicated
        and identical across runs."""
        self.hosted(issuer="hermes", algorithms=["EdDSA", "HS256", "ES256"],
                    audience={"binding": "resource_uri", "value": "https://other.example.test/"},
                    metadata_path="/mcp" + WELL_KNOWN, gap_ids=["auth-gap", "auth-gap"])
        first = self.validate()
        self.assertEqual(first, self.validate())
        self.assertEqual(diagnostics(first), [
            ("auth_rs256_missing", "/service/auth/algorithms"),
            ("auth_algorithm_forbidden", "/service/auth/algorithms/1"),
            ("auth_algorithm_unadmitted", "/service/auth/algorithms/2"),
            ("auth_audience_unbound", "/service/auth/audience/value"),
            ("duplicate_support_reference", "/service/auth/gap_ids"),
            ("invalid_issuer", "/service/auth/issuer"),
            ("auth_metadata_path_mismatch", "/service/auth/metadata_path")])
        self.assertFalse(first["verified_conformance"])

    def test_packaged_deployed_example(self):
        """039 FR-017: the shipped deployed example validates as the runbook says, and
        names only reserved hosts."""
        path = EXAMPLES / "declaration-deployed.example.json"
        run = self.cli(path, "--json", "--snapshot", f"synthetic@{'a' * 40}={EXAMPLES}")
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        report = json.loads(run.stdout)
        self.assertEqual((report["status"], report["diagnostics"]), ("valid-with-gaps", []))
        self.assertFalse(report["verified_conformance"])
        self.assertEqual([gap["id"] for gap in report["gaps"]], ["audit-gap", "auth-gap"])
        service = json.loads(path.read_text())["service"]
        self.assertEqual(service["deployment"], "deployed")
        self.assertEqual(service["auth"]["algorithms"], ["RS256", "EdDSA"])
        for uri in (service["canonical_resource_uri"], service["auth"]["issuer"]):
            self.assertTrue(urlsplit(uri).hostname.endswith(".example.test"), uri)


if __name__ == "__main__":
    unittest.main()
