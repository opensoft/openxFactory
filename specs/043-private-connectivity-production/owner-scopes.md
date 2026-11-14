# Production qualification owner scopes

Status: draft
Created: 2026-11-13
Feature: [043-private-connectivity-production](spec.md)

## Authority recorded by this feature creation

Brett Heap requested the coordinating feature, implementation plan, task generation and cross-artifact analysis/remediation in this session. The current authorized artifact scope is openXfactory's specification/plan/task packet and its analysis/remediation record under specs/043-private-connectivity-production, its feature selector, managed agent-context plan reference and its governance/index handoff links.

This authorizes specification, plan, task-list and analysis/remediation preparation. Q0 is not accepted by this document. The ratified policy approves ownership boundaries, not new runtime code, workflow, schema or deployment path grants. Owner acceptance and concrete realization authority remain required before implementation. The single [tasks.md](tasks.md) represents each implementation item once.

## Responsibility boundaries for Q0 commissioning

| Owner class / repository | Owned production outcome | Scope to make concrete and approve before implementation | Authority not inherited from this draft |
| --- | --- | --- | --- |
| Neutral coordinator / opensoft/openXfactory | Production qualification policy, feature coordination, neutral contract publication if separately required | Named maintainer; exact documentation, contract, schema, validator/test and CI surfaces if commissioned; existing publication/release process and verification commands | Hosted runtime, provider operation, an unallocated contract version, consumer-pin updates or paid resources |
| Package / opensoft/Headscale-Install | Supported package, HTTPS identity and renewal, isolated instance/state lifecycle, backup, upgrade and quarantined recovery | Named maintainer; supported platforms/server/clients, exact package/state and conformance surfaces, release custody and verification commands | Cross-customer operation, entitlement decisions or execution on a registered managed target without handoff |
| Installer / opensoft/xFactory-Installer | Supported setup/distribution for install-new, connect-existing, managed selection and unbound compatibility | Named maintainer; exact selection/setup/distribution and validation surfaces, supported packaging matrix and verification commands | The unrelated workstation-intake application, Store submission, service entitlement or operational administration |
| Hosted product / opensoft/openXsoft-Hosted-Services | Actual provider/identity/entitlement integrations, durable managed operations, factory onboarding, catalog and exact-profile eligibility | Named maintainer; intended platform/provider first, then exact adapter/service/profile/catalog and required-check surfaces, releases and verification commands | Approval of another owner's domain, deployment credentials, provider spend or expansion by declaration |
| Operational executor / opensoft/opsXfactory and the target's managing factory | Managed-subject handoff, custody, monitoring, operational acceptance, emergency containment, recovery and rollback | Named operational owner; registered target subjects, governed channel, exact operating/monitoring surfaces, scoped requests/grants where required, run evidence and commands | A standing builder credential, execution outside accepted target scope, or consent for an unmanaged customer target |
| Actual production DomainxFactory owner / repository selected at Q0 | Actual workload, minimum access, application authorization, exact profile and lifecycle acceptance | Named domain maintainer and actual repository/profile; exact definition-time protection, required validation and workload/access/CI surfaces; release evidence and commands | Another domain/profile's acceptance, feature 040 synthetic-profile eligibility or blanket catalog launch |

Every row is a responsibility boundary, not an approved file allowlist. Concrete repository, file/code/CI/schema surfaces, commands, approver, decision reference and validity are mandatory commissioning fields. Where an owning governance change is required, its acceptance precedes the dependent work. A missing scope remains uncommissioned.

## Human roles and decisions

The commissioning record names the rollout lead and accountable neutral, package, installer, hosted-product, operational and domain owners. It also names customer authority where consent or customer operation is required, evidence/backup/credential custodians, support/on-call and rollback operators for the relevant gates.

One person may hold several roles, but each role and scope is explicit. Brett's request to create this feature does not sign for every runtime owner or customer. The five feature 040 lab-role approvals do not approve these production decisions.

## Execution boundary

For a registered managed target, the producing owner ends at its supported release and realization evidence. Deployment crosses as an accepted client_infrastructure_request, executed through the managing factory's governed channel. A grant-required channel uses a valid scoped grant and closes it on completion. A reviewed governed merge applied by pull reconciliation does not acquire an additional push credential.

An unmanaged customer-operated target remains under its current authorized customer operator and required consent. Environment tier never chooses the executor. Q0 commissioning, target execution, gate acceptance and commercial release are separate authorities.

## Current disposition

T001-T009 are complete. The original T006 E scope and source-only custody remain recorded in their historical ratification. Brett has now ratified the E bootstrap amendment, all five component scopes and matching native Ops/domain packets, and the separate neutral publication/release scope. The accepted file refinements are reconciled into tasks.md and the current review freeze; source consent does not complete T010-T017 or full Q0. T010 still requires actual original evidence and custodian authentication. All three PRs remain draft.

| Accepted source role | Named owner/custodian | Exact governing scope |
| --- | --- | --- |
| E evidence controls | Brett Heap | [Original E scope](../../openspec/changes/commission-private-connectivity-production-evidence/design.md) plus [ratified bootstrap amendment](../../openspec/changes/amend-private-connectivity-evidence-bootstrap/review/ratification.md) |
| N neutral publication/release | Brett Heap | [Accepted publication scope](../../openspec/changes/publish-private-connectivity-production-contract/review/ratification.md); normal atomic cut and late version/inventory allocation |
| L package/source/release | Brett Heap | [Accepted package scope](../../openspec/changes/commission-headscale-production/review/ratification.md) |
| I installer/source/release | Brett Heap | [Accepted installer scope](../../openspec/changes/commission-connectivity-installer-production/review/ratification.md) |
| H hosted product/source/release | Brett Heap | [Accepted hosted-product scope](../../openspec/changes/commission-hosted-headscale-production/review/ratification.md) |
| D domain/profile/source/release | Brett Heap | [Accepted actual MCP source scope](../../openspec/changes/commission-hosted-domain-production/review/ratification.md), with matching native packet |
| O operations/source/release | Brett Heap | [Accepted Ops source scope](../../openspec/changes/commission-connectivity-operations-production/review/ratification.md), with matching native packet |

