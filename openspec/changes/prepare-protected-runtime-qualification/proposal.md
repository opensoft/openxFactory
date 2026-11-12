---
Status: draft
Authored: 2026-11-12
Kind: governance
code_surface: openXwallet (proposed opt-in runtime adapter); openXfactory (governance and generated corpus-ledger row at publication only; no factory product runtime)
target_release: implemented (future source candidate after owner commissioning and review; no bundle cut or activation)
---

## Why

Factory #1304 / adapter #48 accept an offline proof gate and synthetic reference
processes. Landed codeXfactory #581 prepares qualification but supplies no live
issuer client, independent supervisor or workload-bound custody deployment.
The next bounded prerequisite is a machine-only protected runtime composition.

## What Changes

- Propose a trusted issuer-fetch adapter feeding the existing RS256 snapshot verifier, with fixed endpoints, bounded refresh/freshness and no token-directed trust.
- Define a factory-owned operational projection for the trusted launch, authenticated challenge access, supervisor boundary, confined gate/custody identity and persistent replay state.
- Prepare one openXwallet implementation feature, `017-protected-runtime-qualification`; retain its sole executable task list there.
- Require offline conformance first and separately authorized live machine qualification with independent protection and cleanup readback.
- Preserve existing possession/observation semantics, neutral API ownership, offline gates and codeXfactory T002. No human approval, domain marker, consumer execution pin or provider setup is supplied.

## Capabilities

### New Capabilities

- `protected-workload-runtime-qualification`: trusted runtime composition and honest machine-only qualification over the source-accepted factory/workload binding.

### Modified Capabilities

None. The source-accepted `add-workload-factory-binding` profile is a frozen
baseline; this proposal adds deployment composition and does not amend its
signature, time, grant, observation or replay semantics.

## Impact

Canonical composition and proposed operational grammar stay in this factory
packet. Adapter code/tests and the sole Speckit list belong to openXwallet.
Neutral proof, registry and custody APIs stay with openWallet; possession
receipts stay with openMFA. The adapter owns no canonical contract. No socket,
keyholding runtime or deployment is added to openXfactory. The operational
projection is a proposed internal runtime input, not a published contract or
the domain's withheld executable dependency lock.

Brett commissioned preparation. New-profile acceptance and implementation
commissioning remain explicit owner gates. Disposable setup/dispatch, real
service/trust selection and independent human acceptance remain later acts.
Feedback remains deferred; neither historically blocked write is replayed.
