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
| DTN-015 | Learned handling rule / correction-promotion loop | `promote` | P2 | `seed` | handling-rule invariant vocabulary + correction→promotion lifecycle (governed-derived-model profile) |
| DTN-016 | Consent instrument (the rung-1↔rung-2 authority root as a schema'd object) | `promote` | P1 | `staged` | `xfactory_consent_instrument` schema + vocabulary; mapping to memory-gateway consent-profile |
| DTN-017 | Subject establishment (facts → neutral best-practice design → platform realization → verified apply; plus the audit-lift mirror) | `promote` | P1 | `staged` | neutral subject-design + platform-realization artifact kinds, provenance-graded fact set, reference-archetype lifecycle, conformance-tiering dial, verify-by-read-back obligation |
| DTN-018 | Domain-repo conformance-gate check pack | `promote` | P1 | `seed` | neutral inventory/parity/pin checks run from the pinned openxFactory checkout |
| DTN-019 | Proposal-support lifecycle tool | `promote` | P1 | `seed` | `scripts/proposal-support.py` beside its in-repo doc-health consumer (family 5) |
| DTN-020 | Change-ratification workflow contract | `promote` | P2 | `seed` | neutral reference ratification workflow (pre-implementation governance sidecar) |
| DTN-021 | Subject/tenant Hermes layer template schema | `promote` | P2 | `seed` | fold into the `hermes-domain-overlay` / installation-overlay schema family |
| DTN-022 | Avatar client lab neutral home | `split` | P2 | `seed` | home fork open: own repo vs aggregation (avatar-reference-runtime forbids deployable surfaces in openxFactory) |
| DTN-023 | Governance change-review lane | `split` | P2 | `seed` | change-review half of the review lane (ten governance-document dimensions) |

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
design (`xFactories/LedgerxFactory/openspec/changes/archive/2026-07-23-add-ledgerx-ap-intake/`)
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
- `xFactories/LedgerxFactory/openspec/changes/archive/2026-07-23-add-ledgerx-ap-intake/` (ratified, realized, archived 2026-07-23; live workflows at `workflows/{document-intake,invoice-coding,vendor-onboarding}.yaml`)

Domain-local exclusions: clinical trigger categories, patient-specific
authority, clinician review requirements, and (per the Ledgerx shaping)
all document-species vocabulary.

### DTN-006: Candidate-only work product lifecycle

MedxFactory's DDE docs sharply separate candidates from conclusions. This is a
neutral lifecycle useful for any domain where agents generate ideas, findings,
risks, plans, or recommendations before review.

Second consumer shape (2026-07-23): the LedgerxFactory AP-intake design
(`xFactories/LedgerxFactory/openspec/changes/archive/2026-07-23-add-ledgerx-ap-intake/`) — the
extraction record and the **coding candidate** (account/dimension/tax
proposal with confidence and cited precedents) are candidates until
human disposition or ratified-envelope clearance; the standing Ledgerx
memory-fill rule "OCR and AI categorization are candidates until
reconciled or reviewed" is this lifecycle stated as domain policy.

Evidence:

- `xFactories/MedxFactory/docs/differential-discovery-engine.md`
- `xFactories/MedxFactory/workflows/decision-foundation-loop.yaml`
- `xFactories/codexFactory/workflows/pr-admission.yaml`
- `xFactories/LedgerxFactory/openspec/changes/archive/2026-07-23-add-ledgerx-ap-intake/` (ratified, realized, archived 2026-07-23; live workflows at `workflows/{document-intake,invoice-coding,vendor-onboarding}.yaml`)

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
(`xFactories/LedgerxFactory/openspec/changes/archive/2026-07-23-add-ledgerx-ap-intake/`) —
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
- `xFactories/LedgerxFactory/openspec/changes/archive/2026-07-23-add-ledgerx-ap-intake/` (ratified, realized, archived 2026-07-23; live workflows at `workflows/{document-intake,invoice-coding,vendor-onboarding}.yaml`)

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
and the manifest entry lands. NOTE (2026-07-24): the v1.16, v1.17, AND
v1.18 cuts each missed the registration (the deferral lived only in the
archived change's tasks); a pending-registration item now sits at the
top of `contracts/CHANGELOG.md` (Unreleased section) where the next
cutter will see it. The
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

### DTN-015: Learned handling rule / correction-promotion loop

Reserved by the archived LedgerxFactory `add-ledgerx-ap-intake` change
(tasks §7.2) and realized there as a first instance: per-counterparty
handling rules — provenance-cited, review-stated, calibrated governed
derived models of "how this party's paperwork behaves" — fed by a
correction→promotion loop (human exception-fix → correction record →
accumulated promotion candidate → reviewed rule; exception clusters no
rule fixes route to ideation as evidence of a missing workflow). Every
domain will want the loop: Adx per-channel creative-spec rules, Ops
per-system remediation rules, Medx per-modality documentation rules.

Evidence:

- `xFactories/LedgerxFactory/templates/handling-rule.yaml` +
  `templates/correction-record.yaml` (realized 2026-07-23; conformant
  `calibrated` governed-derived-model family)
- `xFactories/LedgerxFactory/openspec/specs/ledgerx-ap-intake/spec.md`
  (Learned handling rules requirement)

Domain-local exclusions: rule content, correction vocabularies,
promotion review seats, calibration cadence.

### DTN-016: Consent instrument (the rung-1↔rung-2 authority root as a schema'd object)

Staged 2026-07-23→2026-07-24: staging topic
[consent-instrument-contract](../ideation/staging/consent-instrument-contract/consent-instrument-contract.md)
(named by Brett Heap during the Meds Rx, Inc onboarding). Every
domain's rung-1↔rung-2 relationship starts with a consent instrument —
engagement letter, patient consent, agency agreement, operating
authorization — and it is the ROOT OF THE AUTHORITY CHAIN: credential
grants cite it, engagement gates verify it, adapters activate on it,
termination cascades to credential revoke+rotate. The shape is
domain-invariant (parties by party-ladder rung incl. third-party estate
hosts, scope, delegation clauses with technical access shapes, autonomy
position, revocation SLA, signed-original custody by opaque locator +
digest, status lifecycle) and composes with memory-gateway
consent-profile (instrument authorizes ACTION; profile governs DATA),
document-cataloging, and credential-contracts.

Evidence:

- `xFactories/LedgerxFactory/docs/engagement-letter-template.md` +
  `xFactories/LedgerxFactory/tenants/ledgerxcorp/clients/medsrx/consent-record.yaml`
  (first schema'd instance, kind `ledgerx_engagement_consent_record`)
- `xFactories/MedxFactory/hermes/patient/consent-model.yaml` +
  `contracts/memory-gateway/consent-profile.schema.yaml`; **second
  schema'd instance COMPLETE** —
  `add-patient-consent-instrument` authored, ratified, realized, and
  archived 2026-07-30 (canonical Medx spec `patient-consent-instrument`,
  8 requirements): custody-bearing `medx_patient_consent_record`
  (template + schema pair + fictional example + negative-tested
  validator cross-checks) with the declared consent-profile derivation.
  The staged exit condition (second domain instantiates) is met —
  `add-consent-instrument` is unblocked
- `docs/party-ladder.md` (rung model; estate-host third parties)

Domain-local exclusions: instrument names, legal form and execution
mechanics, fee/term content, jurisdiction-specific clauses.


### DTN-017: Subject establishment (facts → neutral design → platform realization → verified apply)

Staged 2026-07-28: staging topic
[subject-establishment](../ideation/staging/subject-establishment/subject-establishment.md)
(named by Brett Heap while designing LedgerxFactory's company
provisioning). Every domain runs the same motion at the start of a
subject's life — establish provenance-graded facts, design the
best-practice setup for that subject IN DOMAIN TERMS, decide which
external system of record it lives in, map the design into that
system, review, apply, and verify by reading the result back. Ledgerx's
new client company, Medx's new patient, codex's new engineering
project, Opsx's new managed estate, and Adx's new campaign subject are
the same pipeline with different nouns.

The load-bearing neutral idea is the **design/realization split**: a
platform-neutral design whose elements carry semantic roles, plus a
per-platform overlay that maps them to concrete system objects. It buys
portability (the design survives a platform migration), reviewability
(an expert reviews domain judgment, not vendor trivia), and cheap
support for a second platform (a mapping, not a redesign) — the same
idiom as neutral contract + per-domain overlay, one level down. The
mirror gives every domain an audit product: read the existing
configuration, lift it to neutral, diff against the design the research
would have produced, propose a migration.

Two authority classes that must never share a grant: establishing a NEW
subject in an empty environment (low risk — nothing to damage) versus
MIGRATING an established subject with history (high risk — proposal,
approval, apply, verify).

Evidence:

- `xFactories/LedgerxFactory/ideation/staging/company-provisioning/`
  (first instantiation: `layered-books-design.md` neutral design then
  MSBC realization; `provisioner-identity-model.md` the applying
  identity)
- `xFactories/LedgerxFactory/tenants/ledgerxcorp/ledger-estates/farheap-sandbox-rehearsal-evidence.md`
  (the motivating discovery: an empty, unconfigured subject company —
  and the platform lesson that BC validates before it authorizes, which
  is why verify-by-read-back belongs in the contract)
- `contracts/omnigent/` (the `generate`/`verify`/`challenge` archetypes
  the pipeline already has; terminal apply stays with external
  enforcement and its human authority)

Second consumer DECIDED 2026-07-28 (Brett): **codexFactory
new-project** — `project` is already a first-class codex subject kind
and `check_profile` / `reviewer_group` are neutral-design elements
wearing domain names, so the second instantiation structures existing
material rather than inventing it, and codex brings an existing-subject
population so the audit mirror gets exercised immediately. Its mapping
surfaced the finding Ledgerx structurally could not: the DESIGNING
domain and the APPLYING administrator can be different factories
(GitHub administration is OpsxFactory's `github-administration-workflow`,
not codexFactory's), so the realization artifact must be handoff-shaped
with correlation between design, handoff, and applied result — the seam
is now RATIFIED as the `deployment-handoff-boundary` capability
(`add-deployment-handoff-boundary`, 2026-07-29): the codexFactory second
consumer's realization artifacts cross as `client_infrastructure_request`
handoffs with correlation identifiers, exactly the crossing that
capability defines (linkage recorded 2026-07-30, its task 2.3).

Composes rather than restates: DTN-016 (consent instrument), DTN-015
(correction→promotion, the archetype-harvest loop), governed-derived-
model (tiered conformance), workflow-gate-contract, credential-contracts.

Domain-local exclusions: the CONTENT of any design or archetype (chart
of accounts, care-plan template, branch-protection baseline), which
external systems are supported and their mapping tables, and the expert
seat that reviews a deviating design.

### DTN-018: Domain-repo conformance-gate check pack

Surfaced by the 2026-08-03 codexFactory neutrality sweep (evidence record
under the merged `adopt-neutral-tooling-home` change's `supporting-docs/`).
Three generic domain-repo conformance checks live in codexFactory with no
engineering vocabulary: stack.yaml ↔ on-disk ↔ README required-artifact
agreement, workflow `.md` transition targets ↔ `.yaml` gate `produces[]`
parity, and stack.yaml `contract_ref` ancestry vs the aggregation pin.
Every domain factory has a `stack.yaml`, workflow doc pairs, and an
openxFactory pin; the workflow-gate-contract rule already says canonical
validators run from the pinned checkout, never copied into domain repos,
and `check-openxfactory-pin.py` partially duplicates
`validate-domain-openxfactory-pins.py`.

Evidence:

- `xFactories/codexFactory/scripts/check-inventory-consistency.py`,
  `check-workflow-state-parity.py`, `check-openxfactory-pin.py`
  (~310 LOC + `tests/conformance-gate/`)
- `openxFactory/scripts/validate-domain-openxfactory-pins.py` (the
  neutral home for exactly this class)

Domain-local exclusions: `scripts/validate-docs.sh` (the codex wrapper
and its required-files list stay).

### DTN-019: Proposal-support lifecycle tool

Surfaced by the same sweep; sharpened by `adopt-neutral-tooling-home`:
the doc-health checker (family 5, proposal supporting-document
integrity) now lives in openxFactory while the only producer of the
artifacts it checks remains a codexFactory script. The tool moves staged
supporting documents into an active change, rewrites links, and
preserves the bundle through OpenSpec archive with sha256 manifests —
zero domain vocabulary in 545 LOC.

Evidence:

- `xFactories/codexFactory/scripts/proposal-support.py` +
  `tests/proposal-support/`
- `openxFactory/docs/doc-health.md` family 5 (the in-repo consumer)

Domain-local exclusions: none identified — the tool is pure lifecycle
mechanics.

### DTN-020: Change-ratification workflow contract

Surfaced by the same sweep. codexFactory's `change-ratification`
workflow pair is a pre-implementation governance sidecar (its own
README's words): inputs are committed change, strict validation
evidence, governed review record, dispositions, human ratifier; output a
ratification record. Zero engineering vocabulary; every domain factory
ratifies OpenSpec changes. The promotion shape is a neutral REFERENCE
contract upstream (DTN-001/002 lineage) with the codex instance
declaring conformance — not a relocation.

Evidence:

- `xFactories/codexFactory/workflows/change-ratification.md` + `.yaml`
- `openxFactory/contracts/schemas/xfactory-workflow.schema.yaml` (the
  neutral workflow contract family it instantiates)

Domain-local exclusions: the nine engineering workflows beside it
(branch-review, pr-admission, merge-readiness, spec-kit-execution, …).

### DTN-021: Subject/tenant Hermes layer template schema

Surfaced by the same sweep. `hermes-template.schema.json` carries no
domain vocabulary at all — `subject_kinds`, `required_subject_fields`,
`layer_name`, `role`, `owns`, `must_not_own` — and the neutral home
family already exists (`contracts/hermes-domain-overlay/`,
`domain-installation-overlay.schema.yaml`).

Evidence:

- `xFactories/codexFactory/schemas/hermes-template.schema.json` (2.4 KB)
- `openxFactory/contracts/hermes-domain-overlay/` (receiving family)

Domain-local exclusions: the `$id` host string and codex layer
instances under `hermes/`.

### DTN-022: Avatar client lab neutral home

Surfaced by the same sweep as the special case: the lab (240 files,
~22.9k LOC Dart) is the reference client of the NEUTRAL avatar-first-ui
standard and even ships a MedxFactory patient-intake profile from inside
the engineering repo — but openxFactory's `avatar-reference-runtime`
spec FORBIDS deployable surfaces (no network listener, deployment
manifest, live provider SDK) in its reference package, so the neutral
home cannot be openxFactory. The open fork this entry carries: a
dedicated repo vs the aggregation layer. Upstream drafts already flowed
from the lab into `contracts/avatar-client-lab/` by provenance note.

Evidence:

- `xFactories/codexFactory/apps/avatar-client-lab/` +
  `specs/002-avatar-client-lab/upstream-drafts/`
- `openxFactory/contracts/avatar-client-lab/avatar-state-derivation-table.md`
  (provenance: adopted from the lab)

Domain-local exclusions: codex-specific lab pilots and engineering CI
wiring.

### DTN-023: Governance change-review lane

Surfaced by the same sweep; this entry is the designed revisit hook for
the credential tax `adopt-neutral-tooling-home` design D6 explicitly
accepted. The review lane's change-review half reviews GOVERNANCE
documents — its ten dimensions are normative-coverage,
vocabulary-conformance, authority-isolation, provenance,
scenario-completeness, evidence-levels, security, ownership-boundaries,
traceability, open-questions — and resolves `change:<repo>:<change-id>`
targets across every submodule from the aggregation's committed
`.gitmodules`, proven on an accepted OpsxFactory record. The
PR-admission half (PR verdicts, changed-path allowlists) is legitimately
engineering and stays.

Evidence:

- `xFactories/codexFactory/scripts/review_lane/` (change-review half of
  2,085 LOC) + `.github/workflows/review-lane-reusable.yml`
- `xFactory/.github/workflows/review-lane.yml` (the aggregation caller
  paying the private-sibling token cost)

Domain-local exclusions: `pr:`/`candidate:` target types, PR verdict
vocabulary, `merge_master`, the execution lane.
