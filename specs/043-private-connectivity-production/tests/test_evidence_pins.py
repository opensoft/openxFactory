"""Exact inventory regressions. All repositories and records here are synthetic."""

from copy import deepcopy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
from types import SimpleNamespace

import pytest


ROOT = Path(__file__).resolve().parents[3]
FEATURE = ROOT / "specs/043-private-connectivity-production"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


pins = module("inventory_043_tests", FEATURE / "register-evidence-pins.py")
v = module("evidence_043_for_pin_tests", FEATURE / "verify-evidence.py")
LOCAL = v.COORDINATOR
FOREIGN = "opensoft/headscale-install"
A, B = "a" * 40, "b" * 40


def value():
    return dict(source=dict(repository=LOCAL, revision=A), artifact=dict(repository=FOREIGN, commit=B),
                content_digest="c" * 64)


def owners():
    return {LOCAL: {A}, FOREIGN: {B}}


def test_inventory_covers_every_real_commit_and_no_content_digest():
    assert pins.inventory(value(), owners()) == [dict(repository=LOCAL, openxfactory_commit=A), dict(repository=FOREIGN, foreign_commit=B)]


@pytest.mark.parametrize("mutation", ["unknown", "duplicate", "missing", "extra", "wrong-owner", "wrong-key", "foreign-local"])
def test_stored_inventory_is_exact_and_preserves_local_obligations(mutation):
    data = value()
    data["pin_inventory"] = [dict(repository=LOCAL, openxfactory_commit=A), dict(repository=FOREIGN, foreign_commit=B)]
    if mutation == "unknown": data["pin_inventory"][1]["repository"] = "other/repository"
    if mutation == "duplicate": data["pin_inventory"].append(data["pin_inventory"][0])
    if mutation == "missing": data["pin_inventory"].pop()
    if mutation == "extra": data["pin_inventory"].append(dict(repository=LOCAL, openxfactory_commit="d" * 40))
    if mutation == "wrong-owner": data["pin_inventory"][1] = dict(repository=LOCAL, openxfactory_commit=B)
    if mutation == "wrong-key": data["pin_inventory"][1] = dict(repository=FOREIGN, openxfactory_commit=B)
    if mutation == "foreign-local": data["pin_inventory"][0] = dict(repository=FOREIGN, foreign_commit=A)
    with pytest.raises(ValueError): pins.validate_inventory(data, owners())


def test_repository_casing_is_canonicalized_without_changing_ownership():
    data = dict(source=dict(repository="Opensoft/openXfactory", revision=A))
    assert pins.inventory(data, {"Opensoft/openXfactory": {A}}) == [dict(repository=LOCAL, openxfactory_commit=A)]


def test_unreachable_or_ambiguous_foreign_owner_never_passes():
    for available in ({LOCAL: {A}, FOREIGN: set()}, {LOCAL: {A}, FOREIGN: {B}, "other/fork": {B}}):
        data = value()
        if "other/fork" in available: data["artifact"] = B
        with pytest.raises(ValueError): pins.inventory(data, available)


def test_explicit_owner_cannot_hide_a_local_commit_or_disagree_with_url():
    data = value()
    data["artifact"]["commit"] = A
    with pytest.raises(ValueError): pins.inventory(data, {LOCAL: {A}, FOREIGN: {A}})
    data = value(); data["url"] = "https://github.com/other/repository/commit/" + B
    with pytest.raises(ValueError): pins.inventory(data, owners())


def test_conflicting_owners_for_one_token_are_rejected():
    data = value(); data["another"] = dict(repository="other/repository", commit=B)
    with pytest.raises(ValueError): pins.inventory(data, {**owners(), "other/repository": {B}})


def test_inventory_does_not_change_input_or_import_old_inventory_tokens():
    data = value(); data["pin_inventory"] = [dict(repository="ignored/owner", foreign_commit="e" * 40)]
    before = deepcopy(data)
    assert len(pins.inventory(data, owners())) == 2
    assert data == before


def git(root, *arguments):
    return subprocess.check_output(["git", "-C", str(root), *arguments], text=True).strip()


