# Staged: Qualify Avatar Live Voice — internal-live provider qualification

Status: staged
Kind: architecture
Summary: The change that turns on real voice after the offline lab — internal-live
qualification of the live WebRTC/broker/media plane behind the `SessionTransport`
port (brokered SDP, direct Flutter<->OpenAI media, `gpt-realtime-2.1` candidate),
adding AVC-09/AVC-10 as the ADDED live contracts and a latency-instrumented
activation gate with canary and rollback.
Topics: avatar-client, live-voice, webrtc, brokered-sdp, gpt-realtime-2.1, latency-slo, activation-gate, provider-qualification, canary-rollback, credential-custody, AVC-09, AVC-10
Repository context: openxFactory owns the neutral live-voice acceptance, the ADDED AVC-09/AVC-10 contract schemas, the `interface-lock.yaml` unreservation, and the acceptance-map/validator updates; the live transport behind `SessionTransport` (`avc_adapters_live`) is realized in the private `xfactory-avatar-client` repo and the session broker in the reference runtime
Staging ID: openxFactory:staging:qualify-avatar-live-voice
Source: named successor in the `avatar-client-lab` staging topic and in the F0 feasibility spec (`specs/002-avc-f0-feasibility`, FR-019/FR-020, User Story 5); draws the live-voice baseline, GPT-Live-1 activation gate, latency requirement, and voice-session topology from `flutter-avatar-client-ui-lab.md`, and the reserved AVC-09/AVC-10 contracts + `interface-lock.yaml` from the archived `2026-07-13-define-avatar-client-contract-kernel`
Target capabilities: avatar-live-voice (ADDED)

The offline lab (`avatar-client-lab`) answered *does the interaction work for the
user* deterministically, against replayed fixtures with no live model. The F0
brokered-call spike (`specs/002-avc-f0-feasibility`) answered a second, narrower
question — *is the OpenAI-brokered WebRTC handshake feasible* — and answered it
only under disposable lab conditions with generated audio and no tenant data.
Neither is a live-use qualification, and F0 says so in its own boundary: its
non-qualification requirements (FR-019/FR-020, User Story 5) reject any attempt to
enable internal-live or production media from F0 evidence alone and name **this**
change as the gate that owns live-profile promotion, production topology, and
formal latency budgets.

This topic scopes that gate — the first time real voice is turned on. It qualifies
the live WebRTC/broker/media plane the lab left behind the fail-closed
`SessionTransport` port, the seam whose fixture adapter (`FixtureScenarioTransport`)
is swapped for a live WebRTC/broker transport with **zero reducer or UI change**.
Concretely it covers brokered SDP (Flutter offer -> authenticated openxFactory
session broker -> server-key Realtime call -> SDP answer released only after
sideband readiness), direct Flutter<->OpenAI WebRTC media after setup, the
`gpt-realtime-2.1` qualification candidate, latency instrumentation with SLOs
derived from a measured baseline, and a promotion/activation gate with canary and
rollback. It also lifts **AVC-09** and **AVC-10** from *reserved* to *defined*,
giving live voice its adapter-descriptor and latency-sample contracts.

The boundary is strict and inherited: deterministic fixtures and live Realtime
behavior exercise the **same** AVC-01..AVC-12 contracts; the live plane adds no
media proxy and no second workflow session; authority stays with Hermes — low
conversational latency never buys a bypass of an authority gate. This is provider
qualification for the internal-live release ring only — not a pilot, and not the
GPT-Live-1 default swap.

## Claims

1. **This change turns on real voice; the lab and F0 deliberately do not.**
   `avatar-live-voice` (ADDED) is the neutral capability that qualifies a live
   provider profile for the internal-live release ring — the ring the kernel
   defined as "live provider qualification plus secret scan, telemetry redaction
   verification, kill-switch proof, and measured latency evidence." F0 proved
   feasibility and stopped there by design; this change carries the feasible
   handshake across the non-qualification boundary F0 refuses to cross.

2. **It is a gated change, not begun at will.** Entry requires three landed
   artifacts: a released, code-signed Flutter client from
   `implement-avatar-client-lab` (its fail-closed `SessionTransport` seam realized
   as `avc_adapters_live`); the released contract kernel pinned at its exact
   commit, per-file SHA-256, and interface-lock digest; and an existing F0 overall
   **PASS** (now recorded) with its threat model accepted. The kernel's
   deterministic-first gate blocks internal-live until deterministic-lab acceptance
   passes, so this change consumes those three as preconditions rather than
   re-proving them.

3. **The media plane lives behind the port, not in a relay.** The live transport
   is brokered SDP then direct Flutter<->OpenAI WebRTC, honoring the kernel
   ordering (sideband verified before the AVC-02 `grant` answer is released;
   authoritative `media_authorized` before answer application or provider-bound
   audio) with **no avoidable xFactory-added latency in the continuous media
   path**. The client never carries a standard API key; the broker holds the
   server key and ephemeral client secrets stay a non-production lab option.

4. **`gpt-realtime-2.1` is the qualification candidate; GPT-Live-1 stays
   reserved-disabled.** The candidate is the profile F0 already pinned (voice
   `marin`, `provider_vad` interaction, `server_vad` turn detection). GPT-Live-1
   has no published API contract and MUST NOT be invented ahead of one; its adapter
   status remains `disabled`, and the UI resolves an opaque `primary_live_voice`
   capability name server-side — never a Flutter `if model == gpt-live-1` branch in
   the widget tree.

