# Customer Hermes Memory Model

Status: shared xFactory standard
Repository context: openxFactory
Purpose: define the canonical memory and identity objects owned by the
Customer Hermes layer, including Patient Hermes in MedxFactory.

Implementation architecture: see
[xFactory Memory Gateway Architecture](customer-memory-gateway-architecture.md)
for the product-neutral gateway, rails, provider profile, GBrain adapter, and
Hermes wiring model. That gateway also governs Omnigent expert memory and
external knowledge DB access through the same context-packet and provider-route
pattern. See
[Customer Memory Fill And Maintenance Taxonomy](customer-memory-fill-maintenance-taxonomy.md)
for the general fill and maintenance modes every DomainxFactory must map.

## 1. Core Rule

Customer Hermes owns the customer-subject memory boundary.

```text
Customer Hermes
  owns subject-specific identity, consent, preferences, timeline, evidence,
  current state, active workflow context, memory, follow-up, and promotion
  candidates.

Client Hermes
  owns organization policy, staff, integrations, customer relationships,
  tenant configuration, and local approval gates.

Domain Hermes
  owns reusable domain knowledge, policy, review standards, routing,
  taxonomy, and shared domain memory.

xFactory
  owns the contract for gates, traceability, source authority, promotion,
  credentials, routing, memory/knowledge provider bindings, state transitions,
  and audit.
```

Customer Hermes may specialize by domain:

| Domain | Customer Hermes alias | Customer subject |
| --- | --- | --- |
| MedxFactory | Patient Hermes | patient, case, episode, care context |
| OpsxFactory | Managed System Hermes | tenant, system, service, vault, endpoint fleet |
| AdxFactory | Buyer or Campaign Hermes | buyer, audience, campaign, account |
| LedgerxFactory | Ledger or Client Hermes | ledger, entity, filing, account |
| codexFactory | Project Hermes | project, repo, feature, deployment |

The alias may change, but the object model stays recognizable.

## 2. Canonical Object Set

Every Customer Hermes implementation should support these object families.

```text
identity profile
consent profile
preference profile
timeline
evidence graph
source claim
current state snapshot
memory item
active workflow context
follow-up obligation
promotion candidate
```

These objects are not all the same kind of memory. Some describe the subject,
some describe evidence, some describe active work, and some describe whether
information may move to another layer.

```text
identity profile
  -> anchors the customer subject

consent profile + preference profile
  -> constrain use, sharing, communication, and action

source claim + evidence graph
  -> explain what is known and why

timeline + current state snapshot
  -> summarize what happened and what is true now

memory item
  -> durable subject-specific memory

active workflow context + follow-up obligation
  -> track open work and commitments

promotion candidate
  -> requests movement from customer memory to client or domain memory
```

## 3. Shared Fields

All canonical objects should carry these shared fields when practical.

```yaml
object_id: <stable-id>
object_type: <canonical-object-type>
schema_version: 1
customer_subject_ref: <customer-subject-ref>
owning_layer: customer_hermes
domain_ref: <domain-id>
client_ref: <client-or-tenant-ref>
created_at: <timestamp>
updated_at: <timestamp>
created_by: <actor-or-system-ref>
source_refs: []
authority_level: <L0|L1|L2|L3|L4|L5>
confidence: <unknown|low|medium|high>
privacy_class: <public|client_private|customer_private|regulated|restricted>
retention_policy_ref: <policy-ref>
audit_refs: []
status: <draft|active|superseded|revoked|archived>
```

Authority levels should follow the shared source authority ladder:

```text
L0 unknown or uncited
L1 user-stated or AI-inferred
L2 cited secondary source
L3 ground-source verified current state
L4 Hermes-reviewed truth
L5 operational policy or approved action state
```

## 4. Identity Profile

The identity profile anchors the customer subject. It should identify the
subject without turning Customer Hermes into the source of every external
system identifier.

```yaml
identity_profile:
  object_id: identity.patient_123.v1
  object_type: identity_profile
  customer_subject_ref: patient://pseudonymous-123
  subject_kind: patient
  display_label: <human-safe-label>
  external_identifiers:
    - system_ref: ehr
      identifier_ref: ehr-patient-id-reference
      identifier_value_stored: false
  relationship_refs:
    - care_relationship://clinic-a/patient-123
  aliases: []
  demographic_or_subject_attributes: []
  identity_resolution:
    match_status: confirmed
    matched_by: <actor-or-system-ref>
    evidence_refs: []
  privacy_class: regulated
```

Rules:

- Store references to external identifiers when possible, not raw identifiers.
- Keep identity resolution evidence separate from broad domain memory.
- Domain overlays may add fields, but must preserve `subject_kind`,
  `external_identifiers`, and `identity_resolution`.

## 5. Consent Profile

The consent profile defines what may be accessed, used, shared, retained, or
acted on for the customer subject.

