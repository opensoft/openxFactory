# Tasks: decide-disposition-reading-per-family

Status: draft
Kind: tasks

`code_surface: none`, `target_release: implemented` — the ratified vocabulary's
own doc-only default (*Realization axis declaration* admits `implemented` or a
named release and nothing else), with the absence of any contract release stated
as prose in `proposal.md` rather than smuggled into the value token. Under
`release-realization` an empty code surface archives ON LANDING plus its own task
list rather than on merged-plus-green realization evidence — so there is no
realization group here, and § 6 is the only thing between a ratified packet and
its archive.

**NOTHING IS TICKED THAT DID NOT LAND.** Every ticked box below is a diff in
this pull request or a measurement reproducible from the command named beside
it, recorded verbatim in the pull request body.

**§ 1 (RATIFICATION) IS ENTIRELY OPEN AND IS THE POINT OF THIS PULL REQUEST.**
It carries ONE BOX PER CLASS. Brett Heap's word of 2026-09-11 (~18:20Z)
commissioned the AUTHORING and decided no wording; it is recorded as the origin
in `.openspec.yaml` and is not read as an approval.

**§ 4 (THE ARMS) IS OPEN ON PURPOSE AND MUST STAY OPEN UNLESS A CLASS IS
VETOED.** Under the four recommendations NO ADDITIONAL arm is owed — Class A's
(A1) deliberately KEEPS the family-side reader `modified-block-currency` already
carries, which is a promoted declaration and not something this packet
commissions. Each box below
names what a particular veto would commission; **none of it is built here**, and
building any of it before the ruling is the one thing this packet must not do.

**HOW EVERY BOX CLOSES, AND THE GATE THAT FORCES THE QUESTION.**
`proposal-support.py`'s `archive_change` refuses a packet whose `tasks.md` still
carries an unchecked box — `if tasks.is_file() and re.search(r"^- \[ \]",
tasks.read_text(), re.M): raise SupportError("change has incomplete tasks")` —
so "deliberately open" is not a state this packet may carry INTO its archive, and
each open box below states the event that closes it:

- **§ 1** closes AT THE RULING, one box per class, ticked by recording Brett
  Heap's selection and the record path.
- **§ 4** closes AT THE SAME RULING and never before it. A box whose condition
  ("ONLY IF CLASS B OR CLASS C IS VETOED…") did NOT occur ticks as **NOT
  COMMISSIONED — the recommendation was accepted**, which is a disposition and
  not a silent drop; a box whose condition DID occur ticks by NAMING the
  successor packet or issue the veto commissions, the arm being built there and
  never here.
- **§ 5** closes IN THIS PULL REQUEST, and is ticked below with the real exit
  codes.
