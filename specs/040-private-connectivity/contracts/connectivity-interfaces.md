# Proposed Connectivity Interfaces

Status: draft

This defines observable interface behavior for successor planning. Each owner selects transport, record version, and exact field names in its approved implementation scope. [Logical records](../data-model.md)

| Interface | Inputs and authority | Outcome |
| --- | --- | --- |
| Verify and activate binding | Installation, environment, selected operator mode and endpoint, stable network reference, access scope and approval, retry reference | Ready only after endpoint and authority verification, enrollment, and effective access tests. Existing unbound installations remain compatible. Failure identifies the stage and leaves the requested binding unready. |
| Provision managed network | Authenticated customer, verified independent entitlement, environment and trust boundary, retry key | Return one stable managed network and its endpoint after baseline deny-by-default policy is verified. Retrying the same request returns the same outcome. |
| Attach and enroll | Authorized customer, installation, eligible network, approved source, destination and port scope, retry key | Create or reconcile one scoped attachment. A shared network requires explicit approval for each installation and separate grants for its approved access. Resolve single-use enrollment material through credential custody. Readiness requires verification of the effective grants. |
| Revoke attachment | Authorized actor, current scoped attachment, reason and retry key | Remove its node access and grants within the accepted window. Return revocation state and evidence. Preserve independently entitled networks and unrelated attachments. |
| Recover network | Authorized operator and scoped recovery decision | Fence the old writer. Restore in quarantine and reconcile identity, grants, and current revocations before activation. |
| Terminate network | Separately authorized network termination and approved disposition decision | Revoke the network’s access and apply its disposition policy without changing another network. Factory cancellation revokes its attachment only. |
| Qualify hosted profile | Domain and profile revisions, tenant scope, deployment and lifecycle evidence, applicable connectivity and ingress tests, owner decision | Publish a per-domain qualification result. A missing, stale, unqualified or wrong-domain profile result prevents customer catalog admission. |

## Failure and compatibility rules

Reject mismatched customer, environment, endpoint, and scope before mutation. Reject expired, replayed, and revoked enrollment and approvals. Treat a missing or unverifiable policy as unready. An interrupted or unknown result is reconcilable by the same scoped operation. Changing inputs under the same retry key returns a conflict.

Evidence records input and policy revisions, case ID, expected and observed result, and a redacted audit reference. The installer and hosted paths consume the same binding semantics. Exact published artifact pins and conformance fixtures are successor deliverables.
