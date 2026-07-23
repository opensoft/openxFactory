# xFactory Memory Gateway Architecture

Status: ratified
Kind: architecture
Ratified by: add-customer-memory-gateway-architecture (archived 2026-07-08)
Repository context: openxFactory
Related models:
[Subject Hermes Memory Model](customer-hermes-memory-model.md),
[Customer Memory Fill And Maintenance Taxonomy](customer-memory-fill-maintenance-taxonomy.md),
[xFactory Domain Factory Model](xfactory-domain-factory-model.md)
Purpose: organize the implementation architecture for Subject Hermes brain,
memory, and personality, and for Omnigent expert memory and knowledge access,
without binding xFactory to a single memory or knowledge product.

## 1. Summary

Subject Hermes needs a durable, governed brain for each customer subject:
Patient Hermes for a patient, Managed System Hermes for a tenant or service,
Project Hermes for a software project, Campaign Hermes for a campaign, and so
on.

Domain Omnigent needs the same gateway pattern for expert memory and external
knowledge DBs: root-truth corpora, playbooks, case-pattern stores, evaluation
memory, source workspaces, vector indexes, graph stores, and future specialist
expert systems.

The implementation must cover identity, consent, preferences, timeline,
evidence, current state, memory, workflow context, follow-up, and promotion.
Those concerns should be implemented as xFactory contracts and rails first.
Products such as GBrain, Honcho, AgentMemory, Postgres, graph databases, vector
stores, source workspaces, knowledge DBs, or future systems should map into
those contracts through adapters.

The fill and maintenance taxonomy defines how information enters and changes
Subject Hermes memory. This gateway defines how those candidate writes,
refreshes, corrections, promotions, and migrations are gated and routed.

```text
Memory and knowledge products store and retrieve.
xFactory governs access and movement.
Hermes owns decisions.
Subject Hermes owns customer-subject truth.
Domain Hermes owns reusable domain truth.
Omnigent owns bounded expert execution.
Omnigent receives bounded customer and expert context packets.
External expert DBs are provider-backed resources, not the authority boundary.
```

## 2. Goal Versus Implementation

The customer and expert memory system should be organized in layers:

```text
Goal
  what Subject Hermes must accomplish for the customer subject

Canonical model
  stable Subject Hermes objects, expert knowledge objects, and authority
  boundaries

Gateway ports
  product-neutral operations for read, write, context, promotion, revoke, audit

Rails
  policy checks before memory reaches a provider or a caller

Provider profiles
  declarations of what each product can support natively or through adapters

Provider adapters
  concrete mappings to GBrain, Honcho, AgentMemory, Postgres, graph, vector,
  knowledge DBs, source workspaces, etc.
```

This keeps the architecture portable. A DomainxFactory can use GBrain today and
swap or augment it later without changing the Subject Hermes authority model
or the Omnigent expert call surface.

## 3. Placement In The Stack

```text
Hermes role, council, agent, or Omnigent expert
  -> xFactory Memory Gateway
       -> identity rail
       -> consent rail
       -> source authority rail
       -> privacy and redaction rail
       -> workflow scope rail
       -> promotion rail
       -> audit rail
       -> provider adapter
            -> GBrain, Honcho, AgentMemory, Postgres, graph, vector,
               knowledge DB, source workspace, etc.
```

Hermes should not call a memory provider directly for governed memory. Hermes
should call xFactory memory tools, and xFactory should decide whether the
provider may be used for that operation.

Omnigent should follow the same rule for governed expert memory and external
knowledge DBs. An expert worker should request a bounded expert context packet
or expert query through xFactory, not attach directly to an unrestricted root
truth DB, vector index, graph DB, source workspace, or case-pattern store.

Direct provider calls may exist only for bootstrap, health checks, or
diagnostics using separate operator-scoped credentials that are read-only and
bound to non-production or shadow namespaces. They never create approved
Subject Hermes memory or authoritative expert context.

## 4. Framework Components

The xFactory Memory Gateway is a framework layer, not one service with one
database. A deployment may implement the pieces in-process with Hermes, as an
xFactory control-plane service, or as a small standalone gateway. The component
boundaries should stay stable either way.

| Component | Responsibility | Sync Path |
| --- | --- | --- |
| Gateway API | Receives `xfactory.memory.*` requests from Hermes, Omnigent, tools, or admin jobs. | Yes |
| Request Normalizer | Converts caller input into a canonical gateway request with subject, purpose, workflow, layer, and operation. | Yes |
| Rail Engine | Runs auth, subject safety, consent, privacy, source authority, workflow scope, retention, budget, and provider eligibility checks. | Yes |
| Context Packet Builder | Produces bounded customer or expert context packets with redaction metadata, trace refs, current state snapshot refs, knowledge-source refs, and uncertainty. | Yes |
| Provider Router | Selects provider route by role, layer, domain, client, customer subject, workflow, and migration state. | Yes |
| Provider Adapter | Maps canonical operations to GBrain, Honcho, AgentMemory, Postgres, graph, vector, knowledge DB, source workspace, or other product APIs. | Yes |
| Credential Grant Resolver | Requests short-lived provider grants from the credential broker using binding refs, never raw secrets. | Yes |
| Audit Ledger | Records allowed and denied operations, provider refs, traceability, policy versions, and migration state. | Mostly async, denial records sync |
| Usage Meter | Records billable usage events and budget counters without storing memory content. | Mostly async, budget checks sync |
| Migration Orchestrator | Runs backfill, dual-write, shadow-read, canary, cutover, rollback, and provider mapping updates. | Async jobs, route checks sync |
| Provider Registry | Stores provider profiles, bindings, route tables, health, cost class, and feature support. | Yes |
| Knowledge Source Registry | Stores expert DB, corpus, source workspace, source authority, citation, freshness, and allowed-use metadata. | Yes |
| Cache | Caches policy, consent, route, provider health, and context packets using versioned invalidation. | Yes |

