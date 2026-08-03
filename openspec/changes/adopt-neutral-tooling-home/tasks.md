# Tasks: adopt-neutral-tooling-home

## 1. Tranche A — doc-health spine + sync (openxFactory receives)

- [x] 1.1 Copy from codexFactory@pinned-sha with provenance note (D1):
      `scripts/doc_health/` (EXCLUDING `readiness.py`,
      `readiness_dispatch.py` — D3), `scripts/doc-health.py`,
      `scripts/sync-notebooklm-books.py`, the doc_health prompt `.md`
      contracts, `tests/doc-health/`, `tests/notebooklm/`,
      `.github/workflows/doc-health-reusable.yml`.
      Evidence 2026-08-03: copied via `git archive` from codexFactory
      main@e4caa03bf48655b54bc96fc5450d9ad5bddf4886; also brought the
      suites' pytest infrastructure (`pytest.ini` rootdir anchor,
      `tests/conftest.py`, `tests/hermeticity.py`,
      `tests/hermetic_unittest.py`) and — as a scoped rider —
      `scripts/ideation_dashboard/__init__.py` + `boundary.py`
      (byte-identical to source; `ideation_readiness.persist` and
      `derive_possibles.persist` import `OutputBoundary` at runtime, so
      the tranche-B tree's write-boundary module had to ride tranche A).
      With the D3 modules, their suites left too:
      `tests/doc-health/test_readiness.py`, `test_readiness_dispatch.py`,
      the readiness-CLI half of `test_security_boundaries.py`, and one
      cross-lane integration test in `test_derive_possibles_dispatch.py`
      (`test_readiness_merge_carries_the_possibles_register_through`) —
      all ride tranche D with the modules they exercise.
      `test_readiness_report.py` stays (it tests the in-repo `report.py`).
      Note for tranche B/D: `readiness_dispatch.py` is the
      ideation-readiness LANE dispatch (its own docstring), so
      `ideation-readiness-nightly.py` (task 2.1) will need it reachable
      from wherever tranche D homes it.
- [x] 1.2 Path hygiene in the moved code: `runner.py` `SYNC_SCRIPT`
      becomes the in-repo path; `corpus.py` repo discovery unchanged
      (already aggregation-rooted); imports stay package-relative.
      Evidence 2026-08-03: `SYNC_SCRIPT =
      "openxFactory/scripts/sync-notebooklm-books.py"` (joined against
      the workspace root, verified at `_real_notebook_dryrun`). Full-tree
      `codexFactory` grep classified: fixed 9 moved-entrypoint paths in
      `doc-health-reusable.yml` (doc-health.py ×4,
      ideation-readiness-nightly ×2, derive-possibles-nightly ×2,
      ideation-dashboard-nightly ×1 → `openxFactory/scripts/…`); fixed
      ownership prose in `doc_health/__init__.py`, `organizer.py`,
      `derive_possibles.py`, `ideation_readiness.py` (incl. the emitted
      `_YAML_HEADER` producer note) and the sync charter's "maintained
      by" line. Left as legitimate: `check-worker-readiness.py` workflow
      paths ×5 (stays codexFactory-hosted until tranche D revisits),
      `ideation-readiness-prompt.md`'s `project` tier (names the
      engineering factory as a domain concept; prompt contract text
      untouched), test-fixture workspaces naming codexFactory as a pinned
      factory, and the `specs/003-ideation-readiness/ (codexFactory)`
      contract-provenance citation. No cli/dispatch wiring imported the
      excluded readiness modules (`doc-health.py` → `runner.main` only;
      no subcommand removal needed). Tranche-A guards added where the
      tranche-B package is probed via `find_spec` (self-healing):
      `tests/hermeticity.py` `runner_seams`,
      `tests/notebooklm/test_hermeticity_guard.py` (layer-2 assert),
      `test_sync_notebooklm_books.py`, `test_workbench_sweep_wiring.py`.
- [x] 1.3 Make the neutral citations truthful: the two
      `xfactory-document-catalog-snapshot.schema.yaml` references and
      `validate-document-catalog.py:527` now point at in-repo files;
      `ideation/cross-reference.yaml` producer note names the in-repo
      scorer; `examples/lifecycle-notebook-workspaces.yaml` `managed_by`
      ×3 becomes `openxFactory/scripts/sync-notebooklm-books.py`;
      `docs/doc-health.md` ownership prose (lines ~22/119) and
      `docs/lifecycle-notebook-projection.md` invocation paths ×8
      updated.
      Evidence 2026-08-03: all done, plus same-class in-file citations at
      `validate-document-catalog.py` lines ~41/324/489/562 (present-tense
      "codexFactory owns/realizes" claims → in-repo wording) and the
      lifecycle doc's line-15 reference-implementation pointer. The
      cross-reference.yaml header edit mirrors the
      `ideation_readiness._YAML_HEADER` emitter so regeneration stays
      byte-consistent.
