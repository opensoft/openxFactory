## Context

openxFactory now defines Customer Hermes as the customer-subject memory
boundary through `docs/customer-hermes-memory-model.md`. The current stack also
has product-specific memory helpers: GBrain for Hermes group/project memory,
Honcho for people/profile relationship memory, and AgentMemory for
Omnigent worker-local recall. Those products solve useful storage and recall
problems, but none of them should define xFactory authority, consent,
promotion, traceability, or source truth.

The same problem exists for Domain Omnigent experts. They need access to
external expert memory and knowledge DBs such as root-truth corpora, vector
indexes, graph stores, source workspaces, case-pattern stores, playbooks, and
evaluation memory. Those products should not define domain truth, review
policy, allowed use, billing, migration, or audit by themselves.

The architecture needs a product-neutral gateway between Hermes and memory
providers. Hermes should ask xFactory for memory operations, xFactory should run
the rails, and adapters should map allowed operations to products such as
GBrain.

Omnigent should use the same gateway pattern for expert knowledge operations.
Domain Hermes owns reusable expert truth and review standards; xFactory owns
provider bindings, source-authority rails, grants, route tables, migrations,
metering, and audit; Omnigent receives bounded expert context packets.

## Goals / Non-Goals

**Goals:**

- Define xFactory as the memory rail for Customer Hermes brain, memory, and
  personality.
- Define xFactory as the expert memory and knowledge rail for Domain Omnigent.
- Keep GBrain, Honcho, AgentMemory, and future products behind provider
  adapters.
- Keep root-truth DBs, vector stores, graph stores, source workspaces,
  case-pattern stores, playbooks, and evaluation memory behind expert provider
  adapters.
- Preserve Customer Hermes, Client Hermes, Domain Hermes, and xFactory
  authority boundaries.
- Define product-neutral ports for identity, consent, preference, timeline,
  source claims, evidence graph, current state, memory, workflow context,
  follow-up, promotion, and audit.
- Define how Hermes routes governed GBrain access through xFactory memory tools.
- Define provider authentication and authorization through xFactory provider
  bindings and short-lived credential broker grants.
- Define subject-safety handling for adult versus child/minor users through
  xFactory rails, not provider-specific behavior.
- Define gateway-owned billing/metering so usage, budgets, and chargeback are
  independent of memory providers.
- Define gateway-owned migration so Customer Hermes can move between memory
  models without changing the Hermes call surface.
- Define conformance expectations that prove rails run before provider I/O.
- Define conformance expectations that prove Omnigent expert DB access runs
  through xFactory rails before provider I/O.
- Define customer memory fill and maintenance modes that are general in
  openxFactory and mapped locally by each DomainxFactory.

**Non-Goals:**

- Do not choose one mandatory memory product for every DomainxFactory.
- Do not implement a production gateway service in this proposal.
- Do not migrate existing GBrain, Honcho, or AgentMemory data.
- Do not migrate existing expert memory or knowledge DBs in this proposal.
- Do not implement invoice generation or payment processing.
- Do not make Omnigent workers direct owners of Customer Hermes memory.
- Do not make Omnigent workers direct owners of reusable expert truth or
  external expert DB mutation.
- Do not store raw credentials, unrestricted private records, or canonical
  source truth in memory products.

## Decisions

### Decision: Introduce the xFactory Memory Gateway

Hermes and Omnigent will call a product-neutral xFactory gateway for governed
memory and knowledge operations.

```text
Hermes role or council
  -> xFactory Memory Gateway
  -> rails
  -> provider adapter
  -> memory product

Omnigent expert
  -> xFactory Memory Gateway
  -> expert knowledge rail
  -> provider adapter
  -> external expert memory or knowledge DB
```

Alternative considered: let Hermes call GBrain directly. That is faster for a
single product integration, but it couples authority to a provider and makes it
harder to enforce consent, redaction, promotion, and audit consistently.

Alternative considered: let Omnigent experts call root-truth DBs, vector
indexes, source workspaces, or case stores directly. That is fast for one
expert, but it couples expert behavior to provider internals and bypasses
source authority, billing, migration, and audit.

### Decision: Expose stable xFactory memory tools

The first tool surface should be:

```text
xfactory.memory.query
xfactory.memory.write
xfactory.memory.context_packet
xfactory.memory.propose_promotion
xfactory.memory.revoke_or_tombstone
xfactory.memory.audit
xfactory.memory.provider_health
```

