# Factory Contracts

Status: draft

This directory is the canonical home for shared factory contracts owned by
`openxFactory`.

Contracts belong here when they define behavior between two or more factory
subsystems, including Hermes, Omnigent/Polly, OpenSpec, Spec Kit, GitHub,
merge council, and worker agents.

## Ownership Rule

```text
openxFactory/contracts/
  owns canonical contract meaning, versioning, and compatibility rules

Hermes-Install and Omnigent-Install
  may keep pinned copies, generated adapters, smoke fixtures, or runtime
  configuration derived from these contracts
```

Install repositories must identify the `openxFactory` contract version or
commit they consume before runtime adapters are treated as compatible.

## Planned Contracts

Copied contracts:

| Contract | Purpose | Initial Source |
|---|---|---|
| `schemas/hermes-job-envelope.schema.yaml` | Job request envelope from Hermes to Omnigent/Polly or other workers | `Omnigent-Install/schemas/` |
| `schemas/hermes-job-event.schema.yaml` | Structured event emitted by worker, bridge, or Hermes service | `Omnigent-Install/schemas/` |
| `schemas/hermes-job-run.schema.yaml` | Job run status and lifecycle record | `Omnigent-Install/schemas/` |
| `schemas/clarification-questions.schema.yaml` | Spec Kit clarification questions emitted by lead engineering roles | `Omnigent-Install/schemas/` |
| `schemas/clarification-answer.schema.yaml` | Single routed answer from an authority role | `Omnigent-Install/schemas/` |
| `schemas/clarification-answer-packet.schema.yaml` | Collected answer packet returned to the requesting lead | `Omnigent-Install/schemas/` |
| `schemas/hermes-operational-postgres.sql` | Hermes operational job/run/event/artifact/approval/traceability database contract | `Omnigent-Install/schemas/` |
| `policies/hermes-governance-agents.yaml` | Hermes profile/group governance and routing policy | `Omnigent-Install/policies/` |
| `policies/merge-risk-policy.yaml` | Merge Master risk classification and GitHub action policy | `Omnigent-Install/policies/` |

Native openxFactory contracts:

| Contract | Purpose | Initial Source |
|---|---|---|
| `schemas/avatar-first-ui-profile.schema.yaml` | Domain-neutral avatar-first UI profile contract for xFactory frontends and domain overlays; AVC-kernel-aligned and realized at `contract-v1.8` with per-file SHA-256 in `manifest.yaml` (consumes the `contract-v1.7` kernel read-only) | `openxFactory` |
| `schemas/domain-installation-overlay.schema.yaml` | Domain overlay contract for supplementing, replacing, constraining, or vetoing openxFactory installation stages | `openxFactory` |
| `client-content/` | Neutral tenant-layer content contracts — the three client content kinds (stricter-only policy overrides incl. budget envelopes + tracking granularity + the ratified auto-clear envelope; tenant-isolated memory buckets; reference-only integration boundaries) and the seedable `hermes_client_overlay`; canonical comparability validator; realized at `contract-v1.17` (consumers: the client policy wizard + hermes-install client seeding) | `openxFactory` |
| `hermes-domain-overlay/` | Neutral seedable domain-overlay contract — the `hermes_domain_overlay` schema (identity, approval scopes, authority boundaries with canonical `<domain.id>_owns` + no-overlap rules) and the `hermes_overlay_descriptor` role→path declaration with documented-convention fallback; self-testing examples; realized at `contract-v1.15` (consumer: hermes-install seeding materialization) | `openxFactory` |
| `omnigent/` + `policies/layer-vocabulary.yaml` | The Omnigent execution layer's domain-tier contract family — per-domain overlay payload (five neutral worker archetypes, generalized permission matrix with constitutional `execute_final_action`/`access_secrets` false, four credential tiers incl. `never_assignable`, `worker_profiles` whole-document payload, `stricter_rule_wins` composition) and the install manifest (hermes runtime manifest digest-pinned as single stack identity, one tenant / one domain / N subject workloads, authoritative workload registry, rendered-profile provenance) — plus the ratified canonical Subject/Tenant/Domain layer vocabulary with legacy mapping and frozen-identifier inventory; realized at `contract-v1.16` with per-file SHA-256 in `manifest.yaml` (the validator `scripts/validate-omnigent-contracts.py` and packaged examples/negative fixtures are commit-content-addressed, no per-file digest). First family with canonical vocabulary machine spellings from birth | `openxFactory` |
| `memory-gateway/` | Product-neutral xFactory Memory Gateway contracts, vocabularies, provider profiles, bindings, context packets, migration, usage, erasure, break-glass, and audit | `openxFactory` |
| `avatar-client/` | Neutral avatar-client (AVC) contract kernel — 8 JSON-Schema contracts, 9 closed registries, acceptance map, frozen `interface-lock.yaml` baseline, and conformance fixtures; realized at `contract-v1.7` with per-file SHA-256 in `manifest.yaml` (see `avatar-client/README.md`) | `openxFactory` |
| `hermes-runtime/` | Neutral Hermes customer-subject runtime contract family — topology/identity, trusted-scope authority/binding/approval/traceability records, the PostgreSQL 15/16 operational contract with the governed v1-to-v2 migration and quarantine, scoped v2 job/run/event lifecycle, supported-DomainxFactory regression denominator, and the Gate G0 consumer handoff receipt; governed by `hermes-runtime/contract-index.yaml` and realized (provider side) at `contract-v1.10` with the release digest inventory `releases/contract-v1.10.digests.yaml` (superseding `contract-v1.9`, whose immutable tag and `releases/contract-v1.9.digests.yaml` remain as provenance; see `hermes-runtime/README.md`) | `openxFactory` |
| `schemas/xfactory-document-*.schema.yaml` + `scripts/validate-document-catalog.py` | Neutral document-cataloging contract surface — six JSON-Schema contracts (immutable per-repository catalog snapshot, non-authoritative cataloger-recommendation evidence, namespaced topic-tag registry, owner override/disposition file, and the reusable opaque-locator and handling-gate `$defs` kernels) plus the strict validator; realized at `contract-v1.11` with per-file SHA-256 in `manifest.yaml` (the validator is a commit-content-addressed tool, no per-file digest). Reference examples at `examples/document-cataloging/`; adoption guidance in `docs/document-catalog-adoption.md` | `openxFactory` |
| `avatar-client-lab/` + adopted `examples/avatar-first-ui/fixtures/deterministic/` seeds | Neutral avatar-client-lab evidence surface — the P1 total avatar-state derivation table and the P10 22-capability-scenario register (gate (vi)/(ix)(a)/(ix)(b) sources), the 20 adopted deterministic fixtures closing the state-reachability denominator (P7/P8/P11/P12/P13), and the SCO-001-S05 successor deferral-discharge register `avatar-client/evidence-register.implement-avatar-client-lab.yaml`; realized at `contract-v1.12` with per-file SHA-256 in `manifest.yaml`. The `.md` prose companions and `avatar-client-lab/client-acceptance-map.yaml` are governed by the changelog / `check_client_lab_acceptance_map`, not per-file digests; the reference validators are commit-content-addressed tools. See `avatar-client-lab/README.md` | `openxFactory` |
| `schemas/xfactory-client-infrastructure-request.schema.yaml` + `schemas/xfactory-infrastructure-readiness-result.schema.yaml` + `scripts/validate-client-infrastructure.py` | Neutral client-infrastructure contract family — the durable `client_infrastructure_request` coordination record (six never-conflated identity-reference `$defs`, the three-mode `execution_binding` `client_managed\|managed_host\|opsxfactory_executed`, the closed 13-state `status` enum, embedded `handoff` acceptance record, digest-bearing `package_refs`, cancellation `child_acks`, `supersedes_request_ref`) and the signed/traceable `infrastructure_readiness_result` (never a bare boolean; `ready\|degraded\|not_ready\|unknown\|maintenance`, `valid_until`, per-check `mandatory`/`outcome`/evidence) plus the strict validator; realized at `contract-v1.13` with per-file SHA-256 in `manifest.yaml` (the validator is a commit-content-addressed tool, no per-file digest). Reference examples at `examples/client-infrastructure/`; governing role doc `docs/client-infrastructure-liaison.md` | `openxFactory` |

