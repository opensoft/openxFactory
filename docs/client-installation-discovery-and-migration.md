# Client Installation Discovery And Workflow Migration

Status: shared xFactory standard
Repository context: openxFactory
Purpose: define how Client Hermes may use an installing company's document
management system, historical email, and related collaboration records to
configure an installation without preserving bad current practice as the target
operating model.

## 1. Core Rule

Client installation discovery should treat the client's documents and past
emails as evidence of current state, not as proof of best practice.

```text
client documents and email
  -> current-state evidence
  -> source trace
  -> workflow map
  -> gap review against domain and client standards
  -> migration plan
  -> Hermes-approved target workflow
```

The installer should learn what the client really does today. It should not
silently copy that behavior into the new xFactory deployment.

This discovery workflow runs inside the
[openxFactory Installation Spine And Domain Overlays](openxfactory-installation-spine.md)
model. openxFactory owns the general control plane. Domain repos such as
MedxFactory or LedgerxFactory may supplement, replace, constrain, or veto
specific installation stages when domain expertise changes the correct answer.
They must still emit the required openxFactory installation artifacts.

## 2. Why This Matters

Client documents and emails are valuable because they show real operating
patterns:

- how customers request help
- who receives requests
- who actually approves exceptions
- which templates staff reuse
- which systems are touched
- where handoffs stall
- which rules are written versus merely tribal
- which customer communications are common
- where escalations, complaints, rework, and delays occur

They are risky because they may also encode:

- outdated SOPs
- skipped approvals
- informal workarounds
- overbroad access
- missing customer consent
- untracked commitments
- staff-specific tribal knowledge
- inconsistent customer communication
- unsafe, noncompliant, or low-quality practice

The solution is not to ignore the records. The solution is to separate
discovery from adoption.

## 3. Allowed Source Families

Client Hermes may use these source families during installation when the client
authorizes scoped, read-only access:

| Source family | Useful for | Guardrail |
| --- | --- | --- |
| Document management | SOPs, templates, checklists, policy binders, client-facing forms, implementation guides. | Treat stale or duplicate documents as unresolved until owner and effective date are confirmed. |
| Historical email | Real request patterns, approvals, customer wording, exception handling, staff routing, bottlenecks. | Mine metadata and representative threads; do not dump raw mail into repo artifacts. |
| Ticketing or case systems | Status models, queues, handoffs, SLAs, common issue classes. | Verify whether the ticket state reflects actual completion or only administrative closure. |
| Shared drives and collaboration spaces | Working templates, local job aids, current team habits. | Distinguish official policy from convenient local copies. |
| CRM or customer notes | Relationship stages, account ownership, service history, customer commitments. | Keep customer-specific memory inside the customer or client boundary. |
| Calendar and scheduling records | capacity, service windows, recurring review cadence, handoff meetings. | Use aggregate patterns unless a workflow needs named approver references. |

Forbidden installation inputs remain forbidden: raw credentials, refresh tokens,
private keys, production connection strings, unrestricted customer records, and
unapproved private data exports.

## 4. Authority Model

The source-authority distinction must be explicit.

| Claim type | Example | Maximum authority before review |
| --- | --- | --- |
| Observed current practice | "Requests usually arrive by email and Jane approves exceptions." | `L3_ground_source_verified_current_state` |
| Written client policy | "The SOP says manager approval is required above $5,000." | `L3_ground_source_verified_current_state` |
| Accepted client policy | "Client Hermes accepts this as current local policy." | `L4_hermes_reviewed_truth` |
| Target operational rule | "The new workflow blocks above $5,000 until manager approval." | `L5_operational_policy` |
| Domain best practice | "The domain standard requires separation of requester and approver." | `L5_operational_policy` when owned by Domain Hermes |

Client documents and email can prove what happened or what was written. They do
not prove that the practice is safe, compliant, efficient, or approved for the
new installation.

## 5. Installation Discovery Pipeline

Use this pipeline for client installation.

```text
1. Source inventory
2. Access and consent scope
3. Sampling plan
4. Evidence extraction
5. Current workflow map
6. Workflow definition packet
7. User validation walkthrough
8. Best-practice comparison
9. Gap and risk classification
10. Migration plan
11. Workflow-change consent
12. Client Hermes approval
13. Domain Hermes review when domain standards change or high risk appears
14. Target workflow generation
15. Dry-run and cutover
```

