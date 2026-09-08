# The Heartbeat Becomes a Batch Envelope on the Device Channel — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Per-worker heartbeats travel as a versioned batch envelope over the
authenticated device channel, carrying host generation and sequence plus each
worker's own observation, and the server projects them into the existing
per-worker readiness read model — which removes the volunteer write-token
problem without flattening per-worker freshness into one host document, and
requires deliberate extension of a heartbeat schema that today fixes its version
and forbids extra properties.
Topics: omni-unattended-worker, heartbeat-batch-envelope, worker-readiness,
worker-execution, observability
Repository context: Omnigent-Install owns the heartbeat schema and its
publishers; xFactory-Hermes-Install owns the readiness store and its
strictly-newer rule; openxFactory owns the neutral readiness contract
Captured: 2026-09-05

## Possible feats

- **No write token on volunteer hardware** — readiness reported over the channel
  the device already authenticates on.
- **A batch envelope with per-worker semantics** — one connection, many workers,
  each keeping its own observation age.
- **Deliberate schema extension** — new class fields added as a contract change
  with its consumers named, rather than legacy values fabricated to pass
  validation.

## Focus

How a host reports what it is running, without either handing every volunteer a
write credential or destroying the per-worker readiness semantics the platform
already depends on.

## Proposed model

**The envelope.** A versioned batch envelope over the mutual-TLS device channel.
It carries host generation and sequence, and a list of per-worker observations.
The server verifies that every worker in the batch belongs to the authenticated
installation, then PROJECTS each observation into the existing per-worker read
model.

**Per-worker semantics are preserved, deliberately.** A fresh HOST heartbeat
must not make an old WORKER observation look fresh. The envelope must define
whether an omitted worker is unchanged, unavailable or removed, and explicit
retirement records are the honest encoding for the last of those. Replay and
stale generations are rejected without trusting a client clock: server receipt
time and sequence are separate evidence from the worker's reported observation
time.

**Why this replaces the earlier simplification.** An earlier draft folded
per-worker attestations into ONE host document. That loses the per-worker
freshness the readiness store enforces; batching is a TRANSPORT change, and the
read model stays per worker.

**The compatibility surface is bigger than two new fields.** The heartbeat
schema in the estate today fixes `schema_version` to 1, constrains
`runner_group` to a single value, enumerates `host_class` over the existing
managed classes, and sets `additionalProperties: false`; the readiness store
keys on worker id and requires strictly newer observation times. Adding
`executor_class` and `containment_class` and wrapping the payload in an envelope
therefore touches: the schema, its publishers, the forwarding hop, the readiness
store's projection, and the strictly-newer rule's interaction with batching.
Extend those deliberately for the volunteer classes; do not fabricate legacy
values to make validation pass.

**Authentication does not disappear, it moves.** The volunteer no longer needs a
heartbeat write token, but the server's forwarding hop into the readiness
service still needs a scoped service identity and correct authorization. The hop
became invisible, not unauthenticated.

**Observations remain claims.** Reported executor and containment classes are
checked against qualification records and policy. Sending a class over an
authenticated channel makes it attributable; it does not certify containment.

## Interfaces and boundaries

Consumes: authenticated device identity; per-worker local observations; host
generation and sequence.

Emits: projected per-worker readiness records with preserved observation ages;
rejected-replay and stale-generation events.

Owns: the transport shape and the projection rule.

Does NOT own: what readiness MEANS for dispatch, nor the classes it reports.

## Alternatives and tensions

- **Keep per-worker heartbeats with per-worker write tokens.** No contract change
  and no projection logic; it requires distributing a durable write credential to
  volunteer hardware, which the volunteer estate's own rules refuse.
- **One host readiness document replacing the per-worker model.** Simplest
  server-side; loses per-worker freshness and identity, which the review pass
  rejected.
- **Versioned envelope versus in-place schema bump.** A new envelope keeps the
  managed fleet's current publishers working while the volunteer classes arrive;
  it also means two shapes exist at once and something must eventually retire
  one.
- **Batching versus liveness.** A batch is cheaper and coarser. If the batch
  interval is longer than the readiness staleness threshold, workers flap in the
  read model — a real coupling between two numbers owned by different
  repositories.

## Open questions

- What is the batch interval, and how does it relate to the readiness staleness
  threshold and the participation session's renewal cadence?
- Is an omitted worker unchanged, unavailable or removed — and does the answer
  differ between a partial batch and a full one?
- Does the envelope carry a signature distinct from the channel, or is channel
  authentication sufficient?
- Which service identity carries the forwarding hop, and who owns its lifecycle?
- Do the managed-fleet classes migrate to the envelope, or does it serve
  volunteer classes only?

## Relationships

- [Device certificate authentication](omni-unattended-worker-device-certificate-authentication.md)
  — the channel this rides on.
- [Executor ladder](omni-unattended-worker-executor-ladder.md) — the classes this
  reports as observations.
- [Aggregate budget and owner controls](omni-unattended-worker-aggregate-budget-and-owner-controls.md)
  — the durable states a heartbeat reflects but never sets.
- [Synthesis: governed dispatch](omni-unattended-worker-synthesis-governed-dispatch.md)
  — the cluster this belongs to.
- [Governed Worker Execution Overview](worker-execution-overview.md) — the
  estate's existing readiness and evidence vocabulary.
