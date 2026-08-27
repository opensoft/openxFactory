# Tasks: supersede-lost-pin-baseline

The act this packet performs is a governance act, so the tasks are mostly
statements of what was measured before writing anything down. § 1 records the
filing. § 2 is the record itself. § 3 is the one linkage that lets the
verification report truthfully. § 4 is the gate. § 5 carries three follow-ups
this change deliberately does not write.

**READ THIS FIRST IF YOU ARE TEMPTED TO TIDY THE REGISTER.** Nothing in this
packet licenses deleting a `KNOWN_LOSSES` row. The pin is unrecoverable for
ever, the row is the only place the measurement lives, and removing it makes the
site report as a repairable orphan — a failing verdict with a repair route
nobody can follow. Discharge is by citation, never by deletion.

**ARCHIVED 2026-08-27, AND THE PARAGRAPHS ABOVE STAND AS WRITTEN.** § 4.9 was
the last open arm of the gate; it is ticked below with its evidence, and this
archive act IS that arm. § 5.1, § 5.2 and § 5.3 cross the archive UNTICKED BY
DECISION, not by oversight — each was declared out of scope in `proposal.md`
§ Named follow-ups before any of this landed, and none is a condition of the
gate. The register warning above is the one instruction this archive makes MORE
load-bearing rather than less: the row survives the move, and what moved is
where the record it cites is committed.

## 1. Filing and admission

- [x] 1.1 ORIGIN AND APPROVAL ARE RECORDED FROM THE COMMISSION ITSELF, on the
      `govern-derived-pin-reachability` / `fix-release-reachability-race`
      instruction-as-origin-act shape rather than the blank-pair shape. Brett
      commissioned the filing on 2026-08-27 by a multi-choice; the option he
      selected is quoted verbatim in `.openspec.yaml` § origin.reason and in
      `proposal.md` § Ratified. `approved_by` / `approved_on` are filled from
      that act, and both state in their own text that THE CITATION COVERS THE
      DECISION TO FILE AND NOTHING ELSE.
- [x] 1.2 `kind: staged` was checked before being declined:
      `ideation/staging/` and its `INDEX.md` carry nothing on derivation pins,
      pin losses, or supersession of evidence records. `kind: ad_hoc` is
      therefore unavailable-otherwise rather than preferred.
