"""Structural guards in the doc-health reusable workflow.

The readiness-only mode's guarantee is structural: the dispatch step and
finalize job must carry explicit readiness-only conditions, and the
probe logic must run the real evaluation. These tests parse the workflow
so a refactor cannot silently drop a guard."""

from __future__ import annotations

from pathlib import Path

import yaml

WORKFLOW = (Path(__file__).resolve().parents[2]
            / ".github" / "workflows" / "doc-health-reusable.yml")


def load():
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))


def step(job, name):
    matches = [s for s in job["steps"] if s.get("name") == name]
    assert len(matches) == 1, f"expected exactly one step named {name!r}"
    return matches[0]


def test_readiness_only_input_exists_and_defaults_off():
    wf = load()
    inputs = wf[True]["workflow_call"]["inputs"]  # YAML 1.1 parses `on` as True
    assert inputs["readiness-only"]["type"] == "boolean"
    assert inputs["readiness-only"]["default"] is False


def test_dispatch_step_is_guarded_against_readiness_only():
    prepare = load()["jobs"]["prepare"]
    dispatch = step(prepare, "Dispatch artifact-only analysis child")
    assert "inputs.readiness-only != true" in dispatch["if"]
    assert "steps.readiness.outputs.ready == 'true'" in dispatch["if"]


def test_finalize_job_skips_in_readiness_only():
    finalize = load()["jobs"]["finalize"]
    assert "inputs.readiness-only != true" in finalize["if"]
    assert "always()" in finalize["if"]


def test_readiness_step_probes_when_readiness_only():
    prepare = load()["jobs"]["prepare"]
    readiness = step(prepare, "Evaluate hosted worker readiness")
    assert readiness["env"]["READINESS_ONLY"] == \
        "${{ inputs.readiness-only == true }}"
    script = readiness["run"]
    # readiness-only forces the probe on; the evaluator runs the real
    # fail-closed path (--enabled) whenever the probe is on.
    assert '[ "$READINESS_ONLY" = "true" ] && PROBE="true"' in script
    assert '[ "$PROBE" = "true" ] && ENABLED=(--enabled)' in script
    assert 'WORKER_ENABLED' not in script.split("PROBE=\"$WORKER_ENABLED\"")[1], \
        "probe gates must use PROBE, not WORKER_ENABLED, after initialization"


def test_bundle_steps_skip_in_readiness_only():
    prepare = load()["jobs"]["prepare"]
    bundle = step(prepare, "Build semantic sweep bundle")
    assert bundle["if"] == "inputs.readiness-only != true"


# --- document-cataloger readiness-only guards (mirrors the sweep's own) -----

def test_catalog_bundle_step_skips_in_readiness_only():
    prepare = load()["jobs"]["prepare"]
    bundle = step(prepare, "Build document catalog bundle")
    assert bundle["if"] == "inputs.readiness-only != true"


def test_catalog_dispatch_step_is_guarded_against_readiness_only():
    prepare = load()["jobs"]["prepare"]
    dispatch = step(prepare, "Dispatch artifact-only cataloger child")
    assert "inputs.readiness-only != true" in dispatch["if"]
    assert "steps.catalog-readiness.outputs.ready == 'true'" in dispatch["if"]


# --- catalog-baseline/catalog-scope inputs (task T017/T019) ------------------

def test_catalog_baseline_and_scope_inputs_exist_with_defaults():
    wf = load()
    inputs = wf[True]["workflow_call"]["inputs"]  # YAML 1.1 parses `on` as True
    assert inputs["catalog-baseline"]["type"] == "boolean"
    assert inputs["catalog-baseline"]["default"] is False
    assert inputs["catalog-scope"]["type"] == "string"
    assert inputs["catalog-scope"]["default"] == ""


def test_catalog_baseline_and_scope_inputs_pass_through_to_the_bundle_step():
    prepare = load()["jobs"]["prepare"]
    bundle = step(prepare, "Build document catalog bundle")
    assert bundle["env"]["CATALOG_BASELINE_INPUT"] == \
        "${{ inputs.catalog-baseline }}"
    assert bundle["env"]["CATALOG_SCOPE_INPUT"] == \
        "${{ inputs.catalog-scope }}"
    assert "--catalog-baseline" in bundle["run"]
    assert "--catalog-scope" in bundle["run"]


# --- ideation-readiness lane guards (add-ideation-cross-reference-readiness
#     4.1) — the lane lives entirely in `finalize`, so readiness-only mode
#     (which produces no `finalize` run at all, per
#     test_finalize_job_skips_in_readiness_only above) already covers it
#     without any per-step readiness-only condition of its own.

def test_readiness_only_never_reaches_finalize_so_the_lane_never_dispatches():
    finalize = load()["jobs"]["finalize"]
    assert "inputs.readiness-only != true" in finalize["if"]
    names = {s.get("name") for s in finalize["steps"]}
    assert "Evaluate readiness-scorer worker readiness" in names
    assert "Dispatch artifact-only readiness child" in names


def test_readiness_bundle_and_dispatch_steps_are_guarded_on_local_readiness():
    finalize = load()["jobs"]["finalize"]
    bundle = step(finalize, "Build readiness bundle (per-cluster untrusted "
                           "payloads)")
    dispatch = step(finalize, "Dispatch artifact-only readiness child")
    assert bundle["if"] == "steps.xref-readiness.outputs.ready == 'true'"
    assert "steps.xref-readiness.outputs.ready == 'true'" in dispatch["if"]
    assert "steps.xref-build.outputs.cluster_count != '0'" in dispatch["if"]


def test_readiness_upload_artifact_uses_a_fixed_name_like_its_siblings():
    # Fixed name (mirrors semantic-sweep-bundle / document-catalog-bundle):
    # the child's `run-id: source_run_id` already disambiguates which run's
    # artifact to fetch, so the name itself does not need a correlation
    # suffix (unlike the FINDINGS artifact the child later uploads back,
    # which IS correlation-suffixed since a specific run's collect step
    # matches against its own correlation id).
    finalize = load()["jobs"]["finalize"]
    upload = next(s for s in finalize["steps"]
                 if s.get("uses") == "actions/upload-artifact@v4"
                 and s.get("with", {}).get("name") ==
                 "ideation-readiness-bundle")
    assert upload["with"]["path"] == "xref-bundle"

