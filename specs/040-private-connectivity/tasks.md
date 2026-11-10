# Tasks: Private connectivity for DomainxFactory

Status: draft

**Inputs**: [Plan](plan.md), [specification](spec.md), [research](research.md), [data model](data-model.md), [interfaces](contracts/connectivity-interfaces.md), [pilot quickstart](quickstart.md), and [pilot evidence contract](contracts/pilot-evidence.md).

## Scope and execution

The worktree coordinates delivery and holds redacted gate evidence. Runtime changes run in the authorized owning successors. T001 records each successor’s authority, repository, file scope, release path and verification command before any implementation starts. An implementation or qualification task below owns its local evidence record. The corresponding successor owns its code and live artifacts. The scope verifier checks the structure of T001. Review the actual authority references before accepting it. Complete a task only after its owner’s checks, review of the referenced evidence, and the listed verification command pass. Record the tested revision, cases, expected and observed results, and evidence references. All times below are proposed lab targets until approved in T003.

## Phase 1: Setup and authority

- [x] T001 [O] Record the approved successor scopes and owning repositories for neutral binding, installer, OpsxFactory operations, Headscale install, hosted product/domain work, and feature evidence tooling. Capture each owner, approval reference, release path, exact successor files and verification command. Resolve the installer, install and hosted repository assignments before dispatching code or tooling work. Record `specs/040-private-connectivity/evidence/T001.json`. — files: `specs/040-private-connectivity/evidence/T001.json` — verify: `python3 -c 'import json; from pathlib import Path; p=json.loads(Path("specs/040-private-connectivity/evidence/T001.json").read_text()); keys=("neutral_binding","installer","ops","headscale_install","hosted_product","hosted_domain","evidence_tooling"); fields=("owner","repository","approval_ref","release_path","file_scope","verify"); assert p["task"]=="T001" and p["verdict"]=="pass" and set(p["scopes"])==set(keys) and all(all(isinstance(p["scopes"][k][f],str) and p["scopes"][k][f].strip() for f in fields) for k in keys)'`
- [x] T002 [O] Implement the authorized pilot evidence checker and its self-tests from the fixed case catalogue and evidence contract. Test missing and substituted cases, missing upstream gates, mismatched revisions, placeholder references, over-limit timings, and wrong approval scope. Keep the checker confined to validating redacted evidence for this feature. Requires T001. — files: `specs/040-private-connectivity/verify-evidence.py`, `specs/040-private-connectivity/tests/test_verify_evidence.py` — verify: `python3 -m unittest discover -s specs/040-private-connectivity/tests -p test_verify_evidence.py`
- [x] T003 [O] Record the pilot lead, sign-off and rollback authority, synthetic tenants A and B, generic hosted profile, separate lab networks and hosts, approved account, region and budget, test identity custody, and accepted drill windows and observation intervals. G0 records the actual candidate pins before pilot traffic. Requires T002. Record `specs/040-private-connectivity/evidence/T003.json`. — files: `specs/040-private-connectivity/evidence/T003.json` — verify: `python3 specs/040-private-connectivity/verify-evidence.py --task T003 specs/040-private-connectivity/evidence/T003.json`

## Phase 2: Shared foundation

- [x] T004 [O] Have the authorized successor implement the neutral runtime binding and qualify conformance. Prove optional binding compatibility, exact customer/environment/scope, separate route approval, effective-policy readiness, and reference-only credential custody. Record released version or approved pre-release artifact and consumer pins. Requires T002. Record `specs/040-private-connectivity/evidence/T004.json`. — files: `specs/040-private-connectivity/evidence/T004.json` — verify: `python3 specs/040-private-connectivity/verify-evidence.py --task T004 specs/040-private-connectivity/evidence/T004.json`
- [x] T005 [O] Run synthetic fixture checks for interrupted provisioning and enrollment, duplicate requests, changed input under the same key, unauthorized retries, expired and replayed credentials, and restored revocations. Prove one stable result and fail-closed denial. Real adapters must pass their owning conformance checks before their live gates. Requires T004. Record `specs/040-private-connectivity/evidence/T005.json`. — files: `specs/040-private-connectivity/evidence/T005.json` — verify: `python3 specs/040-private-connectivity/verify-evidence.py --task T005 specs/040-private-connectivity/evidence/T005.json`
- [x] T006 [O] Run G0. Require offline binding and fixture passes, approved lab entry, a complete candidate pin and policy baseline list for the selected pilot, working independent probes, and verified deny-by-default policy in the lab fixture. At each live gate compare the running releases and policy baseline to this approved record and verify deny-by-default policy on each new instance before enrollment. Requires T003, T005. Record `specs/040-private-connectivity/evidence/T006.json`. — files: `specs/040-private-connectivity/evidence/T006.json` — verify: `python3 specs/040-private-connectivity/verify-evidence.py --task T006 specs/040-private-connectivity/evidence/T006.json`

