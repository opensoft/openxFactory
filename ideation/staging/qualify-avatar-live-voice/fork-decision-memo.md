# Staged: Qualify Avatar Live Voice — five-fork PO decision memo

Status: staged
Kind: decision memo
Summary: PO (Brett) decision memo for the five open forks that block the
`qualify-avatar-live-voice` proposal — credential custody + spend cap, latency
budget derivation, activation-gate scope, evaluation-audio consent/data-control,
and canary/rollback semantics. Each fork carries the source constraints, the
options with tradeoffs, a labelled RECOMMENDATION (not a ruling), what the
ruling unblocks/forecloses, and the named gaps that become assumptions Brett
must ratify. The memo decides nothing itself; Brett rules by editing the
"Rulings requested" table or by per-section PR review comments.
Topics: avatar-client, live-voice, decision-memo, credential-custody, spend-cap, latency-slo, activation-gate, consent, data-control, canary-rollback, AVC-09, AVC-10, gpt-realtime-2.1
Repository context: openxFactory (neutral) — this memo is a staging record under the `qualify-avatar-live-voice` topic; it mutates no contract, schema, acceptance map, or interface lock, and is not itself a ratification. The rulings it requests, once made, become the locked decisions the future `qualify-avatar-live-voice` change carries into its proposal.
Staging ID: openxFactory:staging:qualify-avatar-live-voice
Source: the `qualify-avatar-live-voice` staging topic ("Open questions", five forks) and this session's verified per-fork research grounded in the avatar-client contract kernel (archived `2026-07-13-define-avatar-client-contract-kernel`), the F0 brokered-call feasibility evidence (`qualify-avatar-brokered-call-feasibility/evidence/`), the reference-runtime change (`archive/2026-07-13-implement-avatar-reference-runtime`), the credential-access / credential-contracts model, the customer-memory-gateway architecture, the avatar-first-ui standard, and the merge-master autonomous-approval custody precedent landed 2026-07-15 in codexFactory.

This memo is a **decision aid, not a decision**. Every recommendation below is
explicitly labelled a recommendation; nothing here is ratified, and no contract,
schema, acceptance map, or interface lock is touched. The five forks are the
topic's own blocking "Open questions"; the topic cannot become a proposal until
all five are ruled. On all five ruled, the topic's Exit section executes (create
`qualify-avatar-live-voice`, move the staged files into its `supporting-docs/`,
author the spec deltas with these rulings as locked decisions).

## Rulings requested

One row per fork. Recommendations are the researcher's, grounded in the sources
cited per section — they are **not** pre-ratified. Brett rules by writing into
the "Ruling" cell (or by a per-section PR comment).

| # | Fork | Recommendation (one line) | Ruling (Brett) |
| --- | --- | --- | --- |
| 1 | Credential custody + spend cap | **C** — Layered hard-closed: session hard-kill in the broker (reuse the runtime's quota/duration terminal + kill switch + lease revocation), per-tenant/ring hard stop at the F0-proven spend-capped provider project, async Usage Meter for visibility; durable granular per-tenant counter deferred to pilot-hardening | |
| 2 | Latency budget derivation | **C** — Two-tier: a neutral relative-regression SLO is the hard gate (p50+p95, Windows desktop + web at nominal network); per-profile measured numbers recorded in AVC-10 and surfaced in AVC-09 as informational evidence (p99 + teardown recorded, not gated); proposed material threshold >15% relative OR >150 ms absolute (whichever greater) — Brett to ratify the number | |
| 3 | Scope of the eight-condition activation gate | **C** — The kernel's four-element ring is the binding exit contract; the eight GPT-Live-1 conditions are reused as the mapped preflight+canary checklist that produces that evidence, condition 6 reinterpreted to "no material regression vs the direct-provider reference", and all "replace-primary"/default-swap semantics reserved to the later GPT-Live adoption change | |
| 4 | Consent + data-control for evaluation audio | **C** — Synthetic-only model-vs-model evaluation corpus + live-ephemeral consented canary audio (single-model, never retained, never shadowed); consent rides the existing three neutral purposes; retained-real corpus + retention-class unreservation deferred to pilot-hardening | |
| 5 | Canary cohorting + rollback semantics | **B** — Vendor-org + one internal-staffed domain sandbox (synthetic/internally-consented audio only); hybrid rollback under a written policy: safety/integrity breaches auto-revoke active leases, latency/error breaches auto block-new, quality/cost operator-triggered; rollback target is disable-voice → text/handoff (first qualified profile, no model fallback) | |

Note the pattern: forks 1–4 each recommend the "layered / two-tier / mapped"
option (C) — the most fail-closed posture the change can ship without
importing net-new infrastructure the kernel deferred, with the harder version
named as a pilot-hardening follow-on. Fork 5 is the deliberate exception: its
recommendation (B) is NOT the most-contained option — Option A has the
tighter blast radius and builds nothing new — but B is chosen for its
pilot-rehearsal value (it exercises the auto-detection and rollback wiring a
real pilot will need, inside a domain sandbox), trading A's containment for
rehearsal while still refusing C's wider cohort.

---

## Fork 1 — Credential custody + spend cap

**Fork question (verbatim from the topic):** "Credential custody + spend cap.
F0 read a lab key from `OPENAI_API_KEY` in the process environment only, and
never as an artifact. Internal-live needs a real server-side custody model —
where the broker's server key lives (secret store, rotation owner, blast
radius), how ephemeral client secrets are issued and bounded, and an enforced
spend/rate ceiling per session and tenant so a qualification ring cannot run away
on cost. Is the cap a hard broker-enforced ceiling that fails the session
closed, or a monitored budget with alerting?"

### What the sources constrain

- **No repo stores raw credentials; the broker resolves a binding into a
  short-lived scoped grant** — real secrets live only in approved secret
  providers. `docs/credential-access-model.md` §1 (lines 15-26), §4 (lines
  147-155), §13 rules 1-2,6.
- **The promoted credential-contracts shapes the custody model must use**: a
  binding record needs provider / secret_ref / owner / rotation_policy (vault
  optional); a broker contract needs id / resolves / issues / must / must_not.
  `contracts/schemas/xfactory-credential-contracts.schema.yaml` lines 86-107
  (binding_template), 108-132 (broker_contract).
- **F0's key posture**: the lab key was loaded from a mode-600 local file into
  `OPENAI_API_KEY` in the process environment only, never as an
  artifact/arg/result; "Secrets enter only through environment or approved
  secret storage." A dedicated spend-capped OpenAI lab project
  (`openxfactory-realtime-f0-lab`) with project budget + rate controls set
  before any live trial was the account-level cost stop. F0 `design.md` line
  42-43; `f0-live-run-notes-2026-07-12.md` lines 91-99;
  `f0-terminal-pass-report-2026-07-12.md` lines 92-95;
  `sops/openai-realtime-f0-lab-credential.md` (Credential Record table +
  Provisioning req 2).
- **The plaintext key belongs in NO Git repo**; the age-encrypted recovery copy
  lives in the private `xFactory-Agents-Credential-Registry` and is "supervised
  recovery material only... not a deployment source." Owner = openxFactory
  avatar platform maintainers; rotation is create-new / install / verify /
  revoke-old, recording owner+date+reason but never the value.
  `sops/openai-realtime-f0-lab-credential.md` (Credential Record, Encrypted
  Registry Recovery Copy, Rotation and Revocation §1-5).
- **Staging claim 3**: "The client never carries a standard API key; the broker
  holds the server key and ephemeral client secrets stay a non-production lab
  option." `qualify-avatar-live-voice.md` lines 71-72.
- **The session broker is only a deterministic, NON-DEPLOYABLE in-process
  reference today**: explicit non-goals are "A live OpenAI adapter, provider key
  handling, WebRTC, or actual audio" and "nothing deploys, listens on a socket,
  holds a provider key, or processes tenant data." Its grant retry cache is
  process-memory-only and secret material is destroyed on
  connect/expire/abandon/revoke; it holds no durable cross-session state.
  `archive/2026-07-13-implement-avatar-reference-runtime/design.md` Non-Goals
  (lines 27-31), Decision 5 (lines 96-104); `proposal.md` Impact "Operations"
  (line 55-56); `spec.md` "Secret cache is destroyed" scenario (lines 88-90).
- **The reference runtime already models fixture tenant concurrency/duration
  caps, session + model-profile kill switches, and credential-free usage
  records** — a request exceeding a cap emits "the canonical quota or duration
  outcome" (a fail-closed terminal exists for concurrency/duration, **not** for
  durable cumulative spend).
  `archive/2026-07-13-implement-avatar-reference-runtime/spec.md` "Fail-closed
  authority, revocation, usage, and telemetry" + "Usage cap is reached"/"Kill
  switch is active" scenarios (lines 153-179).
- **The reference-runtime change explicitly defers the production deployment
  home, provider SDK, distributed cache, and operational telemetry TO THIS
  FORK's change**: "The production deployment home, network framework, provider
  SDK, distributed cache, and operational telemetry are decided by
  qualify-avatar-live-voice."
  `archive/2026-07-13-implement-avatar-reference-runtime/design.md` Open
  Questions (lines 180-183).
- **House pattern for cost control already exists**: the customer-memory gateway
  runs budget as a SYNCHRONOUS rail that can block the operation
  (`gateway_request` carries `budget.max_billable_units`), while the Usage Meter
  records billable events + budget counters async — "Budget checks that can
  change the operation outcome are sync rails."
  `docs/customer-memory-gateway-architecture.md` Rail Engine + Usage Meter rows
  (lines 121,127), gateway_request budget block (lines 169-171), "budget gate
  when budget can block" (line 905).
