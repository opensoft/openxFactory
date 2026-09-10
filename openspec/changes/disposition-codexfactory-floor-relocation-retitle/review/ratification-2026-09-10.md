# Proposal Ratification: disposition-codexfactory-floor-relocation-retitle

Status: ratified
Kind: report
Decision date: 2026-09-10
Ratifier: Brett Heap (openxFactory convener)
Ratified: 2026-09-10 by Brett Heap (openxFactory convener) — verbatim "go A, ratify the disposition entry as encoded", recorded at https://github.com/opensoft/openxFactory/issues/745#issuecomment-5619833296

## Decision

RATIFIED by Brett Heap.

## The word, and why one sentence is both halves

Brett Heap's instruction, verbatim: **"go A, ratify the disposition entry as
encoded"** — given 2026-09-10 at approximately 14:0xZ, in his own message,
first-hand to Claude session `504bd370`, lane `openxfactory-2` (display
`openXfactory-2`), which authored this packet and writes this record.

**IT CARRIES THE EXIT AND THE TEXT AT ONCE, AND THE TWO CLAUSES DO DIFFERENT
WORK.** *"go A"* answers the question this lane put — the fork posted after
codexFactory #318's phase 2, whose option A was to DISPOSITION the residual
scenario-currency finding in the fleet pin rather than restore the superseded
scenario or hold the archive. *"ratify the disposition entry as encoded"*
ratifies THIS PACKET'S TEXT, against the entry as this packet encodes it, with
"as encoded" naming the encoding rather than inviting one. This differs
deliberately from `disposition-codexfactory-declared-renames`, which needed two
words on one day — *"use recommended name, go on 3 repo shape"* for the plan and
then *"ratify 697"* for the text. Here there is one sentence and one act, so
every document in this packet carries `Status: ratified` from the commit that
writes it rather than passing through `draft`.

The same word is recorded on codexFactory
[#232](https://github.com/codeXfactory/codexFactory/issues/232#issuecomment-5619832944),
the consuming repository's own governing issue, because the finding it disposes
is codexFactory's.

## What this ratification covers

* **The THIRD `repo: codexFactory` entry** in
  `contracts/openspec-cli-pin.yaml` — `item: relocate-review-authority-floor`,
  `path: repository-gate-floor/spec.md`, `level: ERROR`, accepting one
  ERROR-level finding by its whole message, with eight citations, a `why:` that
  states the retitle and what restoring the old title would reinstate, and a
  `retires_when:` naming the archive of the codexFactory change and the tree
  that refuses on that day. The four standing entries are untouched by this
  packet and are ratified by **"take exit 2"** (#677) and **"ratify 697"**
  (#697), not by this word.
* **The pin's header prose**, brought back into agreement with a five-entry
  list, and one new dated paragraph recording how the third codexFactory
  finding arrived.
* **The delta-less shape.** `.openspec.yaml` declares `skip_specs: true` and the
  packet writes no spec delta, on the reading recorded in `design.md` § 3:
  promoted `neutral-product-pin` already states that a disposition is scoped to
  one repository, that an entry naming another is neither applied nor stale,
  and that an entry refuses when its change archives. The precedent's ORDERING
  objection has expired — the requirement is promoted now — and is not reused;
  the reason recorded is that there is nothing in the rule to modify.
* **The two test movements**: the count-pinning test 4 -> 5 with its
  per-repository split kept, and the per-entry citation/authority test tightened
  from shared literals to per-item maps.

## Order of events

1. codeXfactory/codexFactory PR #318 (head `32743fb7`) archived
   `add-floor-regeneration-automation` and promoted the requirement, and its
   `validate` run 34481981940 read the one residual strict finding.
2. This lane measured that finding through openxFactory's pinned entrypoint over
   a read-only clone of #318's tree and posted the fork to Brett Heap.
3. Brett Heap gave **"go A, ratify the disposition entry as encoded"**.
4. The lane claimed the work on #745 and #232 (comments 5619833296 and
   5619832944) and authored this packet, ratified from the first commit.

**THE MERGE HAS NOT HAPPENED AND IS NOT AUTHORIZED BY THIS WORD.** It follows on
a separate merge word, performed by the orchestrator under lane-collision
Rule 6.

## Limits — what this word does NOT ratify

* **Any codexFactory act.** Not the reserved `Merged into` marker on the
  relocate block — which LANDED separately as codexFactory PR #339 → main
  `9b1b0a21`, on this same word, in codexFactory's own pull request and not by
  this ratification — not the advance of codexFactory's declared openxFactory
  pin to this change's merge commit, and not the archive of
  `relocate-review-authority-floor` or of anything in #318. Each is
  codexFactory's, in codexFactory's own pull request.
* **codexFactory #318's `validate` going green.** This entry removes ONE
  reason that gate is red. Whether others remain is codexFactory's verdict.
* **The archive of this change**, or of the change its disposition names. When
  `relocate-review-authority-floor` archives, **codexFactory's** run refuses
  `pin-disposition-stale` until this entry is deleted; `retires_when:` says so.
* **Any tick in another packet.** Nothing in
  `relocate-review-authority-floor-mirror` or
  `mirror-floor-regeneration-automation` is ticked by this ratification.
* **The upstream fix.** `Fission-AI/OpenSpec#1793` is filed, not fixed;
  `tasks.md` 5.5 is the open box that says who is watching (nobody, yet).

## Where the measurements are

Not here. Every run, exit code and total this packet rests on is captured
verbatim in `evidence/codexfactory-floor-relocation-2026-09-10.md`, which is a
`record`. A ratification record states the act and its authority; a measurement
that changed under it would make the record disagree with itself.
