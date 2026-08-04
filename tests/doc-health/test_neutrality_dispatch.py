"""Neutrality-drift dispatch tests (add-neutrality-drift-lane task 1.5):
scout dispatch via a fake-claude script (valid + malformed canned output),
register-seed drafting format-validated against the register's own
parsing, disposition suppression keyed (repo, path, content digest), the
graceful worker-unavailable note, and the lane's authority boundary (its
write surface is the lane tree + the report, nothing else).
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
from datetime import date
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

from conftest import FIXTURES  # noqa: F401  (sys.path side effect)

from doc_health import neutrality, report
from doc_health import neutrality_dispatch as nd
from doc_health.families import fam_register_lifecycle_consistency

WORKSPACE = FIXTURES / "neutrality"
AS_OF = date(2026, 7, 9)
MODEL = "test-model"

FAKE_WORKER = FIXTURES / "fake-claude-neutrality.sh"
FAKE_WORKER_INVALID = FIXTURES / "fake-claude-neutrality-invalid.sh"

PLANTED = "schemas/generic-envelope.schema.yaml"
NEAR_DUP = "contracts/copy-of-neutral.yaml"
UNINVENTORIED = "scripts/tools/check-things.py"


def workspace(tmp_path) -> tuple[Path, dict]:
    """A WRITABLE copy of the fixture workspace (tests never write into
    fixtures): (openx_root, scope)."""
    root = tmp_path / "workspace"
    shutil.copytree(WORKSPACE, root)
    scope = {p.name: p for p in sorted((root / "xFactories").iterdir())}
    return root / "openxFactory", scope


def fake_invoke(script, **env_overrides):
    def _invoke(prompt, model):
        env = dict(os.environ)
        env.update({k: str(v) for k, v in env_overrides.items()})
        return subprocess.run(["sh", str(script)], capture_output=True,
                              text=True, env=env, check=True).stdout
    return _invoke


def tree_digests(root: Path) -> dict:
    return {p.relative_to(root).as_posix():
            hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob("*") if p.is_file()}


# --- prompt contract / envelope -------------------------------------------------


def test_prompt_contract_loads_with_version():
    version, text = nd.load_prompt_contract()
    assert version == 1
    assert "would another domain factory need this file essentially" \
        in text.lower()
    assert "never judge from location alone" in text.lower()
    assert "frozen records are excluded subjects" in text.lower()


def test_envelope_is_neutral_and_deterministic(tmp_path):
    subjects = [neutrality.Candidate("MedxFactory", PLANTED, "a" * 64, ())]
    one = nd.envelope(AS_OF, "run1", MODEL, 1, subjects)
    two = nd.envelope(AS_OF, "run1", MODEL, 1, subjects)
    assert one == two
    job = one["job"]
    assert job["id"].startswith("NEUTJOB-")
    assert job["stop_conditions"]["max_repo_writes"] == 0
    assert job["worker_selector"]["profile"] == "neutrality-scout"
    assert job["traceability"]["lane"] == "neutrality-drift"


def test_next_dtn_id_reads_rows_and_sections():
    text = (WORKSPACE / "openxFactory" / "docs" /
            "domain-neutralization-candidate-register.md"
            ).read_text(encoding="utf-8")
    assert nd.next_dtn_id(text) == 3
    assert nd.next_dtn_id("") == 1


# --- merge: valid scout output drafts a format-valid seed --------------------------


def merge(openx, scope, **kwargs):
    defaults = dict(openx_root=openx, git=SimpleNamespace(
        head_sha=lambda _p: None))
    defaults.update(kwargs)
    return nd.merge_neutrality_findings(scope, AS_OF, MODEL, **defaults)


def test_valid_scout_output_drafts_seed_and_advances_state(tmp_path):
    openx, scope = workspace(tmp_path)
    meta = merge(openx, scope, invoke=fake_invoke(FAKE_WORKER))
    assert meta.skipped_reason is None
    assert meta.candidates == {"MedxFactory": 3, "OpsxFactory": 0}
    assert meta.dispatched == 3 and meta.carried_over == 0
    assert [s[0] for s in meta.seeds] == ["DTN-003"]
    dtn, repo, path, decision, seed_ref = meta.seeds[0]
    assert (repo, path, decision) == ("MedxFactory", PLANTED, "promote")
    seed_file = openx / seed_ref
    assert seed_file.is_file()
    body = seed_file.read_text(encoding="utf-8")
    assert "Status: record" in body
    assert "| DTN-003 |" in body and "### DTN-003:" in body
    # every dispatched subject (returned OR omitted) is now judged
    state = neutrality.load_state(openx)
    judged = state["MedxFactory"]["judged"]
    assert set(judged) == {PLANTED, NEAR_DUP, UNINVENTORIED}
    # ranked-plan item: WARNING + contested, never regression-eligible
    assert len(meta.findings) == 1
    finding = meta.findings[0]
    assert finding.severity == "warning"
    assert finding.family == "neutrality-drift"
    assert finding.resolution == "contested"
    assert finding.disposer == "Brett (DTN register approval)"
    assert report.PLAN_RE.match(report.plan_line(finding))


def test_second_run_with_nothing_new_is_a_quiet_skip(tmp_path):
    openx, scope = workspace(tmp_path)
    merge(openx, scope, invoke=fake_invoke(FAKE_WORKER))
    again = merge(openx, scope, invoke=fake_invoke(FAKE_WORKER))
    assert again.skipped_reason == ("stage 2 not needed: no new or changed "
                                    "stage-1 survivors this run")
    assert again.seeds == []


def test_drafted_seed_parses_under_the_registers_own_family(tmp_path):
    openx, scope = workspace(tmp_path)
    meta = merge(openx, scope, invoke=fake_invoke(FAKE_WORKER))
    seed_file = openx / meta.seeds[0][4]
    body = seed_file.read_text(encoding="utf-8")
    row = next(line for line in body.splitlines()
               if line.startswith("| DTN-003 |"))
    section = body.split("## Register detail section\n\n", 1)[1]
    assert nd.validate_seed(row, section, "DTN-003") == []
    # append the drafted row to the register and run the REAL family
    register = openx / "docs" / "domain-neutralization-candidate-register.md"
    register.write_text(
        register.read_text(encoding="utf-8") + row + "\n",
        encoding="utf-8")
    ctx = SimpleNamespace(repo_paths={"openxFactory": openx})
    assert fam_register_lifecycle_consistency(ctx) == []


def test_validate_seed_reports_defects():
    bad_row = "| DTN-004 | topic | `promote` | P2 | `pending` | x |"
    defects = nd.validate_seed(bad_row, "no heading", "DTN-004")
    assert any("register alias" in d for d in defects)
    assert any("### DTN-004:" in d for d in defects)
    assert any("Evidence:" in d for d in defects)


def test_findings_file_path_matches_inline_invoke(tmp_path):
    openx, scope = workspace(tmp_path)
    raw = subprocess.run(["sh", str(FAKE_WORKER)], capture_output=True,
                         text=True, check=True).stdout
    artifact = tmp_path / "NEUTJOB-abc.json"
    artifact.write_text(raw, encoding="utf-8")
    meta = merge(openx, scope, findings_path=artifact)
    assert meta.skipped_reason is None
    assert [s[0] for s in meta.seeds] == ["DTN-003"]


# --- malformed output: whole-artifact rejection, nothing applied ---------------------


def test_malformed_scout_output_rejects_whole_artifact(tmp_path):
    openx, scope = workspace(tmp_path)
    before = tree_digests(openx.parent)
    meta = merge(openx, scope, invoke=fake_invoke(FAKE_WORKER_INVALID))
    assert meta.rejected == 1
    assert meta.skipped_reason.startswith("scout output rejected")
    assert "suggested_decision" in meta.rejects[0]
    assert meta.seeds == [] and meta.findings == []
    # nothing applied: no seed files, no state advance, nothing anywhere
    assert tree_digests(openx.parent) == before


def test_invented_subject_rejects_whole_artifact(tmp_path):
    openx, scope = workspace(tmp_path)
    meta = merge(openx, scope,
                 invoke=fake_invoke(FAKE_WORKER, REPO="MedxFactory",
                                    DOC_PATH="schemas/invented.yaml"))
    assert meta.rejected == 1
    assert "not a dispatched subject" in meta.rejects[0]


def test_empty_candidates_array_is_a_valid_quiet_answer(tmp_path):
    openx, scope = workspace(tmp_path)
    meta = merge(openx, scope,
                 invoke=lambda prompt, model: '{"candidates": []}')
    assert meta.skipped_reason is None and meta.rejected == 0
    assert meta.seeds == []
    # the whole batch was judged domain-appropriate: digests recorded
    judged = neutrality.load_state(openx)["MedxFactory"]["judged"]
    assert len(judged) == 3


# --- graceful no-worker path ---------------------------------------------------------


def test_worker_unavailable_is_a_note_with_stage1_counts(tmp_path):
    openx, scope = workspace(tmp_path)
    before = tree_digests(openx.parent)
    meta = merge(openx, scope, unavailable_reason="worker_unavailable")
    assert meta.skipped_reason == "worker_unavailable"
    assert meta.candidates["MedxFactory"] == 3  # stage 1 still reported
    assert meta.selected == 3 and meta.dispatched == 3
    assert tree_digests(openx.parent) == before  # nothing advances


def test_empty_scope_records_a_skip_note():
    meta = nd.merge_neutrality_findings({}, AS_OF, MODEL,
                                        openx_root=WORKSPACE / "openxFactory")
    assert "no domain factories in scope" in meta.skipped_reason


# --- disposition suppression (extends the existing dispositions vocabulary) ----------


def write_dispositions(tmp_path, entries) -> Path:
    path = tmp_path / "dispositions.yaml"
    path.write_text(yaml.safe_dump(entries), encoding="utf-8")
    return path


def test_rejected_candidate_stays_rejected_while_unchanged(tmp_path):
    openx, scope = workspace(tmp_path)
    digest = hashlib.sha256(
        (scope["MedxFactory"] / PLANTED).read_bytes()).hexdigest()
    dispositions = write_dispositions(tmp_path, [
        {"family": "neutrality-drift", "repo": "MedxFactory",
         "path": PLANTED, "content_sha256": digest,
         "cite": "Brett 2026-08-04: not-now"}])
    meta = merge(openx, scope, dispositions_path=dispositions,
                 invoke=fake_invoke(FAKE_WORKER))
    assert meta.suppressed == 1
    assert meta.dispatched == 2
    # the scout's canned answer cites the suppressed subject -> whole
    # artifact rejected (it is no longer a dispatched subject)
    assert meta.rejected == 1


def test_changed_digest_refiles_the_candidate(tmp_path):
    openx, scope = workspace(tmp_path)
    planted = scope["MedxFactory"] / PLANTED
    dispositions = write_dispositions(tmp_path, [
        {"family": "neutrality-drift", "repo": "MedxFactory",
         "path": PLANTED,
         "content_sha256": hashlib.sha256(
             planted.read_bytes()).hexdigest(),
         "cite": "Brett 2026-08-04: not-now"}])
    planted.write_text(
        planted.read_text(encoding="utf-8") + "# revised\n",
        encoding="utf-8")
    meta = merge(openx, scope, dispositions_path=dispositions,
                 invoke=fake_invoke(FAKE_WORKER))
    assert meta.suppressed == 0
    assert meta.dispatched == 3
    assert [s[0] for s in meta.seeds] == ["DTN-003"]  # re-filed


# --- manual baseline sweep -------------------------------------------------------------


def test_drained_manual_sweep_records_the_baseline_marker(tmp_path):
    openx, scope = workspace(tmp_path)
    meta = merge(openx, scope, baseline_repo="MedxFactory",
                 invoke=lambda prompt, model: '{"candidates": []}')
    assert meta.baseline_recorded == "MedxFactory"
    marker = neutrality.load_baseline(openx, "MedxFactory")
    assert marker is not None and marker["status"] == "record"
    assert any("full-sweep baseline" in d for d in meta.deviations)


# --- authority boundary (design D4): write surface is the lane tree only ---------------


def test_lane_write_surface_is_only_its_own_tree(tmp_path):
    openx, scope = workspace(tmp_path)
    root = openx.parent
    before = tree_digests(root)
    merge(openx, scope, invoke=fake_invoke(FAKE_WORKER))
    after = tree_digests(root)
    touched = ({p for p in after if after[p] != before.get(p)}
               | (set(before) - set(after)))
    assert touched  # the run did persist something
    assert all(p.startswith("openxFactory/health/neutrality-drift/")
               for p in sorted(touched)), sorted(touched)


def test_seed_evidence_path_is_boundary_checked(tmp_path):
    with pytest.raises(ValueError, match="invalid neutrality run id"):
        nd._seed_path(tmp_path, "2026-07-09", "DTN-003", "../escape")
    with pytest.raises(ValueError, match="invalid drafted DTN id"):
        nd._seed_path(tmp_path, "2026-07-09", "DTN-3x", "run")


def test_persisted_seed_is_immutable(tmp_path):
    from doc_health.catalog import CatalogError
    nd.persist_seed(tmp_path, AS_OF, "DTN-003", "run1", "content\n")
    nd.persist_seed(tmp_path, AS_OF, "DTN-003", "run1", "content\n")  # no-op
    with pytest.raises(CatalogError):
        nd.persist_seed(tmp_path, AS_OF, "DTN-003", "run1", "different\n")


# --- prepare-phase bundle ---------------------------------------------------------------


def test_prepare_bundle_writes_contained_batch_input(tmp_path):
    openx, scope = workspace(tmp_path)
    out = tmp_path / "bundle"
    meta = nd.prepare_neutrality_bundle(
        scope, AS_OF, out, MODEL, openx_root=openx,
        allowed_output_root=tmp_path)
    assert meta["subject_count"] == 3
    manifest = json.loads((out / "manifest.json").read_text())
    assert manifest["job_id"].startswith("NEUTJOB-")
    assert (out / "prompt.md").is_file()
    schema = json.loads((out / "output.schema.json").read_text())
    assert schema == nd.WORKER_OUTPUT_SCHEMA
    payload = (out / "subjects" /
               f"{manifest['job_id']}.input.txt").read_text()
    assert PLANTED in payload and "Untrusted batch payload" in payload
    with pytest.raises(ValueError, match="escapes"):
        nd.prepare_neutrality_bundle(
            scope, AS_OF, tmp_path.parent / "outside", MODEL,
            openx_root=openx, allowed_output_root=tmp_path)


# --- report integration -----------------------------------------------------------------


def test_report_section_and_ranked_plan_folding(tmp_path):
    openx, scope = workspace(tmp_path)
    meta = merge(openx, scope, invoke=fake_invoke(FAKE_WORKER))
    rendered = report.render(AS_OF, [], [], [], [], 0, [], [])
    text = report.insert_neutrality_section(rendered, meta)
    assert "## Neutrality Drift" in text
    assert text.index("## Neutrality Drift") < \
        text.index("## Findings By Family")
    assert "DTN-003 `promote` — MedxFactory:" + PLANTED[:0] in text
    assert "family=neutrality-drift" in text  # ranked-plan line folded
    assert 'class="contested"' in text
    assert "No findings — nothing to stage." not in text


def test_skipped_lane_section_carries_the_note(tmp_path):
    openx, scope = workspace(tmp_path)
    meta = merge(openx, scope, unavailable_reason="worker_unavailable")
    lines = report.build_neutrality_section(meta)
    assert "Skipped: worker_unavailable" in lines
    assert any("stage 1: 3 candidate(s)" in line for line in lines)


# --- workflow wiring (task 1.4) ------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "doc-health-reusable.yml"


def _workflow():
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))


def test_workflow_inputs_exist_with_defaults():
    inputs = _workflow()[True]["workflow_call"]["inputs"]  # YAML 1.1 `on`
    assert inputs["neutrality-drift"]["type"] == "boolean"
    assert inputs["neutrality-drift"]["default"] is True
    assert inputs["neutrality-baseline"]["type"] == "string"
    assert inputs["neutrality-baseline"]["default"] == ""


def test_workflow_wires_lane_through_env_not_interpolation():
    finalize = _workflow()["jobs"]["finalize"]
    run = next(s for s in finalize["steps"]
               if s.get("name") == "Run doc-health suite")
    assert run["env"]["NEUTRALITY_ENABLED"] == \
        "${{ inputs.neutrality-drift }}"
    assert run["env"]["NEUTRALITY_BASELINE_INPUT"] == \
        "${{ inputs.neutrality-baseline }}"
    assert "${{ inputs.neutrality-baseline }}" not in run["run"]
    assert '--neutrality-unavailable-reason "$NEUTRALITY_REASON"' \
        in run["run"]
    assert 'NEUTRALITY+=(--neutrality-baseline "$NEUTRALITY_BASELINE_INPUT")' \
        in run["run"]
    assert '"${NEUTRALITY[@]}"' in run["run"]


def test_recorded_codexfactory_baseline_marker_is_valid():
    marker = neutrality.load_baseline(ROOT, "codexFactory")
    assert marker is not None
    assert marker["commit"] == "a461cabd01446f96c23c4ecffa0aa9403ded6fd4"
    assert marker["as_of"] == "2026-08-03"
    assert "adopt-neutral-tooling-home" in marker["evidence"]
