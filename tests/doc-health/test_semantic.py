"""Semantic sweep: inventory, Hermes-layer scope resolution, finding
contract enforcement, disposer assignment, and the skipped-sweep path.
The analysis invocation is always faked — these tests are hermetic."""

from __future__ import annotations

import json
from datetime import date

from conftest import make_ctx  # noqa: F401  (sys.path side effect)

from doc_health import CONTESTED, WARNING
from doc_health.corpus import Doc
from doc_health import report, semantic

AS_OF = date(2026, 7, 9)          # a Thursday
SUNDAY = date(2026, 7, 12)


def make_docs():
    return [
        Doc("alpha", "docs/a.md", "alpha doc body", "draft"),
        Doc("alpha", "docs/b.md", "beta doc body", "ratified"),
        Doc("openxFactory", "docs/n.md", "neutral doc body", "standard"),
    ]


# --- inventory ---------------------------------------------------------------

def test_inventory_is_sorted_and_hashed():
    inv = semantic.build_inventory(make_docs())
    assert [(e["repo"], e["path"]) for e in inv] == [
        ("alpha", "docs/a.md"), ("alpha", "docs/b.md"),
        ("openxFactory", "docs/n.md")]
    assert all(len(e["content_hash"]) == 64 for e in inv)


def test_changed_paths_detects_new_and_modified_only():
    old = semantic.build_inventory(make_docs())
    docs = make_docs()
    docs[0] = Doc("alpha", "docs/a.md", "EDITED body", "draft")
    docs.append(Doc("alpha", "docs/new.md", "brand new", "draft"))
    changed = semantic.changed_paths(semantic.build_inventory(docs), old)
    assert changed == {("alpha", "docs/a.md"), ("alpha", "docs/new.md")}


# --- Hermes-layer scope resolution --------------------------------------------

def hermes_repo(tmp_path, name, layer, scope):
    repo = tmp_path / name
    d = repo / "hermes" / layer
    d.mkdir(parents=True)
    (d / "overlay.yaml").write_text(
        f"doc_health:\n  sweep_scope: {scope}\n", encoding="utf-8")
    return repo


def test_scope_defaults_when_nothing_declared(tmp_path):
    (tmp_path / "alpha").mkdir()
    scope, layer = semantic.resolve_scope({"alpha": tmp_path / "alpha"})
    assert (scope, layer) == ("incremental", None)


def test_deepest_declaration_wins(tmp_path):
    repos = {
        "alpha": hermes_repo(tmp_path, "alpha", "client", "full-weekly"),
        "beta": hermes_repo(tmp_path, "beta", "domain", "full-nightly"),
    }
    scope, layer = semantic.resolve_scope(repos)
    assert scope == "full-nightly"
    assert layer == "beta/domain"


def test_no_layer_can_lower_another(tmp_path):
    repos = {
        "alpha": hermes_repo(tmp_path, "alpha", "subject", "full-nightly"),
        "beta": hermes_repo(tmp_path, "beta", "client", "incremental"),
    }
    scope, layer = semantic.resolve_scope(repos)
    assert scope == "full-nightly"
    assert layer == "alpha/customer"  # subject dir maps to customer role


def test_unknown_scope_values_are_ignored(tmp_path):
    repos = {"alpha": hermes_repo(tmp_path, "alpha", "client", "everything")}
    assert semantic.resolve_scope(repos) == ("incremental", None)


# --- corpus selection ----------------------------------------------------------

def test_full_nightly_sweeps_everything():
    inv = semantic.build_inventory(make_docs())
    corpus_entries, desc = semantic.select_corpus(inv, "full-nightly", AS_OF, inv)
    assert corpus_entries == inv and "full corpus" in desc


def test_incremental_weekday_sweeps_changed_only():
    old = semantic.build_inventory(make_docs())
    docs = make_docs()
    docs[0] = Doc("alpha", "docs/a.md", "EDITED", "draft")
    corpus_entries, desc = semantic.select_corpus(
        semantic.build_inventory(docs), "incremental", AS_OF, old)
    assert [e["path"] for e in corpus_entries] == ["docs/a.md"]
    assert "changed docs only" in desc


def test_incremental_sunday_and_no_previous_sweep_full():
    inv = semantic.build_inventory(make_docs())
    full_sunday, _ = semantic.select_corpus(inv, "incremental", SUNDAY, inv)
    full_baseline, _ = semantic.select_corpus(inv, "incremental", AS_OF, None)
    assert full_sunday == inv and full_baseline == inv


# --- finding contract ------------------------------------------------------------

def valid_raw(**over):
    raw = {"family": "semantic-normative-prose", "repo": "alpha",
           "path": "docs/a.md", "passage": "Workers must always retry.",
           "confidence": "medium"}
    raw.update(over)
    return raw


