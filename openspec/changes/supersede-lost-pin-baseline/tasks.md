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
      re-ticked. **IT IS BEING ARCHIVED BY THAT SESSION WHILE THIS PACKET
      STANDS OPEN, and nothing here needs to change for it**: this packet cites
      the code and the measurement rather than that packet's paths, and its
      archive PR promotes an ADDED requirement into the `doc-health` spec tail
      that THIS packet's delta only reaches at ITS OWN archive — so the two
      never write the same canon file at the same time.
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
      passed, 0 failed** (76 before this packet, one new change item).
- [x] 4.3 `python3 -m pytest tests/doc-health -q` — **1168 passed, 0 failed**
      (1163 before, five added), run under `set -o pipefail` so a masked failure
      cannot read as green. `tests/doc-health/test_pin_reachability.py` alone:
      **53 passed** (48 before).
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
- [ ] 4.9 MERGED AND GREEN ON MAIN. Open at pull request #429. The archive gate
      is merge-plus-green, the sequence was approved on 2026-08-27 (§ 1.5), and
      **the orchestrating session performs both halves** — it merges on green and
      dispatches the archive pass. This session pushed the rulings and stopped.

## 5. Open — deliberately not closed by this change

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
