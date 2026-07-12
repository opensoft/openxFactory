# Feature Specification: Avatar Brokered-Call F0 Feasibility Experiment

**Feature Branch**: `002-avc-f0-feasibility`

**Created**: 2026-07-11

**Status**: Draft

**Input**: OpenSpec change `qualify-avatar-brokered-call-feasibility` — a disposable,
tenant-data-free lab experiment that empirically proves whether an OpenAI-brokered
WebRTC call can be created, held under sideband control until xFactory control
authorizes media, and terminated within the required bound; and that records where
the provider differs from the frozen `avatar-client-parallel-v1` baseline. The result
gates contract-kernel publication but is explicitly **not** a live-use qualification.

## Clarifications

### Session 2026-07-11

- Q: Does 002's Definition of Done require a live terminal `PASS`, or is the harness plus offline tests plus whatever terminal status a live attempt yields sufficient? → A: 002's implementation deliverable is complete when the full harness, offline self-tests, redaction tests, and a schema-valid terminal evidence record are committed; with no lab key the record is `INCONCLUSIVE` and no provider call is attempted or fabricated. A live `PASS` is not required for completion, and completion is never represented as provider qualification.
- Q: What credential source(s) constitute a valid run, and what is the exact contract? → A: `OPENAI_API_KEY` in the process environment is the runtime contract (CI or an approved secret store may inject it); a gitignored local `.env` may only populate that variable and is never read as a result artifact, copied, printed, or committed; keys supplied via CLI arguments, tracked `.env` files, config files, or evidence files are rejected.
- Q: How does F0 obtain the concrete `ACR-*` IDs the interface-impact report must cite? → A: F0 reads the versioned `openspec/changes/define-avatar-client-contract-kernel/supporting-docs/avatar-client-acceptance-map.yaml` from the `avatar-client-parallel-v1` baseline, records its source commit and digest, and cites concrete `ACR-*` IDs directly; if that map is absent or its expected digest/baseline identity does not match, the run is `INCONCLUSIVE` and F0 mints no placeholder IDs; the contract-kernel owner still owns variance disposition.
- Q: How do the named readiness-timeout, interrupted-run, and cleanup conditions map onto the six schema groups? → A: The six registered groups (F0-A…F0-F) and the 70-trial total are authoritative; readiness-timeout is an assertion/path exercised within F0-C, and interrupted-run and bounded cleanup are cross-cutting assertions exercised across all groups, not additional groups.
- Q: Where does the harness write the three evidence files, and which location is committed? → A: Harness code writes only under `experiments/avatar-brokered-call/`; committed run evidence is written directly and atomically under `openspec/changes/qualify-avatar-brokered-call-feasibility/evidence/`; no second evidence copy is kept. Those are the only writable locations.
- Q: Is "xFactory control readiness / lease-ack" a real external control-plane dependency or an in-harness stub? → A: An in-harness simulated control/lease authorization stub that models lease-ack and media-authorization ordering only; it has no Hermes or external control-plane dependency and is not reusable production broker code.
- Q: What are the audio fixture requirements — canonical reuse or generated per revision? → A: One deterministic synthetic speech-plus-silence fixture is generated per harness revision, with enough detectable speech and trailing silence to trigger the pinned `server_vad` profile and elicit a response; generator parameters and the generated-byte digest are pinned in run metadata; no binary audio is committed and no real-user recording is used.

## User Scenarios & Testing *(mandatory)*

<!--
  User stories map 1:1 to the OpenSpec change's ABF-* requirements so that every
  slice is independently testable and traceable. F0 uses generated audio, a lab
  project key, and no tenant data; the "actors" are the F0 operator running the
  experiment and the contract-kernel owner who consumes its evidence.
-->

### User Story 1 - Prove the brokered-call handshake with the complete trial matrix (Priority: P1)

An F0 operator runs the registered trial matrix against the pinned lab candidate and
obtains per-trial evidence showing that the provider answer is held until sideband
verification and xFactory control readiness authorize media, that failures never leak
media, and that retries neither duplicate a provider call nor disclose a prior answer.

