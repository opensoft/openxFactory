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
- [Avatar Internal-Live Kill Switches SOP](docs/sops/avatar-internal-live-kill-switch.md)
  (the named operator surface for the two server kill switches on the
  `gpt-realtime-2.1` internal-live ring — `qualify-avatar-live-voice` §7.7;
  referenced by `canary-cohort-and-rollback-policy.yaml`
  `rollback_policy.operator_surface`)
- [Avatar-First UI Standard](docs/avatar-first-ui-standard.md)
  ([profile examples](examples/avatar-first-ui/README.md) ·
  [deterministic fixtures](examples/avatar-first-ui/fixtures/README.md))
- [Avatar-Client (AVC) Contract Kernel](contracts/avatar-client/README.md)
  (neutral session/consent/revocation contract family; realized at
  `contract-v1.7` with a fail-closed F0 publication gate, extended at
  `contract-v1.46` by AVC-09 voice adapter descriptor and AVC-10 voice latency
  sample — the two reserved identifiers `qualify-avatar-live-voice` publishes,
  with latency gating held in one neutral relative-regression SLO entry rather
  than in a per-profile budget field)
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
- [NotebookLM Projection — Hosting Migration Runbook](docs/notebook-projection-migration-runbook.md)
- [NotebookLM Projection — Hosting Migration Evidence (2026-08-24)](docs/notebook-projection-migration-evidence-2026-08-24.md)
  (the 2026-08-24 run of that runbook: recorded legacy ids, the re-derived
  books, the parity numbers, and the steps held open)
- [NotebookLM Projection Sync — Open Operational Item](docs/notebooklm-sync-open-item.md)
  (pending sync run, the auth blocker + the `scripts/nlm_auth.py` workaround,
  and the machine-account direction)
- [Support-Bundle Scope in the Archive Gate — Open Contract Item](docs/support-bundle-scope-open-item.md)
- [Archived-Change Record Discrepancies — Open Bookkeeping Register](docs/archive-record-discrepancies.md)
  (the re-derived sweep of all 86 archived changes: one `Status:` header
  corrected with its citation, seven classes recorded open)
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

## Wallet validation gate

Every PR to main runs the `wallet-validation` check, including drafts. The
check is REQUIRED: org ruleset
`openxFactory wallet-gate (require wallet-validation)` (id 21538893, active
2026-08-26) requires it on this repository's default branch. Organization
admins retain the bypass, matching the Tier-1 main-protection ruleset's
pattern.

Since `contract-v2.0` the gate is a CONSUMER gate and its workflow file is
[.github/workflows/openxwallet-consumer-gate.yml](.github/workflows/openxwallet-consumer-gate.yml).
The readers it runs are not openxFactory files any more: it initializes the
`openXwallet` gitlink, refuses unless
[`scripts/verify-openxwallet-pin.py`](scripts/verify-openxwallet-pin.py) can
verify [`contracts/openxwallet-pin.yaml`](contracts/openxwallet-pin.yaml) —
recorded gitlink, checked-out revision, eight per-file `sha256`s and the
`pinned_by_commit_only:` set — and then runs the PINNED
`openXwallet/scripts/wallet-yaml-syntax-gate.py` and
`openXwallet/scripts/validate-openxwallet.py` over **openxFactory's own tree**,
which is where `governance/review-authority/` still lives. A final step asserts
POSITIVELY that the intake register was opened: the log must carry the
`repo scan:` note AND the `intake register read:` NOTE and must carry neither
`no intake register at this tree` nor any `register-*` finding code, because a
green check that opened no register is a vacuous pass.

**The FILE was renamed; the TOKEN was not.** Ruleset 21538893 pins the check
`wallet-validation`, which is a JOB ID and not a filename, so the new workflow
retains `jobs: wallet-validation:` verbatim and the ruleset is edited by nothing.
`tests/openxwallet_consumer_gate/test_gate_invocation.py`, collected by the
REQUIRED `pytest-suite`, pins the job id and the literal invocation — the scan
target must be present and equal to `.`, since the pinned validator reads the
intake register only when it sweeps a directory.

The gate surfaces — `.github/workflows/`, `/contracts/openxwallet-pin.yaml`,
`/scripts/verify-openxwallet-pin.py`, the `/openXwallet` gitlink and
`/.gitmodules` — are owner-routed via
[.github/CODEOWNERS](.github/CODEOWNERS) so changes to them need owner review.
The pin and the gitlink are also in codexFactory's merge-gate
`never_clearable_paths` floor (`split-openxwallet-repo` P3b), because they are
what determine WHICH READER RUNS.

## Python test suite gate

Every PR to main runs the `pytest-suite` check, as does every push to main. It
runs the whole suite — `pytest tests/ -m "not postgres"` — on a hash-pinned
install of [requirements/hermes-runtime-contracts.lock](requirements/hermes-runtime-contracts.lock).
The `postgres`-marked tests are excluded because they drive real Docker
containers and belong to their own release-gate runner,
`scripts/run-hermes-runtime-postgres-tests.sh`. The check is advisory until an
operator marks it required.

Mark it required via the active ruleset governing main:
Repo Settings → Rules → Rulesets → edit the ruleset targeting `main` →
Require status checks → add `pytest-suite`.

The workflow runs unconditionally, with no paths filter, so it is safe to mark
required: a filtered check deadlocks the PRs it skips, and a large group of
these tests scans repository content rather than fixtures, so content-only
changes can legitimately turn the suite red.

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
- openxWallet — **CONSUMED AT PIN, not published here, since `contract-v2.0`**
  (`split-openxwallet-repo` P3). The holder-agnostic core and its first profile
  are published by `opensoft/openXwallet` at tag `wallet-v1.1` and consumed
  through [contracts/openxwallet-pin.yaml](contracts/openxwallet-pin.yaml): a
  nested gitlink pinned by 40-hex COMMIT plus eight per-file `sha256` digests,
  with the validator, the syntax gate, both `examples/` corpora and both family
  READMEs carried as `pinned_by_commit_only:`. Validated by the PINNED
  `openXwallet/scripts/validate-openxwallet.py [<repo-path>] [--strict]`, which
  is this family's conformance validator from `contract-v2.0` forward — a wallet
  is a key REFERENCE with a declared custody model and never key material;
  authority travels as attenuated grants; custody CAPS what a signature
  evidences; and wallets stay optional for every domain (`add-openxwallet`,
  relocated by `split-openxwallet-repo`).
- Identity brokering: [contracts/identity-brokering](contracts/identity-brokering/README.md),
  validated by `scripts/validate-identity-brokering.py [<repo-path>]
  [--strict]` — one persona per human within a broker INSTANCE; organizations
  realize company boundaries ON the persona; the broker asserts identity and
  membership only, with the property set a CLOSED ALLOW-LIST at every depth
  (derived from the schema, never a denylist) so the tenancy graph is never
  mirrored; explicit self-link or admin-approved merge only; workloads are not
  personas; and broker credentials are `credential-contracts` references.
  Registered at `contract-v1.37` (`add-identity-brokering`). Opt-in: a domain
  holding none of these artifacts stays conformant and the check reports a
  notice.
- Trust anchors: [contracts/trust-anchor](contracts/trust-anchor/README.md),
  validated by `scripts/validate-trust-anchor.py [<repo-path>] [--strict]`
  with its pytest wiring at `tests/trust-anchor/` — systems trust ANCHORS and
  certificates only derivatively; issuance happens only under recorded
  authority; declared chain custody DERIVES what a certificate evidences,
  through a closed registry that composes with `openxwallet`'s custody rule at
  run time rather than restating it — read since `contract-v2.0` through the
  pinned `openXwallet/` gitlink
  ([contracts/openxwallet-pin.yaml](contracts/openxwallet-pin.yaml)) and refused
  by a NAMED code if the pin does not verify; renewal that changes key material is a
  rebind obligation over dependents enumerated in advance; revocation
  propagates to the authority the certificate supported; and a realization
  DECLARES the obligations it cannot meet. Registered at `contract-v1.37`
  (`add-trust-anchor`). Product-agnostic and opt-in on the same terms.
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
- Avatar internal-live metering alert: `scripts/avatar-metering-alert.py`
  renders the per-tenant metering issue body and title on the doc-health
  pattern (`qualify-avatar-live-voice` task 6.1.4), reading the page target and
  its runbook from `canary-cohort-and-rollback-policy.yaml`
  `operator_surface`. Like the doc-health checker it never invokes `gh`
  itself; the job step that does lands with the serving install (task 6.1.2).
- Versioning: [Contract Versioning Policy](docs/contract-versioning-policy.md)
  and [contracts/CHANGELOG.md](contracts/CHANGELOG.md).

## OpenSpec Records

Active changes:

