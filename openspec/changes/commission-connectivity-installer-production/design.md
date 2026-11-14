# Design: Commission the production private-connectivity installer

Status: ratified
Ratified: 2026-11-14 by Brett Heap, through [commission-connectivity-installer-production](proposal.md).

## Context

See [proposal](proposal.md). The inspected owner is opensoft/xFactory-Installer. Current source is the landed synthetic pilot, not a qualified production service. T012 records actual owner commissioning; the single executable implementation list remains feature 043.

## Goals / Non-Goals

**Goals:** Deliver the complete owned production outcome, preserve current authority/lifecycle boundaries and retain actual source/release/qualification evidence.

**Non-Goals:** Grant target execution/spend, replace another owner, weaken existing checks, widen the pilot or infer live acceptance from source results.

## Decisions

### Architecture and consumed choices

The customer command calls the existing transactional selection core through production local/managed adapters. Build an isolated private-connectivity distribution from those source files with a deterministic temporary build context and a hash-pinned PEP 517 build-dependency lock; do not repurpose the unrelated workstation application. Managed calls use the authenticated hosted API and current original-subject authority. Local operation remains independent of Hosted Headscale entitlement. Qualified artifact delivery uses the owner's approved candidate/distribution channel; no private repository is made public by this proposal.

Propose Linux Docker server operation with Windows/macOS/Linux clients and a Python CLI/package distribution. Exact client/server/tool versions, published contract/package/service content pins, supported delivery channel and credential/trust custody must be accepted before the corresponding implementation/release/qualification consumer. No raw credential belongs in a manifest, URL, log or repository.

Proposed source/release owner and source-evidence custodian: Brett Heap, subject to explicit role/scope acceptance. Operator/customer roles and target authority remain separate. The owner consumes the coordinator's ratified ownership/neutral decisions and this exact source commissioning. Preserve its existing ownership, release and validation conventions.

### Exact per-task source scope

Paths are relative to opensoft/xFactory-Installer. This is an exact proposed allowlist intersected with the reviewed task envelope, not a directory grant. Proposed new task-file refinements need actual owner review and a refreshed 043 freeze before use.

| Task | Exact proposed files |
| --- | --- |
| T024 | src/private_connectivity/local_provider.py<br>src/private_connectivity/selection.py<br>src/private_connectivity/contract-pin.json<br>src/private_connectivity/headscale-pin.json<br>src/private_connectivity/vendor/contracts/private-connectivity/binding.schema.json<br>src/private_connectivity/vendor/scripts/validate-private-connectivity.py<br>src/private_connectivity/runtime-inventory.json<br>tests/private_connectivity/test_production_local.py<br>evidence/private-connectivity-production/T024.json |
| T025 | src/private_connectivity/selection.py<br>tests/private_connectivity/test_migration.py<br>tests/private_connectivity/test_production_migration.py<br>evidence/private-connectivity-production/T025.json |
| T026 | packaging/private-connectivity/build.py<br>packaging/private-connectivity/pyproject.toml<br>packaging/private-connectivity/requirements-build.in<br>packaging/private-connectivity/requirements-build.lock<br>release/private-connectivity/manifest.json<br>tests/private_connectivity/qualify_production.py<br>tests/private_connectivity/test_production_runner.py<br>docs/private-connectivity.md<br>.github/workflows/validate.yml<br>evidence/private-connectivity-production/T026.json<br>src/private_connectivity/cli.py<br>tests/private_connectivity/test_production_cli.py |
| T034 | src/private_connectivity/managed_provider.py<br>src/private_connectivity/selection.py<br>src/private_connectivity/runtime-inventory.json<br>tests/private_connectivity/test_managed.py<br>tests/private_connectivity/test_production_managed.py<br>evidence/private-connectivity-production/T034.json |
| T035 | tests/private_connectivity/qualify_production.py<br>tests/private_connectivity/test_production_runner.py<br>.github/workflows/validate.yml<br>release/private-connectivity/manifest.json<br>docs/private-connectivity.md<br>evidence/private-connectivity-production/T035.json |

### Required task-file refinements

- T026: add exactly src/private_connectivity/cli.py, tests/private_connectivity/test_production_cli.py.

All remaining task identities, owners, cases, dependencies, verification commands and rollout gates remain intact. If required validation or a producer needs another file, obtain its owning scope before writing; never enlarge a prefix or relax a check. Any shared evidence-reader completion returns to the already commissioned E helper/test files with affected T007/T008 revalidation; a component task still writes one owner tree.

### Source custody, commands and release

Propose reviewed/redacted original source/CI output and genuine human-decision provenance in the private owner's Git history for project lifetime under existing repository access, with Brett as custodian. The already listed exact receipt may retain original source-output payloads sealed by its independently reviewed full-record commit/content identity. A receipt does not approve itself: actual owner review, fixed expected cases/commands, exact tested source/diff and genuine run/job/output identities remain mandatory. Missing provenance, copied verdicts or uncollected suites fail. No unlisted export tree or live/customer/provider custody is granted.

Retain existing source entry points and implement the explicitly proposed new suite/runner paths below; prove their actual collection after implementation:

- make validate
- make test
- python3 -m unittest discover -s tests/private_connectivity -p 'test_*.py'

New qualification commands are source deliverables, not existing execution grants. Target use requires accepted C-03/C-07/C-09 bounds and actual gate entry. Publish/read back supported candidates through the owner's accepted process with immutable provenance, actual CI and compatible content; no version is reserved by drafting.

### Qualification and target handoff

- New/existing/unbound behavior with no mandatory hosted credential.
- Managed service integration and current entitlement/attachment authority.
- Restart/retry/migration/rollback with original cleanup subjects and revoked prior-binding refusal.
- Actual CLI/package build, collected source CI and supported compatible release readback.

Target/GitOps configuration has its own accepted managing-factory request/plan and exact source scope; it is not hidden in this code grant. Q0 commissions accepted source/preparation only. T049 closes final candidate/harness compatibility before preparation. Q1 bounds staging; Q2 requires the actual four-path union/controls; Q3, Q4 and Q5 separately govern each canary, observed window and offer/wave. Missing devices, capacity, custody or numerical limits remain consuming-gate prerequisites. Staging preserves the existing-QA/no-new-resource-spend preference unless separately revised.

## Risks / Trade-offs

- A core library can look like a deployed product → include real entry points, supported build/content and actual target qualification.
- Cross-boundary retry/cleanup can revive access → preserve original subjects, current revocations and fresh required authority.
- Schema/CI/witness coupling can exceed scope → enumerate it, measure actual changes and retain every unrelated guard.
- Source consent can be confused with target permission → keep runtime requests, actual observations and owner gate decisions separate.

## Migration Plan

Preserve 040 evidence and guards. Obtain the owner decision and required local governance, close consumed choices and refresh the listed task-file refinement, then implement through 043's dependencies. Verify actual source/CI and released content before final candidate closure; execute no target before its authority and gate. Preserve failures, contain only affected scope and requalify with reviewed remediation/fresh authority. Do not overwrite accepted observations or disable gates.
