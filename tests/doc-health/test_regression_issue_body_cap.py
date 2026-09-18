"""The doc-health nightly's regression-issue body stays under GitHub's
issue-body limit, and a failed `gh issue create` never fails `finalize`.

Fixes opensoft/openxFactory#1118: `.github/workflows/doc-health-reusable.yml`
"Open regression issue" wrote one bullet per new critical/error finding
straight into the issue body with no size cap. Once the list grew past
GitHub's 65536-character `createIssue` limit, `gh issue create` failed
every night from 2026-09-05 on (decisive log, run 35299844095: `GraphQL:
Body is too long (maximum is 65536 characters) (createIssue)`), reddening
`finalize` at a housekeeping step and hiding any real red elsewhere in the
job. The last issue it managed to open is opensoft/xFactory#236 (2026-09-04).

The cap logic is extracted into `scripts/doc_health/regression_issue_body.py`
(`render()`) rather than kept inline, because the fix needs it in TWO places
in one job run: "Open regression issue" is conditional
(`new_count != '0'`) and sits near the end of a long `finalize` job, but
"Upload report artifact" -- which has to carry the FULL, unabridged list
(`new-findings.md`) so nothing found is ever lost even when the issue body
itself is capped -- runs much earlier, right after `new-findings.json` is
produced. `render()` is called once from each site; this file's structural
tests (mirroring `test_workflow_guards.py`'s yaml.safe_load + step-finder
pattern) check both call sites are actually wired up, and its unit tests
check `render()` itself.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

from doc_health.regression_issue_body import DEFAULT_CAP_BYTES, render

WORKFLOW = (Path(__file__).resolve().parents[2]
            / ".github" / "workflows" / "doc-health-reusable.yml")

OPEN_ISSUE_STEP_NAME = "Open regression issue (one per run, contract regression rule)"


def load():
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))


def step(job, name):
    matches = [s for s in job["steps"] if s.get("name") == name]
    assert len(matches) == 1, f"expected exactly one step named {name!r}"
    return matches[0]


# --- structural: "Open regression issue" step -------------------------------

def test_open_regression_issue_step_name_and_condition_unchanged():
    # The brief requires the step name and `if:` to stay exactly as they
    # were before this fix -- only the run: body and the guard change.
    finalize = load()["jobs"]["finalize"]
    issue_step = step(finalize, OPEN_ISSUE_STEP_NAME)
    assert issue_step["if"] == "steps.run.outputs.new_count != '0'"
    assert issue_step["env"] == {"GH_TOKEN": "${{ github.token }}"}


def test_open_regression_issue_step_calls_the_extracted_renderer_with_the_cap():
    finalize = load()["jobs"]["finalize"]
    script = step(finalize, OPEN_ISSUE_STEP_NAME)["run"]
    assert "from doc_health.regression_issue_body import render" in script
    # The byte-cap constant is passed explicitly (not left to a silent
    # default) so it is visible in the step's own script, matching the
    # module's DEFAULT_CAP_BYTES.
    assert f"cap_bytes={DEFAULT_CAP_BYTES}" in script
    assert 'open("issue-body.md", "w").write(issue_body)' in script


def test_gh_issue_create_is_guarded_so_a_failure_cannot_fail_finalize():
    finalize = load()["jobs"]["finalize"]
    script = step(finalize, OPEN_ISSUE_STEP_NAME)["run"]
    assert "gh issue create" in script
    create_clause = script.split("gh issue create", 1)[1]
    assert "|| echo \"::warning::" in create_clause, (
        "gh issue create must be guarded with || echo \"::warning::...\" -- "
        "mirroring the sibling step's stated posture, \"Every gh call is "
        "guarded so this step can never fail the nightly\""
    )


# --- structural: the full list reaches the report artifact -------------------

def test_run_doc_health_suite_writes_new_findings_md_before_the_upload_step():
    finalize = load()["jobs"]["finalize"]
    run_script = step(finalize, "Run doc-health suite")["run"]
    assert "from doc_health.regression_issue_body import render" in run_script
    assert f"cap_bytes={DEFAULT_CAP_BYTES}" in run_script
    assert 'open("new-findings.md", "w").write(full_list_md)' in run_script

    steps = finalize["steps"]
    names = [s.get("name") for s in steps]
    assert names.index("Run doc-health suite") < names.index("Upload report artifact"), (
        "new-findings.md must be written before 'Upload report artifact' "
        "runs -- 'Open regression issue' is both conditional and much "
        "later in this job, too late for that step to pick the file up"
    )


def test_upload_report_artifact_step_collects_new_findings_md_too():
    finalize = load()["jobs"]["finalize"]
    upload = step(finalize, "Upload report artifact")
    path = upload["with"]["path"]
    lines = [line.strip() for line in path.splitlines() if line.strip()]
    assert "${{ steps.run.outputs.report_out }}" in lines, (
        "the original report path must still be collected"
    )
    assert "new-findings.md" in lines, (
        "new-findings.md (the full, unabridged list) must be collected "
        "alongside the capped report so nothing found is ever lost"
    )


# --- unit: render() itself ----------------------------------------------------

def _finding(i: int, severity: str = "error") -> dict:
    return {
        "severity": severity,
        "family": "promotion-fidelity",
        "repo": "openxFactory",
        "path": f"ideation/staging/topic{i:05d}/fragment-{i:05d}.md",
        "rule": "stale-fragment-reference-needs-review",
        "action": "flag",
        "resolution": "auto-fixable",
        "disposer": None,
    }


def test_render_returns_a_body_under_the_default_cap_for_a_small_list():
    findings = [_finding(i) for i in range(3)]
    body, full = render(findings, "2026-09-18")
    assert len(body.encode("utf-8")) <= DEFAULT_CAP_BYTES
    assert "3 new critical/error findings (the first 3 are listed here" in body
    assert "0 finding(s) omitted" in body
    for i in range(3):
        assert f"fragment-{i:05d}.md" in body
        assert f"fragment-{i:05d}.md" in full


def test_render_caps_a_large_list_and_names_the_full_count_and_omission():
    # 5000 synthetic findings -- deliberately large enough to force
    # truncation under any reasonable byte cap.
    findings = [_finding(i) for i in range(5000)]
    body, full = render(findings, "2026-09-18", cap_bytes=60000)

    encoded_len = len(body.encode("utf-8"))
    assert encoded_len <= 60000
    # Bytes upper-bound characters for UTF-8, so the character count GitHub
    # actually enforces (65536) is safely clear too.
    assert len(body) < 65536

    assert "5000 new critical/error findings (the first " in body
    assert "the full list is in the report artifact and in " in body
    assert "health/reports/2026-09-18.md" in body

    m = re.search(r"the first (\d+) are listed here", body)
    assert m, "count line not found"
    included = int(m.group(1))
    assert 0 < included < 5000, "5000 findings at this cap must truncate"

    m2 = re.search(r"(\d+) finding\(s\) omitted", body)
    assert m2, "omitted line not found"
    omitted = int(m2.group(1))
    assert omitted == 5000 - included

    # The full, unabridged list is never truncated -- every one of the
    # 5000 synthetic findings' distinguishing paths appears in it, one
    # bullet per line.
    for i in range(5000):
        assert f"fragment-{i:05d}.md" in full
    assert len([ln for ln in full.splitlines() if ln]) == 5000


def test_render_body_bytes_never_exceed_a_small_cap_either():
    # Exercises the budget arithmetic at a scale where the header/count/
    # omitted-line skeleton is a large fraction of the cap, catching
    # off-by-one errors in the separator accounting that a generously-sized
    # cap (like the real 60000-byte default) could hide. These values are
    # comfortably above this data shape's fixed skeleton (~400-450 bytes,
    # asserted separately below) so each one still forces real truncation of
    # the 50 bullets (each bullet is itself well over 100 bytes).
    findings = [_finding(i) for i in range(50)]
    for cap in (1000, 1500, 2000, 3000):
        body, _ = render(findings, "2026-09-18", cap_bytes=cap)
        assert len(body.encode("utf-8")) <= cap, f"cap={cap} violated"
        m = re.search(r"the first (\d+) are listed here", body)
        included = int(m.group(1))
        assert 0 < included < 50, (
            f"cap={cap} should force partial truncation of 50 findings, "
            f"got {included} included"
        )


def test_render_raises_when_cap_bytes_cannot_even_hold_the_skeleton():
    # Not a reservation bug: a cap_bytes below the fixed header/count/
    # omitted-line overhead is genuinely unsatisfiable (this never happens
    # in production, where cap_bytes is always the 60000-byte default), and
    # render() says so via AssertionError rather than silently emitting a
    # body over its own cap.
    findings = [_finding(i) for i in range(50)]
    with pytest.raises(AssertionError):
        render(findings, "2026-09-18", cap_bytes=50)


def test_render_empty_findings_list_is_well_formed():
    body, full = render([], "2026-09-18")
    assert full == ""
    assert "0 new critical/error findings (the first 0 are listed here" in body
    assert "0 finding(s) omitted" in body
    assert len(body.encode("utf-8")) <= DEFAULT_CAP_BYTES


def test_module_default_cap_is_60000_matching_githubs_65536_character_limit():
    # 60000 bytes always encodes to <= 60000 characters for any string
    # (UTF-8 bytes >= characters), which is safely under GitHub's actual
    # 65536-character createIssue limit -- the margin covers the header,
    # count line and omitted-count line that always accompany the bullets.
    assert DEFAULT_CAP_BYTES == 60000
    assert DEFAULT_CAP_BYTES < 65536
