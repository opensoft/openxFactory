# Tasks: adopt-neutral-tooling-home

## 1. Tranche A — doc-health spine + sync (openxFactory receives)

- [ ] 1.1 Copy from codexFactory@pinned-sha with provenance note (D1):
      `scripts/doc_health/` (EXCLUDING `readiness.py`,
      `readiness_dispatch.py` — D3), `scripts/doc-health.py`,
      `scripts/sync-notebooklm-books.py`, the doc_health prompt `.md`
      contracts, `tests/doc-health/`, `tests/notebooklm/`,
      `.github/workflows/doc-health-reusable.yml`.
- [ ] 1.2 Path hygiene in the moved code: `runner.py` `SYNC_SCRIPT`
      becomes the in-repo path; `corpus.py` repo discovery unchanged
      (already aggregation-rooted); imports stay package-relative.
- [ ] 1.3 Make the neutral citations truthful: the two
      `xfactory-document-catalog-snapshot.schema.yaml` references and
      `validate-document-catalog.py:527` now point at in-repo files;
      `ideation/cross-reference.yaml` producer note names the in-repo
      scorer; `examples/lifecycle-notebook-workspaces.yaml` `managed_by`
      ×3 becomes `openxFactory/scripts/sync-notebooklm-books.py`;
      `docs/doc-health.md` ownership prose (lines ~22/119) and
      `docs/lifecycle-notebook-projection.md` invocation paths ×8
      updated.
- [ ] 1.4 Amend the active `add-cross-factory-ideation-routing` ownership
      requirement in place (D5): selection, orchestration adapters,
      validation, and report integration move from codexFactory to
      openxFactory; note the amendment in that change's tasks.md.
- [ ] 1.5 Gates: moved doc-health + notebooklm test suites green under
      openxFactory pytest; a full doc-health run over the workspace from
      the new home produces a report byte-comparable (modulo timestamps
      and self-path families) to the last codexFactory-run report;
      `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`.

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
