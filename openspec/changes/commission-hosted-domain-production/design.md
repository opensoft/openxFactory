# Design: Commission actual software-factory hosted connectivity profiles

Status: ratified
Ratified: 2026-11-14 by Brett Heap, through [commission-hosted-domain-production](proposal.md).

## Context

See [proposal](proposal.md). The inspected owner is codeXfactory/codeXfactory. Current source is the landed synthetic pilot, not a qualified production service. T014 records actual owner commissioning; the single executable implementation list remains feature 043.

## Goals / Non-Goals

**Goals:** Deliver the complete owned production outcome, preserve current authority/lifecycle boundaries and retain actual source/release/qualification evidence.

**Non-Goals:** Grant target execution/spend, replace another owner, weaken existing checks, widen the pilot or infer live acceptance from source results.

## Decisions

### Architecture and consumed choices

Reuse the real MCP application behavior and its pinned canonical OAuth resource configuration. A private profile requires private reachability and forbids application public ingress; the separately explicit unbound profile retains independent application authorization and its own reviewed ingress policy. Source/network membership never grants application permission. Qualification's legitimate application control can use authenticated MCP discovery so no paid model call or unrelated workflow effect is implied. Define a strict production profile kind/schema and exact-path protection for both definitions; do not widen or relabel the test/synthetic profile. Schema registration includes schemas/README.md and stack.yaml. Exact definition-time protection uses the established unchanged behavior-witness producer; retain every unrelated predicate/verdict cell and measure actual new admissions. A supported neutral pin advance is atomic with the four actual vendored source captures, their data pin and the established browser pin-lineage producer. Only changed qualified source bytes are re-vendored; do not edit the producer, rewrite old lineage or move shared consumer pins.

The provider currently reports codeXfactory/codeXfactory, repository ID 1281785369; the neutral estate admission currently names codexFactory at codeXfactory/codexFactory. The proposal uses the admitted estate identifier. Verify the selected checkout's actual origin/stable repository ID against the accepted owner mapping; complete any genuinely required identity reconciliation before code rather than assuming a new admission from a casing difference. Select the exact workload artifact/configuration, private and unbound ingress/port/resource audiences, supported release matrix and target authority under C-02/C-05/C-03. A public MCP profile is never a fallback for a failed private requirement.

Proposed source/release owner and source-evidence custodian: Brett Heap, subject to explicit role/scope acceptance. Operator/customer roles and target authority remain separate. The owner's repository already has its canonical OpenSpec store. A corresponding owner-local realization packet must be prepared, linked and ratified there before source implementation; this coordinator packet does not relocate or waive that store.

### Exact per-task source scope

Paths are relative to codeXfactory/codeXfactory. This is an exact proposed allowlist intersected with the reviewed task envelope, not a directory grant. Proposed new task-file refinements need actual owner review and a refreshed 043 freeze before use.

| Task | Exact proposed files |
| --- | --- |
| T036 | profiles/hosted/production-mcp-private.yaml<br>profiles/hosted/production-mcp-unbound.yaml<br>schemas/production-hosted-connectivity-profile.schema.json<br>schemas/README.md<br>src/hosted_connectivity_profile.py<br>tests/private_connectivity/test_production_profile.py<br>tests/private_connectivity/test_production_profile_schema.py<br>tests/private_connectivity/test_production_application_authority.py<br>evidence/private-connectivity-production/T036.json<br>stack.yaml |
| T037 | scripts/validate-examples.py<br>scripts/validate-production-profile.py<br>scripts/validate-docs.sh<br>scripts/merge_master/council_clearance.py<br>tests/private_connectivity/test_required_production_validation.py<br>tests/merge-master/test_production_profile_floor.py<br>tests/merge-master/test_class_floor_differential.py<br>tests/merge-master/test_openxfactory_tree_floor.py<br>tests/merge-master/test_tree_floor_probe.py<br>tests/merge-master/test_behaviour_snapshot.py<br>tests/merge-master/fixtures/tree-floor-probe/codexFactory.yaml<br>.github/workflows/validate.yml<br>evidence/private-connectivity-production/T037.json<br>specs/018-per-tree-floor-instance/behaviour-snapshot.json |
| T038 | tests/private_connectivity/qualify_production.py<br>tests/private_connectivity/test_production_runner.py<br>stack.yaml<br>release/private-connectivity-production.json<br>docs/hosted-connectivity.md<br>evidence/private-connectivity-production/T038.json<br>scripts/merge_master/vendored/vendored-scope-globs.pin.yaml<br>scripts/merge_master/scope_globs.py<br>scripts/merge_master/frontmatter_strict.py<br>scripts/merge_master/validate_scope_globs.py<br>scripts/merge_master/sequenced_after.py<br>scripts/browser_ui_repair/ci/pin-lineage-v1.yaml |

