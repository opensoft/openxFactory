# memory-gateway Specification

## Purpose
Defines the product-neutral xFactory Memory Gateway for governed Customer Hermes memory and Domain Omnigent expert memory or knowledge access, including provider bindings, rails-before-I/O, context packets, consent, subject safety, credential custody, fail modes, audit, conformance tiers, and migration behavior.
## Requirements
Conformance tiers (see design.md, "Requirements are tiered"): a gateway is
minimally conformant at M0 for governed reads and bounded context packets.
Ordinary authoritative writes additionally require the M0 write-minimum:
write request schema, source-backed write rail, deny-before-I/O behavior,
provider mapping, and audit. Cross-layer promotion, revocation/tombstone,
erasure, and migration require the higher tiers that define them.

```text
M0: Gateway Mediates Governed Memory Access; Canonical Ports Are Product
    Neutral; Provider Profiles Declare Capability; Rails Run Before Provider
    I/O; Provider Access Uses Bindings And Short-Lived Grants; Gateway
    Callers Are Authenticated And Hold No Provider Credentials; Consent
    Profiles Are A First-Class Contract; Fail Modes Are Explicit And
    Break-Glass Is Audited; Context Packets Bound Runtime Memory; Memory
    Provider Mapping Is Traceable; Gateway Conformance Is Testable
M1: Promotions Are Explicit And Reviewed; Revocation And Tombstones Preserve
    Audit; Erasure Is Distinct From Revocation; Worker-Local Memory Remains
    Separate; Customer Memory Fill And Maintenance Modes Are Canonical
M2: Subject Safety Rail Handles Adult And Minor Subjects
M3: Usage Metering Is Gateway-Owned
M4: Memory Migration Preserves Hermes Continuity; Expert Memory And
    Knowledge DBs Are Gateway-Governed follows the tier of the operation it
    mirrors (rails at M0, promotion at M1, migration at M4)
```

### Requirement: Gateway Mediates Governed Memory Access

The system SHALL route governed Customer Hermes memory and Domain Omnigent
expert memory or knowledge reads, writes, context-packet creation, promotion,
revocation, and audit operations through an xFactory Memory Gateway before
using a memory or knowledge provider.

#### Scenario: Hermes requests governed GBrain memory

- **WHEN** a Hermes role requests governed Customer Hermes memory that is backed
  by GBrain
- **THEN** Hermes MUST call the xFactory memory gateway rather than treating a
  direct GBrain call as authoritative memory access

#### Scenario: Direct provider access is diagnostic

- **WHEN** a direct provider tool is used for health checks, bootstrap, or
  diagnostics
- **THEN** the result MUST NOT create approved Customer Hermes memory or
  authoritative expert context under any condition
- **AND** the direct access MUST use separate operator-scoped credentials that
  are read-only, bound to non-production or shadow namespaces, and never issued
  to worker identities

#### Scenario: Omnigent requests governed expert knowledge

- **WHEN** an Omnigent expert requires source-backed expert knowledge from a
  root-truth DB, vector index, graph store, source workspace, case-pattern
  store, playbook store, or evaluation store
- **THEN** Omnigent MUST call the xFactory memory gateway rather than treating a
  direct provider call as authoritative expert context

### Requirement: Canonical Ports Are Product Neutral

The system SHALL define product-neutral ports for Customer Hermes identity,
consent, preferences, timeline, source claims, evidence graph, current state,
memory items, active workflow context, follow-up obligations, promotion, and
audit, and for Omnigent expert profiles, expert knowledge, expert case memory,
expert policy memory, expert tool memory, expert evaluation memory, and source
authority.

#### Scenario: Provider implements only some ports

- **WHEN** a provider profile declares native support for memory items but
  external support for consent and evidence graph
- **THEN** the gateway MUST require companion implementations for ConsentPort and
  EvidenceGraphPort before approving governed operations that need those ports

#### Scenario: Expert provider requires source authority companion

- **WHEN** an expert knowledge provider profile declares native support for
  expert knowledge retrieval but external support for source authority
- **THEN** the gateway MUST require a companion SourceAuthorityPort before
  approving governed expert context operations that require cited knowledge

### Requirement: Provider Profiles Declare Capability

The system SHALL use provider profiles to declare provider capabilities,
supported layers, unsupported ports, required companion stores, prohibited
content, and adapter behavior without granting authority.

#### Scenario: GBrain provider profile is loaded

- **WHEN** the gateway loads a GBrain provider profile
- **THEN** the profile MUST declare which canonical Customer Hermes objects are
  native, adapter-backed, external, or unsupported

