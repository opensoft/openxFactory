"""Synthetic source regressions. These fixtures are never qualification evidence."""

from copy import deepcopy
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import subprocess

import pytest


ROOT = Path(__file__).resolve().parents[3]
MODULE = ROOT / "specs/043-private-connectivity-production/verify-evidence.py"
SPEC = importlib.util.spec_from_file_location("production_evidence_043", MODULE)
v = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(v)
TASKS = v.load_contract(ROOT)
NOW = datetime(2030, 1, 2, tzinfo=timezone.utc)
START = "2030-01-01T00:00:00Z"
END = "2030-01-01T00:01:00Z"


class MemoryObjects:
    """Content-addressed immutable objects; no provider or actual customer data."""

    def __init__(self):
        self.objects = {}
        self.diffs = {}

    def put(self, data, path="exports/output.json", repository=v.COORDINATOR, revision=None):
        data = data if isinstance(data, bytes) else json.dumps(data, sort_keys=True).encode()
        sha = v.digest(data)
        revision = revision or sha[:40]
        key = (repository, revision, path)
        assert key not in self.objects or self.objects[key] == data
        self.objects[key] = data
        return dict(repository=repository, commit=revision, path=path, sha256=sha)

    def blob(self, ref):
        v.reference(ref)
        data = self.objects[(ref["repository"], ref["commit"], ref["path"])]
        v.require(v.digest(data) == ref["sha256"], "immutable content digest mismatch")
        return data

    def changed(self, source):
        return self.diffs[(source["repository"], source["revision"])]


class World:
    def __init__(self):
        self.store = MemoryObjects()
        self.review = self.store.put(b"SYNTHETIC independent test review", "reviews/source.txt")
        self.trust = dict(schema="043-reviewed-trust-v1", feature=v.FEATURE, definition=v.DEFINITION,
                          custodian="Brett Heap", review=self.review, custody=dict(kind="source-git"),
                          repositories={"C": v.COORDINATOR, "L": "opensoft/headscale-install", "I": "opensoft/xfactory-installer",
                                        "H": "opensoft/openxsoft-hosted-services", "O": "opensoft/opsxfactory", "D": "test/domain"},
                          revoked_authorities=[], bindings={}, instances={}, aggregates={})
        self.records, self.outputs = {}, {}

    def decision(self, kind, scope):
        return self.store.put(dict(id=kind + "-" + v.digest(json.dumps(scope, sort_keys=True).encode()), kind=kind,
                                   decision="accepted", scope=scope, owner="Synthetic Owner",
                                   valid_from="2029-01-01T00:00:00Z", valid_until="2031-01-01T00:00:00Z"), "decisions/" + kind + ".json")

    def add(self, task, instance=None, scope_changes=None, dependencies=None, decisions=None):
        if task in v.INSTANCE_TASKS and instance is None:
            if task not in self.trust["aggregates"]:
                self.child(task)
                self.aggregate(task)
            return task
        key = task + ("@" + instance if instance else "")
        if key in self.trust["bindings"]:
            return key
        definition = TASKS[task]
        repo = self.trust["repositories"][definition["owner"]]
        changes = set()
        for envelope in definition["files"]:
            changes.add(envelope + "synthetic.txt" if envelope.endswith("/") else envelope)
        source = dict(repository=repo, base="a" * 40, revision=v.digest(key.encode())[:40])
        self.store.diffs[(repo, source["revision"])] = changes
        scope = {field: "not-applicable" for field in v.SCOPE_FIELDS}
        scope.update(run="synthetic-run", candidate="synthetic-candidate", environment="source", phase="source", offering="hosted-headscale")
        if 50 <= int(task[1:]) <= 64:
            scope["phase"] = "staging" if int(task[1:]) <= 56 else "production"
        scope.update(scope_changes or {})
        dependencies = dependencies or {dep: self.add(dep) for dep in definition["dependencies"]}
        binding = dict(task=task, instance=instance, owner=definition["owner"], scope=scope, source=source,
                       files=sorted(changes), command=definition["command"], roles=["synthetic-owner"], decisions=decisions or [],
                       incidents=[], cases={name: [dict(id="actual-identity", kind="equal", expected="observed-original-subject")]
                              for name in definition["cases"]}, dependencies=dependencies, history=[], remediation=None,
                       metrics={}, observation=None, ci={}, artifacts=[], **{"class": definition["class"]})
        if int(task[1:]) >= 10:
            binding["command"] = "synthetic-owner-tool --task " + task
        if definition["class"].startswith("CI-"):
            binding["ci"] = {"tests/synthetic.py": 3}
        if task == "T010":
            binding["ci"] = {v.FEATURE_PATH + "/tests/" + name: 3 for name in ("test_evidence.py", "test_evidence_pins.py")}
        if task == "T051":
            binding["decisions"] = [f"C-{i:02}" for i in range(3, 9)]
        if scope["phase"] in ("staging", "production"):
            if "C-08" not in binding["decisions"]:
                binding["decisions"].append("C-08")
            self.trust["live_custody"] = dict(kind="protected", decision="C-08")
            binding["metrics"] = {"synthetic-latency": dict(minimum=0, maximum=10, unit="seconds", event="probe")}
            binding["observation"] = dict(window=[START, END], max_gap_seconds=0, minimum_observed_seconds=60)
        self.trust["bindings"][key] = binding
        if instance:
            self.trust["instances"].setdefault(task, []).append(instance)
        decision = dict(id="authority-" + key, owner="Synthetic Owner", roles=binding["roles"], decision="accepted", scope=scope,
                        valid_from="2029-01-01T00:00:00Z", valid_until="2031-01-01T00:00:00Z", mode="source",
                        decisions={d: self.decision(d, scope) for d in binding["decisions"]})
        if scope["phase"] != "source":
            decision.update(mode="customer", consent=self.decision("consent", scope))
        binding["authority"] = self.store.put(decision, "decisions/" + key + ".json")
        artifact_path = next(iter(changes))
        paths = set(changes)
        if int(task[1:]) < 10:
            for envelope in definition["files"]:
                if envelope.endswith("/") and envelope.startswith("openspec/"):
                    paths.update((envelope + "proposal.md", envelope + ".openspec.yaml"))
        binding["artifacts"] = [] if task == "T002" else [self.store.put(b"SYNTHETIC source artifact", path, repo, source["revision"]) for path in paths
                                                         if task != "T006" or not path.startswith("openspec/")]
        if task == "T002":
            old = self.store.put(dict(verdict="pass"), "specs/040-private-connectivity/evidence/T021.json", repo, source["revision"])
            baseline = self.store.put(dict(evidence_class="historical-lab", authorizes_production=False, evidence_sha256=old["sha256"]),
                                      v.FEATURE_PATH + "/evidence/baseline.json", repo, source["revision"])
            binding["artifacts"] = [old, baseline]
        if task == "T006":
            base = "openspec/changes/commission-private-connectivity-production-evidence/"
            binding["artifacts"] += [self.store.put(data, base + name, repo, source["revision"]) for name, data in
                                    (("proposal.md", b"Status: ratified"), ("review/ratification.md", b"Ratified: by test owner"),
                                     (".openspec.yaml", b"origin:\n  approved_by: Synthetic Owner"))]
        record = dict(schema="043-bootstrap-import-v1" if int(task[1:]) < 10 else "043-task-evidence-v1",
                      task=task, instance=instance, owner=binding["owner"], evidence_class=binding["class"], scope=scope,
                      attempt="attempt-1", verdict="pass", source=source, command=binding["command"], authority=binding["authority"],
                      artifacts=binding["artifacts"], incidents=[], history=[], dependencies={d: self.ref(k) for d, k in dependencies.items()})
        output = {field: deepcopy(record[field]) for field in ("task", "instance", "scope", "source", "command")}
        output.update(exit_code=0, started_at=START, ended_at=END, events={}, metrics={}, coverage=None,
                      cases=[dict(id=name, scope=deepcopy(scope), source=deepcopy(source), checks=[dict(id="actual-identity", observed="observed-original-subject")]) for name in definition["cases"]],
                      ci={suite: dict(repository=repo, revision=source["revision"], conclusion="success", required=True,
                                      collected=count, passed=count, skipped=0, run_id=101, job_id=201) for suite, count in binding["ci"].items()})
        if scope["phase"] != "source":
            output.update(events=dict(probe=START), metrics={"synthetic-latency": dict(value=1, unit="seconds", event="probe")},
                          coverage=dict(window=[START, END], intervals=[[START, END]]))
        self.records[key], self.outputs[key] = record, output
        self.publish(key)
        return key

    def ref(self, key):
        if key in v.INSTANCE_TASKS:
            return self.trust["aggregates"][key]
        return self.trust["bindings"][key]["record"]

    def publish(self, key):
        record = self.records[key]
        binding = self.trust["bindings"][key]
        record["output"] = self.store.put(self.outputs[key], "outputs/" + key + ".json")
        number = int(binding["task"][1:])
        owner = binding["owner"]
        prefix = v.FEATURE_PATH + "/evidence/" if owner == "C" else "evidence/private-connectivity-production/"
        path = "exports/" + key + ".import.json" if number < 10 else prefix + binding["task"] + ".json"
        if binding["instance"]:
            path = prefix + "instances/" + binding["task"] + "/" + binding["instance"] + ".json"
            if path not in binding["files"]: binding["files"].append(path)
        repository = self.trust["repositories"][owner] if number >= 10 else v.COORDINATOR
        binding["record"] = self.store.put(record, path, repository)

    def verifier(self):
        anchor = self.store.put(self.trust, "commissioning/reviewed-manifest.json")
        return v.Verifier(TASKS, self.store, anchor, now=NOW)

    def check(self, key):
        self.publish(key)
        self.verifier().verify(key)

    def child(self, task, instance="service", scope_changes=None, decisions=None):
        deps = {}
        for dep in TASKS[task]["dependencies"]:
            deps[dep] = self.child(dep, instance, scope_changes) if dep in v.INSTANCE_TASKS else self.add(dep)
        defaults = {"T057": ["C-09"], "T058": ["C-09"], "T061": ["C-10"],
                    "T062": ["C-11"], "T063": ["C-11"], "T064": ["C-11"]}
        selected = list(decisions if decisions is not None else defaults.get(task, []))
        if decisions is None and task in ("T062", "T063", "T064") and (scope_changes or {}).get("wave", "not-applicable") != "not-applicable":
            selected.append("C-12")
        return self.add(task, instance, scope_changes, deps, selected)

    def aggregate(self, task):
        data = dict(schema="043-instance-aggregate-v1", task=task,
                    children={i: self.ref(task + "@" + i) for i in self.trust["instances"][task]})
        owner = TASKS[task]["owner"]
        prefix = v.FEATURE_PATH + "/evidence/" if owner == "C" else "evidence/private-connectivity-production/"
        self.trust["aggregates"][task] = self.store.put(data, prefix + task + ".json", self.trust["repositories"][owner])
        return self.store.blob(self.trust["aggregates"][task])