**Why this priority**: This is the reason the feature exists — the ordering,
failure-containment, and retry behaviors are empirical provider facts that no schema or
mock can prove. Without them there is no feasibility signal. (Traces ABF-002.)

**Independent Test**: Execute the baseline, delayed-sideband, sideband-failure,
exact-retry, changed-retry, and interrupted-run/cleanup trials and inspect the recorded
ordering markers, termination outcomes, and provider-call counts per trial.

**Acceptance Scenarios**:

1. **Given** provider create, sideband attach, and xFactory control acknowledgement all complete within the configured deadline (baseline), **When** the trial runs, **Then** media authorization occurs after both control channels are verified and before answer application or first media, and exactly one provider call is created for the request.
2. **Given** sideband verification completes after an injected delay but still before the configured deadline (delayed-sideband), **When** the trial runs, **Then** the answer remains held and the trial may pass only after ordered media authorization.
3. **Given** sideband attachment or verification fails (sideband-failure), **When** the trial runs, **Then** the harness authorizes no media, applies no answer, and terminates the provider call.
4. **Given** the same request and exact offer identity are retried after a simulated lost response (exact-retry), **When** the trial runs, **Then** evidence shows at most one provider call and an equivalent unconsumed result.
5. **Given** the request ID is reused with a changed offer fingerprint or other non-volatile field (changed-retry), **When** the trial runs, **Then** the prior answer is not disclosed and no second provider call is created under that request ID.
6. **Given** the harness stops during any trial phase (interrupted-run), **When** cleanup runs, **Then** bounded cleanup attempts termination for every known call ID and records the cleanup outcome.

---

### User Story 2 - Guarantee an isolated, tenant-data-free, reproducible environment (Priority: P1)

Before any provider call is created, the harness proves it is running against a
dedicated lab project with generated audio, disabled tools, no tenant data, and a fully
pinned candidate profile — and it refuses to run, or reports INCONCLUSIVE, when those
conditions are not met.

**Why this priority**: Safety is non-negotiable and prerequisite to every trial; a run
that touches tenant data or an unpinned profile is invalid regardless of its results.
(Traces ABF-001.)

**Independent Test**: Supply a configuration containing tenant identifiers, enabled
tools, or a non-lab profile and confirm preflight rejection before any provider call;
separately, make the candidate unavailable and confirm the run reports INCONCLUSIVE
without inferring provider behavior.

**Acceptance Scenarios**:

1. **Given** a valid lab credential and a fully pinned candidate profile, **When** the harness starts, **Then** it records only redacted configuration digests and executes the selected bounded trials.
2. **Given** a configuration containing tenant identifiers, tenant content, enabled tools, or a non-lab profile, **When** the harness starts, **Then** preflight rejects the run before any provider call is created.
3. **Given** the candidate is unavailable or its API shape prevents a mandatory trial from starting, **When** the harness runs, **Then** the run reports INCONCLUSIVE and does not infer provider behavior.

---

### User Story 3 - Produce redacted, schema-valid terminal evidence and a variance handoff (Priority: P1)

Every run emits machine-readable results, a human-readable summary, and an
interface-impact document, classified as PASS, FAIL, or INCONCLUSIVE, with all
prohibited content excluded and every provider variance mapped to the affected
contract-kernel acceptance IDs for disposition.

**Why this priority**: The evidence artifacts are the feature's deliverable and the
input to the kernel publication gate; without publishable, correctly classified
evidence the experiment produces nothing consumable. (Traces ABF-004.)

**Independent Test**: Run the harness to completion and confirm the results validate
against the registered schema, the overall status is exactly one of PASS/FAIL/INCONCLUSIVE
per the classification rules, the interface-impact document is emitted (empty variance
list on a clean pass), and a redaction scan reports zero prohibited findings.

**Acceptance Scenarios**:

1. **Given** every mandatory trial executes with complete redacted evidence and every assertion passes, **When** results are classified, **Then** the overall result is PASS and the interface-impact document is still emitted.
2. **Given** a reproducible observation violates required ordering, timing, retry, cleanup, or redaction behavior, **When** results are classified, **Then** the overall result is FAIL.
3. **Given** a required trial did not run or lacked sufficient observable evidence, **When** results are classified, **Then** the overall result is INCONCLUSIVE and never PASS.
4. **Given** an observation requires a neutral interface correction, **When** the variance is recorded, **Then** F0 records the variance with the affected `ACR-*` IDs and edits no canonical contract or sibling implementation file.

---

### User Story 4 - Measure readiness and revocation timing against the neutral bounds (Priority: P2)

The harness measures every trial with a monotonic clock, enforces the 3,000-millisecond
default and 5,000-millisecond hard readiness ceiling, and proves the provider leg
terminates within five seconds of a revocation, keeping request acceptance and observed
termination as separate evidence.

**Why this priority**: Timing bounds refine the ordering proof and are required for a
full PASS, but the ordering correctness measured in User Story 1 is the prerequisite
observation; timing layers measurable ceilings on top of it. (Traces ABF-003.)

**Independent Test**: Run the F0-C readiness-timeout path and the F0-D revocation/
provider-hangup trials and inspect the recorded monotonic offsets against the selected
deadline and the five-second termination bound, with revocation-request, hangup-request,
and terminal-observation offsets recorded separately.

**Acceptance Scenarios**:

1. **Given** sideband and xFactory control become ready within the selected 1,000-to-5,000-millisecond value (the configured `readiness_deadline_ms`, default 3,000 ms), **When** the readiness assertion is evaluated, **Then** the measured trial may pass its readiness assertion.
2. **Given** either required control channel misses the selected deadline (readiness-timeout), **When** the trial runs, **Then** the harness withholds media authorization, terminates the call, and fails if any media or answer application occurred.
3. **Given** the harness revokes an authorized trial and observes provider termination within five seconds (revocation / provider-hangup), **When** the trial runs, **Then** it records separate revocation-request, hangup-request, and terminal-observation offsets.
4. **Given** a mandatory terminal signal is absent or arrives after five seconds, **When** the revocation assertion is evaluated, **Then** the assertion is FAIL or INCONCLUSIVE according to whether contrary behavior or missing evidence was observed.

---

### User Story 5 - Enforce the non-qualification boundary (Priority: P2)

The F0 result establishes only whether the brokered-call handshake is feasible under the
recorded lab conditions; it never promotes a provider profile, enables internal-live or
production media, or waives gates owned by successor changes.

**Why this priority**: This governance guardrail protects against over-reading the
evidence; it constrains interpretation rather than producing the evidence itself, but a
violation would be a safety-critical defect. (Traces ABF-005.)

**Independent Test**: With an overall PASS result, confirm the contract publication gate
may proceed after variance disposition while the provider profile stays disabled for live
rings; then attempt to enable internal-live or production media using only F0 evidence and
confirm release validation rejects the promotion.

**Acceptance Scenarios**:

1. **Given** the overall F0 result is PASS, **When** the contract publication gate is evaluated, **Then** it may proceed after variance disposition, but the provider profile remains disabled for live rings.
2. **Given** an operator attempts to enable internal-live or production media using only F0 evidence, **When** release validation runs, **Then** it rejects the promotion and requires `qualify-avatar-live-voice`.

---

### Edge Cases

