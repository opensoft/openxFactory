# Tasks: decide-disposition-reading-per-family

Status: draft
Kind: tasks

`code_surface: none`, `target_release: none`. Under `release-realization` an
empty code surface archives ON LANDING plus its own task list rather than on
merged-plus-green realization evidence — so there is no realization group here,
and § 6 is the only thing between a ratified packet and its archive.

**NOTHING IS TICKED THAT DID NOT LAND.** Every ticked box below is a diff in
this pull request or a measurement reproducible from the command named beside
it, recorded verbatim in the pull request body.

**§ 1 (RATIFICATION) IS ENTIRELY OPEN AND IS THE POINT OF THIS PULL REQUEST.**
It carries ONE BOX PER CLASS. Brett Heap's word of 2026-09-11 (~18:20Z)
commissioned the AUTHORING and decided no wording; it is recorded as the origin
in `.openspec.yaml` and is not read as an approval.

**§ 4 (THE ARMS) IS OPEN ON PURPOSE AND MUST STAY OPEN UNLESS A CLASS IS
VETOED.** Under the four recommendations no arm is owed at all. Each box below
names what a particular veto would commission; **none of it is built here**, and
building any of it before the ruling is the one thing this packet must not do.

**§ 7 IS UNTICKED ON PURPOSE**: residue, measured and deliberately not taken.

## 1. Ratification — OWED, NOT GIVEN (one box per class)

- [ ] 1.1 **CLASS A — `modified-block-currency` (4 entries).** Brett Heap rules
      between (A1) NO CHANGE — canon's *A finding is dispositioned* at
      `openspec/specs/doc-health/spec.md` line 2177 already rules it
      (**RECOMMENDED**) — (A2) narrow it to `info`-with-citation, or (A3) widen
      it to archived delta paths. This box ticks by NAMING the word, its
      timestamp and where it is recorded, and by nothing else.
- [ ] 1.2 **CLASS B — `location-conformance` (10) + `document-catalog` (1), 11
      entries.** Brett Heap rules between (B1) DELIBERATELY IGNORE — no
      family-side reading; the entry stays a resolution citation
      (**RECOMMENDED**) — (B2) read and downgrade, or (B3) read and suppress.
- [ ] 1.3 **CLASS C — `proposal-origin` (8), `record-immutability` (5),
      `semantic-contradiction` (1), `semantic-normative-prose` (1), 15 entries.**
      Brett Heap rules between (C1) DELIBERATELY IGNORE — no family-side reading;
      the entry is a governance record and the finding keeps its band
      (**RECOMMENDED**) — (C2) read and downgrade to `info` with the citation, or
      (C3) read and suppress. **This is the class with a live population: ten of
      the fifteen draw a finding today.**
- [ ] 1.4 **CLASS D — `uncited-resolution` (1 entry).** Brett Heap rules between
      (D1a) RECORD THAT IT IS INERT AND LEAVE IT (**RECOMMENDED**), (D1b) teach
      the arm to read its own family's entries, or (D1c) retire the entry in
      `opensoft/xFactory`.
- [ ] 1.5 **THE PACKET'S OWN SHAPE (`design.md` D3).** Brett Heap rules between
      DECISION ONLY with `code_surface: none` (**RECOMMENDED**) and declaring a
      code surface now for a regression test pinning the boundary. A veto of any
      of 1.1–1.4 toward a reading arm changes `code_surface` at that ruling.
- [ ] 1.6 On the ruling, and only then: every document in this packet takes
      `Status: ratified` with exactly one citation line, `.openspec.yaml` gains
      `approved_by`/`approved_on` **ADDED BESIDE** the byte-unmoved drafting
      provenance, and a `review/ratification-<date>.md` record is written
      carrying `Status: ratified` and one citation.

## 2. The measurement — DONE IN THIS PULL REQUEST

- [x] 2.1 The file read at a NAMED sha, not carried from the issue:
      `opensoft/xFactory` `main` `0ecb370e8fec2c1ac78498adf8f6a4ea3ca1c9bb`,
      `health/dispositions.yaml` blob
      `9458d6c2794f0c0a937a82f7f58b802ab4b4027b`, sha256
      `4d9034e34f4189ddf1d08c9a9cffbe467747357ac28cfdc3906701d9577a1c60`, 1701
      lines, root a list, **49 entries** — **18** `ratified-provenance` and
      **31** across eight families. The issue's table was taken at `ecb0cade`
      and is a snapshot; this is the figure this packet carries.
