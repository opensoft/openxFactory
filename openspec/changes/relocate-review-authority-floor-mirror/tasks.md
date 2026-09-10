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

**M-1 STEP (1) REALIZED 2026-09-09, AND IT TICKS FIVE MORE AND NO OTHERS: 2.1,
2.2, 2.4, 2.5 AND 2.6.** Each names "the merged commit", "the same commit", "the
new test green" or "the control green" as its own condition, and this
realization is that commit. **2.3 IS NOT TICKED AND IT IS HALF-SATISFIED**: its
condition is *"the same commit PLUS ONE OBSERVED RUN"*, the reporting is built
and asserted here, and the RUN has not happened — so it stays open beside
**2.7**, which waits on the same first firing against the OLD path. Ticking 2.3
now would count a witness nobody has read.

**M-1 STEP (3) REALIZED 2026-09-09, AND IT TICKS SIX AND NO OTHERS: 2.3, 2.7,
3.1, 3.2, 3.3 AND 4.1 — PLUS THE NEW 3.4 THIS REALIZATION ADDS.** 2.3 and 2.7
were half-satisfied at step (1) and waited on ONE OBSERVED RUN: run
**34303730483** (2026-09-09T02:34Z) resolved candidate one and printed
*"candidate 1 of the declared list, the path in force; no migration in
progress"* with `"action": "noop"` — the witness is read, so both tick. § 3 is
another repository's act and it landed: **3.1** on codexFactory #297 -> merge
commit `8165d1f3` (2026-09-09T04:28:55Z), **3.2** on run **34311220954**
(04:30:18Z), which printed *"fetched
floor/openxfactory-review-authority-floor.yaml at 8165d1f3… (15456 bytes) — NOT
the first declared candidate: scripts/merge_master/… did not resolve, so the
relocation … has landed in codexFactory and M-1 step (3) is now owed here"*, and
**3.3** on the M-5 comparison recorded on #745 (comment 5595953451): 15456 bytes
and sha256 `926d536d…abf3c0` at the old path at `4b12ba83`, at the new path at
`8165d1f3`, and in the vendored snapshot — one digest, three reads, 68 entries
throughout.

**4.2 DOES NOT TICK, AND THE REASON IS A MEASUREMENT RATHER THAN A CHOICE.** The
pin describes the document AT `core_commit` (`taken_at: core_commit`), and
`core_commit` is still `4b12ba83`, which PREDATES the relocation: measured
2026-09-09, `floor/openxfactory-review-authority-floor.yaml` is **HTTP 404** at
that commit. Advancing `floor_snapshot.of` and the `pinned_members` entry now
would make a live pin name a path that does not exist at the commit it pins, and
would take the freshness verifier offline with it —
`test_floor_snapshot.py::locate_pinned_core()` finds the checkout BY that path,
so it would return `None`, the verifier would SKIP, and `pytest-suite`'s
named-verdict gate would red. **THE PIN HAS NOT MOVED BECAUSE THE LANE HAS HAD
NOTHING TO ADVANCE**: codexFactory D-3 fixed the bytes across the move, so every
firing since has been a no-op. **WHAT TICKS 4.2:** the first re-pin advance that
carries `core_commit` past the relocation — codexFactory's next floor
REGENERATION — moving the pin's two path fields, `test_floor_snapshot.py`'s
`FLOOR_IN_CORE` and `test_review_lane_caller.py`'s literal in ONE diff.
`test_repin_lane.py::TheDeclaredCandidateList::test_the_pinned_core_declarations_name_the_document_at_the_pinned_commit`
REDS from that advance until they move, so the box cannot be forgotten: the
bot's own pull request carries the failure. **4.3** waits on the first re-pin run
after this merge, which should print *"candidate 1 of 1 in the declared list,
the path in force; no migration in progress"*.

