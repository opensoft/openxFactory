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