- [x] 2.2 An aggregation-shaped rig assembled and every family run against it:
      `openxFactory` `8015d45fdf68b7bf60abb79dd152585d1a4330fd`, `codexFactory`
      `dc67ad82cf4dd522e6fe033b1e56424bb1086630`, `OpsxFactory`
      `7368cb49830cb332f9afce33c404671c6b92f8bb`, `MedxFactory`
      `9f125a6ae2f12669e10822dd1123f824aedcae36` — the only four repositories the
      thirty-one entries name. `python3 scripts/doc-health.py --repo-root <rig>
      --family <f>`, exit 0 for each of `location-conformance`,
      `proposal-origin`, `record-immutability`, `modified-block-currency` and
      `document-catalog`.
- [x] 2.3 Per-entry outcome measured and tabulated (`design.md` D0.2): **10
      matched**, **7 unmatched with the target present**, **11 target vanished**,
      **3 not deterministically measurable**. Asserted as a set test and not as a
      count: **zero** of the thirty-one names a path under
      `openspec/changes/archive/`.
- [x] 2.4 The CONTROL taken (`design.md` D0.3): the real file replaced by `[]`
      and all five deterministic families re-run — 7/7, 130/130, 16/16, 48/48,
      1/1 plan rows, `diff` of the row sets empty in every case. The file was
      restored and its sha256 re-verified against 2.1 afterwards.
- [x] 2.5 The one arm that reads them proved (`design.md` D0.4): 31 synthetic
      `class="contested"` ranked-plan rows through `report.parse_previous` →
      **30 admitted**; `report.uncited_resolutions` → **30** findings with an
      empty disposition set and **0** with the real file; the single row refused
      admission is the `uncited-resolution` entry itself.
- [x] 2.6 Every reader of the file enumerated by grep across
      `scripts/doc_health/`, and the four families for which CANON declares a
      reading located by heading and line: `promotion-fidelity` (1174),
      `duplicate-packet` (1289), `modified-block-currency` (2177),
      `ratified-provenance` (938). Exactly one of the eight families holding
      entries is among them.

## 3. The delta — DONE IN THIS PULL REQUEST

- [x] 3.1 `## MODIFIED Requirements` over *Finding severity and regression
      handling*, the requirement that owns severity, resolution class and the
      contested-resolution rule for the whole estate — the only family-neutral
      home for a decision about eight families.
- [x] 3.2 The block is canon's own bytes, SLICED and not transcribed: lines
      **198–229** of `openspec/specs/doc-health/spec.md` at `8015d45f`, sha256
      `91e9a13d1fb948b94da3668818ee4f655068807ca4a9a110de53508acbd85d53` on both
      sides. No body paragraph added, edited or removed; no promoted scenario
      moved, retitled or stripped of a bullet; no marker declared, nothing having
      been removed to declare.
- [x] 3.3 ONE `#### Scenario:` appended — *A recorded disposition names a family
      this capability gives no reading* — saying four things: such an entry
      changes no standing finding; it is still read by the contested-resolution
      rule, which is the one effect it has ever had; a family that DOES declare a
      reading is read exactly as its own declaration says, neither widened nor
      narrowed; and an entry naming `uncited-resolution` itself changes nothing
      at all.
- [x] 3.4 ACTIVE-delta sibling search over the heading modified:
      `grep -rn "Finding severity and regression handling" openspec/changes/ |
      grep -v /archive/` returns NOTHING, and the only two active
      `specs/doc-health/` deltas are `add-nightly-dashboard-refresh` (7 ADDED, none
      this one) and `settle-aging-staging-topics` (1 MODIFIED, *Aging threshold
      defaults*). No two-writers collision; `sequenced_after: []` stands on that
      measurement.

## 4. The arms a VETO would commission — SCOPED, NOT BUILT

- [ ] 4.1 **ONLY IF CLASS B OR CLASS C IS VETOED toward (B2)/(B3)/(C2)/(C3):** one
      SHARED helper in `scripts/doc_health/`, called by each opting-in family
      with its own family name, delegating the admission rule to
      `promotion_fidelity.load_dispositions(ctx, <family>)` so a second rule
      about which entries are live is never written — the shape the parent cut
      for `ratified-provenance`, one level up. Per-family OPT-IN, never a blanket
      sweep.
