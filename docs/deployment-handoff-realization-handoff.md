# Deployment-Handoff Realization Handoff

Status: record
Kind: runbook
Ratified by: [add-deployment-handoff-boundary](../openspec/changes/add-deployment-handoff-boundary/proposal.md) (tasks 3.1–3.3)
Repository context: openxFactory
Purpose: the successor-change handoff packets for the ratified
`deployment-handoff-boundary` capability. The capability is neutral and
doc-only; ALL realization lands through these named successor changes in
their owning repositories (repo-boundary governance). Each packet carries
its residual decisions — deliberately deferred at ratification — and the
topic-exit conditions the successors, not the ratifying change, are
accountable for.

Common ground: the managed-subject test is the sole router (environment
tier calibrates governance depth, never the executor); the crossing is a
`client_infrastructure_request` deployment requirements-profile
(`execution_binding.mode: opsxfactory_executed | managed_host`, no new
record kind); credential non-possession is the primary enforcement;
correlation identifiers stamp every touched change surface; break-glass
custody, the checkout realization/test, and the retroactive-request
policy window are OWNED by the `client-credential-escrow-registry` topic
— coordinate, never fork.

## OpsxFactory successor change

1. **QA requirements/validation profile of `deployment.yaml`**: the
   existing `production_critical` deployment workflow gains its QA
   profile — same executor, same request record, same evidence
   obligation; only approval depth and accepted-risk posture differ.
   RESIDUAL DECISION (QA approval calibration), leaning recorded at
   ratification: human and subject-Hermes approval retained; tenant
   approval standing via the accepted-risk register rather than
   per-request (precedent: the Spot-eviction risk explicitly ACCEPTED
   for QA). Decide in this change.
2. **Subject-registry lookup at grant issuance**: the deployment grant
   issues only against an accepted request whose target resolves to a
   registered subject in the service-subject model — the lookup happens
   where the credential is born; no separate checker service exists.
3. **Evidence-correlation audit**: a periodic job joining observed
   changes on managed subjects (configuration-tree commit trailers,
   deployment annotations, endpoint assignment metadata) against
   accepted requests; an uncorrelated change is a first-class finding
   under the established auto-fixable/contested classes — this is how
   break-glass and bypass become visible.
4. **ACR namespace scope map**: which identities push where — producing
   factories hold build-namespace push ONLY; promotion into deployed or
   bench namespaces is the managing factory's act. RESIDUAL DECISION,
   realized together with the worker-host-app bench-pipeline design:
   same registry, same decision — do not decide it twice.
5. **Correlation-stamp conventions**: the concrete stamp formats —
   commit trailers on the governed configuration tree, deployment
   annotations, endpoint assignment metadata — so the audit's join is
   trivial.
6. **Preview-environment threshold** (task 3.3 leaning, decided here):
   a preview surface acquires a subject record — flipping subsequent
   changes to the handoff path — when it gains EXPOSURE to real users
   or PERSISTS beyond its producing job; exact policy values at
   realization.

## codexFactory successor change

1. **The release exit step emits the handoff**: on release completion
   whose target is a registered managed subject, the exit emits the
   `client_infrastructure_request` draft (produce → hand off); the
   producing factory's authority ends at the release artifact, its
   immutable digests, and realization evidence.
2. **No direct deploy path**: any codexFactory path that mutates a
   managed surface directly is removed; producing-factory worker and CI
   identities keep build-namespace push only.
3. **Release-realization evidence carries the correlation identifier**:
   per the modified `release-realization` archive gate, a deployment
   claim with no correlatable accepted request does not count as
   realization evidence.
4. DTN-017 `subject-establishment` alignment: the codexFactory
   new-project second consumer produces handoff-shaped realization
   artifacts on THIS seam (designing domain ≠ applying administrator);
   its change consumes this packet's crossing rather than inventing one.

## Escrow coordination (owned elsewhere)

`client-credential-escrow-registry` owns break-glass custody, the
checkout realization and its TEST, and the retroactive-request policy
window. The boundary's phased-never-gapped adoption holds existing
standing admin as a named, dispositioned exception until that checkout
path provably works; then a dated milestone removes standing
assignments. Standing access is never removed before the emergency path
is proven.

## Topic-exit conditions (tracked on the successors, never here)

Per task 4.3, the ratifying change archives on its artifacts; the TOPIC
exits only when the successors demonstrate, as their own acceptance
evidence:

1. **One real release crosses the rail end-to-end**: a codexFactory
   release emits the request draft, OpsxFactory accepts and executes it
   onto the managed QA stack (`aks-opensoft-platform-qa-01`), the grant
   issues against the registered subject and revokes on completion, and
   the release-realization evidence references the correlation
   identifier.
2. **A clean or fully dispositioned correlation-audit run**: the
   evidence-correlation audit runs at least once over the managed
   surfaces with zero uncorrelated findings, or with every finding
   dispositioned under the established classes.
