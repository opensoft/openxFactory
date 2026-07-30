## Context

The rule was stated by Brett on 2026-07-24 during the worker-host-app
kickoff: "when an application is released, will codeX hand this to opsX to
run the deployment? for production systems it would seem answer should be
yes... maybe if it is headed to the real qa stack that is under opsx
management then it needs to be handed to opsX for even qa testing" —
confirmed the same day as the managed-subject formulation, with seven
clarifying resolutions. Standing evidence that the rule is already half
real: `OpsxFactory/workflows/deployment.yaml` (production_critical, full
approval stack), `OpsxFactory/docs/aks-administration.md` (the
`cir-opensoft-qa-codexfactory-install` QA precedent dispatching through
`client-infrastructure-execution` → `aks_administration`), and the
`client-infrastructure-request` spec's `execution_binding.mode`
vocabulary (`client_managed | managed_host | opsxfactory_executed`).

The failure the rule prevents is the endpoint disease transposed to
deployment: a domain factory mutating another factory's managed surface
out-of-band creates unmanaged state nobody reconciles, drift with no
evidence, and recovery by archaeology (the 2026-07-22/23 CPC incident).
The service-subject model gives every managed surface exactly one
operator; this boundary keeps deployments from silently creating a
second one. It mirrors the bench-ownership division decided the same
day: codexFactory states requirements, OpsxFactory operates the surface.

## Goals / Non-Goals

**Goals:**

- One neutral routing rule — the managed-subject test — binding every
  actor class, with the environment tier calibrating governance depth
  only.
- Reuse the ratified `client_infrastructure_request` as the crossing; no
  new record kind.
- Credential non-possession as the primary preventive enforcement, with
  grant issuance as the authoritative gate.
- Structural channels (pull-only reconciliation, managed assignment)
  where the surface supports them.
- Detectability: correlation stamping plus a periodic audit in which an
  uncorrelated change is a finding.
- Phased-never-gapped adoption for existing standing admin.

**Non-Goals:**

