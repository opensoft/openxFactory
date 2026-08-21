# openxFactory

`openxFactory` documents the open reference stack and domain-neutral xFactory
layer used by Opensoft domain factory projects.

Use these terms precisely:

- `xFactory` is the top-level product family and aggregation repository.
- `openxFactory` is the open reference stack and canonical contract source.
- The `xFactory layer` is the domain-neutral stack composition and workflow
  governance layer inside `openxFactory` and every DomainxFactory. It defines
  which stack parts are required for a domain and how work moves through gates,
  routing, traceability, source authority, memory promotion, credentials, and
  audit. It also governs memory and knowledge provider bindings, migrations,
  metering, and bounded context packets for Subject Hermes and Domain
  Omnigent.
- A `DomainxFactory` is an instantiated domain stack such as `MedxFactory`,
  `LedgerxFactory`, `OpsxFactory`, `AdxFactory`, or `codexFactory`.

See [Terminology And Repository Topology](docs/terminology-and-repo-topology.md)
for the stack, layer, and submodule ownership model.

It defines reusable contracts for:

- workflow gates
- state transitions
- traceability
- routing
- approval handoffs
- review records
- audit expectations
- authority boundaries between governance, workflow, execution, and enforcement layers

## Core Boundary

`openxFactory` is domain-neutral, but it is a stack, not only a layer.

```text
Hermes
  owns intent, policy, memory, approval, and governance history.

xFactory layer
  owns stack composition, contracts, gates, traceability, routing, state
  transitions, memory/knowledge provider governance, and audit.

Domain factory repos
  own domain-specific execution behavior.

Domain Omnigent layers
  run bounded domain agents under Hermes policy and xFactory layer gates,
  including expert memory and knowledge DB access through xFactory context
  packets.

External enforcement systems
  enforce final state where applicable.
```

Domain examples:

```text
codexFactory
  uses Omnigent to run coding and engineering agents.

MedxFactory
  uses Omnigent to run clinical and medical reasoning agents.

OpsxFactory
  uses Omnigent to run sysops, devops, and IT administration agents.
```

## Documentation

Core domain-neutral docs:

- [Architecture](docs/architecture.md)
- [Terminology And Repository Topology](docs/terminology-and-repo-topology.md)
- [openXdox — Capability Naming Record](docs/openxdox-naming.md) (the neutral review-and-disposition workbench; handle `dox`, surface `doxBench`)
- [openXdox Dispatch-Credential Binding Runbook](docs/openxdox-dispatch-credential-binding.md) (operator-hosted vs self-hosted binding for the intent-plane dispatch credential)
- [Party Ladder](docs/party-ladder.md) (author/operator → tenant → subject → third parties; frozen-word reading rules)
- [xFactory Domain Factory Model](docs/xfactory-domain-factory-model.md)
- [Governed Derived Model](docs/governed-derived-model.md)
- [Domain-Ontology Semantic Inventory And Decisions](docs/domain-ontology-semantic-decisions.md)
  (the kernel's term-by-term owners, collision/leak/gap registers, identifier
  grammar, compatibility rubric; realization record of `add-domain-ontology-layer`
  tasks 1.1–1.6 — the contract family lives at
  [contracts/domain-ontology/](contracts/domain-ontology/README.md);
  pilot evidence: [Pilot Report](docs/domain-ontology-pilot-report.md) ·
  [Adoption Handoff](docs/domain-ontology-adoption-handoff.md) ·
  [Guide](docs/domain-ontology-guide.md))
- [Deployment-Handoff Realization Handoff](docs/deployment-handoff-realization-handoff.md)
  (the OpsxFactory + codexFactory successor-change packets for the ratified
  `deployment-handoff-boundary` capability, with the deferred decisions and
  topic-exit conditions)
- [xFactory Taxonomy Model](docs/factory-taxonomy-model.md)
- [Domain Factory Implementation Checklist](docs/domain-factory-implementation-checklist.md)
- [Domain Stack Pin Implementation Plan](docs/domain-stack-pin-implementation-plan.md)
- [xFactory Domain Factory Starter Pack](docs/domain-factory-starter-pack.md)
- [Domain Instantiation Pre-Run Questionnaire](docs/domain-instantiation-pre-run-questionnaire.md)
- [Domain Instantiation Setup Runbook](docs/domain-instantiation-setup-runbook.md)
- [openxFactory Installation Spine And Domain Overlays](docs/openxfactory-installation-spine.md)
- [xFactory Intake And Installer Plan](docs/intake-and-installer-plan.md)
- [TUI Spec Questionnaire](docs/tui-spec-questionnaire.md)
- [Self-Hosted Runtime Binding Plan](docs/self-hosted-runtime-binding-plan.md)
- [Runtime Services Plan](docs/runtime-services-plan.md)
- [Deploy Artifacts Plan](docs/deploy-artifacts-plan.md)
- [Intake Template Catalog](templates/intake/README.md)
- [Intake Subtype Install Readiness Report](docs/intake-subtype-install-readiness-report.md)
- [Intake Subtype Install Runbook](docs/intake-subtype-install-runbook.md)
- [Intake Subtype Second-Pass Gap Report](docs/intake-subtype-second-pass-gap-report.md)
- [Domain Pre-Run Simulation Report](docs/domain-pre-run-simulation-report.md)
- [Domain Repo Review Improvements](docs/domain-repo-review-improvements.md)
- [Document Lifecycle](docs/document-lifecycle.md)
- [Release Realization Flow](docs/release-realization-flow.md)
- [Doc-Health Contract](docs/doc-health.md)
  (implementation in-repo since `adopt-neutral-tooling-home`:
  `scripts/doc_health/` + `scripts/doc-health.py`, the reusable nightly
  workflow, and `scripts/sync-notebooklm-books.py`; the ideation dashboard
  runtime lives at `scripts/ideation_dashboard/` with its
  [session runbook](docs/ideation-dashboard-session-runbook.md); the
  neutrality-drift lane — the nightly scout that drafts DTN-register
  seeds from domain-factory content, `add-neutrality-drift-lane` — lives
  at `scripts/doc_health/neutrality.py` + `neutrality_dispatch.py` with
  its state under `health/neutrality-drift/`)
- [Document Catalog Adoption Guide](docs/document-catalog-adoption.md)
- [Cross-Factory Ideation Routing Adoption Guide](docs/ideation-routing-adoption.md)
- [Domain-To-Neutral Promotion Process](docs/domain-to-neutral-promotion-process.md)
- [Domain Neutralization Candidate Register](docs/domain-neutralization-candidate-register.md)
- [Installation Template Catalog](templates/installation/README.md)
- [xFactory Credential Access Model](docs/credential-access-model.md)
- [Standard Operating Procedures](docs/sops/README.md)
- [OpenAI Realtime F0 Lab Credential SOP](docs/sops/openai-realtime-f0-lab-credential.md)
- [Avatar-First UI Standard](docs/avatar-first-ui-standard.md)
  ([profile examples](examples/avatar-first-ui/README.md) ·
  [deterministic fixtures](examples/avatar-first-ui/fixtures/README.md))
- [Avatar-Client (AVC) Contract Kernel](contracts/avatar-client/README.md)
  (neutral session/consent/revocation contract family; realized at
  `contract-v1.7` with a fail-closed F0 publication gate)
- [Workflow Visualization Standard](docs/workflow-visualization-standard.md)
- [Subject Hermes Memory Model](docs/customer-hermes-memory-model.md)
- [Customer Memory Fill And Maintenance Taxonomy](docs/customer-memory-fill-maintenance-taxonomy.md)
- [xFactory Memory Gateway Architecture](docs/customer-memory-gateway-architecture.md)
- [xFactory Memory Gateway Contracts](contracts/memory-gateway/README.md)
- [Omnigent Contract Family](contracts/omnigent/README.md)
  (domain-overlay payload + install manifest; realized by
  `add-omnigent-domain-overlay`; bundle-registered)
- [Worker Enrollment Contract Family](contracts/worker-enrollment/README.md)
  (one enrollment point / two authentication modes, renewable LEASES instead of
  registrations, fail-closed minimum-app-version floor, temp-estate segregation
  by trust tier, the brokered remove-token issuance shape, and audit records no
  token value can enter; realized by
  `add-worker-enrollment-broker`; registered at `contract-v1.29`)
- [Consent Instrument Contract Family](examples/consent-instrument/README.md)
  (the neutral rung-1↔rung-2 consent instrument — the authority-chain root
  credential grants cite and termination cascades from: schemas
  `contracts/schemas/consent-instrument.schema.yaml`,
  `consent-instrument-class-registry.schema.yaml`, and
  `consent-purpose-model.schema.yaml`; canonical validator
  `scripts/validate-consent-instruments.py`; realized by
  `add-consent-instrument`, registered at `contract-v1.30`)
- [Tenant Hermes Product And Service Scaffold](docs/client-hermes-product-service-scaffold.md)
- [Client Infrastructure Liaison](docs/client-infrastructure-liaison.md)
- [Client Installation Discovery And Workflow Migration](docs/client-installation-discovery-and-migration.md)
- [Workflow Visualization Tooling Exploration](ideation/brainstorm/workflow-visualization-tooling.md)
- [Hermes Mixture Of Agents For xFactory](docs/hermes-mixture-of-agents-for-xfactory.md)
- [NotebookLM Source Workspaces](docs/notebooklm-source-workspaces.md)
- [Lifecycle Notebook Projection](docs/lifecycle-notebook-projection.md)
- [NotebookLM Projection Sync — Open Operational Item](docs/notebooklm-sync-open-item.md)
  (pending sync run, the auth blocker + the `scripts/nlm_auth.py` workaround,
  and the machine-account direction)
- [Ideation Work Area](ideation/README.md) (ratified convention; see
  [Document Lifecycle](docs/document-lifecycle.md))
- [Workflow Contract](docs/workflow-contract.md)
- [Traceability Model](docs/traceability-model.md)
- [Roles and Authority](docs/roles-and-authority.md)
- [Repository Boundary Governance](openspec/specs/repo-boundary-governance/spec.md)
- [Shared Contract Ownership](openspec/specs/shared-contract-ownership/spec.md)
- [Pattern Ledger](openspec/specs/pattern-ledger/spec.md) (recurrence-crystallization
  sensing contracts; realized at `contract-v1.19` — schemas
  `contracts/schemas/pattern-ledger-*.schema.yaml`, canonical validator
  `scripts/validate-pattern-ledger.py`, MVP fixture corpus
  `examples/pattern-ledger/`)
