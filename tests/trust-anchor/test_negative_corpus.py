"""Every negative fixture fires the finding it is named for, one at a time.

The validator's own self-test already does this — and reports it as a single
green bar. This suite adjudicates each fixture INDEPENDENTLY and names it in the
failure, so a regression says WHICH probe stopped proving its rule instead of
saying that something in the corpus is unhappy. It also asserts the two coverage
closures the validator enforces (every requirement carries a probe; every
requirement a fixture claims exists), because those are what make the corpus a
negative confirmation per requirement rather than a pile of negatives.

The adjudication mirrors `self_test`'s exactly, including the two details that
are easy to get wrong and that make a fixture prove nothing:

  * a registry FIXTURE is adjudicated in a context built from ITSELF, or a probe
    against the enumeration would be checked against the canonical registry it is
    deliberately not; and
  * the CANONICAL registry's identity is carried across regardless, or the
    duplicate-registry-id rule reads the fixture as canonical and never fires.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
VALIDATOR = REPO_ROOT / "scripts" / "validate-trust-anchor.py"


def _load():
    spec = importlib.util.spec_from_file_location("validate_trust_anchor",
                                                 VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


MODULE = _load()


def _packaged_context():
    ctx = MODULE.Context(MODULE.load_yaml(MODULE.CUSTODY_REGISTRY_PATH),
                         MODULE.load_yaml(MODULE.OPENXWALLET_REGISTRY_PATH))
    for path in MODULE.positive_paths():
        doc = MODULE.load_yaml(path)
        if isinstance(doc, dict):
            ctx.index(doc)
    return ctx


def _adjudicate(path: Path):
    """(findings, doc) for one fixture, in the packaged corpus's context."""
    ctx = _packaged_context()
    canonical = ctx.canonical_registry
    local = MODULE.Context(ctx.registry, {}, canonical)
    local.openxwallet = dict(ctx.openxwallet)
    local.copy_index_from(ctx)
    doc = MODULE.load_yaml(path)
    if isinstance(doc, dict):
        local.index(doc)
    if isinstance(doc, dict) and doc.get("kind") == \
            "xfactory_trust_anchor_chain_custody_registry":
        local = MODULE.Context(doc, {}, canonical)
        local.openxwallet = dict(ctx.openxwallet)
        local.copy_index_from(ctx)
    findings = MODULE.Findings()
    MODULE.validate_record(findings, f"negative/{path.name}", doc,
                           MODULE.load_schemas(), local)
    return findings


NEGATIVES = MODULE.negative_paths()


def test_there_are_negatives_to_adjudicate() -> None:
    # Without this, every parametrized test below would vacuously pass on an
    # empty parameter list — the same fail-open the validator's
    # `examples-missing` finding exists to refuse.
    assert len(NEGATIVES) >= 65


@pytest.mark.parametrize("path", NEGATIVES, ids=lambda p: p.name)
def test_negative_fires_its_expected_failure(path: Path) -> None:
    code, detail, requirement = MODULE.expected_failure(path)
    findings = _adjudicate(path)
    assert findings.errors, (
        f"{path.name}: expected invalid, validated cleanly — the probe proves "
        f"nothing")
    codes = MODULE.codes_of(findings.errors)
    assert code in codes, f"{path.name}: expected {code!r}, got {sorted(codes)}"
    if detail:
        lines = MODULE.lines_for(findings.errors, code)
        assert any(detail in line for line in lines), (
            f"{path.name}: {code!r} fired but not for {detail!r} — the fixture "
            f"no longer tests the invariant it is named for: {lines}")
    assert requirement in MODULE.REQUIREMENTS, (
        f"{path.name}: claims requirement {requirement!r}")


def test_every_requirement_carries_a_negative_confirmation() -> None:
    covered = {MODULE.expected_failure(p)[2] for p in NEGATIVES}
    missing = sorted(set(MODULE.REQUIREMENTS) - covered)
    assert not missing, f"requirements with no probe: {missing}"


def test_positive_examples_are_valid_together() -> None:
    # The other direction, and the one that catches a rule tightened too far: the
    # positives form ONE coherent corpus, so every cross-record rule is exercised
    # by records that agree with each other.
    ctx = _packaged_context()
    docs = MODULE.load_schemas()
    findings = MODULE.Findings()
    MODULE.validate_record(findings, "registry", ctx.registry, docs, ctx)
    for path in MODULE.positive_paths():
        MODULE.validate_record(findings, path.name, MODULE.load_yaml(path),
                               docs, ctx)
    assert not findings.errors, findings.errors
    assert not findings.warnings, findings.warnings
