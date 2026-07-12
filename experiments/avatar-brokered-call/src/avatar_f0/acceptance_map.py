"""Digest-verified baseline acceptance-map ingestion (FR-018 / Clarifications Q3).

Reads the versioned kernel acceptance map, verifies the interface baseline and content
digest, and returns the concrete ``ACR-*`` IDs the interface-impact report cites. A
missing map, wrong baseline, or digest mismatch fails closed → the run is INCONCLUSIVE;
F0 never mints placeholder IDs. The kernel owner still owns variance disposition.
"""
from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass, field
from typing import List, Optional

import yaml

from . import INTERFACE_BASELINE

# The F0-relevant requirements (those with live_f0 evidence owned by this change).
F0_RELEVANT_ACR = ("ACR-003", "ACR-008", "ACR-011", "ACR-012")

# Pinned known-good digest of the kernel acceptance map (FR-018 fail-closed default).
# A run verifies the map against this digest so ACR IDs are only ever sourced from a
# DIGEST-VERIFIED map; an absent or mismatched digest maps the run to INCONCLUSIVE.
KERNEL_ACCEPTANCE_MAP_SHA256 = (
    "0b1f5742b744e686a0e3a970a5df1ddeea88a8ce0ce6fdd602f3731672f5e50e"
)


class AcceptanceMapError(Exception):
    """Fail-closed error; ``reason`` maps the run to INCONCLUSIVE."""

    def __init__(self, reason: str, detail: str = "") -> None:
        super().__init__(f"{reason}: {detail}" if detail else reason)
        self.reason = reason


@dataclass(frozen=True)
class AcceptanceMapRef:
    source_path: str
    content_sha256: str
    interface_baseline: str
    known_acr_ids: List[str] = field(default_factory=list)
    source_commit: Optional[str] = None

    def f0_relevant(self) -> List[str]:
        return [a for a in F0_RELEVANT_ACR if a in self.known_acr_ids]


def load_acceptance_map(
    path: str,
    expected_sha256: str = "",
    source_commit: Optional[str] = None,
) -> AcceptanceMapRef:
    if not os.path.isfile(path):
        raise AcceptanceMapError("acceptance_map_absent", path)
    # Fail closed: without a pinned expected digest the map is UNVERIFIED and must never
    # be silently accepted (FR-018: absent/mismatched digest ⇒ INCONCLUSIVE).
    if not expected_sha256:
        raise AcceptanceMapError("acceptance_map_expected_digest_absent", path)
    raw = open(path, "rb").read()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != expected_sha256:
        raise AcceptanceMapError("acceptance_map_digest_mismatch", digest)
    try:
        doc = yaml.safe_load(raw)
    except yaml.YAMLError as exc:  # pragma: no cover - defensive
        raise AcceptanceMapError("acceptance_map_unparseable", str(exc)[:80])
    baseline = (doc or {}).get("interface_baseline")
    if baseline != INTERFACE_BASELINE:
        raise AcceptanceMapError("acceptance_map_baseline_mismatch", str(baseline))
    ids = [r.get("id") for r in (doc.get("requirements") or []) if isinstance(r, dict) and r.get("id")]
    acr = [i for i in ids if isinstance(i, str) and i.startswith("ACR-")]
    return AcceptanceMapRef(
        source_path=path,
        content_sha256=digest,
        interface_baseline=baseline,
        known_acr_ids=acr,
        source_commit=source_commit,
    )
