# Tasks: relocate-review-authority-floor-mirror

Status: ratified
Ratified by: relocate-review-authority-floor-mirror — 2026-09-08, Brett Heap,
verbatim "ratify 293 and 817 when green, then realize them" (openxFactory #745,
mirrored on codexFactory #232; record `review/ratification-2026-09-08.md`)
Kind: tasks

`code_surface: openxFactory`, `target_release:` a code surface — so under
`release-realization` this packet archives on merged-plus-green realization
evidence and not on landing.

**THIS PULL REQUEST PERFORMS NOTHING BUT THE PROPOSING AND THE RATIFYING.** No
workflow, script or contract byte of the LANE is edited and nothing in
codexFactory is touched. Two files outside the packet DO move, and both are
gate bookkeeping this packet owes rather than behaviour it changes: the
`## MODIFIED` block's sibling-pairing marker, and the corpus-ledger row seeded
by `python3 scripts/validate-sequenced-after.py . --seed-ledger --moved-by '#817'`.

**RATIFIED 2026-09-08, AND IT TICKS FOUR BOXES AND NO OTHERS: 1.1, 1.2, 5.1 AND
5.2.** Each names the ratifying word or the ratifying commit as its own tick
condition. **1.3 (MQ-2) AND 1.4 (MQ-3) STAY OPEN** — each asks for a word
choosing between named options and the word of 23:51Z chose neither; neither
blocks realization (1). **§ 2, § 3 and § 4 stay open**, each on the act it
already names. **THE REALIZATION IS IN TWO PARTS THAT BRACKET ANOTHER REPOSITORY'S
LANDING** (M-1), and the boxes are grouped that way so a reader cannot mistake
one for the whole. **THE NUMBERING BELOW IS M-1'S, NOT A SECOND SCHEME**: M-1's
three steps are (1) this repository accepts both paths, (2) codexFactory moves,
(3) this repository drops the old path — so this repository performs TWO
realizations, at M-1 steps (1) and (3), and § 3 is another repository's act
standing between them as this packet's gate.

## 1. The word

- [x] 1.1 Brett Heap ratifies this packet. **Ticks on:** a recorded verbatim
      word on openxFactory #745 (mirrored on codexFactory #232) naming this
      packet, over a named head, required checks green, zero unresolved threads,
      and a `review/ratification-<date>.md` record landing with it.
- [x] 1.2 MQ-1 answered — same word as codexFactory #293, or separate.
      **Ticks on:** the ratifying word saying which.
- [ ] 1.3 MQ-2 answered — the binding's `source_documents:` read surface (M-4)
      stands or is vetoed. **Ticks on:** the same word.
- [ ] 1.4 MQ-3 answered — what triggers M-1 step (3), this repository's second realization. **Ticks on:** the same
      word; the default if none is given is M-1's "one advance observed against
      the successor path".

## 2. M-1 step (1) — this repository's FIRST realization: dual-path acceptance, landing BEFORE codexFactory moves

- [ ] 2.1 `.github/workflows/review-lane-repin.yml` declares the ORDERED
      candidate list, old path FIRST, and the fetch step tries each in order.
      **Ticks on:** the merged commit.
- [ ] 2.2 `scripts/review_lane_repin.py` takes the same ordered list and returns
      `floor_document_unobtainable` only when EVERY candidate fails, naming
      every path tried (M-3). **Ticks on:** the same commit.
- [ ] 2.3 The run reports WHICH candidate resolved, and says nothing about a
      migration when it was the first. **Ticks on:** the same commit plus one
      observed run.
- [ ] 2.4 M-4 (if it stands): `contracts/review-lane-repin-binding.template.yaml`
      gains `source_documents:` under `privileges.source_repository`, and the
      lane does NOT read it at run time. **Ticks on:** the same commit.
- [ ] 2.5 The lockstep assertion lands: every declaration of the list — workflow
      env, script constant, `test_floor_snapshot.py`'s `FLOOR_IN_CORE`,
      `test_review_lane_caller.py`'s literal, and the binding if 2.4 stands —
      carries the SAME ordered list. **Ticks on:** the new test green.
- [ ] 2.6 A negative control proves the lane still refuses when NO candidate
      resolves, and does not silently pass. **Ticks on:** the control green.
- [ ] 2.7 **The no-op is proven, not asserted**: one re-pin run observed green
      against the OLD path with dual acceptance in place, resolving candidate
      one and reporting no migration. **Ticks on:** that run.

## 3. M-1 step (2) — codexFactory's move: not this packet's act, but this packet's gate

- [ ] 3.1 codexFactory `relocate-review-authority-floor` is ratified and its
      realization lands, moving the document to
      `floor/openxfactory-review-authority-floor.yaml`. **Ticks on:** that merge.
      **§ 4 MUST NOT BEGIN BEFORE THIS BOX IS TICKED.**
- [ ] 3.2 One re-pin run observed green against the NEW path — candidate one
      404s, candidate two resolves, and the run reports the migration.
      **Ticks on:** that run.
- [ ] 3.3 M-5 proven: `contracts/review-lane-floor-snapshot.yaml`'s content,
      `sha256` and `entry_count` are unchanged across the whole migration.
      **Ticks on:** the comparison recorded on #745.

## 4. M-1 step (3) — this repository's SECOND realization: the list returns to one entry

- [ ] 4.1 The superseded path is removed from every declaration; the list
      carries one path. **Ticks on:** the merged commit.
- [ ] 4.2 `contracts/review-lane-pin.yaml`'s `sources:` entry advances to the
      new path (M-6); its narrative mentions of the old path are LEFT.
      **Ticks on:** the same commit, and a diff showing the narrative untouched.
- [ ] 4.3 One re-pin run observed green with the single new path.
      **Ticks on:** that run.

## 5. Bookkeeping

- [x] 5.1 This packet is listed in the README's OpenSpec Records block.
      **Ticks on:** the ratifying commit.
- [x] 5.2 `openspec validate relocate-review-authority-floor-mirror --strict`
      and `--all --strict` pass, and the repository's own validators report the
      same failure set as `main`. **Ticks on:** the ratifying commit, over the
      recorded runs.
- [ ] 5.3 Archive, once § 2, § 3 and § 4 are all ticked. **Ticks on:** the
      archive pull request.
