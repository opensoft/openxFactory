"""The Python 3.14 leg is wired as ruled, and the required suite is untouched.

Brett Heap's ruling on opensoft/openxFactory#1201, part 3 ("add the 3.14 CI
leg"): `.github/workflows/doc-health-py314.yml` runs `tests/doc-health` on a
real 3.14 interpreter as its OWN job. It is not a matrix on the required
`pytest-suite` job, because a matrix renames that job's check-runs and the
ruleset's pinned `pytest-suite` context would then never report.
"""

from __future__ import annotations

import yaml

from conftest import REPO_ROOT

WORKFLOWS = REPO_ROOT / ".github" / "workflows"


def _workflow(name: str) -> dict:
    return yaml.safe_load((WORKFLOWS / name).read_text(encoding="utf-8"))


def _triggers(document: dict) -> dict:
    # YAML 1.1 reads a bare `on:` key as the boolean True.
    return document.get("on", document.get(True))


def _setup_python_versions(job: dict) -> list[str]:
    return [str(step["with"]["python-version"]) for step in job["steps"]
            if str(step.get("uses", "")).startswith("actions/setup-python")]


def test_the_leg_runs_the_doc_health_suite_on_python_314():
    document = _workflow("doc-health-py314.yml")
    assert set(_triggers(document)) == {"pull_request", "push"}
    assert list(document["jobs"]) == ["doc-health-py314"]
    job = document["jobs"]["doc-health-py314"]
    # No display name and no matrix: the check surfaces as exactly the job id.
    assert "name" not in job and "strategy" not in job
    assert _setup_python_versions(job) == ["3.14"]
    runs = [str(step.get("run", "")) for step in job["steps"]]
    assert any(run.strip().startswith("python -m pytest tests/doc-health")
               for run in runs), runs
    assert any("--require-hashes" in run for run in runs), runs


def test_the_required_pytest_suite_job_keeps_its_name_and_takes_no_matrix():
    job = _workflow("pytest-suite.yml")["jobs"]["pytest-suite"]
    assert "name" not in job and "strategy" not in job
    assert len(_setup_python_versions(job)) == 1
