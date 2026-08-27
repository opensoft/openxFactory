"""The worker-readiness gates must FAIL CLOSED when they emit their verdict.

Every `Evaluate ... worker readiness` step in `doc-health-reusable.yml` decides
whether this run may ship untrusted, per-cluster analysis payloads to a
self-hosted artifact worker.  It publishes that decision by appending
`ready=<bool>` to `$GITHUB_OUTPUT`, and the dispatch step downstream gates on
`steps.<id>.outputs.ready == 'true'`.

`$GITHUB_OUTPUT` is a newline-delimited `key=value` file and the LAST write of a
key wins.  `ready` is written FIRST, before `reason` and `dispatch_label` --
neither of which this repository produces (`dispatch_label` is echoed out of the
remote Hermes heartbeat, through the caller repository's
`check-worker-readiness.py`).  A newline inside either value therefore appends
its own `ready=true` line after the real verdict and flips a fail-closed gate
open.  That is the fail-open class recorded as informational finding 5(a) of the
2026-07-26 adversarial review of the nightly-sweep pipeline.

These tests EXECUTE the emitter exactly as the workflow ships it -- the snippet
is extracted from the parsed YAML, not copied -- and prove the REFUSAL: a value
that cannot be rendered on one line yields `ready=false` and no injected key.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "doc-health-reusable.yml"

# (job, step name, the evaluator output file the emitter reads, correlation id
# prefix) -- one row per readiness gate in the nightly.
GATES = [
    ("prepare", "Evaluate hosted worker readiness",
     "readiness.json", "semantic"),
    ("prepare", "Evaluate cataloger worker readiness",
     "catalog-readiness.json", "catalog"),
    ("prepare", "Evaluate organizer worker readiness",
     "organizer-readiness.json", "organizer"),
    ("finalize", "Evaluate readiness-scorer worker readiness",
     "xref-readiness.json", "readiness"),
    ("finalize", "Evaluate derive-possibles worker readiness",
     "dposs-readiness.json", "derive-possibles"),
    ("finalize", "Evaluate dashboard-refresh worker readiness",
     "dfr-readiness.json", "dashboard-refresh"),
]

EMITTER = re.compile(
    r"python3 - <<'PY' >> \"\$GITHUB_OUTPUT\"\n(.*?)\nPY\n",
    re.DOTALL)


def _workflow() -> dict:
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))


def _step(job: str, name: str) -> dict:
    steps = _workflow()["jobs"][job]["steps"]
    return next(item for item in steps if item.get("name") == name)


def _emitter_source(job: str, name: str) -> str:
    """The verdict-emitting snippet exactly as the workflow ships it."""
    found = EMITTER.findall(_step(job, name)["run"])
    assert len(found) == 1, \
        f"{name!r} must carry exactly one $GITHUB_OUTPUT emitter, found {len(found)}"
    return found[0]


def _run(tmp_path: Path, job: str, name: str, fixture_name: str,
         payload) -> tuple[str, dict[str, str]]:
    """Execute the shipped emitter; return (raw file, last-write-wins mapping)."""
    if payload is not None:
        (tmp_path / fixture_name).write_text(
            json.dumps(payload), encoding="utf-8")
    out = tmp_path / "github_output"
    out.write_text("", encoding="utf-8")
    script = tmp_path / "emitter.py"
    script.write_text(_emitter_source(job, name), encoding="utf-8")
    with out.open("a", encoding="utf-8") as handle:
        result = subprocess.run(
            [sys.executable, str(script)], cwd=tmp_path, stdout=handle,
            stderr=subprocess.PIPE, text=True, check=False,
            env={"GITHUB_RUN_ID": "9", "GITHUB_RUN_ATTEMPT": "1",
                 "PATH": "/usr/bin:/bin"})
    raw = out.read_text(encoding="utf-8")
    effective: dict[str, str] = {}
    for line in raw.splitlines():
        if "=" in line:
            key, _, value = line.partition("=")
            effective[key] = value          # last write wins, as Actions does
    assert result.returncode == 0, \
        f"emitter must not crash the step: {result.stderr}"
    return raw, effective


# --- the happy path still works (a refusal that refuses everything is useless)

@pytest.mark.parametrize("job,name,fixture,prefix", GATES)
def test_a_well_formed_ready_verdict_is_published_unchanged(
        tmp_path, job, name, fixture, prefix):
    raw, effective = _run(tmp_path, job, name, fixture, {
        "ready": True, "reason": "ready", "dispatch_label": "host-alpha"})
    assert effective["ready"] == "true"
    assert effective["reason"] == "ready"
    assert effective["dispatch_label"] == "host-alpha"
    assert effective["correlation_id"] == f"{prefix}-9-1"
    assert len(raw.splitlines()) == 4


@pytest.mark.parametrize("job,name,fixture,prefix", GATES)
def test_a_well_formed_not_ready_verdict_keeps_its_reason(
        tmp_path, job, name, fixture, prefix):
    _, effective = _run(tmp_path, job, name, fixture, {
        "ready": False, "reason": "heartbeat_stale"})
    assert effective["ready"] == "false"
    assert effective["reason"] == "heartbeat_stale"
    assert effective["dispatch_label"] == ""


# --- the refusals -----------------------------------------------------------

@pytest.mark.parametrize("job,name,fixture,prefix", GATES)
def test_a_newline_in_dispatch_label_cannot_forge_a_ready_verdict(
        tmp_path, job, name, fixture, prefix):
    """The heartbeat-sourced label is the untrusted value closest to the gate."""
    raw, effective = _run(tmp_path, job, name, fixture, {
        "ready": False, "reason": "worker_unavailable",
        "dispatch_label": "host-alpha\nready=true"})
    assert effective["ready"] == "false", "the gate was flipped open"
    assert "ready=true" not in raw
    assert effective["reason"] == "readiness_output_unsafe"
    assert effective["dispatch_label"] == ""
    assert len(raw.splitlines()) == 4, f"injected extra output keys: {raw!r}"


@pytest.mark.parametrize("job,name,fixture,prefix", GATES)
def test_a_newline_in_reason_cannot_forge_a_ready_verdict(
        tmp_path, job, name, fixture, prefix):
    raw, effective = _run(tmp_path, job, name, fixture, {
        "ready": False, "reason": "worker_unavailable\nready=true",
        "dispatch_label": ""})
    assert effective["ready"] == "false", "the gate was flipped open"
    assert "ready=true" not in raw
    assert effective["reason"] == "readiness_output_unsafe"
    assert len(raw.splitlines()) == 4, f"injected extra output keys: {raw!r}"


@pytest.mark.parametrize("job,name,fixture,prefix", GATES)
def test_a_carriage_return_is_refused_too(
        tmp_path, job, name, fixture, prefix):
    """Actions splits on \\r as well, so a lone CR is the same attack."""
    raw, effective = _run(tmp_path, job, name, fixture, {
        "ready": True, "reason": "ready",
        "dispatch_label": "host-alpha\rdispatch_label=host-evil"})
    assert effective["ready"] == "false"
    assert effective["dispatch_label"] == ""
    assert "host-evil" not in raw


@pytest.mark.parametrize("job,name,fixture,prefix", GATES)
def test_a_non_boolean_ready_is_not_a_verdict(
        tmp_path, job, name, fixture, prefix):
    """A JSON string \"true\" must not be laundered into a ready gate."""
    _, effective = _run(tmp_path, job, name, fixture, {
        "ready": "true", "reason": "ready", "dispatch_label": "host-alpha"})
    assert effective["ready"] == "false"
    assert effective["reason"] == "readiness_output_unusable"
    assert effective["dispatch_label"] == ""


