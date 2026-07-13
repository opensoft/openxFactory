# Pre-Review Validation Baseline

Status: record
Kind: report
Captured: 2026-07-10
Validated: 2026-07-10 after pre-review hardening
Proposed by: define-avatar-client-runtime

This record separates validation owned by this change from compatibility
observations in independently owned DomainxFactory repositories.

## Owned Review Gate

The following are blocking and must pass from this openxFactory worktree:

- strict validation of `define-avatar-client-runtime`;
- strict validation of all OpenSpec items;
- `scripts/validate-avatar-client.py` after task 2.8 creates it;
- `scripts/validate-avatar-first-ui.py`;
- `scripts/validate-installation-templates.py`;
- `scripts/validate-intake-templates.py`;
- `scripts/validate-memory-gateway.py` as a no-regression check;
- supporting-document manifest hash verification;
- acceptance-map count/name validation against the delta specs; and
- `git diff --check`.

Domain repository validators are compatibility observations. A regression
caused by this change is blocking; a recorded pre-existing failure remains
owned by that DomainxFactory and does not make openxFactory task 5.2
uncompletable.

## Local Baseline

At capture time:

- target strict OpenSpec validation: pass;
- all strict OpenSpec validation: 20 passed, 0 failed;
- avatar-first UI validator: pass;
- installation-template validator: pass;
- intake-template validator: pass;
- memory-gateway validator and runtime smoke: pass;
- DomainxFactory openxFactory pins: pass; and
- `git diff --check`: pass.

The post-edit refresh also verified all 12 registered supporting files, exact
acceptance parity at 25 requirements and 97 scenarios, and a valid F0 results
schema. Task 5.2 stays open until the not-yet-implemented avatar-client
validator also passes.
The live F0 remains `INCONCLUSIVE`: `OPENAI_API_KEY` was unset and no
repository `.env` existed, so no provider request was attempted.

## External Compatibility Observations

| Repository | Strict domain validator | Credential validator | Workflow validator |
| --- | --- | --- | --- |
| AdxFactory | 0 errors, 1 warning; strict fail because `memory_gateway` is absent | pass, 0 contracts | pass, 4 contracts and 6 owner-layer warnings |
| LedgerxFactory | 0 errors, 1 warning; strict fail because `memory_gateway` is absent | pass, 0 contracts | pass, 5 contracts and 6 owner-layer warnings |
| MedxFactory | 0 errors, 1 warning; strict fail because `memory_gateway` is absent | pass, 0 contracts | pass, 1 contract and 1 owner-layer warning |
| OpsxFactory | 3 errors and 9 warnings; strict fail | pass, 5 contracts and 3 policy files skipped | pass, 6 out-of-scope workflows skipped |
| codexFactory | pass, 0 errors and 0 warnings | pass, 0 contracts | pass, 7 contracts and 0 warnings |

OpsxFactory's captured errors are an unrecognized `per_subject` isolation
scope and two secret-scan findings in repository text. This change does not
edit those repositories or claim to resolve those findings.
The post-edit rerun matched every captured external result exactly; this change
introduced no observed DomainxFactory conformance regression.

## Regression Rule

Before review, rerun the same commands. The change fails compatibility only if
it introduces a new error/warning, invalidates a previously valid pin, or
causes a previously passing validator to fail. External baseline remediation
must occur in the owning DomainxFactory change.
