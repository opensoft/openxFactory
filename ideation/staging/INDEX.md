# Staging Index

Status: staged
Kind: register
Repository context: openxFactory
Purpose: single kept-current inventory of every topic under `ideation/staging/`
— one row per topic, one detail section per topic. This file is the source of
truth for what is staged; `ideation/README.md` links here instead of
duplicating the list.

## Maintenance rule

Update this index in the same commit as any of:

- **New topic folder** created under `ideation/staging/` — add a row to the
  table and a detail section below.
- **File added to or removed from** an existing topic — update its Files list
  and Target capabilities if they changed.
- **Partial promotion** (some files move to an OpenSpec change's
  `supporting-docs/`) — drop the moved files from the Files list; keep the row
  if any staged file remains.
- **Full promotion** (no files remain staged) — delete the row and detail
  section here; the pointer belongs in `ideation/README.md`'s "Active
  proposals promoted from staging" list instead.
- **Demotion** (a proposal returns to staging for continued design) — the
  reverse of promotion: the change's artifacts come back as the topic (its
  OpenSpec docs into the topic's `openspec/` drafts), the row and detail
  return here, and the README promoted-list pointer is removed.

## Draft-proposal workspace convention

A staging topic may carry an `openspec/` subfolder holding working drafts
of its future proposal — proposal, design, tasks, and spec-delta slices,
each `Status: draft` with a "Draft slice of:" pointer to the topic's
primary doc. Drafts iterate freely in staging; at the proposal gate they
move to `openspec/changes/<change-id>/` (front-matter restored, draft
headers stripped) and the topic's source docs follow into
`supporting-docs/` per the document lifecycle. Adopted 2026-07-13 (Brett),
first used by ideation-dashboard; formalizing the convention in the
document-lifecycle spec is a candidate for the next lifecycle change.

## Topics

