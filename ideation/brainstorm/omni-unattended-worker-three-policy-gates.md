# Three Independent Policy Gates: Release, Containment, Acceptance — Brainstorm

Status: brainstorm
Kind: architecture
Summary: The system protects the owner from a job, the factory from an untrusted
machine, and one job from another — three independent problems answered by three
independent server-side decisions (may these inputs be disclosed to this
device's administrator; can this executor contain this code; what evidence is
needed before the output affects a decision), where heartbeats only observe and
server policy alone assigns.
Topics: omni-unattended-worker, three-policy-gates, worker-execution,
clearing-dispatch, omnigent-lane, consent
Repository context: openxFactory owns the neutral gate and job contracts;
codexFactory owns engineering acceptance policy; data owners and project policy
own release
Captured: 2026-09-05

## Possible feats

- **Release as a decision, not an adjective** — an explicit authorization that
  named inputs may be disclosed to a named device's administrator.
- **Containment as a matched capability** — a qualified class checked against a
  job's requirement, replacing inference from a backend's name.
- **Acceptance as an independent act** — volunteer output treated as a candidate
  until governed infrastructure says otherwise.

## Focus

The three questions that must be answered separately, and why collapsing any two
of them produces a wrong answer.

## Proposed model

| Gate | Question | Authoritative source |
| --- | --- | --- |
| 1 Release | May these exact inputs be disclosed to this device's administrator? | The data owner and project policy, on governed infrastructure. Public or explicitly release-approved inputs only for volunteered hardware |
| 2 Containment | Can this executor contain this code and enforce the requested limits? | The executor's qualified containment class, matched against the class the job declares |
| 3 Acceptance | What independent evidence is needed before this output affects a decision? | Domain acceptance policy — codexFactory for engineering — on governed infrastructure |

**They are independent because the failures are independent.** An authentic
device can execute malicious code. A managed host can execute untrusted
pull-request code. A publicly releasable input can contain a hostile script. A
valid signature identifies signed bytes or a submitter, never whether a
computation was correct.

**Facts that are recorded separately and never substituted for one another:**
the installation channel (website versus managed assignment), TPM key
protection, device-management enrollment, who administers the machine, and what
data was authorized. None of these implies another.

**"Synthetic" and "de-identified" are PROVENANCE, not permission.** They
describe where data came from; they do not carry a release decision. Private
engineering work stays governed in this version unless a separate policy
explicitly permits disclosure into a particular contributor's administration
domain.

**Heartbeats observe; policy assigns.** A host reports the classes it believes
it offers, its versions and its capacity. Those are claims, checked against a
qualification record and current policy. Sending a claim over an authenticated
channel makes it attributable, not true.

**Release is broader than the payload.** Gate 1 must approve everything the
issued credentials let the recipient retrieve or change, not just the files
handed over — see
[credential reach](omni-unattended-worker-credential-reach-and-contribution-repository.md),
which is where that turned out to bite.

## Interfaces and boundaries

Consumes: input classification and owner policy; the executor's qualification
record; the job's declared containment requirement; the domain's verification
policy.

Emits: three separate authorizations, each recorded, each revocable, each with
its own audit trail.

Owns: the separation itself.

Does NOT own: the mechanics of any executor, the transport of a job, or the
identity of the machine — each of those is answered elsewhere and none of them
answers a gate.

## Alternatives and tensions

- **A single trust score per host.** Simpler to implement and to explain, and it
  is exactly the collapse this design refuses: a host can be perfectly
  authenticated and completely unable to contain a job, or well isolated and
  ineligible for the input.
- **Trust class as a delivery-profile difference.** The original design treated
  managed and personal as delivery paths for one engine; the review pass
  established that the difference is a TRUST class that constrains job INPUTS,
  which is gate 1 in its first form.
- **Simulation-only volunteer runtime** (the competing proposal in the estate).
  It obtains the same Byzantine posture by restricting the RUNTIME rather than
  the INPUTS. The settled direction keeps the posture and drops the runtime
  restriction; that disposition is owed to the competing document rather than
  assumed.
- **Acceptance cost versus contribution value.** If every volunteer result must
  be fully recomputed at equal cost before it has value, the honest benefit is
  triage or latency, not compute savings. Which workloads have cheap
  verification is therefore part of choosing what to dispatch at all.
- **Replication as evidence.** Useful, but different certificates do not prove
  independence and do not defeat collusion.

## Open questions

- What is the input-classification vocabulary, and who classifies — the data
  owner, the project, or the dispatcher?
- Does gate 1 record a per-attempt authorization, or a standing release for a
  corpus?
- What evidence classes does gate 3 recognize (rerun the gating subset,
  reproduce a build, verify a compact proof, treat as advisory), and who picks
  per job family?
- Where do the three gate decisions live — in the dispatcher, in the broker, or
  in the domain factory — and what record makes them auditable together?

## Relationships

- [Executor ladder](omni-unattended-worker-executor-ladder.md) — what gate 2
  matches against.
- [Credential reach and the contribution repository](omni-unattended-worker-credential-reach-and-contribution-repository.md)
  — why gate 1 is broader than the payload.
- [Ephemeral runner attempt grant](omni-unattended-worker-ephemeral-runner-attempt-grant.md)
  — the transport all three gates constrain.
- [Compute-first model placement](omni-unattended-worker-compute-first-model-placement.md)
  — why model authority never crosses gate 1.
- [Synthesis: governed dispatch](omni-unattended-worker-synthesis-governed-dispatch.md)
  — the cluster this belongs to.
- [Governed job lifecycle](worker-execution-governed-job-lifecycle.md) — the
  estate's existing bounded-job vocabulary.
