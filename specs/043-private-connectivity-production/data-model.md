# Logical data model: Production qualification

Status: draft
Created: 2026-11-13
Feature: [043-private-connectivity-production](spec.md)

This is a conceptual coordination model, not a published schema, database migration or new deployment request kind. Existing owner records remain authoritative. Exact formats and new governed readers require C-01 authorization and normal release/compatibility review.

## Owner scope and commissioning decision

An owner scope identifies the accountable human role, canonical repository and inspected revision, exact accepted code/CI/schema/test paths, excluded effects, governing decision, verification commands, validity and release responsibility. A commissioning decision groups only scopes and consumed choices that have actually been approved.

Proposed scope is not accepted scope. Revoked, expired or superseded authority cannot permit new effects. A single person holding multiple roles is represented explicitly in every accepted role/scope; old lab sign-offs do not fill missing production roles.

## Supported candidate set

A candidate identifies exact compatible contract/validator, package, server/client/platform matrix, installer/service/provider/identity integration, policy and actual domain/profile revisions and content digests, plus supported release/provenance references.

A mutable branch/tag, local helper image or draft feature schema alone is insufficient. Candidate identity is frozen for a qualification attempt. Observed artifact/profile/policy drift invalidates affected acceptance; a successor candidate requires impact review and applicable reruns.

## Target execution authority

The target is resolved through the existing managed-subject test. A managed target links to an accepted client_infrastructure_request, governing channel, required approvals, correlation evidence and valid request-scoped grant where the channel requires one. A reviewed governed merge and pull reconciliation does not create an extra push credential.

An unmanaged target links instead to current customer-operator authority and required consent. Neither case inherits execution permission from a candidate release, Q0, a CI result or an accepted gate record alone. Workflow execution completion/readback is distinct from trusted readiness and qualification.

## Binding, network and attachment

Reuse the supported publication of the current binding semantics: installation, customer, environment, operator mode, endpoint, stable network reference, access, separately authorized routes, approval/enrollment/policy/verification and readiness.

A managed network has independent entitlement and dedicated endpoint/state/keys/policy. Each attachment has its own installation, minimum access, enrolled node and revocation identity. Factory cancellation removes only its original attachment subjects; network termination needs its own authority. Unbound operation remains available where the offering/profile has no private requirement.

Ready requires current scope and actual endpoint, enrollment, effective policy and positive/denial verification. A successful network path never grants application permission.

## Durable operation and revocation state

An operation has stable identity, customer/environment/action, immutable original subjects, input fingerprint, current status/result, partial-effect cleanup references and current authorization evidence. A reused key with different inputs conflicts. Restart/retry retains original subjects and rechecks current effect authority.

Current revocation and consumed single-use credential state cannot be rolled back into validity by restoring instance data. A recovery obtains authoritative current decisions before activation; inability to reconcile leaves it quarantined. Cleanup after entitlement loss remains bounded by current revocation/cleanup authority; it does not grant new provisioning or access.

Concurrent lifecycle updates must preserve the newer valid result and enforce the chosen platform's single-writer/fencing model. The current SQLite/locking implementation is an input to qualification, not evidence that an arbitrary replicated deployment is safe.

## Actual domain/profile and release eligibility

A profile identifies its actual domain/workload, definition revision/bytes, environment/customer scope, required access/routes, privacy requirement, ingress and application-authority expectations, lifecycle evidence and governing owner.

Privacy requirements derive from the trusted selected exact profile. Caller flags cannot downgrade a private profile to unbound. Every production definition has strict schema/semantic validation, exact definition-time protection and mandatory validation wiring before it can be qualified.

Eligibility is derived from current exact-profile candidate/evidence and a scoped release/offer decision. It is not a caller-written Boolean or an inherited result from another domain.

## Operating limits and qualification attempt

An approved operating-limit decision names scope, numeric values, units, event anchors, sampling/monitoring-gap rules, minimum observed window, approvers and validity. Numbers must be finite and valid for their field; negatives and missing values are rejected. Zero is accepted only where the approved metric definition permits it.

A run/attempt identifies evidence class, exact candidate/profile, approved customer/environment/target scope, operator authority, expected case registry, actual commands/probes, redacted outputs, incidents and monitoring coverage. Realizations retain failed/blocked attempts and their remediation links; a later pass does not overwrite them.

## Gate decision and evidence relationships

A gate decision identifies Q0–Q5, its precise purpose/scope, prerequisite decisions and immutable evidence dependencies, accountable sign-offs, decision time, validity and disposition. Labels describe capability decisions, not new wire kinds.

Evidence links include content identity, actual command and exit/result, expected/observed subchecks, timestamps/clock anchors, current policy/authority, limit decisions and incident closure. A gate cannot mix source fixtures with deployed observations or substitute another attempt/customer/profile/candidate.

Conceptual dispositions include proposed, accepted, refused, expired, superseded and invalidated. They must be mapped to an owner-approved format before a reader is implemented; writing accepted text is not authorization.

## Offer, expansion and containment

A commercial offer or wave references accepted Q4 evidence, exact eligible candidates/profiles, customer/region/resource/spend bounds and current product/domain/operational authority. Every later wave and every material scope change is evaluated independently.

Containment records affected subjects, preserved authorized neighbors, current revocations, incident evidence, reviewed remediation and required reruns. Resume identifies fresh scoped authority and the earliest affected gate to requalify. A revoked/expired/no-longer-entitled prior binding stays unavailable even when availability is reduced.

## Cardinality and integrity constraints

- One coordinating feature and one executable task list; many owner realization/release records may be referenced.
- One candidate identity per qualification attempt; no mutable silent substitution.
- Each accepted gate has all required prerequisite decisions and matching-scope evidence.
- Each managed customer boundary retains independent state/keys/policy; shared customer installations require explicit distinct attachment/access approval.
- Each actual production profile needs its own protection and qualification; a passed profile does not qualify the directory or another domain.
- Missing/duplicate/unknown cases, stale authority, non-finite measurements, broken positive controls and wrong-scope references fail acceptance.
- Raw secrets, customer payloads and real high-cardinality device identifiers do not enter coordination records; protected custody stores sensitive inputs under references.
