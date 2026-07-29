# Live-Voice Feasibility Evidence Boundary — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Avatar live-voice qualification should produce replayable evidence
for latency, interruption, media handling, broker behavior, privacy, failure,
and cost without silently becoming a production approval.
Topics: avatar-live-voice, avatar-client, feasibility, evidence
Repository context: openxFactory avatar client and brokered-call exploration
Captured: 2026-07-28

## Possible feats

- **Live-voice qualification harness** — capture scripted and human-observed
  sessions with media timing, broker events, errors, cost, and disposition.
- **Feasibility evidence manifest** — pin client, broker, model, network,
  script, media, and measurement revisions for one run.

## Focus

This document isolates the evidence needed to decide whether a brokered avatar
voice path is feasible. A successful demonstration is not sufficient without
repeatability and visible failure conditions.

## Proposed model

The harness records:

- client, broker, model, codec, and network configuration;
- first-audio, turn, interruption, and recovery latency;
- transcript and media alignment;
- disconnect, retry, cancellation, and partial-response behavior;
- privacy and retention disposition for recorded media;
- resource and provider cost;
- observer notes and acceptance thresholds.

Runs are immutable records. A later qualification decision cites a defined
set rather than the latest demonstration.

## Interfaces and boundaries

The active qualification proposal is
[Brokered Call Feasibility](../../openspec/changes/qualify-avatar-brokered-call-feasibility/proposal.md).
The staged successor context is
[Qualify Avatar Live Voice](../staging/qualify-avatar-live-voice/qualify-avatar-live-voice.md).
This brainstorm does not alter either artifact.

## Alternatives and tensions

- Fully synthetic fixtures improve determinism but miss human conversation
  dynamics.
- Recorded real sessions improve realism and raise consent and retention risk.
- Median latency looks good while tail latency often defines usability.

## Open questions

- Which thresholds are hard gates versus observed tradeoffs?
- What media may be retained in CI evidence?
- How are provider outages distinguished from client defects?

## Relationships

The [Client Experience Boundary](avatar-live-voice-client-experience-boundary.md)
defines what the qualified path must feel like and expose to users.
