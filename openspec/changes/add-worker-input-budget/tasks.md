# Tasks: add-worker-input-budget

**House rule: OpenSpec ratifies, Speckit builds.** Group 1 is the authoring
done BY this change. Group 0 is the ratification gate and is the only task a
human must perform. Group 2 is the `code_surface: openxFactory` build and
Group 3 is the aggregation's child-side enforcement, which is a DIFFERENT
repository and therefore a different pull request. No merge is performed by
this change.

## Group 0 — RATIFICATION GATE (human; blocks nothing already built, gates landing)

- [x] 0.1 Rule **OQ-1**, the grounding share: half the budget reserved for
  promoted specs (as built), or another split. At the 2026-09-21 corpus the
  built default sends 93 of 311 documents and defers 218, 71 of them
  promoted specs; measured at shares 0.3 to 0.7 on the 2026-09-24 inventory.
  **RESOLVED 2026-09-26: 0.5, as built** — Brett Heap's ruling in session to
  lane `openxfactory-1`, option verbatim *"Accept both, land #1160"*,
  recorded on opensoft/xFactory#480 comment 5850005209 (item 3, answering
  the RULING NEEDED, comment 5820150177); the lane recommendation to keep 0.5
  is accepted as it stood, and no code changes (`GROUNDING_BUDGET_SHARE` is
  already `0.5`). Evidence in full: `proposal.md` OQ-1.
- [x] 0.2 Confirm **OQ-2**: this packet caps and records; it does NOT carry
  deferred documents over to the next night, because no sweep cursor exists
  and the inventory baseline is emitted unconditionally. A real carry-over is
  a separate packet. Measured 2026-09-24 (the committed baseline has held at
  2026-09-04, no nightly report having landed since). **RESOLVED 2026-09-26:
  confirmed, with the carry-over staged as its own packet** — the same
  ruling and record as 0.1, which took the RULING NEEDED's option (a); the
  topic is `ideation/staging/doc-health-sweep-carry-over/`, created by this
  revision, with the cursor as its own committed record beside the inventory.
  The ruling does not wait on the baseline: opensoft/xFactory#396, ruled the
  same day to land with the nightly's content winning, unsticks it without
  making a deferred document swept. Evidence in full: `proposal.md` OQ-2.
- [x] 0.3 Note **OQ-3**: the HTTP 403 org-entitlement block (filed as live
  since 2026-09-16) is not addressed by any code here and needed an
  administrative act. **RESOLVED 2026-09-23** by that act — Brett Heap's
  Console-side remedy, opensoft/xFactory#491 option 1 — verified by the
  re-dispatched analysis child, opensoft/xFactory run 35889825278 (the
  1,899,789-byte prompt accepted, 4 findings), and by the 2026-09-24 nightly,
  run 35947804907, whose four model children all succeeded with model
  output. Evidence in full: `proposal.md` OQ-3.
- [ ] 0.4 Ratify or amend the two spec deltas.

## Group 1 — authoring (done by this change)

- [x] 1.1 `proposal.md` with the measured evidence table, the budget
  arithmetic, and the normative-versus-detail finding.
- [x] 1.2 `specs/doc-health/spec.md` — one MODIFIED requirement (one added
  scenarios) and one ADDED requirement (six scenarios).
- [x] 1.3 `tasks.md` (this file).
- [x] 1.4 README "OpenSpec Records" entry.

## Group 2 — openxFactory realization (built with this packet, PR `fix/semantic-sweep-input-budget`)

- [x] 2.1 `scripts/doc_health/semantic.py`: `DEFAULT_INPUT_BUDGET_BYTES`,
  `GROUNDING_BUDGET_SHARE`, `render_analysis_input`, `document_cost`,
  `pack_within_budget`, `corpus_documents`,
  `build_analysis_input_with_stats`, `analysis_input_with_stats`, and the
  budget fields on `SweepMeta`.
- [x] 2.2 `prepare_bundle` and `run_sweep` take `input_budget_bytes`; the
  bundle's `meta.json` carries the budget record.
- [x] 2.3 `scripts/doc_health/runner.py`: `--semantic-input-budget-bytes`.
- [x] 2.4 `scripts/doc_health/report.py`: the input line and one line per
  deferred document.
- [x] 2.5 `scripts/doc_health/catalog_dispatch.py`: `shard_analysis_input`
  and the catalog bundle's own `meta.json` (budget plus measured per-shard
  assembled bytes).
- [x] 2.6 `tests/doc-health/test_semantic_input_budget.py`.

## Group 3 — aggregation realization (`opensoft/xFactory`, PR `fix/worker-input-size-guard`)

- [x] 3.1 `doc-health-analysis-worker.yml` and
  `doc-health-cataloger-worker.yml`: read `input_budget_bytes` from the
  bundle, refuse over-budget input before invoking the model, write
  `skip-reason.json`, exit non-zero.
- [x] 3.2 The same two steps capture stderr and print the head of
  `worker-result.json` on failure, before the cleanup step removes the
  workspace.
- [x] 3.3 `tests/test_doc_health_worker_input_guard.py`.

## Group 4 — after ratification