- **Fresh custody precedent landed 2026-07-15 in codexFactory**: a GitHub App
  private key custodied under credential-contracts shapes with least-authority
  defaults — vaulted key custody, short-lived workflow-scoped runtime grants,
  per-action audit record; key stored as an Actions secret
  (`MERGE_MASTER_APP_KEY`), App id as a variable; blast radius contained by
  install-scoping to autonomous-surface repos only and rollback-by-uninstall;
  the grant kept as a constrained instance of existing PR-write scope rather
  than a new credential family.
  `xFactories/codexFactory/openspec/changes/add-merge-master-autonomous-approval/design.md`
  Decision 8 (lines 207-215) + `tasks.md` 2.3 (lines 37-41); ratify decision
  keeping it a constrained instance (`tasks.md` 1.2 lines 12-20).

### Options

**A. Hard broker ceiling on both dimensions (fully synchronous fail-closed).**
Server key vaulted under the `xfactory_credential_binding_template` shape
(provider/vault/secret_ref/owner/rotation_policy), broker-only, in a dedicated
internal-live OpenAI project distinct from the F0 lab project; injected in
CI/hosted as a protected secret exactly like merge-master's
`MERGE_MASTER_APP_KEY`. Client never carries any key and no ephemeral client
secret is issued (claim 3 kept off); the broker holds the server key end-to-end
and issues only the short-lived AVC-02 grant, destroyed on
connect/expire/abandon/revoke. The broker enforces a SYNCHRONOUS hard ceiling on
BOTH per-session (duration + billable-unit budget, mirroring gateway
`max_billable_units`) AND per-tenant (durable cumulative spend + concurrency);
any breach fails the session closed via the kernel's existing quota/duration
terminal outcome + idempotent hangup + lease revocation.
*Tradeoffs:* strongest cost containment and cleanest "cannot run away on cost"
story. But per-tenant cumulative-spend enforcement requires a durable
cross-session counter store that does not exist — the reference broker is
deliberately process-memory-only — so this option imports net-new infrastructure
(the "distributed cache/operational telemetry" the reference runtime deferred)
into the qualification change, enlarging scope before internal-live can ship.

**B. Monitored budget with alerting + provider-project cap as the only hard
stop.** Same vaulted broker-only custody as A. But the broker performs NO
runtime kill for spend: cost is bounded only by (1) the F0-proven dedicated
spend-capped OpenAI project (account-level hard exhaustion), (2) the async Usage
Meter recording billable/budget counters, and (3) operator alerting on threshold
breach. Sessions are observed, never killed by the broker for cost.
*Tradeoffs:* cheapest to build and matches the "monitored budget with alerting"
horn verbatim; reuses F0's proven project cap with zero new broker logic. But it
violates the fork's fail-closed intent at the session grain: a single
looping/stuck qualification session can burn the whole ring's project budget
before the account cap trips, with no per-session containment and no per-tenant
sync gate — exactly the runaway the fork exists to prevent. Alerting is
after-the-fact.

**C. Layered hard-closed: session hard in broker, per-tenant hard at the
provider project, monitored counters for visibility.** Same vaulted broker-only
custody and no-ephemeral-client-secret posture as A. The broker hard-fails a
runaway single session synchronously using the reference runtime's
already-modeled duration/quota terminal outcome + kill switch + lease revocation
(no new durable store needed). The dedicated spend-capped internal-live OpenAI
project is the HARD per-tenant/ring backstop that fails ALL sessions closed at
budget exhaustion (F0-proven). The async Usage Meter + alerting supply
per-tenant observability. Durable synchronous per-tenant broker enforcement
(Option A's counter store) is named as an explicit pilot-hardening follow-on,
not built now.
*Tradeoffs:* fails closed at two independent layers (session + provider project)
using only capabilities the runtime already has, so the change can propose
without importing durable-counter infrastructure. Honest about scope. Cost:
per-tenant spend enforcement is coarse (account-level, not per-tenant-granular
in the broker) until the follow-on lands — acceptable while the internal-live
ring's "tenants" are a small internal qualification cohort, weaker once the ring
admits many tenants.

### RECOMMENDATION — **Option C** (Layered hard-closed) *(recommendation, not a ruling)*

The custody half of the fork is nearly determined by existing contracts and
needs only ratification, not invention: the server key MUST be vaulted under the
credential-binding shape (provider/vault/secret_ref/owner/rotation_policy),
broker-resolved, never in a repo (credential-access-model §1, §6); the
merge-master precedent shows the concrete realization today (vaulted key as a
protected CI secret + id as a variable, least-authority, per-action audit, blast
radius contained by scope). Rotation owner = openxFactory avatar platform
maintainers per the SOP; blast radius = a dedicated internal-live OpenAI project
(F0's proven pattern) so a compromise is contained to that project's budget.
Ephemeral client secrets stay OFF for internal-live per claim 3 — the broker
holds the server key end-to-end and issues only the short-lived AVC-02 grant the
reference runtime already destroys on connect/expire/abandon/revoke. All three
options share this baseline; the live fork is the cap. Between the fork's two
named horns, the fail-closed horn is correct: the staging doc's own premise is
"a qualification ring cannot run away on cost," the house pattern (memory
gateway) already makes budget a synchronous blocking rail, and pure monitoring
(Option B) lets one stuck session drain the ring before an account cap or alert
fires. But Option A's fully-synchronous per-tenant ceiling requires a durable
cross-session spend counter that provably does not exist — the reference broker
is deliberately process-memory-only, and the reference-runtime change explicitly
hands the "distributed cache/operational telemetry" decision to THIS change
without providing it. Option C takes the hard-closed ruling while respecting
that reality: it hard-kills the dominant runaway (a single session) with
machinery the runtime already ships (duration/quota terminal outcome, kill
switches, lease revocation), uses the F0-proven spend-capped project as a real
hard per-tenant/ring stop, and adds async metering for visibility — deferring
only the granular durable per-tenant counter to pilot hardening, where the
reference-runtime design already parks distributed state. C is thus the
maximally fail-closed posture that internal-live can actually ship without a
net-new infrastructure dependency.

### Unblocks / forecloses

**Unblocks now:** it lets the AVC-09 descriptor's authorization-mode and
region/data-control fields be authored with a concrete "broker holds server key,
no client key" value; it lets the internal-live activation gate's secret-scan
condition be written against a real vaulted binding rather than a TBD; and it
lets the reference broker's EXISTING quota/duration terminal outcome + kill
switches carry the session-level cost kill, so no durable-counter infrastructure
blocks landing. It keeps the credential surface a constrained instance of the
promoted credential-contracts shapes (no new credential family), mirroring the
ratified merge-master decision. **Forecloses / makes harder:** committing to
broker-holds-key end-to-end means a later pivot to direct client-held ephemeral
OpenAI secrets would reopen the custody model and the AVC-09 authorization-mode;
and because granular synchronous per-tenant spend enforcement is deferred, once
the internal-live ring admits more than a small internal cohort the durable
cross-session counter store becomes prerequisite work (a pilot-hardening
dependency) before hard per-tenant fail-closed exists — the account-project cap
is the only per-tenant hard stop until then.

### Named gaps → assumptions to ratify

1. No source names the concrete secret store/vault for the internal-live server
   key (Azure Key Vault / AWS Secrets Manager / Opensoft-hosted vault). The
   binding shape supports any provider, and merge-master used a CI Actions
   secret, but the internal-live pick is unmade; F0's mode-600 local file + age
   escrow is explicitly "not a deployment source."
2. No durable cross-session per-tenant spend counter store exists or is
   specified anywhere. The reference broker is deliberately process-memory-only;
   hard synchronous per-tenant cumulative-spend enforcement (Option A) has no
   home in any current contract and would be net-new.
3. No numeric values are given anywhere: no per-session
   duration/billable-unit/dollar ceiling, no per-tenant budget, and no
   configured provider-project cap amount. F0 recorded call counts (~183 short
   calls) but no cost figures or the cap value on `openxfactory-realtime-f0-lab`.
4. "Tenant" is undefined for the internal-live ring — the ring's cohorts
   (internal domains? test accounts? MedxFactory/LedgerxFactory qualification
   scenarios?) are not enumerated, so the per-tenant dimension has no defined
   subject to meter or cap (interacts with Fork 5 canary cohorting).
5. Rotation cadence/SLA for the internal-live server key is unspecified. The SOP
   gives a rotate-and-revoke procedure but no interval or trigger, and the
   credential-binding `rotation_policy` value for this key is unset.
6. No alerting channel or threshold is defined (who is paged, at what percentage
   of budget, with what latency). The memory gateway names a Usage Meter but no
   thresholds for this ring; Option B/C's "alerting" has no concrete wiring in
   the sources.
7. It is unspecified whether a broker-enforced session kill for SPEND emits a
   distinct reason code or reuses the kernel's generic "quota or duration"
   terminal outcome — the reference runtime models the latter but not a
   spend-specific code, which matters for auditability of cost-triggered
   terminations.

---

## Fork 2 — Latency budget derivation

**Fork question (verbatim from the topic):** "Latency budget derivation. The
budgets come from a measured baseline — but which percentiles gate (median +
p95, or also p99), across which network and platform matrix, and what magnitude
of regression against the direct-provider reference is 'material' enough to fail
promotion? Does the budget travel per-profile inside the AVC-09 descriptor, or is
there a single neutral SLO the acceptance map enforces?"

### What the sources constrain

- **F0's measured setup intervals (the only real timing distributions
  produced)**: first-playable-after-authorized p50 603.63 ms / p95 643.488 ms /
  max 665.766 ms (count 40); sideband-ready p50 772.37 ms / p95 1642.119 ms /
  max 1663.667 ms (count 30). Candidate baseline inputs, not budgets.
  `qualify-avatar-brokered-call-feasibility/evidence/f0-results.json` lines
  105-124.
- **F0 produced NO per-platform, per-network numbers**: a single Python/aiortc
  harness with region:null, network_type:'webrtc', runtime:'python3.12' — not
  the real Flutter client on Windows/web; its numbers cannot serve directly as
  the client's direct-provider reference baseline. `f0-results.json` lines
  91-104.
- **hangup_to_terminal_ms count is 0** — teardown latency was never captured as
  a distribution; revocation is a pass/fail 5 s bound (client media-stop within
  5 s + accepted revocation within 5 s; provider settle informational ~8.1 s),
  not a budgeted percentile. `f0-results.json` lines 112-117; `spec.md` lines
  57-88; `design.md` line 83.
- **F0's architecture thresholds** (sideband p95 ≤ 3 s,
  first-playable-after-authorization p95 ≤ 2 s, five-second revocation bound)
  are explicitly inputs, not production SLAs; F0 results MUST NOT satisfy
  production latency budgets — live-profile budgets are owned by
  `qualify-avatar-live-voice`. `qualify-avatar-live-voice.md` claim 6 lines
  96-99; `spec.md` "Feasibility does not qualify live use" lines 115-129.
