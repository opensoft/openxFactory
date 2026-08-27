# Council — systems-architect seat

Status: draft
Round: council, 2026-08-27
Subject: `adopt-council-cleared-merge-gate`, post-alignment draft
**SEAT VERDICT: BLOCK** — ten conditions. **All ten accepted and applied.**

This is the only BLOCK the council returned, and the packet was revised to answer
it rather than to argue with it. The seat's two blocking grounds were explicitly
ones "that text edits cannot reach", and both were resolved by the same act — the
removal of the second candidate class — which the other two seats independently
required on value and security grounds. **That convergence is why the block was
answerable inside one revision.**

## The two blocking grounds

1. **One enrolled class had no traffic, so the change's own safety instrument
   could not complete.** The canary required ≥3 observations in a class whose
   trees have produced zero pull requests in five weeks and, for
   `health/neutrality-drift/`, ever. G7 requires the canary complete, so the flip
   was structurally unreachable.
2. **The boundary as drawn re-admitted a protected comparator**, making it "a
   floor narrowing presented as a boundary, which
   `regular-pr-council-clearance/spec.md:55` forbids outright."

The seat credited the spine as sound: "per-repo self-hosting, App-cast approval,
advisory-first enrollment, gates before acts."

## What the alignment round missed, and this seat caught

**(a) The predecessor class does not exist.**
`openxfactory-derived-health-artifact-advisory-v1` appears **nowhere in
rules-as-code** — only as prose in the **active, unarchived**
`add-classification-intent-and-substantive-classes`, at tasks **7.2 and 7.3, both
unchecked**, where it is merely *"propose[d] … for the Council to accept or
amend"*. Task 7.1 holds Phase 2 outright: "If Phase 1 is refused or amended
beyond the packet's proofs, Phase 2 is void." The draft asserted it was "PREPARED
AND PARKED 2026-08-25" with `state: defined_not_wired` — **attributing a shipped
rules-as-code state to an unchecked task, and claiming succession from an
artifact never authored.** The seat named this "exactly the LS-A3 error the
qa-lead round says this packet was written to prevent", and further noted the
draft's second class was an **unacknowledged Phase-2 expansion in a repository
whose Phase 2 is held**.

**(b) `health/neutrality-drift/**` re-admits a PREV comparator.**
`_has_refused_segment` walks the **pattern**, not changed paths, and the
changed-path test is pure glob — so the broad root validates and then admits
`health/neutrality-drift/baseline/codexFactory.yaml`, **the only file in that
tree**. R5's own comment claims "the roots above are enumerated so a `baseline/`
under them is already refused today" — **true of the xFactory roots and false for
the two openxFactory roots R5 added** on the note that "no class uses them
today". This proposal would have been the first change to open that hole. The
draft meanwhile *claimed* "any `baseline` segment anywhere" is human-only — true
of patterns, false of paths.

**(c) `intent_reference_absent` is opt-in, not automatic.** `:1672` returns
`None` unless the rule declares `requires_intent_reference: true`. The draft
stated the condition applies inherently.

**(d) Three further load-bearing claims about the running system were false** —
mixed-diff arbitration, `check_exclusions`' layer and target, and the pin count.

## Structural findings the seat supplied in the packet's favour

The two-class split was *justified in kind*, with support the proposal had not
cited: `_intent_problem` (`:1672`) requires **both** `approved_scope_ref` and
`feature_id` in the pull-request body, which a bot-generated derived pull request
carries neither of. So `requires_intent_reference: true` is viable for prose and
**structurally fatal for derived** — the classes differ in enforcement, not only
in judgement. The seat's objection was never that two classes was wrong in
principle; it was that the second had no traffic and an unsafe allowlist.

It also confirmed the derived lane's *shape* exists — bot author
`openxfactory[bot]`, stable head refs `doc-health/derive-possibles`,
`doc-health/neutrality-drift`, `intents/rolling`, produced by
`doc-health-reusable.yml` — while the traffic does not.

## Dispositions