| Topic | Delta (target capability) | Files | Readiness |
| --- | --- | --- | --- |
| [hermes-stack-topology-per-client](#hermes-stack-topology-per-client) | ADDED neutral `request-intake-and-admission` + MODIFIED topology contract (per-client stack-vs-layer rule made explicit) | 1 | Ready to iterate — cardinality verified against the runtime spec and the live stack; RESOLVED 2026-08-08: each client gets its own stack (client = Tenant), so onboarding is a stack install; the ledgerx fixture + its bound HCS-002-S03 scenario are stale and owe an OpenSpec correction. BLOCKED on the (a) realize-intake-at-Tenant-Hermes vs (b) stand-up-an-Opsx-stack fork; cross-repo input 2026-08-09: OpsxFactory staged its governance trilogy (tenant-request-intake → hermes-approval-envelopes → tenant-operating-postures) designing the fork's intake/approval side; update 2026-08-10: trilogy exit 1 promoted and RATIFIED as OpsxFactory `add-request-intake-boundary` (intake realized at the Tenant layer — fork branch (a) side), Speckit implementation in flight |
| [mobile-dashboard-surface](#mobile-dashboard-surface) | `avatar-first-ui` realization (possibly a small ADDED requirement) | 1 | Ready to iterate — the layer defaults are already ratified; main forks: shell platform vs the frozen AVC ports, sequencing vs `avatar-pilot-hardening` |
| [workstation-app-shell](#workstation-app-shell) | `avatar-first-ui` realization (possibly a small ADDED requirement for the workstation shell) + MODIFIED `ideation-dashboard` (the local serve becomes app-managed) | 1 | Ready to iterate — layer defaults already ratified and the motivating defect verified; load-bearing content is the Worker Host App boundary (two OS principals, one shell) and codexFactory's missing subject surface; 5 open questions, the shell-platform fork blocks implementation |
| [avatar-pilot-hardening](#avatar-pilot-hardening) | ADDED `avatar-pilot-hardening` | 1 | Blocked — last successor; gated on `qualify-avatar-live-voice` + the client lab landing, plus its own open forks |
| [ideation-action-plane](#ideation-action-plane) | ADDED `ideation-intent-plane`; MODIFIED `document-lifecycle` (gates happen on main); fragment 2: MODIFIED `lifecycle-notebook-projection` (Drive membrane) | 2 | Exit 1 raised at this gate (`add-ideation-intent-plane`); fragment 2 blocked on the Drive↔NLM markdown-ingestion spike |
| [client-credential-escrow-registry](#client-credential-escrow-registry) | MODIFIED `credential-contracts` (escrow registry + break-glass custody; possibly a sixth record kind); touches `client-infrastructure-liaison` | 1 | Ready to iterate — design inputs settled with Brett 2026-07-19; 6 open questions (delta shape + break-glass topology hardest); first consumer live (opensoft self-client QA install) |
| [client-layer-tuning](#client-layer-tuning) | MODIFIED client scaffold (`roles/` + FAO + `cost_reporting_steward`); ADDED client content schemas + `validate-client-content`; wizard verb in hermes-install | 1 | **COMPLETE 2026-07-24** — all three exits ratified, realized, archived (2a contract-v1.17 + canonical spec `client-layer-tuning`; 2b codexFactory defaults; 2c wizard + unified client seeding). The opensoft tenant is tuned and seeded live (phase-2 evidence note). Primary doc + drafts retained as provenance |
| [context-compression-runtime](#context-compression-runtime) | ADDED `context-compression-runtime` (worker-lane compression stage + RAM-only local-store rule + upstream-exclusion obligation + three-tier audit model + per-domain egress-capture knob) | 1 | Ready to iterate — design + headroom v0.32.0 source audit locked with Brett 2026-07-25/26 (RAM-only CCR, audit moved to envelope/transcript/egress tiers); exit gated on the codexFactory-lane pilot in Omnigent-Install producing measured savings |
| [dashboard-repo-selector](#dashboard-repo-selector) | MODIFIED `ideation-dashboard` (repo selector, (repository, ref) snapshot source, runtime fetch + baked fallback, refresh affordances, dispatchable publication) + ADDED snapshot-index contract; later ADDED runtime capability (neutral install-shipped ideation surface, DTN path) | 1 | **Proposed 2026-07-26** as `add-dashboard-repo-selector` (exit 1) — twelve decisions locked with Brett 2026-07-25/26 (runtime plane is the goal, planes separate, per-repo snapshots + index, sparse wheels, bake the app not the snapshot, baked snapshot demoted to fallback, two refresh bindings, off-cycle publication is CI-only, (repository, ref) keying, displayed freshness, branch snapshots never published); neutral-vs-override fork + data-source ratification deliberately open; exit 2 (runtime plane) still staged |
| [dashboard-project-scoping](#dashboard-project-scoping) | MODIFIED `ideation-dashboard` (create-project commission, project-scoped selection, merged cross-repo projection, per-tile repository binding); additive gate-intent / gate-action-record growth | 1 | **Decision round complete 2026-08-06** — D1–D8 locked with Brett, ZERO open questions: true MERGED all-repos view (D1), register writes via COMMISSION (D2), L3 per-tile binding PROCEEDS as its own change (D3), projects only (D4), local register dev-authoritative then derived cache under the tenant-catalog twin (D5), THREE sequenced exits (D6: `add-project-scoped-selection` → `add-project-merged-projection` → `add-project-tile-repository-binding`), register split by role (D7 — core/domains/medx-clinical/installs), repository membership MULTI-PARENT (D8, ruled during exit-1 realization — a repo may live in many projects; snapshot keeps a first-declaring PRIMARY + additive `projects` list; MedxFactory joins medx-clinical); merged-view rules D9–D11 (view-side cluster union by topic tail; composed views read-only + "open in <repo>" jump; project aggregates derived from the register). header redesign D12–D15 ("Opensoft openDox"; project dropdown with New Project first, last-used default; repo filter popover; `edit-project` membership commissions). **Exit 1 proposed, RATIFIED, and REALIZED 2026-08-06 as `add-project-scoped-selection`; exit 2 proposed 2026-08-06 as `add-project-merged-projection` (awaiting ratification); header redesign proposed 2026-08-06 as `add-opendox-project-header` (awaiting ratification)** |
| [workbench-branch-sessions](#workbench-branch-sessions) | MODIFIED `ideation-dashboard` (branch-per-tile working state, commit-per-gate-action, session-local snapshots, PR-as-save `open-pr` verb); MODIFIED `lifecycle-notebook-projection` (per-session notebooks sync from the branch worktree; canon notebooks stay main-only) | 1 | **RATIFIED 2026-07-26** as `add-workbench-branch-sessions` (proposed and ratified the same day, after a 5-lens adversarial review and a rename-completeness audit) — TWENTY-TWO decisions (design D1-D22; D22 is the post-ratification `open-pr` push-identity ruling, 2026-07-26) and **ZERO open questions** — the change carries no parked decision; SEQUENCED strictly after `add-dashboard-repo-selector`, whose (repository, ref) seam it consumes; local plane only until intent-plane §4 |
| [codexfactory-domain-hermes-content](#codexfactory-domain-hermes-content) | codexFactory `hermes/domain/` content (changes A + B) + Omnigent overlay extension in lockstep | 1 | **COMPLETE 2026-07-23** — both changes ratified, realized, archived: change A 2026-07-22 (roles + policies + closure + Omnigent lockstep) and change B 2026-07-23 (mixes, councils, escalation, memory, catalog); canonical spec `domain-hermes-content` carries all nine requirements. The Omnigent extension rode the `add-omnigent-domain-overlay` realization. Primary doc + openspec/ drafts retained as provenance. Change B COMPLETE — ratified + archived 2026-07-23 (`archive/2026-07-23-add-domain-hermes-councils-and-memory`) |
| [github-administration-plane](#github-administration-plane) | MODIFIED `roles-authority-model` (neutral App-identity tiers); new OpsxFactory-owned `github-administration` capability | 1 | COMPLETE 2026-07-15 — both exit changes ratified, realized, archived (2026-07-14-add-github-app-identity-tiers, openxFactory; 2026-07-15-add-github-administration-workflow, OpsxFactory); live rollout done, 2026-07-10 incident closed; primary doc retained as `superseded` provenance |
| [layer-content-materialization](#layer-content-materialization) | ADDED neutral `hermes_domain_overlay` contract + `overlay_path` (openxFactory); hermes-install seeding increment 2 (`layer_content` kernel + materialization) | 1 | **COMPLETE 2026-07-23** — both exits ratified, realized, archived: `add-hermes-domain-overlay-contract` (openxFactory, `contract-v1.15` tag verified) and `add-layer-content-materialization` (hermes-install PR #6 merged 696ec48, archived 2026-07-23; capability spec carries increments 1+2). Deferred increments 3–6 + gate wiring recorded in the capability spec; primary doc retained as provenance |
| [layer-vocabulary-machine-migration](#layer-vocabulary-machine-migration) | MODIFIED `layer-vocabulary` + hermes-runtime v2→next-major identifier migration + domain-stack schema major | 1 | Dormant by design — deferral artifact for `adopt-subject-tenant-domain-vocabulary` tasks 3.1–3.3 (filed 2026-07-23); rides the next major contract bundle, never causes it; Ops/Adx prose sweeps runnable earlier |
| [medxfactory-domain-hermes-content](#medxfactory-domain-hermes-content) | MedxFactory `hermes/domain/` content (changes A + B) + Omnigent `directed_by` lockstep + overlay-manifest digest re-pin | 1 | **Change A COMPLETE 2026-07-29** — authored, ratified, realized, and archived the same day (`archive/2026-07-29-add-domain-hermes-roles-and-policies`; canonical Medx spec `domain-hermes-content`, 6 requirements): eight personas incl. the dedicated ontology-steward, eight medical policy files, the v1.15 overlay with a proven 43-item two-way `medx_owns` closure, `directed_by` on all 11 workers with the manifest re-pinned (omnigent-install fixture digest flagged stale to its own change), and the v13 ontology scaffold landed DRAFT (ruled stewardship policy, explicit content manifest incl. `domain_ontology`, canonical validators in `make validate`, readiness `domain_scaffold_required` pending Domain Hermes publication). **TOPIC COMPLETE — change B realized 2026-07-29, archived 2026-07-30** (`archive/2026-07-30-add-domain-hermes-councils-and-memory`; the canonical Medx `domain-hermes-content` spec carries all TWELVE requirements; MedxFactory is the second domain complete on BOTH layers — one params file from a deployable medical stack pending the flagged omnigent-install fixture digest refresh and the governed ontology publication: review-ensemble mixes with the stated convergence-flow boundary, MxD-MRR formalized with the ontology seats and the three-gate cross-layer flow, escalation elevation preserving the stub items, gateway-vocabulary memory boundaries, `medx_practice_catalog` with the four ruled seeds). (roster DECIDED the same day — decision round with Brett): the derived seven personas PLUS a dedicated ontology-steward (eight total; accountable ontology steward per ratified `add-domain-ontology-layer`); MxD-MRR domain-owned only; convergence flow + review mixes; content manifest declared explicitly incl. `domain_ontology`. No external gates (omnigent overlay realization archived at contract-v1.16) |
| [proposal-origin-contract](#proposal-origin-contract) | none yet — retained rationale for a future regulated-traceability profile | 1 | Held as read-only evidence; the origin contract itself was promoted from this topic 2026-07-12 (pointer in `ideation/README.md`'s promoted list) |
| [worker-host-app](#worker-host-app) | ADDED `worker-host-manifest` + `bench-manifest` (first-consumer drafts in Omnigent-Install, DTN path); realization app in Omnigent-Install + Intune packaging in OpsxFactory | 2 | Ready to iterate — build decision by Brett 2026-07-23; realization under way (substrate steps 1–2 merged); 7 open questions (Omni-001 admin path + SYSTEM-context WSL distro registration, runner-under-virtual-account, bench-manifest home hardest) |
| [worker-enrollment-broker](#worker-enrollment-broker) | ADDED `worker-enrollment-broker` (neutral enrollment/lease contract); realization = standalone broker service (home DECIDED: a new Opsx-owned repo, container app on the platform subscription, NOT the QA AKS cluster) + Omnigent-Install (registration-via-broker, lease renewal) + OpsxFactory (App key, policy, temp runner group) | 1 | **Proposed 2026-07-26** as `add-worker-enrollment-broker` (exit 1) — 7 rulings locked with Brett 2026-07-26 (broker-first standalone, two auth modes, lease + fail-closed version floor, fleet hard-pin vs temp self-update, segregated temp group + trust tier) carried as decided context; all 10 open questions carried as design decisions D1–D10, and **all ten ADOPTED AS DECIDED with Brett's approval of the change on 2026-07-26** — D1 (broker home + hosting) no longer blocks the first realization; the contract (phase-1 tasks 1.1–1.10 + 1.12) is REALIZED, shipping six schemas + a canonical validator, the broker service / Omnigent-Install / OpsxFactory realizations are named successor changes, and the heartbeat/readiness projection is left to a coordinated three-places change |
| [session-notebook-reconciliation](#session-notebook-reconciliation) | MODIFIED `lifecycle-notebook-projection` (a fourth sync mode: reconcile the `xf-session-` namespace against live sessions, fail-closed, report-only by default) + MODIFIED `ideation-dashboard` (a third retirement route for a session that ended without one) | 1 | Ready to iterate — organized 2026-08-10 from the `session-teardown-notebook-coupling` brainstorm on the day two live orphans had to be deleted BY HAND; the five claims are settled (forward-derived detection, fail closed on incomplete knowledge, scoped to this workspace's session repositories, report-only default, `retire` never `delete`); 3 open questions, none blocking (is an orphan evidence worth an import pass; whether hand teardown should be narrowed; cadence) |
| [subject-establishment](#subject-establishment) | ADDED neutral `subject-establishment` (two artifact kinds: neutral subject design + platform realization; provenance-graded fact set; reference-archetype lifecycle; conformance tiering; apply-and-verify-by-read-back; audit-lift mirror); DTN-017 | 1 | Ready to iterate — named by Brett 2026-07-28 from LedgerxFactory's company-provisioning work (first instantiation, in flight); **Second consumer DECIDED 2026-07-28: codexFactory new-project** (`project` is already a first-class codex subject kind; `check_profile`/`reviewer_group` are neutral-design elements wearing domain names). It surfaced the finding Ledgerx could not: for codex the DESIGNING domain and the APPLYING administrator are different factories (GitHub administration is Opsx's), so the realization artifact must be handoff-shaped — likely the same seam as `deployment-handoff-boundary`. 6 open questions; exit gated on Ledgerx reaching proposal |
| [qualify-avatar-live-voice](#qualify-avatar-live-voice) | ADDED `avatar-live-voice` (incl. the reserved AVC-09/AVC-10 contracts) | 1 | Blocked — 5 open questions (credential custody + spend cap and activation-gate scope hardest); also gated on a released client from the lab |
| [tier2-council-clearance-pattern](#tier2-council-clearance-pattern) | ADDED neutral `council-clearance-gate-rule` pattern contract (tier-2 council-clearance template: clearable set, never-clearable floor, anti-normalization, activation gate) | 6 | **Demoted back 2026-08-05** — proposed and demoted the same day (Brett's propose commission, then Brett's reasoned demote: "rule-of-three trigger not fired — no second consumer has named itself"); the full draft packet (proposal, design, tasks, spec delta) sits in the topic's `openspec/` workspace per the draft-proposal convention, ready to re-cross the gate the day a second consumer appears. Organized 2026-08-05 from accepted possible `pos-derived-reusable-tier-2-council-clearance-pattern-beyond`; the first full possible→staged→proposed→demoted traversal of the wheel verbs |
| [recurrence-crystallization](#recurrence-crystallization) | ADDED `pattern-ledger`, `crystallization-decision`, `crystallization-build`, `crystallization-consent`, `crystallized-capability-registry`, `crystallization-dispatch`, `capability-health`; MODIFIED `omnigent-domain-overlay` (crystallized-executor class + rung ceilings) | 2 | Ready to iterate — organized 2026-07-29 from the 19-doc brainstorm packet (2026-07-28) with D1–D11 + V1–V2 locked (authority conservation; artifacts digest-pinned while authority status is live-read (D10); v1 dispatch admits only pure/idempotent effect classes (D11); neutral schemas first (D6)); MVP family DECIDED: packet-capture mechanics at L3, evidenced by two same-shape runs on 2026-07-28; cross-tenant deliberately out of wave (stays brainstorm); exit = add-pattern-ledger (realized contract-v1.19, ARCHIVED 2026-07-29; fragment under the archived change's supporting-docs/) → add-crystallizer-contracts (realized contract-v1.20, ARCHIVED 2026-07-29; fragments under the archived change's supporting-docs/) → add-capability-steward (realized contract-v1.21, ARCHIVED 2026-07-30; fragment under the archived change's supporting-docs/). ALL THREE EXITS ARCHIVED — the staged remainder is the dials register |
| [agent-wallet-identity](#agent-wallet-identity) | ADDED neutral `openxwallet` (holder-agnostic core: key reference + declared custody, attenuated grants as the authority primitive, proof of possession, custody capping authority, key-attributed audit, revocation propagation, distinct-holder constraints, non-substrate rule) + ADDED `openxwallet-agent-profile` (composition + declared-change revocation + authority as grant scope); composes with `roles-authority-model` + `credential-contracts`; `openxVault` consumes the grants | 1 | **PROPOSED 2026-08-06 as `add-openxwallet`** (topic folder keeps the `agent-wallet-identity` name; the change was renamed on restructure). Restructured the same day after Brett asked whether the Medx/Ledgerx intersection lives in openxFactory — it did not, so the change now adds a HOLDER-AGNOSTIC core with GRANTS AS THE PRIMITIVE plus an agent profile, rather than a wallet shaped like an agent binding authority to a second vocabulary. **RATIFIED 2026-08-07** with all three decisions: grants as the primitive, the core holder-class agnostic, and key custody DECLARED and CAPPING authority. **REALIZED 2026-08-07** by Speckit feature `006-openxwallet-contracts`: two neutral contract families (`contracts/openxwallet/` core + `contracts/openxwallet-agent-profile/` as a sibling, so the profile seam is structural), `scripts/validate-openxwallet.py`, and a corpus of 16 positives and 33 negative confirmations covering 11/11 requirements, registered at `contract-v1.31`, and **ARCHIVED 2026-08-08** as `2026-08-08-add-openxwallet` with both capabilities promoted (`openxwallet` 8 requirements, `openxwallet-agent-profile` 3). The topic row stays because the staged fragment remains on disk as provenance carrying the deferred material — batteries, measured drift, qualification tiers and delegation chains, each a named successor gated on a consumer of its own. The feature settled the two decisions the ratification left it: the closed custody set is three members with `evidences` DERIVED from two declared booleans and enforced — so a readable key cannot claim an isolated key's authority, and the collapse is structurally impossible rather than discouraged — and the composition component set covers a retrieval corpus BY REFERENCE (identity plus governing configuration) rather than by contents, which dissolves the include-or-exclude binary. The closed custody enumeration and what each member evidences are now contract content rather than an implementation detail. Organized 2026-08-06 from the 2026-07-15/16 `agent-certification-wallets` brainstorm at the moment a consumer named itself (LedgerxFactory posting segregation of duties, `ledgerx:staging:posting-segregation-of-duties`). Scoped BELOW the brainstorm on purpose: identity + proof + declared-change decert first; batteries, measured drift, qualification levels and delegation chains are named successors, each gated on a consumer. Two ratified Medx specs constrain the design (a wallet address MUST NOT be identity proof; custody stays wallet-neutral), which makes verification rather than registration the load-bearing requirement. 6 open questions — key custody is hardest, since it decides whether a signature proves the AGENT acted or only that the HOST did |
| [manager-review-approval-scope-kind](#manager-review-approval-scope-kind) | MODIFIED `hermes-domain-overlay` (additive `approval_scope_kinds` vocabulary extension — a dedicated `manager_review` kind) | 1 | Registered 2026-08-10 — origin is `xFactory-Hermes-Install` feature `011-three-layer-manager-review-gate`'s implementation plan (tension T2), ruled "register now" by Brett Heap the same day; the live gate proceeds on the `engineering_intent` fallback in the meantime; 2 open questions (envelope-vs-overlay home, naming/scope grain), neither blocking |
| [openxdox-install-app-provisioning](#openxdox-install-app-provisioning) | MODIFIED `credential-contracts` (or a new `install-app-provisioning` capability: two-App manifest provisioning + naming convention + apply-repo home); realization in Omnigent-Install (installer) + codexFactory (manifests + install docs) | 1 | Ready to iterate — named by Brett 2026-08-14 from the openXdox dispatch-migration's manual App toil; GitHub-capability verified (no app-creates-app API; the App Manifest flow is the mechanism, Apps tenant-owned); 6 claims settled (two Apps stay two, manifest flow, tenant-owned, globally-unique-name convention, small apply-workflow repo, tenant only sets the content-App scope); 5 open questions (contract home + managed-vs-self-hosted flow hardest); gated on the QA dispatch migration completing |
| [substantive-review-lane-questions](#substantive-review-lane-questions) | tracks `roles-authority-model` (MODIFIED by in-flight change `add-substantive-review-lane`, PR #178, draft) — no capability delta of its own | 1 | Registered 2026-08-15 — origin is Brett's direction to track the ad-hoc-authored proposal's five declared-open, not-decided questions (this topic is post-proposal tracking, NOT the proposal's origin; the proposal's own `.openspec.yaml` records `kind: ad_hoc`); six decided principles carried as settled context, not reopened; 5 open questions (rollout order, non-engineering persona home, company-policy-lead per-PR seating, per-repo ruleset shape, risk-tier taxonomy), none blocking the pilot; SEQUENCED after the doxBench UI sprint (Brett 2026-08-15) — after `doxbench-editing-model` Phase A, `staged-topic-outline-template`, and Phase B, so the review lane catches the workbench's steady state rather than blocking the sprint |
| [staged-topic-outline-template](#staged-topic-outline-template) | MODIFIED `document-lifecycle` (the primary-fragment template contract: required sections, round-trip-on-demote refresh rule, section provenance, marker usage) and MODIFIED `ideation-dashboard` (the doxBench outline tab renders the template + gains an add-section affordance) | 1 | Registered 2026-08-15 — origin is Brett's direction to make the doxBench outline tab render a distilled TRUE outline (human + AI consumption) instead of a merely conventionally feat-spec-shaped fragment; 7 claims settled (primary fragment recommended as the outline, three required sections, structured open questions, provenance on added sections, round-trip refresh on demote, ratified `xspec:` markers for machine-addressability); carries the full draft template skeleton; 5 open questions (primary-fragment-vs-separate-file, migration of the 30+ existing topics, spec-delta-vs-convention, and the wheel-summary-extraction question hardest), none blocking; SEQUENCED in PARALLEL with `doxbench-editing-model` Phase A (Brett 2026-08-15) as the human decision track, with Q4 upgrading Phase A's chat edits to marker-scoped patches and Q5 riding Phase B |
| [notebook-projection-identity](#notebook-projection-identity) | MODIFIED `lifecycle-notebook-projection` (declared hosting-account field + share-out roster) and MODIFIED `credential-contracts` (two-case account-custody rule: company service account normal case, personal hosting the other legitimate case) | 1 | Registered 2026-08-15 — origin is Brett hitting a live "request access" wall on the personal-Gmail-hosted NotebookLM projection, the same disease as the just-retired openXdox personal PAT; 6 claims settled (company account is the normal case, hosting is a declared install-time intake decision, personal hosting stays legitimate as the other case, company account shares out to users, company-policy Hermes monitors + approves share requests, and this mirrors the ratified openXdox dispatch two-case precedent); first fresh conformer of `staged-topic-outline-template` carrying LIVE `xspec:candidate` markers (verified against the checker: no rejection found, only `record`-status docs are excluded); 5 open questions (contract home, company-account type, share-roster reuse of `add-client-identity-roster`, monitor/approve mechanics with no share API, and opensoft's own migration sequencing), none blocking; SEQUENCED last of today's four topics (Brett 2026-08-15) — behind `doxbench-editing-model` (both phases), the template, and the review-lane topic — since Q3's share-roster reuse waits on the in-flight `add-client-identity-roster` proposal |
| [doxbench-editing-model](#doxbench-editing-model) | MODIFIED `ideation-dashboard` (left-panel dynamic document tabs generalizing the outline/document buffer pair to N document buffers; chat-context binding to the active left-panel selection; docs-wheel tile edit verb + dirty-tile marker; right-panel Editor/Preview tab redesign with Save/Cancel) | 1 | Registered 2026-08-15 — origin is Brett's direction settling the general doxBench interaction model: left panel selects the working document (docs/lens/outline plus dynamic numbered tabs per open edit), center chat binds to whatever is selected, right panel shows the result via Editor/Preview tabs with Save/Cancel (replacing today's split md/preview layout); 7 claims settled; verified live that `BUFFER_KINDS`, the turn-assembly buffer requirement, and the save order are all hard-coded to exactly outline+document today, so the N-buffer generalization is the load-bearing engineering question; 6 open questions (tab overflow, Save/Cancel semantics, dirty-tile storage, chat-binding rule, Editor/Preview default, concurrent-edit safety), none blocking; sibling of `staged-topic-outline-template` Open question 4 (content-contract vs. interaction-model halves of the same AI-edit act); SEQUENCED first, in two phases (Brett 2026-08-15) — Phase A (chat-on-outline + Editor/Preview tabs + Save/Cancel on the existing two-buffer machinery) built before the other three topics, Phase B (N-buffer generalization) following `staged-topic-outline-template`'s ratification |

## hermes-stack-topology-per-client

How many Hermes installations a company actually has, and what each is for.
Verified: a stack holds exactly one Tenant + one Domain + N Subject layers and
rejects anything else before mutating state; a stack is pinned to one domain
factory; Omnigent is "core + per-domain overlay + per-tenant instantiation", so
Omnigent instances multiply 1:1 with stacks while the domain definition stays
singular; and the xFactory runtime CANNOT express a single-layer Hermes, so a
company/business Hermes is the separate FarHeap product, not a stack. The live
opensoft QA stack is three-layer (Tenant `opensoft-company-policy`, Domain
`codexfactory-software-engineering`, Subjects project-alfa/bravo) — already
codexFactory instantiated for the opensoft tenant.

Decision (1) RESOLVED 2026-08-08: each client gets its own stack — a client
company is a Tenant, so onboarding a client is a STACK INSTALL. The
`ledgerx-client-company-hermes` fixture and its bound HCS-002-S03 scenario are
stale against LedgerxFactory's own already-fixed model (Engagement Hermes) and
owe an OpenSpec correction spanning fixture, index, acceptance map and evidence
register. Inventory verified 2026-08-08: the Omnigent execution layer IS running for opensoft (two online CPC runners, seven worker lanes) — the autonomous-council gap is ONE missing worker lane, not a deployment (both stale pins re-pinned 2026-08-08; the drift was two additive semantic_context declarations, and merge_readiness_agent existed at the old pin too). Still blocking: the (a)/(b) fork — realize request
intake and admission at the existing Tenant Hermes (cheap, and the ratified
`client-infrastructure-request` capability already assigns Client Hermes the
source-of-truth role that is currently unrealized), versus additionally standing
up an OpsxFactory domain stack (a second control plane, Postgres, ingress,
identities, and a per-tenant Omnigent). Also open: hosting model, whether
"licensed" becomes a modelled entitlement, and the Opsx layer-naming drift
between the instantiation runbook and OpsxFactory's ratified layer model.

Cross-repo pointer (2026-08-09): OpsxFactory staged a connected governance
trilogy bearing directly on this fork's intake and approval side —
`xFactories/OpsxFactory/ideation/staging/tenant-request-intake/` (tenant-owned
chat intake, authority-free listener, normalized request candidates),
`…/hermes-approval-envelopes/` (human-ratified intensional envelopes under a
no-authority-composition invariant), and `…/tenant-operating-postures/`
(three-seat Hermes council adjudication for non-expert tenant seats +
enrollment-consented `bypassed_full_auto` rail with intent gate and anchored
outcome-match). Landed on OpsxFactory `main` at 5f6c3fa. The trilogy sites
intake ownership at the Tenant layer under either fork resolution, and the
envelope and posture contracts are flagged domain-neutral (DTN-register
shaped) — they would land here in openxFactory on promotion.

Update (2026-08-10): trilogy exit 1 is promoted — the tenant-request-intake
topic became OpsxFactory `add-request-intake-boundary`, ratified 2026-08-09
(OpsxFactory main 3de6355). Speckit implementation is COMPLETE and in review
as **OpsxFactory PR #16** (feature `007-request-intake-boundary`, tip
f0ebdf9): request-candidate contract, authority-free listener, the
five-binding projection rail reusing the ratified projection schema
unchanged, and reference identity closed by a parse-don't-validate
restructure after SEVEN adversarial gate rounds (each found real defects;
round 6 was a design failure — raw `==` on references that never reached
validation let the ratified client alias bypass the self-approval rule).
Two ratifier decisions ride with it: adversarial-Unicode robustness ruled in
scope, with the visibility property then narrowed to what is decidable and
its residual gap declared; and `southside`/`southside-clinic` ratified as one
client, recorded as identity vocabulary resolved by exact lookup with alias
derivation forbidden. The envelopes and postures topics remain staged behind
its landing per their own entry gates (a live request class at volume, then a
calibrated first envelope). The request-candidate shape stays DTN-register
flagged for neutral promotion here after it ships — and the restructure's
typed-reference discipline (parse once at ingestion; identity over resolved
segments; comparison, keying and joins all typed) is a SECOND promotion
candidate, since the aliasing class it closes is domain-neutral and any
factory comparing references by raw string has it.

## agent-wallet-identity

- Staging ID: `openxFactory:staging:agent-wallet-identity`
- Repository context: openxFactory owns the neutral capability; first
  consumer is LedgerxFactory (posting segregation of duties, enforced in
  the LedgerLinc BC extension); omnigent-install already attests the
  version facts a composition hash would consume
- Files: `agent-wallet-identity.md` (primary — identity, proof of control,
  authority binding, declared-change decertification)
- Target capabilities: ADDED neutral `openxwallet` (holder-agnostic core) and
  `openxwallet-agent-profile` (its first profile) — the topic folder keeps
  the `agent-wallet-identity` name it was staged under while the change and
  both capabilities were renamed on the 2026-08-06 restructure; composes with
  `roles-authority-model` and `credential-contracts`, and reuses the
  neutral job envelope's `approval_policy` vocabulary for authority scope
- Source: `ideation/brainstorm/agent-certification-wallets.md` (Brett,
  2026-07-15/16; naming decided 2026-07-16) organized 2026-08-06 when
  LedgerxFactory's poster gained real posting rights and the platform-level
  refusal that had backed "agents never post" disappeared with them
- Readiness: RATIFIED 2026-08-07 as `add-openxwallet` (core + agent
  profile; topic folder name unchanged) and REALIZED the same day by Speckit
  feature `006-openxwallet-contracts` at `contract-v1.31`; the enabling insight is that every agent act
  reaches a platform through ONE shared credential, so no per-agent
  identity exists to compare — which is why segregation of duties is not a
  policy anyone is declining to enforce but a property the platform cannot
  see. The two gates on this exit are both closed: key custody (what a
  signature proves) is a closed three-member set whose `evidences` is derived
  and enforced, and the first exit REQUIRES proof of possession — an asserted
  identity is a recorded non-member, so any interim belongs to a consuming
  domain as a dated exception rather than as a softening of the neutral set

## ideation-action-plane

- Staging ID: `openxFactory:staging:ideation-action-plane`
- Repository context: openxFactory (gate-intent kernel, `ideation-intent-plane`
  capability, document-lifecycle delta); codexFactory (tray/overlay UI, local
  executing gate routes, apply-lane orchestration); omnigent-install (inbox
  service, per-user ingress auth); xFactory aggregation (lane wiring)
- Files: `ideation-action-plane.md` (primary — the intent plane),
  `drive-membrane.md` (fragment 2 — projection mirror out / intake lane in)
- Target capabilities: `ideation-intent-plane` (ADDED), `document-lifecycle`
  (MODIFIED — gates happen on main); fragment 2 targets
  `lifecycle-notebook-projection` (MODIFIED)
- Source: dashboard-action-center + cloud-workstation-topology brainstorms,
  Brett-locked 2026-07-23 (the day the first derive→dispose cycle ran
  end-to-end)
- Readiness: exit 1 (`add-ideation-intent-plane`) raised at this gate with
  the second-touch decision RESOLVED (custody-not-decision, batched
  auto-merge on approval); fragment 2 exits separately after the Drive↔NLM
  ingestion spike

## context-compression-runtime

- Staging ID: `openxFactory:staging:context-compression-runtime`
- Repository context: openxFactory (neutral capability + audit-tier
  contract); Omnigent-Install (pilot wiring: pinned `headroom` in the
  omnigent-worker image behind a build arg, worker-profile activation
  block; later the egress-capture sidecar container); codexFactory
  (pilot lane); Medx/Ledgerx (tier-3 consumers when activated).
- Source: Headroom evaluation session 2026-07-25/26 (Brett Heap) —
  a source audit of headroom v0.32.0 (upstream `4bd1214`) found the
  CCR reversible-compression store is a session-scale correctness
  cache (SQLite on worker disk, 30-min TTL, content-addressed
  `sha256(original)[:24]` keys embedded LLM-visibly) with NO PHI/PII
  exclusion anywhere in the compression path. That flipped the design
  from "durable CCR audit backend" to RAM-only cache + three-tier
  audit.
- Claim: context compression is worker-lane infrastructure (pinned
  dependency, never a submodule, invisible to the domain layer), and
  its safety envelope is domain-invariant: (1) worker-host stores are
  RAM-only; (2) sensitive-data exclusion is an upstream Hermes-ingress
  obligation, never assumed of the compressor; (3) audit is
  three-tier — envelope (authorized in), harness transcript (all
  uncompressed originals, hash-joinable to compression markers),
  optional egress-capture sidecar (exact disclosed bytes,
  NetworkPolicy-enforced as the only provider egress, fail-closed) for
  disclosure-accounting domains only.
- Files:
  - [context-compression-runtime.md](context-compression-runtime/context-compression-runtime.md) — primary: source-audit evidence table, 5 claims, pilot posture, open questions, exit.
- Open questions: tier-3 knob home (omnigent overlay vs worker
  profile vs both); sidecar implementation (mitmproxy vs Envoy tap,
  SSE reassembly, capture retention per domain); whether the
  three-tier audit model deserves its own neutral spec (generalizes
  to any provider-traffic-transforming lane middleware);
  upstream-exclusion mechanics (Hermes-boundary redaction vs tagged
  spans via tag_protector); re-audit cadence for headroom version
  bumps.
- Exit: pilot evidence in Omnigent-Install →
  `add-context-compression-runtime` (`code_surface:
  installs/omnigent-install`), realization gated on the pilot lane
  green with measured savings; tier-3 sidecar delta rides the same
  change or a follow-on.

## dashboard-project-scoping

- Staging ID: `openxFactory:staging:dashboard-project-scoping`
- Repository context: the register instance is aggregation-owned
  (`xFactory/project-register.yaml`); openxFactory owns the neutral
  `project-register` schema; codexFactory owns the dashboard, the selector,
  and the session/gate plane L3 would change
- Files: `dashboard-project-scoping.md` (primary)
- Target capabilities: MODIFIED `ideation-dashboard`; possibly MODIFIED
  `project-register` if a project acquires state beyond navigation
- Source: Brett, 2026-08-02 — "lists existing projects and allows for use to
  create new project ... then allow the user to later select the project,
  then a repo in that project or all repos in that project ... when i click
  on a tile on a wheel, that is tied to a repo and my dashboard operations
  for that tile are in that repo"
- Open questions: Q1 all-repos view shape (merged vs filtered); Q2 where the
  register write lands and under what authority (the file is in ANOTHER
  repo than the served corpus); Q3 whether a tile operation in a non-served
  repository proceeds or refuses (this is the L3 fork); Q4 whether project
  groups are used at all; Q5 authority once the tenant project catalog exists
- Decisions: D1–D8 locked with Brett 2026-08-06 (decision round + one
  realization-day ruling; all five open questions resolved — see the primary
  doc's Decisions section): merged all-repos view; commission-based register
  writes; L3 proceeds as its own change; projects only; dev-authoritative
  register becoming a derived cache under the tenant catalog; three
  sequenced exits; by-role register split; multi-parent repository
  membership (D8 — snapshot keeps a first-declaring PRIMARY `project` plus
  an additive `projects` list).
- Exit path (ruled): content split applied to the aggregation register (D7);
  **exit 1 `add-project-scoped-selection` proposed 2026-08-06** (create-project
  commission + project-scoped selection + the D5 authority declaration);
  exit 2 `add-project-merged-projection` (the D1 merged view); exit 3
  `add-project-tile-repository-binding` (the D3/L3 session-plane change,
  strictly after exit 2)
- Related: `ideation/brainstorm/tenant-project-catalog-and-workstation-cache.md`
  — the runtime-authoritative twin; D5 names the authority split (runtime
  catalog authoritative when it exists; this register becomes its
  workstation-side derived cache)

## dashboard-repo-selector

- Staging ID: `openxFactory:staging:dashboard-repo-selector`
- Repository context: openxFactory (the `ideation-dashboard` capability delta
  + the snapshot-index contract); codexFactory (lane iteration, the
  (repository, ref) snapshot registry, multi-snapshot/multi-root serving,
  selector UI, both refresh bindings); xFactory aggregation (project-register
  instance = the selector roster; the published snapshot data source; the
  dispatchable nightly job); install repos later (the runtime-plane
  capability)
- Files: `dashboard-repo-selector.md` (primary)
- Target capabilities: `ideation-dashboard` (MODIFIED — selector,
  (repository, ref) snapshot source, runtime fetch with baked fallback +
  stale banner, freshness header, both refresh affordances, dispatchable
  publication); ADDED snapshot-index contract (its own additive schema —
  never grown into the snapshot schema); later ADDED runtime capability
  (neutral install-shipped ideation surface; name open; DTN candidate at its
  gate)
- Source: `ideation/brainstorm/ideation-dashboard.md` — the v2 concept
  sketch plus §"Domain drive + the runtime plane (2026-07-25)" (four
  decisions Brett-locked 2026-07-25; same-day drive findings against
  Medx/Adx/Ledgerx); the snapshot/image decoupling mission (Brett
  2026-07-25, relayed via team003, with its motivating stale-doc incident)
  and Brett's (repository, ref) keying decision (2026-07-26, live session)
- Readiness: **exit 1 proposed 2026-07-26** as
  `add-dashboard-repo-selector`; twelve decisions locked with Brett
  2026-07-25/26 (the four original ones plus: bake the app not the
  snapshot, the baked snapshot demoted to a first-boot/offline fallback
  with a never-silent stale banner, one refresh affordance with two plane
  bindings, off-cycle publication as a governed CI dispatch and never the
  pod, (repository, ref) keying with `ref` defaulting to main, a displayed
  freshness header, branch snapshots never published). Open: the
  one-neutral-vs-domain-overrides fork (pending domain-drive vocabulary
  evidence), the data-source ratification (recommendation:
  aggregation-repo raw files), index polling cadence, and whether the local
  regenerate action is gated. Exit 2 (runtime plane) stays staged and gates
  on the content-kind design decision
- Sibling: `workbench-branch-sessions` CONSUMES the (repository, ref) seam
  defined here, so this change strictly precedes it

## workbench-branch-sessions

- Staging ID: `openxFactory:staging:workbench-branch-sessions`
- Repository context: openxFactory (the `ideation-dashboard` capability
  delta — branch sessions, the PR-as-save verb, session-local snapshots —
  plus the `lifecycle-notebook-projection` delta for per-session notebooks);
  codexFactory (worktree lifecycle, the (repository, ref) snapshot registry
  shared with `dashboard-repo-selector`, branch-aware `/source`, the
  chat-rail grounding set, the `open-pr` gate verb)
- Files: `workbench-branch-sessions.md` (primary)
- Target capabilities: `ideation-dashboard` (MODIFIED — the workbench
  becomes a create/edit surface over a session branch); MODIFIED
  `lifecycle-notebook-projection` (canon notebooks stay main-only;
  per-session `xf-session-<topic>` notebooks sync from the branch worktree —
  renamed off the topic's original `xf-wb-<topic>` by the 2026-07-26
  adversarial review, which found that prefix is swept by the workbench
  reference-set orphan sweep)
- Source: Brett's live session decisions 2026-07-25/26 (the workbench
  dogfood pass that produced `add-workbench-bullseye-and-create`, then the
  branch-session design round the next day)
- Readiness: **RATIFIED 2026-07-26** as `add-workbench-branch-sessions`
  (proposed and ratified the same day, after a 5-lens adversarial review whose
  two confirmed findings were fixed, and a rename-completeness audit) —
  nine decisions locked (branch per tile, commit per gate action, instant
  create on the branch, session-only draft visibility, session snapshots
  through the (repository, ref) seam, the tool triangle on the branch,
  PR-as-save, local-plane-only until intent-plane §4, the snapshot registry
  as the one new server plumbing); TWENTY-TWO in the ratified change (design
  D1-D22) — twenty-one once Brett's 2026-07-26 session
  rulings (merge DELETES the session branch — the work is on `main` and the
  branch is residue, while abandon still never deletes pushed history; and
  `propose` REFUSES while the tile carries an unresolved session, since
  proposal ends the pipeline and the human must merge or discard first; and
  the session NotebookLM notebook is RETIRED at session end, never re-pointed
  at `main` — D16, which closes the contradiction the adversarial review
  found; and reworking a tile whose previous session was ABANDONED offers
  RESUME (keep the branch and its name) or NEW (next ordinal), with that
  abandoned branch deletable once the topic's proposal exists — D17, which
  closes what had been open question 1 and gives abandoned branches an end of
  life; a session PR lands as a MERGE COMMIT and is never squashed, because
  the per-gate-action commit series is traceability evidence for medical FDA
  clearance — D18, which makes the merge method a regulatory constraint rather
  than a history-hygiene preference; and a full NotebookLM quota DEGRADES the
  session rather than blocking it — D19, since an external SaaS limit must not
  be able to stop governed work; and a tile carrying a LIVE PROPOSAL refuses to
  open or resume a session, with `demote` as the route back — D20, the mirror of
  the propose-side refusal, making a tile a staging work surface OR a proposal
  but never both; and `open-pr` consults NO readiness signal — D21, naming BOTH
  the blocking staged-to-proposal gate and the advisory recommendation gate,
  because requiring the blocking one would deadlock: it scores `main`, and a
  session's documents reach `main` only through the pull request it would
  refuse) landed, plus D22 ruled POST-RATIFICATION the same day, closing the one
  item the change had left gated to Speckit: `open-pr` pushes under the
  ENGINEER'S OWN credential on the local plane — no App and no stored token —
  and is normatively bound to the openxfactory domain App on the hosted plane
  once that App exists, with no fallback to a personal credential there.
  ZERO open questions remain — every decision is ruled, and what is
  left before archive is realization and evidence, not judgement.
  SEQUENCED strictly after `add-dashboard-repo-selector`, which
  defines the seam this topic consumes
- Exit: `add-workbench-branch-sessions` (code surface: codexFactory +
  openxFactory + aggregation), raised 2026-07-26; archives on merged + green
  realization evidence including a real end-to-end session
- Governed successor: **doxBench**, the named integrated editor/chat evolution
  of the staging workbench, is defined by
  `openspec/changes/add-workbench-integrated-editor-chat/`. It consumes this
  topic's branch-session substrate and does not alter this topic retroactively.

## client-credential-escrow-registry

- Staging ID: `openxFactory:staging:client-credential-escrow-registry`
- Repository context: openxFactory (neutral contract — likely a
  `credential-contracts` delta + the sanctioned repo-policy exception);
  registry realization in the operator's Client Hermes tree
  (`xFactory-Hermes-Install` `config/clients/<client_ref>/credentials/`);
  escrow runbook steps in install repos (`Omnigent-Install` first);
  managed-install obligation in OpsxFactory workflow contracts.
- Source: named by Brett Heap during track-1 QA secret-custody design
  (2026-07-19); first concrete case = the opensoft self-client QA
  install's `kv-opensoft-xfactory-qa` secrets + the Flux deploy key.
- Coordination (recorded 2026-07-30 by `add-deployment-handoff-boundary`
  task 2.2): break-glass CUSTODY, the checkout realization and its test,
  and the retroactive-request POLICY WINDOW are owned HERE and consumed
  by the ratified `deployment-handoff-boundary` capability — its
  phased-never-gapped adoption keeps existing standing admin as a named,
  dispositioned exception until this topic's checkout path is realized
  and TESTED, then a dated milestone removes standing assignments.
  Coordinate, never fork.
- Claim: per-client SOPS/age-encrypted credential escrow, written at
  secret create/rotate and read only at break-glass; exactly ONE
  break-glass key per operator scope in the password manager (public
  recipient committed, so routine escrow never touches the key);
  multi-recipient adds optional client-held recovery; custody is
  operator-side OUTSIDE the client estate (survives client-tenant +
  client-GitHub destruction); under `opsxfactory_executed` escrow is an
  explicit testable obligation, with a drift audit (every `vaultref://`
  has a registry entry) checkable without decryption.
- Files:
  - [client-credential-escrow-registry.md](client-credential-escrow-registry/client-credential-escrow-registry.md) — primary: custody model, 7 claims, 6 open questions, exit.
- Open questions (blocking): delta shape (MODIFIED `credential-contracts`
  vs new capability); master-key rotation/blast-radius runbook;
  break-glass authorization topology + post-use rotation; dedicated
  registry-repo escalation criteria; MUST-escrow scope boundary
  (non-vault plumbing credentials like deploy keys); validator for
  registry structure + SOPS-metadata lint.
- Exit: one openxFactory OpenSpec change; archives only on the first
  escrowed install (opensoft self-client QA) with drift audit green and a
  REHEARSED break-glass restore drill recorded.

## avatar-pilot-hardening

- Staging ID: `openxFactory:staging:avatar-pilot-hardening`
- Repository context: openxFactory (neutral capability + pilot-gate acceptance); real Hermes adapters in `installs/hermes-install`; domain overlays/personas in the DomainxFactory repos; the live client in the private `xfactory-avatar-client` repo.
- Source: named the last successor in the avatar-client parallel-workstream plan; the threat model's deferred-to-pilot items; the reference authority stub in `xfactory/avatar_runtime/`.
- Claim: replace the reference runtime's static fail-closed authority stub with real Hermes control + delegation behind the frozen ports ("tightens rather than changes the protocol"); add per-domain overlays/personas; commission the formal WCAG audit; stand up operations/telemetry; run a staged live pilot with rollback — closing the threat-model items the kernel deferred to pilot (client-integrity TM-03, privacy review, penetration test, production authorization).
- Files:
  - [avatar-pilot-hardening.md](avatar-pilot-hardening/avatar-pilot-hardening.md) — primary: scope, claims, gates (qualified live profile + SBOM + license review + formal a11y audit), open questions, exit.
- Open questions (blocking): see the fragment — plus it is structurally last: it cannot propose until `qualify-avatar-live-voice` publishes a qualified live profile and the client lab lands.
- Exit: create `avatar-pilot-hardening` (`code_surface: openxFactory, xfactory-avatar-client, installs/hermes-install, xFactories/*`); archives only on merged + green + recorded pilot-gate evidence.

## client-layer-tuning

- Staging ID: `openxFactory:staging:client-layer-tuning`
- Repository context: openxFactory (scaffold `roles/`, content schemas,
  `validate-client-content`) + codexFactory `hermes/client/` (domain
  defaults) + `xFactory-Hermes-Install` (wizard verb).
- Source: 2026-07-22 review pass over the client brainstorm cluster
  (`client-layer-scaffold.md`, `client-layer-roster-draft.md`,
  `client-layer-content-draft.md`, `client-policy-wizard.md`).
- Claim: per-client tuning made real — house-team `roles/` join the neutral
  scaffold (11 personas incl. the new Finance & Accounting Officer +
  `cost_reporting_steward` worker; voice floor locked); the facts rule splits
  domain defaults from wizard-only values; stricter-only is enforced
  mechanically per the comparability spec (review fallback); the wizard
  (avatar-assisted first, CLI on the same elicitation schema) drafts and a
  human ratifies the auto-clear envelope (per-unit allowed), emits a park-map
  every run, and commits its output as a per-client overlay that seeds
  through the standard pipeline.
- Files:
  - [client-layer-tuning.md](client-layer-tuning/client-layer-tuning.md) — primary: claims, three exit changes, open questions.
- Open questions (blocking): validator host repo; wizard-overlay digest-pin
  signing (shared with layer-content-materialization); default
  aggressiveness; RBS's directed steward; FAO↔domain efficiency-audit seam;
  avatar-flow prerequisites.
- Exit: three changes — openxFactory scaffold+schemas, codexFactory client
  defaults, hermes-install wizard verb (in that order).

## codexfactory-domain-hermes-content

- Staging ID: `openxFactory:staging:codexfactory-domain-hermes-content`
- Repository context: codexFactory (`hermes/domain/` +
  `omnigent/domain-overlay.yaml` in lockstep); neutral persona/mix/council
  schemas in openxFactory later.
- Source: 2026-07-22 review pass over the domain brainstorm cluster (5
  codexfactory-domain docs + `hermes-persona-character-model.md`); harvest
  map verified against the codexFactory tree.
- Claim: author the Domain Hermes content the seeding runtime is starved for —
  8 Option-E personas (trait vocabulary v1, decide-then-speak guardrail,
  escalation-target audit applied), the stored policy delta (position table,
  contested-position schema, coverage ratchet), two-tier councils with
  enumerated triggers, memory boundaries (worker-proposes/Lead-accepts,
  de-id schema + attestation), and the practice catalog (`promoted_in` +
  `owning_lead`); promotion extends `codex_owns` and adds the two missing
  Omnigent workers in the same change or the seed-time closure check fails.
- Files:
  - [codexfactory-domain-hermes-content.md](codexfactory-domain-hermes-content/codexfactory-domain-hermes-content.md) — primary: claims, exit changes A/B + Omnigent extension, open questions.
- Open questions (carried): gate-rules council seats; `council_small` seat
  sourcing; efficiency-audit ownership; neutral schema timing;
  `finding_class` vocabulary.
- Exit: codexFactory change A (`add-domain-hermes-roles-and-policies` —
  **raised 2026-07-22**, proposal + tasks + `domain-hermes-content` spec
  delta on codexFactory main, strict validation green; the topic's
  `openspec/` drafts are its provenance), then change B (councils/mixes/
  escalation/memory/catalog); the Omnigent extension rides change A.

## github-administration-plane

- Staging ID: `openxFactory:staging:github-administration-plane`
- Repository context: openxFactory (neutral) with an OpsxFactory-owned realization.
- Source: xFactory family decision 2026-07-10 (review-lane first live run
  exposed the factory App holding org-wide `Contents: write` and bypassing
  branch protection).
- Claim: GitHub is a managed platform under the OpsxFactory service-subject
  model; separate the content-only App identity from a new
  administration-tier App identity, and put GitHub administration in
  OpsxFactory alongside Entra/Intune/endpoint management.
- Files:
  - [multi-app-identity-and-github-administration.md](github-administration-plane/multi-app-identity-and-github-administration.md) — claims, open questions, interim stop-gap state, exit.
- Open questions — resolved 2026-07-14 (see the primary doc's "Open questions
  — resolved" section for full recommendations):
  - one administration App or several scoped ones? → one App, narrowed via
    scoped credential grants, not App count (scoped to Opensoft's own org;
    client-tenant execution routes through `client-infrastructure-liaison`).
  - org-level rulesets vs. per-repo branch protection? → org rulesets for
    Opensoft's own org (Enterprise confirmed); client tenants need a
    plan-tier-aware org/repo/classic fallback ladder.
  - gated through a generalized `endpoint_management` workflow or a dedicated
    github-administration workflow? → dedicated workflow, extending the
    existing read-only `github-admin` command class.
  - credential custody/rotation for the administration App key? → DTN-004
    shape unchanged, at the family's strictest existing tier (15-min grants,
    Key Vault, 90-day max age, environment-gated).
  - exact scope and explicit prohibited actions for the administration App?
    → 7-repo Tier 1 now, `installs/*` deferred; rulesets/branch-protection
    only, enforced at the workflow/credential layer.
  - is GitHub administration a second profile of `endpoint_management`, or
    its own capability? → own capability, sibling to `endpoint_management`.
- Interim state already applied (stop-gap, to be superseded): a manual
  codexFactory `main` ruleset requiring PR + 1 approval with OrganizationAdmin
  bypass; the `openxfactory` App holds org-wide `Contents: write` +
  `Pull requests: write` pending the split.
- Exit: COMPLETE — the two planned OpenSpec changes were proposed, ratified,
  realized, and archived: (1) neutral `add-github-app-identity-tiers`
  (openxFactory, archived 2026-07-14) extending `roles-authority-model` with
  the GitHub App identity tiers; (2) `add-github-administration-workflow`
  (OpsxFactory, archived 2026-07-15) instantiating the
  `github-administration` capability. Live rollout done; the 2026-07-10
  incident is closed. The primary doc remains here as `superseded`
  provenance (its header names both successors).

## layer-content-materialization

- Staging ID: `openxFactory:staging:layer-content-materialization`
- Repository context: openxFactory (neutral `hermes_domain_overlay` contract +
  machine-readable `overlay_path`) + `xFactory-Hermes-Install` (seeding
  increment 2).
- Source: 2026-07-22 review pass over `hermes-layer-content-seeding.md` +
  `hermes-layer-seeding-mechanism.md`; increment 1 realized and archived
  2026-07-22 (hermes-install `add-seed-layer-content`, capability spec
  `layer-content-seeding`).
- Claim: take the proven read-only load path to enforcement — hybrid seam
  decided; generic `layer_content` kernel `(layer_id, content_kind,
  enforceable_payload, provenance)` + views; build-time render + seed-time
  verify; seeding-order invariant (domain → client → project,
  REFUSED-not-skip); the field-level enforceable-slice cut list is drafted;
  wizard-written client overlays unify into the same pipeline.
- Files:
  - [layer-content-materialization.md](layer-content-materialization/layer-content-materialization.md) — primary: claims, two exit changes, sequencing.
- Open questions (carried): per-kind `enforceable_payload` schemas; render
  ownership; wizard-overlay pin home/signing; re-pin range recording;
  partial re-seed.
- Exit: openxFactory `add-hermes-domain-overlay-contract` (independent, ready
  now) ∥ domain change A → hermes-install seeding increment 2.

## layer-vocabulary-machine-migration

- Staging ID: `openxFactory:staging:layer-vocabulary-machine-migration`
- Repository context: openxFactory (`contracts/hermes-runtime/`,
  `contracts/schemas/`); ripples to hermes-install, omnigent-install, and
  all five DomainxFactory `stack.yaml` files.
- Source: `adopt-subject-tenant-domain-vocabulary` tasks 3.1–3.3, filed as
  the deferral artifact 2026-07-23; authoritative scope =
  `contracts/policies/layer-vocabulary.yaml` frozen_identifiers inventory.
- Claim: the frozen legacy machine spellings migrate to Subject/Tenant/
  Domain only AT the next major contract bundle (the migration rides the
  major, never causes it); hermes-install adopts at pin bump; Ops/Adx
  prose sweeps can run before the major, key migrations only with it.
- Files:
  - [layer-vocabulary-machine-migration.md](layer-vocabulary-machine-migration/layer-vocabulary-machine-migration.md) — primary: target deltas, 3 claims, 2 open questions, exit.
- Open questions (non-blocking, dormant): fold into other v3 drivers vs
  standalone; `$id` redirect policy for archived digest inventories.
- Exit: per-surface-family OpenSpec changes at the scheduled major +
  mechanical per-repo stack.yaml migrations; archives when every frozen
  identifier is migrated or explicitly retained as archived-only.

## medxfactory-domain-hermes-content

- Staging ID: `openxFactory:staging:medxfactory-domain-hermes-content`
- Repository context: MedxFactory (`hermes/domain/` +
  `omnigent/domain-overlay.yaml` + `omnigent/overlay-manifest.yaml` digest
  re-pin in lockstep).
- Source: team001 omnigent-program handoff next-unit mapping (2026-07-24);
  MedxFactory `docs/` corpus (27 drafts) + the codexFactory
  `domain-hermes-content` pattern; both trees inventoried 2026-07-24.
- Claim: author the Medx Domain Hermes content the seeding runtime needs —
  clinical Plane-1 personas directing the 11 ratified worker classes
  (roster derivation base: the omnigent routing table's undefined domain
  authorities + the MxD-MRR convener), the stored medical policy delta
  (safety/root-truth corpus, store-the-delta filter), MxD-MRR formalized
  as the domain review council, escalation elevation, memory boundaries in
  the gateway vocabulary (patient-derived de-id), and the
  `medx_practice_catalog`; `overlay.yaml` upgrades from pre-contract stub
  to the v1.15 schema with two-way `medx_owns` closure; lockstep adds
  `directed_by` to all 11 workers + re-pins the overlay-manifest digest.
- Files:
  - [medxfactory-domain-hermes-content.md](medxfactory-domain-hermes-content/medxfactory-domain-hermes-content.md) — primary: 7 claims, exit changes A/B, decision record 2026-07-29, 2 residual questions.
- Open questions: RULED 2026-07-29 (decision round with Brett; full record
  in the primary doc) — roster = the derived seven PLUS a dedicated
  ontology-steward persona (eight; the accountable ontology steward per
  ratified `add-domain-ontology-layer`, replacing the pilot placeholder);
  MxD-MRR domain-owned only with cross-layer references (MxC-LOR/MxP-CIR
  ride their layer changes); convergence-packet flow untouched with mixes
  reserved for review ensembles; content manifest declared explicitly incl.
  `domain_ontology` (resolved by the ratified ontology contract). Leanings
  carried to the change-A gate: MxD-MRR wears the ontology review seats;
  `high_impact_requires: [licensed_human]`. Residual (non-gating):
  practice-catalog seed set (change-B input); client-layer-defaults analog
  timing.
- Exit: MedxFactory change A (`add-domain-hermes-roles-and-policies` —
  roles + policies + `medx_owns` closure + Omnigent lockstep), then change
  B (councils/mixes/escalation/memory/catalog), mirroring the codex
  sequence; MxC-LOR/MxP-CIR machine surfaces ride their own layer changes.

## proposal-origin-contract

- Staging ID: `openxFactory:staging:proposal-origin-contract`
- Source: Brett review of the archived `add-proposal-supporting-doc-lifecycle` change, 2026-07-09.
- Partial promotion 2026-07-12: the primary origin-contract doc crossed the
  proposal gate (pointer in `ideation/README.md`'s "Active proposals promoted
  from staging" list); this topic now holds only the regulatory rationale.
- Claim (remaining file): origin provenance is a necessary first traceability
  edge but is **not** by itself sufficient for FDA SaMD compliance; the
  rationale scopes the additional trace graph/QMS/validation work a regulated
  domain (e.g. MedxFactory) would still need.
- Files:
  - [fda-samd-traceability-rationale.md](proposal-origin-contract/fda-samd-traceability-rationale.md) — read-only regulatory rationale retained for a future regulated-traceability profile.
- Exit: the rationale exits with a future regulated-traceability-profile
  topic when a regulated domain needs it; it does not exit with the origin
  contract.

## worker-host-app

- Staging ID: `openxFactory:staging:worker-host-app`
- Repository context: openxFactory (eventual neutral manifests); app +
  manifests first-consumer in Omnigent-Install; Intune packaging + WSL
  policy in OpsxFactory; bench build pipeline owner TBD.
- Source: `ideation/brainstorm/tech-stack-benches.md` organized 2026-07-23
  on Brett's build decision; motivating evidence = the 2026-07-22/23 CPC
  heartbeat/credential recovery; prescription precedent in
  `cloudpc-named-worker-licensing.md` (device-scoped Intune artifacts,
  SYSTEM context).
- Claim: an Intune-delivered Win32 app reconciles a declarative
  `worker_host_manifest` — WSL2 + docker-ce substrate, sealed identities
  (passwordless-first, escrow-at-birth), durable heartbeat tasks with a new
  bench-inventory section, credential profiles from vaultrefs, and
  digest-pinned workBench containers verified against `bench-manifest`
  records — turning any managed Windows machine into a governed worker
  host; first consumer Omni-001, retiring the operator-CPC rider.
- Files:
  - [worker-host-app.md](worker-host-app/worker-host-app.md) — primary:
    7 claims, both manifest sketches, 4 decisions, 6 open questions, exit.
  - [wsl-install-and-setup.md](worker-host-app/wsl-install-and-setup.md) —
    WSL substrate focus (split out 2026-07-25): manifest `substrate:`
    surface, the three observed truths + convergence actions as
    implemented (`substrate_wsl`, Omnigent-Install PR #33), fail-closed
    reboot semantics, 4 WSL-specific open questions (SYSTEM-context
    distro registration is new).
- Open questions (blocking): Omni-001 local-admin/provisioning-policy
  inventory (now also carries the SYSTEM-context WSL distro-registration
  fact-check); actions-runner under virtual service accounts;
  bench-manifest home (repo vs OCI artifact); heartbeat bench-inventory
  three-place contract delta; WSL servicing owner (plus kernel-update and
  `.wslconfig` resource-limit ownership, see the WSL doc); LLM-vault
  consolidation ordering.
- Resolved elsewhere: the parked **registration-credential** decision (the
  fail-closed `runner_services` refusal behind PRs #36/#37) is RESOLVED
  2026-07-26 by `add-worker-enrollment-broker` — enrollment grants a renewable
  lease and a short-lived single-use registration token from a standalone
  broker that holds the opsxfactory administration-tier App key alone, so no
  minting authority ever reaches a host. See the `worker-enrollment-broker`
  topic below and `contracts/worker-enrollment/`.
- Exit: openxFactory OpenSpec change (manifests), Omnigent-Install change
  (the app), OpsxFactory change (packaging); archives on Omni-001 green
  readiness via the app + a governed lane run on an Omni-001 worker +
  operator-CPC rider retirement.

## worker-enrollment-broker

- Staging ID: `openxFactory:staging:worker-enrollment-broker`
- Repository context: openxFactory (neutral enrollment/lease contract);
  standalone broker service (home DECIDED by D1: a new Opsx-owned repo,
  container app on the existing platform subscription, deliberately NOT the
  QA AKS cluster);
  Omnigent-Install (registration-via-broker in `runner_services`, lease
  renewal in the supervisor); OpsxFactory (opsxfactory App key custody,
  minimum-version policy, temp runner group, engineer eligibility).
- Source: clarifying session with Brett 2026-07-26 at the worker-host-app
  runner_services gate, resolving its registration-credential parked
  decision; driving scenario = staff workstations self-installing the
  Worker Host App as long-lived (months) temp workers.
- Claim: one standalone broker owns enrollment for both estates — fleet
  hosts authenticate per-host (Opsx KV standard), volunteers as the
  engineer (device-code, no standing secret) — holding the opsxfactory
  App key centrally (minting authority never on hosts), granting
  renewable LEASES whose renewal enforces a minimum-app-version floor
  fail-closed (below-floor workers stop working until the engineer
  updates); fleet runners hard-pinned via manifest rollouts
  (v2.336.0 + sha256 ruled), temp runners self-update; temp workers ride
  a segregated runner group with a trust tier.
- Files:
  - [worker-enrollment-broker.md](worker-enrollment-broker/worker-enrollment-broker.md)
    — primary: 7 binding rulings, 4 claims, 10 open questions, exit with
    the volunteer-workstation acceptance test (first volunteer = Brett's
    machine, doubling as the NT SERVICE fact-check).
- Open questions (all carried into the proposal's `design.md` as
  decisions D1–D10 with recommendations, and **all ten adopted as DECIDED
  by Brett's approval of the change on 2026-07-26** — none of them is a
  live gate; do not re-escalate): broker home/hosting + credential
  custody (D1 — a dedicated Opsx-owned repo, container app on the
  existing platform subscription and NOT the QA AKS cluster, whose blast
  radius and lifecycle a production control-plane dependency must not
  inherit); lease cadence + grace (D2 — 24h TTL,
  hourly renewal, 12h grace); version-floor policy home (D3 —
  OpsxFactory-owned policy the broker consumes, floor raises through the
  governed lane); enrollment approval (D4 — Entra-group auto-approve in
  v1, trust tier carries the difference, Hermes approval arrives through
  the same door without a contract delta); temp-worker manifest content +
  serving (D5 — broker-served at enrollment, one worker, no benches in
  v1); engineer eligibility (D6 — existing engineering group, one machine
  per engineer); teardown semantics (D7 — full cleanup on volunteer
  uninstall, stop-only on expiry, immediate stop on revocation);
  trust-tier mechanics (D8 — first-class lease field projected into
  runner group/labels and the readiness attestation; labels alone
  rejected as host-assertable); fleet per-host secret provisioning (D9 —
  issued at Intune enrollment, escrow-at-birth, rotatable without
  re-enrollment); heartbeat/readiness lease-state integration (D10 —
  three-places rule, rides the bench-inventory heartbeat delta if it
  lands first).
- Readiness: **exit 1 proposed AND phase-1 realized 2026-07-26** as
  `add-worker-enrollment-broker` — the neutral contract (one enrollment
  point / two auth modes, lease + short-lived token, minting authority
  broker-only incl. remove tokens, renewal carrying the floor,
  fail-closed below-floor and revoked workers, revocation as refusal,
  estate package split, temp segregation + trust tier, audited decisions
  with token values unrepresentable), shipping six schemas, packaged
  positive/negative examples, and `scripts/validate-worker-enrollment.py`
  at the next additive bundle. The heartbeat delta is deliberately
  excluded.
- Exit: `add-worker-enrollment-broker` OpenSpec change (contract,
  PROPOSED 2026-07-26) + realization changes (broker service,
  Omnigent-Install, OpsxFactory); acceptance = the end-to-end volunteer
  workstation scenario on Brett's machine, which doubles as the
  NT SERVICE fact-check.

## session-notebook-reconciliation

- Staging ID: `openxFactory:staging:session-notebook-reconciliation`
- Repository context: openxFactory owns both halves — the session notebook
  lifecycle (`ideation-dashboard`, promoted from workbench-branch-sessions)
  and the sync that operates the projection
  (`lifecycle-notebook-projection`). The notebooks live on ONE account shared
  across the family, which is what makes a wrong delete someone else's live
  session rather than a local mistake
- Files: `session-notebook-reconciliation.md` (primary — the two structural
  facts, five claims, three open questions, exit path)
- Target capabilities: MODIFIED `lifecycle-notebook-projection` (the fourth
  sync mode and its fail-closed + workspace-scoping rules) and MODIFIED
  `ideation-dashboard` (the session-notebook lifecycle gains a third
  retirement route, for a session that ended outside the two governed
  endings)
- Source: `ideation/brainstorm/session-teardown-notebook-coupling.md`
  (2026-08-10), filed with PR #161 alongside the hand deletion it records —
  two orphans (a probe's session from that morning and a 2026-07-27 demo
  topic) verified dead and removed by hand, which is the ungoverned act this
  topic exists to replace
- Readiness: ready to iterate. What is SETTLED is the shape of the detection:
  forward-derived from every live session's own alias (the transform is lossy,
  so a title can never be inverted), fail closed when any session repository
  cannot be enumerated (a missing checkout looks exactly like a dead session
  and the difference is unrecoverable after a delete), scoped to this
  workspace's own session repositories, report-only until `--apply`, and
  retiring through the same `retire` operation the governed endings use. What
  is OPEN is whether an orphan is evidence worth an import-before-retire pass
  (leaning no — a session with no worktree has nothing to import back into),
  whether hand teardown should be narrowed to the abandon path (deliberately
  out of scope: probes and crash recovery legitimately remove worktrees), and
  cadence (manual, like the rest of the sync)

## subject-establishment

- Staging ID: `openxFactory:staging:subject-establishment`
- Repository context: openxFactory (neutral contracts); LedgerxFactory is
  the first full instantiation (`ideation/staging/company-provisioning/` —
  neutral books design then MSBC realization, prompted by an unconfigured
  client company found during the FarHeap sandbox rehearsal);
  MedxFactory (new patient), codexFactory (new engineering project),
  OpsxFactory (new managed estate), AdxFactory (new campaign subject) are
  the named same-shape consumers.
- Source: Brett, 2026-07-28 — "this concept of intake is also a general
  startup. it is the same as new patient or new engineering project. there
  is a setup of facts and then the best practice way to setup that subject
  in that domain. some of this neutral concept should be elevated to
  openXfactory."
- Files: `subject-establishment.md` (primary — the neutral pipeline, the
  five-domain mapping table, 8 claims, an explicit not-neutral list)
- Target capabilities: ADDED a neutral `subject-establishment` capability;
  DTN-017. Deliberately thin — the good outcome COMPOSES DTN-016 (consent
  instrument), DTN-015 (correction→promotion), `governed-derived-model`
  (tiered conformance), `workflow-gate-contract` and `credential-contracts`
  rather than restating them.
- Readiness: Ready to iterate. The design/realization split is the
  load-bearing neutral idea (same idiom as neutral contract + per-domain
  overlay, one level down). Second consumer DECIDED 2026-07-28 —
  codexFactory new-project — chosen for speed of proof and because it
  brings an existing-subject population, so the audit mirror gets real
  exercise immediately. Its mapping exposed the CROSS-FACTORY APPLY SEAM
  (codex designs, Opsx administers GitHub), which Ledgerx structurally
  could not surface and which the contract must not assume away. Open: one
  capability or two (establishment and migration differ by risk class);
  whether "system of record" is new or the existing
  estate/client-infrastructure vocabulary generalized; how much is consumed
  vs restated; whether the Hermes-memory storage ruling is neutral or a
  Ledgerx choice; who owns the conformance verdict when applier and
  designer disagree.

## qualify-avatar-live-voice

- Staging ID: `openxFactory:staging:qualify-avatar-live-voice`
- Repository context: openxFactory owns the neutral live-voice acceptance, the ADDED AVC-09/AVC-10 contract schemas, the `interface-lock.yaml` unreservation, and the acceptance-map/validator updates; the live transport (`avc_adapters_live`) is realized in the private `xfactory-avatar-client` repo.
- Source: named successor in the avatar-client-lab staging topic and the F0 feasibility spec; draws the live-voice baseline, GPT-Live-1 activation gate, latency requirement, and voice-session topology from the archived `flutter-avatar-client-ui-lab` exploration.
- Claim: internal-live provider qualification — the live WebRTC/broker/media plane behind the existing `SessionTransport` port (brokered SDP, direct Flutter↔provider media, `gpt-realtime-2.1` candidate), adding AVC-09 (adapter descriptor) and AVC-10 (latency sample) as the ADDED live contracts, with a latency-instrumented activation gate, canary, and rollback. F0 proved feasibility; this change qualifies live use.
- Files:
  - [qualify-avatar-live-voice.md](qualify-avatar-live-voice/qualify-avatar-live-voice.md) — primary: scope, claims (AVC-09/AVC-10, activation gate, latency budgets), open questions, exit.
- Open questions (blocking): credential custody + spend cap; latency-budget derivation; the activation-gate scope; data-control/consent for evaluation audio; canary/rollback shape. Also gated on a released, code-signed client from the lab.
- Exit: create `qualify-avatar-live-voice` (`code_surface: openxFactory, xfactory-avatar-client`); archives only on merged + green internal-live realization evidence.

## mobile-dashboard-surface

The mobile app realization of the ratified `avatar-first-ui` standard:
one app whose sign-in determines the Hermes layer and whose layer
determines the default surface (subject users avatar-first, tenant
staff hybrid with the conventional dashboard primary, domain authority
conventional with an avatar copilot — the ratified "Hermes-layer
surface defaults" requirement). Also hosts per-domain org-connect
onboarding ceremonies (first consumer: LedgerxFactory
`ledgerx:staging:external-client-connect` — Entra admin-consent + BC
Admin Center extension install driven from the app; Microsoft-native
ceremonies only, no custom credential UI, no standing credentials on
the device; dashboard reads ride token-gated surfaces per the
worker-readiness-surface precedent).

- Files: `mobile-dashboard-surface.md`
- Target capabilities: `avatar-first-ui` (realization evidence or a
  small ADDED requirement); avatar-client track work order
  (post `avatar-pilot-hardening`); per-domain connect flows exit via
  their DomainxFactory topics.
- Source: team-010 LedgerxFactory session 2026-07-26 (Brett).

## workstation-app-shell

The workstation counterpart to `mobile-dashboard-surface`: an app on the
engineer's own machine that OWNS the local dashboard serve — checkout
binding, actor identity, console token, port, lifecycle — instead of a
hand-typed `python3 -m … --repo-root … --repository … --actor …` line. The
motivating defect is verified, not hypothetical: the T092 runbook's literal
first command omitted two required flags and exited 2. The layer-shaped UI
posture is NOT redecided — the ratified `avatar-first-ui` "Hermes-layer
surface defaults" requirement already sets subject avatar-first, tenant
hybrid, domain conventional-with-copilot. What this topic decides is the
delivery vehicle and its BOUNDARY with the Worker Host App, which is the
load-bearing claim: one workstation would host the agent workers AND the
human console, whose whole purpose is to be distinguishable from an agent,
so they run as SEPARATE OS PRINCIPALS in one shell with the console's token
unreadable by the worker principal — using the escrow-before-account /
rotate-don't-read machinery `worker_identities` already shipped. Brett
accepted review finding 2's same-user residual on 2026-07-27 for a world
where workers live elsewhere; bundling without separation would make agent
co-residency the architecture rather than an edge case. Also names the gap
the conversation exposed: codexFactory has NO subject surface. Its subject
layer is `Project Hermes` — per project, not per client company, so consent
and journey state are per-project — and every stakeholder feature maps onto
a gate the funnel already has (intake → a possible with subject-requested
provenance, status → narrated funnel position, approvals → recorded gate
actions structurally like `ratify`, demos → the avatar carveout precedent).
Subject visibility reuses the ratified branch-session rule (drafts
session-only, `main` shared truth) one layer up. Sequencing claim: do not
couple two mid-flight programs — finish the worker host as a host, ship the
shell, stage each domain's subject surface separately.

Extended 2026-07-27 with the COMPUTE SHARE VALVE (claims 11-19): an
engineer volunteers the same workstation as a worker whose jobs may belong to
other projects, so the console carries a valve — share while doing light work,
recover the machine when work gets intense. Brett scoped it to the TEMP/VOLUNTEER
ESTATE ONLY and ruled DRAIN ONLY, which makes it complementary to the Worker Host
App program (that program moves PRODUCTION riders onto dedicated Cloud PCs; R8
already refuses binding a volunteer lease into a standing runner group) rather
than a reversal of it. Grounded: SLOTS are already the canonical unit end to end
(`max_concurrent_jobs`/`current_jobs` in the operational schema, the live
registry, per-lane declarations, dispatcher-enforced) and no resource field is
representable anywhere, so a PERCENTAGE lives only in the console's
recommendation text; the stop-accepting half is already built and smoke-tested;
the lease-renewal response already carries `required_action: stop`; the per-runner
`sc.exe stop` + `start= demand` pair and its exact inverse are already designed
(task 3.5, unbuilt). EVICTION is deliberately unfunded — no job lease, no attempt
counter, no idempotency contract, no destination host, and `current_jobs`
decrements only on completion so an abandoned job would hold its slot forever.
Two verified hazards the build must respect first: a drain expressed on
`worker.status` is silently reverted by the next finishing job
(`release_worker_job` recomputes it unconditionally), and a hand-stopped runner
triggers a FULL ACCOUNT PASSWORD ROTATION via `needs_rebind` — so the valve is
DESIRED STATE (`desired_state: active | paused` on the broker-served temp
manifest plus an app-owned intent sidecar reconcile READS, never able to override
a lease `stop`), signalled by joining the already-queued D10 three-places
heartbeat delta. "Local work first" in v1 is admission control by job class, not a
cgroup weight — the runner is a Windows process with no shared scheduling domain,
and memory does not yield the way CPU does, so the never-shared RAM reserve is a
constant the recommender never tunes. Today's only valve is `OMNIGENT_WORKER`, a
global on/off that would close the window for everyone.

- Files: `workstation-app-shell.md`
- Target capabilities: `avatar-first-ui` (realization evidence, possibly a
  small ADDED requirement for the workstation shell); MODIFIED
  `ideation-dashboard` (app-managed local serve); a later per-domain subject
  surface (name open, codexFactory first consumer). The Worker Host App's
  principal separation is a dependency satisfied in `Omnigent-Install`.
- Open questions: shell platform (recommend sharing the mobile fork); one
  installer vs two; the console token never persisted; which layer an
  engineer's own app defaults to; where the codexFactory subject feature set
  lives.
- Recorded observation: `avatar-first-ui`'s ratified text still uses the
  legacy `Customer`/`Client` layer spellings — legal as released, but the
  next substantive revision should adopt subject/tenant/domain.
- Source: team-004 session 2026-07-27 (Brett).

## recurrence-crystallization

- Staging ID: `openxFactory:staging:recurrence-crystallization`
- Repository context: openxFactory (neutral crystallization contract
  family); codexFactory is the first conformer AND the cross-domain builder
  (D5); composes memory-gateway (promotion consumed — V1: no delta),
  workflow-gate-contract (proof stages), release-realization (build archive
  evidence), credential-contracts (custody), and governed-derived-model
  (capability provenance + derived dispatch index) rather than restating
  them.
- Source: the 19-doc recurrence-crystallization brainstorm packet anchored
  at `brainstorm/crystallization-overview.md` (captured 2026-07-28);
  decision session 2026-07-29 locking D1–D11 + verifications V1–V2,
  recorded in the primary doc.
- Files: `recurrence-crystallization.md` (primary — decision record,
  fragment map, MVP slice, exit path), `dials-and-defaults.md`
  (declared-dials register — the topic's living remainder). Promoted at the
  2026-07-29 raise of `add-pattern-ledger`: the former
  `pattern-ledger-contracts.md` fragment. Promoted at the 2026-07-29
  raise of `add-crystallizer-contracts`: the former
  `crystallizer-contracts.md` and `authority-and-consent.md` fragments
  (both under that change's `supporting-docs/` with hashed manifests);
  each raise also consumed the topic's `openspec/` draft workspace.
  Promoted at the 2026-07-29 raise of `add-capability-steward`: the
  former `steward-contracts.md` fragment (under that change's
  `supporting-docs/` with a hashed manifest); the third raise likewise
  consumed the re-seeded `openspec/` draft workspace.
- Target capabilities: ADDED `pattern-ledger` (episode / outcome-label /
  family / forecast / candidate records), `crystallization-decision`,
  `crystallization-build`, `crystallization-consent` (T1/T2/T3 tiers,
  default deny), `crystallized-capability-registry`,
  `crystallization-dispatch`, `capability-health`; MODIFIED
  `omnigent-domain-overlay` (crystallized-executor profile class +
  per-category rung-ceiling declarations).
- Readiness: Ready to iterate — the 84-claim source packet is individually
  addressable (per-doc ID prefixes) and the load-bearing rulings are
  locked: authority conservation with the constitutional falses at every
  rung; fences + post-conditions + sentinels ("never silently wrong");
  artifacts digest-pinned while authority status is live-read (D10); v1
  dispatch admits only `pure`/`idempotent` effect classes (D11); sentinel
  ε floor never zero. MVP: packet-capture mechanics at L3 under the first
  two exit changes with manual steward stand-ins. Open (carried,
  non-blocking): dial re-tuning by the calibration board, adjudicator
  assignment, shadow statistics, Steward role-vs-contract, platform-actor
  naming. Cross-tenant pooling + DTN promotion out of wave. Exit:
  `add-pattern-ledger` (realized `contract-v1.19`, ARCHIVED 2026-07-29 —
  partial promotion complete; promoted spec `pattern-ledger`) →
  `add-crystallizer-contracts` (realized `contract-v1.20`, ARCHIVED
  2026-07-29 — partial promotion complete; promoted specs
  `crystallization-decision`/`-build`/`-consent` + the omnigent overlay
  delta) →
  `add-capability-steward` (realized `contract-v1.21`, ARCHIVED
  2026-07-30 — partial promotion complete; promoted specs
  `crystallized-capability-registry`/`crystallization-dispatch`/
  `capability-health`). ALL THREE EXITS ARCHIVED (v1.19/v1.20/v1.21);
  the dials register is the topic's living remainder, cross-tenant the
  deliberate brainstorm remainder.

## tier2-council-clearance-pattern

- Staging ID: `openxFactory:staging:tier2-council-clearance-pattern`
- Repository context: openxFactory (the neutral pattern template);
  codexFactory holds the ratified first instantiation
  (`add-nightly-sweep-council-clearance`, rule YAML + `council_clearance.py`,
  ratified as amended by the Gate-Rules Council 2026-07-23); the second
  consumer instantiates from the template.
- Source: accepted possible
  `pos-derived-reusable-tier-2-council-clearance-pattern-beyond`
  (ai-derived from the `cl-codexfactory` cluster sweep; accepted by Brett
  2026-07-23 with the rule-of-three condition; promoted to staging by
  Brett's `promote-to-staging` gate commission 2026-08-05 — the verb's
  first real use — and organized by the fulfilling session the same day).
- Files: `tier2-council-clearance-pattern.md` (primary — the generalized
  tier-2 shape: conjunctive tier-1 envelope, declared clearable set with an
  owner-attributed static allowlist, SHA-pinned unanimous council verdict,
  never-clearable floor, anti-normalization rule, required
  `configured_but_inactive` activation gate; 4 claims).
- Target capabilities: ADDED a neutral `council-clearance-gate-rule`
  pattern contract plus its instantiation checklist; the ratified
  codexFactory rule is cited as the conforming first instance and is not
  modified.
- Files (post-demotion): `tier2-council-clearance-pattern.md` (primary),
  `README.md` (returned-drafts record), and the `openspec/` draft workspace
  (`INDEX.md`, `proposal.md`, `design.md`, `tasks.md`,
  `specs/council-clearance-gate-rule/spec.md` — the returned packet,
  Status: draft).
- Readiness: **Demoted back 2026-08-05.** Proposed the same day as
  `add-council-clearance-rule-template` (Brett's propose commission), then
  returned by Brett's reasoned dashboard demote — "rule-of-three trigger
  not fired — no second consumer has named itself; return the template to
  staging until one does" — planned at the gate console and executed as
  the separate deliberate step (gate records under
  `ideation/dashboard/gate-records/add-council-clearance-rule-template/`).
  The pick edge keeps its `staging_id` and its `change_id` inheritance is
  withdrawn. The staged questions all carry decided answers from the
  accept note and the 2026-07-23 first council exercise; the packet
  re-crosses the proposal gate the day a second sweep or repo names
  itself.

## manager-review-approval-scope-kind

- Staging ID: `openxFactory:staging:manager-review-approval-scope-kind`
- Repository context: openxFactory owns the neutral `hermes-domain-overlay`
  contract that defines `approval_scope_kinds`
  (`contracts/hermes-domain-overlay/hermes-domain-overlay.schema.yaml`,
  canonical spec `openspec/specs/hermes-domain-overlay/spec.md`);
  `xFactory-Hermes-Install` is the motivating consumer whose seeded overlay
  would adopt the new kind on a follow-on realization.
- Source: `xFactory-Hermes-Install` feature `011-three-layer-manager-review-gate`
  implementation plan (`specs/011-three-layer-manager-review-gate/plan.md`,
  Complexity Tracking entry T2, recorded 2026-08-10); governing OpenSpec
  change `add-three-layer-manager-review-gate` (ratified 2026-07-29); ruled
  "register now" by Brett Heap 2026-08-10.
- Claim: the 011 gate commissions three governed manager-review jobs per
  candidate admission packet, and typing those jobs' approvals honestly needs
  a dedicated `manager_review` member of `approval_scope_kinds` so clearance
  policy and audit can discriminate manager reviews from ordinary intent
  approvals; today they ride the `engineering_intent` fallback, which is
  honest-but-loose typing. This is an additive vocabulary extension — the
  enum has no fixed member list (`minItems: 1`, open string array) — raised
  upstream per the Hermes install constitution's Contract Fidelity principle
  (stop-and-raise on a neutral-policy gap, never fork or shadow it locally).
  The v1 gate proceeds on the fallback; this topic is the deferred
  tightening.
- Files:
  - [manager-review-approval-scope-kind.md](manager-review-approval-scope-kind/manager-review-approval-scope-kind.md)
    — primary: context, 3 claims, 2 open questions, exit.
- Open questions (non-blocking): whether `manager_review` belongs in a
  shared neutral job-envelope approval-scope vocabulary versus purely as a
  per-domain `hermes-domain-overlay` addition; whether one shared kind is
  the right grain for the gate's three distinct governed jobs, or whether
  finer-grained kinds are warranted once the live gate's evidence is in.
- Exit: an openxFactory OpenSpec change extending `hermes-domain-overlay`
  with the `manager_review` kind, raised when the live 011 gate's operating
  evidence (real candidate admission packets run under the `engineering_intent`
  fallback) justifies the tightening; the engineering overlay's adoption of
  the new kind is a follow-on realization in the consuming domain repo, not
  part of this exit.

## openxdox-install-app-provisioning

How a DomainxFactory install (first case: a client running codexFactory)
provisions the intent plane's two GitHub Apps with near-zero manual config,
tenant-owned and sovereign. The plane needs two Apps kept separate by
`add-dispatch-credential-contract` — the content App (`Contents: write` on the
governed doc repos, in CI) and the dispatch App (`Actions: write` on the one
apply-workflow repo, held as minted tokens by the exposed inbox) — and opensoft's
QA install created both by hand. Resolution: GitHub has no app-creates-app API,
so the install drives the **GitHub App Manifest flow** — a shipped manifest per
App (permissions pre-filled) the tenant name-and-confirms, GitHub creating it in
THEIR org and returning credentials the installer captures, so the Apps stay
tenant-owned. App names are globally unique, so a naming convention
(`openXdox — <tenant>` / `openxFactory — <tenant>`) replaces identical names. The
apply workflow lives in a small dedicated repo the install creates (the dispatch
App scopes to just it), and the tenant's one real decision is the content App's
repo scope.

- Files: 1 (`openxdox-install-app-provisioning.md`)
- Target capabilities: `credential-contracts` (MODIFIED — or a new
  `install-app-provisioning` capability); realization in Omnigent-Install
  (installer) + codexFactory (manifest files + install docs)
- Open questions: contract home (delta vs new capability); managed
  (`opsxfactory_executed`) vs self-hosted manifest-flow driver; apply-repo home
  (fresh vs template; opensoft's own workflow migrate or stay in `xFactory`);
  credential capture + hand-off to the minter; naming-convention grain
- Exit: an openxFactory proposal once the contract home + the managed-vs-self-
  hosted flow are decided with Brett, plus a named Omnigent-Install installer
  change; gated on the QA dispatch migration completing (it proves the two-App
  runtime shape the installer provisions)

## substantive-review-lane-questions

- Staging ID: `openxFactory:staging:substantive-review-lane-questions`
- Repository context: openxFactory owns the neutral `roles-authority-model`
  capability the tracked proposal's spec delta targets; codexFactory owns
  the `gate_rules_council` / `merge_readiness_council` persona and council
  machinery being generalized; the xFactory aggregation repo owns
  `merge-master-approval.yml` / `merge-approval-envelope.yml`, the
  mechanical GitHub-App enforcer whose candidate-class list the lane
  extends.
- Source: Brett Heap's direction 2026-08-15 to track, as an iterating
  staging topic, the declared-open-not-decided questions of the
  ad-hoc-authored proposal `add-substantive-review-lane` (openxFactory PR
  #178, branch `change/add-substantive-review-lane`, Status: draft —
  awaiting ratification). Same pattern as the
  `manager-review-approval-scope-kind` topic: tracks a sibling in-flight
  artifact's parked question rather than originating it.
- **Not the origin** (honesty note): the proposal's own `.openspec.yaml`
  origin block declares `kind: ad_hoc`, created 2026-08-15 directly from
  verified current-state facts — proven live 2026-08-14 autonomous
  `gate_rules_council` + `merge_readiness_council` deliberation on xFactory
  PRs #85/#100 — and the proposal existed BEFORE this topic was staged.
  This topic is post-proposal tracking of its parked questions only; it
  makes no claim to be a staged origin and edits nothing in the proposal's
  immutable origin declaration.
- Claim: six decided principles are settled in the proposal and are NOT
  reopened here (recorded only as the stable baseline the open questions
  below are read against): councils judge and Merge Master stays the
  mechanical enforcer; accountability is the product (written rationale +
  signed check-run + audit artifact + dedicated App identity); identity
  separation between the reviewing/enforcing identity and the PR author;
  fail-closed with always-available `needs_human_review` escalation;
  council-defined candidate classes carrying a risk tier and a clearance
  rule, reviewing for policy compliance AND best practices; and the
  `opensoft/openxFactory` pilot reviewed by codexFactory's councils.
- Files:
  - [substantive-review-lane-questions.md](substantive-review-lane-questions/substantive-review-lane-questions.md)
    — primary: context, 6 settled claims (not reopened), 5 open questions,
    exit.
- Open questions (none blocking the pilot): (1) rollout order beyond the
  pilot — which governed repo adopts the lane next and what gates each
  adoption; (2) persona home for non-engineering domain repos — do
  Medx/Ledgerx/Ops/Adx instantiate their own review personas/councils, or
  does codexFactory review all software changes regardless of which repo
  carries them; (3) whether the tenant `company-policy-lead` seat joins
  per-PR `merge_readiness_council` deliberation, or stays rules-council-only
  as today; (4) ruleset interaction shape per repo — App `APPROVE` review
  vs. a required check-run, and whether human review remains an always-
  available alternate path; (5) risk-tier taxonomy for candidate classes
  (e.g. docs-only / config / contract / runtime-code) and which tiers, if
  any, are ever autonomously clearable.
- **SEQUENCED after the doxBench UI sprint (Brett 2026-08-15 ruling on
  today's four staging topics)** — deliberately iterated and realized only
  once `doxbench-editing-model` Phase A, `staged-topic-outline-template`,
  and `doxbench-editing-model` Phase B have landed, so the governed review
  lane catches the workbench's steady state rather than blocking the sprint
  that is building it; the sibling `add-substantive-review-lane` proposal's
  own ratification read proceeds independently and is not gated by this
  ordering.
- Exit: each question resolves independently into a pre-ratification edit
  of the governing proposal, a named follow-up OpenSpec change (likeliest
  for rollout order and the risk-tier taxonomy, once pilot evidence exists),
  or a recorded decision Brett rules directly and notes back into the
  fragment. This topic carries no exit change of its own; it closes once
  all five questions carry a disposition.

## staged-topic-outline-template

- Staging ID: `openxFactory:staging:staged-topic-outline-template`
- Repository context: openxFactory owns both target capabilities —
  `document-lifecycle` (the fragment template contract: required sections,
  round-trip-on-demote refresh rule, section provenance, marker usage) and
  `ideation-dashboard` (the doxBench outline tab that renders the template
  and would gain an add-section affordance). The wheel already
  deterministically selects a topic's primary fragment
  (`primaryFragmentPath()`) and extracts its `Summary:` header field for
  the expanded tile's preview (`fragmentSummary()`, both in
  `scripts/ideation_dashboard/web/views/wheel-model.js`) — the template is
  written to stay compatible with both without a selector change.
- Source: Brett Heap's direction 2026-08-15 (in-session): the outline tab
  today renders a staged topic's primary fragment, which is only
  conventionally "feat-spec-shaped" — Brett wants a distilled TRUE outline
  of the staged topic, for both human and AI consumption, with a standard
  template.
- Claim: seven settled claims, not reopened by the open questions below —
  the outline serves both human and AI readers; the primary fragment
  `<staging_id>.md` itself IS the templated outline, carried as the
  RECOMMENDED (not yet ratified) shape; three sections are REQUIRED (idea
  notes, conflicts, open questions); every open question carries Context /
  Recommended answer / Explanation / Disposition status, in that order;
  sections are addable by either a human or an AI, each carrying an
  `Added-by:` provenance line; round-trip semantics refresh the
  proposal-element sections to the ACTUAL last-attempted proposal text on
  demote, never re-blanking them; and the template reuses the ratified
  `xspec:candidate`/`xspec:supersedes` marker grammar for
  machine-addressability rather than inventing a second mechanism.
- Files: **MOVED OUT OF STAGING 2026-08-15.** The topic exited via
  `add-staged-topic-outline-template`, so `scripts/proposal-support.py`
  transitioned its material into that change's `supporting-docs/` — status
  `staged` → `draft`, with a per-file sha256 manifest and a byte-exact
  `source-snapshots/` copy. The staging folder is now empty by design; this row
  stays as the topic's index entry and its exit record.
  - [staged-topic-outline-template.md](../../openspec/changes/add-staged-topic-outline-template/supporting-docs/staged-topic-outline-template.md)
    — primary: 7 claims, the full draft template skeleton (fenced,
    copy-pasteable, marker comments included), 3 idea notes, 3 conflicts,
    5 open questions each with Context/Recommended answer/Explanation/
    Disposition status, exit.
- Open questions (none blocking): (1) does the primary fragment become the
  outline, or does a separate `outline.md` earn a dedicated file
  (recommended: primary fragment — preserves the wheel's one-path rule,
  no selector change); (2) how the 30+ existing staged topics migrate
  (recommended: opt-in conformance, new topics required, doc-health nudges
  rather than blocks); (3) whether this becomes a `document-lifecycle`
  spec delta or stays a staging convention (recommended: spec delta — the
  round-trip/demote guarantee needs contract force); (4) which intent verb
  authorizes AI section-patching (recommended: `edit-apply`, scoped by the
  targeted section); (5) whether the wheel's summary extraction should read
  the template's `Summary:` field explicitly rather than falling through
  its current heuristic (recommended: yes, once the template ratifies).
- All five questions dispositioned 2026-08-15 (accepted as recommended) —
  the parallel decision track this topic was sequenced for is now CLOSED, and
  `add-staged-topic-outline-template` is drafting next. Q4's ruling (`edit-apply`
  covers AI section-patching) is the hinge into `doxbench-editing-model` Phase A:
  it upgrades that phase's freeform chat rewrites into marker-scoped section
  patches. Q5 still rides Phase B as sequenced, because Q2 ruled opt-in
  migration and so the wheel's existing fallback stays for non-conformers.
- **SEQUENCED in PARALLEL with `doxbench-editing-model` Phase A (Brett
  2026-08-15 ruling on today's four staging topics)** — this topic's five
  dispositions are human decisions, not builds, so it runs alongside Phase A
  rather than blocking it; once ratified, its Q4 (the `edit-apply` intent
  verb) upgrades Phase A's chat-driven edits from freeform rewrites to
  marker-scoped section patches, and its Q5 (wheel summary extraction) is
  deferred to ride `doxbench-editing-model` Phase B.
- Exit: iterate in doxBench until all five open questions carry a
  disposition other than `open`; likely lands as a single OpenSpec change
  carrying a `document-lifecycle` delta (the template contract) and an
  `ideation-dashboard` delta (the outline tab rendering + add-section
  affordance).

## notebook-projection-identity

- Staging ID: `openxFactory:staging:notebook-projection-identity`
- Repository context: openxFactory owns both candidate target
  capabilities — `lifecycle-notebook-projection` (the projection
  mechanism: books, sync, aliases, operator runbook) and
  `credential-contracts` (the account-custody rule this topic's two-case
  model would extend) — and hosts `scripts/sync-notebooklm-books.py`
  itself. Whichever repo/install stands up its own xFactory instance is
  the party that would declare its hosting account at intake time; today
  that is Opensoft's own tenant (`opensoft-company-policy`), the only live
  install.
- Source: Brett Heap's live-session ruling 2026-08-15, made immediately
  after he (browsing as his Workspace identity `brett.heap@farheap.com`,
  managed by tech-corps.com) hit "request access" on a dashboard "open
  notebook" link — the request landed in the personal Gmail
  (`brettheap@gmail.com`) that the sync script has always run under by
  default CLI profile, with no declared account of its own. Same disease
  as the personal PAT just retired from openXdox dispatch: dies with the
  account, misattributes, gates access manually, concentrates quota on one
  person.
- Claim: six settled claims, not reopened by the open questions below —
  company service account is the normal hosting case; the hosting account
  is a declared install-time intake decision; personal hosting stays
  legitimate as the other declared case (not a corporate-only rule); the
  normal process stands up a company xFactory user account and shares out
  to users from there; company-policy Hermes gains a governance job to
  monitor that account and approve proper share requests; and this whole
  fork is the exact operator-hosted-vs-self-hosted shape already ratified
  for the openXdox dispatch credential
  (`docs/openxdox-dispatch-credential-binding.md`), asked here as a
  general identity-hosting principle rather than a credential-specific
  one-off.
- Files:
  - [notebook-projection-identity.md](notebook-projection-identity/notebook-projection-identity.md)
    — primary: 6 claims, live `xspec:candidate` Why/What changes/Impact
    sections (first fresh conformer of `staged-topic-outline-template`),
    4 idea notes, 3 conflicts, 5 open questions each with
    Context/Recommended answer/Explanation/Disposition status, exit.
- Open questions (none blocking): (1) which capability owns the
  declared-hosting-location delta — `lifecycle-notebook-projection` for
  the mechanism, `credential-contracts` for the two-case custody rule;
  neither `client-infrastructure-request` nor `client-infrastructure-liaison`
  fits, since both govern a paying client's own tenant, not the operator's
  internal tooling account; (2) company account type — recommended a
  Google Workspace user account in the operator's own domain, never a
  consumer Gmail merely labeled "company"; (3) whether the share-out
  roster should consume the in-flight `add-client-identity-roster`
  proposal — leaning yes but unproven, since that roster's key is
  provider-admission-surface-shaped (service principals), not
  human-invite-shaped; (4) monitor/approve lane mechanics given NotebookLM
  has no documented share/admin API — recommended a governed manual lane
  first, automated only if a real API surface ever exists; (5) migration
  sequencing for opensoft's own personally-hosted books — recreate under
  the company account at the next sync touch (books are derived, not
  migrated, data), verify parity, then explicitly retire the
  personal-hosted originals.
- **SEQUENCED last of today's four topics, by necessity (Brett 2026-08-15
  ruling)** — behind `doxbench-editing-model` (both phases),
  `staged-topic-outline-template`, and `substantive-review-lane-questions`,
  because its Open question 3 (share-roster reuse) waits on the in-flight
  `add-client-identity-roster` proposal rather than on workbench capacity;
  the manual owner-account-approval workaround holds the operational pain
  in the meantime.
- Exit: iterate in doxBench until all five open questions carry a
  disposition other than `open`; likely lands as one or two OpenSpec
  changes (a `lifecycle-notebook-projection` delta and a
  `credential-contracts` delta, combined or sequenced per question 1's
  resolution), raised only once a real company account exists to prove
  the mechanism against.

## doxbench-editing-model

- Staging ID: `openxFactory:staging:doxbench-editing-model`
- Repository context: openxFactory owns `ideation-dashboard`, the sole
  target capability — the doxBench workbench UI this topic reshapes end to
  end (left selector, center chat, right editor/preview surface, docs wheel,
  wheel tiles).
- Source: Brett Heap's direction 2026-08-15 (in-session): the settled
  interaction model for how a user moves between documents, how the chat's
  working context follows that selection, and how the right-hand result
  surface should be redesigned from a split view into tabs.
- Claim: seven settled claims, not reopened by the open questions below —
  the left panel is the selector of what you are working on (docs/lens/
  outline plus a dynamic numbered tab per document opened in edit mode); the
  outline tab focused binds the chat to the outline and shows its unsaved
  version on the right; the docs tab's expanded tile gains a second verb
  (edit, beside the existing read) that loads the doc as a new numbered
  left-panel tab; a doc with an open unsaved edit is visibly marked on its
  wheel tile; a doc tab selected binds the chat to that doc and the right
  panel shows the live edit; the right panel becomes Editor/Preview TABS
  (not the current split md/preview) carrying Save and Cancel; and the
  general model is left-selects/chat-works/right-shows.
- Files:
  - [doxbench-editing-model.md](doxbench-editing-model/doxbench-editing-model.md)
    — primary: 7 claims, live `xspec:candidate` Why/What changes/Impact
    sections, 7 idea notes, 6 conflicts, 6 open questions each with
    Context/Recommended answer/Explanation/Disposition status, exit.
- Verified live by reading the code in this session: `doxbench-state.js`'s
  `BUFFER_KINDS` is frozen to exactly `["outline", "document"]` and its
  state validator throws unless the buffer set is exactly those two keys;
  `doxbench_turns.py`'s `require_outline_and_document` refuses any turn
  request that does not supply exactly one outline buffer and one document
  buffer, and `PROPOSAL_TARGETS` is the same fixed two-tuple; `doxbench-save.js`'s
  `SAVE_BUFFER_ORDER` is a fixed, ordered two-buffer commit sequence (outline
  first, establishing session ancestry the document buffer's commit depends
  on); the right panel (`doxbench-editor.js`) already renders a textarea and
  a preview side by side in one pane per buffer tab — the literal split view
  Claim 6 retires; the docs wheel's expanded tile (`doc-wheel.js`) offers
  exactly one verb today (read); and the wheel (`wheel.js`/`wheel-model.js`)
  carries no dirty-tile concept, only an unrelated health-status badge
  idiom worth reusing. The N-buffer generalization of state, turn assembly,
  and save ordering is therefore the load-bearing engineering question this
  topic surfaces, not a UI-only change.
- Open questions (none blocking): (1) numbered vs. named tabs and the
  overflow policy (recommended: numbered chips with a filename tooltip, LRU
  overflow into a dropdown); (2) Save/Cancel semantics (recommended: Save =
  commit-per-gate-action on the session's draft branch with PR-as-save
  `open-pr` as the promotion act; Cancel = discard to `base_content`, both
  already-designed primitives); (3) dirty-tile signaling storage
  (recommended: a distinct visual state driven by live buffer `dirty` flags,
  session-local, never persisted into the snapshot); (4) the chat-context
  binding rule (recommended: chat always binds to the active left-panel
  selection; every turn names the buffer it acted on, generalizing today's
  `active_document_path` revalidation); (5) Editor/Preview default and sync
  (recommended: Preview default, live re-render on switch, reusing the
  existing debounced-preview pipeline); (6) concurrent-edit safety
  (recommended: keep the existing per-buffer content-hash generation guard,
  applied to however many buffers exist — already buffer-scoped, not
  state-scoped, so this generalizes almost for free).
- Sibling relationship: `staged-topic-outline-template` Open question 4 asks
  which intent verb authorizes an AI patching one template section
  (recommended answer there: `edit-apply`) — that is the content-contract
  half of the same underlying act; this topic is the interaction-model half
  (what the UI looks like while a human or the chat performs that edit).
  Deliberately kept as two separate topics so neither's exit gates the
  other.
- **SEQUENCED first, in two phases (Brett 2026-08-15 ruling on today's four
  staging topics)** — Phase A (chat-on-outline binding + the right-panel
  Editor/Preview tabs with Save/Cancel, built on the EXISTING two-buffer
  machinery verified above, no invariant break) is built before every other
  of today's four topics so the finished workbench itself helps iterate the
  rest; Phase B (numbered multi-doc tabs, the dirty-tile marker, and the
  N-buffer generalization across state/turn/save) follows, sequenced after
  `staged-topic-outline-template`'s ratification since that template's Q5
  (wheel summary extraction) rides Phase B.
- Exit: iterate in doxBench until all six open questions above carry a
  disposition other than `open`; likely lands as a single OpenSpec change
  carrying one `ideation-dashboard` delta, sequenced so the buffer/turn/save
  N-buffer generalization lands first since every UI-facing claim depends
  on it.
- Phase A questions (2 Save/Cancel semantics, 4 chat-context binding, 5
  Editor/Preview default, 6 concurrent-edit/stale-hash safety) dispositioned
  2026-08-15 (accepted as recommended; (1) and (3) stay open as Phase B) —
  Phase A proposal drafting next.
- Phase B design questions (1 tab overflow, 3 dirty-tile signaling)
  dispositioned 2026-08-18 by Brett via live-UI annotations (dropdown-of-
  loaded-files; colored dirty tiles + per-tile save; read/edit/save tile
  verbs); Phase B proposal drafting is next.
- **Phase A proposal raised 2026-08-15** as `add-doxbench-editing-phase-a`
  (active change; one `ideation-dashboard` delta — the canvas presents the
  ACTIVE buffer chosen by the context region, the Editor/Preview view-tab
  pair replaces the split pane, one Save and one Cancel replace the
  per-buffer toolbar pair, the chat binds to the active buffer and STATES that
  binding on the rail, and the panel controls stay inside the per-buffer
  staleness guard). The topic stays STAGED with (1) and (3) open: Phase B —
  numbered multi-document tabs, the docs-wheel edit verb, the dirty-tile
  marker, and the N-buffer generalization — is explicitly out of that
  proposal's scope. Reading the code for the proposal settled the Conflicts
  section's per-buffer-vs-panel-level Save question: `save()` is ALREADY
  whole-canvas (`BUFFER_KINDS.filter(dirty)`, one seam call) and merely drawn
  twice, so Claim 6 changes the button count and no Save semantics; Discard
  is the genuinely per-buffer control, and Q2 names the ACTIVE buffer as
  Cancel's target.
- **PHASE B INHERITS THE TURN-RECORD BUFFER-NAMING OBLIGATION** (F2 carve-out,
  Brett's 2026-08-15 ruling on the PR #196 review): naming the bound buffer in
  a turn record a reader can consult requires releasing the chat-turn contract
  (`xfactory-workbench-chat-turn.schema.yaml` closes the request AND the
  success envelope), which Phase A forbids — and a server-side-only field was
  proven unreadable and mis-derivable, so it was removed rather than left as a
  placeholder. Phase B re-cuts the turn machinery and releases that contract
  anyway, so the naming rides that release; Phase A ships the LIVE binding
  statement on the chat rail instead.