- **Baseline-derivation rule**: instrument each adapter against a
  direct-provider reference; promotion MUST fail when the abstraction adds a
  material regression at MEDIAN OR TAIL latency; numeric budgets set from the
  first measured baseline rather than guessed; the first transport spike
  establishes direct-provider baselines used "as both absolute targets and
  maximum adapter regressions." `flutter-avatar-client-ui-lab.md` lines 313-320
  and 90-92.
- **The kernel deferred the formal AVC-10 latency contract and pilot budgets to
  this change**; a live pilot MUST NOT proceed without approved measured
  budgets; kernel latency evidence was structured logging only.
  `archive/2026-07-13-define-avatar-client-contract-kernel/specs/avatar-client-runtime/spec.md`
  lines 585-604.
- **AVC-10 latency-sample shape (reserved)** carries sample/session/media-leg/turn
  identity, adapter/profile, platform, network, region, clock source/quality,
  monotonic markers, derived intervals, direct-or-brokered reference
  classification, and a reproducible fixture reference; markers cover broker
  request, provider call, sideband ready, media connected, speech, first audio,
  playback, interruption, command, tool outcome, recovery, teardown; no raw
  content or secrets. `archive/.../supporting-docs/avatar-client-neutral-contracts.md`
  lines 243-250.
- **AVC-09 descriptor (reserved)** records adapter/version, provider,
  supported/requested/resolved profiles, config versions, authorization mode,
  sideband readiness, direct-media requirement, region/data controls, and
  experimental/candidate/approved/retired status — it carries STATUS, not
  numeric latency-budget fields.
  `archive/.../supporting-docs/avatar-client-neutral-contracts.md` lines 231-241.
- **The acceptance map is the enforcement locus**: every normative
  requirement/scenario has a stable map entry naming owning task, evidence ID,
  release ring, and status; `scripts/validate-avatar-client.py` compares the map
  to the delta specs and fails on unmapped/missing evidence; internal-live
  requires "measured latency evidence." `archive/.../specs/avatar-client-runtime/spec.md`
  lines 606-624.
- **Activation-gate condition 6**: "Latency and conversational-flow results meet
  or improve on the gpt-realtime-2.1 baseline." Lab platform set is Windows
  desktop and web (first Flutter targets). `flutter-avatar-client-ui-lab.md`
  lines 394-395 and 68, 593.

### Options

**A. Neutral relative-regression SLO only** (acceptance-map gate, p50+p95, no
per-profile budget in AVC-09). One neutral SLO lives in the acceptance map /
spec delta: the governed adapter's p50 and p95 for the gated setup intervals
(first-playable-after-authorized and sideband-ready) must not exceed the
SAME-PLATFORM direct-provider reference by more than a material threshold.
Percentiles gated: median + p95 only (p99 recorded but not gated — F0 yielded
only 30-40 samples). Matrix: Windows desktop + web canvas at nominal broadband;
Linux CI is reference-generation only, never a gated delivery platform. AVC-09
carries only a pointer to the neutral SLO and the pass/fail evidence reference.
AVC-10 samples carry the raw markers for both reference and adapter runs.
*Tradeoffs:* cleanest fit to the reserved AVC-09 shape (no budget field) and to
the acceptance-map/validator model; robust to provider drift because the gate is
relative. Weakness: discards ui-lab's explicit intent (line 92) that baselines
act as ABSOLUTE targets too, and stores no durable per-profile number, so
cross-release trend analysis lives only in loose AVC-10 samples.

**B. Strict per-profile absolute budgets baked into AVC-09** (p50+p95+p99, full
platform+network matrix). Unreserve AVC-09 with an added numeric latency-budget
block: absolute p50/p95/p99 ceilings per gated interval, per profile, plus a
relative regression cap. Gate on median, p95, AND p99. Matrix expands to Windows
desktop + web canvas crossed with a network condition set (nominal + one
degraded/jitter profile). Promotion fails on any percentile breach on any cell
or the relative cap. Budgets travel inside the descriptor, pinned by the same
commit/SHA discipline as the rest of the kernel.
*Tradeoffs:* maximally honors ui-lab's "absolute targets AND maximum adapter
regressions" (line 92) and gives the strongest, most auditable gate. But it adds
a field the reserved AVC-09 shape does not have (neutral-contracts 231-238),
freezes provider-specific numbers into a neutral contract (brittle to point
releases), and gates p99 + a degraded-network matrix that F0's 30-40-sample
single-environment run cannot yet substantiate — the evidence to set those
ceilings does not exist, front-loading a large measurement program before the
ring can open.

**C. Two-tier: neutral relative-regression SLO is the hard gate (p50+p95);
per-profile measured numbers recorded in AVC-10 and surfaced in AVC-09 as
informational evidence (p99 + teardown recorded, not gated).** The HARD gate is
the neutral relative rule in the acceptance map (as in A): adapter p50 and p95 on
the gated setup intervals within a material threshold of the same-platform
direct-provider reference, on Windows desktop + web canvas at nominal network,
Linux CI reference-generation only. Additionally, the specific measured baseline
and adapter values for gpt-realtime-2.1 are persisted per-profile — carried as
AVC-10 samples and summarized in the AVC-09 descriptor's status/evidence section
(NOT as a gating budget field). p99 and teardown/hangup latency are RECORDED as
informational tail evidence for trend-watching but do not gate internal-live;
they are candidates to become hard gates at the pilot ring when sample sizes
support them. Material regression proposed as: adapter percentile exceeds the
reference percentile by more than **15% relative OR 150 ms absolute, whichever is
greater**, on first-playable-after-authorized and sideband-ready.
*Tradeoffs:* best matches the staged-ring model (internal-live is lighter than
pilot per kernel spec 606-618) and the reserved-contract shapes: the gate is a
neutral rule the validator can enforce, while the per-profile numbers live where
the reserved AVC-09/AVC-10 shapes already put them (status/evidence + samples),
no new gating field forced into AVC-09. Honors "absolute targets" as RECORDED
reference values without freezing them as immutable contract thresholds. Cost:
two artifacts to keep coherent (the neutral rule and the recorded numbers), and
the 15%/150 ms number is a proposal Brett must ratify — no source sets it.

### RECOMMENDATION — **Option C** (Two-tier) *(recommendation, not a ruling)*

Three source facts converge on C. (1) The gate the sources actually specify is
relative, not absolute: ui-lab 313-320 says promotion "must fail when the
abstraction adds a material regression at median or tail" against a
direct-provider reference — a comparison, enforced at median and tail. (2) The
reserved contract shapes already tell you where numbers go: AVC-09
(neutral-contracts 231-238) carries STATUS, not budget fields, while AVC-10
(243-250) is purpose-built to carry the raw markers, derived intervals, and
direct-vs-brokered reference classification per sample — so recording per-profile
numbers in AVC-10 and gating on a neutral rule in the acceptance map (the
enforcement locus per kernel spec 620-624) requires zero new contract surface,
whereas Option B must invent an AVC-09 budget field. (3) The evidence base cannot
yet support B's strictness: F0 produced only 30-40 samples from a single
Python/aiortc harness with region:null (f0-results.json 91-124), so a gated p99
and a degraded-network matrix have no measured foundation, and F0's numbers are
explicitly inputs-not-SLAs (staging claim 6). Gating p50+p95 on the two shipping
platforms at nominal network is the defensible envelope for an internal-live
ring, which the kernel deliberately makes lighter than pilot (spec 606-618).
Recording p99 and teardown as informational keeps the door open to promote them
to hard gates at the pilot ring once sample volume supports them — matching the
staged-evidence model. C is A's robustness plus a durable per-profile record of
the "absolute targets" ui-lab line 92 names — RECORDED as reference evidence in
AVC-09/AVC-10, not enforced as a gating budget — without B's brittleness of
freezing provider-specific ceilings into a neutral contract.

### Unblocks / forecloses

