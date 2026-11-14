---
Status: draft
Authored: 2026-11-14
Kind: governance
code_surface: openXwallet (proposed internal bootstrap authentication, workflow integration and isolated tests); openXfactory (governance and generated corpus-ledger row only)
target_release: implemented (future source candidate after explicit profile acceptance and commissioning; no activation or bundle cut)
---

## Why

The source-accepted portable authority binds signed simulated context but cannot
authenticate an actual GitHub job. Landed adapter #63 identifies pre-environment
client identity and dispatch/run correlation as separate unresolved prerequisites.

## What Changes

- Propose a new opt-in internal GitHub bootstrap profile, with a purpose-specific GitHub-signed OIDC identity for readiness only and independent dispatch-journal/API corroboration.
- Explicitly propose an amendment to the earlier no-preflight-OIDC expectation: a future admitted workflow may request a bootstrap-only token before environment approval. The existing default/reference profile remains unchanged; this decision requires owner acceptance before implementation or workflow edits.
- Keep protected proof identity, environment approval, actual run authority, signer access and human/domain approval separate. Bootstrap identity cannot approve a static selection, dispatch, provision, sign or satisfy the proof verifier.
- Require durable consumption of one dispatch attempt before external I/O, provider-returned run correlation, no automatic retry after ambiguity, and fail-closed source/ref/attempt checks.
- Specify source-only implementation and isolated acceptance criteria in the existing adapter feature 017 task list. This packet commissions no code, token request, App, credential, environment, provider permission, setup or dispatch.

## Capabilities

### New Capabilities

- `github-bootstrap-authentication`: authenticated GitHub readiness clients bound to independently approved dispatch context, with explicit separation from protected machine proof authority.

### Modified Capabilities

None under canonical `openspec/specs/`. This is a proposed versioned internal
extension to the source-accepted `fix-protected-runtime-dispatch-bootstrap` and
`add-portable-bootstrap-authority` decisions. Their frozen source/fixture profiles
are not edited or relabeled. The new profile's admission-OIDC amendment is explicit
in the design and needs its own source acceptance; existing neutral proof,
registry/custody APIs and the seven runtime service roles do not change.

## Impact

Factory owns this composition and proposed grammar. openXwallet owns future code,
workflow edits and its sole executable feature 017 tasks. Existing same-commit
caller/local reusable and three dispatch inputs remain. No consumer dependency
lock, neutral contract/pin, release or production activation is supplied.

This proposal recommends bootstrap-only OIDC instead of a stored pre-environment
client secret or a new self-hosted-runner trust plane. Strict no-preflight-OIDC
remains an alternative but requires a separately selected independent client
identity/control-plane design; it cannot inherit the new profile silently.
Source/target decisions and the mutable-main residual-exposure policy remain
explicit owner gates. Feedback stays deferred; neither historical blocked write
is replayed.
