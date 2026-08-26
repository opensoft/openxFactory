# Synthesis: Runtime and Authority — Brainstorm

Status: brainstorm
Kind: architecture
Summary: A durable Subject Hermes episode can coordinate many bounded recursive passes and external waits without granting the reasoning controller standing credentials, unbounded runtime, or terminal action authority.
Topics: hermes-recursive-subject-establishment, runtime-authority, durable-establishment-episode, subject-hermes, consent, synthesis
Repository context: openxFactory neutral Hermes runtime, governance, and execution boundary
Captured: 2026-07-30

## Possible feats

- **Governed recursive-establishment runtime** — resume bounded Hermes
  inference against durable episode state while conserving authority across
  child calls, jobs, waits, and consent changes.

## Members and their joints

Atomic members:
[Durable Subject-Establishment Episode](hermes-recursive-subject-establishment-durable-establishment-episode.md),
[Hermes Control and Execution Boundary](hermes-recursive-subject-establishment-hermes-control-and-execution-boundary.md),
and
[Authority, Consent, and Subject Rights](hermes-recursive-subject-establishment-authority-consent-and-subject-rights.md).

```text
subject-establishment mandate
        |
        v
durable Subject Hermes episode
        |
        v
bounded RLM pass
   |             |
   v             v
reference calls  governed work requests
no tools         typed scope and grants
   |             |
   +------> candidate episode transition
                    |
                    v
             admit | wait | stop | escalate
```

### Durability and bounded inference

The episode stores continuity; the model process does not. Every pass receives
a frozen view of authorized episode state and terminates with a trajectory,
spend record, updated frontier proposal, and explicit stop or wait reason.

External waiting is therefore safe and cheap. When a document, clinical
record, correction, or review arrives, an event can trigger a new bounded pass
under the then-current authority rather than resurrecting old credentials or
cached consent.

### Logical ownership and physical execution

Hermes is the root because establishment changes the system's understanding of
the subject. Tool-less reference calls can assist with bounded reasoning.
Omnigent and adapters execute heavy transforms or provider work under ordinary
job envelopes and scoped grants.

This split avoids two failure modes: a long-lived worker becoming the
unreviewed owner of subject memory, and Hermes accumulating unrestricted
parsers, credentials, sandboxes, and external-action powers.

### Live authority over historical trajectory

The trajectory shows what authority justified past work; current execution
must still evaluate live consent, binding, retention, and revocation state.
Historical approval is not a bearer token.

An episode can become degraded when authority changes. Its previously admitted
claims may remain under declared records policy, become unavailable for new
purposes, require redaction, or be removed through the applicable disposition
path.

## Emergent behavior

Together these ideas support a long-running, adaptive subject-establishment
process that remains revocable, budgeted, auditable, and scoped even when the
source estate is incomplete and evidence arrives asynchronously.

## Tensions to hold

- The controller needs enough state to continue intelligently but should not
  receive the entire sensitive episode history on every pass.
- Durable trajectories improve audit and replay but may themselves contain
  sensitive selections and model disclosures.
- Subject-visible transparency must remain understandable without exposing
  secrets or confidential third-party material.

## Recombination opportunities

The runtime can reuse typed context, budget, trajectory, subordinate-task, and
coverage machinery from the
[Governed Recursive Inference Overview](governed-recursive-inference-overview.md).
It can compose with the active Customer/Subject Hermes runtime isolation
contract without changing its exact-binding and default-deny rules.

## Open questions

- Does one neutral episode contract serve subject establishment, audit, and
  maintenance?
- Which episode evidence belongs in protected audit storage versus the
  subject-visible projection?
- What proves that a resumed pass used only authority valid at resume time?

