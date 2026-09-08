"""`scripts/avatar-metering-alert.py` fails closed on an unreadable policy.

The recipient is the one value §7.4 refuses to send an alert without, and the
policy file is where it is read from — so every way that read can fail has to
end in a clear message and the harness exit code, never a parser traceback.
That is the same boundary `validate-avatar-client.py` draws with its
`MalformedYAML`: catch the parser error AT THE READ and re-raise it carrying
the file's identity.

The script is hyphenated, so it is loaded by file path with `importlib`, the
same way the sibling tests under `tests/avatar_client_validator/` load the
validator.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

import pytest
import yaml

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
ENTRYPOINT = REPOSITORY_ROOT / "scripts" / "avatar-metering-alert.py"
REAL_POLICY = (
    REPOSITORY_ROOT / "contracts" / "avatar-client"
    / "canary-cohort-and-rollback-policy.yaml"
)


def _load_script() -> ModuleType:
    spec = importlib.util.spec_from_file_location("avatar_metering_alert", ENTRYPOINT)
    assert spec and spec.loader, f"cannot load script at {ENTRYPOINT}"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SCRIPT = _load_script()


def _input_file(tmp_path: Path, sessions: list[dict]) -> Path:
    import json

    path = tmp_path / "metering-run.json"
    path.write_text(json.dumps({"sessions": sessions}), encoding="utf-8")
    return path


CROSSING_SESSION = {
    "session_id": "s1",
    "tenant_ref": "COHORT-01",
    "attempt_ref": "req-1",
    "billable_units": 15000,
    "usd_cents": 15000,
    "outcome": "connected",
    "reason": "non_ceiling_terminal",
    "cost_triggered": False,
    "countable": True,
    "opened_at": 0,
    "closed_at": 120,
}


# --- the shipped policy is readable, and the recipient comes from it ------- #
def test_the_shipped_policy_yields_a_named_recipient_and_runbook():
    holder, runbook = SCRIPT.operator_surface(REAL_POLICY)
    assert holder.strip()
    assert runbook == "docs/sops/avatar-internal-live-kill-switch.md"
    # It is the SAME value the policy records, read rather than copied.
    doc = yaml.safe_load(REAL_POLICY.read_text(encoding="utf-8"))
    surface = doc["rollback_policy"]["operator_surface"]
    assert (holder, runbook) == (surface["holder"], surface["mechanism_ref"])


# --- every way the read can fail ends in FailClosed ------------------------ #
@pytest.mark.parametrize(
    "name,body",
    [
        # A YAML SYNTAX ERROR — the case that used to traceback.
        ("unclosed-bracket", "rollback_policy: [oops\n"),
        ("bad-indent", "rollback_policy:\n  operator_surface:\n   holder: x\n  \tbad: y\n"),
        ("duplicate-anchor", "a: *nope\n"),
        ("tab-indent", "rollback_policy:\n\toperator_surface: {}\n"),
        # Parses, but is not a policy.
        ("empty", ""),
        ("not-a-mapping", "- just\n- a\n- list\n"),
        ("scalar", "just a string\n"),
        ("no-rollback-policy", "schema_version: 1\nkind: something-else\n"),
        ("rollback-policy-not-a-mapping", "rollback_policy: a string\n"),
        ("no-operator-surface", "rollback_policy:\n  classes: []\n"),
        ("operator-surface-not-a-mapping", "rollback_policy:\n  operator_surface: 7\n"),
        # Parses and is a policy, but names nobody.
        (
            "unnamed-surface",
            "rollback_policy:\n  operator_surface:\n"
            "    status: unnamed\n    holder: null\n",
        ),
        (
            "named-but-no-holder",
            "rollback_policy:\n  operator_surface:\n"
            "    status: named\n"
            "    mechanism_ref: docs/sops/avatar-internal-live-kill-switch.md\n",
        ),
        (
            "named-but-no-runbook",
            "rollback_policy:\n  operator_surface:\n"
            "    status: named\n    holder: A Person\n",
        ),
    ],
)
def test_an_unreadable_policy_fails_closed_with_a_clear_message(tmp_path, name, body):
    policy = tmp_path / f"{name}.yaml"
    policy.write_text(body, encoding="utf-8")

    with pytest.raises(SCRIPT.FailClosed) as raised:
        SCRIPT.operator_surface(policy)

    message = str(raised.value)
    assert message  # a sentence, not an empty parser repr
    # The file's identity reaches the message, or the field that is missing is
    # named — a reader must know what to go and fix.
    assert str(policy) in message or "operator_surface" in message


def test_a_missing_policy_fails_closed(tmp_path):
    with pytest.raises(SCRIPT.FailClosed):
        SCRIPT.operator_surface(tmp_path / "not-here.yaml")


def test_a_yaml_error_is_not_allowed_to_escape_as_itself(tmp_path):
    """The parser's own exception must be converted, not propagated."""
    policy = tmp_path / "broken.yaml"
    policy.write_text("rollback_policy: [oops\n", encoding="utf-8")
    with pytest.raises(SCRIPT.FailClosed):
        SCRIPT.operator_surface(policy)
    # And the parser error is kept as the cause, so the detail is not lost.
    try:
        SCRIPT.operator_surface(policy)
    except SCRIPT.FailClosed as exc:
        assert isinstance(exc.__cause__, yaml.YAMLError)


# --- and the CLI turns that into the harness exit code, not a traceback ---- #
def test_the_cli_exits_with_the_harness_code_on_a_malformed_policy(tmp_path, capsys):
    policy = tmp_path / "broken.yaml"
    policy.write_text("rollback_policy: [oops\n", encoding="utf-8")
    argv = [
        "--input", str(_input_file(tmp_path, [CROSSING_SESSION])),
        "--run-date", "2026-08-27",
        "--policy", str(policy),
    ]

    code = SCRIPT.main(argv)

    assert code == SCRIPT.HARNESS_ERROR == 2
    err = capsys.readouterr().err
    assert "FAIL-CLOSED" in err
    assert "does not parse as YAML" in err


def test_the_cli_renders_the_alert_against_the_shipped_policy(tmp_path, capsys):
    body_file = tmp_path / "issue-body.md"
    argv = [
        "--input", str(_input_file(tmp_path, [CROSSING_SESSION])),
        "--run-date", "2026-08-27",
        "--policy", str(REAL_POLICY),
        "--body-file", str(body_file),
    ]

    assert SCRIPT.main(argv) == 0
    holder, runbook = SCRIPT.operator_surface(REAL_POLICY)
    rendered = body_file.read_text(encoding="utf-8")
    assert holder in rendered and runbook in rendered
    assert "avatar internal-live metering 2026-08-27" in capsys.readouterr().out


def test_a_quiet_run_reports_its_own_exit_code(tmp_path):
    quiet = dict(CROSSING_SESSION, usd_cents=100, billable_units=100)
    argv = [
        "--input", str(_input_file(tmp_path, [quiet])),
        "--run-date", "2026-08-27",
        "--policy", str(REAL_POLICY),
    ]
    assert SCRIPT.main(argv) == SCRIPT.QUIET_RUN == 3


def test_a_malformed_metering_input_fails_closed_rather_than_tracebacking(tmp_path):
    broken = tmp_path / "run.json"
    broken.write_text("{not json", encoding="utf-8")
    argv = [
        "--input", str(broken),
        "--run-date", "2026-08-27",
        "--policy", str(REAL_POLICY),
    ]
    assert SCRIPT.main(argv) == SCRIPT.HARNESS_ERROR
