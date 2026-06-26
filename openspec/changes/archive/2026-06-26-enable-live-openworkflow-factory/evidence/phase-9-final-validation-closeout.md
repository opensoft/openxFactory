# Phase 9 Evidence: Final Validation And Closeout

Change: `enable-live-openworkflow-factory`
Phase: 9
Date: 2026-06-26
Decision: READY TO ARCHIVE

## Final Validation Commands

From `opensoft/openWorkflow`:

```bash
OPENSPEC_TELEMETRY=0 openspec validate enable-live-openworkflow-factory --strict
OPENSPEC_TELEMETRY=0 openspec validate --all --strict
python3 - <<'PY'
from pathlib import Path
import yaml
for root in ['contracts', 'examples', 'openspec']:
    for path in Path(root).rglob('*'):
        if path.suffix in {'.yaml', '.yml'}:
            yaml.safe_load(path.read_text(encoding='utf-8'))
print('OK YAML parse')
PY
git diff --check
```

From `opensoft/Omnigent-Install`:

```bash
python3 scripts/validate-openworkflow-contracts.py
./scripts/smoke-live-factory-six-workstream.sh
./scripts/smoke-no-committed-secrets.sh
```

## Results

```text
Change 'enable-live-openworkflow-factory' is valid
Totals: 6 passed, 0 failed (6 items)
OK YAML parse
openWorkflow contract compatibility OK: 229761c
OK live factory six-workstream smoke
OK no committed secrets smoke
```

## Evidence Coverage

| Slice | Evidence | Merge readiness |
|---|---|---|
| Phase 1 Proposal and governance | `phase-1-proposal-governance.md` | `merge-readiness-openworkflow-pr-19.md` |
| Phase 2 Contract pinning | `phase-2-contract-pinning.md` | `merge-readiness-openworkflow-pr-20.md` |
| Phase 3 Hermes runtime | `phase-3-hermes-runtime-control-plane.md` | `merge-readiness-openworkflow-pr-21.md` |
| Phase 4 Worker event bridge | `phase-4-omnigent-worker-event-bridge.md` | `merge-readiness-openworkflow-pr-22.md` |
| Phase 5 Spec Kit control | `phase-5-speckit-stage-control.md` | `merge-readiness-openworkflow-pr-23.md` |
| Phase 6 Project Alfa pilot | `phase-6-project-alfa-pilot.md` | `merge-readiness-openworkflow-pr-24.md` |
| Phase 7 PR admission / Merge Council | `phase-7-pr-admission-merge-council.md` | `merge-readiness-openworkflow-pr-25.md` |
| Phase 7b Merge Master routing | `phase-7b-merge-master-human-review-router.md` | `merge-readiness-openworkflow-pr-26.md` |
| Phase 8 Worker/auth/memory/ops | `phase-8-worker-auth-memory-operations.md` | `merge-readiness-openworkflow-pr-27.md` |

## Known Warnings

1. External live GitHub PR mutation remains operator-enabled; the controlled pilot proof uses dry-run/replay gates.
2. Live Claude/Codex auth probes remain explicit; set `RUN_AUTH_PROBES=1` during CloudPC onboarding.
3. Production Merge Master approval requires a dedicated GitHub App/bot identity and branch-protection configuration.

## Archive Decision

All implementation slices have merged into `opensoft/openWorkflow` main. The OpenSpec change is ready to archive.