5. **AVC-09 and AVC-10 move from reserved to ADDED.** The interface-lock
   `reserved_identifiers: [AVC-03, AVC-05, AVC-09, AVC-10]` loses its two live IDs
   here. AVC-09 (voice adapter descriptor) records adapter/version, provider,
   supported + requested/resolved model profiles, authorization mode, sideband
   readiness, direct-media requirement, region/data controls, and
   experimental/candidate/approved/retired status; AVC-10 (voice latency sample)
   carries sample/session/media-leg/turn identity, monotonic markers, derived
   intervals, direct-vs-brokered reference class, and a reproducible fixture
   reference, with no raw content or secrets. The IDs are never reused.

6. **Latency SLOs are derived from a measured baseline, not guessed.** The kernel
   intentionally left latency as structured logging and deferred the formal AVC-10
   contract and pilot budgets to this change. It instruments the first live
   transport against a direct-provider reference and sets numeric median and tail
   budgets from that measurement; promotion fails when the governed adapter adds a
   material regression. F0's architecture thresholds (sideband p95 <= 3 s,
   first-playable-after-authorization p95 <= 2 s, the five-second revocation bound)
   are inputs, not production SLAs.

7. **Promotion runs through an explicit activation gate backed by canary and kill
   switches.** The gate reuses the eight-condition GPT-Live-1 structure —
   published API contract; approved account/regional/retention/data-control terms;
   proven direct low-latency transport without a proxy; capability contract tests
   for transcript/interruption/tool/sideband/reconnect; passing deterministic +
   domain voice evaluations; latency parity or improvement over the baseline;
   safety/exact-value/consent/handoff/blocked-state evaluations across generic,
   MedxFactory, and LedgerxFactory scenarios; and an opt-in canary with server-side
   rollback. Two server kill switches (all new sessions; per model profile) plus
   lease revocation back the rollback. (Whether all eight bind the internal-live
   qualification of `gpt-realtime-2.1` or only the later GPT-Live-1 default swap is
   an open fork below.)

8. **The deterministic-vs-live boundary and Hermes authority are preserved.** Live
   behavior reuses the same AVC-01..AVC-12 contracts and adds no media proxy and no
   second workflow session. Writes, privileged actions, and regulated decisions
   stay governed even when that adds deliberate task latency; `pre_speech_review`
   remains a scoped, exceptional gate mode; and no live customer audio is shadowed
   to two models without explicit consent and an approved data purpose.

## Open questions

These five forks block promotion; each needs a decision before this topic becomes
a proposal.

1. **Credential custody + spend cap.** F0 read a lab key from `OPENAI_API_KEY` in
   the process environment only, and never as an artifact. Internal-live needs a
   real server-side custody model — where the broker's server key lives (secret
   store, rotation owner, blast radius), how ephemeral client secrets are issued
   and bounded, and an enforced spend/rate ceiling per session and tenant so a
   qualification ring cannot run away on cost. Is the cap a hard broker-enforced
   ceiling that fails the session closed, or a monitored budget with alerting?

2. **Latency budget derivation.** The budgets come from a measured baseline — but
   which percentiles gate (median + p95, or also p99), across which network and
   platform matrix, and what magnitude of regression against the direct-provider
   reference is "material" enough to fail promotion? Does the budget travel
   per-profile inside the AVC-09 descriptor, or is there a single neutral SLO the
   acceptance map enforces?

3. **Scope of the eight-condition activation gate.** The gate as written targets
   promoting **GPT-Live-1** over the current primary. This change instead promotes
   `gpt-realtime-2.1` from disabled to internal-live-qualified. Fork: do all eight
   conditions bind the internal-live qualification of the current candidate, or is
   internal-live a lighter ring with the full eight-condition gate reserved for the
   GPT-Live-1 default swap? Which conditions are hard preflight blockers versus
   canary-time checks?

4. **Data-control and consent for evaluation audio.** The gate forbids shadowing
   live customer audio to two models without explicit consent and an approved data
   purpose, and prefers synthetic and consented recordings first. Fork: what is the
   consent + data-purpose contract for qualification-time evaluation audio
   (retention window, region, opt-in surface), how does it sit against the kernel's
   reserved-forbidden transcription-retention class, and may any real consented
   audio be used at all — or does qualification stay synthetic-only like F0?

5. **Canary cohorting and rollback semantics.** The gate calls for an opt-in canary
   on new sessions with server-side profile rollback. Fork: how is the canary
   cohorted (which tenants/domains, what opt-in surface), what are the
   success/abort criteria, and is rollback automatic on a breached criterion or
   operator-triggered? Does rollback revoke active leases or only block new sessions
   on the withdrawn profile — and how does a mid-qualification abort preserve the
   canonical workflow and audit record?

## Exit

Create `qualify-avatar-live-voice` (`code_surface: openxFactory,
xfactory-avatar-client`; `target_release: implemented`, or a named
internal-live release defined in the aggregation repository at proposal
time). At the proposal gate,
move this folder's files into that change's `supporting-docs/`, preserving the
staging origin; author the full `avatar-live-voice` spec deltas — the AVC-09 and
AVC-10 ADDED contracts, the `interface-lock.yaml` unreservation, the internal-live
activation gate with its kill-switch and rollback requirements, and the measured
latency budgets — plus the acceptance-map and `scripts/validate-avatar-client.py`
updates that unreserve the two IDs. **Not yet ready to propose:** the five open
questions above are blocking, with credential custody + spend cap and the
activation-gate scope the hardest forks. Because this change realizes a live code
surface, it archives only on merged plus green internal-live realization evidence
(the kernel's release-realization rule), never on landing alone.
