# Wallet, Identity, Verification, and Domain Boundaries — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Compose issuer-backed identity, wallet possession, additional verification, and domain authorization through explicit interfaces.
Topics: wallet-mfa, openwallet, openmfa, identity-brokering, authority
Repository context: opensoft/openxFactory with cross-product integration references
Captured: 2026-11-10

## Possible feats

- Define a shared authentication profile across wallet-enabled factories.
- Bind wallet proofs to independent domain subjects through trusted issuer attestations.

## Baseline and proposal

This packet captures Brett Heap's design discussion and documentation request. It is non-normative. Repository creation and licensing are authorized scaffold work. Protocol changes and runtime deployment require later governance.

openWallet already defines held keys, custody ceilings, possession proof, attenuated grants, distinct-holder constraints, and revocation at exercise. Its agent profile binds grants to declared composition. The runtime authentication profile and openMFA integration are proposed.

| Component | Responsibility | Boundary |
| --- | --- | --- |
| Identity issuer and domain registry | Attest the subject and its wallet/key binding | The relying party chooses trusted issuers and checks status |
| openWallet | Sign challenges and present key, attestation, and grant references | Private material stays in declared custody |
| openMFA | Verify authenticators and issue fresh, bound evidence | The consuming domain owns action permission |
| OIDC broker | Validate evidence and issue application tokens | Broker adapters require implementation and qualification |
| openXwallet | Bind neutral wallet contracts to factory trust anchors and approval vocabulary | Neutral protocol ownership remains upstream |
| medXfactory and codeXfactory | Resolve subjects and enforce grants, permissions, approvals, and separation of duties | A successful login creates no action approval |
| Credential broker | Mediate approved external-provider credentials | Provider account and wallet actor remain separately attributed |

## Identity and authority

A signature proves key control within its custody ceiling. Trusted issuer evidence connects it to a subject. A self-declared DID or composition hash alone establishes no issuer trust or measured runtime identity.

Patients, practitioners, organizations, and agents have independently resolvable domain subjects. Wallet replacement and recovery preserve those subjects. Account linking requires explicit proof of both identities and collision handling.

## Native and external authentication

Native applications consume wallet authentication through a broker and domain adapter. An external Entra login still follows Entra policy and enrolled methods. TOTP code generation is a separately scoped credential-broker adapter with the external provider performing verification.

## Ownership and alternatives

openWallet owns the neutral proof profile and existing grant/custody contracts. openMFA owns verification and receipt contracts. The shared envelope requires coordinated governance with one canonical owner per field. openxFactory owns this integration packet and factory seams. Each domain owns its pilot.

Keycloak is the proposed first broker adapter. Another OIDC issuer or direct verifier integration remain alternatives to evaluate.

## Relationships

[Shared contracts](wallet-mfa-shared-contracts.md), [assurance](wallet-mfa-independent-assurance.md), and [synthesis](wallet-mfa-synthesis-authentication.md) describe the seams.
