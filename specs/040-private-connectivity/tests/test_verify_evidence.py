"""Regression checks for feature 040 evidence acceptance."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


HERE = Path(__file__).resolve().parents[1]
MODULE = importlib.util.spec_from_file_location("evidence_checker", HERE / "verify-evidence.py")
CHECKER = importlib.util.module_from_spec(MODULE)
MODULE.loader.exec_module(CHECKER)
REV = "git:" + "a" * 40 + ":synthetic/result.json"
ALT = "git:" + "b" * 40 + ":synthetic/result.json"


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.scopes = {}
        for scope in CHECKER.SCOPE_NAMES:
            self.scopes[scope] = {
                "owner": "synthetic-" + scope,
                "repository": "synthetic/" + scope,
                "approval_ref": REV,
                "file_scope": "synthetic/",
                "release_path": "synthetic-candidate",
                "verify": "synthetic-owner-check",
            }
        self.write("T001", {"task": "T001", "verdict": "pass", "scopes": self.scopes})

    def write(self, task, record):
        (self.root / (task + ".json")).write_text(json.dumps(record, indent=2) + "\n")

    def make(self, task):
        path = self.root / (task + ".json")
        if path.exists():
            return json.loads(path.read_text())
        for dep in CHECKER.DEPENDENCIES[task]:
            if dep != "T001":
                self.make(dep)
        scope = CHECKER.TASK_SCOPE[task]
        record = {
            "task": task, "verdict": "pass", "scope": scope,
            "owner": self.scopes[scope]["owner"], "approval_ref": REV,
            "decision_ref": REV, "revision_ref": REV,
            "dependencies": {
                dep: hashlib.sha256((self.root / (dep + ".json")).read_bytes()).hexdigest()
                for dep in CHECKER.DEPENDENCIES[task]
            },
            "cases": {},
        }
        for case in CHECKER.CASES[task].split():
            outcome = "denied" if case in CHECKER.DENIAL_CASES else "verified"
            record["cases"][case] = {
                "expected": outcome, "observed": outcome, "evidence_ref": REV,
                "checks": {
                    check: {"passed": True, "evidence_ref": REV}
                    for check in CHECKER.SUBCHECKS.get((task, case), "result").split()
                },
            }
        if task in CHECKER.IMPLEMENTATION_TASKS:
            record["owner_check"] = {"command": "synthetic-owner-check", "exit_status": 0, "output_ref": REV}
        if task == "T003":
            record["limits"] = {
                "revocation_seconds": 300, "restore_seconds": 3600,
                "backup_age_seconds": 86400, "rollback_seconds": 900,
                "probe_interval_seconds": 10, "sustained_denial_seconds": 30,
            }
        if task in CHECKER.LIVE_TASKS:
            record.update({
                "run_ref": REV, "candidate_pins": {name: REV for name in set(CHECKER.LIVE_REVISION_PINS.values())},
                "policy_baseline": {"tenant-a": REV, "tenant-b": REV},
            })
            if task not in {"T006", "T021"}:
                record["positive_controls"] = {
                    key: {"reachable": True, "evidence_ref": REV}
                    for key in record["policy_baseline"]
                }
        if task == "T018":
            for case in record["cases"].values():
                case["metrics"] = {
                    "elapsed_seconds": 100, "max_probe_gap_seconds": 10,
                    "sustained_denial_seconds": 30, "allowed_after_deadline": False,
                    "quarantine_used": False,
                }
        if task == "T019":
            record["cases"]["restore-timing"]["elapsed_seconds"] = 1800
            record["cases"]["backup-age"]["elapsed_seconds"] = 3600
        if task == "T020":
            record["cases"]["rollback-timing"]["elapsed_seconds"] = 600
        if task == "T021":
            record["signoffs"] = {
                role: REV for role in ("rollout_lead", "installer", "ops", "hosted_product", "hosted_domain")
            }
        self.write(task, record)
        return record

    def verify(self, task):
        return CHECKER.verify_file(self.root / (task + ".json"), task)

    def reject(self, task, record):
        self.write(task, record)
        with self.assertRaises(CHECKER.EvidenceError):
            self.verify(task)

    def test_all_records_and_complete_gate_chain(self):
        self.make("T021")
        for task in ["T001"] + list(CHECKER.CASES):
            with self.subTest(task=task):
                self.verify(task)

    def test_missing_unknown_and_wrong_outcome_cases(self):
        original = self.make("T004")
        for case in ("missing", "unknown", "outcome", "subcheck"):
            record = copy.deepcopy(original)
            if case == "missing":
                del record["cases"]["routes"]
            if case == "unknown":
                record["cases"]["unexpected"] = record["cases"].pop("routes")
            if case == "outcome":
                record["cases"]["routes"]["observed"] = "denied"
            if case == "subcheck":
                del record["cases"]["binding-scope"]["checks"]["wrong-customer"]
            with self.subTest(case=case):
                self.reject("T004", record)

    def test_wrong_task_scope_owner_and_approval(self):
        original = self.make("T004")
        for field, value in (("task", "T005"), ("scope", "installer"),
                             ("owner", "someone-else"), ("approval_ref", ALT)):
            record = copy.deepcopy(original)
            record[field] = value
            with self.subTest(field=field):
                self.reject("T004", record)

    def test_failed_owner_check_and_substituted_command(self):
        original = self.make("T004")
        for field, value in (("exit_status", 1), ("exit_status", False),
                             ("command", "true"), ("output_ref", "TODO")):
            record = copy.deepcopy(original)
            record["owner_check"][field] = value
            with self.subTest(field=field, value=value):
                self.reject("T004", record)

    def test_required_dependency_not_skipped(self):
        record = self.make("T012")
        del record["dependencies"]["T006"]
        self.reject("T012", record)

    def test_changed_and_failed_dependency(self):
        self.make("T006")
        record = json.loads((self.root / "T003.json").read_text())
        record["limits"]["revocation_seconds"] = 299
        self.write("T003", record)
        with self.assertRaises(CHECKER.EvidenceError):
            self.verify("T006")
        record["verdict"] = "fail"
        self.reject("T003", record)

    def test_cross_run_pin_and_policy_changes(self):
        original = self.make("T012")
        for field in ("run_ref", "candidate_pins", "policy_baseline"):
            record = copy.deepcopy(original)
            record[field] = ALT if field == "run_ref" else {"other": ALT}
            with self.subTest(field=field):
                self.reject("T012", record)

    def test_live_tested_revision_must_equal_approved_owner_candidate(self):
        for task in CHECKER.LIVE_REVISION_PINS:
            record = self.make(task)
            record["revision_ref"] = ALT
            with self.subTest(task=task):
                self.reject(task, record)
            record["revision_ref"] = REV
            self.write(task, record)

    def test_positive_control_required_for_every_boundary(self):
        original = self.make("T012")
        for missing in (True, False):
            record = copy.deepcopy(original)
            if missing:
                del record["positive_controls"]["tenant-b"]
            else:
                record["positive_controls"]["tenant-a"]["reachable"] = False
            self.reject("T012", record)

    def test_revocation_metrics(self):
        original = self.make("T018")
        for field, value in (
            ("elapsed_seconds", 301), ("elapsed_seconds", -1),
            ("elapsed_seconds", float("nan")), ("elapsed_seconds", True),
            ("max_probe_gap_seconds", 11), ("sustained_denial_seconds", 29),
            ("allowed_after_deadline", True), ("quarantine_used", True),
        ):
            record = copy.deepcopy(original)
            record["cases"]["direct-existing"]["metrics"][field] = value
            with self.subTest(field=field, value=value):
                self.reject("T018", record)

    def test_restore_backup_and_rollback_windows(self):
        self.make("T020")
        for task, case, value in (("T019", "restore-timing", 3601),
                                 ("T019", "backup-age", 86401),
                                 ("T020", "rollback-timing", 901)):
            original = self.make(task)
            record = copy.deepcopy(original)
            record["cases"][case]["elapsed_seconds"] = value
            with self.subTest(task=task, case=case):
                self.reject(task, record)
            self.write(task, original)

    def test_missing_approved_limits_and_invalid_probe_interval(self):
        original = self.make("T003")
        for mutate in ("missing", "probe"):
            record = copy.deepcopy(original)
            if mutate == "missing":
                del record["limits"]["rollback_seconds"]
            else:
                record["limits"]["probe_interval_seconds"] = 11
            self.reject("T003", record)

    def test_signoff_and_immutable_source_required(self):
        original = self.make("T021")
        record = copy.deepcopy(original)
        del record["signoffs"]["ops"]
        self.reject("T021", record)
        record = copy.deepcopy(original)
        record["cases"]["four-paths"]["evidence_ref"] = "https://github.com/org/repo/blob/main/result"
        self.reject("T021", record)

    def test_duplicates_invalid_json_and_credentials(self):
        path = self.root / "T003.json"
        for raw in ('{"task":"T003","task":"T003","verdict":"pass"}', '[1]', '{'):
            path.write_text(raw)
            with self.assertRaises(CHECKER.EvidenceError):
                self.verify("T003")
        record = self.make("T004")
        record["secret"] = "-----BEGIN PRIVATE KEY-----"
        self.reject("T004", record)

    def test_symlinked_dependency_is_rejected(self):
        self.make("T004")
        original = self.root / "T001.json"
        target = self.root / "saved.json"
        original.rename(target)
        original.symlink_to(target)
        with self.assertRaises(CHECKER.EvidenceError):
            self.verify("T004")

    def test_cli_returns_nonzero_for_blocked_record(self):
        self.make("T003")
        record = self.make("T003")
        record["verdict"] = "blocked"
        self.write("T003", record)
        self.assertEqual(CHECKER.main(["--task", "T003", str(self.root / "T003.json")]), 1)


if __name__ == "__main__":
    unittest.main()
