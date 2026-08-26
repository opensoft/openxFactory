"""Ideation-readiness nightly lane dispatch orchestration
(`readiness_dispatch.py`; openxFactory add-ideation-cross-reference-readiness,
change tasks 4.1/4.3).

Hermetic: no live model calls (the artifact-only child's raw per-cluster
output is a plain JSON fixture, standing in for its findings artifact), a
FAKE validator script stands in for the pinned openxFactory validator (a
separate test proves the wiring against the REAL one, skipped if
unreachable), git facts come from `conftest.FakeGit`, and every write lands
under `tmp_path` — never the shared openxFactory checkout.
"""

from __future__ import annotations

import json
import os
from datetime import date
from pathlib import Path

import pytest

from conftest import AS_OF, FakeGit, REPO_ROOT  # noqa: F401 (sys.path side effect)

from doc_health import ideation_readiness as ir
from doc_health import readiness_dispatch as rd

REV = "a7aac777bedfb83dbb957819a7753436bdabd334"


def doc_text(name: str, *, status="staged", topics=None, caps=None) -> str:
    lines = [f"# {name}", "", f"Status: {status}"]
    if topics:
        lines.append("Topics: " + ", ".join(topics))
    if caps:
        lines.append("Target capabilities: " + ", ".join(caps))
    lines += ["", "## Body", "", f"Body prose for {name} describing the "
             "recurring subject in detail."]
    return "\n".join(lines) + "\n"


def make_agg_root(tmp_path: Path) -> Path:
    """A miniature, fully self-contained aggregation root: a WRITABLE fake
    `openxFactory` checkout (never the shared one) with two clusterable
    topics (alpha: 2 docs, beta: 2 docs)."""
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
        doc_text("beta-1.md", topics=["beta"], caps=["beta"]),
        encoding="utf-8")
    (staging / "beta-2.md").write_text(
        doc_text("beta-2.md", topics=["beta"]), encoding="utf-8")
    return tmp_path


def fake_validator(tmp_path: Path, *, accept: bool = True) -> Path:
    script = tmp_path / "fake_validator.py"
    script.write_text(
        "import sys\n"
        f"sys.exit(0 if {accept!r} else 1)\n",
        encoding="utf-8")
    return script


def _tier_output(passage: str, score=9):
    return {"tiers": [
        {"tier": name, "score": score, "section": "Body", "passage": passage,
         "rationale": f"{name} judged {score}", "confidence": 0.8,
         "alternatives": []}
        for name in ir.TIER_NAMES],
        "extension_fit": {"has_promoted_fit": False,
                          "statement": "no promoted capability evaluated."}}


def cluster_findings(agg_root: Path, *, passage_alpha="recurring subject in "
                     "detail", passage_beta="recurring subject in detail",
                     score=9) -> dict:
    """A findings.json fixture standing in for the artifact-only child's raw
    per-cluster output, keyed by cluster id exactly as
    `merge_readiness_findings` expects."""
    return {
        "cl-alpha": {"output": _tier_output(passage_alpha, score)},
        "cl-beta": {"output": _tier_output(passage_beta, score)},
    }


# --- prepare phase ------------------------------------------------------

def test_prepare_writes_one_untrusted_payload_file_per_cluster(tmp_path):
    agg = make_agg_root(tmp_path)
    out_dir = tmp_path / "bundle"
    manifest = rd.prepare_readiness_bundle(agg, out_dir, run_id="run-1")
    assert manifest["cluster_count"] == 2
    assert sorted(manifest["cluster_ids"]) == ["cl-alpha", "cl-beta"]
    for cid in manifest["cluster_ids"]:
        payload = (out_dir / "clusters" / f"{cid}.txt").read_text("utf-8")
        assert "Untrusted cluster payload" in payload
        assert cid in payload
    assert json.loads((out_dir / "output.schema.json").read_text("utf-8")) \
        == ir.WORKER_OUTPUT_SCHEMA
    assert (out_dir / "manifest.json").is_file()


def test_prepare_with_no_clusterable_docs_writes_empty_manifest(tmp_path):
    (tmp_path / "openxFactory").mkdir()
    manifest = rd.prepare_readiness_bundle(tmp_path, tmp_path / "bundle",
                                           run_id="run-1")
    assert manifest["cluster_count"] == 0
    assert manifest["cluster_ids"] == []


# --- merge phase: happy path ----------------------------------------------

