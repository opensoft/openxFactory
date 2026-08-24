---
code_surface: openxFactory (`contracts/schemas/xfactory-workbench-model-catalog.schema.yaml` — one optional closed `modalities` property on `$defs/model_entry`; `scripts/ideation_dashboard/doxbench_model.py` — reading and refusing it, plus the two type-side bound fixes this release takes; `scripts/validate-ideation-dashboard-contracts.py` and the packaged catalog examples; `tests/ideation-dashboard/`). Schema bytes move, so realization is a CONTRACT RELEASE — see "This is a release". No runtime routing behaviour changes: the field is declared and validated here and CONSUMED by exit (b).
target_release: implementation_pending — the requirements land now; realization runs post-ratification and cuts the next additive contract bundle, following the `add-roster-device-admission-surface` precedent for a vocabulary growth. The bundle number is NOT allocated here: it is `contract-v1.41` only if the pending Unreleased block has not folded first, and the allocation is fresh-counted at realization.
---

# Proposal: add-model-capability-vocabulary

Status: draft
Proposed: 2026-08-24, as exit (a) of the staged topic `doxchat-auto-fit-routing`
on the day its six questions were dispositioned. Ratification is a separate
act, still PENDING.

THE REALIZATION RUNS POST-RATIFICATION. No schema, type, validator or example
edit lands with this proposal, and NO BUNDLE IS CUT at proposal time.

## Why

`contract-v1.38` gave the doxBench catalog a routing rule whose resolution is
STATIC: an `auto` entry names the models it may route to and the one it
currently resolves to. Brett's direction at that release's rule-5 ruling was
that the destination should instead be chosen PER TURN by whether the model can
accommodate the turn — and he named a dimension the catalog cannot express:
"if we need multi modal then we have to select from that. so there are other
items besides raw size that will determine the 'best' route."

The catalog can express size. It has `input_limit_bytes` and
`output_limit_bytes`, and they say how MUCH a model accepts. Nothing in the
entry says WHAT KIND. A router asked to keep a turn carrying an image away from
a text-only model has nothing to read, and `provider_class` is a governance
classification rather than a capability — using it would be inferring
capability from a name.

This change adds the one field that gap requires, and stops there.

## What Changes

**One optional, closed capability declaration.** A catalog entry MAY declare
the input modalities it accepts, from a closed vocabulary of exactly `text` and
`image` — enforced at the WIRE as well as in the type, so the schema itself
requires `text` membership rather than leaving a schema-only consumer to accept
an image-only set the type would refuse. Optional and absence-tolerant, because requiring it would break every
catalog released before it: an entry that declares nothing is read as text-only
for routing and recorded as having declared nothing — the same
absence-is-not-a-claim rule the chat-turn family already uses for handling
posture. Where declared, the set must be non-empty and must contain `text`,
since a chat turn always carries text and a model that cannot accept it is not
routable here at all.

**The vocabulary is closed and extends only by the change that governs a new
member** — the rule the client-identity roster already applies to admission
surfaces. `image` enters because a turn carrying an image is the named
near-term consumer. Audio, video, tool-calling, structured output, latency
class and cost class do not enter: nothing consumes them yet, and this family's
experience is that a vocabulary guessed ahead of its consumers is one nothing
validates against.

**Input acceptance only.** Output modality and tool/structured-output support
are different questions with different consumers; one set answering several
would mean different things to different readers.

## The two batched follow-ups — both TAKEN, and why

The topic's Q3 disposition obliged this release to DECIDE the two recorded
catalog follow-ups that touch the same `$defs/model_entry` and the same
construction gate, rather than silently pass them by. Both are taken. Both were
reproduced before deciding:

1. **The entry-count cap is not enforced type-side.** The released schema caps
   `models` at 64; the type does not. A 65-entry catalog constructs cleanly in
   process (verified by construction).
2. **`model_id` is not held to its released bounds type-side (review N7).**
   The schema gives it `maxLength: 128` and a character pattern; the type
   applies those bounds to the id-bearing REFERENCE fields (`routes_to`
   members, `resolved_model_id`) and deliberately not to `model_id` itself. A
   200-character id and an id containing a space both construct cleanly
   (verified by construction).

