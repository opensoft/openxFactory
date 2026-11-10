# Shared Wallet Authentication Contracts — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Bind versioned challenges, wallet proofs, verification receipts, and delegation references to their requester, audience, and operation.
Topics: wallet-mfa, authentication-contracts, openwallet, openmfa, replay-protection
Repository context: opensoft/openxFactory with cross-product integration references
Captured: 2026-11-10

## Possible feats

- Publish one versioned interoperability profile with cross-implementation test vectors.
- Qualify atomic challenge consumption and request-bound approval.

## Candidate record semantics

These are proposed fields rather than published schemas or endpoints.

| Record | Proposed content |
| --- | --- |
| Challenge | Version, ID, verifier issuer, tenant, audience, subject/session binding, accepted methods, required assurance, nonce, issued time, expiry, optional operation digest |
| Wallet proof | Challenge digest, wallet/key references, signature, issuer attestations, presenting custody, grant chain, agent composition and attestation references |
| Verification receipt | Version, ID, trusted verifier, authenticated subject and actor context, challenge digest, audience, verification time, expiry, verified methods/custody facts, policy version, signer |
| Delegation reference | Delegating subject, agent actor, parent grant/chain, audience, tenant, scope, expiry, revocation reference |

Signatures cover every security-relevant field. The verifier derives assurance from validated evidence. Client-supplied assurance is a claim to evaluate.

## Binding and lifecycle

Authenticate the relying party before creating its challenge. The wallet authenticates the verifier before signing. Verify signature, key membership and state, trusted subject binding, allowed algorithms, custody evidence, and current authority.

Challenges bind the requester or server-side session, audience, tenant, nonce, expiry, and applicable request digest. Receipts are accepted only from a configured issuer for the exact challenge and audience.

Proposed states are issued, pending, verified, consumed, expired, denied, and cancelled. Verification and consumption use atomic transitions. Identical idempotent retries have one stable result. A changed digest under the same key is refused.

Check key, subject, parent-grant, and composition revocation at exercise. Short token expiry alone cannot implement immediate revocation. Specify online checks or synchronously enforced invalidation and failure behavior.

## Token mapping and ownership

The OIDC broker can express human authentication through auth_time, amr, and acr and issue audience-scoped API access tokens. Delegation preserves actor and subject. Select DPoP or mTLS where possession-bound tokens are supported. Domain grants continue to govern authority.

openWallet and openMFA need one jointly governed envelope profile with a declared canonical owner for each definition, coordinated versions, and compatibility vectors. Serialization, canonicalization, algorithm allowlists, discovery, and status lookup remain open implementation decisions.

## Relationships

[Boundaries](wallet-mfa-boundaries.md) assigns owners. [Delegation](wallet-mfa-delegation-approval.md) adds exact-operation consent. [Synthesis](wallet-mfa-synthesis-authentication.md) connects the records.

## Standards references

- [OIDC Core](https://openid.net/specs/openid-connect-core-1_0.html)
- [Token exchange, RFC 8693](https://datatracker.ietf.org/doc/html/rfc8693)
- [DPoP, RFC 9449](https://datatracker.ietf.org/doc/html/rfc9449)
- [Step-up authentication, RFC 9470](https://datatracker.ietf.org/doc/html/rfc9470)