## Phase 3: US1 customer-operated Headscale (P1)

**Independent test**: Install locally and connect to an existing customer-operated server without a Hosted Headscale subscription. Prove an unbound installation remains compatible.

- [x] T007 [P] [US1] [O] Have the install owner implement and qualify local Headscale packaging on a dedicated Linux control host with separate clients. Record version pins, HTTPS endpoint checks, policy initialization, upgrade and backup instructions. Requires T004. Record `specs/040-private-connectivity/evidence/T007.json`. — files: `specs/040-private-connectivity/evidence/T007.json` — verify: `python3 specs/040-private-connectivity/verify-evidence.py --task T007 specs/040-private-connectivity/evidence/T007.json`
- [ ] T008 [US1] [O] Have the installer owner implement and qualify install-new and connect-existing without hosted credentials. Verify the approved destination and port and at least one denied destination or port before readiness. An invalid endpoint, unauthorized enrollment, or unverified policy leaves the candidate unready, reports the failed step without leaking secrets, and preserves an existing approved or unbound installation. Requires T007. Record `specs/040-private-connectivity/evidence/T008.json`. — files: `specs/040-private-connectivity/evidence/T008.json` — verify: `python3 specs/040-private-connectivity/verify-evidence.py --task T008 specs/040-private-connectivity/evidence/T008.json`

## Phase 4: US2 standalone Hosted Headscale (P1)

**Independent test**: Operate two isolated networks without factory subscriptions and test provisioning replay, enrollment, revocation and recovery.

- [x] T009 [P] [US2] [O] Have the hosted product owner implement and qualify independent openXsoft.com entitlements and scoped managed provisioning. A customer without a factory subscription must get one network per boundary, isolated endpoint, keys, state and policy, and a stable response after an interrupted request. Requires T004. Record `specs/040-private-connectivity/evidence/T009.json`. — files: `specs/040-private-connectivity/evidence/T009.json` — verify: `python3 specs/040-private-connectivity/verify-evidence.py --task T009 specs/040-private-connectivity/evidence/T009.json`
- [ ] T010 [US2] [O] Have the service owner implement and qualify enrollment, separate route approval, and independent attachment and entitlement lifecycles. Prove explicit policy before enrollment, scoped short-lived single-use credentials, and individually scoped access for two explicitly approved factories on the same network. Reject sharing without approval. Exercise manual detachment, factory-subscription cancellation, and separately authorized network termination and data disposition without touching another network. Requires T009. Record `specs/040-private-connectivity/evidence/T010.json`. — files: `specs/040-private-connectivity/evidence/T010.json` — verify: `python3 specs/040-private-connectivity/verify-evidence.py --task T010 specs/040-private-connectivity/evidence/T010.json`
- [ ] T011 [P] [US2] [O] Qualify per-instance backup, upgrade and quarantined restore procedures with OpsxFactory and the install owner. Require fencing of the previous writer and replay of current revocations before activation. Requires T009. Record `specs/040-private-connectivity/evidence/T011.json`. — files: `specs/040-private-connectivity/evidence/T011.json` — verify: `python3 specs/040-private-connectivity/verify-evidence.py --task T011 specs/040-private-connectivity/evidence/T011.json`
- [ ] T012 [US2] [O] Run G1. Provision A and B without factory subscriptions and interrupt and retry provisioning. Verify scoped device enrollment and revocation, explicit cross-customer administrative denial, environment separation, endpoint and credential denial, unapproved and separately approved routes, and allowed and denied application traffic over direct and forced-relay paths. Use a disposable network for termination and prove the other entitlement and networks survive. Requires T006, T010, T011. Record `specs/040-private-connectivity/evidence/T012.json`. — files: `specs/040-private-connectivity/evidence/T012.json` — verify: `python3 specs/040-private-connectivity/verify-evidence.py --task T012 specs/040-private-connectivity/evidence/T012.json`

## Phase 5: US1 local factory with Hosted Headscale (P1)

**Independent test**: Use an existing managed network from a local factory. Retry and detach the attachment while unrelated access survives.

- [ ] T013 [US1] [O] Have the installer owner implement and qualify local factory selection of an authorized managed network, retry after partial enrollment, detach, and endpoint cutover and rollback. Preserve a previous approved binding until verified cutover and revoke partial target access on rollback. Requires T008, T010. Record `specs/040-private-connectivity/evidence/T013.json`. — files: `specs/040-private-connectivity/evidence/T013.json` — verify: `python3 specs/040-private-connectivity/verify-evidence.py --task T013 specs/040-private-connectivity/evidence/T013.json`
- [ ] T014 [US1] [O] Run G2. Verify install-new, connect-existing and unbound behavior, including invalid endpoint, unauthorized managed selection, ineffective policy, and one denied destination or port. Attach a local factory to A’s existing network, retry, and verify other devices retain access after detach. Exercise two approved installations sharing A with distinct grants, and prove factory-subscription cancellation revokes only the affected attachment. Use synthetic fixtures and redacted results. Requires T006, T012, T013. Record `specs/040-private-connectivity/evidence/T014.json`. — files: `specs/040-private-connectivity/evidence/T014.json` — verify: `python3 specs/040-private-connectivity/verify-evidence.py --task T014 specs/040-private-connectivity/evidence/T014.json`

