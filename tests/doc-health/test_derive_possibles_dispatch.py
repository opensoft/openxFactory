"""Derive-possibles nightly lane dispatch orchestration
(`derive_possibles_dispatch.py`; openxFactory add-possibles-derivation-lane,
change tasks 4.1/4.2/4.4).

Hermetic: no live model calls (the artifact-only child's raw per-cluster
output is a plain JSON fixture standing in for its findings artifact), a FAKE
validator script stands in for the pinned openxFactory validator, git facts
come from `conftest.FakeGit`, and every write lands under `tmp_path` — never
the shared openxFactory checkout.
"""

from __future__ import annotations

import json
from pathlib import Path

from conftest import AS_OF, FakeGit, REPO_ROOT  # noqa: F401 (sys.path side effect)

from doc_health import derive_possibles as dp
from doc_health import derive_possibles_dispatch as dpd
from doc_health import readiness_dispatch as rd
from doc_health import report as report_mod

REV = "a7aac777bedfb83dbb957819a7753436bdabd334"
PASSAGE_A = ("Body prose for alpha-1.md describing the recurring subject "
             "in detail.")
PASSAGE_B = ("Body prose for beta-1.md describing the recurring subject "
             "in detail.")


def doc_text(name: str, *, status="staged", topics=None) -> str:
    lines = [f"# {name}", "", f"Status: {status}"]
    if topics:
        lines.append("Topics: " + ", ".join(topics))
    lines += ["", "## Body", "", f"Body prose for {name} describing the "
              "recurring subject in detail."]
    return "\n".join(lines) + "\n"


def index_yaml(register=None) -> str:
    import yaml
    index = {
        "schema_version": 1, "kind": "ideation-cross-reference",
        "repository": "openxFactory",
        "generation": {"source_revision": REV, "generator_version": "test"},
        "topic_entries": [
            {"id": "cl-alpha", "name": "Alpha", "topics": ["alpha"],
             "members": [
                 {"path": "ideation/brainstorm/alpha-1.md", "stage": "staged"},
                 {"path": "ideation/brainstorm/alpha-2.md", "stage": "staged"},
             ]},
            {"id": "cl-beta", "name": "Beta", "topics": ["beta"],
             "members": [
                 {"path": "ideation/staging/beta/beta-1.md", "stage": "staged"},
                 {"path": "ideation/staging/beta/beta-2.md", "stage": "staged"},
             ]},
        ],
    }
    if register is not None:
        index["possibles_register"] = register
    return yaml.safe_dump(index, sort_keys=False)


def make_agg_root(tmp_path: Path, register=None) -> Path:
    """A miniature aggregation root: a WRITABLE fake `openxFactory` checkout
    (never the shared one) with two clusters' member docs AND the landed
    index the derive lane reads."""
    openx = tmp_path / "openxFactory"
    brainstorm = openx / "ideation" / "brainstorm"
    brainstorm.mkdir(parents=True)
    (brainstorm / "alpha-1.md").write_text(
        doc_text("alpha-1.md", topics=["alpha"]), encoding="utf-8")
    (brainstorm / "alpha-2.md").write_text(
        doc_text("alpha-2.md", topics=["alpha"]), encoding="utf-8")
    staging = openx / "ideation" / "staging" / "beta"
    staging.mkdir(parents=True)
    (staging / "beta-1.md").write_text(
        doc_text("beta-1.md", topics=["beta"]), encoding="utf-8")
    (staging / "beta-2.md").write_text(
        doc_text("beta-2.md", topics=["beta"]), encoding="utf-8")
    (openx / "ideation" / "cross-reference.yaml").write_text(
        index_yaml(register), encoding="utf-8")
    return tmp_path


def undisposed_derived(cid="cl-alpha"):
    return {"id": "pos-derived-pending", "title": "Pending", "claim": "P.",
            "state": "latent", "origin": "ai-derived",
            "provenance": {"document": "d", "section": "s"},
            "derivation": {"worker_run": {
                "correlation_id": "DPOSS-x",
                "worker_profile": "derive-possibles",
                "prompt_contract_version": "derive-possibles-prompt-v1"},
                "disposition": "pending_review"},
            "claiming_clusters": [cid],
            "supporting_evidence": [{"document": "d", "section": "s",
                                     "passage_sha256": "0" * 64}]}


def fake_validator(tmp_path: Path, *, accept: bool = True) -> Path:
    script = tmp_path / "fake_validator.py"
    script.write_text(
        f"import sys\nsys.exit(0 if {accept!r} else 1)\n", encoding="utf-8")
    return script


def _candidates(passage, path, n=1):
    return {"candidates": [
        {"title": f"Candidate {path.rsplit('/', 1)[-1]} {i}",
         "claim": f"This cluster could become capability {i} of {path}.",
         "rationale": "members converge", "path": path,
         "section": "Body", "passage": passage}
        for i in range(n)]}