- [ ] 4.2 **ONLY ON THAT VETO:** the `## MODIFIED` blocks the vetoed families'
      own requirements then owe, each with its own *A finding is dispositioned*
      or grandfather scenario, and the tests that pin them.
- [ ] 4.3 **ONLY ON THAT VETO:** `code_surface` and `target_release` re-declared
      at the ratification to name the modules and tests, and the archive moved to
      merged-plus-green realization evidence for that reason.
- [ ] 4.4 **ONLY IF CLASS A IS VETOED:** the `## MODIFIED` over
      `modified-block-currency`'s promoted *A finding is dispositioned*, plus the
      change in `scripts/doc_health/modified_block_currency.py` that a narrowing
      or widening implies.
- [ ] 4.5 **ONLY IF CLASS D IS VETOED toward (D1b):** the re-opening of issue
      #515's echo is designed for and tested against before any line is written.
      Named here so the cost is visible at the ruling and not discovered after.

## 5. Verification — RUN IN THIS PULL REQUEST

- [ ] 5.1 `OPENSPEC_TELEMETRY=0 openspec validate decide-disposition-reading-per-family --strict`
      on the PATH CLI and on the pinned CLI, with the exit codes and the output
      recorded in the pull request body.
- [ ] 5.2 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` on both CLIs,
      with this branch's failure set compared against `origin/main`'s and the
      comparison stated as identical or not.
- [ ] 5.3 `python3 scripts/proposal-support.py . verify decide-disposition-reading-per-family`.
- [ ] 5.4 `python3 -m pytest tests/doc-health -q` and the full
      `python3 -m pytest -q`, with exit codes.
- [ ] 5.5 `python3 scripts/doc-health.py --single-repo .` tail,
      `python3 scripts/validate-sequenced-after.py .` and
      `python3 scripts/validate-scope-globs.py .`, with exit codes.
- [ ] 5.6 The corpus-ledger row seeded by the sanctioned tool after this pull
      request exists — `python3 scripts/validate-sequenced-after.py . --seed-ledger
      --moved-by '#<PR>'` — as its own commit, and `--ledger-diff` run after it.

## 6. Archive — OWED, NOT GIVEN

- [ ] 6.1 On a separate word after ratification: promote the `## MODIFIED` block
      into `openspec/specs/doc-health/spec.md` and archive the packet with
      `proposal-support.py`, never with bare `openspec`.
- [ ] 6.2 `Closes #966` is written in the ARCHIVE pull request's body and in NO
      commit message on this branch or that one.
- [ ] 6.3 The README "OpenSpec Records" ACTIVE row is moved to the archived
      block in the same act.

## 7. Measured, and deliberately NOT taken here

- [ ] 7.1 **NO TEST PINS THE BOUNDARY** the added scenario states. `design.md`
      D3 takes that deliberately — the control run in D0.3 proves the property on
      demand and a test would be the first inch of an arm the ruling has not
      commissioned — and records the trade-off: a future refactor could break the
      boundary silently. A successor may pick it up under its own word.
- [ ] 7.2 **THE STALE-ENTRY POPULATION OUTSIDE `ratified-provenance` IS MEASURED
      AND HANDED TO [#965](https://github.com/opensoft/openxFactory/issues/965),
      NOT ACTED ON**: **11** of the thirty-one name a path that no longer exists
      in the repository it names, and **7** more name a present path that draws
      no finding of that family. No finding class is graded and no severity is
      chosen here.
- [ ] 7.3 **`docs/doc-health.md` IS NOT EDITED.** Its only description of this
      file is the neutrality lane's *Dispositions keying* paragraph (line 341),
      accurate about that lane and silent about the estate-wide reading this
      packet decides. The documentation sweep is
      [#967](https://github.com/opensoft/openxFactory/issues/967).
- [ ] 7.4 **THE `--single-repo` SCOPE IS LEFT WITHOUT DISPOSITIONS**, which is
      [#968](https://github.com/opensoft/openxFactory/issues/968) and `design.md`
      D4. The added scenario is written to say nothing about scope.
- [ ] 7.5 **THE THIRTY-ONE CITES ARE NOT RE-VERIFIED.** Whether each disposer's
      ground was sound was that authority's act; re-litigating it in a checker is
      not this capability's authority (`doc-health`, *Semantic finding
      disposition authority*).
