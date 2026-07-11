# Clarify Questions: 002-avc-f0-feasibility

**Spec**: [spec.md](./spec.md)
**Generated**: 2026-07-11
**Question count**: 7
**Mode**: Answered inline; the track agent will encode these decisions into `spec.md`.


## Accepted Answers

**Answered**: 2026-07-10 (America/Los_Angeles)

**Decision summary**: `Q1=A; Q2=A+; Q3=Custom; Q4=A; Q5=A; Q6=A; Q7=A+`.

### Q1: A

Feature 002 completes its implementation deliverable when the full harness,
offline self-tests, redaction tests, and a schema-valid terminal evidence record
are committed. If no lab key is available, the record is `INCONCLUSIVE` and no
provider call is attempted or fabricated. Only a later live `PASS` opens the
kernel publication gate; feature completion must not be represented as provider
qualification.

### Q2: A, with local-file safeguards

`OPENAI_API_KEY` in the process environment is the runtime contract. An
explicitly gitignored local `.env` may be used only to populate that environment
for a developer run; it is never read as a result artifact, copied, printed, or
committed. CLI arguments, tracked `.env` files, evidence files, and config files
containing the key are rejected. CI or an approved secret store may inject the
same environment variable.

### Q3: Custom - use the checked-in parallel baseline map directly

During parallel work, F0 reads the versioned
`openspec/changes/define-avatar-client-contract-kernel/supporting-docs/avatar-client-acceptance-map.yaml`
from the shared `avatar-client-parallel-v1` baseline, records its source commit
and digest, and cites the concrete `ACR-*` IDs directly. If that map is absent or
its expected digest/baseline identity does not match, the run is
`INCONCLUSIVE`; F0 must not mint placeholder IDs. The kernel owner still owns
variance disposition and any change to those IDs.

### Q4: A

The six registered groups and 70-trial total are authoritative.
Readiness-timeout is an assertion/path within F0-C; interrupted-run and bounded
cleanup are cross-cutting assertions exercised across all groups, not additional
groups.

### Q5: A

Harness code writes only under `experiments/avatar-brokered-call/`. Committed
run evidence is written directly and atomically under
`openspec/changes/qualify-avatar-brokered-call-feasibility/evidence/`. Do not
maintain a second evidence copy.

### Q6: A

Use an in-harness simulated control/lease authorization stub. It models
lease-ack and media-authorization ordering but has no Hermes or external
control-plane dependency and is not reusable production broker code.

### Q7: A, with deterministic generation

Generate one deterministic synthetic speech-plus-silence fixture per harness
revision, with enough detectable speech and trailing silence to trigger the
pinned `server_vad` profile and elicit a response. Pin generator parameters and
the generated-byte digest in run metadata. Do not commit binary audio or use a
real-user recording.

## Scope note

The spec derives from the ratified-grade OpenSpec change `qualify-avatar-brokered-call-feasibility`, whose registered protocol (`f0-brokered-call-spike-protocol.md`) and result schema (`f0-results.schema.yaml`) already hard-pin the candidate profile (`gpt-realtime-2.1`, voice `marin`, `provider_vad` / `server_vad` params), the trial counts (F0-A = 20, F0-B–F0-F = 10 each; 70 total across exactly six groups), and the timing bounds (3,000 ms default / 5,000 ms ceiling, 5,000 ms revocation, 2,000 ms first-playable p95). Those are settled and are **not** questioned below. The 7 questions below are the only items I judged genuinely open **and** material to planning or implementation, ordered by the priority scope > authority/security > acceptance evidence > sequencing. Recommended options (row A) reflect the reading most consistent with the OpenSpec source.

---

## Q1: Completion scope — live PASS vs. harness + offline tests + terminal record

**Category**: Functional scope / Definition of Done

**Context (spec)**: Assumptions — *"The lab OpenAI project credential is supplied through the environment; when it is absent no live call is attempted and the run is INCONCLUSIVE (the current recorded execution state), with no fabricated artifacts."* Task 3.1 in the OpenSpec change says "Execute every mandatory trial ... using a lab project key," but the currently recorded execution state is `INCONCLUSIVE` (no key present in the review worktree).

**Question**: What is the Definition of Done for feature 002 — does it require a live terminal `PASS`, or is the harness plus offline self-tests plus whatever terminal status a live attempt yields (including `INCONCLUSIVE` if no lab key is available) sufficient to complete the feature?

