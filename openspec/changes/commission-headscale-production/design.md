# Design: Commission the supported Headscale package

Status: ratified
Ratified: 2026-11-14 by Brett Heap, through [commission-headscale-production](proposal.md).

## Context

See [proposal](proposal.md). The inspected owner is opensoft/Headscale-Install. Current source is the landed synthetic pilot, not a qualified production service. T011 records actual owner commissioning; the single executable implementation list remains feature 043.

## Goals / Non-Goals

**Goals:** Deliver the complete owned production outcome, preserve current authority/lifecycle boundaries and retain actual source/release/qualification evidence.

**Non-Goals:** Grant target execution/spend, replace another owner, weaken existing checks, widen the pilot or infer live acceptance from source results.

## Decisions

### Architecture and consumed choices

The package produces a closed desired-instance plan and qualified deploy/endpoint/recovery mechanisms. Local use needs no hosted subscription. Docker effects require the current authorized local customer operator; managed effects terminate at the existing managing-factory handoff. Headscale state uses a dedicated persistent filesystem per boundary, with one fenced writer and separately protected keys/policy. A shared database or a network filesystem is not assumed compatible merely because it already exists.

Propose Linux Docker as the server platform and the selected Windows/macOS/Linux client scope. Select exact supported versions, immutable image digests, persistent-volume identities, certificate issuer/renewal ownership and recovery limits before their consumers. Candidate v0.29.7 was observed as the upstream stable release; version-specific documentation and actual compatibility still need verification at the cut.

Proposed source/release owner and source-evidence custodian: Brett Heap, subject to explicit role/scope acceptance. Operator/customer roles and target authority remain separate. The owner consumes the coordinator's ratified ownership/neutral decisions and this exact source commissioning. Preserve its existing ownership, release and validation conventions.

### Exact per-task source scope

Paths are relative to opensoft/Headscale-Install. This is an exact proposed allowlist intersected with the reviewed task envelope, not a directory grant. Proposed new task-file refinements need actual owner review and a refreshed 043 freeze before use.

| Task | Exact proposed files |
| --- | --- |
| T020 | deploy/production/instance.py<br>packaging/production-images.json<br>tests/qualification/test_production_package.py<br>evidence/private-connectivity-production/T020.json |
| T021 | deploy/production/endpoint.py<br>tests/qualification/test_production_endpoint.py<br>evidence/private-connectivity-production/T021.json |
| T022 | deploy/production/recovery.py<br>tests/qualification/test_production_recovery.py<br>evidence/private-connectivity-production/T022.json |
| T023 | tests/qualification/qualify_production.py<br>tests/qualification/test_production_runner.py<br>.github/workflows/qualification.yml<br>release/private-connectivity-production.json<br>docs/runbooks/production-package.md<br>evidence/private-connectivity-production/T023.json |

### Required task-file refinements

The candidate directory envelopes are closed to the exact filenames above; no task identity, owner, dependency, case or command changes.

All remaining task identities, owners, cases, dependencies, verification commands and rollout gates remain intact. If required validation or a producer needs another file, obtain its owning scope before writing; never enlarge a prefix or relax a check. Any shared evidence-reader completion returns to the already commissioned E helper/test files with affected T007/T008 revalidation; a component task still writes one owner tree.

### Source custody, commands and release

Propose reviewed/redacted original source/CI output and genuine human-decision provenance in the private owner's Git history for project lifetime under existing repository access, with Brett as custodian. The already listed exact receipt may retain original source-output payloads sealed by its independently reviewed full-record commit/content identity. A receipt does not approve itself: actual owner review, fixed expected cases/commands, exact tested source/diff and genuine run/job/output identities remain mandatory. Missing provenance, copied verdicts or uncollected suites fail. No unlisted export tree or live/customer/provider custody is granted.

Retain existing source entry points and implement the explicitly proposed new suite/runner paths below; prove their actual collection after implementation:

- make validate
- make test
- python3 tests/qualification/qualify_production.py --help

New qualification commands are source deliverables, not existing execution grants. Target use requires accepted C-03/C-07/C-09 bounds and actual gate entry. Publish/read back supported candidates through the owner's accepted process with immutable provenance, actual CI and compatible content; no version is reserved by drafting.

### Qualification and target handoff

- Install-new/connect-existing/unbound and verified endpoint controls with real clients.
- Protected state, backup age/data loss, writer fencing, quarantined restore and current revocations.
- Actual source/CI collection and independently verified supported candidate identity.

Target/GitOps configuration has its own accepted managing-factory request/plan and exact source scope; it is not hidden in this code grant. Q0 commissions accepted source/preparation only. T049 closes final candidate/harness compatibility before preparation. Q1 bounds staging; Q2 requires the actual four-path union/controls; Q3, Q4 and Q5 separately govern each canary, observed window and offer/wave. Missing devices, capacity, custody or numerical limits remain consuming-gate prerequisites. Staging preserves the existing-QA/no-new-resource-spend preference unless separately revised.

## Risks / Trade-offs

- A core library can look like a deployed product → include real entry points, supported build/content and actual target qualification.
- Cross-boundary retry/cleanup can revive access → preserve original subjects, current revocations and fresh required authority.
- Schema/CI/witness coupling can exceed scope → enumerate it, measure actual changes and retain every unrelated guard.
- Source consent can be confused with target permission → keep runtime requests, actual observations and owner gate decisions separate.

## Migration Plan

Preserve 040 evidence and guards. Obtain the owner decision and required local governance, close consumed choices and refresh the listed task-file refinement, then implement through 043's dependencies. Verify actual source/CI and released content before final candidate closure; execute no target before its authority and gate. Preserve failures, contain only affected scope and requalify with reviewed remediation/fresh authority. Do not overwrite accepted observations or disable gates.
