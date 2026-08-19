# Design: align-demote-to-round-trip-rule

Status: draft

The requirement says what must be true. This says how, and records the decisions
that could reasonably have gone the other way.

## Decision 1 — the outline destination is identified in the PURE PLAN, path-only

`plan_demotion` is pure and snapshot-derived; `execute_demotion_plan` does the
I/O. The plan is also the reviewable artifact a human reads before running
`--execute`, and it is written to disk as `demote-<stamp>.plan.yaml`.

So the plan decides which move is the outline, and it decides it PATH-ONLY: a
`FileMove` whose `to_path` equals `<topic_path>/<topic>.md`. `FileMove` gains a
flag (or its `role` gains an `outline-restore` value) and the plan therefore SAYS
which file will be treated as the topic's outline, before anything is written.

Rejected: deciding at execute time by resolving the primary fragment against the
real tree. It would be more general (see the narrowing below) but the plan would
stop describing what execution will do, which is the plan's whole job.

**The narrowing, stated.** `primaryFragmentPath` has two arms: the exact
`<topic>.md`, ELSE the shallowest markdown file. Only the first arm is decidable
from paths alone; the second depends on what else is in the topic folder at
execute time. This change covers the exact-name arm, which is what both real
staged-origin manifests produce and what `transition` writes. A returning
markdown that becomes primary only by being shallowest is NOT covered, and is
left as a known bound rather than half-handled. Worth a follow-up ruling; not
worth guessing here.

## Decision 2 — a new pure module, not more of `gate_console.py`

The slot fill and the `xspec:` section refresh are markdown surgery: fence-aware
scanning, bounded in-place rewriting, EOL preservation. That is a different kind
of code from gate_console's planning and recording, it is the part most worth
unit-testing without a tree, and gate_console.py is already ~1250 lines.

New `scripts/ideation_dashboard/round_trip.py`, pure — text in, text out, no
paths, no I/O. `execute_demotion_plan` reads bytes, calls it, writes bytes.

**Known duplication, named on purpose.** `outline-model.js` already implements
fence-aware section scanning and section INSERTION for the doxBench outline tab,
and `doc_health/families.py` implements the fence-aware heading scan for the
`staged-topic-template` family. This module is a third implementation of the same
fence rule, in the same corpus, and that is exactly the "change both together or
neither" hazard the template family already carries. Mitigation: a test that pins
the three agreeing on a shared fixture set, in the spirit of the existing
`test_the_model_and_the_doc_health_family_agree_on_the_contract`. Sharing the code
is not available — one side is JavaScript in the browser bundle.

## Decision 3 — where each provenance value comes from

`execute_demotion_plan` holds the plan and `at`. Per slot:

| Slot | Source | Notes |
|---|---|---|
| `Change ID` | `plan.change_id` | always available |
| `Demoted` | `at[:10]` | the same value the README note already uses |
| `Demote reason` | `plan.reason` | non-empty by `plan_demotion`'s own refusal |
| `Raised` | the change's supporting-docs manifest `transitioned_at` | the date the topic transitioned INTO the change |
| `Status at demote` | the change's snapshot `status` | see the flag below |

**`Raised` has a read-order constraint.** `supporting-docs/manifest.yaml` is
itself a returning supporting-doc (`classify_change_file` sends it to
`<topic>/manifest.yaml`), and the change folder is removed at the end of
execution. So the manifest must be read BEFORE the moves run. Where a change has
no manifest — seven of the nine changes that have one predate the origin
contract, and most changes have none at all — `Raised` is recorded as unavailable,
never guessed from the folder's archive-date prefix or from a file mtime.

**`Status at demote` — flagged as low-information.** `plan_demotion` REFUSES any
change whose snapshot status is not `active`, so this slot can only ever read
`active` under the current precondition. It is still filled, because a slot
reading `n/a` after a real demote is worse than one reading a true constant, and
because a future widening of the precondition would make it informative without a
second change. If Brett wants the slot to carry something a reader can act on, the
available candidate is the change's `task_progress` from the snapshot — say so and
it goes in; it is deliberately not assumed here.

## Decision 4 — the no-silent-overwrite mechanics

Three cases for the one outline move. Everything else in `execute_demotion_plan`
is unchanged.

**(a) Destination absent.** Restore the snapshot bytes, then refresh. This is
today's behavior plus the refresh, and it is the ordinary case because
`transition` empties the topic folder on the way out.

**(b) Destination present and byte-identical to the snapshot.** Treated as (a).
There is nothing to lose, and routing it through the "differs" path would produce
a preserved-snapshot copy of a file identical to the one beside it.

**(c) Destination present and DIFFERS.** The destination is the authority.

- The snapshot is NOT written to the destination.
- The refresh applies INTO the existing fragment: the provenance slots and the
  marked proposal-element sections, and nothing else. Every other byte survives.
- The snapshot is preserved in the topic as
  `<topic>.snapshot-<change-id>.md`, so "never byte-replace" does not quietly
  become "silently discard the other copy".
- The README note and the transition manifest both say the snapshot was PRESERVED
  rather than applied, and name the file. A human who wanted the snapshot's text
  can see it and merge it themselves; what the mechanism will not do is decide
  that for them.

The preserved copy is deliberately NOT `<topic>.md.orig` or a dotfile: it must be
visible to the corpus readers (doc-health, the wheel) as an ordinary extra topic
file, because a hidden artifact in a governed folder is how material goes missing.
It carries `Status: draft` — it is a snapshot of a proposal-era document, not the
topic's outline.

## Decision 5 — the refresh is a bounded, addressed write

Two operations, both fence-aware, both preserving the document's own line endings
(the `_flip_status` P3 lesson generalizes: a bounded write must not retranslate
the document it touches).

**Slots.** Locate the `## Last proposal attempt (round-trip provenance)` section
outside code fences and rewrite its `Field: value` lines in place. If the section
is ABSENT — which is the case for most of the corpus, since template conformance
is opt-in — it is INSERTED in the template's canonical position (first section
after the header block), exactly as the outline tab's own add-section affordance
would place it. Inserting a section the topic did not have is a real content
change and is why this is a demote-time act rather than something doc-health
should do: it happens because a human ran a gate verb.

**Marked sections.** For each `## ` section in the fragment wrapped in
`<!-- xspec:candidate ... -->`, find the same heading (case-insensitive) in the
returned `proposal.md` and replace the text INSIDE the fence with that section's
body. The marker comments themselves are never rewritten — they are the addressing
key, and rewriting an addressing key mid-operation is how the two sides stop
agreeing.

Sections in the fragment with no counterpart in the proposal are left alone.
Sections in the proposal with no counterpart in the fragment are NOT added: the
fragment's marked set is the human's declaration of which elements this topic
carries, and demote is not the moment to widen it.

**Idempotence** falls out of both operations being addressed rather than
appending: the slots are overwritten with the same values, the fenced bodies with
the same text.

## Decision 6 — the returned `proposal.md` is read from its DESTINATION

The refresh source is the returned proposal, which the same execution has just
moved to `<topic>/openspec/proposal.md`. Reading it from there rather than from
the change folder before the move means the refresh uses the durable artifact a
human can still open afterwards, and it keeps the read order simple: moves first,
then refresh, with the manifest read (Decision 3) as the one thing that must
happen before them.

## What is deliberately not designed here

- Any demote-on-failed-push path. The rule names that trigger; no executor
  exists; this change does not invent one.
- Any change to the plan/execute split, the gate-action record shape, or the
  refusal preconditions.
- Any migration of the corpus's existing non-conforming fragments. Conformance
  stays opt-in; this change only governs what a demote leaves behind.
