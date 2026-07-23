# Governed Derived Model — Staged Topic

Status: draft
Proposed by: add-governed-derived-model
Kind: architecture
Summary: Name and neutralize the pattern three domains instantiate
independently: a governed model derived from evidence — of a synthetic
case, a subject, or a party the subject transacts with — that can never
be mistaken for truth or act on the world. Five verified shared
invariants, two conformance tiers (`governed`, `calibrated`), six
declared dials. Proofs: MedxFactory Dream Object / Simulation Scenario
(ratified templates, line-verified 2026-07-23), AdxFactory Persona /
Campaign Simulation (staged), LedgerxFactory Counterparty Health
Profile / Financial Scenario (staged). Registered as DTN-014. Formerly
titled "Derived Third-Party Model"; renamed because the Medx dream
object models a synthetic case at domain scope and the simulation
scenario models the subject — "third party" over-fit the marketing and
accounting instances.
Topics: derived-model, governed-model, non-authoritative, provenance,
conformance-tiers, calibration, human-gated-promotion, person-modeling,
dtn-014
Repository context: openxFactory (neutral conformance schema + invariant
vocabulary + validator rules); proof domains MedxFactory
(`templates/dream-object.yaml`, `templates/simulation-scenario.yaml`),
AdxFactory (`ideation/staging/adx-persona-simulation/`), LedgerxFactory
(`ideation/staging/ledgerx-counterparty-model/`)
Staging ID: openxFactory:staging:governed-derived-model
Source: cross-domain modeling session with Brett Heap 2026-07-23
(AdxFactory persona/simulation design translated to LedgerxFactory;
Medx precedent recognized as the original instance; invariant set
corrected against the ratified Medx templates the same day).
Captured: 2026-07-23

## Target capability

Three domains converged on the same object shape with no shared
contract, each re-deriving the safety rules by hand. Target: a neutral
`governed-derived-model` capability — a conformance declaration
(`conforms_to: governed-derived-model`), an invariant vocabulary, and
validator rules — so the safety shape is checked instead of re-invented.
Domains keep their own object templates; the neutral artifact owns the
vocabulary and the checks.

## Decisions recorded 2026-07-23

1. **Name: `governed-derived-model`.** What is common to all three
   domains is a model *derived* from evidence and *governed* so it can
   never be mistaken for truth or act on the world; "third party"
   misdescribes the Medx instances. Declaration field
   `conforms_to: governed-derived-model`, conformance kind
   `xfactory_derived_model_conformance`.
2. **Delta shape: new ADDED capability.** One conformance schema under
   `contracts/schemas/`, a vocabulary/guidance doc, and validator rules
   realized in `scripts/` (`code_surface: openxFactory`) — the
   DTN-001/002 precedent. A guidance-only delta could not carry the
   validator, and the validator is most of the value.
3. **One declaration per model family, two member roles.** A domain
   declares a family whose members carry `role: model | scenario`;
   scenario members are optional (Ledgerx's profile is useful standalone)
   but when present must satisfy the scenario invariants (immutable
   truth-snapshot binding where the truth store supports it,
   hypothesis-only output enum, zero action authority).
4. **Two conformance tiers** (memory-gateway M0–M4 precedent):
   `governed` = invariants 1–5 below; `calibrated` = adds the
   calibration loop. Calibration is NOT in the verified intersection —
   the Medx templates carry no calibration or confidence machinery —
   so it is a tier, not an invariant.
5. **Scope is a dial, not an invariant.** The Medx dream object is
   domain-scoped (`owner_layer: medx_domain_hermes`, synthetic cases
   tracing to Root Truth DB records); Adx/Ledgerx models are
   subject-scoped. The invariant underneath is scope-neutral: data never
   crosses the model's declared scope without governed review — Medx
   enforces it inbound (`invented_patient_facts: [none]`, bounded
   patient projections), Adx/Ledgerx outbound (no cross-advertiser /
   cross-client leakage).
6. **`person_modeling` is a required neutral declaration; its policy
   content stays domain.** Enum `synthetic_only | aggregated_only |
   identified_organizations_only | identified_persons_under_policy`,
   the last requiring a domain policy reference whose presence the
   validator checks. The three proofs fill three different slots
   (Medx synthetic_only, Adx aggregated_only, Ledgerx
   identified_organizations_only), which is the evidence this is a real
   dial.
7. **Promotion-by-new-object is the neutral rule.** Adopted verbatim
   from the ratified dream-object note: promotion happens by creating a
   new object of a different kind through review, never by mutating the
   derived object; `authority_status` is immutable. Review/sign-off
   status fields (Adx `approval_status`, Ledgerx `professional_review`)
   may mutate — they track review, not authority. `generation_seed`
   reproducibility joins as a SHOULD (Medx requires it; LLM-driven
   scenario runs cannot honestly claim seed-reproducibility).

## The five invariants (`governed` tier)

Line-verified 2026-07-23 as the exact intersection of the Medx ratified
templates and the Adx/Ledgerx staged drafts:

1. **Non-authoritative by construction** — `authority_status` is the
   single-value enum `[non_authoritative]` and is immutable; promotion
   only by new-object-through-review (decision 7).
2. **Full provenance** — every fact is evidence-traced or a declared
   assumption in a required assumption register; a domain may forbid
   assumptions entirely (the Medx dream object is the strictest case:
   `source_trace` min 1 + `invented_patient_facts: [none]`).
3. **Read-only truth store, zero action authority** — the model and its
   scenarios never write the domain's authoritative store (patient truth
   model, brand truth, the ledger) and carry single-value `[none]` /
   `[read_only]` fields for action-class authority (orders, spend,
   posting); scenarios bind to an immutable snapshot where the truth
   store supports snapshots.
