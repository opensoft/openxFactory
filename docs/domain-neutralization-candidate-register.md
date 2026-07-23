# Domain Neutralization Candidate Register

Status: staged
Kind: register
Repository context: openxFactory
Source scan date: 2026-07-08
Purpose: list domain repo patterns that may become neutral openxFactory
contracts, templates, validators, or specs.

Use this register with
[Domain-To-Neutral Promotion Process](domain-to-neutral-promotion-process.md).

## Storage Rule

This register lives in `openxFactory` because it tracks possible changes to the
neutral xFactory contract. Domain repos remain the source for domain-owned
examples and policy. The top-level `xFactory` aggregation repo should not own
this backlog.

## Candidate List

Status lifecycle: `seed` -> `staged` -> `openspec` -> `implemented` ->
`adopted` (domain re-pin and local-copy retirement complete), or `rejected` /
`deferred` at any point. These are compact aliases for the canonical
[document lifecycle](document-lifecycle.md) spine: `seed` = captured/organized,
`staged` = organized, `openspec` = proposed/ratified, `implemented` =
implemented/promoted, `adopted` = adopted.

| ID | Topic | Decision | Priority | Status | Likely openxFactory artifact |
| --- | --- | --- | --- | --- | --- |
| DTN-001 | Neutral workflow contract schema | `promote` | P0 | `adopted` | `contracts/schemas/xfactory-workflow.schema.yaml` |
| DTN-002 | Gate record and gate outcome vocabulary | `promote` | P0 | `adopted` | gate schema, vocabulary, and validator rules |
| DTN-003 | Generalized job/run/event envelope | `split` | P0 | `adopted` | domain-neutral job envelope schemas replacing engineering-specific fields |
| DTN-004 | Credential broker and runtime capability grant schemas | `split` | P1 | `adopted` | broker, grant, binding, requirement, and audit schemas |
| DTN-005 | Proposed trigger and admission boundary | `promote` | P1 | `seed` | proposed-trigger schema and admission workflow doc |
| DTN-006 | Candidate-only work product lifecycle | `promote` | P1 | `seed` | candidate lifecycle vocabulary and promotion gates |
| DTN-007 | Decision provenance and citation ledger | `split` | P1 | `seed` | neutral decision provenance ledger schema |
| DTN-008 | Foundational data reliability and risk-of-wrong gate | `split` | P1 | `seed` | reliability assessment and risk gate pattern |
| DTN-009 | Client/local organization authority intersection | `promote` | P1 | `seed` | Client Hermes authority-intersection rule |
| DTN-010 | Avatar or conversation safety supervisor | `split` | P2 | `seed` | neutral safety supervisor state machine and overlay slots |
| DTN-011 | Domain profile, tenant, and deployment profile normalization | `promote` | P2 | `seed` | standard profile/deployment questionnaire schema |
| DTN-012 | Memory mapping coverage validator and template | `promote` | P2 | `seed` | mapping template and coverage validator |
| DTN-013 | Neutral roles and authority model | `split` | P0 | `adopted` | abstract roles-and-authority doc; engineering instantiation moves to codexFactory |
| DTN-014 | Governed derived model (non-authoritative models and scenarios, tiered conformance) | `promote` | P2 | `implemented` | `governed-derived-model` capability: conformance schema, invariant vocabulary, `validate-derived-models.py` |

## Candidate Details

### DTN-001: Neutral workflow contract schema

OpenSpec: [promote-workflow-gate-contract](../openspec/changes/archive/2026-07-09-promote-workflow-gate-contract/proposal.md)
(with DTN-002). Adopted 2026-07-09: all five domains validate (Adx 4,
Ledgerx 5, Medx 1, codex 7 contracts; Ops's `opsx_workflow` operational
definitions are out of contract scope — convergence is a possible future
candidate), `promoted_from` declared in every stack.yaml.

Domain workflow YAML files share `workflow.id`, `display_name`, `owner_layer`,
`inputs`, `outputs`, `gates`, `policy`, and `audit`, but openxFactory does not
yet publish a single neutral workflow schema.

Evidence:

- `docs/domain-factory-implementation-checklist.md` requires workflow purpose,
  inputs, states, transitions, gates, outputs, blocking conditions,
  traceability, approvals, and archive behavior.
- `xFactories/AdxFactory/workflows/campaign-intake.yaml`
- `xFactories/LedgerxFactory/workflows/client-intake.yaml`
- `xFactories/MedxFactory/workflows/decision-foundation-loop.yaml`
- `xFactories/codexFactory/workflows/branch-review.yaml`

Domain-local exclusions: specific workflow names, domain triggers, domain
evidence types, reviewer roles, and action policies.

### DTN-002: Gate record and gate outcome vocabulary

OpenSpec: [promote-workflow-gate-contract](../openspec/changes/archive/2026-07-09-promote-workflow-gate-contract/proposal.md)
(with DTN-001). Adopted 2026-07-09 with DTN-001; both observed blocking
styles canonicalized.

The domain repos repeatedly define gate owner, requirements, blocking behavior,
evidence, risk, exception, next transition, and audit outcomes. openxFactory
should own the common gate record and outcome vocabulary.

Evidence:

- `xFactories/AdxFactory/docs/campaign-workflow-gates.md`
- `xFactories/LedgerxFactory/docs/accounting-workflow-gates.md`
- `xFactories/OpsxFactory/docs/workflow-gates.md`
- `xFactories/MedxFactory/workflows/decision-foundation-loop.yaml`

Domain-local exclusions: gate names, evidence standards, professional review
thresholds, and escalation roles.

### DTN-003: Generalized job/run/event envelope

OpenSpec: [neutralize-job-envelope](../openspec/changes/archive/2026-07-09-neutralize-job-envelope/proposal.md).
Adopted 2026-07-09: envelope/run loosened (contract-v1.5), event already
neutral; codexFactory overlay re-tightens engineering jobs and declares
`specializes` (first use). Neutrality test: 7 example envelopes pass core +
overlay; it also surfaced a pre-existing defect — `merge_master` was used
by the canonical example but missing from the old enum (fixed in overlay).

Existing openxFactory job schemas still include engineering-specific fields such
as repository, feature, and engineering job types. The domain repos now show the
need for subject, client, workflow, focal item, gate, and artifact references.

Evidence:

- `contracts/schemas/hermes-job-envelope.schema.yaml`
- `contracts/schemas/hermes-job-run.schema.yaml`
- `contracts/schemas/hermes-job-event.schema.yaml`
- `xFactories/MedxFactory/workflows/decision-foundation-loop.yaml`
- `xFactories/OpsxFactory/workflows/user-lifecycle.yaml`

Domain-local exclusions: GitHub-specific enforcement fields, clinical case
fields, tenant admin command fields, and domain artifact names.

### DTN-004: Credential broker and runtime capability grant schemas

OpenSpec: [promote-credential-contracts](../openspec/changes/archive/2026-07-09-promote-credential-contracts/proposal.md).
Adopted 2026-07-09: five record kinds canonicalized shape-only; all Ops
contracts validated unchanged; Ops policy kinds deliberately out of scope.

openxFactory already owns credential access as a neutral concept. OpsxFactory has
the clearest concrete broker, binding, grant, requirement, and audit templates.
Promote the generic shape while keeping credential families local.

Evidence:

- `docs/credential-access-model.md`
- `xFactories/OpsxFactory/credentials/broker-contract.yaml`
- `xFactories/OpsxFactory/credentials/grants.template.yaml`
- `xFactories/OpsxFactory/credentials/requirements.yaml`
- `xFactories/OpsxFactory/credentials/audit.yaml`

Domain-local exclusions: Entra, Exchange, DNS, GitHub, backup, deployment, EHR,
accounting, ad-platform, or other domain credential families and scopes.

### DTN-005: Proposed trigger and admission boundary

MedxFactory states a reusable boundary: Omnigent may detect and propose, but the
appropriate Hermes layer and openxFactory decide whether the proposal becomes an
admitted workflow.