@pytest.fixture
def commissioned(tmp_path):
    root = tmp_path / "coordinator"; root.mkdir()
    git(root, "init", "-q")
    git(root, "config", "user.name", "Synthetic Test")
    git(root, "config", "user.email", "test@example.invalid")
    git(root, "remote", "add", "origin", "https://github.com/opensoft/openXfactory.git")
    (root / "source").write_text("synthetic source\n")
    git(root, "add", "source"); git(root, "commit", "-qm", "synthetic source")
    revision = git(root, "rev-parse", "HEAD")
    path = v.FEATURE_PATH + "/evidence/T010.json"
    record = dict(schema="043-task-evidence-v1", task="T010", instance=None, source=dict(repository=LOCAL, revision=revision))
    location = root / path; location.parent.mkdir(parents=True); location.write_text(json.dumps(record))
    binding = dict(task="T010", instance=None, owner="C", files=[path], authority={"synthetic": "reviewed"})
    calls = []
    verifier = SimpleNamespace(tasks=v.load_contract(ROOT), trust=dict(repositories={"C": LOCAL}, pin_owners=[]),
                               store=v.GitStore({LOCAL: root}), binding=lambda key: binding,
                               trust_reference=dict(repository=LOCAL, commit=revision, path="source",
                                                    sha256=v.digest((root / "source").read_bytes())),
                               authority=lambda *args: calls.append(args))
    return SimpleNamespace(root=root, path=location, relative=path, record=record, binding=binding,
                           verifier=verifier, calls=calls, revision=revision)


def test_generation_writes_only_an_exact_new_draft_and_check_never_writes(commissioned, monkeypatch):
    c = commissioned
    pins.process(c.verifier, "T010", write=True)
    data = json.loads(c.path.read_text())
    assert data["pin_inventory"] == [dict(repository=LOCAL, openxfactory_commit=c.revision)]
    assert c.calls
    original = c.path.read_bytes()
    def forbidden(*args, **kwargs): pytest.fail("check mode wrote a file")
    monkeypatch.setattr(Path, "write_text", forbidden)
    monkeypatch.setattr(Path, "write_bytes", forbidden)
    pins.process(c.verifier, "T010", write=False)
    assert c.path.read_bytes() == original
    assert (c.root / "source").read_text() == "synthetic source\n"


def commissioning_draft(c):
    c.path.unlink()
    c.relative = v.COMMISSIONING_PATH
    c.path = c.root / c.relative
    c.binding["files"] = [c.relative]
    c.record = dict(schema="043-reviewed-trust-v1", feature=v.FEATURE, definition=v.DEFINITION,
                    source_container=dict(schema="043-source-container-v1", objects={
                        "original": dict(tasks=["T007"], evidence_class="source",
                                         value=dict(source=dict(repository=LOCAL, revision=c.revision)))}))
    c.path.write_text(json.dumps(c.record))


def test_commissioning_generation_and_anchored_check_preserve_source_objects(commissioned):
    c = commissioned
    commissioning_draft(c)
    original = deepcopy(c.record)
    pins.process(c.verifier, "T010", write=True, commissioning=True)
    data = json.loads(c.path.read_text())
    assert pins.body(data) == original
    assert data["pin_inventory"] == [dict(repository=LOCAL, openxfactory_commit=c.revision)]
    git(c.root, "add", c.relative)
    git(c.root, "commit", "-qm", "synthetic pending commissioning")
    c.verifier.trust_reference = dict(repository=LOCAL, commit=git(c.root, "rev-parse", "HEAD"),
                                     path=c.relative, sha256=v.digest(c.path.read_bytes()))
    before = c.path.read_bytes()
    pins.process(c.verifier, "T010", commissioning=True)
    assert c.path.read_bytes() == before
    assert c.calls
    with pytest.raises(ValueError, match="reviewed commissioning"):
        pins.process(c.verifier, "T010", write=True, commissioning=True)