- **Provider unavailable or API shape differs** before a call can be tested → the run is INCONCLUSIVE, never an inferred PASS or FAIL.
- **Acceptance-map source missing or digest/baseline mismatch** → the run is INCONCLUSIVE; F0 never mints placeholder `ACR-*` IDs to proceed.
- **No lab credential present** → no provider call is attempted; the run completes as INCONCLUSIVE with no fabricated artifacts, and this still satisfies feature completion.
- **Redaction failure detected** in any output (logs, traces, crash output, or evidence files) → the run is FAIL and commit is prevented.
- **Weak or absent termination confirmation** → request-accepted and termination-observed are kept as separate fields; the stronger assertion is required where the provider exposes a terminal signal, and missing confirmation is never treated as success.
- **Network jitter obscuring thresholds** → multiple trials and raw monotonic durations are recorded rather than a single sample, and protected payloads are never stored.
- **Latency miss on a p95 or hard-ceiling bound** → cannot be hidden by averages; it is a FAIL requiring an explicit design disposition.
- **Harness drifting into a reusable broker** → reusable-runtime imports are prohibited and all code stays under the experiment path.
- **Interrupted run mid-trial** → bounded cleanup attempts termination for every known call ID and records the outcome.

## Requirements *(mandatory)*

### Functional Requirements

**Environment and safety (ABF-001)**

- **FR-001**: The harness MUST execute only against a dedicated lab provider project, using generated audio, disabled tools, and no tenant data. The provider credential MUST be read only from the `OPENAI_API_KEY` process environment variable (which CI or an approved secret store MAY inject, and which a gitignored local `.env` MAY populate); the credential MUST NEVER be read from command arguments, tracked `.env` files, config files, or result files, and MUST NEVER be copied into, printed to, or committed with any evidence artifact.
- **FR-002**: The harness MUST use an immutable per-run candidate profile identified by a digest covering harness revision, dependency-lock digest, model, voice, turn settings, timeout settings, and generated-audio fixture digest. The generated-audio fixture MUST be one deterministic synthetic speech-plus-silence clip generated per harness revision — with enough detectable speech and trailing silence to trigger the pinned `server_vad` profile and elicit a response — and both its generator parameters and its generated-byte digest MUST be pinned in run metadata; no binary audio is committed and no real-user recording is used.
- **FR-003**: Preflight MUST reject the run before any provider call when the configuration contains tenant identifiers, tenant content, enabled tools, a credential supplied via command arguments or a tracked `.env`/config/evidence file, a readiness value above 5,000 milliseconds, or any non-lab or unpinned profile.
- **FR-004**: When the candidate is unavailable or its API shape prevents a mandatory trial from starting, the run MUST report INCONCLUSIVE and MUST NOT infer provider behavior.
- **FR-005**: The harness MUST terminate every known provider call during cleanup and MUST NOT create a standing service or reusable production broker.

**Trial matrix and ordering (ABF-002)**

- **FR-006**: F0 MUST execute exactly the six registered trial groups totalling 70 trials — F0-A baseline (20), F0-B delayed-sideband (10), F0-C sideband-failure (10), F0-D revocation (10), F0-E exact-retry (10), F0-F changed-retry (10); this group set and total are authoritative. Readiness-timeout MUST be exercised as an assertion/path within F0-C (sideband held until the timeout path), and interrupted-run and bounded cleanup MUST be cross-cutting assertions exercised across all groups — none of these three is a separate trial group.
- **FR-007**: The harness MUST hold the provider answer until both sideband verification and xFactory control readiness complete, and MUST record provider call creation, sideband readiness, media authorization, answer application, and first media as separate observations. "xFactory control readiness / lease-ack" MUST be an in-harness simulated control/lease authorization stub that models the media-authorization ordering only — it MUST NOT depend on Hermes or any external control-plane and MUST NOT be reusable production broker code.
- **FR-008**: In the baseline and delayed-sideband trials, media authorization MUST occur only after both control channels are verified and before answer application or first media.
- **FR-009**: On sideband failure the harness MUST authorize no media, apply no answer, and terminate the provider call.
- **FR-010**: For an exact retry (same request and offer identity) evidence MUST show at most one provider call and an equivalent unconsumed result; for a changed retry (reused request ID with a changed offer fingerprint or non-volatile field) the prior answer MUST NOT be disclosed and no second provider call may be created under that request ID.

**Timing and revocation (ABF-003)**