- [x] 1.4 Amend the active `add-cross-factory-ideation-routing` ownership
      requirement in place (D5): selection, orchestration adapters,
      validation, and report integration move from codexFactory to
      openxFactory; note the amendment in that change's tasks.md.
      Evidence 2026-08-03: "Organizer execution, persistence, and
      readiness isolation" first body line now reads "openxFactory SHALL
      own the organizer contract and schemas, and SHALL also own
      selection, orchestration adapters, validation, and report
      integration" (SHALL kept on line one for strict validation);
      xFactory keeps dispatch + durable reporting; dated Amendments note
      appended to that change's tasks.md citing provenance
      codexFactory main@e4caa03bf48655b54bc96fc5450d9ad5bddf4886.
- [x] 1.5 Gates: moved doc-health + notebooklm test suites green under
      openxFactory pytest; a full doc-health run over the workspace from
      the new home produces a report byte-comparable (modulo timestamps
      and self-path families) to the last codexFactory-run report;
      `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`.
      Evidence 2026-08-03: `python3 -m pytest tests/doc-health
      tests/notebooklm -q` → 551 passed, 3 skipped (all three are the
      tranche-B `ideation_dashboard` probes above, each skip names the
      tranche), and existing suites unaffected (`tests/ideation_dashboard`
      45 passed; document_catalog+ideation_routing+avatar_client_validator
      146 passed). `scripts/doc-health.py --help` and
      `scripts/sync-notebooklm-books.py --help` run from the new home
      (no `--apply` anywhere). Read-only per-family comparison against
      `health/reports/2026-08-02.md` over a CI-shaped symlink mirror of
      the workspace (preflight not run — it executes sibling checkouts'
      validators in their trees): 11/14 deterministic families match the
      nightly's counts exactly; the 3 diffs are corpus drift, not checker
      drift (document-catalog 526 vs 292: +68 stale-entry/+166 coverage
      from two days of repo movement past the persisted Aug-2 catalog
      state; submodule-pin-drift: local pins/credentials differ —
      codexFactory remote main now equals the adoption pin e4caa03b;
      contract-copy-drift 4 vs 5: codexFactory's openxFactory pin caught
      up to canonical HEAD). `OPENSPEC_TELEMETRY=0 openspec validate
      --all --strict` → 54 passed, 0 failed.

## 2. Tranche B — ideation dashboard runtime (openxFactory receives)

- [ ] 2.1 Copy with provenance note: `scripts/ideation_dashboard/`,
      `web/`, `scripts/ideation-dashboard-nightly.py`,
      `ideation-readiness-nightly.py`, `derive-possibles-nightly.py`,
      `docs/ideation-dashboard-session-runbook.md`,
      `tests/ideation-dashboard/`.
- [ ] 2.2 Keep `kickoff.py` `DEFAULT_WORKFLOW` as the documented
      domain-supplied default (D4); no behavior change anywhere — this
      tranche is relocation only.
- [ ] 2.3 Gates: dashboard test suite green in openxFactory; a snapshot
      generation run over the workspace matches the prior codexFactory
      output for the same corpus revision; serve smoke (`serve.py`
      starts, renders the funnel against the packaged snapshot);
      existing `tests/ideation_dashboard/` contract suites still green.

## 3. Tranche C — codexFactory sheds (own repo, after A+B are green)

- [ ] 3.1 Remove the moved trees; README rewrites its tooling sections to
      point at openxFactory; `validate-docs.sh` keeps only its
      codex-specific checks plus the three conformance-gate scripts
      (whose own neutralization is DTN follow-up, not this change).
- [ ] 3.2 Redirect stubs where sessions have muscle memory: a one-line
      `scripts/doc-health.py` and `scripts/sync-notebooklm-books.py`
      exec-shim OR a clear removal notice in README — pick one, never a
      silent 404.
- [ ] 3.3 codexFactory `stack.yaml`/inventory untouched (the moved trees
      were never inventoried — verified 2026-08-03).

## 4. Tranche D — aggregation repoints (own repo)

- [ ] 4.1 `.github/workflows/doc-health-nightly.yml` `uses:` moves to
      `opensoft/openxFactory/.github/workflows/doc-health-reusable.yml@main`;
      drop the App-token mint for codexFactory reads IF doc-health was
      its only reader (verify against merge-master/council callers
      first — D6 keeps those lanes in codexFactory).
- [ ] 4.2 Workspace `CLAUDE.md` sync command becomes
      `python3 openxFactory/scripts/sync-notebooklm-books.py . --apply`.
- [ ] 4.3 Adopt `readiness.py` + `readiness_dispatch.py` into the
      aggregation repo beside the nightly (D3).
- [ ] 4.4 Submodule pointer syncs for all three repos.

## 5. Close-out

- [ ] 5.1 README doc index + OpenSpec Records entry; session-runbook and
      dashboard docs linked from the openxFactory doc index.
- [ ] 5.2 Nightly evidence: one full doc-health nightly and one dashboard
      nightly complete green from the new homes.
- [ ] 5.3 Memory/handoff note for other live sessions (the dashboard
      serve path changes) — recorded in the aggregation repo's handoff
      convention if one is active.
