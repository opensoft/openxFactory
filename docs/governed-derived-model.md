# Governed Derived Model

Status: draft
Proposed by: add-governed-derived-model
Kind: contract

The invariant vocabulary and conformance guidance for the
`governed-derived-model` capability (DTN-014): a governed model derived
from evidence — of a synthetic case, a subject, or a party the subject
transacts with — that can never be mistaken for truth or act on the
world. Domains keep their own object templates and declare conformance;
this document owns the vocabulary, the canonical schema is
`contracts/schemas/xfactory-derived-model-conformance.schema.yaml`, and
the canonical validator is `scripts/validate-derived-models.py` (run
from the pinned openxFactory checkout, never copied).

Proof instantiations: MedxFactory Dream Object / Simulation Scenario
(ratified templates), AdxFactory Persona / Campaign Simulation (staged),
LedgerxFactory Counterparty Health Profile / Financial Scenario
(staged).

## The model family

A domain declares one **family** per governed derived model: a `model`
member (the derived object) and optionally a `scenario` member (the
object that exercises the model — a simulation, stress test, or panel
run). One declaration document per domain at the convention path
`models/derived-model-conformance.yaml` lists all families.

## The five invariants (`governed` tier)

1. **Non-authoritative by construction.** The model's
   `authority_status` is the single-value enum `[non_authoritative]`
   and is immutable. Promotion happens by creating a new object of a
   different kind through the domain's review workflow, never by
   mutating the derived object. Review/sign-off status fields may
   mutate — they track review, not authority.
2. **Full provenance.** Every fact is evidence-traced or a declared
   assumption in a required assumption register. A domain may instead
   forbid assumptions entirely (the strictest form): a required
   evidence-trace field (min 1) plus a single-value invented-facts
   `[none]` enum.
3. **Read-only truth store, zero action authority.** The model and its
   scenarios never write the domain's authoritative store (patient
   truth model, brand truth, the ledger) and can never act externally
   (orders, spend, posting). Templates encode this as single-value
   field locks (`[read_only]` / `[none]`) or as declared gates —
   both bind in the conformance declaration.
4. **Declared scope, no cross-scope data without review.** A family is
   `scope: domain` (e.g. synthetic library cases) or `scope: subject`
   (per-subject models with a declared `per_*` isolation boundary).
   Data crossing the scope in either direction requires governed
   review: no unprovenanced subject facts enter a domain-scoped model;
   no subject-scoped intelligence leaks to another subject.
5. **Human-gated promotion.** Scenario outputs are hypotheses only —
   the output enum is exactly
   `hypothesis_proposed | no_signal | discarded`, with no value
   representing a diagnosis, order, launch, or posting. The family
   names a human promoting authority.

## The `calibrated` tier

Adds the calibration loop: a **designated calibration-writer workflow**
(never the model or scenario itself) records predicted-vs-actual;
`confidence` is derived from calibration history only, never hand-set;
repeated refuted calibrations downgrade confidence and flag
re-modeling. Domains whose truth store natively records outcomes (e.g.
a ledger at close) get calibration nearly free; others designate an
evidence-producing workflow (e.g. a performance review).

## The six dials

| Dial | Values | Notes |
| --- | --- | --- |
| `identity` | `synthetic` \| `synthetic_aggregate` \| `real_entity` | `real_entity` requires the two-object split: an authoritative graph subject (`identity_subject_kind`, never a family member) carries identity; the derived model carries only assessment. |
| `scope` | `domain` \| `subject` | `subject` requires `isolation_boundary` (`per_*`) consistent with the stack's tenancy isolation. |
| `truth_store` / `truth_store_class` | free name + `hermes_memory` \| `external_enforcement` | What the model may never write. |
| `calibration_writer` / `calibration_source` | workflow id + source name | Required at `calibrated` tier; writer separation enforced. |
| `promoting_authority` | human role | Clinician of record, launch approver, licensed professional… |
| `person_modeling` | `synthetic_only` \| `aggregated_only` \| `identified_organizations_only` \| `identified_persons_under_policy` | The last requires `person_modeling_policy` — a domain policy document the validator checks for existence. Policy content stays domain-owned. |

Reference dial settings: Medx `synthetic`/`domain`/`hermes_memory`
/`governed`/`clinician_of_record`/`synthetic_only`; Adx
`synthetic_aggregate`/`subject` (`per_advertiser`)/`hermes_memory`
/`calibrated` (performance review)/`human_launch_approver`
/`aggregated_only`; Ledgerx `real_entity`/`subject` (`per_client`)
/`external_enforcement` (the ledger)/`calibrated` (close cycle)
/`licensed_professional_of_record`/`identified_organizations_only`.

## Reproducibility (SHOULD)

Model and scenario generation SHOULD be reproducible, with the
generation seed part of object identity (the Medx `generation_seed`
rule). For LLM-driven scenario runs, reproducibility means seeded panel
composition and digest-pinned prompt packs — honest re-runnability of
the setup, not bit-identical output.

## Declaring conformance

```yaml
# models/derived-model-conformance.yaml
schema_version: 1
kind: xfactory_derived_model_conformance
conforms_to: governed-derived-model
domain:
  id: <domain id>
families:
  - id: <family id>
    tier: governed | calibrated
    members:
      - role: model
        kind: <template id>
        template: <repo-root-relative path>
        provenance: {form: ..., ...}
        truth_store_access: {field: ..., value: read_only}   # or {gate: ...}
      - role: scenario
        kind: <template id>
        template: <path>
        truth_store_access: {...}
        action_authority: [{field: ..., value: none}]        # or gates
        output_status_field: <field>
    dials: {identity: ..., scope: ..., truth_store: ..., truth_store_class: ...,
            promoting_authority: ..., person_modeling: ...}
```

Validate:

```bash
python3 <openxFactory-checkout>/scripts/validate-derived-models.py <domain-repo>
```

Absence of a declaration is not a failure — conformance is opt-in.
Reference examples (including the three proof-domain shapes and the
negative guardrails) live under `examples/derived-models/`.
