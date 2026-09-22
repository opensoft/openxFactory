# Tasks: add-worker-input-budget

**House rule: OpenSpec ratifies, Speckit builds.** Group 1 is the authoring
done BY this change. Group 0 is the ratification gate and is the only task a
human must perform. Group 2 is the `code_surface: openxFactory` build and
Group 3 is the aggregation's child-side enforcement, which is a DIFFERENT
repository and therefore a different pull request. No merge is performed by
this change.

## Group 0 — RATIFICATION GATE (human; blocks nothing already built, gates landing)

- [ ] 0.1 Rule **OQ-1**, the grounding share: half the budget reserved for
  promoted specs (as built), or another split. At the 2026-09-21 corpus the
  built default sends 93 of 311 documents and defers 218, 71 of them
  promoted specs.
- [ ] 0.2 Confirm **OQ-2**: this packet caps and records; it does NOT carry
  deferred documents over to the next night, because no sweep cursor exists
  and the committed inventory baseline advances unconditionally. A real
  carry-over is a separate packet.
- [ ] 0.3 Note **OQ-3**: the live HTTP 403 org-entitlement block (since
  2026-09-16) is not addressed by any code here and needs an administrative
  act.
- [ ] 0.4 Ratify or amend the two spec deltas.

## Group 1 — authoring (done by this change)

- [x] 1.1 `proposal.md` with the measured evidence table, the budget
  arithmetic, and the normative-versus-detail finding.
- [x] 1.2 `specs/doc-health/spec.md` — one MODIFIED requirement (one added
  scenario) and one ADDED requirement (five scenarios).
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

- [ ] 4.1 Land both pull requests on Brett Heap's word.
- [ ] 4.2 Pin-sync the aggregation's `openxFactory` gitlink so the nightly
  runs the budgeted packer (`prepare` runs `python3
  openxFactory/scripts/doc-health.py` FROM the gitlink).
- [ ] 4.3 Confirm on the first green nightly: `meta.json` carries
  `input_budget_bytes`, the child does not refuse, and the report's sweep
  section states the input line.
