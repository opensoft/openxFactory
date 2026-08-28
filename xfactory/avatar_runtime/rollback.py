"""The recorded revoke-versus-block rollback act (tasks 6.3.2 wiring, 6.3.4).

THE POLICY IS THE SOURCE; THIS IS THE ACT. The three-way split, its triggers,
its revoke flags and its session-outcome tokens are ruled in
`contracts/avatar-client/canary-cohort-and-rollback-policy.yaml` and mirrored
here so the runtime can execute them.
``tests/avatar_runtime/test_ruled_values_pinned.py`` reads that YAML and fails
if the mirror drifts, including the mutation the policy's own validator is
built to catch — ROLLBACK-B's `revoke_active_leases` flipped to true, which
would cut people off mid-conversation on a performance regression.

NO NEW MECHANISM. A rollback act is a :class:`~.values.KillSwitchState` handed
to the runtime's EXISTING ``activate_kill_switch``. ROLLBACK-A's revocation is
that switch's ``revoke_active_on_activate`` path, which performs exactly the
landed consent-withdraw-mid-speech termination — lease revoked, capture
stopped through the idempotent provider hangup, credential-free terminal,
control channel healthy. Nothing here invents a terminal, and the outcome
tokens below are all members of the released, closed `session-outcomes`
registry.

THE ROLLBACK TARGET (6.3.4). `gpt-realtime-2.1` is the FIRST qualified live
profile. Rollback DISABLES VOICE and offers text or human handoff, and
:data:`MODEL_FALLBACK_EXISTS` is ``False`` because there is no other qualified
profile in existence — not because one is switched off. No name, string or
branch in this module offers a second model, and
``tests/avatar_runtime/test_rollback_target.py`` greps this package's own
source for every phrasing that would leave a reader expecting one.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from .values import AttemptStatus, KillSwitchState, OutcomeCode


#: The one qualified live profile at this ring.
CANDIDATE_PROFILE = "gpt-realtime-2.1"

#: 6.3.4, and it binds the copy as well as the code. There is nothing to swap
#: to: this is the first qualified live profile, so the value is a statement
#: about the world, not a feature flag.
MODEL_FALLBACK_EXISTS = False

#: The released `fallback-modes` registry tokens a withdrawn voice profile
#: leaves a session with. Both are existing members; neither is coined here.
ROLLBACK_OFFERED_MODES = ("text", "human_handoff")


class RollbackClass(Enum):
    """The ratified three-way split. CLOSED — a fourth class needs a ruling."""

    A = "ROLLBACK-A"  # hard safety or integrity breach -> abort WITH revocation
    B = "ROLLBACK-B"  # latency / elevated error / quota -> block new, drain
    C = "ROLLBACK-C"  # quality or cost judgment -> operator-selected


class KillSwitchId(Enum):
    """The kernel's two server kill switches. There is no third."""

    ALL_NEW = "SWITCH-ALL-NEW"
    PROFILE = "SWITCH-PROFILE"


class SwitchMode(Enum):
    """The two modes each switch carries (SOP: avatar-internal-live-kill-switch)."""

    BLOCK_NEW = "block_new"
    REVOKE_ACTIVE = "revoke_active"


#: `revoke_active_leases` per class, ruled. ROLLBACK-C's is operator-selected.
CLASS_REVOKES_ACTIVE: dict[RollbackClass, Optional[bool]] = {
    RollbackClass.A: True,
    RollbackClass.B: False,
    RollbackClass.C: None,
}

#: The ruled triggers of each automatic class (§6.3.2). ROLLBACK-C's two are
#: judgment calls and are listed for completeness, not for automation.
CLASS_TRIGGERS: dict[RollbackClass, frozenset[str]] = {
    RollbackClass.A: frozenset(
        {
            "revocation_bound_violation",
            "failed_blocked_state_evaluation",
            "failed_exact_value_evaluation",
            "failed_consent_evaluation",
            "failed_handoff_evaluation",
            "redaction_finding",
            "secret_scan_finding",
            "media_authorization_ordering_violation",
        }
    ),
    RollbackClass.B: frozenset(
        {
            "material_regression_on_a_gated_percentile",
            "elevated_error_rate",
            "elevated_quota_condition",
        }
    ),
    RollbackClass.C: frozenset({"quality_concern", "cost_concern"}),
}

#: §7.8's binding, as declared in advance. Every token is a member of the
#: released closed `session-outcomes` registry; no new token is introduced.
CLASS_SESSION_OUTCOME: dict[RollbackClass, Optional[str]] = {
    RollbackClass.A: "revoked",
    RollbackClass.B: "abandoned",
    RollbackClass.C: None,  # follows the scope the operator selects
}

CLASS_OUTCOME_PATH: dict[RollbackClass, Optional[str]] = {
    RollbackClass.A: "force_terminated_leg",
    RollbackClass.B: "drained_leg_after_block_new",
    RollbackClass.C: None,
}

#: A drained leg that reached its OWN natural terminal inside the drain window
#: is a `completed` session that happened to be in flight, and recording it as
#: `abandoned` would be false (§7.8 `also_permitted`).
DRAINED_LEG_ALSO_PERMITTED = ("completed",)


class RollbackPolicyError(ValueError):
    """A rollback act was requested outside the recorded policy."""