- [x] 1.3 THE PARALLEL SESSION'S SURFACE WAS NOT TOUCHED.
      `openspec/changes/govern-derived-pin-reachability/` was READ (its § 3.6
      and § 5.5 are what this packet discharges) and not edited, moved, or
      re-ticked. **AND IT ARCHIVED WHILE THIS PACKET STOOD OPEN**: pull request
      #428 landed on 2026-08-27, moving that packet to
      `openspec/changes/archive/2026-08-27-govern-derived-pin-reachability/` and
      promoting its requirements into `openspec/specs/doc-health/spec.md` and
      `openspec/specs/ideation-cross-reference/spec.md`. **NOTHING IN THIS PACKET
      NEEDED TO MOVE FOR IT**, which was the point of citing the code and the
      measurement rather than that packet's paths — the one edit it earned is the
      tense of `design.md` § 1, where the hazard argument becomes historical and
      its conclusion stands. `origin/main` was merged into this branch after that
      landing (one conflict, the README active-changes block: this packet's entry
      kept, the archived packet's entry dropped as main had already dropped it),
      so this delta is authored against canon as PROMOTED. The two never wrote
      the same canon file at the same time: that archive promotes its delta,
      this one promotes at ITS own archive.
- [x] 1.4 THE VETO WINDOW IS CLOSED, 2026-08-27. All four § Orchestrator
      decisions CLEARED AS AUTHORED and both § Open Questions RULED, by a
      four-question multi-choice put to Brett by the orchestrating session and
      relayed to this session the same day. He took the packet's own
      recommendation on every question, so **the clearance moved nothing**: the
      `evidence/`-homed record with its glob-pair citation (OD-1), the declared
      `NON_MEMBERS` row (OD-2), the spec delta riding (OD-3) and the register row
      being the disposition (OD-4) all stand as written, and OD-4's own named
      veto branch was NOT taken — **no `health/dispositions.yaml` entry is owed
      and none is added**. Q1 RULED: corroboration only; the record claims
      exactly what is provable and never recovery. Q2 RULED: no aging rule; the
      citation is re-resolved every run and breakage is self-announcing. Both
      rulings match the record and the code as already written, so nothing was
      rewritten to satisfy them. **THIS IS A SECOND ACT, DISTINCT FROM THE
      COMMISSION** recorded at § 1.1: that one admitted the packet, this one
      closed the window. No verbatim wording of the ruling reached this session,
      so none is quoted — approver, date, mechanism and selections are recorded
      instead, in `proposal.md` § Orchestrator decisions and § Open Questions.
- [x] 1.5 THE MERGE-THEN-ARCHIVE SEQUENCE IS APPROVED AND IS NOT THIS SESSION'S
      TO PERFORM. The orchestrating session merges on green and dispatches the
      archive pass afterwards; this session pushes and stops. Recorded because a
      packet that says "archives only after green" should also say who does it.

## 2. The superseding record

- [x] 2.1 THE LOSS RE-MEASURED BEFORE ANYTHING WAS WRITTEN, not copied from the
      day-old declaration. `git cat-file -t` fails in the shared aggregation
      object store; 0 of the 573 refs `git ls-remote origin` advertises match
      (406 of them `refs/pull/*`); `git fetch origin 66b14064…` is refused with
      `upload-pack: not our ref`; no `005-customer-subject-runtime` ref survives
      on the remote; and `refs/retention/pins/*` holds exactly three refs, each
      at the commit its name states and none of them this pin. **The advertised
      ref count moved 566 -> 573 in a day and the answer did not move.**
- [x] 2.2 THE CAUSE IDENTIFIED FROM COMMITTED HISTORY. Every commit of the
      landed `005-customer-subject-runtime` line carries committer date
      `2026-07-14T01:08:50+0000` while author dates spread across the preceding
      day — one rebase, rewriting the whole branch. The record was authored
      before it and carried through unchanged, so it kept naming its pre-rebase
      parent's object name. The retention namespace was not ruled until
      2026-08-27, six weeks later, so no retention ref could have been
      published: **this is the defect class the rule now prevents, observed on
      its oldest instance.**
- [x] 2.3 THE SURVIVING BASELINE STATE IDENTIFIED, BY MEASUREMENT.
      `8f7c99f0db065fb153b7d9498eb1e16b3c3c306b` ("Implement US3 v1-to-v2
      Hermes migration cutover (Gate G0 checkpoint)") is an ancestor of `main`
      and is the parent of `e8ae366cda7b5814b73942891837175b5c43d929`, the
      commit that ADDED the superseded record and the one that record names by
      self-reference as `provider_commit: this-checkpoint`. Corroborated by all
      three differential counts the record states about its baseline, each
      re-measured at both commits: catalog members 34 -> 39
      (`contracts/hermes-runtime/contract-index.yaml`), schema-typed entries
      27 -> 32 (same file), fixture cases 79 -> 110
      (`contracts/hermes-runtime/fixtures/index.yaml`). **LABELLED AS
      CORROBORATION, NOT RECOVERY**, in the record and here: the object is gone,
      tree equality is unprovable by anybody, and one count disagreeing would
      have falsified the identification.
- [x] 2.4 THE ONE LOAD-BEARING CLAIM RECOMPUTED. The PostgreSQL section's
      `inventory_intersection: []` is computed in its own comment as "US4 diff
      vs 66b1406 intersect PG inventory = empty". Recomputed against the
      identified survivor the US4 diff is 62 files, none of them a PostgreSQL
      evidence source: no `.sql` path, nothing under
      `contracts/hermes-runtime/migrations/`, no path matching `postgres`. The
      78-member inventory itself is declared in NO committed artifact and the two
      digests that would identify it appear nowhere else in the repository, so
      that half was never independently checkable at any commit — **recorded as
      such, so a later reader does not attribute it to the loss.**
- [x] 2.5 THE RECORD WRITTEN at
      `openspec/changes/supersede-lost-pin-baseline/evidence/pin-loss-supersession.yaml`:
      `status: record`, the commission quoted as its issuing authority, the
      superseded path with `bytes_edited: false` and the refusal stated, the
      measurement, the cause, the surviving state with its corroboration and its
      limit, verification standing split into retained / lost / never-checkable,
      and the disposition.
- [x] 2.6 THE SUPERSEDED RECORD WAS NOT EDITED. `git diff` touches no path under
      `openspec/changes/archive/`. Verified at the gate (§ 4.4) rather than
      asserted here.

## 3. The discharge linkage

- [x] 3.1 `KnownLoss` gains `superseding_record` (path globs, live and archived)
      and `discharged` (what the record established). Defaults are `()` and
      `""`, so a row that cites nothing awaits its act — there is no implicit
      discharge.
- [x] 3.2 `discharging_record()` READS committed state at the revision under
      test and requires the record to NAME the pin. Three cases behave exactly
      like no citation: a record nobody committed, a record deleted after the
      row cited it, and a stub at the right path. Two tests pin that.
- [x] 3.3 `PinResult` gains `discharge`; `PinClassReport.lost_awaiting_record`
      is added; `fully_verified` consults it instead of `lost`. **The docstring
      already asked this question** — "no declared loss awaiting its superseding
      record" — so the property is completed, not redefined, and its text now
      says which half moved and why deletion is not the other route.
- [x] 3.4 THE VERDICT STAYS `LOST` and the render marker stays `[LOST]`. A
      discharged loss carries its full measurement plus a `DISCHARGED:` clause
      naming the record; `summary()` reports "N lost (declared unrecoverable, M
      awaiting a superseding record)" so both facts are visible at once. No
      fourth verdict is introduced: encoding "an obligation is outstanding" in
      the field that answers "is this pin reachable" would hide the loss from
      anybody scanning for losses.
- [x] 3.5 THE SUPERSESSION RECORD IS DECLARED A NON-MEMBER, with its reason and
      its stated trade, and `SUPERSESSION_RECORD_PATHS` is spelled once and used
      by both the non-member row and the class-wide test. The alternative is
      named as the dodge it would have been: a key outside the sweep vocabulary
      would have hidden the file with NO declaration, which is the
      silent-coverage defect this very pin proved.
- [x] 3.6 FIVE TESTS ADDED to `tests/doc-health/test_pin_reachability.py`, each
      pinned to a defect rather than to the fix: a loss awaiting its record holds
      `fully_verified` open without reddening the run; a loss with a committed
      record is discharged while STILL reporting LOST, still rendering, and
      still leaving the record's path in the report; a record that does not name
      the pin (and an uncommitted one) discharges nothing; a row citing nothing
      is the awaiting state; and — the acceptance signal — no row in this
      repository cites a record the repository does not carry, with the one
      declared loss asserted discharged by name.

## 4. Verification

- [x] 4.1 `OPENSPEC_TELEMETRY=0 openspec validate supersede-lost-pin-baseline
      --strict` — PASS.
- [x] 4.2 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` — **77
      passed, 0 failed** at authoring (76 before this packet, one new change
      item), and **76 passed, 0 failed** re-run after `origin/main` was merged in
      — one item fewer because the sibling packet ARCHIVED, not because anything
      here dropped out. Both numbers are recorded rather than the later one
      overwriting the earlier, because a total that moves for a reason is
      evidence and a total that is quietly restated is not.
- [x] 4.3 `python3 -m pytest tests/doc-health -q` — **1168 passed, 0 failed** at
      authoring (1163 before, five added), and **1183 passed, 0 failed** re-run
      after the merge, the fifteen extra tests arriving with pull requests #427
      and #428 rather than with anything here. Both runs under `set -o pipefail`
      so a masked failure cannot read as green.
      `tests/doc-health/test_pin_reachability.py` alone: **53 passed** (48
      before), re-run on the merged head and still 53.
- [x] 4.4 THE ARCHIVED RECORD IS BYTE-IDENTICAL. `git diff origin/main --stat`
      lists no path under `openspec/changes/archive/`, and
      `git diff origin/main -- openspec/changes/archive/` is empty.
- [x] 4.5 THE CLASS REPORTS ITSELF FULLY VERIFIED, TRUTHFULLY.
      `python3 -m doc_health.pin_class --repo .` still prints the loss as
      `[LOST] … DECLARED UNRECOVERABLE:` with its whole measurement, now
      followed by `DISCHARGED:` and the record's path, and the summary line
      reads "1 lost (declared unrecoverable, 0 awaiting a superseding record)".
      Nothing is silenced; the outstanding obligation is what changed.
- [x] 4.6 NO CONTRACT BUNDLE IS OWED, measured: no edited file appears in any
      `contracts/releases/*.digests.yaml` inventory.
- [x] 4.7 THE DOC-HEALTH SELF-GATE ADDS NOTHING.
      `python3 -m doc_health.runner --single-repo .` reports **0 new regressions
      vs the previous report**, and NO finding names any path this packet adds or
      edits. The five standing `record-immutability` criticals are on documents
      this branch does not touch (`git diff origin/main --name-only` lists nine
      files, none of them among them, and **zero paths under
      `openspec/changes/archive/`**).
- [x] 4.8 `python3 -m compileall` clean on both edited modules; `git diff
      --check` clean. `black` is not installed in this environment and is not
      part of this repository's gate, so it is recorded as not run rather than
      claimed.
- [x] 4.9 MERGED AND GREEN ON MAIN. Open at pull request #429. The archive gate
      is merge-plus-green, the sequence was approved on 2026-08-27 (§ 1.5), and
      **the orchestrating session performs both halves** — it merges on green and
      dispatches the archive pass. This session pushed the rulings and stopped.
      **DONE 2026-08-27 — THE GATE IS FULLY DISCHARGED, AND THIS ENTRY IS THE
      ARCHIVE ACT.** The paragraph above is kept as the state it recorded while
      it stood; every arm below is checked rather than asserted.
      **MERGED ON THE IMPLEMENTED TARGET** — pull request #429, merged
      2026-08-27T19:26:29Z as merge commit
      `94933adfcf993dbef2e74952662a3eb1281693e2`, re-verified here an ancestor of
      `origin/main` (`git merge-base --is-ancestor`, exit 0) rather than taken
      from the pull request page, and a REAL TWO-PARENT MERGE — parents
      `ae6a1e7e76f66dfdeb6cf2aad65f21dff9ae8f19` and
      `06ede5b70fea0952f8182e38ab3c21362879841c` — rather than a rewrite, which
      is worth checking in a packet whose whole forcing instance is a pin
      orphaned by a rewriting landing.
      **GREEN ON THE FINAL HEAD** `06ede5b70fea0952f8182e38ab3c21362879841c`:
      `pytest-suite` **success** 19:10:42Z → 19:25:49Z and `wallet-validation`
      **success** 19:10:41Z → 19:11:01Z, read back from the check-runs API at
      this act rather than from the merge notification. The suite line came out
      of the job log of run 33107163953: **6991 passed, 20 skipped, 338
      deselected, 28 subtests passed, 0 failed in 877.32s (14m37s)**. § 4.3
      recorded 1183 locally on the pre-merge head; the CI total is the whole
      repository suite and both are kept rather than one restating the other.
      **THE REALIZATION RODE IN THE PROPOSING PULL REQUEST**, so merged-plus-green
      is ONE event here rather than two: the record, the discharge mechanism and
      the five tests landed together and there is no second pull request to name.
      **THE ACT.** ARCHIVED to
      `openspec/changes/archive/2026-08-27-supersede-lost-pin-baseline/` by
      `OPENSPEC_TELEMETRY=0 openspec archive supersede-lost-pin-baseline --yes`
      (openspec 1.2.0), which reported `doc-health: update`, `+ 1 added`,
      `Totals: + 1, ~ 0, - 0, → 0` and applied the delta into
      `openspec/specs/doc-health/spec.md`. It also reported `Task status: 25/29`
      and warned on four incomplete tasks, which is CORRECT: this task was the
      twenty-sixth, and § 5.1, § 5.2 and § 5.3 survive as named follow-ups.
      **THE MECHANISM WAS `openspec archive`, NOT `proposal-support archive`**,
      whose blanket `^- \[ \]` gate cannot tell a follow-up declared out of scope
      from unfinished work; that wrapper's origin gate was run separately on both
      sides of the move (`proposal-support.py . verify supersede-lost-pin-baseline`
      ok before, whole-corpus `verify` ok after).
      **THE CLI HAZARD DID NOT FIRE, and it was checked anyway by blob id.**
      `.openspec.yaml` MOVED with the packet rather than being deleted, and all
      six files are byte-identical across the move: `.openspec.yaml`
      `205792871b1736936e70a59cfefea5cf12ea09fc`, `design.md` `82920afc`,
      `evidence/pin-loss-supersession.yaml` `cede7334`, `proposal.md` `6f2f537b`
      (before this entry's own edits), `specs/doc-health/spec.md` `0105332b`,
      `tasks.md` `f9d77f4c`. **ORIGIN RETENTION PASSES**: the `.openspec.yaml`
      blob is byte-identical to the blob at the ratifying commit `0bbeea0a`, so
      `kind`, `id`, `reason`, `approved_by` and `approved_on` are unchanged from
      ratification. Nothing about the merge or this archive went into the origin
      block, because a realization is not origin provenance.
      **THE DISCHARGE STILL RESOLVES AT THE ARCHIVE PATH — the one thing this
      move could have broken, proved rather than assumed.** The record now stands
      at
      `openspec/changes/archive/2026-08-27-supersede-lost-pin-baseline/evidence/pin-loss-supersession.yaml`,
      which is matched by the SECOND glob of the citation pair
      (`openspec/changes/archive/*-supersede-lost-pin-baseline/evidence/pin-loss-supersession.yaml`)
      and by the `NON_MEMBERS` row that declares such a record a non-member. The
      probe re-run on the committed archive state reports **63 declared pin sites
      across 20 class members: 49 reachable, 0 orphaned, 1 lost (declared
      unrecoverable, 0 awaiting a superseding record), 0 inconclusive; 0
      uncovered, 0 vanished, 0 future members now carrying pins** — the same
      answer as before the move, with the `DISCHARGED:` clause now naming the
      archive path. **THIS IS OD-1'S WHOLE ARGUMENT DEMONSTRATED**: a single-path
      citation would have gone dangling at this exact moment, and the pair is why
      it did not.
      **GATES ACROSS THE ACT.** `openspec validate --all --strict` 76 → **75
      passed, 0 failed** (one item fewer, this packet having left the active
      set). `python3 -m pytest tests/doc-health -q` under `set -o pipefail`:
      **1183 passed, 0 failed** before and after; `test_pin_reachability.py`
      alone **53 passed** on both sides. Single-repo doc-health: **5 critical, 7
      error, 41 warning, 12 info, 0 new regressions** before and after, every
      family count unchanged, and `proposal-origin`, `promotion-fidelity`,
      `release-inventory-drift`, `family-enumeration` and `duplicate-packet` all
      **0 before and 0 after** — THE ARCHIVE ADDS NO FINDING. The five standing
      `record-immutability` criticals are pre-existing and on documents this
      branch does not touch.
      **PROMOTION, PROVED BY DIGEST RATHER THAN BY EYE.** `doc-health` canon
      **34 → 35 requirements, 145 → 149 scenarios**, 1488 → 1561 lines,
      **+73 / −0**, 99677 → 105112 bytes. The pre-existing file is a byte-exact
      PREFIX of the promoted one (`cmp -n 99677` clean), so every pre-existing
      requirement is byte-identical and nothing was deleted or reworded. The
      appended region is bytes 99678–105112 and equals the delta's requirement
      body verbatim plus the single trailing blank line canon carries at
      end-of-file: delta body and canon block are both 72 lines, 5434 bytes,
      under one digest
      `sha256:a595d40e7b9b321f32ce5d04c1888e54ae8bab0f4c6aa30e0a4eb4604e711c64`.
      One requirement, four scenarios — the proposal's own declared counts, and
      canon's totals moved by exactly them. `## MODIFIED Requirements` blocks in
      this delta: **zero**, so no archive-order question arises.

## 5. Open — deliberately not closed by this change

**ALL THREE CROSS THE ARCHIVE UNTICKED, EVERY ONE BY DECISION, and the archive
claims nothing they leave open.** Each was declared out of scope in
`proposal.md` § Named follow-ups at authoring, none is an arm of the
merge-plus-green gate, and none was disturbed by the realization. Stated plainly
here rather than left for a reader to assemble: § 5.1 the undeclared 78-member
evidence inventory, which is a gap in the hermes-runtime evidence contract and
the reason ONE claim in the superseded record can only ever be corroborated;
§ 5.2 the differential audit of the hermes evidence family, a sweep rather than
a supersession, and one whose limit the sibling packet already stated (a pin
whose object is gone does not resolve, so the value-resolving direction cannot
find it); § 5.3 the nightly, where NOTHING is enforced and the discharge
mechanism narrows what an enforcing check would report without arguing for
enforcing it. `openspec archive` counted these three plus § 4.9 as its four
warnings; § 4.9 is now ticked and these three remain, which is the correct
residue.

- [ ] 5.1 **THE 78-MEMBER POSTGRESQL EVIDENCE INVENTORY IS DECLARED NOWHERE.**
      The superseded record quantifies over it and digests it twice
      (`source_identity_digest`, `matrix_digest`), and no committed artifact
      defines it while no committed generator reproduces the digests. That is a
      gap in the hermes-runtime evidence contract, not a consequence of this
      loss, and it is the reason one claim in that record can only ever be
      corroborated. Carried unticked.
- [ ] 5.2 **NO DIFFERENTIAL AUDIT OF THE HERMES EVIDENCE FAMILY WAS RUN.** The
      declared class covers every pin it knows and the one unrecoverable loss is
      the one declared; whether another archived evidence record carries a pin
      under a key the vocabulary still does not know is a sweep question, and the
      sweep that would answer it is the one the sibling packet already built and
      whose limit it already stated (a pin whose object is gone does not resolve,
      so the value-resolving direction cannot find it). Carried unticked.
- [ ] 5.3 **NOTHING IS ENFORCED IN THE NIGHTLY.** The discharge mechanism
      narrows what an enforcing check would report; it does not argue for
      enforcing it, and the three reasons the preflight half stays unwired
      (severity on day one, a hardcoded entrypoint tuple, and a
      network-consulting verification whose admissibility is another packet's
      open question) are untouched. Carried unticked.
