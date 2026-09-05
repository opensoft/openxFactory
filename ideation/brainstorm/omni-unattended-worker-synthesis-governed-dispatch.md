# Synthesis: Governed Dispatch to Untrusted Hardware — Brainstorm

Status: brainstorm
Kind: architecture
Summary: The three gates, credential reach, the ephemeral-runner attempt record,
the heartbeat envelope and compute-first placement combine into a dispatch path
whose emergent property is that a volunteer host receives only what it may see,
runs only what it can contain, and returns only candidates — with the
authorization living in a server-side record and the credential deliberately
demoted to launch material that can be revoked, correlated and outlived.
Topics: omni-unattended-worker, governed-dispatch, three-policy-gates,
credential-reach, ephemeral-runner-attempt-grant, heartbeat-batch-envelope,
compute-first-model-placement, clearing-dispatch, worker-readiness, synthesis
Repository context: xFactory owns dispatch integration; codexFactory owns
acceptance; xFactory-Enrollment-Broker mints and records; openxFactory owns the
neutral clearing, job-envelope and readiness contracts
Captured: 2026-09-05

## Possible feats

- **Volunteer compute inside the estate's existing dispatch door** — no new
  transport, no new scheduler, no runner on anybody's Windows host.
- **A complete exposure statement per attempt** — inputs and credential reach
  approved together before anything is delivered.
- **Candidate outputs with a named acceptance act** — a volunteer result that
  cannot become a required check by claiming to be one.

## Members and their joints

Atomic members:
[three policy gates](omni-unattended-worker-three-policy-gates.md),
[credential reach and the contribution repository](omni-unattended-worker-credential-reach-and-contribution-repository.md),
[ephemeral runner attempt grant](omni-unattended-worker-ephemeral-runner-attempt-grant.md),
[heartbeat batch envelope](omni-unattended-worker-heartbeat-batch-envelope.md),
[compute-first model placement](omni-unattended-worker-compute-first-model-placement.md).

```text
gate 1 release ─┐
gate 2 contain ─┼─> attempt-authorization record ─> JIT config ─> sandbox runner
gate 3 accept ──┘            │                                        │
                             │<── workflow_job events, correlation ───┘
                             v
                     candidate artifacts ──> governed acceptance
```

### Release is not complete until credential reach is priced in

Gate 1 asks what may be disclosed to the device's administrator. The
contribution-repository work is what makes that question answerable at all,
because the job token's scope follows the workflow's REPOSITORY, not the payload.
Put the workflow in a private control repository and gate 1 is silently wrong no
matter how public the inputs were. The public repository, empty default
permissions, sealed-bundle inputs and dispatch-only triggers exist so that "the
inputs are public" and "the credential reaches only public things" become the
same sentence.

### The record is the authority; the credential is only launch material

A just-in-time configuration carries a name, a group and labels — no job, no
inputs, no policy epoch, no generation, no Omni expiry. So the authorization has
to live somewhere else, and once it does, three otherwise-awkward problems
resolve into state transitions of one record: reruns, duplicate delivery and
orphan cleanup. It also makes revocation expressible: stop minting, stop
releasing inputs, cancel the job, remove the runner — while honestly recording
that an already-issued job token's lifetime belongs to GitHub.

### Containment is matched from an observation the server never trusts

Gate 2 reads a qualification record, not a heartbeat. The heartbeat envelope
carries the host's CLAIM about its classes over an authenticated channel, which
makes the claim attributable and no more true. The joint is deliberately
one-way: observation flows up, permission flows down, and the two never meet in
the middle.

### Freshness has to agree across three cadences

The heartbeat batch interval, the readiness staleness threshold and the
participation session's renewal cadence are owned by different components, and
dispatch depends on all three agreeing. Set the batch interval longer than the
staleness threshold and workers flap; set the session renewal shorter than the
batch and hosts churn. No atomic owns this; the cluster does.

### Acceptance is what makes compute-first affordable

Because no model credential rides along and outputs are candidates, gate 3 is
not an optional extra step — it is the mechanism that gives a forgeable result
value. It also sets the economics: where verification costs as much as the work,
the honest benefit is triage and latency, and the workload should probably not
be volunteered at all.

## Emergent behavior

- **A hostile volunteer becomes an availability problem, not a security one.**
  Every path from a modified host into the estate ends at a server-side check:
  the attempt record, the correlation to the real GitHub job, the untrusted
  treatment of logs and artifacts, and acceptance.
- **Revocation acquires two halves that must both be executed.** The platform
  half is immediate; the provider half is a request plus a residual lifetime.
  Only the combination is a revocation story, and only the record makes it
  auditable.
- **Volunteer classes force a contract change in a component nobody thought of.**
  The readiness store's strictly-newer rule and the heartbeat schema's closed
  shape become part of the dispatch design, because a new host class cannot
  report itself without them.
- **Workload selection becomes a security control.** Choosing job families with
  cheap verification is what keeps the whole path worth operating — a product
  decision doing security work.

## Tensions to hold

- **Reuse versus control.** Riding GitHub Actions buys everything that exists
  today and inherits a credential model and a token lifetime the estate does not
  own. The bespoke device API remains the v2 answer precisely because this
  tension may not stay acceptable.
- **A public contribution repository** is what makes token-visible material safe
  and is also an invitation to the exact self-hosted-runner pattern GitHub warns
  about; the trigger and runner-group rules carry the whole weight.
- **Advisory results.** Nothing here proves where a job ran. Every future stronger
  claim needs a new mechanism, not a tighter policy.
- **Batching efficiency versus per-worker truth.** The envelope exists to be
  cheap; the projection exists to keep per-worker freshness. They pull opposite
  ways on every design decision inside it.

## Recombination opportunities

- With [the device trust plane](omni-unattended-worker-synthesis-device-trust-plane.md)
  — the attempt grant is the last object in that plane's nesting.
- With [sandboxed execution](omni-unattended-worker-synthesis-sandboxed-execution.md)
  — the qualification record is what gate 2 consumes.
- With the estate's existing
  [governed job lifecycle](worker-execution-governed-job-lifecycle.md) and
  clearing-dispatch door, which already carry sealed bundles.
- With [Omnigent micro-agents](omnigent-micro-agent-overview.md) — a bounded
  task envelope is the natural shape for what a volunteer attempt receives.

## Open questions

- Where does the attempt-authorization record live, and does the neutral
  job-envelope contract already have a place for it?
- Which of the three cadences is authoritative when they disagree?
- Does gate 1 record a per-attempt authorization or a standing corpus release,
  and how is credential reach expressed in either?
- What is the first job family to dispatch, chosen on verification cost rather
  than on convenience?
