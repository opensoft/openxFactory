# Design: relocate-review-authority-floor-mirror

Status: ratified
Ratified by: relocate-review-authority-floor-mirror — 2026-09-08, Brett Heap,
verbatim "ratify 293 and 817 when green, then realize them" (openxFactory #745,
mirrored on codexFactory #232; record `review/ratification-2026-09-08.md`). M-1
through M-7 stand as recommended; no veto entered. MQ-1 is answered — the same
word ratified the codexFactory sibling — and MQ-2 and MQ-3 were not ruled, so
each stands as this document recommends and neither blocks realization (1).
Kind: design

The measurement this packet rests on is the sibling's:
codexFactory `openspec/changes/relocate-review-authority-floor/research/automerge-measurement-2026-09-08.md`.
It is not restated here. Everything asserted about this tree was read at
openxFactory `main` `68712924`.

## 1. The one fact that forces the ordering

`.github/workflows/review-lane-repin.yml:138` declares
`FLOOR_IN_SOURCE: scripts/merge_master/openxfactory-review-authority-floor.yaml`
and `:301` fetches it:

```
gh api "repos/${SOURCE_REPOSITORY}/contents/${FLOOR_IN_SOURCE}?ref=${BRANCH_SHA}"
```

On failure the step writes an empty `path=` output and a `::warning`; the
decision module then returns `Refusal("floor_document_unobtainable", …)`
(`scripts/review_lane_repin.py:377`) and **advances none of the five pinned
sites**. That is the correct behaviour for a missing document and it is kept.

**It is also what every firing would do, forever, from the moment codexFactory
moves the file.** Hence codexFactory D-2 / this packet's M-1: dual acceptance
lands HERE first.

## 2. Why this is a three-site edit and not a one-line one

The constant is duplicated on purpose. `scripts/review_lane_repin.py:65-69`
says why, in the code:

> Restated as a literal rather than read out of the pin, for the reason
> `tests/review_lane_pin/test_floor_snapshot.py` gives about its own copy of
> this constant: a value read from the artifact it is used to check makes the
> check a tautology.

So the live declarations are:

| site | symbol |
|---|---|
| `.github/workflows/review-lane-repin.yml:138` | `FLOOR_IN_SOURCE:` env |
| `scripts/review_lane_repin.py:69` | `FLOOR_IN_SOURCE` |
| `tests/review_lane_pin/test_floor_snapshot.py:80` | `FLOOR_IN_CORE` (used at `:310`, `:350`, `:676`) |
| `tests/review_lane_pin/test_review_lane_caller.py:386` | an inline literal |

and, in realization (3) only, `contracts/review-lane-pin.yaml:517`'s `sources:`
entry — which is a LIVE PIN and must name exactly ONE path, so it moves last
(M-6).

A deliberate duplication needs a **lockstep assertion**, not care. The packet
adds one, over every declaration including the binding's new `source_documents:`
(M-4). That assertion is the thing that makes a two-entry list safe to hold for
a day.

## 3. What "ordered, first-obtained-wins" buys

Realization (1) appends the successor path BELOW the path in force. Until
codexFactory moves, the first candidate always resolves, so **the lane's
observable behaviour is byte-identical to today's** — the widening is provably a
no-op on the day it lands, which is exactly the property that makes it safe to
land ahead of a change in another repository. The day codexFactory moves, the
first candidate 404s, the second resolves, and the run **says so**.

Newest-first would invert that: behaviour would change on the day the list
landed, and the safety argument for landing first would be gone.

## 4. Why the list must not become a feature

Two standing homes means the lane does not know where the document lives, and a
file reappearing at the abandoned path — by a revert, a bad cherry-pick, or an
author who did not read the relocation — would be taken as authoritative and
byte-copied into the snapshot. So the requirement bounds the list to a named,
governed relocation and requires it to return to one entry. Realization (3) is
not tidying; it is the requirement being satisfied.

**And the lane is never taught to search.** Discovery by `kind:
repository_gate_floor`, by basename, or by code search would make any file an
author can plant in codexFactory a candidate for byte-copying into this
repository's witnessed snapshot. An explicit ordered list that fails closed is
the read surface, and M-4 puts it beside the grant that authorizes the read.

## 5. What does not move, and the assertion that proves it

`contracts/review-lane-floor-snapshot.yaml` is a byte copy of the document.
codexFactory D-3 fixes the document's bytes across the move
(`sha256 926d536d9bf5274384710cd9d8170d26b3a41a39108d319eaae76c8311abf3c0`), so
the snapshot's content, its declared `sha256` and its `entry_count` are
identical before, during and after. **The realization asserts that rather than
assuming it**: if the snapshot's digest moves during this migration, what
happened was not a relocation, and the lane should be stopped rather than
followed.

Also unmoved: the LQ-A7 coverage assertion, the byte-identity freshness
verifier, and the pinned core commit. This packet touches no judge.

## 6. Open questions for the ratifying word

* **MQ-1** — does this packet ratify on the same word as codexFactory #293, or
  separately? (It is OQ-3 of that packet.)
* **MQ-2** — M-4: is the binding's `source_documents:` read surface wanted, or
  should the binding stay untouched and the lockstep cover only the code and
  test declarations?
* **MQ-3** — realization (3)'s trigger is "one advance observed against the
  successor path". Is one enough, or should it be one advance plus one clean
  no-op sweep?

## 7. ADDENDUM, 2026-09-09 — a second consumer, and what step (3) could not do

Written at M-1 step (3), against facts that did not exist when § 1–§ 6 were.
Both items are DISCLOSURES: this packet's own enumeration was wrong by one, and
one of its boxes cannot be ticked truthfully yet.

### 7.1 The consumer § 1 missed, because it does not name the document

`code_surface:` says "FIVE sites and no others", and it was arrived at by
finding every place that names the document's PATH. **A sixth consumer finds the
document by SWEEPING A DIRECTORY**, so no path search could have surfaced it:
`.github/workflows/merge-master-approval.yml` step 8 loads every governance
document under the pinned core's `scripts/merge_master`
(`load_governance_paths`) and then picks out the one declaring this repository.

At any core commit after codexFactory's move, that directory holds the two
clearance rules and **no floor**. Measured 2026-09-09, running the shipped step
against real checkouts of both commits:

| core checkout | step 8 as it stood | step 8 as this realization leaves it |
|---|---|---|
| `4b12ba83` (today's pin) | `{"ok": true, "stage": "floor_complete"}` | `floor_complete`, 68 entries, document under `scripts/merge_master/` |
| `8165d1f3` (post-move) | `{"ok": false, "stage": "no_floor"}` | `floor_complete`, 68 entries, document under `floor/` |

`no_floor` exits the step non-zero, so the lane would have **PARKED every
openxFactory merge-master evaluation** from the first pin advance past the
relocation — fail-closed, never a silent approve, but a park whose cause is in
another repository's tidy-up. It is repaired here rather than deferred because
the trigger is a bot's scheduled advance rather than anybody's decision.

**THE REPAIR IS TWO DIRECTORIES, NOT A SEARCH**, which is M-7 applied to a
sweep: the step declares `scripts/merge_master` and `floor` and takes the
declared directories the checkout actually has, so a pin older than the move and
a pin newer than it evaluate identically. Reading both is also STRICTER than
reading either — the core's loader refuses two documents declaring one
repository, so a copy left behind at the abandoned path becomes a loud refusal
rather than a silent choice. codexFactory's own callers took the same shape in
its #297 (`--rule "$RULE_DIR" --rule "$FLOOR_DIR"`); the tolerance for an absent
`floor/` is needed only on this side, because this repository pins an OLDER core
than codexFactory runs against.

### 7.2 M-6 is right and box 4.2 is not yet true

M-6 says the pin "must name a path that exists" and sequences it last. What § 2
did not notice is WHERE it must exist: `contracts/review-lane-pin.yaml` declares
`taken_at: core_commit`, so its `floor_snapshot.of` and its `pinned_members`
entry describe the document **at `core_commit`** — and `core_commit` is still
`4b12ba83`, which predates the relocation. Measured 2026-09-09: the successor
path is `HTTP 404` there.

So step (3) moves what names where the lane FETCHES (the candidate list, its
three sibling declarations) and leaves what names where the PIN carries it. The
pin has not moved because the lane has had nothing to advance: D-3 fixed the
document's bytes across the move, so every firing since has been a no-op, and
`core_commit` advances at codexFactory's next floor REGENERATION. The four
pinned-core declarations move in one diff at that advance, and a test reds from
the advance until they do — the box cannot be lost.