@pytest.fixture
def world():
    return World()


def source_container_world():
    """New commissioning format, built only from synthetic original Git blobs."""
    world = World()
    world.add("T010")
    objects = {}
    def contain(name, task, value):
        objects[name] = dict(tasks=[task], evidence_class="source", value=deepcopy(value))
        return {"object": name}
    for task in sorted(world.trust["bindings"]):
        binding, record = world.trust["bindings"][task], world.records[task]
        authority = v.decode(world.store.blob(binding["authority"]))
        for kind, ref in authority["decisions"].items():
            authority["decisions"][kind] = contain(task + "-" + kind, task, v.decode(world.store.blob(ref)))
        binding["authority"] = contain(task + "-authority", task, authority)
        record["authority"] = binding["authority"]
        record["output"] = contain(task + "-output", task, world.outputs[task])
        record["dependencies"] = {dep: world.ref(selected) for dep, selected in binding["dependencies"].items()}
        if int(task[1:]) < 10:
            binding["record"] = contain(task + "-import", task, record)
        else:
            binding["record"] = world.store.put(record, v.FEATURE_PATH + "/evidence/T010.json")
    world.trust["source_container"] = dict(schema="043-source-container-v1", objects=objects)
    return world


def source_anchor(world, *, accepted=True, mutate_review=None):
    pending = dict(schema="043-source-authentication-v1", decision="pending", custodian="Brett Heap",
                   reviewed_manifest=None, content_sha256=None, reviewed_at=None)
    def publish_review(value):
        fence = bytes([96]) * 3
        return world.store.put(b"# SYNTHETIC custody review\n\n" + fence + b"json\n" + v.canonical_json(value) + b"\n" + fence + b"\n",
                               v.AUTHENTICATION_PATH)
    world.trust["review"] = publish_review(pending)
    first = world.store.put(world.trust, v.COMMISSIONING_PATH)
    if accepted:
        review = dict(pending, decision="accepted", reviewed_manifest=first,
                      content_sha256=v.commissioning_digest(world.trust), reviewed_at="2030-01-01T01:00:00Z")
        if mutate_review:
            mutate_review(review)
        world.trust["review"] = publish_review(review)
    return world.store.put(world.trust, v.COMMISSIONING_PATH)


def test_contained_bootstrap_and_distinct_git_receipt_verify_without_self_hash():
    world = source_container_world()
    anchor = source_anchor(world)
    reader = v.Verifier(TASKS, world.store, anchor, now=NOW)
    before = deepcopy(world.store.objects)
    reader.verify("T010")
    assert reader.cache == {f"T{i:03}" for i in range(1, 11)}
    assert world.store.objects == before
    assert all(set(world.ref(f"T{i:03}")) == {"object"} for i in range(1, 10))
    assert set(world.ref("T010")) == v.REF_FIELDS
    assert world.ref("T010")["commit"] != anchor["commit"]


@pytest.mark.parametrize("prepare", [False, True])
def test_pending_container_never_satisfies_task_or_aggregate(prepare):
    world = source_container_world()
    anchor = source_anchor(world, accepted=False)
    with pytest.raises(v.EvidenceError, match="authentication pending"):
        reader = v.Verifier(TASKS, world.store, anchor, now=NOW, prepare=prepare)
        reader.verify("T010")
    if prepare:
        reader = v.Verifier(TASKS, world.store, anchor, now=NOW, prepare=True)
        with pytest.raises(v.EvidenceError, match="authentication pending"):
            reader.aggregate("T057", b"{}")


@pytest.mark.parametrize("mutation", ["missing", "cycle", "self-cycle", "extra-ref-field", "bad-id",
                                      "unknown-task", "duplicate-task", "live-task", "foreign-owner",
                                      "wrong-class", "array-value", "unused-missing"])
def test_contained_table_is_closed_and_source_only(mutation):
    world = source_container_world()
    objects = world.trust["source_container"]["objects"]
    entry = objects["T007-output"]
    if mutation == "missing": del objects["T007-output"]
    if mutation == "cycle":
        entry["value"]["nested"] = {"object": "T007-authority"}
        objects["T007-authority"]["value"]["nested"] = {"object": "T007-output"}
    if mutation == "self-cycle": entry["value"]["nested"] = {"object": "T007-output"}
    if mutation == "extra-ref-field": world.trust["bindings"]["T007"]["record"]["path"] = "elsewhere"
    if mutation == "bad-id": objects["../escape"] = deepcopy(entry)
    if mutation == "unknown-task": entry["tasks"] = ["T999"]
    if mutation == "duplicate-task": entry["tasks"] *= 2
    if mutation == "live-task": entry["tasks"] = ["T052"]
    if mutation == "foreign-owner": entry["tasks"] = ["T011"]
    if mutation == "wrong-class": entry["evidence_class"] = "staging"
    if mutation == "array-value": entry["value"] = []
    if mutation == "unused-missing":
        objects["unused"] = dict(tasks=["T007"], evidence_class="source", value={"nested": {"object": "absent"}})
    with pytest.raises(v.EvidenceError):
        v.Verifier(TASKS, world.store, source_anchor(world), now=NOW)