1. **SA-C1 — APPLIED by drawing ONE class.** The candidate is fully specified in
   the proposal and in task 3.1: `target_repos`, author matcher,
   `require_same_repository: true` (schema-forced with
   `council_cleared_logins`), a **`head_ref_pattern`** — recorded as the only
   selector `_find_surface` consults — and `check_exclusions`. With one class the
   disjointness and candidate-order requirements do not arise; the proposal
   records them as obligations on any future second class, since first-match-wins
   makes an overlapping second candidate dead code.
2. **SA-C2 — APPLIED.** The mixed-diff claim is **withdrawn** in its own
   proposal subsection and in design D4b. Real semantics stated: no
   cross-candidate arbitration exists; a mixed diff parks on the selected
   candidate's `path_allowlist` overflow. The safety conclusion survives (both
   fail closed); the mechanism was wrong.
3. **SA-C3 — APPLIED.** One gate rule (`applies_to.candidate_id` is singular),
   with every named field enumerated in task 3.4 and design D6b: the `risk_tier.id`
   vocabulary **defined by this change** because `:1263` closes none; explicit
   `anti_normalization` semantics; `activation_dependency`;
   `gate_integrity.never_clearable_paths`; the `council_clearable[]` /
   `docs_class_allowlist` / `clearance_rule` set; and `human.accountable` as a
   **bare login**, since `:1477` refuses the leading `@` every earlier revision
   wrote.
4. **SA-C4 — APPLIED by removal, not narrowing.** `health/neutrality-drift/**` is
   gone entirely; the missing **PR-time `baseline` segment guard** is task 3.7a,
   owed before any derived class is enrolled. The false claim that a `baseline`
   segment is human-only for changed paths is corrected.
5. **SA-C5 — APPLIED.** The succession claim is **withdrawn** in a named
   proposal subsection and design D3b, recorded rather than deleted, with the
   Phase-2 hold stated.
6. **SA-C6 — APPLIED.** `requires_intent_reference: true` is declared for the
   prose class, with its opt-in nature recorded; the derived class's structural
   inability to carry it is recorded as part of why it is deferred.
7. **SA-C7 — APPLIED in four parts.** Distinct approver job id **sharing the
   `merge-master-approval` substring** (so `excluded()`'s substring match still
   covers it, which a wholly distinct id would not — reopening the deadlock);
   `check_exclusions` corrected to a **per-candidate envelope field** listing
   **both** job ids; envelope sequenced **before** approver; and retirement of
   `test_the_caller_ships_no_envelope_instance` owned as task 3.1b.
8. **SA-C8 — APPLIED as task 3.7b**, a named codexFactory change making
   `GATE_INTEGRITY_PROBES` repo-relative, with the explicit instruction **not**
   to resolve the contradiction by silently declining to pass `tree_paths`.
9. **SA-C9 — APPLIED.** Canary re-scoped against measured traffic: prose-only,
   N=3; the derived class deferred to its own change with its own canary.
10. **SA-C10 — APPLIED as task 4.6.** One pin per **repository**, not per
    workflow: the approver shares `contracts/review-lane-pin.yaml` with
    `pinned_members` widened to `council_clearance.py` and `envelope.py` (which
    R1's pin lists neither of), a test asserting every openxFactory core checkout
    resolves the same `core_commit`, and R1's prose `lockstep.obligation` made
    executable **before** a fifth pin surface is added.

## The pin topology, recorded for the successor that will inherit it

Four surfaces today, not three as the draft said, on one clean lineage with **no
cross-surface check anywhere**:

| Surface | Pin | Date |
| --- | --- | --- |
| xFactory `merge-master-approval.yml` + `council-convening-lane.yml` | `3c35ca8b` | 08-21 |
| xFactory gitlink + `review-lane.yml` + test `PIN` | `dc21767` | 08-26 |
| openxFactory R1 `contracts/review-lane-pin.yaml` (unmerged) | `58bd3cf7` | 08-27 |
| codexFactory `origin/main` | `10354e9` | 08-27 |

`58bd3cf7` is 27 commits behind main, none touching `scripts/merge_master/` or
`review-lane-reusable.yml` — **not stale for what it reads.** R1's pin declares
`lockstep: status: diverged` with a prose obligation only. This change adds a
fifth surface, which is why SA-C10 is a condition rather than an observation.
