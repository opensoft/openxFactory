# Expert Panel Review Record

Status: record
Kind: review record
Captured: 2026-07-10
Repository context: openxFactory
Proposed by: define-avatar-client-runtime
Scope: adversarial multi-agent review of the 2026-07-10 first draft of this
change; its verified findings drove the same-day simplification rewrite of
proposal.md, design.md, tasks.md, and the four spec deltas.

This proposal supporting document is non-normative. The delta specifications
are authoritative. This record preserves what the review found, what the
rewrite did with each finding, and which items remain open as repo debt or
successor-change scope.

## Method

Fifteen agents in three phases. Seven experts reviewed the full ~3,100-line
draft through distinct lenses: principal engineering (implementability),
OpenAI Realtime/WebRTC (provider facts verified against current public
documentation), distributed-systems protocol, security and privacy, OpenSpec
spec quality, Flutter client architecture, and delivery pragmatism. Each
expert report was then adversarially fact-checked by an independent verifier
agent that re-read the cited text and marked every finding CONFIRMED,
ADJUSTED (real issue, detail corrected), or REFUTED. A completeness critic
swept the surviving findings for missed angles. All agents were briefed on
the load-bearing invariants (server-held provider keys; untrusted client;
Hermes authority over consent/policy/approval; consent-before-capture; no
secrets in telemetry) so simplification proposals could not gut governance.

Verdict totals: 79 findings produced, 71 survived verification (57
CONFIRMED, 13 ADJUSTED, 1 REFUTED), plus 8 additional findings from the
completeness critic. The full machine-readable output was a session
artifact and is not retained; this record is the durable summary.

## Provider Facts Verified (2026-07-10)

The draft's OpenAI homework was unusually accurate. Verified against current
OpenAI documentation (developers.openai.com Realtime guides and the GPT-Live
announcement):

- `gpt-realtime-2.1` is a released API Realtime model; `gpt-live-1` is
  ChatGPT-only with no API contract.
- `POST /v1/realtime/calls` creates a server-owned call from an SDP offer
  and accepts the full session configuration (model, voice, instructions,
  tools, turn detection) atomically in the create request.
- A server sideband WebSocket attaches to an existing call by call ID.
- Voice is immutable after the model first emits audio.
- Sessions cap near 60 minutes and ~28.7k input tokens with configurable
  auto-truncation.
- In WebRTC mode the client interruption pair is `response.cancel` plus
  `output_audio_buffer.clear`; server VAD auto-truncates unplayed audio.

## Findings And Dispositions

Disposition legend: **Edit** = resolved in the rewrite of this change;
**Deferred** = moved to a named successor change with a closed default;
**Noted** = pre-existing repo debt recorded here, not owned by this change;
**Refuted** = rejected by the verification pass.

### Theme 1 — The foundation did not exist (critical)

- The "openxFactory control API" had no deployment, persistence, or
  authentication story; openxFactory contains one Python module and no
  server, and identity was hand-waved to nonexistent middleware (principal
  P1, security P3). **Edit:** change rescoped to contracts plus a
  deterministic in-memory reference broker documented as non-deployable;
  internal-live authentication named concretely (OIDC bearer at the broker
  plus the AVC-02 control credential); production deployment home and
  topology assigned to `qualify-avatar-live-voice`.
- Hermes, named as the authority for consent/tools/confirmation throughout,
  is a scaffold with no API; no task defined the broker-to-Hermes surface
  (principal P2, delivery P2). **Edit:** fail-closed in-process authority
  stub (static policy bundle, fixture consent records, one reference intake
  workflow) exercises that authority explicitly on behalf of the future
  Hermes boundary; real integration deferred to `avatar-pilot-hardening`.
- One change bundled contract ratification with ~93 tasks of two-repo
  implementation, and `code_surface` included a repository that does not
  exist, so under release-realization the change could not archive until a
  full product shipped (principal P3, spec-quality P4, delivery P11).
  **Edit:** code surface narrowed to openxFactory; client repository
  creation and everything from live media onward moved to the named
  successor map; 24 tasks remain.

### Theme 2 — Protocol redundancy (major)

- Roughly nine delivery/fencing mechanisms where about four suffice for one
  broker and one client per session (protocol P3/P5, flutter P3, security
  P6, delivery P5). **Edit:** kept request-id idempotency, command-id
  dedupe, conditional expected-revision, and epoch+lease fencing; cut
  `previous_event_id` hash chains, snapshot integrity digests,
  `idempotency_scope`, the separate draft-sync key, per-message WSS acks,
  and the entire replay protocol (recovery is snapshot-only over one
  control-API-sequenced event log).
- AVC-06 `binding_digest` was security theater — server-computed, echoed
  back by the untrusted client, proving nothing beyond ID+version, while
  forcing cross-language canonical serialization (security P2, protocol
  P7). **Edit:** dropped; confirmation binds by ID + version + issuing
  revision + expiry with supersede-on-material-change.
