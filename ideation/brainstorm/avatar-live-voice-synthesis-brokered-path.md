# Synthesis: Qualified Brokered Avatar Voice Path — Brainstorm

Status: brainstorm
Kind: architecture
Summary: A visible client state model and replayable feasibility evidence
combine into a brokered live-voice path that can be qualified before product
hardening or deployment.
Topics: avatar-live-voice, brokered-call, qualification, avatar-client, synthesis
Repository context: openxFactory avatar client and live-voice exploration
Captured: 2026-07-28

## Possible feats

- **Brokered live-voice qualification gate** — compare measured evidence
  against client-state, privacy, interruption, accessibility, and recovery
  expectations.

## Members and their joints

Atomic members:
[Live-Voice Feasibility Evidence](avatar-live-voice-feasibility-evidence.md)
and [Avatar Client Experience Boundary](avatar-live-voice-client-experience-boundary.md).

### The client exposes measurable states

Connection, capture, listening, processing, speaking, interruption, recovery,
and termination states give the harness stable points for latency and failure
measurement.

### Evidence tests experience, not transport alone

Qualification must show that broker and media events produce understandable
client behavior, including privacy notices, accessible state, fallback, and
safe stop.

### Feasibility precedes hardening

An accepted feasibility result may justify a separate implementation and
hardening change. It does not itself authorize production media retention,
provider credentials, or deployment.

## Emergent behavior

The system can make a defensible go, revise, or stop decision using evidence
that reflects the actual user experience rather than an isolated network
benchmark.

## Tensions to hold

- Strong qualification thresholds may exclude useful degraded modes.
- Realistic evidence increases privacy and reproducibility burden.
- Provider-specific tuning can improve performance and weaken portability.

## Recombination opportunities

The packet can use the
[Identity and Custody](identity-custody-overview.md) packet for login,
credentials, and retained media, and the
[Medical Domain](medical-domain-overview.md) packet if a clinical avatar use
case is later governed.

## Open questions

- Who owns the final qualification disposition?
- What evidence is portable across broker or model providers?
- Which degraded states are acceptable for a pilot?