Alternative considered: expose one generic `memory.call` method. A generic
method would be simpler to proxy but harder to validate and test as a rail.

The operation frame carries `consumer_layer`, provider role, expert profile,
knowledge scope, and source-authority requirements so `context_packet` can
produce either a Customer Hermes packet or an Omnigent expert packet.

### Decision: Define gateway ports by canonical Customer Hermes objects

The gateway should use ports that map to the canonical object model:
IdentityPort, ConsentPort, PreferencePort, TimelinePort, SourceClaimPort,
EvidenceGraphPort, CurrentStatePort, MemoryItemPort, WorkflowContextPort,
FollowUpPort, PromotionPort, and AuditPort. It should also expose expert ports:
ExpertProfilePort, ExpertKnowledgePort, ExpertCaseMemoryPort,
ExpertPolicyMemoryPort, ExpertToolMemoryPort, ExpertEvaluationMemoryPort, and
SourceAuthorityPort.

Alternative considered: define ports by backend type such as vector, graph, and
relational. Backend-shaped ports are useful internally, but they let storage
shape the authority model.

### Decision: Provider profiles declare capability, not authority

A provider profile declares which canonical objects and ports a product can
support natively, through an adapter, through a companion store, or not at all.
The profile never grants permission by itself.

Expert provider profiles declare the same for root-truth DBs, vector stores,
graph stores, source workspaces, case-pattern stores, playbook stores, and
evaluation stores.

Alternative considered: hard-code a GBrain mapping in Hermes. That would make
the first path shorter, but it would not generalize cleanly to AgentMemory,
Honcho, or domain-specific stores.

### Decision: Provider bindings and grants authenticate providers

Provider access should use xFactory memory provider bindings plus short-lived
credential broker grants. Hermes and Omnigent store no raw provider credentials
and do not decide which provider token to use.

Alternative considered: configure provider credentials directly in Hermes.
That is simple for one provider, but it makes provider migration, customer-owned
memory providers, custody rules, and revocation harder to govern consistently.

### Decision: Rails run before provider I/O

The gateway must run read, write, context-packet, expert knowledge, promotion,
revocation, and audit rails before any governed provider call. Provider
products may add their own safeguards, but xFactory rails remain the canonical
policy boundary.

Alternative considered: let each provider enforce its own policy. That would
duplicate policy and create inconsistent safety behavior across products.

### Decision: Subject safety is an xFactory rail

Adult and child/minor users should be handled through a subject-safety rail
that resolves age band, protected status, guardian or delegated authority,
allowed interaction modes, allowed personalization, redaction, retention, and
audit level before memory provider I/O.

Alternative considered: let each memory provider implement adult/minor rules.
That would make protected-subject behavior inconsistent and would break when a
Customer Hermes layer migrates providers.

### Decision: Context packets are the execution boundary

Hermes and Omnigent should receive bounded context packets, not unrestricted
memory or knowledge DB access. A context packet declares purpose, workflow
scope, source refs, redaction level, current state snapshot refs, knowledge
source refs when applicable, and audit refs.

Alternative considered: inject memory directly into every agent session. That
is convenient but risks irrelevant, stale, or unauthorized context leakage.

### Decision: Customer memory fill and maintenance modes are canonical

openxFactory should define the general fill and maintenance taxonomy for
Customer Hermes memory. The taxonomy includes direct customer interaction,
structured customer input, customer-attached evidence, external system
ingestion, third-party or provider messages, telemetry, staff notes, non-Hermes
agent output, Omnigent work output, workflow outcomes, and migration/backfill.
It also includes refresh, reconciliation, supersession, correction, consent
change, retention expiry, promotion review, de-identification, drift
monitoring, and provider migration.

DomainxFactory repos should map those same mode names into their own terms,
such as Patient Hermes, Managed System Hermes, Project Hermes, Engagement
Hermes, or Campaign Hermes. The domain mapping owns source families, adapters, evidence
types, claim types, reviewer roles, freshness windows, and authority
thresholds.

Alternative considered: let each DomainxFactory invent its own memory-fill
categories. That would make local docs feel natural at first, but it would
break cross-domain validation, shared gateway fixtures, and provider migration
tooling.

### Decision: xFactory governs Omnigent expert memory providers