@pytest.mark.parametrize("mutation", ["task", "scope", "source", "command", "case", "exit"])
def test_authenticated_container_still_checks_original_output_identity(mutation):
    world = source_container_world()
    output = world.trust["source_container"]["objects"]["T007-output"]["value"]
    if mutation == "task": output["task"] = "T008"
    if mutation == "scope": output["scope"]["customer"] = "other-customer"
    if mutation == "source": output["source"]["revision"] = "f" * 40
    if mutation == "command": output["command"] = "echo pass"
    if mutation == "case": output["cases"] = []
    if mutation == "exit": output["exit_code"] = 1
    with pytest.raises(v.EvidenceError):
        v.Verifier(TASKS, world.store, source_anchor(world), now=NOW).verify("T007")


def test_contained_object_cannot_be_borrowed_by_different_task_or_live_scope():
    world = source_container_world()
    reader = v.Verifier(TASKS, world.store, source_anchor(world), now=NOW)
    binding = deepcopy(world.trust["bindings"]["T007"])
    with pytest.raises(v.EvidenceError, match="task substitution"):
        reader.read({"object": "T008-output"}, binding)
    for field, value in [("owner", "L"), ("task", "T011"), ("scope", dict(binding["scope"], phase="staging"))]:
        altered = dict(binding, **{field: value})
        with pytest.raises(v.EvidenceError, match="outside E source"):
            reader.read({"object": "T007-output"}, altered)
    with pytest.raises(v.EvidenceError, match="outside E source"):
        reader.read({"object": "T007-output"})


@pytest.mark.parametrize("field,value", [
    ("decision", "pending"), ("custodian", "Other Owner"), ("content_sha256", "0" * 64),
    ("reviewed_at", "2040-01-01T00:00:00Z"), ("reviewed_at", "2029-01-01T00:00:00Z"),
    ("reviewed_manifest", dict(repository=v.COORDINATOR, commit="f" * 40, path="other.json", sha256="f" * 64)),
])
def test_actual_authentication_must_match_concrete_manifest_and_run(field, value):
    world = source_container_world()
    anchor = source_anchor(world, mutate_review=lambda review: review.update({field: value}))
    with pytest.raises(v.EvidenceError):
        v.Verifier(TASKS, world.store, anchor, now=NOW).verify("T010")


def test_changing_authenticated_payload_or_binding_requires_new_human_review():
    world = source_container_world()
    anchor = source_anchor(world)
    world.trust["source_container"]["objects"]["T007-output"]["value"]["exit_code"] = 1
    substituted = world.store.put(world.trust, v.COMMISSIONING_PATH)
    with pytest.raises(v.EvidenceError, match="authentication content mismatch"):
        v.Verifier(TASKS, world.store, substituted, now=NOW)
    # The original immutable anchor remains usable.
    v.Verifier(TASKS, world.store, anchor, now=NOW).verify("T010")


def test_derived_inventory_can_change_without_rewriting_authenticated_observations():
    world = source_container_world()
    source_anchor(world)
    world.trust["pin_inventory"] = [{"openxfactory_commit": "a" * 40}]
    # Inventory correctness is independently checked by T008/doc-health.
    anchor = world.store.put(world.trust, v.COMMISSIONING_PATH)
    v.Verifier(TASKS, world.store, anchor, now=NOW).verify("T010")


def test_container_cannot_downgrade_to_legacy_nonempty_review():
    world = World()
    world.add("T007")
    anchor = world.store.put(world.trust, v.COMMISSIONING_PATH)
    with pytest.raises(v.EvidenceError, match="source commissioning container required"):
        v.Verifier(TASKS, world.store, anchor, now=NOW)
    with pytest.raises(v.EvidenceError, match="immutable reference"):
        v.reference({"object": "caller-selected"})


def test_container_duplicate_json_object_names_fail_before_authentication():
    world = source_container_world()
    anchor = source_anchor(world)
    raw = world.store.blob(anchor).replace(b'"objects": {', b'"objects": {"dup": {}, "dup": {}, ', 1)
    assert raw != world.store.blob(anchor)
    bad = world.store.put(raw, v.COMMISSIONING_PATH)
    with pytest.raises(v.EvidenceError, match="duplicate JSON key"):
        v.Verifier(TASKS, world.store, bad, now=NOW)


@pytest.mark.parametrize("task", [f"T{i:03}" for i in range(1, 69)])
def test_each_frozen_task_and_case_has_acceptance_and_rejection(world, task):
    if task in v.INSTANCE_TASKS:
        key = world.child(task)
    else:
        if int(task[1:]) >= 65:
            for predecessor in ("T064",):
                world.child(predecessor)
                world.aggregate(predecessor)
        key = world.add(task)
    world.check(key)
    for case in world.outputs[key]["cases"]:
        original = case["checks"][0]["observed"]
        case["checks"][0]["observed"] = "copied pass"
        with pytest.raises(v.EvidenceError, match="expected/observed"):
            world.check(key)
        case["checks"][0]["observed"] = original


@pytest.mark.parametrize("field", sorted(v.SCOPE_FIELDS))
def test_wrong_record_or_output_scope_rejected(world, field):
    key = world.add("T007")
    world.outputs[key]["scope"][field] = "foreign"
    with pytest.raises(v.EvidenceError, match="scope"):
        world.check(key)


@pytest.mark.parametrize("mutation", ["duplicate", "missing", "unknown", "subcheck-duplicate", "subcheck-missing"])
def test_closed_cases_and_subchecks(world, mutation):
    key = world.add("T007")
    cases = world.outputs[key]["cases"]
    if mutation == "duplicate": cases.append(deepcopy(cases[0]))
    if mutation == "missing": cases.pop()
    if mutation == "unknown": cases[0]["id"] = "invented"
    if mutation == "subcheck-duplicate": cases[0]["checks"].append(deepcopy(cases[0]["checks"][0]))
    if mutation == "subcheck-missing": cases[0]["checks"] = []
    with pytest.raises(v.EvidenceError): world.check(key)


@pytest.mark.parametrize("field,value", [("evidence_class", "Q2"), ("owner", "L"), ("command", "echo pass"), ("verdict", "blocked"), ("verdict", "fail")])
def test_wrong_record_class_owner_command_or_result(world, field, value):
    key = world.add("T007")
    world.records[key][field] = value
    with pytest.raises(v.EvidenceError): world.check(key)


@pytest.mark.parametrize("field,value", [("command", "echo pass"), ("exit_code", 1), ("exit_code", False), ("source", {}), ("ended_at", "2040-01-01T00:00:00Z")])
def test_actual_output_must_match_command_revision_and_time(world, field, value):
    key = world.add("T007")
    world.outputs[key][field] = value
    with pytest.raises(v.EvidenceError): world.check(key)


@pytest.mark.parametrize("mutation", ["expired", "future", "revoked", "scope", "roles", "missing-human", "later-approval"])
def test_current_actual_authority(world, mutation):
    key = world.add("T007")
    binding = world.trust["bindings"][key]
    decision = v.decode(world.store.blob(binding["authority"]))
    if mutation == "expired": decision["valid_until"] = START
    if mutation == "future": decision["valid_from"] = "2030-02-01T00:00:00Z"
    if mutation == "later-approval": decision["valid_from"] = "2030-01-01T00:00:30Z"
    if mutation == "revoked": world.trust["revoked_authorities"].append(decision["id"])
    if mutation == "scope": decision["scope"]["customer"] = "foreign"
    if mutation == "roles": decision["roles"] = []
    if mutation == "missing-human": decision["owner"] = ""
    binding["authority"] = world.store.put(decision, "decisions/revised.json")
    world.records[key]["authority"] = binding["authority"]
    with pytest.raises(v.EvidenceError): world.check(key)


