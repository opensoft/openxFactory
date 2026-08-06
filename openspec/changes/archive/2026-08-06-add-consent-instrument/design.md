# Design: add-consent-instrument

All nine design questions were ruled by Brett Heap on 2026-07-31 during
the D10 combined acceptance session, grounded in the two conformant
instantiations: the Ledgerx engagement consent record
(`tenants/ledgerxcorp/clients/medsrx/consent-record.yaml`) and the
archived MedxFactory `add-patient-consent-instrument` (canonical Medx
spec `patient-consent-instrument`, 2026-07-30). The ranked decision
record with full rationale is `supporting-docs/`
`consent-instrument-design-decisions.md`; this file carries the rulings
as design decisions D1–D9. This change carries no parked decision.

## D1. Delta shape — NEW capability + declared mapping

A new neutral `consent-instrument` capability with its own schema under
`contracts/schemas/`, plus a DECLARED mapping to the memory-gateway
consent-profile family. The instrument authorizes ACTION; the profile
governs DATA — related but not the same object. Medx proved the split
with its derived-profile requirement.

## D2. Instrument-class registry — domain-owned under neutral constraints

Each domain declares its own CLOSED class registry; the neutral schema
constrains what every class must declare — its custody-anchor kind and
its execution-evidence kind. A neutral class vocabulary would have
refused either Medx's four medical classes or Ledgerx's mid-engagement
`internal_beta_authorization`; under this ruling both conform as-is.

## D3. Lifecycle — closed neutral enum + declared aliases

The five-state enum (`draft → pending_signatures → executed → amended →
terminated`) is closed and normative. Domain spellings map via a DECLARED
alias at conformance time (Ledgerx `active` → `executed`); non-signature
classes (e.g. portal acceptance) may enter `executed` directly —
class-appropriate skipping, never silent.

## D4. Scope-coverage semantics — purpose-level check; shapes stay technical

The neutral executed-instrument check verifies PURPOSE resolution: the
requested purpose resolves into the record's purposes, which resolve into
a domain-declared purpose model (the Medx pattern). Technical access
shapes on delegation clauses remain credential-contracts enforcement and
are not re-checked by the consent validator. One enforcement truth per
concern.

## D5. Termination/withdrawal cascade — first-class dependent refs

The record carries declared dependent-artifact references (derived
consent profiles, credential grants, adapter activations), each governed
by the record's revocation SLA and evidence obligation; cascade MECHANICS
stay in the owning families. Medx cascades to the derived profile with
SLA-governed timing; Ledgerx cascades to credential revocation within one
business day with evidence — both are instances of one declared-refs
shape.

## D6. Signature/execution modeling — authority basis first-class

The neutral schema carries the AUTHORITY BASIS first-class (the Medx enum
precedent: `direct`, `guardian`, `delegated`, `court_ordered`); signer
and execution mechanics belong to domain policy, with
distinct-signers-across-rungs a SHOULD for related-party cases (the Meds
Rx disclosed-and-consented pattern).

## D7. Amendment lifecycle — transitions with deltas

Amendments are status transitions carrying deltas on the existing
instrument, never new instruments referencing a parent. Fits Medx's
recorded position and Ledgerx's "AR by amendment" first concrete case,
and keeps the citation target stable across amendments — load-bearing
because grants cite the instrument.

## D8. Executed-instrument check home — new standalone validator

A new `scripts/validate-consent-instruments.py`, hostable outside
credential-contracts. The Medx constraint decides this: Medx has no
broker, so the check must run where no credential-contracts validator
lives.

## D9. Real-record placement — originals out; instance placement is domain policy

Neutrally mandatory: the SIGNED ORIGINAL never enters a product repo
(opaque locator + sha256 only — both instantiations already agree). Where
the record INSTANCE lives (repo tenant tree vs governed store) is
declared domain policy driven by data sensitivity: Medx (PHI-adjacent)
mandates the governed store; Ledgerx (corporate) keeps its tenant tree.
