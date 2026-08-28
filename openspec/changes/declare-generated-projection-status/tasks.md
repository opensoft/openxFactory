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

- [ ] 5.1 **THE DISPOSITION ENTRY AT THE AGGREGATION ROOT.**
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
- [ ] 5.2 Merge-plus-green on main: both required checks green on the
      proposing pull request, read back from the check-runs API rather than
      off the pull request page.
- [ ] 5.3 Re-measure `record-immutability` on the merged tree and confirm it
      reads **4 critical**, with the four remaining being the genuine
      hand-maintained records and `ideation/cross-reference.md` absent.

## 6. Named follow-ups, out of scope here

- [ ] 6.1 **A projection's generator and source are declared in PROSE and
      nothing checks it** (Q1). Recommendation: leave it until a second
      projection exists — the rule-of-three has not fired, and a
      `Generated-by:` header would be a second new vocabulary item plus a new
      check for a class of one.
- [ ] 6.2 **Nothing stops a projection being re-classed to `record` to silence
      a real hand edit** (Q2) — the mirror image of the defect fixed here.
      Recommendation: the honest check is not on the status but on whether the
      committed bytes match what the declared generator produces
      (`--check`-mode regeneration in CI). That subsumes the question and
      deserves its own change rather than a guard bolted onto a family whose
      scope this packet deliberately did not touch.
- [ ] 6.3 **The four remaining `record-immutability` criticals are untouched**
      and are a different problem: genuine `Status: record` documents that are
      nonetheless hand-amended under the archive register's append discipline.
      That collision — a family whose remedy is "revert the content edit"
      against a discipline that appends — was named by
      `govern-openspec-corpus-membership` design.md Decision 3 and is still
      open.

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
- [ ] 7.3 **BEFORE ARCHIVE, THIS PROPOSAL'S OWN HEADER MUST MOVE OFF
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
