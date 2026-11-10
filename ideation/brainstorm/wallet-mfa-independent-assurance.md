# Independent Verification and Agent Custody — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Derive assurance from verified factor independence and custody while preserving agent attribution.
Topics: wallet-mfa, custody, multifactor-authentication, workload-identity, openmfa
Repository context: opensoft/openxFactory with cross-product integration references
Captured: 2026-11-10

## Possible feats

- Define evidence classes for wallet possession, attested workload, human presence, and independent approval.
- Prove an agent cannot assign itself higher assurance.

## Evidence and custody

An agent presents its key plus approved workload evidence when required. A trusted runtime or independent attestor binds actual execution, key, and composition. A composition digest asserted by the agent is insufficient.

Two freely invocable keys in one process share a compromise boundary. A password and TOTP seed held by that process have a similar concern. Record the actual evidence and custody rather than inferring independent presence from the number of credentials.

The existing wallet registry distinguishes holder-readable, isolated freely invocable, and isolated per-use-authorized keys. Receipts preserve the presenting key's custody ceiling. An added factor cannot retroactively strengthen another key's custody declaration.

## Methods and separate approval

Human methods may include WebAuthn/passkeys, policy-accepted TOTP, and approved upstream MFA. WebAuthn checks include origin, relying-party ID, challenge, binding, and required presence/verification flags.

Workload evidence may use SPIFFE/SPIRE, platform attestation, or bound CI OIDC. Record its trust domain, runtime boundary, freshness, and measured identity semantics. These facts remain distinct from a human's approval.

For high-impact operations a distinct human or custodian approves the exact operation. The domain checks eligibility and separation of duties.

## External TOTP adapter

A separately authorized broker can generate a code for a dedicated enrolled QA account. The external provider verifies it. Enrollment, allowed methods, and policy remain with that provider and custodian. Keep reusable seeds behind scoped code-generation access where possible. Codes and seeds stay out of model transcripts and artifacts. The provider account is audited separately from the wallet actor.

## Recovery and audit

Enrollment, replacement, and recovery require authorized custody and invalidate dependent uses under explicit policy. Recovery must meet the operation's assurance requirements. Audit safe subject/actor references, methods, policy version, custody, digests, time, and outcomes. Exclude factor responses, passwords, private keys, session tokens, and sensitive payloads.

## Open decisions and relationships

Choose independent runtime attestation, accepted assurance profiles, authenticators, and recovery providers. [Boundaries](wallet-mfa-boundaries.md), [approval](wallet-mfa-delegation-approval.md), and [synthesis](wallet-mfa-synthesis-authentication.md) place this evidence in context.