def test_dependencies_are_immutable_and_failed_predecessor_cannot_pass(world):
    key = world.add("T007")
    original = world.records[key]["dependencies"]["T006"]
    world.records[key]["dependencies"]["T006"] = world.review
    with pytest.raises(v.EvidenceError, match="dependency"): world.check(key)
    world.records[key]["dependencies"]["T006"] = original
    world.records["T006"]["verdict"] = "fail"
    world.publish("T006")
    world.records[key]["dependencies"]["T006"] = world.ref("T006")
    with pytest.raises(v.EvidenceError, match="failed/blocked"): world.check(key)


@pytest.mark.parametrize("field", ["cases", "dependencies", "command", "files", "source-owner"])
def test_trusted_manifest_cannot_waive_frozen_floor(world, field):
    key = world.add("T007")
    binding = world.trust["bindings"][key]
    if field == "cases": binding["cases"] = {}
    if field == "dependencies": binding["dependencies"] = {}
    if field == "command": binding["command"] = "echo pass"
    if field == "files": binding["files"] = ["scripts/unaccepted.py"]
    if field == "source-owner": binding["source"]["repository"] = "foreign/repo"
    with pytest.raises(v.EvidenceError): world.check(key)


def test_source_diff_must_stay_inside_exact_accepted_scope(world):
    key = world.add("T007")
    source = world.records[key]["source"]
    world.store.diffs[(source["repository"], source["revision"])].add(".github/workflows/pytest-suite.yml")
    with pytest.raises(v.EvidenceError, match="diff"): world.check(key)


@pytest.mark.parametrize("task", [f"T{i:03}" for i in range(1, 10)])
def test_bootstrap_requires_original_authenticated_output_not_new_receipt(world, task):
    key = world.add(task)
    world.records[key]["schema"] = "043-task-evidence-v1"
    with pytest.raises(v.EvidenceError, match="import kind"): world.check(key)
    world.records[key]["schema"] = "043-bootstrap-import-v1"
    world.publish(key)
    binding = world.trust["bindings"][key]
    binding["record"] = world.store.put(world.records[key], "evidence/" + task + ".json")
    with pytest.raises(v.EvidenceError, match="fabricated bootstrap"): world.verifier().verify(key)


def metric(world):
    key = world.add("T007")
    binding, output = world.trust["bindings"][key], world.outputs[key]
    binding["metrics"] = {"revocation": dict(minimum=0, maximum=10, unit="seconds", event="revoke")}
    output["events"] = dict(revoke=START)
    output["metrics"] = {"revocation": dict(value=5, unit="seconds", event="revoke")}
    return key, binding, output


@pytest.mark.parametrize("value", [True, False, -1, float("nan"), float("inf"), -float("inf"), "5", None, 11])
def test_numeric_finite_field_and_bound_rejections(world, value):
    key, _, output = metric(world)
    output["metrics"]["revocation"]["value"] = value
    with pytest.raises(v.EvidenceError): world.check(key)


@pytest.mark.parametrize("mutation", ["unit", "event", "missing", "boolean-limit", "nonfinite-limit", "negative-limit"])
def test_approved_metric_identity_and_limits(world, mutation):
    key, binding, output = metric(world)
    if mutation in ("unit", "event"): output["metrics"]["revocation"][mutation] = "wrong"
    if mutation == "missing": output["metrics"] = {}
    if mutation == "boolean-limit": binding["metrics"]["revocation"]["maximum"] = True
    if mutation == "nonfinite-limit": binding["metrics"]["revocation"]["maximum"] = float("inf")
    if mutation == "negative-limit": binding["metrics"]["revocation"]["minimum"] = -1
    with pytest.raises(v.EvidenceError): world.check(key)


def test_positive_metric_and_missing_monitoring_is_not_observed_time(world):
    key, binding, output = metric(world)
    binding["observation"] = dict(window=[START, END], max_gap_seconds=10, minimum_observed_seconds=50)
    output["coverage"] = dict(window=[START, END], intervals=[[START, "2030-01-01T00:00:25Z"], ["2030-01-01T00:00:30Z", END]])
    world.check(key)
    binding["observation"]["minimum_observed_seconds"] = 60
    with pytest.raises(v.EvidenceError, match="omitted monitoring"): world.check(key)


@pytest.mark.parametrize("intervals", [[], [[START, START]], [[START, END], [START, END]], [["2030-01-01T00:00:30Z", END]], [[START, "2030-01-01T00:00:20Z"]]])
def test_monitoring_gaps_overlap_and_omission(world, intervals):
    key, binding, output = metric(world)
    binding["observation"] = dict(window=[START, END], max_gap_seconds=5, minimum_observed_seconds=50)
    output["coverage"] = dict(window=[START, END], intervals=intervals)
    with pytest.raises(v.EvidenceError): world.check(key)


def test_denial_requires_actual_legitimate_control_and_neighbor(world):
    key = world.add("T007")
    name = TASKS[key]["cases"][0]
    binding = world.trust["bindings"][key]
    binding["cases"][name] = [dict(id="control", kind="equal", expected="allowed"), dict(id="neighbor", kind="equal", expected="available"),
                              dict(id="denial", kind="deny", expected="denied", control="control", neighbor="neighbor")]
    checks = [dict(id="control", observed="allowed"), dict(id="neighbor", observed="available"), dict(id="denial", observed="denied")]
    world.outputs[key]["cases"][0]["checks"] = checks
    world.check(key)
    checks[0]["observed"] = "denied"
    with pytest.raises(v.EvidenceError): world.check(key)
    checks[0]["observed"] = "allowed"
    checks[1]["observed"] = "missing"
    with pytest.raises(v.EvidenceError): world.check(key)


@pytest.mark.parametrize("mutation", ["wrong-head", "not-required", "no-collection", "skipped", "failed", "no-job"])
def test_required_ci_proves_actual_collection_exact_head_and_job(world, mutation):
    key = world.add("T010")
    suite = next(iter(world.outputs[key]["ci"].values()))
    if mutation == "wrong-head": suite["revision"] = "b" * 40
    if mutation == "not-required": suite["required"] = False
    if mutation == "no-collection": suite["collected"] = 0
    if mutation == "skipped": suite["skipped"] = 1
    if mutation == "failed": suite["conclusion"] = "failure"
    if mutation == "no-job": suite["job_id"] = 0
    with pytest.raises(v.EvidenceError): world.check(key)


def test_individual_child_advances_without_unrelated_aggregate(world):
    key = world.child("T058")
    world.child("T057", "other-offering")
    assert "T057" not in world.trust["aggregates"]
    world.check(key)
    data = world.aggregate("T057")
    world.verifier().aggregate("T057", data)
    bad = v.decode(data)
    del bad["children"]["other-offering"]
    with pytest.raises(v.EvidenceError, match="aggregate child|immutable reference"):
        world.verifier().aggregate("T057", json.dumps(bad).encode())


def test_canary_still_requires_complete_program_q2(world):
    key = world.child("T058")
    world.records["T056"]["verdict"] = "blocked"
    world.publish("T056")
    predecessor = "T057@service"
    world.records[predecessor]["dependencies"]["T056"] = world.ref("T056")
    world.publish(predecessor)
    world.records[key]["dependencies"]["T057"] = world.ref(predecessor)
    with pytest.raises(v.EvidenceError, match="failed/blocked"): world.check(key)


