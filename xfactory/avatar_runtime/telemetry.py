"""Structured, redacted telemetry (FR-033, SC-007, D9).

A record is published only if it passes redaction. The validator uses an
allowlist of stable field kinds plus rejected pattern classes (U2):
- Allowlist: stable low-cardinality keys, closed-registry enum values, and
  references prefixed ``sha256:`` (salted digest) or ``fixture:``.
- Rejected: SDP blocks, credential shapes, provider payloads / transcript /
  media (by key or content), and opaque high-cardinality identifiers.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


class RedactionError(ValueError):
    """Raised (and record dropped) when protected content is detected."""


# Stable, low-cardinality field keys permitted verbatim.
ALLOWED_KEYS = frozenset(
    {
        "test_id",
        "scenario_id",
        "reason",
        "transition",
        "usage_outcome",
        "clock_ts",
        "epoch",
        "state",
        "outcome",
    }
)

# Keys that MUST NEVER carry raw content.
FORBIDDEN_KEYS = frozenset(
    {
        "sdp",
        "answer",
        "credential",
        "control",
        "payload",
        "provider_payload",
        "transcript",
        "media",
        "secret",
    }
)

# Permitted reference prefixes for otherwise-sensitive values.
ALLOWED_PREFIXES = ("sha256:", "fixture:")

# Credential shapes (mirrors xfactory/memory_gateway.py's SECRET_RE spirit).
_SECRET_RE = re.compile(
    r"-----BEGIN .*PRIVATE KEY-----"
    r"|\b(?:password|passwd|secret|token)\s*[:=]\s*['\"]?[A-Za-z0-9+/]{12,}"
    r"|\bsk-[A-Za-z0-9]{20,}\b"
    r"|\bgh[pousr]_[A-Za-z0-9]{20,}\b"
    r"|\bAKIA[0-9A-Z]{16}\b"
    r"|\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.",  # JWT
    re.IGNORECASE,
)

# SDP / ICE lines.
_SDP_RE = re.compile(r"(?m)^(?:m=|a=|v=|c=IN|o=|s=|candidate:)")

# Raw UUID (opaque, high-cardinality).
_UUID_RE = re.compile(
    r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b"
)


def _value_is_redaction_safe(key: str, value: Any) -> bool:
    if key in FORBIDDEN_KEYS:
        return False
    if not isinstance(value, str):
        # ints/enums/bools are low-cardinality and safe.
        return True
    if value.startswith(ALLOWED_PREFIXES):
        return True
    if _SECRET_RE.search(value):
        return False
    if _SDP_RE.search(value):
        return False
    if _UUID_RE.search(value):
        return False
    # Opaque high-entropy token not on an allowed prefix and not a stable key.
    if key not in ALLOWED_KEYS and re.fullmatch(r"[A-Za-z0-9+/_\-]{24,}", value):
        return False
    return True


@dataclass(frozen=True)
class TelemetryRecord:
    test_id: str
    transition: str
    clock_ts: int
    reason: str
    usage_outcome: str = ""
    refs: dict[str, Any] = field(default_factory=dict)

    def _all_fields(self) -> dict[str, Any]:
        base = {
            "test_id": self.test_id,
            "transition": self.transition,
            "clock_ts": self.clock_ts,
            "reason": self.reason,
            "usage_outcome": self.usage_outcome,
        }
        base.update(self.refs)
        return base

    def redaction_ok(self) -> bool:
        return all(
            _value_is_redaction_safe(k, v) for k, v in self._all_fields().items()
        )


class TelemetrySink:
    """Collects only redaction-passing records; drops the rest (FR-033)."""

    def __init__(self) -> None:
        self.published: list[TelemetryRecord] = []
        self.dropped: int = 0

    def publish(self, record: TelemetryRecord) -> bool:
        if not record.redaction_ok():
            self.dropped += 1
            return False
        self.published.append(record)
        return True