**Unblocks:** authoring the AVC-09/AVC-10 spec deltas immediately using the
reserved shapes as-is (no new AVC-09 budget field to design); a
validate-avatar-client.py rule that checks one neutral relative-SLO entry in the
acceptance map rather than per-profile numeric ceilings; and a small
internal-live measurement program (two platforms, nominal network, p50/p95) that
the client can actually produce before opening the ring. It keeps
p99/degraded-network/teardown budgets as a clean, evidence-gated promotion path
into the pilot ring. **Forecloses / makes harder:** hard absolute SLAs that ops
or a customer contract might later want (C's gate is relative, so a
slowly-regressing provider reference is not caught — that safety net must be
added separately if needed); pinning provider-specific latency ceilings under
the kernel's commit/SHA discipline (numbers live in mutable evidence, not the
frozen contract); and any claim that internal-live latency was validated under
adverse network conditions — it was not, and pilot must redo it. Choosing C now
also commits the team to re-measuring a real client-side direct-provider
baseline (F0's harness numbers do not qualify), which this change must budget for
regardless.

### Named gaps → assumptions to ratify

1. No client-side direct-provider baseline exists yet. F0's numbers
   (first-playable p50 603/p95 643 ms; sideband p50 772/p95 1642 ms) come from a
   single Python/aiortc harness with region:null (f0-results.json 91-124), NOT
   the real Flutter client on Windows/web. This change must MEASURE a fresh
   same-platform direct-provider reference before any regression gate can run;
   the F0 metrics are inputs/sanity-checks, not the baseline.
2. The material-regression magnitude (proposed: >15% relative OR >150 ms
   absolute, whichever greater, on first-playable-after-authorized and
   sideband-ready) has NO source. It is a reasoned proposal — the abstraction's
   overhead is setup-time (broker+sideband), not per-frame (claim 3 keeps
   continuous media direct), so a ceiling on setup-interval percentiles is the
   right shape — but the specific numbers require Brett's ratification.
3. No source defines the network matrix for internal-live. ui-lab names the
   platform targets (Windows desktop + web) but says nothing about network
   conditions; C assumes nominal broadband only, deferring degraded/jitter to
   pilot. Brett must confirm nominal-only is acceptable for the internal-live
   ring.
4. Minimum sample count / trial volume for statistically valid internal-live
   latency evidence is unspecified. F0 used 30-40 samples; nothing defines how
   many turns/sessions per platform cell the internal-live latency evidence
   needs, which directly bounds whether even p95 (let alone p99) is trustworthy.
5. Steady-state conversational turn latency (speech → first audio) was never
   measured. F0 metrics cover only first-playable-after-authorized and
   sideband-ready (setup intervals); the AVC-10 markers for speech/first-audio/
   playback exist but have no F0 distribution. Whether the gate covers per-turn
   conversational latency (ui-lab condition 6 says "conversational-flow results")
   or only setup intervals is undecided — C gates setup intervals; per-turn
   latency is a named gap needing its own baseline.
6. Teardown/termination latency has no budget basis: hangup_to_terminal_ms count
   is 0 in F0 and revocation is a pass/fail 5 s bound, not a distribution. C
   records teardown as informational; whether internal-live needs a teardown
   latency budget at all is unresolved.
7. Unreserving AVC-09 under Option B would require ADDING a numeric
   latency-budget field the reserved shape (neutral-contracts 231-238) does not
   currently have. If Brett prefers B, that schema addition and its validator
   support are net-new work not yet scoped; C avoids it but the choice is a
   genuine open decision.

---

## Fork 3 — Scope of the eight-condition activation gate

**Fork question (verbatim from the topic):** "Scope of the eight-condition
activation gate. The gate as written targets promoting **GPT-Live-1** over the
current primary. This change instead promotes `gpt-realtime-2.1` from disabled to
internal-live-qualified. Fork: do all eight conditions bind the internal-live
qualification of the current candidate, or is internal-live a lighter ring with
the full eight-condition gate reserved for the GPT-Live-1 default swap? Which
conditions are hard preflight blockers versus canary-time checks?"

### What the sources constrain

- **The eight-condition list is titled the "GPT-Live-1 Activation Gate" and
  framed as the DEFAULT SWAP**: "GPT-Live-1 should replace the current primary
  profile only after all of these conditions are met" — (1) OpenAI publishes an
  API model ID and supported API contract; (2) required
  account/regional/retention/data-control terms approved; (3) adapter proves
  direct low-latency Flutter transport without a media proxy; (4)
  transcript/interruption/tool/sideband/reconnect capabilities pass contract
  tests; (5) deterministic UI scenarios and domain voice evaluations pass; (6)
  latency and conversational-flow results meet or improve on the gpt-realtime-2.1
  baseline; (7) safety/exact-value/consent/handoff/blocked-state evaluations pass
  for generic, MedxFactory, and LedgerxFactory; (8) an opt-in canary on new
  sessions succeeds with rollback via a server-side profile change.
  `archive/2026-07-13-define-avatar-client-contract-kernel/supporting-docs/flutter-avatar-client-ui-lab.md:382-399`.
- **The internal-live ring is the kernel's FOUR-element ring, NOT the eight**:
  release rings SHALL be "deterministic lab ..., internal live (live provider
  qualification plus secret scan, telemetry redaction verification, kill-switch
  proof, and measured latency evidence), and pilot (threat-model closure,
  data-handling review, accessibility evidence, and rollback rehearsal)." A later
  ring requires the prior ring's evidence.
  `archive/.../specs/avatar-client-runtime/spec.md:606-618`.
- **gpt-realtime-2.1 is the F0 candidate but MUST stay disabled** for
  internal-live/production until qualify-avatar-live-voice records approved
  promotion evidence; **gpt-live-1 SHALL remain disabled pending its OWN
  qualification** — two models qualified by two distinct acts.
  `archive/.../specs/avatar-client-runtime/spec.md:430-434`.
- **GPT-Live adoption is a SEPARATELY approved change**, distinct from
  qualify-avatar-live-voice which "performs internal-live provider
  qualification." `archive/.../supporting-docs/avatar-client-parallel-workstream-plan.md:89,93`.
- **The expert panel deliberately collapsed five rings to three** (deterministic
  lab, internal live, pilot) and kept the invariant-guarding checks (secret
  scan, redaction verification, kill-switch proof) as CI duties, moving
  SBOM/chaos/formal-audit evidence to the pilot gate only — an explicit ruling
  AGAINST over-gating the zero-user internal ring.
  `archive/.../supporting-docs/expert-panel-review-2026-07-10.md:174-180`.
- **The staging topic scopes this as "provider qualification for the
  internal-live release ring only — not a pilot, and not the GPT-Live-1 default
  swap,"** and Claim 7 says the gate "reuses the eight-condition GPT-Live-1
  structure" (reuse of structure), flagging the binding question as this very
  fork. `qualify-avatar-live-voice.md:43-44,101-112`.
- **F0 delivered Overall: PASS, including F0-C-NO_MEDIA PASS** (direct media, no
  proxy proven) — so condition 1 (published API/contract) and condition 3's
  topology (no-proxy direct transport) are already substantiated for
  gpt-realtime-2.1 before this gate opens.
  `qualify-avatar-brokered-call-feasibility/evidence/f0-results.md:5,22`.
- **Repo-locus binds only conditionally**: "Release evidence obligations SHALL
  activate at the internal-live gate, not at repository creation"; before that
  gate the client MAY consume contracts by co-checkout path reference; when the
  successor change creates xfactory-avatar-client it MUST be private,
  independently releasable, hold no provider keys/server tool handlers; adding it
  to the aggregation requires a SEPARATE reviewed change.
  `archive/.../specs/repo-boundary-governance/spec.md:22-24,30-43,57-59`.
- **The 002 lab record binds the CURRENT home and defers the move**:
  "codexFactory apps/avatar-client-lab/ is the ratified home (the standalone-repo
  wording activates at the internal-live gate, not now)" — but names no change as
  the extractor. The staging doc assumes extraction is in this change's scope
  (code_surface openxFactory, xfactory-avatar-client).
  `specs/002-avatar-client-lab/flutterbench-handoff.md:136-138`;
  `qualify-avatar-live-voice.md:11,167`.

### Options

**A. Four-element ring only; eight reserved wholesale for the default swap.**
Bind internal-live to exactly the kernel's four evidence elements (secret scan,
telemetry redaction verification, kill-switch proof, measured latency evidence)
around live provider qualification; treat the entire eight-condition list as the
property of the separate "GPT-Live adoption" change and do not import it here.
*Tradeoffs:* cleanest fidelity to the literal kernel ring text (spec.md:606-618)
and the panel's anti-over-gating ruling. But "live provider qualification" is
left undefined in substance, so contract-test coverage (cond 4), cross-domain
safety evals (cond 7), and canary/rollback (cond 8) are not explicitly required
at the first-ever real-voice gate — a real under-testing risk for the
highest-consequence transition, and it contradicts Claim 7's intent to reuse the
eight-condition structure.