- [Crystallizer Contracts](openspec/specs/crystallization-decision/spec.md)
  ([decision](openspec/specs/crystallization-decision/spec.md) ·
  [build](openspec/specs/crystallization-build/spec.md) ·
  [consent](openspec/specs/crystallization-consent/spec.md) — the
  only-path-to-spend decision, episode-mined build contracts, and
  default-deny consent tiers; realized at `contract-v1.20` together with
  the crystallized-executor + rung-ceiling additions to the
  [omnigent overlay spec](openspec/specs/omnigent-domain-overlay/spec.md);
  canonical validator `scripts/validate-crystallizer-contracts.py`, MVP
  corpus continuation `examples/crystallizer/`)
- [Capability Steward](openspec/specs/crystallized-capability-registry/spec.md)
  ([registry](openspec/specs/crystallized-capability-registry/spec.md) ·
  [dispatch](openspec/specs/crystallization-dispatch/spec.md) ·
  [health](openspec/specs/capability-health/spec.md) — the single-source
  registry with pins-vs-live-authority (D10), the dispatch junction with
  deterministic fences and pure/idempotent admission (D11), and the
  proof/sentinel/drift/accounting surface with contractual renewal
  write-backs; realized at `contract-v1.21`; canonical validator
  `scripts/validate-capability-steward.py`, MVP corpus completion
  `examples/capability-steward/`)

Engineering-domain implementation docs now belong in `opensoft/codexFactory`.

Medical-domain implementation docs belong in `opensoft/MedxFactory`.

IT operations-domain implementation docs now belong in `opensoft/OpsxFactory`.

## Domain Implementations

- `opensoft/codexFactory` — software, code, repo, and engineering xFactory domain stack.
- `opensoft/MedxFactory` — medical xFactory domain stack for clinical agents and medical workflows.
- `opensoft/OpsxFactory` — IT operations, sysops, devops, identity, infrastructure, and tenant administration xFactory domain stack.
- `opensoft/LedgerxFactory` — accounting, finance, and ledger xFactory domain stack.
- `opensoft/AdxFactory` — marketing and advertising xFactory domain stack.

## Conformance

Every DomainxFactory must validate against the canonical contract:

- Stack shape: [xfactory-domain-stack schema](contracts/schemas/xfactory-domain-stack.schema.yaml)
  — Hermes layers are declared as `hermes.layers` with role keys
  `customer|client|domain`: frozen v1 machine spellings for the canonical
  **Subject / Tenant / Domain** layers (served subject / tenant-operator
  organization / reusable expert domain; mapping published at
  [contracts/policies/layer-vocabulary.yaml](contracts/policies/layer-vocabulary.yaml)).
- Validator: `scripts/validate-domain-factory.py <domain-repo> [--strict]`
  — run from the pinned openxFactory checkout, never copied into domain repos.
- Credential contracts: [xfactory-credential-contracts schema](contracts/schemas/xfactory-credential-contracts.schema.yaml)
  and `scripts/validate-credential-contracts.py <domain-repo>` — the five
  credential record kinds under `credentials/` (DTN-004). Registered in
  `contracts/manifest.yaml` for the first time at `contract-v1.33`, which also
  adds the optional `issuance_preconditions` vocabulary
  (`add-client-identity-roster`).
- Client identity roster: [xfactory-client-identity-roster schema](contracts/schemas/xfactory-client-identity-roster.schema.yaml),
  `scripts/validate-client-identity-roster.py <domain-repo>` and the packaged
  corpus at [examples/client-identity-roster](examples/client-identity-roster/README.md)
  — which identities a domain holds STANDING inside a paying client's provider
  tenant, keyed on (domain, admission surface, authority class, blast-radius
  unit, duty), with verified admission and achieved scope, and a report-only
  drift finding that mutates nothing. A domain publishes its fragments at
  `credentials/client-identity-roster/<client_ref>.yaml`, one file per
  (client, domain) pair; a domain that publishes none stays conformant and the
  check reports a notice. Registered at `contract-v1.33`
  (`add-client-identity-roster`).
- openxWallet: [contracts/openxwallet](contracts/openxwallet/README.md) (the
  holder-agnostic core) and
  [contracts/openxwallet-agent-profile](contracts/openxwallet-agent-profile/README.md)
  (its first profile), validated by `scripts/validate-openxwallet.py
  [<repo-path>] [--strict]` — a wallet is a key REFERENCE with a declared
  custody model and never key material; authority travels as attenuated
  grants; custody CAPS what a signature evidences; and wallets stay optional
  for every domain (`add-openxwallet`).
- Workflow contracts: [xfactory-workflow schema](contracts/schemas/xfactory-workflow.schema.yaml)
  and `scripts/validate-workflow-contracts.py <domain-repo>` — every
  `<domain>_workflow_contract` under `workflows/` validates against the
  neutral shape (DTN-001/002).
- Domain conformance checks + proposal support (the neutral utility pack,
  DTN-018/019/021): `scripts/check-inventory-consistency.py <domain-repo>`,
  `scripts/check-workflow-state-parity.py <domain-repo>/workflows`, and
  `scripts/check-openxfactory-pin.py <domain-repo>` — inventory/parity/pin
  checks run from the pinned openxFactory checkout, never copied into
  domain repos — plus `scripts/proposal-support.py <repo-root>`, the
  canonical supporting-document mover whose manifests doc-health family 5
  checks (adopt-neutral-utility-pack).
- Memory gateway: [contracts/memory-gateway](contracts/memory-gateway/README.md)
  and `scripts/validate-memory-gateway.py` validate the canonical gateway
  schemas, provider examples, conformance fixtures, and first runtime smoke
  path for `xfactory.memory.*`.
- Avatar reference runtime: `scripts/validate-avatar-runtime.py` statically
  proves the non-deployable, stdlib-only boundary of `xfactory/avatar_runtime/`
  (no listener, provider SDK, persistence, credential loading, or provisional
  import) for feature `specs/003-avc-reference-runtime`.
- Versioning: [Contract Versioning Policy](docs/contract-versioning-policy.md)
  and [contracts/CHANGELOG.md](contracts/CHANGELOG.md).

## OpenSpec Records

Active changes:

- [add-roster-device-admission-surface](openspec/changes/add-roster-device-admission-surface/proposal.md)
  — authored 2026-08-19. Admits the single `device` (node-inventory) admission
  surface into the closed `admission_surface` vocabulary of
  `client-identity-roster`, through the capability's own extension route, so
  OpsxFactory can enroll its ratified `microsoft_managed_node_inventory_reader`
  (`Device.Read.All` + `DeviceManagementManagedDevices.Read.All` +
  `CloudPC.Read.All`, tenant-wide read, provider offers nothing narrower — the
  roster's Decision-3 motivating example). ONE surface, not three; the three
  provider areas ride the entry as declared provider-forced breadth.
  Additive — no `contract_schema_version` bump; the realization bumps the
  bundle contract-v1.34 → contract-v1.35 with a digest refresh. Proposed on the
  node-inventory realization evidence per the reader-grant clarify decision Q4;
  the schema/bundle edit waits for Brett's ratification.
  `target_release: implementation_pending`.
- [add-doxbench-editing-phase-b](openspec/changes/add-doxbench-editing-phase-b/proposal.md)
  — authored 2026-08-18, Phase B and the EXIT of the `doxbench-editing-model`
  staged topic: all seven questions dispositioned, 26 claims settled (Brett's
  live-UI annotations and in-session rulings 2026-08-15 → 2026-08-18). Where
  Phase A was a layout-and-binding change on proven substrate, Phase B is the
  state-model generalization plus the working-session model Brett's memory
  ruling added on top of it. Ten pieces: the buffer set widens from exactly two
  to `outline` + N loaded documents (the three pinned layers re-cut together —
  the state validator, `require_outline_and_document`/`PROPOSAL_TARGETS`, and
  `SAVE_BUFFER_ORDER`, whose fixed pair becomes a RULE: outline first as session
  ancestry, then documents independently, so one document's refusal stops no
  other); the chat rail header becomes a DROPDOWN of the loaded documents whose
  selection IS the active buffer (Q1's numbered chips and LRU fold are
  overridden — the dropdown is the overflow policy, and the set is bounded and
  refuses rather than evicting text); the docs-wheel tile carries read / edit /
  save with a colored loaded-and-dirty state (Q3); each loaded document gets a
  persisted THREAD with a structured thread-state header (goal, accepted facts,
  open questions, decisions, evidence refs, pending actions) committing on that
  document's Save; share-session is an explicit commit-push-return-the-ref verb
  reusing the pull-request port's EXISTING `push` member and opening no PR; and
  per-turn context becomes a `memory-gateway` BOUNDED CONTEXT PACKET assembled
  by a Staged-Set Knowledge Service behind ONE MCP boundary (search, get_source,
  promote_finding, reindex; `graph_query` reserved and unimplemented) over an
  internal assembly port — v1 GRAPH-LESS local hybrid on the recorded Mem0-v3
  caution, graph admitted only on a named graduation trigger, backend an
  install-time declaration, approved/ratified content exempt from aggressive
  compression BY THE ASSEMBLER because only it can read a lifecycle `Status:`.
  Compression is three layers with three fidelity contracts (selection,
  semantic compaction, mechanical reversible offload); Headroom is WATCH-LISTED
  with its adoption gates recorded and is deliberately not a dependency. The
  harness is oh-my-pi behind a thin stdlib bridge that is an ADAPTER for the
  unchanged three-member `WorkbenchModelPort` — no fourth port member, one
  harness session per thread, sidecars remain the record, `auto` declares itself
  a routing rule rather than a model. Carries a chat-turn contract release
  discharging Phase A's F2 carve-out (the turn record names the DECLARED bound
  buffer, plus selected-model metadata), realized as a co-resident envelope
  family so the release is ADDITIVE and the bundle minor is allocated at
  realization, never reserved. `memory-gateway` gets ONE delta of its own after
  a full read: a declared SUBJECT-FREE LOCAL CONSUMER CLASS that must name every
  rail it declares inapplicable, refused to any consumer holding provider
  credentials or addressing a subject — because the contract's M0 set assumes a
  customer subject and a credentialed provider this consumer has neither of, and
  "inapplicable" must be declared rather than silently skipped. Seven verify-list
  items (harness memory backends, MCP depth, `SYSTEM.md` cadence, Cognee's
  embedded backend, the artifact store's location, `/shake`'s RPC surface,
  memory-gateway's realization depth) are BLOCKING pre-realization tasks.
  Sequenced AFTER `add-doxbench-editing-phase-a`, three of whose ADDED
  requirements it MODIFIES relative to that change's outcome.
  `target_release: implemented`.

- `add-subject-overlay-contract` — ARCHIVED 2026-08-15
  (`openspec/changes/archive/2026-08-15-add-subject-overlay-contract/`):
  the neutral `hermes_subject_overlay` kind is RELEASED as **`contract-v1.32`**
  (annotated tag verified; 190-entry digest inventory) and CONSUMED —
  hermes-install pins the family at the tag with parity floors covering the
  kind (1 positive + 8 negatives), and the first instance
  (codexFactory `hermes/subject/project-alfa/overlay.yaml`) is LIVE-SEEDED on
  the QA stack (repin+seed window 2026-08-15). OQ-1 ruled: kind name
  canonical, identity `subject.id`, `stricter_only` refused for
  `relation_to_baseline: additive_constraints_only`. Related landing surface
  for staged topic `subject-establishment` (DTN-017).

- [add-staged-topic-outline-template](openspec/changes/add-staged-topic-outline-template/proposal.md)
  — authored 2026-08-15 from the `staged-topic-outline-template` staged topic,
  the track Brett's 2026-08-15 sequencing ruling put in PARALLEL with
  `doxbench-editing-model` Phase A because its five questions were decisions
  rather than builds. All five accepted as recommended, so the parallel track is
  closed. A staged topic's primary fragment gets a required template — three
  required sections, and every open question carrying Context / Recommended
  answer / Explanation / Disposition status in fixed order, so a question is
  never recorded bare. The load-bearing clause is ROUND-TRIP ON DEMOTE: a topic
  that reached proposal and came back does not reset to its aspirational text,
  it carries the ACTUAL last-attempted `proposal.md` with the change id, both
  dates and the reason — nothing learned in flight is lost by falling back.
  Sections added by a human or an AI carry `Added-by:` provenance;
  proposal-element sections reuse the ratified `xspec:` marker grammar rather
  than inventing a second addressing mechanism. Q1 keeps `primaryFragmentPath`
  untouched (the wheel's one-path rule is preserved, not extended); Q2 makes
  existing topics opt-in with doc-health nudging rather than blocking; Q4 rules
  `edit-document` the verb for AI section-patching (Amendment 1, 2026-08-15 —
  ratified text named `edit-apply`, the gate console's main-resident redline
  verb, which requires a change id and cannot reach a session branch), the
  hinge that upgrades Phase A's freeform chat rewrites into marker-scoped
  patches once a successor change builds it (recorded on the
  `doxbench-editing-model` staged topic; neither Phase A nor Phase B shipped
  it). Both deltas are ADDED, not MODIFIED as the staging INDEX predicted —
  the existing requirements govern placement and buffer mechanics, neither
  fragment shape. Sections 1-4 are realized: the template contract in
  `docs/document-lifecycle.md`, doc-health's WARNING-tier `staged-topic-template`
  family, and the outline tab's section index plus gated add-section
  affordance, all with test coverage. Task 4.2's driven round-trip test
  surfaced a live demote defect that spawned and closed
  `align-demote-to-round-trip-rule` (ratified, realized, archived 2026-08-19),
  whose own two follow-ups — `refine-demote-round-trip-mechanics` and
  `align-status-reader-to-real-lines` — are now realized and merged (PR #221,
  #222). Bookkeeping 6.1-6.3 discharged (this row, the exit-marked staging
  fragments, and the `doxbench-editing-model` Q4 handoff). Outstanding: task
  5.4's live browser proof and gates 5.1-5.3. `target_release: implemented`.

- [add-doxbench-editing-phase-a](openspec/changes/add-doxbench-editing-phase-a/proposal.md)
  — authored 2026-08-15, Phase A of the `doxbench-editing-model` staged topic
  (sequenced first of Brett's four 2026-08-15 topics; its four Phase-A open
  questions were dispositioned accepted-as-recommended the same day). Brett's
  model is one sentence — left selects, center chat works, right shows the
  result — and Phase A is the half of it that fits the EXISTING two-buffer
  machinery with no invariant break: the authoring canvas presents the ACTIVE
  buffer, chosen by the context region rather than by a second tablist of its
  own; an Editor/Preview VIEW-TAB pair replaces the side-by-side
  textarea+preview split, with Preview the default and a flush on every switch
  into it; one Save and one Cancel replace the duplicated per-buffer toolbar
  pair (Save keeps its ratified branch-session semantics unchanged — reading
  the code showed `save()` was ALREADY whole-canvas and merely drawn twice —
  while Cancel discards the ACTIVE buffer to its `base_content`); the chat
  binds to the active buffer immediately with no confirm step and STATES that
  binding on the rail; and the per-buffer staleness guard is
  asserted to survive the consolidation. Phase B — numbered multi-document
  tabs, the docs-wheel edit verb, the dirty-tile marker, and the N-buffer
  generalization of `BUFFER_KINDS`/`require_outline_and_document`/`SAVE_BUFFER_ORDER`
  — is explicitly out of scope. No contract release. **Realized 2026-08-15**
  on `change/realize-doxbench-editing-phase-a`: `doxbench-editor.js` carries
  the Editor/Preview view tablist and the panel's one Save / one Cancel,
  `staging-workbench.js` drives the active buffer from the context region's
  selection, `doxbench-chat.js` states the bound buffer above the transcript,
  and `viewer.js`'s external-editor escape hatch is relabelled. Naming the
  bound buffer in the durable TURN RECORD is deferred to Phase B (F2 carve-out,
  Brett 2026-08-15: it needs a chat-turn contract release this change forbids,
  so `doxbench_turns.py` is untouched and the obligation is recorded on the
  staged topic). The archive gate still needs the merged-commit evidence
  (tasks 9.1).
- `add-worker-credential-by-reference` — ARCHIVED 2026-08-14
  (`openspec/changes/archive/2026-08-14-add-worker-credential-by-reference/`):
  credential-by-reference is LIVE on all three CPC claude lanes — vault
  source + rotation proven (§11.4 smokes), and the host is fully
  credential-free (final smoke run 31833019258). Vault deletion is the
  single kill switch; rotation is one vault write.
- [add-dispatch-credential-contract](openspec/changes/add-dispatch-credential-contract/proposal.md)
  — authored 2026-08-13: two neutral `credential-contracts` requirements for the
  openXdox intent-plane dispatch credential — dispatch-only least privilege with
  serving-tier separation (the trigger credential must be a distinct binding from
  the content-write App; the credential-free serving pod must never hold
  contents-write-capable key material), and reference-delivered credential with
  operator-as-binding (generalizing the two-case worker-credential principle:
  vault-referenced, ephemeral, operator per-install, neutral home). Ratifies
  `docs/openxdox-naming.md`; realizes the dispatch binding as an org-owned GitHub
  App + token-minter, retiring the personal PAT `dox-intent-inbox-qa-20260810`.

- [add-worker-enrollment-broker](openspec/changes/add-worker-enrollment-broker/proposal.md)
  — authored 2026-07-26, exit 1 of the `worker-enrollment-broker` staged
  topic: the neutral contract for how a machine becomes a governed worker and
  stays one, ratified BEFORE its three realizations are built. The Worker Host
  App cannot register a host today because the only way to hand it a runner
  registration token is to put administration-tier minting authority on the
  host, which the App identity tiers forbid — the decision parked at PRs
  #36/#37. Brett resolved it on 2026-07-26 by widening the question to two
  estates (the Intune fleet, and staff workstations volunteering as
  long-lived temp workers) served by ONE enrollment point with two
  authentication modes: fleet hosts by per-host identity in an Opsx key vault
  (broker ACCESS, never minting), volunteers as the ENGINEER by device code
  with no standing secret ever written to the machine. Minting authority — for
  registration AND remove tokens — lives only in the broker, under the
  ratified administration-tier custody shapes. The governing inversion is
  ruling 4: enrollment grants a renewable LEASE (id, TTL, trust tier, runner
  group) rather than a permanent registration, so staleness, revocation,
  trust, and audit all become properties of a renewal decision the platform
  re-takes — the only kind of control that works on hardware nobody manages.
  Every renewal response carries the current minimum app version, and a
  below-floor or revoked worker FAILS CLOSED (runner services stop, heartbeat
  reports `update_required`) until the engineer updates; revocation is simply
  refusing the next renewal, needing no reach into the machine. Package policy
  splits by estate (fleet hard-pins version + sha256 with self-update off and
  bumps ride manifest rollouts; temp workers self-update with the observed
  version informational), volunteered hardware lands in a dedicated runner
  group with a trust tier lanes can decline, and every enrollment, renewal,
  refusal, and revocation is audited by a record shape in which no token value
  can appear. Ships seven schemas — the seventh, `worker_removal_grant`, added by
  the 2026-07-26 amendment that is task 2.5's contract half: the remove-token
  issuance response, on the enrollment grant's transient-token discipline, with no
  registration token and no runner package by shape, so drift repair can never
  re-enrol a host — plus packaged positive/negative examples and a
  canonical validator; the broker SERVICE (home unresolved — design D1, the
  first decision), the Omnigent-Install registration/renewal integration, and
  the OpsxFactory custody/policy/runner-group work are named successor
  changes.



- [add-hermes-customer-subject-runtime-contract](openspec/changes/add-hermes-customer-subject-runtime-contract/proposal.md)
  — ratified 2026-07-12: domain-neutral Hermes runtime-topology and
  governed-record-integrity contracts separating the Customer/Client/Domain
  role templates from their runtime layer instances, with repeatable
  pseudonymous Customer subject instances, fail-closed default-deny
  isolation, explicit expiring directional bindings, parallel v2 job
  envelope/run/event and Postgres operational contracts, an idempotent
  v1-to-v2 migration with reconciliation and quarantine, and a versioned
  additive release bundle that Hermes Install must pin before multi-subject
  implementation proceeds (code surface: openxFactory; at the
  acceptance-gate stage — its tasks accept Speckit realization evidence;
  Hermes Install Gate G0/T009 stays closed until the published evidence
  independently reproduces)
- [add-ideation-intent-plane](openspec/changes/add-ideation-intent-plane/proposal.md)
  — staged-origin proposal (ideation-action-plane topic, organized 2026-07-23
  from the dashboard-action-center + cloud-workstation-topology brainstorms;
  ratified 2026-07-23) for the intent plane that makes the dashboard the
  process action center WITHOUT weakening D16: a click emits a signed
  `gate-intent` (actor, verb, target, snapshot_rev_seen); a dispatch-only
  inbox wakes the apply lane; the gate-console engine revalidates and commits
  intent + gate-action record + artifacts atomically via rolling PR
  (second-touch DECIDED: custody-not-decision, batched auto-merge). Two-plane
  rendering (snapshot + intent-feed overlay + refusal panel), identity ladder
  (per-user htpasswd -> Keycloak, contract-invisible), dispose tray as the
  first verb (local loopback-executing routes first, hosted intents second),
  Flutter verdict terminal as the same client class. Also carries the
  document-lifecycle GATES-HAPPEN-ON-MAIN delta (a transition is not real
  until merged). (code surface: codexFactory, openxFactory, omnigent-install,
  xFactory; release allocated at realization)

- [add-model-provider-broker](openspec/changes/add-model-provider-broker/proposal.md)
  — DRAFT, authored 2026-08-08, awaiting ratification (task 0). doxBench has
  a model seam and no model: there is no provider adapter in this repository
  and none is implied, so every model-backed affordance refuses. Brett's
  ruling names openProfiler — unbuilt — as the answer, which makes it a
  credential BROKER, a shape `credential-contracts` already owns. The
  dashboard holds a BINDING (id, label, credential reference, auth kind,
  broker invocation) whose shape has no secret field at all; setting a key is
  a hand-off to the broker's stdin that retains nothing; the invocation is
  declared rather than hardcoded, so openProfiler's real CLI changes a
  binding and no code. RULED 2026-08-08: the broker MINTS a short-lived
  scoped token and doxBench calls the provider directly, because brokered
  dispatch "would be too slow" — which means the "no provider is ever
  contacted from this repository" boundary narrows to ONE named module
  rather than holding, with its structural check rewritten rather than
  deleted, and a minted token that lives in process memory and never
  reaches the browser. (code surface: openxFactory; target release: none;
  depends on openProfiler)

- [add-composed-view-authoring](openspec/changes/add-composed-view-authoring/proposal.md)
  — ratified 2026-08-08 ("yes, we need to draft from a project view").
  `Composed views are read-only with a repository jump` states its reason as
  "a gate verb binds to one served checkout, and a composed view has none" —
  true of a TILE-BOUND verb, false of creating a NEW document, which binds to
  no tile and lands in the serve's own checkout. The blanket rule made the one
  view where cross-repository convergence is visible the one view unable to
  act on it. MODIFIED to distinguish the two, plus: the serve now DECLARES the
  repository it writes to on `/capabilities`, from the same authority a write
  is refused against, because the browser was inferring it and under a
  composed view inferred the PROJECT id. (code surface: openxFactory; target
  release: none)

- [add-lens-document-selection](openspec/changes/add-lens-document-selection/proposal.md)
  — ratified 2026-08-08 from three annotations on the keyword lens. A
  document has three views (the radar's dot, the matrix's row, the signature
  grid's row) and they now publish one key, so pointing at any lights the
  others. The signature grid states its finding — "32 documents share 3
  signatures (largest 17)" — and collapses, because a finding that fits in a
  sentence does not warrant 220px of the best space on the screen. A matrix
  SELECTION drafts a staging-queue fragment: evidence computed (documents,
  repositories, the terms all of them share), argument left to the human,
  nothing written — the exit the keyword radar lacked, distinct from the
  repository lens's DTN register seed. Carries two dark-theme defect fixes
  and their guards: a button reset that never stated its colour, and six
  uses of custom properties the stylesheet never defines whose silent
  fallbacks painted a white popover behind light text. (code surface:
  openxFactory; target release: none)

The avatar-client kernel (`contract-v1.7`), reference runtime, and avatar-first UI
standard (`contract-v1.8`) are realized. The contract kernel, the revocation
clarification, the reference runtime, and the avatar-first UI standard all archived
2026-07-13 (below), and F0 feasibility — the last active avatar change — archived
2026-08-09 (below), which closed issue #30. The F0 hold ("archives only inside a
contract re-cut that repoints `f0_change_path`", Brett 2026-08-04) was SUPERSEDED
by Brett's 2026-08-09 ruling accepting the issue's option C: the F0 gate is now
archive-aware and bundle-aware — it follows the UNCHANGED `f0_change_path` pin
into the dated archive and reads the pinned schemas from the packaged
`supporting-docs.tar.gz`, fail-closed on any ambiguity, with the schema digests
and `source_commit` pins still verifying the bytes wherever they sit — so no
contract re-cut was needed and `contract-v1.7` was never re-tagged. The avatar client lab itself realized and
**archived 2026-08-04** (below), its 9.1 platform gate discharged by Brett's
2026-08-04 disposition (Linux-bench green + portable suite + WCAG web
exception register accepted as v1; Windows/web deferred), and its successors are
staged too: `qualify-avatar-live-voice` (internal-live provider qualification;
blocked on open questions + a released client) and `avatar-pilot-hardening` (real
Hermes/domains/audits + pilot; structurally last) — see the
[Staging Index](ideation/staging/INDEX.md).

Archived changes:

- [refine-demote-round-trip-mechanics](openspec/changes/archive/2026-08-21-refine-demote-round-trip-mechanics/proposal.md)
  The MECHANICS around the round-trip rule `align-demote-to-round-trip-rule` fixed,
  three of them found by DRIVING both gates on the next lap and the fourth by
  Brett's Decision 3 ruling. (1) The origin topic was unresolvable for EVERY active
  change: `generator.py` built `origin_staging_id` only from possibles pick edges,
  which the forward transition destroys along with the staging folder they point at
  — measured, 12 of 12 active changes reported `None` and the corpus held one pick
  edge carrying no `change_id`, so the mapping was EMPTY. The answer was already on
  disk and unread, since the transition WRITES an origin block into `.openspec.yaml`
  that `generator.py` already parsed for `_ratifier_of` alone. Promoted as a
  DECLARED PRECEDENCE ORDER — explicit topic, then the origin block where it
  declares `kind: staged`, then the pick edge — resolving for the changes that came
  from staging and refusing by name for the `ad_hoc` ones that have no topic to
  return to. (2) The demote's own artifacts blocked the topic's next forward
  transition, and `openspec/INDEX.md` was only the first offender in sorted order:
  measured, 93 of 94 `tasks.md`, 154 of 158 spec deltas, 65 of 68 `design.md` and
  49 of 94 `proposal.md` carried no `Status:` header, so nearly every returned
  change artifact made the cycle one-way. Brett's returned-artifact ruling widened
  the fix to all of them, and then to the OUTLINE's refresh-in-place arm, whose
  source is the human's own working document and so never had to pass the forward
  gate to acquire a header. (3) `Proposed by:` accumulated one line per lap, and the
  fix landed on the FORWARD transition that writes it rather than the demote's
  refresh — deduping there would have widened the byte bound the promoted
  requirement pins as "leaving every other byte of that file unchanged", trading a
  data-loss guarantee for tidiness. (4) Ruling 3: the state-at-demote slot carries
  the change's task progress beside its status, which needed a MODIFIED delta
  because the promoted text named a closed list of five values. The realization also
  brought both gates onto ONE status grammar — the two readers disagreed on 11 of
  1133 documents in both directions, and now on 0 — and carved EXACTLY ONE addition
  out of the refresh's byte bound, in the delta that pins it. Promoted one MODIFIED
  and two ADDED requirements on `ideation-dashboard` and one ADDED on
  `document-lifecycle`. Realized 2026-08-20 as PR #221 (`1a7c2a1`, `17bba49`,
  `8c123bf`, `ca9fcaf`, `6c3d87c`) and archived 2026-08-21: `openspec validate --all
  --strict` 64/64 exit 0, `tests/ideation-dashboard` + `tests/proposal-support` 3729
  passed / 14 skipped / exit 0, `tests/doc-health` clean, and the realization proof
  a full LAP on a scratch tree — forward, demote, forward again — with the origin
  resolved from the origin block and no operator workaround. Its §8 items stay open
  BY RULING, not as gaps: the shallowest-markdown arm of the primary-fragment
  selection rule is deferred until a real topic reaches it (0 of 31 do), and the
  read-side half went to `align-status-reader-to-real-lines` below.
- [align-status-reader-to-real-lines](openspec/changes/archive/2026-08-21-align-status-reader-to-real-lines/proposal.md)
  The READ side of the pseudo-line blindness `align-demote-to-round-trip-rule`
  half-closed, and the one place a false finding cost more than a crash.
  `corpus.parse_status` and `parse_kind` scanned `text.splitlines()[:15]`, which
  also breaks on `\x0b`, `\x0c`, `\x1c`-`\x1e`, `\x85`, U+2028 and U+2029 — so a
  header carrying enough of them pushed a real `Status:` past the window and
  doc-health reported "missing status header" about a document that plainly had one,
  while the demote had just written that header correctly. A false finding accuses a
  correct document and leaves the operator no recourse but to disbelieve the
  checker. Promoted one ADDED requirement on `doc-health`: the deterministic pass
  reads a lifecycle header by REAL lines, that rule holds for EVERY reader of the
  header, and the rule is shared with the writers rather than reimplemented per
  reader — with cross-language divergence held by an explicit agreement test rather
  than by convention. The shared primitive is a new `scripts/doc_health/lines.py`,
  placed in `doc_health` on the MEASURED dependency direction (module-level imports
  run `ideation_dashboard` → `doc_health` at five call sites; the reverse is lazy
  and marked `# lazy: house guard`), so the checker layer does not end up downstream
  of the dashboard runtime for a text helper. Scope was RULED WIDE by Brett after an
  adversarial review of the first narrow realization surfaced a contradiction
  between the delta's every-reader clause and a narrower `code_surface:` — the delta
  governs, and all ten readers plus a standalone twin converted in this change on a
  measured zero baseline cost. Realized 2026-08-20 as PR #222 (`e6e3ae5`, `1644d86`,
  `175e972`, `42cc321`, `50bfee2`, `c379a09`) and archived 2026-08-21: `openspec
  validate --all --strict` 64/64 exit 0, `tests/doc-health` clean,
  `tests/ideation-dashboard` + `tests/proposal-support` 3729 passed / 14 skipped /
  exit 0, and task 5.3's own criterion — a doc-health report IDENTICAL to its
  baseline, since a moved finding would mean the zero-exotic-separator measurement
  had gone stale — discharged at all three re-run points and confirmed
  byte-identical across every branch tip. Measured baseline: 0 of 1227 governed
  files carry an exotic separator anywhere, so the fix moves ZERO findings today;
  its value is closing the divergence before something in the corpus makes it
  visible. Four readers stay UNCONVERTED and recorded rather than silently skipped
  (`families._template_gaps`, `ideation_routing._scan_lines`,
  `families._staged_exit_changes`, and `proposal-support.py`'s three rules): none
  reads the six lifecycle header fields, so each sits honestly outside the
  every-*header*-reader clause rather than inside it by omission. Its §7.5 follow-up
  — one stale docstring line in `proposal-support.py` that could only be reworded
  once BOTH sibling branches had merged — is discharged on this archive.
- [align-demote-to-round-trip-rule](openspec/changes/archive/2026-08-19-align-demote-to-round-trip-rule/proposal.md)
  A DEFECT FIX: the demote verb performed precisely the reset the ratified
  round-trip rule is titled against. `classify_change_file` routes anything under
  `supporting-docs/` back to the topic root by bare basename, and
  `proposal-support.py transition` records the topic's own primary fragment there
  — so the demote's destination WAS the primary fragment, and it came back
  carrying the aspirational pre-proposal snapshot with the provenance slots gone
  and `Status: draft` on a file the selector still calls the staged topic's
  outline. Found by DRIVING the verb rather than reading it: a grep for the slot's
  own field names finds no writer anywhere, which is exactly what made an earlier
  review conclude the rule was merely unimplemented. Not a special case — 2 of 2
  staged-origin manifests had the shape. Promoted one requirement on
  `ideation-dashboard` carrying four parts: status preservation, provenance-slot
  fill from values the executor already holds, `xspec:` proposal-element refresh
  from the returned `proposal.md`, and Brett's no-silent-overwrite ruling — the
  snapshot is a fallback SOURCE, never the authority, so a destination that exists
  and differs is refreshed IN PLACE with the snapshot preserved beside it rather
  than written over live human work. Realized 2026-08-19 as PR #215 (`e2c07ef`,
  `d28d36d`, `1c8b58a`, `79ed72e`) and archived 2026-08-19: 3240 tests passing,
  `openspec validate --all --strict` 62/62, doc-health baseline-identical, and a
  driven demote whose fragment came back right. It unblocked
  `add-staged-topic-outline-template` task 4.2, discharged in the parent by driving
  both gates. Three open items the realization surfaced — `corpus.parse_status`'s
  matching read-side blindness, `plan_demotion` resolving the origin topic only
  from a pick edge the forward transition erases, and a demote's own
  `openspec/INDEX.md` blocking the next whole-folder transition — are recorded in
  its `tasks.md` §7.2 rather than filed silently. **Both of its open rulings are
  now RULED** (Brett, 2026-08-19, in-session multiple choice): `Status at demote`
  IS enriched with the change's task progress, riding
  `refine-demote-round-trip-mechanics`, which also carries the three surfaced
  defects; and the shallowest-markdown arm of the primary-fragment selection rule
  stays OUT of path-only scope by ruling — deferred until a real topic hits it,
  not merely unaddressed. The read-side half goes to
  `align-status-reader-to-real-lines`.
- [add-client-identity-roster](openspec/changes/archive/2026-08-15-add-client-identity-roster/proposal.md)
  Promoted the neutral `client-identity-roster` capability (13 requirements)
  from the Business Central admission investigation: the identity layer
  beneath `credential-contracts` and `consent-instrument`. Which identities
  stand inside a paying client's provider tenant, keyed on (domain, admission
  surface, authority class, blast-radius unit, duty); admission is a VERIFIED
  list and consent is never recorded as access; achieved authority is derived
  from granted permissions and its excess over intent declared; structural
  scoping is preferred and its absence must be declared; provider-forced
  breadth is declared, never silently absorbed; destructive authority holds no
  provider identity by default; and drift REPORTS rather than remediates,
  withholding our own credential and refusing grant issuance. MODIFIED FOUR
  capabilities: consent-instrument (the cascade reaches governed identities,
  and `withdrawn` becomes the sixth lifecycle member as a DISTINCT terminal
  state that MUST NOT be declared an alias of `terminated`), doc-health (the
  sixteenth deterministic check family, client identity roster composition,
  scoped to the CROSS-DOMAIN concerns only), domain-conformance-checks (the
  neutral utility pack grows to FOUR checks — pack membership is what makes
  `scripts/validate-client-identity-roster.py` BLOCKING, Decision A
  2026-08-14) and credential-contracts (the optional, CLOSED
  `issuance_preconditions` vocabulary whose first member is the roster-drift
  precondition, Decision B 2026-08-14). Decision C (Brett, 2026-08-15)
  relocated the uncitable multi-surface-reader packaged example to a synthetic
  representability fixture after its provider precondition was falsified.
  Realized 2026-08-15 by Speckit feature `007-client-identity-roster` (PR
  #190) at `contract-v1.33` and archived 2026-08-15. Intra-repo entry
  conformance fails the domain gate; cross-domain composition is advisory.
  This release enforces NO roster completeness rule — neither a missing
  fragment nor a missing entry is a finding — and scoped completeness, plus
  the live refuse-then-allow proof at a domain mint surface, are named
  successors.

- [qualify-avatar-brokered-call-feasibility](openspec/changes/archive/2026-08-09-qualify-avatar-brokered-call-feasibility/proposal.md)
  — tenant-data-free F0 harness for sideband-before-answer ordering, retries,
  readiness, revocation, redacted evidence, and contract interface impacts;
  F0 does not qualify live use. Realized (F0 `PASS`) 2026-07-12; archived
  2026-08-09 under the archive-aware F0 gate (issue #30 option C — the
  `interface-lock.yaml` pin is unchanged and the gate resolves the packaged
  archive, digest-checked, fail-closed).

- [add-openxwallet](openspec/changes/archive/2026-08-08-add-openxwallet/proposal.md)
  Promoted the neutral `openxwallet` core (8 requirements) and
  `openxwallet-agent-profile` (3 requirements). A wallet is a key
  REFERENCE with a declared custody model and never key material;
  authority travels as ATTENUATED GRANTS that narrow monotonically;
  exercise requires proof of possession rather than presentation; custody
  CAPS what a signature evidences; audit is key-attributed; revocation
  propagates through derivation and is checked at exercise;
  distinct-holder constraints are expressible and opt-in; and wallets stay
  optional for every domain, preserving MedxFactory's two ratified
  constraints. Realized 2026-08-07 by Speckit feature
  `006-openxwallet-contracts` at `contract-v1.31` and archived 2026-08-08.
  The feature settled the two decisions ratification left it: the closed
  custody set is three members with `evidences` DERIVED from two declared
  booleans and enforced — so the collapse the ruling closes is
  structurally impossible rather than discouraged — and the composition
  component set covers a retrieval corpus BY REFERENCE (identity plus
  governing configuration) rather than by its contents. Patient and
  practitioner profiles remain named successors, each a NEW profile over
  the same core and each gated on a consumer of its own.
- [add-project-merged-projection](openspec/changes/archive/2026-08-07-add-project-merged-projection/proposal.md)
  Promoted the project merged view into `ideation-dashboard`
  (dashboard-project-scoping exit 2): one composed snapshot per register
  project via derived aggregates (per-repo namespaced ids, repository
  badges, multi-parent membership D8), same-topic cluster union on the
  wheel, read-only composed views with the single "open in <repo>"
  navigation verb, and degrade-never-refuse on missing members. Archived
  2026-08-07 on Brett's first real merged-view pass (correct repository
  attribution verified at the tile annotation); per-tile repository
  binding stays a named successor.
