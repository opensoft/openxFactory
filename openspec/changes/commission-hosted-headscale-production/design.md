# Design: Commission Hosted Headscale and hosted-factory service production

Status: ratified
Ratified: 2026-11-14 by Brett Heap, through [commission-hosted-headscale-production](proposal.md).

## Context

See [proposal](proposal.md). The inspected owner is opensoft/openXsoft-Hosted-Services. Current source is the landed synthetic pilot, not a qualified production service. T013 records actual owner commissioning; the single executable implementation list remains feature 043.

## Goals / Non-Goals

**Goals:** Deliver the complete owned production outcome, preserve current authority/lifecycle boundaries and retain actual source/release/qualification evidence.

**Non-Goals:** Grant target execution/spend, replace another owner, weaken existing checks, widen the pilot or infer live acceptance from source results.

## Decisions

### Architecture and consumed choices

Serve a production HTTP API over the existing durable operation, network and attachment cores. Use a proper WSGI process/container entry point and hash-pinned authentication/server dependencies. Authenticate issuer/audience/key material and derive customer/environment/permissions from trusted identity; require a product-owned authoritative entitlement record, never a caller flag. The Azure/AKS provider submits accepted infrastructure requests through the existing managing-factory channel and consumes authenticated current readback; the product gets no standing deployed write credential. A missing/unready provider cannot fall back to Docker pilot code. Factory onboarding and catalog routes remain unavailable/ineligible until their actual compatible domain/SDK release and current qualification authority exist. The v1 API includes a durable request outbox and authenticated operator pull/ack/readback routes. Customer submission is not case acceptance. Only the current authorized Ops actor can report scoped actual readback, and results remain pending until the required readiness observations pass.

Select the actual Keycloak/OIDC issuer/client/audience and roles, product entitlement authority, protected credential and backup custody, approved request/readback channel and target identities before dependent adapter work. Existing Opensoft services are candidates for reuse. The current openxsoft.com nameservers are Spaceship; no Azure DNS authority is assumed. Exact service/DNS/certificate names and protected custody need their owning decisions. Storage is a qualified dedicated persistent-filesystem/single-writer topology, not an assumed reuse of another tenant's volume. Source unit/CI proof never supplies live service eligibility.

Proposed source/release owner and source-evidence custodian: Brett Heap, subject to explicit role/scope acceptance. Operator/customer roles and target authority remain separate. The owner consumes the coordinator's ratified ownership/neutral decisions and this exact source commissioning. Preserve its existing ownership, release and validation conventions.

### Exact per-task source scope

Paths are relative to opensoft/openXsoft-Hosted-Services. This is an exact proposed allowlist intersected with the reviewed task envelope, not a directory grant. Proposed new task-file refinements need actual owner review and a refreshed 043 freeze before use.

| Task | Exact proposed files |
| --- | --- |
| T028 | services/network-provisioning/production/provider.py<br>tests/qualification/test_production_provider.py<br>release/install-pin.json<br>evidence/private-connectivity-production/T028.json |
| T029 | services/network-provisioning/production/identity.py<br>services/network-provisioning/production/entitlement.py<br>services/network-provisioning/production/custody.py<br>tests/qualification/test_production_authority.py<br>evidence/private-connectivity-production/T029.json |
| T030 | services/network-provisioning/service.py<br>services/network-provisioning/operations.py<br>tests/qualification/test_operations.py<br>tests/qualification/test_production_operations.py<br>evidence/private-connectivity-production/T030.json<br>services/network-provisioning/production/app.py<br>tests/qualification/test_production_api.py |
| T031 | services/network-provisioning/service.py<br>services/network-provisioning/attachments.py<br>services/network-provisioning/supervisor.py<br>tests/qualification/test_production_lifecycle.py<br>evidence/private-connectivity-production/T031.json |
| T032 | services/catalog/production.py<br>services/catalog/qualification.py<br>tests/qualification/test_production_catalog.py<br>evidence/private-connectivity-production/T032.json |
| T033 | tests/qualification/qualify_production.py<br>tests/qualification/test_production_runner.py<br>.github/workflows/qualification.yml<br>release/runtime-inventory.json<br>release/install-pin.json<br>docs/production-headscale.md<br>evidence/private-connectivity-production/T033.json<br>services/network-provisioning/production/requirements.in<br>services/network-provisioning/production/requirements.lock<br>services/network-provisioning/production/Dockerfile<br>services/network-provisioning/production/__main__.py |
| T039 | services/factory-onboarding/production_binder.py<br>services/factory-onboarding/onboarding.py<br>tests/qualification/test_production_onboarding.py<br>release/installer-pin.json<br>release/domain-profile-pin.json<br>evidence/private-connectivity-production/T039.json |
| T040 | services/catalog/production.py<br>services/catalog/qualification.py<br>tests/qualification/test_production_catalog_integration.py<br>release/domain-inventory.json<br>evidence/private-connectivity-production/T040.json |
| T041 | tests/qualification/qualify_production.py<br>tests/qualification/test_production_runner.py<br>.github/workflows/qualification.yml<br>release/runtime-inventory.json<br>release/installer-pin.json<br>release/domain-profile-pin.json<br>evidence/private-connectivity-production/T041.json |