The sync path should stay small. Anything not needed to decide whether the
memory operation may safely proceed should move to an async ledger or job.

## 5. Request Contract

Every gateway operation should normalize to the same request frame.

```yaml
gateway_request:
  request_id: memreq-2026-07-03-0001
  operation: context_packet
  caller:
    actor_ref: hermes://role/patient-care-navigator
    consumer_layer: customer_hermes
    hermes_layer: customer_hermes
    authority_refs: []
  scope:
    domain_ref: medx
    client_ref: clinic-a
    customer_subject_ref: patient://pseudonymous-123
    subject_safety_profile_ref: subject_safety.patient_123.v1
    workflow_ref: workflow://referral-review/001
    purpose: care_navigation
  requested_ports:
    - ConsentPort
    - PreferencePort
    - CurrentStatePort
    - MemoryItemPort
  policy_refs:
    consent_profile_ref: consent.patient_123.v3
    subject_safety_policy_ref: subject_safety.medx.minor.v1
    redaction_profile_ref: redaction.patient_safe.v1
    retention_policy_ref: retention.medx.patient.v1
  provider_role_preferences:
    profile_relationship_memory: primary
    group_project_memory: primary
  budget:
    max_latency_ms: 700
    max_billable_units: 50
  trace:
    job_id: JOB-001
    approval_refs: []
```

The same request frame supports Omnigent expert access. The difference is the
consumer layer, provider roles, allowed use, and source-authority requirements.

```yaml
gateway_request:
  request_id: memreq-2026-07-03-1001
  operation: context_packet
  caller:
    actor_ref: omnigent://expert/medx.oncology.diagnostic_reviewer
    consumer_layer: domain_omnigent
    hermes_layer: domain_hermes
    expert_profile_ref: expert://medx/oncology/diagnostic-reviewer
    authority_refs:
      - hermes-approval://domain/diagnostic-review/001
  scope:
    domain_ref: medx
    client_ref: clinic-a
    workflow_ref: workflow://diagnostic-review/001
    purpose: hypothesis_generation
    customer_subject_ref: patient://pseudonymous-123
  requested_ports:
    - ExpertKnowledgePort
    - ExpertCaseMemoryPort
    - SourceAuthorityPort
    - AuditPort
  policy_refs:
    expert_policy_ref: expert_policy.medx.diagnostic_review.v1
    source_authority_policy_ref: source_authority.medx.clinical.v1
    redaction_profile_ref: redaction.patient_safe.v1
    retention_policy_ref: retention.medx.expert_context.v1
  provider_role_preferences:
    expert_knowledge_memory: primary
    expert_case_memory: secondary
  knowledge_scopes:
    - root_truth_db
    - clinical_guideline_corpus
    - case_pattern_memory
  allowed_uses:
    - hypothesis_generation
    - evidence_review
  prohibited_uses:
    - autonomous_clinical_decision
  minimum_source_authority: L3
  budget:
    max_latency_ms: 900
    max_billable_units: 80
  trace:
    job_id: JOB-EXPERT-001
    approval_refs:
      - hermes-approval://domain/diagnostic-review/001
```

The response should be equally explicit.

```yaml
gateway_response:
  request_id: memreq-2026-07-03-0001
  decision: allow
  context_packet_ref: context://packet/001
  provider_calls:
    - provider_role: profile_relationship_memory
      provider_id: honcho
      provider_object_refs: []
    - provider_role: group_project_memory
      provider_id: gbrain
      provider_object_refs: []
  redaction_level: patient_safe
  subject_safety:
    category: adult
    policy_ref: subject_safety.medx.adult.v1
    guardian_or_delegate_required: false
  audit_ref: audit://memory/memreq-2026-07-03-0001
  usage_event_ref: usage://memory/memreq-2026-07-03-0001
  warnings: []
```

Expert context packets should be equally bounded. They may include source refs,
knowledge snippets, retrieval diagnostics, and uncertainty, but they should not
grant the worker unrestricted database access.

```yaml
gateway_response:
  request_id: memreq-2026-07-03-1001
  decision: allow
  context_packet_ref: context://expert-packet/medx/diagnostic-review/001
  consumer_layer: domain_omnigent
  expert_profile_ref: expert://medx/oncology/diagnostic-reviewer
  knowledge_scopes:
    - root_truth_db
    - clinical_guideline_corpus
  source_authority_minimum: L3
  allowed_uses:
    - hypothesis_generation
    - evidence_review
  prohibited_uses:
    - autonomous_clinical_decision
  provider_calls:
    - provider_role: expert_knowledge_memory
      provider_id: medx-root-truth-vdb
      provider_object_refs:
        - vdb://medx/root-truth/chunk/abc123
    - provider_role: expert_case_memory
      provider_id: medx-case-pattern-store
      provider_object_refs: []
  audit_ref: audit://memory/memreq-2026-07-03-1001
  usage_event_ref: usage://memory/memreq-2026-07-03-1001
  warnings:
    - source freshness must be rechecked before final recommendation
```

Denied responses must identify the rail that blocked the request without
leaking prohibited data.