- [add-project-scoped-selection](openspec/changes/archive/2026-08-06-add-project-scoped-selection/proposal.md)
  Promoted project-scoped selection into `ideation-dashboard`
  (dashboard-project-scoping exit 1): the human-only `create-project`
  commission (register writes stay commissions-only per D2), project as a
  selection scope on the selector, and the gate-intent/gate-action-record
  `target.project_id` additive deltas — registered at contract-v1.30.
  Archived 2026-08-06 with its staged origin declared.
- [add-opendox-project-header](openspec/changes/archive/2026-08-06-add-opendox-project-header/proposal.md)
  Promoted the Opensoft openDox project-first header (topic D12–D15): the
  project selector leads the header, "New Project" rehomes the create
  commission, and the `edit-project` gate verb lands with the ruled guard
  order — contract deltas registered at contract-v1.30. Archived
  2026-08-06 with its staged origin declared.
- [add-proposal-origin-contract](openspec/changes/archive/2026-08-06-add-proposal-origin-contract/proposal.md)
  Promoted the proposal-origin contract: every OpenSpec change declares
  exactly one immutable origin (`staged` with a durable
  `<repo>:staging:<topic>` id, or `ad_hoc` as an explicit approved
  exception) in `.openspec.yaml`, repeated in the support manifest.
  `proposal-support.py` writes the staged origin automatically at
  transition, gains `declare-adhoc`, and fail-closes the per-change verify
  and archive gates; the nightly `proposal-origin` family (the fifteenth)
  reports drift across active and archived proposals with pre-contract
  legacy as WARNING visibility. 22 archived changes were backfilled from
  recorded evidence (2026-07-12 migration); the family's first run caught
  and fixed three real defects. Self-applied: the change's own staged
  origin gated its own archive. Archived 2026-08-06.
