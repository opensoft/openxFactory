"""Execute the workflow's real shell with synthetic untrusted PR bodies."""
from pathlib import Path
import os
import subprocess
import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github/workflows/lane-line.yml"

def workflow():
    return yaml.load(WORKFLOW.read_text(), Loader=yaml.BaseLoader)

def validator():
    steps = workflow()["jobs"]["lane-line"]["steps"]
    return next(step for step in steps if "BODY" in step.get("env", {}))

@pytest.mark.parametrize(("body", "accepted"), [
    ("", True), (" \n\t\r\n", True),
    ("Ordinary outside-lane proposal\n\nDescription.", True),
    ("This prose mentions `Lane:` without declaring one.", True),
    ("Lane: openxFactory-7", True),
    ("\r\n \r\nLane: codeXfactory-2 (review)\r\nBody", True),
    ("Lane:", False), ("Lane: bad_name", False),
    ("Lane: bad/name", False), ("Lane: two names", False),
    ("lane: example-1", False), (" Lane: example-1", False),
    ("Lane : example-1", False), ("Lane:\texample-1", False),
    ("Title\nLane: example-1", False),
    ("Lane: example-1\nLane: example-1", False),
    ("Lane: example-1\n lane: another-2", False),
    ("Lane: example-1 (unterminated", False),
])
def test_optional_declaration_cases(tmp_path, body, accepted):
    result = subprocess.run(["bash", "-e", "-o", "pipefail", "-c", validator()["run"]],
                            cwd=tmp_path, env={**os.environ, "BODY": body},
                            capture_output=True, text=True, timeout=5)
    assert (result.returncode == 0) is accepted, result.stdout + result.stderr

def test_body_is_inert_and_never_reemitted(tmp_path):
    body = "$(touch sentry)\n`touch sentry`\n::error::untrusted-command"
    result = subprocess.run(["bash", "-e", "-o", "pipefail", "-c", validator()["run"]],
                            cwd=tmp_path, env={**os.environ, "BODY": body},
                            capture_output=True, text=True, timeout=5)
    assert result.returncode == 0
    assert not (tmp_path / "sentry").exists()
    assert "untrusted-command" not in result.stdout
    assert body not in result.stdout

def test_events_permissions_and_untrusted_input_plumbing_are_preserved():
    data = workflow()
    assert data["name"] == "lane-line"
    assert data["permissions"] == {"contents": "read"}
    assert data["on"]["pull_request"]["types"] == ["opened", "edited", "synchronize", "reopened"]
    step = validator()
    assert step["env"]["BODY"] == "${{ github.event.pull_request.body }}"
    assert "${{" not in step["run"]
    assert "checkout" not in WORKFLOW.read_text()

def test_existing_bot_exemption_is_preserved():
    job = workflow()["jobs"]["lane-line"]
    if "if" in job:
        # codeXfactory's existing bot check intentionally concludes skipped.
        assert job["if"] == "github.event.pull_request.user.type != 'Bot'"
    else:
        # openxFactory already has a success-concluding bot exemption.
        author = next(step for step in job["steps"] if step.get("id") == "author")
        assert author["env"]["ACTOR_TYPE"] == "${{ github.event.pull_request.user.type }}"
        assert 'if [ "$ACTOR_TYPE" = "Bot" ]' in author["run"]
        assert 'echo "exempt=true"' in author["run"]
        assert validator()["if"] == "steps.author.outputs.exempt != 'true'"