```yaml
gateway_response:
  decision: deny
  denied_by: consent_rail
  denial_code: consent_scope_missing
  safe_message: Consent does not allow this memory use for the requested purpose.
  audit_ref: audit://memory/denial/001
```

## 6. Authentication And Authorization Framework

Authentication has three separate concerns.

```text
caller identity
  who is asking: Hermes role, council, worker, user, service, admin job

subject scope
  what the request applies to: domain, client, tenant, customer subject, workflow

provider credential
  how the selected adapter reaches GBrain, Honcho, AgentMemory, a knowledge DB,
  a source workspace, or another store
```

Hermes should not hold raw provider credentials. xFactory should store provider
binding references and request short-lived grants through the credential broker.

```yaml
memory_provider_binding:
  binding_id: medx-clinic-a-gbrain
  provider_id: gbrain
  provider_role: group_project_memory
  custody: opensoft_hosted
  owner_ref: client://clinic-a
  secret_ref: vault://clinic-a/gbrain-mcp-token
  allowed_layers:
    - client_hermes
    - domain_hermes
  allowed_operations:
    - query
    - write
    - context_packet
  max_grant_minutes: 15
  audit_required: true
```

Expert memory and knowledge providers use the same binding shape, with expert
profile and knowledge-scope constraints added to the allowed route.

```yaml
memory_provider_binding:
  binding_id: medx-root-truth-vdb
  provider_id: medx-root-truth-vdb
  provider_role: expert_knowledge_memory
  custody: opensoft_hosted
  owner_ref: domain://medx
  secret_ref: vault://medx/root-truth-vdb-token
  allowed_layers:
    - domain_omnigent
    - domain_hermes
  allowed_operations:
    - query
    - context_packet
  allowed_expert_profiles:
    - expert://medx/oncology/diagnostic-reviewer
  allowed_knowledge_scopes:
    - root_truth_db
    - clinical_guideline_corpus
  minimum_source_authority: L3
  max_grant_minutes: 10
  audit_required: true
```

Runtime flow:

```text
Hermes or Omnigent calls xfactory.memory.context_packet
  -> xFactory authenticates caller
  -> xFactory authorizes layer + workflow + customer subject
  -> xFactory checks consent, source authority, expert policy, and workflow scope
  -> xFactory selects provider route
  -> xFactory asks credential broker for short-lived provider grant
  -> provider adapter calls provider
  -> xFactory filters response and records audit
```

Provider grants should be scoped to one operation, provider role, domain,
client, customer subject when applicable, and time window.

## 7. Subject Safety And Age/Minor Framework

The gateway should treat adult and child users differently through a
subject-safety rail. This rail is part of xFactory policy, not a memory-provider
feature.

```text
Hermes asks for context or action
  -> xFactory resolves customer subject
  -> subject safety rail resolves age band and protected status
  -> consent and guardian/delegated authority rails run
  -> provider query/write is scoped
  -> context packet is redacted and limited
  -> audit records the applied protection level
```

Subject safety profile:

```yaml
subject_safety_profile:
  profile_id: subject_safety.patient_123.v1
  customer_subject_ref: patient://pseudonymous-123
  subject_category: minor
  age_band: child
  protected_classes:
    - minor
    - patient
  guardian_or_delegate_required: true
  guardian_or_delegate_refs:
    - guardian://parent-001
  allowed_interaction_modes:
    - educational_explanation
    - appointment_support
    - caregiver_mediated_updates
  prohibited_memory_uses:
    - inferred_personality_targeting
    - marketing_personalization
    - autonomous_sensitive_disclosure
  allowed_personalization:
    explicit_preferences_only: true
    inferred_behavioral_personalization: false
  required_approvals:
    - guardian_consent
    - client_policy
    - domain_safety_policy
  redaction_profile_ref: redaction.minor_safe.v1
  retention_policy_ref: retention.minor_sensitive.v1
  audit_level: enhanced
```

Adult profile example:

```yaml
subject_safety_profile:
  profile_id: subject_safety.patient_456.v1
  customer_subject_ref: patient://pseudonymous-456
  subject_category: adult
  age_band: adult
  guardian_or_delegate_required: false
  allowed_interaction_modes:
    - direct_customer_conversation
    - appointment_support
    - preference_capture
  allowed_personalization:
    explicit_preferences_only: false
    inferred_behavioral_personalization: consent_required
  required_approvals:
    - customer_consent
  redaction_profile_ref: redaction.patient_safe.v1
  retention_policy_ref: retention.medx.patient.v1
  audit_level: standard
```

The same pattern applies outside medical domains:

| Domain | Adult Treatment | Minor/Child Treatment |
| --- | --- | --- |
| MedxFactory | direct patient consent where policy allows | guardian/delegate consent, minor-safe redaction, enhanced audit |
| EdxFactory or education overlays | learner consent and school policy | guardian/school authority, classroom-safe context, stricter retention |
| AdxFactory | ordinary preference personalization | no behavioral targeting or marketing personalization unless policy explicitly allows |
| codexFactory | direct project owner or contributor context | restricted student/contributor context if the user is under a protected category |

The subject-safety rail can allow, deny, degrade, or require a different
context packet profile.

```text
adult direct support request
  -> direct consent valid
  -> standard patient-safe packet

minor patient support request
  -> guardian/delegate consent required
  -> minor-safe packet
  -> no inferred personality targeting
  -> enhanced audit
```

Hermes should receive the result as context metadata, not provider-specific
minor handling.