#### Scenario: Unsupported provider operation is requested

- **WHEN** a memory operation requires a port that the selected provider profile
  marks as unsupported and no companion port is configured
- **THEN** the gateway MUST deny the operation before provider I/O

#### Scenario: Expert provider profile is loaded

- **WHEN** the gateway loads an expert knowledge provider profile
- **THEN** the profile MUST declare provider role, supported expert ports,
  allowed layers, allowed knowledge scopes, required companion ports,
  source-authority requirements, prohibited content, and adapter behavior

### Requirement: Expert Memory And Knowledge DBs Are Gateway-Governed

The system SHALL govern Domain Omnigent expert memory and external knowledge DB
access through the same xFactory Memory Gateway model used for Customer Hermes
memory.

#### Scenario: Omnigent receives expert context packet

- **WHEN** a Domain Omnigent expert requests reusable expert knowledge for an
  approved workflow
- **THEN** the gateway MUST verify expert profile, workflow purpose, Domain
  Hermes policy, provider binding, source-authority policy, allowed knowledge
  scope, budget, and audit requirements before provider I/O
- **AND** the returned context MUST be a bounded expert context packet with
  source refs, provider refs, allowed uses, prohibited uses, audit refs, and
  usage refs

#### Scenario: Expert knowledge is below source threshold

- **WHEN** an expert context request requires a minimum source authority level
  and candidate knowledge lacks required citations, freshness metadata, or
  authority level
- **THEN** the gateway MUST deny the candidate, degrade the packet, or mark it
  below-threshold before Omnigent may use it as expert context

#### Scenario: Omnigent proposes durable expert learning

- **WHEN** an Omnigent worker observation should become reusable expert memory,
  case memory, policy memory, tool memory, or evaluation memory
- **THEN** Omnigent MUST submit a promotion candidate for xFactory and Domain
  Hermes review rather than directly mutating an authoritative expert DB

#### Scenario: Expert DB migration preserves Omnigent continuity

- **WHEN** xFactory migrates an expert knowledge provider route from one DB,
  vector index, graph store, source workspace, or case store to another
- **THEN** Omnigent MUST continue using the same `xfactory.memory.*` operation
  names while xFactory updates route tables, provider mappings, migration
  state, and audit records

### Requirement: Rails Run Before Provider I/O

The system SHALL run xFactory rails before any governed provider read, write,
promotion, revocation, or context-packet operation.

#### Scenario: Read denied without consent

- **WHEN** a memory query targets customer-private or regulated memory and the
  active consent profile does not allow the requested use
- **THEN** the gateway MUST deny the provider query and record an audit event

#### Scenario: Write denied without required source references

- **WHEN** a memory write requires source-backed authority but does not include
  required source references
- **THEN** the gateway MUST deny the provider write and report the missing
  source evidence

#### Scenario: Write denied for secret-like content

- **WHEN** a memory write contains raw credentials, tokens, private keys, or
  secret-like values
- **THEN** the gateway MUST deny the write before provider I/O

### Requirement: Provider Access Uses Bindings And Short-Lived Grants

The system SHALL authenticate memory providers through xFactory provider
bindings and short-lived credential broker grants rather than raw provider
credentials stored in Hermes.

#### Scenario: Provider grant is required

- **WHEN** a governed memory operation requires a provider call
- **THEN** the gateway MUST resolve an allowed provider binding and obtain or
  validate a scoped provider grant before adapter I/O

#### Scenario: Provider binding disallows operation

- **WHEN** the selected provider binding does not allow the requested layer,
  operation, client, or customer-subject scope
- **THEN** the gateway MUST deny the operation before provider I/O

### Requirement: Subject Safety Rail Handles Adult And Minor Subjects

The system SHALL apply a subject-safety rail before governed memory retrieval,
write, context-packet creation, promotion, or provider I/O when the customer
subject has an adult, minor, protected, delegated, or guardian-mediated status.

#### Scenario: Adult subject uses direct consent

- **WHEN** an adult customer subject requests a workflow and direct consent is
  valid for the requested purpose
- **THEN** the gateway MUST allow the adult subject safety profile to select the
  standard redaction, retention, personalization, and audit policy for that
  workflow

#### Scenario: Minor subject requires guardian authority

- **WHEN** a minor customer subject requests or is associated with a governed
  memory operation that requires guardian or delegated authority
- **THEN** the gateway MUST verify guardian or delegate authority before
  provider I/O and MUST deny the operation when that authority is missing

#### Scenario: Minor subject blocks prohibited personalization