| Option | Answer | Implications |
|--------|--------|--------------|
| A | Deliver the full harness + offline self-tests as the committed deliverable; run the live matrix only when a lab key is present, otherwise complete 002 with a schema-valid `INCONCLUSIVE` evidence record. A live `PASS` is NOT required to finish 002. **(Recommended)** | Matches the recorded execution state and the "never fabricate artifacts" rule; keeps 002 unblocked by lab-key procurement while still gating kernel publication on a later `PASS`. |
| B | 002 is not complete until a live terminal `PASS` is produced. | Blocks 002 on lab-key access and a green live run; higher confidence but 002 cannot land until the provider run succeeds. |
| C | 002 delivers the harness + offline self-tests only; all live execution is deferred to a separate follow-up feature. | Cleanest separation, but splits the change's tasks 3.1/3.3 across two features and delays any empirical signal. |
| Custom | Provide your own answer | Describe the exact completion bar for 002. |

---

## Q2: Lab credential source contract

**Category**: Security / authority

**Context (spec)**: FR-001 — *"using an externally supplied credential loaded from environment or approved secret storage (never from command arguments or result files)."* The registered protocol names `OPENAI_API_KEY` and notes the review worktree had "no repository `.env`."

**Question**: What credential source(s) constitute a valid run — environment variable only, a gitignored local `.env`, or an external secret store — and what is the exact expected variable/contract?

| Option | Answer | Implications |
|--------|--------|--------------|
| A | Runtime environment variable (`OPENAI_API_KEY`) is the contract; a gitignored local `.env` is an acceptable way to populate the environment; keys in CLI args or result files are rejected by preflight. **(Recommended)** | Aligns with the protocol and constitution (no committed creds); simple and reproducible; preflight FR-003 already rejects credentials-in-arguments. |
| B | Environment variable only, exported by the shell or CI secret store; no `.env` file permitted anywhere. | Strictest; avoids any on-disk key material but adds operator friction for local runs. |
| C | An approved external secret store (e.g., vault) is required; a plain env var is disallowed. | Highest assurance but adds an infrastructure dependency disproportionate to a disposable lab spike. |
| Custom | Provide your own answer | Name the exact acceptable source(s) and variable name. |

---

## Q3: Source of the `ACR-*` IDs the interface-impact report must cite

**Category**: Acceptance evidence / dependencies

**Context (spec)**: FR-018 — *"every variance MUST name the affected `ACR-*` IDs ... and MUST be left for the contract-kernel owner to dispose."* The contract kernel is a parallel, not-yet-published sibling; this change ships no `ACR-*` register of its own.

**Question**: How does F0 obtain the concrete `ACR-*` IDs to reference when the contract kernel that owns them may not be published yet?

| Option | Answer | Implications |
|--------|--------|--------------|
| A | F0 records provisional variance descriptors keyed to the affected `avatar-client-parallel-v1` / AVC-01/AVC-02 fields; if a published `ACR-*` register exists it cites those IDs directly, otherwise the contract-kernel owner binds each descriptor to a concrete `ACR-*` ID at disposition. **(Recommended)** | Lets F0 run fully in parallel (a core design goal) without a hard dependency on kernel publication; the owner performs the final ID binding. |
| B | A published `ACR-*` register must exist before 002 executes; F0 references those IDs directly and blocks if it is absent. | Guarantees exact IDs but couples 002 to kernel sequencing, contradicting the parallel-execution intent. |
| C | F0 mints its own placeholder IDs (e.g., `ACR-TBD-01`) for the kernel owner to rename later. | Simple, but risks placeholder IDs leaking into evidence and needing a rename pass. |
| Custom | Provide your own answer | State where `ACR-*` IDs come from and who binds them. |

---

## Q4: Mapping the named "readiness-timeout" and "interrupted-run / cleanup" trials onto the six pinned groups

**Category**: Acceptance evidence / test design

**Context (spec)**: FR-006 — *"baseline, delayed-sideband, sideband-failure, readiness-timeout, exact-retry, changed-retry, revocation, interrupted-run, and cleanup trials — as the registered six trial groups (F0-A ... 70 trials total)."* The schema pins exactly six groups (F0-A..F0-F = baseline, delayed-sideband, sideband-failure, revocation, exact-retry, changed-retry), so "readiness-timeout," "interrupted-run," and "cleanup" have no dedicated group.

**Question**: How are the three extra named conditions (readiness-timeout, interrupted-run, cleanup) realized against the six authoritative schema groups?

