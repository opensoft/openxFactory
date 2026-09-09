---
code_surface: openxFactory — FIVE sites and no others. `.github/workflows/review-lane-repin.yml` (the `FLOOR_IN_SOURCE:` env at `:138` and the fetch step at `:292`–`:310`) and `scripts/review_lane_repin.py` (the `FLOOR_IN_SOURCE` constant at `:69` and the `floor_document_unobtainable` refusal at `:377`) each become an ORDERED LIST of candidate paths rather than one path; `contracts/review-lane-repin-binding.template.yaml` gains an enumerated `source_documents:` read surface under `privileges.source_repository`; `tests/review_lane_pin/test_repin_lane.py`, `test_floor_snapshot.py` (its own `FLOOR_IN_CORE` copy at `:80`, used at `:310`, `:350` and `:676`) and `test_review_lane_caller.py` (`:386`) carry the list and a lockstep assertion; and, in the SECOND realization only, `contracts/review-lane-pin.yaml`'s `sources:` entry at `:517` advances to the new path. NOT THIS CHANGE'S SURFACE, each for a stated reason: `contracts/review-lane-floor-snapshot.yaml` is a BYTE COPY and the bytes do not move, so its content, its `sha256` and its `entry_count` are all unchanged (codexFactory D-3); the LQ-A7 coverage assertion and the byte-identity freshness verifier are the JUDGE of the bot's pull request and are left exactly as they are; and NO codexFactory FILE IS EDITED HERE — codexFactory authors its own floor and its own move.
target_release: a code surface, so per `release-realization` it archives only on merged + green realization evidence. The evidence is FOUR things: the dual-path realization landed with `tests/review_lane_pin/` green; ONE re-pin run observed green against the OLD path with dual acceptance in place (proving the change is a WIDENING and not a swap); codexFactory's move landed; and ONE re-pin run observed green against the NEW path, after which the second realization drops the old path. No contract bundle is involved — no registered contract row, no digest set, no `contract_bundle_version` and no release tag.
sequenced_after: [mirror-floor-regeneration-automation, codexFactory:relocate-review-authority-floor]
---

# Proposal: relocate-review-authority-floor-mirror