**Sequencing tension, named rather than hidden** (raised by Codex's and
Copilot's review of the PR that ticked 4.1-4.3): this Group's own heading
reads "after ratification," and Group 0 above states it "gates landing" —
yet 4.1 measurably happened on 2026-09-22, while 0.4 (ratifying the two
spec deltas that make this behavior NORMATIVE rather than merely an
implementation fix) is still open even as this line is written. The
landing was not ungated: it ran under a separate, explicit operational
word, Brett Heap's *"land the input-size guard when green"* — the same
word 4.1 cites below, governing issue `opensoft/xFactory#479` — given the
same day the proposal itself was opened, because the nightly's analysis
child had been silently failing every night since 2026-08-30 and the
fix's urgency was judged ahead of waiting on the spec-text ratification.
Whether that operational word is the "approved exception" this house rule
contemplates, or whether 0.4 should have gated 4.1 regardless, is put to
Brett Heap as a RULING (see the PR report); this note records the tension
rather than resolving it by silent omission.

- [x] 4.1 Land both pull requests on Brett Heap's word. **DONE 2026-09-22.**
  `opensoft/openxFactory#1137` ("Bound the bounded workers' input to the
  model's context window", branch `fix/semantic-sweep-input-budget`) merged
  2026-09-22T03:45:21Z at `9da52e318aa7662efa57b750bef3dc1992ff6332`.
  `opensoft/xFactory#481` ("Make the doc-health workers refuse an
  over-budget input, and say why", branch `fix/worker-input-size-guard`)
  merged 2026-09-22T03:45:36Z at `b2479b6e4d9a6bccb8cdf5e2b39417257dc3f5c5`
  — fifteen seconds later. Both landed under the same word: Brett Heap's
  *"land the input-size guard when green"* (governing issue
  `opensoft/xFactory#479`), recorded as a FREEZE/LANDING/LANDED sequence on
  `opensoft/openxFactory#1137` (comments at 03:45:01Z / 03:45:15Z /
  03:45:26Z→merge `9da52e31`) and confirmed on `opensoft/xFactory#481`
  (comment at 03:45:32Z, *"the parent-side budget landed in
  opensoft/openxFactory#1137; the two-file pin-sync follows"*).
- [x] 4.2 Pin-sync the aggregation's `openxFactory` gitlink so the nightly
  runs the budgeted packer. **DONE, and continuously true since
  2026-09-22.** The gitlink first carried the packer via
  `opensoft/xFactory#483` ("Sync submodule pointer: openxFactory aaddda66
  -> 9da52e31, with the clearing PIN in the same commit"), merged
  2026-09-22T03:58:45Z — 13 minutes after `#1137` landed — moving the
  gitlink to `9da52e318aa7662efa57b750bef3dc1992ff6332`, `#1137`'s own merge
  commit. Measured: `git merge-base --is-ancestor 9da52e31 <gitlink>` holds
  for every nightly's gitlink since (`94b6f7f1` 09-24, `dd2466ad` 09-25/26,
  `1c6662e7` 09-27, `133e37d9` 09-28's own nightly) and for every pin-sync
  landed today past that — `opensoft/xFactory#543` ("Sync openxFactory pin
  133e37d9 -> 6b97c601", merged 2026-09-28T17:58:15Z) and
  `opensoft/xFactory#544` ("Sync openxFactory pin 6b97c601 -> e369cb25,
  T007 batch B record", merged 2026-09-28T22:33:16Z). The CURRENT gitlink,
  confirmed live via `gh api "repos/opensoft/xFactory/contents/openxFactory?ref=main"`
  at 2026-09-28T23:05:35Z, is `e369cb25cd9a4ea0c62469777bde003168191a37` —
  `#544`'s target, and a measured descendant of the packer's
  merge commit. `#543`/`#544` are routine lockstep pin-syncs for unrelated
  commits (finalize-job sealed-run containment, a T007 openspec record);
  neither was needed to first admit the packer, which the nightly has run
  under continuously since the night of 2026-09-23.
- [x] 4.3 Confirm on the first green nightly: `meta.json` carries
  `input_budget_bytes`, the child does not refuse, and the report's sweep
  section states the input line. **CONFIRMED, night of 2026-09-24**
  (`opensoft/xFactory` nightly run `35947804907`, conclusion `success`;
  analysis child `35948587830` success; cataloger child `35948591376`
  success — the first fully green night after the pin first carried the
  packer). Measured directly from the downloaded run artifacts:
  `semantic-sweep-bundle/meta.json` — `input_budget_bytes: 1900000`,
  `input_bytes: 1899236`, `docs_included: 96`, `docs_deferred: 227`,
  `truncated: true`. `document-catalog-bundle/meta.json` —
  `input_budget_bytes: 1900000`, a measured `shard_input_bytes` per shard
  (35 shards; largest `CATSHARD-0016-464b736481` at 918,035 bytes),
  `shards_over_budget: []` (none this night). Neither child's bundle
  carries a `skip-reason.json`; the analysis child's own job log states
  `input-size guard: analysis-input.txt is 1899236 bytes against a
  1900000-byte budget from meta.json` immediately before the model call
  that produced real findings — the guard ran and passed, it did not
  refuse. The committed report (`health/reports/2026-09-24.md`, blob
  `761fec1e6de9f8bc0903e9838a1b6b93a31390fd`, reached via commit
  `28f8d918f6` on the rolling report branch behind
  `opensoft/xFactory#396`/`#533`) states, under `## Semantic Sweep`:
  *"- input: 1899236 of 1900000 budgeted bytes, 96 docs sent, 227
  deferred"* — byte for byte the bundle's own `meta.json` record.
  **Residual, as of 2026-09-28 (not a defect in this packet):** the four
  nights since — 09-25, 09-26, 09-27, 09-28 — the analysis and cataloger
  children have both again failed, but measurably NOT on the input-size
  guard: 09-28's analysis child log shows the same guard line passing at
  1,899,526 of 1,900,000 bytes, immediately followed by the model call's
  own `"api_error_status":403, "result":"Your organization has disabled
  Claude subscription access for Claude Code..."` — OQ-3's HTTP 403
  recurring, not a budget refusal. No further nightly has run since
  today's `#543`/`#544` pin-syncs (next scheduled 2026-09-29T02:17Z, cron
  `17 2 * * *`).
