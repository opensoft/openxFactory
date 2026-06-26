# Phase 7b Evidence: Merge Master And Human Review Router

Change: `enable-live-openworkflow-factory`
Phase: 7b
Date: 2026-06-26
Decision: PASS FOR DRY-RUN GOVERNANCE ROUTING

## Scope Verified

This slice closes the remaining Merge Master item from the PR/merge runtime section:

- Merge Master risk policy exists and classifies low, medium, and high risk.
- Low-risk PRs are eligible for Merge Master approval in dry-run policy.
- Medium/high-risk PRs require human/team review routing.
- Merge Master may submit an approving review only when policy permits.
- Merge Master must never merge directly or bypass GitHub branch protection.
- Human review routing resolves Hermes groups through the Hermes API.

## Commands Run

From `opensoft/Omnigent-Install`:

```bash
./scripts/smoke-merge-master-docs.sh
./scripts/smoke-hermes-groups-api.sh
```

Results:

```text
OK merge master docs
merge master docs smoke passed
OK Hermes groups API smoke
```

## Policy Coverage

| Risk | Expected Merge Master action | Coverage |
|---|---|---|
| low | may approve in dry-run / explicit execution mode | merge-risk policy and low-risk example |
| medium | request human/team review | merge-risk policy |
| high | request human/team review or block if evidence is missing | high-risk human-review example and resolver smoke |
| unknown | block | Merge Master policy docs |

## Human Review Routing

Hermes exposes routing helpers for Merge Master and Human Review Router:

- `GET /api/hermes/resolve/groups-for-risk`
- `GET /api/hermes/resolve/review-route`

The groups API smoke verifies high-risk security/tenant-isolation paths resolve to `opensoft/hermes-security` and choose `request_human_review`.

## Acceptance Checks

| Requirement | Result | Evidence |
|---|---:|---|
| Low-risk PR produces approval decision in dry-run | PASS | low-risk Merge Master example and docs smoke |
| Medium/high-risk PR routes to human/team review | PASS | merge-risk policy and Hermes review-route API smoke |
| Missing evidence blocks approval | PASS | Merge Master docs and policy examples |
| Merge Master never merges directly | PASS | Merge Master job fixture disallows `may_merge` |
| GitHub branch protection remains final | PASS | Merge Master docs and policy state branch protection is final enforcement |
| No personal token as production identity | PASS | Merge Master docs require bot/app identity |

## Remaining Work

This proof covers dry-run routing and policy integration. Production enablement still requires a configured GitHub App/bot identity and repository branch-protection settings that recognize that identity as an eligible reviewer.