def child_findings() -> dict:
    """A findings.json fixture standing in for the artifact-only child's raw
    per-cluster output, keyed by cluster id exactly as
    `merge_derive_results` expects."""
    return {
        "cl-alpha": {"output": _candidates(
            PASSAGE_A, "ideation/brainstorm/alpha-1.md")},
        "cl-beta": {"output": _candidates(
            PASSAGE_B, "ideation/staging/beta/beta-1.md")},
    }


def _write_fake_renderer(root: Path) -> Path:
    scripts = root / "scripts"
    scripts.mkdir(parents=True)
    (scripts / "render-ideation-cross-reference.py").write_text(
        "def render_markdown(index):\n    return '# projection\\n'\n",
        encoding="utf-8")
    return root


def merge(agg, tmp_path, *, findings=None, monkeypatch=None, **kw):
    if monkeypatch is not None:
        monkeypatch.setenv("OPENXFACTORY_ROOT",
                           str(_write_fake_renderer(tmp_path / "fake-openx")))
    findings_path = None
    if findings is not None:
        findings_path = tmp_path / "findings.json"
        findings_path.write_text(json.dumps(findings), encoding="utf-8")
    if "validator" not in kw:
        kw["validator"] = fake_validator(tmp_path)
    kw.setdefault("git", FakeGit(heads={"openxFactory": REV}))
    return dpd.merge_derive_results(agg, as_of=AS_OF, run_id="dposs-1",
                                    findings_path=findings_path, **kw)


# --- prepare phase ------------------------------------------------------

def test_prepare_writes_one_untrusted_payload_per_eligible_cluster(tmp_path):
    agg = make_agg_root(tmp_path)
    out_dir = tmp_path / "bundle"
    manifest = dpd.prepare_derive_bundle(agg, out_dir, run_id="run-1")
    assert manifest["cluster_count"] == 2
    assert sorted(manifest["cluster_ids"]) == ["cl-alpha", "cl-beta"]
    for cid in manifest["cluster_ids"]:
        payload = (out_dir / "clusters" / f"{cid}.txt").read_text("utf-8")
        assert "Untrusted cluster payload" in payload
        assert cid in payload
        assert "existing_possibles" in payload  # dedupe-steering context
    assert json.loads((out_dir / "output.schema.json").read_text("utf-8")) \
        == dp.WORKER_OUTPUT_SCHEMA


def test_prepare_skips_clusters_with_an_undisposed_derived_possible(tmp_path):
    agg = make_agg_root(tmp_path, register=[undisposed_derived("cl-alpha")])
    manifest = dpd.prepare_derive_bundle(agg, tmp_path / "bundle",
                                         run_id="run-1")
    assert manifest["cluster_ids"] == ["cl-beta"]


def test_prepare_with_no_index_writes_empty_manifest(tmp_path):
    (tmp_path / "openxFactory").mkdir()
    manifest = dpd.prepare_derive_bundle(tmp_path, tmp_path / "bundle",
                                         run_id="run-1")
    assert manifest["cluster_count"] == 0
    assert manifest["cluster_ids"] == []


# --- merge phase: happy path ----------------------------------------------

def test_merge_happy_path_persists_the_register_and_evidence(tmp_path,
                                                             monkeypatch):
    agg = make_agg_root(tmp_path)
    meta = merge(agg, tmp_path, findings=child_findings(),
                 monkeypatch=monkeypatch)
    assert meta.ok, meta.skipped_reason
    assert meta.persisted and meta.validated is True
    assert len(meta.merged_added) == 2
    assert meta.status_json()["persisted"] is True
    import yaml
    index = yaml.safe_load(
        (agg / "openxFactory/ideation/cross-reference.yaml").read_text())
    register = index["possibles_register"]
    assert [e["id"] for e in register] == meta.merged_added
    for entry in register:
        assert entry["origin"] == "ai-derived"
        assert entry["derivation"]["disposition"] == "pending_review"
    # topic entries pass through untouched
    assert [e["id"] for e in index["topic_entries"]] == ["cl-alpha", "cl-beta"]
    evidence = agg / ("openxFactory/health/derive-possibles/"
                      f"{AS_OF.isoformat()}/dposs-1.yaml")
    assert evidence.is_file()
    record = yaml.safe_load(evidence.read_text(encoding="utf-8"))
    assert record["kind"] == "derive_possibles_run"
    assert record["register_fingerprint_read"] != \
        record["register_fingerprint_written"]
    assert "OK 2 possible(s)" in meta.log_line()


