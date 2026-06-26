# Content Cleanup Decision

Decision: keep migrated install repo policy, schema, and example copies for now
as marked implementation, compatibility, or operational copies.

Do not delete install repo copies in the current migration. The copy-first
migration has moved canonical meaning into `openWorkflow`, but install repos
still use local copies for validators, smoke tests, runtime wiring, examples,
and operational documentation.

## Source Provenance

Reviewed sources:

- `docs/dogfood-content-migration-plan.md`
- `docs/repo-boundary-audit.md`
- `contracts/README.md`
- `examples/README.md`
- `openspec/changes/migrate-canonical-policy-to-openworkflow/evidence/feat-mig-007-install-repo-markers.md`
- `opensoft/Omnigent-Install#2`
- `FarHeap/Hermes-Install#2`

## Decision

```yaml
cleanup_decision:
  policy_copies: keep_marked
  schema_copies: keep_as_compatibility_copies
  example_copies: keep_install_proofs_in_install_repo
  runtime_files: do_not_move_or_delete
  generated_adapters: do_not_move_or_delete
  future_removals: separate_approved_prs_only
```

## Rationale

- `openWorkflow` now owns canonical policy, contracts, and static reference
  examples.
- Install repos still need local copies for compatibility, smoke tests,
  validators, and runtime adapters.
- Removing copies before adapters are updated would create avoidable breakage.
- Keeping marked copies lets engineers understand which files are canonical and
  which files are install-specific.
- The next real cleanup should be driven by validation, not by repo tidiness.

## Future Cleanup Rules

A future cleanup PR may remove or archive a marked install copy only when all of
these are true:

1. The canonical `openWorkflow` replacement exists.
2. The install repo has an adapter, validator, or reference path that consumes
   the canonical replacement or a pinned compatible copy.
3. Smoke tests prove the install still works without the old copy.
4. The PR removes only the approved copy and does not mix runtime code movement,
   generated adapter updates, submodule pointer changes, or unrelated docs.
5. Hermes approval records the cleanup scope.

## What Must Not Be Removed By Policy Cleanup

- runtime manifests;
- service code;
- generated clients or adapters;
- smoke-test harnesses;
- live pilot scripts;
- credentials or auth profiles;
- databases;
- logs;
- local workspaces;
- install backup/restore procedures.

## Rollback Path

If a cleanup PR breaks an install repo:

1. Revert the cleanup PR in the affected install repo.
2. Restore the previous `openWorkflow` submodule pin if a pin was changed.
3. Re-run the install repo smoke/validation checks.
4. Record the failure in OpenSpec evidence.
5. Split adapter work from copy removal before trying again.

## Current State

| Area | Current Action |
|---|---|
| `Omnigent-Install` policy docs | Keep as marked implementation copies |
| `Omnigent-Install/schemas` | Keep as marked compatibility copies |
| `Omnigent-Install/policies` | Keep as marked compatibility copies |
| `Omnigent-Install/examples` | Keep executable proof and install-specific examples |
| `Hermes-Install/README.md` | Keep as operational install/runbook reference |
| `openWorkflow/contracts` | Canonical shared contract home |
| `openWorkflow/examples` | Canonical static reference example home |
| `openWorkflow/docs` | Canonical factory policy home |