- **§ 6** closes AT THE ARCHIVE, which is a separate act on a separate word.
- **§ 7** closes BY RECORDING, on the estate's ruling of 2026-09-06 that an
  owed-successor box ticks when its successor is NAMED — the shape the parent's
  own § 7 archived in. Its boxes are ticked below: TWO of the six name a filed
  successor (#967, #968) and FOUR record a residue with no successor owed —
  #965 is NOT one of them, § 7.2 recording in terms that its residue is not
  handed there.

## 1. Ratification — OWED, NOT GIVEN (one box per class)

- [ ] 1.1 **CLASS A — `modified-block-currency` (4 entries).** Brett Heap rules
      between (A1) NO CHANGE — canon's *A finding is dispositioned* at
      `openspec/specs/doc-health/spec.md` line 2177 (at `origin/main` `d4d96cca`)
      already rules it
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
      (**RECOMMENDED**) — (C2) read and downgrade to `info` with the citation,
      (C3) read and suppress, or (C4) SPLIT THE CLASS on the measured status and
      rule `record-immutability`'s four `Status: record` targets separately.
      **This is the class with a live population: ten of the fifteen draw a
      finding today**, and (C4) exists because the status was measured directly
      rather than inferred from an archive-path prefix (`design.md` D0.2). This
      packet does NOT take (C4); it is put here so the split is ruled rather than
      assumed away.
- [ ] 1.4 **CLASS D — `uncited-resolution` (1 entry).** Brett Heap rules between
      (D1a) RECORD THAT IT IS INERT AND LEAVE IT (**RECOMMENDED**), (D1b) teach
      the arm to read its own family's entries, or (D1c) retire the entry in
      `opensoft/xFactory`.
- [ ] 1.5 **THE PACKET'S OWN SHAPE (`design.md` D3).** Brett Heap rules between
      DECISION ONLY with `code_surface: none` (**RECOMMENDED**) and declaring a
      code surface now for a regression test pinning the boundary. A veto of any
      of 1.1–1.4 toward a reading arm changes `code_surface` at that ruling.
- [ ] 1.6 On the ruling, and only then: every LIFECYCLE-BEARING document in this
      packet — `proposal.md`, `design.md` and `tasks.md`, and those three alone,
      `.openspec.yaml` and the spec delta carrying no lifecycle header by their
      own shape and taking none at ratification — takes
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
- [x] 2.5 The estate-wide arm's LOOKUP proved, and its CONDITION measured beside
      it (`design.md` D0.4): 31 synthetic `class="contested"` ranked-plan rows
      through `report.parse_previous` → **30 admitted**;
      `report.uncited_resolutions` → **30** findings with an empty disposition set
      and **0** with the real file; the single row refused admission is the
      `uncited-resolution` entry itself. **THE SYNTHETIC ROWS FORCE THE CLASS, SO
      THE REAL CLASSES WERE READ OFF THE SAME RIG RATHER THAN ASSUMED**: that arm
      iterates `previous_contested`, which `parse_previous` fills only from rows
      written `class="contested"`, and at the rig `location-conformance` is
      `contested` 7/7, `record-immutability` 16/16 and `modified-block-currency`
      48/48, while `proposal-origin` is **`auto-fixable` 130/130** and
      `document-catalog` **1/1**. 19 of the 31 belong to a contested family; 9 are
      admissible by key and unreachable on today's classes; the remaining 2
      (`semantic-contradiction`, `semantic-normative-prose`) are admitted by
      that same synthetic forcing (19+9+2=**30**, the figure this box opens
      with) but their reach is UNMEASURED here for a THIRD reason, deeper
      than a wrong class: this rig never exercises `semantic.enforce_contract`,
      which DOES emit a WARNING/CONTESTED finding for either family when a
      real semantic sweep runs, merged into `result.findings` before render
      (`runner.py:574`) — a real previous report CAN carry a `contested` row
      for them (§ 7.6(b) below measures exactly that gap), just not from a
      plain deterministic-only rig like this one, leaving the 31st
      (`uncited-resolution`'s own) as the only entry excluded from ADMISSION
      itself rather than reach.
- [x] 2.6 Every reader of the file enumerated by grep across
      `scripts/doc_health/` — `promotion_fidelity.load_dispositions` and its
      **FOUR** call sites, counted rather than summarised:
      `promotion_fidelity.py:813` (its own family), `duplicate_packet.py:410`,
      `modified_block_currency.py:2236` and `families.py:419`, the last being
      `fam_ratified_provenance`'s grandfather pass — so the parent's family is a
      caller of that same helper and not a separate mechanism;
      `neutrality.disposition_suppressions` reached through
      `runner._neutrality_scope` → `neutrality_dispatch`, and `runner.main`'s own
      unconditional read feeding `report.uncited_resolutions` — and the **FIVE**
      families for which CANON declares a reading located by heading and line:
      `promotion-fidelity` (1174), `duplicate-packet` (1289),
      `modified-block-currency` (2177), `ratified-provenance` (938) and
      `neutrality-drift` (681-685, *A rejected candidate stays rejected*, keyed
      by `(repo, path, content digest)`). **EXACTLY ONE of the eight families
      holding entries is among the five** — `modified-block-currency` — and NO
      entry in the population carries `family: neutrality-drift`, so that lane
      moves no figure and is recorded so the narrower "one reader" claim is not
      inherited.

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
- [x] 3.3 **TWO `#### Scenario:` blocks appended**, and it is two rather than
      one because the review round of 2026-09-11 was right that a rule about
      families WITH a declared reading could not live under a `WHEN` whose
      condition is the ABSENCE of one:
      (i) *A recorded disposition names a family this capability gives no
      reading* — such an entry changes no finding OF THE FAMILY IT NAMES; it is
      still read by the contested-resolution rule, which reaches a DERIVED
      `uncited resolution` finding and never the named family's own row, and only
      where the entry's own key was recorded `contested` IN THE IMMEDIATELY
      PREVIOUS REPORT — that ONE report's rows, `parse_previous` reading a
      single `--previous-report` and not a history of them (`report.py:374-383`)
      — and not from the later run's resolution classes, so a key that report
      recorded `contested` stays eligible for THAT TRANSITION even if the
      family's rows in the later, current run are `auto-fixable`, an
      eligibility that does not compound or persist beyond the one comparison
      — AND the later run
      actually EVALUATED the named family and repository (`spec.md:42` states
      the RECORDED-unavailable case, and `spec.md:43` refuses to ratify the
      gaps § 7.6 measures, where a run's scope excludes a family or repository
      without RECORDING it — measured at `report.uncited_resolutions`'
      `unavailable_families` / `unavailable_repos` guards, `report.py:424-427`,
      fed by `runner.main` 792-830 — `unavailable_families` built at 792 and
      extended at 807/809/811/823/830, `unavailable_repos` at 749 — and passed
      at the call site, `runner.py:831`); and an entry naming `uncited-resolution`
      itself changes nothing at all.
      (ii) *A recorded disposition names a family this capability does give a
      reading* — such an entry is read OVER THAT FAMILY'S OWN FINDINGS exactly as
      that family's own declaration says and by that declaration alone, the
      family-neutral contested-resolution rule still reaching it WHEREVER THAT
      RULE'S OWN EVALUATION SCOPE REACHES the named family and repository
      (`spec.md:50` says so in terms, so "by that declaration alone" cannot be
      read as displacing that rule; `spec.md:51`, added in the review round of
      2026-09-11, says a CITED entry missing a further family-specific key — a
      string `content_sha256`, for `neutrality-drift` — is still admitted by
      this same family-neutral reader, which tests only the cite, not that
      further key; and `spec.md:52` says the entry reaches nothing through
      that rule where its scope excludes the named family — measured at
      `runner.py:823` and `runner.py:830`, which add the ideation-readiness and
      neutrality-drift lanes to `unavailable_families` unconditionally because
      their findings are folded in AFTER the deterministic render, so those
      lanes' prior contested rows never enter the pass at all), and
      `spec.md:53` neither widens nor narrows it.
      No body paragraph is added, edited or removed; no promoted scenario moves
      or is retitled; scenario (ii) gained the one bullet named above
      (`spec.md:51`) since first authored, recorded here rather than left
      implicit, and no bullet is lost from either.
- [x] 3.4 ACTIVE-delta sibling search over the heading modified, RE-RUN on the
      committed tree after `origin/main` `c521504c` was merged, and scoped so it
      cannot match this packet's own files:
      `grep -rn "Finding severity and regression handling" openspec/changes/ |
      grep -v /archive/ | grep -v decide-disposition-reading-per-family` returns
      NOTHING (exit 1, no match). WITHOUT the third filter it returns exactly
      FOUR lines and all four are this packet's own — `proposal.md`,
      `specs/doc-health/spec.md`, this task file and `design.md`, the last two
      because each QUOTES the command it is reporting on — which is why the
      filter is part of the test and not a way of hiding a hit. The only two other active
      `specs/doc-health/` deltas are `add-nightly-dashboard-refresh` (7 ADDED,
      none this one) and `settle-aging-staging-topics` (1 MODIFIED, *Aging
      threshold defaults*). No two-writers collision; `sequenced_after: []`
      stands on that measurement. The LATE re-check for #965's packet is
      `design.md` D5, and it caught the change it was taken late to catch: PR
      #981 (`report-stale-grandfather-dispositions`) opened at 20:40Z and its
      delta's single heading, read off the branch, is *Governed corpus membership
      and the lifecycle scan set* — a DIFFERENT requirement, so neither packet
      owes `sequenced_after:` to the other.

## 4. The arms a VETO would commission — SCOPED, NOT BUILT

- [ ] 4.1 **ONLY IF CLASS B OR CLASS C IS VETOED toward (B2)/(B3)/(C2)/(C3), OR
      CLASS C IS SPLIT TOWARD (C4) WITH EITHER HALF GIVEN A READING:** one
      SHARED helper in `scripts/doc_health/`, called by each opting-in family
      with its own family name, delegating the admission rule to
      `promotion_fidelity.load_dispositions(ctx, <family>)` so a second rule
      about which entries are live is never written — the shape the parent cut
      for `ratified-provenance`, one level up. Per-family OPT-IN, never a blanket
      sweep.
- [ ] 4.2 **ONLY ON THAT VETO OR THAT SPLIT:** the `## MODIFIED` blocks the vetoed families'
      own requirements then owe, each with its own *A finding is dispositioned*
      or grandfather scenario, and the tests that pin them.
- [ ] 4.3 **ON ANY VETO THAT COMMISSIONS RUNTIME WORK — (A2), (A3), (B2), (B3),
      (C2), (C3), a (C4) split giving either half a reading, or (D1b), and not
      only a Class B or C veto:** `code_surface` and `target_release` re-declared
      at the ratification to name the modules and tests, and the archive moved to
      merged-plus-green realization evidence for that reason. The condition is
      written as the full option list because every one of those options changes
      a module in `scripts/doc_health/` (§ 4.1, § 4.2, § 4.4, § 4.5), and a
      narrower condition would let a ruling leave `code_surface: none` standing
      over real runtime work — which `release-realization` would then archive on
      landing rather than on merged-plus-green evidence.
- [ ] 4.4 **ONLY IF CLASS A IS VETOED:** the `## MODIFIED` over
      `modified-block-currency`'s promoted *A finding is dispositioned*, plus the
      change in `scripts/doc_health/modified_block_currency.py` that a narrowing
      or widening implies.
- [ ] 4.5 **ONLY IF CLASS D IS VETOED toward (D1b):** `scripts/doc_health/report.py`
      (`parse_previous`'s anti-echo refusal, `UNCITED_RESOLUTION_FAMILY`) is the
      module a family-side reader for `uncited-resolution` would sit in, plus a
      NEW promoted requirement giving `uncited-resolution` its own reading —
      today none does — and the test that pins it; the re-opening of issue
      #515's echo is designed for and tested against before any line is written.
      Named here so the cost is visible at the ruling and not discovered after.

## 5. Verification — RUN IN THIS PULL REQUEST

**EVERY BOX BELOW IS TICKED ON A RUN TAKEN AT `0a5a1088`** — this branch with
`origin/main` `0805c3bb` merged — and every CONTROL was taken at `0805c3bb`
itself in a separate worktree, never in this clone; `origin/main` had not moved
between the control run and this one, verified by `git fetch` immediately
before. The whole set was RE-RUN at this head rather than carried forward from
the earlier runs at `f839bd06`, `ee243dd2` and `14dfd6e2`: each of the four
review rounds changed packet text, so the whole set was taken again after each
one rather than carried forward, and every figure came out the same at all four
heads. The only commit that follows `0a5a1088` on this branch is the one
that writes this section and the pull request body from that run's output; no
measured file changed after it. The exit codes are the commands' own, pasted
from the run and repeated in the pull request body.

- [x] 5.1 `OPENSPEC_TELEMETRY=0 openspec validate decide-disposition-reading-per-family --strict`
      on the PATH CLI (`openspec 1.2.0`) — **exit 0**, `Change
      'decide-disposition-reading-per-family' is valid` — and through the pin,
      `python3 scripts/validate-openspec-cli-pin.py --change
      decide-disposition-reading-per-family --no-cache` (`@fission-ai/openspec@1.12.0`,
      integrity verified) — **exit 0**, `Totals: 1 passed, 0 failed (1 items)`.
- [x] 5.2 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` on the PATH CLI
      — **exit 1**, `Totals: 101 passed, 2 failed (103 items)` — against
      `origin/main`'s **exit 1**, `Totals: 100 passed, 2 failed (102 items)`.
      **THE FAILURE SET IS IDENTICAL**, `disposition-codexfactory-declared-renames`
      and `disposition-codexfactory-floor-relocation-retitle` on both sides, a
      `diff` of the two sorted `✗` lists being empty; the one-item difference in
      the totals is this change itself passing. **THIS BOX TICKS ON THE RUN AND
      THE COMPARISON, NOT ON A CLAIM THAT THE CONSTITUTION'S PRINCIPLE V GATE IS
      SATISFIED.** `.specify/memory/constitution.md`'s Principle V states this
      exact command MUST pass, NON-NEGOTIABLE, before any commit is pushed, and
      it does not pass here: both failing changes are `Status: ratified` (2026-
      09-05) awaiting their own archive act, each with no `specs/` delta at all
      — a wholly separate, already-decided workstream this `code_surface: none`
      documentation packet has no authority to archive on someone else's behalf,
      and no delta of its own to add one to. Whether an IDENTICAL, pre-existing,
      unrelated failure satisfies Principle V for THIS pull request is a policy
      question this packet does not resolve — it is measured and reported, not
      repaired, the same shape as § 7.6's three gaps, and STAYS a question for
      whoever holds that gate's authority. `python3
      scripts/validate-openspec-cli-pin.py --all --no-cache` — **exit 0** on both,
      `0 UNDISPOSITIONED failures` with the SAME two accepted exceptions
      (`add-chain-attestation / signed-execution-chain/spec.md`,
      `add-composed-view-authoring / ideation-dashboard/spec.md`).
- [x] 5.3 `python3 scripts/proposal-support.py . verify decide-disposition-reading-per-family`
      — **exit 0**, `proposal support verification ok`.
- [x] 5.4 `python3 -m pytest tests/doc-health tests/sequenced_after
      tests/scope_globs tests/proposal-support -q --tb=no` — **exit 1**, `7
      failed, 2193 passed, 1 skipped` — against `origin/main`'s **exit 1**, `7
      failed, 2193 passed, 1 skipped`. **THE `FAILED` SET IS IDENTICAL**, a
      `diff` of the two sorted lists being empty: three `test_ideation_readiness`,
      one `test_readiness_dispatch`, two `test_sentinel_vocabulary` and one
      `test_status_reader_real_lines`. They are environment failures present on
      both sides and none of them names this packet.
- [x] 5.5 `python3 scripts/doc-health.py --single-repo .` — **exit 0**,
      `Findings: 32 critical, 11 error, 47 warning, 14 info`, **104 findings**,
      against `origin/main`'s **exit 0** and the same `32 / 11 / 47 / 14` = 104.
      With the repository label normalised the two finding sets are
      BYTE-IDENTICAL — 208 rendered rows each, `diff` empty — and NOT ONE finding
      names this packet: `grep -c decide-disposition-reading-per-family` over the
      report returns **0**. `python3 scripts/validate-sequenced-after.py .` —
      **exit 0** (41 active changes, 11 declaring the field).
      `python3 scripts/validate-scope-globs.py .` — **exit 0**.
- [x] 5.6 The corpus-ledger row was seeded by the sanctioned tool AFTER the pull
      request existed — `python3 scripts/validate-sequenced-after.py .
      --seed-ledger --moved-by '#978'` — as its own commit `6f4268b1`, and
      `python3 scripts/validate-sequenced-after.py . --ledger-diff` re-run at
      `0a5a1088` — **exit 0**, `per-change sweep ledger consistent with the
      corpus (204 rows)`.

## 6. Archive — OWED, NOT GIVEN

- [ ] 6.1 On a separate word after ratification: promote the `## MODIFIED` block
      into `openspec/specs/doc-health/spec.md` and archive the packet with
      `proposal-support.py`, never with bare `openspec`.
- [ ] 6.2 `Closes #966` is written in the ARCHIVE pull request's body and in NO
      commit message on this branch or that one.
- [ ] 6.3 The README "OpenSpec Records" ACTIVE row is moved to the archived
      block in the same act.

## 7. Measured, and deliberately NOT taken here — RECORDED IN THIS PULL REQUEST

**EVERY BOX BELOW IS TICKED BY THE RECORDING AND BY NOTHING ELSE.** No residue
is acted on: no arm is written, no finding class is graded, no severity is
chosen and no entry is edited. TWO of the SIX hand their residue to a NAMED
filed successor (#967, #968), which is the form the estate ruled on 2026-09-06
and the form the parent's own § 7 archived in; FOUR record a residue that owes
no successor and say so.

- [x] 7.1 **NO TEST PINS THE BOUNDARY** the two added scenarios state. NO SUCCESSOR
      IS OWED and none is named — this box ticks on the recording of the
      trade-off, not on a hand-off. `design.md`
      D3 takes that deliberately — the control run in D0.3 proves the property on
      demand and a test would be the first inch of an arm the ruling has not
      commissioned — and records the trade-off: a future refactor could break the
      boundary silently. A successor may pick it up under its own word.
- [x] 7.2 **THE STALE-ENTRY POPULATION OUTSIDE `ratified-provenance` IS MEASURED
      AND RECORDED AS UNASSIGNED RESIDUE — NOT ACTED ON, AND NOT HANDED TO
      [#965](https://github.com/opensoft/openxFactory/issues/965)**: **11** of the
      thirty-one name a path that no longer exists in the repository it names, and
      **7** more name a present path that draws no finding of that family. The
      hand-off an earlier draft of this box recorded was RE-MEASURED against
      #965's own packet (PR #981) and was wrong: #981's D5 and `proposal.md` both
      say the other eight families' 31 entries are #966's subject, and its arm is
      narrow by construction (`_grandfather_cites` asks
      `promotion_fidelity.load_dispositions(ctx, "ratified-provenance")`), so it
      could not report them however the file grows. **NO SUCCESSOR IS NAMED FOR
      THIS RESIDUE** — naming one is an act for Brett Heap's word — and this box
      ticks on the RECORDING of the measurement and of the absence of an owner,
      never on a hand-off. No finding class is graded and no severity is chosen
      here.
- [x] 7.3 **`docs/doc-health.md` IS NOT EDITED**, and the reason was RE-MEASURED
      after `origin/main` `0805c3bb` merged #977 (issue #967's own sweep), which
      rewrote that file's family table. It now describes this file in THREE
      places, not one: the *Ratified provenance* row (line 50) states the
      parent's downgrade pass, the *Promotion fidelity* row (line 60) states that
      family's skip, and the neutrality lane's *Dispositions keying* paragraph
      (line 352, moved from 341) states the digest-keyed suppression. All three
      describe a reading a family's OWN requirement already declares, and not one
      of them says what an entry means for a family that declares none — which is
      the gap this packet decides, and why the file still needs no edit from it.
      The documentation sweep is
      [#967](https://github.com/opensoft/openxFactory/issues/967).
- [x] 7.4 **THE `--single-repo` SCOPE IS LEFT WITHOUT DISPOSITIONS**, which is
      [#968](https://github.com/opensoft/openxFactory/issues/968) and `design.md`
      D4. The review round of 2026-09-11 was right that silence invited being
      read as a promise the code does not keep: both added scenarios' `WHEN`
      now names the aggregation-checkout scope in terms, so a `--single-repo`
      run is outside either `WHEN` and neither scenario states anything about
      it.
- [x] 7.5 **THE THIRTY-ONE CITES ARE NOT RE-VERIFIED.** Whether each disposer's
      ground was sound was that authority's act; re-litigating it in a checker is
      not this capability's authority (`doc-health`, *Semantic finding
      disposition authority*). NO SUCCESSOR IS OWED and none is named; this box
      ticks on the recording of the limit.
- [x] 7.6 **THREE GAPS BETWEEN THE CONTESTED-RESOLUTION ARM'S SCOPE AND WHAT IT
      RECORDS ARE MEASURED AND REPORTED, NOT REPAIRED.** The review rounds of
      2026-09-11 were right that a `MUST NOT emit` written over "the run did not
      evaluate it" would have promised behaviour the shipped code does not give,
      so the scenario was narrowed to what the run RECORDS and a bullet refuses
      to ratify any of the three. Measured at `origin/main` `972b484a` (byte-
      identical to `0805c3bb` over every file these gaps cite — `git diff
      0805c3bb..972b484a -- scripts/doc_health/` is empty):
      (a) an UNSTAMPED previous report is accepted with `unavailable_repos` left
      EMPTY (`runner.py:686-702`, the issue #342 backward-compatibility branch,
      which warns on stderr and proceeds), so a subset-scoped run diffed against
      a legacy baseline can emit an `uncited resolution` for a repository it
      never evaluated; (b) `semantic.SEMANTIC_FAMILY_IDS`
      (`semantic-normative-prose`, `semantic-contradiction`) are NOT members of
      `runner.FAMILIES` — verified by import — so `set(FAMILIES) - {args.family}`
      never contains them, and `runner.py:810-811` adds them only when a sweep
      was requested AND skipped; a `--family X` run whose baseline carried a
      contested semantic row can therefore emit against it; (c)
      `unavailable_families` is built ENTIRELY in `runner.main`
      (`runner.py:792-811`, `823`, `830`) from `args.skip_family`,
      `args.family` exclusivity and the two always-on lane additions — NEVER
      from `run_suite`'s OWN, entirely separate bookkeeping of a family's
      returned `Skip` result (`runner.py:224-277`, appended only to
      `result.skips` at line 272 and never read back by `runner.main`): a
      family whose `fn(ctx)` returns an ordinary `Skip` on its own initiative
      (e.g. `fam_modified_block_currency` returning `Skip(FAMILY, "no
      repository in scope carries an `openspec/changes/` directory this
      family can read")` at `modified_block_currency.py:2232-2234`) leaves
      `unavailable_families` untouched, so a family whose check simply found
      nothing TO run against this time can have a prior contested row read as
      resolved without citation, the same shape as (a) and (b) one
      guard-condition over. **NONE OF THE THREE IS REPAIRED HERE**: all three
      are runtime defects in `scripts/doc_health/`, this packet declares
      `code_surface: none`, and building any of the three arms before the
      ruling is the one thing it must not do. **NO SUCCESSOR IS NAMED** —
      naming one is an act for Brett Heap's word — and this box ticks on the
      recording of the three measurements and of the scenario's refusal to
      ratify them.