4. **Declared scope, no cross-scope data without review** — the family
   declares `scope: domain | subject`; data crossing that scope in
   either direction requires governed review (inbound: no unprovenanced
   subject facts enter a domain-scoped model; outbound: no
   subject-scoped intelligence leaks to another subject).
5. **Human-gated promotion** — scenario outputs are hypotheses only
   (`hypothesis_proposed | no_signal | discarded`; no enum value
   representing a diagnosis, an order, a launch, or a posting exists by
   design); the promoting authority is a declared human role.

### `calibrated` tier adds

A designated calibration-writer workflow (never the model or scenario
itself) records predicted-vs-actual; `confidence` is derived from
calibration history only, never hand-set; repeated misses downgrade
confidence and flag re-modeling.

## The six dials

| Dial | Medx | Adx | Ledgerx |
| --- | --- | --- | --- |
| Identity | synthetic (dream case) | synthetic aggregate (persona) | real entity (two-object split: authoritative counterparty subject + derived assessment) |
| Model scope | domain | subject | subject |
| Truth store | patient truth model (Hermes memory) | brand truth (Hermes memory) | the ledger (external enforcement layer) |
| Conformance tier / calibration source | `governed` (none declared) | `calibrated` via performance_review | `calibrated` via close cycle |
| Promoting authority | clinician of record | human launch approver | licensed professional of record |
| person_modeling | synthetic_only | aggregated_only | identified_organizations_only |

Real-identity families (the Ledgerx dial position) imply the two-object
split the schema must allow: an authoritative graph subject for identity
plus the derived model on top. Synthetic families collapse identity into
the model and declare a `synthetic_only`/`aggregated_only`
person-modeling constraint instead.

## Claims

1. The five invariants above are the verified intersection of the three
   domain implementations (Medx line-verified against ratified
   templates; earlier drafts of this topic claimed six — calibration —
   which Medx disproved).
2. The pattern is checkable: the validator verifies single-value enum
   presence and immutability declarations (`authority_status`,
   truth-store access, action-authority fields), provenance shape and
   assumption-register presence, scope + person_modeling declarations
   (with policy ref where required), hypothesis-only output enums on
   scenario members, and — for `calibrated` — writer separation (the
   model/scenario kinds never write their own calibration). Same class
   of structural checks as `validate-hermes-domain-overlay.py`.
3. This is a conformance promotion, not a runtime: domains keep their
   templates and declare `conforms_to` with tier and dials; the neutral
   artifact owns vocabulary and checks (DTN-004-shaped).
4. Medx conforms at `governed` tier declaration-only — verified, no
   content change needed — making it the cheap first re-pin. Adx and
   Ledgerx declare `calibrated` when their object-model changes land.

## Open questions (realization-phase)

- Declaration home: a `derived_models:` block in the domain's
  `stack.yaml` (mirroring the `memory_gateway` block) or a standalone
  `models/derived-model-conformance.yaml` wired from the stack's
  `models:` map? Leaning stack.yaml block.
- Validator host: extend `validate-domain-factory.py` or a new
  `scripts/validate-derived-models.py` under the same never-copy
  consumption rule? Leaning new script (single-purpose, like
  `validate-memory-gateway.py`).
- `generation_seed` SHOULD semantics for LLM-driven scenario runs:
  what does reproducibility honestly mean there (seeded panel
  composition + pinned prompts rather than bit-identical output)?
  Carried to realization.

## Exit path

Raise `add-governed-derived-model` in openxFactory from this topic's
`openspec/` drafts (`code_surface: openxFactory`; schema + vocabulary
doc + validator + capability spec). Archives when at least two domains
declare conformance and validate green at `governed` or above — Medx
(declaration-only) plus the first of Adx/Ledgerx to land its
object-model change, which also proves the `calibrated` tier. Register
entry: DTN-014.
