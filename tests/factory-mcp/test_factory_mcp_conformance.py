"""Synthetic conformance witnesses; no domain code or network is needed."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/validate-factory-mcp.py"

def load():
    spec = importlib.util.spec_from_file_location("factory_mcp", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class ConformanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.revision = "a" * 40
        self.schema = {"$schema": "https://json-schema.org/draft/2020-12/schema",
                       "type": "object", "properties": {
                           "status": {"enum": ["positive", "negative"]},
                           "code": {"oneOf": [{"const": "UNAVAILABLE"}, {"const": "INVALID"}]}}}
        self.write_schema()
        self.doc = self.declaration()
        self.module = load()

    def write_schema(self):
        data = json.dumps(self.schema).encode()
        (self.root / "outcome.json").write_bytes(data)
        self.ref = {"repository": "synthetic", "revision": self.revision,
                    "path": "outcome.json", "sha256": hashlib.sha256(data).hexdigest()}

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

    def test_valid_with_gaps_is_not_certification(self):
        report = self.validate()
        self.assertEqual(report["status"], "valid-with-gaps")
        self.assertFalse(report["verified_conformance"])
        self.assertTrue(all(report["checks"].values()))
        self.assertEqual(report, self.validate())

    def test_closed_shapes(self):
        for mutate in [
            lambda t: t.update(owner="other"),
            lambda t: t["effects"].update(mutation=True),
            lambda t: t["effects"].update(authority_effect="approve"),
            lambda t: t["binding"].update(authority_source="caller"),
            lambda t: t["limits"].update(request_bytes=True),
            lambda t: t["outcomes"].update(structured_content="wrapped"),
            lambda t: t["evidence_policy"].update(raw_credentials=True),
            lambda t: t.update(unrecognized=True),
        ]:
            with self.subTest(mutate=mutate):
                self.doc = self.declaration()
                mutate(self.doc["tools"][0])
                self.assertEqual(self.validate()["status"], "invalid")

    def test_outcomes_exhaustive_and_typed(self):
        for action in ["missing", "extra", "duplicate", "class", "is_error", "inventory"]:
            with self.subTest(action=action):
                self.doc = self.declaration()
                rows = self.doc["tools"][0]["outcomes"]["mapping"]
                if action == "missing": rows.pop()
                elif action == "extra": rows[0]["value"] = "unrecognized"
                elif action == "duplicate": rows.append(rows[0].copy())
                elif action == "class": rows[-1]["class"] = "completed_evaluation"
                elif action == "is_error": rows[-1]["is_error"] = False
                else: rows[0]["inventory"] = 20
                self.assertEqual(self.validate()["status"], "invalid")

    def test_unresolvable_vocabulary_requires_gap(self):
        self.schema["properties"]["status"] = {"type": "string"}
        self.write_schema()
        self.doc = self.declaration()
        self.assertEqual(self.validate()["status"], "invalid")
        self.doc["gaps"].append({"id": "vocab-gap", "concerns": ["outcomes"], "description": "Not finite."})
        t = self.doc["tools"][0]
        t["gap_ids"].append("vocab-gap")
        t["outcomes"]["inventories"][0]["gap_id"] = "vocab-gap"
        self.assertEqual(self.validate()["status"], "valid-with-gaps")

    def test_repetition_cross_checks(self):
        t = self.doc["tools"][0]
        t["repetition"] = {"mode": "fresh_observation", "deadline": "host_monotonic",
            "trace_ids_are_authority": False, "maximum_age_source": "host",
            "original_timestamps": True, "final_age_check": True}
        self.assertEqual(self.validate()["status"], "invalid")
        t["effects"]["external_reads"] = True
        t["evidence_policy"]["observation_time"] = True
        self.assertEqual(self.validate()["status"], "valid-with-gaps")
        t["repetition"] = {"mode": "lease_replay", "deadline": "host_monotonic",
            "trace_ids_are_authority": False, "key_scope": "principal", "conflict": "reject",
            "in_progress": "explicit", "coordination": "atomic_external", "preserve_timestamps": True}
        self.assertEqual(self.validate()["status"], "invalid")
        t["effects"]["persistence"] = True
        self.assertEqual(self.validate()["status"], "valid-with-gaps")

    def test_support_and_unique_identity(self):
        for action in ["duplicate_tool", "duplicate_id", "missing_id", "audit", "execution", "scope"]:
            with self.subTest(action=action):
                self.doc = self.declaration()
                t = self.doc["tools"][0]
                if action == "duplicate_tool": self.doc["tools"].append(copy.deepcopy(t))
                elif action == "duplicate_id": self.doc["gaps"].append(copy.deepcopy(self.doc["gaps"][0]))
                elif action == "missing_id": t["evidence_ids"] = ["missing"]
                elif action == "audit": t["gap_ids"] = []
                elif action == "execution": t["effects"]["execution"] = True
                else: t["binding"]["scope_references"] = []
                self.assertEqual(self.validate()["status"], "invalid")

    def test_reference_integrity(self):
        for bad in ["/tmp/outcome.json", "../outcome.json", "https://invalid.test/s.json", "absent.json"]:
            with self.subTest(path=bad):
                self.doc = self.declaration()
                self.doc["tools"][0]["input"]["path"] = bad
                self.assertNotEqual(self.validate()["status"], "valid-with-gaps")
        self.doc = self.declaration()
        self.doc["tools"][0]["input"]["sha256"] = "0" * 64
        self.assertEqual(self.validate()["status"], "invalid")
        self.doc = self.declaration()
        self.assertEqual(self.validate({})["exit_code"], 2)

    def test_symlink_escape(self):
        with tempfile.TemporaryDirectory() as outside:
            target = Path(outside) / "outside.json"
            target.write_text("{}")
            (self.root / "escape.json").symlink_to(target)
            self.doc["tools"][0]["input"]["path"] = "escape.json"
            self.assertEqual(self.validate()["status"], "invalid")

    def test_nested_remote_and_bad_local_reference(self):
        for ref in ["https://invalid.test/a.json", "../a.json", "/tmp/a.json", "#/missing"]:
            with self.subTest(ref=ref):
                self.schema["properties"]["nested"] = {"$ref": ref}
                self.write_schema()
                self.doc = self.declaration()
                self.assertEqual(self.validate()["status"], "invalid")

    def test_recursive_local_schema_without_fetch(self):
        self.schema["properties"]["recursive"] = {"$ref": "#"}
        self.write_schema()
        self.doc = self.declaration()
        self.assertEqual(self.validate()["status"], "valid-with-gaps")

    def test_cli_exit_codes(self):
        path = self.root / "declaration.json"
        path.write_text(json.dumps(self.doc))
        run = subprocess.run([sys.executable, str(SCRIPT), str(path), "--json",
                "--snapshot", f"synthetic@{self.revision}={self.root}"], capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)["status"], "valid-with-gaps")
        run = subprocess.run([sys.executable, str(SCRIPT), str(path), "--json"], capture_output=True, text=True)
        self.assertEqual(run.returncode, 2)
        path.write_text("{")
        run = subprocess.run([sys.executable, str(SCRIPT), str(path), "--json"], capture_output=True, text=True)
        self.assertEqual(run.returncode, 1)

    def test_contained_local_reference_is_pinned(self):
        other = {"type": "string", "enum": ["positive", "negative"]}
        raw = json.dumps(other).encode()
        (self.root / "local.json").write_bytes(raw)
        self.schema["properties"]["status"] = {"$ref": "local.json"}
        self.write_schema()
        self.doc = self.declaration()
        self.assertEqual(self.validate()["status"], "invalid")
        self.doc["source"]["artifacts"].append({**self.ref, "path": "local.json",
            "sha256": hashlib.sha256(raw).hexdigest()})
        self.assertEqual(self.validate()["status"], "valid-with-gaps")

    def test_data_keywords_do_not_execute_references(self):
        self.schema["examples"] = [{"$ref": "https://invalid.test/data-not-a-schema"}]
        self.write_schema()
        self.doc = self.declaration()
        self.assertEqual(self.validate()["status"], "valid-with-gaps")

    def test_unsupported_constraints_do_not_claim_exhaustiveness(self):
        self.schema["properties"]["status"]["pattern"] = "^positive$"
        self.write_schema()
        self.doc = self.declaration()
        self.assertEqual(self.validate()["status"], "invalid")

    def test_reference_checks_never_open_network(self):
        from unittest.mock import patch
        self.schema["properties"]["nested"] = {"$ref": "https://invalid.test/schema"}
        self.write_schema()
        self.doc = self.declaration()
        with patch("socket.socket", side_effect=AssertionError("network forbidden")):
            self.assertEqual(self.validate()["status"], "invalid")

    def test_resource_identity_without_optional_format_checker(self):
        from unittest.mock import patch
        self.doc["service"] = {"deployment": "deployed", "installation": "synthetic",
            "environment": "test", "canonical_resource_uri": "relative/path"}
        with patch.dict(self.module.FormatChecker.checkers, {}, clear=True):
            self.assertEqual(self.validate()["status"], "invalid")
            self.doc["service"]["canonical_resource_uri"] = "https://mcp.example.test/"
            self.assertEqual(self.validate()["status"], "valid-with-gaps")

if __name__ == "__main__":
    unittest.main()