First concrete consumer (2026-07-23): the LedgerxFactory AP-intake
design (`xFactories/LedgerxFactory/openspec/changes/add-ledgerx-ap-intake/`)
— a deterministic mailbox monitor emits proposed triggers under Hermes
self-initiation ("downstream system event") and an admission boundary
opens governed `document_intake` jobs. Shaping decision recorded there:
**admission vocabulary stays species-free** — the trigger boundary
classifies channel and plausibility only (one coarse `inbound_document`
admission per channel); document species is pipeline classification, so
the neutral admission contract needs no per-document-type vocabulary.

Evidence:

- `xFactories/MedxFactory/docs/omnigent-trigger-boundary.md`
- `docs/xfactory-domain-factory-model.md`
- `docs/omnigent-constitution.md`
- `xFactories/LedgerxFactory/openspec/changes/add-ledgerx-ap-intake/` (proposed 2026-07-23; all design decisions resolved)

Domain-local exclusions: clinical trigger categories, patient-specific
authority, clinician review requirements, and (per the Ledgerx shaping)
all document-species vocabulary.

### DTN-006: Candidate-only work product lifecycle

MedxFactory's DDE docs sharply separate candidates from conclusions. This is a
neutral lifecycle useful for any domain where agents generate ideas, findings,
risks, plans, or recommendations before review.

Second consumer shape (2026-07-23): the LedgerxFactory AP-intake design
(`xFactories/LedgerxFactory/openspec/changes/add-ledgerx-ap-intake/`) — the
extraction record and the **coding candidate** (account/dimension/tax
proposal with confidence and cited precedents) are candidates until
human disposition or ratified-envelope clearance; the standing Ledgerx
memory-fill rule "OCR and AI categorization are candidates until
reconciled or reviewed" is this lifecycle stated as domain policy.

Evidence:

- `xFactories/MedxFactory/docs/differential-discovery-engine.md`
- `xFactories/MedxFactory/workflows/decision-foundation-loop.yaml`
- `xFactories/codexFactory/workflows/pr-admission.yaml`
- `xFactories/LedgerxFactory/openspec/changes/add-ledgerx-ap-intake/` (proposed 2026-07-23; all design decisions resolved)

Domain-local exclusions: diagnoses, treatments, accounting conclusions,
campaign approvals, deployment approvals, and merge decisions.

### DTN-007: Decision provenance and citation ledger

MedxFactory's decision ledger is medical in content, but the neutral pattern is
broader: record what a decision relied on, source layer, dependency strength,
reliability, review status, and audit hashes.

Evidence:

- `xFactories/MedxFactory/docs/decision-data-citation-ledger.md`
- `docs/traceability-model.md`
- `docs/customer-memory-fill-maintenance-taxonomy.md`

Domain-local exclusions: patient identifiers, clinical packet names, treatment
order rationale fields, medical evidence classes, and clinician attestation.

### DTN-008: Foundational data reliability and risk-of-wrong gate

MedxFactory's distinction between operational truth and reasoning-fallible
evidence is useful beyond medicine. openxFactory can define a neutral pattern
for foundational facts, reliability status, dependency strength, and recheck
requirements.

Second consumer shape (2026-07-23): the LedgerxFactory AP-intake design
(`xFactories/LedgerxFactory/openspec/changes/add-ledgerx-ap-intake/`) —
per-field extraction confidence with source anchors, binding-dependent
message-evidence grades (direct-delivery SPF/DKIM vs forwarded ARC),
and risk-tiered disposition (posting-autonomy position + unwaivable
domain invariants like bank-detail-change-never-auto) are exactly the
reliability-status / dependency-strength / recheck pattern this
candidate names.

Evidence:

- `xFactories/MedxFactory/docs/foundational-data-reliability-and-reverification.md`
- `docs/customer-memory-fill-maintenance-taxonomy.md`
- `docs/traceability-model.md`
- `xFactories/LedgerxFactory/openspec/changes/add-ledgerx-ap-intake/` (proposed 2026-07-23; all design decisions resolved)

Domain-local exclusions: modality-specific clinical failure modes, treatment
risks, and clinician workflows.

### DTN-009: Client/local organization authority intersection

