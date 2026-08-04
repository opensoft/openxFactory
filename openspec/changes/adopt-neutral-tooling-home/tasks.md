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

- [x] 2.1 Copy with provenance note: `scripts/ideation_dashboard/`,
      `web/`, `scripts/ideation-dashboard-nightly.py`,
      `ideation-readiness-nightly.py`, `derive-possibles-nightly.py`,
      `docs/ideation-dashboard-session-runbook.md`,
      `tests/ideation-dashboard/`.
      Evidence 2026-08-03: copied via `git archive` from codexFactory
      main@e4caa03bf48655b54bc96fc5450d9ad5bddf4886 (same pin as tranche
      A). `web/` lives INSIDE the package at
      `scripts/ideation_dashboard/web/` (38 files), so the full-package
      copy carries it. The two tranche-A riders (`__init__.py`,
      `boundary.py`) were overwritten byte-identically (sha256 verified
      before/after). 168 files, ~98.4k LOC total (package py 25.5k, web
      18.0k, tests 53.7k, nightlies+runbook 0.5k, D3 dispatch+test 0.8k).
      **D3 REFINEMENT (needs Brett's eyes — dated note appended to
      design.md D3):** `readiness_dispatch.py` is NOT CloudPC
      infrastructure — its docstring opens "Nightly ideation-readiness
      lane dispatch orchestration (openxFactory
      add-ideation-cross-reference-readiness)", it imports only
      `doc_health.corpus` + `doc_health.ideation_readiness` (+ lazy
      `report`), never `readiness.py`, and
      `ideation-readiness-nightly.py` wraps
      `doc_health.readiness_dispatch.main` — so it was adopted HERE with
      `tests/doc-health/test_readiness_dispatch.py` (29 tests) and the
      cross-lane register-carry test restored byte-identically in
      `test_derive_possibles_dispatch.py`. D3's aggregation-bound scope
      narrows to `readiness.py` only (rides tranche D with
      `test_readiness.py` and the `check-worker-readiness.py` CLI half of
      `test_security_boundaries.py`, which is CloudPC-side, not lane
      dispatch). Tranche A's two already-repointed
      `ideation-readiness-nightly` lines in `doc-health-reusable.yml` are
      now functional with no further edit.
      Cross-repo pins whose SUBJECTS stay in codexFactory were left
      behind with dated tombstones in the moved copies (originals remain
      in codexFactory until tranche C): the three `docs/check-matrix.md`
      pins in `test_session_runbook.py` (one whole test + the matrix
      halves of two both-docs tests), the `scripts/validate-docs.sh`
      source pin in `test_hermeticity.py`, the
      `specs/007-workbench-branch-sessions/playwright-smoke.py` oracle
      pin in `test_smoke_signals.py` (NOTE for tranche C: that smoke
      imports `smoke_signals` from this now-moved suite), the
      `execution_lane.result` half of one `test_session_commits.py` test
      (D6 keeps that lane in codexFactory), the session-ports.md half of
      one `test_session_notebook.py` test, and
      `test_doxbench_contracts.py`'s committed-stack-pin test — **OPEN
      ITEM for Brett/tranche D:** `doxbench_contracts.verify_stack_pin`
      requires the HOSTING repo's `stack.yaml` consumption pin;
      openxFactory is the publisher and has none, so from a publisher
      checkout serve's two doxbench model routes fail CLOSED
      (fail-closed refusal, server otherwise unaffected) until a ruled
      publisher-side declaration lands. Receiving-repo reconciliation:
      the FR-043 guard was registered in `tests/avatar_runtime/conftest.py`
      and `tests/hermeticity.py` `CONFTEST_HOOKUPS` extended, with the two
      `tests/hermes_runtime_contracts/` conftests DECLARED exempt
      (`CONFTEST_EXEMPT_HOOKUPS`) — their bytes are digest-indexed
      PostgreSQL conformance inputs (editing them tripped
      HGR-FIXTURE-DATABASE-RESULT-SOURCE and snapshot collection;
      measured, then reverted); they stay guarded via `tests/conftest.py`.
      `validate-ideation-dashboard-contracts.py` `check_repo_tree` now
      also skips `tests/` (the moved suite's deliberately-INVALID
      negative fixtures are not "real instances"; same class as its
      `examples/` exclusion).
