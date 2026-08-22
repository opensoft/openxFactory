"""The declaration perimeter: the three fields the schemas require and nothing
read, locked one rule at a time.

An adversarial review of 2026-08-21 found the same defect three times. A ruling
was carried into the SHAPE — a required field where the fact lives — and then
never read, so the ruling existed in prose and the record that contradicted it
validated:

  * `realization.authority_operated_by_family` — an operator that runs the
    authority excusing its own key material with a declared R7 shortfall;
  * `issuing_authority.operated_by_family` — OQ1's refused middle option, a
    family-operated authority stopping at the declared issuance floor;
  * `achieved_establishment_level` — a record asserting a stronger establishment
    level than the realization declares it achieves.

Plus the guard that skipped rather than refused when a timestamp was absent, and
the `key_change.changed` premise nothing verified.

These are unit-level on purpose. The packaged corpus proves each rule fires on a
single document; several of these cases need TWO records that disagree, which a
one-document fixture cannot express — so they are constructed here, against the
canonical registries, rather than left to a reviewer's memory.
"""

from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
VALIDATOR = REPO_ROOT / "scripts" / "validate-trust-anchor.py"
EXAMPLES = REPO_ROOT / "contracts" / "trust-anchor" / "examples"


def _load():
    spec = importlib.util.spec_from_file_location("validate_trust_anchor",
                                                 VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


MODULE = _load()
SCHEMAS = MODULE.load_schemas()


def _example(name: str) -> dict:
    return copy.deepcopy(MODULE.load_yaml(EXAMPLES / name))


def _context(*docs: dict) -> "MODULE.Context":
    ctx = MODULE.Context(MODULE.load_yaml(MODULE.CUSTODY_REGISTRY_PATH),
                         MODULE.load_yaml(MODULE.OPENXWALLET_REGISTRY_PATH))
    for doc in docs:
        ctx.index(doc)
    return ctx


def _codes(doc: dict, ctx, label: str = "under-test") -> set[str]:
    findings = MODULE.Findings()
    MODULE.validate_record(findings, label, doc, SCHEMAS, ctx)
    return MODULE.codes_of(findings.errors)


def _warn_codes(doc: dict, ctx, label: str = "under-test") -> set[str]:
    findings = MODULE.Findings()
    MODULE.validate_record(findings, label, doc, SCHEMAS, ctx)
    return {line.split("[", 1)[1].split("]", 1)[0]
            for line in findings.warnings}


def _entry(declaration: dict, obligation: str) -> dict:
    for entry in declaration["obligations"]:
        if entry["obligation"] == obligation:
            return entry
    raise AssertionError(f"no {obligation} entry")


# --------------------------------------------------------------- R7 perimeter

def test_a_family_operated_realization_may_not_declare_an_r7_shortfall() -> None:
    declaration = _example("conformance-declaration-self-hosted.example.yaml")
    assert declaration["realization"]["authority_operated_by_family"] is True
    _entry(declaration, "TA-R7")["satisfaction"] = "cannot"
    codes = _codes(declaration, _context(declaration))
    assert "family-operated-shortfall-claimed" in codes, codes


def test_partial_is_refused_there_too() -> None:
    # `partial` and `cannot` are both shortfalls for every other rule in this
    # family, so treating only `cannot` as one here would leave the softer word
    # as the whole bypass.
    declaration = _example("conformance-declaration-self-hosted.example.yaml")
    _entry(declaration, "TA-R7")["satisfaction"] = "partial"
    codes = _codes(declaration, _context(declaration))
    assert "family-operated-shortfall-claimed" in codes, codes


def test_a_not_operated_realization_may_declare_it() -> None:
    # The honest case, and the reason the rule is conditioned rather than blanket:
    # the family cannot produce a credential record for a key it does not hold.
    declaration = _example(
        "conformance-declaration-managed-authority.example.yaml")
    assert declaration["realization"]["authority_operated_by_family"] is False
    assert _entry(declaration, "TA-R7")["satisfaction"] == "cannot"
    assert not _codes(declaration, _context(declaration))


def test_an_anchor_citing_a_family_operated_shortfall_is_refused() -> None:
    # The citation half, ISOLATED: the entry it names really does declare the
    # shortfall (so `obligation-undeclared` cannot fire) and belongs to the same
    # realization (so the ownership rule cannot). What is left is the rule under
    # test.
    declaration = _example("conformance-declaration-self-hosted.example.yaml")
    _entry(declaration, "TA-R7")["satisfaction"] = "cannot"
    anchor = _example("anchor-core-root.example.yaml")
    anchor["anchor_id"] = "anchor:test-core-root"
    anchor["declared_chain_custody"] = {
        "custody_model": "host_held",
        "registry_id": "trust-anchor-chain-custody",
        "registry_version": 1,
        "declared_at": "2026-08-11T00:00:00Z",
        "declared_shortfall_ref": "ob:core:TA-R7",
    }
    anchor["created_at"] = "2026-08-11T00:00:00Z"
    codes = _codes(anchor, _context(declaration, anchor))
    assert "family-operated-shortfall-claimed" in codes, codes
    assert "obligation-undeclared" not in codes, codes


# ------------------------------------------------------- the lateness guard

def test_a_shortfall_citation_with_no_moment_is_refused_not_skipped() -> None:
    declaration = _example(
        "conformance-declaration-managed-authority.example.yaml")
    anchor = _example("anchor-managed-root.example.yaml")
    anchor["anchor_id"] = "anchor:test-managed-root"
    anchor["declared_chain_custody"].pop("declared_at", None)
    anchor.pop("created_at", None)
    codes = _codes(anchor, _context(declaration, anchor))
    # Refused twice: the schema now requires `declared_at` alongside a shortfall
    # reference, and the rule refuses a citation whose timeliness cannot be shown.
    assert "shortfall-claim-moment-missing" in codes, codes
    assert "schema" in codes, codes


def test_a_dated_citation_still_passes() -> None:
    declaration = _example(
        "conformance-declaration-managed-authority.example.yaml")
    anchor = _example("anchor-managed-root.example.yaml")
    assert not _codes(anchor, _context(declaration, anchor))


# ----------------------------------------------------------- OQ1's perimeter

def _floor_issuance() -> tuple[dict, dict, dict]:
    declaration = _example(
        "conformance-declaration-managed-authority.example.yaml")
    anchor = _example("anchor-managed-issuing.example.yaml")
    issuance = _example("issuance-evidence-floor-managed-broker.example.yaml")
    return declaration, anchor, issuance


def test_a_family_operated_authority_may_not_stop_at_the_floor() -> None:
    declaration, anchor, issuance = _floor_issuance()
    assert issuance["establishment_level"] == \
        "per_policy_attestation_with_authority_log"
    issuance["issuing_authority"]["operated_by_family"] = True
    codes = _codes(issuance, _context(declaration, anchor, issuance))
    assert "issuance-floor-under-a-family-operated-authority" in codes, codes


def test_the_floor_is_conformant_for_an_authority_the_family_does_not_run() -> None:
    declaration, anchor, issuance = _floor_issuance()
    assert not _codes(issuance, _context(declaration, anchor, issuance))


def test_a_record_may_not_assert_a_level_above_the_declared_achievement() -> None:
    declaration, anchor, _ = _floor_issuance()
    assert _entry(declaration, "TA-R2")["achieved_establishment_level"] == \
        "per_policy_attestation_with_authority_log"
    issuance = _example("issuance-evidence-per-certificate.example.yaml")
    issuance["issuance_evidence_id"] = "ie:test-level-above"
    issuance["realization_ref"] = "realization:managed-cloud-authority-canary"
    issuance["anchor_ref"] = "anchor:managed-issuing"
    issuance["authority"] = {
        "authority_ref": "policy:managed-device-issuance-profile",
        "authority_kind": "policy",
    }
    codes = _codes(issuance, _context(declaration, anchor, issuance))
    assert "issuance-level-above-the-declared-achievement" in codes, codes


# --------------------------------------------- the unverified `changed` premise

def _superseded_certificate() -> dict:
    certificate = _example("certificate-core-service.example.yaml")
    certificate["key_generation"] = {
        "generation_ref": "keygen:core-service-01-g2",
        "generated_at": "2026-08-01T00:00:00Z",
        "supersedes_generation_ref": "keygen:core-service-01-g1",
    }
    return certificate


def test_a_renewal_may_not_declare_away_a_key_change() -> None:
    # The renewal-side half of the rule, which no single-document fixture can
    # reach: a coherent positive corpus contains no certificate whose
    # supersession lacks an accounting renewal, so the pair has to be built.
    declaration = _example("conformance-declaration-self-hosted.example.yaml")
    anchor = _example("anchor-core-issuing.example.yaml")
    certificate = _superseded_certificate()
    renewal = _example("renewal-key-preserved.example.yaml")
    ctx = _context(declaration, anchor, certificate, renewal,
                   _example("dependent-binding-gateway.example.yaml"))
    codes = _codes(renewal, ctx)
    assert "renewal-key-change-understated" in codes, codes


def test_a_later_key_preserving_renewal_stays_conformant() -> None:
    # The escape that keeps the rule from being a false positive on the ordinary
    # history: rotate the key once, then renew again without changing it.
    declaration = _example("conformance-declaration-self-hosted.example.yaml")
    anchor = _example("anchor-core-issuing.example.yaml")
    certificate = _superseded_certificate()
    accounting = {
        "schema_version": 1,
        "kind": "xfactory_certificate_renewal_record",
        "renewal_id": "renewal:test-core-service-01-rotation",
        "certificate_ref": "cert:core-service-01",
        "anchor_ref": "anchor:core-issuing",
        "renewal_mode": "requested",
        "planning": {"planned_at": "2026-07-01T00:00:00Z",
                     "certificate_enumeration_state": "complete",
                     "outcome": "proceeded"},
        "key_change": {
            "changed": True,
            "superseded_key_generation_ref": "keygen:core-service-01-g1",
            "new_key_generation_ref": "keygen:core-service-01-g2"},
        "rebind_obligation": {"arises": True, "statement": "New key material."},
        "enumerated_dependents": ["bind:core-service-01-gateway"],
        "dependent_rebinds": [
            {"binding_ref": "bind:core-service-01-gateway",
             "rebind_evidence": {
                 "mode": "authentication_against_new_material",
                 "performed_at": "2026-07-01T01:00:00Z",
                 "result": "succeeded"}}],
        "authority_outcome": "issued",
        "completion_state": "complete",
        "reported_at": "2026-07-01T02:00:00Z",
    }
    later = _example("renewal-key-preserved.example.yaml")
    ctx = _context(declaration, anchor, certificate, accounting, later)
    assert "renewal-key-change-understated" not in _codes(later, ctx)
    assert "renewal-key-change-understated" not in _codes(certificate, ctx)


# ------------------------------------------------- the point-of-use cost (warns)

def test_a_broad_cannot_set_is_reported() -> None:
    declaration = _example(
        "conformance-declaration-managed-authority.example.yaml")
    for obligation in ("TA-R2", "TA-R5", "TA-R6"):
        _entry(declaration, obligation)["satisfaction"] = "cannot"
    warnings = _warn_codes(declaration, _context(declaration))
    assert "declaration-cannot-breadth" in warnings, warnings


def test_one_cannot_is_not_reported() -> None:
    declaration = _example(
        "conformance-declaration-managed-authority.example.yaml")
    assert not _warn_codes(declaration, _context(declaration))


def test_a_binding_requiring_a_partial_obligation_is_reported() -> None:
    # R8's wording refuses what the declaration CANNOT support, so this is a
    # warning rather than an error — and a warning is a nonzero exit under
    # `--strict`, which is how the point-of-use cost is paid.
    declaration = _example(
        "conformance-declaration-managed-authority.example.yaml")
    certificate = _example("certificate-managed-device.example.yaml")
    binding = _example("dependent-binding-device-network.example.yaml")
    binding["required_obligations"] = ["TA-R2"]
    assert _entry(declaration, "TA-R2")["satisfaction"] == "partial"
    ctx = _context(declaration, certificate, binding)
    assert "declared-partial-required" in _warn_codes(binding, ctx)
    assert not _codes(binding, ctx)
