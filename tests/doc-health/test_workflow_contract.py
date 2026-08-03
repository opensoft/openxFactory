from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "doc-health-reusable.yml"


def workflow():
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))


def step(job: dict, name: str) -> dict:
    return next(item for item in job["steps"] if item.get("name") == name)


def test_untrusted_workflow_inputs_are_not_interpolated_into_bash():
    value = workflow()
    prepare = step(value["jobs"]["prepare"], "Build semantic sweep bundle")
    finalize = step(value["jobs"]["finalize"], "Run doc-health suite")
    for script in (prepare["run"], finalize["run"]):
        assert "${{ inputs.skip-families }}" not in script
        assert "${{ inputs.fail-on }}" not in script
    assert prepare["env"]["SKIP_FAMILIES_INPUT"] == \
        "${{ inputs.skip-families }}"
    assert finalize["env"]["FAIL_ON_INPUT"] == "${{ inputs.fail-on }}"
    assert 'SKIPS+=(--skip-family "$family")' in finalize["run"]
    assert 'GATE=(--fail-on "$FAIL_ON_INPUT")' in finalize["run"]


def test_external_worker_failures_cannot_skip_deterministic_finalize():
    value = workflow()
    finalizer = value["jobs"]["finalize"]
    # The invariant is that no RUNTIME outcome (worker failure, dispatch
    # error, cancelled child) can skip finalize — hence always(). The
    # operator-chosen readiness-only mode is the single static exception:
    # it is decided at dispatch time and produces no run to finalize.
    assert finalizer["if"].startswith("always()")
    assert set(finalizer["if"].split(" && ")) == \
        {"always()", "inputs.readiness-only != true"}
    collect = step(finalizer, "Collect bounded worker result")
    run = step(finalizer, "Run doc-health suite")
    assert collect["continue-on-error"] is True
    assert collect["timeout-minutes"] == 45
    assert run["if"] == "always()"
    assert "worker_result_query_failed" in collect["run"]
    assert "RUN_DEADLINE=$((SECONDS + 1800))" in collect["run"]


def test_finalizer_checkout_persists_content_app_token_for_delivery():
    finalizer = workflow()["jobs"]["finalize"]
    steps = finalizer["steps"]
    mint_index = next(
        index for index, item in enumerate(steps)
        if item.get("name") == "Mint xFactory app token"
    )
    checkout_index, checkout = next(
        (index, item) for index, item in enumerate(steps)
        if item.get("uses") == "actions/checkout@v4"
    )
    assert mint_index < checkout_index
    assert checkout["with"]["token"] == \
        "${{ steps.app-token.outputs.token || github.token }}"


def test_approval_dispatch_runs_on_job_token_not_app_token():
    # The content-App token can push through branch confinement but has no
    # `actions` permission — dispatching merge-master-approval with it 403s
    # (live-verified 2026-07-28). The dispatch must override GH_TOKEN with
    # the job token, which the finalize permissions block grants actions: write.
    deliver = step(workflow()["jobs"]["finalize"],
                   "Commit report (deliver via rolling PR — ruleset 18962101)")
    assert deliver["env"]["DISPATCH_TOKEN"] == "${{ github.token }}"
    assert 'GH_TOKEN="$DISPATCH_TOKEN" gh workflow run merge-master-approval.yml' \
        in deliver["run"]
    assert workflow()["jobs"]["finalize"]["permissions"]["actions"] == "write"


def test_dispatch_bundle_is_built_from_deterministic_inventory_first():
    value = workflow()
    prepare = step(value["jobs"]["prepare"], "Build semantic sweep bundle")
    final = step(value["jobs"]["finalize"], "Run doc-health suite")
    assert "--semantic-prepare sweep-bundle" in prepare["run"]
    assert "--inventory-in prepared/inventory.json" in final["run"]
    assert "deterministic_inventory_unavailable" in final["run"]


# --- document-cataloger dispatch/watchdog (001-document-catalog-nightly) ----

