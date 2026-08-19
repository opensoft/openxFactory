---
code_surface: openxFactory (scripts/ideation_dashboard/generator.py — `_change_entry` resolves `origin_staging_id` from the change's own `.openspec.yaml` origin block, and carries `task_progress` through; scripts/ideation_dashboard/gate_console.py — the demote's `openspec/INDEX.md` gains a `Status:` header and the provenance slot carries task progress; scripts/proposal-support.py — the forward transition updates an existing `Proposed by:` line instead of adding a second; tests/ideation-dashboard/test_gate_console.py and tests/proposal-support/)
target_release: implementation_pending — the requirements land now; the change archives only on merged code with green realization evidence, because all four parts are mechanism corrections
Status: ratified
Ratified: 2026-08-19 by Brett Heap — in-session, verbatim: "merge and ratify both", after reading the drafted proposal on PR #218. Same-day scope rulings (in-session multiple choice, all recommended options adopted): Decision 3 (enrich `Status at demote` with task progress) rides this change; Decision 1 (the shallowest-markdown selection arm) is explicitly OUT of scope by the same ruling, deferred until a real topic hits it.
---

# Proposal: refine-demote-round-trip-mechanics

> **APPROVED BUT NOT YET REALIZED.** This change has a non-empty code surface and
> none of it is built: `generator.py` still resolves `origin_staging_id` from pick
> edges alone (the `.openspec.yaml` origin block stays unread), the demote's
> `openspec/INDEX.md` still carries no `Status:` header, `proposal-support.py`
> still appends a fresh `Proposed by:` line per lap, and the provenance slot still
> reads a bare `active`. Under `release-realization`'s archive gate it therefore
> stays ACTIVE as approved intent until its code merges with green realization
> evidence. Nothing here should be read as shipped.

## Why

`align-demote-to-round-trip-rule` made the demote verb stop inverting the
round-trip rule. Driving BOTH gates afterwards — the real forward transition, then
the real demote — turned up three more defects that only a full lap can show, and
Brett's ruling adds a fourth item to the same surface. None of them is the rule
this time; all four are the mechanics around it.

**1. The origin topic is unresolvable for every active change.** `plan_demotion`
refuses without an origin staging topic, and `generator.py` builds
`origin_staging_id` exclusively from possibles-register pick edges — which the
forward transition destroys, because it removes the staging folder those edges point
at. Measured, not inferred: **12 of 12 active changes report
`origin_staging_id: None`**, and the corpus holds exactly **one** pick edge, which
carries no `change_id` at all, so the mapping the generator builds is EMPTY. Every
demote of a real change therefore needs `--staging-topic` typed by hand.

The answer is already on disk and unread. The forward transition WRITES an origin
block into the change's `.openspec.yaml` (`kind: staged`, `id`, `path`), and
`generator.py` already loads that file — `_load_openspec_meta` exists and is called
by `_ratifier_of` alone. The `origin` key is read by nothing.

**2. The demote's own artifact blocks the topic's next forward transition.** A
demote writes `<topic>/openspec/INDEX.md`, and that file carries no `Status:`
header. The forward transition refuses any governed markdown without one, so a
whole-folder transition of a returned topic fails with
`SupportError: governed Markdown lacks Status header` — the demote leaving a
landmine for the next lap of the very cycle it is half of.

**3. `Proposed by:` accumulates one line per lap.** The forward transition rewrites
`Status: staged` into `Status: draft` plus a `Proposed by: <change>` line. The
demote restores `Status: staged` and leaves the `Proposed by:` line alone, so the
next transition adds a second one, and the next a third.

**4. `Status at demote` is a constant (Brett's Decision 3).** `plan_demotion`
refuses any change that is not `active`, so the slot it fills can only ever read
`active`. The realizing change filled it anyway rather than leave `n/a`, and
recorded that the informative value was available: the change's own task progress,
already in the snapshot as `task_progress`.

## What Changes

**Origin resolution gains a precedence order** — explicit `--staging-topic`, then
the change's own `.openspec.yaml` origin block where it declares `kind: staged`,
then the possibles pick edge. Stated as an order rather than a replacement so the
pick edge keeps working where it exists.

Scope stated honestly: this resolves the topic for the **4 of 12** active changes
that declare a staged origin. The other eight declare `ad_hoc` or nothing and have
no staging topic to return to — for those, `--staging-topic` remains genuinely
required, and inventing one would be worse than asking.

**The demote's `INDEX.md` carries a valid `Status:` header**, so the topic it
returns material to can be transitioned again without the operator working around
an artifact the demote itself left.

**The forward transition updates an existing `Proposed by:` line** instead of
adding another.

**`Status at demote` carries the change's task progress** beside its status, from
the snapshot value the executor already holds — `active — 9 of 22 tasks done`.

## Capabilities

### Modified Capabilities

- `ideation-dashboard`: the promoted demote requirement's provenance sentence, for
  Ruling 4 — see the delta decision below.

### New Requirements

- `ideation-dashboard`: origin resolution precedence, and the demote's own
  artifacts not blocking the next transition.
- `document-lifecycle`: the forward transition's `Proposed by:` line is updated
  rather than duplicated.

## Impact

**RULING 4 NEEDS A MODIFIED DELTA, and this is the reasoning.** The promoted
requirement reads: *"SHALL fill the fragment's round-trip provenance slots from
values it holds when it executes — the change id, the date demoted, the demote
reason, the date the change was raised, and the change's status at demote."* That is
a closed list of five values, one of them named "the change's status at demote". A
slot reading `active — 9 of 22 tasks done` carries a SECOND fact, and no reader of
the promoted text could predict that rendering from it. The enrichment also creates
a new unavailability case the promoted sentence must answer — a change with no
`tasks.md` has no progress, and the requirement's own "a value that is genuinely
unavailable SHALL be recorded as unavailable and MUST NOT be fabricated" has to say
what the slot reads then. Both are contract questions, so the delta is MODIFIED
rather than an implementation detail. The alternative reading — that "the change's
status at demote" is loose enough to absorb progress — was considered and declined:
it would make the promoted list mean whatever a later implementation put in the
slot.

**PART 3'S OWNER IS THE FORWARD TRANSITION, NOT THE DEMOTE**, and this correction
matters more than it looks. The obvious place to dedupe `Proposed by:` is the
demote's refresh, since that is what runs when the line comes back. But the promoted
requirement pins the differs-case refresh as *"bounded to the provenance slots and
the marked proposal-element sections, leaving every other byte of that file
unchanged"* — deduping a header line there would break the byte-boundedness
guarantee that makes the refresh safe to run over live human work. The line is
WRITTEN by `proposal-support.py`'s `proposed_content`, so that is where it is
updated instead. The demote's boundedness stays exactly as ratified.

- **Affected capabilities:** `ideation-dashboard` (one MODIFIED, two ADDED) and
  `document-lifecycle` (one ADDED).
- **Decision 1 is explicitly OUT OF SCOPE by the same ruling.** The
  shallowest-markdown arm of the primary-fragment selection rule stays outside
  path-only treatment, deferred until a real topic hits it. Recorded here so a
  reader does not read its absence as an oversight — 0 of the 31 staged topics
  currently reach the fallback arm.
- **Not in scope:** the read-side half of the pseudo-line blindness, which is
  `align-status-reader-to-real-lines` by the same ruling, so doc-health's shared
  reader owns its baseline diff separately.
- **The `origin_staging_id` fix widens a snapshot field's provenance**, so
  `test_snapshot*.py`'s determinism pins are part of the surface: the field's value
  changes for four changes, and that is a deliberate, asserted move rather than
  drift.