**B. All eight bind internal-live, as written.** Adopt the eight-condition
GPT-Live-1 gate verbatim as the internal-live bar for gpt-realtime-2.1, requiring
every clause literally before the ring opens.
*Tradeoffs:* maximal assurance, zero authoring ambiguity. But condition 6 ("meet
or improve on the gpt-realtime-2.1 baseline") is circular when gpt-realtime-2.1
IS the candidate, and condition 1 is trivially already met (F0 pinned it) — so
applying the list literally forces contortions. It over-gates a zero-user
internal ring the expert panel explicitly trimmed (review:174-180) and blurs the
staging boundary that this is "not the GPT-Live-1 default swap."

**C. Four-element ring is the binding exit contract; the eight are reused as the
mapped preflight+canary checklist, with condition 6 reinterpreted and the
"replace-primary" semantics reserved.** Make the kernel's four elements the
enforced acceptance-map contract for the ring. Reuse conditions 1-5,7,8 as the
substantive preflight/canary checks that PRODUCE that evidence; reinterpret
condition 6 from "beat the incumbent" to "no material regression vs the
direct-provider reference" (handing the numbers to Fork 2); and explicitly carve
every "replace the current primary profile" semantic to the later GPT-Live
adoption change. Ship the per-condition preflight/canary/default-swap
classification alongside.
*Tradeoffs:* honors both the literal kernel ring AND Claim 7's "reuses the
eight-condition structure," matches the "internal-live only, not the default
swap" boundary, and keeps a meaningful latency-parity bar. Cost: it is an
authoring construction (the eight-as-internal-live mapping is not an inherited
contract), so Brett must ratify the mapping and the reinterpretation of condition
6 rather than inheriting it.

**D. Adopt all eight but phase-bucket them, marking the comparative/default-only
clauses N/A for this candidate.** Keep the eight-condition list as the checklist
but formally bucket each into hard-preflight / canary-time / default-swap-only,
and mark inapplicable conditions (comparative baseline in cond 6; the
GPT-Live-1-specific reading of cond 1) as "N/A for this candidate," letting
latency be governed only by the four-element ring's raw "measured latency
evidence" with no parity bar at internal-live.
*Tradeoffs:* distinct from C in that it drops the latency-parity/regression gate
at internal-live (no bar until pilot), reducing over-gating but weakening Claim
6's "material regression fails promotion." Simpler to author than C, but leaves
the first live transport without a pass/fail latency criterion — pushing all
latency judgment into Fork 2 with nothing binding it at this ring.

### RECOMMENDATION — **Option C** (four-element ring binding; eight reused as mapped checklist) *(recommendation, not a ruling)*

The sources are decisive on the core fork: internal-live is the kernel's
FOUR-element ring, not the eight. The eight-condition list is literally titled
and framed as GPT-Live-1 replacing "the current primary profile"
(ui-lab:382-399), gpt-live-1 is disabled "pending ... its own qualification"
(spec.md:434), and "GPT-Live adoption" is a separately approved change
(workstream:93). So the eight do NOT inherit onto gpt-realtime-2.1 as a matter
of contract. But Option A under-tests the highest-risk transition and ignores
Claim 7's explicit intent to reuse the structure; Option B is mechanically broken
(cond 6 circular, cond 1 trivially met) and defies the panel's anti-over-gating
ruling; Option D abandons a latency pass/fail bar at the ring. C is the only
option that satisfies all three sources at once — the literal four-element ring
as the enforced acceptance-map contract, the eight-condition substance reused as
the checklist that generates that evidence, and the comparative/promotion
semantics explicitly reserved to the later default-swap change.

**Per-condition classification for the internal-live qualification of
gpt-realtime-2.1:**

1. published API/contract = **HARD-PREFLIGHT**, already satisfied for this
   candidate (F0 pinned it); gating-unknown only for GPT-Live-1 so effectively
   default-swap-only there.
2. account/regional/retention/data-control terms approved = **HARD-PREFLIGHT**
   blocker (couples Fork 1 custody + Fork 4 data-control).
3. direct low-latency no-proxy transport = topology is **HARD-PREFLIGHT**
   (F0-C-NO_MEDIA PASS); the latency figure is CANARY/measurement-time.
4. transcript/interruption/tool/sideband/reconnect contract tests =
   **HARD-PREFLIGHT** (deterministic AVC contract tests).
5. deterministic UI + domain voice evals = deterministic half is a PREFLIGHT
   precondition already landed via the kernel's deterministic-first gate; the
   live domain-voice eval is **CANARY-time**.
6. latency meet/improve on the gpt-realtime-2.1 baseline = **DEFAULT-SWAP-ONLY**
   as written (comparative vs an incumbent); its internal-live analogue is
   CANARY/measurement-time "no material regression vs the direct-provider
   reference" owned by Fork 2.
7. safety/exact-value/consent/handoff/blocked-state across generic/Medx/Ledger =
   blocked-state/exact-value deterministic parts PREFLIGHT; live cross-domain
   safety/consent evals **CANARY-time** (couples Fork 4).
8. opt-in canary + server-side rollback = **CANARY-time** by definition (Fork 5),
   while the two kill switches and rollback machinery are HARD-PREFLIGHT (they
   must exist before any canary traffic, per spec.md:626-629).

### Unblocks / forecloses

**Unblocks:** authoring the internal-live activation gate as a concrete
acceptance-map contract (four kernel elements) that validate-avatar-client.py can
enforce, while giving the AVC-09/AVC-10 spec deltas a defensible
preflight-vs-canary split; it cleanly hands the latency numbers to Fork 2, the
eval-audio consent question to Fork 4, and the canary/rollback mechanics to Fork
5 without double-binding them. It keeps the GPT-Live-1 default swap as a distinct
future change with its own (literal, comparative) eight-condition gate, so
gpt-realtime-2.1 qualifying internal-live does NOT commit anyone to promoting it
to production default. **Forecloses / makes harder:** treating internal-live
qualification as automatic promotion to the primary profile (that stays a
separate ruling), and it means the eight-as-internal-live mapping and the
condition-6 reinterpretation become ratified assumptions Brett owns rather than
inherited contract — if a later reviewer wants the literal eight, they must
reopen this. It also leaves the repo-extraction timing unresolved (see gaps), so
committing this change's code_surface to include xfactory-avatar-client would
silently also commit to performing the standalone-repo extraction inside this
change.

### Named gaps → assumptions to ratify

1. No document enumerates a distinct internal-live "activation gate" as an
   eight-item (or any-item) list beyond the kernel's four-element ring; the
   eight-condition list exists ONLY as the GPT-Live-1 default-swap gate. Mapping
   it onto internal-live is an authoring construction Brett must ratify, not an
   inherited contract.
2. The sources bind that xfactory-avatar-client MUST exist as a private,
   independently-releasable, key-free repo BY the internal-live gate
   (repo-boundary-governance:22-24,30-43) and that the standalone-repo wording
   "activates at the internal-live gate" (002 handoff:136-138) — but NO source
   names which change performs the extraction from codexFactory
   apps/avatar-client-lab. The staging doc assumes it is in-scope for
   qualify-avatar-live-voice (code_surface includes xfactory-avatar-client);
   whether extraction is this change's job or a predecessor change's is Brett's
   to choose. Aggregation-repo wiring is separately and explicitly deferred to
   another reviewed change (repo-boundary-governance:57-59). *(This is the
   latent repo-locus decision surfaced below.)*
3. The numeric "material regression" threshold and percentile set that would make
   condition-6/measured-latency pass or fail are not specified anywhere — that is
   Fork 2 and remains unresolved here.
4. Whether the live domain-voice and cross-domain safety evaluations (conditions
   5,7) may run against real consented audio or must stay synthetic-only at
   internal-live is unspecified — that is Fork 4.
5. The sources say internal-live qualification records "approved promotion
   evidence" and that rollback "selects the last qualified profile"
   (spec.md:430-436), implying qualification yields a selectable profile — but
   they do NOT state whether internal-live qualification of gpt-realtime-2.1 also
   makes it the production DEFAULT primary or leaves it internal-ring-only.
   Staging says internal-live-only; the exact production-default status is an
   unstated assumption.

---

## Fork 4 — Consent + data-control for evaluation audio

**Fork question (verbatim from the topic):** "Data-control and consent for
evaluation audio. The gate forbids shadowing live customer audio to two models
without explicit consent and an approved data purpose, and prefers synthetic and
consented recordings first. Fork: what is the consent + data-purpose contract for
qualification-time evaluation audio (retention window, region, opt-in surface),
how does it sit against the kernel's reserved-forbidden transcription-retention
class, and may any real consented audio be used at all — or does qualification
stay synthetic-only like F0?"

### What the sources constrain

- **Four retention classes are RESERVED and FORBIDDEN in the current kernel** —
  full_transcript, audio, video, independent_transcription — each marked
  "FORBIDDEN in this kernel; successor change only." The active enum is exactly
  three: ephemeral_presentation, operational_telemetry, structured_record.
  `contracts/avatar-client/registries/retention-classes.registry.yaml:9-17`.
- **AVC-07 schema pins the forbidden set in-contract**: "Full transcript, audio,
  video, and independent transcription are RESERVED and forbidden in this kernel
  (spec FR-017; ACR-010-S02). Schema + fixtures only — no live retention
  instances (Q2)." It also forces local_persistence const false.
  `contracts/avatar-client/avc-07-retention-profile.schema.yaml:8-10,21`.
- **The interface-lock freezes reserved_retention_classes**: forbidden as a
  closed default; this change unreserves only AVC-09/AVC-10, not any retention
  class (reserved_identifiers: [AVC-03, AVC-05, AVC-09, AVC-10]).
  `contracts/avatar-client/interface-lock.yaml:10,32`.
- **The kernel exposes exactly three neutral consent purposes (frozen count 3)** —
  avatar.media_capture, avatar.provider_processing, avatar.structured_record —
  and "AVC carries only the consent record reference, version, and required
  purpose ids; domains own evidence/legal-basis/withdrawal."
  `contracts/avatar-client/registries/consent-purposes.registry.yaml:5-12`;
  `interface-lock.yaml:14`.
- **A session's consent_ref carries only a consent_record_ref, consent_version,
  and required_purpose_ids** drawn from the three-value enum — "references only;
  evidence stays in the owning authority."
  `contracts/avatar-client/shared-definitions.schema.yaml:36-54`.
- **The presentation profile maps behaviors to a neutral purpose_ref plus an
  OPTIONAL stricter domain_purpose_ref**; the retention_overlay carries only
  externally-owned policy_refs with "no inline durations/policy/consent
  evidence." `contracts/schemas/avatar-first-ui-profile.schema.yaml:348-364,381-389`.
- **Session-outcome "revoked" = "Lease/consent revoked"**; media_authorization_state
  includes a terminal "revoked"; the UI standard requires consent withdrawal
  stays reachable during the session.
  `contracts/avatar-client/registries/session-outcomes.registry.yaml:13`;
  `shared-definitions.schema.yaml:83`; `docs/avatar-first-ui-standard.md:500`.
- **F0 is synthetic-only by construction**: "generated audio only, tools
  disabled, no tenant data"; "no tenant data; no deployment or standing service"
  — and F0 PASS "is not provider qualification and never enables production or
  live media — that boundary is owned by qualify-avatar-live-voice."
  `qualify-avatar-brokered-call-feasibility/evidence/f0-terminal-pass-report-2026-07-12.md:94,108-110`;
  `proposal.md:55`.
- **Staging claim 8 sets the gate prohibition**: "no live customer audio is
  shadowed to two models without explicit consent and an approved data purpose."
  The prohibition is scoped to two-model shadowing, not to single-model live
  processing. `qualify-avatar-live-voice.md:118-119`.
- **AVC-09 (unreserved by THIS change) is where "region/data controls" live** at
  the adapter-descriptor level — consent/kernel schemas carry no region field.
  `qualify-avatar-live-voice.md:88`.
- **Hermes owns consent in the workspace layer model**; a domain declares
  purposes that resolve to existing consent flags without adding enforcement —
  MedxFactory added consent_purposes (media_capture, provider_processing,
  structured_record) each "governed_by" an existing flag, "NO new enforcement
  rule ... NO default." `/workspace/projects/xFactory/CLAUDE.md` (layer model
  line); `xFactories/MedxFactory/hermes/patient/consent-model.yaml:16-32`;
  `docs/xfactory-domain-factory-model.md:644`.