@pytest.mark.parametrize("task,instance", [("T009", None), ("T011", None), ("T010", "other"), ("T057", "service")])
def test_commissioning_mode_cannot_expand_to_other_tasks_or_instances(commissioned, task, instance):
    c = commissioned
    commissioning_draft(c)
    original = c.path.read_bytes()
    with pytest.raises(ValueError):
        pins.process(c.verifier, task, instance, write=True, commissioning=True)
    assert c.path.read_bytes() == original


@pytest.mark.parametrize("mutation", ["scope", "schema", "definition", "missing-container", "unreachable"])
def test_commissioning_inventory_refuses_unaccepted_paths_and_missing_provenance(commissioned, mutation):
    c = commissioned
    commissioning_draft(c)
    if mutation == "scope": c.binding["files"] = ["specs/043-private-connectivity-production/evidence/other.json"]
    if mutation == "schema": c.record["schema"] = "other"
    if mutation == "definition": c.record["definition"] = "e" * 64
    if mutation == "missing-container": del c.record["source_container"]
    if mutation == "unreachable": c.record["raw_commit"] = "f" * 40
    c.path.write_text(json.dumps(c.record))
    original = c.path.read_bytes()
    with pytest.raises(ValueError):
        pins.process(c.verifier, "T010", write=True, commissioning=True)
    assert c.path.read_bytes() == original


def test_commissioning_check_requires_exact_immutable_anchor(commissioned):
    c = commissioned
    commissioning_draft(c)
    pins.process(c.verifier, "T010", write=True, commissioning=True)
    git(c.root, "add", c.relative)
    git(c.root, "commit", "-qm", "synthetic pending commissioning")
    c.verifier.trust_reference = dict(repository=LOCAL, commit=git(c.root, "rev-parse", "HEAD"),
                                     path=c.relative, sha256=v.digest(c.path.read_bytes()))
    c.path.write_text(c.path.read_text() + "\n")
    before = c.path.read_bytes()
    with pytest.raises(ValueError, match="differs from reviewed"):
        pins.process(c.verifier, "T010", commissioning=True)
    assert c.path.read_bytes() == before


def test_check_rejects_stale_inventory_without_repair(commissioned):
    c = commissioned; original = c.path.read_bytes()
    with pytest.raises(ValueError): pins.process(c.verifier, "T010", write=False)
    assert c.path.read_bytes() == original


@pytest.mark.parametrize("accepted", ["tracked", "reviewed-reference"])
def test_write_refuses_existing_committed_or_accepted_evidence(commissioned, accepted):
    c = commissioned
    if accepted == "tracked":
        git(c.root, "add", c.relative); git(c.root, "commit", "-qm", "existing observation")
    else:
        c.binding["record"] = dict(repository=LOCAL, commit=c.revision, path=c.relative, sha256="f" * 64)
    original = c.path.read_bytes()
    with pytest.raises(ValueError): pins.process(c.verifier, "T010", write=True)
    assert c.path.read_bytes() == original


def test_unaccepted_file_scope_or_owner_root_is_refused(commissioned):
    c = commissioned
    c.binding["files"] = ["elsewhere.json"]
    with pytest.raises(ValueError): pins.process(c.verifier, "T010", write=True)
    c.binding["files"] = [c.relative]
    git(c.root, "remote", "set-url", "origin", "https://github.com/other/repository.git")
    with pytest.raises(ValueError): v.GitStore({LOCAL: c.root})


@pytest.mark.parametrize("kind", ["file-symlink", "directory-symlink", "hardlink"])
def test_write_cannot_follow_links_outside_accepted_file(commissioned, tmp_path, kind):
    c = commissioned
    outside = tmp_path / "outside.json"; outside.write_text(json.dumps(c.record))
    if kind == "directory-symlink":
        c.path.unlink(); c.path.parent.rmdir(); c.path.parent.symlink_to(tmp_path, target_is_directory=True)
        (tmp_path / "T010.json").write_text(json.dumps(c.record))
    else:
        c.path.unlink()
        if kind == "file-symlink": c.path.symlink_to(outside)
        else: os.link(outside, c.path)
    original = outside.read_bytes()
    with pytest.raises(ValueError): pins.process(c.verifier, "T010", write=True)
    assert outside.read_bytes() == original