## Phase 6: US3 hosted DomainxFactories (P2)

**Independent test**: Qualify the generic hosted profile with both managed network choices and with a deployment that requires no binding. Test application authorization and private ingress.

- [ ] T015 [US3] [O] Have the product owner implement and qualify hosted onboarding for a new managed network, authorized reuse and no required binding. Verify entitlement, private service authorization and failed-step reporting. An interrupted request must reconcile the same installation, network and attachment, and policy or enrollment failure must leave the candidate unready without public ingress. Requires T004, T010. Record `specs/040-private-connectivity/evidence/T015.json`. — files: `specs/040-private-connectivity/evidence/T015.json` — verify: `python3 specs/040-private-connectivity/verify-evidence.py --task T015 specs/040-private-connectivity/evidence/T015.json`
- [ ] T016 [P] [US3] [O] Have the domain and product owners implement the per-domain qualification and catalog gate, including the strict profile schema, exact definition-time protection and required validation wiring ratified in codeXfactory/codexFactory#578. Track each DomainxFactory with an accountable owner and profile status. Require evidence tied to the exact domain profile revision for deployment, customer scope, lifecycle, applicable connectivity and ingress, and owner approval. Reject missing, stale, unqualified or wrong-domain evidence. Requires T004. Record `specs/040-private-connectivity/evidence/T016.json`. — files: `specs/040-private-connectivity/evidence/T016.json` — verify: `python3 specs/040-private-connectivity/verify-evidence.py --task T016 specs/040-private-connectivity/evidence/T016.json`
- [ ] T017 [US3] [O] Run G3. Exercise hosted onboarding with new and existing managed networks, no private access requirement and interrupted onboarding. Verify failed-step reporting, unready status after failed policy or enrollment, denial of cross-customer and public access, application denial despite an allowed network path, and detachment with continued independent network use. Confirm only the qualifying synthetic profile is eligible in the lab catalog. Requires T014, T015, T016. Record `specs/040-private-connectivity/evidence/T017.json`. — files: `specs/040-private-connectivity/evidence/T017.json` — verify: `python3 specs/040-private-connectivity/verify-evidence.py --task T017 specs/040-private-connectivity/evidence/T017.json`

## Phase 7: Pilot failure drills and release decision

- [ ] T018 [O] Measure network revocation on established and new sessions over direct and forced-relay paths. Include a peer that loses control-plane access while its direct path persists. Measure from accepted revocation to sustained deny using the approved limits and sampling from T003. Quarantine when the network misses its limit and record a failed network drill. Requires T017. Record `specs/040-private-connectivity/evidence/T018.json`. — files: `specs/040-private-connectivity/evidence/T018.json` — verify: `python3 specs/040-private-connectivity/verify-evidence.py --task T018 specs/040-private-connectivity/evidence/T018.json`
- [ ] T019 [O] Drill service and relay loss, a qualified upgrade and restore of A from a backup predating a known revocation. Fence the previous writer, keep the restore in quarantine, reconcile current revocations, and verify network identity, approved grants and prior revocation before activation. Measure restore and backup age against T003, then verify B remained available. Requires T018. Record `specs/040-private-connectivity/evidence/T019.json`. — files: `specs/040-private-connectivity/evidence/T019.json` — verify: `python3 specs/040-private-connectivity/verify-evidence.py --task T019 specs/040-private-connectivity/evidence/T019.json`
- [ ] T020 [O] Drill successful endpoint cutover and forced rollback after restore. Prove source access is revoked after cutover and partial target grants are revoked on rollback. Restore only the still-authorized prior binding and verify that an expired or revoked prior binding stays unavailable. Measure rollback from operator initiation against T003. Requires T019. Record `specs/040-private-connectivity/evidence/T020.json`. — files: `specs/040-private-connectivity/evidence/T020.json` — verify: `python3 specs/040-private-connectivity/verify-evidence.py --task T020 specs/040-private-connectivity/evidence/T020.json`
- [ ] T021 [O] Record G4 and the pilot decision. Require immutable references to G0–G3 and all drill evidence, the rollout lead’s decision and affected owners’ sign-offs. Confirm four offering paths passed and all incidents and failed probes are closed with rerun evidence. A lab sign-off allows consideration of expansion. Each commercial release still needs its own authorization and profile evidence. Requires T018, T019, T020. Record `specs/040-private-connectivity/evidence/T021.json`. — files: `specs/040-private-connectivity/evidence/T021.json` — verify: `python3 specs/040-private-connectivity/verify-evidence.py --task T021 specs/040-private-connectivity/evidence/T021.json`

