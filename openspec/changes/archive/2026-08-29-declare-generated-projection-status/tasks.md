# Tasks: declare-generated-projection-status

Every read-back was measured on 2026-08-28 in a fresh worktree off
`origin/main` at `6d100e51`.

## 0. Baseline and scope

- [x] 0.1 Record the families this change can touch, before anything moves.
      **DONE.** `record-immutability` **5 critical**; `status-validity`
      4 error (the sibling packet's, on another branch, untouched here);
      `promotion-fidelity` 0; `ratified-provenance` 0.
- [x] 0.2 Measure the size of the class this change is for.
      **DONE — EXACTLY ONE DOCUMENT.** Every `*.md` under the five governed
      roots scanned for a GENERATED / do-not-edit marker inside the header
      window; `ideation/cross-reference.md` is the only hit. Stated plainly
      because it is the main argument against this change, and answered in
      OD-2 rather than hidden.
- [x] 0.3 Identify the adjacent artifacts that must NOT move.
      **DONE.** `health/ideation-readiness/*/*.yaml`,
      `health/derive-possibles/*/*.yaml` and the dated
      `health/reports/YYYY-MM-DD.md` are all generated and all correctly
      `record`: each is written ONCE to a dated path and a second run writes a
      different path. `openspec/specs/doc-health/spec.md:171-183` MANDATES
      `record` for the run report; that requirement is neither touched nor
      contradicted, because the line drawn here is re-derived-in-place versus
      captured-once and every one of those falls on the `record` side.
- [x] 0.4 Collision-check against the active set.
      **DONE — NO COLLISION.** One active change carries a
      `document-lifecycle` delta, `add-ideation-intent-plane`, and it is
      ADDED-only on `Gates happen on main`. This packet's only delta is a
      MODIFIED on `Controlled document status taxonomy`. No requirement name
      is claimed twice.
- [x] 0.5 Parse contract-bundle membership for every touched path.
      **DONE — NO BUNDLE OWED.**
      `contracts/schemas/ideation-dashboard-snapshot.schema.yaml` is the one
      edited file under `contracts/` and it is a member of NO
      `contracts/releases/*.digests.yaml` inventory; all 48 grepped, zero hits
      for it and for every other touched path. The inventories are confined to
      the hermes-runtime surface.

## 1. The consumer check, before choosing a value

- [x] 1.1 Enumerate every reader of `ideation/cross-reference.{md,yaml}` and
      ask which reads the `Status:` header.
      **DONE — tabulated in `proposal.md` § What was measured.** Non-readers:
      `validate-ideation-cross-reference.py` (keys on the YAML `kind:`), both
      `pin_class.py` registry rows (read only the pin line), the three
      `ideation_dashboard` readers (read the YAML), `document_catalog.py` (no
      branch on this path). Readers: `corpus.py` → `ctx.docs` (the file leaves
      the `record` stage census), `inventory.py` (records the literal value,
      no branch), and **`sync-notebooklm-books.py`, which is load-bearing.**
- [x] 1.2 Confirm the YAML sibling carries no status.
      **DONE — zero occurrences of the string `status`, any case, in 12,058
      lines.** It is also unreachable by doc-health regardless:
      `corpus.iter_doc_paths` globs `*.md`. **The whole problem lives in the
      `.md` alone**, so the YAML is not touched.
- [x] 1.3 Decide whether an EXISTING status could serve, rather than a new one.
      **DONE — NO, AND THIS IS THE MEASUREMENT THAT FORCED A NINTH VALUE.**
      `PROJECTED_STATUSES` is `{brainstorm, staged, draft, ratified,
      standard}`; anything in it would START pushing a 4,797-line generated
      index into a NotebookLM book. Outside it sit only `record` (the value
      being escaped), `superseded` and `retired` (both false about a live
      file). **No existing value is both honest and inert.**
- [x] 1.4 Confirm the taxonomy has a built extension point.
      **DONE.** `tests/doc-health/test_promotion_fidelity.py:635-643` exists
      for precisely this event — "A ninth standing added to
      `doc_health.TAXONOMY` and forgotten here would land in the
      presumed-ratified bucket in silence… This test is how it cannot" — and
      asserts `PRE_RATIFICATION | RATIFIED_OR_BEYOND == TAXONOMY`.

## 2. The vocabulary

- [x] 2.1 Add `projection` to `doc_health.TAXONOMY`.
      **DONE**, with the distinguishing test in a comment at the site: not
      "generated" (a `record` is generated too) but RE-DERIVED IN PLACE.
- [x] 2.2 Place it in `promotion_fidelity.RATIFIED_OR_BEYOND`.
      **DONE**, beside `record`, for the same reason: neither is a proposal
      standing, and that split's only question is whether a packet declared a
      standing BELOW ratification. Task 1.4's test asserts the two sets
      exhaust the taxonomy and passes.
- [x] 2.3 Add it to `sync-notebooklm-books.py`'s closed `STATUS_RE`
      alternation.
      **DONE.** Without this the document is unmatched and `scan()` skips it
      SILENTLY — the same outcome by accident. Listed, it is absent from
      `PROJECTED_STATUSES` and therefore skipped by RULE, exactly as `record`
      is. The reason is in a comment at the site.
- [x] 2.4 Add it to the `lifecycle_status` enum in
      `contracts/schemas/ideation-dashboard-snapshot.schema.yaml`.
      **DONE.** A value outside that enum fails snapshot validation and, per
      `scripts/ideation_dashboard/generator.py:415-427`, "poisons the entry"
      and "DoSes the nightly lane". `generator.py`'s `LIFECYCLE_STATUSES`
      derives from `TAXONOMY` and needs no edit.

## 3. The generator and the file

- [x] 3.1 Make the generator emit the new header.
      **DONE** — `scripts/render-ideation-cross-reference.py`, the ONE line
      that writes it. All three writers of this file funnel through
      `render_markdown()` — the renderer itself, `bootstrap-ideation-cross-reference.py`
      (which subprocesses it), and the nightly
      `doc_health/ideation_readiness.py` lane (which imports it) — so one edit
      covers every path and **regeneration cannot reintroduce `record`.**
- [x] 3.2 Prove the regeneration is deterministic BEFORE trusting it.
      **DONE, both directions.** Before changing the emitter, the renderer was
      run against the committed YAML into a scratch path and diffed against
      the committed `.md`: **byte-identical**. After changing it, the
      regenerated file differs from the committed one in **exactly one line**.
      So the new header is the only thing this change writes into that file.
- [x] 3.3 Regenerate `ideation/cross-reference.md`. **DONE** — 290 clusters,
      one-line diff.
- [x] 3.4 Update `docs/document-lifecycle.md`.
      **DONE**, three edits: the taxonomy table gains a `projection` row and
      the `record` row is corrected to say CAPTURED ONCE; the "Generated
      evidence … is always `record`" bullet is corrected and followed by the
      rule that being generated is not what makes a document a record, being
      captured is; and the Gates-In-Practice line gains its clause.

## 4. Canon

- [x] 4.1 MODIFIED delta on `document-lifecycle`.
      **DONE** — one MODIFIED requirement, `Controlled document status
      taxonomy`, restated in full including the seven scenarios it does not
      touch (OD-4). Adds the `projection` standing paragraph with its
      re-derivation test, splits `A generated artifact is stored` into a
      captured-once case and a re-derived case, and ADDS a scenario binding
      the GENERATOR to emit the value so a later regeneration cannot
      reintroduce the old one.
- [x] 4.2 Declare the scenario RENAME to the marker arm.
      **DONE, and it was the check that demanded it.**
      `modified-block-currency`'s scenario-title arm raised a WARNING that the
      block "omits 1 of the 8" scenario titles — correctly: the split renames
      `A generated artifact is stored`. The house instrument for a retitle is
      `**Merged into ... by <change-id> (<date>):**`, not `Removed from canon
      by`, because the bullets are carried rather than dropped. One marker
      line added; **the scenario arm now reads ZERO.**
- [x] 4.3 Discharge the `modified-block-currency` SELF-GATE.
      **DONE.** That gate compares its named subject set with `==`, so any new
      MODIFIED block in the active set fails it by design. One row added to
      `_LEDGER_SUBJECTS` naming this packet's subject, recording that the two
      uncarried units are exactly the two the widening rewrites, that the
      title half is discharged by the 4.2 marker, and the retirement
      condition. **`pytest test_modified_block_currency_self_gate.py` —
      15 passed.**
- [x] 4.4 Add the regression test.
      **DONE** — `tests/doc-health/test_families.py`, asserting BOTH halves,
      because either alone would be the wrong fix: `projection` must be a
      CONTROLLED value (so `status-validity` stays silent — the file is not
      merely unrecognised) AND not a record (so `record-immutability` never
      reaches it). Both runs use the SAME `FakeGit`, so the only difference
      between them is the status value. Then the negative-then-positive
      pairing: the same file re-declared `record`, against the same git, still
      reports the critical — the exemption is not blindness.
- [x] 4.5 README active-changes entry. **DONE.**

## 4a. Gates

- [x] 4a.1 `OPENSPEC_TELEMETRY=0 openspec validate
      declare-generated-projection-status --strict` — **valid**.
- [x] 4a.2 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` —
      **77 passed, 0 failed (77 items)**, grown by exactly one for this packet
      joining the active set.
- [x] 4a.3 `python3 -m pytest tests/doc-health -q` under `set -o pipefail`,
      exit read from `$?` — **1250 passed, 0 failed**, 158.48s, **EXIT=0**, at
      the branch point. Baseline 1249; grown by exactly the one regression test
      4.4 adds. **RE-MEASURED AFTER `origin/main` WAS MERGED IN**, and both
      numbers are kept rather than the later overwriting the earlier: main
      landed `add-unclassified-finding-class`, which touches
      `scripts/doc_health/modified_block_currency.py` and adds twenty-one
      tests and a fixture repository, so the merged head reads **1271 passed,
      0 failed**, 156.73s, EXIT=0 — grown by main's twenty-one and by none of
      this packet's. `test_modified_block_currency_self_gate.py` merged
      cleanly and its ledger carries eight subjects: main's seven and this
      packet's one.
      **RE-MEASURED AGAIN 2026-08-28 after `origin/main` was merged a SECOND
      time**, proactively rather than on a conflict report, so this packet does
      not race its sibling's merge. Main had since landed `#463` (the
      measured-latents filing) and `#469` (archiving
      `add-unclassified-finding-class`, whose twenty-one tests this branch
      already carried from the first merge). The merged head **holds at 1271
      passed, 0 failed**, 188.24s, EXIT=0 — unmoved, because the second merge
      brought governance text and an archive act rather than tests.
      `openspec validate --all --strict` moved 77 → **78 passed, 0 failed**
      (main's two new active packets), and the floor is **unmoved at 4 critical
      / 11 error / 41 warning / 12 info**.
- [x] 4a.3b Resolve the `README.md` conflict main's landing created.
      **DONE — same shape as the sibling's.** `#463` added two active-change
      entries at the head of the OpenSpec Records block where this packet had
      added one: a pure both-sides-inserted-at-the-head conflict in
      `README.md` ALONE. Every code file, the delta, the regenerated
      projection and both test files merged clean, and the taxonomy value and
      the self-gate ledger row were re-checked present afterwards. **Resolved
      by keeping BOTH sides**, this packet's entry at the head as the newest
      arrival and main's two blocks verbatim beneath it. Zero conflict markers
      after; each of the three entries appears exactly once; nothing of
      main's dropped, reworded or reordered.
- [x] 4a.3c Merge `origin/main` a THIRD time, after the sibling packet landed.
      **DONE 2026-08-28.** `clean-doc-health-floor` merged as `#465`
      (merge commit `c79d6e54`) and main also gained `#475`, `#472`, `#471` and
      the wallet-v1.2 register pair. **TWO conflicts, both both-sides-added:**
      (a) `README.md`, the OpenSpec Records block again — resolved keeping BOTH,
      this packet's entry at the head and **MAIN'S version of the
      `clean-doc-health-floor` entry taken verbatim**, since that entry now
      reflects the landed state main holds; verified byte-identical to
      `origin/main:README.md` by diff rather than by eye. (b)
      `tests/doc-health/test_modified_block_currency_self_gate.py`, where the
      sibling's ledger row and this packet's landed at the same spot —
      resolved keeping BOTH rows, since `clean-doc-health-floor` is merged but
      still ACTIVE, so its MODIFIED block is still in the set that arm reads.
      The ledger now carries NINE subjects. Every other file merged clean, and
      the `projection` value was re-checked present at all seven of its sites
      afterwards. **No status-consumer file this packet touches moved in the
      merge**, verified by diffing the merge against its first parent.
      **RE-VERIFIED ON THE MERGED HEAD:** `openspec validate
      declare-generated-projection-status --strict` valid; `--all --strict`
      **79 passed, 0 failed**; `pytest tests/doc-health -q` under pipefail
      **1279 passed, 0 failed, EXIT=0**; the census still reads
      `projection 1 / record 29`, and `ideation/cross-reference.md` is still
      absent from `record-immutability`'s four criticals.
      **THE FLOOR NOW SHOWS BOTH PACKETS AT ONCE — 4 critical / 7 error / 41
      warning / 13 info**, against the 5 critical / 11 error this session
      started from: the sibling's four cleared errors and this packet's one
      cleared critical, on one branch for the first time. The thirteenth info
      is the sibling's own MODIFIED-block subject, now reported here too.
- [x] 4a.4 The suites that own the edited `contracts/` schema were run too,
      because `tests/doc-health` does not read it — `tests/ideation-dashboard`,
      `tests/ideation_dashboard` and `tests/notebooklm`, the three that
      reference `ideation-dashboard-snapshot` or `lifecycle_status`.
      **DONE — 4869 passed, 16 skipped, 26 subtests passed, 0 failed**, 786.79s
      (13m06s), under `set -o pipefail` with the exit read from `$?`. Widening
      an enum is additive and no test pins its contents — verified by grep
      before the run and confirmed by it.
- [x] 4a.4b Run the two repo validators that own the artifacts this change
      edits, per the house rule that the local validator runs before pushing.
      **DONE.** `scripts/validate-ideation-dashboard-contracts.py` —
      **0 errors**, 4 warnings, all pre-existing `workbench-chat-turn`
      deprecation notices unrelated to this change. `scripts/validate-ideation-cross-reference.py`
      — **0 errors on `ideation/cross-reference.yaml`**, which is the file this
      change's regeneration reads and does not modify. It reports 3 errors on
      `tests/ideation-dashboard/fixtures/base-repo/ideation/cross-reference.yaml`
      (`readiness/tiers/*: 'evidence' is a required property`); **these are
      PRE-EXISTING and not this change's**, verified rather than asserted — the
      same three appear on a sibling branch carrying none of these edits, the
      fixture is untouched here, and the missing field has nothing to do with a
      `Status:` header.
- [x] 4a.5 Full doc-health single-repo run, before vs after.
      **DONE — 5 critical / 11 error / 41 warning / 11 info → 4 critical /
      11 error / 41 warning / 12 info.** Exactly one critical cleared and it is
      `ideation/cross-reference.md`; **no error, warning or other critical
      moved.** The added INFO is `modified-block-currency` naming this packet's
      own MODIFIED block (task 4.3). The four remaining criticals are
      `docs/archive-record-discrepancies.md`,
      `docs/domain-ontology-adoption-handoff.md`,
      `docs/domain-ontology-pilot-report.md` and
      `docs/notebook-projection-migration-evidence-2026-08-24.md` — all genuine
      hand-maintained records, all untouched, all still firing.
- [x] 4a.6 Confirm the report's per-stage census renders the new stage rather
      than dropping or mis-bucketing it.
      **DONE — the table now carries `| projection | 1 | 36838 |` and `record`
      falls from 30 documents to 29.** One document moved between two stages
      and nothing else in the census did, which is the whole of this change's
      effect on the corpus measurement. (The `open (operational)` row still
      shows on this branch: it is the sibling packet's to clear and is not
      this one's business.)

## 5. Owed at realization

- [x] 5.1 **THE DISPOSITION ENTRY AT THE AGGREGATION ROOT.**
      `record-immutability` is CONTESTED, so a finding present in the previous
      report and absent from the current one is re-emitted by
      `report.uncited_resolutions` as an `uncited-resolution` ERROR unless an
      entry disposes it. `health/dispositions.yaml` does NOT exist in
      openxFactory — it lives only at the aggregation root — so the entry is
      owed in `opensoft/xFactory`, keyed
      `(record-immutability, openxFactory, ideation/cross-reference.md)` and
      **citing this change**. Not a silencer: the finding really is resolved
      by a cited change, which is the case that instrument exists to record.
      **This packet does not archive until it lands.**
      **REASSIGNED 2026-08-28 — the ORCHESTRATING SESSION writes it as part of
      the merge sequence, not this authoring session.** Left UNTICKED on
      purpose: reassignment is not discharge, the entry is still owed, and
      ticking it here would make the packet's own ledger claim an act nobody
      has performed. It ticks when the entry lands.
      **STILL UNTICKED AT THE ARCHIVE, 2026-08-29 (UTC) — AND MEASURED RATHER
      THAN ASSUMED, BECAUSE THIS IS THE ONE CONDITION THIS ARCHIVE DOES NOT
      MEET.** `/home/brett/projects/xFactory/health/dispositions.yaml` was read
      at this act: it carries THREE `record-immutability` entries and none of
      them is this one — `docs/domain-ontology-pilot-report.md`,
      `examples/patient-assembly/runs/08-connector-input/p1-divergence-report.md`
      and `docs/archive-record-discrepancies.md`. No entry keyed
      `(record-immutability, openxFactory, ideation/cross-reference.md)` exists.
      The obligation is therefore LIVE, and the mechanism is confirmed by
      reading the code rather than the packet's own summary of it:
      `report.uncited_resolutions` re-emits any contested finding that was in
      the previous report and is absent from the current one as an
      `uncited-resolution` ERROR unless `(family, repo, path)` is in
      `dispositions`. The last committed aggregation report,
      `health/reports/2026-08-26.md:235`, still names
      `openxFactory:ideation/cross-reference.md — record document changed after
      capture`, and the finding is gone from the merged tree — so the next
      aggregation nightly raises that ERROR until the entry lands.
      **WHY THE ARCHIVE PROCEEDS ANYWAY, STATED RATHER THAN SMOOTHED OVER.**
      The condition binds the moment the archive LANDS, not the moment it is
      composed, and the archive lands when this pull request MERGES. This
      session cannot discharge it: the aggregation root is another session's
      working tree by the lane it was given, and `health/dispositions.yaml` does
      not exist in this repository at all. **THE ENTRY MUST LAND BEFORE THIS
      PULL REQUEST IS MERGED**, and that is the sharpest item on the pull
      request body rather than a footnote. Ticking it here on a promise would
      be exactly the thing the paragraph above refuses.
      **DISCHARGED — AND THE PARAGRAPH ABOVE IS WRONG ABOUT THE FACT, KEPT AS
      WRITTEN BECAUSE THE ERROR IS INSTRUCTIVE.** The entry LANDED on
      2026-08-28, before this archive was composed. What the paragraph read was
      the SHARED CHECKOUT'S WORKING FILE at
      `/home/brett/projects/xFactory/health/dispositions.yaml`, a tree thirteen
      or more commits behind that repository's `origin/main` — so "measured
      rather than assumed" measured the wrong artifact, which is exactly what a
      working tree in a multi-session checkout produces and the reason the
      register must be read as
      `git -C /home/brett/projects/xFactory show origin/main:<path>`.
      Re-read that way the entry is there: aggregation commit
      **`20aafc4b0ad9befbd6309363d6a52a8107403600`** (2026-08-28T06:48:51-04:00,
      "Restore the dispositions register: 84656c6 dropped the pre-existing
      entries while appending one — every original entry is back verbatim, the
      new record-immutability disposition kept"), carrying at
      `health/dispositions.yaml:239-249` exactly the key § 5.1 named —
      `family: record-immutability`, `repo: openxFactory`,
      `path: ideation/cross-reference.md`, `severity: critical`,
      `disposer: openxFactory ratify gate`, `adjudicated_by: Brett (ruling
      2026-08-28, relayed by the orchestrating session)`, `date: 2026-08-28`,
      `cite: declare-generated-projection-status`. It is the CITED-RESOLUTION
      case the instrument exists to record rather than a silencer: its own
      rationale says the finding disappears because the document is no longer a
      record, nothing having been edited to satisfy the family. The
      `uncited-resolution` ERROR the paragraph above predicted for the next
      aggregation nightly therefore cannot arise, and this archive gate is met
      in full.
- [x] 5.2 Merge-plus-green on main: both required checks green on the
      proposing pull request, read back from the check-runs API rather than
      off the pull request page. **DISCHARGED 2026-08-28 AT THE ARCHIVE, and
      merged and green are ONE event here** — the realization RODE IN the
      proposing pull request, as § code_surface said it would. Pull request
      **#468** merged **2026-08-28T11:25:39Z** as merge commit
      `4d3f540d7a8c762e1077751b040a4839ae14e35f`, re-verified at this act rather
      than read off the pull request page: `git merge-base --is-ancestor
      4d3f540d origin/main` exits 0, and `git cat-file -p` shows a real
      TWO-PARENT merge (`c79d6e54` — the sibling packet's own merge, so the
      ordering Brett directed is legible in the graph — and `cb67a02d`). Green
      on the final head `cb67a02d`, ALL FOUR checks read back from the
      check-runs API: `pytest-suite` success (run 33165034882, 10:52:58Z →
      11:08:45Z, **selected 7637, passed 7616, skipped 21, failures 0,
      errors 0** read out of the job log rather than off a summary),
      `wallet-validation` success, `merge-master-approval` success,
      `copilot-pull-request-reviewer` success.
- [x] 5.3 Re-measure `record-immutability` on the merged tree and confirm it
      reads **4 critical**, with the four remaining being the genuine
      hand-maintained records and `ideation/cross-reference.md` absent.
      **DONE — THE PREDICTION HELD EXACTLY.** `python3 scripts/doc-health.py
      --single-repo .` over the merged tree at `6ce295c2`, before this archive
      act touched anything: **4 critical**, and they are
      `docs/archive-record-discrepancies.md`,
      `docs/domain-ontology-adoption-handoff.md`,
      `docs/domain-ontology-pilot-report.md` and
      `docs/notebook-projection-migration-evidence-2026-08-24.md` — the four the
      packet named, all genuine hand-maintained records, all untouched.
      `ideation/cross-reference.md` is ABSENT from the family, and the reason is
      readable in the file rather than inferred: its line 3 now says
      `Status: projection`, emitted by the generator itself. No family is
      skipped, no path is allowlisted, and no finding is suppressed — the
      document left the family because it stopped being a record.

## 6. Named follow-ups, out of scope here

- [ ] 6.1 **A projection's generator and source are declared in PROSE and
      nothing checks it** (Q1). Recommendation: leave it until a second
      projection exists — the rule-of-three has not fired, and a
      `Generated-by:` header would be a second new vocabulary item plus a new
      check for a class of one.
      **DISPOSITION AT THE ARCHIVE 2026-08-29 (UTC): CARRIED, NOT DISCHARGED.**
      Still a class of ONE — `ideation/cross-reference.md` is the only
      `projection` in the corpus at this act, confirmed by the per-stage census
      reading `projection | 1`. The rule-of-three has not fired, so the
      recommendation is unchanged and the box stays open on purpose, owned by
      whoever files the SECOND projection.

- [ ] 6.2 **Nothing stops a projection being re-classed to `record` to silence
      a real hand edit** (Q2) — the mirror image of the defect fixed here.
      Recommendation: the honest check is not on the status but on whether the
      committed bytes match what the declared generator produces
      (`--check`-mode regeneration in CI). That subsumes the question and
      deserves its own change rather than a guard bolted onto a family whose
      scope this packet deliberately did not touch.
      **DISPOSITION AT THE ARCHIVE 2026-08-29 (UTC): CARRIED, NOT DISCHARGED,
      and now a property of CANON rather than of an active delta.** The
      `document-lifecycle` block promoted by this act is what creates the
      re-class route, so the mirror-image gap it opens outlives the packet.
      Recommendation unchanged: the honest check is `--check`-mode regeneration
      in CI, comparing committed bytes against what the declared generator
      produces, which subsumes the question and deserves its own change rather
      than a guard bolted onto `record-immutability`, whose scope this packet
      deliberately did not touch.

- [ ] 6.3 **The four remaining `record-immutability` criticals are untouched**
      and are a different problem: genuine `Status: record` documents that are
      nonetheless hand-amended under the archive register's append discipline.
      That collision — a family whose remedy is "revert the content edit"
      against a discipline that appends — was named by
      `govern-openspec-corpus-membership` design.md Decision 3 and is still
      open.
      **DISPOSITION AT THE ARCHIVE 2026-08-29 (UTC): CARRIED, NOT DISCHARGED,
      AND RE-MEASURED.** All four still fire on the merged tree (§ 5.3), and
      none of them is a projection — each is a one-shot capture that was
      afterwards hand-amended. The collision named by
      `govern-openspec-corpus-membership` design.md Decision 3 — a family whose
      remedy is "revert the content edit" against a register discipline that
      APPENDS — is untouched by this change and remains open with that packet's
      decision as its record.

## 7. The veto window

- [x] 7.1 Record the rulings of 2026-08-28.
      **DONE.** By a multi-choice put to Brett by the orchestrating session and
      relayed the same day. Selections reaching this packet: **the `projection`
      SPELLING IS APPROVED** (OD-1 stands as authored) and **both pull requests
      merge on green**, which confirms OD-2's premise that this packet lands on
      its own gate. On both he took the packet's own recommendation, so **the
      clearance moved nothing** — none of the seven sites carrying the value is
      renamed and the delta is untouched. **OD-3 and OD-4 were NOT put to him
      and are NOT covered**; they stand as authored and remain flagged. No
      verbatim wording reached this session, so none is quoted; approver, date,
      mechanism and selections are recorded instead. The original flagged text
      is KEPT as marked history in `proposal.md` § Orchestrator decisions,
      because OD-1's argument is what a later reader naming a tenth standing
      will need.
- [x] 7.2 Confirm the ruling changed no artifact.
      **DONE — measured, not assumed.** `git diff` over the ruling commit
      touches `proposal.md` and `tasks.md` only. `doc_health/__init__.py`,
      `promotion_fidelity.py`, `sync-notebooklm-books.py`,
      `render-ideation-cross-reference.py`, the dashboard snapshot schema,
      `docs/document-lifecycle.md`, the regenerated `ideation/cross-reference.md`
      and both test files are byte-identical to what the ruling approved.
- [x] 7.3 **BEFORE ARCHIVE, THIS PROPOSAL'S OWN HEADER MUST MOVE OFF
      `Status: draft`.** The header is deliberately left at `draft`: "merge on
      green" is an authorization to land, and this session will not spell it as
      a ratification act Brett did not state. But it cannot stay `draft`
      through archiving — `promotion_fidelity.PRE_RATIFICATION` is
      `{brainstorm, staged, draft}`, so an archived proposal reading `draft`
      has its deltas discounted as archived design evidence rather than
      promoted canon, which would silently drop this packet's
      `document-lifecycle` MODIFIED block. **110 of 112 archived proposals read
      `ratified`.** The sibling packet measured this defect from the other end
      and its § 1.4 is the write-up. Whoever performs the archive owes the
      header and its citation, derived from the ruling record.
      **DISCHARGED 2026-08-28 BY THE ARCHIVING SESSION, ON BRETT'S RULING OF
      THE SAME DAY**, which directed the merge and the archive together and is
      what the citation names. `Status: draft` → `Status: ratified` plus one
      `Ratified:` line, written BEFORE `openspec archive` ran so it lands in the
      archived copy rather than being retrofitted onto it — which is also what
      makes the promotion of this packet's `document-lifecycle` block count as
      design evidence rather than being discounted. The line takes the
      record-citing spelling because no approving OpenSpec change exists to
      name, and clears its three-way floor on all three axes — approver
      (`by Brett`), date (`2026-08-28`), and a resolvable record path (§ 7.1 of
      this file, which records the selections). Nothing is quoted, because no
      verbatim wording reached the authoring session.

## 8. The archive act

Measured in this worktree at `6ce295c2` (`origin/main` at the act), before and
after `openspec archive`, and re-read rather than predicted.

- [x] 8.1 THE MERGE, READ OUT OF GIT. § 5.2 carries it in full: pull request
      #468, merge commit `4d3f540d`, an ancestor of `origin/main` by
      `git merge-base --is-ancestor` (exit 0) and a real two-parent merge whose
      FIRST parent is `c79d6e54`, the sibling packet's own merge — so the order
      Brett directed is legible in the graph rather than only in the prose.
- [x] 8.2 THE HEADER MOVED FIRST, THEN THE PACKET. `proposal.md` went
      `Status: draft` → `Status: ratified` plus one `Ratified:` line BEFORE
      `openspec archive` ran, so the archived copy carries it. § 7.3 is the
      reason and § 7.1 is the record the citation resolves to.
- [x] 8.3 PROMOTION PROVED BY DIGEST, PER REQUIREMENT.
      `openspec/specs/document-lifecycle/spec.md`: **17 → 17 requirements**,
      **77 → 79 scenarios**, 762 → 777 lines, `git diff --stat` **+18 / −3**.
      Every `### Requirement:` block hashed either side and the sets compared:
      **0 removed, 0 added, exactly 1 changed bytes** — `Controlled document
      status taxonomy`, the only title this packet's MODIFIED block names — and
      **16 of 17 byte-identical**. Canon's replaced block was 5912 bytes / 57
      lines / 8 scenarios under
      `sha256:65dc437f12c73b48b4add97df28297313ebdbff2eba74cd2f9de8aace19b81de`;
      the promoted block is 7882 bytes / 72 lines / 10 scenarios under
      `sha256:04537b7fdb210a74a35038e35cba85e02bccc21bdac68e19efb80d1a926c4e53`
      — **byte-identical to the delta body** in this archived folder. The two
      added scenarios are the split the packet argued for: `A generated artifact
      is captured once` and `A generated artifact is re-derived in place`, plus
      `A generator emits the status it declares`, in place of the single
      `A generated artifact is stored`. The rename half is DECLARED in the
      promoted text by the `Merged into` marker, which is why the
      scenario-title arm read zero throughout.
- [x] 8.4 THE ARCHIVED DELTA IS THE AUTHORED DELTA. `diff` between
      `HEAD:openspec/changes/declare-generated-projection-status/specs/document-lifecycle/spec.md`
      and the archived `specs/document-lifecycle/spec.md` is EMPTY.
      `.openspec.yaml` MOVED rather than being deleted, checked by blob id:
      `6e750e851a2dbf89ebcab921e230f7242a2aa80f`, unchanged.
- [x] 8.5 THE SELF-GATE ROW RETIRED ON ITS OWN STATED CONDITION. The row
      `('declare-generated-projection-status', 'document-lifecycle', 'Controlled
      document status taxonomy')` named its retirement as "when the packet
      archives and its block is promoted"; both halves verified before deletion,
      § 8.3 being the promotion proof. Removed in the same commit as the sibling
      packet's row: **carriage-ledger population 9 → 7, no other subject moving.**
- [x] 8.6 THE FLOOR MOVED BY EXACTLY TWO INFO AND IN NO OTHER LINE, ACROSS BOTH
      ARCHIVES TOGETHER: **4 critical / 7 error / 41 warning / 13 info → 4
      critical / 7 error / 41 warning / 11 info**, the finding lists diffed line
      by line. The per-stage census is unmoved by the archive act itself —
      `projection | 1`, `record | 29` before and after — because this packet's
      corpus effect landed at the realization, not here.
- [x] 8.7 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` **78 → 77
      passed, 0 failed** across this packet's archive. `pytest tests/doc-health`
      counts are in the pull request body, exit code read from `$?`.
- [x] 8.8 **§ 5.1's CONDITION IS MET, AND THE CORRECTION IS RECORDED RATHER
      THAN QUIETLY SWEPT.** This box was first written to say the
      aggregation-root disposition entry did not exist. It did — it landed
      2026-08-28 at aggregation commit
      `20aafc4b0ad9befbd6309363d6a52a8107403600`, keyed `(record-immutability,
      openxFactory, ideation/cross-reference.md)` and citing this change. The
      first reading took the shared checkout's WORKING file, thirteen or more
      commits behind that repository's `origin/main`; re-read against
      `origin/main` the entry stands at `health/dispositions.yaml:239-249`. The
      lesson is worth more than the retraction: in a checkout several sessions
      share, a working file is not evidence of what the repository holds —
      `git show origin/main:<path>` is. Nothing about the archive changes; the
      gate that looked unmet was met before the act began.