```yaml
context_packet:
  subject_safety:
    category: minor
    age_band: child
    guardian_or_delegate_required: true
    applied_redaction_profile: redaction.minor_safe.v1
    blocked_uses:
      - inferred_personality_targeting
      - autonomous_sensitive_disclosure
```

## 8. Billing And Metering Framework

Billing belongs in the gateway because all governed memory operations pass
through it. The gateway should meter usage without storing memory content in
billing records.

```yaml
memory_usage_event:
  usage_event_id: usage.memreq-2026-07-03-0001
  request_id: memreq-2026-07-03-0001
  bill_to: client://clinic-a
  billing_mode: opensoft_hosted
  domain_ref: medx
  client_ref: clinic-a
  customer_subject_ref_hash: sha256:<hash>
  workflow_ref: workflow://referral-review/001
  provider_id: gbrain
  provider_role: group_project_memory
  operation: context_packet
  read_units: 12
  write_units: 0
  storage_delta_bytes: 0
  latency_ms: 184
  provider_cost_class: standard
  content_stored_in_event: false
```

Billing modes:

| Mode | Provider Cost | xFactory Metering |
| --- | --- | --- |
| `opensoft_hosted` | Opensoft pays provider and bills the client. | Required |
| `customer_owned` | Customer pays provider directly. | Required for reporting, quotas, and support |
| `hybrid` | Customer owns storage, Opensoft bills gateway/orchestration. | Required |
| `internal_dev` | No external billing. | Required for capacity and cost modeling |

Budget checks that can change the operation outcome are sync rails. Usage
aggregation, invoices, reports, and analytics should be async.

```text
under budget
  -> allow

near soft limit
  -> allow, warn Hermes or client

over soft limit
  -> require approval or cheaper route

over hard limit
  -> deny or degraded mode
```

## 9. Migration Framework

Migration is an xFactory responsibility. Hermes should keep calling the same
memory tools while xFactory moves a customer subject, client, domain, or whole
provider role to a new memory model.

```text
Hermes keeps calling:
  xfactory.memory.query
  xfactory.memory.write
  xfactory.memory.context_packet

xFactory changes:
  provider route
  provider mapping
  dual-write policy
  shadow-read policy
  cutover and rollback state
```

Migration relies on stable canonical object IDs. Provider object refs may
change; canonical object IDs should not.

```yaml
provider_mappings:
  canonical_object_id: memory.patient_123.prefers_morning_calls.v1
  mappings:
    - provider_id: gbrain-v1
      provider_object_ref: gbrain://old/abc
      status: read_only
    - provider_id: gbrain-v2
      provider_object_ref: gbrain://new/xyz
      status: active
```

Migration manifest:

```yaml
memory_migration:
  migration_id: mem-mig-medx-clinic-a-patient-hermes-v2
  scope:
    domain_ref: medx
    client_ref: clinic-a
    layer: customer_hermes
    customer_subject_selector: selected
  source_provider_route: gbrain-v1
  target_provider_route: gbrain-v2
  mode: dual_write
  object_contract: openxFactory/customer-hermes-memory-model
  consent_policy: preserve_and_recheck
  verification:
    count_match_required: true
    sample_compare_required: true
    authority_level_preserved: true
    audit_refs_preserved: true
  rollback:
    allowed_until: "2026-08-01T00:00:00Z"
    source_route_kept_read_only: true
```

Migration phases:

```text
plan
  define source, target, scope, policy, verification, rollback

prepare
  verify target provider profile, grants, budget, and companion ports

backfill
  copy canonical objects and provider mappings to target

dual_write
  write new changes to source and target

shadow_read
  read target in parallel and compare quality, latency, and completeness

canary
  route selected subjects or workflows to target

cutover
  make target primary route

rollback_window
  keep source read-only or dual-readable

archive
  tombstone, de-identify, or retire old provider refs according to retention
```

The framework goal is that Subject Hermes stays logically continuous even
when its memory provider changes.

## 10. Runtime Request Flow

### Context Packet

```text
Hermes role requests customer context
  -> Gateway API receives request
  -> Request Normalizer validates operation and scope
  -> Rail Engine checks auth, subject safety, consent, privacy, source authority, workflow, budget
  -> Provider Router selects provider roles and migration route
  -> Credential Grant Resolver obtains short-lived provider grants
  -> Provider Adapters retrieve candidate memories
  -> Context Packet Builder filters, redacts, ranks, and packages memory
  -> Audit Ledger records operation
  -> Usage Meter records billable usage
  -> Hermes receives bounded context packet
```

### Expert Context Packet

```text
Omnigent expert requests expert knowledge context
  -> Gateway API receives request with consumer_layer=domain_omnigent
  -> Request Normalizer validates expert profile, workflow, and purpose
  -> Rail Engine checks auth, expert policy, source authority, privacy, workflow, and budget
  -> Provider Router selects expert knowledge, case, policy, or evaluation routes
  -> Credential Grant Resolver obtains short-lived provider grants
  -> Provider Adapters retrieve source-scoped expert memory and knowledge
  -> Context Packet Builder filters, cites, redacts, ranks, and packages context
  -> Audit Ledger records operation
  -> Usage Meter records billable usage
  -> Omnigent receives bounded expert context packet
```

### Write

```text
Hermes proposes a memory write
  -> Gateway validates canonical object shape
  -> Rail Engine checks writer authority, source refs, subject safety, consent, privacy, secrets
  -> Provider Router applies active route and migration dual-write state
  -> Adapter writes provider representation
  -> Provider mapping is stored or emitted
  -> Audit and usage events are recorded
```

