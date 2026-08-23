---
code_surface: openxFactory (dashboard runtime — register_edit_lane module + watch mode, the apply route, the header apply button; tests; runbook)
target_release: none
Status: ratified
Ratified: Brett's "we need to automate that step 2. we need an update button plus a job that watches" on 2026-08-06, with the two-fork ruling (edit+commit+push with pathspec discipline; the serve runs the lane) carried as decided
---

# Proposal: add-register-edit-lane

## Why

Every `project-register-edit` commission (create-project, edit-project) has
so far been fulfilled BY HAND by a terminal session — the accepted interim
posture those verbs shipped with. Brett has now exercised the full loop
(create, add, remove) and ruled the interim closed: "we need to automate
that step 2. we need an update button plus a job that watches."

## What Changes

- ADD the register-edit fulfilment LANE (`register_edit_lane`): scans the
  records tree for dispatched `project-register-edit` descriptors, applies
  each to the aggregation-owned `project-register.yaml` (discovered upward
  from the checkout, comments preserved by surgical block edits), validates
  the result against the pinned schema BEFORE writing, flips the descriptor
  `dispatched → delivered` with structured `delivered_at`/`delivered_by`
  stamps, then commits ONLY the register file (explicit pathspec — the
  shared checkout carries other sessions' work) and pushes with
  pull-rebase-retry. Any refusal or git failure leaves the descriptor
  dispatched and reports; nothing is ever half-applied silently.
- ADD watch mode: the same lane in a polling loop
  (`--watch --interval N`), the "job that watches".
- ADD the apply route + button: a loopback-only, human-gated
  `POST /actions/apply-register-edits` runs the SAME lane code in the
  serve (Brett's ruling: the click is the deliberate human act, and only
  recorded commissions can ever be applied — D2's boundary survives), and
  the header shows "⟳ apply N pending" whenever the projection carries
  pending items under the gate capability.

## Non-Goals

- No new gate verbs and no contract-schema growth (the delivered stamps are
  additive descriptor fields; descriptors are artifacts, not contract
  instances).
- Fulfilment of any OTHER workflow kind (proposal authoring, staging
  fragments, research briefs keep their interim posture).
- Conflict resolution beyond refuse-and-report: a commission the live
  register can no longer satisfy stays dispatched with its reason.

## Impact

- Dashboard runtime only; the aggregation repo is written exactly as the
  hand fulfilments wrote it (same file, same pathspec discipline, same
  commit shape).