**AND MQ-3 (BOX 1.4) IS STILL UNRULED, WHICH THIS REALIZATION IS ANSWERABLE
FOR.** Its stated default trigger is *"one advance observed against the
successor path"*, and what was observed is a NO-OP against the successor. An
ADVANCE cannot be observed at all while the bytes are identical — D-3 made them
identical on purpose — so the default trigger, read strictly, could not fire
until codexFactory's next regeneration. Step (3) was authored on the standing
word to realize, on the lane's own witness naming step (3) as owed, and on the
consumer measured below. The box stays open for the ruling.

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

- [x] 2.1 `.github/workflows/review-lane-repin.yml` declares the ORDERED
      candidate list, old path FIRST, and the fetch step tries each in order.
      **Ticks on:** the merged commit.
- [x] 2.2 `scripts/review_lane_repin.py` takes the same ordered list and returns
      `floor_document_unobtainable` only when EVERY candidate fails, naming
      every path tried (M-3). **Ticks on:** the same commit.
- [x] 2.3 The run reports WHICH candidate resolved, and says nothing about a
      migration when it was the first. **Ticks on:** the same commit plus one
      observed run. **RUN 34303730483, 2026-09-09T02:34Z, success:** *"fetched
      scripts/merge_master/openxfactory-review-authority-floor.yaml … —
      candidate 1 of the declared list, the path in force; no migration in
      progress"*.
- [x] 2.4 M-4 (if it stands): `contracts/review-lane-repin-binding.template.yaml`
      gains `source_documents:` under `privileges.source_repository`, and the
      lane does NOT read it at run time. **Ticks on:** the same commit.
