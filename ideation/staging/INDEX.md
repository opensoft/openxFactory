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
| [signed-execution-chain](#signed-execution-chain) | ADDED a NEUTRAL signed-execution-chain family in openxFactory (the chain from a wallet-presented ratification through atomic enrollment, the traveling contract, harness + runner attestations, the signed PR-open decision, council review of the signed brief, and a CHAIN-VALIDATING MERGE GATE) — composing with `openxwallet`, `trust-anchor`, `identity-brokering` and `roles-authority-model`; plus the ON-CHAIN anchoring/consent layer Brett ruled 2026-08-27 | 2 | Registered 2026-08-27 from Brett's expansion ruling. **A broken chain is a FRAUD SIGNAL and there is no merge** — the chain is a PRECONDITION the omnigent layer enforces (it refuses to build an unverified chain), not an audit trail written afterwards. TIER MODEL forced by a ratified constraint: authority credentials stay HUMAN-HELD because omnigent workers carry `access_secrets: false`, so runners sign only EPHEMERAL PER-TASK attestations issued by the harness controller under its own cert — and the KEY NEVER ENTERS THE WORKER (the controller signs on the runner's request; `access_secrets: false` holds in every configuration and a short lifetime does not make a key non-secret, so "issued to the runner" would breach the same constraint the split honours — Q7 asked which signing mechanism and was RULED 2026-08-29: remote signing served by the harness controller). Tier 1 answers *who permitted this*, tier 2 *what actually ran*, and neither may stand in for the other. ON CHAIN: **salted keyed commitments** (never plain hashes — EDPB Guidelines 02/2025 v2.0 hold that a hash of personal data IS personal data, so erasure is by SALT DESTRUCTION), commitments to consent-log **checkpoints** (consent STATE stays in the governed permissioned layer, which is publicly unlinkable), and anchors — **raw PHI never**, on HIPAA grounds a public chain is append-only, world-readable and permanent; records stay in encrypted off-chain custody with patient-held keys, and hospitals/insurers verify through presentations. **The evidence plane is OFF chain and IS the record** — a signed RFC-6962-style transparency log; anchoring only makes it externally undeniable. DOMAIN MAPPING is the neutral-layer proof — MedxFactory→**HealthLinc** (treatment plan ratified→simulated→reviewed→"merge" = pushed to the patient app or printed as signed orders) and LedgerxFactory→**LedgerLinc** (analysis/review plans, "merge" = published to the ledger app) run the SAME chain, differing in payload and regulator, not in shape. Sequences BEHIND four ACTIVE changes (not staged topics): `add-wallet-carried-review-authority` (S2 issuer anchor REALIZED — the direct predecessor and link 1's instrument), `add-trust-anchor` (certificates + chain custody, realized at contract-v1.37), `add-identity-brokering` (who a signer is), `implement-openxpki-install-repo` (the CA that issues the controller cert). **ALL SEVEN QUESTIONS RULED 2026-08-29 by Brett Heap in a clarify sitting** — Q1/Q2/Q4/Q7 as recommended, Q6 CONFIRMED as recommended, and **TWO DIVERGENCES (Q3, Q5)**. Every gate they held is OPEN: Q3/Q6 gated tranche 3, Q7 gated tranche 2's contract text, tranche 1 was never gated. Q3's research input was a **VENDORED STUDY** (`chain-selection-study.md`, 2026-08-27, sourced + date-checked) recommending transparency log as the evidence plane, **Bitcoin (OpenTimestamps aggregation) primary anchor**, **Kaspa optional secondary** under three conditions (archival node, inclusion proofs retained AT ANCHOR TIME, corroborating-only — Kaspa L1 **prunes tx data after ~3 days**), consent logic in the permissioned layer with anchored state roots, **NOT smart contracts on the anchoring chain and NOT Kasplex/Igra in 2026**; a chain-agnostic MULTI-ANCHOR RECEIPT is the 10-year exit path. **Q3's RULING DIVERGES from that ordering, in TWO ROUNDS**: round 1, verbatim — "lets [sic] use Kaspa as primary and bitcoin as secondary" — then, after the cost facts (Kaspa ~$0.000001/tx; Bitcoin-via-OTS $0 marginal per item on public calendars, ~$2.1k/yr self-run hourly; raw BTC tx $0.12–0.36 with spike history; a cheaper sidechain adds federation trust and saves nothing), round 2: **"Bitcoin-via-OTS on everything"** — BOTH witnesses on EVERY anchored item, **Kaspa FIRST** as the primary/OPERATIONAL witness under the three unchanged conditions and **Bitcoin batched via OTS as the DURABILITY witness — TEN-YEAR CLAIMS CITE BITCOIN** — with no selectivity and no third chain; receipts stay chain-agnostic multi-anchor carrying BOTH proofs. "Primary" is order of arrival, never evidentiary weight. The vendored study is **NOT edited** — a research record rewritten to agree with a later ruling stops being evidence. Brett's three priors came back **QUALIFIED** (Kaspa "non-captured"), **REFUTED for anchoring** ("Bitcoin too expensive" — aggregation makes it ~$0 marginal), **CONFIRMED** (KAS sub-penny fees). **Q6 CONFIRMED 2026-08-29 and it is the ruling's OPERATIVE FORM**: "patients put PHI portions on chain" means SALTED KEYED COMMITMENTS — a verifiable public handle, the portion itself disclosed off-chain under an anchored consent checkpoint, salt destruction as the erasure mechanism; literal raw/encrypted/plain-hashed PHI on chain stays REFUSED and **no later change re-litigates it**. **Q7 RULED as recommended**: REMOTE SIGNING SERVED BY THE HARNESS CONTROLLER, the runner's signing REQUEST recorded beside the signature it received, the controller corroborating the payload against its own link-4 setup attestation; an HSM is a later hardening of the same shape. **Q5 is the second divergence — RULED AGAINST THE RECOMMENDATION**: "allow contract code later" — evidence-only remains today's posture and no tranche now planned puts contract code on any chain, but the change MUST NOT constitutionalize "no contract code ever" nor gate a future adoption on the recommendation's stated trigger; the study's EDPB/HIPAA posture, unaudited-stack risk and irrevocable-deployment class are RECORDED AS ADVISORY CONTEXT for that future change, not as a gate on it. EXIT: tranche 1 (signed ratification + atomic enrollment + the transparency log) is composable TODAY and UNGATED; tranche 2's question-gate is open and what remains is machinery (the omnigent layer + the PKI plane); tranche 3's two question-gates are open and it builds to the RULED configuration, waiting on the PKI plane rather than on a ruling. **The topic is FULLY RULED and EXIT 1 IS RAISED** as the active change `add-signed-execution-chain` (links 1–3 + the transparency log + the short-chain gate, nine ADDED requirements), amended to all seven rulings. Drafting was NOT green-lit in the sitting and was GREEN-LIT SEPARATELY by Brett Heap on 2026-08-29 in session, in the same ruling that collapsed the two parallel packets onto `#495` and ADOPTED NARROWING A — tier 1 is RATIFYING authority, agent-held REVIEW wallets stay lawful. The packet is UNRATIFIED; ratification is a separate act and is his |
| [avatar-pilot-hardening](#avatar-pilot-hardening) | ADDED `avatar-pilot-hardening` | 1 | Blocked — last successor; gated on `qualify-avatar-live-voice` + the client lab landing, plus its own open forks |
| [ideation-action-plane](#ideation-action-plane) | ADDED `ideation-intent-plane`; MODIFIED `document-lifecycle` (gates happen on main); fragment 2: MODIFIED `lifecycle-notebook-projection` (Drive membrane) | 2 | Exit 1 raised at this gate (`add-ideation-intent-plane`); fragment 2 blocked on the Drive↔NLM markdown-ingestion spike; **RECONCILED 2026-08-28** (`settle-aging-staging-topics`): fragment 1's exit `add-ideation-intent-plane` is ACTIVE — ratified 2026-07-23, 13 of 17 tasks ticked — not merely "raised"; fragment 2 (`drive-membrane.md`) is DEFERRED WITH ITS GATE NAMED, the unowned Drive↔NLM markdown-ingestion spike. A deferral is a schedule, not a standing — the folder keeps ageing on fragment 1's account too |
| [client-credential-escrow-registry](#client-credential-escrow-registry) | ADDED to `credential-contracts` — SPLIT INTO TWO PACKETS by Brett 2026-08-28: exit 1 = the break-glass CHECKOUT path (`add-credential-escrow-checkout`, proposed 2026-08-28), exit 2 = the REGISTRY itself (`add-credential-escrow-registry`, the ruled successor: ruling C's home and grandfathered exception, inventory completeness, the readiness binding and the decryption-free lint — NO LONGER the schema, which the OD-2 veto moved into exit 1); touches `client-infrastructure-liaison` | 1 | **EXIT 1 RAISED 2026-08-28** as `add-credential-escrow-checkout`, and **RULED THE SAME DAY over PR #479**: OD-2 VETOED (ruling A's `escrow:` block and the sixth record kind `xfactory_credential_escrow_entry` come into exit 1, so its realization now owes the additive contract cut at the next additive minor, numbered at realization by merge order and not spent in the packet), OD-4 approved as authored, the rest cleared, and all five of exit 1's own open questions ruled — four on its recommendations, one against (the drill must also prove a live refusal). Delta went 7 ADDED / 28 scenarios to **9 ADDED + 1 MODIFIED / 46 scenarios**. All 6 of the topic's ORIGINAL open questions are now closed or carried as obligations: 4 ruled at the split, the master-key rotation runbook and the registry validator remaining as the successor's work rather than as questions. The topic doc stays staged for exit 2. Forcing fact re-verified at the gate: the QA install has read `execution_binding.mode: opsxfactory_executed` at `status: completed` since 2026-07-20 and `config/clients/opensoft/credentials/` does not exist |
| [client-layer-tuning](#client-layer-tuning) | MODIFIED client scaffold (`roles/` + FAO + `cost_reporting_steward`); ADDED client content schemas + `validate-client-content`; wizard verb in hermes-install | 1 | **COMPLETE 2026-07-24** — all three exits ratified, realized, archived (2a contract-v1.17 + canonical spec `client-layer-tuning`; 2b codexFactory defaults; 2c wizard + unified client seeding). The opensoft tenant is tuned and seeded live (phase-2 evidence note). Primary doc + drafts retained as provenance; **CLOSED 2026-08-28 by `settle-aging-staging-topics`: primary doc marked `superseded`**, naming all three archived exits (openxFactory `2026-07-24-add-client-layer-tuning-contracts`, codexFactory `2026-07-24-add-client-layer-defaults`, hermes-install `2026-07-24-add-client-tuning-and-seeding` — each verified at its own tree). Folder retained as provenance |
| [context-compression-runtime](#context-compression-runtime) | ADDED `context-compression-runtime` (worker-lane compression stage + RAM-only local-store rule + upstream-exclusion obligation + three-tier audit model + per-domain egress-capture knob) | 1 | Ready to iterate — design + headroom v0.32.0 source audit locked with Brett 2026-07-25/26 (RAM-only CCR, audit moved to envelope/transcript/egress tiers); exit gated on the codexFactory-lane pilot in Omnigent-Install producing measured savings; **DEFERRED WITH GATE NAMED 2026-08-28** (`settle-aging-staging-topics`): the proximate gate is the codexFactory-lane pilot in Omnigent-Install producing MEASURED savings, and that pilot sits behind the same worker chain as `worker-host-app` (Omnigent-Install PR #40 open since 2026-07-28 → OpsxFactory broker-service tasks 8.1/8.2, both unticked). A deferral is a schedule, not a standing — the topic keeps ageing |
| [dashboard-repo-selector](#dashboard-repo-selector) | MODIFIED `ideation-dashboard` (repo selector, (repository, ref) snapshot source, runtime fetch + baked fallback, refresh affordances, dispatchable publication) + ADDED snapshot-index contract; later ADDED runtime capability (neutral install-shipped ideation surface, DTN path) | 1 | **Proposed 2026-07-26** as `add-dashboard-repo-selector` (exit 1) — twelve decisions locked with Brett 2026-07-25/26 (runtime plane is the goal, planes separate, per-repo snapshots + index, sparse wheels, bake the app not the snapshot, baked snapshot demoted to fallback, two refresh bindings, off-cycle publication is CI-only, (repository, ref) keying, displayed freshness, branch snapshots never published); neutral-vs-override fork + data-source ratification deliberately open; exit 2 (runtime plane) still staged; **EXIT 1 IS TAKEN — recorded 2026-08-28 by `settle-aging-staging-topics`**: `add-dashboard-repo-selector` was ratified 2026-07-29 and ARCHIVED 2026-08-01 (`openspec/changes/archive/2026-08-01-add-dashboard-repo-selector`), and the topic now carries the `Exit taken:` record that stops it ageing as unraised work. Open questions 7–9 (data-source ratification, index polling cadence, local-regenerate gating) were CLOSED by Brett's rulings of 2026-07-26 and cited in that packet's `Ratified:` line, but stood as OPEN in the fragment for a month; they are now marked closed there. **Exit 2 (runtime plane) is NOT taken and is deferred with its gate named: open question 3, what an "idea" IS as governed install content** |
| [dashboard-project-scoping](#dashboard-project-scoping) | MODIFIED `ideation-dashboard` (create-project commission, project-scoped selection, merged cross-repo projection, per-tile repository binding); additive gate-intent / gate-action-record growth | 1 | **Decision round complete 2026-08-06** — D1–D8 locked with Brett, ZERO open questions: true MERGED all-repos view (D1), register writes via COMMISSION (D2), L3 per-tile binding PROCEEDS as its own change (D3), projects only (D4), local register dev-authoritative then derived cache under the tenant-catalog twin (D5), THREE sequenced exits (D6: `add-project-scoped-selection` → `add-project-merged-projection` → `add-project-tile-repository-binding`), register split by role (D7 — core/domains/medx-clinical/installs), repository membership MULTI-PARENT (D8, ruled during exit-1 realization — a repo may live in many projects; snapshot keeps a first-declaring PRIMARY + additive `projects` list; MedxFactory joins medx-clinical); merged-view rules D9–D11 (view-side cluster union by topic tail; composed views read-only + "open in <repo>" jump; project aggregates derived from the register). header redesign D12–D15 ("Opensoft openDox"; project dropdown with New Project first, last-used default; repo filter popover; `edit-project` membership commissions). **Exit 1 proposed, RATIFIED, and REALIZED 2026-08-06 as `add-project-scoped-selection`; exit 2 proposed 2026-08-06 as `add-project-merged-projection` (awaiting ratification); header redesign proposed 2026-08-06 as `add-opendox-project-header` (awaiting ratification)** |
| [workbench-branch-sessions](#workbench-branch-sessions) | MODIFIED `ideation-dashboard` (branch-per-tile working state, commit-per-gate-action, session-local snapshots, PR-as-save `open-pr` verb); MODIFIED `lifecycle-notebook-projection` (per-session notebooks sync from the branch worktree; canon notebooks stay main-only) | 1 | **RATIFIED 2026-07-26** as `add-workbench-branch-sessions` (proposed and ratified the same day, after a 5-lens adversarial review and a rename-completeness audit) — TWENTY-TWO decisions (design D1-D22; D22 is the post-ratification `open-pr` push-identity ruling, 2026-07-26) and **ZERO open questions** — the change carries no parked decision; SEQUENCED strictly after `add-dashboard-repo-selector`, whose (repository, ref) seam it consumes; local plane only until intent-plane §4 |
| [codexfactory-domain-hermes-content](#codexfactory-domain-hermes-content) | codexFactory `hermes/domain/` content (changes A + B) + Omnigent overlay extension in lockstep | 1 | **COMPLETE 2026-07-23** — both changes ratified, realized, archived: change A 2026-07-22 (roles + policies + closure + Omnigent lockstep) and change B 2026-07-23 (mixes, councils, escalation, memory, catalog); canonical spec `domain-hermes-content` carries all nine requirements. The Omnigent extension rode the `add-omnigent-domain-overlay` realization. Primary doc + openspec/ drafts retained as provenance. Change B COMPLETE — ratified + archived 2026-07-23 (`archive/2026-07-23-add-domain-hermes-councils-and-memory`); **CLOSED 2026-08-28 by `settle-aging-staging-topics`: primary doc marked `superseded`**, naming both archived codexFactory exits (`2026-07-22-add-domain-hermes-roles-and-policies`, `2026-07-23-add-domain-hermes-councils-and-memory` — both verified at the codexFactory tree). Folder + drafts retained as provenance |
| [github-administration-plane](#github-administration-plane) | MODIFIED `roles-authority-model` (neutral App-identity tiers); new OpsxFactory-owned `github-administration` capability | 1 | COMPLETE 2026-07-15 — both exit changes ratified, realized, archived (2026-07-14-add-github-app-identity-tiers, openxFactory; 2026-07-15-add-github-administration-workflow, OpsxFactory); live rollout done, 2026-07-10 incident closed; primary doc retained as `superseded` provenance |
| [layer-content-materialization](#layer-content-materialization) | ADDED neutral `hermes_domain_overlay` contract + `overlay_path` (openxFactory); hermes-install seeding increment 2 (`layer_content` kernel + materialization) | 1 | **COMPLETE 2026-07-23** — both exits ratified, realized, archived: `add-hermes-domain-overlay-contract` (openxFactory, `contract-v1.15` tag verified) and `add-layer-content-materialization` (hermes-install PR #6 merged 696ec48, archived 2026-07-23; capability spec carries increments 1+2). Deferred increments 3–6 + gate wiring recorded in the capability spec; primary doc retained as provenance; **CLOSED 2026-08-28 by `settle-aging-staging-topics`: primary doc marked `superseded`**, naming both archived exits (openxFactory `2026-07-23-add-hermes-domain-overlay-contract`, hermes-install `2026-07-23-add-layer-content-materialization` — both verified at their own trees). Folder retained as provenance |
| [layer-vocabulary-machine-migration](#layer-vocabulary-machine-migration) | MODIFIED `layer-vocabulary` + hermes-runtime v2→next-major identifier migration + domain-stack schema major | 1 | Dormant by design — deferral artifact for `adopt-subject-tenant-domain-vocabulary` tasks 3.1–3.3 (filed 2026-07-23); rides the next major contract bundle, never causes it; Ops/Adx prose sweeps runnable earlier |
| [medxfactory-domain-hermes-content](#medxfactory-domain-hermes-content) | MedxFactory `hermes/domain/` content (changes A + B) + Omnigent `directed_by` lockstep + overlay-manifest digest re-pin | 1 | **Change A COMPLETE 2026-07-29** — authored, ratified, realized, and archived the same day (`archive/2026-07-29-add-domain-hermes-roles-and-policies`; canonical Medx spec `domain-hermes-content`, 6 requirements): eight personas incl. the dedicated ontology-steward, eight medical policy files, the v1.15 overlay with a proven 43-item two-way `medx_owns` closure, `directed_by` on all 11 workers with the manifest re-pinned (omnigent-install fixture digest flagged stale to its own change), and the v13 ontology scaffold landed DRAFT (ruled stewardship policy, explicit content manifest incl. `domain_ontology`, canonical validators in `make validate`, readiness `domain_scaffold_required` pending Domain Hermes publication). **TOPIC COMPLETE — change B realized 2026-07-29, archived 2026-07-30** (`archive/2026-07-30-add-domain-hermes-councils-and-memory`; the canonical Medx `domain-hermes-content` spec carries all TWELVE requirements; MedxFactory is the second domain complete on BOTH layers — one params file from a deployable medical stack pending the flagged omnigent-install fixture digest refresh and the governed ontology publication: review-ensemble mixes with the stated convergence-flow boundary, MxD-MRR formalized with the ontology seats and the three-gate cross-layer flow, escalation elevation preserving the stub items, gateway-vocabulary memory boundaries, `medx_practice_catalog` with the four ruled seeds). (roster DECIDED the same day — decision round with Brett): the derived seven personas PLUS a dedicated ontology-steward (eight total; accountable ontology steward per ratified `add-domain-ontology-layer`); MxD-MRR domain-owned only; convergence flow + review mixes; content manifest declared explicitly incl. `domain_ontology`. No external gates (omnigent overlay realization archived at contract-v1.16); **CHANGE B IS ALSO COMPLETE — this row said otherwise until 2026-08-28**: `archive/2026-07-30-add-domain-hermes-councils-and-memory` was verified at the MedxFactory tree. **CLOSED 2026-08-28 by `settle-aging-staging-topics`: primary doc marked `superseded`** naming both archived exits; folder retained as provenance |
| [proposal-origin-contract](#proposal-origin-contract) | none yet — retained rationale for a future regulated-traceability profile | 1 | Held as read-only evidence; the origin contract itself was promoted from this topic 2026-07-12 (pointer in `ideation/README.md`'s promoted list) |
| [worker-host-app](#worker-host-app) | ADDED `worker-host-manifest` + `bench-manifest` (first-consumer drafts in Omnigent-Install, DTN path); realization app in Omnigent-Install + Intune packaging in OpsxFactory | 2 | Ready to iterate — build decision by Brett 2026-07-23; realization under way (substrate steps 1–2 merged); 7 open questions (Omni-001 admin path + SYSTEM-context WSL distro registration, runner-under-virtual-account, bench-manifest home hardest); **DEFERRED WITH GATE NAMED 2026-08-28** (`settle-aging-staging-topics`): Omnigent-Install **PR #40** (phase 3 — enrollment-broker client, leases, fail-closed floor; raised 2026-07-28, STILL OPEN) → OpsxFactory `add-worker-enrollment-broker-service` **tasks 8.1/8.2**, Brett's hosting-target and deployment-credential gates, both unticked. Upstream of all three the broker service itself is MERGED (broker PRs #1 2026-07-27, #2 2026-07-28). A deferral is a schedule, not a standing — the topic keeps ageing |
| [session-notebook-reconciliation](#session-notebook-reconciliation) | MODIFIED `lifecycle-notebook-projection` (a fourth sync mode: reconcile the `xf-session-` namespace against live sessions, fail-closed, report-only by default) + MODIFIED `ideation-dashboard` (a third retirement route for a session that ended without one) | 1 | Ready to iterate — organized 2026-08-10 from the `session-teardown-notebook-coupling` brainstorm on the day two live orphans had to be deleted BY HAND; the five claims are settled (forward-derived detection, fail closed on incomplete knowledge, scoped to this workspace's session repositories, report-only default, `retire` never `delete`); 3 open questions, none blocking (is an orphan evidence worth an import pass; whether hand teardown should be narrowed; cadence) |
| [subject-establishment](#subject-establishment) | ADDED neutral `subject-establishment` (two artifact kinds: neutral subject design + platform realization; provenance-graded fact set; reference-archetype lifecycle; conformance tiering; apply-and-verify-by-read-back; audit-lift mirror); DTN-017 | 1 | Ready to iterate — named by Brett 2026-07-28 from LedgerxFactory's company-provisioning work (first instantiation, in flight); **Second consumer DECIDED 2026-07-28: codexFactory new-project** (`project` is already a first-class codex subject kind; `check_profile`/`reviewer_group` are neutral-design elements wearing domain names). It surfaced the finding Ledgerx could not: for codex the DESIGNING domain and the APPLYING administrator are different factories (GitHub administration is Opsx's), so the realization artifact must be handoff-shaped — likely the same seam as `deployment-handoff-boundary`. 6 open questions; exit gated on Ledgerx reaching proposal; **READINESS CORRECTED 2026-08-28** (`settle-aging-staging-topics`, one line only — the topic is being FILED by another agent and is otherwise untouched here): the Ledgerx first instantiation is NO LONGER "in flight" and the exit is NO LONGER "gated on Ledgerx reaching proposal" — LedgerxFactory `openspec/changes/archive/2026-08-04-add-ledgerx-company-provisioning-and-setup-audit` archived 2026-08-04 (with `2026-08-04-add-ledgerx-msbc-company-realization` and `2026-08-04-modify-ledgerx-ap-intake-for-onboarding-readiness`), so that gate CLEARED on 2026-08-04. FLAGGED, NOT FIXED: DTN-017 still reads `staged` in `docs/domain-neutralization-candidate-register.md`; the filing agent owns that row |
| [tier2-council-clearance-pattern](#tier2-council-clearance-pattern) | ADDED neutral `council-clearance-gate-rule` pattern contract (tier-2 council-clearance template: clearable set, never-clearable floor, anti-normalization, activation gate) | 6 | **Demoted back 2026-08-05** — proposed and demoted the same day (Brett's propose commission, then Brett's reasoned demote: "rule-of-three trigger not fired — no second consumer has named itself"); the full draft packet (proposal, design, tasks, spec delta) sits in the topic's `openspec/` workspace per the draft-proposal convention, ready to re-cross the gate the day a second consumer appears. Organized 2026-08-05 from accepted possible `pos-derived-reusable-tier-2-council-clearance-pattern-beyond`; the first full possible→staged→proposed→demoted traversal of the wheel verbs |
| [recurrence-crystallization](#recurrence-crystallization) | ADDED `pattern-ledger`, `crystallization-decision`, `crystallization-build`, `crystallization-consent`, `crystallized-capability-registry`, `crystallization-dispatch`, `capability-health`; MODIFIED `omnigent-domain-overlay` (crystallized-executor class + rung ceilings) | 2 | Ready to iterate — organized 2026-07-29 from the 19-doc brainstorm packet (2026-07-28) with D1–D11 + V1–V2 locked (authority conservation; artifacts digest-pinned while authority status is live-read (D10); v1 dispatch admits only pure/idempotent effect classes (D11); neutral schemas first (D6)); MVP family DECIDED: packet-capture mechanics at L3, evidenced by two same-shape runs on 2026-07-28; cross-tenant deliberately out of wave (stays brainstorm); exit = add-pattern-ledger (realized contract-v1.19, ARCHIVED 2026-07-29; fragment under the archived change's supporting-docs/) → add-crystallizer-contracts (realized contract-v1.20, ARCHIVED 2026-07-29; fragments under the archived change's supporting-docs/) → add-capability-steward (realized contract-v1.21, ARCHIVED 2026-07-30; fragment under the archived change's supporting-docs/). ALL THREE EXITS ARCHIVED — the staged remainder is the dials register |
| [agent-wallet-identity](#agent-wallet-identity) | ADDED neutral `openxwallet` (holder-agnostic core: key reference + declared custody, attenuated grants as the authority primitive, proof of possession, custody capping authority, key-attributed audit, revocation propagation, distinct-holder constraints, non-substrate rule) + ADDED `openxwallet-agent-profile` (composition + declared-change revocation + authority as grant scope); composes with `roles-authority-model` + `credential-contracts`; `openxVault` consumes the grants | 1 | **PROPOSED 2026-08-06 as `add-openxwallet`** (topic folder keeps the `agent-wallet-identity` name; the change was renamed on restructure). Restructured the same day after Brett asked whether the Medx/Ledgerx intersection lives in openxFactory — it did not, so the change now adds a HOLDER-AGNOSTIC core with GRANTS AS THE PRIMITIVE plus an agent profile, rather than a wallet shaped like an agent binding authority to a second vocabulary. **RATIFIED 2026-08-07** with all three decisions: grants as the primitive, the core holder-class agnostic, and key custody DECLARED and CAPPING authority. **REALIZED 2026-08-07** by Speckit feature `006-openxwallet-contracts`: two neutral contract families (`contracts/openxwallet/` core + `contracts/openxwallet-agent-profile/` as a sibling, so the profile seam is structural), `scripts/validate-openxwallet.py`, and a corpus of 16 positives and 33 negative confirmations covering 11/11 requirements, registered at `contract-v1.31`, and **ARCHIVED 2026-08-08** as `2026-08-08-add-openxwallet` with both capabilities promoted (`openxwallet` 8 requirements, `openxwallet-agent-profile` 3). The topic row stays because the staged fragment remains on disk as provenance carrying the deferred material — batteries, measured drift, qualification tiers and delegation chains, each a named successor gated on a consumer of its own. The feature settled the two decisions the ratification left it: the closed custody set is three members with `evidences` DERIVED from two declared booleans and enforced — so a readable key cannot claim an isolated key's authority, and the collapse is structurally impossible rather than discouraged — and the composition component set covers a retrieval corpus BY REFERENCE (identity plus governing configuration) rather than by contents, which dissolves the include-or-exclude binary. The closed custody enumeration and what each member evidences are now contract content rather than an implementation detail. Organized 2026-08-06 from the 2026-07-15/16 `agent-certification-wallets` brainstorm at the moment a consumer named itself (LedgerxFactory posting segregation of duties, `ledgerx:staging:posting-segregation-of-duties`). Scoped BELOW the brainstorm on purpose: identity + proof + declared-change decert first; batteries, measured drift, qualification levels and delegation chains are named successors, each gated on a consumer. Two ratified Medx specs constrain the design (a wallet address MUST NOT be identity proof; custody stays wallet-neutral), which makes verification rather than registration the load-bearing requirement. 6 open questions — key custody is hardest, since it decides whether a signature proves the AGENT acted or only that the HOST did |
| [manager-review-approval-scope-kind](#manager-review-approval-scope-kind) | MODIFIED `hermes-domain-overlay` (additive `approval_scope_kinds` vocabulary extension — a dedicated `manager_review` kind) | 1 | Registered 2026-08-10 — origin is `xFactory-Hermes-Install` feature `011-three-layer-manager-review-gate`'s implementation plan (tension T2), ruled "register now" by Brett Heap the same day; the live gate proceeds on the `engineering_intent` fallback in the meantime; 2 open questions (envelope-vs-overlay home, naming/scope grain), neither blocking |
| [openxdox-install-app-provisioning](#openxdox-install-app-provisioning) | MODIFIED `credential-contracts` (or a new `install-app-provisioning` capability: two-App manifest provisioning + naming convention + apply-repo home); realization in Omnigent-Install (installer) + codexFactory (manifests + install docs) | 1 | Ready to iterate — named by Brett 2026-08-14 from the openXdox dispatch-migration's manual App toil; GitHub-capability verified (no app-creates-app API; the App Manifest flow is the mechanism, Apps tenant-owned); 6 claims settled (two Apps stay two, manifest flow, tenant-owned, globally-unique-name convention, small apply-workflow repo, tenant only sets the content-App scope); 5 open questions (contract home + managed-vs-self-hosted flow hardest); gated on the QA dispatch migration completing |
| [substantive-review-lane-questions](#substantive-review-lane-questions) | tracks `roles-authority-model` (MODIFIED by `add-substantive-review-lane`, PR #178 — RATIFIED 2026-08-22) — no capability delta of its own | 1 | Registered 2026-08-15 — origin is Brett's direction to track the ad-hoc-authored proposal's five declared-open, not-decided questions (this topic is post-proposal tracking, NOT the proposal's origin; the proposal's own `.openspec.yaml` records `kind: ad_hoc`); six decided principles carried as settled context, not reopened; 5 open questions (rollout order, non-engineering persona home, company-policy-lead per-PR seating, per-repo ruleset shape, risk-tier taxonomy), none blocking the pilot; SEQUENCED after the doxBench UI sprint (Brett 2026-08-15) — after `doxbench-editing-model` Phase A, `staged-topic-outline-template`, and Phase B, so the review lane catches the workbench's steady state rather than blocking the sprint. **CLOSED AND RETIRED FROM STAGING 2026-08-22** — all five questions ruled by Brett Heap in-session that day and encoded into the tracked proposal, which Brett then RATIFIED the same day in a separate ratification read (record `openspec/changes/add-substantive-review-lane/review/ratification-2026-08-22.md`): Q1 rollout order deferred to a named follow-up change on pilot evidence with the evidence bar and the engineering-before-domain ordering principle decided now; Q2 persona home ruled AGAINST the recommendation — codexFactory reviews every governed repo, zero new persona homes; Q3 company-policy-lead seating ruled as a bounded THIRD option — rules-council-only default plus a per-class declared pull-in defined by the gate-rules council at class-definition time, fail-closed for those classes; Q4 ruleset shape ruled as the proven shape everywhere; Q5 risk tiers ruled as a constitutional floor now with the tier vocabulary deferred to the same follow-up path as Q1. The topic met its own closing condition (all five dispositioned) and the folder is retired. Unlike the two prior exited topics, it could NOT exit into a `supporting-docs/` move — the tracked proposal's origin is `ad_hoc` and `proposal-support.py transition` refuses to restate an immutable origin as `staged` — so the fragment's final state is named, not linked; three conflicts are recorded as NOT resolved by the closure — see the detail section |
| [staged-topic-outline-template](#staged-topic-outline-template) | MODIFIED `document-lifecycle` (the primary-fragment template contract: required sections, round-trip-on-demote refresh rule, section provenance, marker usage) and MODIFIED `ideation-dashboard` (the doxBench outline tab renders the template + gains an add-section affordance) | 1 | **PROPOSED 2026-08-15 as `add-staged-topic-outline-template`, RATIFIED the same day** (all 5 open questions accepted as recommended, closing the parallel decision track) — exited staging the same day, material moved to the change's `supporting-docs/` (see detail section below); Q4 corrected by Amendment 1 to `edit-document` (ratified text named `edit-apply`, the gate console's redline verb, which cannot reach a session branch). Sections 1-4 realized (contract text, doc-health's warning-tier nudge, the outline tab + tests) and bookkeeping 6.1-6.3 discharged (this row, the exit record, and the `doxbench-editing-model` Q4 handoff). **CHANGE ARCHIVED 2026-08-21** — all 22 tasks discharged, gates 5.1-5.3 green and task 5.4's live browser proof driven for real (one commit through `edit-document` on a session branch, the verb evidenced three ways); both ADDED requirements promoted, and the topic's material now sits in the archived change's `supporting-docs.tar.gz` bundle rather than a loose folder |
| [notebook-projection-identity](#notebook-projection-identity) | MODIFIED `lifecycle-notebook-projection` (declared hosting-account field + share-out roster) and MODIFIED `credential-contracts` (two-case account-custody rule: company service account normal case, personal hosting the other legitimate case) | 1 | Registered 2026-08-15 — origin is Brett hitting a live "request access" wall on the personal-Gmail-hosted NotebookLM projection, the same disease as the just-retired openXdox personal PAT; 6 claims settled (company account is the normal case, hosting is a declared install-time intake decision, personal hosting stays legitimate as the other case, company account shares out to users, company-policy Hermes monitors + approves share requests, and this mirrors the ratified openXdox dispatch two-case precedent); first fresh conformer of `staged-topic-outline-template` carrying LIVE `xspec:candidate` markers (verified against the checker: no rejection found, only `record`-status docs are excluded); 5 open questions (contract home, company-account type, share-roster reuse of `add-client-identity-roster`, monitor/approve mechanics with no share API, and opensoft's own migration sequencing), none blocking; SEQUENCED last of today's four topics (Brett 2026-08-15) — behind `doxbench-editing-model` (both phases), the template, and the review-lane topic — since Q3's share-roster reuse waits on the in-flight `add-client-identity-roster` proposal. **DISPOSITIONED 2026-08-23 — all five questions now carry a disposition, none `open`**: Q2 and the account timing RULED BY BRETT HEAP in session (a Google Workspace USER account in the operating tenant's own domain, working name `xfactory-books@opensoft.one`, created now/soon — reinforced by the platform fact that a GCP service account cannot drive NotebookLM at all), and Q1/Q3/Q4/Q5 adjudicated against executed evidence. Q1 CORRECTED its own context (the two-case fork is ALREADY a promoted `credential-contracts` requirement, not merely runbook prose beside one) and closed the one-vs-two-changes fork to ONE COMBINED change. Q3 RAN the mapping against the realized client-identity-roster schema and validator — 11 errors when the share-out facts are stated honestly; the force-fit variant passes with one grantee and FAILS with two on `duplicate-identity-key`, because the grantee is not in the uniqueness tuple — proving the two shapes are transposed (one principal / many scopes vs one scope / many principals) and ruling a DISTINCT small share-out roster. Q4 kept the governed manual lane and unified the approval record WITH that roster entry (one artifact, not an audit trail beside it). Q5 adopted the `split-ideation-book-per-repo` retirement runbook, parity reconciled against the corpus scan rather than the legacy books. The 2026-08-15 sequencing rationale is spent — `add-client-identity-roster` archived, and its shape was tested and found structurally unable to carry this. **ACCOUNT CONFIRMED the same day (Brett, 2026-08-23): `xFactor001@opensoft.one`** — a Google Workspace user in `opensoft.one`, exactly Q2's ruled shape (the earlier `xfactory-books@opensoft.one` was a working name, never created). The exit precondition is MET and Brett authorized raising the combined change, so the topic exits via `add-notebook-projection-identity` rather than waiting; Opensoft's own install is the declared Case A instance its migration path applies to |
| [doxbench-editing-model](#doxbench-editing-model) | MODIFIED `ideation-dashboard` (left-panel dynamic document tabs generalizing the outline/document buffer pair to N document buffers; chat-context binding to the active left-panel selection; docs-wheel tile edit verb + dirty-tile marker; right-panel Editor/Preview tab redesign with Save/Cancel) | 1 | Registered 2026-08-15 — origin is Brett's direction settling the general doxBench interaction model: left panel selects the working document (docs/lens/outline plus dynamic numbered tabs per open edit), center chat binds to whatever is selected, right panel shows the result via Editor/Preview tabs with Save/Cancel (replacing today's split md/preview layout); 26 claims settled (includes the ruled two-plane chat memory design, Claims 13-21, and its 2026-08-18 second-pass addendum settling memory-gateway conformance, the three-layer compression stack with shake v1, and Headroom watch-listed not adopted, Claims 22-26); verified live that `BUFFER_KINDS`, the turn-assembly buffer requirement, and the save order are all hard-coded to exactly outline+document today, so the N-buffer generalization is the load-bearing engineering question; 7 open questions (tab overflow, Save/Cancel semantics, dirty-tile storage, chat-binding rule, Editor/Preview default, concurrent-edit safety, and the chat memory system — ruled 2026-08-18), none blocking; sibling of `staged-topic-outline-template` Open question 4 (content-contract vs. interaction-model halves of the same AI-edit act); SEQUENCED first, in two phases (Brett 2026-08-15) — Phase A (chat-on-outline + Editor/Preview tabs + Save/Cancel on the existing two-buffer machinery) built before the other three topics, Phase B (N-buffer generalization) following `staged-topic-outline-template`'s ratification. **EXITED STAGING 2026-08-21** — both phases raised and realized; `add-doxbench-editing-phase-a` ARCHIVED 2026-08-21 and its spec text promoted, `add-doxbench-editing-phase-b` carried the whole remainder (§4–§11 + §13 realized across PRs #207/#210/#216/#223, `contract-v1.34`) and remains ACTIVE pending §12 share-session, which Brett ruled 2026-08-21 trails as its own slice. The fragment moved to Phase B's `supporting-docs/`; two items are PARKED, not adopted — see the detail section |
| [doxchat-auto-fit-routing](#doxchat-auto-fit-routing) | MODIFIED `ideation-dashboard` (per-turn fit-aware `auto` resolution; the no-fit warn/ask surface and its session-sticky consent; compress-to-fit as a turn outcome) + a likely ADDITIVE model-catalog release (capability dimensions beyond byte limits, at minimum modality) + a likely additive chat-turn release (the recorded fit decision) | 1 | Registered 2026-08-21 — origin is Brett's direction given at the `contract-v1.38` rule-5 ruling, quoted VERBATIM in the fragment; 6 claims settled (per-turn fit-aware resolution, filter out models too small for the turn, no-fit is a human decision, session-sticky continue-all consent, compress-to-fit on continue, and fit is multi-dimensional with raw size only one axis); 6 open questions, none blocking. **DISPOSITIONED 2026-08-24 — all six resolved**, architect adjudications on verified evidence anchored in Brett's rulings, with TWO of the fragment's own recommendations CORRECTED by recon. Q1: the ROUTE decides, upheld, but at the ASSEMBLY POINT INSIDE STEP 9 — not at precondition 7, because the packet does not exist there (steps: 5 scope, 6 identity, 7 model+limits, 8 idempotency, 9 dispatch, with assembly at `serve.py:2926`); the route's `error` is free-form `^[a-z][a-z0-9_]{2,63}$`, not an enum, so a no-fit code costs no contract act. A review-found CONSTRAINT rides with it: request bytes are bounded EARLIER against the selected entry (`:2677`/`:2730`), so exit (b) must also move or redefine that pre-assembly guard or a request sized for a wider `routes_to` member is refused before routing runs. Q2: `resolved_model_id` STAYS as the declared default, naming debt accepted explicitly, removal rejected. Q3: one closed additive `modalities`, PLUS a batching obligation — the release must decide, not silently pass, the type-side `models.maxItems` question and the `model_id` bounds gap (N7). Q4: turn-record self-description plus a RECORDED arm, adjudicated under Brett's own intake-lane OQ-3 test (a recorded gate action suffices on the single-operator loopback; an instrument is required only on tenant/shared installs), with the consent scoped to session identity/rekey/generation and NEVER a wall clock, honoring his arm-and-reconfirm ruling. Q5: three sequenced exits, with (c) REDEFINED — a fit-reducing act ALREADY happens silently under `posture: full` (`serve.py:2935-2956`; `dropped_evidence` reaches no wire field), so (c) discloses it via a third `reduced_reason` constant on the RELEASED v1.40 field with zero contract change; a third posture VALUE is rejected. Corrected on review: what already runs is LAYER-1 SELECTION (lossless by reference, and it REFUSES when mandatory threads alone overflow), so (c) also owes the real LAYER-2 compaction Claim 5 needs — the module's own `assert_fidelity` refuses conflating the two. Q6: union badge unchanged and non-negotiable; the record carries both badges. **SEQUENCING GATE CLEARED** — Phase B archived 2026-08-22 and 10.7 shipped as `contract-v1.40`; the remaining sequencing fact is the model-intake lane's collision with exit (b), which exit (a) avoids |
| [notebook-access-wallet-governance](#notebook-access-wallet-governance) | MODIFIED `lifecycle-notebook-projection` (the ratified share-out roster entry becomes a wallet-governed record; the grant lane's provider act and revocation semantics) and possibly MODIFIED `openxwallet` (though the grant's closed scope and wallet-only audience already answer the interesting half) | 1 | Registered 2026-08-24 — origin is Brett's direction: sharing happens THROUGH THE APP, so if the books were opened org-wide in the Google machinery the access would still sit on the user, and he asked whether this can go in the wallet and be controlled per repo or finer. Two rulings the same day: the Google-side posture is **RESTRICTED with the app as the sole grantor** (org-visible REJECTED), and the topic is staged rather than proposed. 7 claims settled — sharing through the app; restricted posture; **Google's ACLs are the OUTER enforcement**, so an org-visible book is provider-granted access no app record can subtract; deny-by-default with every grant through the governed lane; the provider's enforcement atom is per-notebook/per-user/viewer-editor; per-repo control maps to per-book because `split-ideation-book-per-repo` already made the books per-repo; and finer-than-book is NOT provider-enforceable, a named non-goal of the Google half. The org-visible rejection rests on `client-identity-roster`'s promoted doctrine — where a provider-enforced principal IS available it must be used, and recording a bound as provider-enforced when none exists is a finding — so org-visibility would downgrade an available provider-enforced bound to a logic-enforced one. 7 open questions (whether a wallet grant can scope an external resource at all — checked against the schema: its `audience` must be a wallet and its `scope` has no property for a provider or a provider-side role, so the wallet holds the AUTHORITY to perform a granting act, narrowed to books via free-form `scope.objects` — while the GRANTEE, holding no wallet, cannot appear in a grant at all; one record or two; what revocation means provider-side, contrasted with #282's bearer-secret lesson; who approves and whether this closes task 2.4; whether a repo may declare its own book's policy as a derived input; where finer-than-book lives; and how a grantee is NAMED, since a persona's subject pattern admits no `@` while `nlm share invite` needs exactly an email). **SEQUENCED AFTER the migration thread's held steps clear** — nothing to grant access to under the declared account until the books are re-derived there (migration in flight as PR #289), and both `add-notebook-projection-identity` and `add-notebook-hosting-credential-custody` are ACTIVE with ratified-but-unpromoted deltas this topic would amend |
| [treatment-options-engine](#treatment-options-engine) | MODIFIED `governed-derived-model` (a `role: recommendation` member emitting ranked, cited, non-authoritative options; a declared `evidence_floor` dial with labelled, structurally non-mixable relaxed modes; an `editorial_weights` declaration for ranking inputs no truth store supplies) — with the realized half MedxFactory-owned across `root-truth-grounding` (adverse-reaction and mechanism-of-action backfill), `terminology-normalization` (drug-class and indication mapping tables) and `treatment-plan-generation` (the engine itself) | 1 | Registered 2026-08-26 — Brett's build decision ("we will build this"), six steps: indicated → minus contraindicated → minus interacting → weighed by adverse reactions → rebalance on a charted non-response → off-label mode with the evidence floor lowered and mechanism similarity as the candidate generator. 7 claims settled, the governance boundary among them and NOT a dial: the engine PROPOSES and a clinician decides, `execute_final_action: false` holds, the plan gate stays human-reviewed, and the rebalance trigger is a chart observation rather than a timer. **Corpus recon 2026-08-26 corrected the described shape in four ways that change the deltas**: (a) `adverse_effect` is ALREADY in the closed ten-member claim-type enum with 3 records, so §6 work is a BACKFILL, not a new claim type; (b) the drug→condition edge is effectively ABSENT — 5 of 6,510 grounded pairs are `condition_*` — so "list all drugs indicated for X" is unanswerable today rather than merely slow; (c) the condition namespace already carries TWO id conventions (generated `condition_<icd10>` vs curated readable slugs, curated silently winning), which `indicated_for` must settle before writing a row; (d) evidence_grade is already multi-valued (6,499 regulatory_label + 7 across three lower grades), so the off-label floor has grades to drop to. Corpus measured at 6,506 records / 1,302 medication concepts / 1,298 custody SPLs (≈22% of the 5,803-row prescribable RxNorm set). 10 open questions, all `open`; three are hard blockers — Q7 (MoA as an eleventh enum member vs overloading `target`) fixes every backfilled record id, Q9 (no Medx policy authorizes `person_modeling: identified_persons_under_policy`, and the Medx conformance file declares `synthetic_only`) blocks declaring the family at all, and Q10 (WHO ATC's licence commit rule) is a structural validate gate with FDA-EPC-alone as the fallback. Q8 asks whether the engine is a MODIFIED `treatment-plan-generation` rather than a new capability — its nine promoted requirements already cover the entry point, the citation obligation, the closed worker plane, consent, the model pin and the plan-G1 gate. Exits NEUTRAL-FIRST: the `governed-derived-model` delta once Q7/Q8/Q9 dispose, then the Medx corpus+engine change once Q10 clears and the extractor-model policy re-pin (a governed version bump of `medx.domain.policy.plan_authoring_models` v1, recommended on cost) is made or declined |
| [openxwallet-neutral-home](#openxwallet-neutral-home) | REMOVED `openxwallet` + REMOVED `openxwallet-agent-profile` from the openxFactory corpus (moved to `opensoft/openXwallet`); ADDED `domain-descendant-boundary` (the general standard: a domain consumes a neutral open* product through a `<Domainx><Product>` pin-and-profile descendant) + ADDED `neutral-product-pin` (commit + per-file sha256 + `pinned_by_commit_only`, tag-only refused, fail closed on an uninitialized submodule or digest drift); MODIFIED `trust-anchor` (custody registry resolved from the pin) + MODIFIED `review-authority-intake` (the reader is the pinned tool inside a REQUIRED consumer check) | 1 | **PROPOSED 2026-08-26 as `split-openxwallet-repo`** (PR opensoft/openxFactory#391) and **RATIFIED 2026-08-26** by Brett Heap in session, AS PROPOSED — R1-R8 standing unchanged, Q1-Q5 carried at the design's dispositions (Q1/Q2/Q3 travel, Q4/Q5 decided); realization proceeds through Speckit features, one per `tasks.md` group, not `/opsx:apply`. Registered 2026-08-26 — origin is Brett's two questions (is openXwallet a repo or features in another repo; do domains integrate the neutral product directly or through a `<Domain>Wallet` that pins it) and his ruling the same day, verbatim: "approve R1-R8 as recommended, stage the topic and propose". **ALL EIGHT RULINGS SETTLED** — R1 `opensoft/openXwallet` on the house `openX<type>` form (which owes `docs/openxdox-naming.md` an Amendment 2, since that ratified record currently names `openxWallet` as a family EXCEPTION); R2 machine keys FROZEN in v1 (paths, capability ids, the `xfactory_wallet_*` kind prefix, the envelope kind, finding codes — a rename in the same change as the move is unbisectable, and LedgerxFactory pins five kinds and several finding-code strings by name); R3 the new repo owns the wallet's own standard (both contract families + corpus, validator, syntax gate, CI workflow, the two promoted specs, Speckit 006/010/012, the `2026-08-08-add-openxwallet` archive) while openxFactory keeps the SEAM (`governance/review-authority/`, Speckit 013/014, the trust-anchor / identity-brokering / roles-authority-model compositions, all ideation provenance) — which amends the aggregation's working rule #1; R4 the pin is BIDIRECTIONAL and acyclic (openxFactory pins openXwallet by commit + per-file sha256 + `pinned_by_commit_only`; openXwallet vendors exactly ONE openxFactory artifact, `contracts/schemas/hermes-job-envelope.schema.yaml`, because validator rule (g) reads it); R5 root-level `openXwallet/` submodule in the aggregation, on the DTN-022 precedent; R6 the register STAYS (codexFactory's merge-gate floor pins `governance/review-authority/register.yaml` in `opensoft/openxFactory` and refuses wildcards) while its READER travels with the validator as a generic authority-register mode; R7 descendants are `MedxWallet` / `LedgerxWallet` / `codexWallet` / `OpsxWallet` / `AdxWallet`, the `<Domainx><Product>` form all four existing descendants use; R8 `LedgerxWallet` first, at extraction time, because LedgerxFactory is the only live consumer. The load-bearing FINDING is that the descendant repo is already the house standard with **no counter-example** — openChart -> MedxChart, openPractice -> MedxPractice, openAvatar -> MedxAvatar/LedgerxAvatar — so this topic ratifies the pattern ONCE as a general standard instead of paying for a fourth bespoke boundary change. First release is a **byte-identical pure move**: the eight artifact sha256s must equal openxFactory HEAD's manifest rows before `wallet-v1.0` is tagged. 5 open questions, none blocking the move — Q1 (promote the register as a wallet primitive vs split the reader back) is expected to TRAVEL to the council rather than resolve, since either answer converts a provably-empty diff into a design change. Hard sequencing: LedgerxFactory's forward-compatible finder lands BEFORE openxFactory sheds (its `validate_wallet_estate.py::find_openxfactory()` fails loudly, never skips), `wallet-v1.0` exists before openxFactory changes, and consume-and-shed is ONE atomic PR because `validate-trust-anchor.py` hard-exits without the custody registry. Verified NOT affected: hermes-install reseed (wallet content is not in `CONTENT_KINDS`) and codexFactory (the register does not move). **EXIT TAKEN — the change is ARCHIVED 2026-08-28** as `openspec/changes/archive/2026-08-28-split-openxwallet-repo/`, on merged-plus-green realization evidence across six repositories (openXwallet at `wallet-v1.0` then `wallet-v1.1`; openxFactory at `contract-v1.47` then `contract-v2.0`, which shed 92 local copies; codexFactory #117; xFactory #161; LedgerxFactory #25/#29/#30/#31; OpsxFactory #129) plus the first descendant LedgerxWallet at `lxw-v1.0`. **The row and the fragment are KEPT ON DISK as provenance**, on the `agent-wallet-identity` precedent above — that topic's change archived 2026-08-08 and its row stayed because the staged fragment remains on disk carrying the deferred material, which is the same reason here. **The topic is NOT fully exited**: it still carries a LIVE successor exit, `create-ledgerxwallet-overlay-boundary`, ratified and realized but an ACTIVE change still |

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
- Exit taken: `2026-08-01-add-dashboard-repo-selector` — exit 1 (dev
  plane), ratified 2026-07-29, ARCHIVED 2026-08-01. Exit 2 (runtime
  plane) is NOT taken; its gate is open question 3.
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
- Rulings, Brett 2026-08-28 (four multi-choice selections over a
  READ-ONLY decision round, each taking the prep's recommendation):
  **A — delta shape**: additive optional `escrow:` relationship block on
  the existing `xfactory_credential_binding_template` PLUS one new record
  kind for the escrow entry, on the trust-anchor precedent that "operator
  escrow is a relationship on the credential record, not a custody tier".
  **B — key topology**: per-client recipient PLUS one operator root on
  every file, drills restricted to the per-client key, and the escrow
  recipient set DISJOINT from every runtime decryption-controller
  recipient (the live QA Flux age recipient may never be an escrow
  recipient); the root's worst-case radius is every client, recorded.
  **C — registry home**: Client Hermes
  `config/clients/<client_ref>/credentials/` canonical, the openxpki
  install-repo escrow grandfathered as a named dispositioned exception
  until migrated, and three structural escalation tests any one of which
  forces a dedicated registry repo. **D — scope: SPLIT**, checkout first
  so the standing-admin exception can close; plus two sub-confirmations —
  the retroactive-request POLICY WINDOW is set by the checkout packet, and
  the QA Flux deploy key is SHOULD-escrow under the re-mint test (it is
  regenerable while the operator holds GitHub org ownership).
- Open questions: ZERO REMAIN OPEN. 4 of the original 6 were ruled at the
  split above (delta shape; break-glass authorization topology +
  after-use rotation; registry-repo escalation criteria; MUST-escrow
  scope boundary). The other two — the master-key rotation /
  blast-radius runbook and the validator for registry structure +
  SOPS-metadata lint — are carried as the successor's WORK rather than
  as questions. The five NEW questions raised at the exit-1 gate were
  all RULED on 2026-08-28 over PR #479: one drill per client; the
  recommended cadence (every escrow-identity rotation plus at least
  annually); an explicit scope amendment to `thin-independent-approval`
  rather than a silent reuse; the operator root's private half held
  OFFLINE rather than beside the per-client keys in the password
  manager; and — the one ruling that went AGAINST the packet's own
  recommendation — the drill MUST also prove a live refusal.
- Exit: TWO openxFactory OpenSpec changes, not one. **Exit 1 RAISED
  2026-08-28** as `add-credential-escrow-checkout` — the break-glass
  authorization, the evidence a checkout leaves, the policy window,
  after-use rotation, the recipient rules, the re-mint test, and the
  rehearsed drill as its archive gate (one drill also discharges
  `deployment-handoff-boundary`'s phased-never-gapped milestone).
  **Exit 2 open** as the ruled successor `add-credential-escrow-registry`
  — ruling C's home and grandfathered exception, inventory completeness
  bound to managed-install readiness (including the per-client drill
  obligation), the operator-root custody runbook, the drill cadence, and
  the decryption-free lint; it archives on the first escrowed install
  with the drift audit green. **Ruling A's schema surface is NO LONGER
  exit 2's** — the OD-2 veto of 2026-08-28 moved the `escrow:` block and
  the `xfactory_credential_escrow_entry` record kind into exit 1, whose
  realization now owes the additive contract cut in consequence.

## avatar-pilot-hardening

- Staging ID: `openxFactory:staging:avatar-pilot-hardening`
- Repository context: openxFactory (neutral capability + pilot-gate acceptance); real Hermes adapters in `installs/hermes-install`; domain overlays/personas in the DomainxFactory repos; the live client in the private `openAvatar` repo.
- Source: named the last successor in the avatar-client parallel-workstream plan; the threat model's deferred-to-pilot items; the reference authority stub in `xfactory/avatar_runtime/`.
- Claim: replace the reference runtime's static fail-closed authority stub with real Hermes control + delegation behind the frozen ports ("tightens rather than changes the protocol"); add per-domain overlays/personas; commission the formal WCAG audit; stand up operations/telemetry; run a staged live pilot with rollback — closing the threat-model items the kernel deferred to pilot (client-integrity TM-03, privacy review, penetration test, production authorization).
- Files:
  - [avatar-pilot-hardening.md](avatar-pilot-hardening/avatar-pilot-hardening.md) — primary: scope, claims, gates (qualified live profile + SBOM + license review + formal a11y audit), open questions, exit.
- Open questions (blocking): see the fragment — plus it is structurally last: it cannot propose until `qualify-avatar-live-voice` publishes a qualified live profile and the client lab lands. That gating change was RAISED 2026-08-26 (`openspec/changes/qualify-avatar-live-voice/`) but is unrealized, so the gate is still shut; raising it does not publish a profile.
- Named deferrals this topic now CARRIES, confirmed by Brett's latent decision 2 of 2026-08-26: the durable synchronous per-tenant cumulative-spend counter (from that change's Fork 1), the retention-class unreservation with its retained-real evaluation corpus and evaluation consent surface (Fork 4), the contract flag that would make the single-model non-shadowing guarantee structural rather than operational, and the promotion of p99, teardown, degraded-network and per-turn conversational latency from recorded evidence to hard gates (Fork 2).
- Exit: create `avatar-pilot-hardening` (`code_surface: openxFactory, openAvatar, installs/hermes-install, xFactories/*`); archives only on merged + green + recorded pilot-gate evidence.

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
  minting authority ever reaches a host. See that topic's promoted fragment
  under [`add-worker-enrollment-broker` supporting-docs](../../openspec/changes/add-worker-enrollment-broker/supporting-docs/worker-enrollment-broker.md)
  and `contracts/worker-enrollment/`.
- Exit: openxFactory OpenSpec change (manifests), Omnigent-Install change
  (the app), OpsxFactory change (packaging); archives on Omni-001 green
  readiness via the app + a governed lane run on an Omni-001 worker +
  operator-CPC rider retirement.

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
- Files: **RETIRED FROM STAGING 2026-08-22.** The topic met its own closing
  condition — all five questions dispositioned — so the folder is retired and
  its content kept as provenance. It could NOT take the exit route the two
  prior exited topics took (`scripts/proposal-support.py transition` into the
  governing change's `supporting-docs/`): the tracked proposal's
  `.openspec.yaml` declares `origin.kind: ad_hoc`, a transition must declare
  `kind: staged`, and the tool refuses the disagreement outright ("origins are
  immutable"). That refusal is correct — this topic never was the proposal's
  origin, and its own honesty note has said so since capture — so forcing a
  supporting-docs move would have falsified the record to satisfy a
  convention. The fragment is therefore NAMED rather than linked, because a
  link would resolve to nothing:
  - `ideation/staging/substantive-review-lane-questions/substantive-review-lane-questions.md`
    at its final committed state, openxFactory commit `f1acf0d0`
    ("Disposition all five substantive-review-lane questions in the
    fragment"), file sha256
    `84d0ebb22a1f479cbbb9f97f5233bf816c415e1506bcafca6ff7751a8d503f2b`.
    Recoverable with
    `git show f1acf0d0:ideation/staging/substantive-review-lane-questions/substantive-review-lane-questions.md`.
    That final state is the ratified outline template's full shape — context,
    6 settled claims (not reopened), idea notes, conflicts, 5 questions each
    with Context / Recommended answer / Explanation / Disposition status /
    Added-by, and the exit — and it drew ZERO doc-health findings
    (`_template_gaps` → `[]`, `_staged_exit_changes` → `[]`).
  This row is KEPT, not deleted, as the topic's index entry and its exit
  record — the same treatment `doxbench-editing-model` and
  `staged-topic-outline-template` received. The "Full promotion" maintenance
  rule above (delete the row) does not apply: nothing was promoted, and there
  is no `ideation/README.md` promoted-proposal pointer to carry the record
  instead.
- Open questions — **ALL FIVE DISPOSITIONED 2026-08-22, ruled by Brett Heap
  in-session.** None was blocking the pilot; none is open now. Route in
  brackets:
  1. **Rollout order beyond the pilot** — RULED as recommended. The ORDER
     goes to a named follow-up change raised on pilot evidence; the EVIDENCE
     BAR (≥3 council-cleared substantive PRs spanning ≥2 candidate classes,
     zero enforcer incidents, one completed gate-rules review cycle) and the
     ORDERING PRINCIPLE (engineering-owned repos before domain repos) are
     decided now. [proposal edit for the bar and the principle; named
     follow-up path for the order]
  2. **Persona home for non-engineering domain repos** — RULED, and the
     recommendation was OVERRIDDEN. The recommendation was a two-axis split
     (codexFactory owns the engineering dimension, the owning domain stands
     up its own body for domain content); Brett ruled instead that
     codexFactory's councils review substantive PRs in ALL governed repos —
     a PR's diff is software regardless of the domain — with NO domain repo
     instantiating personas for this lane and the tenant
     `company-policy-lead` seat carrying the policy dimension. The
     adoption-change-per-repo mechanism survives; only the persona-home fork
     is removed. [proposal edit]
  3. **Company-policy-lead per-PR seating** — RULED, and Brett chose a
     bounded THIRD option rather than either surveyed shape. Rules-council-
     only remains the DEFAULT (the 2026-07-22 separation stands); as a
     declared exception a candidate class MAY carry a company-policy pull-in
     condition, defined by the `gate_rules_council` at class-definition time
     and never per PR, which pulls the seat into that PR's
     `merge_readiness_council` — fail-closed for those classes only, under
     the existing `missing_required_seat: refused` rule. [proposal edit;
     `design.md` Decision D marked SUPERSEDED IN PART, its text kept]
  4. **Ruleset interaction shape per repo** — RULED as recommended: the
     proven shape everywhere. Real App `APPROVE` satisfies required review;
     the council-verdict check-run stays verdict transport and is NEVER a
     ruleset-accepted satisfier; human review remains an always-available
     alternate path on every repo (no App-path-only repo); divergence needs
     its own recorded decision in that repo's adoption change. [proposal
     edit]
  5. **Risk-tier taxonomy** — RULED as recommended, split. The
     CONSTITUTIONAL FLOOR is decided now in three clauses: the ratified
     never-clearable floor is tier-independent and unoverridable by
     unanimity; classes touching contract bytes, gate/workflow definitions,
     credential surfaces, or security posture are permanently human-only;
     autonomous clearance is eligible only for docs-/derived-artifact-shaped
     blast radii. The enumerated, ordered tier VOCABULARY is deferred to the
     same evidence-driven follow-up path as (1). [proposal edit for the
     floor; named follow-up path for the vocabulary]
- **NOT RESOLVED BY THIS CLOSURE — three conflicts the retired fragment
  records rather than papers over**, named here because they must survive the
  folder: (a) Q2's override leaves the objection the recommendation was built
  around standing — a domain repo's PR whose CONTENT is domain governance is
  reviewed by a council with no standing in that domain; the accepted
  mitigations are `needs_human_review` at every class, the gate-rules
  council's human-only power, and the Q5 floor. (b) Q3's exception is a real
  inconsistency with the codexFactory council files' own "PERMANENTLY
  DISTINCT" 2026-07-22 wording, deliberately bounded rather than repealed; if
  that wording is ever amended, saying so is the amendment's job. (c) Q3
  against `design.md` Decision D as authored — superseded in part, not
  replaced, with the original text kept verbatim.
- **SEQUENCED after the doxBench UI sprint (Brett 2026-08-15 ruling on
  today's four staging topics)** — deliberately iterated and realized only
  once `doxbench-editing-model` Phase A, `staged-topic-outline-template`,
  and `doxbench-editing-model` Phase B have landed, so the governed review
  lane catches the workbench's steady state rather than blocking the sprint
  that is building it; the sibling `add-substantive-review-lane` proposal's
  own ratification read proceeds independently and is not gated by this
  ordering.
- Exit: each question resolved independently into a pre-ratification edit
  of the governing proposal, a named follow-up OpenSpec change (which is
  exactly where rollout order and the risk-tier vocabulary went, as this
  entry predicted), or a recorded decision Brett ruled directly and noted
  back into the fragment. This topic carried no exit change of its own.
  **CLOSED 2026-08-22** on the fifth disposition, per its own stated
  condition. What the closure itself did NOT do: it did not ratify the
  tracked proposal. The clarify round settled the five parked questions; the
  ratification of the requirement set was Brett's separate read, and he made
  it later the same day — `add-substantive-review-lane` is **RATIFIED
  2026-08-22** (record
  `openspec/changes/add-substantive-review-lane/review/ratification-2026-08-22.md`),
  where four further items were ruled: form elevation accepted, the Q1 bar
  counts any council-cleared verdict (App- or human-approved), the ordering
  principle stays absolute, and ratify. Two acts, one day, recorded
  separately — this topic's closing condition was the five dispositions, not
  the ratification.

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
  **PATH MOVED AGAIN 2026-08-21 when the change ARCHIVED.** The loose
  `supporting-docs/` folder was packaged into a deterministic bundle beside the
  archived change, per `document-lifecycle`'s `Supporting-document archive
  retention`, so the fragment is no longer a linkable file: it lives inside
  `openspec/changes/archive/2026-08-21-add-staged-topic-outline-template/supporting-docs.tar.gz`,
  with its per-file sha256 readable outside the bundle in the sibling
  `supporting-docs.manifest.yaml`. Named rather than linked, because a link
  would resolve to nothing.
  - `staged-topic-outline-template.md`
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
  `add-staged-topic-outline-template` was raised, ratified, and has sections
  1-4 realized and bookkeeping 6.1-6.3 discharged (gates 5.1-5.4 outstanding
  before archive). Q4's ruling — corrected by
  the change's Amendment 1 (2026-08-15) to `edit-document`, since `edit-apply`
  is the gate console's redline verb and cannot reach a session branch — is
  the hinge into `doxbench-editing-model`: it upgrades that topic's freeform
  chat rewrites into marker-scoped section patches, an upgrade neither
  realized Phase A nor Phase B built, recorded as a handoff on that staged
  topic's own fragment for a successor change. Q5 still rides Phase B as
  sequenced, because Q2 ruled opt-in migration and so the wheel's existing
  fallback stays for non-conformers.
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
    4 idea notes, 3 conflicts, 5 questions each with
    Context/Recommended answer/Explanation/Disposition status — all five
    DISPOSITIONED 2026-08-23, each carrying a dated disposition paragraph
    and a `Dispositioned-by:` line beneath its status line, plus two dated
    in-place corrections: the contract-home error (fixed in Q1's context,
    in its recommended answer and in the Impact section's matching clause)
    and Q3's "in-flight proposal" framing — exit.
- **Dispositioned 2026-08-23 — none of the five remains `open`.** Q2 and
  the account timing were RULED BY BRETT HEAP in session: the hosting
  identity is a dedicated Google Workspace USER account in the operating
  tenant's own domain, never a consumer Gmail, and the account is created
  now/soon. CONFIRMED the same day: the account EXISTS as
  `xFactor001@opensoft.one` (the earlier `xfactory-books@opensoft.one` was
  a working name and was never created), and Brett authorized raising the
  combined change on it. A platform fact the 2026-08-15 capture predates
  reinforces it — a GCP service account CANNOT drive NotebookLM (no API,
  consumer web UI only), so the hosting identity must be a Google user
  account, which is what a Workspace user is; that also settles the
  fragment's own loose "company service account" wording.
  Q1/Q3/Q4/Q5 were adjudicated against executed evidence. Q1: the
  recommended split stands, but its context was CORRECTED — the two-case
  fork is already a PROMOTED `credential-contracts` requirement ("The
  credential vault operator is an execution binding, never contract
  content"), not merely runbook prose, so the custody delta GENERALIZES an
  existing requirement and needs no new record kind (that schema has one
  closure against the roster schema's eleven — parsed counts, corrected
  2026-08-23 on Copilot's review note); the one-vs-two-changes
  fork closes to ONE COMBINED change. Q3: the mapping the question
  demanded was PERFORMED against the realized roster schema and its
  validator — 11 errors stated honestly (closed `identity_kind`, closed
  `admission_surface` routing non-Entra surfaces out of scope, closed
  residency, unresolvable `consent_ref`, no home for
  granted_by/granted_at/hosting_account), and a force-fit variant with
  eight marked lies that PASSES with one grantee and FAILS with two on
  `duplicate-identity-key`, because the grantee is not in the uniqueness
  tuple. The shapes are transposed (one principal / many scopes vs one
  scope / many principals), so the disposition is a DISTINCT small roster
  keyed on `(hosting_account, user, book_or_alias, role, granted_at,
  granted_by)` — the honest fallback, now proven rather than assumed. Two
  post-capture facts ride with it: the ratified identity-brokering family
  models the human-persona half (roster entries should reference a persona
  where one resolves), and its surface-adoption schema requires
  `human_accounts_held_by_surface: false`, so sharing to arbitrary
  unresolvable Google accounts is a shape the governed layer refuses —
  reinforcing the company-account direction. Q4: the governed MANUAL lane
  as recommended (no NotebookLM share/admin API exists, re-verified), with
  one unification the capture missed — the approval act's record IS the Q3
  roster entry, which also gives the lane the home the Impact section said
  it lacked. Q5: the `split-ideation-book-per-repo` retirement runbook is
  the template — one `--apply` re-creation, parity as per-book title-set
  equality plus a union reconciliation against THE CORPUS SCAN (not the
  legacy books) plus a final zero-pending dry run, then retirement by
  recorded manual act (archive-rename, delete the alias, retire the
  workspace record); realization notes: the sync passes NO profile today
  (`subprocess.run(["nlm", *args])`), so profile selection is real code,
  and two review findings (Codex on PR #272, verified) bound what "one
  run" covers — a plain `--apply` never creates live `xf-session-*`
  notebooks (each needs its own run, or a bulk mode, before the personal
  account is retired), and `ensure_workspace_record()` refuses to
  re-register a same-key book with a new provider id, so the cutover needs
  an explicit workspace-record replacement step rather than retirement
  alone.
- Open questions AS CAPTURED 2026-08-15 (all five now dispositioned above;
  kept for the record): (1) which capability owns the
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
  in the meantime. That sequencing rationale is SPENT as of 2026-08-23:
  `add-client-identity-roster` archived, its shape was actually tested,
  and the answer came back negative — the wait it imposed is over.
- Exit (updated 2026-08-23): ONE COMBINED OpenSpec change — MODIFIED
  `lifecycle-notebook-projection` (declared hosting-account field, `nlm`
  profile selection at sync time, share-out-from-the-account rule, and the
  amendment of the shared-account model that spec currently ratifies in
  text), MODIFIED `credential-contracts` (the two-case account-custody
  rule, generalizing the vault-operator-custody requirement already
  promoted there), the new small share-out roster shape, and one code
  surface (the sync's profile selection). The account precondition is MET:
  Brett confirmed `xFactor001@opensoft.one` on 2026-08-23 and authorized
  raising the change, so the topic exits via `add-notebook-projection-identity`
  rather than waiting. Opensoft's install is the declared Case A instance
  the change's migration path applies to.

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
- Files: **MOVED OUT OF STAGING 2026-08-21.** The topic exited via
  `add-doxbench-editing-phase-b`, so `scripts/proposal-support.py transition`
  moved its material into that change's `supporting-docs/` — status `staged` →
  `draft`, `Proposed by:` recorded, a per-file sha256 manifest and a byte-exact
  `source-snapshots/` copy, and the change's `.openspec.yaml` origin
  declaration byte-identical before and after (checked, because an origin
  mutated after ratification is rejected at the archive gate). The staging
  folder is now empty by design; this row stays as the topic's index entry and
  its exit record.
  **PATH MOVED AGAIN 2026-08-22 when the change ARCHIVED.** The loose
  `supporting-docs/` folder was packaged into a deterministic bundle beside the
  archived change, per `document-lifecycle`'s `Supporting-document archive
  retention`, so the fragment is no longer a linkable file: it lives inside
  `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/supporting-docs.tar.gz`
  (bundle sha256
  `3d3db064b9b2a9127dd3a92802591780277a6bff140052d5a936ec6a77d9bfa6`), with the
  fragment's OWN per-file sha256
  `16761d875d5603b75bfe4ab142669ccb435ba2a1b83b1988894e257830a6cd10` readable
  outside the bundle in the sibling `supporting-docs.manifest.yaml`. Named
  rather than linked, because a link would resolve to nothing.
  - `doxbench-editing-model.md`
    — primary: 26 claims, live `xspec:candidate` Why/What changes/Impact
    sections, 7 idea notes, 6 conflicts, 7 open questions each with
    Context/Recommended answer/Explanation/Disposition status, exit.
- **PARKED AT EXIT — two items this topic settled that are NOT adopted, and
  where each one now lives.** A topic exit must neither silently adopt nor
  silently drop what it carried, so both are named here with a location that
  survives this row:
  1. **Headroom is WATCH-LISTED, not adopted** (Claim 26, and the second-pass
     addendum's Claims 22–26). It survives as EXECUTABLE DATA rather than as
     prose: `scripts/ideation_dashboard/doxbench_packet.py`'s
     `WATCH_LISTED_CANDIDATES` records the candidate with all five of the
     topic's gates — the credential findings fixed and `SECURITY.md` truthful,
     telemetry default-off in the OSS build, prompt-cache fidelity stable
     across releases, a sandboxed trial showing net savings on doxBench's own
     workload, and a caller-metadata hook without which the lifecycle-status
     exemption could not live inside it — and its `WatchListedCandidate`
     constructor RAISES on `adopted=True`, so the parked state cannot be
     flipped by prose alone. Nothing in the capability depends on it. The
     reasoning stays readable in the moved fragment above.
  2. **The graph-engine GRADUATION TRIGGER is recorded, not fired** (Claims
     13–21's two-plane design; v1 retrieval is graph-less by ruling). It
     survives in `scripts/ideation_dashboard/doxbench_knowledge.py`:
     `graph_query` is a DECLARED but reserved-unimplemented tool whose fixed
     `RESERVED_REFUSAL` names the trigger a graph engine, store, or index would
     have to clear — a recurring need for dependency traversal, contradiction
     detection, or change-impact analysis — so a caller asking today gets a
     governance answer rather than a missing name.
  Neither is a Phase B task and neither blocks the landing; both are Brett's to
  fire, and both are reachable from live code rather than from a retired
  staging folder.
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
- A thread-per-document / set-wide-context chat memory model was added
  2026-08-18 via Brett's live-UI annotations (each loaded document gets its
  own persisted, savable chat thread; the model sees every thread across the
  staged set); which memory system persists and assembles that (Q7) was
  RULED 2026-08-18 (Brett, in-session, synthesizing his live-UI annotations,
  a web-research pass, and an external design review he supplied): a
  two-plane design — per-document sidecar thread-state files on the session
  branch as truth, plus a Staged-Set Knowledge Service (governed, shared,
  derived retrieval over the staged set and promoted findings) behind one
  MCP boundary, graph-less in v1 with a concrete graduation trigger for
  adding a graph manager later, and the chat running through the oh-my-pi
  harness via a thin stdlib bridge. Every Phase B question is now
  dispositioned (nine new claims recorded, 13-21); Phase B proposal drafting
  is next.
- Memory design COMPLETE 2026-08-18 (memory-gateway conformance +
  three-layer compression, shake-v1, Headroom watch-listed); Phase B
  proposal drafting NOW LAUNCHING.

## doxchat-auto-fit-routing

- Staging ID: `openxFactory:staging:doxchat-auto-fit-routing`
- Repository context: openxFactory owns every piece — `ideation-dashboard`
  (the doxBench capability and the chat-turn contracts),
  `contracts/schemas/xfactory-workbench-model-catalog.schema.yaml` (the
  routing declaration `contract-v1.38` released), and the runtime under
  `scripts/ideation_dashboard/` (`doxbench_model.py`'s catalog types and
  `effective_limit_bytes`, `doxbench_packet.py`'s assembled packet,
  `doxbench_bridge.py`'s adapter). No domain repo is implicated;
  codexFactory is a downstream CONSUMER of the catalog contract and would
  re-pin, not co-author.
- Source: Brett Heap, in-session 2026-08-21, immediately after ruling on
  rule 5' of the `contract-v1.38` model-catalog release. The ruling itself
  ("Swap to rule 5'" — bound a routing rule's declared limits against its
  RESOLVED model rather than the minimum over `routes_to`) was made BECAUSE
  a min-cap would have baked in semantics contradicting this direction;
  Brett then said "Stage the topic". The fragment carries his requirements
  as a VERBATIM origin quote, with the claim decomposition beside it so a
  reader can check the interpretation against the source.
- Claim: six settled claims, not reopened by the open questions —
  `auto` resolution becomes PER-TURN and fit-aware, decided against the
  assembled packet rather than declared once; a model too small for this
  turn is filtered out of the candidate set before any "best" question is
  asked; no fit is a HUMAN DECISION (warn and ask), never a silent failure;
  the answer may be session-sticky at the human's option, which makes it a
  standing consent with a scope and a subject rather than a UI preference;
  continuing means COMPRESSING the context to fit the best-fitting model,
  not truncating silently; and fit is MULTI-DIMENSIONAL — multi-modal need
  constrains the routable set independently of bytes, and raw size is one
  axis among several.
- Files:
  - [doxchat-auto-fit-routing.md](doxchat-auto-fit-routing/doxchat-auto-fit-routing.md)
    — primary: the verbatim origin quote, 6 claims, Why/What changes/Impact,
    5 idea notes, 5 conflicts (one added 2026-08-24: the silent trim), 6
    questions each with Context/Recommended answer/Explanation/Disposition
    status — ALL SIX DISPOSITIONED 2026-08-24, each carrying a dated
    disposition paragraph and a `Dispositioned-by:` line — a related-work
    section, and the exit. Conformant with `staged-topic-outline-template`
    (staged after ratification, so conformance is REQUIRED).
- Questions AS CAPTURED 2026-08-21 (all six dispositioned 2026-08-24; see the
  row above for where each landed): (1) where the fit decision lives —
  recommended the ROUTE, before dispatch at the existing precondition-7
  revalidation, since the port is ratified at exactly three members and a
  fourth would be "a second provider verb by another name" (CORRECTED at
  disposition: the route is right, precondition 7 is not — the packet does not
  exist until step 9's assembly); (2) what happens
  to the released `resolved_model_id` — recommended it STAYS as the declared
  default rather than being removed, since removal breaks consumers pinned
  weeks earlier for no gain, at the cost of a naming debt; (3) the capability
  vocabulary beyond byte size — recommended ONE closed additive `modalities`
  set and nothing else until a consumer names itself, on the roster's
  `admission_surface` precedent; (4) whether the session-sticky continue-all
  is a governed record — recommended that the TURN record state the posture
  it ran under (browser state alone rejected), because the failure that
  matters is a later reader not knowing the answer came from compressed
  context, which is the same class of defect §11.7's review found in the
  sidecar; (5) one change or three, and compression's home — recommended
  three sequenced exits with compress-to-fit CONSUMING task 10.7's
  posture-and-reason field rather than inventing a second way to say it, and
  reusing `context-compression-runtime`'s vocabulary where they overlap (10.7
  has since SHIPPED as `contract-v1.40`, and the disposition redefined (c) as
  disclosure of an already-silent trim);
  (6) whether the union badge survives per-turn routing — recommended YES,
  unchanged, because the human still chooses before the destination is known
  and narrowing the badge would disclose after the fact.
- Conflicts recorded (5, one added at disposition): the SILENT TRIM — under
  today's `posture: full` the server already fits the packet to the selected
  model's budget and drops evidence that reaches no wire field, so compression
  is not introduced by this topic but already runs undisclosed; against
  `contract-v1.38`'s own static
  `resolved_model_id`; against rule 5' itself, which loses its referent once
  resolution is per-turn; against `dispatch_turn`'s CLOSED four-code refusal
  set, which has no member for "no model fits, awaiting a human answer"; and
  against the `add-doxchat-model-intake` lane, which touches the same
  selector and the same catalog type.
- **SEQUENCING GATE CLEARED 2026-08-24.** It read "SEQUENCED after the doxBench
  sprint archives — after `add-doxbench-editing-phase-b` closes task 10.7 and
  its 13.8 evidence tick". That change ARCHIVED 2026-08-22 and 10.7 shipped as
  `contract-v1.40`, so the static resolution this topic builds on has shipped
  and been consumed. The remaining sequencing fact is different: the
  `add-doxchat-model-intake` lane (ratified, unbuilt) collides with exit (b) on
  `doxbench-chat.js`, `serve.py` and `doxbench_model.py`. Exit (a) touches only
  the schema, the type and the validator, so it is safe to raise now.
- Exit (updated 2026-08-24): THREE SEQUENCED CHANGES — (a) the catalog
  capability release (closed additive `modalities` + the two batched catalog
  follow-ups, each decided); (b) fit-aware routing (the step-9 route decision,
  the no-fit warn/ask surface and its recorded session consent, the
  turn-record facts with both badges); (c) compress-to-fit disclosure (a third
  `reduced_reason` constant on the released field, plus issue #263's non-blank
  hardening). Raise (a) first, at `Status: draft`.

## signed-execution-chain

- Staging ID: `openxFactory:staging:signed-execution-chain`
- Repository context: openxFactory owns the neutral family this proposes. It
  composes with four capabilities already governed here — `openxwallet` (the
  authority instrument a ratifier presents), `trust-anchor` (certificates and
  declared chain custody, realized at `contract-v1.37`), `identity-brokering`
  (who a signer is), and `roles-authority-model` (what authority means). The
  domain realizations are NOT openxFactory's: MedxFactory carries HealthLinc and
  LedgerxFactory carries LedgerLinc.
- Source: Brett Heap's expansion ruling 2026-08-27 — the signed-execution-chain
  vision goes ON CHAIN definitively, "especially financial and medical records";
  the domain mapping corrected in the same ruling (patient app = HealthLinc for
  MedxFactory; LedgerLinc = financial analysis and reviews for LedgerxFactory);
  and the expansion includes patients putting PHI portions on chain and working
  with hospitals and insurers through it — which this topic architects honestly
  as salted keyed commitments and anchored consent CHECKPOINTS on chain, records
  never, raising the narrowing as Q6 rather than assuming it. **Brett CONFIRMED
  that reading on 2026-08-29**, so the architected form IS the ruling's operative
  form rather than a topic's interpretation of one.
- **DISPOSITIONED 2026-08-29 — all seven open questions ruled by Brett Heap in a
  clarify sitting.** Q1 (wallet presentation in the shipped grant vocabulary plus
  proof-of-possession, recorded in the ratification record, no new artifact), Q2
  (the on-chain boundary as contract text with a validator refusing
  payload-shaped records AND unsalted commitments), Q4 (tranche one = links 1–3
  only; the transparency log is a tranche-1 artifact; the gate exists from
  tranche one) and Q7 (remote signing served by the harness controller, the
  runner's REQUEST recorded beside the signature, the controller corroborating
  against its own link-4 setup attestation; HSM a later hardening) were ruled AS
  RECOMMENDED. Q6 was CONFIRMED as recommended. **Q3 and Q5 DIVERGE**, and the
  divergences are labelled where they land in the fragment. Every gate is open:
  Q3/Q6 gated tranche 3, Q7 gated tranche 2's contract text, tranche 1 was never
  gated.
- **Q3's divergence, in two rounds and recorded as such.** Round 1, verbatim:
  "lets [sic] use Kaspa as primary and bitcoin as secondary" — inverting the
  study's ordering. It is kept in the record because a two-round ruling is only
  honest if the first round survives inside it. Cost facts were then put to him
  (Kaspa ~$0.000001/tx; Bitcoin-via-OTS $0 marginal per item on public calendars
  and ~$2.1k/yr for a self-run hourly calendar; a raw BTC transaction
  $0.12–0.36 with a spike history; a cheaper sidechain adds federation trust and
  saves nothing), and round 2 is the operative configuration:
  **"Bitcoin-via-OTS on
  everything"** — BOTH witnesses on EVERY anchored item, **Kaspa FIRST** as the
  primary/OPERATIONAL witness under the study's three unchanged conditions,
  **Bitcoin batched via OpenTimestamps as the DURABILITY witness with ten-year
  claims citing Bitcoin**, no selectivity and no third chain, receipts
  chain-agnostic and multi-anchor carrying BOTH proofs. "Primary" is order of
  arrival, never evidentiary weight — the ~3-day pruning finding is carried
  forward untouched. The vendored study is NOT edited: it is a dated research
  record, and one rewritten to agree with a later ruling stops being evidence.
- **Q5's divergence: RULED AGAINST THE RECOMMENDATION.** "Allow contract code
  later." Today's posture is preserved exactly as recommended — the anchoring
  chains are evidence-only and no tranche now planned puts contract code on any
  of them — but the change MUST NOT constitutionalize "no contract code ever" and
  MUST NOT gate a future adoption on the recommendation's stated trigger. A
  future change MAY adopt on-chain contract code on its own merits. The study's
  regulatory caution (EDPB/HIPAA posture, unaudited-stack risk, the
  irrevocable-deployment class) is RECORDED AS ADVISORY CONTEXT for that future
  change, not as a gate on it. Encoding a "not now" as a "never" would be the
  quiet-narrowing defect this topic already refused at Q6, run in reverse.
- Files: `signed-execution-chain.md` (primary fragment, template-conformant);
  `chain-selection-study.md` (vendored research input, 2026-08-27 — the
  chain-selection study answering Q3, carried verbatim below a relabelled header;
  research input, not governance text, and nothing in it is ratified by being
  vendored).
- The claim that makes it worth raising: **the chain is a PRECONDITION, not a
  record.** The weak version — omnigent records what it did and something later
  checks — yields an audit trail a compromised lane can write falsely. The strong
  version is that the omnigent layer REFUSES TO EXECUTE a step whose inbound chain
  does not verify, and the chain-validating merge gate refuses to land work whose
  chain is broken. A broken link is a FRAUD SIGNAL, never a warning: it means
  either the act did not happen or something is misrepresenting that it did.
- The tier model is FORCED BY A RATIFIED CONSTRAINT rather than chosen: omnigent
  workers carry `access_secrets: false`, so a worker cannot hold an authority
  credential and any design where a runner signs AUTHORITY contradicts ratified
  text. Authority stays human-held (tier 1, "who permitted this"); runners sign
  ephemeral per-task attestations issued by the harness controller under its own
  certificate (tier 2, "what actually ran"). Neither may stand in for the other.
  The constraint reaches the attestation key as well, which the first draft
  missed and the review round caught: the runner never holds it either, so the
  controller SIGNS on the runner's request and no key bytes cross into a worker
  — "ephemeral" is a lifetime, not a relaxation of custody. **Q7 RULED the
  mechanism 2026-08-29**: remote signing served by the harness controller, with
  the runner's signing REQUEST recorded alongside the signature it received.
- The PHI architecture is the part that must not be hand-waved: **raw PHI never
  goes on a public chain**, because append-only + world-readable + permanent are
  each individually incompatible with HIPAA, and "encrypted on chain" only makes
  key management the single permanent point of failure. Records live in encrypted
  off-chain custody with patient-held keys; the chain carries salted keyed
  commitments, commitments to consent-log CHECKPOINTS (the consent state itself
  stays in the governed permissioned layer, where it is not publicly linkable to
  a person), and the execution anchors. Hospitals and insurers
  verify through presentations without reading what they were not granted. The
  limit is stated rather than implied: **nothing on a chain can be un-published**,
  and no revocation reaches an already-disclosed copy.
- Why neutral: HealthLinc and LedgerLinc run the SAME chain, differing in payload
  and regulator rather than in shape, and "merge" is domain-interpreted — a git
  merge in codexFactory, a push to the patient app or printed signed orders in
  HealthLinc, a publication in LedgerLinc. A family that only fit one domain would
  belong in that domain's repository.
- SEQUENCING, and the collision risk: the four neighbours are ACTIVE OPENSPEC
  CHANGES, not staged topics, so their ratified text governs and this topic
  composes with it. `add-wallet-carried-review-authority` is the direct
  predecessor — its realized S2 issuer anchor IS link 1's instrument, and this
  topic must not re-invent a signing primitive. The live risk to avoid is
  inventing a SECOND identity or certificate vocabulary when three of the four
  already own one; every link should resolve to an existing family or be raised as
  an explicit gap.
- A conflict inside the vision itself, recorded rather than smoothed: a broken
  chain is a fraud signal AND nothing on chain can be un-published, so a false
  attestation that reaches the chain is permanent. That argues for anchoring LATE
  — committing only what has been validated — and is a design constraint on
  tranche three.
- 7 questions, ALL RULED 2026-08-29 — they were the topic's open set and are
  kept here as the record each disposition is read against. None ever blocked
  tranche one; Q3 and Q6 were the tranche-three blockers and Q7 gated tranche
  two's contract text, and all three gates are now open. The set:
  wallet-presentation mechanics; the exact
  on-chain boundary (recommended as a REFUSING validator rather than prose,
  mirroring how the hosting record refuses secret-shaped fields by name — and now
  refusing UNSALTED commitments too); chain selection — **the research fan-out
  COMPLETED and is vendored as `chain-selection-study.md`**, so Q3 carried its
  recommendation (Bitcoin primary anchor via OpenTimestamps aggregation, Kaspa
  optional secondary under three conditions, consent logic in the permissioned
  layer, no contracts on the anchoring chain) into a ruling that **inverted its
  ordering and dropped its optionality**; tranche boundaries; whether smart
  contracts or an L2 are in scope (evidence-only for today, but the "never" was
  **overruled** — Ethereum L2 + EAS remains the study's answer IF public
  programmability is ever forced, as advice rather than as the only door); and
  **Q6 — whether the ruling's "patients put PHI portions on chain" means
  COMMITMENTS**, the one place the topic interpreted a ruling rather than
  applying it, raised for Brett rather than assumed and **CONFIRMED by him**; and
  **Q7 — where an attestation signature physically happens**, added by the
  review round on this topic's own PR, which correctly read the draft's per-task
  key as runner-held custody.
- The study also settled Brett's three priors, recorded honestly including the one
  that failed: "Kaspa is one of the only non-captured chains" **QUALIFIED** (launch
  fairness holds; operational capture — pool concentration, a miner targeting ~16%
  of hashrate, VC-funded L2s absorbing core devs — does not support the absolute);
  "Bitcoin is just too expensive" **REFUTED for anchoring** (Merkle aggregation
  makes it ~$0 marginal, ~$2.1k/yr even self-anchoring hourly) — this refutation
  is what moved Bitcoin into an anchor seat at all, the study's primary one and,
  after the ruling, the durability witness on every anchored item; it is also
  what turned Q3's round one into round two; "KAS is fractions of a penny"
  **CONFIRMED and understated** (~$0.000001–0.000003), with the honest caveat that
  it partly reflects low demand and an unfunded security budget.
- Exit path: OpenSpec change(s) in three tranches, and **no tranche is held by a
  question any more** after the 2026-08-29 sitting. **Tranche 1 — signed
  ratification + atomic enrollment, plus the off-chain signed transparency log
  that IS the record — is composable TODAY and was never gated**; it needs no
  omnigent layer and no chain, and Q4 fixed its boundary at links 1–3. Tranche 2
  (harness + runner attestation) had its question-gate opened by Q7 and may now
  name the signing mechanism in contract text; what remains for it is machinery,
  the omnigent layer and the PKI plane. Tranche 3 (on-chain anchoring) had both
  its question-gates opened by Q3 and Q6; it builds to the RULED configuration
  (Kaspa first, Bitcoin-via-OTS on everything), builds the chain-agnostic
  MULTI-ANCHOR RECEIPT first — the receipt is what keeps the anchor choice
  reversible over a 10-year horizon, and it carries the anchor transaction and
  its inclusion proof rather than a block header and a transaction reference,
  which prove nothing once the transaction is pruned — and waits on the PKI plane
  rather than on a ruling. The chain-validating gate should exist FROM TRANCHE
  ONE validating a short chain, so the refusal path is exercised from the start
  rather than first tested when it matters most; Q4 ruled that sequencing.
- **EXIT 1 IS RAISED, 2026-08-29 — the active change `add-signed-execution-chain`**
  (`openspec/changes/add-signed-execution-chain/proposal.md`), carrying links 1–3
  plus the transparency log plus the short-chain gate, with a NEW neutral
  `signed-execution-chain` capability of nine ADDED requirements. **NOT recorded
  as `Exit taken:`, deliberately**: that record silences `staged-candidate-aging`
  only when it names an ARCHIVED change, and this topic must keep ageing while
  tranches two and three are unraised. The packet renames link 2's act **`chain
  inception`** — `specs/025-openxfactory-review-lane-caller/spec.md` FR-008
  already owns "enrollment" here for the entry of a candidate class into a
  `merge-approval-envelope`, and a second adjacent sense on the same pull
  requests is the collision the 2026-08-28 seats named as the live risk.
- **The packet is AMENDED TO THE SEVEN RULINGS** (`#499`, squash `9c501df6`) and
  no longer carries a clarify round of its own: Q1's answer is encoded as ruled
  rather than flagged, Q4's two sequencing facts are met by the transparency-log
  and short-chain-gate requirements, and Q5 is restated so that **no trigger
  condition is written here in advance**. Q2, Q3, Q6 and Q7 govern the later
  tranches and are recorded, never pre-encoded — the packet names no chain, no
  anchor and no contract-code posture.
- **NARROWING A IS ADOPTED — ruled by Brett Heap, 2026-08-29, in session.** Tier 1
  is **RATIFYING** authority. Agent-held **REVIEW** wallets stay lawful, so the
  realized `wal-agent-mrc-0001` is untouched; what the gate refuses is an
  agent-held wallet performing the **ratifying** act. The literal tier-model
  sentence would have refused an artifact this repository already runs, and the
  ruling narrows the tier rather than the artifact. Narrowing B — Q1's "rather
  than a new artifact" read as *invent no new artifact* — is carried by Q1's own
  ruling, which says no new artifact is created for the presentation.
- **THE COLLAPSE, ruled by Brett Heap 2026-08-29 in session.** Two parallel
  sessions raised this same tranche into the same change directory within three
  minutes (`#494` and `#495`). He ruled `#495` the surviving base and closed
  `#494`, whose four hardenings are carried into this packet by harvest rather
  than discarded: the actor-to-wallet attestation binding, per-ratification
  uniqueness, one digest construction for every digest, and the named-reader
  required-check rule.
- **State: FULLY RULED and DRAFTING GREEN-LIT.** Brett Heap gave the drafting
  green-light on **2026-08-29, in session**, which is the authorization the
  clarify sitting deliberately did not give. The packet remains **UNRATIFIED** —
  ratification is a separate act and is his.

## notebook-access-wallet-governance

- Staging ID: `openxFactory:staging:notebook-access-wallet-governance`
- Repository context: openxFactory owns every capability this topic touches —
  `lifecycle-notebook-projection` (the books, the share-out roster ratified by
  `add-notebook-projection-identity`, and the sync that performs provider
  acts), `openxwallet` (the candidate holder of the grant authorities), and
  `identity-brokering` (the persona half of a grantee). The provider act is
  `nlm share invite --profile`, run under the declared hosting account.
- Source: Brett Heap's direction 2026-08-24, in session, verbatim: "we are
  doing the sharing thru the app. so if we allow org wide in the google
  machinery, we still have this on the user right? can we add this to the
  wallet and then control with repo or even more fine grain access?" Two
  question-prompt rulings followed: the Google-side posture is RESTRICTED with
  the app as the SOLE GRANTOR (org-visible rejected), and this topic is staged
  rather than proposed now.
- Claim: seven settled claims, not reopened by the open questions — sharing
  happens through the app; the posture is restricted; Google's ACLs are the
  OUTER enforcement, so an org-visible book is provider-granted access no
  app-side record can subtract (which is the answer to Brett's own "we still
  have this on the user right?"); deny-by-default at the provider with every
  grant flowing through the governed lane; the provider's enforcement atom is
  per-notebook, per-user, viewer-or-editor and nothing smaller; per-repo
  control maps to per-book because the books are already per-repo; and
  finer-than-book granularity is not provider-enforceable, existing only
  through our own surface and named as a NON-GOAL of the Google half.
- The org-visible rejection is doctrinal, not preferential: `client-identity-roster`
  promotes that where a provider-enforced principal IS available it SHALL be
  used, and that recording a bound as provider-enforced when no per-unit
  principal exists SHALL be a finding. Google offers a per-notebook, per-user
  principal, so org-visibility would take an available provider-enforced bound
  and downgrade it to a logic-enforced one — our records asserting a
  restriction the provider is not applying.
- Files:
  - [notebook-access-wallet-governance.md](notebook-access-wallet-governance/notebook-access-wallet-governance.md)
    — primary: 7 claims, live `xspec:candidate` Why/What changes/Impact
    sections (targets `lifecycle-notebook-projection` and `openxwallet`, both
    resolving), 4 idea notes, 3 conflicts, 7 open questions each with
    Context/Recommended answer/Explanation/Disposition status, exit.
- Open questions (none blocking, all `open`): (1) may an openxWallet grant
  scope an EXTERNAL provider's resource — checked against the schema, and the
  answer is narrower than the question expects: `scope`'s PROPERTY SET is
  closed (`additionalProperties: false`) so no provider or provider-side role
  can be written — though `scope.objects` takes free-form identifiers, so a
  book id IS writable and simply confers nothing at the provider — and
  `audience` requires a `wallet_ref`, so an ordinary human grantee cannot be
  the audience at all.
  Recommended answer keeps the wallet holding the AUTHORITY TO PERFORM THE
  GRANTING ACT while the provider's ACL remains the access — three nouns kept
  apart. The fragment's Q1 carries a dated correction: it was first drafted
  claiming the scope was open and that such a grant would validate; (2) whether the ratified
  roster entry BECOMES the wallet-governed record or a wallet grant points at
  it — recommended one record, since the ratified text exists precisely to stop
  an audit trail sitting beside the roster; (3) what revocation means
  provider-side, contrasted with PR #282's bearer-secret lesson (a Google ACL
  is a reference the provider evaluates per request, so removal genuinely
  removes access — the opposite of a disclosed bearer secret); (4) who approves,
  and whether this topic names the actor and closes the stranded task 2.4 of
  `add-notebook-projection-identity`; (5) whether a repository may declare its
  own book's access policy as a DERIVED input rather than an independent
  authority; (6) where finer-than-book access lives, given Google cannot
  enforce it — recommended as a named non-goal here and a separate topic for
  the surface-side route; and (7) how a grantee is NAMED, since a persona's
  `subject` pattern admits no `@` — an email is unrepresentable there by
  construction — while the provider act `nlm share invite <notebook> <email>`
  needs exactly an address, so the recommendation carries both with distinct
  jobs: the persona as the durable governed identity, the email as a provider
  addressing datum marked as such.
- Conflicts recorded, not resolved: the wallet's "never an identity substrate"
  bound against a roster entry keyed on a user; the risk of reopening the
  deliberate decision that kept the roster OUT of `contracts/` (which would
  fire the contract-release ritual); and that two of the three capabilities
  this topic would amend are carried by ACTIVE changes whose deltas are
  ratified but UNPROMOTED.
- **SEQUENCED after the migration thread's held steps clear** (Brett, 2026-08-24
  — staged rather than proposed for this reason). There is nothing to grant
  access to under the declared account until the books are re-derived there;
  the migration is in flight as PR #289.
- Exit: iterate until all seven questions carry a disposition other than `open`,
  then raise ONE OpenSpec change carrying the `lifecycle-notebook-projection`
  delta (wallet-governed roster entry, the grant lane's provider act,
  revocation semantics) together with whatever `openxwallet` delta question 1
  resolves to.

## treatment-options-engine

- Staging ID: `openxFactory:staging:treatment-options-engine`
- Repository context: SPLIT on purpose. openxFactory owns the neutral half —
  `governed-derived-model` — with `omnigent-domain-overlay` (constitutional
  `execute_final_action: false`) and `workflow-gate-contract` (where the
  clinician's decision is recorded) supplying refusal and gate surfaces the
  topic reuses rather than re-invents. MedxFactory owns the realized half:
  `root-truth-grounding` (the SPL §6 / §12.1 backfill over already-pinned
  custody XMLs), `terminology-normalization` (drug-class and indication mapping
  tables) and `treatment-plan-generation` (the engine). Staged HERE because the
  neutral delta is the one that needs designing; the Medx work is comparatively
  mechanical once it lands. The fragment deliberately does NOT fence the Medx
  capabilities as `xspec:candidate` targets — they do not resolve from an
  openxFactory document and fencing them would emit tag-hygiene findings for a
  claim this repo cannot host.
- Source: Brett Heap, in session 2026-08-26, deciding to build rather than
  explore — "we will build this" — with the capability given in six steps: list
  all drugs INDICATED for the condition, remove those CONTRAINDICATED for the
  patient, check INTERACTIONS against current medications, weigh ADVERSE
  REACTIONS, REBALANCE toward a combination with fewer negative and more
  positive interactions and a better reaction profile (rerunning when the chart
  observes non-response after a trial period), and an OFF-LABEL MODE running the
  same engine with the evidence-grade gate lowered and mechanism-of-action
  similarity admitted as a candidate generator.
- Claim: seven settled, not reopened by the questions — it is a build decision;
  the engine PROPOSES and a clinician DECIDES (the governance boundary, and not
  a dial: Omnigent constitutional `execute_final_action: false` and
  `access_secrets: false` hold, the treatment-plan gate stays human-reviewed,
  and nothing selects, orders, or cycles a regimen); the rebalance trigger is a
  charted OBSERVATION, never a timer and never an automatic rerun; every line of
  every output cites a root-truth record, with un-citable steps surfaced as gaps
  rather than run silently; on-label first, with off-label a separate MODE whose
  outputs are structurally un-mixable with on-label ones; the interaction
  severity and combination weights are EDITORIAL POLICY — versioned,
  human-reviewed, and visible in every output that used them; and the backfill
  FETCHES NOTHING NEW, running over the 1,298 custody SPL XMLs already pinned by
  digest.
- Corpus recon 2026-08-26 (measured, and it corrected the described shape):
  6,506 records over 1,302 distinct `medication_*` concepts, 1,298 custody XMLs
  (261 MB) under `var/root-truth-sources/`, ≈22% of the 5,803-row prescribable
  RxNorm ingredient set. Four corrections that change the deltas: (1)
  `adverse_effect` is ALREADY the ninth member of the closed ten-member
  claim-type enum (`scripts/root_truth/validate_root_truth.py:24-25`) with 3
  records, so the §6 work is a backfill under an existing member and not a new
  claim type — while `mechanism_of_action` genuinely does not exist and the
  nearest member, `target`, holds 1 record; (2) the drug→condition edge is
  effectively absent — exactly 5 of 6,510 grounded pairs are `condition_*`, and
  indications are one prose blob per family (`RT-SIMVASTATIN-IND-0001` carries
  six indication limbs in a single `claim` string) — so the engine's first step
  is not answerable from the corpus at all today; (3) the condition namespace
  already carries two colliding id conventions, generated `condition_<icd10>`
  from the 98,184-row FY2026 table versus curated readable slugs in
  `examples/terminology/tables/conditions.yaml`, with the generated manifest
  stating curated keys are SKIPPED at generation, and the five existing
  condition pairs use both; (4) evidence_grade is already multi-valued (6,499
  `regulatory_label`, 3 `retrospective_cohort_study`, 2
  `clinical_practice_guideline`, 2 `public_health_guidance`), so the off-label
  floor has real grades to drop to. There is no drug-class field anywhere.
- Build order (Brett's, with one governance note): (1) backfill §6 + §12.1 over
  existing sources — NOTE that the extractor model is pinned by
  `medx.domain.policy.plan_authoring_models` v1 at `claude-fable-5`, whose own
  `policy-revision-is-governed` position says the admissible set moves only
  through an OpenSpec change, so re-pinning extraction to a cheaper tier for
  ~2,600 extractions is a POLICY VERSION BUMP rather than a configuration
  change; (2) the MED-RT class/indication/MoA table via RxClass, scripted and
  deterministic with no model in the loop; (3) the derived treatment-options
  model, on-label only; (4) the interaction-severity table, then rebalance
  (never rebalance first — a search built before the scale hard-codes the
  judgement); (5) off-label mode.
- Files:
  - [treatment-options-engine.md](treatment-options-engine/treatment-options-engine.md)
    — primary: 7 claims, a measured current-state section, three live
    `xspec:candidate` blocks (all targeting `governed-derived-model`, all
    resolving), the Medx-side delta in unfenced prose, a build-order section, 6
    idea notes, 6 conflicts, 10 open questions each with Context / Recommended
    answer / Explanation / Disposition status, a related-work map, and a
    two-change exit.
- Open questions (10, all `open`): (1) which reference GRADES interactions and
  can we cite it — recommended: define our own small ordinal scale as the
  editorial policy artifact rather than adopt a commercial one, since a scale we
  cannot redistribute makes the "weights visible in every output" obligation
  unsatisfiable; (2) how patient state enters — recommended: yes, through the
  promoted `one-patient-integration-contracts` snapshot, pinned per run with no
  second path, the open part being whether the snapshot's current shape carries
  allergies and the active medication list at enough fidelity to key
  interactions; (3) where POSITIVE-interaction evidence comes from — recommended:
  split the term, since pharmacokinetic boosting IS label-grade and in the
  corpus already while clinical synergy is guideline-grade and must contribute
  separately rather than blend into one score; (4) ICD-10 vs SNOMED —
  recommended ICD-10-CM now (SNOMED needs an affiliate licence and the promoted
  licence commit rule is structural), retiring the curated slugs to aliases and
  carrying the code system alongside the concept so SNOMED is later additive;
  (5) whether adverse-reaction weighting needs INCIDENCE data — recommended yes
  where §6 presents tables, because severity without incidence ranks a
  30%-incidence nuisance level with a 0.01% catastrophe, which also makes the §6
  backfill materially more expensive than §12.1 and feeds the model-tier
  decision; (6) off-label consent and liability gates in Hermes — recommended a
  DISTINCT consent purpose reusing the promoted machinery, with the mode and
  floor as a structural disclosure, and no attempt to encode liability beyond
  recording who requested what; (7) **blocker** — is mechanism-of-action the
  existing `target` type or an ELEVENTH enum member, recommended eleventh
  member because a molecular target and a mechanism are different claims and
  off-label similarity reasons on the mechanism, and it must settle before
  extraction because it fixes every record id; (8) is the engine a new Medx
  capability or a MODIFIED `treatment-plan-generation` — recommended MODIFIED,
  since the nine promoted requirements (charted-diagnosis entry point, citation
  from a pinned run, knowledge-basis declaration, closed worker plane, consent
  purpose, model pin, plan-G1 fixture replay with zero EMR writes) are all
  needed unchanged; (9) **blocker** — which domain policy authorizes
  `person_modeling: identified_persons_under_policy`, given the promoted family
  FAILS validation when the referenced policy does not exist and MedxFactory's
  `models/derived-model-conformance.yaml` declares its single `dream_simulation`
  family as `synthetic_only` at `scope: domain`; recommended a new
  `patient_derived_modeling` domain policy rather than stretching
  `patient-consent-instrument`, which answers a different question; (10)
  **blocker** — whether RxClass/MED-RT and WHO ATC clear the pin registry's
  licence commit rule, recommended MED-RT under the existing derived-table
  pattern with ATC as a separate pin, and FDA EPC alone (label-derived, already
  in custody) as a genuinely acceptable fallback.
- Conflicts recorded, not resolved: the claim-type enum is closed at ten ON
  PURPOSE and Q7 wants an eleventh; editorial weights are un-sourced numbers
  entering a corpus built to refuse un-sourced assertions (the neutral
  `editorial_weights` declaration is a reconciliation, not an absence of
  tension); `treatment-plan-generation`'s "charted diagnoses are the only plan
  entry points" versus an off-label generator that reaches drugs no charted
  diagnosis indicates — whether that requirement bounds the entry point or the
  whole candidate set must be read before off-label is built; the Medx
  conformance file's `synthetic_only` dial is currently INCONSISTENT with what
  this topic needs; the two condition-id conventions, where a miss in the filter
  chain looks exactly like "no drug is indicated for this"; and that "rebalance
  reruns" reads like a loop claim 2 forbids, so the proposal must state the
  trigger as an event a human authored.
- Exit: TWO changes, neutral first. The neutral change modifies
  `governed-derived-model` (recommendation member role, evidence-floor dial with
  declared relaxed modes, editorial-weights declaration, plus validator support)
  and can be raised once Q7, Q8 and Q9 carry dispositions — those three
  determine whether the Medx family can be declared against the role at all. The
  Medx change (or changes) covers the corpus backfill, the new terminology
  tables and the engine, and cannot be raised until Q10 clears and the
  extractor-model policy re-pin is made or explicitly declined. Q1's severity
  scale must be decided BEFORE any rebalance work begins rather than alongside
  it.

## openxwallet-neutral-home

- Staging ID: `openxFactory:staging:openxwallet-neutral-home`
- Repository context: SPLIT across three homes on purpose. `opensoft/openXwallet`
  (to be created) becomes the neutral product's home and owns both contract
  families, the validator, the syntax gate, the conformance corpus and the two
  promoted capabilities. openxFactory keeps the SEAM — `governance/review-authority/`,
  the `trust-anchor` / `identity-brokering` / `roles-authority-model`
  compositions, Speckit 013/014, and all ideation provenance — and consumes the
  product at a commit-and-digest pin. The xFactory aggregation gains a root-level
  `openXwallet/` submodule. `LedgerxWallet` is the first domain descendant.
- Source: Brett Heap's direction 2026-08-26, in session. He asked two questions —
  is openXwallet a repo-level project or features inside another repo, and do
  domains integrate the neutral product directly or through a `<Domain>Wallet`
  repo that pins it — and then ruled all eight recommendations at once, verbatim:
  "approve R1-R8 as recommended, stage the topic and propose". Origin provenance
  is the `agent-certification-wallets` brainstorm (Brett, 2026-07-15/16) and the
  promoted change `2026-08-08-add-openxwallet`.
- Claim: eleven settled claims, not reopened by the open questions — the eight
  rulings R1-R8, the no-counter-example finding, the four descendant-repo rules,
  and the byte-identical-first-release rule. R1 names the repo and brand
  `opensoft/openXwallet` on the ratified house `openX<type>` form, which removes
  the `openxWallet` family exception `docs/openxdox-naming.md` currently records
  and therefore owes that record an Amendment 2. R2 FREEZES every machine key in
  v1 — paths, capability ids, the `xfactory_wallet_*` kind prefix, the envelope
  kind `openxfactory-openxwallet-contract-schema`, finding codes, filenames —
  because brand and label differ by design and a rename landing in the same
  change as the move would be unbisectable. R3 splits along a seam rather than a
  file type: the wallet primitives are ratified holder-agnostic and non-substrate,
  so they are not factory-layer content, while how the review gate USES wallet
  authority is. R4 makes the dependency bidirectional and acyclic. R5 places the
  submodule at the aggregation's neutral root. R6 keeps the register and moves its
  reader. R7 fixes descendant casing at `<Domainx><Product>`. R8 makes
  `LedgerxWallet` first.
- The descendant-repo finding is the reusable half: **the house standard is
  already the domain descendant repo, and there is no counter-example.** openChart
  is consumed through MedxChart, openPractice through MedxPractice, and openAvatar
  through MedxAvatar and LedgerxAvatar (DTN-022, Brett 2026-08-03 — descendants are
  "pin-and-profile DISTRIBUTIONS … never code forks"). No DomainxFactory consumes
  any open* product by direct integration; the only direct consumer of neutral
  contracts is openxFactory-as-layer through `stack.yaml`, and openxFactory is the
  neutral layer rather than a domain. So the topic ratifies the pattern ONCE as
  `domain-descendant-boundary` — pin by commit TWICE (gitlink plus
  `contracts/<product>-pin.yaml`, same commit); carry only profiles, overlays,
  branding, deploy config and domain validators; nest into the DomainxFactory as a
  submodule and optionally aggregate at `xFactories/`; create lazily on the
  domain's first profile — instead of paying for a fourth bespoke boundary change.
- Inventory measured against the live corpus 2026-08-26: two neutral contract
  families, one validator plus a syntax gate and its tests, one CI workflow, two
  promoted capabilities (`openxwallet` 8 requirements, `openxwallet-agent-profile`
  3, registered at `contract-v1.31`), five Speckit features (006/010/012/013/014),
  a live governance estate, and a conformance corpus of 17 positives and 36
  negative confirmations. Four facts constrain the sequencing: validator rule (g)
  reads `contracts/schemas/hermes-job-envelope.schema.yaml`, so a moved validator
  with no vendored copy fails on every run; `scripts/validate-trust-anchor.py`
  hard-exits when `contracts/openxwallet/openxwallet-custody.registry.yaml` is
  absent, so consume-and-shed must be ONE atomic PR; LedgerxFactory's
  `tests/validate_wallet_estate.py::find_openxfactory()` fails loudly rather than
  skipping, so its forward-compatible finder lands FIRST; and codexFactory's
  merge-gate floor pins `governance/review-authority/register.yaml` in
  `opensoft/openxFactory` with a parser that refuses wildcards, so the register
  cannot move. Two negatives verified: wallet content is NOT in `CONTENT_KINDS`,
  so hermes-install's reseed is untouched (the reseed-drift fix is not a
  precondition after all), and `contracts/releases/*.digests.yaml` never indexed
  the family, so there is nothing to carry — a gap to record, not to backfill
  inside a byte-identical move. Bookkeeping surface: `contracts/manifest.yaml`
  rows 1967-2082 removed plus seven incoming citations reworded to the pin (2089,
  2146, 2251, 2287, 2423, 2473-2475, 2494-2495).
- Files:
  - [openxwallet-neutral-home.md](openxwallet-neutral-home/openxwallet-neutral-home.md)
    — primary: 11 claims, a measured evidence-and-inventory section, three live
    `xspec:candidate` blocks (all targeting `openxwallet`, all resolving; the two
    ADDED capabilities are deliberately unfenced because neither resolves yet), a
    seven-item sequencing-constraints section, 5 idea notes, 5 conflicts, 5 open
    questions each with Context / Recommended answer / Explanation / Disposition
    status, and a one-change exit.
- Open questions (5, all `open`, none blocking the move): (1) promote the
  review-authority register to a wallet primitive or split the reader back into
  openxFactory — recommended NEITHER yet, carried to the council, because either
  answer converts a provably-empty diff into a design change and the promotion
  argument only strengthens with a second consumer; (2) whether
  `tenants/ledgerxcorp/wallets/*` records move into `LedgerxWallet` or stay tenant
  data — recommended profiles move, records stay, and it is Ledgerx's ruling
  inside its own boundary change; (3) the deprecation window for renaming the kind
  prefix `xfactory_wallet_*` to `openxwallet_*` — recommended dual-accept for
  exactly one bundle release, closing on consumers-migrated rather than a date,
  since the consumer set is one; (4) when `openXwallet-Install` becomes real and
  whether Hermes is its issuer host — recommended register the NAME and build
  nothing, since the runtime has zero footprint today and the whole arc gates
  successors on consumers; (5) openXwallet's own bundle-tag scheme — recommended
  `wallet-vN.M` with openxFactory's bundle semantics and NO range expression in
  the pin, keeping the tag advisory while the digest stays authoritative.
- Conflicts recorded, not resolved: the aggregation's working rule #1
  ("domain-neutral contracts live ONLY in openxFactory") is flatly contradicted
  the moment this lands and is the rule currently in force until amended;
  `docs/openxdox-naming.md` is `Status: ratified` and names `openxWallet` an
  exception, so it says the opposite of R1 until Amendment 2 exists; TWO of the
  three descendant precedents are NOT ratified in this repo — checked 2026-08-26,
  `create-medxchart-overlay-boundary` and `create-medxpractice-overlay-boundary`
  both stand `Status: draft`, leaving DTN-022's openAvatar ruling as the single
  ratified member of the precedent table; R2 ships a known-stale vocabulary into a
  brand-new repo's first release; and R6 leaves one kindless contract's data and
  its only schema in different repositories.
- Readiness: RATIFIED 2026-08-26 as `split-openxwallet-repo` (PR
  opensoft/openxFactory#391), on Brett Heap's in-session ruling taken after both
  required checks on that pull request reported green — ratified AS PROPOSED,
  with R1-R8 standing unchanged and Q1-Q5 carried at the design's dispositions
  (Q1, Q2 and Q3 travel; Q4 `openXwallet-Install` is a registered NAME with no
  repository, Q5 is `wallet-vN.M` with no range in the pin). Realization ran
  through Speckit features, one per `tasks.md` group in the design's Migration
  Plan order — OpenSpec ratified the boundary and Speckit built it — from the
  change's own packet bookkeeping (Amendment 2 to `docs/openxdox-naming.md`, the
  xFactory working-rule #1 amendment) and P5a.1, LedgerxFactory's three-candidate
  finder that lands before the carve, through to P6. **THE EXIT IS TAKEN: the
  change is ARCHIVED 2026-08-28** as
  `openspec/changes/archive/2026-08-28-split-openxwallet-repo/`, on
  merged-plus-green realization evidence across six repositories — openXwallet
  (`wallet-v1.0`, then `wallet-v1.1`, the tag openxFactory pins), openxFactory
  (`contract-v1.47`, then `contract-v2.0` = `c9a1500e1a960be827cd714d8024d9aacb40aeb2`,
  which shed 92 local copies), codexFactory (#117), xFactory (#161),
  LedgerxFactory (#25, #29, #30, #31) and OpsxFactory (#129) — plus the first
  domain descendant, LedgerxWallet at `lxw-v1.0`. **The row above and this
  fragment are KEPT ON DISK as provenance**, on the `agent-wallet-identity`
  precedent: that topic's change archived 2026-08-08 and its row stayed "because
  the staged fragment remains on disk as provenance carrying the deferred
  material", and the reason is the same here — Q1-Q5 and the named successors
  outlive the change that carried them. **The topic is NOT fully exited.** It
  still carries a LIVE successor exit, `create-ledgerxwallet-overlay-boundary`,
  ratified in openxFactory #449 and realized as LedgerxWallet, but an ACTIVE
  change still
- Exit: ONE OpenSpec change, `split-openxwallet-repo`, declaring a code surface of
  scripts, CI workflows, pin files and submodule gitlinks — so it archives only on
  merged plus green realization evidence. It carries the two REMOVED deltas with
  successor locations recorded, the two ADDED capabilities, the two MODIFIED
  deltas, Amendment 2 to the naming record, and the working-rule amendment.
  Speckit features follow per phase (carve and scaffold with byte-identity proven
  before tagging; consume and shed in one atomic PR; aggregate the root submodule;
  repoint consumers), and the first domain descendant is `LedgerxWallet` via
  `create-ledgerxwallet-overlay-boundary` on the standard this change ratifies.
