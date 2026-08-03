---
code_surface: openxFactory (contracts/schemas consent-instrument record family + vocabulary, canonical validator scripts/validate-consent-instruments.py, packaged examples/negatives — contracts, examples, validators only; the Ledgerx and Medx conformance DECLARATIONS are coordination tasks in their own repos, and no runtime/broker realization rides this change)
target_release: next additive contract bundle (allocated at realization per docs/contract-versioning-policy.md)
---

# Proposal: add-consent-instrument

## Why

Every domain's rung-1↔rung-2 relationship starts with a consent
instrument — the engagement letter, the patient consent, the agency
agreement — and in the realized stacks it is already the ROOT OF THE
AUTHORITY CHAIN: credential grants cite it (`consent_ref`,
broker-must-verify), the engagement gate checks its status and effective
dates, adapters activate on it, and its termination drives the
`engagement_end` revoke-and-rotate cascade. No other single record has
that property. Yet the factory holds it as prose plus two independently
invented shapes: LedgerxFactory's `ledgerx_engagement_consent_record`
(first schema'd instance, 2026-07-24) and MedxFactory's custody-bearing
`medx_patient_consent_record` (canonical Medx spec
`patient-consent-instrument`, archived 2026-07-30) — while AdxFactory,
OpsxFactory, and codexFactory carry the same instrument implied and
unmodeled. Two conformant instantiations satisfied the staged topic's
exit condition, and all nine design questions were ruled by Brett Heap on
2026-07-31 (D10 live session). Without the neutral contract, the chain's
root stays machine-checkable in exactly two domains and un-checkable in
three, and every new domain reinvents parties, lifecycle, custody, and
cascade semantics from scratch.

## What Changes

- ADD neutral capability `consent-instrument`: an
  `xfactory_consent_instrument` record kind that every domain's
  rung-1↔rung-2 instrument instantiates — parties by party-ladder rung
  (including third-party estate hosts), scope with stated out-of-scope,
  delegation clauses carrying the technical access shape, autonomy
  position, authority basis first-class, revocation right with SLA,
  signed-original custody by opaque locator + sha256, the closed
  five-state lifecycle, first-class dependent-artifact references for the
  termination cascade, and a DECLARED mapping to the memory-gateway
  consent-profile family (the instrument authorizes ACTION; the profile
  governs DATA).
- ADD the domain instrument-class registry contract: each domain declares
  its own CLOSED class registry under neutral constraints — every class
  declares its custody-anchor kind and its execution-evidence kind
  (ruling 2). Medx's four medical classes and Ledgerx's
  `internal_beta_authorization` conform as-is.
- ADD the canonical executed-instrument check as a NEW standalone
  `scripts/validate-consent-instruments.py` (ruling 8 — hostable where no
  credential-contracts broker lives): schema conformance, lifecycle/alias
  discipline, custody rules, and PURPOSE resolution (requested purpose →
  record purposes → domain-declared purpose model); technical access
  shapes stay credential-contracts enforcement and are not re-checked
  (ruling 4).
- DECLARE conformance for the two existing instances rather than
  rewriting them (the topic's exit path): the Ledgerx engagement consent
  record (alias `active` → `executed`) and the Medx patient consent
  record (stricter custody posture as declared domain policy under
  ruling 9). The declarations land in their own repos as coordination
  tasks.
- Register the schema family in `contracts/manifest.yaml`,
  `contracts/CHANGELOG.md`, and the contracts README at the next additive
  bundle cut (registration-at-realization precedent). DTN-016 moves to
  `adopted` at ratification.

## Impact

- New capability spec: `consent-instrument` (this change's delta).
- Composes with three ratified families rather than competing:
  memory-gateway consent-profile (declared derivation mapping),
  document-cataloging (signed-original custody pattern),
  credential-contracts (grants cite the instrument; termination drives
  revocation policy). No delta to any of the three — the seams are
  citations and declared refs, not shared schemas.
- LedgerxFactory / MedxFactory: conformance declarations only; neither
  record is rewritten. AdxFactory, OpsxFactory, codexFactory: named
  candidates for later instantiation, no work in this change.
- No runtime surface: contracts, vocabulary, validator, and examples
  only.
