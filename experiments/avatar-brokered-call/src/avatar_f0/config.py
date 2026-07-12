"""Run configuration + fail-closed preflight (FR-001 / FR-003 / SC-009).

Preflight rejects a run BEFORE any provider call is created when the configuration
contains tenant data, enabled tools, a credential supplied via a prohibited channel, a
readiness value above the 5,000 ms ceiling, or any non-lab / unpinned profile.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from .acceptance_map import KERNEL_ACCEPTANCE_MAP_SHA256
from .candidate import READINESS_CEILING_MS, READINESS_DEFAULT_MS

VALID_GROUPS = ("F0-A", "F0-B", "F0-C", "F0-D", "F0-E", "F0-F")


class PreflightError(Exception):
    """Raised (fail-closed) when a run configuration is unsafe/unpinned.

    ``reason`` is a stable, bounded reason code (never free-form tenant content).
    """

    def __init__(self, reason: str, detail: str = "") -> None:
        super().__init__(f"{reason}: {detail}" if detail else reason)
        self.reason = reason


@dataclass
class RunConfig:
    lab_project_ref: str
    selected_groups: Tuple[str, ...] = VALID_GROUPS
    readiness_deadline_ms: int = READINESS_DEFAULT_MS
    acceptance_map_path: str = (
        "openspec/changes/define-avatar-client-contract-kernel/"
        "supporting-docs/avatar-client-acceptance-map.yaml"
    )
    # Default to the pinned known-good digest so a normal run verifies the map (FR-018).
    acceptance_map_expected_sha256: str = KERNEL_ACCEPTANCE_MAP_SHA256
    tools_enabled: bool = False
    profile_pinned: bool = True
    is_lab_profile: bool = True
    # Any populated entry here is treated as prohibited tenant material.
    tenant_fields: List[str] = field(default_factory=list)
    # Credential MUST arrive via env only; this must always be False.
    credential_in_arguments: bool = False
    credential_source: str = "env"


def validate_preflight(cfg: RunConfig) -> None:
    """Fail closed on any unsafe/unpinned configuration (FR-003 / SC-009)."""
    if cfg.tenant_fields:
        raise PreflightError("tenant_data_present", ",".join(sorted(set(cfg.tenant_fields))))
    if cfg.tools_enabled:
        raise PreflightError("tools_enabled")
    if cfg.credential_in_arguments or cfg.credential_source != "env":
        raise PreflightError("credential_in_arguments", cfg.credential_source)
    if cfg.readiness_deadline_ms > READINESS_CEILING_MS:
        raise PreflightError("readiness_above_ceiling", str(cfg.readiness_deadline_ms))
    if cfg.readiness_deadline_ms < 1000:
        raise PreflightError("readiness_below_floor", str(cfg.readiness_deadline_ms))
    if not cfg.is_lab_profile:
        raise PreflightError("non_lab_profile")
    if not cfg.profile_pinned:
        raise PreflightError("unpinned_profile")
    bad = [g for g in cfg.selected_groups if g not in VALID_GROUPS]
    if bad:
        raise PreflightError("unknown_trial_group", ",".join(bad))
    if not cfg.lab_project_ref.strip():
        raise PreflightError("missing_lab_project_ref")


def preflight_ok(cfg: RunConfig) -> Tuple[bool, Optional[str]]:
    try:
        validate_preflight(cfg)
        return True, None
    except PreflightError as exc:
        return False, exc.reason
