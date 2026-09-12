# Tasks: disposition-codexfactory-regular-pr-council-clearance-archive

Status: ratified
Ratified by: disposition-codexfactory-regular-pr-council-clearance-archive — 2026-09-12, Brett Heap, "ratify the openxFactory disposition change when it's up" (2026-09-12T03:26:21.850Z, bare and conditional; condition satisfied at PR #1004's creation 2026-09-12T14:57:26Z; RATIFIED AS DISCLOSED; record `review/ratification-2026-09-12.md`)
Kind: tasks

**NOTHING IS TICKED THAT DID NOT LAND.** Every ticked box below is a diff in
this pull request or a run recorded verbatim in
`evidence/codexfactory-regular-pr-council-clearance-archive-2026-09-11.md`.
Group 6 is OWED work belonging to OTHER repositories and OTHER packets, and is
deliberately unticked, each box naming whose it is.

**TWO WORDS RATIFY TWO DIFFERENT THINGS, WHICH IS WHY 6.4 AND 6.6 ARE BOTH
TICKED AND THE HEADER NOW SAYS `ratified`.** Word one, 2026-09-12T03:04:29.167Z,
*"ratified_by — ratify the entries as encoded"*, was given on the authority-field
question and ratifies the two pin ENTRIES' text (6.4). Word two,
2026-09-12T03:26:21.850Z, *"ratify the openxFactory disposition change when it's
up"* — BARE and CONDITIONAL on the DRAFT PR existing, satisfied at PR #1004's
creation 2026-09-12T14:57:26Z — ratifies THIS PACKET (6.6). ~~It is not a word on
this packet's prose~~ — **STRUCK, not deleted**: true of word one alone.

**RATIFIED AS DISCLOSED.** A bare word resolves nothing it does not name, so
GROUP 6 IS NOT TICKED BY IT: 6.1, 6.2, 6.3 and 6.5 stay open at the defaults
this file states, flagged rather than resolved. **THE MERGE IS STILL A SEPARATE
ACT** and is not ticked anywhere in this file.

---

## 1. The retirement, measured before it was performed

- [x] 1.1 (2026-09-12) The stale entry was PROVEN stale rather than assumed:
      `python3 scripts/validate-openspec-cli-pin.py --repo <codexFactory@87ea247f>
      --all` at `1.12.0` against the pin as it stands on openxFactory `main`
      `323c7adf` — **exit 2**, `Totals: 33 passed, 3 failed (36 items)`,
      `REFUSE pin-disposition-stale` naming exactly
      `add-regular-pr-council-clearance / merge-master-approval/spec.md`.
- [x] 1.2 (2026-09-12) The whole entry is DELETED — `repo`, `item`, `path`,
      `level`, `finding`, `why`, `cited_to`, `ratified_by`, `retires_when` — and
      not marked, flagged or moved to a history block. Deletion is this file's
      only form for a retirement and is the tool's own printed remedy.
- [x] 1.3 (2026-09-12) The entry's own `retires_when:` is QUOTED in the packet
      and in the pin's new dated note, because it named this exact day in these
      exact words and a prediction that came true is the strongest evidence the
      mechanism works.
- [x] 1.4 (2026-09-12) The 2026-09-05 comment block above the pair is left
      UNEDITED — it is that change's dated record of what arrived that day — and
      a dated **RETIRED 2026-09-11** note is added beneath it so a reader of the
      old paragraph reaches the correction in the next sentence.

## 2. The two additions, discovered rather than assumed

- [x] 2.1 (2026-09-12) The SECOND HALF OF THIS PACKET WAS FOUND BY MEASUREMENT.
      With only the stale entry deleted, the same command exits **1** with
      **two UNDISPOSITIONED** findings —
      `extend-merge-master-envelope-to-floor-bot-lanes` and
      `relocate-review-authority-floor`, both `merge-master-approval/spec.md`.
      A pull request carrying only the deletion would have moved codexFactory's
      gate from exit 2 to exit 1 and called it fixed.
- [x] 2.2 (2026-09-12) Both findings were PRODUCED, not transcribed: the message
      is copied WHOLE from the run's own output into `finding:`, which is what
      the matcher compares after whitespace normalization. The two messages are
      byte-identical to each other, one per sibling change.
- [x] 2.3 (2026-09-12) Each entry carries `repo: codexFactory`, `level: ERROR`,
      a `why:` that says what moved and what copying the scenarios in today
      would do, a non-empty `cited_to:` (8 and 9), Brett's word, and a
      `retires_when:` naming the re-derivation OR the archive.
- [x] 2.4 (2026-09-12) **THE CLASS IS DECLARED RATHER THAN BLURRED.** Neither
      sibling block carries a reserved `Merged into` marker and neither should —
      neither change performed the retitle — so neither entry cites the marker
      requirement. Both cite `doc-health`'s *Currency of an active change's
      MODIFIED requirement blocks* (`openspec/specs/doc-health/spec.md:1597`),
      the requirement that DEFINES the check that reported them, and `:1625`,
      the line that makes the finding legitimate rather than spurious.
- [x] 2.5 (2026-09-12) The second entry NAMES the other entry the same change
      carries (`relocate-review-authority-floor /
      repository-gate-floor/spec.md`), and says they retire on different events,
      so no reader takes one to cover the other.
- [x] 2.6 (2026-09-12) Nothing else in the pin moved: `package`,
      `source_repository`, `version`, `revision_kind`, `integrity`, `shasum`,
      `tarball`, `lockfile`, `lockfile_integrity`, `lockfile_packages`,
      `rollback:`, `binary:`, `verify_pin:`, `consumer_entrypoint:`,
      `pinned_invocation:` and `resync_runbook:` are byte-identical, and NO
      surviving `dispositions[]` entry is edited.

## 3. The pin's prose made true again, and one class declared

- [x] 3.1 (2026-09-12) The rollback note's "the five entries below" becomes
      "six".
- [x] 3.2 (2026-09-12) A NEW dated paragraph records how the fourth and fifth
      findings arrived: the archive, what it retired, what it promoted, the
      measured exits, that the two blocks carry no marker and should not, and
      Brett's two words and what each does.
- [x] 3.3 (2026-09-12) **The block above `dispositions:` is rewritten from a
      COUNT into TWO DECLARED CLASSES.** It said *"EVERY ENTRY BELOW IS THE SAME
      DISAGREEMENT, five times"* — a sentence these two entries FALSIFY. It now
      names MARKER-BLINDNESS (four) and CANON MOVED UNDER AN UN-RE-DERIVED DELTA
      (two), says what each class must cite, records that one codexFactory
      CHANGE carries two entries in two classes, and keeps the two-repository
      grouping.

## 4. The tests, tightened rather than renumbered

- [x] 4.1 (2026-09-12) The count-pinning test moves 5 → 6 by ONE DELETION and
      TWO ADDITIONS, KEEPING the per-repository split, and is renamed. Its
      docstring reads the movement, as the precedent's reads its own.
- [x] 4.2 (2026-09-12) `DISPOSITION_MEASUREMENT` and
      `DISPOSITION_AUTHORITY_PREFIX` are RE-KEYED from `item` to the
      `(repo, item, path)` triple the verifier matches on. **FORCED, not
      cosmetic**: `relocate-review-authority-floor` now carries two entries with
      different measurements and different authority dates, and an item-keyed
      map asserts one against the other, silently, in the direction of passing.
      A new assertion pins that no two entries share a triple.
- [x] 4.3 (2026-09-12) A new `DISPOSITION_CLASS` map asserts the reserved-marker
      citation **if and only if** the entry is marker-blindness — measured:
      `"Merged into"` is cited by exactly the four older entries and by neither
      new one. A future canon-moved entry reaching for a marker citation to
      satisfy a shared literal now FAILS.
- [x] 4.4 (2026-09-12) The authority is read through BOTH spellings
      `mod.DISPOSITION_AUTHORITY` admits, with a NEW assertion that exactly one
      stands. The old test indexed `entry["ratified_by"]` and would have raised
      `KeyError` on the first `recorded_by:` entry — a grammar the shipped
      verifier has accepted since the bump — so this is a CORRECTION, not a
      relaxation. The SPELLING is deliberately not pinned per entry
      (`design.md` § 4): a convener's upgrade must cost one key name in the pin
      and nothing else, and this packet is its own worked example.
- [x] 4.5 (2026-09-12) `python3 -m pytest tests/openspec_cli_pin -q` green —
      **154 passed**.
- [x] 4.6 (2026-09-12) **TWO CITATION DEFECTS WERE FOUND BY THIS REPOSITORY'S
      OWN ARMS AND FIXED BEFORE ANY OF IT REACHED CI**, recorded because a
      packet that only reports its green runs is half a record.
      (a) `scripts/validate-pin-registrations.py` exited 1: a citation written
      as ``this pin's own `relocate-review-authority-floor /
      repository-gate-floor/spec.md` entry above`` parses as an ABSOLUTE path
      `/` plus an unresolvable in-tree path. Reworded to name
      `contracts/openspec-cli-pin.yaml` and describe the sibling entry in prose.
      (b) `tests/pin_registrations/test_pin_registration_sweep.py::
      test_the_live_pins_citation_bytes_align_with_its_parsed_structure` failed
      on both new entries: a citation ending `… at #434's head` hits BOTH of
      this file's known reader divergences at once — `yaml.safe_load` splits it
      at the `: ` inside the quoted requirement title AND truncates it at the
      ` #` it reads as a comment — and the two together cannot be rejoined byte
      for byte. Either divergence ALONE is tolerated and already occurs 18 times
      in this file; the COMBINATION is not. Reworded to `… at head 87ea247f`.
      Both arms green after.

## 5. The runs, all five directions

- [x] 5.1 (2026-09-12) BEFORE on #434's tree: **exit 2**, REFUSE stale, one
      entry named. (Evidence § 1.)
- [x] 5.2 (2026-09-12) DELETION ONLY on #434's tree: **exit 1**, two
      UNDISPOSITIONED. (Evidence § 2.)
- [x] 5.3 (2026-09-12) AFTER on #434's tree: **exit 0**,
      `Totals: 33 passed, 3 failed (36 items)` UNCHANGED, `DISPOSITIONED
      FINDINGS in codexFactory (4 applied)`, and the honest trailer
      `THIS IS NOT A CLEAN TREE: 4 finding(s) are ACCEPTED EXCEPTIONS`.
      (Evidence § 3.)
- [x] 5.4 (2026-09-12) AFTER on openxFactory's own tree — the gate's literal
      invocation, `--all --no-cache`: **exit 0**,
      `Totals: 101 passed, 2 failed (103 items)` (one more item than before
      this packet existed — this change itself, and it passes), its own two
      applied, all four
      codexFactory entries neither applied nor stale. (Evidence § 4.)
- [x] 5.5 (2026-09-12) On codexFactory `main` `3c31a2e4`: the two new entries
      are **STALE and the run REFUSES** (`pin-disposition-stale`, **exit 2**)
      where the pre-edit pin exits 0 — measured, not assumed. **This fixes an
      ORDER** (#434 first or together, the pin advance never before) and is not
      a defect in the entries. (Evidence § 5.)
- [x] 5.6 (2026-09-12) The pinned CLI validates THIS packet `--strict` with
      `skip_specs: true` and no `specs/` directory, and the whole corpus
      `--all --strict` is green on this branch.

## 6. Owed, and not this packet's to tick

- [ ] 6.1 **codexFactory's declared openxFactory pin advances** to a commit AT
      OR AFTER this change's merge. An earlier pin resolves a pin file without
      these entries and codexFactory `validate` stays red on #434's tree.
      **Brett Heap ruled 2026-09-12T03:04:29.167Z that lane `codeXfactory-1`
      carries it** (*"codeXfactory-1 carries it"*), sequenced after that lane's
      **#435 → #433**. **AND THE ORDER IS FIXED BY MEASUREMENT**: the advance
      must not reach codexFactory `main` before PR #434 merges, or `main`
      refuses `pin-disposition-stale` on both new entries (evidence § 5). It is
      codexFactory's act, in codexFactory's own pull request.
- [ ] 6.2 **codexFactory PR #434's `validate` going green** is a codexFactory
      verdict, not this one. This packet removes the `openspec-cli-pin` reason
      its gate is red and claims nothing about the others.
- [ ] 6.3 **The two sibling re-derivations**, under the convener's *"This change
      first"* ordering: each packet re-derives its `## MODIFIED "Bounded
      autonomous surface"` block against the archived canon before its own
      archive. Each retires its entry here and, on that day, codexFactory's
      `--all` REFUSES until the entry is deleted — the mechanism working, and
      both `retires_when:` fields say so in advance. Neither is drafted or begun
      here.
- [x] 6.4 (2026-09-12) **The ENTRIES are ratified.** Brett Heap, first-hand, in
      session, verbatim **"ratified_by — ratify the entries as encoded"**,
      2026-09-12T03:04:29.167Z, recorded on openxFactory #745 (comment
      5643056862). Record at `review/ratification-2026-09-12.md` — a diff in
      this pull request, which is what lets this box be ticked under the rule at
      the top of this file. ~~THE PACKET'S OWN TEXT IS NOT RATIFIED BY THAT
      WORD~~ — struck, not deleted: true of this word, and box 6.6 records the
      later one that does. **THE MERGE IS STILL NOT COVERED BY EITHER.**
- [x] 6.6 (2026-09-12) **The PACKET is ratified.** Brett Heap, first-hand, in
      session, verbatim **"ratify the openxFactory disposition change when it's
      up"**, 2026-09-12T03:26:21.850Z — **BARE** (it answers no question stated
      in its own text) and **CONDITIONAL** (the condition is that the DRAFT
      PULL REQUEST EXISTS), the condition satisfied at PR #1004's creation,
      **2026-09-12T14:57:26Z**. On the estate's lane registry at
      `opensoft/brett-wip` commit `1c27a188bb772c69b15d9acb94821b6e8122a1ab`,
      `lanes/LANES.md`, row `provenance-autonomous-merge`, and in the lane
      handoff. Record at `review/ratification-2026-09-12.md`.
      **RATIFIED AS DISCLOSED** — 6.1, 6.2, 6.3 and 6.5 above are NOT ticked by
      it and stay at the defaults this file states. **AND IT IS NOT THE MERGE**,
      which is Rule 6 and the orchestrator's act.
- [ ] 6.5 **Watch `Fission-AI/OpenSpec#1793`** — filed 2026-09-05, NOT fixed.
      If a release honours a declared rename, the next pin bump re-derives the
      list against it and the four MARKER-BLINDNESS entries match nothing, so
      the pin REFUSES until each is deleted. That refusal is the INTENDED
      RETIREMENT PATH for that class and not a regression. **It does not reach
      the two entries this packet adds**: they exist because canon moved under
      an un-re-derived delta, not because a marker is unreadable, and an
      upstream marker fix retires neither. Nobody owns noticing it yet; this box
      says so and does not claim the precedent's box as discharged.