MedxFactory's Care Organization Hermes clearly models effective access as the
intersection of customer consent, client policy, domain policy, legal
constraints, role or credential state, and encounter context. That is a neutral
Client Hermes rule.

Evidence:

- `xFactories/MedxFactory/docs/care-organization-hermes.md`
- `docs/xfactory-domain-factory-model.md`
- `contracts/schemas/xfactory-domain-stack.schema.yaml`

Domain-local exclusions: care organization names, clinical roles, standing
orders, medical director policy, MRNs, and care-team assignment.

### DTN-010: Avatar or conversation safety supervisor

MedxFactory's patient-facing conversation supervisor has reusable structure:
parallel monitoring, fast and slow loops, deterministic policy gatekeeper,
handoff router, risk levels, pause states, and escalation paths.

Evidence:

- `xFactories/MedxFactory/docs/patient-facing-conversation-safety-supervisor.md`
- `xFactories/MedxFactory/docs/patient-facing-provider-agent-trust.md`
- `docs/avatar-first-ui-standard.md`

Domain-local exclusions: medical safety categories, emergency clinical
escalation, patient-specific disclosure wording, and clinician handoff policy.

### DTN-011: Domain profile, tenant, and deployment profile normalization

Domain repos define profiles and deployment/tenant shapes differently. Opsx's
instantiation questionnaire is already marked `xfactory_schema`, making it a
strong neutral candidate.

Evidence:

- `xFactories/OpsxFactory/schemas/instantiation-questionnaire.schema.yaml`
- `xFactories/MedxFactory/schemas/deployment-profile.schema.yaml`
- `xFactories/MedxFactory/schemas/tenant.schema.yaml`
- `xFactories/codexFactory/schemas/deployment-profile.schema.json`
- `docs/domain-instantiation-pre-run-questionnaire.md`

Domain-local exclusions: clinic, firm, agency, managed-system, and software-team
profile content.

### DTN-012: Memory mapping coverage validator and template

openxFactory already owns the memory fill and maintenance taxonomy. Each domain
has a local mapping. The next neutral improvement is a template and validator
that checks every domain maps each required mode.

Evidence:

- `docs/customer-memory-fill-maintenance-taxonomy.md`
- `xFactories/MedxFactory/docs/patient-memory-fill-maintenance-mapping.md`
- `xFactories/OpsxFactory/docs/managed-system-memory-fill-maintenance-mapping.md`
- `xFactories/codexFactory/docs/project-memory-fill-maintenance-mapping.md`
- `xFactories/AdxFactory/docs/campaign-memory-fill-maintenance-mapping.md`
- `xFactories/LedgerxFactory/docs/client-ledger-memory-fill-maintenance-mapping.md`

Domain-local exclusions: source families, evidence types, authority thresholds,
retention rules, privacy rules, and reviewer roles.

### DTN-013: Neutral roles and authority model

OpenSpec: [split-roles-authority](../openspec/changes/archive/2026-07-09-split-roles-authority/proposal.md).
Adopted 2026-07-09: neutral doc keeps governance layers/roles/principles;
engineering instantiation (execution leads, escalation routes, groups YAML)
moved to codexFactory/docs/engineering-roles-and-authority.md with a
`specializes` declaration.

`docs/roles-and-authority.md` lives in openxFactory but is engineering-specific:
it describes itself as the model "for the AI software development factory",
defines the engineering-only LE/LC/LQ/LI/LS lead-role set, and names GitHub as
the external enforcement system. This contradicts the repo's neutrality rule
(`docs/omnigent-constitution.md`, `docs/workflow-contract.md`). The split:
keep an abstract role/authority/escalation model here (authority tiers, lead
roles as slots, external-enforcement slot), and move the engineering
instantiation (LE/LC/LQ/LI/LS, GitHub enforcement) down to codexFactory.

Evidence:

- `docs/roles-and-authority.md`
- `docs/omnigent-constitution.md`
- `docs/workflow-contract.md`

Domain-local exclusions: concrete role names, reviewer group mappings, and the
domain's external enforcement system.

### DTN-014: Governed derived model (non-authoritative models and scenarios, tiered conformance)

