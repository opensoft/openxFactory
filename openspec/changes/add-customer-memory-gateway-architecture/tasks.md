## 0. Rename And Governance Housekeeping

- [ ] 0.1 `git mv openspec/changes/add-customer-memory-gateway-architecture/specs/customer-memory-gateway openspec/changes/add-customer-memory-gateway-architecture/specs/memory-gateway` (capability renamed to `memory-gateway`; see proposal).
- [ ] 0.2 Retrospectively record approval for tasks 7.6/7.7, which were implemented (fill/maintenance taxonomy + domain mapping docs) before this change was archived — note the exception in the change record rather than reverting.

## 1. Architecture And Contract Schemas

- [ ] 1.1 Add `contracts/memory-gateway/consent-profile.schema.yaml` FIRST — the versioned consent profile contract every read rail depends on (subject refs, purposes, authority basis, guardian/delegate authority, effective windows, audit refs).
- [ ] 1.2 Add `contracts/memory-gateway/` request, response, provider profile (including per-port erasure capability and expensive-operation classes), provider binding, provider mapping, subject-safety profile, context packet (including TTL, purpose binding, redaction class), expert context packet, expert knowledge source, promotion candidate, migration manifest, usage event, revocation, erasure, break-glass profile, and audit event schemas.
- [ ] 1.3 Add closed-set vocabularies for gateway operations, canonical ports, provider roles, expert provider roles, provider support levels, binding custody modes, subject categories, age bands, guardian/delegate authority modes, rail denial reasons, privacy classes, authority levels, billing modes, migration modes, knowledge scopes, promotion statuses, conformance tiers (M0-M4), fail modes per operation class, erasure capability levels, and redaction classes.
- [ ] 1.4 Add a schema README that explains which files are canonical xFactory contracts and which files are examples.
- [ ] 1.5 Link the gateway schemas from the existing contract manifest or contracts README, and register them in `contracts/CHANGELOG.md`.

## 2. Provider Profiles And Examples

- [ ] 2.1 Add a GBrain provider profile example that maps canonical Customer Hermes objects to GBrain-backed memory.
- [ ] 2.2 Add Honcho and AgentMemory provider profile examples that preserve their profile-memory and worker-local boundaries.
- [ ] 2.3 Add a local Postgres or document-store profile example for deployments that do not start with GBrain.
- [ ] 2.4 Add provider mapping examples that include canonical object id, provider id, provider object ref, namespace, layer, and audit refs.
- [ ] 2.5 Add provider binding examples for Opensoft-hosted, customer-owned, hybrid, and internal development memory providers.
- [ ] 2.6 Add adult and minor subject-safety examples with direct consent, guardian/delegate consent, redaction, retention, personalization, and audit policy.
- [ ] 2.7 Add expert knowledge provider profile examples for root-truth DB, vector index, source workspace, case-pattern store, playbook store, and evaluation memory.
- [ ] 2.8 Add expert provider binding examples with allowed expert profiles, knowledge scopes, source-authority minimums, allowed uses, prohibited uses, and short-lived grant settings.

## 3. Rails And Conformance Fixtures

- [ ] 3.1 Add fixtures for read denial when customer consent is missing or withdrawn.
- [ ] 3.2 Add fixtures for write denial when required source refs are missing.
- [ ] 3.3 Add fixtures for write denial when secret-like content is detected.
- [ ] 3.4 Add fixtures for promotion denial when de-identification or required review is missing.
- [ ] 3.5 Add fixtures for successful context packet creation with trace refs, redaction metadata, and current state snapshot refs.
- [ ] 3.6 Add fixtures for provider binding denial when a layer, operation, client, or subject scope is not allowed.
- [ ] 3.7 Add fixtures for minor subject denial when guardian/delegate authority is missing.
- [ ] 3.8 Add fixtures for minor subject degradation when prohibited personalization or autonomous sensitive disclosure is requested.
- [ ] 3.9 Add fixtures for usage event emission and budget hard-limit denial.
- [ ] 3.10 Add fixtures for migration dual-write, shadow-read, cutover, and rollback states.
- [ ] 3.11 Add provider profile validation checks for required ports, unsupported operations, companion stores, and prohibited content.
- [ ] 3.12 Add fixtures for expert context packet creation with expert profile, source refs, knowledge scopes, allowed uses, prohibited uses, provider refs, usage refs, and audit refs.
- [ ] 3.13 Add fixtures for expert source-authority denial or degradation when knowledge is uncited, stale, prohibited, or below the required authority threshold.
- [ ] 3.14 Add fixtures for expert DB migration route behavior across source and target providers while Omnigent keeps using the same gateway operation.
- [ ] 3.15 Add fixtures for the six threat-model cases (over-broad packet request, purpose gaming/break-glass abuse, confused deputy across tenants, worker bypass via credential absence, memory laundering via worker-local stores, cross-tenant namespace residue), each asserting the denying rail and audit event.
- [ ] 3.16 Add fixtures for caller-identity denial (unattributable call), diagnostic credential scope (read-only, non-production), and worker-identity provider-credential absence.
- [ ] 3.17 Add fixtures for fail modes: write fail-closed during gateway outage, read degradation to cached redacted packet, degradation denial when no cache exists, break-glass minimal packet with enhanced audit + retrospective review task, break-glass denial for undeclared workflows.
- [ ] 3.18 Add fixtures for packet leash: TTL expiry re-runs rails, cross-purpose packet rejection, packet-derived worker memory redaction inheritance violation.
- [ ] 3.19 Add fixtures for erasure: provider-side deletion with confirmation refs, routing denial to `unsupported`-erasure providers for regulated subjects, revocation-does-not-claim-erasure tracking.
- [ ] 3.20 Add fixtures for consent contract: rail decision records consent version, consent change audit (actor, authority basis, effective time), backing-store swap without contract change.

