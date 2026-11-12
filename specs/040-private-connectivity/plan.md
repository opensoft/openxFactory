# Implementation Plan: Private connectivity for DomainxFactory

**Branch**: `040-private-connectivity` | **Date**: 2026-11-10 | **Spec**: [Feature specification](spec.md)

Status: draft

**Input**: [Ratified add-private-connectivity packet](../../openspec/changes/add-private-connectivity/proposal.md) and the three delivery specs.

## Summary

Introduce one optional runtime binding for local and hosted factories. Deliver a customer-operated Headscale install path and an independent openXsoft.com Hosted Headscale product. Hosted DomainxFactories use that product when private connectivity is required. Prove all four offering paths in a synthetic pilot before qualifying any customer-facing release.

## Technical Context

| Area | Plan |
| --- | --- |
| Languages and interfaces | Use the owning installer and product stacks. Use the neutral repository's existing Python validation and deterministic fixtures where a successor authorizes neutral conformance code. |
| Dependencies | Pin a qualified Headscale release and supported client build in the install owner. Use existing runtime binding and credential custody for enrollment. Use scoped product authorization for managed operations. |
| Storage | Dedicated SQLite, policy, keys, and protected backup per pilot Headscale instance. Persist product entitlement, operations, and attachment records under the product owner's custody. Keep current revocations available independently of the instance backup. |
| Platforms | Dedicated Linux pilot control hosts and separate Linux workload clients in one approved non-production landing zone plus a separate synthetic customer site. Use private application endpoints and HTTPS control endpoints reachable by pilot clients. |
| Qualification | Offline conformance fixtures followed by real-client positive and negative tests, fault injection, restore, and endpoint rollback. [Research](research.md) · [Pilot quickstart](quickstart.md) |
| Scale and targets | Two synthetic customers, one hosted domain profile, one approved private HTTPS service per boundary, and a separate environment-denial fixture. Pilot targets are 5 minutes for revocation, 60 minutes for restore, and 15 minutes for rollback. |

## Constitution Check

| Principle | Before research and after design |
| --- | --- |
| I. Domain-neutral core | openxFactory defines binding and evidence semantics. Domain policy, install implementation, and hosted runtime stay with their owners. |
| II. OpenSpec before implementation | The ratified packet governs this planning handoff. It is a policy-only change. Each successor must record its own authorized code surface and release before runtime implementation. Speckit owns implementation task decomposition. |
| III–IV. Lifecycle and artifact discipline | Planning records are draft and indexed. Proposed interfaces use repo-relative references and secret-free examples. |
| V. Validation | Each owner runs its repository gates and produces deterministic conformance evidence. Cross-owner pilot results record the exact tested revisions and expected and observed outcomes. |
| VI. Releases | A successor publishing neutral contract bytes follows the atomic release policy and allocates its version at realization. Consumers pin the released commit and digests. |
| VII. Authority | Reject unknown or unauthorized bindings and operations. Require verified effective policy before readiness and preserve current revocations across restore. Use redacted evidence. |

## Project Structure

The [data model](data-model.md), [interface contracts](contracts/connectivity-interfaces.md), [pilot quickstart](quickstart.md), and [pilot evidence contract](contracts/pilot-evidence.md) live alongside the [feature specification](spec.md). Phase 0 records the planning decisions in [research](research.md). Phase 1 defines the logical records, interfaces, and pilot checks. Phase 2 hands the delivery sequence to Speckit tasks for executable decomposition.

| Owner | Implementation surface and handoff |
| --- | --- |
| openxFactory | Extend the neutral runtime binding contract and verification semantics via its authorized successor. Start at the [runtime binding plan](../../docs/self-hosted-runtime-binding-plan.md) and reuse the existing credential model. |
| Installer owner | Realize install-new, connect-existing, and managed selection in the factory installer. Evaluate the aggregation's xFactory-Installer as the integration candidate. Confirm the owner and version before assigning code paths. |
| OpsxFactory and install owner | OpsxFactory governs operations. The proposed Headscale-Install surface owns packaging, instance lifecycle, validation, backups, and recovery after its repository boundary is approved. |
| openXsoft.com and domain owners | The product owner assigns repositories for entitlement, managed operations, and hosted onboarding. Domain owners publish access declarations and qualify their hosted profiles. |

## Delivery Sequence

1. **Establish shared semantics.** Freeze the draft interface against the ratified requirements. Prepare fixtures for binding compatibility, tenant scope, readiness, credential custody, idempotency, and revocation. Confirm successor scopes and owners before implementing runtime or evidence tooling. Approve lab authority before any live pilot traffic. Record candidate pins at G0.
2. **Local Headscale.** Qualify install-new and connect-existing with customer-operated policy and no managed entitlement. Add managed selection through the same binding after the standalone managed flow is available. Verify pre-existing unbound installations and failure recovery.
3. **Standalone Hosted Headscale.** Build scoped entitlement, per-boundary provisioning, deny-by-default policy, enrollment and revocation, and backup and restore. Qualify two independent customers without factory subscriptions. Bind and detach a local factory from an existing managed network and verify other access survives.
4. **Hosted DomainxFactories.** Use the shared binding in hosted onboarding. Qualify one pilot domain with new and existing managed networks, plus a hosted profile that requires no private connectivity. Gate each domain release on its own signed-off evidence.
5. **Pilot decision.** Run the [pilot quickstart](quickstart.md) in order. Publish redacted evidence and record the operator and owner decisions before expanding beyond the lab. Commercial rollout and each domain launch require their own acceptance. Keep a domain rollout inventory and admit each profile only after its exact revision qualifies.

## Pilot Release Gates

The rollout owner records pilot approval, participating owners, approved region and budget, qualified versions, and drill windows before running live tests. The pilot halts on cross-boundary access, exposed private ingress, credential leakage, duplicate provisioning, revived access after revocation, or a failed recovery or rollback window. Resume only after remediation and a clean rerun of the affected controls and adjacent isolation tests.

The [merge-preparation record](merge-preparation.md) defines the owner PR landing order and final source/CI validation boundary.
