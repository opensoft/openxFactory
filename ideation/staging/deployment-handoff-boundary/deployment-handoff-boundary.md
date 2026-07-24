# Staged: Deployment Handoff Boundary (the managed-subject test)

Status: staged
Kind: policy
Summary: A single routing rule for who executes a deployment: execution
authority follows management of the TARGET SURFACE, not the environment
tier. If the target is a registered OpsxFactory subject (managed surface
with lifecycle, health, and evidence), the producing factory hands the
release to OpsxFactory as a governed request and OpsxFactory executes —
for production AND for the managed QA stack alike. If the target lives
inside the producing factory's own execution lane (ephemeral CI
containers, per-job workBench instances, torn down with the job, no
subject record), the factory self-serves and no handoff exists. Today the
rule is only implied by OpsxFactory's `deployment` workflow file and the
`cir-opensoft-qa-codexfactory-install` QA precedent; this topic makes it
a ratified neutral requirement with a layered enforcement design.
Topics: deployment, handoff, opsxfactory, codexfactory, managed-subject,
qa-stack, client-infrastructure-request, release-realization, gitops,
credential-contracts, enforcement
Repository context: openxFactory (the neutral routing requirement and its
capability home — see decisions); OpsxFactory (deployment workflow risk
calibration, subject-registry lookup, evidence-correlation audit);
codexFactory (release exit step: produce → hand off, first consumer);
omnigent-install / hermes-install (evidence surfaces where correlation
audits read).
Staging ID: openxFactory:staging:deployment-handoff-boundary
Source: operator conversation 2026-07-24 (Brett Heap, during
worker-host-app kickoff): "when an application is released, will codeX
hand this to opsX to run the deployment? for production systems it would
seem answer should be yes... maybe if it is headed to the real qa stack
that is under opsx management then it needs to be handed to opsX for even
qa testing" — confirmed with the managed-subject formulation. Standing
evidence: `OpsxFactory/workflows/deployment.yaml` (production_critical,
full approval stack), `OpsxFactory/docs/aks-administration.md`
(`cir-opensoft-qa-codexfactory-install`: the codexFactory install surface
on the QA cluster already dispatches through
`client-infrastructure-execution` → `aks_administration`), and the
`client-infrastructure-request` spec's `execution_binding.mode`
(`client_managed | managed_host | opsxfactory_executed`).

## The rule

**A release deployment SHALL be executed by the factory that manages the
target surface.** Concretely, for the engineering domain:

1. codexFactory's authority ends at the release: the built artifact, its
   immutable digests, and release-realization evidence (merged + green).
2. Any act that mutates a surface carrying a registered OpsxFactory
   subject — production or QA — crosses the boundary as a governed
   handoff: a `client_infrastructure_request` (or its deployment-workflow
   specialization) that OpsxFactory approves, executes, validates, and
   holds evidence for.
3. Work inside the producing factory's own execution lane — CI test runs,
   per-job containers on workers, ephemeral state torn down with the job —
   never crosses the boundary. No subject exists, so no request exists.

The decision procedure is the **managed-subject test**: *does the target
resolve to a registered subject in the OpsxFactory service-subject model
(`it-service-subject-model.md`)?* Yes → handoff. No → self-serve. The
environment's NAME (prod/qa/dev) never decides; the QA AKS stack
(`aks-opensoft-platform-qa-01`) is a managed subject, so it takes the
handoff path even for QA testing, while a preview container on a runner
does not, even if it runs production-candidate code.

What varies by tier is not WHO executes but HOW MUCH governance attends
it: risk level, approval depth, and accepted-risk posture calibrate down
for QA (precedent: the Spot-eviction risk on the QA nodepool is
"explicitly ACCEPTED for QA" in `aks-administration.md`), while the
executor, the request record, and the evidence obligation stay constant.

## Why (the failure this prevents)