### Required task-file refinements

- T030: add exactly services/network-provisioning/production/app.py, tests/qualification/test_production_api.py.
- T033: add exactly services/network-provisioning/production/requirements.in, services/network-provisioning/production/requirements.lock, services/network-provisioning/production/Dockerfile, services/network-provisioning/production/__main__.py.

All remaining task identities, owners, cases, dependencies, verification commands and rollout gates remain intact. If required validation or a producer needs another file, obtain its owning scope before writing; never enlarge a prefix or relax a check. Any shared evidence-reader completion returns to the already commissioned E helper/test files with affected T007/T008 revalidation; a component task still writes one owner tree.

### Source custody, commands and release

Propose reviewed/redacted original source/CI output and genuine human-decision provenance in the private owner's Git history for project lifetime under existing repository access, with Brett as custodian. The already listed exact receipt may retain original source-output payloads sealed by its independently reviewed full-record commit/content identity. A receipt does not approve itself: actual owner review, fixed expected cases/commands, exact tested source/diff and genuine run/job/output identities remain mandatory. Missing provenance, copied verdicts or uncollected suites fail. No unlisted export tree or live/customer/provider custody is granted.

Retain existing source entry points and implement the explicitly proposed new suite/runner paths below; prove their actual collection after implementation:

- make validate
- make test
- python3 -m unittest discover -s tests/qualification -p 'test_*.py'

New qualification commands are source deliverables, not existing execution grants. Target use requires accepted C-03/C-07/C-09 bounds and actual gate entry. Publish/read back supported candidates through the owner's accepted process with immutable provenance, actual CI and compatible content; no version is reserved by drafting.

### Qualification and target handoff

- Actual authenticated API and provider; dedicated two-customer/environment boundaries; no synthetic fallback.
- Trusted identity, independent entitlement, scoped secrets and original-subject durable concurrency/retries.
- Standalone and local-managed lifecycle, scoped sharing and independent cancellation/termination.
- Trusted real domain/profile, independent application permission and strict current catalog authority.
- Collected source CI, buildable supported service candidates and guarded actual-platform runner.

Target/GitOps configuration has its own accepted managing-factory request/plan and exact source scope; it is not hidden in this code grant. Q0 commissions accepted source/preparation only. T049 closes final candidate/harness compatibility before preparation. Q1 bounds staging; Q2 requires the actual four-path union/controls; Q3, Q4 and Q5 separately govern each canary, observed window and offer/wave. Missing devices, capacity, custody or numerical limits remain consuming-gate prerequisites. Staging preserves the existing-QA/no-new-resource-spend preference unless separately revised.

## Risks / Trade-offs

- A core library can look like a deployed product → include real entry points, supported build/content and actual target qualification.
- Cross-boundary retry/cleanup can revive access → preserve original subjects, current revocations and fresh required authority.
- Schema/CI/witness coupling can exceed scope → enumerate it, measure actual changes and retain every unrelated guard.
- Source consent can be confused with target permission → keep runtime requests, actual observations and owner gate decisions separate.

## Migration Plan

Preserve 040 evidence and guards. Obtain the owner decision and required local governance, close consumed choices and refresh the listed task-file refinement, then implement through 043's dependencies. Verify actual source/CI and released content before final candidate closure; execute no target before its authority and gate. Preserve failures, contain only affected scope and requalify with reviewed remediation/fresh authority. Do not overwrite accepted observations or disable gates.
