## 0. Rename And Governance Housekeeping

- [x] 0.1 `git mv openspec/changes/add-customer-memory-gateway-architecture/specs/customer-memory-gateway openspec/changes/add-customer-memory-gateway-architecture/specs/memory-gateway` (capability renamed to `memory-gateway`; see proposal).
- [x] 0.2 Retrospectively record approval for tasks 7.6/7.7, which were implemented (fill/maintenance taxonomy + domain mapping docs) before this change was archived — note the exception in the change record rather than reverting.

## 1. Architecture And Contract Schemas

- [x] 1.1 Add `contracts/memory-gateway/consent-profile.schema.yaml` FIRST — the versioned consent profile contract every read rail depends on (subject refs, purposes, authority basis, guardian/delegate authority, effective windows, audit refs).
- [x] 1.2 Add `contracts/memory-gateway/` request, response, provider profile (including per-port erasure capability and expensive-operation classes), provider binding, provider mapping, subject-safety profile, context packet (including TTL, purpose binding, redaction class), expert context packet, expert knowledge source, promotion candidate, migration manifest, usage event, revocation, erasure, break-glass profile, and audit event schemas.
- [x] 1.3 Add closed-set vocabularies for gateway operations, canonical ports, provider roles, expert provider roles, provider support levels, binding custody modes, subject categories, age bands, guardian/delegate authority modes, rail denial reasons, privacy classes, authority levels, billing modes, migration modes, knowledge scopes, promotion statuses, conformance tiers (M0-M4), fail modes per operation class, erasure capability levels, and redaction classes.
- [x] 1.4 Add a schema README that explains which files are canonical xFactory contracts and which files are examples.
- [x] 1.5 Link the gateway schemas from the existing contract manifest or contracts README, and register them in `contracts/CHANGELOG.md`.

## 2. Provider Profiles And Examples

- [x] 2.1 Add a GBrain provider profile example that maps canonical Customer Hermes objects to GBrain-backed memory.
- [x] 2.2 Add Honcho and AgentMemory provider profile examples that preserve their profile-memory and worker-local boundaries.
- [x] 2.3 Add a local Postgres or document-store profile example for deployments that do not start with GBrain.
- [x] 2.4 Add provider mapping examples that include canonical object id, provider id, provider object ref, namespace, layer, and audit refs.
- [x] 2.5 Add provider binding examples for Opensoft-hosted, customer-owned, hybrid, and internal development memory providers.
- [x] 2.6 Add adult and minor subject-safety examples with direct consent, guardian/delegate consent, redaction, retention, personalization, and audit policy.
- [x] 2.7 Add expert knowledge provider profile examples for root-truth DB, vector index, source workspace, case-pattern store, playbook store, and evaluation memory.
- [x] 2.8 Add expert provider binding examples with allowed expert profiles, knowledge scopes, source-authority minimums, allowed uses, prohibited uses, and short-lived grant settings.

## 3. Rails And Conformance Fixtures