- **WHEN** a context packet request for a minor subject includes inferred
  personality targeting, marketing personalization, or autonomous sensitive
  disclosure
- **THEN** the gateway MUST block the prohibited use or degrade to a minor-safe
  context packet profile before provider I/O

#### Scenario: Minor subject receives enhanced audit

- **WHEN** the gateway allows a governed memory operation for a minor or other
  protected subject category
- **THEN** it MUST include the applied subject-safety profile, redaction profile,
  retention profile, and enhanced audit level in the audit record or context
  packet metadata

### Requirement: Context Packets Bound Runtime Memory

The system SHALL provide bounded context packets for Hermes and Omnigent runtime
use instead of exposing unrestricted Customer Hermes memory or unrestricted
expert knowledge DB access.

#### Scenario: Context packet created for active workflow

- **WHEN** Hermes requests context for an active workflow
- **THEN** the gateway MUST use workflow purpose, subject-safety profile,
  consent, privacy, authority, current state snapshot refs, redaction policy,
  and source trace refs to build the context packet

#### Scenario: Omnigent receives memory context

- **WHEN** Omnigent needs customer-subject context for an approved job
- **THEN** Omnigent MUST receive a bounded context packet from Hermes or
  xFactory rather than direct unrestricted provider access

#### Scenario: Omnigent receives expert knowledge context

- **WHEN** Omnigent needs expert knowledge context for an approved job
- **THEN** Omnigent MUST receive a bounded expert context packet from xFactory
  rather than direct unrestricted DB, vector index, graph, or source workspace
  access

#### Scenario: Context packet expires

- **WHEN** a context packet's declared TTL has elapsed
- **THEN** the packet MUST be invalid as workflow input and a new packet
  request MUST re-run the rails

#### Scenario: Context packet used for a different purpose

- **WHEN** a context packet issued for one workflow purpose is presented as
  input to a different workflow or purpose
- **THEN** the consuming surface MUST reject the packet and request a new
  packet for the actual purpose

#### Scenario: Packet-derived worker memory inherits redaction class

- **WHEN** an Omnigent worker stores content derived from a context packet in
  worker-local memory such as AgentMemory
- **THEN** the stored derivative MUST inherit the packet's redaction class and
  subject refs, and storing packet-derived content above its redaction class
  MUST be treated as a rail violation

### Requirement: Customer Memory Fill And Maintenance Modes Are Canonical

The system SHALL define general customer memory fill and maintenance modes in
openxFactory and SHALL require DomainxFactories to map those modes to their own
customer layer names, source families, evidence types, review rules, and
adapters.

#### Scenario: Customer interaction becomes memory candidate

- **WHEN** a customer interacts through an avatar-first UI, conventional UI,
  voice session, chat, form, or attachment surface
- **THEN** the raw interaction material MUST be treated as source material
  until Hermes distills it into a candidate source claim, timeline event,
  preference, follow-up, current-state change, memory item, or promotion
  candidate
- **AND** xFactory MUST gate durable memory writes or updates before provider
  I/O

#### Scenario: Domain maps fill modes locally

- **WHEN** a DomainxFactory declares a Customer Hermes, Patient Hermes, Managed
  System Hermes, Project Hermes, Engagement Hermes, Campaign Hermes, or
  equivalent customer layer
- **THEN** it MUST map the general fill modes to domain source families,
  adapters, authority thresholds, evidence types, and reviewer rules

#### Scenario: Domain maps maintenance modes locally

- **WHEN** customer memory can be refreshed, reconciled, superseded, corrected,
  revoked, expired, promoted, de-identified, drift-monitored, or migrated
- **THEN** the DomainxFactory MUST declare which local source families,
  reviewers, retention rules, and provider routes control that maintenance mode

### Requirement: Promotions Are Explicit And Reviewed

The system SHALL represent movement from Customer Hermes memory into Client
Hermes or Domain Hermes memory as explicit promotion candidates.

#### Scenario: Customer memory proposed for domain learning

- **WHEN** customer-scoped memory may be useful as reusable domain learning
- **THEN** the gateway MUST create or validate a promotion candidate with
  consent, de-identification, source refs, target layer, and required review
  metadata before promotion

#### Scenario: Promotion lacks required review

- **WHEN** a promotion candidate requires client or domain review and the review
  record is missing
- **THEN** the gateway MUST block promotion to the target layer

### Requirement: Revocation And Tombstones Preserve Audit

The system SHALL support revocation and tombstone operations that prevent future
prohibited use while preserving audit and traceability records.

#### Scenario: Consent is withdrawn

