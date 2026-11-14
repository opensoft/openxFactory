# Design: Commission production connectivity execution and operations

Status: ratified
Ratified: 2026-11-14 by Brett Heap, through [commission-connectivity-operations-production](proposal.md).

## Context

See [proposal](proposal.md). The inspected owner is opensoft/opsXfactory. Current source is the landed synthetic pilot, not a qualified production service. T015 records actual owner commissioning; the single executable implementation list remains feature 043.

## Goals / Non-Goals

**Goals:** Deliver the complete owned production outcome, preserve current authority/lifecycle boundaries and retain actual source/release/qualification evidence.

**Non-Goals:** Grant target execution/spend, replace another owner, weaken existing checks, widen the pilot or infer live acceptance from source results.

## Decisions

### Architecture and consumed choices

The receiving workflow maps an accepted neutral request onto the already governed managed-system/AKS channel. Keep requester, executor, approvals, correlation and channel-required grants distinct; a reviewed pull-reconciled configuration change needs no extra push credential. The private-connectivity adapter performs only the current accepted subject/action set and preserves validation_pending until trusted readback. Recovery, cutover, monitoring and incidents operate on immutable original subjects and current revocations. Source changes grant no target effect. Any required target configuration/GitOps edit remains a separately reviewed owning request/plan rather than an implicit path grant in this repository. Use a separate private-connectivity-validation check with an explicit private-suite invocation and make that exact GitHub Actions context required only after the workflow is present on main. Preserve every existing required context and the native Ops validation/restart-group protocol. The qualification workflow is manual/approved-run driven, never a pull-request or push trigger for live operations. The hosted API's durable outbox/operator pull-ack route carries request references; the Ops actor accepts the case and executes through the existing channel, then sends authenticated actual readback. Product runtime readiness remains distinct from Q acceptance and commercial eligibility.

Freeze actual managed subjects, target channel, operator/executor identities, current request/grant or reviewed-merge authority, protected output/backup custody and numeric limits before effects. The provider reports opensoft/opsXfactory while the neutral admitted identifier remains OpsxFactory; verify the accepted owner mapping against the actual stable repository ID before use; do not infer a new repository merely from display casing. Existing QA/production cluster facts guide proposal preparation only. No new billable Azure resource, node scale-up, volume reuse or destructive/shared-node drill is authorized by source commissioning.

Proposed source/release owner and source-evidence custodian: Brett Heap, subject to explicit role/scope acceptance. Operator/customer roles and target authority remain separate. The owner's repository already has its canonical OpenSpec store. A corresponding owner-local realization packet must be prepared, linked and ratified there before source implementation; this coordinator packet does not relocate or waive that store.

### Exact per-task source scope

Paths are relative to opensoft/opsXfactory. This is an exact proposed allowlist intersected with the reviewed task envelope, not a directory grant. Proposed new task-file refinements need actual owner review and a refreshed 043 freeze before use.

| Task | Exact proposed files |
| --- | --- |
| T043 | workflows/private-connectivity/production_recovery.py<br>workflows/private-connectivity/recovery.py<br>tests/private_connectivity/test_production_recovery.py<br>evidence/private-connectivity-production/T043.json<br>workflows/private-connectivity/production.yaml<br>workflows/private-connectivity/production.md<br>workflows/private-connectivity/production_execution.py<br>scripts/client_infrastructure_execution.py<br>tests/private_connectivity/test_production_handoff.py |
| T044 | workflows/private-connectivity/production_monitoring.py<br>tests/private_connectivity/test_production_monitoring.py<br>docs/private-connectivity/production-monitoring.md<br>evidence/private-connectivity-production/T044.json |
| T045 | workflows/private-connectivity/production_cutover.py<br>tests/private_connectivity/test_production_cutover.py<br>evidence/private-connectivity-production/T045.json |
| T046 | workflows/private-connectivity/production_incidents.py<br>tests/private_connectivity/test_production_incidents.py<br>evidence/private-connectivity-production/T046.json |
| T047 | tests/private_connectivity/test_required_validation.py<br>evidence/private-connectivity-production/T047.json<br>.github/workflows/private-connectivity-validation.yml |
| T048 | tests/private_connectivity/qualify_production.py<br>tests/private_connectivity/test_production_runner.py<br>workflows/private-connectivity/install-pin.json<br>workflows/private-connectivity/runtime-inventory.json<br>docs/private-connectivity/production.md<br>evidence/private-connectivity-production/T048.json<br>.github/workflows/private-connectivity-qualification.yml |