def test_catalog_bundle_build_precedes_cataloger_dispatch_in_prepare():
    prepare = workflow()["jobs"]["prepare"]
    names = [s.get("name") for s in prepare["steps"]]
    assert names.index("Build document catalog bundle") < \
        names.index("Dispatch artifact-only cataloger child")
    catalog_bundle = step(prepare, "Build document catalog bundle")
    assert "--catalog-prepare catalog-bundle" in catalog_bundle["run"]


def test_catalog_collector_never_blocks_deterministic_finalize():
    value = workflow()
    finalizer = value["jobs"]["finalize"]
    collect = step(finalizer, "Collect bounded cataloger result")
    run = step(finalizer, "Run doc-health suite")
    assert collect["continue-on-error"] is True
    assert collect["timeout-minutes"] == 45
    assert run["if"] == "always()"
    assert "worker_result_query_failed" in collect["run"]
    assert "QUEUE_DEADLINE=$((SECONDS + 600))" in collect["run"]
    assert "RUN_DEADLINE=$((SECONDS + 1800))" in collect["run"]
    assert '"$REASON" = "child_timeout"' in collect["run"]
    assert '"$REASON" = "child_queue_timeout"' in collect["run"]
    assert "gh run cancel" in collect["run"]
    assert "catalog-unavailable-reason.txt" in collect["run"]
    assert "catalog-unavailable-reason.txt" in run["run"]
    assert "--catalog-findings-in" in run["run"]
    assert "--catalog-unavailable-reason" in run["run"]


def test_catalog_readiness_reuses_the_evaluator_with_a_distinct_profile():
    prepare = workflow()["jobs"]["prepare"]
    readiness = step(prepare, "Evaluate cataloger worker readiness")
    assert "--required-label document-cataloger" in readiness["run"]
    assert "--required-profile document-cataloger" in readiness["run"]
    assert "--required-policy-version artifact-worker-v1" in readiness["run"]
    assert "check-worker-readiness.py" in readiness["run"]


# --- ideation-readiness lane (add-ideation-cross-reference-readiness 4.1) ----
#
# Unlike the semantic sweep and cataloger lanes above (whose readiness-check/
# dispatch live in `prepare`, before the deterministic pass), this lane's own
# ADDED requirement binds it to run AFTER the deterministic pass, against the
# SAME inventory snapshot -- so every one of its steps lives in `finalize`,
# after "Run doc-health suite".

def test_readiness_lane_steps_live_in_finalize_not_prepare():
    value = workflow()
    prepare_names = {s.get("name") for s in value["jobs"]["prepare"]["steps"]}
    finalize_names = {s.get("name") for s in value["jobs"]["finalize"]["steps"]}
    assert "Evaluate readiness-scorer worker readiness" not in prepare_names
    assert "Evaluate readiness-scorer worker readiness" in finalize_names
    assert "Dispatch artifact-only readiness child" in finalize_names


def test_readiness_check_runs_after_run_doc_health_suite():
    finalize = workflow()["jobs"]["finalize"]
    names = [s.get("name") for s in finalize["steps"]]
    assert names.index("Run doc-health suite") < \
        names.index("Evaluate readiness-scorer worker readiness") < \
        names.index("Build readiness bundle (per-cluster untrusted payloads)") < \
        names.index("Dispatch artifact-only readiness child") < \
        names.index("Collect bounded readiness result") < \
        names.index("Ideation readiness lane (merge, persist, report link)")


def test_readiness_check_reuses_the_evaluator_with_a_distinct_profile():
    finalize = workflow()["jobs"]["finalize"]
    readiness = step(finalize, "Evaluate readiness-scorer worker readiness")
    assert "--required-label ideation-readiness" in readiness["run"]
    assert "--required-profile readiness-scorer" in readiness["run"]
    assert "--required-policy-version artifact-worker-v1" in readiness["run"]
    assert "check-worker-readiness.py" in readiness["run"]
    # sourced from the job output already computed once in `prepare`, not a
    # second read of vars.OMNIGENT_WORKER.
    assert readiness["env"]["WORKER_ENABLED"] == \
        "${{ needs.prepare.outputs.omnigent }}"