# --------------------------------------------------------------------------- #
# Terminal -> released session-outcome token
# --------------------------------------------------------------------------- #
def session_outcome_token(
    status: AttemptStatus, outcome: Optional[OutcomeCode] = None
) -> Optional[str]:
    """Map a media-leg terminal onto the released `session-outcomes` token.

    Returns None for a status this ring has not bound a token to, rather than
    guessing one. §7.8's whole point is that a path whose token was inferred
    after the fact lets two readers count the same event differently.
    """
    if status is AttemptStatus.REVOKED:
        return "revoked"
    if status is AttemptStatus.ABANDONED:
        return "abandoned"
    if status is AttemptStatus.EXPIRED:
        return "expired"
    if status is AttemptStatus.TERMINATED and outcome is OutcomeCode.CONNECTED:
        # The leg reached its own natural end. `completed` is the released
        # token for a logical session that finished.
        return "completed"
    return None


# --------------------------------------------------------------------------- #
# The act
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class RollbackDecision:
    rollback_class: RollbackClass
    trigger: str
    switch: KillSwitchId
    mode: SwitchMode
    revoke_active_leases: bool
    block_new_sessions: bool
    profile: str
    session_outcome: Optional[str]
    session_outcome_path: Optional[str]

    def kill_switch_state(self) -> KillSwitchState:
        """The EXISTING kill-switch value this decision hands to the runtime."""
        return KillSwitchState(
            all_session=self.switch is KillSwitchId.ALL_NEW,
            disabled_profiles=frozenset({self.profile}),
            revoke_active_on_activate=self.revoke_active_leases,
        )


def decide(
    rollback_class: RollbackClass,
    *,
    trigger: str,
    profile: str = CANDIDATE_PROFILE,
    profile_specific: bool = True,
    operator_revokes_active: Optional[bool] = None,
) -> RollbackDecision:
    """Resolve a rollback class and trigger into the switch act it authorises.

    SCOPE SELECTION follows the runbook's rule: ``SWITCH-PROFILE`` unless the
    condition is not specific to the candidate profile, because
    ``SWITCH-ALL-NEW`` is the wider blast radius and stops sessions that were
    never part of this ring.

    MODE SELECTION is not the operator's mood — it is this policy. A and B
    carry their ruled flags; only C is operator-selected, and C REQUIRES the
    operator to state the choice rather than defaulting to either reading.
    """
    if not isinstance(rollback_class, RollbackClass):
        raise RollbackPolicyError(f"unknown rollback class: {rollback_class!r}")
    allowed = CLASS_TRIGGERS[rollback_class]
    if trigger not in allowed:
        raise RollbackPolicyError(
            f"{rollback_class.value} does not recognise trigger {trigger!r}; "
            f"recorded triggers are {sorted(allowed)}"
        )
    ruled = CLASS_REVOKES_ACTIVE[rollback_class]
    if ruled is None:
        if operator_revokes_active is None:
            raise RollbackPolicyError(
                "ROLLBACK-C is operator-triggered: the operator must select "
                "whether active leases are revoked; there is no default"
            )
        revokes = bool(operator_revokes_active)
    else:
        if operator_revokes_active is not None:
            raise RollbackPolicyError(
                f"{rollback_class.value}'s revocation is ruled, not selected"
            )
        revokes = ruled
    outcome = CLASS_SESSION_OUTCOME[rollback_class]
    path = CLASS_OUTCOME_PATH[rollback_class]
    if rollback_class is RollbackClass.C:
        # C's outcome follows the scope the operator selects, in the same idiom
        # the class already uses for `action` and `revoke_active_leases`.
        outcome = "revoked" if revokes else "abandoned"
        path = "force_terminated_leg" if revokes else "drained_leg_after_block_new"
    return RollbackDecision(
        rollback_class=rollback_class,
        trigger=trigger,
        switch=KillSwitchId.PROFILE if profile_specific else KillSwitchId.ALL_NEW,
        mode=SwitchMode.REVOKE_ACTIVE if revokes else SwitchMode.BLOCK_NEW,
        revoke_active_leases=revokes,
        block_new_sessions=True,
        profile=profile,
        session_outcome=outcome,
        session_outcome_path=path,
    )


# --------------------------------------------------------------------------- #
# 6.3.4 — what a session-creation request is answered with after a rollback
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class RollbackPosture:
    """The posture the session-creation path answers with once voice is off.

    `voice_enabled` is False and the offered modes are the released
    `fallback-modes` tokens ``text`` and ``human_handoff``.
    ``model_fallback_exists`` is False and ``qualified_profiles_remaining`` is
    empty because `gpt-realtime-2.1` is the first qualified live profile: an
    operator or a user who waits for a swap is waiting for something that
    cannot happen, so the posture says so in the shape a caller can read.
    """

    voice_enabled: bool
    offered_modes: tuple[str, ...]
    model_fallback_exists: bool
    qualified_profiles_remaining: tuple[str, ...]
    withdrawn_profile: str
    statement: str


ROLLBACK_TARGET_STATEMENT = (
    "Voice is disabled for this profile. Text or human handoff is offered. "
    "gpt-realtime-2.1 is the first qualified live profile, so no model "
    "fallback exists and there is no other qualified profile to move to."
)


def rollback_posture(profile: str = CANDIDATE_PROFILE) -> RollbackPosture:
    """The answer a blocked session-creation request carries alongside its refusal."""
    return RollbackPosture(
        voice_enabled=False,
        offered_modes=ROLLBACK_OFFERED_MODES,
        model_fallback_exists=MODEL_FALLBACK_EXISTS,
        qualified_profiles_remaining=(),
        withdrawn_profile=profile,
        statement=ROLLBACK_TARGET_STATEMENT,
    )


@dataclass(frozen=True)
class RollbackOutcome:
    """What an applied rollback act did — the record the ring reads afterwards."""

    decision: RollbackDecision
    revoked_sessions: tuple[str, ...]
    blocked_profile: str
    posture: RollbackPosture