| Option | Answer | Implications |
|--------|--------|--------------|
| A | The six schema groups are authoritative: readiness-timeout is exercised inside F0-C (sideband failure held until the timeout path → `media_readiness_timeout`), and interrupted-run/cleanup is a cross-cutting behavior asserted across all groups (not a seventh group). **(Recommended)** | Keeps `f0-results.json` schema-valid (exactly six groups, 70 trials) and matches the protocol's F0-C description and the always-on cleanup requirement. |
| B | Add dedicated readiness-timeout and cleanup trial groups. | Would break the pinned schema (group set and 70-trial total) and require a schema change first. |
| C | Fold readiness-timeout into F0-B (delayed-sideband pushed past the ceiling) and cleanup into F0-D (revocation). | Schema-valid but conflates distinct assertions, muddying which group evidences the timeout-containment behavior. |
| Custom | Provide your own answer | Specify the exact group-to-condition mapping. |

---

## Q5: Evidence output and commit location

**Category**: Acceptance evidence / sequencing

**Context (spec)**: FR-015 refers to `evidence/f0-results.json` (bare relative path); SC-011 permits writes to *"`experiments/avatar-brokered-call/` and the change's `evidence/` directory"*; FR-021 requires harness **code** to live under `experiments/avatar-brokered-call/`. The protocol pins the three evidence files under `openspec/changes/qualify-avatar-brokered-call-feasibility/evidence/`.

**Question**: Where does the harness write the three evidence files, and which location is committed?

| Option | Answer | Implications |
|--------|--------|--------------|
| A | Evidence is written to and committed under `openspec/changes/qualify-avatar-brokered-call-feasibility/evidence/` (per the protocol); harness code stays under `experiments/avatar-brokered-call/`. Those two are the only writable locations. **(Recommended)** | Matches the registered protocol and SC-011; keeps evidence with the OpenSpec change for archival, code with the experiment. |
| B | Evidence is written under `experiments/avatar-brokered-call/evidence/` and copied into the change directory only at archival. | Keeps all run output co-located with code, but adds a copy step and diverges from the protocol's committed path. |
| C | Both locations — a working copy under the experiment path plus a published copy under the change directory. | Redundant artifacts risk drift between the two copies. |
| Custom | Provide your own answer | Name the single authoritative evidence path. |

---

## Q6: Is "xFactory control readiness" a real dependency or an in-harness stub?

**Category**: Integration / external dependencies

**Context (spec)**: FR-007 — *"MUST hold the provider answer until both sideband verification and xFactory control readiness complete."* Design decision 3 says the harness uses "an internal probe envelope corresponding to the provisional AVC baseline" and lists "reusable broker, client, Hermes integration, or deployment" as non-goals.

**Question**: For F0, is the "xFactory control readiness / lease-ack" channel a real external control-plane (or Hermes) integration, or an in-harness simulated authorization stub?

| Option | Answer | Implications |
|--------|--------|--------------|
| A | An in-harness simulated control stub — a local lease/authorization state machine that models the media-authorization ordering only; F0 has no external control-plane or Hermes dependency. **(Recommended)** | Matches the "no reusable broker/Hermes integration" non-goal and keeps F0 self-contained; the ordering assertion is what F0 measures, not a live control plane. |
| B | A real xFactory control-plane / Hermes integration is required. | Adds a live external dependency and deployment surface, contradicting the change's non-goals. |
| C | Configurable — simulated stub by default, with an optional real integration behind a flag. | Flexible but doubles the surface to build and test for no F0 benefit. |
| Custom | Provide your own answer | State exactly what backs the control-readiness channel. |

---

## Q7: Generated audio fixture requirements

**Category**: Domain / reproducibility

**Context (spec)**: Dependencies — *"Generated audio fixture: a synthetic phrase-and-silence fixture; never a real user recording."* The candidate uses `server_vad` (threshold 0.5, 500 ms silence), so the fixture must actually trigger turn detection for baseline trials to observe first output.

**Question**: What are the fixture requirements, and is there a canonical fixture to reuse or one generated and pinned per harness revision?

| Option | Answer | Implications |
|--------|--------|--------------|
| A | A synthetic fixture containing detectable speech followed by silence sufficient to trigger `server_vad` turn detection and elicit a model response, generated and digest-pinned per harness revision (no shared committed binary). **(Recommended)** | Guarantees baseline/first-media assertions can fire; the fixture digest is already part of the pinned candidate profile (FR-002); avoids committing binary audio to the repo. |
| B | A single canonical fixture committed as a binary artifact and reused across all runs. | Maximizes run-to-run comparability but commits binary audio and a shared artifact to maintain. |
| C | Multiple fixtures of varied phrase length to stress VAD timing. | Broader timing coverage but adds trial variance not required by the pinned matrix. |
| Custom | Provide your own answer | Specify the fixture's content, duration, and provenance requirements. |

---

*End of block — 7 questions. Accepted answers are recorded above; do not proceed to `/speckit-plan` until the track agent integrates them into `spec.md`.*
