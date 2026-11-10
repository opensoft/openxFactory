# Pilot evidence contract

Status: draft

This feature-local contract defines the records accepted by the checker in T002. Owners run their actual verification commands and retain redacted outputs. The checker verifies the record and its dependencies. Acceptance also requires a reviewer to confirm the linked output, tested revision and approval scope. [Tasks](../tasks.md) · [Pilot quickstart](../quickstart.md)

## Records and verification

- Store one JSON record per task at `evidence/TNNN.json`. Use `task` and `verdict` for every record. The closed verdict set is `pass`, `fail` and `blocked`. Only `pass` satisfies a dependency. T001 uses the documented `scopes` mapping and its bootstrap verifier. T002 produces the checker and self-test, and has no evidence record.
- For T003–T021, require an `owner` role, an immutable `decision_ref` or tested `revision_ref` as applicable, `cases` keyed by the IDs below, and redacted source references. Each case carries its `expected` and `observed` outcome, plus an `evidence_ref` identifying the underlying result. For implementation and qualification, also require the owner verification command, exit status, and immutable output reference. A failed owner check fails the task.
- Freeze the expected outcomes by case in the checker. Reject missing, duplicate, substituted or unknown cases, an observation that disagrees with the expected outcome, and placeholder or empty references. Require the applicable allowed connection to succeed before a denial case can count as network evidence. For cross-boundary probes, verify the destination works from its legitimate boundary.
- For live records require `run_ref`, the G0 decision and pin set, and the exact approved candidate revisions tested at that gate. Provisioning outputs record each instance's effective policy revision before enrollment. Later policy mutations link to their authorizing decision. If an applicable runtime pin or baseline changes, require an updated approved G0 record and rerun affected gates.
- Require immutable references to the actual prior gate or drill records. Validate their task IDs, verdicts, revisions, and shared pilot run. G1 requires G0, G2 requires G0 and G1, G3 requires G2, and G4 requires G0–G3 plus all three drill records. Reject evidence from another pilot or a superseded attempt. Blocked and failed attempts stay in the owner’s incident record. A later pass links the resolution and the clean rerun.
- Never record credentials, customer data, raw provider payloads or real device identifiers. Use synthetic identifiers and controlled evidence references. Store rollout and owner sign-off references separately from the cases they accept.

## Required cases

Every ID in a row is required. A grouped case must reference evidence for each of its named subchecks.