def test_child_cannot_borrow_foreign_offering_or_wave_authority(world):
    key = world.child("T058")
    world.child("T057", "foreign", {"profile": "other-profile"})
    world.trust["bindings"][key]["dependencies"]["T057"] = "T057@foreign"
    world.records[key]["dependencies"]["T057"] = world.ref("T057@foreign")
    with pytest.raises(v.EvidenceError, match="scope transition|foreign offering"): world.check(key)
    wave = world.child("T062", "wave", {"wave": "first-wave"}, decisions=["C-11"])
    with pytest.raises(v.EvidenceError, match="C-12"): world.check(wave)


def test_wave_requires_corresponding_previously_admitted_offer(world):
    key = world.child("T063", "wave", {"wave": "wave-1"}, decisions=["C-11", "C-12"])
    # Rejects the absent offer before any caller-selected output could grant it.
    with pytest.raises((v.EvidenceError, KeyError)): world.check(key)
    offer = world.child("T063", "offer")
    world.trust["bindings"][key]["offer_admission"] = offer
    world.check(key)


def test_source_only_custody_and_source_authority_do_not_admit_live_observations(world):
    key = world.child("T057", scope_changes={"phase": "production"})
    del world.trust["live_custody"]
    with pytest.raises(v.EvidenceError): world.check(key)


def test_failed_history_requires_reviewed_remediation_and_fresh_resume(world):
    key = world.add("T007")
    failed = deepcopy(world.records[key]); failed.update(verdict="fail", attempt="earlier")
    history = [world.store.put(failed, "history/earlier.json")]
    world.records[key]["history"] = history
    world.trust["bindings"][key]["history"] = history
    with pytest.raises((v.EvidenceError, KeyError)): world.check(key)


@pytest.mark.parametrize("path", ["../secret", "/etc/passwd", "a/../b", "a//b", "./a", "a\\b", "C:/secret", "a/./b"])
def test_reference_path_traversal_rejected(path):
    with pytest.raises(v.EvidenceError): v.relative(path)


def test_duplicate_json_and_nonfinite_json_rejected():
    for data in (b'{"verdict":"fail","verdict":"pass"}', b'{"value":NaN}', b'{"value":Infinity}', b'{"value":1e999}'):
        with pytest.raises(v.EvidenceError): v.decode(data)


def test_immutable_digest_and_unreviewed_input_rejected(world):
    key = world.add("T007")
    verifier = world.verifier()
    with pytest.raises(v.EvidenceError, match="independently reviewed"):
        verifier.verify(key, b'{"verdict":"pass"}')
    ref = world.trust["bindings"][key]["record"]
    ref["sha256"] = "0" * 64
    with pytest.raises(v.EvidenceError, match="digest"):
        world.verifier().verify(key)


def git(root, *args):
    result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, check=True)
    return result.stdout.decode().strip()


def test_git_store_reads_immutable_blob_and_rejects_symlink(tmp_path):
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.name", "Synthetic Test")
    git(tmp_path, "config", "user.email", "test@example.invalid")
    git(tmp_path, "remote", "add", "origin", "https://github.com/Opensoft/openXfactory.git")
    (tmp_path / "output").write_bytes(b"actual committed bytes")
    (tmp_path / "link").symlink_to("output")
    git(tmp_path, "add", "output", "link")
    git(tmp_path, "commit", "-qm", "synthetic fixture")
    revision = git(tmp_path, "rev-parse", "HEAD")
    ref = dict(repository=v.COORDINATOR, commit=revision, path="output", sha256=v.digest(b"actual committed bytes"))
    before = git(tmp_path, "status", "--porcelain=v1")
    store = v.GitStore({v.COORDINATOR: tmp_path})
    assert store.blob(ref) == b"actual committed bytes"
    with pytest.raises(v.EvidenceError, match="symlink"):
        store.blob(dict(ref, path="link"))
    assert git(tmp_path, "status", "--porcelain=v1") == before
    with pytest.raises(v.EvidenceError, match="origin"):
        v.GitStore({"other/repo": tmp_path})


def test_source_authentication_uses_distinct_real_git_commits_read_only(tmp_path):
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.name", "Synthetic Test")
    git(tmp_path, "config", "user.email", "test@example.invalid")
    git(tmp_path, "remote", "add", "origin", "https://github.com/opensoft/openXfactory.git")
    def commit(path, data):
        target = tmp_path / path
        target.parent.mkdir(parents=True, exist_ok=True)
        raw = data if isinstance(data, bytes) else v.canonical_json(data)
        target.write_bytes(raw)
        git(tmp_path, "add", path)
        git(tmp_path, "commit", "-qm", "synthetic commissioning revision")
        return dict(repository=v.COORDINATOR, commit=git(tmp_path, "rev-parse", "HEAD"),
                    path=path, sha256=v.digest(raw))
    def review_bytes(data):
        fence = bytes([96]) * 3
        return fence + b"json\n" + v.canonical_json(data) + b"\n" + fence + b"\n"
    review = dict(schema="043-source-authentication-v1", decision="pending", custodian="Brett Heap",
                  reviewed_manifest=None, content_sha256=None, reviewed_at=None)
    trust = World().trust
    trust["review"] = commit(v.AUTHENTICATION_PATH, review_bytes(review))
    trust["source_container"] = dict(schema="043-source-container-v1",
        objects={"original": dict(tasks=["T007"], evidence_class="source", value={"original": "synthetic bytes"})})
    first = commit(v.COMMISSIONING_PATH, trust)
    review.update(decision="accepted", reviewed_manifest=first, content_sha256=v.commissioning_digest(trust),
                  reviewed_at="2030-01-01T01:00:00Z")
    auth = commit(v.AUTHENTICATION_PATH, review_bytes(review))
    trust["review"] = auth
    final = commit(v.COMMISSIONING_PATH, trust)
    before = git(tmp_path, "status", "--porcelain=v1")
    reader = v.Verifier(TASKS, v.GitStore({v.COORDINATOR: tmp_path}), final, now=NOW)
    assert reader.authenticated
    assert len({first["commit"], auth["commit"], final["commit"]}) == 3
    assert git(tmp_path, "status", "--porcelain=v1") == before


def test_verifier_never_executes_evidence_commands_or_writes(world, monkeypatch):
    key = world.add("T007")
    def forbidden(*args, **kwargs):
        pytest.fail("verifier attempted a mutation or owner command")
    monkeypatch.setattr(subprocess, "run", forbidden)
    monkeypatch.setattr(Path, "write_bytes", forbidden)
    monkeypatch.setattr(Path, "write_text", forbidden)
    verifier = world.verifier()
    before = deepcopy(world.store.objects)
    verifier.verify(key)
    assert world.store.objects == before


def test_cli_fails_closed_without_custody_anchor(tmp_path):
    result = subprocess.run(["python3", str(MODULE), "--task", "T007", str(tmp_path / "invented.json")],
                            capture_output=True, text=True, env={"PATH": "/usr/bin:/bin"})
    assert result.returncode == 1
    assert "PC_EVIDENCE_TRUST is required" in result.stderr


def test_registry_has_all_68_tasks_and_current_freeze():
    assert set(TASKS) == {f"T{i:03}" for i in range(1, 69)}
    assert all(set(d["dependencies"]) < set(TASKS) for d in TASKS.values())
    assert TASKS["T057"]["dependencies"] == ["T056"]
    assert TASKS["T050"]["dependencies"][-1] == "T049"