### Promotion

```text
Worker, Hermes role, or user proposes durable learning
  -> Gateway creates promotion candidate
  -> Consent and de-identification rails run
  -> Client or Domain Hermes review is required when policy says so
  -> Approved promotion writes to target layer/provider
  -> Rejected promotion remains audit evidence
```

## 11. Omnigent Expert Memory And Knowledge DB Framework

The Omnigent layer needs external memory and knowledge, but it should not own
the canonical authority boundary for that knowledge. xFactory should maintain
the external provider bindings, route tables, source-authority requirements,
usage metering, migrations, and audit trail. Domain Hermes should own reusable
domain truth, expert policy, review standards, and promotion decisions.

Expert memory uses the same gateway model as Subject Hermes memory, with
different scopes and ports.

```text
customer_subject_memory
  private customer-subject memory owned by Subject Hermes

profile_relationship_memory
  person, organization, relationship, and preference memory

group_project_memory
  shared Hermes group, project, client, or domain memory

worker_local_memory
  short-lived or local Omnigent worker recall, such as AgentMemory

expert_knowledge_memory
  external root-truth DBs, source corpora, vector indexes, graph stores,
  NotebookLM-style source workspaces, and other knowledge substrates

expert_case_memory
  prior cases, examples, simulations, dream DB outputs, and pattern libraries

expert_policy_memory
  expert routing rules, review standards, allowed-use policy, and safety policy

expert_tool_memory
  tool capabilities, playbooks, procedures, runbooks, and operating recipes

expert_evaluation_memory
  benchmarks, eval results, known failures, calibration notes, and test suites
```

The same gateway operation can serve both consumers:

```text
Subject Hermes
  -> xfactory.memory.context_packet
  -> customer context packet

Domain Omnigent expert
  -> xfactory.memory.context_packet
  -> expert context packet
```

The packet changes by consumer layer, but the rails stay shared:

```text
consumer_layer
  customer_hermes | client_hermes | domain_hermes | domain_omnigent

provider_role
  customer_subject_memory | profile_relationship_memory | group_project_memory
  | worker_local_memory | expert_knowledge_memory | expert_case_memory
  | expert_policy_memory | expert_tool_memory | expert_evaluation_memory

source_authority
  required for expert context just like source refs are required for durable
  Subject Hermes memory writes
```

Omnigent writes follow a promotion path:

```text
Omnigent worker observes or infers something
  -> worker_local_memory may store local recall
  -> worker proposes promotion when it should become durable expert memory
  -> xFactory validates source refs, allowed use, privacy, budget, and route
  -> Domain Hermes reviews when policy requires reusable expert truth
  -> approved item writes to expert knowledge, case, policy, tool, or eval store
```

This keeps AgentMemory useful without letting it become an unreviewed expert
truth database. It also lets xFactory migrate expert providers underneath
Omnigent. For example, MedxFactory can move from one root-truth vector DB to a
graph/vector hybrid, or OpsxFactory can split one runbook store into playbook
and evaluation stores, while Omnigent keeps requesting the same expert context
packet operation.

## 12. Implementation Surface

The first implementation should add these repo surfaces.

```text
contracts/memory-gateway/
  gateway-request.schema.yaml
  gateway-response.schema.yaml
  provider-profile.schema.yaml
  provider-binding.schema.yaml
  provider-mapping.schema.yaml
  subject-safety-profile.schema.yaml
  context-packet.schema.yaml
  expert-context-packet.schema.yaml
  expert-knowledge-source.schema.yaml
  promotion-candidate.schema.yaml
  migration-manifest.schema.yaml
  usage-event.schema.yaml
  revocation.schema.yaml
  erasure.schema.yaml
  break-glass-profile.schema.yaml
  audit-event.schema.yaml
  README.md

examples/memory-gateway/
  gbrain-provider-profile.yaml
  honcho-provider-profile.yaml
  agentmemory-provider-profile.yaml
  local-postgres-provider-profile.yaml
  expert-provider-profiles.yaml
  provider-bindings.example.yaml
  provider-mappings.example.yaml
  conformance-fixtures.yaml
  medx-patient-context-packet.example.yaml
  medx-omnigent-diagnostic-reviewer-context.example.yaml
  opsx-managed-system-context-packet.example.yaml
  opsx-runbook-expert-context.example.yaml
  customer-memory-migration-manifest.example.yaml
  subject-safety.example.yaml
  medx-break-glass.example.yaml

scripts/
  validate-memory-gateway.py

xfactory/
  memory_gateway.py
```

The first runtime slice lives in `xfactory/memory_gateway.py`. It is a local
control-plane module with a service-ready API boundary: extraction to a
standalone service must not change the `xfactory.memory.*` surface.

## 13. Minimum Implementable Slice

The first slice should be deliberately narrow.

```text
One operation:
  xfactory.memory.context_packet

One provider role:
  group_project_memory for Subject Hermes
  expert_knowledge_memory for the first Omnigent proof

One provider adapter:
  GBrain adapter or fake GBrain-compatible adapter
  local or fake expert knowledge adapter

One domain example:
  MedxFactory Patient Hermes context packet
  MedxFactory diagnostic reviewer expert context packet

One auth model:
  provider binding ref + short-lived grant stub

One subject safety model:
  adult versus minor subject safety profile and redaction selection

One metering model:
  usage event emitted, no invoice logic

One migration behavior:
  provider mapping table supports source and target refs
```

