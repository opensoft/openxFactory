# Staged: Avatar Client Lab — offline deterministic Flutter UI lab

Status: staged
Kind: architecture
Summary: An offline, deterministic Flutter avatar client UI lab (F1-F4) that
renders the full avatar-first interaction and authority model from replayed
fixtures, with no live model/voice/WebRTC/broker; the neutral acceptance lives
in openxFactory, the Flutter app in a private repo.
Topics: avatar-client, flutter, ui-lab, deterministic, fixtures, offline, authority, accessibility, repo-boundary
Repository context: openxFactory (neutral acceptance + fixtures); Flutter application realized in the private `xfactory-avatar-client` repository
Staging ID: openxFactory:staging:avatar-client-lab
Source: v1 brainstorm 2026-07-13 (six-dimension synthesis); named successor in the avatar-client parallel-workstream plan; supersedes the historical `flutter-avatar-client-ui-lab` exploration
Target capabilities: avatar-client-lab (ADDED)

## Problem

The avatar-client kernel (`contract-v1.7`), the avatar-first UI standard
(`contract-v1.8`), and the non-deployable reference runtime are realized, but
none can be exercised by a person. The reference runtime is a conformance proof,
not a client. To test the avatar — interaction, consent, approval, handoff,
recovery — a real client is required. A live-voice client entangles two questions
that must be separated:

- **Does the interaction work for the user?** — provable deterministically.
- **Can a live model and governed runtime drive it?** — a separate, online,
  credential-bearing question.

This topic scopes only the first: an offline, deterministic Flutter UI lab.

## Capability and delta

- **Target capability:** `avatar-client-lab` (ADDED) — the neutral acceptance
  requirements for the offline, deterministic avatar client: non-production
  boundary, content-addressed contract consumption, fixture-replay determinism,
  re-derives-never-decides authority, the replaceable six-state avatar seam, the
  accessibility baseline, the repository boundary, and the fail-closed deferral
  of voice/WebRTC/Hermes.
- openxFactory owns the neutral acceptance map + conformance fixtures for the
  lab. It does **not** own the Flutter application.

## Scope — in vs out

**IN (F1-F4, offline, deterministic):** adaptive shell with five persistent
regions + an always-on authoritative status strip; three client-local
presentation modes (conversation/work/review); a generic service-intake
workflow; governed-action cards rendering only canonical intent and approval
state; a lightly-animated non-photorealistic six-state avatar (no lip-sync);
accessibility first-class (the eleven avatar-first UI baseline capabilities,
keyboard-only F1-F4, non-color cues, text-only peer renderer); a developer lab
harness compiled out of production.

**OUT (deferred; fail-closed seam only, no live code):** any live model or
provider credential; WebRTC, media plane, brokered SDP, real session broker,
real Hermes control channel; microphone/audio/VAD/push-to-talk; lip-sync;
interactive workflow editing (the separate web console); native iOS/Android;
real i18n beyond a pseudo-locale; web token-exchange handoff; real multi-device
takeover; latency SLOs and production telemetry. Each keeps a fail-closed default
(drafts disabled on web, attachments reference-only, second instance denied,
reserved gate/mode fails preflight) so the later live seam is a clean line.

The successors that lift these deferrals are separate topics/changes:
`qualify-avatar-live-voice` (internal-live provider qualification) and
`avatar-pilot-hardening` (real Hermes/domains/accessibility evidence + pilot).

## Acceptance and tests (summary; authored in full at the proposal gate)

- Content-addressed consumption of `contract-v1.7` + `contract-v1.8` (exact
  commit + per-file SHA-256), fail-closed on drift; a tag-only pin fails.
- Fixture-replay determinism: every canonical session state reached by a
  replayable fixture; identical normalized view-state across repeated replay.
- Client re-derives authority and never decides it: renders canonical
  intent/approval only, never executes a tool call; control-loss fails closed.
- The six-state avatar sits behind a replaceable renderer interface; presentation
  state is derived from authority; control-lost ⇒ `blocked`, never `speaking`.
- Accessibility baseline as gating tests; keyboard-only F1-F4; non-color cues.
- Repository boundary enforced (neutral contracts stay in openxFactory).
- Deferred live capabilities are port interfaces with fixture adapters + a
  fail-closed default.

See [architecture-and-stack.md](architecture-and-stack.md) for the design
decisions and [open-decisions.md](open-decisions.md) for the forks that must be
resolved before this topic is ready to propose.

## Readiness

**Not yet ready to propose** — six open decisions block it (see
[open-decisions.md](open-decisions.md)). The design direction is settled; the
open items are the contested implementation forks (Dart schema validator, web
a11y conformance claim, golden platform, and three others).

## Exit

Create `implement-avatar-client-lab` (`code_surface: openxFactory,
xfactory-avatar-client`; `target_release: implemented`). At the proposal gate,
move this folder's files into that change's `supporting-docs/`, preserving the
staging origin; author the full `avatar-client-lab` spec deltas and the F1-F4
task list in the change.
