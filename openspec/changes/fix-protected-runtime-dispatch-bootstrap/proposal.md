---
Status: draft
Authored: 2026-11-13
Kind: governance
code_surface: openXwallet (internal bootstrap and prepared workflow); openXfactory (governance and generated corpus-ledger row only; no factory runtime)
target_release: implemented (source candidate only; no release, setup or dispatch)
---

## Why

Accepted openXwallet #59 requires a full runtime config digest before dispatch,
but that config contains the run ID/attempt assigned by GitHub afterward. Exact
admission correctly refuses different run values. Resolve this circularity
without weakening runtime authorization or rewriting accepted history.

## What Changes

- Define a closed, domain-separated static selection commitment containing the
  full runtime config except launch run ID and attempt.
- Migrate manual/reusable inputs from `config_digest`/`operation_grant_ref` to
  `selection_digest`/`preauthorization_ref` at the same immutable source.
- Require independently authenticated current bootstrap readback binding the
  approved selection, source, repository, case and actual run/attempt to the
  final full config digest and operation grant before existing admission.
- Retain full runtime validation, independent approval, fresh protection and
  registered cleanup/lease checks before environment/OIDC work.
- Test only in isolation; provide no hosting client, credential, provider setup,
  dispatch, consumer pin or operational authorization.

## Capabilities

### New Capabilities

- `protected-workload-dispatch-bootstrap`: static dispatch selection followed
  by independently authenticated actual-run binding into existing admission.

### Modified Capabilities

None. This composes `prepare-protected-runtime-qualification` without changing
the original full runtime digest, signed claims, neutral APIs or proof semantics.

## Impact

Factory governance owns the composition/migration. openXwallet feature 017 owns
implementation and the sole executable task list. Existing origins and accepted
source history stay unchanged. This instruction commissions isolated candidate
implementation; paired source acceptance and all operational/human/domain gates
remain separate. Feedback stays deferred; neither blocked write is replayed.
