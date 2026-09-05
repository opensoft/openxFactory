# Compute First: Model Authority Stays on Governed Hosts — Brainstorm

Status: brainstorm
Kind: architecture
Summary: The governed agent keeps its seat and delegates COMPUTE, sending
artifact-in/artifact-out jobs to volunteered hardware on release-approved inputs
exactly as the estate's existing lanes already work — so no organisational model
credential is present on a contributed machine, seat-backed local agents remain a
governed-host profile until unattended provisioning is demonstrated, and a
provider-supported gateway is an option to evaluate rather than a licence to
share a seat.
Topics: omni-unattended-worker, compute-first-model-placement, omnigent,
credential-contracts, worker-execution
Repository context: codexFactory owns the engineering agent lanes and their
acceptance; OpsxFactory and the existing model authority own credential custody;
openxFactory owns the neutral credential contracts
Captured: 2026-09-05

## Possible feats

- **Compute donation without credential donation** — useful contributed work
  from machines that hold no model account at all.
- **Artifact-in/artifact-out as the v1 integration** — reusing how the estate's
  lanes already produce candidate patches and consume revisions.
- **An evaluated gateway path** — if a workload genuinely needs model calls
  inside a job, a provider-supported gateway with per-job scope and spend limits.

## Focus

Where the model session lives when the compute lives somewhere else, and why
that placement is a security decision rather than a deployment preference.

## Proposed model

**The default.** A governed agent — the coding-patch lane on a governed node,
with its seat — produces candidate patches as artifacts. Build, test, search and
bounded transformation jobs go to Omni as artifact-in/artifact-out work on
release-approved inputs. Results are CANDIDATES until the domain's acceptance
re-runs the gating subset on governed infrastructure.

**No new tool adapter is required for v1.** The estate already runs agents this
way: a coding-patch lane emits a candidate patch as an artifact, and build and
test lanes consume a revision and return artifacts. Compute-first is realized as
those jobs, not as a remote shell for the agent. That also means the general
question — can any given agent delegate its tools transparently to a remote
executor — stays OPEN rather than being declared solved by the one example.

**No organisational model credential on volunteered hardware in v1.** The
enrollment work in flight already gives a temporary-estate worker no
authentication profiles; this design keeps that. Prompts and answers on a
contributed machine are visible to its administrator, so a credential there is
exfiltratable and its outputs are forgeable regardless.

**Seat-backed local agents remain a governed-host profile** until an unattended
provisioning and refresh path is DEMONSTRATED for the selected profile. The
estate's current model plane has an interactive sign-in rung; nothing has yet
shown that credential can be provisioned unattended to a second machine, and
whether a provider permits it at all is a question for Brett and the provider,
not for a repository.

**If a workload genuinely needs model calls inside the job**, the option to
evaluate is a provider-supported gateway enforcing job, model, token and spend,
concurrency and expiry limits while provider credentials stay on governed
infrastructure. A gateway must constrain ACTUAL provider usage — a token-budget
field in a local manifest is not a control. Nothing here licenses converting an
existing seat into a shared credential.

**The consequence for the product.** If unattended seat provisioning is not
available, volunteers run non-model work — tests, builds, doc-health sweeps,
searches, simulations — and model-backed lanes stay on governed nodes. That is
a smaller product, and it is still a product; nothing in this design depends on
the provider answer being yes.

## Interfaces and boundaries

Consumes: release-approved inputs; the job envelope; the governed agent's own
existing model access.

Emits: candidate artifacts, quarantined until accepted.

Owns: the placement rule for model authority.

Does NOT own: acceptance policy (gate 3), the transport, or provider commercial
terms.

## Alternatives and tensions

- **Local seat-backed agents on volunteer machines.** The most capable version of
  the product and the one that requires a credential where it cannot be
  protected. Kept as a governed-host profile, not deleted.
- **A remote tool adapter** giving the governed agent transparent remote
  execution — working directory, artifacts, timeouts, cancellation. Proposed in
  the review lineage, not proven; not needed for artifact jobs.
- **A gateway on the volunteer path.** Keeps provider credentials governed while
  allowing in-job model calls; still exposes prompts and answers to the local
  administrator, and needs provider support the estate has not established.
- **Verification economics.** Volunteer compute is worth having where verification
  is cheaper than the work — speculative search, test selection, triage. Where
  every result must be recomputed at equal cost, the honest claim is latency and
  triage, not compute savings. This tension decides which workloads are worth
  dispatching more than any security property does.

## Open questions

- Do provider terms permit an unattended machine-identity flow for the selected
  profile at all?
- Which job families have verification cheap enough to be worth volunteering?
- Does any planned workload actually require in-job model calls, or is the
  gateway a hypothetical need?
- What would demonstrate unattended provisioning and refresh well enough to move
  a seat-backed agent onto a governed CPC profile?

## Relationships

- [Three policy gates](omni-unattended-worker-three-policy-gates.md) — release
  and acceptance, which bound what a volunteer job may see and what its output
  may become.
- [Credential reach and the contribution repository](omni-unattended-worker-credential-reach-and-contribution-repository.md)
  — the other credential class that stays off volunteer hardware.
- [Ephemeral runner attempt grant](omni-unattended-worker-ephemeral-runner-attempt-grant.md)
  — the transport these artifact jobs ride.
- [Synthesis: governed dispatch](omni-unattended-worker-synthesis-governed-dispatch.md)
  — the cluster this belongs to.
- [Omnigent Micro-Agent System Overview](omnigent-micro-agent-overview.md) — the
  estate's bounded-agent vocabulary this placement rule serves.
