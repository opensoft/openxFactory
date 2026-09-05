# Credential Reach and the Public Contribution Repository — Brainstorm

Status: brainstorm
Kind: architecture
Summary: A job's token is scoped to the repository holding its workflow rather
than to the inputs it was handed, so approving a public payload does not bound
what the recipient can retrieve — and Brett's ruling answers that with a
dedicated public repository in opensoft holding only volunteer child workflows,
pinned schemas and a README, with empty default permissions, sealed-bundle
inputs, no organisation secrets, dispatch-only triggers and a runner group that
admits nothing else.
Topics: omni-unattended-worker, credential-reach, contribution-repository,
three-policy-gates, clearing-dispatch, worker-execution
Repository context: openxFactory owns the clearing contract the inputs travel
on; the contribution repository would be a new public repository in the opensoft
organisation, created and named by Brett under the repo-shape conventions
Captured: 2026-09-05

## Possible feats

- **Release policy that covers credentials, not only payloads** — an
  authorization over everything the issued credential can reach.
- **A public contribution repository** — one narrow, releasable surface whose
  token-visible material is safe to expose to a volunteer host.
- **Sealed-bundle inputs over the clearing contract** — so no volunteer job
  needs repository read access at all.

## Focus

The specific way a correct-looking release decision leaks: the payload is
public, and the credential that arrives with it is not scoped to the payload.

## Proposed model

**The defect.** GitHub creates a job token scoped to the repository CONTAINING
the workflow. Its effective permissions and lifetime are separate from the
selected payload, and job execution can read it. So a volunteer job could
receive only a public test archive while running inside a private control
repository with `contents: read`, and its token would then reach repository
content nobody released. "Public inputs plus read-only permissions" is therefore
an INCOMPLETE rule, and the earlier design that relied on it is corrected here.

**The rule.** Approve not just the explicit inputs but everything the issued
credentials allow the recipient to retrieve or change. Artifact and cache
services that issue their own credentials get the same examination; a token
permission block is not a universal switch over every credential in a job.

**Brett's ruling, verbatim: "New public repo in opensoft."** A repository
holding ONLY the volunteer child workflows, pinned job schemas and a README:

- `permissions: {}` by default, with individually justified per-job grants;
- inputs delivered as SEALED BUNDLES through the existing clearing contract, so
  no job needs `contents: read` anywhere;
- no organisation secrets, deployment credentials, package authority or cloud
  OIDC authority granted to it;
- dispatch-only triggers — no pull-request triggers;
- the runner group `xfactory-temp-volunteer-workers` admits ONLY this repository
  and allowlists only its workflows;
- ephemeral just-in-time runners destroyed after one job.

GitHub warns against using self-hosted runners with public repositories, because
anyone who can open a pull request could otherwise run code on them. These
mitigations are the answer to exactly that warning: there are no pull-request
triggers, the runner group admits one repository and an allowlist of workflows,
and the runner is destroyed after a single job.

**Repository creation and naming are Brett's acts**, following the repo-shape
lane's conventions. This document proposes the shape, not the name.

**Adjacent rules that travel with it.** Pin and govern the workflow that
DISPATCHES to these runners; untrusted input must never select a privileged
workflow or widen runner access. Treat uploaded artifacts and logs as untrusted
data regardless of the run's completion colour — including when a governed agent
reads them, since a test log is not an instruction. Only governed verification
promotes an output into a required check, a release or a trusted cache.

## Interfaces and boundaries

Consumes: the release decision from gate 1; the clearing contract's sealed
bundles; the runner-group and workflow allowlist policy.

Emits: the complete credential-exposure statement for an attempt — what the job
token can reach, for how long, and what else was issued alongside it.

Owns: the boundary between "these inputs were released" and "this credential can
reach".

Does NOT own: the runner minting mechanism, the attempt-authorization record, or
result acceptance.

## Alternatives and tensions

- **Run volunteer workflows from an existing private repository** with a
  narrowed permission block. Fewer moving parts and no new repository; it leaves
  the token pointed at private content and depends on every future workflow
  author getting `permissions:` right.
- **A bespoke device API and job protocol** that never issues a provider
  credential into the sandbox at all. It removes this problem completely and
  replaces it with an unbuilt transport; kept as the v2 option in
  [the runner atomic](omni-unattended-worker-ephemeral-runner-attempt-grant.md).
- **Public repository versus internal one.** A public repository is what makes
  the token-visible material safe by construction; it also publishes the shape
  of the volunteer lane and invites the exact self-hosted-runner attack pattern
  GitHub warns about, which is why the trigger and runner-group rules are not
  optional decorations.
- **Sealed bundles versus checkout.** Bundles remove `contents: read` and add a
  packaging step, a size limit and a cache question that a plain checkout does
  not have.

## Open questions

- What is the repository named, and when is it created?
- Which per-job permissions turn out to be genuinely necessary, and who
  justifies each one in review?
- How do artifact upload and cache credentials get scoped for a volunteer job,
  given they are not covered by the workflow permission block?
- Does the clearing contract's sealed bundle already carry everything a build or
  test job needs, or does it need an extension for large inputs?
- What stops a future workflow from being added to the allowlist without the
  same review?

## Relationships

- [Three policy gates](omni-unattended-worker-three-policy-gates.md) — gate 1,
  which this completes.
- [Ephemeral runner attempt grant](omni-unattended-worker-ephemeral-runner-attempt-grant.md)
  — the credential whose reach this bounds.
- [Compute-first model placement](omni-unattended-worker-compute-first-model-placement.md)
  — the other credential that never enters a volunteer job.
- [Synthesis: governed dispatch](omni-unattended-worker-synthesis-governed-dispatch.md)
  — the cluster this belongs to.
