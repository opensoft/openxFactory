# Pilot Quickstart: Private connectivity

Status: draft

This is the execution order and acceptance record for an authorized non-production pilot. It uses synthetic tenants A and B, separate Linux client and control hosts, and a mock HTTPS service with one allowed port per boundary.

## Entry

Record the accountable rollout lead, installer and OpsxFactory operators, hosted product and domain owners, and sign-off authority. Record the approved lab region/account and budget, test identity and secret custody, exact releases and policies, rollback authority, and observation windows. Verify test clients can reach the control endpoints and that private application endpoints have no public ingress. Set up probes outside both networks and verify that the positive controls work. At G0 verify deny-by-default on the lab fixture and record the approved candidate pins and baseline policies. At each live gate compare actual releases and policies with the approved record. Verify effective deny-by-default on each new instance before issuing enrollment.

## Rollout and evidence

| Stage | Execute | Evidence and pass condition |
| --- | --- | --- |
| 0. Offline | Validate shared fixtures against each authorized implementation. Test existing unbound installations and retry after a simulated partial write. | Valid requests converge to one result. Invalid, cross-customer, changed-input retries, and secret-bearing records are rejected. |
| 1. Standalone | Provision A and B with no factory subscription. Enroll and revoke devices. Retry provisioning after interrupting the response. Test wrong customer administration, enrollment and traffic, wrong environment, port, route, endpoint and credential. Verify authorized route approval and independently authorized termination on a disposable network. | One instance per boundary, one result per retry, 100% of negative probes denied. Record actual application traffic over direct and forced-relay paths. |
| 2. Local factory | Attach a local factory to A, retry, then detach. Use two approved installations with distinct grants. End one factory subscription and verify only its attachment is revoked. Exercise install-new, connect-existing, no-binding, and invalid or unready binding flows. | Attachment-specific access and revocation work. A retains unrelated devices. Both customer-operated paths succeed without a hosted entitlement. |
| 3. Hosted factory | Use the hosted test profile with a new managed network and authorized reuse of A in separate runs. Verify customer isolation, application authorization, denial of public ingress, failed-step reporting, stable identity on retry, independent detachment, and behavior when private access is unnecessary. Reject missing, stale, unqualified or wrong-domain catalog evidence. | Both managed choices pass and the qualification record is tied to the tested profile. An unauthorized app request is denied even over an allowed network path. |
| 4. Failure drills | Exercise revocation, then service or relay loss and upgrade and restore, then endpoint cutover and rollback. Run the drills serially. Restore a snapshot taken before a known revocation. Verify rollback refuses an expired or revoked prior binding. | Measure against the T003 approved windows. Draft targets are revocation within 5 minutes, restore within 60 minutes from a backup at most 24 hours old, and rollback within 15 minutes. Restored access honors current revocations. B keeps operating during A's drills. |

For revocation, test existing sessions and new connection attempts over direct and relayed paths. Include a peer that has lost control-plane connectivity while its direct path is still available. Probe at least every 10 seconds or more frequently if T003 requires it and record the time from accepted revocation to sustained denial. Use destination or application quarantine if the network cannot meet the window. Record that as a failed network revocation drill until the intended control passes.

## Halt, contain, and resume

Halt new enrollments if any private endpoint is publicly reachable, any cross-boundary or unauthorized probe succeeds, a secret leaks, a retry creates a duplicate, or a target window is missed. Isolate the affected network and preserve redacted evidence. Fence the previous control writer before restore. Apply current revocations before reopening. On endpoint rollback, revoke partial target access and restore the last still-approved binding. Rerun the affected checks and neighboring boundary probes before seeking operator approval to resume.

Record stage, tested release and policy references, actor role, case, expected and observed results, timing, and approved disposition. Store redacted evidence with the owning successor. The rollout lead and affected owners sign off on the lab decision. Each customer-facing launch requires its own authorization and exact profile evidence. Use the required cases and record format in the [pilot evidence contract](contracts/pilot-evidence.md).