A domain factory mutating another factory's managed surface out-of-band
is the same disease the worker-host-app topic exists to cure on
endpoints: unmanaged state that nobody reconciles, drift with no evidence
trail, and recovery by archaeology (the 2026-07-22/23 CPC incident). The
subject model gives every managed surface exactly one operator; this rule
keeps deployments from silently creating a second one. It also mirrors
the bench-ownership decision taken the same day (2026-07-24): codexFactory
states requirements, OpsxFactory operates the surface — one consistent
division across benches, worker hosts, and deployments.

## Claims

1. **Execution authority follows subject management.** The managed-subject
   test is the sole routing rule; environment tier only calibrates
   governance depth, never the executor.
2. **The handoff artifact already exists.** The ratified
   `client-infrastructure-request` record is the crossing: durable,
   idempotent, six identity-reference classes, digest-only package refs,
   `execution_binding.mode = opsxfactory_executed` (or `managed_host`),
   closed lifecycle with a trusted-validator verdict. No new record kind
   is needed for v1 — deployments are a requirements-profile of it.
3. **Producing factories hold no deployment credentials.** The preventive
   core: codexFactory identities (workers, CI) possess no credential that
   can mutate a managed surface. `deployment_operator` credentials exist
   only as OpsxFactory grants under `credential-contracts`, issued per
   request and revoked on completion (`revocation_record` is already
   required evidence in `deployment.yaml`).
4. **Managed surfaces admit changes only through governed channels.**
   Where the surface supports it, the channel is structural: GitOps
   pull-only reconciliation (Flux, pinned, self-managed) from an
   OpsxFactory-governed config tree whose branch protection and review
   ownership ARE the external enforcement; Intune assignment for
   endpoints. Push-path mutation is the exception that requires a grant,
   never the norm.
5. **Out-of-band change is detectable, not just forbidden.** Every
   observed change on a managed subject must correlate to an accepted
   request; a change with no correlated request is a first-class finding
   (detection surface: GitOps drift, Azure activity logs, endpoint
   reconcile evidence à la worker-host-app, heartbeat inventory deltas).
6. **QA rides the same rail with calibrated approvals.** Same executor,
   same record, same evidence vocabulary; a QA requirements/validation
   profile relaxes approval depth and accepts documented risks, per the
   existing accepted-risk register pattern.

## Enforcement design (layered — no single mechanism carries it)

| Layer | Mechanism | Mode | Status today |
| --- | --- | --- | --- |
| Constitutional | Omnigent permission matrix: `execute_final_action: false`, `access_secrets: false` — no worker archetype can deploy directly | preventive | ratified (`omnigent-domain-overlay`) |
| Credential | `deployment_operator` exists only as an OpsxFactory grant (credential-contracts); codexFactory CI/worker identities carry zero write RBAC on managed scopes (Azure RBAC assignments, GitHub environment required-reviewers); ACR namespace split — factories push build artifacts to their build repos, only OpsxFactory promotes into deployed/bench namespaces | preventive | partially real (RBAC exists; the namespace-split and grant-issuance discipline need realization) |
| Structural | Managed clusters reconcile pull-only from an OpsxFactory-governed GitOps tree (Flux pinned, `flux-system` self-managed per Amendment 1); deploying = merging into that tree behind branch protection + review ownership; endpoints reconcile via Intune-delivered apps (worker-host-app pattern) | preventive | real for the QA cluster; the "who may merge the GitOps tree" ownership statement needs ratifying |
| Detective | Evidence-correlation audit: periodically join observed changes (Flux revision history, Azure activity log, endpoint reconcile evidence) against accepted request records; uncorrelated change ⇒ finding (doc-health finding-class pattern: auto-fixable vs contested) | detective | design only |
| Governance | `deployment.yaml` approval stack (domain + tenant + subject Hermes + human) at `production_critical`; a QA profile of the same workflow with calibrated approvals + accepted-risk references | corrective/approval | prod workflow ratified; QA profile missing |