def test_readiness_build_bundle_consumes_this_runs_run_date():
    finalize = workflow()["jobs"]["finalize"]
    build = step(finalize, "Build readiness bundle (per-cluster untrusted "
                          "payloads)")
    assert "ideation-readiness-nightly.py" in build["run"]
    assert "--phase prepare" in build["run"]
    assert '--as-of "${{ steps.run.outputs.run_date }}"' in build["run"]
    assert build["if"] == "steps.xref-readiness.outputs.ready == 'true'"


def test_readiness_collector_never_blocks_deterministic_finalize():
    finalize = workflow()["jobs"]["finalize"]
    collect = step(finalize, "Collect bounded readiness result")
    run = step(finalize, "Run doc-health suite")
    assert collect["continue-on-error"] is True
    assert collect["timeout-minutes"] == 45
    assert run["if"] == "always()"
    assert "worker_result_query_failed" in collect["run"]
    assert "QUEUE_DEADLINE=$((SECONDS + 600))" in collect["run"]
    assert "RUN_DEADLINE=$((SECONDS + 1800))" in collect["run"]
    assert '"$REASON" = "child_timeout"' in collect["run"]
    assert '"$REASON" = "child_queue_timeout"' in collect["run"]
    assert "gh run cancel" in collect["run"]
    assert "xref-findings/unavailable-reason.txt" in collect["run"]
    assert "doc-health-readiness-worker.yml" in collect["run"]
    assert "ideation-readiness-findings-${CORRELATION_ID}" in collect["run"]


# --- same-day commit gate (dashboard-lane-resilience Fix 3) ------------------
#
# A same-day rerun redirects only the DATED report/inventory to RUNNER_TEMP
# (records are immutable), but STILL refreshes living health/ artifacts (the
# ideation-dashboard lane status + snapshot, document-catalog runs, inventories).
# Gating the whole "Commit report" step on the same-day `commit` flag silently
# discarded those, leaving a stale-success lane status committed.

def test_commit_step_commits_living_health_on_same_day_reruns():
    finalize = workflow()["jobs"]["finalize"]
    # Prefix lookup: the step's name carries a delivery-mode suffix that has
    # already changed once (d72a0ca renamed it for the rolling-PR delivery)
    # -- the contract under test is the step's behavior, not its label.
    commit = next(item for item in finalize["steps"]
                  if (item.get("name") or "").startswith("Commit report"))
    # NOT gated on the same-day `commit` flag — so it runs on same-day reruns too.
    assert "steps.run.outputs.commit" not in (commit.get("if") or "")
    # It sweeps health/ and no-op-guards on a real tree diff (idiom-agnostic:
    # `|| git commit` and `if git diff --cached --quiet; then ... exit 0` both
    # satisfy the same-day-rerun contract; the redirected dated report never
    # re-enters the tree, so it cannot be re-committed).
    assert "git add health/" in commit["run"]
    assert "git diff --cached --quiet" in commit["run"]
    assert "git commit" in commit["run"]


def test_dated_report_and_inventory_stay_immutable_on_same_day_reruns():
    # The immutability half of Fix 3: the same-day redirect of the DATED artifacts
    # to RUNNER_TEMP is preserved, so `git add health/` cannot pick them up.
    run = step(workflow()["jobs"]["finalize"], "Run doc-health suite")
    assert 'REPORT_OUT="${RUNNER_TEMP}/doc-health-${RUN_DATE}.md"' in run["run"]
    assert 'INV_OUT="${RUNNER_TEMP}/inventory-${RUN_DATE}.json"' in run["run"]


def test_readiness_merge_step_always_runs_and_never_gates_on_readiness():
    finalize = workflow()["jobs"]["finalize"]
    merge = step(finalize, "Ideation readiness lane (merge, persist, report "
                          "link)")
    assert merge["if"] == "always()"
    assert merge["continue-on-error"] is True
    assert "ideation-readiness-nightly.py" in merge["run"]
    assert "--phase merge" in merge["run"]
    assert '--report-in "${{ steps.run.outputs.report_out }}"' in merge["run"]
    # not gated on xref-readiness/xref-dispatch outputs (unlike the steps
    # above): the whole point is it must run even when they never ran.
    assert "steps.xref-readiness" not in merge["if"]
    assert "steps.xref-dispatch" not in merge["if"]
