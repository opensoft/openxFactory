---
code_surface: openxFactory (scripts/ideation_dashboard/gate_console.py — `classify_change_file` gains the outline-restore classification, `execute_demotion_plan` gains the fragment-refresh step and stops byte-replacing a differing destination; a new pure `scripts/ideation_dashboard/round_trip.py` owning the slot fill and the `xspec:` section refresh; tests/ideation-dashboard/test_gate_console.py plus a new test_round_trip.py)
target_release: implementation_pending — the requirement lands now; the change archives only on merged code with green realization evidence, because its whole content is a mechanism correction
Status: draft
Ruling: 2026-08-19 by Brett Heap — draft the 4.2 defect-fix proposal. Scope set to all four parts in one change (status preservation, slot fill, proposal-element refresh, no-silent-overwrite guard).
---

# Proposal: align-demote-to-round-trip-rule

## Why

The demote verb performs precisely the reset the ratified round-trip rule is
titled against.

`docs/document-lifecycle.md` states the rule under the heading **"Round-trip on
demote — the load-bearing rule"**: *"A demoted topic does not reset to its
aspirational text."* The mechanism resets it to exactly that, silently, over the
one file the wheel, doc-health and the doxBench outline tab all read.

This was found by DRIVING the verb, not by reading it — and only by driving it.
A search for the round-trip slot's own field names finds no writer anywhere, which
is what made an earlier review conclude the rule was merely unimplemented. The
fragment is not written by name; it is written by ROUTING:

- `classify_change_file` (gate_console.py:548-549) sends anything under
  `supporting-docs/` back to the topic root under its BARE BASENAME, with a
  `Status: draft` flip.
- `proposal-support.py transition` records the topic's own primary fragment there.
  This repo's own `add-staged-topic-outline-template` manifest carries
  `path: staged-topic-outline-template.md` with `remaining_paths: []`.
- A primary fragment's basename IS `<topic>.md`. So the demote's destination IS
  the primary fragment path.

Driven against the real console and executor, with a fixture fragment carrying
real post-proposal text and a filled round-trip slot, the fragment came back:

- carrying the ASPIRATIONAL snapshot verbatim — the in-flight text gone;
- with all five `## Last proposal attempt` slots gone with it;
- flipped to `Status: draft`, on a file `_primary_fragment` and
  `primaryFragmentPath` still select as the STAGED topic's outline.

**Not a special case.** Of the nine changes carrying a supporting-docs manifest,
two declare a `staged` origin, and both record a file whose basename equals
`<topic>.md` — 2 of 2 would overwrite their topic's primary fragment on demote.
The other seven predate the origin contract and declare none. This is the shape
`transition` produces, so it is the shape every future staged-origin change has.

**Why it has not bitten yet, and why that is luck rather than safety.**
`transition` empties the topic folder on the way out (`remaining_paths: []`), so
the destination is usually ABSENT when the move lands and the restore reads as a
harmless recreation. Leave a fragment behind, or re-stage and work the topic
before a demote, and the identical move overwrites live human work byte for byte
with no diff, no prompt, and no record beyond a README note listing the path.

## What Changes

One requirement on `ideation-dashboard`, carrying four parts. All four are needed
for the mechanism to satisfy the rule; the first three without the fourth would
make a data-loss path more likely to fire, not less.

1. **Status preservation.** A demote move whose destination is the topic's
   declared primary fragment keeps `Status: staged`. A staged topic's outline is
   staged; today it returns as `draft` while the selector still calls it the
   topic's outline, so the corpus's own `status-validity` reader and the wheel
   disagree with the file.

2. **Slot fill.** `execute_demotion_plan` fills the `## Last proposal attempt
   (round-trip provenance)` slots from values it holds at that moment: the change
   id, the demote date, the demote reason, the raised date, and the change's
   status at demote. Where a value is genuinely unavailable the slot says so and
   is never fabricated.

3. **Proposal-element refresh.** The fragment's `xspec:candidate` proposal-element
   sections carry the returned `proposal.md`'s REAL text. This is the rule's whole
   point and the genuinely new surface — the other three parts are corrections to
   an existing move; this one is a capability the mechanism has never had.

4. **The no-silent-overwrite guard.** The supporting-docs snapshot is a fallback
   SOURCE, never the authority. When the destination fragment exists and differs,
   demote MUST NOT byte-replace it: the refresh applies INTO the existing
   fragment, bounded to the slots and the marked sections, and the snapshot is
   preserved beside it rather than discarded. Only where no fragment exists does
   the snapshot restore first.

## Impact

- **Affected capabilities:** `ideation-dashboard` — one ADDED requirement.
- **`Human gate console` is NOT modified.** Its text speaks only of "the proposal
  documents continuing as draft ideas in the topic's `openspec/` workspace" — the
  outline fragment is neither a proposal document nor bound for `openspec/`, so
  nothing there contradicts this behavior. Folding four detailed fragment rules
  into a requirement about the three-action console would overload a requirement
  that answers a different question. Recorded because a reader may expect a
  MODIFIED delta here and its absence is deliberate.
- **The round-trip rule is NOT promoted yet**, and this change does not depend on
  its promotion. The rule lives as an ADDED requirement in the still-active
  `add-staged-topic-outline-template` (`specs/document-lifecycle/spec.md`). This
  change therefore states its behavior on its own terms rather than by reference,
  so it is valid and reviewable whether that change ratifies before, with, or
  after it. No delta is proposed against `document-lifecycle`: the rule needs no
  amendment — the mechanism does.
- **Realizing this unblocks `add-staged-topic-outline-template` task 4.2.** That
  task is the round-trip test, and it is currently blocked because the only
  honest test against today's mechanism would assert the inversion. The test
  stays that change's task, not this one's; this change makes it writable.
- **It corrects a misconception recorded in the ARCHIVED corpus.**
  `openspec/changes/add-doxbench-editing-phase-a/tasks.md:193-194` states the
  round-trip slot "fills on demote only, per the template". Nothing fills it, and
  the same demote deletes it. The correction is recorded HERE; the archived record
  is not edited, because a record amended to agree with a later finding stops
  being a record.
- **Out of scope, and stated so the boundary is not mistaken for coverage:** the
  rule names two triggers — "by the demote verb, or by a failed or reverted
  push". Only the demote verb has an executor; no code path demotes on a failed
  or reverted push. This change corrects the trigger that exists and leaves the
  other exactly as unimplemented as it is today.
- **Not in scope:** any change to `primaryFragmentPath` / `_primary_fragment`
  selection (the one-path rule is preserved, not extended), and any change to the
  plan-versus-execute split — the plan stays pure and snapshot-derived, and a
  human still runs `--execute`.