Component source custody is reviewed/redacted original source/CI and genuine decision provenance retained in each private owning Git repository for project lifetime under existing permissions, bound to exact commits/content, actual run/job/command identities and actual owner review. Coordinator E keeps its accepted public secret-free source Git policy. Neutral publication follows its accepted existing versioning/release custody and verification process. None selects protected live/customer/provider custody.

The accepted source repositories and exact file lists grant no target operation. Actual provider/target/service choices, supported version/distribution matrix and consumed integration/limit/custody decisions must be accepted before their consumers. No source or release role supplies an operator/customer grant, a standing deployment credential or commercial admission. The approved USD 10 QA storage financial envelope and separately applied repository Mac zero-paid guard retain their exact limits; they authorize no provisioning or runner job.

## Candidate implementation and verification surfaces

These are inspected source anchors and proposed new areas for C-01 review, not an accepted allowlist. Close each scope to exact files/commands under the owning decision before edits. Some inspected owner primary checkouts are stale; verify the selected owner revision and accepted release rather than assuming a local main is current.

| Commissioning boundary | Existing source anchors / proposed new work | Existing verification and required production extension |
| --- | --- | --- |
| Neutral publication | scripts/validate-private-connectivity.py and tests/private_connectivity currently consume the feature 040 draft schema. Proposed supported publication is contracts/private-connectivity with contracts/manifest.yaml, contracts/CHANGELOG.md and generated contracts/releases inventories | Existing binding conformance plus normal release build/commit/promotion/tag verification. Accept exact publication/reader/test scope first, allocate version at the approved cut, then verify published consumer content pins |
| Coordinator evidence | Proposed new specs/043-private-connectivity-production/verify-evidence.py, register-evidence-pins.py, tests/test_evidence.py and tests/test_evidence_pins.py. Shared scripts/doc_health/pin_class.py, tests/doc-health/test_pin_reachability.py and test_sentinel_vocabulary.py census, plus .github/workflows/pytest-suite.yml if required wiring changes, are separate governed surfaces | Commission verifier/case/command/dependency tests and an explicit required invocation of the new feature suite. Obtain narrow owning OpenSpec authority before shared-reader, census or workflow edits; 040 registration does not cover 043 |
| Headscale-Install | deploy/pilot.py, workloads.py, application.py and preflight.py are fixed lab controls; deploy/recovery.py provides backup/quarantine rehearsal. packaging, release, docs/runbooks and tests/qualification anchor supported packaging/renewal/state/recovery work. Exact distinct production files are selected by the owner | make validate and make test are existing source/fixture commands under .github/workflows/qualification.yml. Commission actual supported-client/TLS-renewal/recovery/platform qualification before Q1; preserve lab guards and release helper provenance |
| xFactory-Installer | src/private_connectivity/selection.py, pilot_provider.py and managed_provider.py; existing contract/headscale pins, vendor/requirements and runtime inventory; tests/private_connectivity and docs/private-connectivity.md. Exact production adapter/setup/distribution files require accepted scope | make validate and make test under .github/workflows/validate.yml, with the declared schema dependency. Qualify new/existing/unbound and managed production choices plus current authority/retry/migration/rollback. No workstation-intake or Store scope is inherited |
| Hosted product | services/network-provisioning/service.py, operations.py, attachments.py and supervisor.py; synthetic docker_pilot.py/docker_nodes.py; services/factory-onboarding/onboarding.py and pilot_binder.py; services/catalog/qualification.py and release inventories/pins | make validate and make test under .github/workflows/qualification.yml. Actual provider/authentication/entitlement/custody/workload adapters and strict production catalog semantics need exact newly accepted paths. Preserve durable original-subject state and derive privacy from the trusted profile |
| Ops/managing factory | workflows/client-infrastructure-execution.yaml, scripts/client_infrastructure_execution.py, deployment/custody interfaces, workflows/private-connectivity/recovery.py and docker_recovery.py, docs/private-connectivity and tests/private_connectivity | Existing intake/correlation self-checks and explicit python3 -m pytest tests/private_connectivity -q. Commission actual operational adapters, monitoring/custody and required CI invocation. Generic shard discovery omits this nested suite; changing scripts/run_test_shards.py is only necessary if that discovery solution is selected, otherwise use an accepted explicit required entry point |
| Actual domain | Selection and exact production paths are blocked on C-02. Historical codeXfactory anchors are profiles/hosted/private-connectivity.yaml, schemas/hosted-connectivity-profile.schema.json, tests/private_connectivity, scripts/merge_master/council_clearance.py and required doc/CI wiring | The historical profile is test/synthetic/customer-ineligible and its protection is exact to that file. A selected production owner must accept actual workload/profile/schema, exact definition-time protection and fail-closed required validation/dependencies. Equivalent owner mechanisms are acceptable; copying a directory prefix or another profile's evidence is not |

The plan's E/N/L/H/I/D/O workstreams and [validation matrix](validation-matrix.md) use these boundaries. This source-anchor table does not enlarge the exact ratified per-task scopes above. Ops uses the accepted separate private-connectivity-validation workflow; scripts/run_test_shards.py and the existing opsx-validation workflow are excluded from that source grant.
