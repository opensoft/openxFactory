# openWallet and openMFA Integration Overview — Brainstorm

Status: brainstorm
Kind: reference
Summary: Propose reusable wallet authentication and verification with a codeXfactory pilot requiring separate human approval.
Topics: wallet-mfa, openwallet, openmfa, codexfactory, medxfactory, identity-brokering
Repository context: opensoft/openxFactory with cross-product integration references
Captured: 2026-11-10

## Possible feats

- Deliver neutral wallet authentication and verifier products with factory adapters.
- Qualify a first synthetic agent-authentication and separate-approval pilot.

## Motivation, goals, and intended delivery

Agents need attributable access under bounded delegation. Humans need independent consent for operations requiring approval. Applications need common authentication interfaces with domain-owned subjects and permissions.

Intended outcomes are fresh possession proof, trusted subject binding, truthful custody, exact-request approval, effective revocation, replay resistance, and clear actor attribution.

## Scope and status

This is non-normative design capture. The public Apache-2.0 openMFA triad is requested scaffolding. Runtime services, endpoints, schemas, tenant configuration, and deployment require governed implementation.

openWallet remains optional for reconstructing domain subjects. Its records refer to held keys. openMFA verifies additional evidence. The broker issues application tokens. Domain policy determines permitted actions. Public materials use synthetic examples. Deployment secrets and clinical or proprietary records remain in their owning custody.

## Document map

- [Authentication synthesis](wallet-mfa-synthesis-authentication.md)
  - [Boundaries](wallet-mfa-boundaries.md)
  - [Shared records](wallet-mfa-shared-contracts.md)
  - [Independent assurance](wallet-mfa-independent-assurance.md)
  - [Delegation and approval](wallet-mfa-delegation-approval.md)

## Repository ownership

| Repository | Responsibility |
| --- | --- |
| openxFactory | Cross-factory packet and authority integration seams |
| openWallet-spec | Neutral wallet proof and custody profile proposal |
| openMFA | Assembly root, pinned spec/code legs, Apache-2.0 licensing |
| openMFA-spec | Verifier design, future governance and service contracts |
| openMFA-code | Future service implementation and tests |
| openXwallet | Factory trust-anchor and approval-vocabulary binding |
| codeXfactory/codexFactory | Synthetic QA pilot and domain acceptance |
| medXfactory | Future clinical profile with independent subjects and approval policy |

## Related packets

- [Wallet profile](https://github.com/opensoft/openWallet-spec/blob/docs/wallet-mfa-design/ideation/brainstorm/wallet-mfa-overview.md)
- [Verifier service](https://github.com/opensoft/openMFA-spec/blob/docs/wallet-mfa-design/ideation/brainstorm/wallet-mfa-overview.md)
- [codeXfactory pilot](https://github.com/codeXfactory/codexFactory/blob/docs/wallet-mfa-design/ideation/brainstorm/wallet-mfa-overview.md)

Review-time links name documentation branches. Future contract consumers pin an assembly commit and its declared digests.

## medXfactory fit

A future profile could let an agent prepare a synthetic summary while a practitioner authenticates and approves the exact version before release. Patient identity, practitioner standing, consent, clinical scope, and approval remain domain-owned. Clinical execution is outside this pilot.

## First milestone and open decisions

The pilot authenticates an agent, performs a bounded read, submits a pending operation, obtains distinct human approval, and applies one idempotent synthetic effect. Negative, interruption, and cleanup evidence are required.

Decide canonical wire ownership, serialization, broker adapter, workload/composition attestation, custody, authenticators, and revocation availability before implementation.