Domain Omnigent expert memory should be organized as provider roles behind the
same gateway: `expert_knowledge_memory`, `expert_case_memory`,
`expert_policy_memory`, `expert_tool_memory`, and `expert_evaluation_memory`.
xFactory owns route tables, bindings, short-lived grants, source authority,
metering, migration, and audit for those providers.

Domain Hermes owns reusable expert truth, allowed-use policy, and review
standards. Omnigent may write worker-local recall and may propose durable
expert learning, but it must not directly mutate authoritative expert memory or
knowledge DBs.

Alternative considered: give each Omnigent expert its own direct DB
connection. That makes early experiments easy, but it prevents consistent
provider swapping, cost control, source authority, redaction, and migration.

### Decision: Usage metering and budget rails live in the gateway

The gateway should emit usage events for governed memory operations and enforce
budget rails that can allow, warn, require approval, degrade, or deny. Billing
records must not store memory content.

Alternative considered: rely on each provider's billing. Provider billing is
still useful for reconciliation, but it does not know xFactory workflow,
customer subject, consent, route, or domain context.

### Decision: Promotions are explicit workflow objects

Customer-to-client and customer-to-domain learning must flow through promotion
candidates reviewed by the appropriate Hermes layer. No provider may silently
promote memories across layers.

Alternative considered: allow memory providers to consolidate and share learned
facts automatically. Automatic consolidation is useful inside a scope, but
cross-layer movement needs consent, de-identification, review, and traceability.

### Decision: Requirements are tiered so "conformant gateway" has a minimal meaning

The requirements are grouped into conformance tiers so implementation and
domain adoption proceed incrementally instead of treating every SHALL as
equally blocking:

```text
M0  core boundary: rails-before-I/O, context packets, caller identity,
    credential custody, consent contract, fail modes, audit
M1  lifecycle: promotion review, revocation and erasure, tombstones
M2  subject safety: adult/minor rails, guardian authority, minor-safe packets
M3  economics: usage metering, budgets, billing events
M4  portability: provider migration (dual-write, shadow-read, cutover,
    rollback)
```

A gateway implementation is minimally conformant at M0. Domains must not
enable governed authoritative writes through a gateway below M0. Higher tiers
gate the features they describe (for example, no provider migration without
M4 conformance) but do not block M0 adoption.

Alternative considered: keep a flat requirement list. That reads simpler but
recreates the documentation-outruns-implementation failure mode this repo has
already experienced, and gives implementers no order of attack.

### Decision: First gateway runtime is an xFactory control-plane module

The first implementation lives inside xFactory control-plane code as a module
with a service-ready API boundary (resolving the former open question). It can
be extracted to a standalone service later without changing the
`xfactory.memory.*` surface. This keeps the first vertical slice cheap while
forcing the API to be defined as if remote.

Regardless of placement, every gateway call must carry an authenticated caller
identity (Hermes role, council, or Omnigent worker identity plus
`consumer_layer`), verified before rails run. A gateway that cannot attribute
a call to a caller identity must deny the call.

### Decision: Workers and Hermes roles never hold provider credentials

Bypass prevention is credential custody, not labeling. Worker and Hermes-role
identities are never issued provider credentials in any environment. Provider
credentials exist only inside the gateway's binding resolution path, obtained
through short-lived credential broker grants at operation time.

Diagnostic direct-provider access uses separate operator-scoped credentials
that are read-only, bound to non-production or shadow namespaces, and never
issued to worker identities. The earlier framing "direct calls are treated as
non-authoritative" remains true but is now a consequence of custody (workers
cannot reach governed namespaces at all) rather than an interpretive rule.

### Decision: Consent profiles are a first-class contract backed by Hermes state

The consent profile schema is the first schema deliverable of this change
(before provider profiles), because every read rail decision depends on it.
Consent profiles are backed by Hermes operational state initially (resolving
the former open question); a dedicated consent service may replace the backing
store later without changing the consent profile contract. Consent profiles
are versioned, and every consent change is an audited event with actor,
authority basis, and effective time.

### Decision: Revocation and erasure are distinct operations

`revoke_or_tombstone` blocks future use at the rail layer while preserving
audit. It does not remove content from providers. A separate `erase_content`
operation exists for legal erasure (GDPR/HIPAA-class obligations). Provider
profiles must declare erasure capability per port: `hard_delete`,
`requires_reindex`, `companion_managed`, or `unsupported`. Routing
regulated-subject memory to a provider whose erasure capability is
`unsupported` requires an explicit, documented compensating control and shows
up in conformance validation. Erasure completion is itself an audited event
with provider-side confirmation refs.