### Options

**A — Fully synthetic-only internal-live (F0 mirror), all consented-real audio
deferred to pilot-hardening.** Internal-live uses only generated/scripted audio
with no tenant data, exactly like F0. The safety/exact-value/consent/handoff
evaluation corpus is synthetic; even the opt-in canary runs on internal staff
exercising scripted content, not spontaneous real utterances. No
consent-purpose or retention change is authored; the reserved-forbidden classes
are untouched. Any real consented audio is deferred to a later pilot-hardening
change.
*Tradeoffs:* maximally safe and fastest to author (zero consent/retention
contract work; strict F0 parity). But it hollows out Fork 5's "opt-in canary on
new sessions" — a canary with no real user audio proves little about real-world
latency, VAD, and safety behavior, so the internal-live ring's value drops and
the same evaluation risk merely reappears at pilot with no groundwork laid.

**B — Admit retained consented-real recordings for evaluation at internal-live.**
Author a real evaluation corpus of consented recorded human audio at
internal-live. This requires unreserving the `audio` and/or
`independent_transcription` retention classes in THIS change, adding a new
evaluation consent purpose (breaking the frozen count of 3), and defining a
region + retention-window + opt-in contract plus a Hermes consent record and
withdrawal path so recordings can be stored and replayed against candidates.
*Tradeoffs:* richest, most realistic evaluation and reusable regression corpus.
But it directly contradicts the kernel: retention classes are "FORBIDDEN in this
kernel; successor change only" and AVC-07 is "schema + fixtures only — no live
retention instances (Q2)"; it breaks the frozen consent-purpose count; and it
drags a full retention/region/withdrawal regime into a change scoped to unreserve
only AVC-09/AVC-10. Largest blast radius, highest consent/privacy risk, and
mis-scoped.

**C — Synthetic evaluation corpus + live-ephemeral consented canary audio, no
retention and no shadowing; retained-real deferred to pilot-hardening.** The
model-vs-model evaluation corpus (the eighth gate condition's
safety/exact-value/consent scenarios) stays synthetic-only. Separately, the
opt-in canary MAY put real consented users on the single candidate, where their
audio is processed live and strictly ephemeral — captions/deltas fall under
ephemeral_presentation, decisions/consent-versions/outcomes under
structured_record, and no `audio`/`full_transcript`/`independent_transcription`
instance is ever created and nothing is shadowed to a second model. Consent rides
the existing three neutral purposes (media_capture, provider_processing) plus an
optional domain_purpose_ref; withdrawal maps to the existing "revoked" outcome.
Region/data-control is declared in the AVC-09 descriptor. Retained real
recordings and any two-model shadowing are deferred to pilot-hardening (which
would carry the retention-class unreservation).
*Tradeoffs:* keeps the reserved-forbidden classes untouched and the
consent-purpose count frozen while still letting the canary observe real
behavior — it threads staging claim 8 (which forbids only two-model shadowing,
not single-model live processing). Costs: it relies on operational discipline to
guarantee "ephemeral, single-model, never retained" (no schema field enforces
non-shadowing today), and it leaves retention-window and opt-in-surface specifics
to be pinned as ratified assumptions.

### RECOMMENDATION — **Option C** (synthetic eval corpus + live-ephemeral consented canary) *(recommendation, not a ruling)*