Planned contracts:

| Contract | Purpose | Initial Source |
|---|---|---|
| `pr-admission-packet.schema.yaml` | Evidence packet used before opening a GitHub PR | To define |
| `merge-readiness-report.schema.yaml` | Merge council readiness report contract | To define |
| `repo-boundary-release-map.schema.yaml` | Mapping between `openxFactory` release and install repo commits | To define |

### Native Contract Index And Pending Realization

This table indexes native contract artifacts whether published or still owned
by an active OpenSpec change. A row that names a `contract-v*` release is in
`contracts/manifest.yaml` and the matching changelog; an untagged active row
remains pending until its owning registration task realizes it. Bundle numbers
are allocated late under the
[Contract Versioning Policy](../docs/contract-versioning-policy.md).

| Contract | Purpose | Owning change |
|---|---|---|
| `schemas/pattern-ledger-*.schema.yaml` (five kinds: episode, outcome-label, recurrence-family, recurrence-forecast, crystallization-candidate) | Sensing contracts for recurrence crystallization — episodes as derived projections over existing audit/run/metering/label streams with default-deny consent tiers, append-only outcome labels (quality is a fold, never a stored verdict), tenant-scoped family register entries with recorded merge/split transitions, maturity-dated scored forecasts with declared cost-regime assumptions, and the nominate-never-spend crystallization candidate | `add-pattern-ledger` |
| `scripts/validate-pattern-ledger.py` + `examples/pattern-ledger/` | Canonical pattern-ledger validator: schema conformance (dependency-free 2020-12 subset checker) plus the named policy rules the shapes deliberately omit (consent-tiers, mutable-verdict, tenant-mismatch, transition-order, idempotency-missing/-family-mismatch, candidate-evidence, forecast-min-evidence, score-pairing); self-testing over 7 positive files (incl. the MVP packet-capture fixture corpus hand-derived from the real 2026-07-28/29 runs) and 7 indexed negatives | `add-pattern-ledger` |
| `schemas/crystallization-{decision,spec,build,consent}.schema.yaml` | Crystallizer contracts — the decision as the only path from candidate to spend (ceilings-before-valuation, deflation + survival discounting, shape-not-boolean outputs, not-yet ledger, frozen L0–L6 rung vocabulary), the episode-mined micro-spec (acceptance corpus with declared equivalence predicates, scope fence, effect class), the governed build record (gapless provenance, dry-run + leak-scan acceptance, budget caps, declared artifact residence per the rung→home lean), and the three-tier default-deny consent grant | `add-crystallizer-contracts` |
| `scripts/validate-crystallizer-contracts.py` + `examples/crystallizer/` + the additive `omnigent/omnigent-domain-overlay.schema.yaml` fields (crystallized-executor binding, `rung_ceilings`) enforced by the extended `scripts/validate-omnigent-contracts.py` | Canonical crystallizer validator (12 named policy rules incl. candidate-required, ceiling-exceeded, outcome-shape, braid-complete, ladder-maturity, counterexample-floor, byte-golden, effect-class-missing, automation-scope; self-testing 4 positives — the MVP corpus continuation: funded L3 decision, mined spec with a real counterexample, consent grants, illustrative build — and 9 indexed negatives) plus the omnigent authority-conservation subset rules (existing archetypes only, permissions/credential families never exceed the replaced configuration, ceiling-category uniqueness; 2 new overlay negatives) | `add-crystallizer-contracts` |
| `schemas/{crystallized-capability-registry,dispatch-record,adjudication-record,sentinel-policy,capability-health-report,savings-entry,calibration-score}.schema.yaml` | Capability-steward contracts — the registry record (proof-gated status spine mirroring the document lifecycle; artifacts digest-pinned while authority is live-read, D10; digests-never-payloads), the path-invariant dispatch record (six-cause fallback taxonomy, metered overhead), the shared parity/sentinel adjudication record (bidirectional verdict↔consequence pairing), the sentinel policy (strictly-positive floor), the capability-health report (auto vs contested findings; cost-ordered drift responses), and the sentinel-anchored savings entry + maturity-graded calibration score | `add-capability-steward` |
| `scripts/validate-capability-steward.py` + `examples/capability-steward/` | Canonical capability-steward validator (11 named policy rules: digests-only, status-transition, authority-status, demotion-bundle, effect-class-admission, fallback-cause, postconditions-required, provenance-required, sentinel-floor, savings-anchor, adjudication-pairing; self-testing 6 positives — the MVP corpus completion: shadow registry record, served/fence-miss/sentinel dispatch records, the ε=0.20-no-decay policy, a code-was-right adjudication, a health report with one auto and one contested finding, a sentinel-anchored savings entry + the first calibration score — and 10 indexed negatives) | `add-capability-steward` |
| `schemas/ideation-dashboard-snapshot.schema.yaml` | Deterministic ideation-area dashboard projection snapshot; staging-workbench staged-topic growth registered at `contract-v1.26` | `add-ideation-dashboard`, `add-staging-workbench` |
| `schemas/ideation-dashboard-snapshot-index.schema.yaml` | Snapshot index: the thin (repository, ref) locator the repository selector renders; registered at `contract-v1.26` | `add-dashboard-repo-selector` |
| `schemas/xfactory-workbench-model-catalog.schema.yaml` | doxBench approved-model catalog wire envelope (public allowlist: seven required base fields plus, since `contract-v1.38`, the three OPTIONAL routing-declaration fields that let an `auto` entry declare itself a ROUTING RULE over opaque catalog handles; empty = editor-only posture); registered at `contract-v1.27`, grown at `contract-v1.38` | `add-workbench-integrated-editor-chat`, `add-doxbench-editing-phase-b` |
| `schemas/xfactory-workbench-chat-turn.schema.yaml` | doxBench grounded chat-turn wire family (request / success / fixed redacted failure; exact content-hash identity, non-identity working_subject); registered at `contract-v1.27`, widened at `contract-v1.34` with a CO-RESIDENT second family (`workbench-chat-turn-v2*`) carrying the outline plus every loaded document, the DECLARED bound-buffer key on request and record, observed hashes keyed by buffer key, a buffer-key proposal target, and the selected-model metadata. Grown again at `contract-v1.40` with ONE optional property on the widened record, `context_packet` — the POSTURE (`full \| reduced`) the turn's bounded context packet was assembled under plus that reduction's own reason, so the ratified "with the reduced posture STATED" clause is readable by a consumer and showable to the human. Its absence means a producer older than `contract-v1.40`, never a full context. The v1 envelopes are byte-identical to their `contract-v1.31` bytes and keep validating; the v1 family is DEPRECATED at `contract-v1.34` with removal target `contract-v2.0` (see the schema's `deprecated_envelopes` and the CHANGELOG migration note) and is deliberately NOT widened by `contract-v1.40` | `add-workbench-integrated-editor-chat`, `add-doxbench-editing-phase-b` |
| `schemas/ideation-workbench.schema.yaml` | Gitignored user-assembled workbench reference-set manifest | `add-ideation-dashboard` |
| `schemas/ideation-possibles-register.schema.yaml` | Possibles-register consolidation `$defs` kernel (embedded in the cross-reference index); AI-derivation intake delta (`origin` + `derivation`) registered at `contract-v1.14` | `add-ideation-dashboard`, `add-possibles-derivation-lane` |
| `schemas/project-register.schema.yaml` | Repository → project → project-group navigation hierarchy (D10) | `add-ideation-dashboard` |
| `schemas/gate-action-record.schema.yaml` | Human-authenticated gate-console action audit record (D16/D17); create/document action growth, branch-session verbs, and the D23 `provenance` block registered at `contract-v1.26`; wheel commissions registered at `contract-v1.29`; abandoned-branch cleanup adds exact scope/evidence correlation and `prepared`/`completed` transaction state at `contract-v1.43` | `add-ideation-dashboard`, `add-workbench-bullseye-and-create`, `add-workbench-branch-sessions`, `add-wheel-action-verbs`, `fix-abandoned-session-cleanup-terminal-states` |
| `schemas/demotion-execution-receipt.schema.yaml` | Durable proof that an explicit demotion returned every planned artifact to the exact staged destination and removed the source change; paths are repository-relative and the receipt is written only after complete execution | `fix-abandoned-session-cleanup-terminal-states` |
| `schemas/gate-intent.schema.yaml` | Attributed request envelope for zero-write-authority dashboard/mobile actions; pending/applied/refused lifecycle and request-to-record linkage, first registered at `contract-v1.29` with the wheel verbs | `add-ideation-intent-plane`, `add-wheel-action-verbs` |
| `scripts/validate-ideation-dashboard-contracts.py` | Strict validator: schema conformance (FormatChecker-enforced), snapshot referential integrity, workbench recipe/override + committed-manifest guard, possibles-register id-uniqueness + transition legality, project-register single-parent hierarchy, gate-action kickoff-ratification precondition, exact cleanup evidence identity, and safe complete demotion receipts; content-addressed in the release inventory from `contract-v1.43` | `add-ideation-dashboard`, `fix-abandoned-session-cleanup-terminal-states` |
| `domain-ontology/` | Neutral ontology meta-contract family (thirteen kinds): content-addressed ontology packages with immutable namespaced identifiers, acyclic multi-parent specialization, and label/alias uniqueness; the `core/` xFactory semantic kernel (24 concepts + 9 relation primitives, DRAFT with pending adoption until the pilot packages resolve two adopters per term); by-reference external mappings with license classes and no mirrored content; append-only candidate records carrying model extraction-run identity; steward-attributed release records (a worker/agent-attributed publication fails); breaking/retiring migration maps with retained-version bytes; the bounded semantic-context artifact (closed-or-truncated term subsets, exact kernel+package pins, tenant-binding agreement — the Omnigent worker-scope seam); and the quality report with computable signals under the distinct-subject/distinct-tenant aggregation floor. Semantic plane only: closed shapes carry no effect/permission/grant field and no authority-plane instance reference | `add-domain-ontology-layer` |
| `scripts/validate-domain-ontology.py` | Canonical domain-ontology validator: schema conformance plus digest closure (fail closed on drift), ontology-family-only inventory, namespace/ID/label uniqueness, specialization acyclicity, relation domain/range resolution, exact kernel-import agreement, kernel adoption evidence at publication, source/steward completeness, mapping registration + license permitted-use, compatibility/migration/retention, subject-URN and endpoint privacy scans, aggregation-floor enforcement, reserved authority-field and authority-target rejection, candidate/release stewardship rules, semantic-context closure/pin/binding agreement, and the `domain_ontology` content-manifest cross-check; self-testing over 4 positive units and 37 indexed negatives (incl. paired-revision misclassification, council resolution, floor and maintenance-report rules), plus the `--readiness` generated-domain gate with a `--determinism` repeat-identity mode | `add-domain-ontology-layer` |
| `scripts/ontology-maintenance.py` + `scripts/ontology-release.py` | Stewardship tooling: deterministic trigger evaluation over governed maintenance inputs (append-only candidates + maintenance reports, privacy floor fail-closed) and the governed release transition (accountable-steward gate, migration evidence, quality gate with recorded reviewed exceptions, byte-identical retention, new line on breaking); proven by `scripts/test-ontology-stewardship.py` | `add-domain-ontology-layer` |
| `schemas/consent-instrument.schema.yaml` | Registered at `contract-v1.30`, amended at `contract-v1.33` (`contract_schema_version` 1 → 2, additive) — the `xfactory_consent_instrument` record kind, the authority-chain root: parties by rung (incl. estate hosts), scope with stated out-of-scope, delegation clauses, autonomy position, `authority_basis`, revocation right + SLA, opaque signed-original custody, the closed SIX-state lifecycle with declared aliases (`withdrawn` added at `contract-v1.33` as a second terminal state and a DISTINCT member, never an alias of `terminated`), amendment deltas, dependent-artifact references — including the named `governed_identity` kind with its `identity_removal_evidence` and `admission_withdrawal_evidence` siblings, so the cascade reaches a standing identity in a client's tenant rather than only its credentials — and the declared consent-profile mapping (or explicit `data_consent: none`). The RECORD envelope's `schema_version` stays `const: 1`: the growth is an added enum member plus optional properties, so no existing instrument becomes invalid | `add-consent-instrument`, `add-client-identity-roster` |
| `schemas/consent-instrument-class-registry.schema.yaml` | Registered at `contract-v1.30`, amended at `contract-v1.33` (`contract_schema_version` 1 → 2, additive) — the domain-owned CLOSED instrument-class registry: every class declares custody-anchor and execution-evidence kinds, `signature_phase` posture (false is the declared direct-to-executed skip), and per-domain status aliases, whose target enum now tracks the six-state lifecycle (a domain spelling MAY map to `withdrawn`; declaring `withdrawn` itself as an alias of `terminated` is nonconformant). No existing alias declaration becomes invalid | `add-consent-instrument`, `add-client-identity-roster` |
| `schemas/consent-purpose-model.schema.yaml` | Registered at `contract-v1.30` — the domain-declared purpose model the neutral purpose-resolution check (D4) resolves instrument purposes against; access SHAPES stay technical contracts owned elsewhere | `add-consent-instrument` |
| `scripts/validate-consent-instruments.py` + `examples/consent-instrument/` | Canonical validator published by exact commit with `contract-v1.30`: schema conformance plus lifecycle/alias discipline, custody rules, termination cascade-evidence and data-consent coherence, and purpose resolution against a domain purpose model (`--purpose`); self-testing over 5 positives, 5 indexed negatives, and 2 purpose probes | `add-consent-instrument` |
| `schemas/xfactory-idea-routing-record.schema.yaml` | Registered at `contract-v1.30` — Canonical cross-factory idea routing record (`routing.yaml`); one per unclassified, mixed, cross-domain, or claim-split idea | `add-cross-factory-ideation-routing` |
| `schemas/xfactory-idea-routing-reference.schema.yaml` | Registered at `contract-v1.30` — Reusable structured repository/path/revision reference `$defs` kernel (mirrors `xfactory-document-opaque-locator.schema.yaml`); no top-level envelope | `add-cross-factory-ideation-routing` |
| `schemas/xfactory-ideation-routing-index.schema.yaml` | Registered at `contract-v1.30` — Central Idea-ID allocation ledger (`ideation/routing-index.yaml`) | `add-cross-factory-ideation-routing` |
| `schemas/xfactory-ideation-organizer-recommendations.schema.yaml` | Registered at `contract-v1.30` — Immutable non-mutating ideation-organizer recommendation evidence | `add-cross-factory-ideation-routing` |
| `scripts/validate-ideation-routing.py` | Canonical validator published by exact commit with `contract-v1.30`. Strict validator: schema/vocabulary conformance, central Idea-ID and Claim-ID uniqueness, legal transitions, destination-owner acceptance, structured repository-reference resolution, paired-document identity, prospective legacy compatibility | `add-cross-factory-ideation-routing` |
| `openxwallet/*.schema.yaml` (six kinds: wallet record, custody registry, grant, grant exercise, distinct-holder constraint, subject attestation) + `openxwallet/openxwallet-custody.registry.yaml` | Registered at `contract-v1.31` — the neutral holder-agnostic wallet core: a wallet as a key REFERENCE with a declared custody model and never key material; authority as attenuated grants with monotonic narrowing; exercise requiring proof of possession rather than presentation; the CLOSED custody set stating what each model evidences and the authority it caps, with `evidences` DERIVED from two declared booleans so a readable key cannot claim an isolated key's authority; key-attributed audit; revocation propagating through derivation and checked at exercise; opt-in distinct-holder constraints; and the non-substrate rule preserving MedxFactory's two ratified wallet constraints | `add-openxwallet` |
| `openxwallet-agent-profile/openxwallet-agent-composition.schema.yaml` | Registered at `contract-v1.31` — the FIRST profile over the wallet core, a sibling family rather than a modification of it: an agent's declared composition hash WITH the component set it covers, each component declaring a `binding_mode` (`content` digests the component; `reference` covers a corpus's identity and governing configuration but not its row-level contents), plus declared-change revocation with no tolerance band | `add-openxwallet` |
| `scripts/validate-openxwallet.py` + `openxwallet*/examples/` | Canonical validator published by exact commit with `contract-v1.31`: schema conformance plus nineteen rules the shapes cannot express — key material at any depth (names AND values), the custody `evidences` derivation, unearned ceilings, custody collapse, custody capping grant authority, monotonic attenuation, one authority vocabulary read at run time from the canonical job envelope, posture/tier coherence, proof of possession and the absence a refusal names, verification failure versus unauthenticated request, attribution laundering, revocation checked at use, distinct-holder evaluation, the non-substrate rule, composition binding completeness, and declared-change revocation; self-testing over 16 positives and 33 intended-invalid negatives covering 11/11 requirements, with coverage closed in both directions | `add-openxwallet` |
| `schemas/xfactory-client-identity-roster.schema.yaml` | Registered at `contract-v1.33` — the neutral CLIENT IDENTITY ROSTER, two kinds behind one top-level `oneOf`: the roster FRAGMENT a domain publishes (one client as seen by one owning domain, every governed identity standing in that client's provider tenant, keyed on the five-element tuple of domain, admission surface, authority class, blast-radius unit and duty; verified admission with achieved scope, where a claimed-but-unevidenced verification is unrepresentable; structural scoping preferred over name-based; declared provider-forced breadth; and a fragment-scoped free-token legend), and the REPORT-ONLY drift finding that cites an entry when observed state departs from the declaration and mutates nothing. Declared placement: `credentials/client-identity-roster/<client_ref>.yaml` in the domain repository, one file per (client, domain) pair and a direct child of that directory; `scripts/validate-credential-contracts.py`'s skip-with-notice over that path is EXPECTED and BLESSED, because the canonical roster validator claims it | `add-client-identity-roster` |
| `scripts/validate-client-identity-roster.py` + `examples/client-identity-roster/` | Canonical validator published by exact commit with `contract-v1.33`, run from the pinned checkout against an explicit target repository and never copied into a domain repo: schema conformance plus the rules the shapes cannot express — five-element tuple uniqueness, legend completeness and single declaration, verified-admission/achieved-scope coherence, undeclared scope excess and undeclared reach, the name-understates-achieved-authority rule with its `declared_excess` cure, `mutate` without a ratified capability as an ERROR rather than a report, consent-instrument linkage, provider-forced breadth obligations, alias-pair observational identity, placement misplacement anywhere in the target tree, and drift-finding well-formedness; self-testing over 4 example YAMLs and 31 indexed negatives before it scans anything, with a registered probe missing its file, a file with no registration, a passing negative, a negative failing for the WRONG code, and a code firing without its pinned detail all themselves errors. A domain publishing no fragment exits 0 with an explicit notice | `add-client-identity-roster` |
| `schemas/xfactory-credential-contracts.schema.yaml` | FIRST registered at `contract-v1.33` — the five credential-contract record kinds promoted at DTN-004 (credential requirements, runtime capability grant, credential binding, credential broker contract, credential audit policy), shape only, with the semantic invariants owned by [`docs/credential-access-model.md`](../docs/credential-access-model.md). The schema was promoted without a manifest row, so the digest consumers are told to verify did not exist; `contract-v1.33` closes that gap and registers its one additive growth in the same cut — the OPTIONAL `issuance_preconditions` object on a credential requirement, a CLOSED vocabulary (`accepted_request_required`, `registered_active_subject`, `roster_drift_clear_required`) whose every value is `const: true`, because a precondition is declared or not declared and `false` would read as governance while asserting nothing | `promote-credential-contracts`, `add-client-identity-roster` |
| `schemas/ideation-cross-reference.schema.yaml` | Unified cross-stage cross-reference readiness index (source of truth `ideation/cross-reference.yaml`; `.md` is a generated projection); four-schema co-load, embeds the possibles-register kernel | `add-ideation-cross-reference-readiness` |
| `scripts/validate-ideation-cross-reference.py` | Strict validator: four-schema-registry conformance (FormatChecker-enforced), extension-fit citation resolution against promoted/active-change capabilities, min>=8 gate arithmetic, spread-conflict consistency, topic-entry id uniqueness; delegates register-entry shape/transitions to `validate-ideation-dashboard-contracts.py` | `add-ideation-cross-reference-readiness` |
| `scripts/render-ideation-cross-reference.py` / `scripts/bootstrap-ideation-cross-reference.py` | Deterministic YAML→Markdown projection renderer, and the one-time header-derived bootstrap generator that seeds `ideation/cross-reference.yaml` + `.md` | `add-ideation-cross-reference-readiness` |
| `worker-enrollment/` | Neutral worker-enrollment contract family, registered at `contract-v1.29` — one enrollment point serving both estates through two authentication modes (`host_identity` / `device_code`) as FIELDS of one request shape; the `worker_lease` authority record that carries no token field at all (leases over registrations, so staleness/revocation/trust are renewal decisions rather than facts on a machine); the grant with its estate-split runner package (fleet hard pin + sha256 + self-update disabled vs temp self-update, no pin) and its TRANSIENT `writeOnly` registration token; the renewal exchange whose response always carries the minimum-app-version floor; the OpsxFactory-owned policy instance shape; the audit record whose shape — no token/secret/key property, bounded free text — IS the redaction rule; and the `worker_removal_grant` remove-token issuance response (added by the 2026-07-26 amendment as task 2.5's contract half), which repeats that transient-token discipline for the remove token and carries NO registration token and NO runner package by shape, so drift repair removes a registration and never re-enrols a host | `add-worker-enrollment-broker` |
| `scripts/validate-worker-enrollment.py` | Canonical validator published by exact commit with `contract-v1.29`: schema conformance (FormatChecker-enforced, `$id`-keyed registry for the grant's embedded lease `$ref`) plus the cross-shape rules — no token/secret-shaped property or value in any record or lease, chunk-resistant (separator-stripped values, concatenated arrays and bounded flag maps) and class-filtered against the shared `avatar-client/redaction/` denylist; temp leases — AND temp removal grants, whose `binding.runner_group` is the remove token's blast radius — never bound into a standing execution-lane runner group (declared policy facts, else a fail-closed naming fallback that says so); the estate runner-package split, with the fleet pin checked against the policy's declared package; a MEANINGFUL floor on every renewal response; estate/subject/host-management/trust-tier coherence on all three shapes that carry the four facts; a device-code renewal holding no standing secret; lease expiry consistent with the cadence and short-lived registration AND remove tokens (checked on the clock, not asserted); and no standing execution lane accepting volunteered hardware | `add-worker-enrollment-broker` |
| `identity-brokering/*.schema.yaml` (six kinds: persona assertion, broker organization, actor-subject reference, identity link record, broker client declaration, surface adoption) | Registered at `contract-v1.37` — the neutral identity-brokering family: what any broker must assert about an authenticated human (issuing INSTANCE, stable opaque subject, display name, federated upstreams, organization memberships — a CLOSED ALLOW-LIST at every depth, so a role, group, grant, project, stack, layer or entitlement has nowhere to go and the never-mirror rule is enforced by the shape); organizations as company boundaries with `company_role: tenant \| served` bridged to the canonical layers (`tenant` -> `tenant`, `served` -> `subject`) read from `policies/layer-vocabulary.yaml` at run time, and `governed_record_refs` bounded at ONE closed item (the pointer-not-projection line); the STRUCTURED actor-subject reference with three provenance classes whose wrong combinations are unrepresentable (a `pre_broker_username` admits no issuer or subject and carries `presented_as_persona: false` as a required constant); explicit self-link or admin-approved merge as the ONLY two modes, each requiring its actor by shape, with attribute-match auto-linking unwritable and every pre-merge subject carried to its survivor; service clients declared as TRANSPORT through three required constants and no field for an actor role or membership-as-authority; and a surface's declared authorization posture where a write action cannot hide under the weak one and isolation escalates by broker INSTANCE with the contract silent on instance count. Keycloak is the realization being adopted and appears in no schema, enumeration or requirement | `add-identity-brokering` |
| `scripts/validate-identity-brokering.py` + `identity-brokering/examples/` | Canonical validator published by exact commit with `contract-v1.37`, run from the pinned checkout against an explicit target repository: schema conformance plus fourteen lettered rules (a)-(n) the shapes cannot express — the closed allow-list DERIVED FROM THE SCHEMA (local `$ref`s resolved, branches unioned) and walked over every property PATH so an unrecognized property is refused BY NAME rather than by denylist; one persona per human per broker instance across a corpus, including whitespace-padded upstream-subject evasion; explicit initiator or approver resolved on every link/merge and every pre-merge subject resolving to the survivor, with a merge approved by one of its own parties refused; no display name, address or upstream account name in an identifier position; credential-value detection BY CLASS with chunk reassembly, so a secret cannot be smuggled through a legitimate free-text field; posture/write-action coherence and the decision-point locator walk (a `governed_layer` declaration naming the broker's own admin API is refused); a retired shared credential; and the layer-vocabulary, linking-basis and authorization-target vocabularies READ AT RUN TIME rather than restated. Self-testing over 14 positives and 41 indexed negatives, 9/9 requirements covered in both directions, with 22 finding codes red-proven | `add-identity-brokering` |
| `trust-anchor/*.schema.yaml` (seven kinds: trust anchor, certificate record, issuance evidence, dependent binding, renewal record, revocation propagation, conformance declaration) + `trust-anchor/chain-custody-registry.schema.yaml` + `trust-anchor/trust-anchor-chain-custody.registry.yaml` | Registered at `contract-v1.37` — the neutral trust-anchor family, product-agnostic because two realizations are real (live Intune Cloud PKI canary; OpenXPKI planned for the Opensoft production core): systems trust ANCHORS and a certificate only derivatively, with chain position coherent or refused and an anchor's window bounding its subordinates; trust with ONE representable basis (`held_anchor_record`) and standing `checked_at_use`, so neither a certificate's own strength nor issuance-time validity can be recorded as current trust; issuance stating what must be ESTABLISHED with a declared two-member floor whose weaker form is a CONJUNCTION and whose unestablished case forbids asserted provenance by shape; dependent bindings enumerated against the certificate so a renewal's rebind set is computable BEFORE the renewal, joined on the key GENERATION; renewal where "successful with an unevidenced dependent" is unrepresentable as a SCHEMA constraint and the failure is attributed to the ISSUING WORKFLOW by constant; revocation riding openxWallet's derivation mechanism by constant, with an arithmetically checked window and an unevidenced closed window recorded as `incomplete_open_exposure`; a conformance declaration CLOSED over the eight obligations with per-entry `declared_at`; and the closed chain-custody registry pair whose `evidences` is DERIVED from two booleans and whose every member maps to an `openxwallet` custody member resolved at run time, so the two sets cannot drift into two custody models (operator escrow is a deliberate non-member — a relationship on the credential record, not a tier) | `add-trust-anchor` |
| `scripts/validate-trust-anchor.py` + `trust-anchor/examples/` + `tests/trust-anchor/` | Canonical validator published by exact commit with `contract-v1.37`: schema conformance plus 34 lettered rules the shapes cannot express — key material by name AND value including reversible encodings; the `evidences` and `assurance_ceiling` derivations recomputed, with a record's ceiling capped by any anchor in its chain whose key is readable by its using host; chain resolution and anchor-window bounding, with a missing anchor NAMED; the chain-custody registry held to `openxwallet-custody.registry.yaml` at run time; declared-shortfall references resolved and refused when the obligation is recorded satisfied or was declared later than the citing record; a family-operated authority refused the excuse of its own shortfall; the renewal's dependent set required to equal the CERTIFICATE's enumeration; rebind status compared against the certificate with no renewal record in the way; the revocation window's arithmetic and its anchor-transitive closure over the corpus; and eight-obligation coverage checked in both directions. Two layers (packaged self-test, then a repo scan), exit 0/1/2, self-testing over 34 positives and 65 indexed negatives at 8/8 requirement coverage with 50 non-`schema` finding codes red-proven. CI wiring is the per-family convention — a canonical validator plus `tests/trust-anchor/` under pytest (validator exit code and reported corpus counts; every negative adjudicated independently; the declaration-perimeter rules whose cases need two records that disagree) | `add-trust-anchor` |

Reference examples for the ideation-dashboard family (29 valid + 50 invalid
fixtures + 8 transition pairs) live at `examples/ideation-dashboard/`;
`scripts/validate-ideation-dashboard-contracts.py` self-tests them, validates a
given file/directory by kind detection, runs register transitions via
`--transition OLD NEW`, and scans the checkout for committed workbench manifests.
The wheel-expanded gate-intent and gate-action-record surface is registered at
`contract-v1.29`; remaining untagged family rows retain their owning task.

Reference examples for the ideation-routing family (8 valid + 8 invalid
fixtures, one violation per negative file) live at
`examples/ideation-routing/`; `scripts/validate-ideation-routing.py`
self-tests them (schema/`kind`-or-fragment validation) and additionally
validates any real `ideation/routing-index.yaml`, `ideation/**/routing.yaml`,
and `health/ideation-organizer/**/*.yaml` artifacts under a given checkout,
reporting absent paths as skipped rather than passed. See
`openspec/changes/add-cross-factory-ideation-routing/specs/ideation-routing/spec.md`
for the requirements these schemas realize. Per this section's rule, these
entries move to `contracts/manifest.yaml` and `contracts/CHANGELOG.md` when
`add-cross-factory-ideation-routing` archives (its task 8.4).

Reference examples for the ideation-cross-reference family (1 comprehensive
valid index + 2 negatives — one schema-layer, one validator-layer) live at
`examples/ideation-cross-reference/`; `scripts/validate-ideation-cross-reference.py`
self-tests them (four-schema co-load), then scans the checkout for the real
`ideation/cross-reference.yaml`. The index's `.md` sibling is a generated
projection produced by `scripts/render-ideation-cross-reference.py`; the initial
YAML+MD were seeded by `scripts/bootstrap-ideation-cross-reference.py` (task 2.4).
See `openspec/changes/add-ideation-cross-reference-readiness/specs/ideation-cross-reference/spec.md`
for the requirements these realize. Per this section's rule, these entries move
to `contracts/manifest.yaml` and `contracts/CHANGELOG.md` when
`add-ideation-cross-reference-readiness` archives (its task 5.2).

Reference examples for the worker-enrollment family (11 positives — both estates
end to end, a renewal carrying the floor, a below-floor refusal, the refusal
audit record, a revocation record, a drift-repair and a revocation-driven removal
grant, and the policy instance — plus 27 negatives,
one violation per file, each declaring its `# expected_failure:` reason and, where
a finding code alone is too coarse an anchor, an `# expected_failure_detail:`
substring that pins the fixture to the invariant it is named for) live beside the
schemas at
`contracts/worker-enrollment/examples/`, the packaged-fixture convention the
`hermes-domain-overlay` and `client-content` families use.
`scripts/validate-worker-enrollment.py` self-tests them and additionally scans a
given checkout for real enrollment artifacts, excluding that examples tree. Family
overview, the two authentication modes, and the redaction rule:
[contracts/worker-enrollment/README.md](worker-enrollment/README.md); the
requirements these schemas realize are in
`openspec/changes/add-worker-enrollment-broker/specs/worker-enrollment-broker/spec.md`.
The seven schemas and their raw-byte digests are registered in
`contracts/manifest.yaml` and `contracts/CHANGELOG.md` at `contract-v1.29`
(`add-worker-enrollment-broker` task 1.11); validator and fixtures are pinned
by the exact release commit.

## Contract Manifest

The machine-readable inventory is:

```text
contracts/manifest.yaml
```

Each entry records:

- source path
- source compatibility reference
- copied schema or policy version when available
- intended consumers
- adapter ownership rule

## Version Pinning

Contract consumers must pin compatibility in one of these forms:

```yaml
openxfactory_contract_ref:
  repo: opensoft/openxFactory
  commit: <git-sha>
  contract: contracts/<contract-name>
  version: <semantic-version-or-date>
```

or:

```yaml
openxfactory_contract_ref:
  repo: opensoft/openxFactory
  tag: <release-tag>
  contract: contracts/<contract-name>
```

## Adapter Rule

An install repo may keep implementation-specific files derived from a contract,
including:

- generated clients
- service adapters
- smoke-test fixtures
- pinned schema copies
- runtime validation configs

Those files are not canonical unless the contract explicitly delegates
ownership. They must link back to the corresponding `openxFactory` contract.

## Breaking Changes

A contract change is breaking when an existing Hermes or Omnigent adapter,
worker, smoke test, or workflow artifact would fail without coordinated
changes.

Breaking contract changes must be one of:

- split from adapter migration and staged behind compatibility support
- explicitly approved as a breaking change by Hermes governance
- paired with install repo PRs that update adapters and smoke tests

## Migration Rule

Contract migration is copy-first:

```text
existing install repo schema
  -> copy or summarize canonical contract into openxFactory/contracts/
  -> add version and compatibility notes
  -> update install repo adapter to reference canonical contract
  -> remove or mark legacy copies only after replacement checks pass
```

Do not move runtime adapters, generated clients, or smoke fixtures into this
directory unless they are part of the canonical contract itself.