def test_merge_happy_path_persists_scored_index_and_returns_findings(tmp_path):
    agg = make_agg_root(tmp_path)
    findings_path = tmp_path / "findings.json"
    findings_path.write_text(
        json.dumps(cluster_findings(agg)), encoding="utf-8")

    meta = rd.merge_readiness_findings(
        agg, as_of=AS_OF, run_id="run-1", findings_path=findings_path,
        validator=fake_validator(tmp_path, accept=True),
        git=FakeGit(heads={"openxFactory": REV}))

    assert meta.ok
    assert meta.skipped_reason is None
    assert meta.total_clusters == 2
    assert meta.scored_clusters == 2
    assert meta.validated is True
    assert meta.source_revision == REV
    index_path = agg / meta.index_path
    assert index_path.is_file()
    assert meta.index_md_path is None or (agg / meta.index_md_path).is_file()
    assert meta.evidence_path is not None
    assert (agg / meta.evidence_path).is_file()
    # both clusters scored all-9s -> both flagged -> two findings (plus no
    # extension-fit/spread findings from this fixture).
    assert len(meta.findings) == 2
    assert all(f.family == "ideation-readiness" for f in meta.findings)
    assert all(f.resolution == "contested" for f in meta.findings)
    assert all(f.severity == "warning" for f in meta.findings)


def test_merge_a_worker_error_for_one_cluster_falls_back_to_unscored(tmp_path):
    agg = make_agg_root(tmp_path)
    raw = cluster_findings(agg)
    raw["cl-beta"] = {"error": "simulated worker failure"}
    findings_path = tmp_path / "findings.json"
    findings_path.write_text(json.dumps(raw), encoding="utf-8")

    meta = rd.merge_readiness_findings(
        agg, as_of=AS_OF, run_id="run-1", findings_path=findings_path,
        validator=fake_validator(tmp_path, accept=True),
        git=FakeGit(heads={"openxFactory": REV}))

    assert meta.ok
    assert meta.scored_clusters == 1
    assert meta.skipped_clusters == [("cl-beta",
                                      "worker failed: simulated worker "
                                      "failure")]


# --- merge phase: skip-not-resolved (change 5.1's last case) -----------------

def _seed_existing_scored_index(agg: Path) -> None:
    """Persist a scored index directly (bypassing the lane) so a later SKIPPED
    run has a prior state to preserve."""
    findings_path = agg / "seed-findings.json"
    findings_path.write_text(
        json.dumps(cluster_findings(agg)), encoding="utf-8")
    meta = rd.merge_readiness_findings(
        agg, as_of=AS_OF, run_id="seed-run", findings_path=findings_path,
        validator=fake_validator(agg, accept=True),
        git=FakeGit(heads={"openxFactory": REV}))
    assert meta.ok and meta.findings  # sanity: the seed actually has findings


def test_skip_with_no_findings_path_preserves_prior_findings(tmp_path):
    agg = make_agg_root(tmp_path)
    _seed_existing_scored_index(agg)

    meta = rd.merge_readiness_findings(
        agg, as_of=AS_OF, run_id="run-2", findings_path=None,
        git=FakeGit(heads={"openxFactory": REV}))

    assert not meta.ok
    assert meta.skipped_reason == rd.WORKER_UNAVAILABLE
    # absent findings from a skipped lane are NOT treated as resolved: the
    # prior run's findings are still reported.
    assert len(meta.findings) == 2
    assert meta.index_path is not None
    index_text_before = (tmp_path / meta.index_path).read_text("utf-8")
    assert "cl-alpha" in index_text_before  # the prior index is untouched


def test_skip_with_explicit_unavailable_reason_preserves_prior_findings(
        tmp_path):
    agg = make_agg_root(tmp_path)
    _seed_existing_scored_index(agg)

    meta = rd.merge_readiness_findings(
        agg, as_of=AS_OF, run_id="run-2",
        unavailable_reason="child_timeout",
        git=FakeGit(heads={"openxFactory": REV}))

    assert not meta.ok
    assert meta.skipped_reason == "child_timeout"
    assert len(meta.findings) == 2


def test_rejected_index_is_never_persisted_and_prior_findings_survive(
        tmp_path):
    agg = make_agg_root(tmp_path)
    _seed_existing_scored_index(agg)
    prior_bytes = (agg / "openxFactory/ideation/cross-reference.yaml") \
        .read_bytes()

    findings_path = tmp_path / "findings-2.json"
    findings_path.write_text(
        json.dumps(cluster_findings(agg)), encoding="utf-8")
    meta = rd.merge_readiness_findings(
        agg, as_of=AS_OF, run_id="run-2", findings_path=findings_path,
        validator=fake_validator(tmp_path, accept=False),  # reject
        git=FakeGit(heads={"openxFactory": REV}))

    assert not meta.ok
    assert meta.validated is False
    assert "rejected" in meta.skipped_reason
    # the prior index is byte-unchanged -- a rejected run never persists.
    assert (agg / "openxFactory/ideation/cross-reference.yaml") \
        .read_bytes() == prior_bytes
    assert len(meta.findings) == 2  # still reads back the prior findings