## 4. Gateway Runtime Slice

- [ ] 4.1 Implement the gateway as an xFactory control-plane module with a service-ready API boundary (decision recorded in design.md; extraction to a standalone service must not change the `xfactory.memory.*` surface).
- [ ] 4.1a Implement caller-identity verification (deny unattributable calls) before rail execution.
- [ ] 4.2 Implement the first gateway operation path for `xfactory.memory.context_packet`.
- [ ] 4.3 Implement deny-by-default rail checks before provider I/O.
- [ ] 4.4 Implement subject-safety rail resolution for adult and minor profiles before provider I/O.
- [ ] 4.5 Implement provider binding resolution and short-lived provider grant stubs before adapter dispatch.
- [ ] 4.6 Implement provider adapter dispatch with a GBrain adapter stub or local fake adapter.
- [ ] 4.7 Emit audit events for allowed and denied gateway operations.
- [ ] 4.8 Emit content-free usage events for successful and denied governed memory operations.
- [ ] 4.9 Implement the first expert context packet path for `consumer_layer=domain_omnigent` with a fake or local expert knowledge adapter.
- [ ] 4.10 Implement fail-mode behavior: fail-closed writes, declared read degradation from packet cache, and the break-glass path (minimal emergency packet, bounded time, enhanced audit, retrospective review task).
- [ ] 4.11 Implement packet TTL and purpose-binding checks at packet issuance and consumption.
- [ ] 4.12 Scope the M0 tier as the definition of done for this section; M1-M4 features (promotion, erasure, metering, migration) follow as separate slices.

## 5. Hermes Wiring

- [ ] 5.1 Add Hermes memory gateway configuration that points governed memory calls at xFactory memory tools.
- [ ] 5.2 Register or document the `xfactory.memory.*` tool surface for Hermes roles and councils.
- [ ] 5.3 Update Hermes guidance so direct GBrain calls are diagnostic or non-authoritative unless explicitly routed through the gateway.
- [ ] 5.4 Add a smoke path where Hermes requests a context packet through xFactory and receives GBrain-backed, redacted, traceable memory.
- [ ] 5.5 Add a smoke path showing Hermes continues using the same memory tool while xFactory changes provider route state.
- [ ] 5.6 Add Omnigent guidance so direct expert DB calls are diagnostic or experimental unless routed through the gateway.
- [ ] 5.7 Add a smoke path where Omnigent requests an expert context packet through xFactory and receives source-scoped, traceable expert knowledge.

## 6. Domain Factory Integration

- [ ] 6.1 Add a DomainxFactory `customer_memory_gateway` stack configuration example.
- [ ] 6.2 Add a MedxFactory Patient Hermes context packet example.
- [ ] 6.3 Add an OpsxFactory Managed System Hermes context packet example.
- [ ] 6.4 Add a MedxFactory or generic Customer Hermes migration manifest example.
- [ ] 6.5 Add a MedxFactory minor Patient Hermes subject-safety example and an adult Patient Hermes comparison example.
- [ ] 6.6 Update the domain starter pack so new DomainxFactories scaffold memory gateway placeholders without selecting a required provider.
- [ ] 6.7 Add a DomainxFactory `omnigent_expert_memory_gateway` stack configuration example.
- [ ] 6.8 Add MedxFactory diagnostic reviewer and OpsxFactory runbook expert context packet examples.
- [ ] 6.9 Add a `memory_gateway` block to `contracts/schemas/xfactory-domain-stack.schema.yaml` (providers, per-layer-scope bindings, declared break-glass workflows, conformance tier) and extend `scripts/validate-domain-factory.py` to validate it and to flag provider endpoints/connection refs inside `hermes/` overlay files as direct-binding violations.
- [ ] 6.10 Add a MedxFactory break-glass example: emergency clinical escalation declared as break-glass-eligible with its minimal emergency packet profile and retrospective review routing.

## 7. Validation And Documentation

- [ ] 7.1 Add validation commands or scripts for gateway schemas, provider profiles, and conformance fixtures.
- [ ] 7.2 Update documentation indexes to reference the xFactory Memory Gateway architecture.
- [ ] 7.3 Run OpenSpec validation for the proposal artifacts.
- [ ] 7.4 Run repository documentation and schema validation commands that apply to the touched files.
- [ ] 7.5 Validate that expert provider profiles and DomainxFactory expert route examples declare source-authority policy, allowed knowledge scopes, migration behavior, and audit requirements.
- [x] 7.6 Add the openxFactory customer memory fill and maintenance taxonomy.
- [x] 7.7 Add DomainxFactory mapping docs for MedxFactory, OpsxFactory, codexFactory, LedgerxFactory, and AdxFactory.