- [x] 3.1 Add fixtures for read denial when customer consent is missing or withdrawn.
- [x] 3.2 Add fixtures for write denial when required source refs are missing.
- [x] 3.3 Add fixtures for write denial when secret-like content is detected.
- [x] 3.4 Add fixtures for promotion denial when de-identification or required review is missing.
- [x] 3.5 Add fixtures for successful context packet creation with trace refs, redaction metadata, and current state snapshot refs.
- [x] 3.6 Add fixtures for provider binding denial when a layer, operation, client, or subject scope is not allowed.
- [x] 3.7 Add fixtures for minor subject denial when guardian/delegate authority is missing.
- [x] 3.8 Add fixtures for minor subject degradation when prohibited personalization or autonomous sensitive disclosure is requested.
- [x] 3.9 Add fixtures for usage event emission and budget hard-limit denial.
- [x] 3.10 Add fixtures for migration dual-write, shadow-read, cutover, and rollback states.
- [x] 3.11 Add provider profile validation checks for required ports, unsupported operations, companion stores, and prohibited content.
- [x] 3.12 Add fixtures for expert context packet creation with expert profile, source refs, knowledge scopes, allowed uses, prohibited uses, provider refs, usage refs, and audit refs.
- [x] 3.13 Add fixtures for expert source-authority denial or degradation when knowledge is uncited, stale, prohibited, or below the required authority threshold.
- [x] 3.14 Add fixtures for expert DB migration route behavior across source and target providers while Omnigent keeps using the same gateway operation.
- [x] 3.15 Add fixtures for the six threat-model cases (over-broad packet request, purpose gaming/break-glass abuse, confused deputy across tenants, worker bypass via credential absence, memory laundering via worker-local stores, cross-tenant namespace residue), each asserting the denying rail and audit event.
- [x] 3.16 Add fixtures for caller-identity denial (unattributable call), diagnostic credential scope (read-only, non-production), and worker-identity provider-credential absence.
- [x] 3.17 Add fixtures for fail modes: write fail-closed during gateway outage, read degradation to cached redacted packet, degradation denial when no cache exists, break-glass minimal packet with caller identity, subject scope, provider binding, redaction, max TTL, enhanced audit, notifications, retrospective review SLA, and denial for undeclared workflows.
- [x] 3.18 Add fixtures for packet leash: TTL expiry re-runs rails, cross-purpose packet rejection, packet-derived worker memory redaction inheritance violation.
- [x] 3.19 Add fixtures for erasure: provider-side deletion with confirmation refs, routing denial to `unsupported`-erasure providers for domain-policy-constrained subjects, revocation-does-not-claim-erasure tracking.
- [x] 3.20 Add fixtures for consent contract: rail decision records consent version, consent change audit (actor, authority basis, effective time), backing-store swap without contract change.

## 4. Gateway Runtime Slice

- [x] 4.1 Implement the gateway as an xFactory control-plane module with a service-ready API boundary (decision recorded in design.md; extraction to a standalone service must not change the `xfactory.memory.*` surface).
- [x] 4.1a Implement caller-identity verification (deny unattributable calls) before rail execution.
- [x] 4.2 Implement the first gateway operation path for `xfactory.memory.context_packet`.
- [x] 4.3 Implement deny-by-default rail checks before provider I/O.
- [x] 4.4 Implement subject-safety rail resolution for adult and minor profiles before provider I/O.
- [x] 4.5 Implement provider binding resolution and short-lived provider grant stubs before adapter dispatch.
- [x] 4.6 Implement provider adapter dispatch with a GBrain adapter stub or local fake adapter.
- [x] 4.7 Emit audit events for allowed and denied gateway operations.
- [x] 4.8 Emit content-free usage events for successful and denied governed memory operations.
- [x] 4.9 Implement the first expert context packet path for `consumer_layer=domain_omnigent` with a fake or local expert knowledge adapter.
- [x] 4.10 Implement fail-mode behavior: fail-closed writes, declared read degradation from packet cache, and the break-glass path (minimal emergency packet, bounded time, enhanced audit, retrospective review task).
- [x] 4.11 Implement packet TTL and purpose-binding checks at packet issuance and consumption.
- [x] 4.12 Scope the M0 tier as the definition of done for governed reads/context packets, and define M0 write-minimum separately as write schema + source-backed write rail + deny-before-I/O + provider mapping + audit; M1-M4 features (promotion, erasure, metering, migration) follow as separate slices.

## 5. Hermes Wiring

- [x] 5.1 Add Hermes memory gateway configuration that points governed memory calls at xFactory memory tools.
- [x] 5.2 Register or document the `xfactory.memory.*` tool surface for Hermes roles and councils.
- [x] 5.3 Update Hermes guidance so direct GBrain calls are read-only, operator-scoped, non-production/shadow diagnostics and can never create authoritative memory.
- [x] 5.4 Add a smoke path where Hermes requests a context packet through xFactory and receives GBrain-backed, redacted, traceable memory.
- [x] 5.5 Add a smoke path showing Hermes continues using the same memory tool while xFactory changes provider route state.
- [x] 5.6 Add Omnigent guidance so direct expert DB calls are read-only, operator-scoped, non-production/shadow diagnostics and can never create authoritative expert context.
- [x] 5.7 Add a smoke path where Omnigent requests an expert context packet through xFactory and receives source-scoped, traceable expert knowledge.

