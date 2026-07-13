"""Read-only acceptance sourcing with content-digest verification (FR-034a, C2).

The required scenario set is derived from TWO digest-verified acceptance maps —
never a second hand-maintained enumeration:

- runtime ARR map (role ``arr``): the reference runtime's own 34 scenarios. It is
  RUNTIME-OWNED and lives in this test tree (relocated here from the change
  supporting-docs at realization so it is not archived with the change dir).
- client ACR map (role ``acr``): the applicable kernel scenarios, sourced from the
  released kernel contract ``contracts/avatar-client/acceptance-map.yaml``
  (authoritative post-realization; the ``avatar-client-parallel-v1`` baseline map
  it superseded lived in the 001 change supporting-docs and is retired).

At realization the enumerated required-set is FROZEN into ``realization-pin.yaml``
(``required_scenarios`` + ``acceptance_source_digests``). The ``--final`` checker
sources the required-set from the pin (content-addressed) and cross-verifies the
live maps' digests and enumerated sets against it, so the required-set stays
content-addressed after the change dirs archive on landing (FR-034/FR-034a).
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import yaml

# tests/avatar_runtime/conformance/acceptance_source.py -> worktree root
ROOT = Path(__file__).resolve().parents[3]

# Runtime-owned ARR map (in this test tree, so it is NOT archived with the change
# dir). ACR is sourced from the released kernel contract (stable, non-archived).
ARR_MAP = "tests/avatar_runtime/conformance/avatar-reference-runtime-acceptance-map.yaml"
ACR_RELEASED_MAP = "contracts/avatar-client/acceptance-map.yaml"
# Retired at realization: the avatar-client-parallel-v1 baseline map lived in the
# 001 change supporting-docs; post-realization the released map is authoritative in
# both modes. Kept as an alias so any external importer still resolves.
ACR_BASELINE_MAP = ACR_RELEASED_MAP


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
    # Post-realization the released kernel map is authoritative in both modes.
    return _scenario_ids(ACR_RELEASED_MAP, root)


def required_scenarios(final: bool = False, root: Path = ROOT) -> set[str]:
    return required_arr(root) | required_acr(final=final, root=root)


def source_digests(final: bool = False, root: Path = ROOT) -> dict[str, str]:
    return {
        "arr": content_digest(ARR_MAP, root),
        "acr": content_digest(ACR_RELEASED_MAP, root),
    }


# --------------------------------------------------------------------------- #
# Pin-authoritative required-set (FR-034a: content-addressed after archive)
# --------------------------------------------------------------------------- #
def pinned_required_scenarios(pin: dict) -> set[str]:
    """The frozen required-set recorded in realization-pin.yaml. This is the
    authoritative source at ``--final`` — it does not depend on any live map, so
    it survives the change dirs archiving."""
    rs = (pin or {}).get("required_scenarios") or {}
    return set(rs.get("arr") or []) | set(rs.get("acr") or [])


def verify_sources_against_pin(pin: dict, root: Path = ROOT) -> list[str]:
    """Cross-verify the live acceptance maps against the frozen pin, returning a
    list of drift problems (fail closed). A map that is PRESENT MUST match both its
    pinned digest and its pinned enumerated set exactly. A map that is ABSENT is
    drift UNLESS ``conformance.sources_archived: true`` is explicitly set in the pin
    — deliberate archival then makes the pinned set the sole content-addressed
    source; an accidental rename or stale constant fails closed instead of silently
    disabling the cross-check."""
    problems: list[str] = []
    conf = (pin or {}).get("conformance") or {}
    rs = (pin or {}).get("required_scenarios") or {}
    dg = conf.get("acceptance_source_digests") or {}
    # A vanished pinned source silently disables its live cross-check, so absence
    # must be a DELIBERATE, auditable state — never inferred from a stale constant
    # or a moved file. Require an explicit conformance.sources_archived flag;
    # otherwise a missing pinned source is itself drift (fail closed).
    archived = bool(conf.get("sources_archived"))
    for role, path, pinned_ids in (
        ("arr", ARR_MAP, rs.get("arr")),
        ("acr", ACR_RELEASED_MAP, rs.get("acr")),
    ):
        fpath = root / path
        if not fpath.exists():
            if (dg.get(role) or pinned_ids is not None) and not archived:
                problems.append(
                    f"{role} pinned source absent at {path} but conformance.sources_archived "
                    f"is not set — the live cross-check would be silently disabled "
                    f"(stale constant or moved map?)")
            continue  # deliberate archival only: the pinned set stands (content-addressed)
        actual = content_digest(path, root)
        if dg.get(role) and dg.get(role) != actual:
            problems.append(
                f"{role} source digest drift: pin {dg.get(role)} != actual {actual} ({path})")
        if pinned_ids is not None and set(_scenario_ids(path, root)) != set(pinned_ids):
            problems.append(
                f"{role} source set drift: live map != pinned required_scenarios.{role} ({path})")
    return problems
