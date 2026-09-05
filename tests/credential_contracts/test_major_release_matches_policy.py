"""MAJOR_RELEASE, cross-checked against the policy entries it is derived from
(openxFactory#634).

`scripts/validate-credential-contracts.py` no longer PINS `MAJOR_RELEASE` as a
literal string; it DERIVES "one major past the bundle currently cut" from
`contracts/manifest.yaml`'s `contract_bundle_version`. That derivation matches
`docs/contract-versioning-policy.md` § Deprecations Currently In Force only
because that section's own restatement rule has, every time a spent target
arrived unexecuted, moved it forward by exactly one major — a GOVERNANCE
pattern this code cannot prove of itself, only rely on. So this file reads the
section's own text for the two entries this validator's messages depend on —
the consumer block's eight SHAPE codes, and the requirement-ref
resolution-integrity pair, which the policy states SHARE one deprecation
window — and asserts the derived constant still names what the policy names.
A restatement that breaks the "next major" pattern, or that splits the two
entries onto different targets, fails here rather than shipping a validator
whose messages silently name the wrong release again.
"""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "docs" / "contract-versioning-policy.md"


def _validator_module():
    spec = importlib.util.spec_from_file_location(
        "credential_contracts_validator_major_release",
        ROOT / "scripts" / "validate-credential-contracts.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


V = _validator_module()


def _policy_text() -> str:
    return POLICY.read_text()


def _consumer_block_target(text: str) -> str:
    found = re.search(
        r"is DECLARED at contract-v2\.4 and CONSTRAINED at (contract-v\d+\.\d+)", text)
    assert found, "policy entry for the consumer block's DECLARED/CONSTRAINED pair not found"
    return found.group(1)


def _resolution_integrity_target(text: str) -> str:
    # The bullet is named by its opening phrase; everything after it, up to
    # the next bullet or section, is this entry's own text.
    marker = "A `requirement_ref` that RESOLVES TO NOTHING"
    assert text.count(marker) == 1, f"expected exactly one {marker!r} bullet"
    section = text.split(marker, 1)[1]
    found = re.search(r"removal target RESTATED to (contract-v\d+\.\d+)", section)
    assert found, "resolution-integrity entry's restated removal target not found"
    return found.group(1)


def test_the_consumer_block_entry_names_the_same_release_the_validator_derives():
    """§ Deprecations Currently In Force names the release the eight
    `consumer-*` shape codes' messages promise a refusal at; MAJOR_RELEASE
    must name the same one."""
    assert _consumer_block_target(_policy_text()) == V.MAJOR_RELEASE


def test_the_resolution_integrity_entry_names_the_same_release_the_validator_derives():
    """`requirement-ref-unresolved` and `requirement-ref-ambiguous` are the
    second family this validator emits, and the policy restates their target
    independently of the consumer block's; MAJOR_RELEASE must still agree."""
    assert _resolution_integrity_target(_policy_text()) == V.MAJOR_RELEASE


def test_both_policy_entries_still_name_the_same_target_as_each_other():
    """Independent of the validator: the policy's own claim that the two
    entries 'share ONE deprecation window and ONE major'. A restatement that
    splits them would leave MAJOR_RELEASE unable to name both correctly at
    once, which this pins as its own failure rather than a hidden one."""
    text = _policy_text()
    assert _consumer_block_target(text) == _resolution_integrity_target(text)