- Load-bearing mechanics were unspecified: heartbeat/lease renewal
  protocol, retry "equivalence", who assigns state revisions,
  snapshot-versus-live handover (protocol P2/P4/P8/P9). **Edit:** all four
  specified (heartbeat carries epoch + last-applied sequence and extends
  the lease; equivalence is canonical-form equality excluding declared
  volatile fields; the control API is the sole sequencer; recovery
  discards events at or below the snapshot revision).
- `expected_state_revision` mandatory on all commands would make benign
  commands chronically race live-voice event flow (protocol P6). **Edit:**
  required only on registry-flagged revision-guarded command types.

### Theme 3 — Provider-facing design flaws (major)

- The one-time SDP answer contradicted "retries return the same result":
  the primary retry case is exactly the one where the answer was already
  minted (realtime P1, protocol P1). **Edit:** grant persisted and
  redelivered verbatim to the same client instance until first media
  connect or expiry; SDP answers single-use and offer-bound; a retry whose
  call never connected receives a fresh media leg under the same logical
  session.
- Sideband-readiness-before-SDP-answer serialized avoidable setup latency;
  the create request already applies configuration atomically (realtime
  P2). **Edit:** answer released immediately, sideband attaches in
  parallel, and tool intents/consequential responses stay blocked until
  attach verifies; media leg revoked on attach failure.
- Default-deny context carryover meant an ordinary network drop produced an
  assistant with total amnesia (realtime P3). **Edit:** bounded ephemeral
  same-session recent-turns carryover defined as the reconnect default;
  full-transcript carryover remains policy-gated and out of scope.
- The AVC-01 field list omitted the SDP offer that design step 2 said it
  carries (spec-quality P2). **Edit:** transient never-persisted
  `sdp_offer` field added.
- The constrained data channel was viable but unnamed (realtime P6).
  **Edit:** complete outbound allowlist named: `response.cancel` and
  `output_audio_buffer.clear`; `conversation.item.truncate` excluded.
- Speculative AVC-03 capability enums encoded GPT-Live behaviors the
  non-goal disclaims (realtime P8). **Edit:** capabilities inlined into the
  grant and trimmed to what the qualified adapter reports.

### Theme 4 — Features without consumers (major)

Each deferred with a closed default rather than unspecified behavior:

- Offline drafts (platform crypto, key destruction, sync conflict review)
  — an encrypted-sync subsystem inside a client that is online by
  construction (principal P8, security P7, flutter P5, delivery P7).
  **Deferred** to `avatar-offline-drafts`; the client persists no sensitive
  session data locally; the online stale-revision review rule covers the
  conflict UX.
- `pre_speech_review` reviewed-speech pipeline had no implementing slice or
  contract surface (principal P7, security P11, delivery P9). **Deferred**:
  the enum value stays reserved and fail-closed (selection fails preflight
  into text/human fallback). The stronger claim that the gate was
  unsatisfiable as specified was **Refuted** — the draft already allowed
  text fallback; the deferral is a scope decision, not a correctness fix.
- Mid-session persona change with media-leg rotation (realtime P7, delivery
  P9). **Deferred**: persona fixed per logical session; changing persona
  ends the session; voice fixed per media leg.
- Seamless provider-context rollover with rehydration packets (principal
  P9, realtime P4). **Deferred**: profile duration caps below provider
  limits plus an explicit `session_limit_reached` resume state.
- Web-console handoff exchange codes for a console that does not exist
  (security P12). **Deferred** to the web-console change; the two URL/
  exchange invariants ratify now.
- Multi-client takeover (delivery defer list). **Deferred**: second
  instance denied; epoch retained for revocation fencing.
- AVC-09 adapter descriptor and AVC-10 latency sample had no in-scope
  consumer (principal P5, flutter P4). **Deferred** to
  `qualify-avatar-live-voice`; IDs reserved; latency evidence is structured
  logging plus the F0 spike until then.

### Theme 5 — Disproportionate or impossible gates (major)

- Five release rings with SBOM/chaos/WCAG-audit/canary/rollback-rehearsal
  per ring, for a private lab client with zero users (principal P6,
  security P8, flutter P9, delivery P4). **Edit:** three rings
  (deterministic lab, internal live, pilot); invariant-guarding checks
  (secret scan, redaction verification, kill-switch proof) kept as CI
  duties; SBOM/chaos/formal-audit evidence lands once at the pilot gate in
  `avatar-pilot-hardening`.
- Full WCAG 2.2 AA on canvas-rendered Flutter web is not achievable and
  would hard-block every release (flutter P2). **Edit:** Windows is the
  accessibility-qualified surface; web must be screen-reader and keyboard
  operable with a documented exception register; the full web audit moves
  to the web-console change or pilot gate.
- Six kill-switch scopes where two cover every in-scope case (security P9).
  **Edit:** all-session-creation and per-model-profile switches, each with
  optional active-lease revocation.