- **FR-011**: The harness MUST measure durations with a monotonic clock, recording per-trial offsets from provider-create acceptance for at least: provider response, call-ID availability, sideband connection, sideband verification, xFactory control readiness, media authorization, answer application, first media, revocation request, hangup request, and confirmed termination where observable. Wall-clock timestamps are coarse run metadata only.
- **FR-012**: Media readiness MUST use a 3,000-millisecond default and MUST NOT exceed the 5,000-millisecond neutral ceiling; when a required control channel misses the selected deadline, the trial MUST withhold media authorization, terminate the call, and fail if any media or answer application occurred.
- **FR-013**: A revocation trial MUST request provider termination immediately and MUST observe provider termination within five seconds when the provider exposes an observable terminal signal, recording revocation-request, hangup-request, and terminal-observation offsets separately.
- **FR-014**: When a mandatory terminal signal is absent or arrives after five seconds, the revocation assertion MUST be FAIL or INCONCLUSIVE according to whether contrary behavior or missing evidence was observed — never PASS.

**Evidence, redaction, and handoff (ABF-004)**

- **FR-015**: Each run MUST emit schema-valid machine-readable results, a human-readable summary, and an interface-impact document, written directly and atomically under `openspec/changes/qualify-avatar-brokered-call-feasibility/evidence/` as `f0-results.json`, `f0-results.md`, and `f0-interface-impact.yaml`; no second copy of the evidence is kept. The results MUST validate against the registered result schema and include the SHA-256 of the human-readable report.
- **FR-016**: The overall result MUST be classified as PASS only when every mandatory trial ran and every required assertion passed; FAIL when a mandatory trial produced a contrary, reproducible observation; and INCONCLUSIVE when a mandatory trial could not run or lacked sufficient evidence.
- **FR-017**: Committed evidence — and all logs, traces, and crash output — MUST exclude credentials, SDP, raw provider payloads, raw media/audio, transcript content, arbitrary or high-cardinality subject identifiers, and unbounded strings; a redaction failure MUST make the run FAIL and prevent commit.
- **FR-018**: The interface-impact document MUST be emitted on every run (with an empty variance list on a clean pass); every variance MUST name the affected `ACR-*` IDs, observed provider behavior, evidence references, severity, proposed contract correction, and whether sibling work can continue behind a closed default, and MUST be left for the contract-kernel owner to dispose. F0 MUST source the concrete `ACR-*` IDs by reading the versioned `openspec/changes/define-avatar-client-contract-kernel/supporting-docs/avatar-client-acceptance-map.yaml` from the `avatar-client-parallel-v1` baseline and MUST record that map's source commit and content digest in the evidence. If the map is absent or its expected digest/baseline identity does not match, the run MUST be `INCONCLUSIVE`; F0 MUST NOT mint placeholder `ACR-*` IDs.

**Non-qualification boundary (ABF-005)**

- **FR-019**: The F0 result MUST establish only feasibility under the recorded lab conditions and MUST NOT promote a provider profile, enable internal-live or production media, satisfy production latency budgets, or waive deterministic, security, accessibility, operational, or rollback gates owned by successor changes.
- **FR-020**: On overall PASS, the contract publication gate MAY proceed after variance disposition while the provider profile remains disabled for live rings; an attempt to enable internal-live or production media using only F0 evidence MUST be rejected by release validation, which requires `qualify-avatar-live-voice`.

**Scope isolation**

- **FR-021**: The harness and all its code MUST live under `experiments/avatar-brokered-call/`, and committed run evidence MUST live under `openspec/changes/qualify-avatar-brokered-call-feasibility/evidence/`; these are the only two locations the run may write. The harness MUST NOT modify canonical contracts (`contracts/avatar-client/`), release metadata, reference-runtime, UI, DomainxFactory, or deployment files, and MUST NOT import reusable runtime code.

### Key Entities *(include if feature involves data)*