Done means:

- consent-denied read never calls the provider
- source-less write is denied before provider I/O
- context packet includes trace refs, redaction level, provider refs, audit ref,
  and usage event ref
- minor subject context packet requires guardian/delegate authority and uses a
  minor-safe redaction profile
- provider profile validation catches unsupported required ports
- Hermes can keep using `xfactory.memory.context_packet` while the route table
  changes from one provider profile to another
- Omnigent can keep using `xfactory.memory.context_packet` while an expert
  knowledge route changes from one provider profile to another

## 14. Latency Guardrails

The gateway should add safety without becoming the slow path.

```text
hot-path xFactory overhead target
  20-100 ms

interactive context packet total target
  300-700 ms including provider retrieval

back-office workflow context target
  under 1-2 s including provider retrieval
```

Sync rails:

- caller auth
- route lookup
- subject safety profile check
- consent check
- privacy/redaction check
- workflow scope check
- budget gate when budget can block

Async work:

- billing aggregation
- audit enrichment
- migration verification
- provider quality comparison
- promotion review workflow
- memory consolidation

Cache keys should include consent version, route version, workflow purpose,
current state snapshot version, and redaction profile.

## 15. Ownership Boundaries

| Layer | Owns | Does Not Own |
| --- | --- | --- |
| Subject Hermes | customer-subject identity, consent, preferences, timeline, evidence, current state, memory, active workflow context, follow-up, promotion candidates | reusable domain truth, tenant-wide credentials, client policy |
| Tenant Hermes | client organization policy, local staff, integrations, customer relationship, tenant configuration, local approval gates | global domain standards, customer-private memory by default |
| Domain Hermes | reusable domain knowledge, expert truth, review standards, routing, taxonomy, safety policy, domain memory | individual customer consent, raw customer records, provider secrets |
| xFactory | memory and knowledge rails, provider bindings, source authority, gates, promotion, traceability, audit, migration, metering, provider neutrality | product-specific storage internals, domain truth decisions |
| Provider adapter | mapping canonical objects and operations to a product API | authority decisions |
| Memory or knowledge product | durable storage, retrieval, indexing, provider-specific capabilities | final truth, approval, consent, promotion policy |
| Domain Omnigent | bounded execution using approved customer and expert context packets | direct unrestricted customer memory access, authoritative expert DB mutation |

## 16. Canonical Gateway Ports

The gateway exposes product-neutral ports that map to the canonical Customer
Hermes object model and the expert memory model used by Domain Omnigent.

```text
IdentityPort
ConsentPort
SubjectSafetyPort
PreferencePort
TimelinePort
SourceClaimPort
EvidenceGraphPort
CurrentStatePort
MemoryItemPort
WorkflowContextPort
FollowUpPort
PromotionPort
AuditPort
ExpertProfilePort
ExpertKnowledgePort
ExpertCaseMemoryPort
ExpertPolicyMemoryPort
ExpertToolMemoryPort
ExpertEvaluationMemoryPort
SourceAuthorityPort
```

These ports can be implemented by one product, many products, or a gateway
storage layer plus provider-specific search/indexing.

Example:

```text
ConsentPort
  may be implemented by Hermes operational state or a regulated consent system

MemoryItemPort
  may be backed by GBrain, Honcho, Postgres, vector search, or another store

EvidenceGraphPort
  may require a graph store even if GBrain handles semantic recall

ExpertKnowledgePort
  may be backed by a root-truth DB, vector index, graph DB, document corpus,
  source workspace, or domain-specific knowledge product

ExpertEvaluationMemoryPort
  may be backed by eval results, benchmark suites, failure libraries, or
  calibration stores
```

## 17. Gateway Operations

The first xFactory memory tool surface should be small and stable.

```text
xfactory.memory.query
xfactory.memory.write
xfactory.memory.context_packet
xfactory.memory.propose_promotion
xfactory.memory.revoke_or_tombstone
xfactory.memory.erase_content
xfactory.memory.audit
xfactory.memory.provider_health
```

### Query

Returns memory or expert knowledge candidates only after consent, privacy,
source authority, expert policy, scope, and workflow checks. Results include
trace refs, source refs, and redaction metadata.

### Write

Writes a canonical object or provider-backed representation only after source,
consent, expert policy, privacy, retention, and secret-scanning checks.

### Context Packet

Builds the bounded context that Hermes or Omnigent may use for a workflow. A
context packet is purpose-bound and should reference a current state snapshot
or expert knowledge-source refs instead of handing out unrestricted memory or
database access.

### Promotion

Creates a promotion candidate when customer-scoped learning might belong in
client or domain memory, or when Omnigent-local expert learning should become
durable expert memory. Nothing silently crosses from customer to client,
domain, or expert knowledge scope.

### Revoke Or Tombstone

Applies consent withdrawal, retention expiry, correction, supersession, or
policy removal. The gateway must preserve audit evidence while preventing
future prohibited use.

### Audit

Records every governed read, write, promotion, revocation, and provider call
with enough traceability to explain what happened later.

### Migration Plan And Status

Creates, validates, monitors, and reports memory migrations without changing
the Hermes memory call surface.

## 18. Rails

Rails run before provider I/O whenever the operation is governed.

### Read Rail

```text
caller identity valid
  -> Hermes layer authority valid
  -> workflow purpose declared
  -> customer subject resolved
  -> subject safety profile permits use
  -> consent permits use
  -> privacy class allowed
  -> authority level sufficient
  -> retention policy allows retrieval
  -> provider query allowed
  -> result redacted and traced
```

