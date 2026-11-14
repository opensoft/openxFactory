---
Status: draft
Authored: 2026-11-14
Kind: governance
code_surface: openXwallet (portable reference authority, authenticated adapter and isolated rehearsal); openXfactory (governance and generated corpus-ledger row only; no product runtime)
target_release: implemented (source candidate; no release, provider setup or protected dispatch)
---

## Why

Accepted factory #1311 / adapter #60 define independent actual-run bootstrap but
provide no authority service. A portable reference implementation can qualify
durable one-run binding and a real authenticated path into the existing wallet
proof flow without choosing a deployment or claiming live GitHub authentication.

## What Changes

- Implement explicit reference-store initialization, durable atomic preauthorization
  binding, revocation and restart refusal for missing/replaced/corrupt state.
- Add a bounded loopback mTLS reference service and authenticated client with
  separate operator, signed-control-plane, admission-reader and denied-worker roles.
- Verify independently signed fixture control-plane observations before accepting
  assigned run identity; never treat reader/worker context as authoritative.
- Connect authority-approved full configuration/grant readback to unchanged
  bootstrap/admission, owning wallet proof and independent cleanup in isolation.
- Keep feature 017 as the sole implementation list. Actual provider authentication,
  administrative isolation, T013/T014/T015 and human/domain acceptance remain gated.

## Capabilities

### New Capabilities

- `portable-bootstrap-authority`: durable authenticated fixture-scope authority
  and an isolated owning-wallet integration over the accepted bootstrap boundary.

### Modified Capabilities

None. Existing runtime/dispatch profiles, signed wallet proof, grant semantics,
one-use reservations and neutral custody APIs retain their accepted meaning.

## Impact

Factory owns the internal reference composition/wire decision; openXwallet owns
implementation and tests. No neutral contract, executable consumer lock, pin bump,
keyholding factory runtime or real GitHub authority is introduced. Test fixtures
hold synthetic signing roots and private loopback credentials; these establish
fixture behavior, not independently administered deployment. Existing CLI
operational binding construction still refuses before outputs/OIDC.

Brett commissioned this bounded source candidate and isolated qualification.
Candidate ratification and all setup/dispatch remain separate. Feedback stays
deferred; neither historical blocked write is replayed.
