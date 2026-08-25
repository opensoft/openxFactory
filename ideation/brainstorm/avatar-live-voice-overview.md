# Avatar Live-Voice Overview — Brainstorm

Status: brainstorm
Kind: reference
Summary: The avatar live-voice packet proposes a visible, interruptible,
privacy-aware client state model and a replayable evidence harness for
qualifying a brokered conversation path.
Topics: avatar-live-voice, avatar-client, brokered-call, qualification
Repository context: openxFactory avatar client evolution
Captured: 2026-07-28

## Possible feats

- **Qualified avatar live-voice pilot** — governed client state, broker
  integration, deterministic fixtures, empirical runs, privacy controls,
  accessibility, and failure recovery.

## Motivation

The avatar client has contract and UI foundations, while live voice adds
latency, interruption, capture privacy, provider failure, and evidence needs
that cannot be settled by static UI work or one successful call.

## Goals

- Make voice and broker state visible and interruptible.
- Define privacy, consent, retention, and fallback behavior.
- Collect reproducible latency, failure, and cost evidence.
- Test the complete client experience, not transport alone.
- Separate feasibility, qualification, hardening, and production approval.

## Non-goals

- A feasibility run does not approve production deployment.
- The client does not store provider credentials.
- This packet does not select a permanent broker, model, or media provider.
- Avatar presence does not imply domain or clinical authority.

## What the system delivers

The team can run a pinned brokered-call configuration, observe client and
media state, collect timing and failure evidence, evaluate privacy and
accessibility behavior, and issue a qualified disposition with clear limits.

## System model

```text
visible client state + consent
  → brokered media/model path
  → interruption, recovery, and fallback
  → pinned measurements and observer evidence
  → qualification disposition
  → separate pilot hardening or stop decision
```

## Cluster map

- [Qualified Brokered Avatar Voice Path](avatar-live-voice-synthesis-brokered-path.md)
  — joins user-visible behavior to replayable feasibility evidence.

## How it fits

This packet is companion exploration for the active feasibility and client
lab proposals and the staged live-voice and hardening subjects. It does not
rewrite their requirements or tasks.

## Key decisions and open questions

Open choices include first-version interaction mode, qualification thresholds,
retained media, accessible state announcements, provider portability, and the
authority that accepts a pilot.

## Document map

### Synthesis

- [Qualified Brokered Avatar Voice Path](avatar-live-voice-synthesis-brokered-path.md)

### Atomic explorations

- [Live-Voice Feasibility Evidence](avatar-live-voice-feasibility-evidence.md)
- [Avatar Client Experience Boundary](avatar-live-voice-client-experience-boundary.md)

### Proposal and staging context

- [Brokered Call Feasibility](../../openspec/changes/archive/2026-08-09-qualify-avatar-brokered-call-feasibility/proposal.md)
- [Avatar Client Lab](../../openspec/changes/archive/2026-08-04-implement-avatar-client-lab/proposal.md)
- [Qualify Avatar Live Voice](../staging/qualify-avatar-live-voice/qualify-avatar-live-voice.md)
- [Avatar Pilot Hardening](../staging/avatar-pilot-hardening/avatar-pilot-hardening.md)