- **Trial**: A single execution of one controlled condition (identified as `F0-<A–F>-NN`), carrying a status (PASS/FAIL/INCONCLUSIVE), a set of monotonic duration offsets, the assertion IDs it covers, and a hashed (not raw) provider request identifier.
- **Trial group**: An aggregate over one controlled condition (F0-A…F0-F) recording planned, completed, passed, and failed counts.
- **Candidate profile**: The immutable pinned configuration under test — model, voice, interaction mode, turn-detection parameters, tools-disabled state, generated-audio fixture, timeout values, dependency lock, and harness revision — represented as digests, never raw secrets.
- **Assertion**: A named mandatory check (e.g. ordering, single-call, timing, redaction) with a status and passed/failed trial counts.
- **Evidence record (`f0-results.json`)**: The schema-valid machine-readable run output — protocol version, environment metadata, candidate, trial groups, per-trial rows, duration metrics (p50/p95/max), assertion results, redaction-scan result, overall status, and report hash.
- **Human-readable summary (`f0-results.md`)**: The narrative companion recording deviations, API-shape corrections, threat-model disposition, and reviewer decision; its SHA-256 is bound into the evidence record.
- **Interface-impact variance report (`f0-interface-impact.yaml`)**: The list of provider/baseline mismatches, each naming affected `ACR-*` IDs, observed behavior, evidence, severity, proposed correction, and closed-default continuation status.
- **Redaction-scan result**: The status and count of prohibited-content findings that gate whether a run may be committed.

## Success Criteria *(mandatory)*

<!--
  Timing and ordering bounds are part of WHAT this experiment must establish, so they
  appear here as measurable, technology-agnostic outcomes rather than implementation
  detail. All are verifiable from the committed evidence record.
-->

### Measurable Outcomes

- **SC-001**: In 100% of baseline and delayed-sideband trials, media authorization is recorded after both control channels are verified and before answer application or first media, and exactly one provider call is created per request.
- **SC-002**: Baseline sideband verification has a p95 no greater than 3,000 milliseconds, and no trial exceeds 5,000 milliseconds from provider-create acceptance.
- **SC-003**: First playable output after media authorization has a p95 no greater than 2,000 milliseconds.
- **SC-004**: 100% of sideband-failure and readiness-timeout trials authorize no media and apply no answer, and every affected provider call is terminated.
- **SC-005**: 100% of revocation trials reach provider-terminal state and cease observable provider-bound input/output within 5,000 milliseconds, with request and observed-termination offsets recorded separately.
- **SC-006**: 100% of exact-retry trials produce at most one provider call, and 100% of changed-retry trials disclose no prior answer and create no second provider call under the reused request ID.
- **SC-007**: The redaction scan reports zero prohibited-content findings across evidence, logs, traces, and crash output on every committed run.
- **SC-008**: `f0-results.json` validates against the registered result schema with zero errors, and the overall status is exactly one of PASS, FAIL, or INCONCLUSIVE per the classification rules (PASS requires every mandatory trial and assertion to pass).
- **SC-009**: 100% of preflight runs configured with tenant data, enabled tools, a non-lab or unpinned profile, credentials in arguments, or a readiness value above 5,000 milliseconds are rejected before any provider call is created.
- **SC-010**: The interface-impact document is emitted on 100% of runs (empty variance list on a clean pass), and every recorded variance names at least one affected `ACR-*` ID drawn from the digest-verified `avatar-client-acceptance-map.yaml`; zero placeholder or unsourced `ACR-*` IDs appear in committed evidence.
- **SC-011**: Zero files outside `experiments/avatar-brokered-call/` and `openspec/changes/qualify-avatar-brokered-call-feasibility/evidence/` are modified by an F0 run — no canonical contract, release metadata, reference-runtime, UI, DomainxFactory, or deployment file changes.
- **SC-012**: Zero live rings are enabled from F0 evidence alone; any attempt to enable internal-live or production media using only F0 evidence is rejected pending `qualify-avatar-live-voice`.
- **SC-013**: Feature 002's implementation deliverable is complete once the harness, offline self-tests, redaction tests, and a schema-valid terminal evidence record are committed; when no lab key is available that record is `INCONCLUSIVE` with zero provider calls attempted and zero fabricated artifacts. A live `PASS` is not required for feature completion, and completion is never represented as provider qualification.