### Write Rail

```text
writer authority valid
  -> object type allowed
  -> source refs present when required
  -> no raw secrets
  -> subject safety profile permits write
  -> consent allows storage
  -> privacy class assigned
  -> retention policy assigned
  -> provider write allowed
  -> audit event recorded
```

### Promotion Rail

```text
promotion candidate created
  -> consent permits promotion
  -> subject safety profile permits promotion target and use
  -> de-identification applied when required
  -> client review performed when required
  -> domain review performed when required
  -> target layer allowed
  -> destination provider selected
  -> audit event recorded
```

### Context Packet Rail

```text
active workflow context selected
  -> current state snapshot selected or generated
  -> subject safety profile selected
  -> memory query scoped to workflow purpose
  -> evidence and uncertainty preserved
  -> redaction profile applied
  -> context packet emitted with trace refs
```

### Expert Knowledge Rail

```text
expert profile selected
  -> Domain Hermes approval or policy authorizes expert work
  -> knowledge scopes allowed for workflow purpose
  -> source authority minimum selected
  -> provider profile and binding allow expert role
  -> stale, uncited, or prohibited sources filtered or denied
  -> customer-private context redacted when mixed with expert context
  -> expert context packet emitted with source refs and audit refs
```

### Subject Safety Rail

```text
customer subject resolved
  -> age band and protected status resolved
  -> guardian/delegate requirement checked
  -> allowed interaction mode checked
  -> allowed personalization level checked
  -> redaction and retention profiles selected
  -> prohibited memory uses blocked
  -> enhanced audit selected when required
```

## 19. Provider Profiles

A provider profile declares how a product implements the gateway ports. It does
not grant authority by itself.

Provider roles should be explicit so a product cannot silently change what it
means to the stack.

```text
customer_subject_memory
profile_relationship_memory
group_project_memory
worker_local_memory
expert_knowledge_memory
expert_case_memory
expert_policy_memory
expert_tool_memory
expert_evaluation_memory
```

```yaml
provider_profile:
  provider_id: gbrain
  provider_kind: hermes_group_memory
  supported_layers:
    - domain_hermes
    - client_hermes
    - customer_hermes
  supports:
    identity_profile: adapter_required
    consent_profile: external_required
    preference_profile: native_or_adapter
    timeline: adapter_required
    source_claim: adapter_required
    evidence_graph: external_required
    current_state_snapshot: adapter_required
    memory_item: native
    active_workflow_context: external_required
    follow_up_obligation: adapter_required
    promotion_candidate: adapter_required
  required_companion_ports:
    - ConsentPort
    - EvidenceGraphPort
    - AuditPort
  prohibited_content:
    - raw_credentials
    - unrestricted_private_records_without_consent
```

The profile lets xFactory ask:

```text
Can this provider satisfy the requested operation?
Which rails must run outside the provider?
Which companion stores are required?
Which content must never be sent?
```

Expert provider profiles follow the same structure.

```yaml
provider_profile:
  provider_id: medx-root-truth-vdb
  provider_kind: expert_knowledge_db
  provider_role: expert_knowledge_memory
  supported_layers:
    - domain_omnigent
    - domain_hermes
  supports:
    expert_profile: external_required
    expert_knowledge_source: native
    source_claim: adapter_required
    evidence_graph: external_required
    memory_item: adapter_required
    audit_event: external_required
  required_companion_ports:
    - ExpertProfilePort
    - SourceAuthorityPort
    - EvidenceGraphPort
    - AuditPort
  allowed_knowledge_scopes:
    - root_truth_db
    - clinical_guideline_corpus
  prohibited_content:
    - raw_credentials
    - uncited_clinical_recommendation_as_truth
    - unrestricted_private_records_without_consent
```

## 20. GBrain Wiring

GBrain should be treated as a Hermes memory backend, not the architecture.

```text
Hermes role
  -> xfactory.memory.context_packet
  -> xFactory rails
  -> GBrain adapter
  -> GBrain retrieval
  -> xFactory filtering and trace packaging
  -> Hermes receives bounded context
```

For a write:

```text
Hermes Memory Curator
  -> xfactory.memory.write
  -> xFactory validates object, source refs, consent, privacy, retention
  -> GBrain adapter maps canonical metadata to GBrain record
  -> GBrain stores provider record
  -> xFactory records canonical audit event and provider ref
```

Example mapping:

```yaml
canonical_object:
  object_type: memory_item
  object_id: memory.patient_123.prefers_morning_calls.v1
  owning_layer: customer_hermes
  customer_subject_ref: patient://pseudonymous-123
  authority_level: L3
  privacy_class: regulated
  consent_profile_ref: consent.patient_123.v3
  source_refs: []

provider_mapping:
  provider: gbrain
  provider_object_ref: gbrain://memory/abc123
  namespace: medx/client-a/customer/patient-123
  tags:
    - memory_item
    - customer_hermes
    - regulated
```

## 21. AgentMemory, Honcho, And Expert Memory Boundaries

AgentMemory remains worker-local Omnigent memory.

```text
Omnigent worker writes local observation
  -> agentmemory stores worker-local recall
  -> worker proposes promotion if durable
  -> Hermes reviews promotion
  -> xFactory rail decides destination
```

External expert memory and knowledge DBs are different from AgentMemory. They
are provider-backed domain resources governed by xFactory routes, bindings,
source-authority policy, billing, migration, and audit.

