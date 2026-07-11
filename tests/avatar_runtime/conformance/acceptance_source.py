"""Read-only acceptance sourcing with content-digest verification (FR-034a, C2).

The required scenario set is derived from TWO digest-verified acceptance maps —
never a second hand-maintained enumeration:

- runtime ARR map (role ``arr``): the reference runtime's own 34 scenarios.
- client ACR map (role ``acr``): the applicable kernel scenarios. During
  parallel work this is the ``avatar-client-parallel-v1`` baseline; at
  realization it switches to the digest-pinned released map.

Both maps are sibling-owned and consumed read-only. Each map's content digest is
recorded in ``realization-pin.yaml`` so the required-set source stays
content-addressed after the change dirs archive on landing.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import yaml

# tests/avatar_runtime/conformance/acceptance_source.py -> worktree root
ROOT = Path(__file__).resolve().parents[3]

ARR_MAP = "openspec/changes/implement-avatar-reference-runtime/supporting-docs/avatar-reference-runtime-acceptance-map.yaml"
ACR_BASELINE_MAP = "openspec/changes/define-avatar-client-contract-kernel/supporting-docs/avatar-client-acceptance-map.yaml"
ACR_RELEASED_MAP = "contracts/avatar-client/acceptance-map.yaml"


def content_digest(rel_path: str, root: Path = ROOT) -> str:
    data = (root / rel_path).read_bytes()
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _scenario_ids(rel_path: str, root: Path = ROOT) -> set[str]:
    doc = yaml.safe_load((root / rel_path).read_text())
    return {
        s["id"]
        for req in doc.get("requirements", [])
        for s in req.get("scenarios", [])
    }


def required_arr(root: Path = ROOT) -> set[str]:
    return _scenario_ids(ARR_MAP, root)


def required_acr(final: bool = False, root: Path = ROOT) -> set[str]:
    return _scenario_ids(ACR_RELEASED_MAP if final else ACR_BASELINE_MAP, root)


def required_scenarios(final: bool = False, root: Path = ROOT) -> set[str]:
    return required_arr(root) | required_acr(final=final, root=root)


def source_digests(final: bool = False, root: Path = ROOT) -> dict[str, str]:
    acr_path = ACR_RELEASED_MAP if final else ACR_BASELINE_MAP
    return {
        "arr": content_digest(ARR_MAP, root),
        "acr": content_digest(acr_path, root),
    }