- Golden-test matrix multiplied into a cross-platform flake generator
  (flutter P7). **Edit:** one pinned CI platform, one bundled font family
  with an RTL face, three viewports plus one long-string/bidi composite;
  accessibility modes verified by semantics assertions.
- Mandatory reproducible Dart codegen from an unnamed schema dialect
  (flutter P1, spec-quality P3, principal P10). **Edit:** schemas declared
  as YAML-serialized JSON Schema draft 2020-12; hand-written bindings
  permitted; canonical fixture conformance is the drift protection.

### Theme 6 — Spec-quality and consistency defects

- Strict validation failed on two requirements whose SHALL sat on a wrapped
  second line (spec-quality P1). **Edit:** fixed; change and full repo pass
  `--strict`.
- Five behavioral rules were stated twice across the two new capabilities,
  inviting drift (spec-quality P5). **Edit:** avatar-client-runtime is
  canonical for behavior/policy; avatar-first-ui restated as presentation
  duties with cross-references.
- F5/F6 acceptance IDs were required but never authored (spec-quality P6).
  **Edit:** moot under the rescope; deterministic acceptance stays, live
  acceptance catalogs belong to the successor change.
- Unverifiable "prove/equivalent" clauses (spec-quality P7). **Edit:**
  replaced with named artifacts or deleted (including the ephemeral-token
  "security review" escape clause).
- The validator was scoped as a protocol simulator duplicating the broker
  test suite (spec-quality P11). **Edit:** validator is schema+fixture
  only; protocol behavior is proven by the reference broker tests.

### Completeness-critic additions

- No cost/quota/metering for a server-paid provider key (critic). **Edit:**
  per-tenant usage records, concurrent-session and duration caps, canonical
  quota-blocked result.
- Domain overlay was a required reference with no defined shape (critic).
  **Edit:** the avatar-first UI profile schema is declared the overlay
  carrier; consent purposes extend the memory-gateway consent profile
  (task 4.3 resolves schema-vs-vocabulary while implementing).
- The contract "release tag" substrate does not exist — the repo has no git
  tags, and `contracts/manifest.yaml` says contract-v1.3 while
  `contracts/CHANGELOG.md` is at contract-v1.6 (critic). **Edit:** pins
  defined as commit SHA plus per-file sha256; **Noted:** the bundle-version
  drift is pre-existing repo debt, reconciled by task 2.8.
- The broker contradicted repo-boundary-governance by planting a deployable
  server in a contracts repo (critic). **Edit:** reference runtime declared
  non-deployable; deployment home decided by `qualify-avatar-live-voice`.
- Broker tenancy topology was undecided (critic). **Edit:** intended
  simplest topology recorded (one broker deployment per domain deployment,
  one project-scoped key each); final decision with the deployment change.
- Extra model profiles (mini/whisper/translate) appeared only in a
  supporting doc; the independent-transcription retention class had no
  producer (critic). **Edit:** all non-`gpt-realtime-2.1` profiles disabled
  pending qualification; transcription retention is a reserved-forbidden
  class.
- Localization burden without a locale set (critic). **Edit:** qualified
  locale is English plus a pseudo-locale fixture for long-string/bidi.

### Security additions kept (cheap, load-bearing)

- WSS reconnect credential rotation via heartbeat responses (security P1).
- Named internal-live authentication mechanism (security P3).
- Per-environment project-scoped provider keys, secret storage only,
  documented manual rotation before internal live (security P4).
- Server-side consent invalidation revokes the lease no later than the next
  heartbeat (security P5).

## Simplification Map

| Dimension | Draft (2026-07-10 am) | Rewrite (2026-07-10 pm) |
| --- | --- | --- |
| Contracts | 12 (AVC-01..12) | 8 (AVC-03/05 absorbed; AVC-09/10 reserved) |
| Concurrency machinery | ~9 mechanisms | 4 (request-id, command-id, conditional revision, epoch+lease) |
| Recovery | streams + chains + replay + digests | single log + snapshot-only |
| Code surface | openxFactory + nonexistent client repo | openxFactory only |
| Tasks | 93 across 13 sections | 24 across 5 sections |
| Release rings / kill switches | 5 / 6 | 3 / 2 |
| Client slices in-change | F1-F6 | none (successor map) |
| Wire state axes | 5 | 4 (presentation mode client-local) |

## Residual Items

- `contracts/manifest.yaml` bundle-version drift (v1.3 vs CHANGELOG v1.6):
  pre-existing debt, reconciled by task 2.8 of this change.
- The supporting documents in this folder describe the pre-review
  12-contract design; they are frozen hash-pinned inputs, and design.md
  states the deltas supersede them where they differ.
- The F0 spike (task 1.1) is the remaining empirical check on the brokered
  flow; its timing evidence feeds AVC-02 before contract freeze.
