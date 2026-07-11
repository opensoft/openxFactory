"""In-process runtime assembly (FR-001/FR-003).

Wires the injected ports together. Holds only in-memory state; ``destroy()``
discards everything and requires no migration, durable-state cleanup, or
recovery of secret grant material (SC-009). This is deliberately NOT an
application factory: it opens no socket and loads no credential.

The Foundational skeleton exposes port wiring, a session registry, and
``destroy()``. The US1 phase composes the protocol managers (broker, control,
media authorization, event log, snapshots, authority, consent, operations,
usage, kill switches) onto this facade.
"""

from __future__ import annotations

from typing import Optional

from .ports import (
    ClockPort,
    ConsentPort,
    IdPort,
    OperationPort,
    PolicyPort,
    ProviderPort,
    UsagePort,
)
from .telemetry import TelemetrySink
from .values import KillSwitchState


class AvatarRuntime:
    def __init__(
        self,
        *,
        clock: ClockPort,
        ids: IdPort,
        provider: ProviderPort,
        policy: PolicyPort,
        consent: ConsentPort,
        operation: OperationPort,
        usage: UsagePort,
        kill_switch: Optional[KillSwitchState] = None,
        telemetry: Optional[TelemetrySink] = None,
    ) -> None:
        self.clock = clock
        self.ids = ids
        self.provider = provider
        self.policy = policy
        self.consent = consent
        self.operation = operation
        self.usage = usage
        self.kill_switch = kill_switch or KillSwitchState()
        self.telemetry = telemetry or TelemetrySink()

        # In-memory registries (no persistence).
        self.sessions: dict = {}
        self._destroyed = False

        # Protocol managers are attached lazily by the US1 composition layer.
        self._compose()

    def _compose(self) -> None:
        """Attach protocol managers if the US1 layer is present."""
        try:
            from .composition import attach_managers
        except ImportError:
            return
        attach_managers(self)

    # ------------------------------------------------------------------ #
    def destroy(self) -> None:
        """Discard all in-memory state — no durable state exists (FR-003)."""
        self.sessions.clear()
        self._destroyed = True

    @property
    def destroyed(self) -> bool:
        return self._destroyed
