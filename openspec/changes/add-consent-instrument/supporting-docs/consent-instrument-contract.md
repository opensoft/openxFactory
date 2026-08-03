# Staged: Consent Instrument Contract

Status: staged
Kind: architecture
Summary: Every domain's rung-2 relationship starts with a consent instrument — the engagement letter, the patient consent, the agency agreement — and the factory treats it as a schema'd governed object, not prose: the ROOT OF THE AUTHORITY CHAIN that credential grants cite, gates verify, adapters activate on, and whose termination cascades to revocation. All nine design questions RULED 2026-07-31; the ranked record is consent-instrument-design-decisions.md beside this doc.
Topics: consent-instrument, engagement-letter, authority-chain, party-ladder, delegation, revocation, memory-gateway, consent-profile, document-cataloging, credential-contracts
Repository context: openxFactory (neutral schema + vocabulary; proof instruments in MedxFactory and LedgerxFactory; implied-but-unmodeled instruments in AdxFactory, OpsxFactory, codexFactory)
Staging ID: openxFactory:staging:consent-instrument-contract
Source: Meds Rx, Inc onboarding (LedgerxFactory, 2026-07-24) — drafting the LedgerXCorp↔MedsRx engagement letter surfaced that the letter is the single record the whole authority chain resolves to; named by Brett Heap ("this is what allows xFactory to act for the tenant on the client").
Target capabilities: ADDED `consent-instrument` — RULED 2026-07-31: a new neutral capability with its own schema plus a DECLARED mapping to the memory-gateway consent-profile family.

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
| MedxFactory | patient consent (`hermes/patient/consent-model.yaml`) + the memory-gateway consent-profile | **second schema'd instance COMPLETE**: `add-patient-consent-instrument` authored, ratified, realized, and archived 2026-07-30 (canonical Medx spec `patient-consent-instrument`, 8 requirements) — custody-bearing `medx_patient_consent_record` (parties by rung incl. estate hosts, closed four-class instrument registry with `executed_by.authority_basis`, purposes resolving to the consent model, out-of-scope required, revocation SLA, opaque locator + sha256 custody, five-state lifecycle, fixed `hypothesis_only` autonomy, declared consent-profile derivation; real records never enter the repo) |
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

## Open questions — all resolved 2026-07-31

Rulings by Brett Heap during the D10 live session; the ranked record with
rationale and instantiation grounding is
[consent-instrument-design-decisions.md](consent-instrument-design-decisions.md).

1. Delta shape — RESOLVED (Brett, 2026-07-31): a NEW `consent-instrument`
   capability with its own schema under `contracts/schemas/`, plus a
   DECLARED mapping to the consent-profile family. The instrument
   authorizes ACTION; the profile governs DATA.
2. Signature/execution modeling — RESOLVED (Brett, 2026-07-31): the
   neutral schema carries the AUTHORITY BASIS first-class; signer and
   execution mechanics belong to domain policy, with
   distinct-signers-across-rungs a SHOULD for related-party cases.
3. Amendment lifecycle — RESOLVED (Brett, 2026-07-31): amendments are
   status transitions carrying deltas on the existing instrument, not new
   instruments referencing a parent (fits Ledgerx's "AR by amendment").
4. Broker-side check home — RESOLVED (Brett, 2026-07-31): a new standalone
   `validate-consent-instruments.py`, hostable outside
   credential-contracts (Medx constraint: no broker).
5. Instrument-class registry (surfaced 2026-07-31) — RESOLVED (Brett,
   2026-07-31): DOMAIN-OWNED closed registries under neutral constraints —
   every class declares its custody-anchor kind and execution-evidence
   kind; Medx's four medical classes and Ledgerx's
   `internal_beta_authorization` both conform as-is.
6. Lifecycle enum vs real spellings (surfaced 2026-07-31) — RESOLVED
   (Brett, 2026-07-31): the five-state enum is closed and normative;
   domain spellings map via a DECLARED alias at conformance time (Ledgerx
   `active` → `executed`); non-signature classes may enter `executed`
   directly — class-appropriate skipping, never silent.
7. Scope-coverage semantics (surfaced 2026-07-31) — RESOLVED (Brett,
   2026-07-31): the neutral executed-instrument check verifies PURPOSE
   resolution (requested purpose → record purposes → domain-declared
   purpose model, the Medx pattern); technical access shapes stay
   credential-contracts enforcement.
8. Termination/withdrawal cascade (surfaced 2026-07-31) — RESOLVED
   (Brett, 2026-07-31): cascade targets are FIRST-CLASS dependent-artifact
   references on the record (derived consent profiles, credential grants,
   adapter activations), each governed by the record's revocation SLA and
   evidence obligation; cascade mechanics stay in the owning families.
9. Real-record placement (surfaced 2026-07-31) — RESOLVED (Brett,
   2026-07-31): neutrally mandatory that the SIGNED ORIGINAL never enters
   a product repo (opaque locator + sha256 only); record-instance
   placement (repo tenant tree vs governed store) is declared domain
   policy driven by data sensitivity.

## Exit path

OpenSpec change in openxFactory (`add-consent-instrument` shape) after
one more domain instantiates. Register entry: DTN-016. The Ledgerx
`ledgerx_engagement_consent_record` is the reference instance; on
ratification it declares conformance rather than being rewritten.

**EXIT CONDITION MET (2026-07-30):** MedxFactory's
`add-patient-consent-instrument` landed — authored, ratified, realized,
and archived the same day (canonical Medx spec `patient-consent-instrument`,
8 requirements). Its design.md §Feedback records Medx positions on the four
originally listed questions, all adopted by the 2026-07-31 rulings above.
`add-consent-instrument` is ready to author against two conformant
instances: the Ledgerx engagement consent record (instrument-class registry
generalization) and the Medx patient consent record (instrument/profile
ACTION-vs-DATA split proven; stricter no-real-records-in-repo custody
posture — now a declared domain policy under ruling 9).

**RULINGS RECORDED (2026-07-31):** all nine design questions resolved
during the D10 live session; this packet is proposal-ready pending the
`propose` commission.
