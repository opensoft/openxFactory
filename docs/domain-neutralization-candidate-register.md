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
| DTN-014 | Derived third-party model (governed non-authoritative models and scenarios) | `promote` | P2 | `staged` | derived-model invariant vocabulary, conformance schema, and validator rules |

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

Evidence:

- `xFactories/MedxFactory/docs/omnigent-trigger-boundary.md`
- `docs/xfactory-domain-factory-model.md`
- `docs/omnigent-constitution.md`

Domain-local exclusions: clinical trigger categories, patient-specific
authority, and clinician review requirements.

### DTN-006: Candidate-only work product lifecycle

MedxFactory's DDE docs sharply separate candidates from conclusions. This is a
neutral lifecycle useful for any domain where agents generate ideas, findings,
risks, plans, or recommendations before review.

Evidence:

- `xFactories/MedxFactory/docs/differential-discovery-engine.md`
- `xFactories/MedxFactory/workflows/decision-foundation-loop.yaml`
- `xFactories/codexFactory/workflows/pr-admission.yaml`

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

Evidence:

- `xFactories/MedxFactory/docs/foundational-data-reliability-and-reverification.md`
- `docs/customer-memory-fill-maintenance-taxonomy.md`
- `docs/traceability-model.md`

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

### DTN-014: Derived third-party model (governed non-authoritative models and scenarios)

Staged 2026-07-23: staging topic
[derived-third-party-model](../ideation/staging/derived-third-party-model/derived-third-party-model.md)
(named during the Adx→Ledgerx cross-domain modeling session with Brett
Heap; Medx recognized as the original instance).

Three domains independently converged on the same object shape: a
governed model of a party the served subject cares about but who holds
no authority in the stack — Medx models a synthetic patient (dream
object + simulation scenario), Adx models the advertiser's customer
(persona + campaign simulation), Ledgerx models the client company's
customers and vendors (counterparty health profile + financial
scenario). All three carry the same six invariants: non-authoritative by
construction (single-value enums), per-fact provenance with a declared
assumption register, read-only access to the domain truth store with
zero action authority, per-subject isolation, human-gated promotion of
hypotheses into action, and calibration-derived confidence written only
by a designated workflow. What varies is four dials: third-party
identity (synthetic vs real entity), truth store (Hermes memory vs
external enforcement system), calibration source, and promoting
authority. Promote the invariant vocabulary, a `conforms_to` conformance
declaration, and validator rules; domains keep their own object
templates.

Evidence:

- `xFactories/MedxFactory/templates/dream-object.yaml` (ratified; conforms as-is)
- `xFactories/MedxFactory/templates/simulation-scenario.yaml` (ratified)
- `xFactories/AdxFactory/ideation/staging/adx-persona-simulation/` (staged 2026-07-23)
- `xFactories/LedgerxFactory/ideation/staging/ledgerx-counterparty-model/` (staged 2026-07-23)

Domain-local exclusions: the modeled party's kind and fields, signal/trait
vocabularies, truth-store identity, benchmark content, approver roles,
and person-modeling policy (aggregation rules, fair-credit constraints).