def test_unknown_bootstrap_or_uncommissioned_instance_cannot_create_record(commissioned):
    c = commissioned
    for task, instance in (("T999", None), ("T001", None), ("T010", "other")):
        with pytest.raises(ValueError): pins.process(c.verifier, task, instance, write=True)


def test_foreign_missing_checkout_or_undeclared_root_fails_closed(commissioned):
    c = commissioned
    data = deepcopy(c.record); data["artifact"] = dict(repository=FOREIGN, commit=B)
    c.path.write_text(json.dumps(data))
    original = c.path.read_bytes()
    with pytest.raises(ValueError): pins.process(c.verifier, "T010", write=True)
    assert c.path.read_bytes() == original


def test_cli_requires_explicit_mode_and_independent_trust():
    environment = {key: value for key, value in os.environ.items() if not key.startswith("PC_EVIDENCE_")}
    for arguments, message in ((["--task", "T010"], "required"), (["--task", "T010", "--check"], "PC_EVIDENCE_TRUST")):
        result = subprocess.run(["python3", str(FEATURE / "register-evidence-pins.py"), *arguments], capture_output=True, text=True, env=environment)
        assert result.returncode != 0
        assert message in result.stderr


def test_foreign_checkout_is_verified_and_each_commit_has_one_inventory_row(commissioned, tmp_path):
    c = commissioned
    other = tmp_path / "foreign"; other.mkdir()
    git(other, "init", "-q")
    git(other, "config", "user.name", "Synthetic Test")
    git(other, "config", "user.email", "test@example.invalid")
    git(other, "remote", "add", "origin", "https://github.com/opensoft/Headscale-Install.git")
    (other / "artifact").write_text("separate synthetic owner source")
    git(other, "add", "artifact"); git(other, "commit", "-qm", "synthetic foreign release")
    foreign = git(other, "rev-parse", "HEAD")
    c.verifier.trust["repositories"]["L"] = FOREIGN
    c.verifier.store = v.GitStore({LOCAL: c.root, FOREIGN: other})
    c.record["artifact"] = dict(repository=FOREIGN, commit=foreign)
    c.path.write_text(json.dumps(c.record))
    pins.process(c.verifier, "T010", write=True)
    rows = json.loads(c.path.read_text())["pin_inventory"]
    assert len(rows) == 2
    assert dict(repository=FOREIGN, foreign_commit=foreign) in rows
    pins.process(c.verifier, "T010", write=False)


def test_importing_verifier_for_check_does_not_create_owner_bytecode(commissioned):
    before = {str(path): path.stat().st_mtime_ns for path in FEATURE.rglob("*.pyc")}
    pins.verifier_module()
    assert before == {str(path): path.stat().st_mtime_ns for path in FEATURE.rglob("*.pyc")}


def test_child_inventory_requires_exact_commissioned_instance_file(commissioned):
    c = commissioned
    c.binding.update(task="T057", instance="first")
    c.verifier.trust["instances"] = {"T057": ["first"]}
    path = v.FEATURE_PATH + "/evidence/instances/T057/first.json"
    c.binding["files"] = [path]
    location = c.root / path; location.parent.mkdir(parents=True)
    data = dict(c.record, task="T057", instance="first")
    location.write_text(json.dumps(data))
    pins.process(c.verifier, "T057", "first", write=True)
    pins.process(c.verifier, "T057", "first", write=False)
    with pytest.raises(ValueError): pins.process(c.verifier, "T057", "unaccepted", write=True)


