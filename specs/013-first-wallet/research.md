# Research: The First Wallet (013)

**Feature**: 013-first-wallet | **Grounded**: 2026-08-24

Every load-bearing fact below was verified against the tree at `origin/main`
(`d95623ea`) before authoring.

## Substrate facts

1. **§4 is the whole scope.** tasks.md:115–136 of
   `add-wallet-carried-review-authority`: 4.1 `[OPERATOR]` mint one wallet for
   `merge_readiness_council` as a body, custody `holder_readable`; 4.2 write
   the record IN THE SAME TREE as the register; 4.3 record the custody
   ATTESTATION row. 4.4 (composition) is `[codexFactory]`. No grant and no
   register anywhere in §4.
2. **Day-one order** (proposal.md:731–741): S1 → S2 → **the first wallet** →
   S4's MVP. "S3 and S5 follow; neither is reachable before a grant exists
   that a reader honours."
3. **Zero live instances today.** proposal.md:700–704: no `xfactory_wallet`
   record outside `contracts/openxwallet/examples/`; openxwallet is
   contract-only and has never been instantiated.
4. **The exception is declared, not accidental.** clarifications.md N7
   (:114–128): scan target must include the register path AND the wallets its
   rows reference; "a grant whose audience wallet lives in a different
   repository has no resolution path today"; the MVP's single holder must have
   its wallet record in the same tree.
5. **`holder_readable` reaches `act` deliberately** (clarifications N13,
   :212–227): registry designed for exactly the no-key-infrastructure case;
   approval-before-apply is the compensating control, already constitutional.
6. **Unattested custody caps at `request`** (proposal.md:330–333): "A custody
   model with no recorded attestation — who verified the isolation, against
   what, when — caps a review-authority grant at `request`, not `act`." Task
   4.3 exists to prevent that cap at cold start.
7. **Composition is NOT a minting precondition.** validate-openxwallet.py
   docstring rule (q) (:125–129): "the core imposes composition on no class";
   `check_agent_composition` only validates records that exist and must
   resolve to an agent-class wallet. Legal to mint ahead of 4.4.
8. **Scanner mechanics** (validate-openxwallet.py:1611–1644): `repo_scan`
   sweeps `*.y*ml`, skips packaged corpus by `examples` path segment, indexes
   any doc whose `kind` is in KIND_TO_SCHEMA into a repo-local context, and
   cross-validates in-tree. A kindless YAML is SKIPPED ENTIRELY - not indexed, not validated.
9. **Identifier grammars**: `$defs/identifier` =
   `^[A-Za-z0-9][A-Za-z0-9._:/-]*$` (no `@`). S2's authorized widening created
   `issuer_identifier` (with `@`) used by grant `issued_by` ALONE. Wallet
   `custody.declared_by` keeps the strict grammar → `Brett.Heap`.
10. **DID/key shapes**: record schema `did` pattern admits `did:key:...`;
    optional `public_key_multibase` pattern `^z[1-9A-HJ-NP-Za-km-z]+$` is
    base58btc multibase — what an ed25519 did:key carries. Packaged examples
    use `did:web:xforge.us:wallets:*`, but that form is honest only where
    something actually resolves; the operator ruled operator-minted did:key.
11. **Wallet schema requirements** (openxwallet-record.schema.yaml):
    required = schema_version, kind, wallet_id, holder(holder_id +
    holder_class ∈ person/practitioner/organisation/agent), key_reference(did
    + key_id), custody(model + registry_version), state ∈ active/suspended/
    revoked; additionalProperties false throughout; validator separately
    rejects PEM/private-JWK material.

## Rulings consumed (Brett Heap, 2026-08-24, in-session)

- Key identity: OPERATOR mints an ed25519 keypair and supplies only the public
  multibase; private half stays operator-side (vault), never enters any repo
  or agent session.
- `holder_class`: `agent`.
- Attestation content: drafted for confirmation rather than dictated.
- Placement: new `governance/review-authority/` namespace.

## Precedent conventions mirrored

specs/010-wallet-validator-ci and specs/012-wallet-issuer-anchor packet sets
(spec / plan / research / data-model / quickstart / tasks / checklist /
implementation-notes); example field spellings from
`contracts/openxwallet/examples/wallet-agent-creator.example.yaml`.