- Designing break-glass custody, checkout, or the retroactive-request
  policy window (owned by `client-credential-escrow-registry`;
  coordinate, don't fork).
- Building the OpsxFactory QA profile, subject-registry lookup, audit
  job, or ACR namespace scope map here (successor OpsxFactory change).
- Building the codexFactory release exit step here (successor
  codexFactory change).
- A dispatch-time checker service (rejected; see Decision 4).
- Binding domains other than codexFactory now (first-consumer path).

## Decisions

### 1. A new neutral capability, not a fold into the request record

The rule gets its own capability home, `deployment-handoff-boundary`.
The alternative — MODIFIED requirements inside
`client-infrastructure-request` and `release-realization` only — was
rejected because the rule binds PRODUCING factories (codexFactory et
al.), not just the request record's own lifecycle; it needs a home both
sides can cite. Confirmed at this proposal gate from the staging lean.

### 2. The managed-subject test is the sole router

Does the target resolve to a registered subject in the managing
factory's service-subject model (`it-service-subject-model.md`)? Yes →
handoff. No → self-serve. The environment NAME never decides: the QA
AKS stack (`aks-opensoft-platform-qa-01`) is a managed subject, so it
takes the handoff path even for QA testing, while a preview container
on a runner does not, even running production-candidate code. What
varies by tier is approval depth and accepted-risk posture (precedent:
the Spot-eviction risk explicitly ACCEPTED for QA), never the executor,
the request record, or the evidence obligation.

### 3. Every actor class is bound; credentials are the primary teeth

Resolution 1 (2026-07-24): the rule binds factory workers, human
engineers, and CI pipelines alike. A GitHub Actions workflow holding a
kubeconfig, or an engineer with standing admin on a managed scope,
violates the boundary exactly as a worker deploying would. Enforcement
is layered, and the credential layer does most of the preventive work —
you cannot violate a boundary you have no key to cross:

```text
constitutional  Omnigent permission matrix: execute_final_action and
                access_secrets false for every worker    (ratified)
credential      deployment_operator exists only as an OpsxFactory grant;
                producing identities carry zero write RBAC on managed
                scopes; ACR namespace split             (partially real)
structural      pull-only GitOps reconciliation from a governed tree;
                Intune assignment for endpoints         (real for QA)
detective       evidence-correlation audit over stamped changes
                                                        (design only)
governance      deployment workflow approval stack; QA profile with
                calibrated approvals                    (prod ratified)
```

Prose alone enforces nothing; that is why this exits through OpenSpec
into requirements with scenarios and successor realization tasks.

### 4. Grant issuance is the authoritative gate; no checker service

Resolution 3: the mechanical test point is credential issuance — the
managing factory issues a deployment grant only against an accepted
request whose target resolves to a registered subject, so the
subject-registry lookup happens where the key is born. The structural
gate is merge authority on the governed configuration tree. A separate
dispatch-time checker service was rejected: it would be a second
authority to keep consistent, while the grant path already fails closed.

### 5. Correlation is stamped everywhere; the audit is a join

Resolution 4: execution stamps the request's `correlation_id` into
configuration-tree commit trailers, deployment annotations, and endpoint
assignment metadata. The audit becomes a trivial join of observed
changes against accepted requests; any unstamped change is automatically
a finding — which is exactly what makes break-glass and bypass visible.
Finding handling follows the established auto-fixable vs contested
classes.

### 6. Cadenced publication rides one standing request per period

Resolution 5: bench publication mutates the managed ACR and the
`xfactory-workbenches` subject, so it is on the rail; per-build
approvals were rejected as cadence-hostile. The weekly-plus-triggered
rebuild cadence rides one standing approved request per policy period,
each run stamping correlation and digests as evidence.

### 7. Break-glass is a retroactive request; custody stays in escrow

Resolution 6: this capability requires only that a break-glass action be
followed by a retroactive request — correlating the out-of-band change,
with evidence and disposition — within a policy window. Who can break
glass, how credentials are custodied, and the window's length belong to
`client-credential-escrow-registry`.

### 8. Adoption is phased, never gapped

Resolution 2: the rule ratifies at full strength with the target state
explicit. Existing standing admin (the operator's Azure/GitHub owner
rights) is a named, dispositioned exception until the escrow-registry
break-glass checkout is realized and TESTED; then a dated milestone
removes standing assignments. Standing access is never removed before
the emergency path provably works.

### 9. codexFactory is the sole first consumer

Resolution 7: the capability is written domain-neutrally; only
codexFactory realizes now, on the established first-consumer path. Other
domains bind when they grow deployment surfaces. DTN-017
`subject-establishment` already names this seam for its codexFactory
second consumer, where the designing domain and the applying
administrator are different factories.

### 10. The release-realization delta is correlation, not duplication

Realization evidence for a deployment onto a managed subject references
the completed handoff request by correlation identifier; the request
record stays with the executing factory. Note `add-proposal-origin-contract`
also carries a release-realization delta, but it ADDs a different
requirement (origin retention at archive); the two deltas are disjoint
and no ordered-delta reference is required.

## Risks / Trade-offs

- **The rule reads as bureaucracy for QA** → the QA profile calibrates
  approval depth and accepted risk down; only the executor, record, and
  evidence stay constant. The standing-request pattern keeps cadenced
  work friction-free.
- **Grant-issuance gating stalls emergencies** → break-glass exists by
  design, made visible by the retroactive request and the correlation
  audit rather than forbidden into shadow use.
- **Standing-admin strip breaks recovery** → phased-never-gapped: the
  exception stays dispositioned until the checkout path provably works.
- **The audit drowns in findings** → stamping makes correlation the
  default; findings should be rare and either break-glass (retroactively
  correlated) or real bypass. Finding classes reuse doc-health's
  auto-fixable/contested split.
- **Preview environments blur the test** → the threshold leaning
  (exposure to real users or persistence beyond the producing job ⇒
  subject) is recorded; the exact policy lands with the OpsxFactory
  realization.

## Migration Plan

1. Ratify the capability and the release-realization delta (this change).
2. OpsxFactory successor change: QA requirements/validation profile of
   the deployment workflow, subject-registry lookup at grant issuance,
   evidence-correlation audit, ACR namespace scope map (with the
   worker-host-app bench-pipeline design — same registry, same decision).
3. codexFactory successor change: the release exit step emits the
   request draft; any direct deploy path is removed.
4. Escrow-registry coordination: break-glass checkout realized and
   tested, then the dated milestone strips standing admin.
5. Topic exit: one real release crosses the rail end-to-end onto the
   managed QA stack, and the correlation audit runs once with zero
   uncorrelated findings or dispositioned findings only.

Rollback: the capability is doc-only; consumers un-adopt by reverting
their successor changes. The request record, grants, and audit evidence
already produced remain valid history.

## Open Questions

- QA approval calibration: which approvals relax at QA. Leaning: human
  and subject-Hermes approval retained; tenant approval standing via the
  accepted-risk register rather than per-request. Decided in the
  OpsxFactory realization change.
- ACR namespace scope map: which identities may push where (build vs
  deployed/bench namespaces). Realized with the OpsxFactory
  bench-pipeline design from the worker-host-app topic.
- Preview-environment threshold: at what lifetime or exposure a preview
  acquires a subject record. Leaning: exposure to real users or
  persistence beyond its producing job ⇒ subject; exact policy at
  realization.
- Break-glass policy window: how long after an out-of-band action the
  retroactive request must land. Realization detail; the escrow topic
  may set it.