Status: ratified
Ratified: 2026-09-08, Brett Heap (openxFactory repository owner), in session,
verbatim **"ratify 293 and 817 when green, then realize them"** — recorded
2026-09-08T23:51Z on openxFactory issue #745 and mirrored on codexFactory issue
#232, applied over PR #817 on the condition that its checks be green. **THEY
WERE NOT WHEN THE WORD WAS GIVEN, AND THAT IS RECORDED RATHER THAN SMOOTHED**:
`pytest-suite` was red for two causes, both this packet's own — an undeclared
sibling-pairing on the `## MODIFIED` block, and a missing corpus-ledger row —
and both were fixed in the packet, never in a test, before this header was
written. **M-1 THROUGH M-7 STAND AS RECOMMENDED — no veto was entered.**
**NOTHING IS REALIZED BY THE RATIFICATION**: *"then realize them"* is a SECOND
act in the same word, and this repository's step (1) is the FIRST realization of
the pair — codexFactory's move may not be opened before it. **THE SAME WORD
RATIFIED THE SIBLING** `codexFactory:change:relocate-review-authority-floor`
(codexFactory #293), which answers MQ-1: the same word, not separately.
**BOXES 1.3 (MQ-2) AND 1.4 (MQ-3) ARE NOT RULED BY THIS WORD** and neither
blocks realization (1). Record `review/ratification-2026-09-08.md`.
Proposed: 2026-09-08
Origin: codexFactory issue
[#232](https://github.com/opensoft/codexFactory/issues/232), mirrored on
openxFactory issue
[#745](https://github.com/opensoft/openxFactory/issues/745). Brett Heap ruled
shape 1 of the finding-(3) STOP report on 2026-09-08T13:49:30Z, verbatim
**"rule shape 1, measure first, this lane realizes it"** (comment 5586188401).
The codexFactory sibling `relocate-review-authority-floor` (pull request
[#293](https://github.com/opensoft/codexFactory/pull/293), DRAFT) names this
packet as its owed companion in **decision D-7** and sequences it FIRST in
**decision D-2**. **No separate openxFactory governing issue is filed**: #745 is
the mirror of #232 and is cited in both repositories, following the same
practice `mirror-floor-regeneration-automation` recorded.
**THE RULING RATIFIES NO TEXT.** Whether this packet's words are the right
dual-path acceptance is Brett Heap's separate act.

## Why

This repository's re-pin lane fetches codexFactory's authoritative floor
document **by path**:

```yaml
FLOOR_IN_SOURCE: scripts/merge_master/openxfactory-review-authority-floor.yaml
…
gh api "repos/${SOURCE_REPOSITORY}/contents/${FLOOR_IN_SOURCE}?ref=${BRANCH_SHA}"
```

and, when that 404s, `scripts/review_lane_repin.py` refuses with
`floor_document_unobtainable` and advances none of the five pinned sites. That
refusal is correct and stays. **But codexFactory is about to move the document**,
and on the day it does, this lane's every firing becomes that refusal.

The constant is duplicated **deliberately** — the workflow env, the script's
`FLOOR_IN_SOURCE`, and `tests/review_lane_pin/test_floor_snapshot.py`'s own
`FLOOR_IN_CORE`, each a literal, for the reason the code writes down: *"a value
read from the artifact it is used to check makes the check a tautology."* So
the widening is a three-or-more-site edit by construction, and it needs a
lockstep assertion rather than care.

## What changes

`FLOOR_IN_SOURCE` becomes **an ordered list of candidate paths**, tried in
order, with the FIRST one obtained winning:

1. `scripts/merge_master/openxfactory-review-authority-floor.yaml` (today's)
2. `floor/openxfactory-review-authority-floor.yaml` (codexFactory D-1's)

The lane refuses `floor_document_unobtainable` only when **none** of them
resolves — so the refusal keeps its meaning and gains no exemption. When
codexFactory's move has landed and one full cycle has run green against the new
path, a second realization deletes entry (1) and the list is one path again.

**THE LIST IS A MIGRATION WINDOW, NOT A PERMANENT FEATURE.** A standing list of
two paths would mean the lane no longer knows where the document lives, and a
document silently reappearing at the abandoned path would be read as
authoritative. So the requirement below bounds it: the list SHALL be ordered,
SHALL be short-lived, SHALL name the governed relocation that opened it, and a
firing that resolves anything but the FIRST entry SHALL say so in its report.

## Impact

- **Affected specs:** `review-lane-floor-mirror` — ONE requirement MODIFIED
  (*"The automated advance re-copies the vendored snapshot and recomputes its
  witnesses from the bytes it wrote"*).
- **Affected code (realization only, not this pull request):** the five sites in
  `code_surface:` above, across TWO realizations.
- **Affected repositories:** openxFactory here; codexFactory by its own sibling,
  which lands BETWEEN this packet's two realizations.
- **Not affected:** `contracts/review-lane-floor-snapshot.yaml`'s content, its
  `sha256` or its `entry_count`; the LQ-A7 coverage assertion; the freshness
  verifier; the pinned core commit; and every codexFactory file.

## Decisions

Each is a recommendation; **M-1 is a safety ordering rather than a preference.**

**M-1 — the two realizations bracket codexFactory's move, and the order is not
negotiable.** (1) this repository accepts BOTH paths → (2) codexFactory moves →
(3) this repository drops the old path. Between (1) and (3) the lane can resolve
the document wherever it is, so no window exists in which it 404s. Realization
(1) MUST land before codexFactory #293's realization is opened; realization (3)
MUST NOT land until one re-pin run has been observed green against the new path.

**M-2 — an ORDERED list, first-obtained-wins, and the order is the migration
direction.** Old path first during the window, so that the lane's behaviour is
byte-identical to today's until codexFactory actually moves — realization (1) is
then observably a no-op, which is what makes it safe to land ahead of anything
else. After the move, realization (3) leaves the new path alone at the head.
**Not** newest-first, which would change behaviour on the day it landed rather
than on the day the document moved.

**M-3 — the refusal keeps its identifier and its meaning.**
`floor_document_unobtainable` fires when EVERY candidate fails, and its message
names every path tried. It does not gain a variant, and no other refusal is
introduced: a lane that cannot find the document still advances nothing.

**M-4 — the binding template gains an enumerated `source_documents:` read
surface, and it is documentation with a lockstep test, never an input.** The
binding at `contracts/review-lane-repin-binding.template.yaml` today declares
WHICH repository the lane reads (`privileges.source_repository`,
`grants: [contents:read]`) but not WHAT it reads. Adding the ordered path list
there makes the read surface reviewable in the same document as the grant. **The
workflow and the script SHALL NOT read the list from the binding** — that is
exactly the tautology the existing code comments refuse — so a test asserts the
three declarations agree, the same shape as the existing two-site lockstep.
*Alternative, if this is unwanted:* leave the binding untouched and keep the
lockstep over the workflow, the script and the two test constants; the packet
loses nothing but the reviewability.

**M-5 — nothing about the snapshot changes, and the realization proves it.** The
document's bytes do not move (codexFactory D-3, `sha256`
`926d536d9bf5274384710cd9d8170d26b3a41a39108d319eaae76c8311abf3c0`), so
`contracts/review-lane-floor-snapshot.yaml` is byte-identical across the whole
migration. The realization asserts that rather than assuming it: **if the
snapshot's digest moves during this migration, something other than a relocation
happened.**

**M-6 — `contracts/review-lane-pin.yaml`'s `sources:` entry advances in
realization (3), not (1).** It is a LIVE pin naming the file it digests, and it
must name exactly one path. Advancing it in (1) would point it at a path that
does not yet exist; advancing it in (3) is the last act of the migration. Its
NARRATIVE mentions of the old path elsewhere in that file are history and are
left (codexFactory D-4).

**M-7 — the lane is NOT taught to discover the document.** A search — by
`kind: repository_gate_floor`, by basename, by code search — would let a file
appearing anywhere in codexFactory be read as authoritative. The list is
explicit, ordered, and short. **An explicit list that fails closed is the whole
point.**

## What this pull request does NOT do

It edits no workflow, no script, no contract and no pin byte of the lane, and it
edits nothing in codexFactory. Two files outside the packet do move, and both
are gate bookkeeping this packet owes rather than behaviour it changes: the
`## MODIFIED` block's sibling-pairing marker, and the corpus-ledger row seeded
by `validate-sequenced-after.py --seed-ledger`. **THE RATIFICATION OF 2026-09-08
TICKS FOUR BOXES AND NO OTHERS** — 1.1, 1.2, 5.1 and 5.2, each because that
box's own stated condition is the ratifying word or the ratifying commit — and
every remaining box, 1.3 (MQ-2) and 1.4 (MQ-3) included, is untouched by merging
this.
