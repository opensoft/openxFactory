# Planned production product interfaces

Status: draft
Created: 2026-11-13
Feature: [043-private-connectivity-production](../spec.md)

These are observable requirements across owners. Exact transport, command flags, storage topology and published format/version are selected under accepted owner scope. No new API or production schema is implemented or published here.

## Supported binding and readiness

Preserve the current neutral semantics for installation/customer/environment, customer_operated or managed mode, approved endpoint, stable network, access and separately approved routes. Scope approval, enrollment, effective policy and successful positive/denial verification are all needed before ready.

The supported contract must be published normally before production consumers pin it. The existing feature 040 schema and validator are compatibility research inputs. Schema validation alone does not establish endpoint identity, actual policy or application authority.

Install-new/connect-existing require no hosted subscription credentials. Unbound behavior remains unchanged until opt-in. Managed selection requires a service eligible for that phase/scope plus current entitlement and attachment approval.

## Actual identity, entitlement and custody adapters

Map authenticated identity and current roles to trusted customer/environment authority using the actual approved integration. A caller cannot construct its own authoritative Principal or entitlement result.

Before each sensitive effect/retry and activation, verify current scoped authority. Return only credential/node references through declared custody; enrollment is short-lived and single-use. Reject expired, replayed, revoked or mismatched material. Bindings, logs and support output contain no raw secrets or provider/customer payloads.

## Provider, durable lifecycle and recovery

Provisioning outputs retain stable network/instance/endpoint/state/key/policy identity and establish approved deny-by-default policy before enrollment. Reuse the operation core's original-subject, input-fingerprint and restart semantics. Changed inputs conflict; interrupted effects reconcile without duplicate resources.

Attach/remove operations are scoped per installation and network. Cancellation retries operate on the original approved attachment set, preserving independent network entitlement and unrelated devices. Network termination is separately authorized.

Recovery fences the prior writer, restores in quarantine, reconciles authoritative current revocations and authority, verifies identity/grants/policy/application behavior and authorized neighbors, then rechecks activation authority. Missing current authority blocks activation. Failed endpoint cutover removes partial target access before any currently valid prior binding can return.

## Actual workload onboarding

Replace the synthetic PilotBinder with an approved actual workload integration. Privacy comes from the trusted selected exact profile, not private_required supplied by a caller. A private profile cannot enter the unbound path by changing a Boolean.

Private profiles qualify managed-new and managed-existing. Qualified unbound profiles do not require a private-network subscription. Every path enforces actual application permission independently of network reachability. Partial provisioning, policy, enrollment, network or application failure remains unready with a redacted failed-stage result and retained cleanup identity.

## Profile validation and eligibility

Each selected production profile has its own strict schema and semantic rules, exact definition-time protection and fail-closed required validation/dependencies. Unknown fields/kinds, missing schema dependencies and wrong domain/environment/profile scope must fail rather than warn or skip successfully.

Eligibility derives from exact current candidate/profile bytes/revision, accepted correct-scope Q2/Q4 evidence, fresh owner authority and the applicable bounded offer/wave decision. Caller flags, mutable references, stale evidence, another profile's results or changing the catalog's test literal do not supply production eligibility.

## Release and failure compatibility

Compatible changes follow the normal owner publication/pin process. Material provider, identity, policy, profile, region or artifact changes trigger impact review and affected requalification. Do not silently widen historical lab schemas, allowed boundaries or numeric/role assumptions.

Missing or unverifiable authority/policy is unready. Preserve authorized neighbors during containment, keep current revocations effective, and require reviewed remediation, affected/adjacent reruns and fresh scoped resume authority.