@pytest.mark.parametrize("mode", ["managed-pull", "managed-push", "customer"])
def test_authorized_channels_and_missing_or_expired_carriers(world, mode):
    key = world.child("T058")
    binding = world.trust["bindings"][key]
    authority = v.decode(world.store.blob(binding["authority"]))
    authority["mode"] = mode
    fields = ["consent"] if mode == "customer" else ["request", "grant" if mode == "managed-push" else "reviewed_merge"]
    for field in fields:
        authority[field] = world.decision(field, binding["scope"])
    binding["authority"] = world.store.put(authority, "decisions/channel.json")
    world.records[key]["authority"] = binding["authority"]
    world.check(key)
    bad = v.decode(world.store.blob(authority[fields[-1]]))
    bad["valid_until"] = START
    authority[fields[-1]] = world.store.put(bad, "decisions/expired-carrier.json")
    binding["authority"] = world.store.put(authority, "decisions/expired-channel.json")
    world.records[key]["authority"] = binding["authority"]
    with pytest.raises(v.EvidenceError, match="not current"): world.check(key)


def test_managed_attachment_needs_service_eligible_for_same_phase_and_scope(world):
    key = world.child("T058", "domain", {"offering": "hosted-domain"})
    with pytest.raises((v.EvidenceError, KeyError)): world.check(key)
    service = world.child("T058", "service")
    world.trust["bindings"][key]["eligibility"] = service
    # Its decision predecessor also needs its own service eligibility.
    world.trust["bindings"]["T057@domain"]["eligibility"] = "T057@service"
    world.check(key)
    foreign = world.child("T058", "foreign", {"customer": "another-customer"})
    world.trust["bindings"][key]["eligibility"] = foreign
    with pytest.raises(v.EvidenceError, match="phase/scope"): world.check(key)


def test_explicit_reviewed_scope_transition_allows_new_cohort_without_borrowing(world):
    key = world.child("T062", "offer", {"customer": "new-cohort"})
    old = world.child("T061", "canary", {"customer": "internal-canary"})
    binding = world.trust["bindings"][key]
    binding["dependencies"]["T061"] = old
    world.records[key]["dependencies"]["T061"] = world.ref(old)
    with pytest.raises(v.EvidenceError, match="scope transition"): world.check(key)
    binding["transitions"] = {"T061": deepcopy(world.trust["bindings"][old]["scope"])}
    world.check(key)


@pytest.mark.parametrize("field", ["scope", "source"])
def test_case_cannot_import_foreign_observations(world, field):
    key = world.add("T007")
    world.outputs[key]["cases"][0][field] = {}
    with pytest.raises(v.EvidenceError, match="mixed case"): world.check(key)


def test_mixed_staging_runs_and_changed_canary_candidates_rejected(world):
    key = world.add("T056")
    world.trust["bindings"]["T052"]["scope"]["run"] = "other-run"
    with pytest.raises(v.EvidenceError, match="mixed staging run"): world.check(key)
    world.trust["bindings"]["T052"]["scope"]["run"] = "synthetic-run"
    canary = world.child("T057", scope_changes={"candidate": "untested-candidate"})
    with pytest.raises(v.EvidenceError, match="candidate changed"): world.check(canary)


def test_source_classes_cannot_be_relabelled_staging_or_production(world):
    key = world.add("T007")
    world.trust["bindings"][key]["scope"]["phase"] = "production"
    with pytest.raises(v.EvidenceError, match="evidence phase"): world.check(key)


def test_real_cli_reads_committed_evidence_and_leaves_tree_unchanged(tmp_path):
    import os
    import shutil
    target = tmp_path / v.FEATURE_PATH
    shutil.copytree(ROOT / v.FEATURE_PATH, target, ignore=shutil.ignore_patterns("__pycache__", "tests"))
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.name", "Synthetic Test")
    git(tmp_path, "config", "user.email", "test@example.invalid")
    git(tmp_path, "remote", "add", "origin", "https://github.com/opensoft/openXfactory.git")
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "-qm", "synthetic source")
    revision = git(tmp_path, "rev-parse", "HEAD")
    world = World(); key = world.add("T001")
    binding, record, output = world.trust["bindings"][key], world.records[key], world.outputs[key]
    source = dict(repository=v.COORDINATOR, base=revision, revision=revision)
    for value in (binding, record, output): value["source"] = source
    for case in output["cases"]: case["source"] = source
    output.update(started_at="2020-01-01T00:00:00Z", ended_at="2020-01-01T00:01:00Z")
    authority = v.decode(world.store.blob(binding["authority"]))
    authority.update(valid_from="2019-01-01T00:00:00Z", valid_until="2100-01-01T00:00:00Z")
    binding["authority"] = world.store.put(authority, "decisions/long-lived-source.json")
    record["authority"] = binding["authority"]
    artifact = v.FEATURE_PATH + "/checklists/requirements.md"
    binding["artifacts"] = record["artifacts"] = [dict(repository=v.COORDINATOR, commit=revision, path=artifact, sha256=v.digest((tmp_path / artifact).read_bytes()))]
    # Export actual fixture objects, commit each layer, and rebind references to
    # their real Git commits. Source and receipt commits are deliberately distinct.
    def export(data, path):
        destination = tmp_path / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
        git(tmp_path, "add", path)
        git(tmp_path, "commit", "-qm", "synthetic reviewed export")
        return dict(repository=v.COORDINATOR, commit=git(tmp_path, "rev-parse", "HEAD"), path=path, sha256=v.digest(data))
    binding["authority"] = record["authority"] = export(json.dumps(authority).encode(), "decisions/source.json")
    record["output"] = export(json.dumps(output).encode(), "outputs/T001.json")
    binding["record"] = export(json.dumps(record).encode(), "exports/T001.import.json")
    world.trust["review"] = export(b"SYNTHETIC independently reviewed fixture", "reviews/fixture.txt")
    trust_ref = export(json.dumps(world.trust).encode(), "commissioning/fixture.json")
    environment = {name: value for name, value in os.environ.items() if not name.startswith("PC_EVIDENCE_")}
    environment.update(PC_EVIDENCE_TRUST=trust_ref["commit"] + ":" + trust_ref["path"], PC_EVIDENCE_TRUST_SHA256=trust_ref["sha256"])
    before = git(tmp_path, "status", "--porcelain=v1")
    result = subprocess.run(["python3", str(target / "verify-evidence.py"), "--task", key, str(tmp_path / binding["record"]["path"])],
                            capture_output=True, text=True, env=environment)
    assert result.returncode == 0, result.stderr
    assert "structurally verified" in result.stdout
    assert git(tmp_path, "status", "--porcelain=v1") == before


def test_failed_attempts_are_preserved_with_reviewed_reruns_and_fresh_resume(world):
    key = world.add("T007")
    binding, record = world.trust["bindings"][key], world.records[key]
    earlier = deepcopy(record); earlier.update(verdict="blocked", attempt="prior-attempt")
    binding["history"] = record["history"] = [world.store.put(earlier, "history/blocked.json")]
    binding["decisions"] = ["C-13"]
    reruns = [record["output"]]
    decision = v.decode(world.store.blob(world.decision("C-13", binding["scope"])))
    decision["reruns"] = reruns
    authority = v.decode(world.store.blob(binding["authority"]))
    authority["decisions"] = {"C-13": world.store.put(decision, "decisions/resume-reruns.json")}
    resumed = world.store.put(authority, "decisions/fresh-resume.json")
    binding["authority"] = record["authority"] = binding["remediation"] = record["remediation"] = resumed
    binding["resume_outputs"] = reruns
    world.check(key)
    binding["resume_outputs"] = []
    with pytest.raises(v.EvidenceError, match="rerun"): world.check(key)


def test_incidents_cannot_be_omitted_and_need_reviewed_closure(world):
    key = world.add("T007")
    binding = world.trust["bindings"][key]
    closure = v.decode(world.store.blob(world.decision("incident-closure", binding["scope"])))
    closure["reruns"] = [world.records[key]["output"]]
    ref = world.store.put(closure, "incidents/closed.json")
    binding["incidents"] = [ref]
    with pytest.raises(v.EvidenceError, match="incident history"): world.check(key)
    world.records[key]["incidents"] = [ref]
    world.check(key)