def test_missing_openxfactory_checkout_is_skipped(tmp_path):
    meta = rd.merge_readiness_findings(
        tmp_path, as_of=AS_OF, run_id="run-1", findings_path=None)
    assert not meta.ok
    assert meta.skipped_reason == "openxFactory checkout not found"
    assert meta.findings == []


def test_missing_git_head_is_skipped(tmp_path):
    agg = make_agg_root(tmp_path)
    findings_path = tmp_path / "findings.json"
    findings_path.write_text(
        json.dumps(cluster_findings(agg)), encoding="utf-8")
    meta = rd.merge_readiness_findings(
        agg, as_of=AS_OF, run_id="run-1", findings_path=findings_path,
        git=FakeGit(heads={}))  # no head recorded for openxFactory
    assert not meta.ok
    assert "source_revision" in meta.skipped_reason


# --- CLI smoke ---------------------------------------------------------

def test_main_prepare_then_merge_round_trip(tmp_path, capsys):
    agg = make_agg_root(tmp_path)
    out_dir = tmp_path / "bundle"
    rc = rd.main(["--repo-root", str(agg), "--phase", "prepare",
                 "--out-dir", str(out_dir), "--as-of", AS_OF.isoformat(),
                 "--run-id", "run-1"])
    assert rc == 0
    assert "2 cluster(s) bundled" in capsys.readouterr().out

    findings_path = tmp_path / "findings.json"
    findings_path.write_text(
        json.dumps(cluster_findings(agg)), encoding="utf-8")
    validator = fake_validator(tmp_path, accept=True)
    report_path = tmp_path / "report.md"
    report_path.write_text(
        "# Doc-Health Report\n\n## Findings By Family\n\nNo findings.\n\n"
        "## Ranked Plan\n\nNo findings — nothing to stage.\n",
        encoding="utf-8")
    # main() has no --validator/--git seams (production always uses the real
    # ones); exercise the merge function directly for the injectable path and
    # only prove main()'s CLI plumbing (arg parsing + report rewiring + exit
    # code) via the module-level merge function it calls under the hood.
    import doc_health.readiness_dispatch as rd_mod
    original = rd_mod.merge_readiness_findings

    def _patched(*args, **kwargs):
        kwargs["validator"] = validator
        kwargs["git"] = FakeGit(heads={"openxFactory": REV})
        return original(*args, **kwargs)

    rd_mod.merge_readiness_findings = _patched
    try:
        rc = rd.main(["--repo-root", str(agg), "--phase", "merge",
                     "--as-of", AS_OF.isoformat(), "--run-id", "run-2",
                     "--findings-in", str(findings_path),
                     "--report-in", str(report_path)])
    finally:
        rd_mod.merge_readiness_findings = original
    assert rc == 0
    out = capsys.readouterr().out
    assert "ideation-readiness lane: OK" in out
    updated = report_path.read_text("utf-8")
    assert "## Ideation Readiness" in updated
    assert "severity=warning family=ideation-readiness" in updated


def test_main_never_raises_and_reports_skip_on_unhandled_error(tmp_path,
                                                                capsys):
    rc = rd.main(["--repo-root", str(tmp_path), "--phase", "merge",
                 "--as-of", AS_OF.isoformat(), "--run-id", "run-1"])
    assert rc == 0
    assert "SKIPPED" in capsys.readouterr().out


# --- real validator (skipped if unreachable) --------------------------------

# harden-ideation-readiness-check. Spelled identically in
# `test_ideation_readiness.py` (which carries the full rationale) and in
# `test_derive_possibles.py`. The duplication is deliberate and tracked: the
# packet's Q3 / tasks § 5.1 — whether the three collapse into one shared
# fixture — is OPEN and is not decided by this realization. Edit one, edit all
# three.
ROOT_FALLBACK_MARKER = "[openxfactory-root] fallback"
INDEX_REL = Path("ideation") / "cross-reference.yaml"
SIBLING_INDEX_REL = Path("openxFactory") / INDEX_REL


