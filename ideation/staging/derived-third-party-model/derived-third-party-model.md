# Derived Third-Party Model — Staged Topic

Status: staged
Kind: architecture
Summary: Name and neutralize the pattern three domains now instantiate
independently: a governed model of a third party related to the served
subject — synthetic or real — that is non-authoritative by construction,
provenance-tagged per fact, read-only against the domain truth store,
isolated per subject, promoted into action only through a human gate, and
calibrated against actuals. Proofs: MedxFactory Dream Object /
Simulation Scenario (ratified templates), AdxFactory Persona / Campaign
Simulation (staged), LedgerxFactory Counterparty Health Profile /
Financial Scenario (staged). Registered as DTN-014.
Topics: derived-model, third-party, non-authoritative, provenance,
simulation, calibration, human-gated-promotion, dtn-014
Repository context: openxFactory (neutral template schema + invariant
vocabulary + validator rules); proof domains MedxFactory
(`templates/dream-object.yaml`, `templates/simulation-scenario.yaml`),
AdxFactory (`ideation/staging/adx-persona-simulation/`), LedgerxFactory
(`ideation/staging/ledgerx-counterparty-model/`)
Staging ID: openxFactory:staging:derived-third-party-model
Source: cross-domain modeling session with Brett Heap 2026-07-23
(AdxFactory persona/simulation design translated to LedgerxFactory;
Medx precedent recognized as the original instance).
Captured: 2026-07-23

## Target capability

Three domains have converged on the same object shape with no shared
contract: a model of someone the subject cares about but who holds no
authority in the stack — Medx models a synthetic patient (dream object),
Adx models the advertiser's customer (persona), Ledgerx models the client
company's customers and vendors (counterparty health profile). Each
domain re-derives the same invariants by hand. Target: a neutral
`derived-third-party-model` contract — template schema, invariant
vocabulary, and validator rules — that domain object templates declare
conformance to, so the safety shape is checked instead of re-invented.

## The pattern

A conforming domain declares a **model object** and usually a companion
**scenario object**, with these six neutral invariants:

1. **Non-authoritative by construction** — `authority_status` is the
   single-value enum `[non_authoritative]`; the model is never the
   domain truth.
2. **Per-fact provenance** — every trait/signal carries a provenance tag
   (evidence with source refs, or an explicitly declared assumption in a
   required assumption register); no invented facts.
3. **Read-only against the truth store** — the model and its scenarios
   can never write the domain's authoritative store (patient truth
   model, brand truth, the ledger) nor execute external actions
   (`spend_authority`/`posting_authority`-class fields are single-value
   `[none]`).
4. **Per-subject isolation** — a model derived within one subject's
   scope never informs another subject without domain-layer review that
   severs attribution (privacy + competitive/confidentiality wall).
5. **Human-gated promotion** — scenario outputs are hypotheses
   (`hypothesis_proposed | no_signal | discarded`); nothing a model
   produces becomes action, truth, or an accounting/clinical/launch
   decision except through the domain's existing human approval gate.
6. **Calibration loop** — a designated workflow (never the model or the
   scenario itself) writes predicted-vs-actual calibration records back
   onto the model; `confidence` is derived from calibration history
   only, never hand-set, and repeated misses downgrade and flag
   re-modeling.

## The four domain dials

What varies per domain is exactly four choices, which the neutral schema
should carry as declared fields, not hard-code:

| Dial | Medx | Adx | Ledgerx |
| --- | --- | --- | --- |
| Third-party identity | synthetic (dream patient) | synthetic aggregate (persona, `aggregated_only`) | real entity (counterparty; identity authoritative, assessment derived) |
| Truth store | patient truth model (Hermes memory) | brand truth (Hermes memory) | the ledger (external enforcement layer) |
| Calibration source | clinician-reviewed outcomes | performance_review workflow evidence | native truth store (close cycle actuals) |
| Promoting authority | clinician of record | human launch approver | licensed professional of record |

Real-identity third parties (the Ledgerx dial position) imply a
two-object split the schema must allow: an authoritative graph subject
for identity plus the derived model on top. Synthetic third parties
(Medx, Adx) collapse identity into the model and add an
aggregation/no-real-person invariant instead.

## Claims

1. The six invariants above are exactly the intersection of the three
   domain implementations — nothing in the list is domain-specific, and
   each domain's remaining rules map onto one of the four dials.
2. The pattern is checkable: a neutral validator can verify single-value
   enum presence (`authority_status`, truth-store access, action
   authority), assumption-register presence, calibration-writer
   separation (the model/scenario kinds never write their own
   calibration), and isolation-scope declaration — the same class of
   structural checks `validate-hermes-domain-overlay.py` already does.
3. This is a template-schema + vocabulary promotion (DTN-004-shaped),
   not a runtime: domains keep their own object templates and merely
   declare `conforms_to: derived-third-party-model` with the dial
   settings; the neutral artifact owns the invariant vocabulary and the
   validator rules.
4. Medx needs no content change to conform — its ratified templates
   already satisfy all six invariants; conformance is a declaration plus
   validation, which makes it the cheap first re-pin.

## Open questions

- Delta shape: a new capability (`derived-third-party-model`) or a
  MODIFIED `xfactory-domain-factory-model` guidance section plus a
  schema under `contracts/schemas/`? Leaning new capability with one
  schema + vocabulary doc, mirroring how workflow-gate-contract landed.
- Does the scenario object get its own conformance kind, or is it a
  profile of the same declaration? (Medx and both staged domains pair
  them 1:1, but a domain could plausibly ship a model without
  scenarios.)
- Naming: `derived_third_party_model` vs `modeled_subject_adjunct` vs
  something better — "third party" reads oddly for Medx, where the dream
  object models the subject themself. The invariant set is identical
  either way; the name should not over-fit the marketing/accounting
  cases.
- Natural-person modeling constraints (Ledgerx's fair-credit question,
  Adx's `aggregated_only`): does the neutral vocabulary carry a
  `person_modeling_constraint` dial, or is that purely domain policy?

## Exit path

One openxFactory OpenSpec change adding the capability (schema +
invariant vocabulary + validator rules), with `code_surface: openxFactory`
realization in `scripts/`; archives when at least two domains declare
conformance and validate green — Medx (declaration-only) plus whichever
of Adx/Ledgerx lands its object-model change first. Register entry:
DTN-014 in `docs/domain-neutralization-candidate-register.md`.