C is the only option that satisfies every hard source constraint at once while
still letting the internal-live ring do useful work. The kernel is unambiguous
that audio/full_transcript/independent_transcription retention is forbidden until
a successor change (retention-classes.registry.yaml:13-17; AVC-07:8-10), and this
change unreserves only AVC-09/AVC-10 (interface-lock.yaml:10) — so B is out of
scope and would break the frozen consent-purpose count of 3
(interface-lock.yaml:14). A is safe but self-defeating: Fork 5 calls for an
"opt-in canary on new sessions," and a canary that never hears a real utterance
cannot exercise real VAD, latency-tail, or safety behavior, so it merely
relocates the evaluation risk to pilot with nothing built. C respects the letter
of the prohibition — staging claim 8 forbids specifically shadowing "live
customer audio to two models" (qualify-avatar-live-voice.md:118-119), and C never
shadows and never retains audio: real canary audio stays inside the three active
classes (ephemeral_presentation captions, structured_record decisions), consent
rides the existing three neutral purposes with an optional domain_purpose_ref
(avatar-first-ui-profile.schema.yaml:348-364), and withdrawal maps onto the
already-defined "revoked" outcome (session-outcomes.registry.yaml:13). It keeps
the synthetic evaluation corpus posture inherited from F0 ("generated audio only
... no tenant data", f0-terminal-pass-report:94) for the model-vs-model
comparison where the shadowing hazard actually lives, and cleanly hands the
retained-real corpus — which genuinely needs a retention-class unreservation — to
the pilot-hardening successor the kernel already anticipates ("successor change
only").

### Unblocks / forecloses

**Unblocks:** a real opt-in internal-live canary that observes genuine user
behavior without any kernel retention change; authoring the AVC-09 descriptor's
region/data-control fields as the single home for evaluation-audio locality
(qualify-avatar-live-voice.md:88); and reusing the existing three consent
purposes plus domain_purpose_ref so domains (e.g. MedxFactory's
consent-model.yaml) declare evaluation intent without new enforcement. It keeps
consent ownership with Hermes and evidence/withdrawal with domains
(consent-purposes.registry.yaml:5-8). **Forecloses / defers:** any retained
real-audio regression corpus, any two-model shadow evaluation, and any
independent_transcription — all now require the pilot-hardening successor that
carries the retention-class unreservation, a new evaluation consent purpose
(relaxing the frozen count of 3), and a full retention-window/region/withdrawal
regime. It also commits the program to enforcing "ephemeral, single-model,
never-retained" operationally, since no current schema field blocks a
second-model shadow — a control gap that pilot-hardening should close with an
explicit contract flag.

### Named gaps → assumptions to ratify

1. Retention WINDOW for any evaluation/canary-derived structured_record is
   undefined in the sources: AVC-07 carries only retention_class +
   local_persistence:false with no duration field, and retention_overlay exposes
   only externally-owned policy_refs "with no inline durations"
   (avc-07:18-23; avatar-first-ui-profile.schema.yaml:381-389). The concrete
   window must be set as a domain-owned policy and ratified.
2. REGION / data-locality for evaluation audio has no value in any consent or
   kernel schema; staging claim 5 asserts AVC-09 "records ... region/data
   controls" but the actual region binding for gpt-realtime-2.1 internal-live is
   unspecified. Assume it is pinned in the AVC-09 descriptor at proposal time.
3. OPT-IN SURFACE for evaluation/canary consent is not specified: the standard
   requires withdrawal stays reachable (avatar-first-ui-standard.md:500) and the
   profile maps behaviors to purposes, but no evaluation-specific opt-in UI or
   copy is defined. Needs a ratified surface design (overlaps Fork 5's canary
   cohorting).
4. Whether an evaluation-specific consent purpose (e.g. avatar.evaluation) is
   required, or reusing avatar.provider_processing suffices, is unresolved — the
   count is frozen at 3, so adding one is a kernel change. C assumes reuse of
   provider_processing; Brett should ratify that reuse is legally adequate.
5. No schema-level control currently prevents a second-model shadow or audio
   retention; C's "single-model, ephemeral, never-retained" guarantee rests on
   operational discipline, not an enforced contract field. Whether that needs an
   explicit AVC-09/adapter flag before internal-live is an open assumption.
6. The "pilot-hardening" successor that would carry the retention-class
   unreservation and retained-real evaluation corpus is referenced only
   implicitly ("successor change only"); no such change is named or staged yet.
   Its existence and scope are assumed, not sourced. *(Note: an
   `avatar-pilot-hardening` topic IS staged — see the family INDEX — but the
   sources for this fork do not cite it as the retention-unreservation carrier;
   the linkage is Brett's to confirm.)*
7. The internal-live ring's canary population (internal staff vs. real external
   customers) is not defined for consent purposes and overlaps Fork 5; the
   consent contract's applicability depends on it and must be settled jointly.

---

## Fork 5 — Canary cohorting + rollback semantics

**Fork question (verbatim from the topic):** "Canary cohorting and rollback
semantics. The gate calls for an opt-in canary on new sessions with server-side
profile rollback. Fork: how is the canary cohorted (which tenants/domains, what
opt-in surface), what are the success/abort criteria, and is rollback automatic
on a breached criterion or operator-triggered? Does rollback revoke active leases
or only block new sessions on the withdrawn profile — and how does a
mid-qualification abort preserve the canonical workflow and audit record?"

### What the sources constrain

- **The internal-live ring is a defined release ring** — "live provider
  qualification plus secret scan, telemetry redaction verification, kill-switch
  proof, and measured latency evidence" — a later ring (pilot) requires the prior
  ring's evidence; live provider behavior is NOT release-eligible until
  deterministic acceptance passes. This is qualification, explicitly not the
  pilot ring (which owns threat-model closure, data-handling review,
  accessibility evidence, and rollback rehearsal).
  `specs/avatar-client-runtime/spec.md:606-613`.
- **Exactly two server kill switches exist** — all-new-session-creation, and
  per-model-profile — EACH with OPTIONAL revocation of active leases. Rollback
  SHALL stop new sessions on the withdrawn profile, revoke affected active leases
  WHEN SAFETY REQUIRES IT, and preserve only policy-required records. The
  mechanism supports both block-new and revoke-active; a recorded policy decides
  which applies. `specs/avatar-client-runtime/spec.md:626-629`; `design.md`
  Decision 13:492-495.
- **On kill-switch activation the control API MUST enforce the selected scope
  immediately for new work AND revoke affected active leases "according to the
  recorded policy"** — but that recorded policy is not written in the sources.
  `specs/avatar-client-runtime/spec.md:643-645`.
- **gpt-realtime-2.1 is the FIRST qualified live profile** — this change is what
  qualifies it. Rollback selects the last qualified profile only if one exists;
  if none exists, rollback disables voice and offers text or human handoff. So
  for this canary there is no graceful model fallback: rollback = disable voice →
  text/handoff. `specs/avatar-client-runtime/spec.md:435-437`; `design.md`
  Decision 10:435-442.
- **The revocation guarantee is CLIENT-ENFORCED** (ACR-005 ruling): on revoke the
  client stops its own media leg immediately and requests provider hangup within
  5 s; provider-side authoritative settle (~8.1 s REST 404) is informational, not
  gated. A provider profile that cannot prove media-leg termination within 5 s of
  broker revocation is not eligible for media authorization.
  `f0d-revocation-rerun-notes-2026-07-12.md:69-89`;
  `specs/avatar-client-runtime/spec.md:521-522`.
- **F0 measured the real revocation bound**: client media-leg stop after
  revocation request 2-3 ms; provider hangup acceptance ~250 ms;
  first-playable-after-authorization p50 604 / p95 643 ms; sideband ready p50 772
  / p95 1642 ms. Inputs to the budget, not production SLAs.
  `f0-terminal-pass-report-2026-07-12.md:36-38`.
- **The lease/epoch fence is what rollback mechanically rides**: a session epoch
  fences prior grants, commands, and media legs after revocation or lease expiry;
  lease expiry always closes the media leg even when provider connectivity is
  healthy. Landed P8 fixtures prove the fencing is deterministic
  (lease-epoch-takeover: stale epoch-0 command rejected via
  command_rejected+second_instance_denied, incumbent unaffected;
  stale-revision-command-fenced: command_conflict, control healthy;
  snapshot-barrier-recovery: gap → barrier → snapshot → clean drain, control
  healthy). `design.md` Terms:66-69 +
  `fixtures/deterministic/lease-epoch-takeover.yaml:43-75`,
  `stale-revision-command-fenced.yaml:48-59`, `snapshot-barrier-recovery.yaml:55-66`.
- **A mid-session consent/lease revocation is an authoritative, authored
  terminal** — media leaves "speaking", capture stops, media-gated governed
  commands disable, ending to a credential-free terminal with session_outcome
  "revoked" (NOT a "blocked" safety trip); control_state stays healthy. This is
  the deterministic terminal a rollback-with-active-revocation reuses.
  `fixtures/deterministic/consent-withdraw-mid-speech.yaml:37-55`;
  `session-outcomes.registry.yaml:7-14`.
- **The four authoritative state axes are orthogonal**: session lifecycle
  (broker), control health (lease), media state (adapter), and workflow
  projection (authority-stub/Hermes-owned). The logical session IS the
  user-facing xFactory conversation and workflow identity and survives media
  reconnects; the live plane adds NO second workflow session. Aborting a media
  leg does not by itself terminate the workflow — the workflow projection and its
  records are authority-owned, separate from the media plane. `design.md`
  Decision 2:169-178, Terms:54-56; staging claim 8.
- **Retained-under-policy audit survives an abort**: structured confirmation
  decisions, consent versions, approvals, tool outcomes, and final workflow
  outcomes are retained; SDP/credentials/partial transcripts/provider payloads
  are ephemeral by definition. Rollback "preserves only policy-required records."
  Terminal/revoked/expired/completed/abandoned sessions never resume as active.
  `design.md` Decision 12:472-485, Decision 9:426;
  `specs/avatar-client-runtime/spec.md:364,628-629`.
- **The internal-live cohort/opt-in surface is NOT DEFINED anywhere** in the
  avatar-client sources — a grep across docs/, contracts/, and the kernel change
  for canary|cohort|opt-in returns no cohorting definition; the expert panel's
  original five-ring SBOM/chaos/canary/rollback-rehearsal model was deliberately
  simplified to three rings. `expert-panel-review-2026-07-10.md:174-177` vs
  `specs/avatar-client-runtime/spec.md:607-612`.
- **Authenticated identity for the internal-live ring uses a named concrete
  mechanism** (OIDC bearer validated by the broker for AVC-01 plus the
  per-session control credential in AVC-02); the intended simplest topology is
  one broker deployment per domain deployment with one project-scoped provider key
  per deployment. Release-evidence obligations (incl. a rollback target
  reference) activate AT the internal-live gate. `design.md:97-103`;
  `specs/repo-boundary-governance/spec.md:30-47`.
- **F0 PASS explicitly does not qualify live use**; it may only proceed the
  contract publication gate while the provider profile remains disabled for live
  rings, and any attempt to enable internal-live from F0 evidence alone must be
  rejected and routed through qualify-avatar-live-voice.
  `specs/avatar-brokered-call-feasibility/spec.md:115-128`.

### Options

**Option A — Vendor-org-only, block-new rollback, operator-triggered.** Cohort =
openxFactory/vendor-org INTERNAL accounts only (internal staff, synthetic and
internally-consented audio, zero external tenant and zero real domain-customer
data). Opt-in = a server-side allowlist of named internal actors resolving the
opaque primary_live_voice capability; no client-visible toggle. Rollback default
= the per-model-profile kill switch in BLOCK-NEW mode only (stop new sessions on
gpt-realtime-2.1, let active leases drain to their natural terminal);
active-lease revocation is reserved and fires only through the pre-existing
safety auto-terminals the kernel already guarantees (consent withdrawal, the 5 s
revocation bound, control-loss). No new automatic-abort criteria: latency,
error-rate, and quality breaches are operator judgment calls read off telemetry.
Rollback target is disable-voice → text/handoff (no prior qualified profile
exists). Canonical workflow and audit are preserved because block-new never
touches an in-flight logical session; drained legs terminate cleanly to
session_outcome completed/abandoned with policy-required records retained.
*Tradeoffs:* safest blast radius and simplest to reason about — every abort path
already has a landed deterministic fixture, and nothing new must be built to
auto-detect breaches. But it under-rehearses the very thing the pilot ring will
require: rollback-with-active-lease-revocation is never exercised except by
consent/control terminals, so the "revoke affected active leases when safety
requires it" policy stays untested going into pilot. Operator-only abort also
means a latency or safety-eval regression the operator is slow to catch keeps
serving degraded/unsafe sessions longer than an auto-trip would.

**Option B — Vendor-org + internal domain sandbox, hybrid auto/operator rollback
with a written revoke-vs-block policy.** Cohort = vendor-org internal PLUS one
internally-staffed domain sandbox (e.g. a MedxFactory/LedgerxFactory internal
test tenant) using synthetic and internally-consented audio only — still no real
external customer data, consistent with Fork 4's synthetic-first lean. Opt-in =
server-side capability resolution gated to an allowlisted internal cohort, with a
per-session opt-in recorded in the AVC-01 request context. Rollback is SPLIT by a
recorded policy this fork ratifies: (1) AUTO-abort WITH active-lease revocation on
hard safety/integrity breaches — a revocation-bound violation, a blocked-state /
exact-value / consent / handoff safety-eval failure, a redaction/secret-scan
finding, or a media-authorization ordering violation (these reuse the landed
consent-withdraw-mid-speech terminal: media revoked, capture stops,
credential-free terminal, session_outcome revoked, control healthy); (2) AUTO
block-new WITHOUT active revocation on Fork-2 latency-budget breaches (median/p95
material regression vs the direct-provider reference) and elevated error/quota,
letting in-flight legs drain; (3) OPERATOR-triggered for quality/cost judgment
calls. Success criteria are a clean soak of the cohort against Fork-2 budgets plus
green safety/exact-value/consent/handoff/blocked-state evaluations across generic
+ MedxFactory + LedgerxFactory scenarios. Rollback target is disable-voice →
text/handoff. Canonical workflow survives because the workflow projection is
authority-owned and orthogonal to the media leg (revoking a leg ends media, not
the logical session's governed record); audit is preserved by retaining
policy-required structured records on every terminal.
*Tradeoffs:* best fidelity-to-risk balance: it actually rehearses active-lease
revocation under a written policy (the artifact pilot needs), ties abort criteria
to the two forks that own them (2 and safety), and keeps blast radius internal.
Cost: it forces Brett to ratify the revoke-vs-block criteria split and the
"internal domain sandbox counts as internal-live" boundary now, and it requires
building the auto-detection wiring (latency and safety-eval trips) that Option A
defers. The internal-domain-sandbox inclusion leans on a vendor/tenant
distinction the avatar-client sources do not themselves define.

**Option C — Broad multi-domain canary with automatic-first, aggressive
active-lease revocation.** Cohort spans multiple domains including a limited set
of real consented external tenants; opt-in surfaced as a client-visible toggle.
Rollback is automatic-first on ANY breached criterion — including latency and
quality — and defaults to revoking active leases aggressively to guarantee the
withdrawn profile stops instantly everywhere. Success/abort thresholds set once,
globally, and enforced identically across all domains.
*Tradeoffs:* maximizes qualification coverage and gives the strongest single kill
guarantee, but over-reaches the ring: real external-tenant data collides with
Fork 4's synthetic-first stance and with F0's synthetic-only precedent, and
"internal live" is explicitly not the pilot ring that owns data-handling review
and real-tenant scale. Aggressive auto-revocation of active leases on a mere
latency breach needlessly cuts users off mid-conversation (block-new would
suffice) and burns the exact safety mechanism that should be reserved for genuine
safety trips — the kernel only mandates active-lease revocation "when safety
requires it", not for performance regressions.

### RECOMMENDATION — **Option B** (vendor-org + internal domain sandbox, hybrid rollback with a written policy) *(recommendation, not a ruling)*

Option B is the only option that produces the artifact the next ring demands. The
kernel makes pilot require "rollback rehearsal" and the prior ring's evidence
(spec.md:606-613); Option A never exercises active-lease revocation outside
consent/control terminals, so it walks into the pilot gate with the "revoke
affected active leases when safety requires it" policy (spec.md:626-629, 643-645)
still unwritten and untested. Option B writes and rehearses exactly that policy.
It also honors what the mechanism actually supports: the kernel gives two kill
switches EACH with OPTIONAL active-lease revocation — so a split where safety
breaches revoke active leases (reusing the landed consent-withdraw-mid-speech
terminal path) while latency breaches only block-new is a faithful use of the
primitive, not an invention. It respects the ring boundary that Option C
violates: internal-live is qualification, not pilot, and real external-tenant
data belongs to the pilot's data-handling review — Fork 4 and F0 both establish
synthetic/consented-internal as the norm, so B's internal-domain-sandbox-with-
synthetic-data stays inside the line. Critically, all three options must accept
the same honest constraint — gpt-realtime-2.1 is the FIRST qualified profile
(spec.md:435-437), so rollback can only disable voice to text/handoff; there is
no graceful model fallback, and B names that plainly rather than implying a
hot-swap. On the workflow/audit question the sources are decisive and B relies on
them exactly: the four state axes are orthogonal and the workflow projection is
authority-owned (design Decision 2), the logical session survives media reconnects
(Terms:54-56), and no second workflow session exists (claim 8) — so aborting a
media leg ends media, never the canonical governed record, and policy-required
structured records are retained on every terminal (Decision 12). B is chosen over
A on rehearsal value and over C on blast-radius discipline.

### Unblocks / forecloses

**Unblocks:** a real internal-live qualification of gpt-realtime-2.1 with a
rehearsed, written revoke-vs-block rollback policy that becomes the pilot ring's
rollback-rehearsal evidence; a concrete tie from abort criteria to Fork 2
(latency budgets gate block-new) and to the
safety/exact-value/consent/handoff/blocked-state evaluations (which gate
active-lease revocation); and a cohort small enough (vendor-org + internal
synthetic-data sandbox) that the OIDC-bearer + control-credential identity model
and one-broker-per-domain topology already described suffice without new
tenant-facing infrastructure. **Forecloses / makes harder:** it does NOT test
real external-tenant scale, cross-domain concurrency, or real-customer consent
flows — those are deliberately pushed to the pilot ring, so no scale or real-data
confidence comes out of this gate; it COMMITS operators to "disable voice →
text/handoff" as the only rollback target for this first profile (no model
fallback until a second profile qualifies); and it requires Brett to ratify NOW
both the revoke-vs-block criteria split and the claim that an internal domain
sandbox counts as "internal-live", because the avatar-client sources define
neither.

### Named gaps → assumptions to ratify

1. Canary cohort membership, size, and the opt-in surface are undefined in every
   avatar-client source (grep for canary|cohort|opt-in across docs/, contracts/,
   and the kernel change returns no definition; the expert panel's five-ring
   canary model was simplified to three rings). Brett must ratify the cohort
   boundary and whether opt-in is a server allowlist, a per-session request flag,
   or a client toggle — this memo proposes server-allowlist + per-session-record.
2. The vendor-org vs client-tenant distinction the fork asks to bound the ring by
   is not defined in the avatar-client sources (it lives in a separate
   github-administration-plane context, not here). Whether an internal-staffed
   domain sandbox legitimately counts as "internal-live" rather than "pilot"
   needs Brett's ratification.
3. No numeric canary success/abort thresholds exist for the canary itself —
   minimum session count, soak duration, tolerated error rate, or the exact
   Fork-2 percentile/regression magnitude that trips block-new. The kernel gives
   kill-switch mechanics but no canary exit criteria, and these depend on Fork
   2's still-open budget derivation.
4. The "recorded policy" that decides which criteria require active-lease
   revocation versus block-new (spec.md:645) is not written anywhere; this memo
   proposes the split (safety/integrity → revoke active; latency/error →
   block-new; quality/cost → operator) but it is a proposal for Brett to ratify,
   not an existing constraint.
5. There is no mapping rule for which session_outcome a profile-rollback abort
   must emit — the registry offers both "revoked" and "abandoned", but only
   consent/lease revocation is fixture-bound to "revoked"; an operator-triggered
   profile rollback of a drained leg vs a force-terminated leg has no specified
   outcome token.
6. No operator surface or console for firing the kill switches is defined — the
   web console is an explicit non-goal/deferred item in the kernel, so who holds
   the kill switch and how they trigger it during the canary is unspecified and
   must be named at proposal time.

---

## Latent decisions surfaced

Beyond the five named forks, the research surfaced coupled decisions that are not
themselves fork questions but that a ruling implicates. They are flagged here so
Brett can rule on them alongside, or explicitly defer them.

1. **Repo-locus / extraction timing (from Fork 3, substantiated).** The sources
   bind that a private, independently-releasable, key-free `xfactory-avatar-client`
   repo MUST exist BY the internal-live gate (repo-boundary-governance:22-24,30-43)
   and that the standalone-repo wording "activates at the internal-live gate"
   (002 handoff:136-138) — but **no source names which change performs the
   extraction** from codexFactory `apps/avatar-client-lab`. The staging doc's
   Exit assumes it is in scope for `qualify-avatar-live-voice` (`code_surface:
   openxFactory, xfactory-avatar-client`). If Brett accepts that, this change also
   owns the standalone-repo extraction; if not, a predecessor change must do it
   first. Separately, adding the new repo to the aggregation is explicitly a
   distinct reviewed change (repo-boundary-governance:57-59) — not this one.
   *Decision requested: does qualify-avatar-live-voice perform the extraction, or
   does a predecessor?*
2. **The named pilot-hardening successor (from Forks 1 and 4).** Both the
   custody fork (durable per-tenant spend counter) and the consent fork
   (retention-class unreservation + retained-real corpus) defer work to a
   "pilot-hardening" successor the avatar-client sources reference only implicitly
   ("successor change only"). An `avatar-pilot-hardening` topic IS staged in the
   family INDEX and is described as the last successor gated on
   `qualify-avatar-live-voice` — but the Fork 1/4 sources do not cite it by name
   as the carrier of these specific deferrals. *Decision requested: confirm that
   `avatar-pilot-hardening` is the intended carrier of the deferred durable-counter
   and retention-unreservation work, or name a different successor.*
3. **Production-default status of a qualified gpt-realtime-2.1 (from Fork 3).**
   The sources say internal-live qualification records "approved promotion
   evidence" and rollback "selects the last qualified profile" (spec.md:430-436),
   implying qualification yields a *selectable* profile — but they do not state
   whether qualifying gpt-realtime-2.1 internal-live also makes it the production
   DEFAULT primary. Staging says internal-live-only. *Decision requested: confirm
   internal-live qualification does NOT auto-promote to production default (a
   separate future ruling).*

## Ruling mechanics

- **How Brett rules.** Rule each fork by writing into the "Ruling" cell of the
  "Rulings requested" table above (the recommendation column is advisory only),
  or by leaving a decision comment on the corresponding per-fork section in PR
  review. A ruling may accept the recommended option, pick another labelled
  option, or state a variant — and should, where the option depends on a named
  gap, also settle (or explicitly defer) the numeric/assumption items in that
  fork's "Named gaps → assumptions to ratify" list.
- **What a ruling is.** A ruling here is a **staging decision** that becomes a
  locked input to the future `qualify-avatar-live-voice` change; it is not itself
  a contract mutation, an OpenSpec ratification, or an interface-lock change.
  Nothing in this memo is pre-ratified.
- **On all five ruled.** The topic's Exit section executes: create the
  `qualify-avatar-live-voice` change (`code_surface: openxFactory,
  xfactory-avatar-client`; `target_release: implemented` or a named internal-live
  release defined at proposal time), move this folder's staged files into that
  change's `supporting-docs/` preserving the staging origin, and author the
  `avatar-live-voice` spec deltas — AVC-09/AVC-10 ADDED contracts, the
  `interface-lock.yaml` unreservation, the internal-live activation gate with its
  kill-switch and rollback requirements, and the measured latency budgets — plus
  the acceptance-map and `scripts/validate-avatar-client.py` updates that
  unreserve the two IDs, carrying these five rulings (and any latent-decision
  rulings) as the locked decisions. Because the change realizes a live code
  surface, it archives only on merged plus green internal-live realization
  evidence, never on landing alone.