def test_contract_enforcement_accepts_and_annotates():
    inv = semantic.build_inventory(make_docs())
    findings, dropped = semantic.enforce_contract([valid_raw()], inv)
    assert not dropped and len(findings) == 1
    f = findings[0]
    assert f.severity == WARNING and f.resolution == CONTESTED
    assert f.family == "semantic-normative-prose"
    assert "[id=" in f.rule and "confidence=medium" in f.rule
    assert f.disposer == "alpha authority (Domain Hermes)"
    assert "never merge-blocking in v1" in f.action


def test_contract_enforcement_drops_malformed():
    inv = semantic.build_inventory(make_docs())
    bad = [
        valid_raw(family="made-up-family"),
        valid_raw(passage="  "),
        valid_raw(confidence="certain"),
        valid_raw(path="docs/invented.md"),
        valid_raw(family="semantic-contradiction"),  # no conflicts_with
        "not an object",
    ]
    findings, dropped = semantic.enforce_contract(bad, inv)
    assert not findings and len(dropped) == 6


def test_disposer_follows_content_ownership():
    assert semantic.assign_disposer("alpha", None) == \
        "alpha authority (Domain Hermes)"
    assert semantic.assign_disposer("openxFactory", None) == \
        "openxFactory ratify gate"
    assert semantic.assign_disposer(
        "alpha", "openxFactory/openspec/specs/doc-health/spec.md — X") == \
        "openxFactory ratify gate"


def test_stable_ids_survive_whitespace_changes():
    a = semantic.passage_id("r", "p.md", "Workers  must\nalways retry.")
    b = semantic.passage_id("r", "p.md", "Workers must always retry.")
    assert a == b and len(a) == 10


# --- the sweep orchestration -------------------------------------------------------

def test_run_sweep_success_path(tmp_path):
    docs = make_docs()
    raw = json.dumps([valid_raw(),
                      valid_raw(family="semantic-contradiction",
                                repo="openxFactory", path="docs/n.md",
                                passage="neutral doc body",
                                conflicts_with="openxFactory/openspec/specs/doc-health/spec.md — Health report contract")])
    findings, meta = semantic.run_sweep(
        {"alpha": tmp_path}, docs, AS_OF, None, None,
        invoke=lambda prompt, model: f"Here you go:\n{raw}\nDone.")
    assert len(findings) == 2 and meta.skipped_reason is None
    assert meta.prompt_version == "2"
    assert meta.envelope_ref.startswith("SEMSWEEP-")
    assert {f.disposer for f in findings} == {
        "alpha authority (Domain Hermes)", "openxFactory ratify gate"}


def test_run_sweep_failure_is_recorded_not_raised(tmp_path):
    def broken(prompt, model):
        raise RuntimeError("model unavailable")
    findings, meta = semantic.run_sweep(
        {"alpha": tmp_path}, make_docs(), AS_OF, None, None, invoke=broken)
    assert findings == [] and "model unavailable" in meta.skipped_reason


def test_run_sweep_writes_envelope(tmp_path):
    semantic.run_sweep({"alpha": tmp_path}, make_docs(), AS_OF, tmp_path,
                       None, invoke=lambda p, m: '{"findings": []}')
    env = tmp_path / "health" / "envelopes" / "2026-07-09-semantic-sweep.yaml"
    assert env.is_file()
    text = env.read_text(encoding="utf-8")
    assert "issued_by: Hermes" in text
    assert "auth_profile: read_only_no_credentials" in text


# --- dispatch mode: bundle prepare and findings merge ---------------------------

def test_prepare_bundle_is_self_contained(tmp_path):
    repo = tmp_path / "alpha"
    spec_dir = repo / "openspec" / "specs" / "cap"
    spec_dir.mkdir(parents=True)
    (spec_dir / "spec.md").write_text("# cap spec\n", encoding="utf-8")
    out = tmp_path / "bundle"
    meta = semantic.prepare_bundle(
        {"alpha": repo}, make_docs(), AS_OF, None, out,
        allowed_output_root=tmp_path)
    assert (out / "corpus" / "alpha" / "docs" / "a.md").read_text(
        encoding="utf-8") == "alpha doc body"
    assert (out / "corpus" / "alpha" / "openspec" / "specs" / "cap"
            / "spec.md").is_file()  # grounding specs always ship
    prompt = (out / "analysis-input.txt").read_text(encoding="utf-8")
    assert "docs/a.md" in prompt and "alpha doc body" in prompt
    assert (out / "findings.schema.json").is_file()
    assert json.loads((out / "inventory.json").read_text()) == \
        semantic.build_inventory(make_docs())
    saved = json.loads((out / "meta.json").read_text(encoding="utf-8"))
    assert saved == meta
    assert meta["corpus_size"] == 3 and meta["prompt_version"] == "2"
    assert meta["envelope_ref"].startswith("SEMSWEEP-")


