# Tasks: add-target-release-deferred-allocation

Status: ratified
Ratified by: Brett Heap, 2026-09-13T01:0xZ — verbatim "accept all A on 1022" (record `review/ratification-2026-09-13.md`)
Kind: tasks
Lane: hermes-wallet-exercise

## 1. Ratification — GIVEN 2026-09-13, Brett Heap's and nobody else's

- [x] 1.1 Brett Heap rules `proposal.md` § Open questions OQ-1 … OQ-10. The
      recommended option in each is what this packet already encodes, so
      **`accept all A on <n>` ratifies and moves not one byte**; any other
      answer rewrites the requirement it names first. **RULED: Brett Heap,
      2026-09-13T01:0xZ, verbatim "accept all A on 1022"** — all ten OQs at
      their RECOMMENDED option (`proposal.md` § Rulings;
      `review/ratification-2026-09-13.md`).
- [x] 1.2 On the word: `Status: draft` → `Status: ratified` on `proposal.md`,
      `design.md` and this file, each gaining a `Ratified:` line naming the
      human, the UTC instant as GIVEN (never invented) and the verbatim word;
      `.openspec.yaml` gains `approved_by` / `approved_on` **ADDED BESIDE** the
      untouched drafting pair (`add-drafted-proposal-origin`'s shape). The specs
      delta carries no lifecycle header and has none to flip. **DONE** in this
      same commit; the instant is recorded `01:0xZ`, the precision the word was
      taken at, never invented finer. The delta's absence of a lifecycle header
      was CHECKED, not assumed. `design.md`'s ten `## D1 … D10` headers each
      gained an inline `— RULED (a), 2026-09-13T01:0xZ` marker and no other byte
      in that file moved.
- [x] 1.3 `review/ratification-<date>.md` records the word, the ten decisions as
      put and as ruled, what the word admits and does not, and what is owed
      after. **DONE**: `review/ratification-2026-09-13.md`, `Status: ratified`.
- [x] 1.4 `proposal.md` § Rulings filled, one line per OQ. **DONE**: a ten-row
      table, each row carrying `RESOLVED (a)` with the ruler, the instant and
      the verbatim word, plus the alternatives considered and not adopted; and
      the section states in terms that no delta byte moved as a result, proven
      by `git diff --stat` over `specs/` across the ratification commit.

## 2. Realization — IN THIS PULL REQUEST (OQ-10)

The precedent's shape exactly: `gate-realization-axis-vocabulary` carried its
validator, its register and its tests in the SAME pull request as its
ratification, and archived later on merged-plus-green.

- [ ] 2.1 `scripts/target_release.py`: `DEFERRED_ALLOCATION` beside
      `IMPLEMENTED`, admitted in `scan()` before the register lookup so the
      value is VOCABULARY and never an exception; `deferred_allocation` counted
      on `Report`; archived records carrying it counted separately and REPORTED,
      never judged (OQ-4).
- [ ] 2.2 `scripts/validate-target-release.py`: the two new counts printed.
      **`CLOSED_REGISTER` does not move** — this change admits a VALUE, not an
      ENTRY, which is the distinction the promoted sentence draws.
- [ ] 2.3 `scripts/target-release-register.yaml`: the `deferred-allocation`
      class note amended to record that canon now admits the value, that each
      of the twelve entries retires on its own packet's correction and not on
      this admission, and that the entry is deleted in the same pull request
      that makes the correction.
- [ ] 2.4 `tests/target_release/test_target_release_gate.py`: unit tests for the
      admitted token, for the doc-only refusal path, for the archived
      report-never-refuse behaviour, and for the class note's continued
      conformance. `test_corpus_target_release_validates` re-run green.
- [ ] 2.5 Re-measure and record both rows of `proposal.md` § The measurement on
      the tree this packet lands on.

## 3. Verification — IN THIS PULL REQUEST

- [ ] 3.1 `OPENSPEC_TELEMETRY=0 openspec validate add-target-release-deferred-allocation --strict`
- [ ] 3.2 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` — the same
      pre-existing `disposition-codexfactory-*` failures as `main` and zero new.
- [ ] 3.3 `python3 scripts/validate-sequenced-after.py .` — this packet declares
      `sequenced_after: [add-structured-scope-substrate]` and is the first
      arm's subject.
- [ ] 3.4 `python3 scripts/validate-target-release.py .` — exit 0.
- [ ] 3.5 `python3 -m pytest tests/target_release -q` — the full gate suite.

## 4. The first consumer — ANOTHER LANE'S ACT (OQ-9)

- [ ] 4.1 **NOT PERFORMED HERE.** After this packet lands, openxFactory #1017's
      own lane corrects `encode-wallet-authority-rulings-r6-r12/proposal.md`'s
      `target_release:` to `deferred-allocation` — one value token, the prose
      gloss preserved verbatim, the correction method
      `gate-realization-axis-vocabulary` D2 used for its own six.
- [ ] 4.2 `merge 1017 when green` (Brett Heap, 2026-09-13 ~00:2xZ) is already
      given and applies to that head unchanged; Rule 6 at landing.

## 5. Archive — OWED, NOT GIVEN

- [ ] 5.1 `code_surface` is NON-EMPTY, so this packet archives on
      MERGED-PLUS-GREEN realization evidence — this pull request merged into
      `main` and a green `pytest-suite` at the tree that merge carries — and on
      its own word, never on landing.
- [ ] 5.2 **THE ORDERING AGAINST `add-structured-scope-substrate`, STATED
      HONESTLY.** *Ordered deltas and branch vocabulary*'s ARCHIVE-ORDER hold
      keys on "a requirement the promoted specification does not carry", and
      canon carries *Realization axis declaration* — so that hold does NOT bind
      this packet, and the obligation it does owe is the REFERENCE-AND-DECLARE
      half, discharged by `sequenced_after:` and by a pre-text written from that
      change's outcome. The residual hazard is the one the requirement names in
      its own words — "whichever writer archives last is the text canon keeps":
      if this packet archives FIRST, the substrate's block, written over the
      older text, would on ITS archive drop the third value. So before archiving,
      re-read `add-structured-scope-substrate`'s block and either archive after
      it or have it carry the third value, and record which.

## 6. Measured, and deliberately NOT taken here

- [ ] 6.1 **THE TWELVE STANDING CARRIERS ARE NOT SWEPT** (OQ-7). Each retires
      when its owning packet corrects its own declaration, the register entry
      deleted in that same pull request — which the validator's exit-2 stale
      refusal already forces. Only the class NOTE moves here.
- [ ] 6.2 **THE "AGGREGATION REPOSITORY" WORDING IS NOT REPAIRED.**
      `gate-realization-axis-vocabulary` `tasks.md` § 6.2's separate successor
      over the same title; it would land in a MODIFIED block over *Realization
      axis declaration*, which this packet now carries — but folding it in would
      widen a ruled remedy into an unruled one, so it is named and left.
- [ ] 6.3 **`code_surface:` IS STILL NOT GATED** — § 6.3's successor,
      openxFactory [#1013](https://github.com/opensoft/openxFactory/issues/1013),
      unclaimed and untouched here.
- [ ] 6.4 **THE ARCHIVED RECORDS ARE NOT TOUCHED.** Frozen record: read,
      counted, judged never — and this packet's own new archive rule is written
      to bind the ARCHIVING ACT rather than the archived record, precisely so it
      creates no standing finding with no remedy.
- [ ] 6.5 **NO OTHER ESTATE REPOSITORY IS REACHED.** The validator takes a
      `REPO_ROOT` and this packet runs it only against `opensoft/openxFactory`.
