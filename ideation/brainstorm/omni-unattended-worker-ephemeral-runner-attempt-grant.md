# Ephemeral Runners and the Attempt-Authorization Record — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Dispatch reuses the estate's existing GitHub Actions machinery by
starting a just-in-time ephemeral runner INSIDE the disposable sandbox and
destroying it with the sandbox after one job — but the just-in-time
configuration is the CREDENTIAL, not the grant, so a small server-side
attempt-authorization record holds the installation, worker, attempt, policy
epoch, permitted inputs, authorized workflow revision and expiry, and is
correlated to the real GitHub run through the runner name and the job events.
Topics: omni-unattended-worker, ephemeral-runner-attempt-grant, clearing-dispatch,
worker-execution, worker-enrollment, omnigent-lane
Repository context: xFactory-Enrollment-Broker would mint the configuration and
hold the record; xFactory owns dispatch integration; openxFactory owns the
neutral job-envelope and clearing contracts
Captured: 2026-09-05

## Possible feats

- **One attempt per boundary with no new transport** — every property a bespoke
  protocol was wanted for, obtained from software the estate already runs.
- **A durable, non-secret attempt record** — the policy object that a
  secret-bearing launch configuration cannot be.
- **Server-side correlation to the real run** — the authorized attempt matched
  to the actual GitHub job, runner and run attempt from authenticated events.

## Focus

How an authorized attempt reaches a sandbox, and what object actually carries
the authorization once it gets there.

## Proposed model

**The transport.** For each attempt the host manager creates a fresh sandbox and
injects a just-in-time runner configuration minted server-side. The runner
registers, runs exactly one job, and is gone with the sandbox. GitHub's
just-in-time runners perform at most one job and are then removed; disposable
execution state is the complementary control, and the estate already has the
pieces — a broker that mints single-use registration tokens, a clearing-dispatch
door, restricted runner groups with workflow allowlists, artifact-in/artifact-out
lanes and readiness gating.

Properties obtained: one attempt per boundary; no persistence across jobs; no
runner on the Windows host itself; job-scoped credentials bounded by gate 1 and
by the child workflow's permission block; server-side fencing by attempt.

**The correction that matters.** The just-in-time configuration is NOT the
attempt grant. The minting endpoint takes a runner name, a group, labels and an
optional work folder — it does not take an authorized job id, an input digest,
a worker or generation, a policy epoch, or an Omni expiry. "At most one job" is
not the same property as "one specifically authorized job".

**So the server keeps a small authorization record** associating:

```text
installation + generation + worker + attempt + policy epoch + permitted inputs
    <-> authorized repository / workflow revision / run attempt / job
    <-> issued runner id + execution profile + expiry and cancellation state
```

The just-in-time configuration is the CREDENTIAL issued as a consequence of that
record: secret-bearing launch material, not the durable policy object.

**Binding to the real run.** The runner NAME is the attempt id, and the
`workflow_job` event's runner and run/attempt fields are correlated server-side
from authenticated GitHub events or API state — never from a guest's claimed job
id. Reruns, cancellation, duplicate delivery, stale runners and orphan cleanup
are state transitions OF that record. Result acceptance requires the current
authorized attempt; results from superseded attempts are rejected.

**Revocation has a GitHub side.** Revoking participation or the device
certificate does not terminate an established runner session or expire an issued
job token. The server stops minting and stops releasing inputs, requests job
cancellation and runner cleanup through the authorized path, and rejects stale
results. The residual lifetime of provider-issued authority is GitHub's, not
Omni's, and must be recorded rather than wished shorter by an expiry field.

**What mTLS does and does not carry here.** Device mTLS authenticates DELIVERY
of the configuration to the installation. It does not bind the runner session to
the TPM key and does not prove where the job executed. A hostile administrator
can copy launch material or alter execution — compatible with advisory volunteer
results, and with nothing stronger.

**The broker extension is new work.** The broker's current mint interface
exposes registration-token and removal-token minting; just-in-time configuration
generation is an extension needing new response handling, policy binding,
auditing and cleanup semantics. Existing test counts do not verify it.

## Interfaces and boundaries

Consumes: the three gate decisions; the sealed input bundle; the authorized
workflow revision; the host's participation session.

Emits: an attempt-authorization record and, from it, one single-use runner
configuration; state transitions as the attempt proceeds.

Owns: the authorization-to-execution correlation.

Does NOT own: credential REACH inside the job (that is the contribution
repository's permission design), containment (the executor's), or acceptance.

## Alternatives and tensions

- **A bespoke device API and job protocol** — a device gateway, a guest agent, a
  management protocol and a quarantine namespace. It keeps GitHub credentials
  entirely out of the sandbox and gives Omni control over the job's whole
  lifetime; nothing of it exists, and it duplicates dispatch the estate already
  governs. Preserved as the v2 option, taken only if runner-based dispatch
  proves insufficient for a workload the program actually needs.
- **Registering the host itself as a general self-hosted runner.** Rejected: it
  persists across jobs, puts a runner on the Windows host, and makes the
  credential boundary the runner group alone.
- **Grant-in-the-credential versus record-plus-credential.** The first is one
  object and no new storage; it cannot express the bindings that make an attempt
  authorized, which is why it was rejected.
- **Advisory results versus provable execution.** Nothing in this transport
  proves where a job ran. Any future claim stronger than "advisory" needs a
  different mechanism, not a tighter runner policy.

## Open questions

- Where does the attempt-authorization record live — in the broker's schema, or
  in a dispatch-side service?
- What is the attempt expiry, and what happens to an attempt whose GitHub job
  never starts?
- Which authenticated event stream carries `workflow_job`, and who owns its
  delivery and replay handling?
- How are orphaned runners detected and removed when a host disappears
  mid-attempt?
- Does the existing clearing-dispatch door need a new operation for this, or
  does the volunteer lane ride the one it has?

## Relationships

- [Credential reach and the contribution repository](omni-unattended-worker-credential-reach-and-contribution-repository.md)
  — what the issued credential may touch.
- [Authority object lifetimes](omni-unattended-worker-authority-object-lifetimes.md)
  — the parents this attempt nests inside.
- [Three policy gates](omni-unattended-worker-three-policy-gates.md) — the
  decisions this transport carries but never makes.
- [Synthesis: governed dispatch](omni-unattended-worker-synthesis-governed-dispatch.md)
  — the cluster this belongs to.
