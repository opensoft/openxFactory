# Phase 7 Evidence: PR Admission And Merge Council Runtime

Change: `enable-live-openworkflow-factory`
Phase: 7
Date: 2026-06-26
Decision: PASS FOR PR ADMISSION AND MERGE COUNCIL

## Scope Verified

Phase 7 verified that the PR admission and Merge Council paths are enforceable and repeatable in the local runtime proof.

The Merge Master dry-run and human-review routing item is intentionally left for Phase 8 because it is a Hermes governance-agent behavior, not the admission/council substrate.

## Commands Run

From `opensoft/Omnigent-Install`:

```bash
./scripts/smoke-pr-admission.sh
./scripts/smoke-merge-council.sh
./scripts/smoke-non-doc-pr-admission.sh
./scripts/smoke-non-doc-merge-council.sh
```

Results:

```text
OK PR admission smoke
OK merge council smoke
OK non-doc pilot contracts
OK non-doc stage-gate contracts
OK non-doc PR admission contracts
OK non-doc PR admission evaluator self-test
OK non-doc PR admission smoke
OK non-doc merge council contracts
OK non-doc merge council smoke
```

## PR Admission Blocking Rules

The runtime path blocks PR admission when required evidence is missing or invalid:

- approved scope missing
- Spec Kit artifacts missing
- deterministic checks missing or failed without waiver
- branch review has blocking findings
- changed-line policy exceeded
- traceability incomplete
- Omnigent attempts PR opening before Hermes PR admission approval

## Merge Council Lanes

The Merge Council runtime path covers the required lanes:

- Spec Traceability
- Security
- Tests
- Architecture
- Maintainability
- Integration

## Decision Coverage

| Decision / gate | Coverage |
|---|---|
| PR admission ready | `smoke-pr-admission.sh`, `smoke-non-doc-pr-admission.sh` |
| PR admission blocked | non-doc evaluator self-test |
| PR open only after approval | live factory replay and PR admission smoke |
| Merge readiness ready | `smoke-merge-council.sh`, `smoke-non-doc-merge-council.sh` |
| Merge readiness blocked | blocked merge council fixture in merge council smoke |
| GitHub branch protection remains final | Merge Council fixtures record GitHub enforcement as final merge authority |

## Acceptance Checks

| Requirement | Result | Evidence |
|---|---:|---|
| Failing branch review prevents PR admission | PASS | non-doc PR admission evaluator self-test |
| Missing acceptance criterion prevents merge readiness | PASS | merge council blocked fixture |
| Passing low-risk doc/tooling PR reaches merge readiness | PASS | PR admission and Merge Council smokes |
| Merge Council report exists before merge approval record | PASS | merge council smoke artifact ordering |
| Traceability links branch evidence, PR admission, and merge readiness | PASS | PR admission and Merge Council traceability assertions |

## Remaining Work

Phase 8 verifies Merge Master dry-run decisions, medium/high-risk human-review routing, and the rule that Merge Master may submit review decisions but must never merge directly or bypass branch protection.
