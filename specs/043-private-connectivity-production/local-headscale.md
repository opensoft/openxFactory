# Local Headscale production acceptance

Status: draft
Created: 2026-11-13
Feature: [043-private-connectivity-production](spec.md)

This track covers customer-operated Headscale and a local factory's optional selection of Hosted Headscale. Cases are acceptance requirements for future qualification, not completed tests or an executable task list.

### L-01: Install-new and connect-existing without a hosted subscription

Given an authorized customer operator, a supported package/server/client/platform combination and an approved endpoint, install-new and connect-existing both establish the intended binding without hosted subscription credentials. Legitimate required access succeeds, unapproved access is denied, and an unbound installation retains its existing behavior until opt-in. Record both successful and refused cases for the approved matrix.

### L-02: Refuse an unverified endpoint or access result

An invalid or expired endpoint identity, unsupported combination, failed enrollment or ineffective policy keeps the result unready. A reachable endpoint alone is insufficient. Verification never disables TLS identity checks, exposes credentials or treats a failed positive control as an isolation pass.

### L-03: Renew identity and recover a failed endpoint cutover

Qualify identity renewal and approved endpoint migration with real supported clients. A failed migration removes partial access before restoring a prior binding, and only if that prior binding remains currently authorized and entitled. Revoked or expired prior access stays unavailable. Measure renewal, cutover, rollback and observation against approved limits.

### L-04: Protect and recover the instance state

Prove isolated protected writable state, backup age/data-loss limits, supported upgrades and rollback, retained network identity and single-writer fencing. A protected backup is restored in quarantine; current revocations are reconciled before activation. A second writer cannot use the same writable state. Record measured restore/rollback results and still-revoked subjects.

### L-05: Apply the correct authority to a local canary

An unmanaged customer-operated target can enter only its bounded approved canary with accepted staging evidence, required consent, a current authorized customer operator and working monitoring. It requires no managing-factory deployment request or grant. Missing customer consent or authority blocks activation.

A registered managed local target instead requires its accepted client_infrastructure_request and managing-factory execution. A channel requiring a grant needs a valid request-scoped grant. A reviewed merge into the managing factory's governed tree and pull reconciliation require no additional push credential. All other canary conditions still apply.

### L-06: Select a separately eligible managed network

A local factory may select Hosted Headscale only when the service is eligible for that approved phase/scope, its entitlement is current and its attachment/access scope is approved. Retries reconcile the original operation, and failed setup does not widen or reactivate access or alter unrelated bindings. No private attachment is activated from a lab-only provider pass.

## Qualification evidence

Q1 records the approved support matrix, operator/target authority, endpoint and custody ownership, candidate pins and numeric limits. Q2 observes these cases with real clients, including direct and relay paths where applicable, positive/denial controls and authorized-neighbor availability. Q3–Q5 require the local offering's own decisions; hosted selection additionally depends on the managed service's eligible scope. See [rollout gates](rollout-gates.md).