- [x] 2.2 Keep `kickoff.py` `DEFAULT_WORKFLOW` as the documented
      domain-supplied default (D4); no behavior change anywhere — this
      tranche is relocation only.
      Evidence 2026-08-03: `kickoff.py` is byte-identical to the pin
      (all four of its codexFactory mentions kept, incl. the
      `DEFAULT_WORKFLOW` comment and the line-172 outline literal).
      Full-tree byte diff vs the pin: exactly 14 files differ, all
      deliberate; `serve.py`, `web/` (all 38), `boundary.py`,
      `readiness_dispatch.py`, `test_readiness_dispatch.py`, and the
      restored `test_derive_possibles_dispatch.py` are byte-identical.
      Path hygiene (tranche-A 1.2 classification style) — fixed as
      moved-entrypoint/repo-shape: `test_nightly_lane.py:443` asserted
      workflow command → `openxFactory/scripts/…` (matches the
      tranche-A-repointed `doc-health-reusable.yml` line 2143);
      `test_aggregation_register_instance.py` `AGG_ROOT` becomes
      `REPO_ROOT.parent` (openxFactory sits directly under the
      aggregation root). Fixed as ownership prose:
      `ideation_dashboard/__init__.py` (in-repo realization + adoption
      note), `nightly_lane.py` line 5 (the reusable workflow is now
      in-repo), `workbench.py` ×3 ("in-repo doc-health machinery"),
      `generator.py`/dashboard `conftest.py` ("fixture base-repo lives
      inside the openxFactory git repo"). Left as legitimate:
      `kickoff.py` ×4 (D4), `session_pr.py` D22 App-ruling history,
      `branch_session.py` Speckit worktree-root citation,
      `test_doxbench_routes.py` PR #63 citation, and every test-fixture
      workspace naming codexFactory as a pinned factory
      (`test_branch_session.py`, `test_session_harness.py`,
      `test_gate_console.py`, `test_authoring_agent.py`
      `repository_context` values, `test_repo_root_guard.py` example
      prose, the real seed-register row in
      `test_aggregation_register_instance.py`). Session runbook: only
      self-referential/context edits — `Repository context:` header now
      `openxFactory` (the runtime's home; the serve commands it documents
      are repo-root-relative and stay correct verbatim), and its four
      codexFactory-resident citations (`specs/007…` ×2,
      `docs/check-matrix.md`, `docs/pr-admission-merge-readiness.md`)
      are qualified as codexFactory's; no other content rewritten.
- [x] 2.3 Gates: dashboard test suite green in openxFactory; a snapshot
      generation run over the workspace matches the prior codexFactory
      output for the same corpus revision; serve smoke (`serve.py`
      starts, renders the funnel against the packaged snapshot);
      existing `tests/ideation_dashboard/` contract suites still green.
      Evidence 2026-08-03: `python3 -m pytest tests/ideation-dashboard
      -q` → 2522 passed, 23 skipped (all environment-conditional:
      4 doxbench released-checkout probes want `OPENXFACTORY_ROOT`,
      4 aggregation-scope register tests skip in this worktree — the
      worktree's parent is not the aggregation root — and the balance
      are the suite's own pre-existing conditional skips; identical skip
      count on the first post-copy run). `tests/doc-health
      tests/notebooklm` → 610 passed, 0 skipped: tranche A's 551, plus
      the 3 `find_spec` probes activating (the two module-level skips
      expand to 6 + 38 collected tests, the hermeticity-guard layer-2
      probe passes), plus `test_readiness_dispatch.py`'s 13 and the 1
      restored cross-lane test — 551 + 45 + 14 = 610. Pre-existing
      suites unaffected:
      `tests/ideation_dashboard` 45,
      document_catalog+ideation_routing+avatar_client_validator 146
      (191 in one run), avatar_runtime 97,
      hermes `test_validator_cli.py` 21 (green only after the exemption
      rework above). Snapshot: `cli.py generate --repo-root <this
      checkout> --repository openxFactory` (read-only, scratchpad
      output; with `--project-register` pointed at the aggregation
      register) → validation 0 errors/0 warnings; vs the committed
      `health/ideation-dashboard/openxFactory-snapshot.json` the SHAPE is
      identical (same top-level keys incl. `project: xfactory`, same
      document entry fields, same generator_version 0.1.0); deltas are
      corpus drift only (source_revision ede1656e→385dfaff: changes
      67 vs 65, clusters/keywords 265 vs 270, staged_topics 20 vs 21,
      documents 240 both). Serve smoke: `serve.py --snapshot <generated>
      --checkout-root <this checkout> --port 8763` → GET /index.html and
      GET / both HTTP 200, 5473-byte dashboard page, process killed
      clean. `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` →
      54 passed, 0 failed.

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
