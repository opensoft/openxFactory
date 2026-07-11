"""US2-S2 / FR-003 / SC-009: preflight rejects unsafe/unpinned configs before any call."""
import pytest

from avatar_f0.config import PreflightError, RunConfig, validate_preflight


def _cfg(**kw):
    base = dict(lab_project_ref="lab:f0")
    base.update(kw)
    return RunConfig(**base)


def test_clean_config_passes():
    validate_preflight(_cfg())


@pytest.mark.parametrize("kw,reason", [
    (dict(tenant_fields=["subject_name"]), "tenant_data_present"),
    (dict(tools_enabled=True), "tools_enabled"),
    (dict(credential_in_arguments=True), "credential_in_arguments"),
    (dict(credential_source="file"), "credential_in_arguments"),
    (dict(readiness_deadline_ms=6000), "readiness_above_ceiling"),
    (dict(readiness_deadline_ms=500), "readiness_below_floor"),
    (dict(is_lab_profile=False), "non_lab_profile"),
    (dict(profile_pinned=False), "unpinned_profile"),
    (dict(selected_groups=("F0-Z",)), "unknown_trial_group"),
    (dict(lab_project_ref="  "), "missing_lab_project_ref"),
])
def test_preflight_rejects(kw, reason):
    with pytest.raises(PreflightError) as exc:
        validate_preflight(_cfg(**kw))
    assert exc.value.reason == reason


def test_credential_in_arguments_helper():
    from avatar_f0.credential import CredentialError, reject_if_in_arguments
    with pytest.raises(CredentialError):
        reject_if_in_arguments(["run", "sk-ABCDEF0123456789abcdef0123456789"])
    # a normal arg / a 64-hex digest must NOT trip the guard
    reject_if_in_arguments(["run", "--groups", "F0-A", "a" * 64])
