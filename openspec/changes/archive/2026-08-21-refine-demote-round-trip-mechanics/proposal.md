---
code_surface: openxFactory (scripts/ideation_dashboard/generator.py — `_change_entry` resolves `origin_staging_id` from the change's own `.openspec.yaml` origin block, taking the first path segment below `ideation/staging/`, and carries `task_progress` through; scripts/ideation_dashboard/gate_console.py — the demote's `openspec/INDEX.md` gains a `Status:` header, every returned governed markdown lacking one is given `Status: draft` through the status-flip decode arm, and the provenance slot carries task progress; scripts/proposal-support.py — the forward transition keeps exactly one `Proposed by:` record, fence-aware and anchored to the status header's block, on shared line/fence primitives; tests/ideation-dashboard/{test_gate_console,test_generator,test_round_trip}.py and tests/proposal-support/)
target_release: implementation_pending — the requirements land now; the change archives only on merged code with green realization evidence, because all four parts are mechanism corrections
Status: ratified
Ratified: 2026-08-19 by Brett Heap — in-session, verbatim: "merge and ratify both", after reading the drafted proposal on PR #218. Same-day scope rulings (in-session multiple choice, all recommended options adopted): Decision 3 (enrich `Status at demote` with task progress) rides this change; Decision 1 (the shallowest-markdown selection arm) is explicitly OUT of scope by the same ruling, deferred until a real topic hits it. Same-day scope ruling (in-session multiple choice, recommended option adopted, 2026-08-19): the returned-artifact half of the whole-folder requirement is realized in this change; the demote adds `Status: draft` to returned governed markdown lacking a header via the sanctioned decode arm; the byte-exact-move reading was rejected as citing no ratified text.
---

# Proposal: refine-demote-round-trip-mechanics

> **REALIZED AND ARCHIVED 2026-08-21.** The code is merged on the implemented
> target as PR #221 (merged 2026-08-20T01:23:54Z, rebase-merge; the branch's
> commits landed on main as `1a7c2a1`, `17bba49`, `8c123bf`, `ca9fcaf`, `6c3d87c`)
> and green there: `openspec validate --all --strict` 64/64 exit 0,
> `tests/ideation-dashboard` + `tests/proposal-support` 3729 passed / 14 skipped /
> exit 0, `tests/doc-health` 691 items with no genuine failure. All four parts are
> built: `generator.py` resolves `origin_staging_id` from the change's own
> `.openspec.yaml` origin block, every governed markdown the demote returns carries
> a `Status:` header, `proposal-support.py` keeps exactly one fence-aware
> `Proposed by:` record per document, and the provenance slot reads the status
> together with the change's task progress. The realization proof is a full LAP on a
> scratch tree — forward, demote, forward again — with the origin resolved from the
> origin block and no operator workaround. Task detail, the gate evidence, and the
> items left open by ruling are in `tasks.md`.
>
> This block REPLACED the release-realization "APPROVED BUT NOT YET REALIZED"
> banner rather than carrying it through the rename, following
> `align-demote-to-round-trip-rule` (archived 2026-08-19), which established that
> precedent for the same reason: archiving a record whose first paragraph says
> "none of it is built" would state something false about a realized change.

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

**Every governed markdown the demote writes into a topic carries a valid
`Status:` header** — its own `INDEX.md`, and equally the `tasks.md`, `design.md`
and spec deltas it returns there, which by OpenSpec convention carry none. So the
topic can be transitioned again without the operator working around an artifact
the demote left. Returned material that already has a header keeps it; the value
added is `draft`, and it is written through the same decode arm the status flip
uses, so a CRLF document does not come back with one LF line in it.

**The forward transition keeps exactly one `Proposed by:` line** — updating the
existing record rather than adding another, collapsing duplicates a document
already carried, ignoring occurrences inside code fences (an example is not a
record), and anchoring the record to the status header's own block rather than to
the first match anywhere in the document.

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
- **The `origin_staging_id` fix widens a snapshot field's provenance**, and the
  scope stated here at proposal time — "the field's value changes for four
  changes" — counted only ACTIVE changes and is off by roughly nine times.
  Corrected by measurement at `8426dbc`: **35 changes gain a value** (the 4 active
  ones that declare a staged origin, plus **31 archived** ones, because the
  generator projects the field uniformly over `changes[]`), and **16 new
  `staged -> change` wheel edges render where 0 rendered before**. The remaining
  19 resolve to topics the forward transition already removed, and
  `wheel-model.js`'s `link()` drops an edge whose endpoint is missing, so none of
  them dangles; the pinned schema types the field `[string, "null"]` with no
  referential constraint.
- **No determinism pin actually moved, and the task that predicted one was
  wrong.** No test in the suite reads `origin_staging_id` against the real
  corpus, and the base-repo fixture change carries no `.openspec.yaml`, so its
  existing pin still resolves through the retained pick-edge fallback. The one
  pin that did move belongs to part 4 —
  `test_a_demote_restores_an_absent_outline_and_refreshes_it` re-derives the
  provenance dict to prove idempotence, and its `Status at demote` value is now
  the enriched one.
- **The whole-folder obligation covers RETURNED artifacts too** (Brett's ruling,
  2026-08-19). The defect stated above as "the demote's `openspec/INDEX.md`
  carries no `Status:` header" is only the first offender in sorted order: the
  forward gate refuses on the FIRST governed markdown without a header, and
  `INDEX.md` sorts before `tasks.md`, which hid the rest. Measured at `8426dbc`:
  93 of 94 `tasks.md`, 154 of 158 spec deltas, 65 of 68 `design.md` and 49 of 94
  `proposal.md` carry no header at all, so nearly every returned change artifact
  blocked the next lap. The demote therefore adds `Status: draft` to any returned
  governed markdown that lacks a header, through the same decode arm the status
  flip already uses, preserving the document's own line-ending flavor. The one
  real demoted topic in the corpus corroborates it:
  `ideation/staging/tier2-council-clearance-pattern/openspec/` carries hand-added
  status headers on its `INDEX.md`, `tasks.md` and `design.md` — an operator
  working around exactly this.
- **The obligation reaches the OUTLINE, and specifically its refresh-in-place
  arm.** An earlier pass of this change declared the outline out of scope on the
  grounds that its source always arrives carrying a header. That is true of the
  snapshot the restore arm applies and FALSE of the live fragment the
  refresh-in-place arm reads — a document the human owns, which never passed the
  forward gate and so never had to acquire one. Demonstrated, not argued: a
  header-less working outline demoted cleanly (`outline_refusal: None`), was
  written back with no header, and left the topic one-way, the next whole-folder
  transition refusing on the fragment itself. The outline's header value is
  `staged`, not the `draft` returned change artifacts get, taken from the same
  expression the restore arm uses; and because the add defers to an existing
  header, a live fragment's own status is still never rewritten.
- **The two gates now read the status header with ONE grammar.** The reverse
  gate's reader (15-row window, fence-blind, prefix match) disagreed with the
  forward gate's (whole document, fence-aware, strict) on **11 of the corpus's
  1133 markdown documents**, in both directions: 10 that the forward gate refuses
  were judged headed by the demote — 7 of them archived-change evidence artifacts
  whose `Status: record · …` and `Status: record (in progress — …)` lines satisfy
  a prefix test — and a real header below row 15 was invisible here, so a SECOND
  one was inserted beside it. After the alignment the two readers disagree on **0
  of 1133**. The strict grammar also stops `_flip_status` overwriting such a line,
  which was silent data loss dressed as a status flip.