- **WHEN** consent is withdrawn for a customer subject
- **THEN** the gateway MUST block future memory use covered by the withdrawn
  consent and record revocation or tombstone metadata

### Requirement: Usage Metering Is Gateway-Owned

The system SHALL emit memory usage events for governed memory operations without
storing memory content in billing or usage records.

#### Scenario: Context packet usage is metered

- **WHEN** the gateway creates a context packet using one or more memory
  providers
- **THEN** it MUST emit a usage event that records operation, provider role,
  provider id, client, domain, workflow, bill-to target, usage units, latency,
  and content-free customer-subject reference

#### Scenario: Budget hard limit is exceeded

- **WHEN** a request exceeds a configured hard budget limit for an operation
  class marked expensive in the provider profile
- **THEN** the gateway MUST deny the operation or route to an approved degraded
  mode before provider I/O

#### Scenario: Routine operation uses asynchronous soft limits

- **WHEN** a routine (non-expensive) governed operation is requested
- **THEN** budget accounting MAY be asynchronous with warn or
  require-approval escalation, and MUST NOT add a synchronous budget check to
  the operation's latency path

### Requirement: Memory Migration Preserves Hermes Continuity

The system SHALL migrate Customer Hermes memory providers by changing xFactory
routes, provider mappings, and migration state without changing the Hermes
memory call surface.

#### Scenario: Migration enters dual-write

- **WHEN** a migration manifest puts a provider route into dual-write mode
- **THEN** the gateway MUST write new allowed memory updates to both source and
  target routes and record provider mappings for each route

#### Scenario: Migration cutover occurs

- **WHEN** migration verification passes and cutover is approved
- **THEN** the gateway MUST make the target provider route primary while Hermes
  continues using the same `xfactory.memory.*` operation names

#### Scenario: Migration rollback is requested

- **WHEN** a migration rollback is requested inside the rollback window
- **THEN** the gateway MUST restore the previous provider route or configured
  fallback route and record the rollback decision in audit

### Requirement: Memory Provider Mapping Is Traceable

The system SHALL store or emit mapping metadata between canonical Customer
Hermes objects and provider-specific object references.

#### Scenario: Canonical memory item is stored in GBrain

- **WHEN** the gateway writes a canonical memory item to GBrain through an
  adapter
- **THEN** the resulting record MUST include or emit a provider mapping with the
  canonical object id, provider id, provider object ref, namespace, layer, and
  audit refs

### Requirement: Worker-Local Memory Remains Separate

The system SHALL preserve the boundary between Omnigent worker-local memory,
Hermes-governed Customer Hermes memory, and xFactory-governed expert memory or
knowledge providers.

#### Scenario: AgentMemory observation becomes durable learning

- **WHEN** an Omnigent worker writes an observation to AgentMemory and the
  observation should become durable client or domain memory
- **THEN** the worker or Omnigent MUST submit a promotion candidate for Hermes
  and xFactory review instead of directly writing authoritative memory

#### Scenario: AgentMemory observation becomes expert learning

- **WHEN** an Omnigent worker writes an observation to AgentMemory and the
  observation should become durable expert knowledge, case memory, policy
  memory, tool memory, or evaluation memory
- **THEN** the worker or Omnigent MUST submit a promotion candidate for xFactory
  and Domain Hermes review instead of directly writing an authoritative expert
  memory provider

### Requirement: Gateway Callers Are Authenticated And Hold No Provider Credentials

The system SHALL verify an authenticated caller identity (Hermes role,
council, or Omnigent worker identity plus consumer layer) before running
rails, and SHALL ensure worker and Hermes-role identities are never issued
memory provider credentials in any environment.

#### Scenario: Gateway call lacks attributable caller identity

- **WHEN** a gateway operation cannot be attributed to an authenticated caller
  identity and consumer layer
- **THEN** the gateway MUST deny the operation before rails run

#### Scenario: Worker identity cannot reach providers directly

- **WHEN** an Omnigent worker attempts a direct call to a governed memory
  provider namespace
- **THEN** the call MUST fail because worker identities hold no provider
  credentials, and provider credentials MUST exist only inside the gateway's
  binding resolution path as short-lived broker grants

#### Scenario: Diagnostic access is operator-scoped

- **WHEN** direct provider access is needed for health checks, bootstrap, or
  diagnostics
- **THEN** it MUST use separate operator-scoped credentials that are
  read-only and bound to non-production or shadow namespaces, and MUST NOT be
  issued to worker identities

### Requirement: Consent Profiles Are A First-Class Contract

The system SHALL define a versioned consent profile contract, backed initially
by Hermes operational state, that rail decisions reference by version, with
every consent change recorded as an audited event.