- [add-cross-factory-ideation-routing](openspec/changes/archive/2026-08-06-add-cross-factory-ideation-routing/proposal.md)
  Promoted the governed cross-factory routing plane: durable `XFI-` Idea IDs
  from the central allocation ledger, per-idea routing records with
  claim-level ownership, destination-owner acceptance, and owner-authorized
  dispositions; the non-mutating ideation organizer (deterministic-first
  nightly child with watchdog and immutable evidence); and the fourteenth
  deterministic doc-health family. Contracts registered at
  **contract-v1.30**, five domains re-pinned, and archived 2026-08-06 on
  the two-idea pilot (XFI-2026-001 openxWallet unknown-owner intake,
  XFI-2026-002 subject-document-estate domain-origin split) with a real
  organizer run, authorized dispositions, nightly run 31129751955 green,
  and zero fabricated history in any legacy brainstorm.
- [add-consent-instrument](openspec/changes/archive/2026-08-06-add-consent-instrument/proposal.md)
  Promoted the neutral `xfactory_consent_instrument` record kind — the
  authority-chain root credential grants cite, gates verify, and whose
  termination cascades through declared dependent references — with the
  domain-owned closed class registry and the purpose model for the neutral
  purpose-resolution check (D1–D9, zero open questions). Registered at
  **contract-v1.30** (DTN-016 `adopted`); both proven instances conform by
  declaration, never rewrite: LedgerxFactory 8b5c03a (engagement classes,
  active→executed alias, tenant-tree placement) and MedxFactory 3c7715a
  (four medical classes, consent-profile dependent ref, governed-store
  placement), each pinned to the release commit with validator sweeps and
  purpose probes green. Archived 2026-08-06.