The teeth ranking: layer 2 (credential non-possession) does most of the
preventive work — you cannot violate a boundary you have no key to cross;
layer 3 makes the compliant path also the only convenient path; layer 4
catches what leaks around both (break-glass, human operators with
standing access); layer 5 keeps humans accountable for what the machine
can't judge. Prose alone (this document) enforces nothing — that is why
this exits through OpenSpec into requirements with scenarios, validator
hooks, and realization tasks.

## Target capability and delta (leaning — confirm at proposal gate)

- ADDED (openxFactory, neutral) `deployment-handoff-boundary`: the
  managed-subject routing requirement, the no-deployment-credentials
  requirement for producing factories, the out-of-band-detectability
  requirement, and the tier-calibration principle. Small capability, few
  requirements, heavy scenario coverage.
- MODIFIED `release-realization`: realization evidence for a release
  whose `code_surface` deploys to a managed subject SHALL reference the
  completed handoff request (correlation, not duplication).
- OpsxFactory realization change: QA requirements/validation profile for
  the `deployment` workflow; subject-registry lookup at dispatch;
  evidence-correlation audit job; ACR namespace-split policy.
- codexFactory realization change: release exit step emits the request
  draft (produce → hand off) instead of any direct deploy path.
- Alternative shape considered: fold the routing rule into
  `client-infrastructure-request` as a MODIFIED requirement. Rejected as
  leaning because the rule binds PRODUCING factories (codexFactory et
  al.), not just the request record's own lifecycle — it needs a home
  both sides can cite.

## Decisions to take

- Capability home: new `deployment-handoff-boundary` vs MODIFIED
  `client-infrastructure-request` + `release-realization` only (leaning:
  new capability, above).
- QA approval calibration: which approvals relax at QA (leaning: human +
  subject-Hermes approval retained; tenant approval standing via the
  accepted-risk register rather than per-request).
- ACR namespace split enforcement point: registry RBAC scope map — which
  identities may push where (needs the OpsxFactory bench-pipeline design
  from the worker-host-app topic; same registry, same decision).
- Long-lived preview environments: at what lifetime/exposure does a
  "preview" acquire a subject record and flip to the handoff path
  (leaning: exposure to real users or persistence beyond its producing
  job ⇒ subject).

## Open questions

- Where does the managed-subject test evaluate mechanically — dispatch
  time in the request pipeline (subject-registry lookup), pre-merge in
  the GitOps tree (CODEOWNERS as approximation), or both?
- What is the correlation key for the detective audit — request
  `correlation_id` stamped into GitOps commits / deployment annotations /
  Intune app metadata? (Leaning: yes, stamp it; uncorrelatable changes
  are then trivially findable.)
- Does bench publication count as a deployment under this rule? (Leaning:
  yes and it is already conformant — OpsxFactory owns the bench pipeline
  per the 2026-07-24 decision; publishing a bench mutates the managed
  ACR + the `xfactory-workbenches` application_service subject.)
- Break-glass: when a human deploys around the rail in an incident, what
  retroactive record restores correlation (pattern exists in
  client-credential-escrow-registry staging — coordinate, don't fork).
- Do the other domain factories (Medx, Ledgerx, Adx) have deployment
  surfaces at all yet, or does the neutral capability ratify now with
  codexFactory as sole first consumer? (Leaning: sole first consumer;
  that is the normal DTN-ish path.)

## Exit

An openxFactory OpenSpec change (working id
`add-deployment-handoff-boundary`) ratifying the neutral capability +
the `release-realization` delta, followed by the OpsxFactory realization
change (QA profile, audit, registry scope map) and the codexFactory
release-exit realization. The topic archives when (a) the capability is
ratified, (b) one real release crosses the rail end-to-end — codexFactory
release → request → OpsxFactory executes onto the managed QA stack →
validated + evidenced, and (c) the evidence-correlation audit runs once
over the QA cluster with zero uncorrelated-change findings (or findings
dispositioned).