#### Scenario: Rail decision references consent version

- **WHEN** a rail allows or denies an operation based on consent
- **THEN** the audit record MUST include the consent profile version the
  decision used

#### Scenario: Consent change is audited

- **WHEN** a consent profile is created, modified, or withdrawn
- **THEN** the change MUST record actor, authority basis (direct, guardian,
  delegated), effective time, and affected purposes

#### Scenario: Consent backing store is replaceable

- **WHEN** the consent backing store moves from Hermes operational state to a
  dedicated consent service
- **THEN** the consent profile contract and rail call surface MUST NOT change

### Requirement: Fail Modes Are Explicit And Break-Glass Is Audited

The system SHALL define failure behavior per operation class when the gateway
or a provider is unavailable, and SHALL support declared break-glass workflows
with enhanced audit.

#### Scenario: Write fails closed during gateway outage

- **WHEN** a governed write, promotion, revocation, or migration operation is
  requested and the gateway or required rail state is unavailable
- **THEN** the operation MUST fail closed

#### Scenario: Read degrades according to declared policy

- **WHEN** a governed read or context-packet request cannot complete and the
  operation class declares a degraded mode
- **THEN** the gateway MAY serve a previously issued, unexpired,
  already-redacted packet from cache or MUST deny, and MUST NOT bypass rails
  to reach a provider

#### Scenario: Break-glass workflow requests emergency context

- **WHEN** a domain-declared break-glass workflow (for example emergency
  clinical escalation) asserts an emergency basis
- **THEN** the gateway MUST verify caller identity, domain-declared workflow
  eligibility, subject scope, provider binding, redaction profile, and maximum
  TTL before resolving a pre-defined minimal emergency packet profile within a
  bounded time
- **AND** it MUST record an enhanced audit event, notify the configured
  escalation targets, and create a mandatory retrospective review task with the
  domain-declared review SLA

#### Scenario: Break-glass is not available to undeclared workflows

- **WHEN** a caller asserts an emergency basis for a workflow that is not
  domain-declared as break-glass-eligible
- **THEN** the gateway MUST deny the emergency path and process the request
  through standard rails

### Requirement: Erasure Is Distinct From Revocation

The system SHALL provide an erase-content operation, distinct from
revoke-or-tombstone, for domain/legal-policy-declared erasure or suppression
obligations, and SHALL require provider profiles to declare erasure capability
per port.

#### Scenario: Erasure is requested for a policy-constrained subject

- **WHEN** a domain or legal policy-declared erasure or suppression obligation
  applies to customer-subject memory
- **THEN** the gateway MUST execute provider-side content deletion through the
  adapter, record provider confirmation refs in the audit trail, and preserve
  content-free audit metadata

#### Scenario: Provider cannot erase

- **WHEN** memory for a domain-policy-constrained subject category would be
  routed to a
  provider whose profile declares erasure capability `unsupported` for the
  required port
- **THEN** the gateway MUST deny the routing unless an explicit, documented
  compensating control is configured, and conformance validation MUST surface
  the exception

#### Scenario: Revocation does not claim erasure

- **WHEN** a revoke-or-tombstone operation completes
- **THEN** the result MUST NOT be represented as content erasure, and any
  erasure obligation MUST remain tracked until an erase-content operation
  confirms provider-side deletion

### Requirement: Gateway Conformance Is Testable

The system SHALL provide conformance fixtures or checks for provider profiles,
rail denials, caller identity, credential custody, fail modes, break-glass,
context-packet metadata, packet leash behavior, expert context-packet
metadata, consent contract behavior, promotion review, revocation, erasure,
migration, and audit, mapped to the conformance tiers.

#### Scenario: Domain stack declares xFactory memory gateway provider

- **WHEN** a DomainxFactory declares an xFactory Memory Gateway provider profile
  or an Omnigent expert memory provider profile
- **THEN** validation MUST verify required ports, subject-safety rails,
  source-authority rails, prohibited content, companion stores, erasure
  capability, migration behavior, and example customer or expert
  context-packet behavior

#### Scenario: Domain stack declares gateway configuration

- **WHEN** a DomainxFactory stack.yaml declares a `memory_gateway` block
  (providers, per-layer-scope bindings, declared break-glass workflows,
  conformance tier)
- **THEN** the canonical conformance validator
  (`openxFactory/scripts/validate-domain-factory.py`) MUST validate the block
  against the gateway contract schemas, and MUST flag provider endpoints or
  connection references found inside Hermes overlay files as direct-binding
  violations
