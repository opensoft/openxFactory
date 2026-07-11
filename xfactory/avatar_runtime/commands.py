"""Governed command validation + dedupe (FR-024/025)."""

from __future__ import annotations

from typing import Optional

from .control import ControlLease
from .session import LogicalSession
from .values import Command, CommandResult, ReasonCode

DEFAULT_ALLOWLIST = frozenset({"speak", "stop", "noop", "set_profile"})


class CommandProcessor:
    def __init__(self, allowlist: Optional[frozenset[str]] = None) -> None:
        self.allowlist = allowlist or DEFAULT_ALLOWLIST
        self._results: dict[str, CommandResult] = {}

    def submit(
        self,
        command: Command,
        *,
        session: LogicalSession,
        lease: Optional[ControlLease],
        now: int,
        lease_manager,
    ) -> CommandResult:
        # Dedupe by command id: return the first recorded result, no repeat effect.
        prior = self._results.get(command.command_id)
        if prior is not None:
            return prior

        reason = self._validate(command, session, lease, now, lease_manager)
        accepted = reason is ReasonCode.OK
        if accepted:
            session.state_revision += 1
        result = CommandResult(
            command_id=command.command_id,
            accepted=accepted,
            reason=reason,
            revision=session.state_revision,
        )
        self._results[command.command_id] = result
        return result

    def _validate(self, command, session, lease, now, lease_manager) -> ReasonCode:
        if lease is None or not lease.active or lease_manager.is_expired(lease, now):
            return ReasonCode.DENIED
        if command.epoch != session.epoch:
            return ReasonCode.DENIED
        if command.verb not in self.allowlist:
            return ReasonCode.DENIED
        if (
            command.expected_revision is not None
            and command.expected_revision != session.state_revision
        ):
            return ReasonCode.DENIED  # stale revision guard — no transition appended
        return ReasonCode.OK
