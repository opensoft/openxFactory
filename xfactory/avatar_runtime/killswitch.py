"""All-session and per-profile kill switches (FR-031)."""

from __future__ import annotations

from .values import KillSwitchState


class KillSwitchGate:
    @staticmethod
    def blocks_new(state: KillSwitchState, profile: str) -> bool:
        return state.all_session or (profile in state.disabled_profiles)

    @staticmethod
    def revokes_active(state: KillSwitchState) -> bool:
        # Active leases are revoked only when the switch policy requests it.
        return state.revoke_active_on_activate