def test_prepare_bundle_rejects_inventory_from_another_snapshot(tmp_path):
    inventory = semantic.build_inventory(make_docs())
    inventory[0]["content_hash"] = "0" * 64
    try:
        semantic.prepare_bundle(
            {"alpha": tmp_path}, make_docs(), AS_OF, None,
            tmp_path / "bundle", inventory=inventory,
            allowed_output_root=tmp_path)
    except ValueError as exc:
        assert "differs from the deterministic corpus" in str(exc)
    else:
        raise AssertionError("mismatched inventory was accepted")


def test_prepare_bundle_rejects_output_outside_boundary(tmp_path):
    try:
        semantic.prepare_bundle(
            {"alpha": tmp_path}, make_docs(), AS_OF, None,
            tmp_path.parent / "outside-bundle",
            allowed_output_root=tmp_path)
    except ValueError as exc:
        assert "output escapes" in str(exc)
    else:
        raise AssertionError("out-of-bound bundle output was accepted")


def test_findings_file_invoke_reads_artifact(tmp_path):
    artifact = tmp_path / "findings.json"
    artifact.write_text('[{"a": 1}]', encoding="utf-8")
    assert semantic.findings_file_invoke(artifact)("p", "m") == '[{"a": 1}]'


def test_findings_file_invoke_missing_is_worker_offline(tmp_path):
    findings, meta = semantic.run_sweep(
        {"alpha": tmp_path}, make_docs(), AS_OF, None, None,
        invoke=semantic.findings_file_invoke(tmp_path / "absent.json"))
    assert findings == []
    assert "no findings artifact from the omnigent worker" in meta.skipped_reason


def test_findings_file_invoke_preserves_readiness_reason(tmp_path):
    findings, meta = semantic.run_sweep(
        {"alpha": tmp_path}, make_docs(), AS_OF, None, None,
        invoke=semantic.findings_file_invoke(
            tmp_path / "absent.json", "heartbeat_stale"))
    assert findings == []
    assert "heartbeat_stale" in meta.skipped_reason


# --- report integration ---------------------------------------------------------

def test_report_carries_semantic_section_and_disposer():
    inv = semantic.build_inventory(make_docs())
    findings, _ = semantic.enforce_contract([valid_raw()], inv)
    meta = semantic.SweepMeta(
        scope="changed docs only (1 of 3, scope incremental)",
        declared_by="alpha/client", corpus_size=1, total_docs=3,
        model="claude-sonnet-5", prompt_version="1",
        envelope_ref="SEMSWEEP-abc")
    text = report.render(AS_OF, findings, [], [], make_docs(), 10, [], [],
                         semantic_meta=meta)
    assert "## Semantic Sweep" in text
    assert "declared by alpha/client" in text
    assert "### semantic-normative-prose" in text
    plan = [l for l in text.splitlines() if l.startswith("- severity=")]
    m = report.PLAN_RE.match(plan[0])
    assert m and m.group(7) == "contested"
    assert m.group(8) == "alpha authority (Domain Hermes)"


def test_report_records_skipped_sweep():
    meta = semantic.SweepMeta(
        scope="full corpus (no previous inventory, scope incremental)",
        declared_by=None, corpus_size=3, total_docs=3,
        model="claude-sonnet-5", prompt_version="1",
        envelope_ref="SEMSWEEP-abc",
        skipped_reason="analysis worker failed: model unavailable")
    text = report.render(AS_OF, [], [], [], make_docs(), 10, [], [],
                         semantic_meta=meta)
    assert "Skipped: analysis worker failed: model unavailable" in text
    assert "contract default" in text


def test_worker_output_parsing_tolerates_prose():
    assert semantic.parse_worker_output("[]") == []
    assert semantic.parse_worker_output('noise [{"a": 1}] trailing') == [{"a": 1}]
    wrapped = '{"structured_output":{"findings":[{"a":1}]}}'
    assert semantic.parse_worker_output(wrapped) == [{"a": 1}]


def test_real_invoke_is_stdin_only_and_disables_tools(monkeypatch):
    captured = {}

    class Result:
        returncode = 0
        stdout = '{"structured_output":{"findings":[]}}'
        stderr = ""

    def fake_run(command, **kwargs):
        captured["command"] = command
        captured.update(kwargs)
        return Result()

    monkeypatch.setattr(semantic.subprocess, "run", fake_run)
    semantic.real_invoke("private corpus", "test-model")
    command = captured["command"]
    assert captured["input"] == "private corpus"
    assert "private corpus" not in command
    assert command[command.index("--tools") + 1] == ""
    assert "--no-session-persistence" in command
    assert "--json-schema" in command
    assert captured["env"]["CLAUDE_CODE_SKIP_PROMPT_HISTORY"] == "1"
    assert "GITHUB_TOKEN" not in captured["env"]