- [x] 2.5 The lockstep assertion lands: every declaration of the list — workflow
      env, script constant, the test literal, and the binding if 2.4 stands —
      carries the SAME ordered list; **and the two sites that declare ONE path
      rather than the list — `test_floor_snapshot.py`'s `FLOOR_IN_CORE` and
      `test_review_lane_caller.py`'s literal — are asserted to equal CANDIDATE
      ONE.** **Ticks on:** the new test green.
      **TEXT CORRECTED 2026-09-09, WITH THE TICK, ON A COPILOT FINDING**
      (#823 comment 3963705705). As written this box asked those two sites to
      carry the two-entry list, and they cannot: both declare what
      `contracts/review-lane-pin.yaml` names, and **M-6 freezes that pin until
      step (3)** — making them carry the successor would land step (3) early and
      point a live pin at a file codexFactory has not created. They are
      declarations of the PATH IN FORCE, not of the candidate list, so the
      assertion that fits them is head-equality, and that is what now lands. The
      original tick over-claimed and this is the correction, not a widening.
- [x] 2.6 A negative control proves the lane still refuses when NO candidate
      resolves, and does not silently pass. **Ticks on:** the control green.
- [x] 2.7 **The no-op is proven, not asserted**: one re-pin run observed green
      against the OLD path with dual acceptance in place, resolving candidate
      one and reporting no migration. **Ticks on:** that run — the same run
      **34303730483** (2026-09-09T02:34Z), `"action": "noop"`, pin unchanged at
      `4b12ba83`. M-2's safety argument is therefore MEASURED and not only
      reasoned: dual acceptance changed no behaviour on the day it landed.

## 3. M-1 step (2) — codexFactory's move: not this packet's act, but this packet's gate

- [x] 3.1 codexFactory `relocate-review-authority-floor` is ratified and its
      realization lands, moving the document to
      `floor/openxfactory-review-authority-floor.yaml`. **Ticks on:** that merge
      — codexFactory **#297 -> `8165d1f3954a23198ffe6a61438b10d24f6852ce`**,
      2026-09-09T04:28:55Z. **§ 4 MUST NOT BEGIN BEFORE THIS BOX IS TICKED**, and
      it did not.
- [x] 3.2 One re-pin run observed green against the NEW path — candidate one
      404s, candidate two resolves, and the run reports the migration.
      **Ticks on:** that run — **34311220954**, 2026-09-09T04:30:18Z, success,
      `"action": "noop"`, witness *"fetched
      floor/openxfactory-review-authority-floor.yaml at 8165d1f3… (15456 bytes)
      — NOT the first declared candidate: scripts/merge_master/… did not
      resolve, so the relocation … has landed in codexFactory and M-1 step (3)
      is now owed here"*. **THE SAME RUN TICKS codexFactory's OWN BOX 5.2**
      (*"the re-pin lane is observed running green against the NEW path"*) —
      there, not here.
- [x] 3.3 M-5 proven: `contracts/review-lane-floor-snapshot.yaml`'s content,
      `sha256` and `entry_count` are unchanged across the whole migration.
      **Ticks on:** the comparison recorded on #745 — comment **5595953451**,
      2026-09-09, measured through the contents API at three reads: the old path
      at `4b12ba83`, the new path at `8165d1f3`, and the vendored snapshot on
      `main`, each **15456 bytes**, each sha256
      `926d536d9bf5274384710cd9d8170d26b3a41a39108d319eaae76c8311abf3c0`, each
      **68** `never_clearable_paths` — the value the pin declares. The two
      ABSENCES are recorded with it: the new path is 404 at `4b12ba83` and the
      old path is 404 at `8165d1f3`.

- [x] 3.4 **THE CONSUMER THE ENUMERATION MISSED, because it finds the document
      by SWEEPING A DIRECTORY rather than by file name** — so no search for the
      old path could have surfaced it, and `code_surface:`'s "FIVE sites and no
      others" was wrong by one. `.github/workflows/merge-master-approval.yml`
      step 8 sets its governance directory to the pinned core's
      `scripts/merge_master`, loads every governance document there and picks
      out the one declaring this repository. At any core commit AFTER the
      relocation that directory holds the two clearance rules and no floor, so
      the step refuses `no_floor` and PARKS every openxFactory merge-master
      evaluation — fail-closed, never a silent approve, but a full park nobody
      would connect to another repository's tidy-up. **MEASURED, both
      directions, over the shipped step and real checkouts of both commits
      (2026-09-09):** the step as it stood returns
      `{"ok": true, "stage": "floor_complete"}` at `4b12ba83` and
      `{"ok": false, "stage": "no_floor", "reason": "… no repository_gate_floor
      for opensoft/openxFactory (floors present: [])"}` at `8165d1f3`; the step
      as this pull request leaves it returns `floor_complete` with 68 entries at
      BOTH, naming the document under `scripts/merge_master/` at the old commit
      and under `floor/` at the new one. **THIS BOX SITS IN § 3 BECAUSE IT IS A
      CONSEQUENCE OF STEP (2)** — it was found when codexFactory's move landed —
      though this repository performs the repair. **Ticks on:** the merged
      commit. It is fixed here rather than deferred because the next pin advance
      is what triggers it, and that advance is a bot's act on a schedule.

## 4. M-1 step (3) — this repository's SECOND realization: the list returns to one entry

- [x] 4.1 The superseded path is removed from every declaration; the list
      carries one path. **Ticks on:** the merged commit. FOUR DECLARATIONS OF
      THE LIST move together — `.github/workflows/review-lane-repin.yml`'s
      `FLOOR_IN_SOURCE_CANDIDATES`, `scripts/review_lane_repin.py`'s constant,
      `contracts/review-lane-repin-binding.template.yaml`'s `source_documents:`
      (M-4, still a recommendation under an open MQ-2) and
      `test_repin_lane.py`'s `EXPECTED_CANDIDATES` — and the lockstep assertion
      holds them equal. **THE TWO SITES THAT DECLARE ONE PATH RATHER THAN THE
      LIST ARE NOT DECLARATIONS OF IT** (box 2.5's correction says so in those
      words): they name what the PIN names, and the pin has not moved — see 4.2.
      The module's `floor_source_path` parameter went out with the entry it
      served, returning `plan_advance`'s closed-interface pin to SEVEN, exactly
      as the step-(1) comment said it would.
- [x] 4.2 `contracts/review-lane-pin.yaml`'s `sources:` entry advances to the
      new path (M-6); its narrative mentions of the old path are LEFT.
      **Ticks on:** the same commit, and a diff showing the narrative untouched.
      **TICKED 2026-09-10 ON THIS COMMIT — the condition the disclosure below
      named came true, exactly as it was written.** codexFactory's floor
      regenerations landed — its **#314** (merge `b08958ae`,
      2026-09-09T23:27:22Z: generated block 60 -> 61, gaining
      `openspec/specs/ideation-intent-plane/spec.md`, generated at openxFactory
      `17167481`) and, while this commit was being authored, its **#325** (merge
      `df42f803`, 2026-09-10T01:55:14Z: 61 -> 62, gaining
      `openspec/specs/repository-identity/spec.md`, generated at openxFactory
      `e32d580a`) — and the hourly lane's next two firings each found the
      advance owed and each FAILED at *Submit the advance to the checks that
      will judge it*: run **34423536950** (2026-09-10T00:58Z) and run
      **34425967673** (2026-09-10T01:33Z), both fetching
      `floor/openxfactory-review-authority-floor.yaml` at
      `aa0dced6132113ea07d3cfe6754fe440a4d9ca83` (15507 bytes), both deciding
      `"action": "advance"`, both red on
      `test_repin_lane.py::TheDeclaredCandidateList::test_the_pinned_core_declarations_name_the_document_at_the_pinned_commit`
      (*1 failed, 197 passed, 2 skipped*) — the red this box predicted, naming
      this box. THIS COMMIT IS THAT ADVANCE, TAKEN BY HAND ONCE, because the
      lane's own judging step refuses it until the four declarations move in the
      same diff and the lane may not move them.
      **THE ADVANCE**, produced by the lane's own driver
      (`scripts/review_lane_repin.py --write`, not by hand-editing the five
      sites), against the codexFactory head resolved at authoring time —
      `b594ef2a`, which carries BOTH regenerations, the lane having refused
      twice in the interval: `core_commit` `4b12ba83` -> `b594ef2a`; snapshot
      `sha256` `926d536d…abf3c0` -> `77611b0e…f53de`; snapshot bytes 15456 ->
      15556; floor total (`entry_count`) 68 -> 70; generated block
      `generated_at` `64aad02e` -> `e32d580a` and its counted entries 60 -> 62;
      the two covered-pending paths the advisory lane was deferring BOTH
      cleared. `b594ef2a` is codexFactory's #323 merge and changes no floor
      byte: the document there is the #325 output, digest for digest.
      **THE FOUR DECLARATIONS,
      IN THIS SAME DIFF:** the pin's `floor_snapshot.of` and its `pinned_members`
      entry (the `sources:` entry M-6 names — the pin carries no literal
      `sources:` key; design § 2 names it at `contracts/review-lane-pin.yaml:517`,
      which is that entry), `test_floor_snapshot.py`'s `FLOOR_IN_CORE` and
      `test_review_lane_caller.py`'s literal, all four to
      `floor/openxfactory-review-authority-floor.yaml`. **THE NARRATIVE IS
      UNTOUCHED, PROVEN BY DIFF RATHER THAN CLAIMED:** the pin's five prose
      mentions of the superseded path (lines 333, 370, 421, 435 and the
      `refresh:` field) are byte-identical to `main`, and the pin's whole
      advance-history block is unchanged — the same shape the lane's own bot
      advance `8d92bfaf` shipped, which touched four value lines and no prose.
      M-6's criterion is met at last: measured 2026-09-10, the new path resolves
      at `b594ef2a` (15556 bytes, `77611b0e…f53de`, the digest the pin now
      declares) and `scripts/merge_master/…` is **HTTP 404** there, while at
      `4b12ba83` it is the exact inverse (`floor/…` 404, the old path 15456
      bytes) — which is why the box could not tick on 2026-09-09 and can now.
      The `locate_pinned_core()` hazard is discharged rather
      than inherited: with a real `b594ef2a` checkout on disk,
      `tests/review_lane_pin` reports 200 passed / 0 skipped, so the freshness
      verifier and the vector replay both RAN and PASSED.
      **SUPERSEDED, NOT DELETED — the disclosure that stood from 2026-09-09
      until this commit, kept because it is the reason for the one-day gap:**
      *NOT THIS COMMIT, AND THE PACKET'S EXPECTATION IS NOT MET — DISCLOSED
      RATHER THAN SILENTLY DIVERGED FROM. M-6's own criterion is that the pin
      "must name a path that exists"; the pin names the document AT
      `core_commit`, `core_commit` is the PRE-relocation `4b12ba83`, and the new
      path is HTTP 404 there (measured 2026-09-09). Advancing it now would point
      a live pin at a file its own commit does not carry AND would skip the
      freshness verifier, which `pytest-suite`'s named-verdict gate turns into a
      red job. WHAT TICKS IT: the first re-pin advance that carries `core_commit`
      past `8165d1f3` — codexFactory's next floor regeneration, the lane having
      had nothing to advance since the move because D-3 fixed the bytes — in one
      diff with `test_floor_snapshot.py`'s `FLOOR_IN_CORE` and
      `test_review_lane_caller.py`'s literal.
      `test_repin_lane.py::TheDeclaredCandidateList::test_the_pinned_core_declarations_name_the_document_at_the_pinned_commit`
      reds from that advance until they move, and names this box in its failure
      message. codexFactory's box 5.1 is therefore satisfied IN PART by this
      merge — the old path is dropped from the lane; the pin advance is owed —
      and it ticks there, not here.*
      **codexFactory's box 5.1 IS NOW SATISFIED IN FULL by this merge**, the
      owed pin advance being this commit; it still ticks there, not here.
      **THREE FINDINGS, RECORDED RATHER THAN FIXED HERE.** (a) The driver moves the
      five pinned sites and the snapshot's two witnesses, and it does NOT move
      `floor_snapshot.of`, the `pinned_members` entry, or the two test literals —
      which is why this advance needed a hand. That is correct for every advance
      but a relocation-crossing one, and no packet yet owes the driver a
      path-moving act; naming it here is the disclosure, not a change to
      `scripts/review_lane_repin.py`, which this commit does not touch.
      (b) FOUR PIECES OF LEFT NARRATIVE NOW READ AGAINST THE FILE'S OWN DATA,
      and they are left because this box's tick condition says to leave the
      narrative — not because they are right, and not by this author's choice:
      the driver CANNOT reach prose (`_commit_line`'s leading `\s*` cannot
      reach a `#`, so every advance-history comment is unreachable by every
      rewrite it performs), so the first automated advance that changes
      `entry_count` leaves exactly these behind too. Counted at
      `contracts/review-lane-pin.yaml`: line 519, the `pinned_members` `why:`
      prose, still says "SIXTY-EIGHT never-clearable paths as of this advance"
      where `floor_snapshot.entry_count` now says 70; line 543, the same
      paragraph's PLUS ONE sentence, still says the generated block carries
      "SIXTY" tracked paths where it now carries 62; line 692, in the
      divergence paragraph, still contrasts xFactory's four against
      "SIXTY-EIGHT" — and that one the file ALREADY FORGIVES BY NAME, its own
      2026-09-05 note recording that the sentence "had read 64 … and was
      carried stale through" three later advances and that "the live figure is
      this file's own `floor_snapshot.entry_count` above"; and line 676, the
      `refresh:` field, still instructs a future re-point to "re-copy the file
      from `scripts/merge_master/…`", a path that is HTTP 404 at the commit
      this pin now names. THE LAST IS THE SHARP ONE — a live procedure rather
      than a count, and the only one a reader could act on wrongly — and all
      four are owed to whichever act next edits the pin's prose. The dated
      advance-history figure at line 763 (`ad15a898` "carrying a SIXTY-EIGHT-
      entry floor") is NOT in this list: it is true as written of the advance
      it records.
      (c) **A THIRD FINDING, RAISED BY THE CODEX REVIEW OF THE 4.2 PULL REQUEST
      AND RECORDED HERE BECAUSE ITS REPAIR IS NOT THIS ACT'S TO MAKE.** Two
      LIVE OPERATIONAL comment blocks — `.github/workflows/review-lane-repin.yml`
      lines 196-203 and `scripts/review_lane_repin.py` lines 92-98 — say in the
      present tense that `core_commit` "is still the PRE-relocation `4b12ba83`"
      and that "the pin and the two single-path test declarations still name
      the old path", both of which this commit falsifies. The finding is
      CORRECT and is not disputed. It is not repaired here because those two
      files are THE LANE'S OWN WORKFLOW AND DRIVER, and this pull request's
      central claim — that the advance is the driver's own output and nothing
      else, provable by re-running it in a pristine clone — is only falsifiable
      while the diff leaves both byte-untouched. A commit that advanced the pin
      AND edited the driver in the same act could not be checked that way. The
      repair is also owed once rather than per-advance: the driver cannot reach
      a comment at all, so every future automated advance leaves the same two
      blocks stale. The owed act therefore restates both in the
      superseded-not-deleted idiom AND makes them self-clearing (naming the
      invariant rather than the commit), and it belongs in a successor change
      against the lane's own files.
- [ ] 4.3 One re-pin run observed green with the single new path.
      **Ticks on:** that run — the first hourly `review-lane-repin` firing after
      this merge, which should print *"fetched
      floor/openxfactory-review-authority-floor.yaml at <codexFactory main>
      (15456 bytes) — candidate 1 of 1 in the declared list, the path in force;
      no migration in progress"* and `"action": "noop"`.
      **THE EVIDENCE EXISTS AND IS NAMED HERE, BUT THIS BOX IS NOT TICKED BY THE
      4.2 COMMIT** — its act is a RUN, not this diff, and an author moving a box
      on somebody else's act is the thing the packet discipline forbids. Run
      **34416680260** (2026-09-09T23:22:59Z, `conclusion: success`) printed the
      sentence above verbatim — *"fetched
      floor/openxfactory-review-authority-floor.yaml at
      cb242dc28767cefddc49cd9d7282ec4fd4ad6302 (15456 bytes) — candidate 1 of 1
      in the declared list, the path in force; no migration in progress"* — and
      `"action": "noop"`, and every green firing from 34324088114 (07:29Z)
      onward did the same. Whoever ticks this box cites that run. NOTE FOR
      WHOEVER DOES: after 4.2 lands, the byte count in the quoted sentence is
      15556, not 15456 — the TWO regenerations that made 4.2 fall due
      (codexFactory #314 and #325) changed it, and the quotation above is of a
      PRE-regeneration run.

## 5. Bookkeeping

- [x] 5.1 This packet is listed in the README's OpenSpec Records block.
      **Ticks on:** the ratifying commit.
- [x] 5.2 `openspec validate relocate-review-authority-floor-mirror --strict`
      and `--all --strict` pass, and the repository's own validators report the
      same failure set as `main`. **Ticks on:** the ratifying commit, over the
      recorded runs.
- [ ] 5.3 Archive, once § 2, § 3 and § 4 are all ticked. **Ticks on:** the
      archive pull request. § 2, § 3 and 4.1/4.2 are now complete; **§ 4 holds
      it on 4.3 ALONE** — the first hourly `review-lane-repin` firing after the
      4.2 merge, printing the one-candidate sentence and `"action": "noop"`.
      The packet therefore stays ACTIVE across that one wait rather than
      archiving with an open box, which `proposal-support` would refuse in any
      case. **SUPERSEDED, NOT DELETED — this box read, until the 4.2 commit:**
      *"§ 2 and § 3 are now complete; § 4 holds it — 4.3 on the next hourly
      run, and 4.2 on codexFactory's next floor regeneration, which is not this
      lane's act to schedule."* That regeneration arrived (codexFactory PR #314
      and PR #325) and 4.2 is discharged, so the instruction is narrowed to the
      one trigger that is still outstanding rather than left telling an
      operator to wait for a thing that has happened.
