# Avatar Live-Voice Client Experience Boundary — Brainstorm

Status: brainstorm
Kind: architecture
Summary: The avatar client should present voice state, interruption,
recording, broker failure, privacy, and fallback explicitly while remaining a
replaceable client of the governed avatar contract.
Topics: avatar-live-voice, avatar-client, client-experience, privacy
Repository context: openxFactory avatar client lab and live-voice exploration
Captured: 2026-07-28

## Possible feats

- **Live conversation state model** — idle, connecting, listening, thinking,
  speaking, interrupted, reconnecting, failed, ended, and consent-blocked.
- **Voice privacy controls** — visible capture state, consent, mute, stop,
  retention notice, and deletion request path.

## Focus

This document isolates the user-visible contract for a live avatar voice
session. Media transport and model choice are implementation details unless
they affect state, consent, latency, or recovery.

## Proposed model

The client displays:

- connection and broker state;
- whether microphone or other media is actively captured;
- current listening, processing, and speaking phase;
- interruption and cancellation affordances;
- partial transcript or accessible equivalent when appropriate;
- reconnect, text fallback, and safe termination;
- clear notices for recording, retention, and provider boundaries.

Every action is idempotent where practical. A failed broker call returns the
client to a comprehensible state rather than leaving an ambiguous active
capture.

## Interfaces and boundaries

The UI lab proposal is
[Avatar Client Lab](../../openspec/changes/archive/2026-08-04-implement-avatar-client-lab/proposal.md).
The staged hardening context is
[Avatar Pilot Hardening](../staging/avatar-pilot-hardening/avatar-pilot-hardening.md).
The client experience consumes the brokered contract but does not own provider
credentials or clinical authority.

## Alternatives and tensions

- Rich animation improves presence but can obscure actual voice state.
- Continuous listening reduces turn friction and increases privacy risk.
- Transcript display improves accessibility while retaining extra sensitive
  content.

## Open questions

- Is push-to-talk the safest default for the first live version?
- Which state transitions must be announced accessibly?
- What fallback remains when audio succeeds but animation or transcript fails?

## Relationships

The [brokered voice-path synthesis](avatar-live-voice-synthesis-brokered-path.md)
joins experience requirements to qualification evidence.