### Required task-file refinements

- T036: add exactly stack.yaml.
- T037: add exactly specs/018-per-tree-floor-instance/behaviour-snapshot.json.
- T038: add exactly scripts/merge_master/vendored/vendored-scope-globs.pin.yaml, scripts/merge_master/scope_globs.py, scripts/merge_master/frontmatter_strict.py, scripts/merge_master/validate_scope_globs.py, scripts/merge_master/sequenced_after.py, scripts/browser_ui_repair/ci/pin-lineage-v1.yaml.

All remaining task identities, owners, cases, dependencies, verification commands and rollout gates remain intact. If required validation or a producer needs another file, obtain its owning scope before writing; never enlarge a prefix or relax a check. Any shared evidence-reader completion returns to the already commissioned E helper/test files with affected T007/T008 revalidation; a component task still writes one owner tree.

### Source custody, commands and release

Propose reviewed/redacted original source/CI output and genuine human-decision provenance in the private owner's Git history for project lifetime under existing repository access, with Brett as custodian. The already listed exact receipt may retain original source-output payloads sealed by its independently reviewed full-record commit/content identity. A receipt does not approve itself: actual owner review, fixed expected cases/commands, exact tested source/diff and genuine run/job/output identities remain mandatory. Missing provenance, copied verdicts or uncollected suites fail. No unlisted export tree or live/customer/provider custody is granted.

Retain existing source entry points and implement the explicitly proposed new suite/runner paths below; prove their actual collection after implementation:

- python3 scripts/validate-examples.py
- python3 -m pytest tests/private_connectivity -q
- python3 -m pytest tests/merge-master/test_production_profile_floor.py -q
- bash scripts/validate-docs.sh

New qualification commands are source deliverables, not existing execution grants. Target use requires accepted C-03/C-07/C-09 bounds and actual gate entry. Publish/read back supported candidates through the owner's accepted process with immutable provenance, actual CI and compatible content; no version is reserved by drafting.

### Qualification and target handoff

- Actual MCP application/profile identity with independent OAuth/application authority.
- Strict profile schema/semantics and exact definition-time protection for both concrete paths.
- Required validation really collected; missing dependencies/unknown kinds fail.
- Actual private new/existing and separately qualified unbound controls with public-ingress denial where required.
- Supported compatible profile/workload release and guarded real-application runner.
- Schema/stack registration, unchanged-producer behavior witness and measured tree admissions; atomic contract/vendor/lineage coupling.

Target/GitOps configuration has its own accepted managing-factory request/plan and exact source scope; it is not hidden in this code grant. Q0 commissions accepted source/preparation only. T049 closes final candidate/harness compatibility before preparation. Q1 bounds staging; Q2 requires the actual four-path union/controls; Q3, Q4 and Q5 separately govern each canary, observed window and offer/wave. Missing devices, capacity, custody or numerical limits remain consuming-gate prerequisites. Staging preserves the existing-QA/no-new-resource-spend preference unless separately revised.

## Risks / Trade-offs

- A core library can look like a deployed product → include real entry points, supported build/content and actual target qualification.
- Cross-boundary retry/cleanup can revive access → preserve original subjects, current revocations and fresh required authority.
- Schema/CI/witness coupling can exceed scope → enumerate it, measure actual changes and retain every unrelated guard.
- Source consent can be confused with target permission → keep runtime requests, actual observations and owner gate decisions separate.

## Migration Plan

Preserve 040 evidence and guards. Obtain the owner decision and required local governance, close consumed choices and refresh the listed task-file refinement, then implement through 043's dependencies. Verify actual source/CI and released content before final candidate closure; execute no target before its authority and gate. Preserve failures, contain only affected scope and requalify with reviewed remediation/fresh authority. Do not overwrite accepted observations or disable gates.

### Owner-local realization packet

The matching exact source scope is published for review in draft [owner PR #583](https://github.com/codeXfactory/codeXfactory/pull/583). Its owning OpenSpec packet must be ratified with the matching coordinating acceptance before implementation. Required hosted checks and actual Codex review remain distinct from source validation; this link supplies no owner consent or target authority.
