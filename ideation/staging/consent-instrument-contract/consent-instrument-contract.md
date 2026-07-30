# Staged: Consent Instrument Contract

Status: staged
Kind: architecture
Summary: Every domain's rung-2 relationship starts with a consent
instrument — the engagement letter, the patient consent, the agency
agreement, the operating/authorization agreement — and the factory
should treat it as a schema'd governed object, not prose. It is the
ROOT OF THE AUTHORITY CHAIN: credential grants cite it, engagement/
scope gates verify it, adapters activate on it, and its termination
cascades to credential revocation and rotation. Target: a neutral
consent-instrument schema (parties by party-ladder rung including
third-party estate hosts, scope/out-of-scope, delegation clauses with
technical access shapes, autonomy position, revocation SLA, signed-
original custody by opaque locator + digest, status lifecycle) that
domain instruments instantiate, mapped to the existing memory-gateway
consent-profile contract.
Topics: consent-instrument, engagement-letter, authority-chain,
party-ladder, delegation, revocation, memory-gateway, consent-profile,
document-cataloging, credential-contracts
Repository context: openxFactory (neutral schema + vocabulary; proof
instruments in MedxFactory, LedgerxFactory — first schema'd instance —
and implied-but-unmodeled instruments in AdxFactory, OpsxFactory,
codexFactory)
Staging ID: openxFactory:staging:consent-instrument-contract
Source: Meds Rx, Inc onboarding (LedgerxFactory, 2026-07-24) — drafting
the LedgerXCorp↔MedsRx engagement letter surfaced that the letter is
the single record the whole authority chain resolves to, and that the
same is true in every domain; named by Brett Heap ("this is what
allows xFactory to act for the tenant on the client").
Target capabilities: ADDED `consent-instrument` (neutral schema +
vocabulary + guidance; or MODIFIED `memory-gateway` extending the
consent-profile family — open question below)

## Target capability

A neutral `xfactory_consent_instrument` record kind that every domain's
rung-1↔rung-2 instrument instantiates, so the authority chain's root is
machine-checkable: the broker can verify a grant's consent citation
resolves to an executed instrument covering the requested scope; the
engagement gate can verify status and effective dates; termination can
mechanically trigger the credentials `engagement_end` cascade.

## The per-domain instantiation (evidence)

| Domain | Instrument | State |
| --- | --- | --- |
| LedgerxFactory | engagement letter (firm↔client company) | **first schema'd instance**: `docs/engagement-letter-template.md` + `tenants/ledgerxcorp/clients/medsrx/consent-record.yaml` (kind `ledgerx_engagement_consent_record`, 2026-07-24) |
| MedxFactory | patient consent (`hermes/patient/consent-model.yaml`) + the memory-gateway consent-profile | **second schema'd instance COMPLETE**: `add-patient-consent-instrument` authored, ratified, realized, and archived 2026-07-30 (canonical Medx spec `patient-consent-instrument`, 8 requirements) — custody-bearing `medx_patient_consent_record` (`templates/patient-consent-record.yaml` + schema pair + fictional example: parties by rung incl. estate hosts, closed four-class instrument registry with `executed_by.authority_basis`, purposes resolving to the consent model, out-of-scope required, revocation SLA, opaque locator + sha256 custody, five-state lifecycle, fixed `hypothesis_only` autonomy, declared consent-profile derivation; real records never enter the repo) |
| AdxFactory | agency↔advertiser services agreement (advertiser sign-off machinery exists: persona `advertiser_approved`, launch approval) | implied, unmodeled as an instrument |
| OpsxFactory | client operating/authorization agreement (`opsxfactory_executed` obligations, client-infrastructure requests) | implied, unmodeled as an instrument |
| codexFactory | project/engagement authorization (intent owner, execution-lane contract) | implied, unmodeled as an instrument |

## Claims

1. **The instrument is the root of the authority chain.** In the
   realized Ledgerx stack, every authority-bearing artifact resolves to
   it: `consent_ref` on grants (broker must-verify), the
   `engagement_scope_gate`, the mailbox adapter's activation gate, and
   the `engagement_end` revoke-and-rotate cascade. No other single
   record has this property.
2. **The shape is domain-invariant.** Parties by party-ladder rung —
   including third-party **estate hosts** whose authorization a
   delegation needs (the Medxcorp pattern: the subject's estate hosted
   in a tenant owned by neither firm nor client); scope and stated
   out-of-scope; delegation clauses carrying the *technical* access
   shape (permission + constraint + read-only limits + verification
   evidence); autonomy position; revocation right with SLA; custody of
   the signed original by opaque locator + sha256 (document-cataloging
   pattern — the original never enters a product repo); status
   lifecycle (`draft → pending_signatures → executed → amended →
   terminated`).
3. **It composes with three ratified contract families rather than
   competing**: memory-gateway consent-profile (the instrument is the
   engagement-level source that data-consent profiles derive from),
   document-cataloging (signed-original custody), credential-contracts
   (grants cite it; termination drives revocation policy).
4. **Related-party engagements make it more necessary, not less** — the
   Meds Rx case: when one person controls multiple rungs, the executed
   instrument with distinct signers is what makes the conflict record
   read as disclosed-and-consented instead of implicit.

## Open questions

- Delta shape: new `consent-instrument` capability with a schema under
  `contracts/schemas/`, or a MODIFIED `memory-gateway` extending the
  consent-profile family? Leaning new schema + a declared mapping to
  consent-profile (the instrument authorizes ACTION; the profile
  governs DATA — related but not the same object).
- Signature/execution modeling: how much does the neutral schema say
  about signers (distinct-signers-across-rungs as a SHOULD for
  related-party cases?) versus leaving execution mechanics to domain
  policy?
- Amendment lifecycle: are amendments new instruments referencing the
  parent, or status transitions with deltas? (Ledgerx's "AR by
  amendment" note is the first concrete case.)
- Does the broker-side check (grant's consent citation resolves to an
  executed instrument covering the requested scope) belong in the
  neutral credential-contracts validator or a new
  `validate-consent-instruments.py`?

## Exit path

OpenSpec change in openxFactory (`add-consent-instrument` shape) after
one more domain instantiates — the natural second is AdxFactory's
agency↔advertiser agreement (its advertiser sign-off machinery already
implies it), or MedxFactory upgrading patient consent to a custody-
bearing instrument record. Register entry: DTN-016. The Ledgerx
`ledgerx_engagement_consent_record` is the reference instance; on
ratification it declares conformance rather than being rewritten.

**EXIT CONDITION MET (2026-07-30):** MedxFactory's
`add-patient-consent-instrument` landed — authored, ratified, realized,
and archived the same day (canonical Medx spec
`patient-consent-instrument`, 8 requirements) — the custody-bearing
patient consent branch of this exit path. Its design.md §Feedback
records Medx positions on all four open questions (supports the
new-schema leaning; authority-basis first-class over signer mechanics;
amendments as transitions-with-deltas; the executed-record check must
be hostable outside credential-contracts — Medx has no broker).
`add-consent-instrument` is unblocked and ready to author against two
conformant instances: the Ledgerx engagement consent record (with its
instrument-class registry generalization) and the Medx patient consent
record (with the instrument/profile ACTION-vs-DATA split proven and
the stricter no-real-records-in-repo custody posture).