- [settle-aging-staging-topics](openspec/changes/settle-aging-staging-topics/proposal.md)
  — authored 2026-08-28 on Brett's four bulk rulings over a read-only triage
  survey of the fourteen staging topics `doc-health`'s
  `staged-candidate-aging` family was warning on. **The family read one fact
  about a staged topic — the folder's last commit date — and no `Status:`, no
  register row, no exit record**, so SIX of the fourteen were finished work:
  every exit change ratified, realized and ARCHIVED, the folder retained as
  provenance, and the finding telling a reader to raise a proposal that had
  already landed and closed. One of the six, `github-administration-plane`,
  had carried `Status: superseded` for forty-two days and warned anyway —
  which is the proof the defect was in the READING, not in the corpus's
  record-keeping. The family now honours two records and no others: a primary
  fragment that is `superseded`/`retired`, or an `Exit taken:` line naming a
  change that has ARCHIVED. **A citation of an ACTIVE change does not
  silence** — that is `clean-doc-health-floor`'s archived-packet rule arriving
  from the other side of the same lifecycle, and hiding the age would hide
  half of one live obligation. The unperformable action line ("mark it
  deferred") is corrected: **no `deferred` state exists for a staged topic and
  this change deliberately adds none**, so the five topics it records as
  deferred-with-gate-named — `worker-host-app` and
  `context-compression-runtime` behind Omnigent-Install PR #40 then
  OpsxFactory tasks 8.1/8.2, `proposal-origin-contract`,
  `layer-vocabulary-machine-migration`, `ideation-action-plane` fragment 2 —
  KEEP AGEING, and each says so in its own text. **The number worth reading**:
  measured at a common `--as-of 2026-12-31` so that a folder this change
  touched cannot be mistaken for a folder it silenced, staged-topic findings
  go **33 → 27**, exactly the six — re-measured on the merged head and
  unmoved, which is why that as-of and not today's is the load-bearing
  number. Today's run goes 14 → 3, because the five deferred topics fell
  silent by MTIME RESET rather than by rule the moment their folders were
  committed; they return 2026-09-27 still deferred. MODIFIES one `doc-health`
  requirement (`Aging threshold defaults`), whose promoted text pins the
  mtime-only reading and already carries the exact analogue of the new
  exclusion one clause later, for routing records. Five orchestrator
  decisions flagged for veto, OD-1 first: `dashboard-repo-selector` takes the
  exit record rather than `superseded`, because its exit 2 is unproposed and
  closing it would declare a topic finished that still holds live design.
- [add-credential-escrow-checkout](openspec/changes/add-credential-escrow-checkout/proposal.md)
  — **EXIT 1 OF A TWO-PACKET SPLIT** ruled by Brett on 2026-08-28, over a
  read-only decision round on the staged topic
  `client-credential-escrow-registry`: four multi-choice questions, four
  selections, each taking the prep's recommendation. **A SECOND ACT THE SAME DAY,
  over PR #479, closed the veto window and changed the packet's shape**: OD-2
  VETOED (the schema comes in here after all), OD-4 APPROVED as authored, the
  other five CLEARED, and all five open questions ruled — four on the packet's
  own recommendations and ONE against it (the drill must also prove a live
  refusal). The BREAK-GLASS CHECKOUT
  PATH ships first so that `deployment-handoff-boundary`'s standing-admin
  exception can close — its promoted text holds the operator's existing standing
  administrative access open as a named, dispositioned exception "until the
  break-glass checkout path is realized and tested", and its
  no-standing-credentials requirement already says human direct access is
  "a time-boxed credential checkout with evidence, followed by a retroactive
  request within the governing policy window" while leaving all three of WHO,
  WHAT EVIDENCE and HOW LONG undefined. That change's own design says so:
  "Who can break glass, how credentials are custodied, and the window's length
  belong to `client-credential-escrow-registry`." **Seven ADDED requirements on
  `credential-contracts`, 28 scenarios, no MODIFIED block anywhere**: the
  checkout as an administration-tier custody act (the escrow decryption identity
  is ITSELF a credential, so the ratified `roles-authority-model` custody shape
  applies unchanged, and a client-layer steward holding references may not
  authorize release of values); the three correlated records a break-glass
  leaves, with the audit ENUMERATING EVERY object decrypted; the policy window;
  after-use rotation scoped to what was DECRYPTED rather than what was
  reachable, with the escrow identity itself rotating only where its private half
  left custody onto a non-ephemeral host; escrow recipients DISJOINT from every
  runtime decryption controller, two per object, drills on the per-client key;
  the rehearsed drill as the realization gate; and the re-mint test that decides
  MUST-escrow from SHOULD-escrow. **THE WINDOW THIS SETS**, which
  `add-deployment-handoff-boundary` deferred here in one line and which has no
  numeric precedent anywhere in the family: **opened within 24 hours, disposed
  within 5 business days, both bounds running from the checkout's expiry or
  revocation, neither tolling.** The opening bound is derived from the DETECTOR,
  not from taste — a window longer than the evidence-correlation audit's period
  makes every legitimate break-glass manufacture a finding, and an audit
  destroyed by its own true positives stops being read. Waits are `conditions` on
  the request, which is how that contract already models holds; a late filing
  still correlates and its lateness is its own separate finding, because "late
  means void" makes silence strictly better than filing. **THE FORCING FACT**,
  verified rather than asserted: the opensoft QA install has read
  `execution_binding.mode: opsxfactory_executed` at `status: completed` since
  2026-07-20 and `config/clients/opensoft/credentials/` does not exist — the
  managed-install escrow duty has been live and unmet for five weeks. **NO SCHEMA
  SURFACE** (OD-2): Brett's ruling A — an additive `escrow:` block on the binding
  template plus an escrow-entry record kind — is deferred WHOLE to the successor
  `add-credential-escrow-registry`, because the checkout is expressible in the
  five already-promoted record kinds and the one field it needs beyond them rides
  the promoted audit policy's open `minimum_fields` array. The code surface is
  packaged conformance fixtures at the next additive bundle (`contract-v2.0` is
  declared; the minor is allocated at realization by merge order and is not spent
  here), and the ARCHIVE GATE IS
  MERGE PLUS GREEN PLUS ONE REHEARSED DRILL — the same drill that discharges the
  boundary's phased-never-gapped milestone and closes its exception. **AND THEN
  THE SCHEMA CAME BACK.** The OD-2 veto moved ruling A's `escrow:` relationship
  block on `xfactory_credential_binding_template` and the sixth record kind
  `xfactory_credential_escrow_entry` into this packet on A's literal shape,
  taking the delta from 7 ADDED / 28 scenarios / no MODIFIED block to **9 ADDED +
  1 MODIFIED / 46 scenarios**. The MODIFIED block is surgical and its size is the
  point: a promoted requirement enumerating FIVE record kinds becomes false the
  moment a sixth exists, so five becomes six, two promoted scenarios carrying
  "five" are amended (the only promoted words that move), and two scenarios are
  added pinning the property the whole cut depends on — a binding predating the
  block still validates. The entry shape is the RUNNING PRIOR ART made neutral
  rather than a fresh design, and its one load-bearing property is that every
  field is non-secret metadata, which is what makes the successor's
  decryption-free lint possible at all. **The cut is owed, but not for the usual
  reason, and this was measured rather than assumed**: the credential schema is
  NOT among the 192 entries of `contracts/releases/contract-v2.0.digests.yaml`
  (the closure is `contracts/hermes-runtime/contract-index.yaml` `release_member`
  entries, which hold no credential entry), so release-inventory-drift does not
  force it — the VERSIONING POLICY does, a registered bundle contract gaining a
  record kind and an optional field being the additive minor class verbatim.
  Ruling C's home, grandfathered exception and escalation tests STAY with the
  successor; only the schema half moved.

- [adopt-medxsoft-repository-identity](openspec/changes/adopt-medxsoft-repository-identity/proposal.md)
  — authored 2026-08-27 for the 2026-08-26 transfer of `opensoft/MedxFactory`
  and `opensoft/MedxEHR` to the `MedxSoft` organization, whose operational half
  (remotes, aggregation `.gitmodules`, `medx-roottruth-install` pins) was
  rewired the same day outside OpenSpec. ADDS one capability,
  `repository-identity` (four requirements): the canonical `<owner>/<repo>`
  owed on live normative surfaces, a provider redirect being a grace period
  rather than an identity; the published transfer mapping
  `contracts/policies/repository-identity.yaml`, sibling of
  `layer-vocabulary.yaml`; the freeze on archived packets, dated decision
  records and point-in-time verification tables; and the additive change class a
  transfer takes. Follows `adopt-subject-tenant-domain-vocabulary` exactly —
  rename the live surfaces, freeze the recorded spellings, resolve the frozen
  ones by lookup — with the freeze here justified by evidence integrity rather
  than by pinned consumers. **30 occurrences across 23 files: 20 renamed across
  15, 10 frozen across 8.** Owes a contract bundle, measured: six edited files
  are non-editorial members of the declared `contract-v2.0` digest inventory, so
  `release-inventory-drift` reports six `ERROR`s until the cut re-baselines the
  inventory; the minor is allocated at realization and none is reserved here.
  The consequence a sweep would have missed is recorded in `design.md` § 4 —
  the regression denominator is bytewise sorted, `M` precedes `o`, so the entry
  moves to the head of the list and `PINNED_TABLE` moves with it in the same
  commit.
- [create-ledgerxwallet-overlay-boundary](openspec/changes/create-ledgerxwallet-overlay-boundary/proposal.md)
  — **RATIFIED 2026-08-28** (in-session ruling "ratify #449" on PR #449, both
  required checks green; ratified AS PROPOSED, meaning the NARROWED v1 — see
  below; realization via Speckit), authored 2026-08-27 as **P6 of the ratified
  `split-openxwallet-repo`**, which names this change by id in its § Successors
  named and again as its `tasks.md` 12.1; opened on Brett's in-session ruling of
  the same day over the successor set ("approved. do all of these"), recorded in
  `.openspec.yaml` as an ADMISSION to the queue and not a ratification of content.
  Registered under DTN-026, whose resolution names `LedgerxWallet` as the first
  descendant (R8). **The FIRST domain descendant repository created under the
  ratified `domain-descendant-boundary`** — a standard that until now had five
  requirements and no instance. ADDS one capability,
  `ledgerxwallet-overlay-boundary` (five requirements): the pin declared TWICE in
  ONE commit and checked by the descendant's OWN validator; the domain resolving
  openXwallet only through the nested descendant, at a fixed path, in tooling AND
  in written procedure; profile-never-estate-never-fork; a relocation reducing no
  coverage and breaking no prepared procedure; and a creation gate scoped to
  Ledgerx that CITES the ratified rule for the four sibling names rather than
  re-legislating it. Issues NO delta against `domain-descendant-boundary` or
  `neutral-product-pin`, which are RATIFIED-IN-CHANGE and **not yet promoted** —
  `openspec/specs/` holds 52 capabilities and neither is among them, because that
  change archives only on merged plus green realization evidence.
  **What the packet argues:** the rule-1 breach is a RESOLUTION PATH, and P5b
  (LedgerxFactory PR #30, `b131286`) narrowed it without closing it —
  `VALIDATOR_CANDIDATES` still holds two candidates and both are paths in other
  repositories reached by a five-level walk, with a second breach site in
  `specs/016/quickstart.md:19`, which invokes the neutral validator through
  openxFactory's checkout. Candidate pruning cannot make a walk into a pin; a
  descendant can. **What it moves is deliberately small: the pin and
  `templates/wallet-exercise.template.yaml`, and nothing else.** The packet was
  **narrowed by its own review** — it originally relocated the estate validator
  and the distinct-holder constraint too, and withdrew both on arithmetic rather
  than preference: openXwallet `wallet-v1.1` PRUNES nested repositories from its
  sweep (`sweep_candidates`, `validate-openxwallet.py:2063`), so a relocated
  record would be adjudicated by NOTHING; the constraint's move takes
  `check_real_estate`'s `>= 5` artifact floor to 4 and voids its
  `EXPECTED_CONSTRAINT` lookup; and the validator is LedgerxFactory-AUTHORED, so
  rule 1 — which forbids integrating THE PRODUCT'S validator — never required
  moving it, while moving it would have opened four seams (`REPO` serves four
  referents; `find_aggregation()` is a second upward walk feeding a leg the
  parent's ratified `tasks.md` 6.2 makes this bar the only observer of). Both
  relocations are successors with stated preconditions. Placement is
  **nested-only** on the RATIFIED DTN-022 precedent this domain already realizes
  for `LedgerxAvatar`, with its price NAMED: a nested descendant is outside every
  governed-repo enumeration in the corpus, as `MedxAvatar` and `LedgerxAvatar`
  already are. Review was heavy and is retained in full: **alignment 37 findings
  across two reviewers; council 54 verdicts across three seats — Product Advocate
  and Systems Architect PROCEED WITH CONSTRAINTS, Adversary Engineer
  RESTRUCTURE**, and **the RESTRUCTURE was TAKEN rather than argued down**.
  `clarifications.md` carries fourteen constraints plus a register of the findings
  MOOTED by the narrowing, so the record shows which objections were answered by
  argument and which by removing the thing objected to. **Q2 — the parent's one
  open question, do `tenants/ledgerxcorp/wallets/*` move? — is RULED STAY at this
  ratification and is CLOSED**, on the records' instance-shaped contents, the
  nested prune (relocating them would move them OUT of adjudication, not into a
  boundary), and the Product Advocate's own reason: those five files are the
  commit target of the runsheet's unexecuted Phase 3.4, which mints real keys.
  Two further ratification items: the **custody-posture cut STANDS** as a
  successor, and the **nested-only placement's governed-enumeration gap STANDS**
  with its cost named rather than closed.
  `code_surface` spans three repositories and `target_release: implemented`, so it
  archives only on merged plus green realization evidence, never on landing.
  Realization is Speckit AFTER ratification; preconditions P5b and P3b
  (codexFactory PR #117, `58bd3cf7`) are both DISCHARGED and P4 does not gate it.
  **REALIZATION, 2026-08-28 — groups 3, 4 and 5 built; NOT yet archivable.**
  `opensoft/LedgerxWallet` EXISTS (private, created empty; `main` at
  `0a0141ca`): the pin manifest and the nested `openXwallet/` gitlink at
  `63f5a1adac89f017e70bab9a4ffe7cf02d6e6705` in ONE commit (`304cd3c`),
  `tests/validate_pin.py` with four fail-closed checks all RED-proven,
  `.github/workflows/pin-validation.yml`, and
  `templates/wallet-exercise.template.yaml` carried byte-identically (blob
  `dda063c0` in both trees). Ruleset `21701436` went EVALUATE -> reported (PR #1)
  -> **ACTIVE**, so `pin-validation` is a REQUIRED context on that repository's
  `main`. LedgerxFactory PR #31 (feature `020-ledgerxwallet-descendant-nest`)
  carries group 5 as ONE commit with the full 17-validator bar green, the
  artifact floor still at 5, the pin-reconciliation leg still reporting, and the
  parent's finder evidence MIGRATED rather than deleted. **Two things remain
  before archive:** that pull request is open rather than merged, and the tag
  `lxw-v1.0` (task 6.10) is an unperformed `[OPERATOR]` act — as is telling the
  live window's operator that the template's path moved (task 5.7), which is not
  a file edit and which the runsheet's own P0.5 does not substitute for.

- [qualify-avatar-live-voice](openspec/changes/qualify-avatar-live-voice/proposal.md)
  — **RATIFIED 2026-08-27** (in-session, "ratify avatar"; §2/§3 build lands in
  the same round) — authored 2026-08-26 as the staged topic's Exit, executed on Brett Heap's
  in-session rulings of the same day: all five blocking forks and all three
  latent decisions, carried into the proposal as LOCKED decisions rather than
  re-litigated. This is the change that turns on real voice — internal-live
  provider qualification of the live WebRTC/broker/media plane behind the
  fail-closed `SessionTransport` port, with `gpt-realtime-2.1` as the
  candidate. ADDS the neutral `avatar-live-voice` capability (nine
  requirements): AVC-09 voice adapter descriptor and AVC-10 voice latency
  sample lifted from reserved to defined using their RESERVED SHAPES AS-IS —
  Fork 2's Option C means AVC-09 gains NO numeric latency-budget field; the
  internal-live activation gate as the kernel's FOUR-element ring (secret
  scan, telemetry-redaction verification, kill-switch proof, measured latency
  evidence) with the eight-condition GPT-Live-1 list demoted to the mapped
  preflight/canary checklist that produces that evidence and condition 6
  reinterpreted as no-material-regression; a neutral relative-regression
  latency SLO at the RATIFIED threshold (>15% relative OR >150 ms absolute,
  whichever is greater, on first-playable-after-authorized and sideband-ready;
  p50+p95 gated on Windows desktop + web canvas at nominal network; p99 and
  teardown recorded, not gated); a fresh client-side direct-provider baseline,
  because F0's Python/aiortc figures explicitly do not qualify as the
  reference; broker-held custody with two independent fail-closed spend layers
  (session hard-kill on the existing duration/quota terminal, dedicated
  spend-capped internal-live provider project as the per-tenant/ring stop) and
  the durable per-tenant counter deferred; synthetic evaluation audio with a
  strictly ephemeral, single-model, never-retained consented canary that
  unreserves NO retention class and adds NO consent purpose; and the written
  revoke-versus-block rollback policy the kernel required and never had, with
  disable-voice-to-text/handoff as the only rollback target because this is
  the first qualified profile. MODIFIES three `avatar-client-runtime`
  requirements (the reserved-set release of exactly AVC-09/AVC-10, the
  internal-live-ONLY reading of promotion evidence, and the latency-evidence
  rule) plus `repo-boundary-governance` and `avatar-client-lab`, because
  latent decision 1 makes this the change that owns the client extraction
  from codexFactory `apps/avatar-client-lab` — an
  obligation canon carried with no change owning it. `Status: ratified`
  (2026-08-27, in-session), with §2 (the AVC-09/AVC-10 schemas, their packaged
  positive and negative examples, and the manifest/CHANGELOG registration) and
  §3 (the interface-lock unreservation of exactly those two ids, the validator's
  rules for them, the two-tier latency rule, and the acceptance-map entries)
  built in the ratifying round. **§4.1 and §6.3.1-§6.3.2 landed 2026-08-27**:
  the internal-live activation checklist
  (`contracts/avatar-client/internal-live-activation-checklist.yaml`) recording
  the eight conditions in the ratified preflight/canary split with condition 6
  in its reinterpreted form only, and the canary cohort plus **the recorded
  revoke-versus-block policy** the kernel has referenced since it was written
  and never had (`contracts/avatar-client/canary-cohort-and-rollback-policy.yaml`),
  both machine-checked by new fail-closed `validate-avatar-client.py` rules
  proven by an 18-mutation check. REMAINING: the four ring-evidence elements
  (§4.2-§4.5), the fresh client-side latency baseline and gated cells (§5),
  credential custody and spend containment (§6.1), the live transport (§6.4.3),
  and release evidence (§6.4.4).
  **§6.4.1 is TICKED SATISFIED-BY-DTN-022 and §6.4.2 is RE-SCOPED, on Brett's
  naming rulings of 2026-08-27** (in-session, via AskUserQuestion). §6.4.1 and
  §6.4.2 had been raised as mis-specified against the world and were not
  executed: codexFactory `apps/avatar-client-lab/` was deleted on 2026-08-03
  (`2b79da35`, PR #74) when Brett's DTN-022 ruling moved the lab to
  `opensoft/openAvatar` with full subtree-split history — already pinned into
  the aggregation — while the `xfactory-avatar-client` name pointed at a repo
  parked since 2026-07-14. The rulings: **R1** the client repo KEEPS the name
  `openAvatar` (it already IS the extracted client) and canon's
  `xfactory-avatar-client` — a name predating openAvatar becoming a
  first-class product — is amended to it; **R2** `openAvatar-server` is
  recorded as the named future home for deployable avatar server code, created
  only by whichever change first ships such code; **R3** the parked, empty
  `opensoft/xfactory-avatar-client` was deleted 2026-08-27, nothing having
  referenced it. §6.4.2 is now a RESYNC of `openAvatar/contract_pin.yaml` to
  `contract-v1.46` at `046466a0`, discharged by a PR in openAvatar and left
  unticked here until it merges.
  `code_surface: openxFactory, openAvatar` and
  `target_release: implementation_pending`, so it archives only on merged plus
  green internal-live realization evidence, never on landing. Aggregation
  admission of the client repo, the GPT-Live-1 default swap, and the
  `avatar-pilot-hardening` deferrals are explicitly out of scope.

- [add-standing-policy-compliance-contract](openspec/changes/add-standing-policy-compliance-contract/proposal.md)
  — authored 2026-08-24, **NOT YET RATIFIED** (`Status: draft`). Neutral-first
  front-end half of codexFactory issue #3, ruled by Brett Heap the same day:
  machine-readable standing-policy veto vocabulary, loud compliance-decision
  evidence and a central revocable policy-allowance registry whose IDs — never
  copied payloads — travel through governed bindings. Every dispatch keeps a
  permanent deterministic floor; a bounded classifier may escalate ambiguity
  but cannot erase a deterministic finding; live Hermes intake adds judgment
  above the floor rather than subsuming it. codexFactory is the named first
  conformer through successor `add-intent-compliance-gate`, with FEAT-003 as
  the regression: no allowance blocks before worker tokens are spent, a valid
  allowance passes explicitly, and revocation blocks the next dispatch and
  admission. Realization cuts the next additive contract bundle; no domain
  detector, runtime registry service or allowance instance lives here.
- [add-model-capability-vocabulary](openspec/changes/add-model-capability-vocabulary/proposal.md)
  — authored 2026-08-24, **NOT YET RATIFIED** (`Status: draft`). Exit (a) of the
  staged topic `doxchat-auto-fit-routing`, whose six questions were
  dispositioned the same day. `contract-v1.38` gave the catalog a routing rule
  whose resolution is STATIC; Brett's direction at that release's rule-5 ruling
  was that the destination be chosen PER TURN by whether the model can
  accommodate the turn — and he named a dimension the catalog cannot express
  ("if we need multi modal then we have to select from that"). The entry says
  how MUCH a model accepts (`input_limit_bytes`) and nothing about WHAT KIND, so
  a router asked to keep an image turn away from a text-only model has nothing
  to read. Adds ONE optional, closed `modalities` declaration — exactly `text`
  and `image` — extended only by the change that governs a new member, the rule
  the client-identity roster already applies to admission surfaces. Optional and
  absence-tolerant because requiring it would break every catalog released
  before it: absence means "a producer older than the field" and is read as
  text-only for routing, reusing the chat-turn family's own idiom. Per Q3's
  batching obligation it also DECIDES the two recorded catalog follow-ups rather
  than passing them by, and TAKES both after reproducing each: the released
  64-entry cap is unenforced type-side (a 65-entry catalog constructs), and
  `model_id` is not held to its released length and pattern (a 200-character id,
  and one containing a space, both construct) — the same type-weaker-than-wire
  divergence this capability already closed once for `routes_to`, and N7's
  recorded reason for deferring ("a behaviour change belonging to no release")
  is dissolved because this IS that release. Requirements are ADDED, not
  MODIFIED: the requirement governing the catalog already carries a live
  MODIFIED delta from the ratified-but-unbuilt intake lane. **Realization is a
  CONTRACT RELEASE** — schema bytes move — but the bundle number is deliberately
  NOT allocated in the proposal: `contract-v1.41` only if the pending Unreleased
  block has not folded first, fresh-counted at allocation. Exits (b) fit-aware
  routing and (c) compress-to-fit disclosure are named successors; (a) touches
  only the schema, the type and the validator, which is why it is safe to raise
  while (b) must be sequenced against the intake build.
- [add-notebook-hosting-credential-custody](openspec/changes/add-notebook-hosting-credential-custody/proposal.md)
  — authored 2026-08-23, **NOT YET RATIFIED** (`Status: draft`). The follow-up
  to `add-notebook-projection-identity`, on Brett Heap's direction the same day:
  *"this is a xFactor001 login. and we want to store the password in a kv and
  have xFactory and openXdox login with its own authority."* The declared
  hosting identity change named the account and said nothing about its
  CREDENTIAL, leaving the password wherever its creator put it — the
  personal-account failure moved one level down rather than removed. Adds the
  POSITIVE custody obligation the ratified generalization lacks (that
  generalization forbids hard-coding a credential; it does not require custody
  to exist, so an account whose password lives only in its creator's head
  satisfies it), extends custody to the whole credential set including a
  second factor's seed, and rules ONE IDENTITY / PER-SYSTEM AUTHORITY: each
  consuming system reaches the shared account through its own binding, access
  identity, grant, rotation visibility and audit trail — one identity may be
  shared, one authority may not. The hosting record gains a BY-REFERENCE
  custody pointer, never secret material. Two findings shaped it: the promoted
  by-reference requirement already refuses distributing refreshable session
  state, and the `nlm` profile is exactly that class — so Brett's
  no-shared-session ruling is independently required on credential-class
  grounds, not just accountability; and the live binding INSTANCES do not
  belong here at all, because `contracts/manifest.yaml` records that
  *"openxFactory ships no instance records (they live in client installs,
  credential-contracts residency model)"* — so the neutral obligations land
  here and the concrete bindings land in the install lane and openXdox's own,
  a redirection of the ruling's route that is FLAGGED for the ratification
  read rather than decided quietly. Honest gaps recorded, not assumed away:
  **custody is not automation** (the sign-in is a browser flow with ~20-minute
  sessions and possible 2FA; automated login stays future work), a TOTP seed
  may itself need custody, and **no live secret is created, moved or read by
  this change**. `target_release: none` — the binding-template shape is already
  published, `contracts/` is untouched, no bundle is cut.
- [declare-client-standing-policy-contract](openspec/changes/declare-client-standing-policy-contract/proposal.md)
  — authored and ratified 2026-08-23 (Brett Heap, in-session). Closes
  `opensoft/openxFactory#254`: `hermes_client_overlay` is a contract THIS repo
  owns, and a live runtime already validates and seeds two blocks on it that no
  file here declares. hermes-install `add-client-overlay-standing-policy`
  (ratified 2026-08-22, merged) gave a **Tenant** layer an optional
  `client.policies` map plus a `client.policy_namespace` it is address-validated
  against, so company-wide standing policy can seed at the tenant-operator seat
  — closing the design/code half of `xFactory-Hermes-Install#34`. Brett's
  sequencing ruling landed that deliberately rather than gating it upstream
  ("nothing in the current runtime enforces against the unknown field … But
  `client.policies`/`client.policy_namespace` are currently an UNDECLARED
  extension of a contract this repo owns"); this change formalizes it.
  DECLARES both properties INLINE under `client` — not as a fourth sibling
  schema file, because the three existing siblings each dispatch on a
  self-identifying inner `kind:` these entries do not carry, and the subject
  family answered the same question the same way. `client.required` stays
  byte-frozen at `[ref, display_name, policy_overrides]`, so an overlay that
  declares neither key takes exactly its previous verdict and no consumer is
  forced to re-pin. A faithful mirror of `subject.policies` one layer up with
  ONE ruled difference: **no `relation_to_*` field**, because a tenant's
  standing policy is a POSITION and not a deviation.
  `scripts/validate-client-content.py` learns the six rules the shape cannot
  express (JSON Schema in this family has no `if`/`then`, so the conditional
  namespace requirement lives in the validator) plus a prohibited-block and
  credential scan **scoped to the `client.policies` subtree only** — the
  asymmetry with the subject path's whole-document walk is DELIBERATE, since
  widening it would re-decide the verdict of released overlays that use none of
  the block and would invert the one-directional divergence the sequencing
  ruling was granted on. Its self-test hardcoded exactly one positive filename,
  so it now sweeps every packaged positive; one new positive and eight
  negatives ship. Delta: `client-layer-tuning` (MODIFIED
  `Client content shapes are contract-validated`, ADDED
  `Tenant standing policy is address-resolvable and validated` and
  `A declared standing-policy block is never empty and never carries key
  material`). Release is SHARED: the manifest digest is recomputed and a
  `## Unreleased` section opened, but **no minor is allocated** — the cut, the
  digest inventory and the tag happen once, with the other next-additive-bundle
  changes. Archives only when hermes-install re-pins and admits
  `hermes_client_overlay` to its `PARITY_KINDS` sweep.
- [create-medxpractice-overlay-boundary](openspec/changes/create-medxpractice-overlay-boundary/proposal.md)
  — MedxPractice owns the private practice-operations composition boundary and
  pins the independent public openPractice application at an immutable commit.
- [add-notebook-projection-identity](openspec/changes/add-notebook-projection-identity/proposal.md)
  — authored and ratified 2026-08-23 (Brett Heap, in-session). The single exit
  of the staged topic `notebook-projection-identity`, raised the day its last
  precondition was met. The whole governed NotebookLM projection — every
  per-repo Ideation book, `xf-drafts`, `xf-canon`, every live `xf-session-*` —
  is created under one person's personal consumer Gmail, because the `nlm` CLI's
  default profile is whoever ran `nlm login` first; proven live 2026-08-15 when
  Brett hit a "request access" wall on a dashboard notebook link and the request
  landed in that personal inbox. This makes the hosting identity a DECLARED
  TWO-CASE INTAKE FACT: operator-hosted (a company-owned Google Workspace USER
  account in the operating party's own domain) or self-hosted/personal, both
  legitimate. A Google USER account is a platform constraint, not a preference —
  NotebookLM has no API and a service account cannot drive its consumer web UI.
  Opensoft declares Case A on `xFactor001@opensoft.one` (confirmed by Brett
  2026-08-23, who also authorized raising this change). The sync runs under the
  declared account's profile; access is shared out FROM that account and never
  by handing out its credentials; a governed manual approval act WRITES the
  share-out roster, which IS the record rather than an audit trail beside one,
  keyed `(hosting_account, user, book_or_alias, role, granted_at, granted_by)`.
  The custody rule GENERALIZES `credential-contracts`' promoted vault-operator
  execution-binding requirement rather than adding beside it — no new record
  kind. Encodes the five dispositions merged as PR #272, of which Q3 is the
  evidence centerpiece: the mapping onto `client-identity-roster` was RUN, not
  assumed, and refused the shape structurally (11 honest errors; the force-fit
  passes with one grantee and fails with two on `duplicate-identity-key`,
  because the grantee is not in the uniqueness tuple — that roster is one
  principal / many scopes, a share-out list is one scope / many principals).
  Migration follows the 2026-08-10 retirement runbook with parity proven against
  THE CORPUS SCAN, carrying two review-verified gaps as scope: a plain `--apply`
  never creates live session notebooks, and `ensure_workspace_record()` refuses
  to re-register a same-key book under a new provider id.
  `target_release: implementation_pending` — it archives only on Opensoft's own
  cutover, proven parity, and the personal-hosted books retired by recorded act.
- [create-medxchart-overlay-boundary](openspec/changes/create-medxchart-overlay-boundary/proposal.md)
  — local topology realization completed 2026-08-23: MedxChart now owns the
  Medx composition boundary, pins openChart at an immutable commit, and the
  xFactory aggregate no longer tracks openChart directly. The intended
  `opensoft/MedxChart` remote still requires a separate publication act.
- [add-nightly-dashboard-refresh](openspec/changes/add-nightly-dashboard-refresh/proposal.md)
  — authored 2026-08-22, **RATIFIED 2026-08-25** against its realized system
  (Brett, in-session: "ratify add-nightly-dashboard-refresh against its
  realized system"). Its code is MERGED AND WIRED across all three
  repositories — openxFactory #260/#261, aggregation opensoft/xFactory #141,
  Omnigent-Install #123/#126/#129/#143/#146/#153 — with required-check ruleset
  21294850 live on Omnigent-Install's default branch. **The ARCHIVE gate stays
  OPEN**: this change's own `target_release` requires one real nightly pin PR
  merged and reconciled PLUS one wider diff refused and parked, and NEITHER has
  happened — the build+push child has never run, no `bot/dox-dashboard-pin` PR
  has ever existed, and both nightlies since the chain landed failed with every
  refresh step skipped. Merged and wired is not exercised; §7 and §8.5 stay
  open, discharged by the first real nightly in either direction. The
  openxFactory COMPANION to Omnigent-Install's just-merged
  `add-dox-gitops-reconciliation` (its `main` `7d0370d`, 2026-08-22), which took
  the APPLY and deliberately deferred two open questions to this change. Gives
  the nightly a sixth lane: an ideation-dashboard IMAGE REFRESH stage on the
  `cpc-omni01` artifact worker, ordered after the report delivery — fresh
  openxFactory `main` checkout, `--strict` snapshot generation from THAT
  checkout (0 errors / 0 warnings, and the gate precedes the push, so a strict
  failure publishes nothing), image build from Omnigent-Install's
  `containers/ideation-dashboard/Dockerfile` at ITS `main` over the assembled
  workspace context, date-stamped push to `acropensoftxfactoryqa.azurecr.io`,
  digest captured. One revision for snapshot and baked `/source` corpus by
  construction, which is what keeps the freshness header honest. The no-change
  short-circuit is decided on INPUT REVISIONS BEFORE the build — unmoved corpus
  and unmoved build recipe ⇒ no checkout, no build, no push, no PR, no deploy —
  explicitly NOT on built-vs-pinned digest equality, which can never hold
  (fresh-checkout mtimes move the copied layers; the base image tag floats) and
  would therefore redeploy content-equivalent images nightly. Provenance for
  that check is a machine-readable block in the pin's own overlay comment (the
  precedent the two hand-written pins already set in prose), scoped to each
  repository's BAKED INPUTS rather than its branch tip so the lane's own merged
  pin cannot force the next rebuild; absent/unparseable provenance counts as
  changed and bootstraps. RULES both deferred questions: **(a)** the auto-merge
  mechanism is the aggregation's existing Merge Master pattern extended to
  Omnigent-Install with a SECOND candidate class in its reviewed
  `candidates:` list (author + fixed head `bot/dox-dashboard-pin` + base +
  one-file `path_allowlist` + `require_all_checks`, with the LINE-level
  digest-shape predicate contributed by a repository-side required check,
  because no envelope field expresses it) — fail-closed, base-branch-only
  rules and logic, revocable in one config edit, no org-ruleset bypass;
  **(b)** the lane identity is the EXISTING `XFACTORY_APP` the reusable
  workflow already mints per run, requiring its installation on
  Omnigent-Install at `contents: write` + `pull_requests: write` (verified by a
  real authenticated call, not a settings page), with a dedicated App as the
  recorded contingency. Worker/App/approver/GitHub/Flux hold four separate
  rungs; `execute_final_action` and `access_secrets` stay false; the only new
  grant is a push-scoped, host-local, by-reference ACR credential (needs an
  Omnigent-Install schema delta — `acr_pull` is
  `additionalProperties: false`). SIX ADDED requirements on `doc-health` (the
  lane contract, where every sibling nightly lane already lives) plus ONE ADDED
  and ONE MODIFIED on `ideation-dashboard` (the served plane's rebake bound;
  the MODIFIED restates all four promoted scenarios verbatim, preserves "an
  image rebuild MUST NOT be required to reflect newly published snapshots"
  exactly, and RECORDS the standing conformance gap that the hosted image
  performs no runtime fetch today, so its baked artifacts are its data).
  `target_release: implementation_pending`.
- [add-roster-directory-admission-surface](openspec/changes/add-roster-directory-admission-surface/proposal.md)
  — authored 2026-08-22, **NOT YET RATIFIED** (`Status: draft`). Admits the
  single `directory` (service-discovery) admission surface into the closed
  `admission_surface` vocabulary of `client-identity-roster`, through the
  capability's own extension route, so OpsxFactory can enroll its realized
  `microsoft_service_discovery_reader` (`Organization.Read.All` +
  `Application.Read.All` + `Domain.Read.All`, `exact_effective_scopes`,
  `reject_write_or_destructive_scopes`). Sibling of the archived
  `add-roster-device-admission-surface`, and the change its ratified F2 note
  anticipated ("endpoint-MUTATION and Entra-DIRECTORY remain SEPARATE FUTURE
  surfaces with their own governing changes"). `directory` is ONE tenant-wide
  READ surface: one admission act (admin consent for exactly those three
  read-only roles on one registration — a directory-wide role such as
  `Directory.Read.All` is outside it, since it also reads the admitted `device`
  surface), one scoping mechanism (tenant-wide read, no narrower provider
  selector, `enforcement_mode: logic_enforced`), and its governed unit IS the
  tenant directory/service estate — so tenant-wide read is the GOVERNED scope
  (`exceeds_governed_unit: false`, no `declared_excess`, no `spanned_surfaces`)
  and the provider areas read live only in the member's `description` prose.
  Entra-directory MUTATION and endpoint MUTATION stay separate future surfaces.
  Proposed on the realization evidence of OpsxFactory
  `add-managed-service-inventory` §1–§6 (merged 2026-08-22, `main` `824f8ef`),
  per that change's ratified F1 ordering, which makes this vocab extension a
  blocking PREREQUISITE of its §7 live sweep and requires it to be justified on
  the DETERMINISTIC contract, never on a live snapshot. ONE MODIFIED delta on
  "Identities are enumerated by admission surface, not by product name" (all
  three promoted scenarios restated verbatim, one scenario added). Additive —
  no `contract_schema_version` bump; realization (tasks §1–§5, post-ratification)
  bumps the bundle contract-v1.38 → contract-v1.39.
  `target_release: implementation_pending`.
- [implement-keycloak-install-repo](openspec/changes/implement-keycloak-install-repo/proposal.md)
  — authored, RATIFIED, and REALIZED 2026-08-21 (Brett: "do both install
  repos"). Created and seeded `opensoft/Keycloak-Install` (private, repo id
  1342329131, seed `1aa184e`) under the ratified "Keycloak install repository
  boundary" requirement: boundary README, `contract-v1.37` pin (manifest
  digests re-derived from the tag's blobs), credential-free deploy templates,
  boundary validator with red-proven self-test, session-open-pr mirror,
  1-review main ruleset. PENDING: the org-owner act adding the repo to the
  openxfactory App installation (tasks 1.3/3.3); aggregation admission is a
  named separate change. Sibling of `implement-openxpki-install-repo`.
- [implement-openxpki-install-repo](openspec/changes/implement-openxpki-install-repo/proposal.md)
  — authored, RATIFIED, and REALIZED 2026-08-21 (same instruction). Created
  and seeded `opensoft/OpenXPKI-Install` (private, repo id 1342329163, seed
  `05f4404`) under the ratified "OpenXPKI install repository boundary"
  requirement: boundary README, `contract-v1.37` pin, the digest-only
  deploy home (no manifests — the QA topology migrates per the amended
  `add-openxpki-qa-image-pipeline` tasks 3.4 once that draft lands),
  boundary validator with red-proven self-test incl. DER-structure and
  build-source classes, session-open-pr mirror, 1-review main ruleset. Same
  PENDING org-owner act; found and booked: the `contract-v1.37` release
  digest inventory omits both new families (tasks 4.7/4.8 bookkeeping).
  Sibling of `implement-keycloak-install-repo`.
- [add-doxchat-model-intake](openspec/changes/add-doxchat-model-intake/proposal.md)
  — authored 2026-08-21 from Brett's live browser annotation on the doxBench
  chat rail ("this model selector is not working… we need to have add model as
  the first option… bring up a wizard that helps the user auth with oauth to
  their subscription or add a api"). Diagnosis first: the selector is not
  broken but structurally empty — `serve.py`'s `main()` has no model flag, so
  `reserve-dashboard.sh`'s `python3 -m ideation_dashboard.serve` declares no
  `model_port_factory` and the catalog route honestly returns the empty
  editor-only posture; nothing is hardcoded and no model list was ever
  withheld. The change adds the intake affordance FIRST in the selector and
  default when the catalog is empty (never when it could not be READ), an
  intake flow that hands an API key or an OAuth authorization to the declared
  credential broker and keeps only a `credential-contracts` binding, and the
  seam nobody had written down: intake PROPOSES and a recorded human gate
  action APPROVES, so supplying a payment credential never doubles as
  approving a provider for governed work. Sequencing is a requirement, not a
  note — the affordance never ships ahead of the flow. Depends on
  `add-model-provider-broker` (custody, minting, the narrowed provider
  boundary), which is itself blocked on openProfiler; needs an additive
  `gate-action-record` action enum member at realization.
  **BUILT 2026-08-26.** The blocking dependency is discharged on both sides —
  `add-model-provider-broker` merged (PR #392, main `bb7d7ae8`) and openProfiler
  declared its CLI surface (PR #18, main `d0538c31`, `docs/broker-cli.md`) — and
  sections 1, 2 and 3 are complete: the affordance renders first and defaults on
  an empty catalog (never on an unreadable one), the flow streams what a human
  supplies straight into the declared broker and keeps only the binding, a
  PENDING declaration contributes no available entry, and
  `POST /actions/workbench/model-approval` writes an `approve-model` gate action
  carrying issuer/approver/expiry/audit reference before anything becomes
  selectable. It also discharges the task handed over by
  `add-model-provider-broker` (its 2.4): the mid-turn re-mint and the paid retry
  it buys are now VISIBLE in the turn record and in the rail, per Brett's
  2026-08-26 ruling. Both land as one ADDITIVE cut,
  `target_release: contract-v1.45` (`approve-model` plus `target.model_declaration`
  and `model_approval` on `gate-action-record`; the optional `provider_retry` on
  `workbench-chat-turn-v2-success`). It stays ACTIVE: tasks 4.1 (live-console
  proof, which needs a human at a real browser) and 4.2 (realization evidence)
  are open, and under `release-realization` this change archives only on merged
  plus green.
- [add-identity-brokering](openspec/changes/add-identity-brokering/proposal.md)
  — authored and **RATIFIED 2026-08-21** (recommendations adopted as written;
  the OQ-5 co-residence gate discharged: HealthLinc patients found and
  pre-declared the first dedicated-instance client — see the change's
  review/ finding). The neutral identity-brokering capability (exit 1 of
  the `identity-brokering-plane` staged topic, from Brett's 2026-08-21
  rulings): one persona per human within a broker instance, organizations
  realizing company boundaries on the persona, the broker asserting identity
  and membership only (never mirroring the tenancy graph), explicit
  linking/admin-merge only, workloads-are-not-personas, broker credentials as
  credential-contract records, and isolation escalating by broker instance.
  Also ADDS the `Keycloak-Install` repository boundary to
  `repo-boundary-governance` (avatar-client template; creation by successor
  `implement-keycloak-install-repo`). Sibling of `add-trust-anchor`.
  **REALIZED 2026-08-21** by Speckit feature
  `008-identity-brokering-contracts` (six schemas at
  `contracts/identity-brokering/`, canonical validator
  `scripts/validate-identity-brokering.py`, 14 positive + 41 negative
  fixtures at 9/9 requirement coverage), hardened by a two-panel adversarial
  review across the sibling families (14 + 14 confirmed findings — 28 and 52
  bypass probes respectively — all fixed, ruled, or documented, with zero
  ratified-corpus regressions), and **registered at `contract-v1.37`**.
- [add-trust-anchor](openspec/changes/add-trust-anchor/proposal.md)
  — authored and **RATIFIED 2026-08-21** (OQ1 and OQ2 ruled per their
  recommendations: establish-obligation with a declared floor; closed
  custody enumeration, escrow as a relationship not a tier). The neutral trust-anchor capability (exit 1 of the
  `pki-trust-anchor-plane` staged topic): anchors as governed records,
  issuance only under recorded authority with evidence obligations, declared
  chain custody deriving what a certificate evidences (composing with
  `openxwallet`, consumed at
  [contracts/openxwallet-pin.yaml](contracts/openxwallet-pin.yaml) since
  `contract-v2.0`), renewal-as-rebind with dependent bindings recorded against
  the certificate, revocation propagation, CA material as
  `credential-contracts` records, and the declared-degraded-obligation rule —
  product-agnostic across the two converging realizations (live Intune Cloud
  PKI canary; OpenXPKI planned for the Opensoft production core). Also ADDS
  the `OpenXPKI-Install` repository boundary to
  `repo-boundary-governance` (creation by successor
  `implement-openxpki-install-repo`; image custody stays in
  `opensoft/Opensoft-Tenant`). Time-critical rider: the OpsxFactory
  `add-openxpki-qa-image-pipeline` Impact amendment must land before that
  change ratifies. Sibling of `add-identity-brokering`.
  **REALIZED 2026-08-21** by Speckit feature `009-trust-anchor-contracts`
  (seven schemas plus the closed chain-custody registry pair at
  `contracts/trust-anchor/`, canonical validator
  `scripts/validate-trust-anchor.py` with its `tests/trust-anchor/` pytest
  wiring, 34 positive + 65 negative fixtures at 8/8 requirement coverage),
  hardened by a two-panel adversarial review across the sibling families
  (14 + 14 confirmed findings — 52 and 28 bypass probes respectively — all
  fixed, ruled, or documented, with zero ratified-corpus regressions), and
  **registered at `contract-v1.37`**.
- [add-substantive-review-lane](openspec/changes/add-substantive-review-lane/proposal.md)
  — proposed 2026-08-15, **RATIFIED 2026-08-22** by Brett Heap (in-session
  via question prompts; record
  `openspec/changes/add-substantive-review-lane/review/ratification-2026-08-22.md`):
  generalizes codexFactory's proven
  `gate_rules_council` + `merge_readiness_council` + Merge Master machinery
  (live autonomous deliberation 2026-08-14, xFactory PRs #85/#100) beyond its
  one rules-as-code candidate class (`doc-health-nightly`,
  `docs_only_path_overflow`) into a named substantive review lane: councils
  judge, Merge Master stays the mechanical enforcer; every seat's rationale,
  a signed identity-bound check-run, and an audit artifact make review
  accountable; reviewer/enforcer identity stays separate from the PR
  author's; the envelope fails closed outside a defined candidate class or a
  non-unanimous verdict. MODIFIES `roles-authority-model` (ten ADDED
  requirements). Pilot: `opensoft/openxFactory` reviewed by codexFactory's
  councils. **All five questions the proposal declared open on 2026-08-15
  were RULED by Brett Heap in-session 2026-08-22 and encoded** (proposal
  "Decided questions"; four new requirements plus a rewritten pilot
  requirement): rollout order DEFERRED to a named follow-up change on pilot
  evidence, but the bar (≥3 council-cleared substantive PRs across ≥2
  candidate classes, zero enforcer incidents, one completed gate-rules
  review cycle) and the ordering principle (engineering-owned repos before
  domain repos) are decided now; persona home — codexFactory's councils
  review substantive PRs in EVERY governed repo, zero new persona homes
  (Brett overrode the recommended two-axis split); company-policy-lead seat
  rules-council-only BY DEFAULT with a bounded per-class pull-in a candidate
  class may declare, defined by the gate-rules council at class-definition
  time and fail-closed for those classes (Brett's third option, superseding
  design.md Decision D in part); ruleset shape — the proven shape everywhere
  (real `APPROVE` review satisfies required review; the council-verdict
  check-run is transport only and never a satisfier; human review always
  available, no App-path-only repo); and risk tiers — the constitutional
  floor is ruled now (the ratified never-clearable floor is tier-independent
  and unoverridable by unanimity; contract bytes, gate/workflow definitions,
  credential surfaces, and security posture are permanently human-only;
  autonomous clearance only ever for docs-/derived-artifact-shaped blast
  radii) with the enumerated tier vocabulary DEFERRED to the same
  evidence-driven follow-up path. The ratification read (also 2026-08-22, a
  distinct act from the clarify round) ruled four further items: the FORM
  ELEVATION of Q1's bar and Q5's floor from proposal text into promoted
  requirements is ACCEPTED; the Q1 bar counts ANY council-cleared verdict,
  App-approved or human-approved, because it measures council quality rather
  than enforcer autonomy (overriding the encoder's autonomous-only reading);
  the ordering principle stays ABSOLUTE, the dormant-engineering-repo
  consequence accepted, with escalation to Brett inside a future adoption
  change as the escape path rather than requirement text; and RATIFY.
  `target_release: none` — no contract bytes move; realization across the
  three repos (tasks §3–§5) is now authorized, tracked-not-performed work.
- [add-wallet-carried-review-authority](openspec/changes/add-wallet-carried-review-authority/proposal.md)
  — authored 2026-08-22, RESTRUCTURED 2026-08-23 on the convener's ruling after
  council review, and **RATIFIED 2026-08-23** (Brett Heap, in-session — the
  same mechanism that ratified `add-substantive-review-lane` the day before).
  The proposal carries the ruling record verbatim: ratified as restructured
  (PART I doctrine, PART II substrate, PART III the declined floor), all four
  lead constructions confirmed and each overturnable by a later ruling, and Q8
  deferred to S5's design; Q9 and Q10 stay open as carried items because they
  amend `add-substantive-review-lane`'s text rather than this change's. The
  successor to
  `add-substantive-review-lane`, acting on finding LS-A3 from the
  `codexfactory-routine-code-clearance` convening (the widen-only validator did
  not enforce the widenings it was given, so non-self-review cannot rest on an
  in-tree path rule alone). Circulated first as `add-assembly-plane-separation`,
  a three-repository topology; reshaped on the convener's ruling that a topology
  fights the ratified single-reviewing-home model, whereas wallet-carried
  authority travels to any repository without restructuring it. **The doctrine:**
  review authority is held as an `openxwallet` grant and by nothing else —
  spec authority and code authority as two grant scopes, a general refusal-only
  non-self-review rule, ownership conferring nothing, and the three-repository
  layout demoted to a project schema a human (`PA`) elects and that confers
  nothing. **The substrate, named with nothing pretended** after three council
  seats independently found the proposal treating described controls as existing
  ones: S1 wires `validate-openxwallet` into CI (REQUIRED since
  2026-08-26 by org ruleset 21538893 — see "Wallet validation gate" above; the
  "advisory until an operator marks it required" reading was true at authoring,
  when the validator ran in no workflow at all and no grant was operative, and
  is STALE from 2026-08-26, corrected here by `split-openxwallet-repo` P3); S2
  anchors the issuer (root
  issuer = the responsible operator, standing under the Human Escalation
  Contract, no wallet needed); S3 records the exercise at verdict conformance in
  the Hermes runtime (audit-trail-evidenced exercise REJECTED — it records
  `unauthenticated_request`/`unattributed` and confers nothing checkable); S4
  lands the register and its reader TOGETHER as a ratification condition, at a
  one-file/one-holder MVP, declared permanently human-only; S5 reconciles
  revocation with the runtime's admission stamp and pins composition so a
  provider alias roll is a governed re-issuance, not a silent fleet-wide
  revocation. **The narrowed floor amendment is DECLINED** — digest-disjointness
  measures byte identity and is anti-correlated with independence; the
  constitutional floor stands whole and assembly-class surfaces stay permanently
  human-only. This change ends no `--admin` merge directly and says so in its
  Why: it is a PRECONDITION. `review-authority-intake` (12 ADDED) plus
  `roles-authority-model` (2 ADDED, 1 MODIFIED declared relative to
  `add-substantive-review-lane`'s outcome per `release-realization:64-74`).
  `target_release: implemented` — no contract bytes move; S1–S5 are named
  successors, each carrying its OWN `code_surface` and archiving on its own
  merged, green evidence, so this change's own ledger does not tick from a
  successor's landing. **Successors landed so far** (Speckit features in this
  repository): S1 as `010-wallet-validator-ci` (PR #275, 2026-08-23) —
  `.github/workflows/wallet-validation.yml` ran
  `scripts/wallet-yaml-syntax-gate.py` and `scripts/validate-openxwallet.py`
  on every pull request to `main`; since `contract-v2.0` that workflow is
  `.github/workflows/openxwallet-consumer-gate.yml` (same job id, so the same
  required token) and both readers come from the `openXwallet` pin — the
  Speckit feature directory left the repository with the carve and its record is
  the archived one; S2 as `012-wallet-issuer-anchor` (PR #299, 2026-08-24),
  likewise carried to `opensoft/openXwallet`; the first-wallet cold start as `013-first-wallet` (PR #308,
  2026-08-25); and S4 as `014-register-and-reader` (PR #341, 2026-08-25),
  landing `governance/review-authority/register.yaml` at the ruled
  one-row MVP together with its reader. S3 (`[hermes-install]`) and S5 remain
  outstanding.
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



- [add-hermes-customer-subject-runtime-contract](openspec/changes/archive/2026-08-27-add-hermes-customer-subject-runtime-contract/proposal.md)
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

- [fix-content-resolution-conflation](openspec/changes/archive/2026-08-29-fix-content-resolution-conflation/proposal.md)
  — **ARCHIVED on merged-plus-green PLUS THE CUT**, which is the gate its own
  `target_release` field named at filing and the reason it was split from its
  sibling. Pull request #490 merged 2026-08-29T02:26:14Z as merge commit
  `571e64d5540cbe6240cfb068ef137778e53611f8`, re-verified at this act an
  ancestor of `origin/main` (`git merge-base --is-ancestor`, exit 0) and a real
  two-parent merge (`3cebf83e` + `b57874f3`) read out of `git cat-file -p`
  rather than off the pull request page; the sibling's merge `8690ec29` is an
  ancestor of it, so the order Brett directed is legible in the graph. Green on
  the final head `b57874f3`, all four checks from the check-runs API:
  `pytest-suite` **selected 7704, passed 7683, skipped 21, 0 failures, 0
  errors** (run 33228174754, counts read out of the job log), plus
  `wallet-validation`, `merge-master-approval` and
  `copilot-pull-request-reviewer`. **THE CUT IS `contract-v2.1` AND ALL FOUR
  SURFACES AGREE**, re-read at the archive rather than quoted from the
  realization: `contracts/manifest.yaml:3` reads `contract-v2.1`, the changelog
  opens with the `contract-v2.1 — 2026-08-28 (additive)` section, the digest
  inventory `contracts/releases/contract-v2.1.digests.yaml` carries **192**
  entries — the same count as `contract-v2.0`, the additive class showing in
  the membership rather than being asserted — and both moved members carry new
  digests equal to the tree's own `sha256sum`: `release.py` `660e55ca…` →
  `bb845d70…`, `content.py` `bad04c65…` → `509ad91b…`. The tag is ANNOTATED and
  on the merge (`tag e2a1fcc4` over commit `571e64d5`), `verify-tag --remote
  origin --tag contract-v2.1` re-run here reports `pass`, **exit 0**, and
  doc-health's `release-inventory-drift` family reports **no findings**. The one
  command that no longer passes is reported rather than omitted:
  `verify-promotion` now exits 1 with `HGR-RELEASE-TAG-EXISTS`, which is the
  PRE-tag gate refusing a tag that exists — it passed in the window before the
  tag was cut, and `verify-tag` is the post-tag proof. **PROMOTION PROVED BY
  DIGEST, PER REQUIREMENT**: `shared-contract-ownership` goes **10 → 12
  requirements**, **39 → 46 scenarios**, 373 → 506 lines, `git diff --stat`
  **+133 / −0**. Every `### Requirement:` block was hashed either side of the
  act and the two sets compared: **0 removed, 2 added, 0 changed bytes, 10 of
  10 pre-existing byte-identical**. The two promoted blocks are the delta's own
  bodies byte-for-byte — `sha256:3f20ecb4…` (5782 bytes, 4 scenarios, the
  distinction) and `sha256:7c7f4d3f…` (3278 bytes, 3 scenarios, the executable
  proofs) — the same digests computed from `specs/shared-contract-ownership/
  spec.md` in the archived folder, so zero deletions is a measured fact about
  all ten untouched requirements rather than an inference from a diff stat.
  `.openspec.yaml` MOVED with the packet under openspec 1.2.0, checked by blob
  id rather than by presence: `aa517729`, unchanged. No header move was owed —
  the packet already read `Status: ratified` with a citation clearing the record
  spelling's three-way floor, all six orchestrator decisions cleared and all
  four questions ruled 2026-08-28. All four § 7 follow-ups stay OPEN with an
  archive-time disposition each, none ticked, because the archive performed
  none of them.
- [fix-pin-value-boundary-and-sentinel-split](openspec/changes/archive/2026-08-29-fix-pin-value-boundary-and-sentinel-split/proposal.md)
  — **ARCHIVED on merged-plus-green ALONE**, and that it could is the whole
  argument of OD-1: this packet touches no contract inventory member, so it
  never had to wait on its sibling's human-gated tag. Pull request #478 merged
  2026-08-28T11:33:42Z as merge commit
  `8690ec297e9bbe276e77cc61262b71913f443087`, re-verified at this act an
  ancestor of `origin/main` (exit 0) and a real two-parent merge (`31344941` +
  `0529fb4a`) read out of `git cat-file -p`. Green on the final head
  `0529fb4a`: `pytest-suite` **selected 7650, passed 7629, skipped 21, 0
  failures, 0 errors** (run 33165708443, counts read out of the job log), plus
  `wallet-validation`, `merge-master-approval` and
  `copilot-pull-request-reviewer`. **THE PIN CLASS REPORTS `clean` AND ONE
  NUMBER MOVED, FOR A CAUSE THAT IS NAMED RATHER THAN ROUNDED AWAY**:
  `scripts/doc_health/pin_class.py` exits 0 and reads **67 declared pin sites
  across 23 class members — 51 reachable, 0 orphaned, 1 lost (declared
  unrecoverable, 0 awaiting a superseding record), 0 inconclusive; 0 uncovered,
  0 vanished, 0 arrived; 7 legal non-pins, 0 undeclared non-commit values, 3
  recognized legacy absences, 0 unused vocabulary members**. Against the
  realization's **66 sites / 50 reachable**, two counts moved and thirteen did
  not, and the move is not this packet's: the sixty-seventh site is
  `openspec/changes/add-worker-enrollment-broker/supporting-docs/manifest.yaml:21`,
  added by `21bc40ac` in pull request #489, pinning `93f883f4` and reachable —
  proven by `git ls-tree` at both commits and `git log --diff-filter=A`, not
  asserted. Every full promotion writes a supporting-docs manifest and a
  manifest is a pin site. The corpus sweep behind the packet's zero was re-run
  too: **1124 scan-suffix files, 184 read after non-member exclusion, and 0
  values of 41 or more hexadecimal characters under any vocabulary key** — the
  one number that must not move, and it did not. **NO CONTRACT TAG OWED,
  re-affirmed at the archive by PARSE against the bundle as it stands today**
  rather than as it stood at filing, which matters because the bundle MOVED to
  `contract-v2.1` under this packet's own sibling: the inventory's 192 entries
  were walked and not one path under `scripts/doc_health/`,
  `scripts/ideation_dashboard/` or `experiments/` appears in it.
  **PROMOTION PROVED BY DIGEST**: `doc-health` goes **39 → 40 requirements**,
  **181 → 185 scenarios**, 2127 → 2208 lines, `git diff --stat` **+81 / −0**,
  with **0 requirements removed, 1 added, 0 changed bytes and 39 of 39
  pre-existing byte-identical** under a per-block sha256 set comparison taken
  either side of the act. The promoted block is the delta's own 5953-byte /
  4-scenario body under `sha256:5d364da4…`, byte-for-byte. `.openspec.yaml`
  MOVED with the packet, checked by blob id: `cef67a9b`, unchanged. No header
  move was owed — `Status: ratified` with a citation was already in place, all
  five orchestrator decisions cleared and all four questions ruled 2026-08-28.
  All five § 6 follow-ups stay OPEN with an archive-time disposition each, and
  § 6.5's stale "66 sites" is corrected to 67 in place rather than left to age.
- [declare-generated-projection-status](openspec/changes/archive/2026-08-29-declare-generated-projection-status/proposal.md)
  — **ARCHIVED on merged-plus-green**, where merged and green are ONE event: the
  realization RODE IN the proposing pull request, so the argument for the value
  and the value itself were reviewed together. Pull request #468 merged
  2026-08-28T11:25:39Z as merge commit
  `4d3f540d7a8c762e1077751b040a4839ae14e35f`, re-verified at this act an
  ancestor of `origin/main` (`git merge-base --is-ancestor`, exit 0) and a real
  two-parent merge (`c79d6e54` — the sibling packet's own merge, so the order
  Brett directed is legible in the graph — and `cb67a02d`), read out of
  `git cat-file -p` rather than off the pull request page. Green on the final
  head `cb67a02d`, all four checks from the check-runs API: `pytest-suite`
  **selected 7637, passed 7616, skipped 21, 0 failures, 0 errors** (run
  33165034882, counts read out of the job log), `wallet-validation`,
  `merge-master-approval` and `copilot-pull-request-reviewer` all pass. **THE
  PREDICTION HELD EXACTLY AND WAS RE-MEASURED RATHER THAN ASSUMED**:
  `record-immutability` reads **4 criticals** on the merged tree, and
  `ideation/cross-reference.md` is absent from them — not allowlisted, not
  suppressed, not skipped, but no longer a record, its line 3 now reading
  `Status: projection` because the generator emits it. The four that remain are
  the genuine hand-maintained records the packet named, all untouched, all still
  firing. **PROMOTION PROVED BY DIGEST**: `document-lifecycle` holds at **17
  requirements**, scenarios **77 → 79**, +18 / −3 lines, and of the 17
  requirement blocks **exactly ONE changed bytes** — `Controlled document status
  taxonomy`, the one the MODIFIED block names — the other 16 byte-identical
  under a per-block sha256 set comparison taken either side of the act. The
  promoted block is the delta's 7882-byte / 72-line body under
  `sha256:04537b7fdb210a74a35038e35cba85e02bccc21bdac68e19efb80d1a926c4e53`,
  byte-for-byte; canon's replaced text was 5912 bytes / 57 lines under
  `sha256:65dc437f12c73b48b4add97df28297313ebdbff2eba74cd2f9de8aace19b81de`.
  `.openspec.yaml` MOVED with the packet under openspec 1.2.0, checked by blob
  id rather than by eye (`6e750e85`, unchanged). **THE HEADER MOVED AT THE
  ARCHIVE**: `Status: draft` → `ratified` with a `Ratified:` line citing Brett's
  2026-08-28 merge-and-archive ruling, written before `openspec archive` ran so
  it lands in the archived copy — necessary because
  `promotion_fidelity.PRE_RATIFICATION` is `{brainstorm, staged, draft}`, so an
  archived proposal reading `draft` would have had this packet's own
  `document-lifecycle` delta discounted as design evidence. **THE ACT OWED IN
  ANOTHER REPOSITORY LANDED FIRST, AND THE ARCHIVE WAITED ON IT**: § 5.1's
  disposition entry at the AGGREGATION root, keyed `(record-immutability,
  openxFactory, ideation/cross-reference.md)` and citing this change, is present
  at aggregation commit `20aafc4b` of 2026-08-28,
  `health/dispositions.yaml:239-249` — the cited-resolution case that instrument
  exists to record, not a silencer. Verified against that repository's
  `origin/main` rather than its shared working tree, a distinction this packet's
  own § 5.1 records because the first reading got it wrong. Three further
  follow-ups archive CARRIED with
  written dispositions rather than blank boxes: the prose-only generator
  declaration (a class of one — the census reads `projection | 1`), the
  mirror-image re-class hole whose honest remedy is `--check`-mode regeneration
  in CI, and the four remaining record-immutability criticals, which are the
  append-discipline collision `govern-openspec-corpus-membership` already owns.

- [clean-doc-health-floor](openspec/changes/archive/2026-08-29-clean-doc-health-floor/proposal.md)
  — **ARCHIVED on merged-plus-green**, on the same terms and in the same act as
  its sibling above: the realization rode in the proposing pull request. Pull
  request #465 merged 2026-08-28T10:47:25Z as merge commit
  `c79d6e54cf5093d18565f06afa1c2ea6216418de`, re-verified at this act an
  ancestor of `origin/main` (`git merge-base --is-ancestor`, exit 0) and a real
  two-parent merge (`0c0075df` + `a1067f08`) read out of `git cat-file -p`.
  Green on the final head `a1067f08`, all four checks from the check-runs API:
  `pytest-suite` **selected 7629, passed 7608, skipped 21, 0 failures, 0 errors**
  (run 33159846355, counts read out of the job log), `wallet-validation`,
  `merge-master-approval` and `copilot-pull-request-reviewer` all pass. **THE
  NUMBER WORTH READING IS THE ONE THAT DID NOT MOVE.** `status-validity` went
  **4 errors → 0** on the four backfills, as the packet predicted; but
  `location-conformance` stayed at **3**, and that is the fix working rather
  than failing. The forcing document cites TWO changes — the archived
  `implement-avatar-client-lab` and the active `qualify-avatar-live-voice` — and
  the arm reported `cited[0]` off a sorted list, so the ARCHIVED id won on
  alphabetical order and HID a performable remedy behind an impossible one. The
  row is now re-pointed at the active proposal and stays an error, correctly,
  because that move CAN be performed. That corrects the commission's own stated
  expectation and is recorded as such rather than smoothed over. **PROMOTION
  PROVED BY DIGEST**: `doc-health` holds at **39 requirements**, scenarios
  **179 → 181**, +21 / −2 lines, and of the 39 requirement blocks **exactly ONE
  changed bytes** — `Proposal supporting-document integrity checks`, the one the
  MODIFIED block names — the other 38 byte-identical under a per-block sha256
  set comparison taken either side of the act. The promoted block is the delta's
  2628-byte / 42-line body under
  `sha256:81267524a00f7ae9582347067687959a445997cc11bab3f07947067b7e2591b2`,
  byte-for-byte; canon's replaced text was the 1390-byte / 23-line block under
  `sha256:b0e1bc81916bd8ed865565544021670aeb0089fffa7e1955dd153edf0416081c`, the
  one that pinned "active or archived" twice. `.openspec.yaml` MOVED with the
  packet under openspec 1.2.0, checked by blob id (`fa04b8a7`, unchanged since
  the PR #465 amendment that corrected its `approved_by` narrative). **THE
  HEADER MOVED AT THE ARCHIVE**, as § 6.3 said whoever performed it would owe:
  `Status: draft` → `ratified` with a `Ratified:` line citing Brett's 2026-08-28
  merge-and-archive ruling, for the defect § 6.3 measured from the other end —
  an archived `draft` has its deltas discounted, which would have silently
  dropped this packet's own MODIFIED block, the very failure § 1.4 measured
  against somebody ELSE's archived record. The `modified-block-currency`
  SELF-GATE row this packet added on filing was REMOVED by the same act, on the
  retirement condition the row itself stated, and its sibling's row with it —
  the carriage-ledger population 9 → 7 with no other subject moving. Two
  follow-ups archive CARRIED with written dispositions: the staged-exit arm
  still reports only `cited[0]` where two ACTIVE changes are cited (Q1 — a count
  change owing its own cross-repository before/after), and a staged fragment
  whose every cited exit has archived is now reported by nothing (Q2 — a real
  lifecycle gap, now a property of canon, whose plausible owner is
  `staged-candidate-aging`).

- [add-unclassified-finding-class](openspec/changes/archive/2026-08-28-add-unclassified-finding-class/proposal.md)
  — **ARCHIVED 2026-08-28** on the merge-plus-green rule the packet declared, and
  on TWO merges rather than one, this packet having been amended mid-flight.
  Realization pull request #466 merged as squash `db2442ce` (Speckit
  `026-unplaced-finding-drift`), preceded by the DELTA AMENDMENT pull request
  #461, squash `6d100e51` — both re-verified at this act as ancestors of
  `origin/main` (`git merge-base --is-ancestor`, exit 0 on each) rather than read
  off a pull-request page. The amendment had to land FIRST, the realization's
  spec citing the amended text. **RATIFIED 2026-08-27** (in-session
  commissioning, verbatim "Amend now"), **AMENDED 2026-08-28 by Brett**
  (in-session, verbatim "Amend: shape = arm template, all interpolations masked"
  — D3's shape-identity rule widened from quoted-spans-plus-digits to every
  interpolated field, after Speckit 026 measured SIX `warning` rows for ONE
  remedy on the real tree; `specs/026-unplaced-finding-drift/plan.md` § OPEN-1).
  **THE GATE NUMBERS**, base `db2442ce`, before → after the act:
  `pytest tests/doc-health` **1270 → 1270 passed, 0 failed**, no test falling due
  and none re-aimed; `openspec validate --all --strict` **76 → 75 passed, 0
  failed** (24 active + 52 specs → 23 + 52, **−1** exactly as promotion of one
  change predicts); `doc-health --single-repo .` **byte-identical at 5 critical,
  11 error, 41 warning, 11 info, 0 new regressions**, moving **+0 `warning` / +7
  `info`** against `--skip-family modified-block-currency` in both readings,
  equal to the family's own counts. Promotion is a **PURE APPEND**: canon 38 → 39
  requirements and 173 → 179 scenarios, `git diff --stat` **73 insertions(+), 0
  deletions(-)**, the remainder byte-identical at **139505 == 139505** raw and
  canon before a strict byte PREFIX of canon after — the strongest reading a
  promotion admits, and one a `MODIFIED` block could never offer. The whole
  report diff across the act is THREE lines and none is a finding — canon words
  218169 → 219088 (+919), the SAME +919 in governance words as those words move
  from active-change prose into promoted prose, canon share 31.6% → 31.7%, and
  the promoted-specs row — an ADDED-only packet having drawn no self-finding to
  depart, which is where this act differs from its sibling
  `add-modified-block-currency-check`, whose archive re-aimed five tests and
  retired one. **THE FIFTH CLASS READ ZERO ON THE DAY IT SHIPPED, AND THAT IS THE
  WHOLE OF ITS EVIDENCE**: the family's block renders `unplaced-finding drift: 0`
  and the residual row does not render at all. Substantively —
  the modified-block-currency family's report block
  already detects that its own class map has drifted from its arms, and then
  says so in PROSE: the `unclassified` residual row carries no severity, is not
  a finding, and is therefore reached by neither `--fail-on` nor the ranked plan
  that "Health report contract" requires every finding to appear in. One ADDED
  requirement on `doc-health` makes an unplaced rule text emit one `warning`
  **per distinct rule SHAPE per run** — a shape being the ARM'S TEMPLATE with
  every field it interpolates masked (quoted spans, digit runs, the promoted
  spec's path, change identifiers, unit-kind lists), the mask derived from the
  arm templates themselves so it cannot drift from them — naming that shape's
  count and the first instance's
  rule text verbatim, carrying its repo and delta path, with the action line
  "extend the class map in `scripts/doc_health/modified_block_currency.py`, or
  fix the drifted rule text the finding names". Per shape rather than per run
  because two drifted shapes are two map entries to write, and per shape rather
  than per repository because the map is one module constant with one remedy.
  The finding is itself placed by the map into a FIFTH `FindingClass` (id
  `unplaced`, label `unplaced-finding drift` — neither may contain the substring
  `unclassified`, which a standing pin asserts absent from a clean summary) under
  a FOURTH severity constant `_DRIFT_SEVERITY`, so § 7.2's flip of
  `_LAUNCH_SEVERITY` cannot drag it; and its pattern is ANCHORED at the start of
  the rule text, because the finding quotes a rule text that may itself begin in
  the shape of an arm. The residual row stays; it is what makes the tally sum.
  **NO `## MODIFIED Requirements` block**, and that is a measurement rather than
  a preference: canon enumerates the three comparison ARMS and never the classes,
  the class map, or the residual, so restating 14 scenarios of "Currency of an
  active change's MODIFIED requirement blocks" would risk the defect the family
  exists to catch in order to say something canon does not say. The requirement
  BODY is deliberately lean — 36 lines, down from 70 — because every body line is
  carriage-ledger surface a future MODIFIED block must restate. Adds NO check
  family; the enumeration and its numerals are untouched. Band `warning` and the
  family stays absent from `FAMILY_RESOLUTION`, so the finding retiring when
  somebody extends the map cannot become an uncited-resolution `error`; § 7.2's
  flip is untouched and still owed. Predicted movement **zero in every band**,
  and the act measured exactly that. Realization moved the standing pins by name
  — of the EIGHT sites § 3.6 predicted would red, five actually did — added a
  behavioural fixture tree (`modified-block-currency-unplaced`; no corpus title
  can produce an unplaced rule text, measured at 20,065 fuzzed rule texts and 0
  unplaceable, so the honest trigger is a REMOVED map pattern rather than a
  crafted title), and AMENDED the byte-level report contract
  `specs/022-modified-block-currency-reporting/contracts/report-section.md`,
  which enumerated the four classes four times over.
  Group 2 is ticked against #466, EIGHT of its fifteen boxes carrying a
  `RECONCILED` clause rather than a silent tick: § 2.4, § 2.6 and § 2.14 moved by
  the amendment, and § 2.3, § 2.7, § 2.8, § 2.10 and § 2.15 by defects in the
  packet that realization found and recorded as plan decisions O3–O8 — the
  three-versus-four test files, the eight predicted reds that were five, the
  function rename the pin roster did not ask for, F2's provenance checker that
  would not have covered the new tree, the mutant no value comparison can kill,
  and an unforeseen allowlist pin. § 4 stays OPEN as authored — § 4.2's first
  nightly with this emit present is the measurement no archive act can supply,
  the population being empty on this tree and unmeasured everywhere else — and
  § 1.2's veto flag on the three orchestrator decisions stays open with it,
  not-vetoed being neither vetoed nor ruled. `add-modified-block-currency-check`
  § 7.2's flip of the scenario-title arm to `error` is untouched and still owed;
  `_DRIFT_SEVERITY` exists so that flip cannot drag this class with it.

- [declare-sentinel-pin-vocabulary](openspec/changes/archive/2026-08-28-declare-sentinel-pin-vocabulary/proposal.md)
  — **ARCHIVED 2026-08-28** on merged-plus-green. Pull request #457 merged
  2026-08-28T04:57:04Z as merge commit
  `157e423dfb62b1405d87b49f9681d729526a7c42`, re-verified at this act an ancestor
  of `origin/main` (`git merge-base --is-ancestor`, exit 0) and a real two-parent
  merge (`52999f01` + `9142b5e3`) rather than a rewrite — read out of git rather
  than off the pull request page, which is worth the check in a packet whose
  sibling capability declares a pin an orphaning rewrite destroyed. Green on the
  final head `9142b5e3`: `pytest-suite` **selected 7524, passed 7503, skipped 21,
  0 failures, 0 errors** in 15m16s (run 98756219935, counts read out of the job
  log), `wallet-validation`, `merge-master-approval` and
  `copilot-pull-request-reviewer` all pass, read from the check-runs API here.
  **THE UNGOVERNED HALF OF A PIN IS NOW READ.** Before this, a value that was
  honestly not a commit — content from a working tree nobody committed, a
  derivation performed outside any repository, a revision that could not be read
  — produced **no site at all**: `pin_class.py` bound both site regexes' value
  group to `([0-9a-f]{40})`, so seven committed sentinels were not reachable, not
  orphaned, not lost, and **not uncovered**, and the class reported itself fully
  verified over artifacts whose central provenance claim nothing had ever read.
  The delivered surface: a registry module `scripts/doc_health/pin_sentinels.py`
  beside the pin class — five conditions, five members, each stating its
  condition, its standing and its measured emitters, with absence declared a
  RECOGNIZED LEGACY STATE and refused membership; a **separate** classification
  pass in `pin_class.py` whose `_field_re` and `_VOCAB_RE` are byte-unchanged and
  whose wide regexes skip anything commit-shaped, so no site can be classified
  twice and no reachability verdict is reachable through the new code; a
  `status --porcelain` dirty-tree sentinel branch in `git_generation()` **scoped
  to the corpus pathspecs** (`:(glob)` magic load-bearing — git's default `*`
  crosses `/`, and a whole-tree check would throw away a true pin over an
  unrelated open file); the three drifted `proposal-support.py` guards reconciled
  against the declaration, closing the latent `SupportError` the proposal
  measured; and 33 new tests, with the 53 in `test_pin_reachability.py` green and
  **not one line edited**. **THE SEVEN COMMITTED SENTINELS MOVED FROM INVISIBLE
  TO LEGAL NON-PINS AND NOT ONE MANIFEST BYTE WAS TOUCHED** — the fifth outcome
  does NOT hold full verification open, because an artifact making an honest
  claim about content nobody can reconstruct is conforming. The probe at the
  merge commit, **identical before and after the packet moved**: 66 declared pin
  sites across 23 class members — 50 reachable, 0 orphaned, 1 lost (declared
  unrecoverable, 0 awaiting a superseding record), 0 inconclusive, 0 uncovered, 0
  vanished, 0 future members now carrying pins; **7 legal non-pins, 0 undeclared
  non-commit values, 3 recognized legacy absences, 0 unused vocabulary members**.
  That the move changed nothing was CHECKED rather than assumed, on the hazard
  `supersede-lost-pin-baseline` met: `pin_sentinels.py` and `pin_class.py` were
  read for packet-path references first, and they name this change only in prose
  and comments — the packet's own `.openspec.yaml` is a declared NON-MEMBER under
  a live-plus-archive glob pair, so the move crosses from one arm to the other.
  **TWO CARRIED DECISIONS WERE TAKEN BY MEASUREMENT, NOT BY PREFERENCE.**
  `"unknown"` is its OWN condition (`unestablished-revision`, the weakest member)
  rather than a second spelling of `"uncommitted"`'s: the same-condition rule
  folds two spellings only where measurement shows one condition, and its three
  emitters showed three — an index entry whose recorded revision is absent, an
  unreadable `HEAD`, and a readable repository whose named content was never
  committed. Folding it would have made every artifact carrying it assert
  something false at two of the three. The call-site split is follow-up § 5.6.
  And `"composed"` is declared with the qualified `composed:<repo>@<ref>:<sha>,…`
  prefix its emitter actually writes, because declaring only the bare spelling
  would have left the lane's real output undeclared — precisely what Q3's seeding
  ruling forbids. **ONE DIVERGENCE ARCHIVES STANDING, FLAGGED RATHER THAN
  HIDDEN**: `repo_revision()` was deliberately NOT given a dirty-tree branch. It
  has no untrue pin to repair — it compares every source file's sha256 against
  the committed blob at the revision it stamped and RAISES rather than writing a
  manifest its content contradicts, so it satisfies the generator obligation BY
  REFUSING — and adding the branch would loosen a live guard no ruling asked to
  loosen. Brett was shown that flag on 2026-08-28 and pre-authorized the
  merge-plus-archive sequence with it standing; it is recorded as a standing
  divergence-by-measurement at `tasks.md` § 2.7 and § 4.6, not as an oversight.
  **PROMOTION PROVED BY DIGEST, per capability**: `ideation-cross-reference`
  **16 → 18 requirements, 48 → 57 scenarios**, +152 / −0 lines, delta body and
  canon block both 151 lines / 11012 bytes under
  `sha256:57fd47c62234482e0231a3609df924ed09da46ec2eacf454360c76da58f2b543`;
  `doc-health` **36 → 38 requirements, 163 → 173 scenarios**, +176 / −0 lines,
  both 175 lines / 12632 bytes under
  `sha256:8334a943694ccc17dd1042dc1eb4e8575cdadd540e6c0a7bb74c88a088f44634`. Zero
  deletions in both, proved rather than eyeballed — the pre-existing file is a
  byte-exact PREFIX of the promoted one (`cmp -n 28159` and `cmp -n 126872`
  clean) — and zero `## MODIFIED Requirements` blocks in either delta, so no
  archive-order question arises and the sibling `add-nightly-dashboard-refresh`
  block on `doc-health` is untouched. Both archived deltas are byte-identical to
  the authored files. `.openspec.yaml` MOVED with the packet under openspec 1.2.0
  (checked by blob id anyway: `24ba794e`, unchanged from ratification), so origin
  retention holds through the archive. `openspec validate --all --strict` 78 → 77
  passed / 0 failed, `pytest tests/doc-health -q` **1249 passed** under
  `set -o pipefail` with the exit code read rather than inferred, doc-health
  families unmoved at 5 critical / 7 error / 41 warning / 11 info across the act.
  **NO CONTRACT BUNDLE OWED**, re-affirmed by parse rather than grep: all 40
  `contracts/releases/*.digests.yaml` inventories walked into 192 distinct member
  paths, none of the seven touched files among them. Adds no deterministic check
  family and does not restate the enumeration. **SIX follow-ups carried unticked
  by decision** — the `corpus.py` `head_sha()` seam feeding six lanes,
  cross-repository pins, whether `"composed"` belongs in a pin key at all, the
  unwired preflight half, the `_field_re` / `_VOCAB_RE` trailing-boundary gap
  found while measuring, and the three `"unknown"` call sites § 5.6 would split
  onto the conditions they mean. **DISCHARGES** `harden-ideation-readiness-check`
  § 5.3 and `govern-derived-pin-reachability` § 5.1, the two items Brett ruled
  were one packet.

- [split-openxwallet-repo](openspec/changes/archive/2026-08-28-split-openxwallet-repo/proposal.md)
  — **ARCHIVED 2026-08-28** on merged-plus-green realization evidence across SIX
  repositories, which is what a `code_surface` spanning six of them and
  `target_release: implemented` obliged: this change could never archive on
  landing. Authored 2026-08-26 as the first and only exit of the staged topic
  `openxwallet-neutral-home` and **RATIFIED 2026-08-26** (in-session ruling on PR
  #391, both required checks green) on Brett Heap's R1–R8 rulings of the same
  day, carried as LOCKED constraints rather than re-litigated (verbatim: "approve
  R1-R8 as recommended, stage the topic and propose"); registered as DTN-026,
  which advances to `adopted` at this act. **The wallet's contracts ARE a
  product, filed as features of a factory layer** — so the product gets its own
  repository and openxFactory keeps the seam. R1 the repo and brand are
  `opensoft/openXwallet` on the house `openX<type>` form; R2 machine keys FROZEN
  in v1, because a rename in the same change as the move is unbisectable; R3 the
  new repo owns the wallet's own standard while openxFactory keeps
  `governance/review-authority/`, Speckit 013/014 and the trust-anchor /
  identity-brokering / roles-authority-model compositions; R4 the pin is
  bidirectional and acyclic (openXwallet vendors exactly one openxFactory
  artifact, `contracts/schemas/hermes-job-envelope.schema.yaml`, because
  validator rule (g) reads it); R5 a root-level `openXwallet/` submodule in the
  aggregation; R6 the register stays and its READER travels; R7 descendant casing
  is `<Domainx><Product>`; R8 `LedgerxWallet` is first. Alignment review raised 30
  findings across two reviewers (all MISMATCH / DRIFT / GAP applied) and the
  council returned 14 verdicts — **all VALID, none DISMISSED** — plus 8
  NOTED-class constraints carried into `clarifications.md`; all five review
  records travel in the packet.
  **The wave, in merge order.** P5a.1 LedgerxFactory **#25** (`e2cedb68`, the
  wallet validator resolved through three ordered candidates, landing before the
  carve because `validate_wallet_estate.py::find_openxfactory()` fails loudly
  rather than skipping) → P2 openXwallet **#1** (`936ceb20`, tagged
  **`wallet-v1.0`**, the carve out of the NAMED CARVE COMMIT
  `30565e48ffe3d8a9773e10af33425701845e10f6`) → P2b openXwallet **#2**
  (`63f5a1ad`, **`wallet-v1.1`** — the nested-repository sweep prune and the
  register-read note, and the tag openxFactory actually pins) → P2.5 openxFactory
  **#417** (`af7ac0fa`, **`contract-v1.47`**, **renumbered from the proposed
  v1.46 at merge order**: the eight `relocating:` manifest rows, the CHANGELOG
  migration note and the WARN-tier emitter, since the cut is a MAJOR and owes a
  preceding deprecation minor whose marker is MANIFEST-carried and never
  validator-carried) → P5a.2 LedgerxFactory **#29** (`e09902d7`, pinning that
  deprecation minor and observing its relocating rows) → P3 openxFactory **#431**
  (`c9a1500e1a960be827cd714d8024d9aacb40aeb2`, **`contract-v2.0`** — the atomic
  consume-and-shed, atomic because `scripts/validate-trust-anchor.py` hard-exits
  without the custody registry) with P3b codexFactory **#117** (`58bd3cf7`,
  widening the merge-gate floor to `contracts/openxwallet-pin.yaml` and the
  `openXwallet` gitlink, because `matching_paths` is exact set membership and the
  pin is what determines WHICH READER RUNS; ratified in codexFactory #118) and P4
  xFactory **#161** (`0893f0db`, the root-level submodule at the D11
  gitlink-parity floor) → P5b LedgerxFactory **#30** (`b1312869`) and OpsxFactory
  **#129** (`f63c7cd2`) → P4b openxFactory **#440** (`86212300`, root-level
  governed-repo recognition by allowlist and the aggregation parity lane) → P6,
  ratified in openxFactory **#449** as `create-ledgerxwallet-overlay-boundary`
  and realized as **LedgerxWallet**: repository created 2026-08-28, ruleset
  **21701436** requiring `pin-validation` and ACTIVE, PR #1 merged as
  `0a0141cafc1fecd5d0e38b14e4f40a67a54a08d3` and tagged **`lxw-v1.0`**, consumed
  by LedgerxFactory **#31** (`38743cf3`) and ticked with its evidence in
  openxFactory **#454** → P7, this archive.
  **Green.** P3's post-rebase head `746fe3f9` reported `wallet-validation` run
  **33115267228** (24s) and `pytest-suite` run **33115267254** (14m39s), with the
  pinned counts read out of run **33111235491**: `selected=7090 passed=7070
  skipped=20 failures=0 errors=0`. P2 and P2b are green on both openXwallet
  checks (runs 33024308629 / 33024308567 and 33035937510 / 33035937545), P2.5 on
  runs 33086366248 / 33086366020, P4b on 33126031126 / 33126031118, P4 on
  `validate` run **33117801366** plus `merge-master-approval`, P3b on `validate`,
  `merge-master-approval` and `sonar`, and P6's LedgerxWallet on `pin-validation`
  run **33137519688**. LedgerxFactory runs no CI gate beyond the Copilot
  reviewer, so its estate evidence is the recorded `validate_wallet_estate.py`
  output rather than a check run. **THE LIVE REQUIRED CHECK SURVIVED BY ALIAS,
  NOT BY REPOINT**: `openxwallet-consumer-gate.yml` keeps `jobs:
  wallet-validation:`, ruleset 21538893 re-fetched at this act still requires the
  same two tokens it required before the wave, and **no ruleset edit occurred
  anywhere in the wave** — no operator act ever stood between P3 and merge. That
  the aliased gate can still FAIL was proved rather than assumed: PR **#432**,
  opened RED-PROOF ONLY and closed unmerged by design, drove `wallet-validation`
  red in 21s on run **33109857156** with `[register-row-malformed]`.
  **The first release is a byte-identical pure move, proved before the tag.** The
  completeness diff of the two sorted listings was EMPTY at **100 files** over 26
  carried commits; byte identity ran **8/8** three-way against the carve commit's
  manifest rows, EMPTY on every floored path, **100/100** at the carve layer and
  **97/100** after the scaffold, the three exceptions declared in advance (the
  two promoted specs and `wallet-validation.yml`). P3 then shed **92 files** —
  the carve's 100 minus the 8 that stay — and the post-merge re-verify printed
  `OK openxwallet-pin verified: openXwallet@63f5a1adac89f017e70bab9a4ffe7cf02d6e6705
  (tag label wallet-v1.1), gitlink read from HEAD, 8 digest(s) recomputed`, with
  `contracts/releases/contract-v1.47.digests.yaml` carrying 192 members.
  **THIS IS THE CORPUS'S FIRST `## REMOVED Requirements` PROMOTION.** The
  promoted capability directories `openspec/specs/openxwallet/` (8 requirements)
  and `openspec/specs/openxwallet-agent-profile/` (3) are DELETED from the
  corpus — the house's first capability exit, not a supersession in place. All
  eleven titles are named verbatim in the deltas because
  `scripts/doc_health/promotion_fidelity.py` keys on (capability, normalized
  title). Their successor is openXwallet's own openspec, and it is recorded in
  three places so that no reader of any one surface is left holding a dangling
  capability: the REMOVED deltas' Migration lines, `contracts/openxwallet-pin.yaml`,
  and `contracts/README.md` with `CHANGELOG.md`. Against those two exits, two
  capabilities PROMOTE to `openspec/specs/`: `domain-descendant-boundary` (five
  requirements — how a domain consumes a neutral `open*` product through a
  `<Domainx><Product>` descendant that pins by commit TWICE, carries profile and
  never forks, sits at one of two placements whose differing STANDING is stated
  rather than blended, and is created lazily on its first profile artifact) and
  `neutral-product-pin` (nine — how openxFactory consumes an external neutral
  product, a direction it had never consumed in: the ratified
  `pinned_contract_manifest` grammar reused unchanged, fail-closed on an
  uninitialized submodule or a digest disagreement, the PINNED reader at the
  PINNED digest as what a required check runs, a pinned validator invoked with no
  scan target REFUSING rather than self-testing, and the declared pin living at
  `contracts/<product>-pin.yaml` rather than `stack.yaml`). The MODIFIED
  `shared-contract-ownership` delta applied to its promoted spec, one requirement
  modified — the third case, where openxFactory is the CONSUMER.
  **Two MODIFIED deltas were HELD BACK from the apply** and travel into the
  archived packet unapplied: `trust-anchor`, whose target capability lives in the
  ACTIVE change `add-trust-anchor`, and `review-authority-intake`, whose target
  lives in the ACTIVE `add-wallet-carried-review-authority`. The CLI refuses a
  MODIFIED delta whose target capability is not yet in `openspec/specs/`, so
  applying either here would have written a requirement into a capability the
  corpus does not hold. That is the ordered-delta rule
  (`openspec/specs/release-realization/spec.md:64-79`) applied by parity, exactly
  as the proposal declared it would be, and the pending application is recorded
  on each active change's own `tasks.md` so the obligation lands with whichever
  of the two archives first rather than resting on memory.
  **Successors registered**, named here in one place because the README is the
  house's successor register. (1) The required-check token rename
  `wallet-validation` → `openxwallet-consumer-gate`: add the new check alongside
  the old, land ONE green pull request reporting under both, then drop the old —
  the alias exists precisely because the token cannot be renamed in place without
  an operator act, so the rename owes the same care. (2) The kind-prefix rename
  `xfactory_wallet_*` → `openxwallet_*`, owned by openXwallet and a wallet MAJOR,
  on Q3's dual-accept window: `wallet-v1.1` accepts either spelling and warns,
  `wallet-v2.0` refuses the old, and the window closes on consumers-migrated
  rather than on a date, the consumer set being one. (3) The stale corpus counts
  inside openXwallet — `contracts/manifest.yaml:1968-1969`'s "16 valid + 33
  intended-invalid" and `contracts/README.md:108`'s "nineteen rules", against a
  tree of 17 positives, 36 negatives and 21 rules `(a)`–`(u)` — correctable only
  AFTER `wallet-v1.0`, because correcting them inside the move would have broken
  the byte identity the tag exists to prove. (4) `openXwallet-Install` as a
  registered NAME with no repository (Q4), the runtime having zero footprint
  today and the whole arc gating successors on consumers. (5) The
  nested-descendant governed-enumeration gap: P4b widened recognition to
  root-level governed repos, but a repository nested INSIDE another governed
  repository — `LedgerxFactory/LedgerxWallet/` — is still enumerated nowhere, so
  it gets no ideation book, and the ratified openAvatar descendants sit in the
  same hole. (6) The xFactory ↔ openxFactory review-lane pin convergence
  ceremony. (7) **A prose-tagging target form for a capability that has left the
  corpus** — added at the archive itself, because the act produced it: deleting
  `openspec/specs/openxwallet/` left four `<!-- xspec:candidate target=openxwallet -->`
  markers in `ideation/staging/` with no referent, since
  `families.py::_resolve_capability` admits only an in-tree capability or an
  active change id. Measured, not predicted — a full `--single-repo` doc-health
  run before and after this archive differs by exactly those four `tag-hygiene`
  findings and nothing else of substance. They are left standing rather than
  auto-fixed: retargeting a marker to `domain-descendant-boundary` or
  `neutral-product-pin` would make it name a capability the tagged prose is not
  about, and deleting the markers would drop four blocks out of the conversion
  queue silently. The grammar needs a form that can name a capability now living
  in a pinned neutral product, which is a change and not an edit. Same class as
  (5), one layer down: the corpus's first capability exit found two places where
  the tooling assumes every referent is in-tree. Beyond those seven,
  `MedxWallet`, `codexWallet`, `OpsxWallet` and
  `AdxWallet` each arrive lazily on their own domain's first profile artifact,
  and the review-authority register is promoted as a wallet primitive only if Q1
  resolves that way AND a second consumer of authority registers exists.

- [supersede-lost-pin-baseline](openspec/changes/archive/2026-08-27-supersede-lost-pin-baseline/proposal.md)
  — **ARCHIVED 2026-08-27** on merged-plus-green, where merged and green are ONE
  event: **the realization rode IN the proposing pull request**, so the record,
  the discharge mechanism and the five tests landed together and there is no
  second pull request to name. Pull request #429 merged 2026-08-27T19:26:29Z as
  merge commit `94933adf`, re-verified at this act an ancestor of `origin/main`
  (`git merge-base --is-ancestor`, exit 0) and a real two-parent merge
  (`ae6a1e7e` + `06ede5b7`) rather than a rewrite — read out of git rather than
  off the pull request page, which is worth the check in a packet whose forcing
  instance is a pin orphaned by a rewriting landing. Green on the final head
  `06ede5b7`: `pytest-suite` **6991 passed / 20 skipped / 338 deselected / 28
  subtests passed / 0 failed** in 14m37s (run 33107163953, counts read back out
  of the job log), `wallet-validation` pass, both read from the check-runs API
  here. **THE ONE THING THIS ARCHIVE COULD HAVE BROKEN IS PROVED NOT TO HAVE
  BROKEN.** The superseding record moved with its packet to
  `openspec/changes/archive/2026-08-27-supersede-lost-pin-baseline/evidence/pin-loss-supersession.yaml`,
  and the `KNOWN_LOSSES` row cites it by a LIVE-PLUS-ARCHIVE GLOB PAIR chosen
  for exactly this moment (cleared OD-1): the archive path matches the second
  glob, the record still names the pin, and the probe re-run on committed
  archive state reports **63 declared pin sites across 20 members — 49
  reachable, 0 orphaned, 1 lost (declared unrecoverable, **0 awaiting a
  superseding record**), 0 inconclusive, 0 uncovered, 0 vanished** — the same
  answer as before the move, with the `DISCHARGED:` clause now naming the
  archive path. A single-path citation would have gone dangling here; the pair is
  why it did not. **THE LOSS IS NOT SILENCED BY ITS DISCHARGE**: the row is
  untouched, the site still reports `[LOST]` with its whole measurement, and it
  is still re-measured, so the day that object turns out to be recoverable the
  declaration fails as stale. **NO BYTE OF THE SUPERSEDED ARCHIVED RECORD WAS
  TOUCHED** by the realization or by this act — zero paths under
  `openspec/changes/archive/2026-08-27-add-hermes-customer-subject-runtime-contract/`
  in either diff. One `doc-health` requirement and four scenarios reach canon
  whole: **34 → 35 requirements, 145 → 149 scenarios**, +73 / −0 lines, and the
  promotion is proved by digest rather than by eye — the pre-existing file is a
  byte-exact PREFIX of the promoted one (`cmp -n 99677` clean, so zero
  deletions and every pre-existing requirement byte-identical), and the delta's
  requirement body and canon's appended block are both 72 lines / 5434 bytes
  under
  `sha256:a595d40e7b9b321f32ce5d04c1888e54ae8bab0f4c6aa30e0a4eb4604e711c64`.
  Zero `## MODIFIED Requirements` blocks, so no archive-order question arises.
  `.openspec.yaml` MOVED with the packet under openspec 1.2.0 (checked by blob
  id anyway) and is byte-identical to the blob at the ratifying commit
  `0bbeea0a`, so the origin-retention gate passes with no restoration:
  `openspec validate --all --strict` 76 → **75 passed / 0 failed**,
  `proposal-support verify` ok before and after, `pytest tests/doc-health`
  **1183 passed / 0 failed** on both sides under `pipefail` with
  `test_pin_reachability.py` at **53 passed**, and single-repo doc-health
  identical at 5 critical / 7 error / 41 warning / 12 info with 0 new
  regressions, every family count unchanged, and `proposal-origin`,
  `promotion-fidelity`, `release-inventory-drift`, `family-enumeration` and
  `duplicate-packet` all zero — **the archive adds no finding**, `diff` over the
  two whole reports being **exactly two lines**, both canon-share arithmetic
  (31.1% → 31.2%, promoted-spec words 148998 → 149898), which is the promotion
  showing up in the corpus ratio. No contract
  bundle was owed, re-affirmed by that run's `release-inventory-drift` at zero.
  **MAIN MOVED TWICE UNDER THIS ACT** (#433, then #431) and both sets of numbers
  are kept rather than the later overwriting the earlier: at the final head with
  `origin/main` at `c9a1500e`, validate holds at 75, `tests/doc-health` reads
  **1209 passed / 0 failed** on the merged head and 1209 on `origin/main` itself
  in a second worktree — grown by twenty-six for main's reasons and by none for
  this act — and the declared class grew with main to **65 sites across 22
  members, 50 reachable, still 0 orphaned / 0 awaiting a superseding record / 0
  uncovered**, the discharge answer not having moved. **A THIRD MOVE CONFLICTED
  THE PROMOTION**: `add-modified-block-currency-check` archived on main and
  promoted into the same capability, so canon conflicted at the tail where both
  had appended. Resolved by keeping BOTH blocks in ARCHIVE ORDER — the sibling's
  first, this packet's after it — and the digest proof was RE-RUN rather than
  carried over: main's canon is a byte-exact prefix of the resolved file
  (`cmp -n 121437` clean), the appended region is still this delta's requirement
  body verbatim plus canon's trailing blank line at the SAME digest, and canon
  reads **35 → 36 requirements, 159 → 163 scenarios** against main as it now
  stands. Validate holds at **74 passed / 0 failed** and `tests/doc-health` at
  **1209 passed / 0 failed** on the resolved tree.
  **THREE FOLLOW-UPS CROSS THE ARCHIVE UNTICKED, EVERY ONE BY DECISION**, all
  three declared out of scope at authoring and none an arm of the gate: the
  undeclared 78-member evidence inventory the superseded record quantifies over
  and digests twice (a gap in the hermes-runtime evidence contract, and the
  reason ONE claim in that record can only ever be corroborated); the
  differential audit of the hermes evidence family, a sweep rather than a
  supersession; and the nightly, where nothing is enforced and the discharge
  mechanism narrows what an enforcing check would report without arguing for
  enforcing it.
  **RATIFIED 2026-08-27** (Brett, in-session commission of the filing,
  selected verbatim from a multi-choice as "Commission the superseding record
  (Recommended)"). The commission is the origin act, so
  `approved_by`/`approved_on` are recorded from it — the
  `govern-derived-pin-reachability` shape. **THE CITATION COVERS THE DECISION TO
  FILE AND NOTHING ELSE** — and a SECOND, later act on the same day disposed
  everything it did not reach. **ALL FOUR § Orchestrator decisions CLEARED AS
  AUTHORED and BOTH § Open Questions RULED, 2026-08-27**, by a four-question
  multi-choice put to Brett by the orchestrating session and relayed the same
  day; on every question he took the packet's own recommendation, so the
  clearance moved nothing. OD-1 through OD-4 cleared, none vetoed (the
  `evidence/`-homed record with its live-plus-archive glob citation, the declared
  `NON_MEMBERS` row, the spec delta riding, and the register row being the
  disposition) — and **OD-4's own named veto branch was not taken, so no
  `health/dispositions.yaml` entry is owed**. **Q1 RULED** — corroboration only:
  the record claims exactly what is provable and never recovery. **Q2 RULED** —
  no aging rule: the citation is re-resolved every run and breakage is
  self-announcing. Both rulings match the record and the code as written, so
  neither rewrote anything. The merge-then-archive sequence was approved in the
  same act and belongs to the orchestrating session. **Performs the one
  governance act
  `govern-derived-pin-reachability` uncovered and marked NEEDS BRETT** (its
  § 3.6 and § 5.5): the archived hermes provider verification pins
  `us3_baseline_commit: 66b14064…`, and that object is UNRECOVERABLE —
  re-measured on the day of filing at 0 of 573 advertised refs, `git cat-file`
  failing in the shared object store, and the server refusing
  `git fetch` with `upload-pack: not our ref`. Retention is impossible, the
  record's bytes are immutable, and **no byte of the archived record is
  touched**. Issues a superseding record
  (`evidence/pin-loss-supersession.yaml`) stating the loss, its cause (one
  rebase rewrote the whole `005-customer-subject-runtime` line six weeks before
  the retention namespace was ruled), and the verification standing the archived
  evidence retains and loses. **THE MEASUREMENT FOUND MORE THAN A HOLE**: the
  baseline STATE is reachable under a rewritten object name, `8f7c99f0…`, the
  parent of the commit that added the record — corroborated by all three
  differential counts the record itself states (catalog members 34 -> 39, schema
  entries 27 -> 32, fixture cases 79 -> 110, each re-measured at both commits) —
  and the record labels that CORROBORATION, not recovery, because the object is
  gone and tree equality is unprovable. **Restores `fully_verified` truthfully
  rather than by silencing**: the `KNOWN_LOSSES` row now cites the record, the
  verification reads committed state to find it and requires it to name the pin,
  and only a loss AWAITING its record holds full verification open — the loss
  stays declared, reported `[LOST]` with its whole measurement, and re-measured
  for ever, while deleting the row makes the site report as a failing orphan
  instead of a clean class. One ADDED `doc-health` requirement carries that rule
  into canon; no check family is added and the enumeration is untouched. The
  disposition lives in the register row rather than in
  `health/dispositions.yaml`, measured: that file exists only at the aggregation
  root and matches findings by `(family, repo, path)`, and this verification
  registers no family and emits no family finding for an entry to match.
  (code surface: openxFactory; target release: implemented)

- [add-modified-block-currency-check](openspec/changes/archive/2026-08-27-add-modified-block-currency-check/proposal.md)
  — **ARCHIVED 2026-08-27** on the merge-plus-green rule the packet declared
  (§ 8.1), after all four Speckit features landed and were re-verified ancestors
  of `origin/main` at this act with `git merge-base --is-ancestor` rather than
  read off a pull request page: F1 `19e3f6b5` (#420, the family and its three
  registrations), F2 `76a2ad27` (#426, the regression catalogue reconstructing
  #351 and #329 from history), F3 `f728d57f` (#427, the self-gate against this
  repository), F4 `4def2274` (#433, the report section and the workflow
  boundary). Gate numbers, all measured in the archive worktree at base
  `4def2274`: `pytest tests/doc-health` **1209 passed** before the act and
  **1209 passed** after; `openspec validate --all --strict` **76 → 75 items**
  (24 → 23 active, 52 specs); the single-repo doc-health run against the same run
  with `--skip-family modified-block-currency` moving **+1 `warning`, +8 `info`,
  0 `error`, 0 `critical`** before the act and **+1 `warning`, +7 `info`** after
  it, the one lost `info` being the family's own self-finding leaving the active
  set. The gated bands do not move either way, so a `--fail-on error` run is
  unaffected by construction. § 4.5's authored prediction of `+11 info` is
  HISTORY — measured at `9be81a40` over 23 blocks, re-measured at 9 then 8 as
  the corpus moved under it — and the invariant that holds is that the movement
  EQUALS the family's own per-severity counts. Canon promoted at **404
  insertions, 5 deletions** across two specifications: `doc-health` requirements
  34 → 35 and file scenarios 145 → 159, `document-lifecycle` 16 → 17 and 72 →
  77 with ZERO deletions. **"Deterministic check families" promoted 8 → 8** —
  scenario titles an identical set in identical order, seven of the eight
  byte-identical bullet for bullet, all three of canon's dated self-repair notes
  restated verbatim, and exactly SIX differences: the total `twenty-one` →
  `twenty-two`, the enumeration gaining `modified-block currency`, `Four of the
  twenty-one` → `twenty-two`, `the other seventeen families` → `eighteen`, ONE
  new body sentence declaring this family's document set, and ONE new `AND`
  bullet in `A run executes the check families` (12 → 13). Differences 1–2 are
  one canon sentence and 3–4 are another, so exactly TWO canon body units are
  not carried — **which is what the family's OWN self-finding reported against
  this packet, `2 of the 39` units, the check verifying its own block**, and the
  archive gate's independent derivation agreed with it unit for unit. The § 2.1
  ordering against `add-family-enumeration-check` was resolved by the recorded
  D5 SEQUENCING rather than by whichever archived first: that change archived
  FIRST at `f027d3b3`, so its enumeration was already canon and the block was
  written relative to CANON — and canon's requirement was proven byte-IDENTICAL
  between `f027d3b3` and this base (0 hunks), so the block reverted nothing.
  Authored and ratified 2026-08-27 (in-session, verbatim "Ratify as-is") against
  issues #357, #329 and #330, which name one mechanism: `## MODIFIED
  Requirements` replaces a requirement wholesale and `openspec validate
  --strict` reads only a delta's shape, so an active change whose block restates
  stale canon deletes whatever it did not restate, silently, on archive. Four
  instances in one week, each caught by a human — `add-doxchat-model-intake`
  (#351: six body clauses, two scenarios, one reverted line; repaired by PR
  #358) and three check families that each restated 1 of 8 scenarios of this
  very requirement (#329) — and `promotion-fidelity` cannot see the class,
  because after an archive act canon IS the delta (#330). ADDS the authoring
  obligation to `document-lifecycle` (a MODIFIED block restates the requirement
  as canon currently states it; currency is owed continuously while the change
  is active; a deliberate deletion is declared by a reserved marker) and
  doc-health's TWENTY-SECOND family, which compares active deltas to current
  canon in three arms: scenario-title completeness (the gate), a carriage ledger
  of body units and scenario bullets (`info`), and title resolution. Matching is
  same-kind and exact after whitespace normalization; containment and similarity
  are both forbidden, because canon's bullet is a SUBSTRING of the widened line
  #351 introduced. **Two-writer ordering is BY DECLARATION** (ruled the same
  day): the change that writes "relative to <sibling>" is the later writer,
  reusing `release-realization`'s existing spelling rather than adding date
  arithmetic. Advisory at launch in BOTH halves — `_LAUNCH_SEVERITY` is not
  `error` and the family is deliberately absent from `FAMILY_RESOLUTION` — and
  § 7.2's flip of the scenario-title arm is the ONE task box the archive leaves
  owed on a measured population, one finding standing (`add-composed-view-authoring`'s
  deliberate rename, named and never claimed a defect). **CLOSES #329**: its ask
  was detection, both instances are disposed, and the class is now detected
  before an archive rather than at one. **#357 IS `Refs`, NOT `Closes`, BY
  RULING** — that issue's own remedy asked for a CONTESTED-class finding, and
  this family launched ADVISORY and absent from `FAMILY_RESOLUTION` with § 7.2
  owing exactly that flip, so closing it would mark done a remedy whose stated
  form is unbuilt. **#330 was closed by hand on 2026-08-27 (16:43Z)**; § 7.1
  stands as the record of what this change did NOT build — shape 1, the post-hoc
  lost-scenario check, which needs a third measurement basis inside a family
  whose promoted requirement obliges it to declare which of TWO it measured. So
  does § 7.4 (the
  domain factories are UNMEASURED, which is why the launch is advisory) and
  #318 (§ 7.5, whose ruling recorded this packet's admission without giving the
  taxonomy an origin kind for "proposed, not approved"). The five § Orchestrator
  decisions were NOT VETOED at ratification, which is not the same as
  affirmatively ruled, so § 1.2 stays open and the flags stay where they were.
  The self-gate's own § 4.2 group fell due at this act and was disposed by the
  disposition F3 recorded for the day: two assertions RE-AIMED at the archived
  path through the family's own `parse_delta` and `derive_units` — a change of
  SUBJECT, the family excluding `openspec/changes/archive/` by construction —
  and the third, the self-finding quote, RETIRED with its dated record in its
  own docstring, nothing deleted silently and no module changed.
  (code surface: openxFactory; target release: implemented)

- [govern-derived-pin-reachability](openspec/changes/archive/2026-08-27-govern-derived-pin-reachability/proposal.md)
  — **ARCHIVED 2026-08-27** on merged-plus-green. Realization pull request #424
  merged 2026-08-27T17:51:07Z as merge commit `175682e2`, re-verified at this act
  an ancestor of `origin/main` (`git merge-base --is-ancestor`, exit 0) rather
  than read off the pull request page, and green on head `b4cd8073`:
  `pytest-suite` **6933 passed / 20 skipped / 338 deselected / 28 subtests
  passed / 0 failed** in 14m32s (run 33091394406, counts read back out of the
  job log), `wallet-validation` pass. Implementation:
  `scripts/doc_health/pin_class.py` declares the class — **25 members, 20
  current and 5 future**, six `NON_MEMBERS` exclusion rows each with a reason,
  and a `KNOWN_LOSSES` row — with `pin_class.verify()` and
  `ideation_readiness.verify_pin_reachability()` riding the existing
  readiness-proof surface. **NO DETERMINISTIC CHECK FAMILY WAS ADDED and
  `families.py` has a ZERO diff, asserted STRUCTURALLY rather than promised**,
  which is cleared OD-2 honoured beside the still-active 21 → 22 enumeration
  change. Real-repo proof at the gate: **63 pin sites across 20 members — 46
  reachable through `main`, 3 through `refs/retention/pins/<full-sha>` (and
  asserted NOT reachable from `main`, which is the intended end state rather
  than a residue), 13 cross-repository, 1 declared LOST, and 0 orphaned, 0
  uncovered, 0 vanished** — re-verified against advanced `main` `76a2ad27`
  before the merge with identical results. **A THIRD ORPHAN was found and
  RETAINED during realization**: `refs/retention/pins/74022ea5…`, a pin inside
  an archived proposal-support manifest, so the namespace now advertises three
  refs and each is at the commit its name states; the act was within the
  retention route Brett had already ruled. No contract bundle was owed, and
  that was measured by PARSING all 38 `contracts/releases/*.digests.yaml`
  inventories into their 192 inventoried paths rather than by `grep`.
  `.openspec.yaml` MOVED with the packet under openspec 1.2.0 and is
  byte-identical to the ratifying commit `f57287c7` (blob `f77f14a4`), so the
  origin-retention gate passes with no restoration needed.
  **THREE RULINGS RECORDED AT THE ARCHIVE** — Brett, 2026-08-27, by a
  multi-choice put by the orchestrating session; no verbatim wording reached
  the archiving session, so mechanism, approver, date and the option selected
  are stated and nothing is quoted. (1) The **merge-plus-archive sequence is
  APPROVED**, and this archive is that ruling's second half. (2) The permanent
  loss of `66b14064` gets a **COMMISSIONED superseding record plus
  disposition, filed IN PARALLEL as its own packet** — so it crosses this
  archive as an IN-FLIGHT follow-up, and the `KNOWN_LOSSES` row and
  `fully_verified: FALSE` STAND until that packet lands rather than being
  resolved or softened here. (3) The **sentinel-pin vocabulary is a NAMED
  FOLLOW-UP**, recorded beside § 5.1's `git_generation()` dirty-tree gap as ONE
  future packet: the proposal-support sentinels already do what § 5.1 asks
  (`"uncommitted-worktree"` ×6, `"not-applicable-ad-hoc"` ×1, absent ×3), and
  the future packet decides whether that vocabulary becomes shared and
  declared.
  **RATIFIED 2026-08-27** (Brett, in-session commissioning of the filing,
  verbatim: "file the pin-governance follow-up change"). The commission is the
  origin act, so `approved_by`/`approved_on` are recorded from it — the
  `fix-release-reachability-race` shape, not the blank-pair shape its other
  sibling was raised under. **THE CITATION COVERS THE DECISION TO FILE AND
  NOTHING ELSE** — and a SECOND, later act on the same day disposed everything
  it did not reach. **ALL FIVE § Orchestrator decisions CLEARED AS AUTHORED and
  ALL THREE OPEN QUESTIONS RULED, 2026-08-27**, by a four-question multi-choice
  put to Brett by the orchestrating session and relayed the same day; on every
  question he took the packet's own recommendation. No verbatim wording reached
  the packet, so none is quoted — approver, date, mechanism and selected option
  are stated instead. **OD-1 through OD-5 cleared, none vetoed** (the
  three-capability all-ADDED shape, the no-new-check-family enforcement home,
  re-pinning defined by reproduction, record repair by retention, the change
  name), and the clearance moved nothing because all five stand as authored.
  **THE QUESTION RULINGS DID MOVE THE PACKET, which is why the two acts stay
  distinct**: **Q1 RULED** — the declared pin class lives in a registry module
  beside `scripts/doc_health/families.py`, so the declaration is itself checked
  (recorded at `design.md` § 4 and `tasks.md` § 2.1; NO delta text changed, because
  a promoted requirement that pins an implementation path must be MODIFIED the
  next time the module moves). **Q2 RULED AND ALREADY EXECUTED** — publish the
  retention refs FIRST, independently of this packet; the orchestrating session
  did so on 2026-08-27 and this session verified it rather than taking it on
  report: `git ls-remote origin 'refs/retention/*'` returns exactly
  `refs/retention/pins/da9bf3b7d0ee1d86d2d437d42a715c238dddce4b` and
  `refs/retention/pins/f13a3b6007736292e1e157febef1ac733e534de9`, each at the
  commit its name states, so `ls-remote | grep -c` now returns `1` for both pins
  where it returned `0` at authoring. **THE GARBAGE-COLLECTION WINDOW IS CLOSED
  AND BOTH RECORDS ARE CONFORMING WITH THEIR ORIGINAL PINS UNEDITED** — which is
  requirement 2's whole claim demonstrated on the two instances that forced it,
  and it discharges `tasks.md` § 3 entire plus the § 4.5 archive gate, before the
  merge rather than merely before the archive. **Q3 RULED** — formalize the
  retention namespace, and it is the one Q2's execution used:
  **`refs/retention/pins/<full-sha>`**, now NAMED IN THE DELTA rather than left
  as convention (requirement 1 names it and refuses any other name; requirement 2
  obliges publishing it with the ref name COMPUTED from the pin rather than
  chosen; requirement 4 states it as half the ref set a verification consults,
  `main` plus that namespace and no more). Three scenarios moved with it;
  requirement and scenario counts are UNCHANGED at four and sixteen, and nothing
  was MODIFIED. Retention LIFETIME is deliberately still unstated — a retained
  commit is retained because a committed record names it, so the ref outlives the
  record. `.openspec.yaml`'s origin block is deliberately unedited: a veto
  clearance is not origin provenance, and `release-realization`'s
  origin-retention rule makes rewriting a complete declaration a contested-class
  act. **THE FOLLOW-UP
  `harden-ideation-readiness-check` DEFERRED BY NAME** (its § Named follow-ups,
  and § 5.2 unticked at archive; its OD-1 declined an index-side requirement
  "to avoid pre-empting the deferred governance packet" — this packet takes it).
  ONE CORRECTION TO THE COMMISSION, recorded rather than smoothed:
  `fix-release-reachability-race` does NOT defer the rule by name — its § Named
  follow-ups carries three bullets, none about pins — and is cited instead for
  its § Family relation table, which names the orphaned index pin as the
  family's stale operand. **A pin that no ref reaches is a DEFECT, not
  staleness.** Pull request #322 regenerated the cross-reference index on a
  branch pinning `da9bf3b7`, the pin was moved BY HAND to the branch tip
  `f13a3b60` with no body regeneration, and the branch landed rewritten as
  `4e57009c` (single parent `700c1a19`), orphaning both at once; the index's
  orphaned pin then turned the readiness derivation proof into a `pytest.skip`
  for the packet's whole life, so seven real-corpus proofs never ran on a runner
  until PR #400 (889 passed / 7 skipped → 920 / 0). **TWO ORPHANED PINS ARE
  STILL STANDING ON `main`, MEASURED 2026-08-27 at `42662b70`** — the sibling
  repaired the INDEX and left both readiness-run records:
  `health/ideation-readiness/2026-08-24/brainstorm-packet-migration-20260824.yaml:5`
  (`da9bf3b7`) and `…-final-20260824.yaml:5` (`f13a3b60`), each with
  `git branch -a --contains` EMPTY, `ls-remote` count `0`, and
  `merge-base --is-ancestor origin/main` false. Both carry `status: record`, so
  neither pin may be edited — and both objects were STILL RECOVERABLE in a local
  clone, a window that has since been closed by the Q2 retention refs above,
  with both records left byte-identical to capture. `is-ancestor origin/main` is
  still false for both, and that is the intended end state rather than a residue:
  the pins resolve through the retention namespace, not through `main`. Four
  requirements ADDED
  across three capabilities, sixteen scenarios, NONE MODIFIED:
  `ideation-cross-reference` gets the artifact rule (orphaned is a defect,
  reachable-but-stale is legal, judged against REFS not a clone's object store)
  and the record-repair rule (repair by publishing
  `refs/retention/pins/<full-sha>`, never by editing the record — immutable
  evidence and record-immutability collide, and only one ordering is coherent:
  when the record cannot move, the commit does);
  `release-realization` gets the landing rule, with re-pinning DEFINED BY
  REPRODUCTION — byte-for-byte at the new pin where the artifact's tooling
  defines derivation, a named measurement otherwise, and never a hand-moved pin,
  which is the exact act that produced `f13a3b60`; `doc-health` gets the
  enforcement, extending the sibling's index-only obligation to a DECLARED
  artifact class whose declaration is itself checked. **ADDS NO DETERMINISTIC
  CHECK FAMILY and does not restate the enumeration**, for two reasons: a
  reachability probe is not deterministic in that requirement's sense (identical
  corpus, different answer at different clone depths), and every added family
  owes a wholesale restatement of that requirement, which is how three changes in
  three days truncated it. **THE SECOND PREMISE MOVED WITHIN A DAY AND THE
  CONCLUSION HELD** — as authored it named `add-family-enumeration-check`'s active
  `MODIFIED` block; that packet ARCHIVED 2026-08-27 promoting the twenty-one
  enumeration, and `add-modified-block-currency-check` now owes the same block at
  realization to reach twenty-two, so a family added here would reach
  twenty-three with canon decided by archive order. The delta states it in the
  durable form, about the mechanism rather than today's holder. The pin
  inventory is swept and every pin resolved rather than sampled — nine pins,
  eight committed artifacts, four generators, two orphaned, plus four
  schema-declared future members with no committed real pin yet; cross-repository
  pins (aggregation gitlinks, `neutral-product-pin`, release digests, image
  digests) are named OUT of scope. **AND THAT SWEEP DID NOT SURVIVE MEASUREMENT,
  WHICH IS THE ARGUMENT FOR A DECLARED CLASS EXISTING AT ALL.** The realization
  re-measured over committed structured state — every standalone 40-hex token in
  every committed `.yaml`/`.yml`/`.json`, resolved against the object database
  rather than matched by key name — and found **63 sites across 20 members**,
  with four whole generator families the key-name sweep had missed (31
  proposal-support transition manifests, 11 cross-factory ideation routing
  records, the avatar-client kernel with its lab register and F0 evidence, and
  the hermes-runtime handoff evidence with the neutrality-drift baseline) and
  **TWO MORE ORPHANS the packet never knew about**: `74022ea5…`, retained the
  day it was found, and `66b14064…` under the key `us3_baseline_commit` that no
  sweep vocabulary knew — UNRECOVERABLE (`cat-file` fails, absent from all 566
  advertised refs, `git fetch` refused by the server with `upload-pack: not our
  ref`), and therefore the first instance this repository has had to route
  through requirement 2's other branch. The authored table is kept VERBATIM in
  the packet and corrected in `tasks.md` § 2, per this packet's own
  measurement-preservation convention.
  **SIX FOLLOW-UPS CROSS THE ARCHIVE UNTICKED, EVERY ONE BY DECISION**: § 5.1
  `git_generation()` pinning `HEAD` regardless of a dirty tree, now carrying the
  sentinel-vocabulary question Brett ruled a named follow-up; § 5.2 the
  cross-repository pin families; § 5.3 a recorded-measurement format for a
  re-pin, raised by § 2.5's honest gap — the reproduction check is implemented
  for the tool-defined members and the NON-TOOL half is PROSE-ONLY, because no
  field, schema or convention exists anywhere in this repository for a re-pin to
  record a named measurement in; § 5.4 markdown is not swept for coverage, a
  stated trade; § 5.5 the superseding record § 3.6 owes, now COMMISSIONED and
  in-flight as its own packet; and § 5.6 the preflight half of the enforcement
  home, deliberately UNWIRED because wiring a network-consulting check into the
  nightly would answer `fix-release-reachability-race`'s own named open question
  by implementation, for every governed repository at once. Two further
  honesties are recorded rather than smoothed over: § 2.8's landing obligation
  is STATED, NOT AUTOMATED — discoverability IS implemented, `repair_route()`
  naming the allowed route at the moment a finding fires, and no workflow
  enforces it — and the authored 9-pin inventory table stands corrected rather
  than rewritten. A third follow-up the packet carried no longer survives at
  all: the retention namespace was RULED rather than deferred.
  (code surface: openxFactory; target release: implemented)

- [add-family-enumeration-check](openspec/changes/archive/2026-08-27-add-family-enumeration-check/proposal.md)
  — **ARCHIVED 2026-08-27** on the merge-plus-green rule the packet declared, and
  on the precondition `add-modified-block-currency-check` § D5 priced: that change
  registers the TWENTY-SECOND family, and `fam_family_enumeration` checks every
  ACTIVE change's restatement of "Deterministic check families" against the live
  registry, so the twenty-second family's own enumeration block is owed at ITS
  realization relative to THIS packet's outcome. Realization re-verified ancestors
  of `main` at the gate rather than read out of a PR body: PR #340 `253c5e87`
  shipped the family advisory and PR #343 `1bf16533` took § 5.2's ruled
  `FAMILY_IDS` repair. Gate numbers: `pytest tests/doc-health` **980 passed**
  before and after; `openspec validate --all --strict` **76 → 75 items** (24 → 23
  active, 52 specs); the single-repo doc-health headline **byte-identical — 5
  critical, 8 error, 42 warning, 6 info, 0 new regressions** — the whole report
  diff being eight non-finding lines of canon word census (203344 → 204720 words,
  31.0% → 31.1%). Canon promoted at **128 insertions, 6 deletions**, requirements
  32 → 33, file scenarios 133 → 141, and "Deterministic check families" **8 → 8**
  with seven of its eight scenarios byte-identical and the eighth gaining exactly
  one `AND` bullet. The per-requirement pass found TWO canon body units differing,
  both this packet's declared numeral rewording (`twenty` → `twenty-one` with
  `family enumeration` appended to the list, and `Four of the twenty` / `the other
  sixteen` → `twenty-one` / `seventeen`), each verified against the live registry
  — `len(FAMILIES)` = 21, 21 names, 0 unresolved, `21 − 4 = 17` — and canon's
  requirement block proven byte-IDENTICAL between the delta's branch point
  `fe34b73c` and `501a3ae0`, so the block reverted nothing. Authored and ratified
  2026-08-25, commissioned in-session ("commission the §5.5 enumeration check").
  `doc-health`'s own "Deterministic check families" requirement NAMES every check
  family and COUNTS them three times in prose, and every new family must restate
  the whole requirement to add itself — so a requirement every new family must
  restate is a requirement every new family can truncate. It broke THREE TIMES IN
  THREE DAYS and a human caught it every time:
  `add-release-inventory-drift-check`, `add-promotion-fidelity-check` and
  `add-duplicate-packet-check` each restated ONE of its EIGHT scenarios, and
  because `MODIFIED` replaces a requirement wholesale each would have destroyed
  seven on promotion with the file-level scenario count never moving. The
  enumeration half had drifted more quietly before that — `staged-topic-template`
  registered 2026-08-15 and stayed uncounted until 2026-08-23. Closes the
  candidate `add-duplicate-packet-check` § 5.5 recorded and left named. Adds
  doc-health's TWENTY-FIRST family, which derives the enumeration and all three
  numerals from `families.FAMILIES` instead of trusting the hand-restatement:
  the CANON half compares the promoted requirement, and the ACTIVE-DELTA half —
  the real prevention — compares every in-flight change that restates it, so a
  truncation is reported at authoring time rather than at an archive gate. Canon
  is exempt while an active delta restates the requirement, because a change
  registering family N+1 leaves canon at N until it archives: pending, not
  divergent. ADVISORY at launch in both halves, with the flip a recorded task
  box — **§ 5.1 is the ONE box left unticked at the archive**, owed on a measured
  population that by construction cannot be taken in advance. **The irony is the
  acceptance test**: adding the check as a new family forced exactly the
  restatement it polices, so with the family registered and no delta written it
  reported three findings against canon — the omitted name and two stale numerals
  — and zero once this change's own delta was written. Its own restatement was
  verified by its own check before it could be committed. That self-gate's
  anti-vacuity guard was RE-AIMED by the archive act rather than deleted: with the
  block promoted there is no active delta to find, so
  `test_this_changes_own_delta_is_the_statement_under_test` became
  `test_canon_is_the_statement_under_test`, the same three assertions one document
  over. Of the two adjacent gaps recorded rather than folded in, both have since
  closed: § 5.2's `FAMILY_IDS` repair was RULED and taken on 2026-08-25 (PR #343,
  61 findings that had been counted in the headline while rendering under no
  section), and § 5.3 — the scenario-completeness half, the one that actually
  destroyed text — is DISCHARGED by `add-modified-block-currency-check`, whose
  spike found two ledger units on this packet's own block and whose gate is
  scenario-title completeness.

- [add-shared-identity-seeds](openspec/changes/archive/2026-08-27-add-shared-identity-seeds/proposal.md)
  — **ARCHIVED 2026-08-27**; authored and ratified 2026-08-07 (Brett's "yes,
  lets start that now", accepting the successor named at the close of
  `add-repository-lens`), built the same day. Implements the FIRST of the
  promotion process's four ways a DTN candidate is born — "two or more domain
  repos use the same structure with different domain nouns" — which had never
  been automated: none of the neutrality-drift lane's four stage-1 signals asks
  whether two DOMAIN repositories carry the same thing, so that rule was served
  by manual search passes only. The repository lens already computes exactly
  that population (ring 2 and inward on the carrier-count plot), so the change
  adds `doc_health/shared_identity.py` (the deterministic detector plus a seed
  drafter emitting the register's own row and `### DTN-NNN:` detail section,
  numbered from the register so a drafted-but-unmerged gap never collides), a
  loopback drafting route on the dashboard serve that recomputes carriers from
  the serve's own composed view and returns TEXT, and the lens drill-in
  affordance (convergent regions draftable, single-carrier regions refused with
  the reason). SEED-FIRST, NEVER A WRITE: the register is never opened for
  writing and a candidate enters the lifecycle only when a human merges the
  seed — which is what makes the affordance legitimate on a composed READ-ONLY
  view and leaves D10 untouched. No contract growth: no schema, no gate verb,
  no gate-action record.
  **ARCHIVE GATE MET, on the code surface rather than on the target**, the same
  reading `add-model-provider-broker` recorded a day earlier: the declaration is
  non-empty, so `release-realization` requires merged-plus-green and
  `target_release: none` cannot downgrade that to archive-on-landing.
  MERGED: PR #105 landed 2026-08-07 as main `82e3ec4e` (branch head
  `8a028c21`), an ancestor of `origin/main` `42662b70`, with all five declared
  surface files present and the detector module byte-identical to the day it
  landed. GREEN: PR #105 predates this repository's only pytest gate by 17 days
  (`pytest-suite.yml` first landed 2026-08-24 as `74af6cc4`, PR #304), so it
  carries no check runs at all and the green claim rests on MAIN, where the
  gate has run over this code ever since — every uncancelled green main run
  from the first (`cbf2368d`, run `32802536347`) to the last
  (`42662b70`, run `33062355435`, `success` 2026-08-27) carries the detector,
  the route, the affordance and the test file at the same blobs, and the
  workflow has no paths filter, so `tests/ideation-dashboard/test_shared_identity.py`
  is inside each of them. Tasks 1.1–4.4 are discharged, including the
  2026-08-07 live browser check on the real five-factory `domains` project
  (three convergent regions enabled, five single-carrier rows disabled with
  their reason, the 3-carrier sector drafting DTN-025 for
  `docs/credentialing.md`, checkout unchanged); 4.5 too — Brett ruled
  in-session 2026-08-26 to merge that first drafted seed, landed as PR #380
  (`73a535d9`), and the register's highest entry is now DTN-025.
  Promotion is ADDED-ONLY: `ideation-dashboard` 99 -> 100 requirements, 453 ->
  457 scenarios, and all 99 pre-existing bodies re-hashed byte-identical
  afterwards, so no promoted block was restated and no canon repair was owed.
  **5.1 STAYS UNTICKED BY DESIGN** — promoting the detector to a FIFTH
  neutrality-drift stage-1 signal is the named successor, owned elsewhere and
  measurably unbuilt (`SIGNAL_NAMES` still carries four names at `42662b70`);
  the box is left unticked the way `add-roster-device-admission-surface` left
  its §6, because ticking it would claim work this change never did.
  Verification record:
  [`review/archive-verification-2026-08-27.md`](openspec/changes/archive/2026-08-27-add-shared-identity-seeds/review/archive-verification-2026-08-27.md).
  (code surface: openxFactory; target release: none)

- [add-model-provider-broker](openspec/changes/archive/2026-08-27-add-model-provider-broker/proposal.md)
  — **ARCHIVED 2026-08-27**; authored 2026-08-08, **ratified 2026-08-26**
  (Brett, in-session), built in the same round. doxBench has
  a model seam and no model: there is no provider adapter in this repository
  and none is implied, so every model-backed affordance refuses. Brett's
  ruling names openProfiler — external to this repository, and unbuilt at
  ruling time (its broker surface merged 2026-08-26) — as the answer, which makes it a
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
  reaches the browser. RULED 2026-08-26: at mid-turn expiry the dashboard
  re-mints and retries ONCE, with the re-mint and the paid retry visibly
  recorded, and a second expiry in the same turn refuses. BUILT: the binding
  record and its store, a `model-binding` CLI verb group, a credential
  hand-off that streams a handle to the broker's stdin and keeps only the
  reference, the one provider-client module, the package-wide boundary sweep
  that narrows the eleven per-module scans without deleting any of them, and
  the brokered port both entrypoints resolve — with the unconfigured posture
  byte-identical. Task 0.2 is DISCHARGED — openProfiler PR #18 merged
  2026-08-26 (`docs/broker-cli.md`, openProfiler main `d0538c31`), answering
  what a minted token carries: provider-native in both kinds, with `api_key`
  expiry as broker bookkeeping the consumer honours and the whole oauth path
  DECLARED-DESIGN. Cross-checking this seam against that declaration found
  SIX incompatibilities (operation framing, the enrolment stdin, a mint
  answer carrying neither `endpoint` nor `dialect`, the reference key, an
  unpassed `--retry-of`, and EPIPE handling); they are recorded in 0.2's body
  and were RECONCILED the same day as task 2.6: the seam speaks the declared
  subcommand contract, `endpoint`/`dialect` moved onto the binding, and an
  end-to-end test drives the real `openprofiler-broker` binary through
  intake, mint, a `--retry-of`-correlated re-mint, and revoke.
  **ARCHIVE GATE MET, on the code surface rather than on the target.** The
  declaration is non-empty (`code_surface: openxFactory`), so
  `release-realization` requires merged-plus-green and
  `target_release: none` cannot downgrade that to archive-on-landing —
  the gate's antecedent is the surface, and the archive-on-landing path is
  keyed to `code_surface: none`, which this is not. MERGED: PR #392 landed
  2026-08-26 as main `bb7d7ae8`, all five branch commits ancestors of main,
  all eight declared surface files present at `7b7447da`. GREEN: `pytest-suite`
  and `wallet-validation` both SUCCESS on #392's head `0c131981` and again on
  consumer PR #401's head `7eee092d`; on main itself the merge commit
  `bb7d7ae8` carries its own uncancelled green run (`33023028983`), and the
  last uncancelled green main run — `d3e140ea`, run `33031366342` — descends
  from it and carries all three broker modules and all three broker test
  files. The cancelled main runs either side are the
  `pytest-suite-${{ github.ref }}` concurrency group cancelling itself as main
  advances, not reds. Promotion is ADDED-ONLY: `ideation-dashboard` 95 -> 99
  requirements, 444 -> 453 scenarios, and all 95 pre-existing bodies re-hashed
  byte-identical afterwards, so no promoted block was restated. Verification
  record:
  [`review/archive-verification-2026-08-27.md`](openspec/changes/archive/2026-08-27-add-model-provider-broker/review/archive-verification-2026-08-27.md).
  Two residuals are named there rather than buried: `target_release: none` is
  outside the field's declared vocabulary (five other active changes spell it
  the same way, so it is a corpus habit and history is left as written), and
  the real-`openprofiler-broker` end-to-end coverage is point-in-time from task
  2.6's build session — those three tests self-skip on CI, so the standing
  green run proves the seam's behaviour against a contract-speaking fake, not
  that the declaration and the program still agree.
  (code surface: openxFactory; target release: none;
  depended on openProfiler)
- [harden-ideation-readiness-check](openspec/changes/archive/2026-08-27-harden-ideation-readiness-check/proposal.md)
  — **ARCHIVED 2026-08-27**; authored 2026-08-26 and **ADMITTED the same day**
  (Brett, admission ruling against § Open Questions Q0 while the packet stood
  at PR #372). It was raised `Status: draft` with deliberately BLANK
  `approved_by`/`approved_on` rather than fabricated provenance — the refusal
  PR #344 already made once — and the admission filled both fields and moved
  `Status:` to `ratified` under the record-citing spelling, clearing the two
  `ad-hoc origin lacks required` errors that blank pair produced. **THE
  ADMISSION COVERED THE PACKET AND NOTHING ELSE**; the questions and the
  flagged decisions were disposed by a SECOND, later act. **ALL THREE OPEN
  QUESTIONS RULED AND ALL FOUR § Orchestrator decisions CLEARED 2026-08-27** —
  a four-question multi-choice put to Brett by the orchestrating session after
  2026-08-26T23:31Z and relayed the same day. **Q1 RATIFIED** (keep the
  narrowed skip, which fires only on an OBSERVED shallow clone), **Q2
  RATIFIED** (`4e57009c` as the re-pin target), **Q3 RULED LEFT OPEN
  DELIBERATELY** (the three helper copies stay in place with the parametrized
  anti-drift guard; the collapse survives as the named follow-up § 5.1 — the
  question is DISPOSED, not unanswered, so § 5.1 crosses the archive unticked
  BY DECISION), and OD-1 through OD-4 cleared as authored, none vetoed (the
  ADDED-in-`doc-health` shape, the committed-revision read point, the re-pin
  target, and the repair riding this change). No verbatim wording reached the
  packet, so none is quoted — approver, date, mechanism and selected option are
  stated instead. Nothing moved: every ruling matched what the realization had
  already shipped, so the clearance required no edit to a requirement, delta,
  task or design entry — the shape PR #307 recorded when Brett cleared the two
  codex dispositions. `.openspec.yaml`'s origin block is deliberately unedited
  and verified byte-identical to the ratifying commit `5c10ce6d`
  (blob `2d0f7605`), because `release-realization`'s origin-retention rule
  makes rewriting a complete declaration a contested-class act.
  Three `doc-health` requirements ADDED,
  nine scenarios, none MODIFIED. Raised from a 2026-08-26 triage that found TWO
  independent defects in one test —
  `test_derivation_reproduces_the_real_bootstrap_clusters`, the proof that the
  readiness lane's derivation still reproduces the landed
  `ideation-cross-reference` index. **A**: its `_openxfactory_root()` walks UP
  to the first ancestor holding `openxFactory/ideation/cross-reference.yaml`,
  which inside this workspace is always the ONE SHARED CHECKOUT — so every
  agent worktree proves a verdict about another session's working tree, and a
  concurrent uncommitted pin bump there (67 listed clusters against 253
  derived) reddened every worktree on the machine while every isolated clone
  passed at every revision; the checker's own `find_index_validator()` carries
  the identical walk and was measured resolving the shared checkout's
  validator. **B**: `main`'s index pinned `f13a3b60`, reachable from NO ref
  local or remote — the branch that generated it landed squashed as
  `4e57009c`, and diffing branch tip against landed index shows exactly one
  changed line, a hand-bumped pin — and the test turned that into
  `pytest.skip`, so the assertion had NEVER RUN in a fresh clone, with a stated
  reason ("shallow clone?") that is false where it fires because
  `pytest-suite.yml` checks out at `fetch-depth: 0`. The three requirements:
  resolve the repository under test first and announce any fallback; read the
  index from COMMITTED state so no concurrent edit can move the verdict; and
  fail — never skip — on an unresolvable pin in a complete clone, keeping the
  skip only for a genuinely truncated one, with the reason naming which was
  observed. The one-line index re-pin to `4e57009c` rode the same change
  because requirement 3 would otherwise have landed it red on its own gate.
  EXPLICITLY DEFERRED to its own future packet: the governance rule that an
  index pin must be re-derived when a branch lands rewritten.
  **REALIZED 2026-08-27 as pull request #400** (merged 2026-08-27T03:05:03Z,
  merge commit `78ffb7f1`, green on head `e9886d77` — `pytest-suite` 6638
  passed / 20 skipped / 0 failed in 13m36s, `wallet-validation` pass): all
  three requirements implemented, the pin and its `.md` projection repaired, 24
  regressions added (`tests/doc-health/test_readiness_proof_resolution.py`),
  `tests/doc-health` **920 passed / 0 skipped**, and the single-repo doc-health
  report byte-identical before and after. The acceptance signal is measured,
  not asserted: with a sibling checkout holding the 2026-08-26 dirty-index
  shape, the PRE-change suite reproduces the packet's **1 failed / 895 passed**
  baseline while the fixed suite is **920 passed** — the same verdict it
  returns beside a clean sibling. TWO CORRECTIONS THE REALIZATION MEASURED: the
  derivation reproduces the committed 290-entry body at `da9bf3b7` and
  `4e57009c`, but at then-current `main` it derives **288** — the corpus moved
  since `31c931fa`, so Q2's alternative now owes a body regeneration; and the
  assertion was unreachable by TWO routes, since in an ISOLATED clone (how this
  repo's own CI `validate` job checks out) the pre-change resolver could not
  find the repository's own index at all — isolated clones went from **889
  passed / 7 skipped** to **920 passed / 0 skipped**, seven real-corpus proofs
  that no runner had ever run. NO CONTRACT BUNDLE WAS OWED, checked rather than
  assumed: no edited file appears in any `contracts/releases/*.digests.yaml`
  inventory. **THREE FOLLOW-UPS SURVIVE THE ARCHIVE and none is asserted
  anywhere in canon** — § 5.1 (the Q3 collapse, ruled open), § 5.2 (the
  governance rule for a `source_revision` recorded on a branch that lands
  rewritten) and § 5.3 (`git_generation()` pinning `HEAD` on a dirty tree).
  (code surface: openxFactory; target release: implemented)

- [fix-release-reachability-race](openspec/changes/archive/2026-08-26-fix-release-reachability-race/proposal.md)
  — **ARCHIVED 2026-08-26**; authored and **ratified 2026-08-26** (Brett,
  in-session commissioning of the filing, verbatim: "file the
  release-inventory CI race fix change"). The
  commission is the origin act, so `approved_by`/`approved_on` are recorded from
  it rather than left blank — the `add-family-enumeration-check` shape, NOT the
  blank-pair shape its sibling was raised under, because that packet had no
  instruction behind it and this one does. **THE CITATION COVERS THE DECISION TO
  FILE AND NOTHING ELSE**: Q1 (object fetch or ref fetch), Q2 (whether the
  offline fixture mechanism even works), Q3 (whether reconciled skew should be
  observable) and Q4 (the unswept sibling modules) stay OPEN. **THE FOUR
  § Orchestrator decisions were CLEARED the same day** — Brett approved all four
  as authored, none vetoed, by a four-question multi-choice on which he selected
  the recommended "keep" option each time (OD-1 the
  ADDED-in-`shared-contract-ownership` shape, OD-2 fetch-before-check, OD-3 the
  archive gate on the bundle cut, OD-4 real-fixture-first with the monkeypatch
  fallback). Nothing in the packet moved: every decision stands as authored, so
  the clearance required no edit to a requirement, delta, task or design entry —
  the shape PR #307 recorded when Brett cleared the two codex dispositions. The
  clearance covers those four and nothing else: Q1 and Q3 stay open, Q4 stays
  declined rather than ruled, and Q2 is SPLIT — OD-4 ruled its mechanism half
  and left its measurement half undischarged. `.openspec.yaml`'s origin block is
  deliberately unedited, because `release-realization`'s origin-retention rule
  makes rewriting a complete declaration a contested-class act, and a veto
  clearance is not origin provenance. Three
  `shared-contract-ownership` requirements ADDED, **TEN** scenarios, none
  MODIFIED — nine as authored, and a tenth on requirement 2 when Brett's
  2026-08-26 ruling folded the shallow-clone rule (§ 6.4) into the same pull
  request.
  **The defect**: `scripts/hermes_runtime_validation/release.py` asks the REMOTE
  for the current `refs/heads/main` object id (`_ls_remote` at `:718` and
  `:803`) and then answers reachability inside the STATIC clone
  (`git merge-base --is-ancestor` at `:723` and `:807`). When main advances after
  the clone, that object is absent locally, `merge-base` exits 128 rather than 0
  or 1, and the guard raises `ReleaseDependencyError("commit reachability could
  not be determined")` — a fail-closed refusal caused by clock skew, not by the
  candidate. **Proven on PR #372**, a doc-only change, run `32934803039`, all
  three attempts at ONE head (`5c10ce6d`): attempt 1 (05:37:56Z-05:49:18Z)
  FAILED and #365 merged at 05:46:00Z inside its window; attempt 2
  (05:52:35Z-06:04:47Z) FAILED and #374 merged at 05:54:06Z inside its window;
  attempt 3 (06:07:45Z-06:20:21Z) PASSED with a quiet window. One tree, three
  verdicts, decided by what else landed during an eleven-minute suite. **THEN
  REPRODUCED UNDER CONTROL** the same day in the packet's own worktree, which
  fell into the defect while the packet was being written: remote `main` at
  `c1c9c0dc`, `git cat-file -e c1c9c0dc^{commit}` exiting 128 locally, the
  realization test failing at `release.py:200`, one `git fetch origin c1c9c0dc`
  exiting 0, and the same test then passing with nothing else changed — which is
  simultaneously the reproduction, the diagnosis, and a hand-run proof of the
  chosen fix, and which settles the primary half of Q1 (the canonical remote
  serves a bare object id under no tracked ref). TWO more
  hazard sites are MASKED behind the first: the same live `main_oid` reaches
  `_surface_drift` (`:686` raises `"Git command failed"` on an absent commit;
  `:689` would compare a real blob against `None` and emit FALSE surface drift),
  and `verify_tag` reads the remote-derived TAG object locally at `:816` — which
  is why the fix resolves the OPERAND on entry rather than retrying the
  comparison. The three requirements: resolve every remote-derived object before
  reading it locally, with reachability's meaning explicitly unweakened; name
  which of three conditions was observed (genuine non-reachability -> the
  existing refusal; unretrievable object -> the existing fail-closed error with
  a reason naming the retrieval; reconciled skew -> no finding at all); and pin
  both new paths with proofs demonstrated to fail when the resolution step alone
  is removed. SAME DEFECT FAMILY as `harden-ideation-readiness-check` — a
  verification answering about LIVE state out of PINNED or STALE state and
  reporting the mismatch as a fact about its subject — and the mirror image of
  it: the sibling made a proof honest by REFUSING to answer from state it could
  not resolve, this one by RESOLVING the state before answering. A BUNDLE IS
  OWED, unlike the sibling: `release.py` is itself a non-editorial member of
  `contracts/releases/contract-v1.43.digests.yaml` (`:993-996`, digest matching
  the tree as of 2026-08-26), so editing it without a cut is exactly the
  non-editorial drift `release-surface-integrity` calls a defect —
  `contract-v1.10` was cut for this same file for this same cause
  (`CHANGELOG.md:2170-2185`). (code surface: openxFactory; target release: next
  additive contract bundle) **REALIZED 2026-08-26 as `contract-v1.44`**: the
  resolution step (`_resolve_remote_object` — `git cat-file -e` probe, then a
  narrow single-object `git fetch --no-tags --no-write-fetch-head`) is called
  where each remote-derived object id enters the local world, covering all four
  readers; six new proofs pin the skew, the release-surface verdict, the
  unavailable-object refusal and the mutation. Q1 DECIDED ON MEASUREMENT — no
  ref-fetch fallback: the canonical remote served a bare object id under no
  tracked ref in 4.80s from a depth-1 clone, so a remote that declines is the
  fail-closed case rather than a case for a speculative wider fetch. Q2's
  MEASUREMENT half is discharged, and it corrected the fixture: `chmod 000` on
  the whole bare `objects/` directory makes git refuse the path as a repository
  at all, so `ls-remote` exits 128 and the fixture would have proved the
  pre-existing "remote main is unavailable" path — revoking read on the single
  object FILE keeps advertisement working while `upload-pack` answers "not our
  ref", which is the condition wanted.
  **ARCHIVED 2026-08-26 on a fully discharged gate.** Merged as PR #390
  (2026-08-26T21:21:13Z, merge commit `8894901c`, re-verified an ancestor of
  `origin/main`); green on the final head `d548d04d` (`pytest-suite` and
  `wallet-validation` both `success`; local full suite 6497 passed / 0 failed,
  `tests/hermes_runtime_contracts` 508 passed); and the bundle CUT, which is the
  arm its doc-only siblings never had — `contract-v1.44` inventory built twice
  byte-identical at 192 entries, `verify-commit` pass, `verify-promotion` pass on
  the merge commit before the tag, the annotated tag `contract-v1.44` published
  on `8894901c` ("additive: the release verifier resolves its remote operand
  before it compares") with `verify-tag` pass re-run at the archive, and the
  aggregation submodule pointer synced at `901bd04a` naming that same sha.
  Canon effect: `openspec/specs/shared-contract-ownership/spec.md` 7 → 10
  requirements and 23 → 33 scenarios, 162 lines inserted and NONE deleted, the
  promoted block byte-identical to the delta
  (`sha256:a645ce31…`). `target_release` was rewritten at the archive from the
  forward-looking "next additive contract bundle" to the `implemented —
  <evidence>` shape register C1 ruled, since the bundle it awaited is now cut.
  FOUR ITEMS SURVIVE AS NAMED FOLLOW-UPS AND NONE OF THEM REACHED CANON: § 5.4
  (the many-runs-identical property — unprovable by construction, recorded
  unproven and substituted by the deterministic skew fixtures plus one live
  probe), § 6.1 (the unperformed sweep of the sibling verifier modules,
  `consumer_handoff.py` first), § 6.2 (the eleven-minute exposure window, a
  `pytest-suite.yml` question) and § 6.3 (`_blob_object_id` conflating an absent
  blob with an absent commit).

- [add-doxbench-distilled-abstract](openspec/changes/archive/2026-08-26-add-doxbench-distilled-abstract/proposal.md)
  — **ARCHIVED 2026-08-26**; authored and **ratified 2026-08-25** (Brett, all
  eight rulings as recommended); `target_release: none` under ruling 2(b), but
  `code_surface` was non-empty, so the archive gate was merge-plus-green PLUS one
  operator run on the real corpus through a real adapter, recorded in
  `realization-evidence.md`.
  Three requirements MODIFIED, seven ADDED. The MODEL half of `#84`: the
  distilled per-document abstract the docs subpane was built to carry. Ruling 0
  SPLIT this change — the doc-only half is
  `ratify-doxbench-landed-context-surfaces`, which took the `:439` simultaneity
  reversal and FIVE of the six integration-surface items and ARCHIVED FIRST on
  2026-08-25, so this change's `:863` delta is authored against that change's
  landed text (verified at that archive: canon plus this change's own additions,
  no canon line missing). The sixth item, the loaded-document selector's claim on
  the accessible name (`:1827`), came back here at packet review because it needs
  code, and is carried by this change's added captioning requirement rather than
  by modifying `:1827`. What is
  left here is the reversal that was actually asked for: Brett's 2026-08-03 ruling
  that the abstract be "header + structure, honestly labelled ... NOT an AI
  distillation" is reversed, and its test pin — a whole-file substring sweep
  (`test_doxbench_context_panes.py:144-152`) that bans "distilled" while missing
  "distillation" — is RELOCATED onto the Node harness as a per-abstract caption
  assertion rather than deleted, because after this change both captions live in
  one file and a file-level sweep cannot tell them apart. Council review then
  found the first draft describing a feature that could not run. A real adapter
  EXISTS — `OmpHarnessBridge` (`doxbench_bridge.py:869`) supervises an
  `omp --mode rpc` child with no credential — but NO ENTRYPOINT declares
  `model_port_factory`, so `_workbench_model_port` returns `None` on every real
  serve. Packet review sharpened that twice more: `serve()` has no callers at all,
  so the declaration belongs at `cli.py:298` beside the notebook adapter and the
  knowledge declaration; and the bridge is unconstructible bare (keyword-only
  `session_root`, no default) and INERT if given only that (catalog defaults to
  `EMPTY_CATALOG`), so the entrypoint must declare catalog, session root and
  launch config install-time — and must build ONE instance for the process, since
  the bridge is stateful and `spec.md:1991` requires one harness session per
  document thread. The prompt ASSEMBLER is new surface, not a reuse:
  `build_prompt_envelope` is chat-shaped to its bones — outline plus documents, a
  non-blank human message, a transcript — so an abstract request needs its own
  assembler, whose pin is that it REFUSES a context packet of any purpose (a new
  purpose constant would have been dead code, since the request carries no packet
  at all). Layer 2 is NOT widened: a comma-joined second owner in a one-owner
  field would degrade the fidelity checker to a comment, so the abstract is a
  layer-2-CLASS SIBLING under the requirement's universal non-authoritative
  clause and `compact_thread` keeps sole ownership with its equality pin green
  unchanged. The verifier's base is the SNAPSHOT'S declared topics and
  destinations — so it fires on the FIRST generation, not only on a regeneration
  — and its check is named SUBJECT-MENTION COVERAGE rather than fidelity, because
  `dispatch_turn` returns one opaque string and claiming more would be this change
  committing the sin it exists to prevent; the one structurally decidable clause
  is that the abstract must name its subject and no path its request did not
  carry, which is also what discharges the injection-leak case. Ruling 7 was the
  sharpest finding: disclosure on this surface REQUIRES EDIT AUTHORITY
  (`doxbench_scope.py:390`), `editable_paths` is fed only by `owned` sections and
  exactly ONE section is owned, so on a cluster tile the eligible subject set is
  EMPTY — either the abstract is refused there or a feature PR quietly opens a new
  disclosure path. Ruled 7(a), with the widening named as a follow-on ruling.
  `clarifications.md` carries the five council constraints (N1-N5), chief among
  them that the abstract cache MUST NOT be the chat `TurnStore`, whose 64-entry /
  16 MB bound abstract churn would evict and whose same-key-different-digest
  conflict rule forces the content digest INTO the cache key. Packet review
  (Codex, PR #352) then closed two holes in that store: the RESOLVED MODEL ID
  joins path and digest in the key, because a human can change the selected model
  while the document stands still and a two-part key would replay the first
  model's prose under the second model's recorded id; and the RE-GENERATE control
  carries an EXPLICIT REFRESH INTENT that invalidates the completed entry before
  dispatching, because a regeneration against unchanged content and an unchanged
  model has an identical key and plain identical-key replay made the required
  control inert except by the accident of eviction. The one-in-flight arm stays
  unconditional, so a double-click still spends one model call.

  **The outcome.** The code merged as #365 (`02477d40`) and the surface then took
  one more round: the FIRST operator run, 2026-08-26, found two defects and closed
  nothing. Four presses of Generate all failed inside the operator's adapter on
  `observed_hashes`, and because `model_failed` is an error-shaped body that names
  no subject, the pane's subject recheck returned before recording anything — all
  four presses left the region on the not-yet-generated caption and the whole of
  `ABSTRACT_ERROR_SENTENCES` was unreachable, so the required control read as one
  that did nothing. A diagnostic dispatch in the same session then returned a
  2_018-byte abstract against `MAX_ABSTRACT_PROSE_BYTES = 1_500` — a good abstract,
  every claim holding against the document's own fields, refused in full only by
  the length bound, after a model call had been spent. #386 (`d4740415`) fixed
  both: a refusal is now recorded against the path the request was DISPATCHED for,
  ahead of the recheck, and the prompt asks for ~150 WORDS
  (`MAX_ABSTRACT_PROSE_WORDS`) — a number a model can count while it writes — with
  the byte bound left where the 280px region put it. Attempt 2, on the corpus at
  `d4740415`, PASSED: Brett at the local console served by
  `~/doxbench-operator/t100_serve.py` — the T100 subscription adapter over the
  `claude` CLI, the second of the two adapters §10.3 allows, `omp` not being
  installed on that host — generated an abstract for
  `ideation/staging/avatar-pilot-hardening/avatar-pilot-hardening.md`
  (digest `20b36eb3…be505a`) on `claude-haiku-subscription.low`, 1119 bytes, and
  the pane rendered it under the ruled model-derived caption beside both controls:
  `caption_state: model-derived`, verifier ACCEPTED, no refusal class. `generation`
  and `wait_bound_seconds` are recorded as NOT CAPTURED rather than invented — the
  operator read the pane, not the network tab. One thing changed at the archive
  itself: the INTAKE FOLD was REVERSED. This change and `add-doxchat-model-intake`
  both modify `doxBench model catalog and provider boundary`, and archive replaces
  canon's block with the archiving delta's raw markdown, so the last archiver must
  carry the other's text; the recorded plan had intake go first. Intake stands at
  0/22 tasks with a real code surface and a blocking broker dependency, so
  archiving this change with intake's four additions folded in would have written
  an intake affordance NOBODY HAS BUILT into canon. This change therefore archived
  FIRST carrying only its own additions — grep for `INTAKE affordance` over
  promoted canon returns 0 — and intake, as the later archiver, now declares
  relative to this change's outcome, which is the direction
  `release-realization/spec.md:64-74` asked for. Promotion: three requirements
  MODIFIED and seven ADDED, canon 88 → 95 requirements and 404 → 444 scenarios,
  85 requirements byte-identical and none removed. `specs/015-doxbench-distilled-abstract`
  is NOT created here; task 11.1 stays open for the Speckit flow.

- [add-omnigent-domain-terminology](openspec/changes/archive/2026-08-26-add-omnigent-domain-terminology/proposal.md)
  — **ARCHIVED 2026-08-26** on met realization evidence, after a task-level
  verification sweep. Authored 2026-08-09 from Brett's direction ("we have a
  neutral spine
  cross domain, but we also need all notices to users and logs shown in
  domain best-practice and well-adopted terminology"), **RATIFIED 2026-08-26**
  (Brett, in-session: "do the omnigent-terminology ratification" — task 1.2,
  read-back in tasks.md). Ratification covers the RULE only — the optional
  `terminology` block, the descriptive-crosswalk shape, and the
  human-facing rendering requirement — not any domain's realization.
  ANNOTATE, NEVER RENAME: an optional `terminology` block on the
  omnigent-domain-overlay contract carries display labels for the ids an
  overlay declares (`workers`, `job_types`, `stop_conditions`, `routing`),
  presentation only, so a label never changes an archetype, permission,
  credential tier, or authority; plus an optional per-worker
  `standards_alignment` crosswalk that is descriptive, asserts no
  conformance, and requires `no_clean_equivalent` WITH a note rather than a
  forced mapping. Extends the pattern this family already runs twice —
  `permission_aliases`, and the Hermes layer model's fixed-roles /
  specializable-display-names rule. Contract half is realized on main
  (`target_release: implemented`): the schema block, semantic checks in
  `scripts/validate-omnigent-contracts.py` for orphan keys, duplicate labels
  and unnoted `no_clean_equivalent`, three negative fixtures under
  `contracts/omnigent/examples/fixtures/negative/`, and the canonical
  `contracts/policies/standards-bodies.yaml` registry (44 bodies, every one
  jurisdiction-tagged after the China round exposed an all-Anglo-American
  skew; `onet_marketing_occupations` added 2026-08-26 because AdxFactory had
  no role-level body registered at all, and marketing spans SOC families
  11-0000, 13-0000, 15-0000 and 27-0000 rather than concentrating in one the
  way computing does in 15-0000). The §3b research rounds produced the
  change's blunt finding, NARROWED 2026-08-26 from nine bodies to eight:
  every commercially stewarded body assessed EXCEPT APQC (SFIA, ITIL, COBIT,
  SWEBOK, ISO/IEC/IEEE 12207, GRADE, SNOMED CT, and the declined CC BY-SA
  Scrum Guide) fails the product-configuration reuse test — each tested
  against its own licence text, and each bar stands. APQC's did not: that
  verdict read apqc.org's site Terms of Service rather than the licence APQC
  prints on page 2 of the PCF itself, which grants a perpetual, worldwide,
  royalty-free right to use, copy, publish, modify and create derivative
  works of the PCF against one verbatim attribution paragraph (3b.5k; Brett
  read PCF 8.0's page in a browser 2026-08-26, and the same paragraph
  text-extracts from the primary 7.4, 7.3.1 and 7.3.0 PDFs). O*NET (CC BY
  4.0) remains the ROLE-level crosswalk in four domains and is not
  displaced (both bodies are now licence-usable; APQC's grant carries its
  attribution condition) — naming a ROLE and naming a PROCESS are different claims — and
  MedxFactory registers none: its eleven workers record
  `no_clean_equivalent` against the PROVIDER taxonomy specifically, because
  labelling a reasoning agent with a role carrying clinical standing is the
  mapping a contributor would reach for and the dangerous one. Ratification
  (task 1.2) is now closed, and so are FOUR of the five domain populations:
  **3.1 OpsxFactory and 3.4 codexFactory ticked 2026-08-26** on their O*NET
  crosswalks with the task-3.0 verification discharged for both — every
  registered occupation code and title re-read verbatim against the body's
  own current publication, and the O*NET Database's move from 30.3 (May 2026)
  to 31.0 (August 2026) caught and pinned in the registry rather than
  inherited silently, which is the APQC failure mode 3b.3 named. Opsx ships
  6 mapped / 3 `no_clean_equivalent` across 9 workers, codex 8 / 3 across 11;
  both populations cover every declared id in all four vocabularies; both
  land via their own domain PRs. **3.2 LedgerxFactory and 3.3 AdxFactory
  ticked 2026-08-26**, the two populations the APQC bar had held: both now
  ship a PROCESS layer beside their role layer, which is the first time the
  multi-body design (task 2.2b) is exercised anywhere in the family. Ledgerx
  restores `apqc_pcf` as a third body beside O*NET and COSO — 6 mapped / 3
  scoped `no_clean_equivalent` / 5 deliberately omitted, the crosswalk
  BOUNDED to the three nodes 3b.5b preserved (9.3 10730, 9.6 10733, 9.9
  10736) with the omitted workers' plausible homes named outside that bound
  rather than declared absent — and moves the stale O*NET 30.3 pin to 31.0
  together with its by-version attribution, which is what the registry flag
  required and what discharges it. Adx goes from 3 of 10 workers crosswalked
  to 10 of 10 workers carrying at least one crosswalk entry (O*NET 5 mapped /
  5 absent, PCF 6 / 4; IAB stays a 3-worker carry-forward, not a full-domain
  body), and it is the domain that proves the design: its two
  workers with no honest occupation, `media_planner` and
  `lifecycle_marketer`, have clean process homes a single-body crosswalk
  would have written off. Its long-unrun marketing brief (3b.5e) ran as part
  of that act. STILL OPEN: 3.5 MedxFactory, whose box is unticked but whose
  overlay already ships the population 3b.5i ruled: eleven workers, every one
  `no_clean_equivalent` against `nucc_taxonomy`, which IS the realization
  rather than an absence of one. Also open: task-level
  verification for every crosswalk in the family, which stays OCCUPATION- and
  PROCESS-level and says so; PCF 8.0's NUMBERING, which neither population
  could re-read because apqc.org answers HTTP 403 to automation — names,
  numbers and element IDs shipped from the primary 7.4 PDF, with APQC's
  stable five-digit IDs carrying the citations and the decimals recorded as
  7.4's; the
  ledgerx UN/CEFACT + BIAN brief, the last of 3b.5f's five and never run,
  whose premise has narrowed from filling the process-layer gap (now closed)
  to widening past cross-industry PCF; and the §4 consumer
  follow-up naming domain surfaces that render their own vocabulary outside
  the overlay. NO LONGER OPEN: the APQC written licence confirmation (3b.5d),
  which gated LedgerxFactory's and AdxFactory's pulled PCF 8.0/3.0 crosswalks
  (3b.5b) but never MedxFactory, which by design registers no APQC/PCF
  mapping at all. It closed 2026-08-26 on a licence APQC had already
  published rather than on correspondence, so PCF element names and numbers
  may ship in product configuration provided the attribution paragraph rides
  with them. 3b.5b is SUPERSEDED, NOT REWRITTEN — it and the ledgerx report
  are record-class evidence with a 2026-08-09 cutoff and stand as written,
  and 3b.5b's other finding, that the shipped 8.x finance numbering was wrong
  for every version, is untouched. Not covered by the grant, and recorded
  rather than assumed: PCF process DEFINITIONS, which ship in separate APQC
  documents whose front matter has not been read.
  **ALSO NO LONGER OPEN, 2026-08-26: the IAB entry (3b.5l).** Both findings
  the adx brief flagged and left unacted are discharged. The STEWARD was
  wrong and is corrected — IAB Technology Laboratory, Inc., a separate
  501(c)(6) from the Interactive Advertising Bureau trade association — and
  the REUSE TEST, which had never been run on the one body predating the
  licence discipline, now passes: **CC BY 3.0, `yes_with_conditions`**. The
  "no licence text" reading was a false negative of the same shape as APQC's
  and was caught the same way — the landing pages publish none, but the grant
  is printed on the artifacts, here on page 2 of the Content Taxonomy 3.0
  Implementation Guide, and the site ToU's redistribution ban defers to any
  "Separate License". So the registry's second grant-inside-the-artifact
  finding in one day narrows 3b.5j again, to eight of ten. What is REGISTERED
  BUT NOT RESOLVED, and stays visible on the entry rather than being averaged
  into the verdict: the best-scoped grant sits on a "Released for Public
  Comment" PDF; only Content Taxonomy is named by it, so Audience and Ad
  Product rest on blanket wording one notch weaker; two of three version
  dates are CONTESTED between the steward's own surfaces and BOTH readings
  are recorded on each rather than one being picked; there is no LICENSE file
  and no notice in the .tsv files, so attribution must be authored into every
  consuming overlay; and the IPR Policy PDF is gated and unread, assessed
  non-blocking because it reaches only members' Submissions. The three
  AdxFactory crosswalks come off PROVISIONAL in that domain's own repo.
  **THE ARCHIVE GATE WAS THE REALIZATION GATE, not the doc-only one.** This
  proposal declares a `code_surface` (the `contracts/omnigent/` schema, example
  and negative fixtures, plus the semantic checks in
  `scripts/validate-omnigent-contracts.py`) with `target_release: implemented`,
  so it could not archive on landing the way a doc-only change does: it needed
  the code merged on the implemented target AND a green run of the runnable
  surface. Both hold — every code-surface commit is an ancestor of `main`, and
  `validate-omnigent-contracts.py` exits 0 at `main` in a fresh clone with all
  three terminology negatives rejected for their declared reasons. **Promotion
  was ADDED-only and byte-faithful**: `omnigent-domain-overlay` goes 8
  requirements to **11** and 21 scenarios to **29**, with all eight
  pre-existing requirement bodies hashed before and after and UNCHANGED, 8/8 —
  the delta carries no MODIFIED section, so no promoted requirement block was
  restated and none could be thinned.
  **THE SWEEP FOUND ONE DEFECT AND REPAIRED IT** rather than archiving over it:
  task 3b.5f, ticked CLOSED once the ledgerx UN/CEFACT + BIAN round ran, still
  carried its pre-run tail saying that round "has NEVER been run", plus a
  broken antecedent that read the ledgerx round as having produced no report
  when it produced
  `research/ledgerx-international-process-bodies-research-report.md`. Both are
  corrected in place under the append discipline — marked SUPERSEDED, not
  deleted, so the closing note stays checkable against what was still owed when
  it was written. Everything else reproduced against the artifacts at live
  main: five overlay-manifest digests recomputed and matching 5/5, every
  registry body count re-derived from git rather than trusted
  (17 -> 30 -> 41 -> 44, each claim exact), and the identity surface diffed
  across all six population commits — worker ids, archetypes, permissions and
  credential tiers IDENTICAL IN SIX OF SIX, which is the constitutional
  5.1/5.2 claim measured rather than asserted. Full record:
  `openspec/changes/archive/2026-08-26-add-omnigent-domain-terminology/review/task-verification-2026-08-26.md`.
  **THE LAST THREE BOXES CLOSED AT THE GATE.** 3.0, the standing per-domain
  term-and-version obligation, is discharged for all five domains — opsx and
  codex by 3.0a, ledgerx and adx by the 2026-08-26 population slices, and medx
  VACUOUSLY, because an obligation over chosen bodies is discharged by choosing
  none. 3.5 is ticked on 3b.5i's own finding rather than by re-arguing it:
  Medx's all-`no_clean_equivalent` stance IS its population, covering every
  declared id (11 workers, 6 job types, 9 stop conditions, 7 routing classes)
  with zero mapped by design. 4.1, the consumer follow-up this change named
  rather than assumed, was BUILT AND MERGED — OpsxFactory PR **#115**
  (`f1065cc`) declares `workflow.adjudication` label pairs in its workflow
  contract, renders them through `_adjudication_refusal`, and asserts by
  `assertNotIn` that the check id never reaches a human-read message, which is
  the principle carried outside the overlay and the whole reason it was named.
  Three residuals ride those ticks rather than hiding under them: PCF 8.0's
  NUMBERING was never re-read (apqc.org 403s automation, so names and element
  IDs came from the primary 7.4 PDF), two of three IAB version dates stay
  CONTESTED with both readings recorded and neither resolved, and TASK-LEVEL
  verification is outstanding and unclaimed in all four crosswalking domains —
  every mapping in the family is occupation-level. §5 stays unticked by
  precedent: an unticked out-of-scope box means owned elsewhere, and ticking it
  would claim work this repository never did.

- [add-dispatch-credential-contract](openspec/changes/archive/2026-08-25-add-dispatch-credential-contract/proposal.md)
  — **ARCHIVED 2026-08-25** on landed realization, no contract bundle owed.
  Authored 2026-08-13, RATIFIED that day by the landing of PR **#168** (merge
  `4e4190cb`). Two neutral `credential-contracts` requirements for the openXdox
  intent-plane dispatch credential — dispatch-only least privilege with
  serving-tier separation (the trigger credential must be a distinct binding from
  the content-write App; the credential-free serving pod must never hold
  contents-write-capable key material), and reference-delivered credential with
  operator-as-binding (generalizing the two-case worker-credential principle:
  vault-referenced, ephemeral, operator per-install, neutral home). Both promoted
  into `openspec/specs/credential-contracts/spec.md`, taking it 5 requirements to
  **7** and 18 scenarios to **24**, byte-for-byte from an ADDED-only delta.
  **The realization LANDED** — the plan voice this row carried while active is
  discharged. Contract side on PRs **#171** (`fceaf837`) and **#172**
  (`eb3cb2f1`): the packaged dispatch/content example records, three negatives
  each naming the rule it violates in `scripts/validate-credential-contracts.py`,
  and the operator-neutral binding runbook. Operator binding: the org-owned
  **openXdox Intent Dispatch** GitHub App, ID **`4582547`**, installation
  **`153530982`** on `opensoft/xFactory`, permissions exactly
  `{actions: write, metadata: read}`; the token-minter resolved as an in-cluster
  **CronJob** pinned at omnigent-install **`66ca33fd`**. Proven end to end: an
  authorized intent fired `intent-apply` run **`31856312594`**
  (completed/success) on `opensoft/xFactory`, the minted token showing
  `actions:write` on that one repo and repository-contents 403, with
  `XFACTORY_APP` still the separate content-write binding. Closed out in
  `installs/hermes-install` — readiness result
  `ready-opensoft-dox-qa-dispatch-minter-20260815t013000z` `ready` on 6/6
  mandatory checks, and CIR `cir-opensoft-qa-dox-dispatch-minter` `completed` at
  seq 9, 2026-08-15T01:35Z. The personal-PAT stopgap
  `dox-intent-inbox-qa-20260810` is **deleted** (Brett, via GitHub settings,
  2026-08-15 — an operator attestation, recorded as such: a fine-grained PAT
  under an individual account is not enumerable by the automation, which is the
  fragility this change existed to retire). Also ratifies
  `docs/openxdox-naming.md` and, in the archive slice itself,
  `docs/openxdox-dispatch-credential-binding.md` (`draft -> ratified`).
  `target_release: none` — it moves no bytes under `contracts/`; the schema shape
  it uses was published at DTN-004 and registered at `contract-v1.33` by
  `add-client-identity-roster`, which is also where routing that registration
  through THIS lane was rejected as cross-lane coupling. The proposal's original
  "next additive contract bundle" line was authoring boilerplate, ruled
  mis-authored 2026-08-25; the stale PR **#177**, which acted on it by allocating
  a `contract-v1.32` cut, was closed the same day as superseded.

- [admit-install-repos-to-aggregation](openspec/changes/archive/2026-08-25-admit-install-repos-to-aggregation/proposal.md)
  — **ARCHIVED 2026-08-25** on merged realization in another repository, which
  is the only place this change's code surface could land. Authored and
  RATIFIED 2026-08-21 (Brett: "do the aggregation admission change, the two
  repos are added to openXfactory github app"). The separate reviewed change
  BOTH ratified install-repo boundary requirements demand before a pin is
  supported, and which they forbid their own creation changes from being: an
  eight-field admission record per repository — path, remote, visibility,
  exact validated commit, checkout, compatibility, update, rollback — for
  `installs/keycloak-install` (`opensoft/Keycloak-Install`, private,
  `1aa184e`) and `installs/openxpki-install` (`opensoft/OpenXPKI-Install`,
  private, `05f4404`). Every value is a read-back: both pin `contract-v1.37`
  at contract commit `c1ffa0f`, and neither carries a `.gitmodules`, so
  recursive checkout is plain checkout and rollback is one revert of one
  gitlink. **The aggregation act LANDED** — the "PENDING" this row carried
  while active is discharged, not still open: xFactory PR **#127** merged at
  **`e02d0a8`**, verified an ANCESTOR of aggregation `main` at the gate
  (`behind_by: 0`) rather than trusted as a branch tip, carrying exactly the
  five recorded paths — `.gitmodules`, `README.md`, both gitlinks at exactly
  the validated commits, and the folded `openxFactory` pointer `eeb095d`. Read
  back on `main`: both stanzas live, `path` + `url` only, **no `branch` key**.
  Discharges the long-deferred `add-trust-anchor` tasks 8.1 with ONE MODIFIED
  delta on "Install repository scope" — verified at the archive gate as a
  canon-complete restatement (both promoted scenarios byte-identical,
  enumeration extended, canon last amended 2026-07-13 so no later writer's
  amendment was overwritten), and the promotion touched that requirement and
  no other: 473 requirements across 50 capabilities before and after, 0 added,
  0 removed, 1 modified. Also closed `implement-*` tasks 1.3/3.3 in both
  changes: installation 145372182 lists both repositories (19 total).
  Authorized no deployment and no pin advance beyond the recorded commits, and
  all **seven §5 not-this-change boxes are archived OPEN** as the recorded
  boundary, on the `roster-device` precedent. **Named, not resolved:** both
  pins have since advanced past the validated commits (`ddfb007`, `3ee98d6`) —
  permitted by §5.7, which fixes the ROUTE rather than forbidding the act, and
  both advances took it (aggregation PRs #135 and #142), so the recorded
  update discipline held on its first two exercises; 5.7 stays open as a
  standing boundary on every future advance. `target_release:
  repository-bootstrap`.
- [ratify-doxbench-landed-context-surfaces](openspec/changes/archive/2026-08-25-ratify-doxbench-landed-context-surfaces/proposal.md)
  — **ARCHIVED 2026-08-25**; authored and ratified the same day (Brett, ruling 0
  of `add-doxbench-distilled-abstract`, recorded as a comment on
  `opensoft/openxFactory#84`). `code_surface: none`, so the applicable arm of the
  archive gate is doc-only landing (`release-realization/spec.md:15-16`) with no
  realization evidence to gather, and origin retention (`:97-103`) is satisfied
  by a `.openspec.yaml` with exactly ONE commit in its history — its own creation,
  `5c547610`. The half of `#84` that needed no ruling and should not have waited
  for seven. Three surfaces shipped into the doxBench context panes on 2026-08-03
  — the lens in three subtabs, the docs subpane split into an abstract region
  above a document wheel, and the deterministic per-document abstract those two
  exist to carry — and the spec mentioned NONE of them: before this archive, grep
  `abstract` or `subtab` over `openspec/specs/ideation-dashboard/spec.md` returned
  ZERO — the full path, because `ideation-dashboard/spec.md` is not a path this
  repo has and the shorthand read as a runnable command. One of
  them did worse than go unmentioned. `spec.md:439` required the bullseye "above
  the always-present flat matrix" and said in those words that the matrix "MUST
  NOT become a toggle-only alternate"; the shipped subtabs make the three sections
  mutually exclusive tabpanels (`staging-workbench.js:488` sets
  `subPanes.get(name).hidden = !on`), so the requirement had been FALSE about this
  surface every day since the subtabs landed. That is what a council split bought:
  a doc-only change that removes a live falsified requirement in one pass rather
  than waiting on a model-derived abstract's adapter wiring and prompt assembler.
  The reversal is taken on what the clause was actually protecting — ACCESS to the
  matrix, not simultaneous rendering — so each section becomes a named,
  always-reachable member of one APG tablist, the `above` ordering is discharged
  by the tablist's declared section order, and a keyboard-reachability scenario is
  added because the guarantee moved from geometry to a widget and a tablist
  without arrow keys is a worse promise than the one it replaced. FIVE
  requirements MODIFIED whole (`:438`, `:863`, `:1853`, `:1705`, `:948` — the
  Active entry read "Six" beside a list of five; the delta always carried five, as
  the proposal's Capabilities block said) plus one ADDED for what is already true
  of the deterministic abstract: never captioned as a distillation (pinned at
  `test_doxbench_context_panes.py:144-152`), an absence STATED rather than
  rendered as an empty box (shipped verbatim at
  `staging-workbench-model.js:1578-1581`), and a named field OMITTED rather than
  placeheld. Ruling 6 is settled here only where it needs no code: a surface that
  selects a subject to DESCRIBE is not a second buffer-selection surface, so the
  buffer contract needs no change and pointing at a document neither loads nor
  keys nor dirties a buffer. **Packet review CUT two clauses that would have made
  this change not doc-only** — the region's accessible name is the static string
  `"selected document"` today (`staging-workbench.js:250`) and no provenance
  caption exists at all (`renderAbstract` emits none), so ruling 6's rename, the
  loaded-document-selector requirement (`:1827`, consequently NOT modified here),
  and the POSITIVE "From the document's own headers" caption all moved to
  `add-doxbench-distilled-abstract`, which owns that line. **The cross-check WAS
  the change, and it came back clean.** All seven claims were read against the
  source and the suites that pin it — the three-section APG tablist with roving
  tabindex, arrows and Home/End (`staging-workbench.js:457-503`); the vertical
  split with the abstract above (`:245-259`); the single-reel drum sharing
  `drumProject`, `nextExpanded` and `inReelWindow` with a real spin
  (`doc-wheel.js:41-53`, `:211`, `:445-451`) over one flattened, still-labelled
  reel (`staging-workbench-model.js:1607-1644`); selection driving the abstract's
  SUBJECT and nothing else (`:278-288`, the Phase A binding route recorded as
  retired at `:197-199`); a pure re-presentation whose `summary` traces to the
  document's own `Summary:` header through `generator.py:458`; the honest absence
  verbatim at `:1578-1581` with true field OMISSION in `renderAbstract`; and the
  `role=region`-with-no-heading idiom — and **NOT ONE WORD of the delta needed
  correcting**, because the two clauses that would have needed it were cut before
  it got here. Its three EXPECTED findings were RECORDED rather than repaired,
  which is what doc-only has to mean: the stale comment at
  `staging-workbench.js:508` still claiming the bullseye sits "ABOVE the
  always-present matrix", and two suites still asserting the wheel is DEFERRED
  (`test_doxbench_context_panes.py:19-25` and `:217-229` — the latter green only
  by ACCIDENT, since the "wheel" it finds near the selector is now the comment
  announcing the wheel DELIVERED) while `test_doc_wheel.py:393` already pins the
  opposite. A fourth rides with them: the arrows/Home/End scenario this change
  adds has NO test pin, its evidence here being a code read. All four sit on
  `add-doxbench-distilled-abstract` (§2.5, and §7.10 for the region rename).
  **Promotion was verified four ways rather than asserted**: the promoted text is
  in canon (`subtab` 0 → 1 hits, `abstract` 0 → 20, `wheel` 14 → 26, `tablist`
  1 → 10); the falsified clause is GONE (all three of "above the always-present
  flat matrix", "toggle-only alternate" and "always-available view of the same
  membership" now return ZERO where each returned one); nothing unrelated moved
  (**82 of 87 requirement bodies byte-identical**, the five that changed are
  exactly the five MODIFIED, none removed, order unchanged); and no scenario was
  lost (**376 → 386**, the exact +10 the packet predicted — `:438` +1, `:863` +3,
  `:1853` +1, `:1705` +1, `:948` +1, ADDED +3 — with zero scenario headings
  dropped). `openspec validate --all --strict` is green at 78 passed / 0 failed
  after the archive, the archived delta file is byte-identical to the authored
  one, and `tests/doc-health` plus the three doxBench suites are green on the
  promoted file. Archived BEFORE `add-doxbench-distilled-abstract`, whose own
  `:863` delta was authored against this text: verified at this archive to equal
  new canon plus its own additions — every canon line and all 16 canon scenarios
  present, diverging only by its declared narrowing of the no-new-ANALYSIS clause
  and its two new scenarios — so it needed no re-authoring.
- [add-projection-title-uniqueness](openspec/changes/archive/2026-08-25-add-projection-title-uniqueness/proposal.md)
  — **ARCHIVED 2026-08-25** on merge-plus-green plus the one piece of evidence
  code alone could not give: a provider read. PR #353 was REBASE-merged, so the
  shas that landed are `79bec8a7` (the derivation, the parity amendment, the
  doc rule, the test file) and `839e0d8e` (the migration record), both verified
  ancestors of `main` at the gate — the branch tips `58af80ee`/`e4ff1f93` are
  not, which is exactly the trap this repository's archive record already
  carries once. Authored and ratified 2026-08-25 (Brett Heap, in-session).
  Raised off that morning's lifecycle-notebook sync report, which recorded FOUR
  MedxFactory staging topics synced into a book holding ONE source for them. A
  source title is the projection's identity key — the sync keys its desired set
  by path and reconciles it by TITLE — but titles derived from a document's file
  stem and the governing rule (`docs/lifecycle-notebook-projection.md` § 2)
  special-cased exactly one repeated stem, `README`. Every other repeated stem
  collapsed: `wanted_titles` is a SET, the deletion pass holds each title at one
  source, and the manifest still recorded all N documents as synced. Nothing
  reported the losers, and `--parity` was structurally blind — it compared a set
  of derived titles against a set of live titles, so a collapse is equal to
  itself and reported OK. Measured corpus-wide against the live mains the books
  mirror: 693 derived book slots resolved to 688 titles, FIVE documents
  displaced across THREE collisions (`[staged] MedxFactory: topic` ×4, `[draft]
  openxFactory: requirements` ×2, `[staged] OpsxFactory:
  exchange-execution-bringup` ×2), and the provider agreed to the source — 695
  live sources where the scan wanted 700. The delta MODIFIES `Authority framing`
  to state INJECTIVITY over the derived set rather than a filename exception,
  and amends parity to prove membership at the DOCUMENT level. **The rule choice
  was measured, not chosen**: the always-`<parent>/<stem>` candidate costs 572
  renames AND STILL LEAVES A COLLISION (both checklists sit in a directory named
  `checklists`), and a declared list of structural stems leaves one too
  (`exchange-execution-bringup` is a topic name no list would carry) — so a fixed
  enumeration is provably insufficient on this corpus, which is what the `README`
  case already was. Ruled: the shortest distinguishing path suffix, repository-
  scoped, against 611 renames and 1222 operations for the fully-qualified
  alternative. **Q1 through Q4 were ruled the same day** in one in-session
  multiple-choice round — the recommendation adopted throughout, Q4's scope
  sub-question folded into Q1 (so the three latent pairs one `Status:` edit from
  collapsing close as a side effect), Q2 keeping the migration on the
  realization's own slice, and Q3 ordering the record that
  `docs/archive-record-discrepancies.md` now carries as its 2026-08-25 addendum.
  No capacity delta was owed and the absence is measured — the guard already
  counts DOCUMENTS, so no guard number moved and the largest book stays at 247 of
  300. **The migration ran and the provider says so**: the dry run matched
  `design.md` § 6 row for row (14 `ADD`, 9 `DEL`, 3 `UPD` — 9 and not 14 because
  three vacated titles were collapsed ones holding a single source between them,
  which is this packet's own arithmetic correction to the "28 ops" figure), the
  apply took the seven books from **695 to 700 sources** (`drafts` 188 → 189,
  `ideation-medxfactory` 49 → 52, `ideation-opsxfactory` 16 → 17, four books
  unchanged), `--parity` returned **PROVEN** in DOCUMENTS under the amended rule,
  and a convergence dry run planned **zero** operations — but only on the second
  attempt: the first caught an oversized `contracts/CHANGELOG.md` source sitting
  under its temp filename, a known readiness race repaired by hand and recorded
  rather than smoothed over. Verified at the gate by requirement map:
  `lifecycle-notebook-projection` **14 → 14 requirements, 48 → 52 scenarios**,
  nothing removed, **13 of 14 requirements byte-for-byte identical**, and the one
  that moved is `Authority framing` at 2 → 6 scenarios — its restatement carries
  the promoted body and both existing scenarios verbatim, and reaches canon
  byte-for-byte (the promoted file diffs as 51 lines inserted, **0 deleted**).
  `promotion-fidelity` reads **0 findings at `--fail-on error`** on the archive
  event itself. FOUR items survive as RECORDED, NOT CLOSED in the packet's § 5:
  titles stay collision-dependent under the ruled rule (variant (a′), manifest-
  pinned monotonic qualification, is measured and not taken); nothing checks
  injectivity outside the sync's own suite, so a corpus-only doc-health family is
  a named candidate; the manifest is never pruned; and which document's content
  survived a collapse is unrecoverable, named as unrecoverable rather than
  guessed.

- [add-duplicate-packet-check](openspec/changes/archive/2026-08-25-add-duplicate-packet-check/proposal.md)
  — **ARCHIVED 2026-08-25** on Brett's ruling ("archive add-duplicate-packet-check
  on its realization evidence"), on merge-plus-green: PR #327 `d5f447e8` shipped
  the family advisory and PR #328 `55bae8a1` flipped it to ENFORCING in both
  halves, each re-verified an ancestor of `main` at the gate. Authored and
  ratified 2026-08-24, commissioned in-session ("commission the duplicate-packet
  check"). The neighbour class of promotion fidelity, and the one that family is
  structurally blind to: TWO archived packets can promote the same delta content
  — one ruling discharged twice — and because canon then holds exactly what both
  packets said it should, the archived-delta-vs-canon comparison reads 0 either
  way. The near miss is on this repository's own record: PR #317 and the landed
  `2026-08-25-apply-branch-sessions-deltas` both restated the identical
  2026-08-01 `add-workbench-branch-sessions` delta — the same git blob — from
  parallel sessions, and a human closed the second unmerged twenty minutes later.
  `document-lifecycle` gains "A ruling is discharged once" (a packet restating
  another's ratified delta content names it, and the naming records LINEAGE, not
  authority); `doc-health` gains the TWENTIETH family, which compares archived
  deltas ONLY AGAINST EACH OTHER and moves no census, canon-share figure,
  inventory entry or catalog record. Content identity is byte-equality above
  trailing whitespace, never a similarity heuristic. The lineage exemption keeps
  the lawful remedy legal: a pair where either proposal names the other's change
  id stays quiet, while two remedials of one ruling that do NOT name each other
  fire. ENFORCING at archive — `error` severity plus a `CONTESTED` resolution
  row, pinned together by an invariant test that fails by name on a half-flip —
  sequenced behind the FULL pinned population measured at zero: 19 repositories,
  207 archived packets, 1124 identities, 3 restated groups all of them recorded
  lineage, 0 findings. The archive act promotes the enumeration to twenty and is
  the LAST of the three same-day family changes that each restated that
  requirement; all three had written a thin `MODIFIED` block that would have
  destroyed seven of its eight scenarios, and all three were caught — this one
  in `d9e545dd`, before its gate ran. Verified at the gate 8-of-8
  scenario-complete, 27 of 28 pre-existing `doc-health` requirements
  byte-for-byte untouched (28 → 29 requirements, 116 → 124 scenarios;
  `document-lifecycle` 15 → 16, 68 → 72), and both now-enforcing families read
  0 findings at `--fail-on error` on the archive event itself. **The BASIS is
  ruled too** — Brett closed § 5.2 on 2026-08-25 ("keep the pinned basis"), so
  the family measures and enforces on the pinned checkout permanently and the
  live-`main` basis stays scoped to promotion fidelity alone; canon already said
  so as an unconditional SHALL, so the ruling removed an option rather than
  adding an obligation. ONE item survives as RECORDED, NOT FIXED in the packet:
  § 5.5, deriving the family-count enumeration instead of restating it so a thin
  `MODIFIED` block cannot regress canon a fourth time.

- [add-promotion-fidelity-check](openspec/changes/archive/2026-08-25-add-promotion-fidelity-check/proposal.md)
  — **ARCHIVED 2026-08-25** on merge-plus-green, the
  `govern-openspec-corpus-membership` precedent: the five realization merges
  landed on `main` first — PRs #310 `73766b48`, #315 `1274b9bf`, #316
  `51a875ab`, #320 `055a514b`, #325 `44505d1e`, each cited by the sha the
  MERGE produced and each verified an ancestor of `main` — and the archive act
  is this separate later commit. Authored and ratified 2026-08-24,
  commissioned in-session ("commission the archived-delta-vs-promoted-spec
  check"). Closes the prevention question
  `docs/archive-record-discrepancies.md` § FU-DOM-CODEX left open by name when
  codexFactory PR #85 applied a ratified delta that had sat unpromoted since
  2026-08-08: "no check yet compares archived deltas to promoted specs, so the
  class stays unreported." `openspec --strict` validates a delta's SHAPE, never
  its ARRIVAL, and the four lifecycle families read a packet's headers, not its
  bodies — so a ratified requirement could archive and silently never reach
  canon while every check called the repository healthy. `document-lifecycle`
  gained the obligation (a ratified delta reaches its promoted spec; a packet
  whose own proposal does not claim ratification carries archived design
  evidence instead; the most recent archived delta is the authority for a
  requirement). `doc-health`'s eighteenth deterministic family reads archived
  spec DELTAS and promoted SPECS rather than either document set, so no census,
  canon-share figure, inventory entry or catalog record moves. Three resolution
  rules each prevent a measured false positive: latest-writer-wins (478
  capability/requirement pairs, 59 written more than once, one written ten
  times — per-writer checking fires 20 findings where this fires 2), `RENAMED`
  retiring the title it names, and the standing exemption — RELAXED by task
  4.1's ruling (PR #320) from "the proposal says `ratified`" to its opposite:
  archiving is PRESUMED to be ratification, and only a packet whose own
  `proposal.md` declares `draft` or a lower standing is exempt, which is what
  lets annotated and headerless archives be checked at all. **ENFORCING, not
  advisory** — the launch state was `warning` with the family deliberately
  absent from `FAMILY_RESOLUTION`, and PR #325 took the ruled flip in BOTH
  halves at once (severity `error` AND `"promotion-fidelity": CONTESTED`),
  because moving either alone lets a contested resolution gate through
  `uncited-resolution` or leaves an `error` no citation can resolve. The two
  live findings the first run reported against this repository's own archive —
  both against `2026-08-01-add-workbench-branch-sessions` — were DISCHARGED
  before the flip, by `2026-08-25-apply-branch-sessions-deltas` (PR #316), the
  "apply via a proper change" ruling; the family reads **0 findings** in
  openxFactory at `--fail-on error`, before and after this archive act.
  Its own archive gate found a defect worth the halt: this packet's
  `doc-health` delta restated ONE scenario of an eight-scenario MODIFIED
  requirement, so archiving as drafted would have destroyed the other seven —
  the same defect `add-release-inventory-drift-check` carried and Brett ruled
  on the same day, and the one `add-duplicate-packet-check` still carried
  until the commit before this one. Because the sibling archived first
  carrying this change's own inherited text, the faithful block is now CURRENT
  CANON VERBATIM: the archive act leaves all 26 pre-existing `doc-health`
  requirements byte-for-byte untouched and adds only this change's two
  (26 → 28 requirements, 105 → 116 scenarios; `document-lifecycle` 14 → 15,
  63 → 68). The structural blindness that let it through — latest-writer-wins
  makes a destroying delta look faithful — is recorded in the packet's § 5.5
  as a named candidate for a pre-archive restatement-completeness check.

- [add-release-inventory-drift-check](openspec/changes/archive/2026-08-25-add-release-inventory-drift-check/proposal.md)
  — **ARCHIVED 2026-08-25** on Brett's ruling; authored and ratified 2026-08-24
  from issue #312, realized and released the same arc. `validate-contract-release.py
  verify-commit` had been failing at `origin/main` since the `contract-v1.40`
  tag with NO gate running it — a release-inventory gate that nothing runs is a
  gate in name only. Promotes the NEW capability `release-surface-integrity`
  ("the declared bundle describes the release surface", three editorial members
  allowed to drift between cuts) and doc-health's NINETEENTH deterministic
  family, which checks it. Realized at PR #324 / `0780875b`, with
  `contract-v1.41` published and verified from the remote (object `48efdfbe` →
  `0780875b`), and the family reporting 0 error / 0 info at that commit —
  issue #312's symptom, resolved.
  **THE ARCHIVE ITSELF CAUGHT A DEFECT IN THIS CHANGE'S OWN RATIFIED DELTA,
  and the first attempt was reverted uncommitted.** Its `MODIFIED` block for
  doc-health's `Deterministic check families` restated one of eight scenarios,
  and `MODIFIED` REPLACES A REQUIREMENT WHOLESALE — so promotion would have
  dropped seven ratified scenarios silently, the file-level count staying at 98
  because the seven lost exactly offset the seven this change adds. Corrected
  scenario-complete on Brett's ruling of 2026-08-25 and re-verified
  byte-for-byte: 8 of 8 promoted identical, doc-health 98 → 105 scenarios.
  Two issues were filed from that finding — **#329**, the sibling changes
  carrying the same latent loss, and **#330**, the `promotion-fidelity` blind
  spot that cannot see it (that family compares delta→promoted, so scenarios
  lost from a promoted spec the delta never mentions are invisible).

- [reconcile-lifecycle-books-count](openspec/changes/archive/2026-08-25-reconcile-lifecycle-books-count/proposal.md)
  — **ARCHIVED 2026-08-25** (the CLI's UTC stamp; the act ran 2026-08-24
  local, the shape `2026-08-25-apply-branch-sessions-deltas` below already
  set); authored and ratified 2026-08-24. **RATIFIED** on Brett's in-session
  commissioning — "commission the successor change reconciling the
  lifecycle-books count" — given on the residual PR #317's closing comment
  flagged in the same words; no approving OpenSpec change exists to name,
  because the amending act IS this change, so the proposal carries the
  record-citing `Ratified:` spelling `sanction-ratified-record-spelling`
  sanctioned, clearing its three-way floor on approver and date. The successor
  the promotion changes owed. Canon and the `Status: standard` workflow doc
  both counted "the three lifecycle books" — a count made stale on 2026-08-10
  by `split-ideation-book-per-repo`, which replaced the single shared Ideation
  book with ONE IDEATION BOOK PER GOVERNED REPOSITORY beside the shared
  Working Drafts and Canon books and retired the legacy shared book and its
  `xf-ideation` alias. That split's own Impact declared "no changes to … scan
  scope", which is why the count was never in its diff; the staleness was
  collateral. The count then reached the promoted spec through
  `2026-08-25-apply-branch-sessions-deltas`, which promoted 2026-07-26
  ratified text byte-for-byte and declined the correction ON PURPOSE ("Any
  improvement to that text is a separate change with its own ratification"),
  as did the closed duplicate PR #317 — the codex PR #85 discipline forbids
  editing ratified text inside a promotion change. This is the lawful exit
  both named. `Corpus scan scope` now reads "The LIFECYCLE BOOKS' projection —
  one Ideation book per governed repository, plus the shared Working Drafts
  and Canon books —"; `Branch-session notebooks` reads "one of the lifecycle
  books". Both phrases are `split-ideation-book-per-repo`'s own ratified
  vocabulary, reused rather than invented, and count-free so the next split
  cannot restale them. Fidelity is proven by sha256 rather than asserted: each
  block extracted from canon BEFORE promotion hashes identical to the hashes
  `apply-branch-sessions-deltas` recorded (`99fa2a84…`, `107ede78…`), and each
  block extracted AFTER promotion hashes identical to this packet's delta
  (`94565264…`, `f5be6d40…`); the promotion moves exactly two lines, and the
  word-diff is `three` out plus the topology clause in, twice, with all nine
  scenarios byte-identical. The workflow doc's five instances move with them
  (§1 main-only rule, §7 hybrid exclusion, §9 session exclusion, §9 quota
  note, §10 workspace records), and the doc records the amending act on an
  `Amended by:` header line, the convention that same split set on it.
  Behavior moves nowhere: the sync has projected per-repo books since
  2026-08-10 and only the text lagged. `code_surface: none`, so it archived on
  landing. The phrase survives in code comments, one operator message, and
  their tests — declared out of scope here and owed as a separate change,
  since this one acquires no code surface.
- [apply-branch-sessions-deltas](openspec/changes/archive/2026-08-25-apply-branch-sessions-deltas/proposal.md)
  — **ARCHIVED 2026-08-25** (the CLI's UTC stamp; the act ran 2026-08-24
  local, the shape `2026-08-24-govern-openspec-corpus-membership` below
  already set); authored and ratified 2026-08-24. **RATIFIED** on Brett's
  ruling "apply via a proper change", recorded in `add-promotion-fidelity-check`
  task 5.1; no approving OpenSpec change exists to name, so the proposal
  carries the record-citing `Ratified:` spelling
  `sanction-ratified-record-spelling` sanctioned, clearing its three-way floor
  on approver and date. The openxFactory equivalent of codexFactory PR #85: a
  ratified delta that never reached canon is applied through its own change
  rather than by a silent edit. `2026-08-01-add-workbench-branch-sessions`
  carried a `lifecycle-notebook-projection` delta whose ADDED
  `Branch-session notebooks` was absent from the promoted spec entirely and
  whose MODIFIED `Corpus scan scope` had arrived carrying its PREVIOUS
  writer's text — three scenarios where the ratified text says four, and none
  of the amendment that scopes the exclusion to the three lifecycle books,
  names branch-session worktrees inside it, and makes session notebooks the
  ONLY notebook surface permitted to read a worktree while never contributing
  a source, title, or repository name to a lifecycle book. Archive commit
  `a0ea7666` moved the packet and never touched the promoted spec. Both gaps
  are the promotion-fidelity family's first live catch, reported against this
  repository's own archive and deliberately left by the change that found
  them. Drift was checked BEFORE applying: the `Corpus scan scope` region
  hashes to `bbb402c4…` at its 2026-07-12 introduction (`1efa5756`), at the
  source archive (`a0ea7666`), and at all three later commits touching the
  file (`d5e6d428`, `e9a4be6e`, `18a4ffc3` — which touched other requirements
  only), and `Branch-session notebooks` had never been in canon at any commit,
  so the ratified text clobbered no later work. Fidelity is proven by sha256
  rather than asserted: the packet's delta file hashed identical to the
  archived one (`f6ffd39a…`), and each requirement block extracted from canon
  after promotion hashes identical to the ratified delta's (`99fa2a84…`,
  `107ede78…`). Canon gains one requirement and one scenario; behavior moves
  nowhere, because the branch-session realization landed in 2026-07 and only
  the text lagged. `code_surface: none`, so it archived on landing, and its
  landing ticks `add-promotion-fidelity-check` task 5.1 — the box that RULED
  note said closes when this change lands. The family reads ZERO
  promotion-fidelity findings in openxFactory after it.
- [govern-openspec-corpus-membership](openspec/changes/archive/2026-08-24-govern-openspec-corpus-membership/proposal.md)
  — **ARCHIVED 2026-08-24**; authored, ratified and fully realized 2026-08-23.
  (The folder date is the CLI's UTC stamp and the archive act ran at 22:57
  local — the shape `2026-08-22-add-roster-device-admission-surface` and
  `2026-08-22-add-dashboard-account-menu` already set.) **RATIFIED 2026-08-23**
  by Brett Heap in an in-session multiple-choice round over all six Open
  Questions; no approving OpenSpec change exists, so the proposal carries the
  record-citing `Ratified:` spelling `sanction-ratified-record-spelling`
  sanctioned. Takes — and this archive ticks — the last unticked box of that
  change (task 5.1: "`openspec/` joining `GOVERNED_ROOTS` — the event that
  makes the 15 latent lines live. Separate decision, much larger blast
  radius"). MEASURED rather than argued, at `20f3e7e`, by patching
  `corpus.GOVERNED_ROOTS` in memory so no tracked file was ever at risk;
  restoration verified by a byte-identical re-run. **Full membership would
  have cost 573 findings** (82 → 655; 4 → 27 critical, 6 → 556 error),
  **13.2 points of the canon-share headline** (31.3% → 18.1% here, 28.9% →
  16.7% across the six-repo aggregation) and **123 of 724 doc-health tests** —
  121 of them one structural collision, `duplicate inventory key` on promoted
  specs arriving twice, plus two pinned invariants it contradicts outright —
  with at least five of its new fires demonstrably false. **RULED AND BUILT
  instead: a scoped lifecycle scan set**, `openspec/changes/**/proposal.md`
  plus `openspec/changes/**/review/*.md`, read by exactly four families
  (status validity, standard backing, ratified provenance, succession
  integrity) and by nothing that computes a census, a word count, a canon
  share, an inventory entry or a catalog record. Both families are needed, not
  just the ratification one: the two hand-fixed defects that prompted the
  question were replayed against their real pre-fix blobs and split —
  phase-b's uncited `ratified` header is caught by `ratified-provenance`,
  roster-device's line-41 header is invisible to it (`parse_status` returns
  `None`) and is caught only by `status-validity`. **All six questions ruled
  2026-08-23**, four as recommended and two WIDER. **OQ-4**: rewrite every
  `Ratified by:` line that cites a record rather than a change as a prefix
  respell to `Ratified:`, content carried verbatim and each justified from its
  own record — **17, extended the same day to 33** when the slice-5A review
  found 16 lines naming the document's OWN change id, which passes the family
  by self-reference and should not (a change is not its own approving change);
  those 16 are LATENT, so the extension grew the edits and not the findings.
  **OQ-6**: backfill ALL 47 headerless proposals from their own records rather
  than granting `proposal-origin`'s pre-contract-legacy grandfather, with the
  campaign required to STOP AND REPORT any document whose record cannot
  support a header rather than invent one; this supersedes the class half of
  `docs/archive-record-discrepancies.md` C2's 2026-08-22 ruling ("The
  forty-six-wide option was not taken"), while C2's per-record findings stand.
  **OQ-2 was ruled TWICE.** The second time, after slice 5D's adversarial
  review found the ruled glob `**/review/*.md` wider than the delta's prose
  ("any `review/` record whose subject is the ratification"), Brett kept the
  RAW GLOB and widened the DELTA: every `review/` record under a packet is a
  governance document, with the taxonomy obligation reaching all of them and
  the ratification-citation obligation reaching only those whose status IS
  `ratified`. Measured at **zero new findings** — openxFactory's 13 review
  records are 5 `ratified` (each already cited under OQ-5) and 8 `record`
  (a conforming value) — so the widening changed what the rule says and not
  what the corpus owes. A separate correction in the same lap made the
  byte-exact-evidence MUST NOT enforceable on MEMBERSHIP rather than left to a
  census: `corpus.EVIDENCE_PARTS` excludes any path carrying a
  `supporting-docs`, `source-snapshots` or `evidence` segment, applied AFTER
  the ruled globs resolve so the globs themselves are untouched, and it
  removes **nothing** from the real corpus at the aggregation's pinned SHAs
  (285 scan-set documents before and after). **REALIZED across four merged
  PRs, every one rebase-merged, so what is cited is what `main` carries and
  not the branch commits**: **PR #279** (`da1b0e9`, `450735f`) slice 5A, the
  thirteen active lifecycle-header defects, 9 critical + 4 error; **PR #280**
  (`d615da5`) slice 5B, twenty-eight archived-record citations — twelve live
  criticals cleared and the sixteen latent self-citers respelled — under the
  B1/B2 in-place-overwrite discipline with a travelling bookkeeping note per
  record; **PR #283** (`64d8087`, `4246592`) slice 5C, forty-four archived
  backfills by two named derivation routes, 43 direct and one stop-and-report
  (`enable-live-openxfactory`) resolved the same day by ruling, 44 error; and
  **PR #284** (`d4ab3ba`, `7157fa3`, `bf0bda0`) slice 5D — four stragglers that
  landed from other sessions mid-campaign discharged FIRST, on a tree where the
  gate did not yet exist, then the enforcement, then the review's fix lap.
  The enforcement itself is `LIFECYCLE_SCAN` + `EVIDENCE_PARTS` and
  `load_lifecycle_docs` in `scripts/doc_health/corpus.py`, one `Context` field
  in `runner.py`, and `_lifecycle_scope(ctx)` at exactly four call sites in
  `families.py`, with `tests/doc-health` at **744** (724 + 20, every new test
  mutation-validated). **New standing findings on the day it landed: zero** —
  §5 discharged the whole standing population first (68 at proposal, 69 by
  5A's start, plus the four that arrived mid-campaign), which is why the gate
  reads **0 critical / 0 error over the 126-document scan set measured through
  `runner.build_context`**, the code CI runs, rather than through a replay.
  **The corpus did not move**: the whole `--single-repo` report is
  byte-identical with the scan set present and with it neutralized in memory,
  and stands at 4 critical / 8 error / 68 warning / 4 info over 328 documents.
  The domain repositories' own **36 critical / 75 error** across 159 packet
  documents at the aggregation's pinned SHAs are ADVISORY BY RULING and are
  not silenced — no contract date, no reduced-severity class, no exclusion —
  and are recorded as seven named follow-ups (FU-DOM-ADX, -HEALTHLINC,
  -LEDGERX, -MEDXEHR, -MEDXFACTORY, -OPSX, -CODEX) in
  `docs/archive-record-discrepancies.md`, durably rather than only in a packet
  that would archive. **PROMOTED**: `doc-health` (MODIFIED `Deterministic
  check families` — sixteen families corrected to seventeen, the four scan-set
  readers named, and the census/word-count/canon-share/inventory/catalog
  exclusion stated; ADDED `Governed corpus membership and the lifecycle scan
  set`, 5 scenarios) and `document-lifecycle` (ADDED `Proposal packets carry
  the lifecycle header`, 6 scenarios). Verified by requirement-map diff either
  side of the archive: 24 → 25 and 13 → 14 requirements, 93 → 98 and 57 → 63
  scenarios, ZERO requirements dropped, all eight of the modified
  requirement's scenarios surviving, and zero drift byte-for-byte on every
  requirement the deltas do not name.
- [sanction-ratified-record-spelling](openspec/changes/archive/2026-08-22-sanction-ratified-record-spelling/proposal.md)
  — **ARCHIVED 2026-08-22**, authored, ratified and realized the same day.
  Closes the gap between the one ratification-citation spelling
  `docs/document-lifecycle.md` § Status Claim Rules sanctioned
  (`Ratified by: <change>`) and the two the corpus actually writes, which the
  2026-08-22 adversarial review recorded in
  `docs/archive-record-discrepancies.md` (B1, C2, C7) and which Brett's own
  C2 ruling then made an instruction ("a citation line in whichever existing
  spelling honestly fits"). Measured at `ca0b905`: under the governed roots,
  29 documents carry `Ratified by:` — all 29 naming a resolvable change id,
  13 of them naming ONLY the change id — and zero carry a `Ratified:`
  header; under `openspec/`, 42 of 86 archived proposals plus 11 active ones
  carry `Status: ratified`, split 38 `Ratified by:` / 15 `Ratified:`, and
  only 20 of the 38 name a resolvable change id, so the primary spelling was
  already half record-citing in practice. Not one of those 53 lines fails an
  approver-or-date-or-record test — the rule is written to fit what the
  corpus already does, and **no existing citation line anywhere was
  rewritten**. **The ratified intent:** `Ratified by:` stays PRIMARY wherever
  an approving change exists; `Ratified:` is sanctioned as the RECORD-CITING
  alternative ONLY where none does, and must name at least one of an
  approver, a date, or a resolvable record path — the three-way floor scoped
  to that form alone, because applying it to `Ratified by:` would turn those
  13 sound governed documents CRITICAL in one commit. Exactly ONE citation
  line per document, counted as one TOTAL across both spellings, so the same
  spelling twice is the same finding as one of each. A bare uncited
  `Status: ratified` stays illegal either way. **RATIFIED 2026-08-22** by
  Brett in an in-session multiple-choice round over all five Open Questions,
  every recommendation adopted (PR #267, merge `a316a10`); each ruling is
  recorded inline beside its question, and the proposal is its own first
  conformance test — having no approving change to name, it cites itself in
  the record-citing spelling it sanctions. **REALIZED the same day** as
  **PR #268**, rebase-merged, so cite what `main` carries and not the branch:
  `c854814` (the widened `fam_ratified_provenance`, the § Status Claim Rules
  rewrite, and `tests/doc-health/test_ratified_citation_spellings.py`),
  `8b874a0` (six adversarial-review fixes, two of which amended this change's
  own deltas to transcribe the OQ-4 ruling the realization was already
  obeying), `e8dc70b` (Copilot: report the duplicate-citation finding on the
  count, not the pair) and `93d6216`. The family reads TWO prefixes and never
  a prefix match on the bare word, which would swallow body prose; a new
  `_header_lines` returns every matching header line so "exactly one" can be
  counted rather than short-circuited at the first match. Eight mutations
  were hand-applied and killed, three of them added after the review
  demonstrated two loosenings the first five all survived. Promotion verified
  by diffing the requirement maps either side of the archive: ONE MODIFIED
  requirement on `document-lifecycle` (`Controlled document status taxonomy`
  — the citation rule promoted for the FIRST time; 13 requirements unchanged,
  52 → 57 scenarios, the modified requirement 3 → 8 with all three
  pre-existing scenarios surviving) and ONE MODIFIED on `doc-health`
  (`Deterministic check families` — 24 requirements and 93 scenarios
  unchanged, the whole diff being one widened WHEN bullet that now names four
  ratification violation kinds where it named one). No contract bundle and no
  release tag: `target_release: implemented` owes neither. Gates at the
  archive: `openspec validate --all --strict` 67/67 exit 0 (68 before),
  `tests/doc-health` 724 passed, workbench 140 passed, and a `--single-repo`
  doc-health run unmoved at 4 critical / 6 error / 68 warning / 4 info, which
  is the measurement the change promised — the widening reaches no live
  document. §5 stays unticked as a recorded scope boundary, not a gap:
  whether `openspec/` joins `GOVERNED_ROOTS` (the event that makes the 15
  latent `Ratified:` lines live), the two archived-record citation defects
  the register routes through a ruling per record, and any rewrite of an
  existing citation line are all deliberately outside it.
- [add-doxbench-editing-phase-b](openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md)
  — **ARCHIVED 2026-08-22** on Brett's explicit word, the doxBench editing
  sprint complete. Realization evidence at the gate: §3 verify list PR #206 /
  `e7e7a84`; §4–§9 core PR #207 / `a4a6f6e`; §13 contract release PR #210 /
  `5daa173` (`contract-v1.34`); §10 knowledge service PR #216 / `ece236a`;
  §11 harness bridge PR #223 / `7312c25`; §12 share-session; §11.7 PR #244 /
  `0f50b352` (`contract-v1.38`); and §10.7 PR #256 / `671a6908`
  (`contract-v1.40` — re-cut from v1.39 when PR #259 took that number
  mid-review). Its spec text promoted, **+9 ADDED and ~8 MODIFIED** into
  `ideation-dashboard` (78 → 87 requirements) and **+1 ADDED** into
  `memory-gateway` (21 → 22), verified byte-for-byte against the deltas with
  zero drift across the 91 untouched requirements; supporting-docs packaged as
  `supporting-docs.tar.gz` (3 files) beside its manifest. One follow-up is
  recorded as issue #263 (a whitespace-only `reduced_reason` passes all five
  posture gates — unreachable from this repository's producer, real for a
  third-party one). Authored 2026-08-18, Phase B and the EXIT of the
  `doxbench-editing-model` staged topic:
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
- [add-dashboard-account-menu](openspec/changes/archive/2026-08-22-add-dashboard-account-menu/proposal.md)
  — **ARCHIVED 2026-08-22** (folder dated in UTC; the act fell just after
  midnight UTC on a machine reading 2026-08-21). Authored 2026-08-21. The
  hosted dashboard finally says WHO is signed in and offers a way to leave:
  `/capabilities` gains a per-request `hosted_actor` read from the dox-auth
  gateway's stamped `X-Auth-Request-User` header (`null` when absent, i.e.
  local/loopback serving), and a user-account popover joins the theme and
  settings buttons in the corner controls — signed-in username, an access level
  DERIVED from the existing `actions` map plus loopback state, and a logout
  control that navigates to the gateway-owned `/logout`, because the dashboard
  terminates no session itself. The recorded D16 boundary nuance is the fact to
  keep: reading a stamped identity header is not HOLDING a credential or
  BECOMING an auth authority — nothing authorizes on the value, and a hosted
  request with a stamped actor still gets no write/gate/edit affordance,
  because those capabilities were never keyed on identity presence but on the
  loopback console verdict. No schema, contract, or register change; the
  unversioned `/capabilities` shape grows additively with no version bump, the
  same pattern the `model` and `repository` fields followed. Realized as
  **PR #248** (full dashboard suites 3836 passed / 13 skipped) and DEPLOYED to
  QA — dox-dashboard rolled to the account-menu image (Omnigent-Install #121,
  digest 65e9a293) and live-verified in-pod at the archive commit. Four ADDED
  `ideation-dashboard` requirements promoted; `openspec validate --all
  --strict` green (65). Task 6.2 archives part-ticked on purpose: its live
  browser leg was written as deferred to after the deploy, since the menu only
  renders a hosted actor from behind the gateway.
- [add-roster-device-admission-surface](openspec/changes/archive/2026-08-22-add-roster-device-admission-surface/proposal.md)
  — **ARCHIVED 2026-08-22** (folder dated in UTC; the act fell just after
  midnight UTC on a machine reading 2026-08-21). Authored 2026-08-19. Admits
  the single `device` (node-inventory) admission surface into the closed
  `admission_surface` vocabulary of `client-identity-roster`, through the
  capability's own extension route, so OpsxFactory can enroll its ratified
  `microsoft_managed_node_inventory_reader` (`Device.Read.All` +
  `DeviceManagementManagedDevices.Read.All` + `CloudPC.Read.All`, tenant-wide
  read, provider offers nothing narrower — the roster's Decision-3 motivating
  example). ONE surface, not three — and the three provider areas are NOT
  declared provider-forced breadth, which is the framing adversarial finding F1
  rejected before ratification: the governed unit IS the tenant device estate,
  so tenant-wide read is the GOVERNED scope (`exceeds_governed_unit: false`, no
  `declared_excess`, no `spanned_surfaces`), and Entra / Intune / Windows 365
  are named only in the member's `description` prose because the schema would
  refuse them anywhere structured. Additive — no `contract_schema_version`
  bump. Proposed on the node-inventory realization evidence per the
  reader-grant clarify decision Q4. **RATIFIED 2026-08-19** (record: the
  change's `review/ratification-2026-08-19.md`; clarify rulings plus a
  cross-model adversarial review, F1 fixed pre-ratification and F2 accepted,
  the latter being the read/mutate reslice that keeps endpoint MUTATION and
  Entra-directory as separate future surfaces). Realized the same day as
  **PR #220** (`78f8e01` — squash-merged, so its four branch commits are
  reachable on `main` only through that one commit): the `device` `oneOf`
  member in `contracts/schemas/xfactory-client-identity-roster.schema.yaml`,
  the resliced extension-route prose, the validator's refusal string in sync,
  a packaged `device` example on the governed-tenant-scope shape, and the
  bundle cut as `contract-v1.35 — 2026-08-19` with its digests file (the
  bundle has since moved on to contract-v1.37; a later cut does not unmake
  it). The archive gate closed on its own re-measurements rather than the
  merge run's: roster validator self-test PASS from a clean path (4 positives
  clean, 31 negatives refused for their registered reason),
  `openspec validate --all --strict` 65/65 exit 0 (66 before this archive),
  `validate-contract-release.py verify-commit` pass on `78f8e01`,
  `tests/doc-health` clean from a clean path, and a doc-health run diffed
  against its own base with zero findings moved. Its ONE MODIFIED requirement
  promoted with the device scenario as its third, the capability's requirement
  count unchanged at 13. `target_release` was corrected from a bare
  `implementation_pending` to `implemented` on this archive, and the
  pre-realization banner replaced, since both read as though merged work were
  still owed. §6 stays unticked as a recorded boundary, not a gap: the
  downstream OpsxFactory `device` roster entry and its consent ceremony are
  authored in that repository under its own governance.
- [add-doxbench-editing-phase-a](openspec/changes/archive/2026-08-21-add-doxbench-editing-phase-a/proposal.md)
  — **ARCHIVED 2026-08-21** (realization evidence recorded at the gate: PR #196
  / `6ac42ed`, plus its own annotation round at #199 / `224bf22` and #201 /
  `96975c1`; its spec text promoted, +5 ADDED and ~2 MODIFIED, which is what
  gave Phase B's three Phase-A-relative MODIFIED requirements something to
  amend). Authored 2026-08-15, Phase A of the `doxbench-editing-model` staged
  topic
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
  staged topic) — and that F2 obligation is DISCHARGED by Phase B's §13
  release, `contract-v1.34`, which is why Phase A archived first. Task 9.1's
  merged-commit evidence is recorded in the archived proposal.
- [add-staged-topic-outline-template](openspec/changes/archive/2026-08-21-add-staged-topic-outline-template/proposal.md)
  — **ARCHIVED 2026-08-21**, all 22 tasks discharged and the realization
  evidence recorded at the gate. THIS CHANGE'S OWN REALIZATION CHAIN is eight
  merged PRs, each of which edits this change's own files: #193 (`93f4241`,
  doc-health's WARNING-tier `staged-topic-template` family), #195 (`ea42a43`,
  the template as contract text in `docs/document-lifecycle.md`), #198
  (`e0dbcea`, `642dd64`, the outline section model and Amendment 1), #208
  (`26558e7`, `3a1f3aa`, `cd9f683`, the outline tab, tasks 3.1-3.5 + 4.4), #211
  (`9dfd59a`, `4c9b46b`, the mutation-validated tests, tasks 4.1 + 4.3), #217
  (`55e8a67`, `7469d1a`, `b84a936`, task 4.2 discharged by DRIVING the real
  round trip), #224 (`8dde22f`, `2f9e876`, bookkeeping 6.1-6.3) and #227
  (`5654343`, `8780bf5`, `67ad236`, `a70bf01`, `0d4cf16`, gates 5.1-5.4).
  SPAWNED CHANGES REALIZED SEPARATELY, and NOT part of the chain above — each
  has its own archive record carrying its own evidence, and none of these three
  PRs touches a file of this change: `align-demote-to-round-trip-rule` (PR #215
  / `79ed72e`, archived 2026-08-19 by this change's #217),
  `refine-demote-round-trip-mechanics` (PR #221 / `6c3d87c`) and
  `align-status-reader-to-real-lines` (PR #222 / `c379a09`), the last two
  archived 2026-08-21 by #225. All three descend from task 4.2's driven round
  trip. Separately, #228 (Phase B wave 2) edited this change's `tasks.md` to
  reconcile its 5.3 enumeration and 6.3 path after the `doxbench-editing-model`
  topic exited staging — a cross-change bookkeeping repoint, not a realization
  of anything here. Two ADDED requirements promoted —
  `document-lifecycle`'s "Staged topic primary-fragment template" (5 scenarios)
  and `ideation-dashboard`'s "The outline tab renders the staged-topic template"
  (4 scenarios) — and the staged origin's support bundle archived beside the
  change as `supporting-docs.tar.gz` + manifest, per `Supporting-document
  archive retention`. Authored 2026-08-15 from the
  `staged-topic-outline-template` staged topic,
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
  surfaced a live demote defect, which is where all three spawned changes
  listed above came from; every one of them is closed before this change
  archived. Bookkeeping 6.1-6.3 discharged (this row, the exit-marked staging
  fragments, and the `doxbench-editing-model` Q4 handoff). GATES 5.1-5.4 ARE
  NOW CLOSED, task 5.4 by driving a real headless browser against a throwaway
  scratch checkout: the outline tab opened on a conforming and a pre-template
  topic, a section added to the conforming one through the free-form control,
  and the shipped Save landing ONE commit on session branch
  `draft/outline-conformer` whose `edit-document` verb is evidenced three ways
  (the `/actions/gate/first-edit` response, the commit subject plus its
  `Gate-Action` trailer, and the committed gate-action record's own `action:`).
  5.3's enumeration also surfaced that `staged-topic-template` is registered in
  `families.FAMILIES` but absent from `FAMILY_IDS`, so the report prints no
  section for its 29 warnings — the same pre-existing omission `proposal-origin`
  has, left for `doc-health` to fix. The archive gate then closed on its own
  measurements: `openspec validate --all --strict` 63/63 exit 0 (64 before this
  archive), `tests/ideation-dashboard` green, `tests/doc-health` clean from a
  clean path, and a doc-health run diffed against its own base with zero
  findings moved. `target_release: implemented`, satisfied.
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
- [add-subject-overlay-contract](openspec/changes/archive/2026-08-15-add-subject-overlay-contract/proposal.md)
  — ARCHIVED 2026-08-15:
  the neutral `hermes_subject_overlay` kind is RELEASED as **`contract-v1.32`**
  (annotated tag verified; 190-entry digest inventory) and CONSUMED —
  hermes-install pins the family at the tag with parity floors covering the
  kind (1 positive + 8 negatives), and the first instance
  (codexFactory `hermes/subject/project-alfa/overlay.yaml`) is LIVE-SEEDED on
  the QA stack (repin+seed window 2026-08-15). OQ-1 ruled: kind name
  canonical, identity `subject.id`, `stricter_only` refused for
  `relation_to_baseline: additive_constraints_only`. Related landing surface
  for staged topic `subject-establishment` (DTN-017).
- [add-worker-credential-by-reference](openspec/changes/archive/2026-08-14-add-worker-credential-by-reference/proposal.md)
  — ARCHIVED 2026-08-14:
  credential-by-reference is LIVE on all three CPC claude lanes — vault
  source + rotation proven (§11.4 smokes), and the host is fully
  credential-free (final smoke run 31833019258). Vault deletion is the
  single kill switch; rotation is one vault write.
- [align-doxbench-contract-pin-to-publisher](openspec/changes/archive/2026-08-13-align-doxbench-contract-pin-to-publisher/proposal.md)
  — **ARCHIVED 2026-08-13**, ratified 2026-08-11 by Brett ("ratify the
  change"). doxBench's two model routes had been dead since
  `adopt-neutral-tooling-home` moved the dashboard runtime into openxFactory:
  `verify_stack_pin` demands the HOSTING repository's `stack.yaml` consumption
  pin, openxFactory is the publisher and has none, so the model-catalog and
  chat-turn routes refused fail-closed from every checkout of this repository —
  the tranche-D open item that relocation itself recorded and deferred. The
  ruling is PUBLISHER MODE over adding a `stack.yaml` here (design Decision 1;
  the alternative was put and declined): tooling hosted inside the publisher
  verifies its consumption by the released BYTES it reads, since a checkout
  carrying the manifest, the schemas, and the family validator IS the release —
  a consumer checkout keeps the declared-pin requirement exactly as it stands.
  Two defects hidden behind the refusal went with it: the hard pin moved
  contract-v1.28 to contract-v1.31 (digest-neutral — v1.31's manifest records
  the two digests already pinned), and resolution now prefers the publisher
  checkout the runtime is running in instead of walking past itself into a
  sibling checkout sitting on another session's branch. Realized as **PR #164**
  (`5d8e963`) and green on the implemented target (`tests/ideation-dashboard`
  2850 passed / 5 skipped, `openspec validate --all --strict` 58/58), plus live
  browser proof: the request that answered `500 catalog_unavailable` before the
  restart answered `200` with a conformant empty catalog after it. One
  requirement promoted into each of `ideation-dashboard` and
  `shared-contract-ownership`.
- [add-session-notebook-reconciliation](openspec/changes/archive/2026-08-13-add-session-notebook-reconciliation/proposal.md)
  — **ARCHIVED 2026-08-13**, ratified 2026-08-10 by Brett ("fix the session
  teardown notebook gap"). A branch session's notebook is supposed to die with
  its session, but a session that ends outside the two governed endings — a
  probe removing its worktree by hand, a crash — retires nothing, and the
  governed retire path correctly REFUSES a dead session, so the one case that
  needs cleaning had no governed door at all. On 2026-08-10 two orphans were
  found on the shared live account and deleted by hand. The fix is a fourth
  sync mode, `--session-sweep`, reconciling the `xf-session-` namespace against
  the live-session set, and each of its five properties is a decision: detection
  runs FORWARD-derived, because `notebook_alias` is lossy and a title can never
  be inverted to a `(repository, branch)` key; a repository that cannot be
  enumerated refuses the WHOLE run rather than retiring what it could not
  account for; a notebook whose repository slug this workspace does not carry is
  reported out of scope and never judged; report-only until `--apply`; and
  retirement goes through `retire`, never `delete`, so the session-prefix and
  key-derived-title guards apply. The dry run earned its place — the first run
  called both of Brett's LIVE sessions dead because they were opened from
  feature worktrees the enumeration never asked, which fail-closed could not
  catch ("no sessions in this checkout" is a legitimate answer); enumeration now
  covers every worktree git lists, pinned by
  `test_a_session_opened_from_a_feature_worktree_is_seen_as_live`. Realized as
  **PR #163** (`1b964ba`), green at 2850 passed / exit 0; one requirement
  promoted into each of `ideation-dashboard` and
  `lifecycle-notebook-projection`. Archived by the one-at-a-time gate pass that
  deliberately LEFT four sibling changes active (two on unbuilt work, two on a
  disposition call: their code is merged and green but Brett has not used the
  feature once), and that flagged without fixing `target_release: none` as an
  illegal value carried here and by five siblings.
- [split-ideation-book-per-repo](openspec/changes/archive/2026-08-10-split-ideation-book-per-repo/proposal.md)
  — **ratified and archived 2026-08-10** on realization evidence (Brett,
  verbatim "ratified" — the cross-model decision review's one declined judgment
  therefore stands as authored: headroom warning plus further-delta rule, no
  pre-authorized splits). That morning the shared Ideation book hit
  NotebookLM's 300-source per-notebook cap MID-SYNC: the next `nlm source add`
  failed with an empty provider error, the run died, and every subsequent
  ideation document across all governed repos went silently unprojected. Of the
  300 capped sources: openxFactory 188, LedgerxFactory 62, MedxFactory 36,
  codexFactory 11, OpsxFactory 4. Ideation books become PER-REPOSITORY,
  resolved by TITLE (`xFactory Ideation — <RepoName>`, the provider's truth),
  with the `xf-ideation-<repo-slug>` alias family a machine-local operator
  convenience — re-registered idempotently, never fatal when absent, since a
  second host or CI runner must not die on a per-machine alias store. Books are
  created lazily on the first apply-mode sync where a repo has ideation
  membership; Working Drafts and Canon stay single. The new PROJECTION CAPACITY
  GUARD makes the next crossing a warned, named, governed event instead of a
  dead run: headroom warning at 30 sources or fewer, a deterministic in-cap
  prefix with the exact excess reported and a nonzero exit on overflow, and
  per-book containment so one bad book never kills the rest. The legacy
  `xf-ideation` book and alias were RETIRED, never repointed — an alias that
  silently changed meaning would corrupt every operator habit and doc reference
  at once — after per-repo parity was proven by title-set equality against the
  corpus scan rather than against the capped book. Task 4.3 was left unticked in
  the archive commit (`e9a4be6`) by oversight and corrected in place with a
  note rather than silently, per the contested-finding rule.

- [qualify-avatar-brokered-call-feasibility](openspec/changes/archive/2026-08-09-qualify-avatar-brokered-call-feasibility/proposal.md)
  — tenant-data-free F0 harness for sideband-before-answer ordering, retries,
  readiness, revocation, redacted evidence, and contract interface impacts;
  F0 does not qualify live use. Realized (F0 `PASS`) 2026-07-12; archived
  2026-08-09 under the archive-aware F0 gate (issue #30 option C — the
  `interface-lock.yaml` pin is unchanged and the gate resolves the packaged
  archive, digest-checked, fail-closed).
- [add-project-visible-set](openspec/changes/archive/2026-08-09-add-project-visible-set/proposal.md)
  — **ARCHIVED 2026-08-09** on Brett's ruling that the day's Playwright
  acceptance session (13-repository local plane, project `domains`) satisfied
  task 3.4; ratified by his 2026-08-07 view-selector ruling
  (`dashboard-project-scoping` D19). The project filter stops being an
  INDICATOR of a decision made elsewhere and becomes the VISIBILITY CONTROL it
  visually promised: each member row's eyeball ticks its repository into or out
  of the view, `all` and `none` are the two bulk moves (which is why "all
  repositories" needs no line of its own), and the composed view spans the
  visible set — narrowing applied BEFORE the ratified cluster union, so merged
  tallies count visible contributions, and `composed_from` trimmed so the
  freshness header names the repositories actually rendered. Exactly one
  visible repository serves that repository's OWN snapshot with full
  capabilities; any other count serves the read-only composed aggregate; an
  empty set renders honestly empty. D20 then renamed the second mode SHARED and
  reset its threshold to TWO OR MORE visible carriers rather than every one —
  on five visible repositories the strict all-of-them rule had shown 0 clusters
  where SHARED showed 8 cluster topics, which is the finding D20 exists to
  surface. It also carries a canon CORRECTION: the promoted
  membership-commission requirement still refused a second in-flight edit while
  the code had queued them since D18 shipped on 2026-08-07, that amendment
  having landed in the `add-opendox-project-header` packet after that change
  archived. No contract growth — no schema, route, or gate verb; the narrowing
  is a pure view derivation over data the composition already carries. Its
  `.openspec.yaml` origin declaration was missing at archive because the bare
  `openspec` CLI was used rather than the proposal-support wrap, so the
  fail-closed origin gate never asked for it; the declaration landed the same
  day (`f9bb1a8`).
- [add-repository-lens](openspec/changes/archive/2026-08-09-add-repository-lens/proposal.md)
  — **ARCHIVED 2026-08-09** on the same acceptance ruling (task 4.4); ratified
  by Brett's 2026-08-07 observation (`dashboard-project-scoping` D21) that the
  repository filter and the keyword lens are one mechanism wearing different
  words. `repositoryVocabulary()` re-expresses a composed snapshot in the shape
  the lens already reads — vocabulary terms are member repositories,
  "documents" are cross-repository document IDENTITIES, a document "carries" a
  repository when that repository has that identity — so the lens engine is not
  modified at all, and the bullseye answers HOW shared rather than merely
  union-or-shared: a ring per carrier count, a sector per exact repository
  combination. On the real five-factory `domains` project that distribution WAS
  the finding — 215 identities in exactly one repository, one in two, one in
  three, two in all five: a family almost entirely domain-specific over a
  two-document neutral core, which is precisely the question the
  domain-neutralization candidate register exists to ask. The repository rail's
  ticks ARE the visible set of its sibling exit `add-project-visible-set`, read
  and written through so filter and lens always agree, with local redraws
  instead of reloads; activating the bullseye's centre or a sector DRILLS IN,
  scoping the whole shell to that region's document set behind a banner that
  names and clears it, every other plane keeping only what references that set.
  No contract growth; saving a repository recipe as a workbench manifest or
  cluster is deliberately out of scope and would be a successor with real
  gate-verb growth. Same missing-origin repair as its sibling (`f9bb1a8`).

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
  **Annotation (`split-openxwallet-repo` P3, `contract-v2.0`):** the two
  capabilities this change promoted, its Speckit feature directory and every
  path it names were CARRIED to `opensoft/openXwallet` at `wallet-v1.1` and
  REMOVED from this repository at `contract-v2.0`; openxFactory now consumes the
  family at [contracts/openxwallet-pin.yaml](contracts/openxwallet-pin.yaml).
  The archived packet at
  [openspec/changes/archive/2026-08-08-add-openxwallet](openspec/changes/archive/2026-08-08-add-openxwallet/proposal.md)
  is a RECORD and stays: it is annotated, never rewritten into agreement with a
  later tree.
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
- [add-register-edit-lane](openspec/changes/archive/2026-08-07-add-register-edit-lane/proposal.md)
  — **ARCHIVED 2026-08-07** (folder dated in UTC; the act fell late on
  2026-08-06 local) with all 12 tasks done, the lane's requirement promoted
  into `ideation-dashboard`, suites 2761 passed and strict validation green.
  Ratified by Brett's 2026-08-06 ruling closing the interim hand-fulfilment
  stance every `project-register-edit` commission had shipped with — "we need
  to automate that step 2. we need an update button plus a job that watches" —
  with the two-fork decision (edit + commit + push under pathspec discipline;
  the serve runs the lane) carried as decided. The `register_edit_lane` scans
  dispatched `project-register-edit` descriptors, applies each to the
  aggregation-owned `project-register.yaml` by surgical block edits that
  preserve comments, validates the result against the pinned schema BEFORE
  writing, stamps `delivered_at`/`delivered_by` on the dispatched-to-delivered
  flip, then commits ONLY the register file (explicit pathspec — the shared
  checkout carries other sessions' work) and pushes with pull-rebase-retry; any
  refusal or git failure leaves the descriptor dispatched and reports, and
  nothing is ever half-applied silently. Watch mode is the same lane in a
  polling loop, and the header's "⟳ apply N pending" button runs the SAME code
  inside the serve over a loopback-only, human-gated route, so the click is the
  deliberate human act and only recorded commissions can ever be applied. No
  new gate verbs and no contract-schema growth. Task 3.5 closed on the first
  UNATTENDED fulfilment: Brett commissioned AdxFactory into `xfactory` from the
  dashboard at 2026-08-07T01:30:23Z and the polling watcher delivered it at
  01:31:13Z — register-only commit `dd1179e` pushed to the aggregation's
  `origin/main`, no terminal session involved.
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
- [add-workbench-integrated-editor-chat](openspec/changes/archive/2026-08-02-add-workbench-integrated-editor-chat/proposal.md)
  — **ARCHIVED 2026-08-02** (task 7.8), the change that NAMES the integrated
  workbench **doxBench** and turns a read-only viewer into one governed
  authoring loop: an editable Outline/Document canvas over two independent
  buffers, a chat rail grounded on the live buffers, scope, ref and content
  hashes (so unsaved human edits reach the next turn without becoming governed
  corpus state), model choice from a server-side allowlist with provider
  credentials never entering browser state, chat payloads, git or snapshots,
  typed AI proposals a human APPLIES by explicit gesture — AI output never
  writes a file — refusal of a stale proposal when either target buffer moved
  (no silent merge), and batch Save through the existing branch-session gate
  actions instead of per-keystroke commits. The free-form field is renamed
  **Working subject** so it cannot be confused with a `subject_ref` or any
  identity-bearing subject. Brett's 2026-07-29 governed implementation-start
  exception let the Speckit lane begin before the five predecessor dashboard
  changes archived; it started implementation ONLY, permitting neither a merge
  nor an archive against an unpromoted capability. The contract half landed
  FIRST, recorded as fact rather than intention: `contract-v1.27` (tag
  `fb912b9`) plus the G-1 nullability amendment `contract-v1.28` (openxFactory
  PR #53, tag `a6f49bb` dereferencing to `ff64e81`), both ancestors of main
  while codexFactory PR #63 was still open, with the consumer pinning those
  exact bytes. Realization is that **PR #63**, merged `c80264c` (2,327 passed /
  6 skipped; doxBench contracts 30/30 against the released bytes) after an
  independent two-pass review of frozen head `7b63c6a` — 128 raised, 106
  confirmed after three-vote refutation, 84 distinct, 15 P1 — whose F1-F4
  landed and were re-verified on the live surface. The archive promoted
  `+ 6, ~ 2, - 0, → 1` into `ideation-dashboard`, exactly the scratch-copy
  dry-run's prediction, leaving 46 requirements with `doxBench scoped view`
  replacing `Staging workbench scoped view`. Two rulings on the record survive
  it: 24 tasks archive OPEN on purpose, annotated honestly rather than
  force-ticked, and the front matter's `status: proposed` was left UNTOUCHED —
  no other change in this repository carries a `status:` field, no post-archive
  vocabulary is defined for one, and a change's location under `archive/` is
  its status of record. Carried, not closed: the F5-F10 follow-up wave, R-12,
  the unexercised Narrator/NVDA legs, and the Sonar coverage wiring, whose
  quality gate is red on a coverage MEASUREMENT GAP the reviewer of record
  accepted explicitly.
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
- [add-client-layer-tuning-contracts](openspec/changes/archive/2026-07-24-add-client-layer-tuning-contracts/proposal.md)
  — **ratified 2026-07-24, released as `contract-v1.17`** (annotated tag
  verified) and archived the same day with the staging INDEX marking the
  `client-layer-tuning` topic complete: the neutral tenant-layer contract set
  every operating organization needs before a domain specializes it. Three
  parts — the Plane-1 house team under `templates/client-layer/roles/` (a
  `house_style` baseline with respect and discretion LOCKED and warmth floored
  at `moderate`, ten deciders plus the Client Infrastructure Liaison as a
  composed CAPABILITY rather than a member, and the Finance & Accounting
  Officer owning cost reporting with its `cost_reporting_steward` worker added
  to the scaffold); the `contracts/client-content/` schemas the wizard writes
  and the seeder validates (policy overrides, memory boundaries, integration
  boundaries, and the seedable `hermes_client_overlay` at the decided canonical
  path `config/clients/<client_ref>/overlay.yaml`, declared through the repo's
  overlay descriptor and digest-pinned in the install's compatibility
  manifest); and `scripts/validate-client-content.py` implementing the
  STRICTER-ONLY comparability spec — allowlists subset, denylists superset,
  ceilings at or below, floors at or above, clearances and conjunctive
  envelopes add-only, ordered enums at or above, and anything with no partial
  order routed to `review_required` rather than passing silently — one
  implementation enforced at two points, wizard write time and seeder
  validation time. Live-proven: the opensoft tenant tuned and seeded on
  aks-opensoft-platform-qa-01 (hermes-install phase-2 flip evidence).
- [add-omnigent-domain-overlay](openspec/changes/archive/2026-07-24-add-omnigent-domain-overlay/proposal.md)
  — **ratified 2026-07-22, contracts registered at `contract-v1.16`, archived
  2026-07-24** when the last gated realization landed ("the omnigent program is
  closed"), promoting `omnigent-domain-overlay` + `omnigent-install-manifest`
  (11 requirements, 38/38 strict). Gave the Omnigent layer the domain tier it
  lacked — nothing in the install said it was a software-engineering Omnigent,
  and the only path to a medical or accounting one was copy-fork. Per-domain
  content is now authored once in each DomainxFactory under `omnigent/`
  (sibling of `hermes/domain/`) and consumed by install repos ONLY by digest
  pin, composed under the existing `domain_installation_overlay` operations
  with `stricter_rule_wins`; every declared worker class maps to exactly one of
  five neutral archetypes (`frame`, `generate`, `verify`, `challenge`,
  `assemble_for_admission`) and declares the six-boolean permission matrix with
  `execute_final_action` and `access_secrets` CONSTITUTIONALLY false in-schema,
  beside a `never_assignable` credential tier stronger than
  `unassigned_by_default`. The install manifest digest-pins the Hermes runtime
  manifest as the single source of stack identity — no parallel identity
  document — at exactly one tenant, one domain overlay and N subject workloads,
  composed fail-closed with seeding-vocabulary evidence and pre-rendered
  effective worker profiles. A new family, so canonical Subject/Tenant/Domain
  spellings from birth; legacy spellings survive only inside the pinned
  upstream manifest and are read through the layer-vocabulary mapping. All four
  gated follow-ups are evidenced in the task ledger: omnigent-install's manifest
  increment (`3f31270`), hermes-install's worker-readiness port (`09af670`) and
  its 2026-07-24 live cutover, codexFactory's first overlay with the live
  coding-patch-worker profile rendered BYTE-VERBATIM from overlay + params
  (`469322b` / `def6a56`, sha256 `f2f70eb2…`), and MedxFactory's second-domain
  params fixture proving the pattern with zero core edits. Worker-host mutation
  verbs and multi-domain fleet federation were REJECTED for this generation.
- [adopt-subject-tenant-domain-vocabulary](openspec/changes/archive/2026-07-23-adopt-subject-tenant-domain-vocabulary/proposal.md)
  — **ratified and archived 2026-07-23**, registered at `contract-v1.16`
  (manifest per-file sha256, tenth CHANGELOG release, annotated tag verified),
  promoting `layer-vocabulary`. Freezes the canonical Hermes layer vocabulary
  Brett selected on 2026-07-22 — **Subject Hermes** (the served party or work
  subject), **Tenant Hermes** (the tenant-operator organization running the
  installation), **Domain Hermes** (unchanged) — which is review fix priority
  #2 and closes the §A1 defect where LedgerxFactory's "Client Hermes" was its
  served-subject layer while canonical "Client Hermes" was the tenant-operator
  layer. Domain aliases (Patient, Project, managed system…) SPECIALIZE the
  canonical names and never replace them; "Customer" and "Client" are reserved
  against use as layer names on new or substantively revised governance
  surfaces while staying legal in prose about commercial relationships; and
  released machine identifiers — `customer_subject_ref`, role kinds
  `customer|client|domain`, `contracts/hermes-runtime/` `$id`s — are FROZEN
  byte-stable until the next major bundle, interpreted through the published
  mapping in `contracts/policies/layer-vocabulary.yaml`. The identifier
  migration and the five per-repo migrations are filed as the deliberately
  dormant `layer-vocabulary-machine-migration` staging topic that rides that
  major bundle; hermes-install adopts at its first pin bump.
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
- [add-hermes-domain-overlay-contract](openspec/changes/archive/2026-07-23-add-hermes-domain-overlay-contract/proposal.md)
  — **ratified 2026-07-23, released as `contract-v1.15`** (annotated tag
  verified) and archived the same day with `hermes-domain-overlay` promoted:
  the neutral `hermes_domain_overlay` schema (domain identity, non-empty
  approval scope kinds and required approval fields, and `authority_boundaries`
  split three ways — `<domain>_owns` / `xfactory_owns` / `repository_owns`,
  each non-empty with no overlaps), the `hermes_overlay_descriptor` that turns
  the seeder's hard-coded role-to-path rule into a declaration (a missing
  descriptor falls back to the shipped convention; an unrecognized role fails
  closed), and `scripts/validate-hermes-domain-overlay.py` with
  positive/negative fixtures. Closes the gap the seeding runtime had carried
  since 2026-07-22, when it loaded `hermes/domain/overlay.yaml` under a minimal
  structural check because no neutral schema existed — two conventions held
  together by agreement, now contract. Proved against the real consumer: the
  validator passes on codexFactory's live 37-authority overlay UNMODIFIED, and
  seeding increment 2 replaces the runtime check with validation against the
  pinned bundle. First exit of the `layer-content-materialization` staged
  topic.
- [add-sops-ciphertext-ruling](openspec/changes/archive/2026-07-19-add-sops-ciphertext-ruling/proposal.md)
  — **ratified by Brett 2026-07-19 and archived on landing** (`code_surface:
  none`), promoting the delta into `credential-contracts` (the 24th promoted
  capability delta at the time) on PR #34's merge (`c9dd404`). The durable
  record for a ruling that had first been made as a direct doc edit: SOPS
  ciphertext is NOT a raw credential, so a Flux-managed repository may be the
  single reconciled source of truth for secrets — provided the repository holds
  ciphertext only, the decryption identity is custodied externally, recipients
  are per-environment, plaintext is rejected pre-commit, controller-compromise
  blast radius is accounted for, and exposure rotates the identity AND the
  credential, historical git ciphertext remaining recoverable. Ratification is
  conferred by an OpenSpec change under the document lifecycle and the
  omnigent-install record already cited this ruling as ratified in its
  Amendment 3, so this change is that missing record.
  `docs/credential-access-model.md` §1.1 now cites it. No retroactive blessing
  of base64 or ad hoc encryption — those remain raw credentials. First approved
  realization is the xFactory QA environment: one QA-wide age identity, durable
  private copy only in 1Password, replaceable runtime projection.
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
- [add-doc-health-semantic-sweep](openspec/changes/archive/2026-07-12-add-doc-health-semantic-sweep/proposal.md)
  — **realized and archived 2026-07-12**, promoting +8 requirements (and ~1
  modified) into `doc-health` through the proposal-support wrap, so its
  supporting docs packaged as tar.gz plus a readable manifest; 24/24 strict.
  Adds the AGENTIC second pass beside the deterministic one: an LLM worker
  reads the governance corpus for the two defect classes twelve grep-shaped
  families cannot find — untagged normative prose and prose-vs-spec
  contradictions. Findings are PROPOSALS, never verdicts (always contested,
  severity capped at warning, each naming doc, passage, suspected conflicting
  requirement and a confidence note; the sweep blocks no merge in v1);
  authority splits between deterministic orchestration under the factory
  identity and a CREDENTIAL-LESS analysis worker bounded by an Omnigent worker
  profile whose job envelope the report cites; disposition follows content
  ownership (the owning factory's Domain Hermes for its own docs, the neutral
  ratify gate for neutral or cross-repo findings); and sweep scope is
  Hermes-owned policy, deepest `doc_health.sweep_scope` declaration winning,
  defaulting to incremental. The deterministic pass's "semantic sweeps are out
  of scope" sentence is RE-SCOPED rather than deleted: that pass makes no model
  calls, and the capability now owns both. Realization evidence is nightly run
  29178217833 (2026-07-12, green), whose `health/reports/2026-07-12.md` carries
  the Semantic Sweep section (claude-sonnet-5, prompt contract v2, envelope
  SEMSWEEP-21cd3ce31acd) with findings in both families, its analysis child
  29178226880 running on the CloudPC worker `xfactory-artifact-cpc-brett01`.
  The implementation lived in codexFactory's `scripts/doc_health/` under the
  ownership split of the day; `adopt-neutral-tooling-home` relocated it into
  openxFactory on 2026-08-03.
- [exclude-worktrees-from-notebook-projection](openspec/changes/archive/2026-07-12-exclude-worktrees-from-notebook-projection/proposal.md)
  — **ratified by Brett 2026-07-12 and archived the same day** on complete
  realization evidence, promoting the corpus scan scope requirement into
  `lifecycle-notebook-projection`. The nightly sync's dry run had reported ~230
  pending operations, ~39 of them triplicated sources from
  `xFactories/OpsxFactory-worktrees/` — three feature-branch worktree checkouts
  the scan had treated as a governed repository named `OpsxFactory-worktrees`.
  Applying would have published duplicate, unmerged branch content into the
  shared books under colliding titles; the defect was caught in DRY RUN, so no
  worktree source ever reached a notebook. The projection now scans
  openxFactory and each DomainxFactory under `xFactories/` and excludes nested
  git working copies below a scanned root (`<repo>-worktrees/` containers,
  embedded clones, nested submodule installs) — a scope that had been prose in
  the workflow doc and never a spec requirement at all, which is why the fix
  needed a delta first. Realized in codexFactory (`d71f45b`) with regression
  tests; the backlog dropped 230 to 194 legitimate operations, all applied
  2026-07-12 with zero errors and a clean follow-up dry run (canon 34 / drafts
  114 / ideation 32 desired sources).
- [define-human-escalation-contract](openspec/changes/archive/2026-07-12-define-human-escalation-contract/proposal.md)
  — route/park/interrupt escalation ladder with a deliberately high interrupt
  bar (containment failure only, cited classes), parked-decision packets at
  existing gates, fail-closed silence, the Merge Master low-risk envelope,
  and structural parking in external enforcement; ratified 2026-07-12,
  archived on landing (`code_surface: none`); resolves the dangling `HR`
  consultation in the engineering escalation table
- [add-xfactory-installer-repository](openspec/changes/archive/2026-07-10-add-xfactory-installer-repository/proposal.md)
  — **archived 2026-07-10** (folder dated in UTC; the act fell on a machine
  reading 2026-07-09), promoting `workstation-intake` and extending
  `repo-boundary-governance`. Draws the repository boundary BEFORE any
  application code exists: private `opensoft/xFactory-Installer` becomes the
  implementation home for xFactory intake and installer surfaces —
  bootstrapped with ownership, architecture, contract-consumption, security,
  validation and release documentation, deliberately claiming no WinUI
  application, tagged `v0.1.0-bootstrap`, then pinned into the aggregation at
  `installs/xfactory-installer` at an exact commit. The authority split is the
  point: canonical intake and enrollment evidence contracts stay in
  openxFactory, Intune/Graph administration and tenant credentials stay in
  OpsxFactory, workstation end-state requirements stay in CloudPC-Install, and
  the installer consumes openxFactory by explicit compatibility declaration
  rather than copying canonical policy. `xFactory Workstation Intake` is the
  first product surface; any later website, CLI/TUI or cross-platform surface
  shares the same neutral intake contract. Task 5.2 records what the bootstrap
  does NOT claim — WinUI implementation, Intune enrollment, Graph grants,
  signing and Store submission are successor work, not realization.
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
