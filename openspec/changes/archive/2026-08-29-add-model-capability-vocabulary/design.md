# Design: add-model-capability-vocabulary

Status: ratified
Ratified: 2026-08-24 — `review/ratification-2026-08-24.md`

Three decisions and one non-decision, each recorded with what was checked.

## Decision 1 — `text` and `image`, and nothing else

The topic's Q3 disposition left the members to drafting judgement, with one
instruction: keep it minimal and closed, and state the extension rule the way
the roster's `admission_surface` states it.

Two members. `image` because Brett's direction names multi-modal explicitly and
a turn carrying an image is the one consumer that exists. `text` because the
set has to be checkable: a router asking "can this candidate carry what the
turn contains" needs every needed modality present in the declaration, and a
turn always contains text. A set that omitted text would make the common case a
special case in every reader.

Refused: audio, video, tool-calling, structured output, latency class, cost
class. Each is plausible and none has a consumer. The family's own experience
is on the record — the roster's `admission_surface` grew `device` only when the
Opsx node-inventory reader appeared, and its schema states the rule this
requirement mirrors: a member enters with the ratified change that governs it.
The cost of being too narrow is one additive extension. The cost of guessing is
a vocabulary nothing validates against, which is worse because it looks like
governance.

## Decision 2 — optional, with absence carrying no claim

Requiring the field would make every catalog released before it invalid, which
an additive growth must not do. So it is optional — and the interesting part is
what ABSENCE means.

Absence is not "this model rejects images". It is "this producer predates the
field". A reader treats an undeclared entry as text-only FOR ROUTING (the safe
reading: never route an image turn to a model that has not said it accepts
images) while recording that no declaration was made, so a later reader can
tell a conservative default from a stated capability.

This is not invented here. The chat-turn schema already uses exactly this
idiom for handling posture — absence "means a producer older than v1.40" rather
than a posture claim — and reusing the idiom keeps one rule in the reader's
head instead of two.

## Decision 3 — both batched follow-ups TAKEN

Q3 obliged this release to decide them rather than pass them by. Both were
REPRODUCED before deciding, by constructing the offending values against the
real type:

- a 65-entry catalog constructs cleanly, while the released schema caps
  `models` at 64;
- a 200-character `model_id`, and one containing a space, both construct
  cleanly, while the released schema gives the field `maxLength: 128` and a
  character pattern.

Both are the type gate being weaker than the wire gate. This capability has
closed that exact divergence once already, for `routes_to`'s 64-target cap, and
the code records what it cost: a catalog that "constructed fine and could be
dispatched by the turn route... while `GET /workbench/model-catalog` refused to
serve the very catalog holding it". Nothing about that reasoning is specific to
`routes_to`.

N7's deferral reason is the one that decides it. The code says tightening
`model_id` "would be a behaviour change belonging to no release". This is a
release, it opens `$defs/model_entry` anyway, and both fixes are type-side with
no schema bytes — so they ride at no additional release cost. Declining would
mean opening these definitions a third time to do work already in hand.

The honest cost, stated: two constructions that succeed today will fail after
this lands. Both were already unservable over the wire, so what changes is
WHERE they fail, not whether. That is the direction a gate should move.

## Non-decision — the bundle number

Not allocated here, deliberately. The next additive cut is `contract-v1.41`
only if the pending Unreleased block has not folded first, and this repository
has renumbered mid-flight more than once. The number is fresh-counted at
allocation, during realization; a proposal that pre-allocates is how a
renumber becomes a conflict.

## Why ADDED and not MODIFIED

The requirement that governs this catalog — "doxBench model catalog and
provider boundary" — is a single very large requirement carrying seven
scenarios, and `add-doxchat-model-intake` (ratified, unbuilt) ALREADY holds a
live MODIFIED delta on it. A second active change modifying the same
requirement would put two live deltas on one text, which is the hazard worth
avoiding on its own; restating a 177-line requirement to append one clause
would also risk the scenario-preservation defect this session has already had
to fix once elsewhere.

Both new obligations stand on their own terms as requirements. Nothing in the
existing text has to change for them to be true.

## What this change does NOT do

It does not read the field. Choosing a destination by fit — including by
modality — is exit (b), which consumes this vocabulary and carries the routing
behaviour, the no-fit surface and the recorded consent. Landing the vocabulary
first is what lets (b) be designed against a released field rather than a
proposed one, and it is why the topic sequenced this exit first.