def _openxfactory_root(under_test=None, *, fallback=None, announce=print):
    """Resolve the openxFactory checkout this run is a proof ABOUT: the
    REPOSITORY UNDER TEST first, then an explicit `fallback`, then
    `OPENXFACTORY_ROOT`, then the ancestor walk to a sibling `openxFactory/` —
    every rung past the first announcing which checkout it resolved and why.
    None when nothing is reachable."""
    base = Path(under_test or REPO_ROOT).resolve()
    if (base / INDEX_REL).is_file():
        return base

    why = f"the repository under test ({base}) carries no {INDEX_REL.as_posix()}"
    if fallback is not None and (Path(fallback) / INDEX_REL).is_file():
        resolved = Path(fallback).resolve()
        announce(f"{ROOT_FALLBACK_MARKER}: resolved {resolved} from the "
                 f"explicit argument because {why}")
        return resolved

    declared = os.environ.get("OPENXFACTORY_ROOT")
    if declared and (Path(declared) / INDEX_REL).is_file():
        resolved = Path(declared).resolve()
        announce(f"{ROOT_FALLBACK_MARKER}: resolved {resolved} from "
                 f"OPENXFACTORY_ROOT because {why}")
        return resolved

    for d in [base, *base.parents]:
        if (d / SIBLING_INDEX_REL).is_file():
            resolved = d / "openxFactory"
            announce(f"{ROOT_FALLBACK_MARKER}: resolved {resolved} by walking "
                     f"up from the repository under test because {why}")
            return resolved
    return None


def _openxfactory_root_or_skip(under_test=None):
    """The resolved checkout, or a skip whose reason names what was searched."""
    root = _openxfactory_root(under_test)
    if root is None:
        base = Path(under_test or REPO_ROOT).resolve()
        pytest.skip(f"proof NOT PERFORMED: no openxFactory checkout serves it "
                    f"— the repository under test ({base}) carries no "
                    f"{INDEX_REL.as_posix()}, OPENXFACTORY_ROOT names no "
                    f"checkout that does, and no ancestor of it holds "
                    f"{SIBLING_INDEX_REL.as_posix()}")
    return root


def test_merge_wires_the_real_validator_for_a_genuinely_scored_index(
        tmp_path):
    """Not the T007 15-cluster proof (test_ideation_readiness.py owns that)
    -- only proves THIS module's own plumbing reaches the pinned openxFactory
    validator (no `validator=` seam here) and that a genuinely scored,
    contract-compliant index it assembles (real passages, real revision
    shape) validates clean end to end. Never touches the shared checkout:
    the validator SCRIPT is discovered from the real sibling repo, but the
    index it validates and the `--repo` it resolves citations against are
    both this test's own tmp fixture. Since
    harden-ideation-readiness-check the validator resolves out of the
    REPOSITORY UNDER TEST first rather than out of whichever checkout sits
    above it on the filesystem."""
    real_openx = _openxfactory_root_or_skip()  # noqa: F841 (the gate, not the arg)

    agg = make_agg_root(tmp_path)
    findings_path = tmp_path / "findings.json"
    findings_path.write_text(
        json.dumps(cluster_findings(agg)), encoding="utf-8")

    meta = rd.merge_readiness_findings(
        agg, as_of=AS_OF, run_id="run-1", findings_path=findings_path,
        git=FakeGit(heads={"openxFactory": REV}))

    assert meta.ok, meta.rejection_detail
    assert meta.validated is True
    assert meta.scored_clusters == 2


# --- per-run cluster budget (the 67-cluster corpus outgrew the child cap) ---

def test_prepare_budget_is_unscored_first_and_capped(tmp_path):
    import yaml as yaml_mod
    openx = tmp_path / "openxFactory"
    brainstorm = openx / "ideation" / "brainstorm"
    brainstorm.mkdir(parents=True)
    # 15 clusterable topics (alpha00..alpha14), two docs each
    for i in range(15):
        topic = f"alpha{i:02d}"
        for j in (1, 2):
            (brainstorm / f"{topic}-{j}.md").write_text(
                doc_text(f"{topic}-{j}.md", topics=[topic]), encoding="utf-8")
    # the on-disk index has SCORED the first three alphabetical clusters
    scored = [{"id": f"cl-alpha{i:02d}",
               "readiness": {"tiers": [], "recommendation":
                             {"flagged": False, "disposition": "pending_review",
                              "summary": "s"}}} for i in range(3)]
    (openx / "ideation" / "cross-reference.yaml").write_text(
        yaml_mod.safe_dump({"topic_entries": scored}), encoding="utf-8")

    manifest = rd.prepare_readiness_bundle(tmp_path, tmp_path / "bundle",
                                           run_id="run-1")
    assert manifest["total_clusters"] == 15
    assert manifest["cluster_count"] == rd.MAX_CLUSTERS_PER_RUN
    bundled = manifest["cluster_ids"]
    # every UNSCORED cluster (12 of them) gets a turn before any scored one
    unscored = [f"cl-alpha{i:02d}" for i in range(3, 15)]
    assert sorted(bundled) == sorted(unscored)
    assert not any(c in bundled for c in ("cl-alpha00", "cl-alpha01", "cl-alpha02"))