def test_one_failed_cluster_never_loses_the_other(tmp_path, monkeypatch):
    findings = child_findings()
    findings["cl-alpha"] = {"error": "worker timed out"}
    agg = make_agg_root(tmp_path)
    meta = merge(agg, tmp_path, findings=findings, monkeypatch=monkeypatch)
    assert meta.ok
    assert len(meta.merged_added) == 1
    assert any("worker timed out" in reason
               for _cid, reason in meta.skipped_clusters)


def test_merge_report_section_links_outcome_and_never_touches_ranked_plan(
        tmp_path, monkeypatch):
    agg = make_agg_root(tmp_path)
    meta = merge(agg, tmp_path, findings=child_findings(),
                 monkeypatch=monkeypatch)
    rendered = ("# Doc Health\n\n## Ranked Plan\n\nNo findings.\n\n"
                "## Findings By Family\n\nnone\n")
    out = report_mod.insert_derive_possibles_section(rendered, meta)
    assert "## Derived Possibles" in out
    assert out.index("## Derived Possibles") < out.index(
        "## Findings By Family")
    for pid in meta.merged_added:
        assert pid in out
    # the Ranked Plan stays byte-identical (exclusion by contract)
    plan = out[out.index("## Ranked Plan"):out.index("## Derived Possibles")]
    assert plan == "## Ranked Plan\n\nNo findings.\n\n"


# --- merge phase: skip paths (the lane never blocks, never mutates) ---------

def _register_unchanged(agg) -> bool:
    import yaml
    index = yaml.safe_load(
        (agg / "openxFactory/ideation/cross-reference.yaml").read_text())
    return "possibles_register" not in index


def test_explicit_unavailable_reason_skips(tmp_path):
    agg = make_agg_root(tmp_path)
    meta = merge(agg, tmp_path, unavailable_reason="worker_unavailable")
    assert not meta.ok and meta.skipped_reason == "worker_unavailable"
    assert not meta.persisted and _register_unchanged(agg)
    assert "SKIPPED" in meta.log_line()


def test_missing_findings_artifact_skips(tmp_path):
    agg = make_agg_root(tmp_path)
    meta = merge(agg, tmp_path)
    assert meta.skipped_reason == dpd.WORKER_UNAVAILABLE
    assert _register_unchanged(agg)


def test_malformed_findings_artifact_skips(tmp_path):
    agg = make_agg_root(tmp_path)
    findings_path = tmp_path / "findings.json"
    findings_path.write_text("[]", encoding="utf-8")
    meta = dpd.merge_derive_results(
        agg, as_of=AS_OF, run_id="dposs-1", findings_path=findings_path,
        validator=fake_validator(tmp_path),
        git=FakeGit(heads={"openxFactory": REV}))
    assert "malformed" in meta.skipped_reason
    assert _register_unchanged(agg)


def test_rejected_index_is_never_persisted(tmp_path, monkeypatch):
    agg = make_agg_root(tmp_path)
    meta = merge(agg, tmp_path, findings=child_findings(),
                 monkeypatch=monkeypatch,
                 validator=fake_validator(tmp_path, accept=False))
    assert meta.validated is False
    assert "rejected by the pinned validator" in meta.skipped_reason
    assert not meta.persisted and _register_unchanged(agg)


def test_unresolvable_head_skips(tmp_path):
    agg = make_agg_root(tmp_path)
    meta = merge(agg, tmp_path, findings=child_findings(), git=FakeGit())
    assert "cannot resolve openxFactory HEAD" in meta.skipped_reason
    assert _register_unchanged(agg)


def test_no_openxfactory_checkout_skips(tmp_path):
    meta = dpd.merge_derive_results(
        tmp_path, as_of=AS_OF, run_id="dposs-1")
    assert meta.skipped_reason == "openxFactory checkout not found"


def test_all_duplicate_proposals_skip_without_persisting(tmp_path,
                                                         monkeypatch):
    # the register already carries DISPOSED derived entries with the same
    # claims: derivation dedupe voids everything -> nothing survives ->
    # SKIPPED, register untouched.
    entry_a = undisposed_derived("cl-alpha")
    entry_a["claim"] = ("This cluster could become capability 0 of "
                        "ideation/brainstorm/alpha-1.md.")
    entry_a["derivation"]["human_disposition"] = {
        "outcome": "rejected", "authority": "gate"}
    entry_a.update(state="rejected", reason="r", citation="c")
    entry_b = dict(undisposed_derived("cl-beta"))
    entry_b["id"] = "pos-derived-pending-b"
    entry_b["claim"] = ("This cluster could become capability 0 of "
                        "ideation/staging/beta/beta-1.md.")
    entry_b["derivation"] = dict(entry_b["derivation"])
    entry_b["derivation"]["human_disposition"] = {
        "outcome": "rejected", "authority": "gate"}
    entry_b.update(state="rejected", reason="r", citation="c")
    agg = make_agg_root(tmp_path, register=[entry_a, entry_b])
    meta = merge(agg, tmp_path, findings=child_findings(),
                 monkeypatch=monkeypatch)
    assert not meta.ok
    assert "no proposal survived" in meta.skipped_reason
    assert len(meta.voided) == 2  # both reported as duplicates