```yaml
consent_profile:
  object_id: consent.patient_123.v3
  object_type: consent_profile
  customer_subject_ref: patient://pseudonymous-123
  consent_status: granted
  scope:
    allowed_uses:
      - care_navigation
      - record_review
    prohibited_uses:
      - external_research
    allowed_source_families:
      - ehr
      - lab_portal
    allowed_recipients:
      - care_team
    sharing_constraints:
      deidentification_required_for_domain_promotion: true
  effective_from: <timestamp>
  effective_until: <timestamp-or-null>
  revoked_at: null
  consent_evidence_refs: []
  renewal_required: false
```

Rules:

- Consent gates memory retrieval, source access, customer-facing action, and
  promotion.
- Revoked consent must block new use unless an explicit legal, safety, or
  contractual exception is recorded by the owning Hermes layer.
- Privileged action consent is separate from credential approval.

## 6. Preference Profile

The preference profile records subject-specific preferences that should shape
communication, routing, burden, timing, language, accessibility, and outcomes.

```yaml
preference_profile:
  object_id: preferences.patient_123.v2
  object_type: preference_profile
  customer_subject_ref: patient://pseudonymous-123
  communication:
    preferred_channels: []
    language: en
    accessibility_needs: []
    message_tone: plain_language
  scheduling_or_timing: []
  burden_or_risk_preferences: []
  escalation_preferences: []
  domain_specific_preferences: []
  preference_evidence_refs: []
```

Rules:

- Preferences guide recommendations and communication; they do not override
  domain safety, legal constraints, client policy, or required review.
- Preference conflicts should be represented explicitly, not silently merged.

## 7. Timeline

The timeline records subject-scoped events in time order. It is an index over
events, not a dumping ground for raw records.

```yaml
timeline:
  object_id: timeline.patient_123.primary
  object_type: timeline
  customer_subject_ref: patient://pseudonymous-123
  events:
    - event_id: event_001
      event_type: encounter
      occurred_at: <timestamp-or-date-range>
      recorded_at: <timestamp>
      summary: <short-summary>
      actors: []
      source_claim_refs: []
      related_workflow_refs: []
      confidence: high
      privacy_class: regulated
```

Rules:

- Timeline events must point to source claims or approved memory items.
- Uncertain dates should be represented as ranges or uncertainty notes.
- Timeline updates should be append-friendly and auditable.

## 8. Source Claim

A source claim is an atomic claim extracted from a cited source.

```yaml
source_claim:
  object_id: claim.patient_123.lab_001
  object_type: source_claim
  customer_subject_ref: patient://pseudonymous-123
  claim_type: observation
  claim_text: <short-canonical-claim>
  source_ref: source://ehr/lab-result-001
  source_location_ref: <page-row-field-or-message-ref>
  extracted_by: <actor-or-system-ref>
  extraction_method: deterministic
  authority_level: L3
  confidence: high
  conflicts_with: []
  supersedes: []
```

Rules:

- A source claim should be small enough to evaluate, verify, conflict-check,
  and supersede.
- AI-inferred claims stay below L3 until grounded in a source and reviewed as
  required.

## 9. Evidence Graph

The evidence graph connects source claims, memory items, timeline events,
current state assertions, hypotheses, decisions, and workflow outcomes.

```yaml
evidence_graph:
  object_id: evidence_graph.patient_123.primary
  object_type: evidence_graph
  customer_subject_ref: patient://pseudonymous-123
  nodes:
    - node_id: claim.patient_123.lab_001
      node_type: source_claim
  edges:
    - edge_id: edge_001
      from: claim.patient_123.lab_001
      to: state.patient_123.current
      relation: supports
      strength: high
      rationale: <short-rationale>
  unresolved_conflicts: []
  review_state: needs_review
```

Rules:

- The evidence graph should preserve conflicting evidence.
- A current state snapshot should reference the evidence graph instead of
  flattening uncertainty away.

## 10. Current State Snapshot

The current state snapshot is a dated summary of what Customer Hermes currently
believes is true about the subject for a defined purpose.

```yaml
current_state_snapshot:
  object_id: state.patient_123.2026_07_03T090000Z
  object_type: current_state_snapshot
  customer_subject_ref: patient://pseudonymous-123
  purpose: care_navigation
  generated_at: <timestamp>
  state_items:
    - state_id: state_item_001
      summary: <current-state-summary>
      source_claim_refs: []
      evidence_graph_refs: []
      authority_level: L4
      confidence: medium
      uncertainty: <known-uncertainty>
      stale_after: <timestamp-or-null>
  open_questions: []
  blocked_by: []
```

Rules:

- Current state is purpose-bound and time-bound.
- Stale or uncertain state must be visible to downstream workflows.
- Operational action should use a snapshot ID, not an unversioned memory query.

## 11. Memory Item

A memory item is durable customer-subject memory that has passed the domain's
write rules.

```yaml
memory_item:
  object_id: memory.patient_123.prefers_morning_calls.v1
  object_type: memory_item
  customer_subject_ref: patient://pseudonymous-123
  memory_kind: preference
  summary: <memory-summary>
  normalized_value: {}
  source_claim_refs: []
  consent_profile_ref: consent.patient_123.v3
  write_basis: source_backed
  update_policy: replace_on_newer_source
  expires_at: null
  domain_visibility: customer_private
```