The pipeline is the openxFactory installation spine for Client Hermes. Domain
overlays may specialize a stage, but they must preserve source traceability,
current-state versus target-state separation, workflow-change consent, and the
shared artifact families.

### 5.1 Source Inventory

Record the systems, folders, mailbox scopes, date windows, document types, and
owners. The install should prefer narrow, representative source sets over
unbounded ingestion.

### 5.2 Evidence Extraction

Extract structured claims:

- workflow name
- trigger
- customer or subject type
- current input artifacts
- current output artifacts
- staff roles
- actual approvers
- exception paths
- systems touched
- customer communications
- observed timing
- source references
- confidence
- unresolved ambiguity

### 5.2.1 How Resources Become Flow

Use a hybrid method. Deterministic algorithms build the evidence graph and
candidate process graph. AI helps extract and normalize meaning from messy
documents and messages.

Deterministic steps:

- parse source metadata, including sender, recipient, timestamp, document owner,
  ticket status, folder, revision date, attachment links, case IDs, customer IDs,
  and system references
- normalize entities, including people, roles, departments, customers, systems,
  products, services, and request types
- group related resources into candidate cases or workflow instances by thread,
  ticket, customer, subject, document link, time window, and referenced IDs
- create an event ledger with timestamped events such as request received,
  information requested, approval requested, approval granted, work assigned,
  customer messaged, exception raised, completed, rejected, or reopened
- infer candidate edges by temporal order, explicit references, ticket
  transitions, reply chains, assignment changes, attachments, and status changes
- compute frequencies, durations, loops, missing approvals, common variants, and
  bottlenecks

AI-assisted steps:

- classify unstructured text into workflow activities, intents, decisions,
  exceptions, approvals, customer messages, and implied handoffs
- map synonyms to the same activity, such as "send to manager", "needs manager
  OK", and "route for approval"
- identify likely missing steps or undocumented handoffs as hypotheses
- summarize variants and explain why a candidate workflow was inferred
- draft current-state diagrams, target-state candidates, and user-facing
  walkthrough explanations

AI output remains a hypothesis until backed by source references and accepted by
the workflow owner or affected users. The authoritative workflow packet is the
structured record with source links, confidence, unresolved questions, and
validation status.

### 5.3 Current Workflow Map

The current workflow map describes how the client operates today. It may include
bad practices. Label it as `current_state`, not `target_state`.

### 5.4 Workflow Definition Packet

Convert extracted resources into a draft workflow definition packet before any
best-practice migration work starts.

The packet should define:

- workflow name and purpose
- offer, product, service, or customer-subject it supports
- trigger events
- entry criteria
- actors and user groups
- requester, doer, reviewer, approver, and escalation roles
- current states
- allowed transitions
- decision points and approval gates
- source artifacts used at each step
- systems touched
- customer-facing messages
- completion criteria
- exception paths
- unresolved questions
- evidence confidence

The packet must include a source trace for each step. If different sources
conflict, the packet should preserve the conflict and route it to a validation
walkthrough instead of guessing.

### 5.5 User Validation Walkthrough

Before comparing to best practice, the affected users or workflow owner should
validate the current-state map.

The avatar should walk users through:

- "This is what we think happens today."
- "These are the emails, documents, tickets, or records that support it."
- "These steps conflict or are unclear."
- "These approvals appear informal or missing."
- "These steps look risky before automation."

The conventional console should show the same packet as a table, timeline, or
state diagram with source links and confidence levels.

The output is a validated current-state workflow, not consent to change it.

Visualization candidates for this walkthrough are tracked in
[Workflow Visualization Tooling Exploration](workflow-visualization-tooling-exploration.md).

### 5.6 Best-Practice Comparison

Compare the current workflow against:

- openxFactory workflow and gate requirements
- domain Hermes standards
- Client Hermes policy and risk tolerance
- legal, compliance, privacy, and professional authority boundaries
- security and credential-minimization rules
- customer-facing communication standards
- operational quality targets

### 5.7 Gap And Risk Classification

Every mismatch gets a gap record. Use these dispositions:

| Disposition | Meaning |
| --- | --- |
| `adopt_as_is` | Current practice matches target standard and can be configured directly. |
| `configure_variant` | Current practice is valid but needs domain-specific or client-specific configuration. |
| `migrate_to_best_practice` | Current practice works operationally but is weaker than the target standard. |
| `contain_temporarily` | Current practice may continue only under extra controls during transition. |
| `quarantine` | Current practice is too risky to automate or recommend. |
| `reject` | Current practice must not be carried into the installation. |

### 5.8 Workflow-Change Consent

Migrating to best practice changes how people work. The install must get
explicit consent before cutting over from current practice to target practice.

Consent is separate from source access. A client may consent to analyze email and
documents without consenting to change workflows.

Workflow-change consent should confirm:

- which current workflow is changing
- which target workflow will replace or constrain it
- why the change is recommended
- which users or roles are affected
- which old steps will be retired
- which steps will be automated, blocked, or moved to approval
- what training or communication will be provided
- when dual-run, shadow-run, or cutover starts
- what rollback or repair path exists
- who may approve the change
- whether affected users were notified, trained, or asked to acknowledge

If consent is missing, the target workflow may remain a recommendation, draft,
or shadow-run. It must not become the enforced workflow.

## 6. Migration Ladder

Bad current practice should move through a controlled ladder.

```text
observe
  -> contain
  -> map target
  -> design migration
  -> dual-run or shadow-run
  -> approve cutover
  -> retire old practice
  -> monitor drift
```

### Observe

Capture what the client does today with source references. Do not judge or
change behavior yet.

### Contain

If the current practice is risky but still operating, add temporary guardrails:

- require human review
- keep automation read-only
- block external send/write actions
- narrow credential grants
- require manual approval for exceptions
- add audit notes

### Map Target

Describe the target workflow using domain best practice and client constraints.
Keep target behavior separate from the current-state map.

### Design Migration

Define the migration path:

- old step
- target step
- difference
- reason for change
- affected roles
- data or template changes
- training or communication need
- transition controls
- success metric
- cutover condition
- rollback or repair path

### Dual-Run Or Shadow-Run

For high-risk workflows, run the new workflow beside the old workflow first.
Compare outputs, timing, exception rates, and staff friction before cutover.

### Approve Cutover

Client Hermes approves local operating adoption. Domain Hermes reviews when the
change touches reusable domain standards, regulated practice, high-risk action,
or domain memory promotion.

Cutover approval must reference the workflow-change consent record. For material
workflow changes, approval should come from both the accountable client approver
and the workflow owner or affected user representative.

### Retire Old Practice

Deprecated workflow variants should be explicitly blocked or hidden after
cutover. The avatar may explain the change, but the conventional console should
show the old practice as retired.

### Monitor Drift

After cutover, monitor for staff reverting through email, ad hoc documents, or
manual side channels. Treat drift as either a training gap, policy gap, tooling
gap, or target workflow defect.

## 7. Agent Scaffold

Add these Client Hermes roles for installation discovery:

| Agent | Purpose |
| --- | --- |
| Source Inventory Agent | Catalogs document, email, ticket, CRM, calendar, and collaboration sources approved for installation discovery. |
| Evidence Extraction Agent | Converts source material into cited workflow claims without promoting claims to policy. |
| Workflow Mapper Agent | Builds current-state workflow maps from observed documents, emails, and system records. |
| Workflow Definition Agent | Converts current-state claims into a workflow definition packet with states, transitions, roles, artifacts, systems, and confidence. |
| Practice Gap Auditor | Compares current-state workflows to domain standards, client policy, security rules, and customer-facing expectations. |
| Migration Planner Agent | Produces migration ladders, dual-run plans, transition controls, and cutover criteria. |
| Consent And Adoption Gatekeeper | Collects workflow-change consent and blocks cutover when affected-user or client approval is missing. |
| Change Adoption Coach | Helps staff understand the target workflow and drafts training, handoff, and customer communication materials. |
| Drift Monitor Agent | Watches post-cutover evidence for return to retired practices or new workarounds. |

These are role definitions. They may be implemented as prompts, deterministic
services, review queues, or human-assisted workflows.

## 8. Skill Scaffold

Installation discovery should add these skills:

```text
source_inventory
  find approved source systems, owners, date windows, and access boundaries

document_sop_extraction
  extract SOPs, templates, checklists, policy claims, and ownership metadata

email_workflow_mining
  reconstruct request, approval, exception, and customer communication patterns

workflow_trace_reconstruction
  connect documents, emails, tickets, and system records into current-state flows

workflow_definition_packet
  define states, transitions, roles, gates, artifacts, systems, and completion criteria

practice_gap_analysis
  compare current practice with domain and client target standards

migration_plan_design
  design containment, dual-run, cutover, retirement, and monitoring steps

workflow_change_consent
  collect explicit consent to replace, constrain, automate, or retire current practice

change_communication
  explain why the target workflow differs from current practice

drift_monitoring
  detect post-cutover reversion or new workaround patterns
```

## 9. User Interaction Pattern

Use avatar UI when the work is explanatory or change-management heavy:

- "Show me how we think this workflow works today."
- "Why is this current practice risky?"
- "What is the recommended target workflow?"
- "What will change for staff?"
- "What do we need the client to approve?"
- "Who needs to consent before we change this workflow?"
- "What can we automate now, and what must stay manual?"

Use conventional UI when the user needs dense review:

- source inventory
- evidence claim table
- current-state workflow map
- best-practice gap matrix
- migration backlog
- consent and acknowledgement register
- cutover checklist
- drift and exception dashboard
- audit trace search

## 10. Required Records

Every installation discovery should support these record families:

```yaml
installation_source_inventory:
  source_id: string
  source_family: document_management | email | ticketing | crm | calendar | collaboration
  owner_ref: string
  access_scope: read_only | metadata_only | sampled_read
  date_window: string
  retention_rule: string
  approved_by: string

workflow_evidence_claim:
  claim_id: string
  workflow_ref: string
  claim_type: current_step | policy | approver | exception | artifact | communication
  source_refs: []
  authority_level: L0 | L1 | L2 | L3 | L4 | L5
  confidence: low | medium | high
  current_state_only: true
  unresolved_questions: []

workflow_definition_packet:
  workflow_ref: string
  status: draft_current_state | user_validated_current_state | target_candidate | approved_target
  trigger_events: []
  actors: []
  states: []
  transitions: []
  approval_gates: []
  artifacts: []
  systems_touched: []
  customer_messages: []
  completion_criteria: []
  exception_paths: []
  source_claim_refs: []
  unresolved_questions: []

practice_gap:
  gap_id: string
  workflow_ref: string
  current_claim_refs: []
  target_standard_refs: []
  risk_level: low | medium | high | critical
  disposition: adopt_as_is | configure_variant | migrate_to_best_practice | contain_temporarily | quarantine | reject
  rationale: string

workflow_migration_plan:
  plan_id: string
  workflow_ref: string
  current_state_refs: []
  target_state_refs: []
  containment_controls: []
  dual_run_required: boolean
  cutover_criteria: []
  retired_practices: []
  rollback_or_repair_path: string
  approval_refs: []

workflow_change_consent:
  consent_id: string
  workflow_ref: string
  consent_type: source_analysis | current_state_validation | workflow_change | cutover
  consenting_party_ref: string
  consenting_party_role: client_approver | workflow_owner | affected_user_representative | domain_reviewer | customer_subject
  affected_user_groups: []
  current_workflow_ref: string
  target_workflow_ref: string
  changes_approved: []
  training_or_notice_required: []
  effective_window: string
  rollback_or_repair_acknowledged: boolean
  consent_status: requested | granted | denied | expired | withdrawn
  evidence_refs: []
```

## 11. Validation Rules

Validation should fail when:

- a target workflow is generated directly from email or document mining without a
  gap review
- a current-state claim is marked `L5_operational_policy` without Hermes approval
- a bad-practice gap has no disposition
- a high-risk gap lacks containment controls
- a cutover plan lacks approver references
- a target workflow lacks a workflow definition packet
- a migration plan lacks a current-to-target delta
- a workflow change is enforced without workflow-change consent
- affected users are materially impacted without notice, training, acknowledgement,
  or representative approval according to client policy
- raw email exports or private records are written into repo artifacts
- customer-specific facts are promoted to domain memory without approved
  de-identification and review

The installation can be fast, but it cannot confuse discovery with adoption.