### Decision: Context packets are leashed after issuance

Packets bound entry to memory; the leash bounds what happens after issuance.
Every context packet carries an expiry (TTL appropriate to the workflow), is
purpose-bound (a packet issued for one workflow purpose is invalid input for
another), and its content is classified: worker-local memory derived from
packet content inherits the packet's redaction class and subject refs, so
governed memory cannot be laundered into ungoverned worker-local stores.
AgentMemory writes that embed packet-derived content above their redaction
class are rail violations, not merely promotion candidates.

### Decision: Fail modes are explicit and break-glass is audited

The gateway is a synchronous dependency of agent runtime, so failure behavior
is part of the contract, not an ops detail:

- Governed writes, promotions, revocations, and migrations always fail closed.
- Governed reads and context packets may degrade according to a declared
  per-operation-class policy: serve a previously issued, still-unexpired,
  already-redacted packet from cache, or deny. Never bypass rails to a
  provider.
- Domains may declare break-glass workflows (for example Medx emergency
  escalation). Break-glass grants a pre-defined minimal emergency packet
  profile, requires the caller to assert the emergency basis, always succeeds
  or fails within a bounded time, and always produces an enhanced audit
  record plus a mandatory retrospective review task.

Alternative considered: leave availability behavior to the implementation.
For a component that sits between a clinician-facing agent and patient
context, undefined failure behavior is itself a safety defect.

### Decision: Budget enforcement is synchronous only where it must be

Hard budget limits are enforced synchronously before provider I/O only for
operation classes marked expensive in the provider profile (bulk retrieval,
re-embedding, cross-provider migration). Routine operations use asynchronous
soft-limit accounting with warn/require-approval escalation. This keeps the
metering rail off the latency-critical path while preserving deny-capability
where cost is real.

### Decision: Migration changes routes, not Hermes calls

Memory model migration should happen through xFactory route tables, provider
mappings, backfill jobs, dual-write, shadow-read, canary, cutover, and rollback.
Hermes should continue calling the same `xfactory.memory.*` operations during
migration.

Alternative considered: rewire Hermes to a new provider during migration. That
would make every memory-provider migration a Hermes behavior change and would
break the portability boundary.

## Threat Model

The gateway is a security boundary, so its design must answer adversarial
cases, not only happy paths. Top abuse cases and the rail that kills each:

1. **Prompt-injected role requests an over-broad packet.** A compromised or
   manipulated Hermes role asks for "all memory" or an unrelated subject's
   context. Killed by: purpose-bound context packets (purpose must resolve to
   an approved active workflow), consent rail, and caller-identity scope
   checks (a role only reaches subjects its layer and binding allow).
2. **Purpose-string gaming ("purpose: emergency").** Callers assert an
   emergency basis to reach the break-glass path. Killed by: break-glass being
   available only to workflows a domain pre-declared as break-glass-eligible,
   the minimal emergency packet profile (not a full-context packet), and
   mandatory retrospective review of every break-glass use.
3. **Confused deputy across tenants.** A domain-level council or shared worker
   requests customer memory using its own (broader) authority on behalf of the
   wrong client. Killed by: provider bindings scoped to
   layer+client+subject, and the rule that packet subject refs must match the
   requesting workflow's declared subject — mismatches deny before I/O.
4. **Worker bypasses the gateway for provider speed.** Killed by: credential
   custody (worker identities hold no provider credentials; governed
   namespaces are unreachable), plus diagnostic credentials being read-only
   and non-production-scoped.
5. **Memory laundering via worker-local stores.** Packet content is cached
   into AgentMemory, then later promoted or leaked without its original
   redaction class. Killed by: the packet leash (derivatives inherit
   redaction class and subject refs) and promotion review requiring source
   refs that trace back to the originating packet.
6. **Cross-tenant residue inside a shared provider.** Namespace collisions or
   provider-side search that spans tenants. Killed by: provider mapping
   metadata (canonical id + namespace + layer per record), per-tenant
   namespace requirements in provider profiles, and conformance fixtures that
   probe cross-namespace reads.