Rules:

- Memory writes need a write basis: user-stated, source-backed,
  Hermes-reviewed, or policy-approved.
- Raw documents, transcripts, credentials, and unrestricted private records are
  not memory items.
- Memory retrieval must be filtered by consent, purpose, workflow, and actor.

## 12. Active Workflow Context

Active workflow context binds customer memory to work currently in flight.

```yaml
active_workflow_context:
  object_id: workflow_context.patient_123.referral_001
  object_type: active_workflow_context
  customer_subject_ref: patient://pseudonymous-123
  workflow_ref: workflow://referral-review/001
  workflow_state: awaiting_review
  requested_outcome: <outcome>
  current_state_snapshot_ref: state.patient_123.2026_07_03T090000Z
  consent_profile_ref: consent.patient_123.v3
  required_approvals: []
  assigned_roles: []
  allowed_actions: []
  blocked_actions: []
  credential_requirement_refs: []
  audit_refs: []
```

Rules:

- Active context should declare what may be read, what may be changed, and what
  approval is missing.
- Omnigent workers should receive bounded context packets derived from this
  object, not unrestricted customer memory.
- Omnigent expert knowledge packets use the same xFactory gateway, but they are
  expert-scoped and do not change the Customer Hermes object model.

## 13. Follow-Up Obligation

A follow-up obligation records a commitment, reminder, monitoring need,
handoff, unanswered question, or required review.

```yaml
follow_up_obligation:
  object_id: followup.patient_123.lab_recheck_001
  object_type: follow_up_obligation
  customer_subject_ref: patient://pseudonymous-123
  obligation_type: review
  description: <what-must-happen>
  owner_ref: <role-or-person-ref>
  due_at: <timestamp-or-null>
  trigger_conditions: []
  related_workflow_refs: []
  related_memory_refs: []
  status: open
  closure_evidence_refs: []
```

Rules:

- Follow-up obligations should not be hidden inside free text memory.
- Closing an obligation requires evidence or an explicit cancellation reason.

## 14. Promotion Candidate

A promotion candidate is a request to move customer-scoped learning into client
or domain memory.

```yaml
promotion_candidate:
  object_id: promotion.patient_123.workflow_gap_001
  object_type: promotion_candidate
  customer_subject_ref: patient://pseudonymous-123
  proposed_target_layer: domain_hermes
  proposed_target_memory_kind: workflow_lesson
  source_memory_refs: []
  source_claim_refs: []
  deidentification_required: true
  consent_profile_ref: consent.patient_123.v3
  client_review_required: true
  domain_review_required: true
  rationale: <why-this-should-be-promoted>
  promotion_status: proposed
  decision_refs: []
```

Rules:

- Nothing silently moves from Customer Hermes to Client Hermes or Domain
  Hermes.
- Customer-to-domain promotion requires consent and de-identification when
  required by domain policy.
- Rejected promotion candidates remain useful audit evidence.

## 15. Read And Write Path

Customer Hermes memory should be accessed through bounded context packets.

```text
workflow asks for customer context
  -> active workflow context identifies purpose and scope
  -> consent profile filters allowed use
  -> memory retrieval filters by privacy, purpose, actor, and authority
  -> current state snapshot is generated or selected
  -> xFactory records trace refs in the job envelope
  -> Omnigent receives bounded context, not raw memory
```

The same gateway pattern applies when Omnigent needs expert knowledge:

```text
workflow asks for expert knowledge context
  -> Domain Hermes policy identifies the expert profile and allowed use
  -> xFactory source-authority rail filters external knowledge DBs
  -> expert provider route retrieves source-scoped candidates
  -> xFactory emits bounded expert context with source refs and audit refs
  -> Omnigent receives expert context, not raw DB access
```

Customer Hermes memory and Omnigent expert memory may appear in the same
workflow, but they remain different authority scopes. Customer Hermes owns
customer-subject truth. Domain Hermes owns reusable expert truth. xFactory owns
the gates, provider bindings, migrations, and audit trail between them.

Writes follow a similar path:

```text
source or workflow produces evidence
  -> source claim is created
  -> evidence graph is updated
  -> timeline event or memory item is proposed
  -> Hermes write policy reviews if required
  -> current state snapshot is refreshed
  -> follow-up or promotion candidate is created when needed
```

## 16. Minimum Domain Implementation

A DomainxFactory should at least define:

- customer subject kinds
- identity profile extensions
- consent profile extensions
- preference profile extensions
- allowed memory kinds
- allowed source claim types
- evidence graph relation vocabulary
- current state snapshot purposes
- workflow context fields
- follow-up obligation types
- promotion candidate targets and review policy

For MedxFactory, Patient Hermes should specialize these objects for patient
identity, care relationships, consent, clinical preferences, encounter
timeline, patient evidence graph, case state snapshot, patient memory,
care workflow context, follow-up obligations, and de-identified promotion to
medical domain memory.