def test_self_verification_is_not_exact_ci_or_owner_execution(world):
    key = world.add("T010")
    world.trust["bindings"][key]["command"] = TASKS[key]["command"]
    with pytest.raises(v.EvidenceError, match="self-verification"): world.check(key)


def test_frozen_definitions_reject_changed_task_command(tmp_path):
    import shutil
    target = tmp_path / v.FEATURE_PATH
    shutil.copytree(ROOT / v.FEATURE_PATH, target, ignore=shutil.ignore_patterns("__pycache__", "tests"))
    task_path = target / "tasks.md"
    task_path.write_text(task_path.read_text().replace("cases=frozen-cases,", "cases=caller-cases,"))
    with pytest.raises(v.EvidenceError, match="unreviewed"):
        v.load_contract(tmp_path)


def test_manifest_cannot_substitute_fixed_component_owner(world):
    world.add("T007")
    world.trust["repositories"]["L"] = "other/headscale"
    with pytest.raises(v.EvidenceError, match="canonical component owner"):
        world.verifier()


def test_aggregate_permits_only_reviewed_inventory_metadata(world):
    world.child("T057")
    record = v.decode(world.aggregate("T057"))
    record["pin_inventory"] = []
    original = world.trust["aggregates"]["T057"]
    world.trust["aggregates"]["T057"] = world.store.put(record, original["path"], original["repository"])
    world.verifier().aggregate("T057", world.store.blob(world.trust["aggregates"]["T057"]))
    record["caller_waiver"] = True
    world.trust["aggregates"]["T057"] = world.store.put(record, original["path"], original["repository"])
    with pytest.raises(v.EvidenceError, match="aggregate child"):
        world.verifier().aggregate("T057", world.store.blob(world.trust["aggregates"]["T057"]))


def completed_run(world, key, mode="managed-push"):
    """Synthetic grants close after the original run, never actual authority."""
    binding = world.trust["bindings"][key]
    authority = v.decode(world.store.blob(binding["authority"]))
    authority["mode"] = mode
    fields = ["consent"] if mode == "customer" else ["request", "grant" if mode == "managed-push" else "reviewed_merge"]
    for field in fields:
        carrier = v.decode(world.store.blob(world.decision(field, binding["scope"])))
        carrier["valid_until"] = "2030-01-01T00:02:00Z"
        authority[field] = world.store.put(carrier, "closed/" + field + ".json")
        if field == "grant":
            world.trust["revoked_authorities"].append(carrier["id"])
            closure = dict(kind="authority-closure", authority_id=carrier["id"], scope=binding["scope"],
                           closed_at="2030-01-01T00:01:01Z", disposition="completed", owner="Synthetic Ops Owner")
            world.trust.setdefault("completed_authorities", {})[carrier["id"]] = world.store.put(closure, "closed/proof.json")
    authority["valid_until"] = "2030-01-01T00:02:00Z"
    binding["authority"] = world.store.put(authority, "closed/authority.json")
    world.records[key]["authority"] = binding["authority"]
    return binding


def admit_run(world, key, **changes):
    binding = world.trust["bindings"][key]
    world.publish(key)
    admission = dict(kind="evidence-admission", id="admission-" + key, decision="accepted",
                     scope=binding["scope"], owner="Synthetic Evidence Owner", roles=["synthetic-evidence-owner"],
                     authority=binding["authority"], reviewed_output_sha256=world.records[key]["output"]["sha256"],
                     reviewed_at="2030-01-01T00:03:00Z", valid_from="2030-01-01T00:02:00Z",
                     valid_until="2031-01-01T00:00:00Z")
    admission.update(changes)
    binding["admission_roles"] = ["synthetic-evidence-owner"]
    binding["admission"] = world.store.put(admission, "reviews/" + key + ".json")
    world.records[key]["admission"] = binding["admission"]
    return admission


@pytest.mark.parametrize("mode", ["managed-push", "managed-pull", "customer"])
def test_completed_execution_uses_current_independent_admission(world, mode):
    key = world.child("T058")
    completed_run(world, key, mode)
    admit_run(world, key)
    world.check(key)


def test_expired_execution_without_admission_stays_rejected(world):
    key = world.child("T058")
    completed_run(world, key)
    with pytest.raises(v.EvidenceError):
        world.check(key)


@pytest.mark.parametrize("changes", [
    {"valid_until": START}, {"reviewed_at": START}, {"reviewed_at": "2040-01-01T00:00:00Z"},
    {"roles": []}, {"owner": ""}, {"decision": "rejected"}, {"kind": "request"},
    {"reviewed_output_sha256": "f" * 64}, {"authority": {}},
])
def test_independent_admission_cannot_waive_scope_time_roles_or_output(world, changes):
    key = world.child("T058")
    completed_run(world, key)
    admit_run(world, key, **changes)
    with pytest.raises(v.EvidenceError):
        world.check(key)


def test_admission_must_have_exact_scope_and_reviewed_record_reference(world):
    key = world.child("T058")
    completed_run(world, key)
    scope = deepcopy(world.trust["bindings"][key]["scope"])
    scope["site"] = "foreign-site"
    admit_run(world, key, scope=scope)
    with pytest.raises(v.EvidenceError):
        world.check(key)
    admit_run(world, key)
    world.records[key].pop("admission")
    with pytest.raises(v.EvidenceError):
        world.check(key)


@pytest.mark.parametrize("changes", [
    {"valid_until": START}, {"valid_until": END}, {"valid_from": END},
])
def test_admission_does_not_retroactively_authorize_execution(world, changes):
    key = world.child("T058")
    binding = completed_run(world, key)
    authority = v.decode(world.store.blob(binding["authority"]))
    authority.update(changes)
    binding["authority"] = world.store.put(authority, "closed/invalid-period.json")
    world.records[key]["authority"] = binding["authority"]
    admit_run(world, key)
    with pytest.raises(v.EvidenceError):
        world.check(key)


@pytest.mark.parametrize("mutation", ["missing", "early", "foreign", "rejected", "other-authority", "future"])
def test_post_run_revocation_needs_authenticated_completion_closure(world, mutation):
    key = world.child("T058")
    completed_run(world, key)
    admit_run(world, key)
    closures = world.trust["completed_authorities"]
    identity, ref = next(iter(closures.items()))
    proof = v.decode(world.store.blob(ref))
    if mutation == "missing":
        closures.pop(identity)
    else:
        if mutation == "early": proof["closed_at"] = START
        if mutation == "future": proof["closed_at"] = "2040-01-01T00:00:00Z"
        if mutation == "foreign": proof["scope"] = {**proof["scope"], "customer": "foreign"}
        if mutation == "rejected": proof["disposition"] = "incident"
        if mutation == "other-authority": proof["authority_id"] = "another"
        closures[identity] = world.store.put(proof, "closed/invalid-proof.json")
    with pytest.raises(v.EvidenceError):
        world.check(key)


def test_admission_cannot_reuse_closed_grant_for_a_new_operation(world):
    key = world.child("T058")
    binding = completed_run(world, key)
    admit_run(world, key)
    world.check(key)
    verifier = world.verifier()
    with pytest.raises(v.EvidenceError):
        verifier.authority(binding["authority"], binding)


def test_current_admission_is_rechecked_for_cached_evidence(world):
    key = world.child("T058")
    completed_run(world, key)
    admission = admit_run(world, key)
    world.publish(key)
    verifier = world.verifier()
    verifier.verify(key)
    verifier.trust["revoked_authorities"].append(admission["id"])
    with pytest.raises(v.EvidenceError, match="revoked"):
        verifier.verify(key)