Both are the SAME DIVERGENCE CLASS this capability has already closed once —
the type gate weaker than the wire gate — and it was closed for `routes_to`'s
64-target cap with a concrete consequence recorded in the code: such a catalog
"constructed fine and could be dispatched by the turn route... while
`GET /workbench/model-catalog` refused to serve the very catalog holding it".
That consequence applies identically here.

N7's own recorded reason for deferral was that "tightening it here would be a
behaviour change belonging to no release". **This is that release.** It touches
`$defs/model_entry` and the entry's construction gate anyway, both fixes are
type-side only, and neither moves a schema byte — so taking them adds no
release surface beyond what `modalities` already brings. Leaving them would
mean opening the same definitions a third time.

## This is a release

Schema bytes move: one optional property on `$defs/model_entry`. Realization
therefore cuts the next ADDITIVE contract bundle and carries the full ritual —
CHANGELOG allocation, manifest row and digest, `contract_bundle_version` bump,
inventory rebuilt AFTER the bump, verify-commit, and the tag at the landing
squash. None of that happens at proposal time.

**The bundle number is deliberately NOT allocated here.** It is
`contract-v1.41` only if the pending Unreleased block has not folded first, and
the number is fresh-counted at allocation. This repository has renumbered
mid-flight more than once, and pre-allocating in a proposal is how that
happens.

## Sequencing

This is exit (a) of three the topic's Q5 resolved to, and it is first because
it is safe:

- **(b) fit-aware routing** — the route-level decision at the step-9 assembly
  point, the no-fit warn/ask surface with its recorded session consent, and the
  turn-record facts including both badges. It CONSUMES this vocabulary.
- **(c) compress-to-fit disclosure and compaction** — a third `reduced_reason`
  constant on the released `contract-v1.40` field, disclosing a fit-reducing
  act that already runs silently, PLUS the real layer-2 compaction the ruled
  behaviour needs when mandatory threads overflow. Plus issue #263's non-blank
  hardening.

**The intake-lane collision is (b)'s, and (a) deliberately avoids it.**
`add-doxchat-model-intake` is ratified and unbuilt, and its own delta MODIFIES
the very requirement that governs this catalog — it touches
`doxbench-chat.js`, `serve.py` and `doxbench_model.py`. This change therefore
ADDS requirements rather than modifying that one, and its code surface is the
schema, the catalog type and the validator only. It changes no route, no
selector and no browser file. Exit (b) is where the two lanes genuinely meet,
and it must be sequenced against the intake build rather than discovering the
same files.

**A constraint (b) inherits, recorded here because it was found while
dispositioning:** request bytes are bounded before assembly and against the
SELECTED entry, so a request sized for a wider `routes_to` member is refused
before routing could choose it. (b) must move or redefine that pre-assembly
bound. It does not affect (a).

## Impact

- **Affected specs.** `ideation-dashboard` — 2 ADDED requirements (the modality
  declaration; the type-enforces-released-bounds rule). Nothing is MODIFIED:
  the requirement that governs the catalog already carries an active MODIFIED
  delta from the intake lane, and a second live delta on one requirement is a
  collision worth avoiding.
- **Consumers re-pin.** codexFactory pins the catalog schema by digest. The
  growth is additive and a consumer may ignore the field, but the pin moves.
- **Two behaviour changes, both refusals that tighten a type toward its own
  released schema.** A 65-entry catalog and an out-of-bounds `model_id` stop
  constructing. Both were already unservable; the change is where they fail.
- **Three parity gaps NAMED but not closed** (surfaced in review): the type
  bounds neither `label` (released `maxLength: 200`), `provider_class` (64) nor
  `data_handling` (500), checking all three only for blankness. Same divergence
  class; recorded as a named follow-up and explicitly excluded from the
  requirement's wording, because the batching obligation named two follow-ups
  and quietly growing that to five is the opposite of deciding each one.
- **The declaration must reach the wire, and that is not automatic.** The public
  projection emits an explicit key list, so the realization has to project
  `modalities` deliberately — following the present-only-when-declared idiom the
  routing fields already use, so an undeclared entry's bytes are unchanged.
- **No routing behaviour changes here.** The field is declared and validated;
  reading it to choose a destination is (b).