## 6. Domain Factory Integration

- [x] 6.1 Add a DomainxFactory `customer_memory_gateway` stack configuration example.
- [x] 6.2 Add a MedxFactory Patient Hermes context packet example.
- [x] 6.3 Add an OpsxFactory Managed System Hermes context packet example.
- [x] 6.4 Add a MedxFactory or generic Customer Hermes migration manifest example.
- [x] 6.5 Add a MedxFactory minor Patient Hermes subject-safety example and an adult Patient Hermes comparison example.
- [x] 6.6 Update the domain starter pack so new DomainxFactories scaffold memory gateway placeholders without selecting a required provider.
- [x] 6.7 Add a DomainxFactory `omnigent_expert_memory_gateway` stack configuration example.
- [x] 6.8 Add MedxFactory diagnostic reviewer and OpsxFactory runbook expert context packet examples.
- [x] 6.9 Add a `memory_gateway` block to `contracts/schemas/xfactory-domain-stack.schema.yaml` (providers, per-layer-scope bindings, declared break-glass workflows, conformance tier) and extend `scripts/validate-domain-factory.py` to validate it and to flag provider endpoints/connection refs inside `hermes/` overlay files as direct-binding violations.
- [x] 6.10 Add a MedxFactory break-glass example: emergency clinical escalation declared as break-glass-eligible with allowed actor classes, subject scope, minimal emergency packet profile, max TTL, notification/escalation targets, and retrospective review SLA.

## 7. Validation And Documentation

- [x] 7.1 Add validation commands or scripts for gateway schemas, provider profiles, and conformance fixtures.
- [x] 7.2 Update documentation indexes to reference the xFactory Memory Gateway architecture.
- [x] 7.3 Run OpenSpec validation for the proposal artifacts.
- [x] 7.4 Run repository documentation and schema validation commands that apply to the touched files.
- [x] 7.5 Validate that expert provider profiles and DomainxFactory expert route examples declare source-authority policy, allowed knowledge scopes, migration behavior, and audit requirements.
- [x] 7.6 Add the openxFactory customer memory fill and maintenance taxonomy.
- [x] 7.7 Add DomainxFactory mapping docs for MedxFactory, OpsxFactory, codexFactory, LedgerxFactory, and AdxFactory.

## Bookkeeping correction (2026-08-23, `govern-openspec-corpus-membership`)

`proposal.md` gained TWO header lines in one edit — `Status: ratified` and a single `Ratified:` citation, at real lines 1 and 2, both well inside the fifteen-real-line header window. Nothing else on the page moved: the writer asserted per file that deleting the two header lines plus a blank separator recovers the original bytes, and refused to write otherwise. The ruling is OQ-6's of 2026-08-23 (Brett Heap, in-session multiple-choice round), which DEPARTED from its own recommendation — no grandfather, no contract date, no reduced-severity class — and backfills every headerless proposal from its OWN record, stopping and reporting rather than inventing where a record cannot carry one. The status and the citation are coupled because the promoted rule in `openspec/specs/document-lifecycle/spec.md` holds that a bare, uncited `Status: ratified` is a violation whatever else the document says.

This document's citation takes derivation route (b), the archive act itself, because no explicit ratification act appears anywhere on the record: the archive commit `d5ada44` applied this change's spec delta into the canonical specs, and a change whose spec deltas have PROMOTED is ratified by construction — the reasoning `bdd09c2` recorded and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites as its own. The three-way floor is cleared on the DATE axis and a resolvable RECORD PATH, measured through `doc_health.families` before the line was written, not assumed.

It is entered in `docs/archive-record-discrepancies.md` as C2's successor. This note travels with the change, as 5B's twenty-seven do.