## Dependencies and parallel execution

- Shared conformance T004 unlocks local packaging T007 and managed provisioning T009. The local customer-operated path through T008 is the first usable increment.
- After T009, the lifecycle qualification T010 and recovery qualification T011 can proceed independently in their owning scopes. Hosted profile evidence T016 can proceed after T004 and in parallel with hosted onboarding T015 once T010 passes.
- G0 gates all live pilot work. G1 gates G2, and G2 gates G3. The hosted product and installer teams may qualify independently before their live gates using offline fixtures or disposable environments authorized by their successors. Shared pilot traffic starts after G0.
- G3 unlocks the revocation drill. Run revocation, restore and migration serially against tenant A in that order. G4 needs all three results and owner sign-off.

## Pilot validation gates

| Gate | Task | Pass criteria |
| --- | --- | --- |
| G0 offline and entry | T006 | All offline conformance fixtures pass. Approval, lab, candidate pins, deny-by-default fixture and independent probes are recorded. Verify the running pins and every fresh instance’s policy before enrollment. |
| G1 standalone | T012 | Two isolated networks without factory subscriptions. One result per retry, approved traffic directly and through relay, every unauthorized probe denied, and separate termination qualified on a disposable network. |
| G2 local | T014 | Three local binding choices and unbound compatibility pass. Hosted retry converges. Two approved installations retain distinct grants, and both detach and subscription cancellation preserve unrelated access. |
| G3 hosted | T017 | Both managed choices and the no-binding path pass. Wrong-tenant, unauthorized app and public-ingress probes are denied. Failed onboarding leaves the binding unready. Catalog eligibility is tied to the exact qualified profile. |
| G4 drills and sign-off | T021 | Approved time limits are met, prior revocations survive restore, rollback removes partial access, tenant B remains available, and every failed gate has a reviewed remediation and clean rerun. Owners approve redacted evidence before expansion. |

Halt enrollment and isolate the affected network if cross-boundary access, public exposure, leaked credentials, duplicate provisioning, revived access or a missed drill window is observed. Preserve redacted evidence, remediate, then rerun the affected and neighboring boundary probes before requesting approval to resume. See the [pilot quickstart](quickstart.md).

## Requirement and success criterion traceability

| ID | Implementing or validating tasks |
| --- | --- |
| FR-001 | T004, T008, T014, T015 |
| FR-002 | T004, T008, T010, T012, T015, T017 |
| FR-003 | T004, T005, T008, T010, T012 |
| FR-004 | T001, T003, T004, T021 |
| FR-005 | T012, T014, T017, T021 |
| SC-001 | T012, T014, T017, T021 |
| SC-002 | T012, T014, T017 |
| SC-003 | T014, T017, T018, T019, T020, T021 |
| LC-01 | T008, T013, T014 |
| LC-02 | T007, T008, T014 |
| LC-03 | T008, T014 |
| LC-04 | T013, T014, T020 |
| LC-SC-01 | T014 |
| LC-SC-02 | T014 |
| LC-SC-03 | T020 |
| HS-01 | T009, T010, T012 |
| HS-02 | T009, T010, T012, T014 |
| HS-03 | T010, T012, T018 |
| HS-04 | T010, T012, T014, T017 |
| HS-05 | T011, T019 |
| HS-SC-01 | T012 |
| HS-SC-02 | T012, T014, T018 |
| HS-SC-03 | T019 |
| HD-01 | T016, T017 |
| HD-02 | T015, T017 |
| HD-03 | T004, T015, T017 |
| HD-04 | T016, T017 |
| HD-05 | T015, T017 |
| HD-SC-01 | T017 |
| HD-SC-02 | T017 |
| HD-SC-03 | T016, T017 |

## Ratified scenario traceability

| Ratified scenario | Evidence tasks |
| --- | --- |
| Customer installs Headscale locally | T007, T008, T014 |
| Customer brings an existing network | T008, T013, T014 |
| Customer uses Headscale without a factory | T009, T012 |
| Customer later attaches a factory | T010, T013, T014 |
| Hosted factory needs private access | T015, T017 |
| New domain joins the hosted catalog | T016, T017 |
| A customer attempts to cross a network boundary | T012, T014, T017 |
| Customer authorizes two factories on one network | T010, T014 |
| Factory requests a private service | T004, T008, T014, T017 |
| Factory attachment ends | T010, T014, T017, T018 |
| A managed instance needs recovery | T011, T019 |