@pytest.mark.parametrize("mutation", ["during-run", "source-mode", "changed-output", "uncommissioned-admission"])
def test_historical_admission_keeps_execution_and_content_floors(world, mutation):
    key = world.child("T058")
    binding = completed_run(world, key)
    if mutation in ("during-run", "source-mode"):
        authority = v.decode(world.store.blob(binding["authority"]))
        if mutation == "during-run":
            grant = v.decode(world.store.blob(authority["grant"]))
            grant["valid_until"] = END
            authority["grant"] = world.store.put(grant, "closed/early-expiry.json")
        else:
            authority["mode"] = "source"
        binding["authority"] = world.store.put(authority, "closed/invalid-execution.json")
        world.records[key]["authority"] = binding["authority"]
    admit_run(world, key)
    if mutation == "changed-output":
        world.outputs[key]["exit_code"] = 1
    if mutation == "uncommissioned-admission":
        binding.pop("admission")
    with pytest.raises(v.EvidenceError):
        world.check(key)


def test_source_scope_approval_can_last_until_superseded(world):
    key = world.add("T007")
    binding = world.trust["bindings"][key]
    authority = v.decode(world.store.blob(binding["authority"]))
    authority["valid_until"] = "until-superseded"
    binding["authority"] = world.store.put(authority, "decisions/source-lifetime.json")
    world.records[key]["authority"] = binding["authority"]
    world.check(key)
    world.trust["revoked_authorities"].append(authority["id"])
    with pytest.raises(v.EvidenceError, match="revoked"):
        world.check(key)


def test_source_admission_can_persist_without_reopening_completed_grants(world):
    key = world.add("T007")
    binding = completed_run(world, key)
    admission = admit_run(world, key, valid_until="until-superseded")
    world.check(key)
    with pytest.raises(v.EvidenceError):
        world.verifier().authority(binding["authority"], binding)
    world.trust["revoked_authorities"].append(admission["id"])
    with pytest.raises(v.EvidenceError, match="revoked"):
        world.check(key)


def test_source_custody_decision_can_last_until_superseded(world):
    key = world.add("T007")
    binding = world.trust["bindings"][key]
    binding["decisions"] = ["C-08"]
    authority = v.decode(world.store.blob(binding["authority"]))
    decision = v.decode(world.store.blob(world.decision("C-08", binding["scope"])))
    decision["valid_until"] = "until-superseded"
    authority["decisions"] = {"C-08": world.store.put(decision, "decisions/source-custody.json")}
    binding["authority"] = world.store.put(authority, "decisions/source-custody-authority.json")
    world.records[key]["authority"] = binding["authority"]
    world.check(key)
    world.trust["revoked_authorities"].append(decision["id"])
    with pytest.raises(v.EvidenceError, match="revoked"):
        world.check(key)


@pytest.mark.parametrize("field", ["authority", "grant", "request", "decision", "admission"])
def test_live_authority_and_admission_require_finite_validity(world, field):
    key = world.child("T058")
    binding = completed_run(world, key)
    authority = v.decode(world.store.blob(binding["authority"]))
    if field == "admission":
        admit_run(world, key, valid_until="until-superseded")
    else:
        if field == "authority":
            authority["valid_until"] = "until-superseded"
        else:
            ref = authority["decisions"]["C-09"] if field == "decision" else authority[field]
            value = v.decode(world.store.blob(ref))
            value["valid_until"] = "until-superseded"
            updated = world.store.put(value, "decisions/live-unbounded.json")
            if field == "decision": authority["decisions"]["C-09"] = updated
            else: authority[field] = updated
        binding["authority"] = world.store.put(authority, "decisions/live-unbounded-authority.json")
        world.records[key]["authority"] = binding["authority"]
        admit_run(world, key)
    with pytest.raises(v.EvidenceError):
        world.check(key)


@pytest.mark.parametrize("mode", ["managed-push", "managed-pull", "customer"])
def test_source_phase_does_not_make_execution_channels_unbounded(world, mode):
    key = world.add("T007")
    binding = completed_run(world, key, mode)
    authority = v.decode(world.store.blob(binding["authority"]))
    authority["valid_until"] = "until-superseded"
    binding["authority"] = world.store.put(authority, "decisions/unbounded-source-channel.json")
    world.records[key]["authority"] = binding["authority"]
    admit_run(world, key)
    with pytest.raises(v.EvidenceError):
        world.check(key)


def test_source_lifetime_cannot_authorize_a_run_before_approval(world):
    key = world.add("T007")
    binding = world.trust["bindings"][key]
    authority = v.decode(world.store.blob(binding["authority"]))
    authority.update(valid_from=END, valid_until="until-superseded")
    binding["authority"] = world.store.put(authority, "decisions/late-source-approval.json")
    world.records[key]["authority"] = binding["authority"]
    with pytest.raises(v.EvidenceError):
        world.check(key)


@pytest.mark.parametrize("mode", ["managed-push", "managed-pull", "customer"])
def test_source_policy_lifetime_is_independent_of_finite_execution_channel(world, mode):
    key = world.add("T007")
    binding = completed_run(world, key, mode)
    binding["decisions"] = ["C-08"]
    authority = v.decode(world.store.blob(binding["authority"]))
    policy = v.decode(world.store.blob(world.decision("C-08", binding["scope"])))
    policy["valid_until"] = "until-superseded"
    authority["decisions"] = {"C-08": world.store.put(policy, "decisions/source-policy.json")}
    binding["authority"] = world.store.put(authority, "decisions/source-policy-channel.json")
    world.records[key]["authority"] = binding["authority"]
    admit_run(world, key, valid_until="until-superseded")
    world.check(key)


@pytest.mark.parametrize("mode,field", [
    ("managed-push", "request"), ("managed-push", "grant"),
    ("managed-pull", "request"), ("managed-pull", "reviewed_merge"),
    ("customer", "consent"),
])
def test_source_policy_never_makes_request_grant_or_consent_unbounded(world, mode, field):
    key = world.add("T007")
    binding = completed_run(world, key, mode)
    authority = v.decode(world.store.blob(binding["authority"]))
    carrier = v.decode(world.store.blob(authority[field]))
    carrier["valid_until"] = "until-superseded"
    authority[field] = world.store.put(carrier, "decisions/unbounded-carrier.json")
    binding["authority"] = world.store.put(authority, "decisions/source-unbounded-carrier.json")
    world.records[key]["authority"] = binding["authority"]
    admit_run(world, key, valid_until="until-superseded")
    with pytest.raises(v.EvidenceError):
        world.check(key)


def test_source_wrapper_cannot_make_a_production_policy_indefinite(world):
    key = world.add("T007")
    binding = world.trust["bindings"][key]
    binding["decisions"] = ["C-08"]
    live_scope = {**binding["scope"], "phase": "production"}
    binding["decision_scopes"] = {"C-08": live_scope}
    authority = v.decode(world.store.blob(binding["authority"]))
    policy = v.decode(world.store.blob(world.decision("C-08", live_scope)))
    policy["valid_until"] = "until-superseded"
    authority["decisions"] = {"C-08": world.store.put(policy, "decisions/production-policy.json")}
    binding["authority"] = world.store.put(authority, "decisions/wrapped-production-policy.json")
    world.records[key]["authority"] = binding["authority"]
    with pytest.raises(v.EvidenceError):
        world.check(key)


@pytest.mark.parametrize("kind", ["C-03", "C-08", "C-09", "C-10", "C-11", "C-12", "C-13"])
def test_source_decision_scope_override_cannot_satisfy_a_live_gate(world, kind):
    key = world.child("T058")
    binding = world.trust["bindings"][key]
    source_scope = {**binding["scope"], "phase": "source"}
    binding["decision_scopes"] = {kind: source_scope}
    ref = world.decision(kind, source_scope)
    with pytest.raises(v.EvidenceError, match="phase"):
        world.verifier().decision(ref, binding, kind)