```text
Omnigent expert requests domain knowledge
  -> xfactory.memory.context_packet
  -> expert knowledge rail runs
  -> expert provider adapter retrieves source-scoped context
  -> Omnigent receives bounded expert packet
```

Honcho remains people/profile/relationship memory.

```text
Hermes needs user/profile preference context
  -> xFactory memory query declares profile/person purpose
  -> Honcho adapter retrieves allowed profile memory
  -> xFactory redacts and packages result
```

Neither AgentMemory nor Honcho should silently become Subject Hermes truth.
Neither AgentMemory nor an external expert DB should silently become Domain
Hermes truth without a reviewed promotion path.

## 22. Minimum MVP

The first implementation should prove one vertical path:

```text
Hermes asks for governed context
  -> xFactory context packet rail runs
  -> GBrain adapter retrieves candidate memory
  -> xFactory filters, redacts, and audits
  -> Hermes receives bounded context with trace refs

Omnigent asks for expert context
  -> xFactory expert knowledge rail runs
  -> expert knowledge adapter retrieves source-scoped candidates
  -> xFactory cites, redacts, and audits
  -> Omnigent receives bounded expert context with source refs
```

MVP files and concepts:

```text
contracts/memory-gateway/
  gateway-request.schema.yaml
  gateway-response.schema.yaml
  provider-profile.schema.yaml
  context-packet.schema.yaml
  expert-context-packet.schema.yaml
  promotion-candidate.schema.yaml

examples/memory-gateway/
  gbrain-provider-profile.yaml
  agentmemory-provider-profile.yaml
  expert-provider-profiles.yaml
  medx-patient-context-packet.example.yaml
  medx-omnigent-diagnostic-reviewer-context.example.yaml

docs/
  customer-memory-gateway-architecture.md

xfactory/
  memory_gateway.py
```

MVP conformance checks:

- read denied when consent is missing
- write denied when required source refs are missing
- write denied when secret-like content is detected
- promotion denied when de-identification or review is required but missing
- context packet includes trace refs and redaction metadata
- subject safety profile blocks minor-disallowed memory uses
- expert context packet denies uncited or below-threshold expert knowledge when
  source authority is required
- provider profile declares unsupported ports and companion requirements

## 23. Domain Specialization

Each DomainxFactory should declare how it specializes the gateway:

```yaml
customer_memory_gateway:
  canonical_contract: openxFactory/contracts/memory-gateway
  customer_layer_name: Patient Hermes
  customer_subject_kinds:
    - patient
    - episode
    - case
  provider_profiles:
    - gbrain-medx-customer-memory
  required_ports:
    - IdentityPort
    - ConsentPort
    - SubjectSafetyPort
    - EvidenceGraphPort
    - CurrentStatePort
    - MemoryItemPort
    - PromotionPort
    - AuditPort
  default_context_packet_redaction: patient_redacted
  subject_safety_profiles:
    adult: subject_safety.medx.adult.v1
    minor: subject_safety.medx.minor.v1
```

The same DomainxFactory should declare the expert memory and knowledge routes
that its Omnigent overlay may use.

```yaml
omnigent_expert_memory_gateway:
  canonical_contract: openxFactory/contracts/memory-gateway
  consumer_layer: domain_omnigent
  expert_profiles:
    - expert://medx/oncology/diagnostic-reviewer
  provider_profiles:
    - medx-root-truth-vdb
    - medx-case-pattern-store
  provider_roles:
    expert_knowledge_memory:
      primary: medx-root-truth-vdb
    expert_case_memory:
      secondary: medx-case-pattern-store
  required_ports:
    - ExpertProfilePort
    - ExpertKnowledgePort
    - ExpertCaseMemoryPort
    - SourceAuthorityPort
    - AuditPort
  default_expert_context_packet_redaction: patient_safe
  source_authority_policy_ref: source_authority.medx.clinical.v1
  allowed_uses:
    - hypothesis_generation
    - evidence_review
  prohibited_uses:
    - autonomous_clinical_decision
```

MedxFactory should specialize this for Patient Hermes. OpsxFactory should
specialize it for Managed System Hermes. codexFactory should specialize it for
Project Hermes.

## 24. Implementation Sequence

1. Document the architecture and OpenSpec requirements.
2. Add gateway schemas and provider profile schemas.
3. Add provider binding, subject safety, usage event, and migration manifest schemas.
4. Add example GBrain, Honcho, AgentMemory, Postgres, and expert knowledge
   provider profiles.
5. Add Hermes memory gateway config examples.
6. Add conformance fixtures for rails and provider profiles.
7. Implement a small gateway module or service.
8. Register `xfactory.memory.*` tools in Hermes.
9. Route governed GBrain memory access through xFactory.
10. Route governed Omnigent expert knowledge access through xFactory.
11. Add domain-specific customer and expert context packet examples.
12. Add migration route-table examples and dual-write fixtures for customer
    memory and expert DB routes.
13. Tighten direct provider access so it cannot create authoritative Customer
    Hermes memory or Omnigent expert context; governed operations require the
    gateway.

## 25. Design Rule

Use this rule when evaluating implementation options:

```text
If a memory product can be replaced without changing Subject Hermes authority,
the architecture is healthy.

If an expert knowledge DB can be replaced without changing the Omnigent expert
call surface or Domain Hermes authority, the architecture is healthy.

If a memory product defines consent, promotion, traceability, or source
authority by itself, the architecture has leaked.

If an expert DB defines reusable domain truth, review policy, or allowed use by
itself, the architecture has leaked.
```
