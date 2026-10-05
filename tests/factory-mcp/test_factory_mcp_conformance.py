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
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

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
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                              capture_output=True, text=True, cwd=ROOT)

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

    def test_integral_float_inventory_indexes(self):
        """Review r4187464393: JSON `0.0` and `0e0` are integers to the schema."""
        rows = self.tool()["outcomes"]["mapping"]
        rows[0]["inventory"] = json.loads("0.0")
        rows[2]["inventory"] = json.loads("1e0")
        self.assertValidWithGaps()

    # ---- H3: outcome inventories across union branches ---------------------

    def error_union(self, name="domain-error.json", *, required_code=True):
        """Codex-shaped: a root object whose `error` is a `$ref` to a `oneOf` of `$ref`
        branches, each an object carrying its code in `properties.code.const`."""
        def branch(code, retryable):
            return {"type": "object", "additionalProperties": False,
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
                            "error": {"oneOf": [{"$ref": "#/$defs/unavailableError"},
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

    def test_symlink_loop_is_refused_not_raised(self):
        """Review r4187464151: a symlink loop is a refusal, never a crash."""
        (self.root / "loop.json").symlink_to(self.root / "loop.json")
        self.tool()["input"]["path"] = "loop.json"
        self.assertDiagnostics([("unsafe_reference_path", "/tools/0/input")])

    def test_references_must_target_schemas(self):
        """Review r4187464184: a `$ref` into annotation data is not a schema."""
        for target, extra, code in [
                ("#/examples/0", {"examples": [{"type": 7}]}, "invalid_referenced_schema"),
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
        self.doc["service"] = {"deployment": "deployed", "installation": "synthetic",
            "environment": "test", "canonical_resource_uri": "relative/path"}
        with patch.dict(self.module.FormatChecker.checkers, {}, clear=True):
            self.assertDiagnostics([("invalid_resource_uri", "/service/canonical_resource_uri")])
            self.doc["service"]["canonical_resource_uri"] = "https://mcp.example.test/"
            self.assertValidWithGaps()

    def test_resource_uri_is_https_without_fragment_or_userinfo(self):
        """L2: a canonical resource URI is an absolute https URI with no fragment or userinfo."""
        self.doc["service"] = {"deployment": "deployed", "installation": "synthetic",
            "environment": "test", "canonical_resource_uri": "https://mcp.example.test/mcp"}
        with patch.dict(self.module.FormatChecker.checkers, {}, clear=True):
            self.assertValidWithGaps()
        for uri in ["http://mcp.example.test/mcp", "https://mcp.example.test/mcp#frag",
                    "https://user@mcp.example.test/mcp", "https://user:pw@mcp.example.test/mcp",
                    "javascript:alert(1)", "urn:example:mcp", "https:///mcp", "https://mcp.example.test:99999/",
                    "https://mcp.example.test/m cp", "https://mcp.example.test/\x00",
                    "https://mcp.example.test\\evil"]:
            with self.subTest(uri=uri):
                self.doc["service"]["canonical_resource_uri"] = uri
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


if __name__ == "__main__":
    unittest.main()