OpenSpec: [add-governed-derived-model](../openspec/changes/archive/2026-07-23-add-governed-derived-model/proposal.md).
Implemented 2026-07-23 — same-day capture → decisions → promotion →
ratified/realized/archived. Canonical spec
`openspec/specs/governed-derived-model/`; contract
`contracts/schemas/xfactory-derived-model-conformance.schema.yaml`;
validator `scripts/validate-derived-models.py`. Conformers: MedxFactory
(`governed` tier, declaration-only, 0987bca), AdxFactory (`calibrated`
tier, first, eb98f84 via add-adx-object-model), and LedgerxFactory
(`calibrated` tier, first real-entity two-object split, fc624a5 via
add-ledgerx-counterparty-model) — three of five domains conform; all
three dial-position archetypes (synthetic/domain, synthetic-aggregate/
subject, real-entity/external-enforcement) are now proven live. Flips to
`adopted` when domain stack pins advance to a ref containing the schema
and the manifest entry lands — at the NEXT bundle cut: contract-v1.16
was cut 2026-07-23 (omnigent family + layer vocabulary) before this
schema registered, so the deferred items target contract-v1.17. The
former staging topic
[governed-derived-model](../openspec/changes/archive/2026-07-23-add-governed-derived-model/supporting-docs/governed-derived-model.md)
rides under the change's `supporting-docs/` (named during the
Adx→Ledgerx cross-domain modeling session with Brett Heap; Medx
recognized as the original instance; renamed from "derived third-party
model" — the Medx dream object models a synthetic case at domain scope
and the simulation scenario models the subject, so "third party"
over-fit the marketing/accounting instances).

Three domains independently converged on the same object shape: a
governed model derived from evidence that can never be mistaken for
truth or act on the world — Medx models synthetic patient cases (dream
object + simulation scenario), Adx models the advertiser's customer
(persona + campaign simulation), Ledgerx models the client company's
customers and vendors (counterparty health profile + financial
scenario). Five invariants are the verified intersection (line-checked
2026-07-23 against the ratified Medx templates): non-authoritative by
construction with promotion-by-new-object (authority never mutates in
place), full provenance (assumption register, or the
assumptions-forbidden form: evidence trace min 1 + invented-facts
`none`), read-only truth store with zero action authority, declared
scope (domain|subject) with no cross-scope data without review, and
human-gated promotion of hypothesis-only outputs. Calibration
(designated-writer loop, derived-only confidence, miss-downgrade) is a
second conformance tier (`calibrated`), not an invariant — the Medx
templates carry none. Six declared dials: identity (synthetic vs real
entity; real implies a two-object identity/assessment split), model
scope, truth store (Hermes memory vs external enforcement system),
calibration source, promoting authority, and person_modeling
(`synthetic_only | aggregated_only | identified_organizations_only |
identified_persons_under_policy`, the last requiring a policy ref).
Promote the conformance declaration
(`conforms_to: governed-derived-model`, kind
`xfactory_derived_model_conformance`), the invariant vocabulary, and
`validate-derived-models.py`; domains keep their own object templates.
Draft proposal/spec/tasks live in the staging topic's `openspec/`.

Evidence:

- `xFactories/MedxFactory/templates/dream-object.yaml` (ratified; conforms at `governed` tier declaration-only)
- `xFactories/MedxFactory/templates/simulation-scenario.yaml` (ratified)
- `xFactories/AdxFactory/openspec/changes/archive/2026-07-23-add-adx-object-model/` (realized 2026-07-23 — first `calibrated` conformer; live templates at `templates/{persona,campaign-simulation}.yaml`)
- `xFactories/LedgerxFactory/openspec/changes/archive/2026-07-23-add-ledgerx-counterparty-model/` (realized 2026-07-23 — second `calibrated` conformer, first real-entity split; live templates at `templates/{counterparty-health-profile,financial-scenario}.yaml`)

Domain-local exclusions: the modeled party's kind and fields, signal/trait
vocabularies, truth-store identity, benchmark content, approver roles,
and person-modeling policy (aggregation rules, fair-credit constraints).