def test_inventory_check_admits_completed_execution_but_write_needs_current_authority(commissioned):
    from datetime import datetime, timezone

    c = commissioned
    verifier = object.__new__(v.Verifier)
    verifier.__dict__.update(c.verifier.__dict__)
    verifier.objects = {}
    del verifier.authority
    verifier.now = datetime(2030, 1, 2, tzinfo=timezone.utc)
    verifier.trust["revoked_authorities"] = []
    scope = {field: "not-applicable" for field in v.SCOPE_FIELDS}
    scope.update(phase="source", environment="source")
    c.binding.update(scope=scope, roles=["synthetic-source-owner"], decisions=[],
                     admission_roles=["synthetic-evidence-owner"])

    def save(name, value):
        path = c.root / name
        path.write_text(json.dumps(value, sort_keys=True))
        git(c.root, "add", name)
        git(c.root, "commit", "-qm", "synthetic immutable object")
        return dict(repository=LOCAL, commit=git(c.root, "rev-parse", "HEAD"), path=name,
                    sha256=v.digest(path.read_bytes()))

    authority = dict(id="completed-source", decision="accepted", owner="Synthetic Source Owner", mode="source",
                     roles=c.binding["roles"], scope=scope, decisions={},
                     valid_from="2029-01-01T00:00:00Z", valid_until="2030-01-01T00:02:00Z")
    c.binding["authority"] = save("authority.json", authority)
    output = save("output.json", dict(started_at="2030-01-01T00:00:00Z", ended_at="2030-01-01T00:01:00Z"))
    admission = dict(kind="evidence-admission", id="current-admission", decision="accepted", scope=scope,
                     owner="Synthetic Evidence Owner", roles=c.binding["admission_roles"],
                     authority=c.binding["authority"], reviewed_output_sha256=output["sha256"],
                     reviewed_at="2030-01-01T00:03:00Z", valid_from="2030-01-01T00:02:00Z",
                     valid_until="2031-01-01T00:00:00Z")
    c.binding["admission"] = save("admission.json", admission)
    record = {**c.record, "authority": c.binding["authority"], "admission": c.binding["admission"], "output": output}
    commits = pins.owner_commits(record, verifier)
    record["pin_inventory"] = pins.inventory(record, commits)
    c.path.write_text(json.dumps(record, sort_keys=True))
    git(c.root, "add", c.relative)
    git(c.root, "commit", "-qm", "synthetic accepted historical record")
    c.binding["record"] = dict(repository=LOCAL, commit=git(c.root, "rev-parse", "HEAD"),
                              path=c.relative, sha256=v.digest(c.path.read_bytes()))
    original = c.path.read_bytes()
    pins.process(verifier, "T010", write=False)
    assert c.path.read_bytes() == original
    with pytest.raises(ValueError):
        pins.process(verifier, "T010", write=True)
    verifier.trust["revoked_authorities"].append(admission["id"])
    with pytest.raises(ValueError, match="revoked"):
        pins.process(verifier, "T010", write=False)
    assert c.path.read_bytes() == original


def test_inventory_source_permission_remains_current_until_withdrawn(commissioned):
    from datetime import datetime, timezone

    c = commissioned
    verifier = object.__new__(v.Verifier)
    verifier.__dict__.update(c.verifier.__dict__)
    del verifier.authority
    verifier.now = datetime(2030, 1, 2, tzinfo=timezone.utc)
    verifier.trust["revoked_authorities"] = []
    scope = {field: "not-applicable" for field in v.SCOPE_FIELDS}
    scope.update(phase="source", environment="source")
    c.binding.update(scope=scope, roles=["synthetic-source-owner"], decisions=[])
    authority = dict(id="source-scope", decision="accepted", owner="Synthetic Source Owner", mode="source",
                     roles=c.binding["roles"], scope=scope, decisions={},
                     valid_from="2029-01-01T00:00:00Z", valid_until="until-superseded")
    path = c.root / "source-authority.json"
    path.write_text(json.dumps(authority))
    git(c.root, "add", "source-authority.json")
    git(c.root, "commit", "-qm", "synthetic source permission")
    c.binding["authority"] = dict(repository=LOCAL, commit=git(c.root, "rev-parse", "HEAD"),
                                  path="source-authority.json", sha256=v.digest(path.read_bytes()))
    c.record["authority"] = c.binding["authority"]
    c.path.write_text(json.dumps(c.record))
    pins.process(verifier, "T010", write=True)
    pins.process(verifier, "T010", write=False)
    original = c.path.read_bytes()
    verifier.trust["revoked_authorities"].append(authority["id"])
    for write in (False, True):
        with pytest.raises(ValueError, match="revoked"):
            pins.process(verifier, "T010", write=write)
        assert c.path.read_bytes() == original