### Required task-file refinements

- T043: add exactly workflows/private-connectivity/production.yaml, workflows/private-connectivity/production.md, workflows/private-connectivity/production_execution.py, scripts/client_infrastructure_execution.py, tests/private_connectivity/test_production_handoff.py.
- T047: add exactly .github/workflows/private-connectivity-validation.yml.
- T048: add exactly .github/workflows/private-connectivity-qualification.yml.
- Exclude unused candidate paths from this grant: scripts/run_test_shards.py, .github/workflows/opsx-validation.yml.

All remaining task identities, owners, cases, dependencies, verification commands and rollout gates remain intact. If required validation or a producer needs another file, obtain its owning scope before writing; never enlarge a prefix or relax a check. Any shared evidence-reader completion returns to the already commissioned E helper/test files with affected T007/T008 revalidation; a component task still writes one owner tree.

### Source custody, commands and release

Propose reviewed/redacted original source/CI output and genuine human-decision provenance in the private owner's Git history for project lifetime under existing repository access, with Brett as custodian. The already listed exact receipt may retain original source-output payloads sealed by its independently reviewed full-record commit/content identity. A receipt does not approve itself: actual owner review, fixed expected cases/commands, exact tested source/diff and genuine run/job/output identities remain mandatory. Missing provenance, copied verdicts or uncollected suites fail. No unlisted export tree or live/customer/provider custody is granted.

Retain existing source entry points and implement the explicitly proposed new suite/runner paths below; prove their actual collection after implementation:

- python3 scripts/client_infrastructure_execution.py
- python3 scripts/evidence_correlation_audit.py self-check
- python3 -m pytest tests/private_connectivity -q

New qualification commands are source deliverables, not existing execution grants. Target use requires accepted C-03/C-07/C-09 bounds and actual gate entry. Publish/read back supported candidates through the owner's accepted process with immutable provenance, actual CI and compatible content; no version is reserved by drafting.

### Qualification and target handoff

- Real existing-channel handoff and current scoped authority, including pull reconciliation and grant-required refusal.
- Fenced quarantined recovery with independent authoritative current revocations.
- Independent monitoring, finite approved limits, actual gaps, cleanup and authorized neighbors.
- Safe cutover/rollback and bounded incident containment with fresh resume after affected reruns.
- Explicit collected private suite, guarded actual-platform operational runner and support handoff.

Target/GitOps configuration has its own accepted managing-factory request/plan and exact source scope; it is not hidden in this code grant. Q0 commissions accepted source/preparation only. T049 closes final candidate/harness compatibility before preparation. Q1 bounds staging; Q2 requires the actual four-path union/controls; Q3, Q4 and Q5 separately govern each canary, observed window and offer/wave. Missing devices, capacity, custody or numerical limits remain consuming-gate prerequisites. Staging preserves the existing-QA/no-new-resource-spend preference unless separately revised.

## Risks / Trade-offs

- A core library can look like a deployed product → include real entry points, supported build/content and actual target qualification.
- Cross-boundary retry/cleanup can revive access → preserve original subjects, current revocations and fresh required authority.
- Schema/CI/witness coupling can exceed scope → enumerate it, measure actual changes and retain every unrelated guard.
- Source consent can be confused with target permission → keep runtime requests, actual observations and owner gate decisions separate.

## Migration Plan

Preserve 040 evidence and guards. Obtain the owner decision and required local governance, close consumed choices and refresh the listed task-file refinement, then implement through 043's dependencies. Verify actual source/CI and released content before final candidate closure; execute no target before its authority and gate. Preserve failures, contain only affected scope and requalify with reviewed remediation/fresh authority. Do not overwrite accepted observations or disable gates.

### Owner-local realization packet

The matching exact source scope is published for review in draft [owner PR #628](https://github.com/opensoft/opsXfactory/pull/628). Its owning OpenSpec packet must be ratified with the matching coordinating acceptance before implementation. Required hosted checks and actual Codex review remain distinct from source validation; this link supplies no owner consent or target authority.