| Task | Required case IDs and evidence |
| --- | --- |
| T003 | `lab-scope` approved synthetic fixtures, account, region and budget. `operators` named rollout, sign-off and rollback roles. `custody` approved test credentials and protected evidence. `windows` approved timing, sampling and sustained-denial criteria. |
| T004 | `binding-shape` correct required fields and unbound compatibility. `binding-scope` wrong customer, environment, endpoint and approval denied. `readiness` policy, approval and enrollment required. `credential-custody` no raw secret in binding, logs or support output. `routes` separate scoped approval. |
| T005 | `retries` interrupted and duplicate calls converge to one result. `changed-input` changed payload under a reused key rejected. `reauthorization` unauthorized retries denied. `credentials` expiry and replay denied. `revocation-replay` revoked state cannot return to active. |
| T006 | `offline` shared fixtures pass. `candidate-pins` approved releases and policy baselines recorded. `deny-baseline` fixture policy verified. `probe-control` independent probes, valid controls and external ingress observation ready. |
| T007 | `local-package` dedicated control host and separate client. `local-endpoint` HTTPS identity verified. `local-ops` policy, backup and upgrade procedure qualified. |
| T008 | `new-local`, `existing-local`, `unbound` each pass. `local-scope` only approved destination and port work. `local-unready` invalid endpoint, authorization or policy keeps candidate unready with a redacted error and prior state preserved. |
| T009 | `standalone-entitlement` operate without a factory subscription. `dedicated-instance` separate endpoint, state, keys and policy. `provision-retry` one network after interruption. |
| T010 | `policy-before-enroll`, `managed-credential` and `route-approval` verify grants, single-use short-lived credential scope, and separate routes. `share-scoped` two explicitly approved installations with distinct access. `share-denied` no implicit sharing. `detach` and `subscription-end` revoke only the affected attachment. `terminate` requires separate approval and applies the recorded disposition. |
| T011 | `backup`, `upgrade` and `quarantine-restore` verify per-instance recovery procedures, fencing and reconciliation. |
| T012 | `standalone-a-b`, `retry-one-network`, `enroll-and-revoke` verify both tenants. `cross-customer` denies administration, enrollment and traffic. `wrong-environment`, `wrong-endpoint`, `wrong-credential`, `wrong-port` deny. `routes` unapproved denied and scoped approved route works. `direct`, `relay` record allowed and denied real application traffic. `terminate-isolated` disposable network only, unrelated access preserved. |
| T013 | `local-managed`, `partial-enrollment`, `local-detach`, `migration-rehearsal` verify managed choice, one attachment on retry, independent detach and fenced cutover/rollback. |
| T014 | `new-local`, `existing-local`, `unbound`, `local-managed` pass. `invalid-binding` covers invalid endpoint, unauthorized selection, missing effective policy and denied destination or port. `managed-retry`, `shared-distinct-grants`, `detach`, `subscription-end` verify isolation and surviving access. |
| T015 | `hosted-new`, `hosted-reuse`, `hosted-unbound` verify each selection. `hosted-authorization`, `hosted-failed-step`, `hosted-retry` verify access, unready policy/enrollment failures and stable identities after interruption. |
| T016 | `domain-inventory` accountable owner and profile status for each domain. `profile-evidence` exact domain, profile revision, tenant, deployment, lifecycle and connectivity evidence. Its revision proof uses the explicit `profile_revision` check label, distinct from a scalar repository pin declaration. `catalog-deny` reject absent, stale, unqualified and wrong-domain records. |
| T017 | `hosted-new`, `hosted-reuse`, `hosted-unbound` qualify. `hosted-retry`, `hosted-unready`, `cross-customer`, `public-ingress`, `application-auth`, `hosted-detach` and `catalog-scope` verify negative and lifecycle behavior and exact lab catalog eligibility. |
| T018 | `direct-existing`, `direct-new`, `relay-existing`, `relay-new`, `disconnected-peer` each report time from accepted revocation to sustained denial. A quarantine workaround is a failed network drill. |
| T019 | `service-loss`, `relay-loss`, `upgrade`, `restore-timing`, `backup-age`, `fence-and-quarantine`, `restored-identity-and-grants`, `revocation-survives`, `neighbor-available` document isolated recovery with actual probes. |
| T020 | `cutover-source-revoked`, `rollback-timing`, `partial-target-revoked`, `prior-binding-valid`, `prior-binding-revoked` demonstrate allowed rollback and denial of an expired or revoked prior binding. |
| T021 | `four-paths`, `gate-chain`, `drills`, `incidents-closed`, `owner-signoff` and `rollout-decision` verify the complete evidence set and its decision. |

## Timing and recovery checks

Use elapsed seconds with the T003 approved decision as the source of limits. The draft thresholds are 300 seconds for revocation, 3,600 seconds for restore, 86,400 seconds of maximum backup age, 900 seconds for rollback, and at most 10 seconds between revocation probes. Measure restore from recovery start to verified service, backup age at recovery start, and rollback from initiation to verification of the prior authorized binding. Record actual elapsed values and the maximum observed sampling gap. The approved revocation probe interval must be at most 10 seconds. Reject missing, negative, non-finite or over-limit observations, and fail any case where an existing or new connection remains usable after the approved revocation window. Require separate evidence for tenant B’s availability while A is in recovery. [Pilot quickstart](../quickstart.md)
