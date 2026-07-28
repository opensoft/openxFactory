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
| [mobile-dashboard-surface](#mobile-dashboard-surface) | `avatar-first-ui` realization (possibly a small ADDED requirement) | 1 | Ready to iterate — the layer defaults are already ratified; main forks: shell platform vs the frozen AVC ports, sequencing vs `avatar-pilot-hardening` |
| [workstation-app-shell](#workstation-app-shell) | `avatar-first-ui` realization (possibly a small ADDED requirement for the workstation shell) + MODIFIED `ideation-dashboard` (the local serve becomes app-managed) | 1 | Ready to iterate — layer defaults already ratified and the motivating defect verified; load-bearing content is the Worker Host App boundary (two OS principals, one shell) and codexFactory's missing subject surface; 5 open questions, the shell-platform fork blocks implementation |
| [avatar-pilot-hardening](#avatar-pilot-hardening) | ADDED `avatar-pilot-hardening` | 1 | Blocked — last successor; gated on `qualify-avatar-live-voice` + the client lab landing, plus its own open forks |
| [ideation-action-plane](#ideation-action-plane) | ADDED `ideation-intent-plane`; MODIFIED `document-lifecycle` (gates happen on main); fragment 2: MODIFIED `lifecycle-notebook-projection` (Drive membrane) | 2 | Exit 1 raised at this gate (`add-ideation-intent-plane`); fragment 2 blocked on the Drive↔NLM markdown-ingestion spike |
| [client-credential-escrow-registry](#client-credential-escrow-registry) | MODIFIED `credential-contracts` (escrow registry + break-glass custody; possibly a sixth record kind); touches `client-infrastructure-liaison` | 1 | Ready to iterate — design inputs settled with Brett 2026-07-19; 6 open questions (delta shape + break-glass topology hardest); first consumer live (opensoft self-client QA install) |
| [client-layer-tuning](#client-layer-tuning) | MODIFIED client scaffold (`roles/` + FAO + `cost_reporting_steward`); ADDED client content schemas + `validate-client-content`; wizard verb in hermes-install | 1 | **COMPLETE 2026-07-24** — all three exits ratified, realized, archived (2a contract-v1.17 + canonical spec `client-layer-tuning`; 2b codexFactory defaults; 2c wizard + unified client seeding). The opensoft tenant is tuned and seeded live (phase-2 evidence note). Primary doc + drafts retained as provenance |
| [consent-instrument-contract](#consent-instrument-contract) | ADDED `consent-instrument` (neutral schema + vocabulary; or MODIFIED `memory-gateway` consent-profile family — open); DTN-016 | 1 | Ready to iterate — named 2026-07-24 during the Meds Rx onboarding; first schema'd instance live in LedgerxFactory (`ledgerx_engagement_consent_record`); exit gated on a second domain instantiating (Adx agency agreement or Medx custody-bearing patient consent) |
| [context-compression-runtime](#context-compression-runtime) | ADDED `context-compression-runtime` (worker-lane compression stage + RAM-only local-store rule + upstream-exclusion obligation + three-tier audit model + per-domain egress-capture knob) | 1 | Ready to iterate — design + headroom v0.32.0 source audit locked with Brett 2026-07-25/26 (RAM-only CCR, audit moved to envelope/transcript/egress tiers); exit gated on the codexFactory-lane pilot in Omnigent-Install producing measured savings |
| [dashboard-repo-selector](#dashboard-repo-selector) | MODIFIED `ideation-dashboard` (repo selector, (repository, ref) snapshot source, runtime fetch + baked fallback, refresh affordances, dispatchable publication) + ADDED snapshot-index contract; later ADDED runtime capability (neutral install-shipped ideation surface, DTN path) | 1 | **Proposed 2026-07-26** as `add-dashboard-repo-selector` (exit 1) — twelve decisions locked with Brett 2026-07-25/26 (runtime plane is the goal, planes separate, per-repo snapshots + index, sparse wheels, bake the app not the snapshot, baked snapshot demoted to fallback, two refresh bindings, off-cycle publication is CI-only, (repository, ref) keying, displayed freshness, branch snapshots never published); neutral-vs-override fork + data-source ratification deliberately open; exit 2 (runtime plane) still staged |
| [workbench-branch-sessions](#workbench-branch-sessions) | MODIFIED `ideation-dashboard` (branch-per-tile working state, commit-per-gate-action, session-local snapshots, PR-as-save `open-pr` verb); MODIFIED `lifecycle-notebook-projection` (per-session notebooks sync from the branch worktree; canon notebooks stay main-only) | 1 | **RATIFIED 2026-07-26** as `add-workbench-branch-sessions` (proposed and ratified the same day, after a 5-lens adversarial review and a rename-completeness audit) — TWENTY-TWO decisions (design D1-D22; D22 is the post-ratification `open-pr` push-identity ruling, 2026-07-26) and **ZERO open questions** — the change carries no parked decision; SEQUENCED strictly after `add-dashboard-repo-selector`, whose (repository, ref) seam it consumes; local plane only until intent-plane §4 |
| [codexfactory-domain-hermes-content](#codexfactory-domain-hermes-content) | codexFactory `hermes/domain/` content (changes A + B) + Omnigent overlay extension in lockstep | 1 | **COMPLETE 2026-07-23** — both changes ratified, realized, archived: change A 2026-07-22 (roles + policies + closure + Omnigent lockstep) and change B 2026-07-23 (mixes, councils, escalation, memory, catalog); canonical spec `domain-hermes-content` carries all nine requirements. The Omnigent extension rode the `add-omnigent-domain-overlay` realization. Primary doc + openspec/ drafts retained as provenance. Change B COMPLETE — ratified + archived 2026-07-23 (`archive/2026-07-23-add-domain-hermes-councils-and-memory`) |
| [deployment-handoff-boundary](#deployment-handoff-boundary) | ADDED `deployment-handoff-boundary` (managed-subject routing rule + layered enforcement); MODIFIED `release-realization` (handoff-record correlation); realization in OpsxFactory (QA deployment profile, correlation audit) + codexFactory (release exit step) | 1 | **Ready for proposal** — rule + all 7 clarifying resolutions locked with Brett 2026-07-24 (all-actor scope, creds-primary, grant-issuance gate, correlation stamping, benches on standing request, phased admin strip, codexFactory sole first consumer); residual decisions are proposal-gate/realization detail |
| [github-administration-plane](#github-administration-plane) | MODIFIED `roles-authority-model` (neutral App-identity tiers); new OpsxFactory-owned `github-administration` capability | 1 | COMPLETE 2026-07-15 — both exit changes ratified, realized, archived (2026-07-14-add-github-app-identity-tiers, openxFactory; 2026-07-15-add-github-administration-workflow, OpsxFactory); live rollout done, 2026-07-10 incident closed; primary doc retained as `superseded` provenance |
| [layer-content-materialization](#layer-content-materialization) | ADDED neutral `hermes_domain_overlay` contract + `overlay_path` (openxFactory); hermes-install seeding increment 2 (`layer_content` kernel + materialization) | 1 | **COMPLETE 2026-07-23** — both exits ratified, realized, archived: `add-hermes-domain-overlay-contract` (openxFactory, `contract-v1.15` tag verified) and `add-layer-content-materialization` (hermes-install PR #6 merged 696ec48, archived 2026-07-23; capability spec carries increments 1+2). Deferred increments 3–6 + gate wiring recorded in the capability spec; primary doc retained as provenance |
| [layer-vocabulary-machine-migration](#layer-vocabulary-machine-migration) | MODIFIED `layer-vocabulary` + hermes-runtime v2→next-major identifier migration + domain-stack schema major | 1 | Dormant by design — deferral artifact for `adopt-subject-tenant-domain-vocabulary` tasks 3.1–3.3 (filed 2026-07-23); rides the next major contract bundle, never causes it; Ops/Adx prose sweeps runnable earlier |
| [medxfactory-domain-hermes-content](#medxfactory-domain-hermes-content) | MedxFactory `hermes/domain/` content (changes A + B) + Omnigent `directed_by` lockstep + overlay-manifest digest re-pin | 1 | Ready to iterate — pattern + material verified 2026-07-24; roster composition is the change-A gating decision (needs a decision round with Brett); no external gates (omnigent overlay realization archived at contract-v1.16) |
| [proposal-origin-contract](#proposal-origin-contract) | none yet — retained rationale for a future regulated-traceability profile | 1 | Held as read-only evidence; the origin contract itself was promoted from this topic 2026-07-12 (pointer in `ideation/README.md`'s promoted list) |
| [worker-host-app](#worker-host-app) | ADDED `worker-host-manifest` + `bench-manifest` (first-consumer drafts in Omnigent-Install, DTN path); realization app in Omnigent-Install + Intune packaging in OpsxFactory | 2 | Ready to iterate — build decision by Brett 2026-07-23; realization under way (substrate steps 1–2 merged); 7 open questions (Omni-001 admin path + SYSTEM-context WSL distro registration, runner-under-virtual-account, bench-manifest home hardest) |
| [worker-enrollment-broker](#worker-enrollment-broker) | ADDED `worker-enrollment-broker` (neutral enrollment/lease contract); realization = standalone broker service (home DECIDED: a new Opsx-owned repo, container app on the platform subscription, NOT the QA AKS cluster) + Omnigent-Install (registration-via-broker, lease renewal) + OpsxFactory (App key, policy, temp runner group) | 1 | **Proposed 2026-07-26** as `add-worker-enrollment-broker` (exit 1) — 7 rulings locked with Brett 2026-07-26 (broker-first standalone, two auth modes, lease + fail-closed version floor, fleet hard-pin vs temp self-update, segregated temp group + trust tier) carried as decided context; all 10 open questions carried as design decisions D1–D10, and **all ten ADOPTED AS DECIDED with Brett's approval of the change on 2026-07-26** — D1 (broker home + hosting) no longer blocks the first realization; the contract (phase-1 tasks 1.1–1.10 + 1.12) is REALIZED, shipping six schemas + a canonical validator, the broker service / Omnigent-Install / OpsxFactory realizations are named successor changes, and the heartbeat/readiness projection is left to a coordinated three-places change |
| [subject-establishment](#subject-establishment) | ADDED neutral `subject-establishment` (two artifact kinds: neutral subject design + platform realization; provenance-graded fact set; reference-archetype lifecycle; conformance tiering; apply-and-verify-by-read-back; audit-lift mirror); DTN-017 | 1 | Ready to iterate — named by Brett 2026-07-28 from LedgerxFactory's company-provisioning work (first instantiation, in flight); **Second consumer DECIDED 2026-07-28: codexFactory new-project** (`project` is already a first-class codex subject kind; `check_profile`/`reviewer_group` are neutral-design elements wearing domain names). It surfaced the finding Ledgerx could not: for codex the DESIGNING domain and the APPLYING administrator are different factories (GitHub administration is Opsx's), so the realization artifact must be handoff-shaped — likely the same seam as `deployment-handoff-boundary`. 6 open questions; exit gated on Ledgerx reaching proposal |
| [qualify-avatar-live-voice](#qualify-avatar-live-voice) | ADDED `avatar-live-voice` (incl. the reserved AVC-09/AVC-10 contracts) | 1 | Blocked — 5 open questions (credential custody + spend cap and activation-gate scope hardest); also gated on a released client from the lab |

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

## consent-instrument-contract

- Staging ID: `openxFactory:staging:consent-instrument-contract`
- Repository context: openxFactory (neutral schema + vocabulary); proof
  instruments: LedgerxFactory (first schema'd instance —
  `docs/engagement-letter-template.md` +
  `tenants/ledgerxcorp/clients/medsrx/consent-record.yaml`,
  2026-07-24), MedxFactory (patient consent + memory-gateway
  consent-profile, not yet custody-bearing), Adx/Opsx/codex (implied,
  unmodeled).
- Source: the Meds Rx, Inc onboarding — drafting the
  LedgerXCorp↔MedsRx engagement letter surfaced that the instrument is
  the single record the whole authority chain resolves to (grants cite
  it, gates verify it, adapters activate on it, termination cascades to
  credential revoke+rotate); named by Brett Heap 2026-07-24.
  Registered as DTN-016.
- Claim: every domain's rung-1↔rung-2 relationship starts with a
  consent instrument, and its shape is domain-invariant — parties by
  party-ladder rung incl. third-party ESTATE HOSTS (the Medxcorp
  pattern), scope/out-of-scope, delegation clauses carrying the
  technical access shape, autonomy position, revocation SLA,
  signed-original custody by opaque locator + sha256, status lifecycle.
  It composes with (not competes with) memory-gateway consent-profile,
  document-cataloging, and credential-contracts. Schema it; stop
  treating it as prose.
- Files:
  - [consent-instrument-contract.md](consent-instrument-contract/consent-instrument-contract.md) — primary: per-domain instantiation table, 4 claims, open questions, exit.
- Open questions: delta shape (new capability vs MODIFIED
  memory-gateway — leaning new schema + declared consent-profile
  mapping: instrument authorizes ACTION, profile governs DATA);
  signature/execution modeling depth (distinct-signers SHOULD for
  related-party cases?); amendment lifecycle; broker-side check host
  (credential-contracts validator vs new validate-consent-instruments).
- Exit: `add-consent-instrument` after a second domain instantiates;
  the Ledgerx record declares conformance rather than being rewritten.

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

## deployment-handoff-boundary

- Staging ID: `openxFactory:staging:deployment-handoff-boundary`
- Repository context: openxFactory (neutral routing requirement);
  OpsxFactory (QA deployment profile, subject-registry lookup,
  evidence-correlation audit, ACR namespace scope map); codexFactory
  (release exit step, first consumer); evidence surfaces in
  omnigent-install / hermes-install.
- Source: operator conversation 2026-07-24 (Brett, during worker-host-app
  kickoff); standing evidence = OpsxFactory `workflows/deployment.yaml`,
  the `cir-opensoft-qa-codexfactory-install` QA precedent, and
  `client-infrastructure-request`'s `execution_binding.mode`.
- Claim: deployment execution authority follows management of the target
  surface, not the environment tier — the **managed-subject test**. A
  release headed to any registered OpsxFactory subject (production OR the
  managed QA stack) crosses as a governed `client_infrastructure_request`
  that OpsxFactory executes; work inside the producing factory's own
  execution lane (ephemeral CI/bench containers, no subject) self-serves.
  The rule binds ALL actor classes — workers, human engineers, CI. Tier
  calibrates approval depth and accepted risk, never the executor.
  Enforced in layers: constitutional (Omnigent matrix), credential
  non-possession (the teeth — only opsX identities hold standing keys;
  human access is break-glass), structural GitOps pull-only + Intune,
  detective correlation audit, human approvals.
- Files:
  - [deployment-handoff-boundary.md](deployment-handoff-boundary/deployment-handoff-boundary.md)
    — primary: the rule + test, 6 claims, layered enforcement table,
    7 clarifying resolutions (2026-07-24), residual decisions, exit.
- Open questions: RESOLVED 2026-07-24 (clarifying session) — all-actor
  scope; phased strip of human standing admin (never before tested
  break-glass); grant-issuance + GitOps-merge as the mechanical gates;
  correlation_id stamped into GitOps trailers / k8s annotations / Intune
  metadata; benches on one standing maintenance request per period;
  break-glass = retroactive request, custody per
  client-credential-escrow-registry; codexFactory sole first consumer.
  Residual (proposal gate/realization): capability home, QA approval
  calibration, ACR namespace scope map, preview-environment threshold,
  break-glass window.
- Exit: openxFactory `add-deployment-handoff-boundary` (capability +
  `release-realization` delta), then OpsxFactory + codexFactory
  realization changes; archives on one real release crossing the rail
  end-to-end onto the managed QA stack plus a clean (or dispositioned)
  correlation-audit run.

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
  - [medxfactory-domain-hermes-content.md](medxfactory-domain-hermes-content/medxfactory-domain-hermes-content.md) — primary: 7 claims, exit changes A/B, 6 open questions.
- Open questions (carried): roster composition (change-A gating; candidate
  seven-persona derivation offered as decision input); council placement
  across layers (only MxD-MRR is domain-owned); specialist pods vs mixes;
  practice-catalog seed set; explicit content manifest vs convention;
  client-layer-defaults analog timing.
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
