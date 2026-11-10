# Data Model: Private connectivity

Status: draft

These logical records define what each owner needs to validate. Exact schemas and storage are successor decisions.

| Record | Key fields and relationships | Custody |
| --- | --- | --- |
| Factory installation | Installation ID, client ID, domain, environment, hosting mode. Zero or one current binding, with a separate candidate during migration. | Factory runtime owner |
| Access request and approval | Request ID, installation, requesting and approving authority references, source identities, destination names or prefixes, ports/protocols, optional separately approved routes, validity and policy revision. An approval applies to the exact scope and boundary. | Customer operator or managed authority |
| Connectivity binding | Binding ID, installation, environment, operator mode, approved HTTPS control endpoint, stable network reference, approval reference, effective policy revision, state, and verification evidence reference. No secret values. | Factory runtime owner |
| Managed entitlement and network | Entitlement reference independent of factory subscriptions. Network ID and customer/environment boundary, dedicated endpoint, instance/policy revision, and protected backup and recovery references. Sharing within a boundary is explicit and approved per installation. | openXsoft.com and install operator |
| Factory attachment | Attachment ID, network, installation, approval, active node references, grant scope, state, revocation record, and operation reference. | Managed service |
| Managed operation | Customer and network scope as applicable, operation type, request fingerprint, retry key, status, stable result reference, and audit reference. | Managed service |
| Hosted profile and evidence | Domain, profile revision, tenant-scoping result, deployment and lifecycle evidence, connectivity applicability and results, release decision reference. | Domain owner and openXsoft.com |

## Lifecycle

- Binding progresses from requested to approved, enrolled, and verified ready. Failed checks leave it unready. Revocation disables readiness. Migration tracks the old and candidate bindings separately and activates the candidate only after verification. Rollback reuses the old binding only while its approval remains valid.
- Network progresses from provisioning to policy verified and active. Recovery fences the old writer and starts in quarantine. Return to active follows identity, policy, and current revocation checks. Termination is a separate action against the entitlement.
- Attachment progresses from authorized to enrolled and active, then revoked. A retry or a restored snapshot cannot transition a revoked attachment back to active. A new attachment requires current authority and a distinct operation.
- Persist operation identity before external effects. Scope the key by authenticated customer, environment, operation type, and immutable target where applicable. Reauthorize each retry. The same scoped key and request fingerprint return the original result or continue reconciliation. A reused key with different inputs fails before mutation.

## Invariants

An installation, binding, attachment, approval, and applicable network must agree on customer and environment. A network reference alone confers no authority. Route approval remains separate from enrollment. Verification and audit contain references and redacted outcomes. Enrollment material stays in credential custody, and current revocations are retained independently of instance snapshots.