- [add-lens-gate-verbs](openspec/changes/archive/2026-08-06-add-lens-gate-verbs/proposal.md)
  Promoted the two lens gate verbs into the dashboard's gate console:
  `lens-save-recipe` and `lens-add-as-cluster` beside dispose/ratify/
  propose — same human-only enforcement and refusal/record mechanics,
  capability-gated execute affordance on the lens plan confirmation, CLI
  parity. Archived 2026-08-06 under Brett's 3.3 disposition: route tests
  + the Playwright smoke of the exact dogfood scenario + the real
  wheel-verbs 4.4 human pass on the same gate engine accepted as
  realization evidence, first real lens use standing as retroactive
  confirmation.
- [add-neutrality-drift-lane](openspec/changes/archive/2026-08-05-add-neutrality-drift-lane/proposal.md)
  The nightly doc-health lane that scouts the domain factories for content
  that belongs in openxFactory: four deterministic stage-1 signals plus a
  bounded model scout under prompt contract v1, drafting DTN-register
  seeds through the rolling health PR; dispositions are digest-keyed and
  movement always follows the promotion process. Archived 2026-08-05 on
  full verification: first live nightly (run 31001274147) carried the
  report section, and the dry-run evidence
  (archived change's `evidence/dry-run-2026-08-05.md`) proved no
  false-positive on the post-shed codexFactory engineering core, the
  synthetic-fixture catch-and-draft path, and unchanged-rejected
  suppression with digest-keyed re-filing.
- [add-wheel-action-verbs](openspec/changes/archive/2026-08-05-add-wheel-action-verbs/proposal.md)
  Four gate verbs for the wheel's expanded-tile action row (Brett's
  2026-07-25 rulings): `demote` promoted to an executing dashboard verb
  (plan + record on the click; the corpus move stays the separate human-run
  step) and three recorded commissions on propose's mechanic —
  `promote-to-staging`, `derive-possibles`, `research-brief` — with the
  additive gate-intent / gate-action-record enum + `cluster_id` extension
  (shipped `contract-v1.29`) and the shared (verb, target)
  undelivered-commission index. Engine/routes/CLI/wheel realization rode the
  `adopt-neutral-tooling-home` Tranche B adoption; the four ADDED
  requirements live in the `ideation-dashboard` spec. Archived 2026-08-05 on
  the 4.x evidence: suites green (2572 passed), the live browser check, and
  Brett's first real commissions — one full
  possible→staged→proposed→demoted traversal, the demote executed as two
  deliberate steps (PRs #66/#67/#71); the fulfilment lanes remain named
  successor work.
- [adopt-neutral-tooling-home](openspec/changes/archive/2026-08-05-adopt-neutral-tooling-home/proposal.md)
  The contract owner adopted its implementations: the doc-health checker
  suite, the ideation dashboard runtime, the routing/organizer lanes, and
  the NotebookLM lifecycle sync moved from codexFactory to openxFactory
  (tranches A-D; codexFactory shed via PR #72). Archived 2026-08-05 on the
  5.2 nightly evidence: xFactory run 31001274147 green with the dashboard
  lane publishing 14/14 snapshots + index from the new homes, after fixing
  the three adoption regressions in the way (openxFactory Actions access
  `none` -> `organization`; App grants for the HealthLinc/MedxEHR/openAvatar
  submodules; the finalize job's missing `rfc3339-validator`).
- [implement-avatar-client-lab](openspec/changes/archive/2026-08-04-implement-avatar-client-lab/proposal.md)
  Realized the offline, deterministic Flutter avatar client UI lab
  (codexFactory `apps/avatar-client-lab/`, openxFactory fixtures + acceptance
  map): content-addressed contract-v1.7/v1.8 consumption, fixture-replay
  determinism, the six-state avatar seam, five-region adaptive shell,
  keyboard-only F1-F4. Archived 2026-08-04 under Brett's 9.1 disposition —
  Linux-bench green + the portable suite + the WCAG web exception register
  accepted as the v1 realization; Windows/web platform evidence deferred to
  the first pilot-era change that stands up the repo-root CI caller.
- [add-ideation-cross-reference-readiness](openspec/changes/archive/2026-08-04-add-ideation-cross-reference-readiness/proposal.md)
  Promoted the unified cross-stage topic cluster + readiness surface:
  `ideation/cross-reference.yaml` (generated `.md` projection), the
  four-schema index contract with extension-fit citations, the three-tier
  Hermes readiness panel, and the min>=8 recommendation gate. Realized
  2026-07-14 (codexFactory `003-ideation-readiness` merged `1fc0bd7`,
  aggregation child workflow `669d60a`, omnigent-install readiness-scorer
  profile `f31a019`); the scoring lane reports SKIPPED until a host
  advertises the profile — the recorded valid landed state (CPC deploy +
  submodule commit-back remain on the ops ledger). Archived 2026-08-04.
- [add-possibles-derivation-lane](openspec/changes/archive/2026-08-04-add-possibles-derivation-lane/proposal.md)
  Promoted the AI-assisted derive-possibles worker lane: bounded read-only
  Omnigent worker deriving `pending_review` possibles from the landed
  cross-reference index, the additive possibles-register kernel delta
  (contract-v1.14), nightly dispatch with watchdog + dormant rolling-PR
  commit-back, THE WHEEL's non-`indexed` `inferred` rendering. Realized
  2026-07-22 (codexFactory PRs #25/#27/#28, Omnigent-Install PR #22,
  xFactory child workflow); first live lane run 2026-07-23 (run
  30000105423, 3 possibles merged via openxFactory PR #38). Archived
  2026-08-04.
- [adopt-neutral-utility-pack](openspec/changes/archive/2026-08-04-adopt-neutral-utility-pack/proposal.md)
  The neutral utility pack came home (DTN-018/019/021): the three
  domain-repo conformance checks and the proposal-support mover moved from
  codexFactory to openxFactory with their test suites, and the
  subject/tenant Hermes layer-template schema joined
  `contracts/hermes-domain-overlay/` with a neutralized `$id`. Archived
  2026-08-04 after the codexFactory shed landed (PR #73, merge 25e46fd1bf)
  and DTN-018/019/021 moved to `adopted`.
- [add-workbench-branch-sessions](openspec/changes/archive/2026-08-01-add-workbench-branch-sessions/proposal.md)
  Promoted branch-per-tile working sessions into `ideation-dashboard`:
  commit-per-gate-action on a `draft/` branch, session-local snapshots the
  panels follow, PR-as-save carrying the D18 merge-commit-never-squash
  series, and the human-only session verbs. Archived 2026-08-01 after the
  D10 live pass ran a real session end to end (9.2 PASS WITH FINDINGS
  F8/F10/F12).
- [add-dashboard-repo-selector](openspec/changes/archive/2026-08-01-add-dashboard-repo-selector/proposal.md)
  Promoted the (repository, ref) snapshot registry, the repository
  selector, serving-side runtime fetch with the baked-snapshot fallback,
  both refresh bindings, and the dispatchable publication lane. Archived
  2026-08-01 with the hosted acceptance AND the deliberate human
  observation complete (6.2 PASS; image digest byte-identical).
- [add-workbench-bullseye-and-create](openspec/changes/archive/2026-08-01-add-workbench-bullseye-and-create/proposal.md)
  Promoted the bullseye scope reading (rings/sectors over the checked
  keyword set) and the create gesture with its per-tab create affordances
  (header-compliant, create-only gate verb). Archived 2026-08-01 after the
  D10 live creation pass (7.2 PASS WITH FINDINGS F5).
- [add-staging-workbench](openspec/changes/archive/2026-08-01-add-staging-workbench/proposal.md)
  Promoted the staging workbench: scoped docs/lens context, per-document
  completeness bars over the five-signal scorer, and the
  `READY_MIN_SCORE` 0.60 staged-to-proposal gate with typed, explainable
  blockers. Archived 2026-08-01 after the D10 calibration pass (6.5 PASS
  WITH FINDINGS F2/F3 — the scorer-depth V2 register).
- [add-propose-verb](openspec/changes/archive/2026-08-01-add-propose-verb/proposal.md)
  Promoted the `propose` verb: the human-gated staged-topic commission
  emitting a workflow-job descriptor plus gate-action record behind the
  live readiness guard. Archived 2026-08-01 after the first REAL
  commission (4.3 PASS — `add-consent-instrument` dispatched from the
  D10 pass).

- [add-deployment-handoff-boundary](openspec/changes/archive/2026-07-30-add-deployment-handoff-boundary/proposal.md)
  — **ratified 2026-07-29, realized and archived 2026-07-30** (doc-only;
  supporting bundle packaged per the proposal-support archive gate).
  Promoted the `deployment-handoff-boundary` capability (7 requirements):
  the managed-subject test is the sole deployment router (tier calibrates
  governance depth, never the executor; binds workers, CI, and human
  engineers alike); the crossing is the ratified
  `client_infrastructure_request` requirements-profile; credential
  non-possession is the primary enforcement (grants issue only against
  accepted requests targeting registered subjects; break-glass is a
  retroactive request with escrow-owned custody); structural channels
  (merge IS the deployment); correlation stamping makes out-of-band
  change a first-class audit finding; benches ride standing requests;
  adoption is phased-never-gapped. MODIFIED `release-realization`:
  managed-subject deployment evidence references the handoff correlation
  identifier. Successor packets for OpsxFactory and codexFactory (with
  the four deferred decisions and the topic-exit conditions):
  [docs/deployment-handoff-realization-handoff.md](docs/deployment-handoff-realization-handoff.md);
  escrow coordination and the DTN-017 seam linkage recorded in their
  owning registers.
- [publish-semantic-kernel](openspec/changes/archive/2026-07-30-publish-semantic-kernel/proposal.md)
  — **the capstone: ratified, realized, cut at contract-v1.25, and
  archived 2026-07-30**. The xFactory semantic kernel's first governed
  publication: all 34 terms published by explicit per-term steward act
  (25 concepts + 9 relations, every one adoption-evidenced), released
  0.1.0 → 1.0.0 by the accountable `openxfactory-maintainers` council
  through `ontology-release.py`, meaning untouched. The bootstrap window
  closes in ratified text (the active kernel line never regresses to
  pending adoption), the kernel's stewardship policy is an EXPLICIT
  scoping decision (openxFactory change governance; reopening trigger
  recorded), and the capstone review's P-wave made retention TRUTHFUL IN
  BOTH DIRECTIONS (active snapshots state published; supersession flips
  exactly one governed line; orphans fail), added version-AND-digest
  kernel-import checking, and turned the recurring stale-count slip into
  a validator lint that caught its own author on introduction. Reviewer
  APPROVED at ce95d27 with zero new findings — every finding from the
  original release review and all subsequent waves is closed. Consumers
  MedxFactory 516bac9 + codexFactory 6f037d5 declare and pin kernel
  1.0.0. Corpus 57 negatives / 10 positives.
- [add-ontology-stewardship-hardening](openspec/changes/archive/2026-07-30-add-ontology-stewardship-hardening/proposal.md)
  — **authored, ratified, realized, cut at contract-v1.24, and archived
  2026-07-30**, closing the ENTIRE carried-forward set from the
  domain-ontology release review. F21: the release tool's manifest
  rewrite carries every declared field, evidence paths are contained
  inside the package, and retained snapshots are born
  `lifecycle_state: superseded` (the F3 byte seal independently
  re-verified intact across all 13 snapshots). F24: readiness blocks on
  the starter marker's STRUCTURAL placeholder record — a rename can never
  launder a scaffold into readiness. F25: the marker is inventoried,
  digest-covered content. F26: quality signals declare min OR max (rate
  ceilings expressible directly) and a declared source-review cadence
  requires external review deadlines — a rule that caught a real defect
  in the codex pilot's own sources on first run. F27: the eight semantic
  gateway conformance fixtures are EXECUTED (all six probes proven
  load-bearing; delegates resolution-verified). Plus starter v14's
  `--ontology-only` adoption mode: mature repositories adopt the ontology
  without the whole-repo scaffold spray. Corpus 55 negatives / 10
  positives; contract-v1.24 remote-verified and DELIVERING the v1.23
  erratum correction; reviewer APPROVED at 55a6202. Consumers MedxFactory
  f4ca313 + codexFactory 11777a9 (inventoried markers; their v13 markers
  gain the placeholders block when a publication-driving change
  regenerates them).
- [add-omnigent-semantic-wiring](openspec/changes/archive/2026-07-30-add-omnigent-semantic-wiring/proposal.md)
  — **authored, ratified, realized, cut at contract-v1.23, and archived
  2026-07-30**, closing the follow-up named at add-domain-ontology-layer
  6.7 / design decision 13: the Omnigent seam is wired end to end. The
  domain overlay declares each worker's semantic-context profile by
  identity (repo-mode resolution against inventoried profiles,
  archetype-or-class scope agreement); the install manifest pins the
  compiled per-worker artifacts with exact kernel/package digests,
  both-direction completeness fail-closed, and — after the review's N5 —
  the content digest RECOMPUTED from artifact bytes at both gates (the
  install pin catches tampering even when an artifact is self-consistent;
  the ontology validator catches drift wherever a context lands). Seam
  hardening landed F19 (transitive truncation itemization, tool +
  validator) and F20 (drifted package bytes refuse compilation); the
  review also surfaced N7 — a stale `contracts/manifest.yaml` digest
  carried v1.18→v1.23 with no checker — fixed with
  `scripts/validate-manifest-digests.py` (104/104) and a recorded v1.23
  erratum. Ontology corpus 51 negatives / 10 positives; wiring suite 16
  checks. First consumer MedxFactory (80a81af: two profiles, two
  declarations, overlay-manifest re-pinned); tag `contract-v1.23`
  remote-verified; reviewer APPROVED at 792afd2.
- [add-ontology-term-lifecycle-enforcement](openspec/changes/archive/2026-07-30-add-ontology-term-lifecycle-enforcement/proposal.md)
  — **authored, ratified, realized, and archived 2026-07-30**, landing F18
  (the first carried-forward finding from the ontology release review):
  term-level `lifecycle_state`/`effective_version` are enforced, never
  decorative. A published package carries no draft term — publication is a
  per-term steward act refused by both the validator
  (`ONT-TERM-LIFECYCLE`) and `ontology-release.py`; term lifecycle only
  moves forward across revisions (resurrection fails for every
  compatibility class); meaning-bearing changes bump `effective_version`
  (`ONT-TERM-VERSION`); retired terms refuse new compilation at the
  compile tool (requested OR closure-pulled), in worker profiles, and in
  current-pin contexts, while prior-pin contexts keep their original
  interpretation. Five new indexed negatives (corpus 49, ratchet 49);
  pilots publish their terms as recorded steward acts. Reviewer-verified
  by construction and APPROVED at 0033d7c. No schema bytes changed
  (target_release: none). ADDED requirement promoted into
  `domain-ontology-lifecycle`; `Bounded semantic context` updated in
  `xfactory-semantic-kernel`.
- [add-domain-ontology-layer](openspec/changes/archive/2026-07-30-add-domain-ontology-layer/proposal.md)
  — **ratified 2026-07-28, realized 2026-07-28/29, archived 2026-07-30 at
  contract-v1.22**: the semantic plane. Promoted `xfactory-semantic-kernel`
  and `domain-ontology-lifecycle` plus deltas to layer-vocabulary,
  hermes-domain-overlay, and memory-gateway. Realized: the eighteen-kind
  `contracts/domain-ontology/` family with the `xf/core` kernel (24 concepts,
  9 relations, per-term owning contracts + evidenced adoption; DRAFT pending
  the governed publication decision); canonical validator
  `validate-domain-ontology.py` (10 positives incl. the retained
  MedxFactory/codexFactory pilots, 44 indexed negatives, determinism,
  readiness, repo-scoped registry); starter v13 ontology generation with
  conflict-preserving candidate ingestion; stewardship tooling
  (accountable-steward releases with per-signal quality exceptions,
  consumer-impact evidence, byte-true self-retention; maintenance triggers
  with identifier fail-closed inputs); purpose-bounded semantic-context
  compilation + memory-gateway packet preflight (closed packet shapes,
  real pilot-stamped example digests). Guide:
  [docs/domain-ontology-guide.md](docs/domain-ontology-guide.md); pilots:
  [docs/domain-ontology-pilot-report.md](docs/domain-ontology-pilot-report.md).
  Released through a four-round independent adversarial review (16 blocking
  findings + N1–N4 all resolved, APPROVED at 5d39bb4); bundle tag
  `contract-v1.22` remote-verified. MedxFactory adopted (kernel
  digest-pinned); codexFactory/hermes-install/omnigent adoption recorded as
  explicit deferrals with the follow-up omnigent change named.
- [add-capability-steward](openspec/changes/archive/2026-07-30-add-capability-steward/proposal.md)
  — **authored, ratified, and realized 2026-07-29; archived 2026-07-30**,
  closing the `recurrence-crystallization` program: promoted
  `crystallized-capability-registry` (6 requirements),
  `crystallization-dispatch` (8), and `capability-health` (9) — the
  single-source registry with the proof-gated spine and
  pins-vs-live-authority (D10), the dispatch junction with deterministic
  fences and pure/idempotent admission (D11), and the
  proof/sentinel/drift/accounting surface with contractual renewal
  write-backs. Realized at `contract-v1.21`; with `v1.19` (pattern-ledger)
  and `v1.20` (crystallizer), all three crystallization waves went
  brainstorm → canon in three days, and the MVP packet-capture corpus runs
  the entire flywheel in fixtures — episode to verified savings. The dials
  register remains the topic's staged living remainder; cross-tenant is
  the deliberate brainstorm remainder for the pooling wave.
- [add-crystallizer-contracts](openspec/changes/archive/2026-07-29-add-crystallizer-contracts/proposal.md)
  — **authored, ratified, realized, and archived 2026-07-29** (same-day
  full cycle; exit 2 of the `recurrence-crystallization` staged topic):
  promoted `crystallization-decision` (7 requirements),
  `crystallization-build` (8), and `crystallization-consent` (4), and grew
  `omnigent-domain-overlay` by two — the crystallized-executor binding on
  the EXISTING five archetypes (constitutional matrix binds verbatim;
  authority conservation is a mechanical subset check) and per-category
  rung ceilings with the conservative L3 default. Realized at
  `contract-v1.20`; the MVP corpus now runs candidate → funded L3
  decision → mined spec (real Topics-wrap counterexample) → consent
  grants → accepted-build shape, end to end in fixtures. Successor exit
  stays staged: `add-capability-steward`.
- [add-pattern-ledger](openspec/changes/archive/2026-07-29-add-pattern-ledger/proposal.md)
  — **authored, ratified, realized, and archived 2026-07-29** (same-day
  full cycle; exit 1 of the `recurrence-crystallization` staged topic):
  promoted the `pattern-ledger` capability (8 requirements) — the five
  sensing record schemas (episode / outcome-label / recurrence-family /
  recurrence-forecast / crystallization-candidate), the canonical validator
  with nine named policy rules (self-testing 7 positives / 7 indexed
  negatives), and the MVP packet-capture fixture corpus hand-derived from
  the real 2026-07-28/29 runs. Realized at `contract-v1.19`, whose cut also
  discharged the standing `xfactory-derived-model-conformance`
  registration. The candidate autonomy boundary — nominate, never spend —
  is the wave's constitutional line; successor exits stay staged:
  `add-crystallizer-contracts`, `add-capability-steward`.
- [add-ideation-dashboard](openspec/changes/archive/2026-07-29-add-ideation-dashboard/proposal.md)
  — **re-ratified 2026-07-14 (D1–D17), realized, and archived 2026-07-29**:
  promoted the `ideation-dashboard` capability (15 requirements), created
  `ideation-cross-reference` (2), and grew doc-health and
  document-lifecycle by one each. The generated dashboard: realization
  funnel snapshot over a possibles register, cluster canvas, keyword lens
  with cluster-as-recipe persistence, project grouping roll-ups, drill-down
  explorer and read-only viewer, human gate console and next-step kickoff,
  per-actor authoring authority, and the nightly snapshot lane; web-based
  v1 on the internal xForge plane. Archive-gate evidence: codexFactory
  feature 002 merged (231 tests + 34 contract fixtures, adversarial review
  ACCEPT), doc-health-nightly green with fresh per-repository snapshots on
  the archive date, live at ideation-dashboard.xforge.us (never-public
  boundary answering 401 unauthenticated), the contract family registered
  (`ideation-possibles-register` kernel in `contracts/manifest.yaml`, the
  family in the contracts README doc index), and the supporting bundle
  manifest hash-refreshed at preflight to cover the two post-transition
  governance commits. Seven active changes stack MODIFIED deltas on the
  promoted spec (repo-selector, branch-sessions, bullseye-and-create,
  staging-workbench, and the lens/wheel/propose verbs) — all validating
  strict against it (49/49).
- [add-hermes-domain-content-manifest](openspec/changes/archive/2026-07-24-add-hermes-domain-content-manifest/proposal.md)
  — **ratified, realized, and archived 2026-07-24** (seeding increment 4b,
  contract half; released as `contract-v1.18`, annotated tag verified): the
  optional `hermes_domain_content_manifest` declaring a domain repo's
  seedable content set (convention-then-contract successor to increment
  4a's well-known-path list) and the `hermes_memory_binding` record schema
  formalizing increment 3's derived gateway-rails input; canonical
  validator extensions green over fixtures and the real codexFactory tree,
  with the live-derived opensoft bindings as the packaged example.
- [add-governed-derived-model](openspec/changes/archive/2026-07-23-add-governed-derived-model/proposal.md)
  — **ratified, realized, and archived 2026-07-23** (same-day promotion of
  the governed-derived-model staging topic; DTN-014): the
  `governed-derived-model` capability — conformance declaration
  (`xfactory_derived_model_conformance`) with `governed`/`calibrated`
  tiers, five line-verified invariants, six declared dials (incl.
  `person_modeling`), the vocabulary doc
  (`docs/governed-derived-model.md`), and
  `scripts/validate-derived-models.py` with positive/negative fixtures.
  Realization evidence: MedxFactory conforms at `governed`
  declaration-only (0987bca, unchanged ratified templates); AdxFactory
  is the first `calibrated`-tier conformer (eb98f84, via
  `add-adx-object-model`). Deferred to the contract-v1.16 cut: manifest
  entry + DTN-014 `adopted` flip.
- [add-client-infrastructure-liaison](openspec/changes/archive/2026-07-17-add-client-infrastructure-liaison/proposal.md)
  — exit of `ideation/staging/client-infrastructure-liaison`: the neutral
  Client Infrastructure Liaison coordination profile (promoted capabilities
  `client-infrastructure-liaison` + `client-infrastructure-request`) and the
  `client_infrastructure_request` contract family — two schemas, reference
  examples, and the strict validator — with three execution bindings
  (client-managed / managed-host / OpsxFactory-executed), readiness-gated
  completion, and the OpsxFactory handoff boundary; MODIFIES
  `roles-authority-model` so client-tenant infrastructure execution routes
  here (closing the github-administration-plane carve-out). PO gate signed
  off by Brett 2026-07-16; realized as **`contract-v1.13`** and archived
  2026-07-17 with the verified supporting-doc bundle. Successor per-domain
  adoption changes (OpsxFactory binding/readiness producer first, then
  Medx/Ledger/Ad/codex aliases) are proposed per the impact map's sequence
- [adopt-avatar-client-lab-candidates](openspec/changes/archive/2026-07-16-adopt-avatar-client-lab-candidates/proposal.md)
  — the owning change for the avatar-client-lab P-ledger escalations and
  fixture adoptions: landed the P1 neutral avatar-state derivation table and
  the P10 22-capability-scenario register (new `avatar-lab-evidence`
  capability), adopted the panel-confirmed P7/P8/P11/P12/P13 deterministic
  fixture families into `examples/avatar-first-ui/`, and cut `contract-v1.12`
  (also manifest-registering the successor evidence register so the
  SCO-001-S05 discharge takes effect). Realized via codexFactory PR #17
  (avatar-client-lab contract-pin resync, nine gates green on the resynced
  pin; Brett Tier-1 approval, merge `0fed12c`), archived 2026-07-16
- [add-github-app-identity-tiers](openspec/changes/archive/2026-07-14-add-github-app-identity-tiers/proposal.md)
  — exit of `ideation/staging/github-administration-plane`: extended
  `roles-authority-model`'s structural-parking requirement so any identity
  able to modify a GitHub enforcement gate is authority-separated from any
  identity doing ordinary content/workflow work on the same surface, adding
  the content-vs-administration App identity tiers and administration-tier
  credential-custody requirements (code surface: none — doc/spec only);
  ratified and archived on landing 2026-07-14. Sibling OpsxFactory change
  `add-github-administration-workflow` (realized, archived 2026-07-15)
  instantiates the tiering concretely; live rollout done
- [add-document-cataloging](openspec/changes/archive/2026-07-14-add-document-cataloging/proposal.md)
  — external governed-document catalog, controlled discovery taxonomy,
  immutable snapshots, thirteenth deterministic doc-health family, and the
  bounded document-cataloger lane; realized as `contract-v1.11` with the
  225/225 full-corpus mechanical baseline and nightly dispatch wiring,
  archived 2026-07-14
- [define-avatar-client-contract-kernel](openspec/changes/archive/2026-07-13-define-avatar-client-contract-kernel/proposal.md)
  — canonical eight-contract AVC kernel, registries, fixtures, validator, and
  repository-boundary rules; realized as `contract-v1.7`, archived 2026-07-13
- [clarify-avatar-revocation-client-enforced](openspec/changes/archive/2026-07-13-clarify-avatar-revocation-client-enforced/proposal.md)
  — ACR-005 disposition: revocation is client-enforced within the 5 s bound;
  archived 2026-07-13
- [implement-avatar-reference-runtime](openspec/changes/archive/2026-07-13-implement-avatar-reference-runtime/proposal.md)
  — non-deployable deterministic broker/control reference realized against
  `contract-v1.7`, with archive-safe content-addressed conformance (FR-034a);
  archived 2026-07-13
- [align-avatar-first-ui-standard](openspec/changes/archive/2026-07-13-align-avatar-first-ui-standard/proposal.md)
  — avatar-first UI standard, domain profile carrier, template, examples, and
  offline realization validator; realized as `contract-v1.8` (acceptance map
  relocated to `examples/avatar-first-ui/` so the validator survives archive);
  archived 2026-07-13
- [define-human-escalation-contract](openspec/changes/archive/2026-07-12-define-human-escalation-contract/proposal.md)
  — route/park/interrupt escalation ladder with a deliberately high interrupt
  bar (containment failure only, cited classes), parked-decision packets at
  existing gates, fail-closed silence, the Merge Master low-risk envelope,
  and structural parking in external enforcement; ratified 2026-07-12,
  archived on landing (`code_surface: none`); resolves the dangling `HR`
  consultation in the engineering escalation table
- [add-proposal-supporting-doc-lifecycle](openspec/changes/archive/2026-07-09-add-proposal-supporting-doc-lifecycle/proposal.md)
  — proposal-owned supporting documents, deterministic archive bundles, and
  proposal-stage NotebookLM returns (ratified and realized 2026-07-09)
- [add-release-realization-flow](openspec/changes/archive/2026-07-09-add-release-realization-flow/proposal.md)
- [add-lifecycle-notebook-hybrid-imports](openspec/changes/archive/2026-07-09-add-lifecycle-notebook-hybrid-imports/proposal.md)
- [neutralize-job-envelope](openspec/changes/archive/2026-07-09-neutralize-job-envelope/proposal.md)
- [split-roles-authority](openspec/changes/archive/2026-07-09-split-roles-authority/proposal.md)
- [promote-credential-contracts](openspec/changes/archive/2026-07-09-promote-credential-contracts/proposal.md)

- [add-contested-finding-rule](openspec/changes/archive/2026-07-09-add-contested-finding-rule/proposal.md)

- [promote-workflow-gate-contract](openspec/changes/archive/2026-07-09-promote-workflow-gate-contract/proposal.md)

- [refine-promotion-provenance](openspec/changes/archive/2026-07-09-refine-promotion-provenance/proposal.md)
- [adopt-workflow-visualization-stack](openspec/changes/archive/2026-07-09-adopt-workflow-visualization-stack/proposal.md)

- [add-doc-health-contract](openspec/changes/archive/2026-07-09-add-doc-health-contract/proposal.md)
- [concretize-prose-tagging-syntax](openspec/changes/archive/2026-07-09-concretize-prose-tagging-syntax/proposal.md)
- [add-lifecycle-notebook-projection](openspec/changes/archive/2026-07-09-add-lifecycle-notebook-projection/proposal.md)
- [add-document-lifecycle-vocabulary](openspec/changes/archive/2026-07-09-add-document-lifecycle-vocabulary/proposal.md)
- [reconcile-domain-neutral-and-engineering-spec-ownership](openspec/changes/archive/2026-07-09-reconcile-domain-neutral-and-engineering-spec-ownership/proposal.md)

- [add-customer-memory-gateway-architecture](openspec/changes/archive/2026-07-08-add-customer-memory-gateway-architecture/proposal.md)
- [enable-live-openxfactory](openspec/changes/archive/2026-06-26-enable-live-openxfactory/proposal.md)
- [restructure-factory-repo-boundaries](openspec/changes/archive/2026-06-26-restructure-factory-repo-boundaries/proposal.md)
- [migrate-canonical-policy-to-openxfactory](openspec/changes/archive/2026-06-26-migrate-canonical-policy-to-openxfactory/proposal.md)

Canonical specs:

- [canonical-contract-migration](openspec/specs/canonical-contract-migration/spec.md)
- [canonical-policy-migration](openspec/specs/canonical-policy-migration/spec.md)
- [memory-gateway](openspec/specs/memory-gateway/spec.md)
- [reference-proof-placement](openspec/specs/reference-proof-placement/spec.md)
- [repo-boundary-governance](openspec/specs/repo-boundary-governance/spec.md)
- [shared-contract-ownership](openspec/specs/shared-contract-ownership/spec.md)

## Install Repo Pins

`openxFactory` pins approved install repo revisions under `installs/` when needed.
Long-term workspace aggregation belongs in the top-level `xFactory` repo, not in
`openxFactory`. DomainxFactory repos should pin the `openxFactory` version they
consume; `openxFactory` should not need to pin every DomainxFactory consumer.

Current submodules:

- [installs/omnigent-install](installs/omnigent-install) -> `opensoft/Omnigent-Install`

Clone or refresh with:

```bash
git submodule update --init --recursive
```

Hermes install is not yet a submodule. Its canonical remote decision is still open; see [Decision 0001](docs/decisions/0001-install-repo-submodules.md).

## Status

This repository is documentation-first. It should not contain live credentials, production memory-provider databases, runtime secrets, generated agent workspaces, or domain-specific runtime data.
