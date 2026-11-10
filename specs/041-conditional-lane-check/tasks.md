# Tasks: Conditional Lane Check

Status: draft

## Phase 1: Governance and setup

- [X] T001 [O] Record the in-force rule, owner commissioning, delta and feature handoff; files: openspec/changes/honor-conditional-lane-attribution/**, specs/041-conditional-lane-check/**; verify: openspec validate honor-conditional-lane-attribution --strict

## Phase 2: US1 and US2

- [X] T002 [O] [US1] Accept absent declarations and retain strict supplied-declaration validation without changing bot behavior; files: .github/workflows/lane-line.yml; verify: python3 -m pytest tests/lane_line/test_conditional_lane_line.py -q
- [X] T003 [S] [US2] Exercise the exact workflow shell for absent, valid, malformed, duplicate, misplaced and inert-input cases; files: tests/lane_line/test_conditional_lane_line.py; verify: python3 -m pytest tests/lane_line/test_conditional_lane_line.py -q

## Phase 3: Verification and landing

- [X] T004 [O] Reconcile measured admission counts where applicable and record actual source-check results; files: tests/merge-master/test_tree_floor_probe.py (codeXfactory only), specs/041-conditional-lane-check/evidence.md; verify: affected tests pass; hosted checks remain a landing condition
Landing evidence will be recorded on the integration PR after its exact-head review and required checks complete. This lifecycle condition is not a second implementation list.

Dependencies: T001 precedes implementation; T002 and T003 jointly verify US1/US2; T004 follows their passing result; landing follows all required review and hosted checks. Single-session execution is sufficient. No parallel work is required.