def test_stale_register_between_read_and_merge_is_refused(tmp_path,
                                                          monkeypatch):
    agg = make_agg_root(tmp_path)
    real_load = dpd._load_index
    calls = {"n": 0}

    def racy_load(openx):
        index = real_load(openx)
        calls["n"] += 1
        if calls["n"] > 1 and index is not None:
            # a concurrent run advanced the register after our first read
            index["possibles_register"] = [undisposed_derived("cl-gamma")]
        return index
    monkeypatch.setattr(dpd, "_load_index", racy_load)
    meta = merge(agg, tmp_path, findings=child_findings(),
                 monkeypatch=monkeypatch)
    assert not meta.ok
    assert "stale overwrite refused" in meta.skipped_reason
    assert _register_unchanged(agg)


# --- integration: the readiness re-score preserves the register -------------

def test_readiness_merge_carries_the_possibles_register_through(tmp_path,
                                                                monkeypatch):
    monkeypatch.setenv("OPENXFACTORY_ROOT",
                       str(_write_fake_renderer(tmp_path / "fake-openx")))
    register = [undisposed_derived("cl-alpha")]
    agg = make_agg_root(tmp_path, register=register)

    def tier_output(passage):
        return {"tiers": [
            {"tier": name, "score": 9, "section": "Body", "passage": passage,
             "rationale": "judged", "confidence": 0.8, "alternatives": []}
            for name in ("domain", "company", "project")],
            "extension_fit": {"has_promoted_fit": False,
                              "statement": "no promoted capability."}}
    findings_path = tmp_path / "readiness-findings.json"
    findings_path.write_text(json.dumps({
        "cl-alpha": {"output": tier_output(PASSAGE_A)},
        "cl-beta": {"output": tier_output(PASSAGE_B)},
    }), encoding="utf-8")
    meta = rd.merge_readiness_findings(
        agg, as_of=AS_OF, run_id="readiness-1",
        findings_path=findings_path, validator=fake_validator(tmp_path),
        git=FakeGit(heads={"openxFactory": REV}))
    assert meta.ok, meta.skipped_reason
    import yaml
    index = yaml.safe_load(
        (agg / "openxFactory/ideation/cross-reference.yaml").read_text())
    # the readiness re-score NEVER drops the derive-possibles lane's register
    assert index["possibles_register"] == register


# --- CLI ---------------------------------------------------------------------

def test_cli_merge_writes_status_json_and_never_fails(tmp_path, monkeypatch,
                                                      capsys):
    agg = make_agg_root(tmp_path)
    monkeypatch.chdir(tmp_path)
    status_out = tmp_path / "status.json"
    # no findings artifact -> SKIPPED, exit 0 (the lane never fails the
    # nightly), status persisted=false
    rc = dpd.main(["--repo-root", str(agg), "--phase", "merge",
                   "--as-of", AS_OF.isoformat(), "--run-id", "dposs-cli",
                   "--status-out", str(status_out)])
    assert rc == 0
    assert "SKIPPED" in capsys.readouterr().out
    status = json.loads(status_out.read_text(encoding="utf-8"))
    assert status["persisted"] is False


# --- per-run derivation budget (the rescored index carries every cluster) ---

def test_prepare_budget_caps_eligible_clusters_richest_first(tmp_path):
    import yaml as yaml_mod
    agg = make_agg_root(tmp_path)
    openx = agg / "openxFactory"
    index = yaml_mod.safe_load(
        (openx / "ideation/cross-reference.yaml").read_text())
    # inflate the index well past the budget: 14 single-member clusters plus
    # the two rich two-member fixtures
    for i in range(14):
        index["topic_entries"].append(
            {"id": f"cl-extra{i:02d}", "name": f"Extra {i}",
             "members": [{"path": "ideation/brainstorm/alpha-1.md",
                          "stage": "staged"}]})
    (openx / "ideation/cross-reference.yaml").write_text(
        yaml_mod.safe_dump(index), encoding="utf-8")

    manifest = dpd.prepare_derive_bundle(agg, tmp_path / "bundle",
                                         run_id="run-1")
    assert manifest["cluster_count"] == dpd.MAX_CLUSTERS_PER_RUN
    bundled = manifest["cluster_ids"]
    # richest member sets first: both two-member clusters make the cut
    assert "cl-alpha" in bundled and "cl-beta" in bundled
