# Staged: Avatar Client Lab — offline deterministic Flutter UI lab

Status: draft
Proposed by: implement-avatar-client-lab
Kind: architecture
Summary: An offline, deterministic Flutter avatar client UI lab (F1-F4) that
renders the full avatar-first interaction and authority model from replayed
fixtures, with no live model/voice/WebRTC/broker; the neutral acceptance lives
in openxFactory, the Flutter app in codexFactory `apps/avatar-client-lab/`.
Topics: avatar-client, flutter, ui-lab, deterministic, fixtures, offline, authority, accessibility, repo-boundary
Repository context: openxFactory (neutral acceptance + fixtures); Flutter application realized in codexFactory `apps/avatar-client-lab/`
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

**IN (F1-F4, offline, deterministic — the four acceptance foci are enumerated
in [acceptance-and-tests.md](acceptance-and-tests.md)):** adaptive shell with
five persistent regions + an always-on authoritative status strip; three
client-local presentation modes (conversation/work/review); a generic
service-intake workflow; governed-action cards rendering only canonical intent
and approval state — an authoritative denial rendered as a governed outcome,
distinct from a fail-closed failure; a lightly-animated non-photorealistic
six-state avatar (no lip-sync);
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
- The lab also discharges named deferred/co-owned scenarios across four
  released capabilities (`avatar-client-runtime` ACR-*, `shared-contract-ownership`
  SCO-*, `repo-boundary-governance` RBG-*, and `avatar-first-ui` AFU-*) whose
  released acceptance maps already name `implement-avatar-client-lab` as an
  owner change — the topic is not greenfield; the exact inherited scenario set
  is enumerated in [acceptance-and-tests.md](acceptance-and-tests.md).

See [architecture-and-stack.md](architecture-and-stack.md) for the design
decisions, [open-decisions.md](open-decisions.md) for the six locked decision
records, and [acceptance-and-tests.md](acceptance-and-tests.md) for the F1-F4
acceptance foci, inherited scenario map, and CI gate set.

## Exit (satisfied 2026-07-14)

The staged exit was satisfied as planned: the six blocking decisions were
locked 2026-07-13 (see [open-decisions.md](open-decisions.md)), and on
2026-07-14 all four topic fragments moved with Git history into
`implement-avatar-client-lab`'s `supporting-docs/` (`code_surface:
openxFactory, codexFactory`; `target_release: implemented`),
preserving the staging origin (`openxFactory:staging:avatar-client-lab`). The
change carries the full `avatar-client-lab` spec deltas and the F1-F4 task
list, including the acceptance/evidence map (inherited + new scenario IDs) and
the nine CI gates from [acceptance-and-tests.md](acceptance-and-tests.md).
