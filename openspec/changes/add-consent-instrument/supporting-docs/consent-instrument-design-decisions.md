# Consent Instrument — Design Decisions

Status: staged
Kind: architecture
Summary: Ranked record of the nine consent-instrument design rulings (Brett Heap, 2026-07-31, D10 live session): each question, its ruling, its rationale, and its grounding in the Ledgerx and Medx instantiations — the decision log for the authority chain's root object.
Topics: consent-instrument, authority-chain, party-ladder, credential-contracts, delegation, consent-profile
Repository context: openxFactory
Captured: 2026-07-31
Source: staging workbench scope: staged consent-instrument-contract · keyword-lens recipe: checked none · pinned none · at source_revision d09d5820de5b63b9528f6baea884a6dccde9b158

All nine rulings were made by Brett Heap on 2026-07-31 during the D10
combined acceptance session, grounded in the two conformant instantiations:
the Ledgerx engagement consent record
(`tenants/ledgerxcorp/clients/medsrx/consent-record.yaml`, first schema'd
instance) and the archived MedxFactory `add-patient-consent-instrument`
(canonical Medx spec `patient-consent-instrument`, 2026-07-30). Questions
1–4 were the packet's original open questions; 5–9 were surfaced during the
session by comparing the packet against what both instantiations actually
needed. Companion doc:
[consent-instrument-contract.md](consent-instrument-contract.md).

## The rulings, ranked by architectural weight

### 1. Delta shape — NEW capability + declared mapping

A new neutral `consent-instrument` capability with its own schema under
`contracts/schemas/`, plus a DECLARED mapping to the memory-gateway
consent-profile family. Rationale: the instrument authorizes ACTION; the
profile governs DATA — related but not the same object. Grounding: the
packet's own leaning, adopted by Medx's §Feedback; Medx proved the
ACTION-vs-DATA split with its derived-profile requirement.

### 2. Instrument-class registry — domain-owned under neutral constraints

Each domain declares its own CLOSED class registry; the neutral schema
constrains what every class must declare — its custody-anchor kind and its
execution-evidence kind. Rationale: Medx closed four medical classes
(`signed_consent_form`, `portal_acceptance`, `documented_verbal_consent`,
`court_order`) while Ledgerx legitimately invented
`internal_beta_authorization` mid-engagement; a neutral class vocabulary
would have refused one of them. Both conform as-is under this ruling.

### 3. Lifecycle — closed neutral enum + declared aliases

The five-state enum (`draft → pending_signatures → executed → amended →
terminated`) is closed and normative. Domain spellings map via a DECLARED
alias at conformance time (Ledgerx `active` → `executed`); non-signature
classes (e.g. portal acceptance) may enter `executed` directly —
class-appropriate skipping, never silent. Grounding: the real Ledgerx
record's `status: active` is outside the enum; Medx's `portal_acceptance`
has no signatures phase.

### 4. Scope-coverage semantics — purpose-level check; shapes stay technical

The neutral executed-instrument check verifies PURPOSE resolution: the
requested purpose resolves into the record's purposes, which resolve into a
domain-declared purpose model (the Medx pattern). Technical access shapes
on delegation clauses remain credential-contracts enforcement and are not
re-checked by the consent validator. Rationale: one enforcement truth per
concern; no duplicated shape-checking.

### 5. Termination/withdrawal cascade — first-class dependent refs

The record carries declared dependent-artifact references (derived consent
profiles, credential grants, adapter activations), each governed by the
record's revocation SLA and evidence obligation; cascade mechanics stay in
the owning families. Grounding: Medx cascades to the derived profile with
SLA-governed timing; Ledgerx cascades to credential revocation within one
business day with evidence — both are instances of one declared-refs shape.

### 6. Signature/execution modeling — authority-basis first-class

The neutral schema carries the AUTHORITY BASIS first-class (the Medx enum
precedent: `direct`, `guardian`, `delegated`, `court_ordered`); signer and
execution mechanics belong to domain policy, with
distinct-signers-across-rungs a SHOULD for related-party cases (the Meds Rx
disclosed-and-consented pattern).

### 7. Amendment lifecycle — transitions with deltas

Amendments are status transitions carrying deltas on the existing
instrument, never new instruments referencing a parent. Grounding: Medx's
recorded position; fits Ledgerx's "AR by amendment" first concrete case;
keeps the citation target stable across amendments.

### 8. Executed-instrument check home — new standalone validator

A new `validate-consent-instruments.py`, hostable outside
credential-contracts. Grounding: the Medx constraint — it has no broker, so
the check must run where no credential-contracts validator lives.

### 9. Real-record placement — originals out; instance placement is domain policy

Neutrally mandatory: the SIGNED ORIGINAL never enters a product repo
(opaque locator + sha256 only — both instantiations already agree). Where
the record INSTANCE lives (repo tenant tree vs governed store) is declared
domain policy driven by data sensitivity: Medx (PHI-adjacent) mandates the
governed store; Ledgerx (corporate) keeps its tenant tree.

## Possible feats

- `add-consent-instrument` (openxFactory) — the OpenSpec change these nine
  rulings make authorable: neutral schema + vocabulary + conformance
  declarations for the two existing instances. RESOLVED as the packet's
  exit path; the propose commission is the D10 session's Step E.