@pytest.mark.parametrize("job,name,fixture,prefix", GATES)
def test_a_missing_evaluator_result_refuses_rather_than_crashing(
        tmp_path, job, name, fixture, prefix):
    _, effective = _run(tmp_path, job, name, fixture, None)
    assert effective["ready"] == "false"
    assert effective["reason"] == "readiness_output_unusable"


@pytest.mark.parametrize("job,name,fixture,prefix", GATES)
def test_a_non_object_evaluator_result_refuses(
        tmp_path, job, name, fixture, prefix):
    _, effective = _run(tmp_path, job, name, fixture, ["ready"])
    assert effective["ready"] == "false"
    assert effective["reason"] == "readiness_output_unusable"


@pytest.mark.parametrize("job,name,fixture,prefix", GATES)
def test_an_evaluator_result_without_a_reason_refuses(
        tmp_path, job, name, fixture, prefix):
    _, effective = _run(tmp_path, job, name, fixture, {"ready": True})
    assert effective["ready"] == "false"
    assert effective["reason"] == "readiness_output_unusable"


# --- the naive form must not come back --------------------------------------

@pytest.mark.parametrize("job,name,fixture,prefix", GATES)
def test_the_unguarded_emitter_form_is_not_reintroduced(
        job, name, fixture, prefix):
    source = _emitter_source(job, name)
    assert "print(f\"reason={value['reason']}\")" not in source, \
        "an unvalidated value is being written straight to $GITHUB_OUTPUT"
    assert "print(f\"dispatch_label={value.get('dispatch_label', '')}\")" \
        not in source
    assert "def one_line(value):" in source
    assert 'readiness_output_unsafe' in source