Conformance fixtures for these six cases are required at the tier that
introduces the relevant rail (cases 1, 3, 4 at M0; case 5 at M1; case 2 at
M0 break-glass; case 6 at M0 mapping).

## Risks / Trade-offs

- Gateway indirection adds integration work -> keep the first tool surface small
  and prove one GBrain vertical slice first; conformance tiers make M0 the
  only blocking scope.
- The gateway is a single synchronous choke point for agent runtime -> declared
  fail modes per operation class, cached degraded reads, break-glass for
  declared emergency workflows, and latency budgets recorded in provider
  profiles.
- Provider capability mismatch may frustrate teams -> use provider profiles to
  declare unsupported ports and required companion stores.
- Credential and billing logic can make the gateway heavy -> keep provider
  grants scoped and short-lived, and move billing aggregation off the hot path.
- Subject-safety policy can become domain-specific quickly -> keep a canonical
  subject-safety profile shape and let DomainxFactories specialize allowed age
  bands, approvals, interaction modes, redaction, and retention.
- Direct GBrain tools may bypass rails -> treat direct provider tools as
  non-authoritative for governed memory and later restrict authoritative writes.
- Context packets may omit useful memory -> include traceable retrieval
  diagnostics and allow Hermes to request another packet with a new purpose.
- Expert context packets may include stale, uncited, or below-threshold
  knowledge -> require source-authority policy, freshness metadata, citations,
  and downgrade or denial behavior before expert provider I/O returns context.
- Omnigent workers may bypass xFactory for expert DB speed -> treat direct
  expert DB calls as diagnostic or experimental unless routed through gateway
  bindings and audit.
- Promotion review may slow learning -> support lightweight promotion candidates
  with clear status and batch review.
- Migration can silently lose meaning across providers -> preserve canonical
  object IDs, provider mappings, authority levels, consent refs, knowledge
  source refs, source-authority levels, and audit refs.
- Domain implementations may diverge -> require conformance fixtures for rails,
  provider profiles, and context packets.

## Migration Plan

1. Add architecture and OpenSpec requirements.
2. Add gateway request, response, provider profile, provider binding, provider
   mapping, subject-safety profile, context packet, promotion, usage event,
   migration manifest, expert context packet, expert knowledge source, and
   audit schemas.
3. Add example GBrain, Honcho, AgentMemory, local-store, root-truth DB,
   case-memory, playbook, and evaluation-memory provider profiles.
4. Add Hermes configuration that points governed memory calls at xFactory.
5. Implement a local gateway module or service with deny-by-default rails.
6. Add provider grant resolution through the credential broker.
7. Add a GBrain adapter behind the gateway.
8. Register `xfactory.memory.*` tools in Hermes.
9. Add migration route-table examples and dual-write/shadow-read fixtures for
   Customer Hermes memory and Omnigent expert DB routes.
10. Update Hermes guidance so direct GBrain access is diagnostic or
   non-authoritative unless explicitly approved.
11. Add conformance tests for consent denial, subject-safety denial, source-ref
   denial, redaction, promotion review, revocation, billing event emission,
   migration route behavior, expert source-authority denial, expert context
   packet behavior, and provider profile validation.
12. Add DomainxFactory examples for Patient Hermes, Managed System Hermes,
   Medx diagnostic reviewer expert context, and Opsx runbook expert context.

Rollback is straightforward during early rollout: keep existing provider tools
available for diagnostics, disable gateway-backed authoritative writes, and
continue using existing Hermes memory helper behavior until a domain stack
passes conformance.

## Open Questions

Resolved in this revision (2026-07-03): gateway placement (xFactory
control-plane module with service-ready API) and consent backing store
(Hermes operational state first, behind a stable consent profile contract) —
see Decisions above.

- Which provider should carry the first Patient Hermes vertical slice: GBrain
  alone, GBrain plus Postgres, or GBrain plus a graph store?
- How strict should the initial direct-provider restriction be for existing
  Hermes agents?
- Which system owns invoice generation after the gateway emits usage events?
- Should the first migration proof use GBrain-to-GBrain version migration or
  GBrain-to-local-store migration?
- Which DomainxFactory should provide the first protected-subject example:
  MedxFactory minor patient, education minor learner, or AdxFactory child-safe
  marketing prohibition?
- Which expert DB route should provide the first Omnigent proof: Medx root
  truth plus case memory, Opsx runbook/playbook memory, or codexFactory project
  engineering knowledge?
