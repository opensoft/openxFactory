# Synthesis: Wallet Authentication and Bound Approval — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Combine wallet proof, additional verification, and grant checks into an auditable authentication-to-execution flow.
Topics: wallet-mfa, identity-brokering, authentication-contracts, delegation, synthesis
Repository context: opensoft/openxFactory with cross-product integration references
Captured: 2026-11-10

## Possible feats

- Qualify one broker adapter and one independent human-approval flow.
- Publish shared replay and revocation refusal vectors.

## Members and their joints

Members are [boundaries](wallet-mfa-boundaries.md), [shared contracts](wallet-mfa-shared-contracts.md), [assurance](wallet-mfa-independent-assurance.md), and [delegation](wallet-mfa-delegation-approval.md).

### Subject to authentication

The registry resolves the subject and trusted issuer binding. The broker challenges the wallet and checks declared keys and attestations. openMFA verifies additional evidence for the same audience and transaction.

### Authentication to permission

The broker issues an application-scoped access token. The application validates possession evidence, current grants, and domain permission. A step-up challenge requests required assurance or freshness. Broker support needs implementation and live qualification.

### Approval to execution

The distinct human authenticates in a separate session and approves an immutable request. The application checks eligibility and distinctness, consumes the approval once, and rechecks current authority before the effect.

## Sequence

    Agent wallet -> Broker: challenge signature and attestation references
    Broker -> openMFA: additional verification when required
    openMFA -> Broker: signed bound receipt
    Broker -> Agent: short-lived application token
    Agent -> Factory: exact operation and grant references
    Factory -> Human: approval request bound to digest
    Human -> openMFA/Broker: independent authentication
    Human -> Factory: approval or denial of the exact digest
    Factory -> Target: one idempotent effect after current authority checks

## Failures and emergent behavior

Untrusted issuer, invalid proof, stale factor, composition drift, wrong audience, denied approval, and unavailable required revocation checks each refuse explicitly. Cancellation closes the challenge and approval window.

The composition permits shared authentication across applications while domain subjects and action policies stay local. External credential brokering can coexist with native wallet authentication.

## Open questions and navigation

Choose adapter, custody, independent attestation, and revocation storage during implementation governance. The [overview](wallet-mfa-overview.md) maps all repositories and packets.