## Assumptions

- The initial pinned candidate is `gpt-realtime-2.1` with voice `marin`, interaction mode `provider_vad`, and `server_vad` turn detection (threshold 0.5, prefix padding 300 ms, silence 500 ms, create/interrupt response enabled), tools empty, and transcript retention disabled — per the registered protocol.
- Provider-create acceptance is the timing origin (t=0) for all monotonic offsets; wall-clock timestamps are coarse run metadata only.
- The readiness default is 3,000 ms with a 5,000 ms hard ceiling; the revocation termination bound is 5,000 ms; the first-playable-after-authorization architecture threshold is a p95 of 2,000 ms (not a production SLA).
- The registered trial matrix comprises six groups totalling 70 trials (F0-A = 20; F0-B–F0-F = 10 each); a full PASS requires every mandatory trial and assertion to pass.
- The lab OpenAI project credential is supplied only via the `OPENAI_API_KEY` process environment variable (optionally populated by a gitignored local `.env`, or injected by CI or an approved secret store); when it is absent no live call is attempted and the run is INCONCLUSIVE (the current recorded execution state), with no fabricated artifacts — and this still counts as feature completion.
- Evidence artifacts are written directly and atomically under `openspec/changes/qualify-avatar-brokered-call-feasibility/evidence/` (the single authoritative location, no second copy) and are publishable by construction via an allowlist that rejects prohibited content before writing.
- The harness models "xFactory control readiness / lease-ack" with an in-harness simulated control/lease authorization stub (no Hermes or external control-plane), and may use an internal probe envelope corresponding to the provisional `avatar-client-parallel-v1` baseline without publishing that envelope as a contract.
- Maintained WebRTC and WebSocket libraries are used rather than a hand-rolled media stack, with a pinned runtime and dependency lock; the specific library choices are implementation decisions deferred to planning.

## Dependencies

- **Frozen interface baseline**: `avatar-client-parallel-v1` (the provisional AVC envelope) — F0 observes against it and records variances; it does not modify it.
- **Lab provider access**: an externally supplied lab OpenAI project and a dedicated provider project; the credential is read only from the `OPENAI_API_KEY` process environment variable (optionally populated by a gitignored local `.env`, or injected by CI/an approved secret store), never from arguments or committed files.
- **Generated audio fixture**: one deterministic synthetic speech-plus-silence clip generated per harness revision (generator parameters and byte digest pinned in run metadata); never a committed binary and never a real user recording.
- **`ACR-*` acceptance-map source**: the versioned `openspec/changes/define-avatar-client-contract-kernel/supporting-docs/avatar-client-acceptance-map.yaml` from the `avatar-client-parallel-v1` baseline, read by digest; the interface-impact report cites its concrete `ACR-*` IDs, and a missing or mismatched map forces an INCONCLUSIVE run.
- **Registered protocol and schema**: `f0-brokered-call-spike-protocol.md` (trial matrix, instrumentation, pass/escalation rules) and `f0-results.schema.yaml` (result-record schema) in the change's `supporting-docs/`.
- **Contract-kernel owner**: consumes the result and interface-impact report at publication and disposes every variance (including any change to the cited `ACR-*` IDs); the F0 result gates that kernel's publication but F0 cannot edit the kernel.
- **Successor change**: `qualify-avatar-live-voice` owns live-profile promotion, production topology, and formal latency budgets — out of scope here.

## Out of Scope

- Qualifying any model or provider profile for internal-live or production use, or enabling any live ring.
- Defining or editing canonical AVC contract fields, release metadata, or any sibling reference-runtime, UI, DomainxFactory, or deployment file.
- Implementing a reusable broker, client, Hermes integration, deployment, or standing service.
- Measuring production SLOs, broad network variance, cost, or accessibility.
- Testing GPT-Live before OpenAI publishes a supported API contract and a new proposal defines its qualification profile.
